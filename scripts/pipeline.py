#!/usr/bin/env python3
# Nuke-Watch Pipeline — refactored from deploy.sh inline Python
# Functions: process_signals(), calculate_probabilities(), apply_coupling(),
#            generate_predictions(), evaluate_predictions(), rebuild_dashboard()
#
# Changes from original:
# 1. Extracted into clean functions
# 2. Signal dedup with TTL: update last_confirmed on re-detection, keep activated_at stable
# 3. Prune fully-decayed signals from signal_timeline during deploy

import html as html_lib
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Make sibling modules importable whether pipeline.py is run as a script
# (python scripts/pipeline.py) or as a package (python -m scripts.pipeline).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from signals import (  # noqa: E402
    calc_severity,
    calc_confidence,
    apply_credibility_weight,
    get_half_life,
    apply_temporal_decay,
    normalize_trend,
    classify_source_category,
    classify_source_credibility as _signals_classify_credibility,
    classify_source as _signals_classify_source,
    is_deescalation_signal as _signals_is_deescalation,
    find_matching_signals as _signals_find_matching,
    get_timeline_details as _signals_get_timeline,
    confirm_signal as _signals_confirm_signal,
    build_signal_data as _signals_build_signal_data,
    build_raw_news_fallback,
    normalize_news_item,
    enrich_news,
    merge_news_signals_into_state,
    extract_signals_from_notes,
)
from probabilities import (  # noqa: E402
    classify_zone as _classify_zone_cfg,
    calculate_global_probability,
    auto_calculate_probabilities,
    apply_coupling,
)
from predictions import (  # noqa: E402
    dedupe_predictions,
    evaluate_all_predictions,
    generate_predictions as _module_generate_predictions,
    generate_forecast_ladder,
    compute_horizon_calibration,
    summarize_forecast_resolution_ledger,
    build_forecast_review_queue,
    summarize_forecast_review_queue,
    compute_eval_stats,
    NARRATIVE_TO_EVAL,
)
from dashboard_builder import (  # noqa: E402
    build_tracker_cards as _module_build_tracker_cards,
    build_dashboard as _module_build_dashboard,
    generate_narrative as _module_generate_narrative,
    _generate_chart_svg as _module_generate_chart_svg,
)
from log_setup import get_logger  # noqa: E402

log = get_logger()


try:
    from models import validate_state as _pyd_validate_state, validate_config as _pyd_validate_config  # noqa: E402
    from pydantic import ValidationError as _PydValidationError  # noqa: E402
except Exception as _e:
    # Pydantic is optional; fall back to no-op validators so pipeline still runs.
    _pyd_validate_state = None
    _pyd_validate_config = None
    _PydValidationError = Exception
    print(f"[pipeline] Pydantic unavailable, skipping strict validation: {_e}")


def validate_state(state):
    """Strict validation of current_state.json.

    Returns (is_valid, errors). When pydantic is installed, validation errors
    abort the pipeline run — the writer contract is not optional.
    """
    if _pyd_validate_state is None:
        # Legacy fallback check — only verifies top-level structure.
        errors = []
        required_top = ["last_updated", "trackers"]
        for field in required_top:
            if field not in state:
                errors.append(f"Missing required top-level field: {field}")
        if not isinstance(state.get("trackers"), dict):
            errors.append("'trackers' must be a dict")
        if errors:
            print(f"[pipeline] State validation FAILED: {'; '.join(errors)}")
            return False, errors
        return True, []
    try:
        _pyd_validate_state(state)
        return True, []
    except _PydValidationError as e:
        msgs = [f"{err['loc']}: {err['msg']}" for err in e.errors()]
        print("[pipeline] State validation FAILED:")
        for m in msgs:
            print(f"  - {m}")
        return False, msgs


_PUBLIC_SOURCE_CAVEAT = (
    "Source mix: official releases, reputable public reporting, public-news "
    "headline indexes, market data, and energy feeds. Upstream source coverage "
    "was degraded in this run, so the assessment uses corroborated fallback "
    "sources and treats single-source claims as watch items until confirmed."
)


_PUBLIC_WEB_SEARCH_SUCCESS_CAVEAT = (
    "Source mix: primary web search succeeded this run and was corroborated "
    "with official releases, reputable public reporting, public-news headline "
    "indexes, market data, and energy feeds. Sparse or stale results are not "
    "treated as calm, and single-source claims remain watch items until "
    "confirmed."
)


def _web_search_succeeded(meta: dict) -> bool:
    """True when this run's internal status says primary web search worked.

    Reads `_meta.source_fallback_detail.web_search_status`, which is internal
    and may carry provider/error detail — so it is only ever inspected here,
    never echoed into the published caveat.
    """
    detail = meta.get("source_fallback_detail")
    if not isinstance(detail, dict):
        return False
    status = detail.get("web_search_status")
    if not isinstance(status, str):
        return False
    return status.strip().lower().startswith("successful")


def _public_source_label(raw: str) -> str:
    """Return a public-safe source caveat, without vendor/API error details."""
    text = (raw or "").strip().lower()
    if not text:
        return (
            "Source mix: official releases, reputable public reporting, market "
            "data, and energy feeds. Single-source claims are treated as watch "
            "items until confirmed."
        )
    if any(token in text for token in (
        "http", "tavily", "web_search", "432", "401", "403", "404",
        "error", "failed", "blocked", "forbidden", "fallback", "rss",
    )):
        return _PUBLIC_SOURCE_CAVEAT
    return raw.strip()


