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
)
from probabilities import classify_zone as _classify_zone_cfg  # noqa: E402
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

def classify_source_credibility(source_str):
    sl = source_str.lower().strip()
    best_tier = "5_unverified"
    best_match_len = 0
    for keyword, tier in SOURCE_CREDIBILITY.items():
        kw = keyword.lower().strip()
        if not kw:
            continue
        # Word-boundary match so "the national" does not hit "the national review".
        if re.search(rf'\b{re.escape(kw)}\b', sl) and len(kw) > best_match_len:
            best_tier = tier
            best_match_len = len(kw)
    weight = TIER_WEIGHTS.get(best_tier, 0.3)
    label = TIER_LABELS.get(best_tier, "Unknown")
    return best_tier, weight, label

def classify_source(source_str):
    tier, _, _ = classify_source_credibility(source_str)
    if tier == "1_official": return "official"
    if tier in ("2_wire", "3_established"): return "western"
    return "other"

# classify_source_category, calc_severity, calc_confidence,
# apply_credibility_weight, get_half_life, apply_temporal_decay are now
# imported from signals.py at the top of this file.

def is_deescalation_signal(text):
    text_lower = text.lower()
    deesc = credibility_cfg.get("deescalation_keywords", [])
    esc = credibility_cfg.get("escalation_keywords", [])
    deesc_count = sum(1 for k in deesc if k in text_lower)
    esc_count = sum(1 for k in esc if k in text_lower)
    return deesc_count > esc_count

def find_matching_signals(text, tid, source_tier="5_unverified"):
    text_lower = text.lower()
    matched = []
    is_deesc = is_deescalation_signal(text_lower)
    for sname, scfg in cfg.get("trackers", {}).get(tid, {}).get("signals", {}).items():
        desc = scfg.get("description", "").lower()
        name_readable = sname.lower().replace("_", " ")
        weight = signal_weights.get((tid, sname), 0)
        triggered = False
        # HIGH-WEIGHT signals (>=10) require exact name match ONLY — no fuzzy matching
        if abs(weight) >= 10:
            # Must have exact name match or very specific phrases
            if name_readable in text_lower:
                triggered = True
        else:
            # Lower weight signals can use fuzzy matching
            if name_readable in text_lower:
                triggered = True
            else:
                terms = [t for t in desc.replace("(", "").replace(")", "").replace(",", "").replace(".", "").split() if len(t) > 4]
                matches = sum(1 for t in set(terms) if t in text_lower)
                if matches >= 3:
                    triggered = True
        if triggered:
            weight = signal_weights.get((tid, sname), 0)
            cred_weighted = apply_credibility_weight(abs(weight), source_tier)
            if is_deesc and weight > 0:
                continue
            final_weight = cred_weighted if weight >= 0 else -cred_weighted
            matched.append({
                "name": sname,
                "weight": round(final_weight, 1),
                "raw_weight": weight,
                "source_tier": source_tier,
                "confidence": "confirmed" if source_tier in ["1_official", "2_wire"] else "reported" if source_tier == "3_established" else "rumored"
            })
    return matched

# normalize_trend is imported from signals.py.

def get_timeline_details(timeline_key, create=False):
    entry = timeline["signals"].get(timeline_key)
    if isinstance(entry, dict):
        activated_at = entry.get("activated_at") or entry.get("last_confirmed") or now_iso
        last_confirmed = entry.get("last_confirmed") or activated_at
        entry["activated_at"] = activated_at
        entry["last_confirmed"] = last_confirmed
        timeline["signals"][timeline_key] = entry
        return entry, activated_at, last_confirmed
    if isinstance(entry, str):
        migrated = {"activated_at": entry, "last_confirmed": entry}
        timeline["signals"][timeline_key] = migrated
        return migrated, entry, entry
    if create:
        created = {"activated_at": now_iso, "last_confirmed": now_iso}
        timeline["signals"][timeline_key] = created
        return created, created["activated_at"], created["last_confirmed"]
    return None, None, None

def confirm_signal(tid, signal_name, confirmed_at=None):
    timeline_key = f"{tid}:{signal_name}"
    entry, activated_at, _ = get_timeline_details(timeline_key, create=True)
    entry["activated_at"] = activated_at or (confirmed_at or now_iso)
    entry["last_confirmed"] = confirmed_at or now_iso
    timeline["signals"][timeline_key] = entry

def build_signal_data(tid):
    tracker = state.get("trackers", {}).get(tid, {})
    signal_data = []

    # Primary: read active_signals from trackers schema (agent-managed signals)
    for signal_name in tracker.get("active_signals", []):
        timeline_key = f"{tid}:{signal_name}"
        _, activated_at, last_confirmed = get_timeline_details(timeline_key, create=True)
        weight = signal_weights.get((tid, signal_name), 0)
        if weight == 0:
            continue
        decayed_weight = apply_temporal_decay(abs(weight), activated_at)
        if decayed_weight == 0:
            continue
        signal_data.append({
            "name": signal_name,
            "positive": weight < 0,
            "activated_at": activated_at,
            "last_confirmed": last_confirmed,
            "original_weight": abs(weight),
            "decayed_weight": round(decayed_weight, 1),
            "expired": False,
            "is_deescalatory": weight < 0
        })

    # Fallback: if no signals from trackers schema, read qualitative zone signals
    # (cron job writes to zones[].signals as {"rhetoric": "medium", ...})
    if not signal_data:
        zone_sigs = state.get("zones", {}).get(tid, {}).get("signals", {})
        if isinstance(zone_sigs, dict):
            weight_map = {"critical": 8, "high": 6, "medium": 4, "low": 2, "rising": 5, "elevated": 4}
            for sig_name, sig_level in zone_sigs.items():
                if sig_level in weight_map:
                    signal_data.append({
                        "name": sig_name.title() + " (" + sig_level + ")",
                        "positive": False,
                        "activated_at": state.get("last_updated", now_iso),
                        "last_confirmed": state.get("last_updated", now_iso),
                        "original_weight": weight_map[sig_level],
                        "decayed_weight": weight_map[sig_level],
                        "expired": False,
                        "is_deescalatory": False,
                        "_from_zones": True  # Tag so auto-calculate knows to skip these
                    })

    signal_data.sort(key=lambda item: item["activated_at"], reverse=True)

    sig_count = len(signal_data)
    avg_tier = 0
    if signal_data:
        tier_scores = {"confirmed": 3, "reported": 2, "rumored": 1}
        avg_tier = sum(tier_scores.get(s.get("confidence", "rumored"), 1) for s in signal_data) / sig_count

    recency_score = 0
    for signal in signal_data[:3]:
        recency_marker = signal.get("last_confirmed") or signal.get("activated_at")
        if recency_marker:
            try:
                act_dt = datetime.fromisoformat(recency_marker.replace("Z", "+00:00"))
                hours_old = (now_dt - act_dt).total_seconds() / 3600
                if hours_old < 24:
                    recency_score += 3
                elif hours_old < 72:
                    recency_score += 2
                else:
                    recency_score += 1
            except Exception as _e:
                log.warning(
                    "recency_score_parse_error",
                    extra={"signal": signal.get("name"), "err": repr(_e)},
                    exc_info=True,
                )

    recency_score = min(3, recency_score / max(1, min(3, sig_count))) if sig_count > 0 else 0
    conf_score = min(40, sig_count * 5) + avg_tier * 15 + min(30, recency_score * 10)
    if conf_score >= 60:
        confidence = "HIGH"
    elif conf_score >= 30:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"
    return signal_data, confidence

