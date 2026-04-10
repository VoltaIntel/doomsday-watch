#!/usr/bin/env python3
"""
signals.py — Signal classification, credibility, decay, and matching.

Extracted from pipeline.py for DoomsdayWatch modular architecture.
"""

from datetime import datetime, timedelta, timezone


def classify_source_credibility(source_str, SOURCE_CREDIBILITY, TIER_WEIGHTS, TIER_LABELS):
    """Classify a source string into a credibility tier.
    Returns (tier_key, weight, label).
    Best-match wins: longest keyword substring match."""
    sl = source_str.lower().strip()
    best_tier = "5_unverified"
    best_match_len = 0
    for keyword, tier in SOURCE_CREDIBILITY.items():
        if keyword in sl and len(keyword) > best_match_len:
            best_tier = tier
            best_match_len = len(keyword)
    weight = TIER_WEIGHTS.get(best_tier, 0.3)
    label = TIER_LABELS.get(best_tier, "Unknown")
    return best_tier, weight, label


def classify_source(source_str, SOURCE_CREDIBILITY, TIER_WEIGHTS, TIER_LABELS):
    """Map source string to broad category: official/western/other."""
    tier, _, _ = classify_source_credibility(source_str, SOURCE_CREDIBILITY, TIER_WEIGHTS, TIER_LABELS)
    if tier == "1_official":
        return "official"
    if tier in ("2_wire", "3_established"):
        return "western"
    return "other"


def classify_source_category(source_str):
    """Categorise source by geopolitical media bloc."""
    sl = source_str.lower().strip()
    if any(k in sl for k in [
        "reuters", "associated press", "ap ", "apnews", "afp", "bbc",
        "new york times", "nyt", "wsj", "wall street journal",
        "washington post", "cnbc", "cnn", "france 24", "the hindu",
        "abc news", "nbc", "cbs", "bloomberg", "guardian"
    ]):
        return "western"
    if any(k in sl for k in [
        "tass", "ria", "interfax", "izvestia", "kommersant",
        "rossiyskaya", "rt ", "moscow times"
    ]):
        return "russian"
    if any(k in sl for k in [
        "xinhua", "cgtn", "china daily", "global times", "scmp",
        "south china morning post"
    ]):
        return "chinese"
    if any(k in sl for k in [
        "al jazeera", "al arabiya", "irna", "isna", "fars", "tasnim",
        "middle east", "haaretz", "times of israel", "jerusalem post",
        "the national", "gulf news", "khaleej", "oman news", "petra",
        "anadolu", "daily sabah", "hurriyet", "israel hayom"
    ]):
        return "arabic"
    if any(k in sl for k in [
        "white house", "pentagon", "iaea", "nato", "centcom",
        "stratcom", "unsc", "idf", "irgc", "kremlin",
        "un security council", "truth social"
    ]):
        return "official"
    return "other"


def calc_severity(impact, text):
    """Compute 1-5 severity from impact direction + keyword escalation."""
    text_lower = text.lower()
    severity = 2 if impact == "up" else 1 if impact == "down" else 1
    if any(w in text_lower for w in ["nuclear", "obliterated", "destroyed", "massive", "record"]):
        severity = min(5, severity + 2)
    elif any(w in text_lower for w in ["killed", "strikes", "attack", "crash", "invasion"]):
        severity = min(5, severity + 1)
    return min(5, max(1, severity))


def calc_confidence(sources_count, max_credibility_weight=0):
    """Derive confidence label from source count & credibility."""
    if max_credibility_weight >= 3 or sources_count >= 3:
        return "confirmed"
    if max_credibility_weight >= 2 or sources_count >= 2:
        return "reported"
    return "rumored"


def apply_credibility_weight(signal_weight, source_tier):
    """Scale signal weight by source tier."""
    tier_order = {
        "1_official": 3,
        "2_wire": 2,
        "3_established": 1.5,
        "4_regional": 1,
        "5_unverified": 0,
    }
    tier_val = tier_order.get(source_tier, 0)
    if tier_val >= 2:
        return signal_weight * 1.0
    elif tier_val >= 1.5:
        return signal_weight * 0.75
    elif tier_val >= 1:
        return signal_weight * 0.5
    else:
        return signal_weight * 0.2


def get_half_life(signal_weight):
    """Tiered half-life in hours based on signal importance (weight magnitude).

    - w >= 15: 168 h (7 days) — nuclear tests, ICBM launches, Article 5
    - w >=  8:  72 h (3 days) — major military actions
    - w >=  4:  24 h (1 day)  — rhetoric, buildup, minor events
    - else:     12 h          — noise, minor indicators
    """
    w = abs(signal_weight)
    if w >= 15:
        return 168
    elif w >= 8:
        return 72
    elif w >= 4:
        return 24
    else:
        return 12