def sanitize_public_meta(state):
    """Scrub public dashboard metadata of internal provider/error strings.

    `data/current_state.json` is force-published with GitHub Pages, so anything
    stored here is viewer-facing. Keep operational error detail in vault/session
    logs, not in the public state payload.
    """
    meta = state.get("_meta")
    if not isinstance(meta, dict):
        return state

    if _web_search_succeeded(meta):
        # Primary web search worked, so don't publish the degraded-run caveat
        # (which is sticky in the state file from any earlier failed run).
        meta["source_limitation"] = _PUBLIC_WEB_SEARCH_SUCCESS_CAVEAT
        meta["search_engine"] = "web_search_plus_public_safe_multi_source_fallback"
    else:
        raw = " ".join(str(meta.get(k, "")) for k in ("source_limitation", "search_engine"))
        public_label = _public_source_label(raw)
        meta["source_limitation"] = public_label
        meta["search_engine"] = "public_safe_multi_source_fallback" if raw.strip() else "public_safe_multi_source"

    probe = meta.get("official_source_probe")
    if isinstance(probe, dict):
        public_probe = {}
        for key, val in probe.items():
            if isinstance(val, dict):
                public_probe[key] = {
                    "ok": bool(val.get("ok")),
                    "source": val.get("title") or val.get("url") or key,
                }
            else:
                public_probe[key] = {"ok": bool(val), "source": key}
        meta["official_source_probe"] = public_probe
    return state


ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

with open("data/current_state.json") as f:
    state = json.load(f)

# Validate state before processing. Hard fail when pydantic flags a bad writer.
_valid, _errors = validate_state(state)
if not _valid:
    if _pyd_validate_state is not None:
        raise SystemExit(
            f"[pipeline] ABORT: state validation failed ({len(_errors)} errors). "
            "Fix data/current_state.json before re-running."
        )
    # Legacy fallback: warn only.
    print(f"[pipeline] WARNING: State validation issues: {_errors}")

# Sanity-guard the Doomsday Clock: the published value has been <= 2 minutes
# for years (2026: 85 seconds ≈ 1.4 min). Any value above 10 is almost
# certainly a cron-writer bug — cap it and warn so the dashboard stops
# publishing impossible numbers.
_ddc = state.get("doomsday_clock_minutes")
if isinstance(_ddc, (int, float)) and _ddc > 10:
    print(f"[pipeline] WARNING: doomsday_clock_minutes={_ddc} is implausible; capping at 2.0")
    state["doomsday_clock_minutes"] = 2.0

with open("data/tracker_config.json") as f:
    cfg = json.load(f)

# Validate config too — a malformed tracker_config is just as fatal as
# bad state.
if _pyd_validate_config is not None:
    try:
        _pyd_validate_config(cfg)
    except _PydValidationError as _cfg_err:
        _errs = [f"{e['loc']}: {e['msg']}" for e in _cfg_err.errors()]
        raise SystemExit(
            "[pipeline] ABORT: tracker_config.json validation failed:\n  - "
            + "\n  - ".join(_errs)
        )

# Load energy prices (fetched by fetch_oil_prices.py)
try:
    with open("data/energy_prices.json") as f:
        energy_data = json.load(f)
except Exception as e:
    print(f"[pipeline] Error loading energy_prices.json: {e}")
    energy_data = {"current": {}, "history": [], "baselines": {}, "changes": {}}

with open("dashboard.html") as f:
    html = f.read()

# Build signal weight lookup: {(tracker_id, signal_name): weight}
signal_weights = {}
for tid, tcfg in cfg.get("trackers", {}).items():
    for sname, scfg in tcfg.get("signals", {}).items():
        signal_weights[(tid, sname)] = scfg.get("weight", 0)

# Load signal timeline for chronological sorting
try:
    with open("data/signal_timeline.json") as f:
        timeline = json.load(f)
except Exception as e:
    print(f"[pipeline] Error loading signal_timeline.json: {e}")
    timeline = {"signals": {}}

now_dt = datetime.now(timezone.utc)
now_iso = now_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
state["last_updated"] = now_iso

# --- Load credibility config and define functions BEFORE processing ---
with open("data/source_credibility.json") as f:
    credibility_cfg = json.load(f)

SOURCE_CREDIBILITY = credibility_cfg.get("sources", {})
TIER_WEIGHTS = {k: v["weight"] for k, v in credibility_cfg.get("tiers", {}).items()}
TIER_LABELS = {k: v["label"] for k, v in credibility_cfg.get("tiers", {}).items()}

# ── Thin wrappers around signals.py + dashboard_builder.py + predictions.py ──
# The canonical implementations live in those modules. These wrappers bind the
# module-level config (SOURCE_CREDIBILITY, cfg, signal_weights, timeline, etc.)
# so existing call sites don't need to change.

def classify_source_credibility(source_str):
    return _signals_classify_credibility(source_str, SOURCE_CREDIBILITY, TIER_WEIGHTS, TIER_LABELS)

def classify_source(source_str):
    return _signals_classify_source(source_str, SOURCE_CREDIBILITY, TIER_WEIGHTS, TIER_LABELS)

def is_deescalation_signal(text):
    return _signals_is_deescalation(text, credibility_cfg)

def find_matching_signals(text, tid, source_tier="5_unverified"):
    return _signals_find_matching(text, tid, cfg, signal_weights, credibility_cfg, source_tier)

def get_timeline_details(timeline_key, create=False):
    return _signals_get_timeline(timeline_key, timeline, now_iso, create=create)

def confirm_signal(tid, signal_name, confirmed_at=None):
    _signals_confirm_signal(tid, signal_name, timeline, now_iso, confirmed_at=confirmed_at)

def build_signal_data(tid):
    return _signals_build_signal_data(tid, state, signal_weights, timeline, now_dt, now_iso)

def build_tracker_cards():
    return _module_build_tracker_cards(state, cfg, tn, signal_weights, timeline, now_dt, now_iso)

# dedupe_predictions is imported directly from predictions.py
# --- End functions ---