def build_tracker_cards():
    cards = []
    # Fallback: if state["trackers"] is absent/empty, read from state["zones"]
    # (cron job writes to zones; pipeline previously only read trackers)
    trackers_src = state.get("trackers", {}) or state.get("zones", {})
    for tid, name, emoji in tn:
        tracker = trackers_src.get(tid, {})
        signal_data, confidence = build_signal_data(tid)
        trend = normalize_trend(tracker.get("trend", tracker.get("trend", "stable")))
        # current_probability (trackers schema) or current_prob (zones schema)
        prob = tracker.get("current_probability", tracker.get("current_prob", 0))
        # zone field: zones schema uses no zone field — derive from probability
        zone = tracker.get("zone")
        if not zone:
            zone_thresholds = cfg.get("scoring", {}).get("zones", {})
            def _zmin(key, default):
                val = zone_thresholds.get(key, {})
                if isinstance(val, list): return val[0] if val else default
                if isinstance(val, dict): return val.get("min", default)
                return default
            p = prob
            if p >= _zmin("imminent", 60): zone = "imminent"
            elif p >= _zmin("critical", 30): zone = "critical"
            elif p >= _zmin("elevated", 15): zone = "elevated"
            else: zone = "deterrent"
        base_rate = tracker.get("base_rate", cfg.get("trackers", {}).get(tid, {}).get("base_rate", 0))
        cards.append({
            "id": tid,
            "name": name,
            "emoji": emoji,
            "prob": prob,
            "zone": zone,
            "trend": trend,
            "signals": signal_data,
            "confidence": confidence,
            "base_rate": base_rate
        })
    return cards

def prediction_identity(pred):
    return (pred.get("tracker_id"), pred.get("expires_at"))

def merge_prediction_records(existing, incoming):
    merged = dict(existing)
    for key, value in incoming.items():
        if value is not None:
            merged[key] = value

    if existing.get("evaluated") and not incoming.get("evaluated"):
        for key in ("evaluated", "evaluated_at", "actual_value", "correct"):
            if key in existing:
                merged[key] = existing[key]

    for key in ("eval_type", "eval_value", "type", "value", "description", "confidence", "signal_name"):
        if merged.get(key) is None and existing.get(key) is not None:
            merged[key] = existing[key]

    return merged

def dedupe_predictions(predictions):
    deduped = {}
    order = []
    for pred in predictions:
        key = prediction_identity(pred)
        if key not in deduped:
            deduped[key] = pred
            order.append(key)
        else:
            deduped[key] = merge_prediction_records(deduped[key], pred)
    return [deduped[key] for key in order]
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
# convert zone signals into news items so the signal feed is populated.
raw_news = state.get("latest_news")
if not raw_news:
    # Enhanced fallback: extract news from zone notes + signals
    raw_news = []
    trackers = state.get("trackers", {})
    zones = state.get("zones", {})

    # First pass: extract news from zone/tracker notes fields
    for zone_id, zone_data in {**trackers, **zones}.items():
        notes = zone_data.get("notes", "")
        if notes and len(notes) > 20:
            # Extract first meaningful sentences as headlines
            sentences = [s.strip() for s in notes.replace('\n', '. ').split('.') if len(s.strip()) > 15]
            for sent in sentences[:2]:
                # Detect source from notes
                source = "Unknown"
                for src in ["Reuters", "AP", "CNN", "BBC", "NYT", "Al Jazeera", "NPR", "ISW", "LA Times", "WaPo", "Guardian", "Bloomberg", "TASS", "Xinhua"]:
                    if src.lower() in sent.lower():
                        source = src
                        break
                # Detect impact direction
                impact = "up" if any(w in sent.lower() for w in ["escalat", "strike", "bomb", "attack", "reject", "critical", "warn", "destroy", "kill", "invasion"]) else "down"
                raw_news.append({
                    "zone": zone_id,
                    "text": sent[:200],
                    "headline": sent[:80],
                    "sources": [source],
                    "impact": impact,
                    "time": "24H"
                })

    # Second pass: convert zone signals into news items
    for zid, zdata in {**zones, **trackers}.items():
        sigs = zdata.get("signals", {})
        if isinstance(sigs, dict) and sigs:
            sig_parts = []
            for k, v in sigs.items():
                if v and v not in ("none", "low"):
                    sig_parts.append(f"{k}: {v}")
            if sig_parts:
                raw_news.append({
                    "zone": zid,
                    "time": "LIVE",
                    "text": f"{zdata.get('name', zid.upper())} — " + " | ".join(sig_parts),
                    "headline": f"Signal update: {', '.join(sig_parts)}",
                    "impact": "elevated" if any(v in ("high", "critical", "rising") for v in sigs.values()) else "neutral",
                    "sources": ["NUCLEAR ESCALATION WATCH"],
                    "severity": 2
                })

    if not raw_news:
        raw_news = [{"zone": "iran", "time": "LIVE", "text": "Monitoring active", "impact": "neutral"}]

news_js = raw_news

# (credibility config and functions loaded at top of script)

# (all functions defined at top of script)

# Enrich news items with credibility scoring
enriched_news = []
seen_signals = {}  # Dedup: track first source for each signal to avoid double-counting

for n in news_js[:10]:
    sources = []
    if isinstance(n.get("source"), str):
        sources = [s.strip() for s in n["source"].split("/")]
    elif isinstance(n.get("sources"), list):
        sources = n["sources"]
    elif isinstance(n.get("source"), list):
        sources = n["source"]

    # Classify each source by credibility tier
    source_types = []
    max_cred_weight = 0
    primary_tier = "5_unverified"
    for s in sources:
        tier, weight, label = classify_source_credibility(s)
        source_types.append(classify_source_category(s))
        if weight > max_cred_weight:
            max_cred_weight = weight
            primary_tier = tier

    full_text = (n.get("headline", "") + " " + n.get("text", ""))
    zone = n.get("zone", "")
    zone_signals = find_matching_signals(full_text, zone, primary_tier) if zone else []

    # Dedup: only count the first (highest-credibility) source for each signal
    deduped_signals = []
    for sig in zone_signals:
        sig_key = f"{zone}:{sig['name']}"
        if sig_key not in seen_signals:
            seen_signals[sig_key] = primary_tier
            deduped_signals.append(sig)
        else:
            # Same signal already seen from another source — mark as duplicate
            sig["weight"] = 0  # Don't double-count
            sig["duplicate"] = True
            deduped_signals.append(sig)

    enriched_news.append({
        "zone": zone,
        "time": n.get("time", ""),
        "text": n.get("text", n.get("headline", "")),
        "headline": n.get("headline", ""),
        "impact": n.get("impact", "neutral"),
        "sources": sources,
        "source_types": source_types,
        "source_tier": primary_tier,
        "credibility_weight": max_cred_weight,
        "confidence": calc_confidence(len(sources), max_cred_weight),
        "severity": calc_severity(n.get("impact", "neutral"), full_text),
        "signals": deduped_signals
    })

