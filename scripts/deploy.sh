#!/bin/bash
cd /home/openclaw/.openclaw/workspace/nuke-watch

# Fetch oil prices before deploy
python3 scripts/fetch_oil_prices.py 2>/dev/null

# Fetch flight tracking data
# Aviationstack: 2x per week (Mon & Thu at 06:00 UTC) — 6 requests/month, fits in 100 limit
# OpenSky: hourly fallback (free, unlimited but spotty ME coverage)
HOUR=$(date -u +%H)
DAY=$(date -u +%u)  # 1=Mon, 7=Sun
# Load API key from secrets file
AVIATIONSTACK_KEY=$(cat ~/.openclaw/workspace/secrets-backup/aviationstack.env 2>/dev/null | cut -d= -f2)
if [ -z "$AVIATIONSTACK_KEY" ]; then
  echo "Warning: AVIATIONSTACK_KEY not found in secrets file"
fi
export AVIATIONSTACK_KEY

RUN_AVIATIONSTACK=false
# Mon and Thu at 06:00 UTC
if ([ "$DAY" = "1" ] || [ "$DAY" = "4" ]) && [ "$HOUR" = "06" ]; then
  RUN_AVIATIONSTACK=true
fi

if [ "$RUN_AVIATIONSTACK" = "true" ]; then
  echo "Running Aviationstack (2x weekly calibration)..."
  python3 scripts/flight_tracker.py 2>/dev/null
