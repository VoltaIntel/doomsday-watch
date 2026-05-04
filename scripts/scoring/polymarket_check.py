"""Polymarket cross-check scoring.

Compares DoomsdayWatch probabilities against Polymarket implied probabilities,
flags divergence, and writes per-tracker comparisons to state for dashboard use.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _ROOT / "scripts"
sys.path.insert(0, str(_SCRIPTS))
from log_setup import get_logger  # type: ignore  # noqa: E402

log = get_logger()

CACHE_PATH = _ROOT / "data" / "polymarket_cache.json"
MAPPING_PATH = _ROOT / "data" / "polymarket_mapping.json"
STATE_PATH = _ROOT / "data" / "current_state.json"
DIVERGENCE_LOG = _ROOT / "data" / "polymarket_divergence.jsonl"

MIN_VOLUME_24H = 100_000.0
DRIFT_PP = 5.0
DIVERGENCE_PP = 15.0
SANITY_FLOOR_PM = 0.02
SANITY_FLOOR_DW = 30.0


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        log.warning("pm_json_read_error", extra={"path": str(path), "err": repr(e)})
        return fallback


def hazard_translate(p_horizon: float, horizon_days: float, target_days: float = 1.0) -> float:
    p = max(0.0, min(1.0, float(p_horizon)))
    h = max(1e-6, float(horizon_days))
    if p >= 1.0:
        return 1.0
    return 1.0 - (1.0 - p) ** (float(target_days) / h)


def _tracker_implied(
    tracker_id: str,
    mapping_entries: List[Dict[str, Any]],
    markets: Dict[str, Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    used: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    liquidity_warn = False
    total_volume = 0.0

    for entry in mapping_entries:
        slug = entry.get("slug", "")
        market = markets.get(slug)
        if not market or market.get("yes_price") is None:
            skipped.append({"slug": slug, "reason": "market_missing"})
            continue

        yes_price = float(market["yes_price"])
        yes_price = max(0.0, min(1.0, yes_price))
        if entry.get("invert"):
            contrib_raw = 1.0 - yes_price
        else:
            contrib_raw = yes_price

        volume = market.get("volume_24h") or 0.0
        if volume < MIN_VOLUME_24H:
            liquidity_warn = True

        used.append({
            "slug": slug,
            "weight": float(entry.get("weight", 1.0)),
            "horizon_days": float(entry.get("horizon_days", 365)),
            "invert": bool(entry.get("invert", False)),
            "yes_price": yes_price,
            "contribution": contrib_raw,
            "volume_24h": volume,
            "question": market.get("question", ""),
        })
        total_volume += float(volume)

    if not used:
        return None

    total_weight = sum(u["weight"] for u in used) or 1.0
    implied_raw = sum(u["contribution"] * u["weight"] for u in used) / total_weight
    horizon_avg = sum(u["horizon_days"] * u["weight"] for u in used) / total_weight
    pm_24h = hazard_translate(implied_raw, horizon_avg, target_days=1.0) * 100.0

    return {
        "tracker_id": tracker_id,
        "implied_raw": round(implied_raw, 6),
        "implied_raw_pct": round(implied_raw * 100.0, 2),
        "implied_24h_pct": round(pm_24h, 3),
        "horizon_days_avg": round(horizon_avg, 1),
        "used_slugs": [u["slug"] for u in used],
        "skipped_slugs": skipped,
        "markets": used,
        "liquidity_warn": liquidity_warn,
        "total_volume_24h": round(total_volume, 2),
    }


def _classify_divergence(
    dw_prob_pct: float, pm_24h_pct: float, tracker_raw_pm: float
) -> Dict[str, Any]:
    delta_pp = float(dw_prob_pct) - float(pm_24h_pct)
    abs_pp = abs(delta_pp)
    if tracker_raw_pm < SANITY_FLOOR_PM and dw_prob_pct > SANITY_FLOOR_DW:
        flag = "critical"
        color = "red"
    elif abs_pp >= DIVERGENCE_PP:
        flag = "divergence"
        color = "red"
    elif abs_pp >= DRIFT_PP:
        flag = "drift"
        color = "yellow"
    else:
        flag = "aligned"
        color = "green"
    arrow = "="
    if delta_pp > 0:
        arrow = "up"
    elif delta_pp < 0:
        arrow = "down"
    return {
        "delta_pp": round(delta_pp, 2),
        "abs_delta_pp": round(abs_pp, 2),
        "flag": flag,
        "color": color,
        "arrow": arrow,
    }


def check_all(
    cache: Optional[Dict[str, Any]] = None,
    mapping: Optional[Dict[str, Any]] = None,
    state: Optional[Dict[str, Any]] = None,
    append_log: bool = True,
) -> Dict[str, Any]:
    if cache is None:
        cache = _load_json(CACHE_PATH, {"markets": {}, "fetched_at": None})
    if mapping is None:
        mapping = _load_json(MAPPING_PATH, {})
    if state is None:
        state = _load_json(STATE_PATH, {"trackers": {}})

    markets = cache.get("markets", {}) if isinstance(cache, dict) else {}
    now_dt = datetime.now(timezone.utc)
    now_iso = now_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    fetched_at = cache.get("fetched_at") if isinstance(cache, dict) else None
    cache_age_hours = None
    if fetched_at:
        try:
            fetched_dt = datetime.fromisoformat(str(fetched_at).replace("Z", "+00:00"))
            cache_age_hours = round(max(0.0, (now_dt - fetched_dt).total_seconds() / 3600.0), 1)
        except Exception:
            cache_age_hours = None
    cache_stale = cache_age_hours is None or cache_age_hours > 12.0

    comparisons: Dict[str, Any] = {}
    banner = {
        "any_divergence": False,
        "any_critical": False,
        "worst_abs_delta_pp": 0.0,
        "worst_tracker": None,
    }

    for tracker_id, entries in mapping.items():
        if tracker_id.startswith("_"):
            continue
        if not isinstance(entries, list) or not entries:
            continue

        implied = _tracker_implied(tracker_id, entries, markets)
        if implied is None:
            comparisons[tracker_id] = {
                "tracker_id": tracker_id,
                "status": "no_market",
                "mapped_slugs": [e.get("slug") for e in entries],
            }
            continue

        tracker_state = state.get("trackers", {}).get(tracker_id, {}) if isinstance(state, dict) else {}
        dw_prob = tracker_state.get(
            "current_probability_with_coupling",
            tracker_state.get("current_probability"),
        )
        if dw_prob is None:
            zone = state.get("zones", {}).get(tracker_id, {}) if isinstance(state, dict) else {}
            dw_prob = zone.get("current_prob", 0)
        try:
            dw_prob = float(dw_prob)
        except (TypeError, ValueError):
            dw_prob = 0.0

        div = _classify_divergence(dw_prob, implied["implied_24h_pct"], implied["implied_raw"])

        entry_out = {
            "tracker_id": tracker_id,
            "status": "ok",
            "dw_prob_pct": round(dw_prob, 2),
            "pm_implied_raw_pct": implied["implied_raw_pct"],
            "pm_implied_24h_pct": implied["implied_24h_pct"],
            "horizon_days_avg": implied["horizon_days_avg"],
            "used_slugs": implied["used_slugs"],
            "total_volume_24h": implied["total_volume_24h"],
            "liquidity_warn": implied["liquidity_warn"],
            "markets": implied["markets"],
            **div,
        }
        comparisons[tracker_id] = entry_out

        if div["flag"] in ("divergence", "critical"):
            banner["any_divergence"] = True
        if div["flag"] == "critical":
            banner["any_critical"] = True
        if div["abs_delta_pp"] > banner["worst_abs_delta_pp"]:
            banner["worst_abs_delta_pp"] = div["abs_delta_pp"]
            banner["worst_tracker"] = tracker_id

    result = {
        "generated_at": now_iso,
        "fetched_at": fetched_at,
        "age_hours": cache_age_hours,
        "stale": cache_stale,
        "stale_after_hours": 12,
        "comparisons": comparisons,
        "banner": banner,
    }

    if append_log:
        _append_divergence_log(result)

    return result


def _append_divergence_log(result: Dict[str, Any]) -> None:
    try:
        DIVERGENCE_LOG.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        ts = result.get("generated_at")
        for tid, c in result.get("comparisons", {}).items():
            if c.get("flag") in ("divergence", "critical"):
                lines.append(json.dumps({
                    "ts": ts,
                    "tracker_id": tid,
                    "flag": c.get("flag"),
                    "delta_pp": c.get("delta_pp"),
                    "dw_prob_pct": c.get("dw_prob_pct"),
                    "pm_implied_24h_pct": c.get("pm_implied_24h_pct"),
                    "pm_implied_raw_pct": c.get("pm_implied_raw_pct"),
                    "liquidity_warn": c.get("liquidity_warn"),
                }))
        if lines:
            with open(DIVERGENCE_LOG, "a") as f:
                f.write("\n".join(lines) + "\n")
    except Exception as e:
        log.warning("pm_divergence_log_error", extra={"err": repr(e)})


if __name__ == "__main__":
    out = check_all()
    print(json.dumps({
        "generated_at": out["generated_at"],
        "banner": out["banner"],
        "trackers_checked": list(out["comparisons"].keys()),
    }, indent=2))