news_js = enriched_news

# BUG FIX: Merge news-found signals with agent-set signals
# News scanner adds new signals; temporal decay removes expired ones
# Agent-set signals (from cron) are preserved unless expired
new_active_signals = {}  # {tracker_id: set(signal_names)}
for n in enriched_news:
    zone = n.get("zone", "")
    if zone:
        if zone not in new_active_signals:
            new_active_signals[zone] = set()
        for sig in n.get("signals", []):
            if not sig.get("duplicate") and sig.get("weight", 0) != 0:
                new_active_signals[zone].add(sig["name"])

# Apply merged signals back to state
for tid, tracker in state.get("trackers", {}).items():
    old_signals = set(tracker.get("active_signals", []))
    news_signals = new_active_signals.get(tid, set())
    
    # Merge: keep old signals that haven't expired + add new news signals
    # Check which old signals have expired via temporal decay
    still_valid = set()
    for s in old_signals:
        timeline_key = f"{tid}:{s}"
        w = signal_weights.get((tid, s), 0)
        if w == 0:
            continue  # Signal removed from config or invalid
        _, activated_at, _ = get_timeline_details(timeline_key, create=True)
        decayed = apply_temporal_decay(abs(w), activated_at)
        if decayed > 0:
            still_valid.add(s)
    
    # Merge: still_valid (agent-set, not expired) + news_signals (newly found)
    merged = still_valid | news_signals
    for signal_name in merged:
        confirm_signal(tid, signal_name)
    
    removed = old_signals - merged
    added = merged - old_signals
    if removed:
        print(f"[{tid}] Cleared {len(removed)} expired signals: {removed}")
    if added:
        print(f"[{tid}] Added {len(added)} new signals: {added}")
    tracker["active_signals"] = sorted(merged)
    tracker["signal_timestamps"] = {}
    for signal_name in tracker["active_signals"]:
        _, activated_at, _ = get_timeline_details(f"{tid}:{signal_name}", create=True)
        tracker["signal_timestamps"][signal_name] = activated_at or now_iso

state["signal_timestamps"] = {
    key: (entry.get("activated_at") if isinstance(entry, dict) else entry)
    for key, entry in timeline.get("signals", {}).items()
}

# ═══════════════════════════════════════════════════════════════════
# EXTRACT SPECIFIC SIGNALS FROM ZONE NOTES (fallback for cron jobs)
# Maps notes content to named signals from signalNameMap in dashboard
# ═══════════════════════════════════════════════════════════════════
_SIGNAL_KEYWORDS = {
    "hormuz_closed": ["hormuz closed", "hormuz shut", "strait closed", "re-closed strait"],
    "hormuz_controlled_not_closed": ["hormuz controlled", "hormuz restricted", "hormuz limited"],
    "hormuz_mining": ["hormuz min", "mined strait", "naval mine"],
    "hormuz_zero_traffic": ["hormuz zero", "hormuz no traffic"],
    "nuclear_rhetoric_official": ["nuclear rhetoric", "nuclear weapon", "nuclear threat", "nuclear capabilit"],
    "enrichment_90": ["90% enrich", "90 percent enrich", "weapons-grade", "weapon-grade enrich"],
    "enrichment_60": ["60% enrich", "60 percent enrich"],
    "diplomacy_refused": ["rejects peace", "rejects diplomacy", "peace talk", "refused diplomac", "refusing diplomac", "unreasonable"],
    "diplomacy_active": ["ceasefire", "peace deal", "diplomatic talk", "negotiat"],
    "missile_range_test": ["missile test", "missile launch", "ballistic missile", "missile range"],
    "iaea_access_denied": ["iaea access", "iaea denied", "iaea inspect"],
    "military_buildup": ["troop deploy", "military buildup", "force deploy", "carrier group"],
    "bomber_redeployment": ["bomber", "b-2", "b-52"],
    "ssbn_positioning": ["ssbn", "submarine deploy", "nuclear sub"],
    "ground_invasion_talk": ["ground invasion", "ground operation", "ground force"],
    "nuclear_test": ["nuclear test", "nuclear detonat"],
    "oil_infrastructure_threat": ["oil threat", "oil infrastructure", "oil target"],
    "ceasefire_violation": ["ceasefire violat", "broke ceasefire", "broke truce", "strikes despite ceasefire"],
}

# Ensure trackers dict exists
if "trackers" not in state:
    state["trackers"] = {}

for zone_id, zone_data in state.get("zones", {}).items():
    notes = zone_data.get("notes", "")
    if not notes or len(notes) < 20:
        continue
    notes_lower = notes.lower()
    matched_signals = []
    for signal_name, keywords in _SIGNAL_KEYWORDS.items():
        for kw in keywords:
            if kw in notes_lower:
                matched_signals.append(signal_name)
                break
    if matched_signals:
        if zone_id not in state["trackers"]:
            state["trackers"][zone_id] = {}
        # Merge with existing active_signals (don't overwrite)
        existing = set(state["trackers"][zone_id].get("active_signals", []))
        existing.update(matched_signals)
        state["trackers"][zone_id]["active_signals"] = sorted(existing)
        if "current_probability" not in state["trackers"][zone_id]:
            state["trackers"][zone_id]["current_probability"] = zone_data.get("current_prob", 0)

trackers_js = build_tracker_cards()

# ═══════════════════════════════════════════════════════════════════
# AUTO-CALCULATE PROBABILITIES FROM SIGNALS
# The agent manages signals. The code manages probabilities.
# Skip if state was written by cron job (zones schema — authoritative probs already set)
# Only auto-calculate when running standalone with signal data present.
# ═══════════════════════════════════════════════════════════════════
has_authoritative_trackors = bool(state.get("trackers", {}))
any_auto_calculated = False  # Track if any tracker was truly auto-calculated