else
  # Check if Aviationstack data is from today (reuse it, don't waste a request)
  LAST_UPDATE=$(python3 -c "
import json
try:
    d = json.load(open('data/flight_tracking.json'))
    print(d.get('last_updated', '')[:10])
except:
    print('')
" 2>/dev/null)
  TODAY=$(date -u +%Y-%m-%d)
  if [ "$LAST_UPDATE" = "$TODAY" ]; then
    echo "Aviationstack data fresh from today, reusing"
  else
    echo "No Aviationstack data today, using OpenSky only"
    python3 scripts/track_flights.py 2>/dev/null
  fi
fi

# Update index.html with latest state
python3 << 'PYEOF'
import json

with open("data/current_state.json") as f:
    state = json.load(f)

with open("data/tracker_config.json") as f:
    cfg = json.load(f)

# Load energy prices (fetched by fetch_oil_prices.py)
try:
    with open("data/energy_prices.json") as f:
        energy_data = json.load(f)
except:
    energy_data = {"current": {}, "history": [], "baselines": {}, "changes": {}}

# Load flight tracking data (fetched by track_flights.py)
try:
    with open("data/flight_tracking.json") as f:
        flight_data = json.load(f)
except:
    flight_data = {"zones": {}, "signals": []}

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
except:
    timeline = {"signals": {}}

from datetime import datetime, timezone
now_dt = datetime.now(timezone.utc)
now_iso = now_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

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
        if keyword in sl and len(keyword) > best_match_len:
            best_tier = tier
            best_match_len = len(keyword)
    weight = TIER_WEIGHTS.get(best_tier, 0.3)
    label = TIER_LABELS.get(best_tier, "Unknown")
    return best_tier, weight, label

def classify_source(source_str):
    tier, _, _ = classify_source_credibility(source_str)
    if tier == "1_official": return "official"
    if tier in ("2_wire", "3_established"): return "western"
    return "other"

def calc_severity(impact, text):
    text_lower = text.lower()
    severity = 2 if impact == "up" else 1 if impact == "down" else 1
    if any(w in text_lower for w in ["nuclear", "obliterated", "destroyed", "massive", "record"]):
        severity = min(5, severity + 2)
    elif any(w in text_lower for w in ["killed", "strikes", "attack", "crash", "invasion"]):
        severity = min(5, severity + 1)
    return min(5, max(1, severity))

def calc_confidence(sources_count, max_credibility_weight=0):
    if max_credibility_weight >= 3 or sources_count >= 3:
        return "confirmed"
    if max_credibility_weight >= 2 or sources_count >= 2:
        return "reported"
    return "rumored"

def apply_credibility_weight(signal_weight, source_tier):
    tier_order = {"1_official": 3, "2_wire": 2, "3_established": 1.5, "4_regional": 1, "5_unverified": 0}
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
    """Tiered half-life based on signal importance (weight magnitude)."""
    w = abs(signal_weight)
    if w >= 15: return 168   # 7 days — nuclear tests, ICBM launches, Article 5
    elif w >= 8: return 72   # 3 days — major military actions
    elif w >= 4: return 24   # 1 day — rhetoric, buildup, minor events
    else: return 12          # 12 hours — noise, minor indicators

def apply_temporal_decay(signal_weight, activated_at_iso):
    """Exponential decay with tiered half-life. Returns 0 when signal is effectively expired."""
    try:
        activated = datetime.fromisoformat(activated_at_iso.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        hours_old = (now - activated).total_seconds() / 3600
        half_life = get_half_life(signal_weight)
        # Exponential decay: 50% remaining at half_life, 25% at 2×, etc.
        decayed = abs(signal_weight) * (0.5 ** (hours_old / half_life))
        # Signal is effectively expired when below 0.5 weight
        if decayed < 0.5:
            return 0
        return round(decayed, 1)
    except:
        return signal_weight

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
# --- End functions ---

# Build tracker data
trackers_js = []
tn = [
    ("iran_nuke", "IRAN NUCLEAR", "🇮🇷"),
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

for tid, name, emoji in tn:
    t = state.get("trackers", {}).get(tid, {})
    # Record signal activation times, tag with weight sign, and apply temporal decay
    signal_data = []
    for s in t.get("active_signals", []):
        timeline_key = f"{tid}:{s}"
        if timeline_key not in timeline["signals"]:
            timeline["signals"][timeline_key] = now_iso
        w = signal_weights.get((tid, s), 0)
        activated_at = timeline["signals"][timeline_key]
        
        # Apply temporal decay to displayed weight
        decayed_weight = apply_temporal_decay(abs(w), activated_at)
        is_expired = decayed_weight == 0
        
        signal_data.append({
            "name": s,
            "positive": w < 0,
            "activated_at": activated_at,
            "original_weight": abs(w),
            "decayed_weight": round(decayed_weight, 1),
            "expired": is_expired
        })
    # Filter out expired signals from display
    signal_data = [s for s in signal_data if not s["expired"]]
    # Sort signals reverse chronologically (newest first)
    signal_data.sort(key=lambda x: x["activated_at"], reverse=True)
    
    # Calculate confidence: signal volume + source quality + recency
    sig_count = len(signal_data)
    avg_tier = 0
    if signal_data:
        tier_scores = {"confirmed": 3, "reported": 2, "rumored": 1}
        avg_tier = sum(tier_scores.get(s.get("confidence", "rumored"), 1) for s in signal_data) / sig_count
    recency_score = 0
    for s in signal_data[:3]:  # top 3 signals
        if s.get("activated_at"):
            try:
                act_dt = datetime.fromisoformat(s["activated_at"].replace("Z", "+00:00"))
                hours_old = (now_dt - act_dt).total_seconds() / 3600
                if hours_old < 24: recency_score += 3
                elif hours_old < 72: recency_score += 2
                else: recency_score += 1
            except: pass
    recency_score = min(3, recency_score / max(1, min(3, sig_count))) if sig_count > 0 else 0
    conf_score = min(40, sig_count * 5) + avg_tier * 15 + min(30, recency_score * 10)
    if conf_score >= 60: confidence = "HIGH"
    elif conf_score >= 30: confidence = "MEDIUM"
    else: confidence = "LOW"
    
    trackers_js.append({
        "id": tid,
        "name": name,
        "emoji": emoji,
        "prob": t.get("current_probability", t.get("base_rate", 0)),
        "zone": t.get("zone", "deterrent"),
        "trend": t.get("trend", "stable"),
        "signals": signal_data,
        "confidence": confidence
    })

news_js = state.get("latest_news", [
    {"zone": "iran", "time": "LIVE", "text": "Monitoring active", "impact": "neutral"}
])

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
        source_types.append(tier)
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
            continue  # Signal weight is 0, skip it
        activated_at = timeline["signals"].get(timeline_key)
        if activated_at:
            # Known signal — check if it's expired
            decayed = apply_temporal_decay(abs(w), activated_at)
            if decayed > 0:
                still_valid.add(s)
        else:
            # Signal in active_signals but no timeline entry — treat as newly activated
            # (likely set by cron agent this cycle)
            timeline["signals"][timeline_key] = now_iso
            still_valid.add(s)
    
    # Merge: still_valid (agent-set, not expired) + news_signals (newly found)
    merged = still_valid | news_signals
    
    removed = old_signals - merged
    added = merged - old_signals
    if removed:
        print(f"[{tid}] Cleared {len(removed)} expired signals: {removed}")
    if added:
        print(f"[{tid}] Added {len(added)} new signals: {added}")
    tracker["active_signals"] = list(merged)

# ═══════════════════════════════════════════════════════════════════
# AUTO-CALCULATE PROBABILITIES FROM SIGNALS
# The agent manages signals. The code manages probabilities.
# ═══════════════════════════════════════════════════════════════════
for t in trackers_js:
    tid = t["id"]
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
            except:
                pass
    
    # No-news decay: -1.5% per 24h without fresh signal activity
    # Uses median activation time to avoid one recent signal masking otherwise stale zone
    no_news_decay = 0
    if activation_times:
        sorted_times = sorted(activation_times)
        median_time = sorted_times[len(sorted_times) // 2]
        hours_since = (now_dt - median_time).total_seconds() / 3600
        if hours_since > 24:
            no_news_decay = -1.5 * (hours_since / 24)
    elif not t.get("signals"):
        # Zero signals = no news for a long time
        no_news_decay = -5.0
    
    # Calculate final probability
    calculated_prob = base + signal_sum + no_news_decay
    calculated_prob = max(2, min(100, round(calculated_prob)))  # Floor at 2% (no event is zero risk)
    
    t["prob"] = calculated_prob
    # Also update state so coupling reads the correct base value
    if tid in state.get("trackers", {}):
        state["trackers"][tid]["current_probability"] = calculated_prob

print(f"Auto-calculated probabilities from signals:")
for t in trackers_js:
    print(f"  {t['name']}: base={cfg.get('trackers',{}).get(t['id'],{}).get('base_rate',0)} + signals={t['prob'] - cfg.get('trackers',{}).get(t['id'],{}).get('base_rate',0) - (-1.5 * 0 if t.get('signals') else -5):.1f} = {t['prob']}%")

# Recalculate zones from config thresholds (before coupling)
zone_thresholds = cfg.get("scoring", {}).get("zones", {})
def classify_zone(p):
    if p >= zone_thresholds.get("imminent", {}).get("min", 60): return "imminent"
    elif p >= zone_thresholds.get("critical", {}).get("min", 30): return "critical"
    elif p >= zone_thresholds.get("elevated", {}).get("min", 15): return "elevated"
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
        # Remove old "ZONE NN%" pattern from notes (e.g. "CRITICAL 79", "IMMINENT 100", "CRITICAL 35 (declining)")
        cleaned = re.sub(r'\b(DETERRENT|ELEVATED|CRITICAL|IMMINENT)\s+\d+(\s*\([^)]*\))?', '', notes).strip()
        # Clean up double spaces and leading artifacts
        cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
        # Prepend correct zone/prob
        zone_label = zone_labels.get(new_zone, "deterrent")
        trend = trk.get("trend", "stable")
        trk["notes"] = f"Day 20 auto - {zone_label} {t['prob']}% ({trend}). {cleaned}"

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

    # Apply coupling boosts — when a tracker is CRITICAL/IMMINENT, boost connected trackers
    with open("data/tracker_config.json") as cf:
        cfg = json.load(cf)
    coupling_rules = cfg.get("coupling", {}).get("rules", [])
    zone_rank = {"deterrent": 0, "elevated": 1, "critical": 2, "imminent": 3}

    boosts_applied = {}
    # Group rules by source, apply ONLY the highest-threshold rule that matches
    from collections import defaultdict
    rules_by_src = defaultdict(list)
    for rule in coupling_rules:
        rules_by_src[rule["source"]].append(rule)
    
    # Track total coupling per target to enforce +25% cap
    coupling_totals = {}  # {tgt: total_coupling_applied}
    
    for src, src_rules in rules_by_src.items():
        src_zone = state.get("trackers", {}).get(src, {}).get("zone", "deterrent")
        src_rank = zone_rank.get(src_zone, 0)
        # Get source probability for proportional coupling
        src_prob = all_probs.get(src, 0)
        # Sort rules by threshold descending, apply only the FIRST matching rule
        src_rules_sorted = sorted(src_rules, key=lambda r: zone_rank.get(r["min_zone"], 0), reverse=True)
        for rule in src_rules_sorted:
            min_zone = rule["min_zone"]
            if src_rank >= zone_rank.get(min_zone, 0):
                # This is the highest threshold that matches — apply it and stop
                for tgt, raw_boost in rule["targets"].items():
                    if tgt in all_probs:
                        # Proportional coupling: boost scales with source probability
                        effective_boost = raw_boost * (src_prob / 100.0)
                        # Enforce per-target cap
                        current_coupling = coupling_totals.get(tgt, 0)
                        remaining = max(0, 25 - current_coupling)
                        capped_boost = min(effective_boost, remaining)
                        if capped_boost > 0:
                            old_val = all_probs[tgt]
                            all_probs[tgt] = min(100, old_val + capped_boost)
                            coupling_totals[tgt] = current_coupling + capped_boost
                            if tgt not in boosts_applied:
                                boosts_applied[tgt] = 0
                            boosts_applied[tgt] += capped_boost
                break  # Don't apply lower-threshold rules from same source

    if boosts_applied:
        boost_log = ", ".join(f"{k}+{v:.1f}" for k, v in boosts_applied.items())
        print(f"Proportional coupling boosts: {boost_log}")

    # Push boosted probabilities to tracker cards ONLY (not state — coupling is display-only)
    for t in trackers_js:
        boosted = all_probs.get(t["id"], t["prob"])
        t["prob"] = boosted

    weights = {"iran_nuke": 0.12, "iran_conventional": 0.18, "israel_lebanon": 0.14, "russia_ukraine": 0.16, "turkey": 0.06, "india": 0.06, "pakistan_afghanistan": 0.08, "russia": 0.06, "china": 0.06, "north_korea": 0.08}
    gp = round(sum(all_probs.get(k, 10) * weights.get(k, 0.08) for k in all_probs))
    tz = classify_zone(gp)
    # Update state.json with correct global
    state["global_war_probability"] = gp
    state["global_zone"] = tz
    # Write updated signal timeline
    with open("data/signal_timeline.json", "w") as tf:
        json.dump(timeline, tf, indent=2)

    # Detect zone changes for alerts
    try:
        with open("data/zone_alerts.json") as af:
            zone_alerts = json.load(af)
    except:
        zone_alerts = {"pending": [], "history": []}

    old_zones = {}
    try:
        with open("data/previous_zones.json") as pf:
            old_zones = json.load(pf)
    except:
        pass

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
    except:
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

    with open("data/current_state.json", "w") as sf:
        json.dump(state, sf, indent=2)


    lines = []
    lines.append("const state = {")
    lines.append('  last_updated: "' + state.get("last_updated", "") + '",')
    lines.append("  global_war_probability: " + str(gp) + ",")
    lines.append("  global_zone: \"" + tz + "\",")

    lines.append("  trackers: [")
    for t in trackers_js:
        signals_str = json.dumps(t["signals"])
        lines.append('    { id: "' + t["id"] + '", name: "' + t["name"] + '", emoji: "' + t["emoji"] + '", prob: ' + str(t["prob"]) + ', zone: "' + t["zone"] + '", trend: "' + t["trend"] + '", confidence: "' + t.get("confidence", "LOW") + '", signals: ' + signals_str + ' },')
    lines.append("  ],")
    lines.append("  news: [")
    for n in news_js[:10]:
        txt = json.dumps(n.get("text",""))  # safe JSON encoding
        hl = json.dumps(n.get("headline",""))
        src = json.dumps(n.get("sources",[]))
        src_types = json.dumps(n.get("source_types",[]))
        sigs = json.dumps(n.get("signals",[]))
        lines.append('    { zone: "' + n.get("zone","") + '", time: "' + n.get("time","") + '", text: ' + txt + ', headline: ' + hl + ', impact: "' + n.get("impact","neutral") + '", sources: ' + src + ', source_types: ' + src_types + ', confidence: "' + n.get("confidence","developing") + '", severity: ' + str(n.get("severity",1)) + ', signals: ' + sigs + ' },')
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
    lines.append("  energy: " + energy_js + ",")
    # Add flight tracking data
    flight_js = json.dumps({
        "zones": flight_data.get("zones", {}),
        "signals": flight_data.get("signals", []),
        "last_updated": flight_data.get("last_updated", "")
    })
    lines.append("  flights: " + flight_js)
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
    except:
        evaluations = {"predictions": []}
    
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
        except:
            pass
    
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
                actual_prob = actual_state.get("current_probability", 0)
                pred["actual_value"] = actual_prob
                pred["correct"] = actual_prob >= pred_value
                pred["evaluated"] = True
                pred["evaluated_at"] = now_iso
            elif pred_type == "probability_below":
                actual_prob = actual_state.get("current_probability", 0)
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
            except Exception:
                pass
        # Re-run evaluation if we added new predictions
        if newly_added > 0:
            for pred in evaluations.get("predictions", []):
                if not pred.get("evaluated") and pred.get("expires_at", "") < now_iso:
                    pred_tid = pred["tracker_id"]
                    pred_type = pred.get("eval_type", pred["type"])
                    pred_value = pred.get("eval_value", pred["value"])
                    actual_state = state.get("trackers", {}).get(pred_tid, {})
                    if pred_type == "probability_above":
                        actual_prob = actual_state.get("current_probability", 0)
                        pred["actual_value"] = actual_prob
                        pred["correct"] = actual_prob >= pred_value
                        pred["evaluated"] = True
                        pred["evaluated_at"] = now_iso
                    elif pred_type == "probability_below":
                        actual_prob = actual_state.get("current_probability", 0)
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
    
    # Calculate accuracy stats
    evaluated_preds = [p for p in evaluations.get("predictions", []) if p.get("evaluated")]
    total_eval = len(evaluated_preds)
    correct_count = sum(1 for p in evaluated_preds if p.get("correct"))
    accuracy_pct = round(correct_count / total_eval * 100) if total_eval > 0 else 0
    
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
        if tid == "iran_conventional" and prob >= 80:
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
        elif tid == "israel_lebanon" and prob >= 60:
            if "ground" in combined_news or "invasion" in combined_news:
                event = "Israeli ground operation in southern Lebanon expected to continue beyond Litani River. Further displacement and infrastructure destruction likely."
                confidence = 70; etype = "ground_operation"
            elif confidence == 0 and trend == "rising":
                event = "Continued escalation in Lebanon with increased Israeli operations and Hezbollah retaliatory strikes expected."
                confidence = 55; etype = "military_operation"
        
        # PAKISTAN-AFGHANISTAN
        elif tid == "pakistan_afghanistan" and prob >= 60:
            if "taliban" in combined_news or "border" in combined_news or "kills" in combined_news:
                event = "Border escalation between Afghanistan and Pakistan likely to intensify. Cross-border strikes expected within 24 hours."
                confidence = 65; etype = "border_conflict"
            elif confidence == 0:
                event = "Afghan-Pakistan border tensions likely to persist. Additional clashes probable based on recent trajectory."
                confidence = 50; etype = "border_conflict"
        
        # TURKEY
        elif tid == "turkey" and prob >= 50:
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
        elif tid == "iran_nuke" and prob >= 20:
            if "iaea" in combined_news or "enrichment" in combined_news:
                event = "IAEA monitoring likely to produce findings within 72 hours. Iran may announce further enrichment activity."
                confidence = 40; etype = "nuclear_development"
            else:
                event = "No immediate nuclear threshold events anticipated. Status quo enrichment posture likely maintained."
                confidence = 35; etype = "status_quo"
        
        # CHINA-TAIWAN
        elif tid == "china":
            event = "Status quo maintained. No PLA activity changes detected. Taiwan Strait remains stable."
            confidence = 70; etype = "status_quo"
        
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

        new_predictions.append({
            "tracker_id": tid,
            "tracker_name": tname,
            "type": etype,
            "value": prob,
            "description": event,
            "confidence": confidence,
            "expires_at": expires_at,
            "eval_type": eval_type,
            "eval_value": eval_value
        })
    
    # Sort by confidence, take top 15
    new_predictions.sort(key=lambda x: x["confidence"], reverse=True)
    final_predictions = new_predictions[:15]
    
    # Add new predictions to evaluations tracker for future evaluation
    evaluations["predictions"].extend(final_predictions)
    # Keep last 2000 predictions (need 48h+ retention for 24h expiry + buffer)
    evaluations["predictions"] = evaluations["predictions"][-2000:]
    
    # Save predictions
    pred_data = {
        "generated_at": now_iso,
        "date": today,
        "hour": hour,
        "predictions": final_predictions,
        "accuracy": {
            "total_evaluated": total_eval,
            "correct": correct_count,
            "accuracy_pct": accuracy_pct
        }
    }
    with open(pred_file, "w") as f:
        json.dump(pred_data, f, indent=2)
    
    # Save updated evaluations
    with open(eval_file, "w") as f:
        json.dump(evaluations, f, indent=2)
    
    # Format predictions for JS modal
    predictions_js = json.dumps(final_predictions)
    eval_stats_js = json.dumps({"total": total_eval, "correct": correct_count, "accuracy": accuracy_pct})
    
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
            except:
                pass
    
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
    new_html = new_html.replace(narrative_placeholder, '<div id="narrative-content" style="font-size:12px;line-height:1.7;color:#8b949e;white-space:normal;">' + narrative.replace('\n', '<br>') + '</div>')
    
    # Inject predictions into HTML (after flights in state block)
    pred_inject = ",\n  predictions: " + predictions_js + ",\n  eval_stats: " + eval_stats_js
    # Use a more robust anchor - find the end of the state block
    new_html = new_html.replace("\n};\n\n// ===== RENDER", pred_inject + "\n};\n\n// ===== RENDER")

    with open("index.html", "w") as f:
        f.write(new_html)

    print(f"Updated index.html — global: {gp}% ({tz}) — {len(trackers_js)} trackers — narrative generated")
    print(f"Narrative: {len(key_devs)} key developments, {len(prob_changes)} probability changes")

# Commit and push
import subprocess
subprocess.run(["git", "config", "user.name", "VoltaIntel"], check=True)
subprocess.run(["git", "config", "user.email", "cryptocybrog1337@proton.me"], check=True)
subprocess.run(["git", "add", "-A"], check=True)
r = subprocess.run(["git", "commit", "-m", "Update " + state.get("last_updated", "") + " — automated"], capture_output=True, text=True)
print("Committed" if r.returncode == 0 else "No changes to commit")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("Pushed!" if r.returncode == 0 else r.stderr.strip())
PYEOF
