#!/usr/bin/env python3
"""
signals.py — Signal classification, credibility, decay, and matching.

Extracted from pipeline.py for DoomsdayWatch modular architecture.
"""

import logging
import re
from datetime import datetime, timedelta, timezone

log = logging.getLogger("doomsdaywatch.signals")


def classify_source_credibility(source_str, SOURCE_CREDIBILITY, TIER_WEIGHTS, TIER_LABELS):
    """Classify a source string into a credibility tier.
    Returns (tier_key, weight, label).
    Longest word-boundary keyword match wins."""
    sl = source_str.lower().strip()
    best_tier = "5_unverified"
    best_match_len = 0
    for keyword, tier in SOURCE_CREDIBILITY.items():
        kw = keyword.lower().strip()
        if not kw:
            continue
        if re.search(rf'\b{re.escape(kw)}\b', sl) and len(kw) > best_match_len:
            best_tier = tier
            best_match_len = len(kw)
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


def _any_word_match(sl, keywords):
    """Return True if any keyword matches on word boundaries in sl."""
    for kw in keywords:
        if re.search(rf'\b{re.escape(kw)}\b', sl):
            return True
    return False


def classify_source_category(source_str):
    """Categorise source by geopolitical media bloc. Uses word-boundary matching
    so short tokens like "ap" and "rt" don't hit substrings inside other words."""
    sl = source_str.lower().strip()
    if _any_word_match(sl, [
        "reuters", "associated press", "ap", "apnews", "afp", "bbc",
        "new york times", "nyt", "wsj", "wall street journal",
        "washington post", "cnbc", "cnn", "france 24", "the hindu",
        "abc news", "nbc", "cbs", "bloomberg", "guardian"
    ]):
        return "western"
    if _any_word_match(sl, [
        "tass", "ria", "interfax", "izvestia", "kommersant",
        "rossiyskaya", "rt", "moscow times"
    ]):
        return "russian"
    if _any_word_match(sl, [
        "xinhua", "cgtn", "china daily", "global times", "scmp",
        "south china morning post"
    ]):
        return "chinese"
    if _any_word_match(sl, [
        "al jazeera", "al arabiya", "irna", "isna", "fars", "tasnim",
        "middle east", "haaretz", "times of israel", "jerusalem post",
        "the national", "gulf news", "khaleej", "oman news", "petra",
        "anadolu", "daily sabah", "hurriyet", "israel hayom"
    ]):
        return "arabic"
    if _any_word_match(sl, [
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
        log.error(
            "temporal_decay_error weight=%s activated=%s err=%r",
            signal_weight, activated_at_iso, e, exc_info=True,
        )
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
            except Exception as e:
                log.warning(
                    "recency_score_parse_error signal=%s err=%r",
                    signal.get("name"), e, exc_info=True,
                )

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


# ── News-feed helpers (moved from pipeline.py) ────────────────────────────────

KNOWN_NEWS_SOURCES = [
    "Reuters", "AP", "CNN", "BBC", "NYT", "Al Jazeera", "NPR", "ISW",
    "LA Times", "WaPo", "Guardian", "Bloomberg", "TASS", "Xinhua",
]

ESCALATION_WORDS = [
    "escalat", "strike", "bomb", "attack", "reject", "critical",
    "warn", "destroy", "kill", "invasion",
]

ZONE_SIGNAL_KEYWORDS = {
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


def build_raw_news_fallback(state):
    """Synthesise raw_news from zone notes + zone signals when latest_news is
    absent. Returns at minimum a single placeholder item."""
    raw_news = []
    trackers = state.get("trackers", {})
    zones = state.get("zones", {})

    for zone_id, zone_data in {**trackers, **zones}.items():
        notes = zone_data.get("notes", "")
        if notes and len(notes) > 20:
            sentences = [
                s.strip() for s in notes.replace('\n', '. ').split('.')
                if len(s.strip()) > 15
            ]
            for sent in sentences[:2]:
                source = "Unknown"
                for src in KNOWN_NEWS_SOURCES:
                    if src.lower() in sent.lower():
                        source = src
                        break
                sent_l = sent.lower()
                impact = "up" if any(w in sent_l for w in ESCALATION_WORDS) else "down"
                raw_news.append({
                    "zone": zone_id,
                    "text": sent[:200],
                    "headline": sent[:80],
                    "sources": [source],
                    "impact": impact,
                    "time": "24H",
                })

    for zid, zdata in {**zones, **trackers}.items():
        sigs = zdata.get("signals", {})
        if isinstance(sigs, dict) and sigs:
            sig_parts = [f"{k}: {v}" for k, v in sigs.items()
                         if v and v not in ("none", "low")]
            if sig_parts:
                raw_news.append({
                    "zone": zid,
                    "time": "LIVE",
                    "text": f"{zdata.get('name', zid.upper())} — " + " | ".join(sig_parts),
                    "headline": f"Signal update: {', '.join(sig_parts)}",
                    "impact": "elevated" if any(
                        v in ("high", "critical", "rising") for v in sigs.values()
                    ) else "neutral",
                    "sources": ["NUCLEAR ESCALATION WATCH"],
                    "severity": 2,
                })

    if not raw_news:
        raw_news = [{
            "zone": "iran", "time": "LIVE",
            "text": "Monitoring active", "impact": "neutral",
        }]
    return raw_news


def _extract_sources(n):
    """Normalise a news item's source(s) to a list of strings."""
    if isinstance(n.get("source"), str):
        return [s.strip() for s in n["source"].split("/")]
    if isinstance(n.get("sources"), list):
        return n["sources"]
    if isinstance(n.get("source"), list):
        return n["source"]
    return []


def enrich_news(raw_news, *, classify_credibility, classify_category,
                find_matching_signals_fn, calc_confidence_fn, calc_severity_fn):
    """Add credibility tier, source category, matched signals, and severity
    to each news item. Deduplicates signals across items — first (highest-
    credibility) source "owns" each signal; duplicates keep entries for
    display but drop the weight.

    Returns enriched list (up to first 10 items).
    """
    enriched = []
    seen_signals = {}

    for n in raw_news[:10]:
        sources = _extract_sources(n)

        source_types = []
        max_cred_weight = 0
        primary_tier = "5_unverified"
        for s in sources:
            tier, weight, _label = classify_credibility(s)
            source_types.append(classify_category(s))
            if weight > max_cred_weight:
                max_cred_weight = weight
                primary_tier = tier

        full_text = (n.get("headline", "") + " " + n.get("text", ""))
        zone = n.get("zone", "")
        zone_signals = find_matching_signals_fn(full_text, zone, primary_tier) if zone else []

        deduped_signals = []
        for sig in zone_signals:
            sig_key = f"{zone}:{sig['name']}"
            if sig_key not in seen_signals:
                seen_signals[sig_key] = primary_tier
                deduped_signals.append(sig)
            else:
                sig["weight"] = 0
                sig["duplicate"] = True
                deduped_signals.append(sig)

        enriched.append({
            "zone": zone,
            "time": n.get("time", ""),
            "text": n.get("text", n.get("headline", "")),
            "headline": n.get("headline", ""),
            "impact": n.get("impact", "neutral"),
            "sources": sources,
            "source_types": source_types,
            "source_tier": primary_tier,
            "credibility_weight": max_cred_weight,
            "confidence": calc_confidence_fn(len(sources), max_cred_weight),
            "severity": calc_severity_fn(n.get("impact", "neutral"), full_text),
            "signals": deduped_signals,
        })
    return enriched


def merge_news_signals_into_state(enriched_news, state, signal_weights, *,
                                  apply_temporal_decay_fn, get_timeline_details_fn,
                                  confirm_signal_fn, now_iso):
    """Merge news-found signals with agent-set signals on each tracker. Drops
    signals whose temporal decay has expired. Writes active_signals +
    signal_timestamps back into state."""
    new_active = {}
    for n in enriched_news:
        zone = n.get("zone", "")
        if not zone:
            continue
        new_active.setdefault(zone, set())
        for sig in n.get("signals", []):
            signal_name = sig.get("name")
            # Signal matching is global, but activation is tracker-specific.
            # Never attach a matched signal to a tracker that does not define it
            # in the canonical tracker config (represented by signal_weights).
            if (
                signal_name
                and signal_weights.get((zone, signal_name), 0) != 0
                and not sig.get("duplicate")
                and sig.get("weight", 0) != 0
            ):
                new_active[zone].add(signal_name)

    for tid, tracker in state.get("trackers", {}).items():
        old_signals = set(tracker.get("active_signals", []))
        news_signals = new_active.get(tid, set())

        still_valid = set()
        for s in old_signals:
            w = signal_weights.get((tid, s), 0)
            if w == 0:
                continue
            _, activated_at, _ = get_timeline_details_fn(f"{tid}:{s}", create=True)
            if apply_temporal_decay_fn(abs(w), activated_at) > 0:
                still_valid.add(s)

        merged = still_valid | news_signals
        for signal_name in merged:
            confirm_signal_fn(tid, signal_name)

        removed = old_signals - merged
        added = merged - old_signals
        if removed:
            print(f"[{tid}] Cleared {len(removed)} expired signals: {removed}")
        if added:
            print(f"[{tid}] Added {len(added)} new signals: {added}")
        tracker["active_signals"] = sorted(merged)
        tracker["signal_timestamps"] = {}
        for signal_name in tracker["active_signals"]:
            _, activated_at, _ = get_timeline_details_fn(f"{tid}:{signal_name}", create=True)
            tracker["signal_timestamps"][signal_name] = activated_at or now_iso


def extract_signals_from_notes(state, signal_weights=None):
    """Keyword-match zone notes → named signals. Fallback for cron writers
    that populate zones[].notes but not trackers[].active_signals directly.

    Mutates state["trackers"][zone_id]["active_signals"] in place.
    """
    if "trackers" not in state:
        state["trackers"] = {}

    for zone_id, zone_data in state.get("zones", {}).items():
        notes = zone_data.get("notes", "")
        if not notes or len(notes) < 20:
            continue
        notes_lower = notes.lower()
        matched = []
        for signal_name, keywords in ZONE_SIGNAL_KEYWORDS.items():
            if signal_weights is not None and signal_weights.get((zone_id, signal_name), 0) == 0:
                continue
            for kw in keywords:
                if kw in notes_lower:
                    matched.append(signal_name)
                    break
        if matched:
            state["trackers"].setdefault(zone_id, {})
            existing = set(state["trackers"][zone_id].get("active_signals", []))
            existing.update(matched)
            state["trackers"][zone_id]["active_signals"] = sorted(existing)
            if "current_probability" not in state["trackers"][zone_id]:
                state["trackers"][zone_id]["current_probability"] = zone_data.get("current_prob", 0)