# Build tracker labels
tn = [
    ("iran_nuclear", "IRAN NUCLEAR", "🇮🇷"),
    ("iran_conventional", "IRAN WAR", "⚔️"),
    ("israel_lebanon", "ISRAEL-LEBANON", "🇱🇧"),
    ("turkey", "TURKEY-NATO", "🇹🇷"),
    ("india", "INDIA-PAKISTAN", "🇮🇳"),
    ("pakistan_afghanistan", "PAKISTAN-AFGHANISTAN", "🇵🇰"),
    ("russia_ukraine", "RUSSIA-UKRAINE", "🇺🇦"),
    ("russia", "RUSSIA-NATO", "🇷🇺"),
    ("china", "CHINA-TAIWAN", "🇨🇳"),
    ("north_korea", "DPRK", "🇰🇵"),
]

# Auto-detect any extra trackers in state that aren't in our list
known = set(t[0] for t in tn)
for k in state.get("trackers", {}).keys():
    if k not in known:
        tn.append((k, k.upper().replace("_", " "), "🌍"))

# BRIDGE: When latest_news is absent (zones schema written by cron),
# synthesise news from zone notes + signals so the feed is populated.
# Normalise legacy title/summary/tracker records to the canonical schema and
# publish those copies: the browser renders STATE.latest_news straight from
# data/current_state.json, so enriching only the embedded payload is not enough.
raw_news = [
    normalize_news_item(n)
    for n in (state.get("latest_news") or build_raw_news_fallback(state))
]
state["latest_news"] = raw_news

# Enrich news with credibility scoring + matched signals (deduplicated across
# items so duplicate sources don't double-count).
news_js = enrich_news(
    raw_news,
    classify_credibility=classify_source_credibility,
    classify_category=classify_source_category,
    find_matching_signals_fn=find_matching_signals,
    calc_confidence_fn=calc_confidence,
    calc_severity_fn=calc_severity,
)

# Merge news-found signals with agent-set signals; decay-expired signals drop.
merge_news_signals_into_state(
    news_js, state, signal_weights,
    apply_temporal_decay_fn=apply_temporal_decay,
    get_timeline_details_fn=get_timeline_details,
    confirm_signal_fn=confirm_signal,
    now_iso=now_iso,
)

state["signal_timestamps"] = {
    key: (entry.get("activated_at") if isinstance(entry, dict) else entry)
    for key, entry in timeline.get("signals", {}).items()
}

# Fallback: extract named signals from zone notes when cron writer only
# populates notes (not active_signals directly).
extract_signals_from_notes(state, signal_weights)

trackers_js = build_tracker_cards()

# Auto-calculate per-tracker probabilities from signals + base rate + decay.
# Falls back to zone's authoritative current_prob when no real signals exist.
any_auto_calculated = auto_calculate_probabilities(trackers_js, state, cfg, now_dt)
if any_auto_calculated:
    print("Auto-calculated probabilities from signals:")
    for t in trackers_js:
        base_rate = cfg.get("trackers", {}).get(t["id"], {}).get("base_rate", 0)
        print(f"  {t['name']}: base={base_rate} = {t['prob']}%")
else:
    print("All trackers using zone fallback (cron job set authoritative probabilities)")

# Recalculate zones from config thresholds (before coupling)
zone_thresholds = cfg.get("scoring", {}).get("zones", {})

def classify_zone(p):
    return _classify_zone_cfg(p, zone_thresholds)


def _iso_age_hours(ts):
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return round(max(0.0, (now_dt - dt).total_seconds() / 3600.0), 1)
    except Exception:
        return None


def _build_watch_triggers(tid, limit=3):
    """Expose the most important up/down triggers for the dashboard."""
    sigs = cfg.get("trackers", {}).get(tid, {}).get("signals", {})
    rows = []
    for name, block in sigs.items():
        if not isinstance(block, dict):
            continue
        weight = float(block.get("weight", 0) or 0)
        rows.append({
            "name": name,
            "weight": weight,
            "label": name.replace("_", " ").upper(),
        })
    up = sorted([r for r in rows if r["weight"] > 0], key=lambda r: r["weight"], reverse=True)[:limit]
    down = sorted([r for r in rows if r["weight"] < 0], key=lambda r: abs(r["weight"]), reverse=True)[:limit]
    return {"up": up, "down": down}


def _source_count_for_tracker(tid):
    sources = set()
    for n in news_js:
        if n.get("zone") != tid:
            continue
        for src in n.get("sources", []) or []:
            if src:
                sources.add(str(src))
    return len(sources)


