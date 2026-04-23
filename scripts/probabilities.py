#!/usr/bin/env python3
"""
probabilities.py — Zone classification, auto-calculation from signals,
coupling spillover, and global probability aggregation.

Extracted from pipeline.py for DoomsdayWatch modular architecture.
"""

import logging
from datetime import datetime

log = logging.getLogger("doomsdaywatch.probabilities")


def _zone_min(zone_thresholds, key, default):
    """Read a zone's minimum threshold, tolerating list or dict format."""
    val = zone_thresholds.get(key, {})
    if isinstance(val, list):
        return val[0] if val else default
    if isinstance(val, dict):
        return val.get("min", default)
    return default


def classify_zone(p, zone_thresholds):
    """Map a probability value (0-100) to a threat zone string.

    Uses config-defined thresholds with sensible defaults. Tolerates both
    list-form ([min, max]) and dict-form ({"min": ..., "max": ...}) configs.
    """
    if p >= _zone_min(zone_thresholds, "imminent", 60):
        return "imminent"
    elif p >= _zone_min(zone_thresholds, "critical", 30):
        return "critical"
    elif p >= _zone_min(zone_thresholds, "elevated", 15):
        return "elevated"
    else:
        return "deterrent"


def calculate_global_probability(all_probs, cfg):
    """Compute weighted global threat score from per-tracker probabilities.

    Uses global_weights from tracker_config.json. Falls back to equal weighting
    (0.08 each) for trackers not listed in weights.

    Returns (global_prob_int, zone_string).
    """
    weights = cfg.get("global_weights", {
        "iran_nuclear": 0.12,
        "iran_conventional": 0.18,
        "israel_lebanon": 0.14,
        "russia_ukraine": 0.16,
        "turkey": 0.06,
        "india": 0.06,
        "pakistan_afghanistan": 0.08,
        "russia": 0.06,
        "china": 0.06,
        "north_korea": 0.08,
    })
    gp = round(
        sum(all_probs.get(k, 10) * weights.get(k, 0.08) for k in all_probs)
    )
    zone_thresholds = cfg.get("scoring", {}).get("zones", {})
    tz = classify_zone(gp, zone_thresholds)
    return gp, tz


def auto_calculate_probabilities(trackers_js, state, cfg, now_dt):
    """Mutate trackers_js in place, computing per-tracker probabilities from
    active signals + base rate + no-news decay. Falls back to the zone's
    authoritative current_prob when no real signals are present.

    Returns True if any tracker was actually auto-calculated (vs. zone fallback).
    """
    has_authoritative_trackers = bool(state.get("trackers", {}))
    any_auto_calculated = False

    for t in trackers_js:
        tid = t["id"]
        tracker_signals = state.get("trackers", {}).get(tid, {}).get("active_signals", [])
        has_real_signals = bool(tracker_signals and any(
            (s.get("original_weight", 0) > 0 and not s.get("_from_zones"))
            if isinstance(s, dict) else True
            for s in tracker_signals
        ))
        if not has_authoritative_trackers or not has_real_signals:
            zone_prob = state.get("zones", {}).get(tid, {}).get("current_prob")
            if zone_prob is not None:
                t["prob"] = int(round(zone_prob))
            continue

        # Respect manually-set probabilities from cron / agent analysis
        tracker_state = state.get("trackers", {}).get(tid, {})
        manual_prob = tracker_state.get("current_probability")
        if manual_prob is not None and manual_prob > 0:
            t["prob"] = int(round(manual_prob))
            continue

        any_auto_calculated = True
        tracker_cfg = cfg.get("trackers", {}).get(tid, {})
        base = tracker_cfg.get("base_rate", 10)

        signal_sum = 0
        activation_times = []
        for s in t.get("signals", []):
            decayed_w = s.get("decayed_weight", s.get("original_weight", 0))
            if s.get("positive", False):
                signal_sum -= decayed_w
            else:
                signal_sum += decayed_w
            activated = s.get("activated_at", "")
            if activated:
                try:
                    act_dt = datetime.fromisoformat(activated.replace("Z", "+00:00"))
                    activation_times.append(act_dt)
                except Exception as e:
                    log.warning(
                        "activation_parse_error activated=%s err=%r",
                        activated, e, exc_info=True,
                    )

        # No-news decay: -1.5% per 24h, floored at -15, so dormant trackers
        # don't get dragged to 2% by compounding silence.
        no_news_decay = 0
        if activation_times:
            sorted_times = sorted(activation_times)
            median_time = sorted_times[len(sorted_times) // 2]
            hours_since = (now_dt - median_time).total_seconds() / 3600
            if hours_since > 24:
                no_news_decay = max(-15, -1.5 * (hours_since / 24))
        elif not t.get("signals"):
            no_news_decay = -5.0

        calculated_prob = base + signal_sum + no_news_decay
        calculated_prob = max(2, min(100, round(calculated_prob)))

        has_real_signals = (
            t.get("signals") and
            any(
                s.get("original_weight", 0) > 0 and not s.get("_from_zones")
                for s in t["signals"]
            )
        )
        if has_real_signals:
            t["prob"] = calculated_prob
            if tid in state.get("trackers", {}):
                state["trackers"][tid]["current_probability"] = calculated_prob
        else:
            zone_prob = state.get("zones", {}).get(tid, {}).get("current_prob")
            if zone_prob is not None:
                t["prob"] = int(round(zone_prob))

    return any_auto_calculated


def apply_coupling(trackers_js, state, cfg, classify_zone_fn):
    """Apply proportional coupling spillover: when a tracker is ELEVATED or
    above, spill probability into connected trackers per cfg["coupling"].

    Mutates trackers_js and state["trackers"][*] in place, populating
    current_probability_with_coupling and coupling_boost per tracker.

    Returns dict of {tracker_id: boost_points} for logging.
    """
    all_probs = {t["id"]: t["prob"] for t in trackers_js}

    coupling_cfg = cfg.get("coupling", {})
    zone_rank = {"deterrent": 0, "elevated": 1, "critical": 2, "imminent": 3}
    min_source_rank = zone_rank["elevated"]
    per_target_cap = 25.0

    boosts_applied = {}
    coupling_totals = {}

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
            raw_boost = ratio_f * min(per_target_cap, float(src_prob))
            current_coupling = coupling_totals.get(tgt, 0.0)
            remaining = max(0.0, per_target_cap - current_coupling)
            capped_boost = max(0.0, min(raw_boost, remaining))
            if capped_boost <= 0:
                continue
            all_probs[tgt] = min(100, all_probs[tgt] + capped_boost)
            coupling_totals[tgt] = current_coupling + capped_boost
            boosts_applied[tgt] = boosts_applied.get(tgt, 0.0) + capped_boost

    for t in trackers_js:
        boosted = all_probs.get(t["id"], t["prob"])
        t["prob"] = round(boosted)
        t["zone"] = classify_zone_fn(t["prob"])
        tracker_state = state.get("trackers", {}).get(t["id"], {})
        base_prob = tracker_state.get("current_probability", 0)
        tracker_state["current_probability_with_coupling"] = t["prob"]
        tracker_state["coupling_boost"] = round(max(0, t["prob"] - base_prob), 1)
        tracker_state["zone"] = t["zone"]

    return boosts_applied, all_probs