for t in trackers_js:
    tid = t["id"]
    # Skip auto-calculation if:
    # (a) no trackers schema exists (cron job uses zones — authoritative probs already set)
    # (b) tracker has no real signals in trackers schema (uses zone fallback instead)
    tracker_signals = state.get("trackers", {}).get(tid, {}).get("active_signals", [])
    has_real_signals = bool(tracker_signals and any(
        (s.get("original_weight", 0) > 0 and not s.get("_from_zones")) if isinstance(s, dict) else True
        for s in tracker_signals
    ))
    if not has_authoritative_trackors or not has_real_signals:
        # Use zone's authoritative probability
        zone_prob = state.get("zones", {}).get(tid, {}).get("current_prob")
        if zone_prob is not None:
            t["prob"] = int(round(zone_prob))
        continue

    # Respect manually-set probabilities from cron job / agent analysis
    tracker_state = state.get("trackers", {}).get(tid, {})
    manual_prob = tracker_state.get("current_probability")
    if manual_prob is not None and manual_prob > 0:
        t["prob"] = int(round(manual_prob))
        continue

    # ═══════════════ ACTUAL AUTO-CALCULATION (only real signal data) ═══════════════
    any_auto_calculated = True
    tracker_cfg = cfg.get("trackers", {}).get(tid, {})
    base = tracker_cfg.get("base_rate", 10)
    
    # Sum active signal weights with temporal decay applied
    signal_sum = 0
    activation_times = []
    for s in t.get("signals", []):
        decayed_w = s.get("decayed_weight", s.get("original_weight", 0))
        raw_w = s.get("original_weight", 0)
        # De-escalation signals (positive flag) reduce probability
        if s.get("positive", False):
            signal_sum -= decayed_w
        else:
            signal_sum += decayed_w
        # Track signal activation times for no-news decay
        activated = s.get("activated_at", "")
        if activated:
            try:
                act_dt = datetime.fromisoformat(activated.replace("Z", "+00:00"))
                activation_times.append(act_dt)
            except Exception as e:
                log.warning(
                    "activation_parse_error",
                    extra={"activated": activated, "err": repr(e)},
                    exc_info=True,
                )

    # No-news decay: -1.5% per 24h without fresh signal activity, floored at -15
    # so dormant trackers don't get dragged to 2% by compounding silence.
    no_news_decay = 0
    if activation_times:
        sorted_times = sorted(activation_times)
        median_time = sorted_times[len(sorted_times) // 2]
        hours_since = (now_dt - median_time).total_seconds() / 3600
        if hours_since > 24:
            no_news_decay = max(-15, -1.5 * (hours_since / 24))
    elif not t.get("signals"):
        # Zero signals = no news for a long time
        no_news_decay = -5.0
    
    # Calculate final probability
    calculated_prob = base + signal_sum + no_news_decay
    calculated_prob = max(2, min(100, round(calculated_prob)))  # Floor at 2% (no event is zero risk)
    
    # If tracker had no active_signals, use zone's authoritative probability instead
    # (the cron job already set correct probs in zones schema — don't overwrite with 5%)
    # Only auto-calculate if signals came from trackers schema (not zone fallback)
    has_real_signals = (
        t.get("signals") and
        any(s.get("original_weight", 0) > 0 and not s.get("_from_zones") for s in t["signals"])
    )
    if has_real_signals:
        t["prob"] = calculated_prob
        # Also update state so coupling reads the correct base value
        if tid in state.get("trackers", {}):
            state["trackers"][tid]["current_probability"] = calculated_prob
    else:
        # No signals from trackers schema (empty active_signals) — use zone's authoritative prob
        zone_prob = state.get("zones", {}).get(tid, {}).get("current_prob")
        if zone_prob is not None:
            t["prob"] = int(round(zone_prob))

if any_auto_calculated:
    print(f"Auto-calculated probabilities from signals:")
    for t in trackers_js:
        print(f"  {t['name']}: base={cfg.get('trackers',{}).get(t['id'],{}).get('base_rate',0)} + signals={t['prob'] - cfg.get('trackers',{}).get(t['id'],{}).get('base_rate',0) - (-1.5 * 0 if t.get('signals') else -5):.1f} = {t['prob']}%")
else:
    print("All trackers using zone fallback (cron job set authoritative probabilities)")

# Recalculate zones from config thresholds (before coupling)
zone_thresholds = cfg.get("scoring", {}).get("zones", {})
def _zone_min(key, default):
    val = zone_thresholds.get(key, {})
    if isinstance(val, list):
        return val[0] if val else default
    if isinstance(val, dict):
        return val.get("min", default)
    return default

def classify_zone(p):
    if p >= _zone_min("imminent", 60): return "imminent"
    elif p >= _zone_min("critical", 30): return "critical"
    elif p >= _zone_min("elevated", 15): return "elevated"
    else: return "deterrent"

for t in trackers_js:
    new_zone = classify_zone(t["prob"])
    t["zone"] = new_zone
    if t["id"] in state.get("trackers", {}):
        state["trackers"][t["id"]]["zone"] = new_zone

# Fix stale notes: strip old probability numbers and replace with auto-calculated values
import re
zone_labels = {"deterrent": "DETERRENT", "elevated": "ELEVATED", "critical": "CRITICAL", "imminent": "IMMINENT"}
for t in trackers_js:
    tid = t["id"]
    trk = state.get("trackers", {}).get(tid, {})
    notes = trk.get("notes", "")
    if notes:
        day_match = re.search(r'\bDay\s+\d+\b', notes, re.IGNORECASE)
        day_prefix = f"{day_match.group(0)} auto - " if day_match else "Auto - "
        cleaned = re.sub(
            r'Day\s+\d+\s+auto\s*-\s*(?:DETERRENT|ELEVATED|CRITICAL|IMMINENT)?\s*\d*%?(?:\s*\([^)]*\))?\.?\s*',
            '',
            notes,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(
            r'Day\s+\d+\s*-\s*(?:DETERRENT|ELEVATED|CRITICAL|IMMINENT)?\s*\d*%?(?:\s*\([^)]*\))?\.?\s*',
            '',
            cleaned,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(r'\b(DETERRENT|ELEVATED|CRITICAL|IMMINENT)\s+\d+%?(\s*\([^)]*\))?', '', cleaned)
        cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip(' .')
        zone_label = zone_labels.get(t["zone"], "DETERRENT")
        trend = normalize_trend(trk.get("trend", "stable"))
        trk["notes"] = f"{day_prefix}{zone_label} {t['prob']}% ({trend}). {cleaned}" if cleaned else f"{day_prefix}{zone_label} {t['prob']}% ({trend})."

# Find and replace the state block using string slicing (NO REGEX)
start = html.find("const state = {")
end = html.find("// ===== RENDER", start)

if start == -1 or end == -1:
    print(f"ERROR: markers not found start={start} end={end}")
else:
    # Build new state block using string concatenation (safe from unicode issues)
    # Recalculate global from actual tracker probabilities
    all_probs = {}
    for t in trackers_js:
        all_probs[t["id"]] = t["prob"]

    # Apply coupling boosts — when a tracker is ELEVATED/CRITICAL/IMMINENT,
    # spill probability into connected trackers using the dict-of-dicts schema:
    #   cfg["coupling"][source_tracker]["affects"][target_tracker] = ratio (0-1)
    with open("data/tracker_config.json") as cf:
        cfg = json.load(cf)
    coupling_cfg = cfg.get("coupling", {})
    zone_rank = {"deterrent": 0, "elevated": 1, "critical": 2, "imminent": 3}
    # A source must be at least "elevated" before it contaminates other trackers.
    min_source_rank = zone_rank["elevated"]
    per_target_cap = 25.0

    boosts_applied = {}
    coupling_totals = {}  # {tgt: total_coupling_applied}

    for src, src_block in coupling_cfg.items():
        if not isinstance(src_block, dict):
            continue
        affects = src_block.get("affects", {})
        if not isinstance(affects, dict):
            continue
        src_zone = state.get("trackers", {}).get(src, {}).get("zone", "deterrent")
        if zone_rank.get(src_zone, 0) < min_source_rank:
            continue
        src_prob = all_probs.get(src, 0)
        if src_prob <= 0:
            continue
        for tgt, ratio in affects.items():
            if tgt not in all_probs:
                continue
            try:
                ratio_f = float(ratio)
            except (TypeError, ValueError):
                continue
            # Proportional spillover, capped at per_target_cap per target.
            raw_boost = ratio_f * min(per_target_cap, float(src_prob))
            current_coupling = coupling_totals.get(tgt, 0.0)
            remaining = max(0.0, per_target_cap - current_coupling)
            capped_boost = max(0.0, min(raw_boost, remaining))
            if capped_boost <= 0:
                continue
            all_probs[tgt] = min(100, all_probs[tgt] + capped_boost)
            coupling_totals[tgt] = current_coupling + capped_boost
            boosts_applied[tgt] = boosts_applied.get(tgt, 0.0) + capped_boost

    if boosts_applied:
        boost_log = ", ".join(f"{k}+{v:.1f}" for k, v in boosts_applied.items())
        print(f"Proportional coupling boosts: {boost_log}")

    # Push boosted probabilities to tracker cards and keep state coupling fields in sync
    for t in trackers_js:
        boosted = all_probs.get(t["id"], t["prob"])
        t["prob"] = round(boosted)  # Round to integer — no decimal percentages
        t["zone"] = classify_zone(t["prob"])
        tracker_state = state.get("trackers", {}).get(t["id"], {})
        base_prob = tracker_state.get("current_probability", 0)
        tracker_state["current_probability_with_coupling"] = t["prob"]
        tracker_state["coupling_boost"] = round(max(0, t["prob"] - base_prob), 1)
        tracker_state["zone"] = t["zone"]

    weights = cfg.get("global_weights", {"iran_nuclear": 0.12, "iran_conventional": 0.18, "israel_lebanon": 0.14, "russia_ukraine": 0.16, "turkey": 0.06, "india": 0.06, "pakistan_afghanistan": 0.08, "russia": 0.06, "china": 0.06, "north_korea": 0.08})
    gp = round(sum(all_probs.get(k, 10) * weights.get(k, 0.08) for k in all_probs))  # Already rounded — round() returns int for float input
    tz = classify_zone(gp)
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
        prob_int = int(round(float(t["prob"])))  # Force integer — no decimals ever
        lines.append(
            "    { id: " + json.dumps(t["id"]) +
            ", name: " + json.dumps(t["name"]) +
            ", emoji: " + json.dumps(t["emoji"]) +
            ", prob: " + str(prob_int) +
            ", zone: " + json.dumps(t["zone"]) +
            ", trend: " + json.dumps(t["trend"]) +
            ", confidence: " + json.dumps(t.get("confidence", "LOW")) +
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

    # Generate static chart SVG
    chart_svg = ""
    if len(hist_entries) >= 2:
        W, H = 600, 120
        padL, padR, padT, padB = 30, 10, 10, 20
        cW, cH = W - padL - padR, H - padT - padB

        chart_svg = '<div id="probChart" style="width:100%;overflow:hidden"><svg width="100%" height="120" viewBox="0 0 ' + str(W) + ' ' + str(H) + '">'
        # Zone backgrounds
        for mx, col in [(15, "rgba(0,230,118,0.06)"), (30, "rgba(255,170,0,0.06)"), (60, "rgba(255,170,0,0.08)"), (100, "rgba(255,45,45,0.06)")]:
            y1 = padT + cH * (1 - mx / 100)
            prev_mx = {15:0, 30:15, 60:30, 100:60}[mx]
            y2 = padT + cH * (1 - prev_mx / 100)
            chart_svg += '<rect x="' + str(padL) + '" y="' + str(y1) + '" width="' + str(cW) + '" height="' + str(y2-y1) + '" fill="' + col + '"/>'
        # Threshold lines
        for th in [15, 30, 60]:
            y = padT + cH * (1 - th / 100)
            chart_svg += '<line x1="' + str(padL) + '" y1="' + str(y) + '" x2="' + str(padL+cW) + '" y2="' + str(y) + '" stroke="rgba(255,255,255,0.08)" stroke-dasharray="3,3"/>'
            chart_svg += '<text x="2" y="' + str(y+3) + '" fill="#484f58" font-size="8" font-family="monospace">' + str(th) + '%</text>'
        # Global line
        pts = []
        for i, e in enumerate(hist_entries):
            x = padL + (i / max(len(hist_entries)-1, 1)) * cW
            y = padT + cH * (1 - (e.get("global", 0) / 100))
            pts.append(str(round(x,1)) + "," + str(round(y,1)))
        chart_svg += '<defs><filter id="cglow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
        chart_svg += '<polyline points="' + " ".join(pts) + '" fill="none" stroke="#ff2d2d" stroke-width="2" filter="url(#cglow)"/>'
        # Current dot
        last = hist_entries[-1]
        lx = padL + cW
        ly = padT + cH * (1 - last.get("global", 0) / 100)
        chart_svg += '<circle cx="' + str(lx) + '" cy="' + str(ly) + '" r="4" fill="#ff2d2d"/>'
        chart_svg += '<text x="' + str(lx-35) + '" y="' + str(ly-8) + '" fill="#e6edf3" font-size="10" font-weight="bold" font-family="monospace">' + str(last.get("global",0)) + '%</text>'
        # Time labels
        ft = (hist_entries[0].get("timestamp",""))[5:16].replace("T"," ")
        lt = (hist_entries[-1].get("timestamp",""))[5:16].replace("T"," ")
        chart_svg += '<text x="' + str(padL) + '" y="' + str(H-4) + '" fill="#484f58" font-size="8" font-family="monospace">' + ft + '</text>'
        chart_svg += '<text x="' + str(W-padR) + '" y="' + str(H-4) + '" fill="#484f58" font-size="8" font-family="monospace" text-anchor="end">' + lt + '</text>'
        chart_svg += '</svg></div>'

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

    # Map old narrative types to evaluable types (backward compat for Mar 14-16 predictions)
    narrative_to_eval = {
        "military_operation": ("probability_above", 0.7),
        "ground_operation": ("probability_above", 0.7),
        "diplomatic": ("probability_below", 0.5),
        "status_quo": ("probability_above", 0.5),
        "border_conflict": ("probability_above", 0.6),
        "nuclear_development": ("probability_above", 0.3),
        "economic_impact": ("probability_above", 0.5),
        "humanitarian": ("probability_above", 0.3),
        "arms_deal": ("probability_above", 0.4),
        "cyber_operation": ("probability_above", 0.3),
        "political_crisis": ("probability_above", 0.4),
    }
    
    # Evaluate yesterday's predictions (check if they expired)
    for pred in evaluations.get("predictions", []):
        if not pred.get("evaluated") and pred.get("expires_at", "") < now_iso:
            # This prediction has expired — evaluate it
            pred_tid = pred["tracker_id"]
            # Get eval_type, with fallback for old narrative types
            pred_type = pred.get("eval_type")
            pred_value = pred.get("eval_value")
            if not pred_type:
                # Old prediction without eval_type — map narrative type
                narrative_type = pred.get("type", "")
                if narrative_type in narrative_to_eval:
                    mapped_type, default_threshold = narrative_to_eval[narrative_type]
                    pred_type = mapped_type
                    # For status_quo: check if prob stayed similar
                    if narrative_type == "status_quo":
                        pred_value = pred.get("value", 50) * 0.7  # within 30% of original
                    else:
                        pred_value = default_threshold * 100  # e.g. 0.7 → 70
                else:
                    pred_type = "probability_above"  # default: "will it stay elevated?"
                    pred_value = 50
            actual_state = state.get("trackers", {}).get(pred_tid, {})

            if pred_type == "probability_above":
                actual_prob = actual_state.get("current_probability_with_coupling", actual_state.get("current_probability", 0))
                pred["actual_value"] = actual_prob
                pred["correct"] = actual_prob >= pred_value
                pred["evaluated"] = True
                pred["evaluated_at"] = now_iso
            elif pred_type == "probability_below":
                actual_prob = actual_state.get("current_probability_with_coupling", actual_state.get("current_probability", 0))
                pred["actual_value"] = actual_prob
                pred["correct"] = actual_prob <= pred_value
                pred["evaluated"] = True
                pred["evaluated_at"] = now_iso
            elif pred_type == "trend_rising":
                actual_trend = actual_state.get("trend", "stable")
                pred["actual_value"] = actual_trend
                pred["correct"] = actual_trend == "rising"
                pred["evaluated"] = True
                pred["evaluated_at"] = now_iso
            elif pred_type == "signal_triggered":
                actual_signals = actual_state.get("active_signals", [])
                pred["actual_value"] = pred.get("signal_name", "") in actual_signals
                pred["correct"] = pred.get("signal_name", "") in actual_signals
                pred["evaluated"] = True
                pred["evaluated_at"] = now_iso
            elif pred_type == "zone_change":
                actual_zone = actual_state.get("zone", "deterrent")
                pred["actual_value"] = actual_zone
                pred["correct"] = actual_zone == pred_value
                pred["evaluated"] = True
                pred["evaluated_at"] = now_iso
            else:
                # Unknown eval type — mark evaluated as False so it doesn't skew stats
                pred["evaluated"] = False
    
    # Fallback: Load expired predictions from individual files not in evaluations.json
    # This handles predictions that were pushed out by the history limit before expiring
    newly_added = 0
    total_eval = 0  # Will be calculated after evaluation
    if True:  # Always try to load from individual files
        import glob
        pred_files = sorted(glob.glob(f"{predictions_dir}/*.json"))
        for pf in pred_files:
            if pf.endswith("evaluations.json"):
                continue
            try:
                with open(pf) as f:
                    pdata = json.load(f)
                for pred in pdata.get("predictions", []):
                    # Only process expired predictions with eval metadata not already tracked
                    if pred.get("expires_at", "") < now_iso and pred.get("eval_type"):
                        # Check if already in evaluations.json by (tracker_id, expires_at) key
                        pred_key = (pred.get("tracker_id"), pred.get("expires_at"))
                        existing_keys = {(p.get("tracker_id"), p.get("expires_at")) for p in evaluations.get("predictions", [])}
                        if pred_key not in existing_keys:
                            pred["evaluated"] = False  # Mark for evaluation
                            evaluations["predictions"].append(pred)
                            newly_added += 1
            except Exception as _e:
                log.warning(
                    "prediction_backfill_error",
                    extra={"file": pf, "err": repr(_e)},
                    exc_info=True,
                )
        # Re-run evaluation if we added new predictions
        if newly_added > 0:
            for pred in evaluations.get("predictions", []):
                if not pred.get("evaluated") and pred.get("expires_at", "") < now_iso:
                    pred_tid = pred["tracker_id"]
                    pred_type = pred.get("eval_type", pred["type"])
                    pred_value = pred.get("eval_value", pred["value"])
                    actual_state = state.get("trackers", {}).get(pred_tid, {})
                    if pred_type == "probability_above":
                        actual_prob = actual_state.get("current_probability_with_coupling", actual_state.get("current_probability", 0))
                        pred["actual_value"] = actual_prob
                        pred["correct"] = actual_prob >= pred_value
                        pred["evaluated"] = True
                        pred["evaluated_at"] = now_iso
                    elif pred_type == "probability_below":
                        actual_prob = actual_state.get("current_probability_with_coupling", actual_state.get("current_probability", 0))
                        pred["actual_value"] = actual_prob
                        pred["correct"] = actual_prob <= pred_value
                        pred["evaluated"] = True
                        pred["evaluated_at"] = now_iso
                    elif pred_type == "trend_rising":
                        actual_trend = actual_state.get("trend", "stable")
                        pred["actual_value"] = actual_trend
                        pred["correct"] = actual_trend == "rising"
                        pred["evaluated"] = True
                        pred["evaluated_at"] = now_iso
                    elif pred_type == "signal_triggered":
                        actual_signals = actual_state.get("active_signals", [])
                        pred["actual_value"] = pred.get("signal_name", "") in actual_signals
                        pred["correct"] = pred.get("signal_name", "") in actual_signals
                        pred["evaluated"] = True
                        pred["evaluated_at"] = now_iso
                    elif pred_type == "zone_change":
                        actual_zone = actual_state.get("zone", "deterrent")
                        pred["actual_value"] = actual_zone
                        pred["correct"] = actual_zone == pred_value
                        pred["evaluated"] = True
                        pred["evaluated_at"] = now_iso
                    else:
                        pred["evaluated"] = False
    
    # Generate EVENT-BASED predictions from news + signals + trends
    news_texts = [((n.get("headline","") or n.get("text",""))).lower() for n in state.get("latest_news",[])]
    combined_news = " ".join(news_texts)
    
    new_predictions = []
    for t in sorted_trackers:
        prob = t["prob"]
        trend = t["trend"]
        tid = t["id"]
        tname = t["name"]
        confidence = 0
        event = ""
        etype = ""
        
        # IRAN CONVENTIONAL
        if tid == "iran_conventional" and prob >= 30:
            if "hormuz" in combined_news or "blockade" in combined_news:
                event = "Strait of Hormuz expected to remain under Iranian blockade. Additional shipping attacks probable within 12 hours."
                confidence = 75; etype = "military_operation"
            elif "dubai" in combined_news or "uae" in combined_news:
                event = "Iranian strikes on UAE infrastructure expected to continue. Further drone and missile attacks on Gulf state targets likely within 24 hours."
                confidence = 70; etype = "military_operation"
            elif confidence == 0 and trend == "rising":
                event = "Current escalation trajectory suggests Iran will sustain offensive operations against US and Israeli regional assets over the next 24 hours."
                confidence = 55; etype = "military_operation"

        # ISRAEL-LEBANON
        elif tid == "israel_lebanon" and prob >= 20:
            if "ground" in combined_news or "invasion" in combined_news:
                event = "Israeli ground operation in southern Lebanon expected to continue beyond Litani River. Further displacement and infrastructure destruction likely."
                confidence = 70; etype = "ground_operation"
            elif confidence == 0 and trend == "rising":
                event = "Continued escalation in Lebanon with increased Israeli operations and Hezbollah retaliatory strikes expected."
                confidence = 55; etype = "military_operation"

        # PAKISTAN-AFGHANISTAN
        elif tid == "pakistan_afghanistan" and prob >= 20:
            if "taliban" in combined_news or "border" in combined_news or "kills" in combined_news:
                event = "Border escalation between Afghanistan and Pakistan likely to intensify. Cross-border strikes expected within 24 hours."
                confidence = 65; etype = "border_conflict"
            elif confidence == 0:
                event = "Afghan-Pakistan border tensions likely to persist. Additional clashes probable based on recent trajectory."
                confidence = 50; etype = "border_conflict"

        # TURKEY
        elif tid == "turkey" and prob >= 15:
            if "incirlik" in combined_news or "nato" in combined_news:
                event = "Turkish military posture shift expected. NATO alliance consultations likely as Turkey repositions forces."
                confidence = 55; etype = "alliance_shift"
            elif trend == "rising":
                event = "Turkey expected to continue escalating rhetoric and military positioning in Eastern Mediterranean."
                confidence = 45; etype = "escalation"

        # RUSSIA-NATO
        elif tid == "russia" and prob >= 50:
            if "ceasefire" in combined_news or "deal" in combined_news:
                event = "Diplomatic negotiations may produce ceasefire framework within 24-72 hours, though implementation remains uncertain."
                confidence = 45; etype = "diplomatic"
            elif trend == "rising":
                event = "Russian military operations expected to continue at current tempo. No significant de-escalation indicators."
                confidence = 40; etype = "status_quo"

        # IRAN NUCLEAR
        elif tid == "iran_nuclear" and prob >= 20:
            if "iaea" in combined_news or "enrichment" in combined_news:
                event = "IAEA monitoring likely to produce findings within 72 hours. Iran may announce further enrichment activity."
                confidence = 40; etype = "nuclear_development"
            else:
                event = "No immediate nuclear threshold events anticipated. Status quo enrichment posture likely maintained."
                confidence = 35; etype = "status_quo"

        # Generic fallback
        if confidence == 0:
            if trend == "rising":
                event = f"Current escalation indicators suggest {tname} will remain on upward trajectory. Monitor for trigger events."
                confidence = 40; etype = "escalation"
            elif trend == "falling":
                event = f"{tname} showing de-escalation signals. Probability expected to decline gradually."
                confidence = 40; etype = "de_escalation"
            else:
                event = f"{tname} remains stable at current levels. No significant changes anticipated."
                confidence = 35; etype = "status_quo"
        
        # Map narrative intent to an evaluable prediction type
        # Rising/conflict predictions: probability should stay above (prob - 10)
        # Stable predictions: probability should stay above (prob - 15)
        # Falling predictions: probability should drop below current
        eval_type = "probability_above"
        eval_value = max(0, prob - 10)
        if etype in ("de_escalation",):
            eval_type = "probability_below"
            eval_value = prob
        elif etype in ("status_quo", "diplomatic", "nuclear_development"):
            eval_type = "probability_above"
            eval_value = max(0, prob - 15)

        # Compute a DIFFERENTIATED forecast value per prediction type so the
        # filter below actually measures whether the forecast moves vs today.
        prob_f = float(prob)
        if etype == "escalation":
            pred_value = int(round(min(100.0, prob_f * 1.15)))
        elif etype == "de_escalation":
            pred_value = int(round(max(0.0, prob_f * 0.85)))
        elif etype == "status_quo":
            pred_value = int(round(prob_f))
        else:
            # operation / diplomatic / nuclear_development / etc. — these are
            # "something happens at current intensity" forecasts; value = current prob.
            pred_value = int(round(prob_f))

        new_predictions.append({
            "tracker_id": tid,
            "tracker_name": tname,
            "type": etype,
            "value": pred_value,
            "description": event,
            "confidence": confidence,
            "expires_at": expires_at,
            "eval_type": eval_type,
            "eval_value": eval_value
        })

    # Drop status_quo forecasts that don't say anything new (pred == current).
    # Escalation / de_escalation now carry a differentiated `value` so they survive.
    filtered_predictions = []
    for pred in new_predictions:
        tid = pred["tracker_id"]
        current_prob = next((t["prob"] for t in sorted_trackers if t["id"] == tid), 0)
        pred_prob = pred["value"]
        if pred["type"] == "status_quo" and abs(pred_prob - current_prob) <= 3:
            continue
        filtered_predictions.append(pred)

    # Sort by confidence, take top 15
    filtered_predictions.sort(key=lambda x: x["confidence"], reverse=True)
    final_predictions = filtered_predictions[:15]

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
        from scripts.scoring.polymarket_check import check_all as _pm_check_all
        pm_result = _pm_check_all(state=state, append_log=True)
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

    # Write state to file (after all updates)
    with open("data/current_state.json", "w") as sf:
        json.dump(state, sf, indent=2)

    # Save updated evaluations + lifetime stats
    with open(eval_file, "w") as f:
        json.dump(evaluations, f, indent=2)
    with open(lifetime_stats_file, "w") as f:
        json.dump(lifetime_stats, f, indent=2)
    with open(brier_history_file, "w") as f:
        json.dump(brier_history, f, indent=2)

    # Format predictions for JS modal
    predictions_js = json.dumps(final_predictions)
    eval_stats_js = json.dumps({
        "total": total_eval,
        "correct": correct_count,
        "accuracy": accuracy_pct,
        "mean_brier": mean_brier,
    })
    
    # ===== GENERATE INTELLIGENCE NARRATIVE =====
    from datetime import datetime, timezone
    utc_now = datetime.now(timezone.utc)
    date_str = utc_now.strftime("%B %d, %Y")
    time_str = utc_now.strftime("%H:%M UTC")
    
    # Sort trackers by probability (highest first)
    sorted_trackers = sorted(trackers_js, key=lambda t: t["prob"], reverse=True)
    
    # Key developments (signals activated in last 6 hours)
    key_devs = []
    for t in sorted_trackers:
        for s in t.get("signals", []):
            try:
                activated = datetime.fromisoformat(s["activated_at"].replace("Z", "+00:00"))
                hours_ago = (utc_now - activated).total_seconds() / 3600
                if hours_ago < 6:
                    key_devs.append((t["name"], t["emoji"], s["name"].replace("_", " "), hours_ago))
            except Exception as e:
                log.warning(
                    "signal_timestamp_parse_error",
                    extra={"err": repr(e)},
                    exc_info=True,
                )

    # Zone summary
    zone_counts = {}
    for t in sorted_trackers:
        z = t["zone"]
        if z not in zone_counts:
            zone_counts[z] = []
        zone_counts[z].append(t)
    
    zone_order = ["imminent", "critical", "elevated", "deterrent"]
    zone_emoji = {"imminent": "\u2588\u2588\u2588\u2588", "critical": "\u2593\u2593\u2593", "elevated": "\u2592\u2592", "deterrent": "\u2591"}
    zone_verbal = {"imminent": "IMMINENT", "critical": "CRITICAL", "elevated": "ELEVATED", "deterrent": "DETERRENT"}
    
    # Probability changes
    prob_changes = {}
    if len(hist_entries) >= 2:
        prev = hist_entries[-2] if len(hist_entries) >= 2 else None
        curr = hist_entries[-1]
        if prev:
            for tid in curr.get("trackers", {}):
                p_old = prev.get("trackers", {}).get(tid, 0)
                p_new = curr.get("trackers", {}).get(tid, 0)
                diff = p_new - p_old
                if diff != 0:
                    prob_changes[tid] = diff
    
    # Rising trackers
    rising = [t for t in sorted_trackers if t["trend"] == "rising"]
    falling = [t for t in sorted_trackers if t["trend"] == "falling"]
    
    # Overall assessment
    gp_change = ""
    if len(hist_entries) >= 2:
        prev_g = hist_entries[-2].get("global", gp)
        diff_g = gp - prev_g
        if diff_g > 0:
            gp_change = f" (+{diff_g} from prior hour)"
        elif diff_g < 0:
            gp_change = f" ({diff_g} from prior hour)"
    
    # Highest threat
    top = sorted_trackers[0]
    
    # ===== CIA-STYLE NARRATIVE =====
    # Section 1: Headline assessment
    if gp >= 60:
        severity_word = "ELEVATED"
        overall = f"The global security environment remains {severity_word.lower()} with a composite threat score of {gp}%{gp_change}."
    elif gp >= 30:
        severity_word = "CONCERNING"
        overall = f"The global threat posture is {severity_word.lower()} at {gp}%{gp_change}."
    else:
        severity_word = "STABLE"
        overall = f"Global threat levels remain {severity_word.lower()} at {gp}%{gp_change}."
    
    # Section 2: Immediate threats (imminent/critical only)
    immediate = []
    for z in ["imminent", "critical"]:
        if z in zone_counts:
            for t in zone_counts[z]:
                sig_names = [s["name"].replace("_", " ") for s in t.get("signals", [])[:3]]
                sig_text = "; ".join(sig_names) if sig_names else "dormant"
                trend_word = "escalating" if t["trend"] == "rising" else "de-escalating" if t["trend"] == "falling" else "holding"
                immediate.append(f"  {t['emoji']} {t['name']} — {t['prob']}% ({trend_word}). {sig_text}.")
    
    # Section 3: Notable developments (formatted concisely)
    notable = []
    for tname, emoji, sig_name, hrs in key_devs[:5]:
        if hrs < 1:
            time_ref = f"{int(hrs*60)}m"
        else:
            time_ref = f"{hrs:.1f}h"
        notable.append(f"  {emoji} {tname} — {sig_name} ({time_ref} ago)")
    
    # Section 4: Trend analysis
    trend_parts = []
    if rising:
        names = ", ".join(t["name"] for t in rising[:3])
        trend_parts.append(f"Escalating: {names}")
    if falling:
        names = ", ".join(t["name"] for t in falling[:3])
        trend_parts.append(f"De-escalating: {names}")
    if not trend_parts:
        trend_parts.append("No significant directional shifts this cycle")
    
    # Section 5: Outlook
    outlook_parts = []
    if rising:
        outlook_parts.append(f"Monitor {rising[0]['name']} for continued escalation — currently {rising[0]['prob']}% and trending upward.")
    if prob_changes:
        biggest = max(prob_changes.items(), key=lambda x: abs(x[1]))
        name = next((t["name"] for t in sorted_trackers if t["id"] == biggest[0]), biggest[0])
        outlook_parts.append(f"{name} showed largest probability shift ({'+' if biggest[1] > 0 else ''}{biggest[1]}%).")
    if not outlook_parts:
        outlook_parts.append("No immediate escalation catalysts identified.")
    
    # Assemble CIA-style narrative
    narrative = f"""THREAT ASSESSMENT — {date_str} {time_str}

{overall}

IMMEDIATE THREATS:
{chr(10).join(immediate) if immediate else "  None currently in IMMINENT/CRITICAL zone."}

NOTABLE DEVELOPMENTS:
{chr(10).join(notable) if notable else "  No significant developments this cycle."}

TREND: {' | '.join(trend_parts)}

OUTLOOK: {' '.join(outlook_parts)}

CONFIDENCE: {"HIGH" if len(key_devs) >= 5 else "MEDIUM" if len(key_devs) >= 2 else "LOW"} | {sum(len(t.get('signals',[])) for t in sorted_trackers)} active signals | {len(key_devs)} new this cycle"""

    # Save narrative to state for JS injection
    narrative_js = json.dumps(narrative)
    
    # Inject narrative into HTML
    narrative_placeholder = '<div id="narrative-content" style="font-size:12px;line-height:1.7;color:#8b949e;white-space:normal;"></div>'
    safe_narrative_html = html_lib.escape(narrative).replace("\n", "<br>")
    new_html = new_html.replace(narrative_placeholder, '<div id="narrative-content" style="font-size:12px;line-height:1.7;color:#8b949e;white-space:normal;">' + safe_narrative_html + '</div>')
    
    # Inject predictions + polymarket into HTML (in state block)
    # Slim polymarket payload for dashboard (drop heavy `markets` list from per-tracker
    # entries but keep summary fields + banner).
    pm_for_dash = {"comparisons": {}, "banner": state.get("polymarket", {}).get("banner", {}),
                   "fetched_at": state.get("polymarket", {}).get("fetched_at")}
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
        + ",\n  eval_stats: " + eval_stats_js
        + ",\n  polymarket: " + polymarket_js
    )
    # Use a more robust anchor - find the end of the state block
    new_html = new_html.replace("\n};\n\n// ===== RENDER", pred_inject + "\n};\n\n// ===== RENDER")

    with open("index.html", "w") as f:
        f.write(new_html)

    print(f"Updated index.html — global: {gp}% ({tz}) — {len(trackers_js)} trackers — narrative generated")
    print(f"Narrative: {len(key_devs)} key developments, {len(prob_changes)} probability changes")

# Commit and push only when explicitly requested by the deploy wrapper.
if os.environ.get("NUKE_WATCH_AUTO_GIT") == "1":
    import subprocess
    subprocess.run(["git", "config", "user.name", "VoltaIntel"], check=True)
    subprocess.run(["git", "config", "user.email", "cryptocybrog1337@proton.me"], check=True)
    # Force-add data files (gitignored but needed on GitHub Pages)
    subprocess.run(["git", "add", "-f", "data/current_state.json", "data/signal_timeline.json", "data/predictions/", "data/energy_prices.json", "data/flight_tracking.json"], check=False)
    subprocess.run(["git", "add", "-A"], check=True)
    r = subprocess.run(["git", "commit", "-m", "Update " + state.get("last_updated", "") + " — automated"], capture_output=True, text=True)
    print("Committed" if r.returncode == 0 else "No changes to commit")
    r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    print("Pushed!" if r.returncode == 0 else r.stderr.strip())
else:
    print("Skipped git commit/push (set NUKE_WATCH_AUTO_GIT=1 to enable).")
