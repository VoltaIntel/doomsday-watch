"""Polymarket ingester — poll public Gamma API, cache to data/polymarket_cache.json.

Runs as a standalone script or as a library. Never places trades, never
authenticates — pure read.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _ROOT / "scripts"
sys.path.insert(0, str(_SCRIPTS))
from log_setup import get_logger  # type: ignore  # noqa: E402

log = get_logger()

GAMMA_MARKETS_URL = "https://gamma-api.polymarket.com/markets"
CACHE_PATH = _ROOT / "data" / "polymarket_cache.json"
DEFAULT_LIMIT = 500
REQUEST_TIMEOUT = 20.0
DEFAULT_MAX_CACHE_AGE_HOURS = 12.0


def _parse_utc(ts: Any) -> Optional[datetime]:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def cache_age_hours(cache: Dict[str, Any], now: Optional[datetime] = None) -> Optional[float]:
    """Return cache age in hours, or None when fetched_at is missing/invalid."""
    fetched = _parse_utc(cache.get("fetched_at") if isinstance(cache, dict) else None)
    if fetched is None:
        return None
    now_dt = now or datetime.now(timezone.utc)
    if now_dt.tzinfo is None:
        now_dt = now_dt.replace(tzinfo=timezone.utc)
    return max(0.0, (now_dt.astimezone(timezone.utc) - fetched).total_seconds() / 3600.0)


def cache_is_fresh(cache: Dict[str, Any], max_age_hours: float = DEFAULT_MAX_CACHE_AGE_HOURS) -> bool:
    """True only when the cache has markets and fetched_at is within max_age_hours."""
    if not isinstance(cache, dict) or not cache.get("markets"):
        return False
    age = cache_age_hours(cache)
    return age is not None and age <= float(max_age_hours)


def _fetch_page(offset: int, limit: int) -> List[Dict[str, Any]]:
    qs = f"?limit={limit}&offset={offset}&active=true&closed=false"
    url = GAMMA_MARKETS_URL + qs
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "nuke-watch/1.0 (+github.com/openclaw)"},
    )
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        return payload["data"]
    return []


def fetch_active_markets(max_pages: int = 4, per_page: int = DEFAULT_LIMIT) -> List[Dict[str, Any]]:
    """Pull active non-closed markets. Returns raw market dicts."""
    out: List[Dict[str, Any]] = []
    for page in range(max_pages):
        try:
            page_rows = _fetch_page(offset=page * per_page, limit=per_page)
        except urllib.error.URLError as e:
            log.warning("polymarket_fetch_failed", extra={"page": page, "err": repr(e)})
            break
        except Exception as e:  # pragma: no cover — defensive
            log.error("polymarket_unexpected_error", extra={"err": repr(e)}, exc_info=True)
            break
        if not page_rows:
            break
        out.extend(page_rows)
        if len(page_rows) < per_page:
            break
    return out


def _safe_float(v: Any) -> Optional[float]:
    try:
        if v in (None, ""):
            return None
        return float(v)
    except (TypeError, ValueError):
        return None


def _pick_yes_price(m: Dict[str, Any]) -> Optional[float]:
    """Extract the YES-side price from a Gamma market dict (robust to schema drift)."""
    # Direct fields: outcomePrices can be a list of strings or a JSON string.
    op = m.get("outcomePrices")
    prices: List[float] = []
    if isinstance(op, str):
        try:
            op = json.loads(op)
        except Exception:
            op = []
    if isinstance(op, list):
        for p in op:
            fp = _safe_float(p)
            if fp is not None:
                prices.append(fp)
    if prices:
        # YES is typically the first outcome in binary markets.
        return prices[0]
    for key in ("lastTradePrice", "bestAsk", "bestBid"):
        fp = _safe_float(m.get(key))
        if fp is not None:
            return fp
    return None


def _pick_volume_24h(m: Dict[str, Any]) -> Optional[float]:
    for key in ("volume24hr", "volume24Hr", "volume24h", "volumeNum"):
        fp = _safe_float(m.get(key))
        if fp is not None:
            return fp
    return None


def summarise_market(m: Dict[str, Any]) -> Dict[str, Any]:
    """Normalise a raw market dict to the minimal fields DW needs."""
    return {
        "slug": m.get("slug") or m.get("conditionId") or "",
        "question": m.get("question") or m.get("title") or "",
        "end_date": m.get("endDate") or m.get("end_date") or m.get("endDateIso"),
        "yes_price": _pick_yes_price(m),
        "volume_24h": _pick_volume_24h(m),
        "liquidity": _safe_float(m.get("liquidity")),
        "closed": bool(m.get("closed")),
        "active": bool(m.get("active", True)),
        "updated_at": m.get("updatedAt") or m.get("updated_at"),
    }


def build_cache(slugs: Optional[Iterable[str]] = None) -> Dict[str, Any]:
    """Fetch markets and return a cache dict. If slugs provided, only keep those."""
    markets = fetch_active_markets()
    wanted = set(slugs) if slugs else None
    filtered = []
    for m in markets:
        slug = m.get("slug") or ""
        if wanted is not None and slug not in wanted:
            continue
        filtered.append(summarise_market(m))
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    return {
        "fetched_at": now,
        "source": "gamma-api.polymarket.com",
        "markets": {row["slug"]: row for row in filtered if row["slug"]},
    }


def load_cache() -> Dict[str, Any]:
    if not CACHE_PATH.exists():
        return {"fetched_at": None, "markets": {}}
    try:
        with open(CACHE_PATH) as f:
            return json.load(f)
    except Exception as e:
        log.warning("polymarket_cache_read_error", extra={"err": repr(e)})
        return {"fetched_at": None, "markets": {}}


def save_cache(cache: Dict[str, Any]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2, sort_keys=True)


def refresh_cache(slugs: Optional[Iterable[str]] = None, offline_ok: bool = True) -> Dict[str, Any]:
    """Fetch fresh cache; on network failure fall back to existing cache."""
    try:
        cache = build_cache(slugs=slugs)
        if cache["markets"]:
            save_cache(cache)
            log.info(
                "polymarket_cache_refreshed",
                extra={"count": len(cache["markets"]), "fetched_at": cache["fetched_at"]},
            )
            return cache
        log.warning("polymarket_empty_payload")
    except Exception as e:
        log.warning("polymarket_refresh_failed", extra={"err": repr(e)}, exc_info=True)
    if offline_ok:
        cache = load_cache()
        log.info(
            "polymarket_using_stale_cache",
            extra={"fetched_at": cache.get("fetched_at")},
        )
        return cache
    raise RuntimeError("polymarket refresh failed and offline_ok=False")


def refresh_cache_if_stale(
    slugs: Optional[Iterable[str]] = None,
    max_age_hours: float = DEFAULT_MAX_CACHE_AGE_HOURS,
    offline_ok: bool = True,
) -> Dict[str, Any]:
    """Refresh only when the local cache is stale/missing.

    This keeps normal pipeline runs fast while preventing the dashboard from
    silently carrying multi-day-old Polymarket data.
    """
    cache = load_cache()
    if cache_is_fresh(cache, max_age_hours=max_age_hours):
        log.info(
            "polymarket_cache_fresh",
            extra={
                "fetched_at": cache.get("fetched_at"),
                "age_hours": round(cache_age_hours(cache) or 0.0, 2),
            },
        )
        return cache
    return refresh_cache(slugs=slugs, offline_ok=offline_ok)


if __name__ == "__main__":
    # CLI: refresh cache in-place.
    c = refresh_cache()
    print(json.dumps({"fetched_at": c.get("fetched_at"), "markets": len(c.get("markets", {}))}))