def _strip_auto_note_scaffolding(note):
    """Remove legacy generated `Auto - ...` prefixes from tracker narrative notes."""
    text = str(note or "")
    if not text:
        return ""
    # Repeated pipeline runs used to prepend `Auto - ZONE NN% (trend).` and then
    # fail to remove the previous prefix, producing mobile garbage like
    # `Auto - IMMINENT 100% ... Auto - . Auto - .`.
    text = re.sub(
        r"(?:\bDay\s+\d+\s+)?\b(?:auto|manual)\s*-\s*"
        r"(?:(?:DETERRENT|ELEVATED|CRITICAL|IMMINENT)\s*\d*%?(?:\s*\([^)]*\))?)?\s*\.?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip(" .")


def _dashboard_note_for_tracker(tid, trk):
    zone_note = state.get("zones", {}).get(tid, {}).get("notes", "")
    clean_zone = _strip_auto_note_scaffolding(zone_note)
    clean_tracker = _strip_auto_note_scaffolding(trk.get("notes", ""))
    if len(clean_zone) > 20:
        return clean_zone
    return clean_tracker


def _decorate_dashboard_trackers(trackers):
    for t in trackers:
        tid = t["id"]
        trk = state.get("trackers", {}).get(tid, {})
        base_rate = cfg.get("trackers", {}).get(tid, {}).get("base_rate", t.get("base_rate", 0))
        raw_prob = trk.get("current_probability", t.get("prob", 0))
        boost = trk.get("coupling_boost", max(0, t.get("prob", 0) - raw_prob))
        try:
            signal_delta = round(float(raw_prob) - float(base_rate), 1)
        except Exception:
            signal_delta = 0
        t["notes"] = _dashboard_note_for_tracker(tid, trk)
        t["attribution"] = {
            "base_rate": round(float(base_rate or 0), 1),
            "raw_probability": round(float(raw_prob or 0), 1),
            "signal_delta": signal_delta,
            "coupling_boost": round(float(boost or 0), 1),
            "final_probability": int(round(float(t.get("prob", 0)))),
        }
        ages = [_iso_age_hours(s.get("activated_at")) for s in t.get("signals", []) if isinstance(s, dict)]
        ages = [a for a in ages if a is not None]
        source_count = _source_count_for_tracker(tid)
        signal_count = len(t.get("signals", []) or [])
        newest = min(ages) if ages else None
        label = "HIGH" if source_count >= 3 and signal_count >= 3 else "MEDIUM" if source_count >= 1 or signal_count >= 2 else "LOW"
        t["evidence_quality"] = {
            "label": label,
            "source_count": source_count,
            "signal_count": signal_count,
            "newest_signal_age_hours": newest,
        }
        t["watch_triggers"] = _build_watch_triggers(tid)
    return trackers

for t in trackers_js:
    new_zone = classify_zone(t["prob"])
    t["zone"] = new_zone
    if t["id"] in state.get("trackers", {}):
        state["trackers"][t["id"]]["zone"] = new_zone

# Sanitize tracker narratives for dashboard use. Previous pipeline versions prepended
# `Auto - ZONE NN% ...` on every run; repeated executions produced `Auto - .`
# garbage that dominated mobile dossier cards. Keep probability/zone as structured
# fields and leave notes as plain source narrative.
for t in trackers_js:
    tid = t["id"]
    trk = state.get("trackers", {}).get(tid, {})
    if not trk:
        continue
    cleaned = _dashboard_note_for_tracker(tid, trk)
    trk["notes"] = cleaned
    if tid in state.get("zones", {}):
        state["zones"][tid]["notes"] = _strip_auto_note_scaffolding(state["zones"][tid].get("notes", ""))

# Find and replace the state block using string slicing (NO REGEX)
start = html.find("const state = {")
end = html.find("// ===== RENDER", start)

if start == -1 or end == -1:
    print(f"ERROR: markers not found start={start} end={end}")
else:
    # Reload config (coupling section may have changed mid-run if edited live)
    with open("data/tracker_config.json") as cf:
        cfg = json.load(cf)

    # Apply coupling spillover (elevated-or-above sources contaminate connected
    # trackers per cfg["coupling"]). Mutates trackers_js + state in place.
    boosts_applied, all_probs = apply_coupling(trackers_js, state, cfg, classify_zone)
    if boosts_applied:
        boost_log = ", ".join(f"{k}+{v:.1f}" for k, v in boosts_applied.items())
        print(f"Proportional coupling boosts: {boost_log}")

    gp, tz = calculate_global_probability(all_probs, cfg)
    trackers_js = _decorate_dashboard_trackers(trackers_js)
    state["dashboard_trackers"] = trackers_js
    # Update state.json with correct global
    state["global_war_probability"] = gp
    state["global_zone"] = tz
    state["global_probability"] = gp

    # Prune stale timeline entries before saving
    pruned_timeline = {"signals": {}}
    for key, entry in timeline.get("signals", {}).items():
        if ":" not in key:
            continue
        tid_part, sname = key.split(":", 1)
        tracker_signals = cfg.get("trackers", {}).get(tid_part, {}).get("signals", {})
        if sname not in tracker_signals:
            continue
        activated_at = entry.get("activated_at") if isinstance(entry, dict) else entry
        weight = signal_weights.get((tid_part, sname), 0)
        if weight and apply_temporal_decay(abs(weight), activated_at) == 0:
            continue
        if isinstance(entry, dict):
            pruned_timeline["signals"][key] = entry
        else:
            pruned_timeline["signals"][key] = {"activated_at": entry, "last_confirmed": entry}
    timeline = pruned_timeline

    # Write updated signal timeline
    with open("data/signal_timeline.json", "w") as tf:
        json.dump(timeline, tf, indent=2)

    # Detect zone changes for alerts
    try:
        with open("data/zone_alerts.json") as af:
            zone_alerts = json.load(af)
    except Exception as e:
        print(f"[pipeline] Error loading zone_alerts.json: {e}")
        zone_alerts = {"pending": [], "history": []}

    old_zones = {}
    try:
        with open("data/previous_zones.json") as pf:
            old_zones = json.load(pf)
    except Exception as e:
        log.warning(
            "previous_zones_load_error",
            extra={"err": repr(e)},
            exc_info=True,
        )

    new_zones = {}
    for t in trackers_js:
        new_zones[t["id"]] = t["zone"]

    zone_labels = {"deterrent": "DETERRENT", "elevated": "ELEVATED", "critical": "CRITICAL", "imminent": "IMMINENT"}
    zone_emojis = {"deterrent": "🟢", "elevated": "🟡", "critical": "🟠", "imminent": "🔴"}

    for tid in new_zones:
        if tid in old_zones and old_zones[tid] != new_zones[tid]:
            old_z = old_zones[tid]
            new_z = new_zones[tid]
            zone_rank_new = {"deterrent": 0, "elevated": 1, "critical": 2, "imminent": 3}
            direction = "⬆️" if zone_rank_new.get(new_z, 0) > zone_rank_new.get(old_z, 0) else "⬇️"
            tracker_name = next((t["name"] for t in trackers_js if t["id"] == tid), tid)
            tracker_prob = next((t["prob"] for t in trackers_js if t["id"] == tid), 0)
            alert = {
                "timestamp": now_iso,
                "tracker": tracker_name,
                "tracker_id": tid,
                "from": old_z,
                "to": new_z,
                "direction": direction,
                "prob": tracker_prob
            }
            zone_alerts["pending"].append(alert)
            zone_alerts["history"].append(alert)
            print(f"ALERT: {tracker_name} {old_z.upper()} → {new_z.upper()} {direction}")

    # Keep last 50 alerts in history
    zone_alerts["history"] = zone_alerts["history"][-50:]
    zone_alerts["pending"] = zone_alerts["pending"][-3:]  # Only show last 3 pending alerts
    with open("data/zone_alerts.json", "w") as af:
        json.dump(zone_alerts, af, indent=2)

    # Save current zones for next comparison
    with open("data/previous_zones.json", "w") as pf:
        json.dump(new_zones, pf, indent=2)

    # Append to probability history
    try:
        with open("data/probability_history.json") as hf:
            history = json.load(hf)
    except Exception as e:
        print(f"[pipeline] Error loading probability_history.json: {e}")
        history = {"entries": []}
    history["entries"].append({
        "timestamp": now_iso,
        "global": gp,
        "zone": tz,
        "trackers": {t["id"]: t["prob"] for t in trackers_js},
        "base_probs": {t["id"]: state.get("trackers", {}).get(t["id"], {}).get("current_probability", 0) for t in trackers_js}
    })
    # Keep last 336 entries (2 weeks at hourly)
    history["entries"] = history["entries"][-336:]
    with open("data/probability_history.json", "w") as hf:
        json.dump(history, hf, indent=2)

    # State write moved to after predictions section (line 1070+)


    lines = []
    lines.append("const state = {")
    lines.append("  last_updated: " + json.dumps(state.get("last_updated", "")) + ",")
    lines.append("  global_war_probability: " + str(gp) + ",")
    lines.append("  global_zone: " + json.dumps(tz) + ",")

    lines.append("  trackers: [")
    for t in trackers_js:
        signals_str = json.dumps(t["signals"])
        attribution_str = json.dumps(t.get("attribution", {}))
        evidence_str = json.dumps(t.get("evidence_quality", {}))
        watch_str = json.dumps(t.get("watch_triggers", {"up": [], "down": []}))
        prob_int = int(round(float(t["prob"])))  # Force integer — no decimals ever
        lines.append(
            "    { id: " + json.dumps(t["id"]) +
            ", name: " + json.dumps(t["name"]) +
            ", emoji: " + json.dumps(t["emoji"]) +
            ", prob: " + str(prob_int) +
            ", zone: " + json.dumps(t["zone"]) +
            ", trend: " + json.dumps(t["trend"]) +
            ", confidence: " + json.dumps(t.get("confidence", "LOW")) +
            ", attribution: " + attribution_str +
            ", evidence_quality: " + evidence_str +
            ", watch_triggers: " + watch_str +
            ", signals: " + signals_str + " },"
        )
    lines.append("  ],")
    lines.append("  news: [")
    for n in news_js[:10]:
        txt = json.dumps(n.get("text", ""))
        hl = json.dumps(n.get("headline", ""))
        src = json.dumps(n.get("sources", []))
        src_types = json.dumps(n.get("source_types", []))
        sigs = json.dumps(n.get("signals", []))
        lines.append(
            "    { zone: " + json.dumps(n.get("zone", "")) +
            ", time: " + json.dumps(n.get("time", "")) +
            ", text: " + txt +
            ", headline: " + hl +
            ", impact: " + json.dumps(n.get("impact", "neutral")) +
            ", sources: " + src +
            ", source_types: " + src_types +
            ", confidence: " + json.dumps(n.get("confidence", "reported")) +
            ", severity: " + str(n.get("severity", 1)) +
            ", signals: " + sigs + " },"
        )
    lines.append("  ],")
    # Add probability history (last 48 entries for chart)
    hist_entries = history["entries"][-48:]
    hist_js = json.dumps(hist_entries)
    lines.append("  history: " + hist_js + ",")
    # Add pending zone alerts
    alerts_js = json.dumps(zone_alerts.get("pending", []))
    lines.append("  zone_alerts: " + alerts_js + ",")
    # Add energy prices
    energy_js = json.dumps({
        "current": energy_data.get("current", {}),
        "baselines": energy_data.get("baselines", {}),
        "changes": energy_data.get("changes", {}),
        "history": energy_data.get("history", [])[-48:]
    })
    lines.append("  energy: " + energy_js)
    lines.append("};")

    # Generate static chart SVG via dashboard_builder module
    chart_svg = _module_generate_chart_svg(hist_entries)

    lines.append("")
    lines.append("// ===== RENDER")

    new_state = "\n".join(lines)
    new_html = html[:start] + new_state + html[end:]

    # Insert chart SVG into HTML (after new_html is created)
    chart_placeholder = '<div id="probChart" style="width:100%;height:120px"></div>'
    if chart_svg:
        new_html = new_html.replace(chart_placeholder, chart_svg)

    # ===== GENERATE 24-HOUR PREDICTIONS =====
    import os
    from datetime import timedelta
    utc_now = datetime.now(timezone.utc)
    sorted_trackers = sorted(trackers_js, key=lambda t: t["prob"], reverse=True)
    expires_at = (utc_now + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    predictions_dir = "data/predictions"
    os.makedirs(predictions_dir, exist_ok=True)
    
    today = utc_now.strftime("%Y-%m-%d")
    hour = utc_now.strftime("%H")
    pred_file = f"{predictions_dir}/{today}-{hour}.json"
    eval_file = f"{predictions_dir}/evaluations.json"
    
    # Load evaluations tracker
    try:
        with open(eval_file) as f:
            evaluations = json.load(f)
    except Exception as e:
        print(f"[pipeline] Error loading evaluations.json: {e}")
        evaluations = {"predictions": []}

    # Load lifetime (running) prediction stats — never truncated. Captures
    # cumulative Brier + accuracy across ALL evaluated predictions so the
    # windowed stats in evaluations.json can be rebuilt but the lifetime
    # numbers keep growing.
    lifetime_stats_file = f"{predictions_dir}/lifetime_stats.json"
    try:
        with open(lifetime_stats_file) as f:
            lifetime_stats = json.load(f)
    except Exception:
        lifetime_stats = {
            "total_evaluated": 0,
            "correct": 0,
            "sum_brier": 0.0,
            "last_updated": None,
        }
    brier_history_file = f"{predictions_dir}/brier_history.json"
    try:
        with open(brier_history_file) as f:
            brier_history = json.load(f)
    except Exception:
        brier_history = {"entries": []}

    forecast_resolutions_file = f"{predictions_dir}/forecast_resolutions.json"
    forecast_review_queue_file = f"{predictions_dir}/forecast_review_queue.json"
    try:
        with open(forecast_resolutions_file) as f:
            forecast_resolutions = json.load(f)
    except Exception:
        forecast_resolutions = {"version": "forecast_resolutions_v1", "forecasts": []}

    def _prediction_brier(pred):
        """Brier contribution for a single evaluated prediction: (p - outcome)^2
        where p is the forecast as a probability in [0,1] and outcome is 1 if
        `correct`, else 0. Non-probability predictions fall back to value/100.
        """
        try:
            p = float(pred.get("value", 50)) / 100.0
        except (TypeError, ValueError):
            p = 0.5
        p = max(0.0, min(1.0, p))
        outcome = 1.0 if pred.get("correct") else 0.0
        return (p - outcome) ** 2
    
    # Also load any unevaluated predictions from individual files (backup if evaluations.json was pruned)
    import glob as glob_mod
    pred_files = sorted(glob_mod.glob(f"{predictions_dir}/*.json"))
    for pf in pred_files:
        if pf.endswith("evaluations.json"):
            continue
        try:
            with open(pf) as pfh:
                pf_data = json.load(pfh)
            for p in pf_data.get("predictions", []):
                # Add to evaluations if not already there (match by description + expires_at)
                key = f"{p.get('tracker_id')}:{p.get('expires_at')}"
                existing_keys = {f"{ep.get('tracker_id')}:{ep.get('expires_at')}" for ep in evaluations["predictions"]}
                if key not in existing_keys:
                    evaluations["predictions"].append(p)
        except Exception as e:
            log.warning(
                "prediction_file_load_error",
                extra={"file": pf, "err": repr(e)},
                exc_info=True,
            )

    evaluations["predictions"] = dedupe_predictions(evaluations.get("predictions", []))

    # Evaluate expired predictions against current state (uses NARRATIVE_TO_EVAL
    # for legacy predictions without eval_type/eval_value set).
    evaluate_all_predictions(evaluations, state, now_iso)

    # Backfill: pull in expired predictions from individual files not yet in
    # evaluations.json (can happen if the evaluations window was pruned before
    # the prediction reached its expiry).
    import glob as _glob
    newly_added = 0
    for pf in sorted(_glob.glob(f"{predictions_dir}/*.json")):
        if pf.endswith("evaluations.json"):
            continue
        try:
            with open(pf) as f:
                pdata = json.load(f)
            for pred in pdata.get("predictions", []):
                if pred.get("expires_at", "") < now_iso and pred.get("eval_type"):
                    pred_key = (pred.get("tracker_id"), pred.get("expires_at"))
                    existing_keys = {(p.get("tracker_id"), p.get("expires_at")) for p in evaluations.get("predictions", [])}
                    if pred_key not in existing_keys:
                        pred["evaluated"] = False
                        evaluations["predictions"].append(pred)
                        newly_added += 1
        except Exception as _e:
            log.warning(
                "prediction_backfill_error",
                extra={"file": pf, "err": repr(_e)},
                exc_info=True,
            )
    if newly_added > 0:
        evaluate_all_predictions(evaluations, state, now_iso)

    # Generate new 24-hour predictions from news + signals + trends
    final_predictions = _module_generate_predictions(trackers_js, state, now_iso)
    forecast_ladder = generate_forecast_ladder(trackers_js, state, now_iso)
    historical_forecasts = []
    for pf in sorted(_glob.glob(f"{predictions_dir}/*.json")):
        if pf.endswith((
            "evaluations.json",
            "lifetime_stats.json",
            "brier_history.json",
            "forecast_resolutions.json",
            "forecast_review_queue.json",
        )):
            continue
        try:
            with open(pf) as f:
                pdata = json.load(f)
            historical_forecasts.extend(pdata.get("forecast_ladder", []) or [])
        except Exception as _fe:
            log.warning(
                "forecast_review_history_read_failed",
                extra={"file": pf, "err": repr(_fe)},
                exc_info=True,
            )
    all_forecasts_for_review = historical_forecasts + forecast_ladder
    forecast_calibration = compute_horizon_calibration(forecast_resolutions.get("forecasts", []))
    forecast_resolution_status = summarize_forecast_resolution_ledger(forecast_resolutions, forecast_ladder)
    forecast_review_queue = build_forecast_review_queue(all_forecasts_for_review, forecast_resolutions, now_iso, limit=50)
    forecast_review_status = summarize_forecast_review_queue(forecast_review_queue)
    forecast_resolutions["calibration"] = forecast_calibration
    forecast_resolutions["status"] = forecast_resolution_status
    forecast_resolutions["review_status"] = forecast_review_status

    # ========== Update LIFETIME stats incrementally ==========
    # Every prediction that is `evaluated` but not yet `lifetime_counted` rolls
    # into cumulative counters. Stored separately from the truncated
    # evaluations.json window so lifetime numbers are monotonic.
    new_evaluated = [
        p for p in evaluations.get("predictions", [])
        if p.get("evaluated") and not p.get("lifetime_counted")
    ]
    for p in new_evaluated:
        b = _prediction_brier(p)
        p["brier"] = round(b, 4)
        p["lifetime_counted"] = True
        lifetime_stats["total_evaluated"] = lifetime_stats.get("total_evaluated", 0) + 1
        if p.get("correct"):
            lifetime_stats["correct"] = lifetime_stats.get("correct", 0) + 1
        lifetime_stats["sum_brier"] = lifetime_stats.get("sum_brier", 0.0) + b
    if new_evaluated:
        lifetime_stats["last_updated"] = now_iso
        tot = lifetime_stats.get("total_evaluated", 0)
        mean_brier = lifetime_stats.get("sum_brier", 0.0) / tot if tot else 0.0
        brier_history.setdefault("entries", []).append({
            "timestamp": now_iso,
            "total_evaluated": tot,
            "correct": lifetime_stats.get("correct", 0),
            "mean_brier": round(mean_brier, 4),
        })
        # Keep brier_history bounded so the file doesn't grow forever.
        brier_history["entries"] = brier_history["entries"][-1000:]

    # Add new predictions to evaluations tracker for future evaluation
    evaluations["predictions"].extend(final_predictions)
    evaluations["predictions"] = dedupe_predictions(evaluations.get("predictions", []))
    # Keep last 2000 predictions (need 48h+ retention for 24h expiry + buffer).
    # Lifetime accuracy is tracked separately in lifetime_stats.json so this
    # truncation no longer biases published stats.
    evaluations["predictions"] = evaluations["predictions"][-2000:]

    evaluated_preds = [p for p in evaluations.get("predictions", []) if p.get("evaluated")]
    total_eval = lifetime_stats.get("total_evaluated", 0)
    correct_count = lifetime_stats.get("correct", 0)
    accuracy_pct = round(correct_count / total_eval * 100) if total_eval > 0 else 0
    mean_brier = round(lifetime_stats.get("sum_brier", 0.0) / total_eval, 4) if total_eval > 0 else 0.0
    
    # Save predictions
    pred_data = {
        "generated_at": now_iso,
        "date": today,
        "hour": hour,
        "predictions": final_predictions,
        "forecast_engine": {
            "version": "forecast_v2",
            "model_version": "base_rate_evidence_v1",
            "calibration_version": forecast_calibration.get("version"),
            "resolution_status_version": forecast_resolution_status.get("version"),
            "review_status_version": forecast_review_status.get("version"),
            "resolution_method": "manual_or_source_verified",
            "horizons": ["24h", "72h", "7d", "30d"],
        },
        "forecast_ladder": forecast_ladder,
        "forecast_calibration": forecast_calibration,
        "forecast_resolution_status": forecast_resolution_status,
        "forecast_review_status": forecast_review_status,
        "accuracy": {
            "total_evaluated": total_eval,
            "correct": correct_count,
            "accuracy_pct": accuracy_pct,
            "mean_brier": mean_brier,
        }
    }
    with open(pred_file, "w") as f:
        json.dump(pred_data, f, indent=2)

    # Write predictions to state for dashboard access
    state["predictions"] = final_predictions
    state["forecast_ladder"] = forecast_ladder
    state["forecast_engine"] = {
        "version": "forecast_v2",
        "model_version": "base_rate_evidence_v1",
        "calibration_version": forecast_calibration.get("version"),
        "resolution_status_version": forecast_resolution_status.get("version"),
        "review_status_version": forecast_review_status.get("version"),
        "resolution_method": "manual_or_source_verified",
        "horizons": ["24h", "72h", "7d", "30d"],
    }
    state["forecast_calibration"] = forecast_calibration
    state["forecast_resolution_status"] = forecast_resolution_status
    state["forecast_review_status"] = forecast_review_status
    state["eval_stats"] = {
        "total": total_eval,
        "correct": correct_count,
        "accuracy": accuracy_pct,
        "mean_brier": mean_brier,
    }

    # ===== POLYMARKET CROSS-CHECK =====
    # Compare DW probabilities against Polymarket implied probs, flag
    # divergence, surface to dashboard. Missing cache / network failures do not
    # block the pipeline — we degrade to no-op.
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from scripts.ingest.polymarket import refresh_cache_if_stale as _pm_refresh_if_stale
        from scripts.scoring.polymarket_check import check_all as _pm_check_all

        pm_mapping = {}
        pm_slugs = []
        try:
            with open("data/polymarket_mapping.json") as _pmf:
                pm_mapping = json.load(_pmf)
            for _entries in pm_mapping.values():
                if isinstance(_entries, list):
                    pm_slugs.extend([_e.get("slug") for _e in _entries if _e.get("slug")])
        except Exception as _map_e:
            log.warning("polymarket_mapping_read_failed", extra={"err": repr(_map_e)}, exc_info=True)

        pm_cache = _pm_refresh_if_stale(slugs=pm_slugs, max_age_hours=12.0, offline_ok=True)
        pm_result = _pm_check_all(cache=pm_cache, mapping=pm_mapping or None, state=state, append_log=True)
        state["polymarket"] = pm_result
        if pm_result["banner"].get("any_divergence"):
            worst = pm_result["banner"].get("worst_tracker")
            delta = pm_result["banner"].get("worst_abs_delta_pp")
            print(f"[polymarket] divergence detected — worst: {worst} {delta:.1f}pp")
        else:
            checked = len([c for c in pm_result["comparisons"].values() if c.get("status") == "ok"])
            print(f"[polymarket] aligned — {checked} trackers compared")
    except Exception as _pm_e:
        log.warning("polymarket_check_failed", extra={"err": repr(_pm_e)}, exc_info=True)
        state["polymarket"] = {"comparisons": {}, "banner": {"any_divergence": False}, "error": repr(_pm_e)}

    # Write state to file (after all updates). This file is published with
    # GitHub Pages, so scrub internal provider/API diagnostics before writing.
    sanitize_public_meta(state)
    with open("data/current_state.json", "w") as sf:
        json.dump(state, sf, indent=2)

    # Save updated evaluations + lifetime stats
    with open(eval_file, "w") as f:
        json.dump(evaluations, f, indent=2)
    with open(lifetime_stats_file, "w") as f:
        json.dump(lifetime_stats, f, indent=2)
    with open(brier_history_file, "w") as f:
        json.dump(brier_history, f, indent=2)
    with open(forecast_resolutions_file, "w") as f:
        json.dump(forecast_resolutions, f, indent=2)
    with open(forecast_review_queue_file, "w") as f:
        json.dump(forecast_review_queue, f, indent=2)

    # Format predictions for JS modal
    predictions_js = json.dumps(final_predictions)
    forecast_ladder_js = json.dumps(forecast_ladder)
    forecast_calibration_js = json.dumps(forecast_calibration)
    forecast_resolution_status_js = json.dumps(forecast_resolution_status)
    forecast_review_status_js = json.dumps(forecast_review_status)
    eval_stats_js = json.dumps({
        "total": total_eval,
        "correct": correct_count,
        "accuracy": accuracy_pct,
        "mean_brier": mean_brier,
    })
    
    # Generate CIA-style threat assessment narrative via dashboard_builder.
    narrative = _module_generate_narrative(trackers_js, hist_entries, gp, now_dt)

    # Stats for the post-run summary print (same derivation as narrative uses).
    key_devs_count = 0
    for _t in sorted(trackers_js, key=lambda t: t["prob"], reverse=True):
        for _s in _t.get("signals", []):
            try:
                _act = datetime.fromisoformat(_s["activated_at"].replace("Z", "+00:00"))
                if (now_dt - _act).total_seconds() / 3600 < 6:
                    key_devs_count += 1
            except Exception as _se:
                log.warning(
                    "signal_timestamp_parse_error",
                    extra={"err": repr(_se)}, exc_info=True,
                )
    prob_changes = {}
    if len(hist_entries) >= 2:
        _prev = hist_entries[-2]
        _curr = hist_entries[-1]
        for _tid in _curr.get("trackers", {}):
            _diff = _curr.get("trackers", {}).get(_tid, 0) - _prev.get("trackers", {}).get(_tid, 0)
            if _diff != 0:
                prob_changes[_tid] = _diff

    # Inject narrative into HTML
    narrative_placeholder = '<div id="narrative-content" style="font-size:12px;line-height:1.7;color:#8b949e;white-space:normal;"></div>'
    safe_narrative_html = html_lib.escape(narrative).replace("\n", "<br>")
    new_html = new_html.replace(narrative_placeholder, '<div id="narrative-content" style="font-size:12px;line-height:1.7;color:#8b949e;white-space:normal;">' + safe_narrative_html + '</div>')
    
    # Inject predictions + polymarket into HTML (in state block)
    # Slim polymarket payload for dashboard (drop heavy `markets` list from per-tracker
    # entries but keep summary fields + banner).
    pm_for_dash = {"comparisons": {}, "banner": state.get("polymarket", {}).get("banner", {}),
                   "fetched_at": state.get("polymarket", {}).get("fetched_at"),
                   "generated_at": state.get("polymarket", {}).get("generated_at"),
                   "stale": state.get("polymarket", {}).get("stale", False),
                   "age_hours": state.get("polymarket", {}).get("age_hours")}
    for _tid, _c in (state.get("polymarket", {}) or {}).get("comparisons", {}).items():
        if _c.get("status") != "ok":
            pm_for_dash["comparisons"][_tid] = _c
            continue
        pm_for_dash["comparisons"][_tid] = {
            k: _c[k] for k in (
                "tracker_id", "status", "dw_prob_pct", "pm_implied_raw_pct",
                "pm_implied_24h_pct", "horizon_days_avg", "used_slugs",
                "total_volume_24h", "liquidity_warn", "delta_pp",
                "abs_delta_pp", "flag", "color", "arrow",
            ) if k in _c
        }
    polymarket_js = json.dumps(pm_for_dash)
    pred_inject = (
        ",\n  predictions: " + predictions_js
        + ",\n  forecast_ladder: " + forecast_ladder_js
        + ",\n  forecast_calibration: " + forecast_calibration_js
        + ",\n  forecast_resolution_status: " + forecast_resolution_status_js
        + ",\n  forecast_review_status: " + forecast_review_status_js
        + ",\n  eval_stats: " + eval_stats_js
        + ",\n  polymarket: " + polymarket_js
    )
    # Use a more robust anchor - find the end of the state block
    new_html = new_html.replace("\n};\n\n// ===== RENDER", pred_inject + "\n};\n\n// ===== RENDER")

    with open("index.html", "w") as f:
        f.write(new_html)

    print(f"Updated index.html — global: {gp}% ({tz}) — {len(trackers_js)} trackers — narrative generated")
    print(f"Narrative: {key_devs_count} key developments, {len(prob_changes)} probability changes")

# Commit and push only when explicitly requested by the deploy wrapper.
if os.environ.get("NUKE_WATCH_AUTO_GIT") == "1":
    import subprocess
    subprocess.run(["git", "config", "user.name", "VoltaIntel"], check=True)
    subprocess.run(["git", "config", "user.email", "cryptocybrog1337@proton.me"], check=True)
    # Force-add only the generated/data files needed on GitHub Pages. Never use
    # `git add -A` here: the workspace can contain unrelated private artifacts,
    # and a deploy must not sweep them into the public dashboard repository.
    subprocess.run([
        "git", "add", "-f",
        "data/current_state.json",
        "data/signal_timeline.json",
        "data/polymarket_cache.json",
        "data/polymarket_mapping.json",
        "data/predictions/",
        "data/energy_prices.json",
        "data/flight_tracking.json",
        "data/tracker_config.json",
        "index.html",
    ], check=True)
    r = subprocess.run(["git", "commit", "-m", "Update " + state.get("last_updated", "") + " — automated"], capture_output=True, text=True)
    print("Committed" if r.returncode == 0 else "No changes to commit")
    r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    print("Pushed!" if r.returncode == 0 else r.stderr.strip())
else:
    print("Skipped git commit/push (set NUKE_WATCH_AUTO_GIT=1 to enable).")