def apply_temporal_decay(signal_weight, activated_at_iso):
    """Exponential decay with tiered half-life.

    Returns 0 when signal weight decays below 0.5.
    """
    try:
        activated = datetime.fromisoformat(activated_at_iso.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        hours_old = (now - activated).total_seconds() / 3600
        half_life = get_half_life(signal_weight)
        decayed = abs(signal_weight) * (0.5 ** (hours_old / half_life))
        if decayed < 0.5:
            return 0
        return round(decayed, 1)
    except Exception as e:
        print(f"[signals] Error in temporal decay: {e}")
        return signal_weight


def is_deescalation_signal(text, credibility_cfg):
    """Return True if de-escalation keywords outnumber escalation keywords."""
    text_lower = text.lower()
    deesc = credibility_cfg.get("deescalation_keywords", [])
    esc = credibility_cfg.get("escalation_keywords", [])
    deesc_count = sum(1 for k in deesc if k in text_lower)
    esc_count = sum(1 for k in esc if k in text_lower)
    return deesc_count > esc_count


def find_matching_signals(text, tid, cfg, signal_weights, credibility_cfg,
                          source_tier="5_unverified"):
    """Match text against tracker signals. Returns list of matched signal dicts.

    High-weight signals (|w| >= 10) require exact name match only.
    Lower-weight signals allow fuzzy description matching (>=3 term hits).
    """
    text_lower = text.lower()
    matched = []
    is_deesc = is_deescalation_signal(text_lower, credibility_cfg)
    for sname, scfg in cfg.get("trackers", {}).get(tid, {}).get("signals", {}).items():
        desc = scfg.get("description", "").lower()
        name_readable = sname.lower().replace("_", " ")
        weight = signal_weights.get((tid, sname), 0)
        triggered = False
        # HIGH-WEIGHT signals (>=10) require exact name match ONLY
        if abs(weight) >= 10:
            if name_readable in text_lower:
                triggered = True
        else:
            if name_readable in text_lower:
                triggered = True
            else:
                terms = [
                    t for t in desc.replace("(", "").replace(")", "")
                    .replace(",", "").replace(".", "").split()
                    if len(t) > 4
                ]
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
                "confidence": (
                    "confirmed" if source_tier in ["1_official", "2_wire"]
                    else "reported" if source_tier == "3_established"
                    else "rumored"
                ),
            })
    return matched


def normalize_trend(trend):
    """Normalise trend string to rising/falling/stable."""
    trend = (trend or "stable").lower().strip()
    if trend in {"up", "rising", "rise", "escalating", "escalation"}:
        return "rising"
    if trend in {"down", "falling", "fall", "de-escalating", "deescalating", "declining"}:
        return "falling"
    return "stable"


def get_timeline_details(timeline_key, timeline, now_iso, create=False):
    """Retrieve or create timeline entry for a signal.

    Handles migration from old string-only format.
    Returns (entry_dict, activated_at, last_confirmed).
    """
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


def confirm_signal(tid, signal_name, timeline, now_iso, confirmed_at=None):
    """Mark a signal as confirmed (update last_confirmed, preserve activated_at)."""
    timeline_key = f"{tid}:{signal_name}"
    entry, activated_at, _ = get_timeline_details(timeline_key, timeline, now_iso, create=True)
    entry["activated_at"] = activated_at or (confirmed_at or now_iso)
    entry["last_confirmed"] = confirmed_at or now_iso
    timeline["signals"][timeline_key] = entry


def build_signal_data(tid, state, signal_weights, timeline, now_dt, now_iso):
    """Build enriched signal list for a tracker with decay applied.

    Returns (signal_data_list, confidence_label).
    """
    tracker = state.get("trackers", {}).get(tid, {})
    signal_data = []

    # Primary: read active_signals from trackers schema (agent-managed signals)
    for signal_name in tracker.get("active_signals", []):
        timeline_key = f"{tid}:{signal_name}"
        _, activated_at, last_confirmed = get_timeline_details(
            timeline_key, timeline, now_iso, create=True
        )
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
            "is_deescalatory": weight < 0,
        })

    # Fallback: zone qualitative signals
    if not signal_data:
        zone_sigs = state.get("zones", {}).get(tid, {}).get("signals", {})
        if isinstance(zone_sigs, dict):
            weight_map = {
                "critical": 8, "high": 6, "medium": 4,
                "low": 2, "rising": 5, "elevated": 4,
            }
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
                        "_from_zones": True,
                    })

    signal_data.sort(key=lambda item: item["activated_at"], reverse=True)

    sig_count = len(signal_data)
    avg_tier = 0
    if signal_data:
        tier_scores = {"confirmed": 3, "reported": 2, "rumored": 1}
        avg_tier = sum(
            tier_scores.get(s.get("confidence", "rumored"), 1)
            for s in signal_data
        ) / sig_count

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
            except Exception:
                pass

    recency_score = (
        min(3, recency_score / max(1, min(3, sig_count)))
        if sig_count > 0 else 0
    )
    conf_score = min(40, sig_count * 5) + avg_tier * 15 + min(30, recency_score * 10)
    if conf_score >= 60:
        confidence = "HIGH"
    elif conf_score >= 30:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"
    return signal_data, confidence
