#!/bin/bash
cd /home/openclaw/.openclaw/workspace/nuke-watch

# Update index.html with latest state
python3 << 'PYEOF'
import json

with open("data/current_state.json") as f:
    state = json.load(f)

with open("data/tracker_config.json") as f:
    cfg = json.load(f)

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
now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Build tracker data
trackers_js = []
tn = [
    ("iran_nuke", "IRAN NUCLEAR", "🇮🇷"),
    ("iran_conventional", "IRAN WAR", "⚔️"),
    ("israel_lebanon", "ISRAEL-LEBANON", "🇱🇧"),
    ("turkey", "TURKEY", "🇹🇷"),
    ("india", "INDIA-PAKISTAN", "🇮🇳"),
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
    # Record signal activation times and tag with weight sign
    signal_data = []
    for s in t.get("active_signals", []):
        timeline_key = f"{tid}:{s}"
        if timeline_key not in timeline["signals"]:
            timeline["signals"][timeline_key] = now_iso
        w = signal_weights.get((tid, s), 0)
        signal_data.append({
            "name": s,
            "positive": w < 0,
            "activated_at": timeline["signals"][timeline_key]
        })
    # Sort signals reverse chronologically (newest first)
    signal_data.sort(key=lambda x: x["activated_at"], reverse=True)
    trackers_js.append({
        "id": tid,
        "name": name,
        "emoji": emoji,
        "prob": t.get("current_probability", t.get("base_rate", 0)),
        "zone": t.get("zone", "deterrent"),
        "trend": t.get("trend", "stable"),
        "signals": signal_data
    })

news_js = state.get("latest_news", [
    {"zone": "iran", "time": "LIVE", "text": "Monitoring active", "impact": "neutral"}
])

# Source type classification
SOURCE_TYPES = {
    "western": ["reuters", "apnews", "ap news", "bbc", "nytimes", "new york times",
                "washington post", "theguardian", "guardian", "cbs", "politico", "cnn", "fox",
                "bloomberg", "cnbc", "axios", "wapo", "afp", "getty", "wp ", "jpost",
                "israeli news", "times of israel", "japan times", "the hindu", "isw", "aei"],
    "arabic": ["aljazeera", "al jazeera", "middleeasteye", "middle east eye",
               "farsnews", "fars", "al arabiya", "alarabiya", "sabreen", "al araby",
               "iraq news", "iran international", "isna", "irna", "tasnim"],
    "russian": ["tass", "rt.com", "ria novosti", "interfax", "sputnik", "izvestia", "kommersant"],
    "chinese": ["scmp", "south china", "xinhua", "global times", "cgtn", "china daily", "sixth tone"],
    "israeli": ["timesofisrael", "times of israel", "haaretz", "jerusalem post",
                "jpost", "ynet", "israel hayom", "maariv"],
    "official": ["nato", "pentagon", "white house", "kremlin", "un ", "iaea", "doe",
                 "state dept", "downing street", "eyelyse palace", "bundestag", "kremlin.ru",
                 "iran health ministry", "jcs", "idf"],
}

def classify_source(source_str):
    sl = source_str.lower()
    for stype, keywords in SOURCE_TYPES.items():
        for kw in keywords:
            if kw in sl:
                return stype
    return "other"

def find_matching_signals(text, tid):
    """Find which signals this news article likely triggered based on keywords."""
    text_lower = text.lower()
    matched = []
    for sname, scfg in cfg.get("trackers", {}).get(tid, {}).get("signals", {}).items():
        desc = scfg.get("description", "").lower()
        # Use signal name (converted to readable form) as primary match
        name_readable = sname.lower().replace("_", " ")
        if name_readable in text_lower:
            weight = signal_weights.get((tid, sname), 0)
            matched.append({"name": sname, "weight": weight})
            continue
        # Extract 2+ key phrases from description (4+ chars)
        terms = [t for t in desc.replace("(", "").replace(")", "").replace(",", "").replace(".", "").split() if len(t) > 4]
        matches = sum(1 for t in set(terms) if t in text_lower)
        if matches >= 3:
            weight = signal_weights.get((tid, sname), 0)
            matched.append({"name": sname, "weight": weight})
    return matched

def calc_severity(impact, text):
    """Calculate 1-5 severity based on impact and keywords."""
    text_lower = text.lower()
    severity = 2 if impact == "up" else 1 if impact == "down" else 1
    # Boost for major keywords
    if any(w in text_lower for w in ["nuclear", "obliterated", "destroyed", "massive", "record"]):
        severity = min(5, severity + 2)
    elif any(w in text_lower for w in ["killed", "strikes", "attack", "crash", "invasion"]):
        severity = min(5, severity + 1)
    return min(5, max(1, severity))

def calc_confidence(sources_count):
    """Confidence tier based on number of independent sources."""
    if sources_count >= 3: return "confirmed"
    if sources_count >= 2: return "reported"
    return "developing"

# Enrich news items
enriched_news = []
for n in news_js[:10]:
    sources = []
    if isinstance(n.get("source"), str):
        sources = [s.strip() for s in n["source"].split("/")]
    elif isinstance(n.get("sources"), list):
        sources = n["sources"]
    elif isinstance(n.get("source"), list):
        sources = n["source"]

    source_types = list(set(classify_source(s) for s in sources))
    full_text = (n.get("headline", "") + " " + n.get("text", ""))
    zone = n.get("zone", "")
    zone_signals = find_matching_signals(full_text, zone) if zone else []

    enriched_news.append({
        "zone": zone,
        "time": n.get("time", ""),
        "text": n.get("text", n.get("headline", "")),
        "headline": n.get("headline", ""),
        "impact": n.get("impact", "neutral"),
        "sources": sources,
        "source_types": source_types,
        "confidence": calc_confidence(len(sources)),
        "severity": calc_severity(n.get("impact", "neutral"), full_text),
        "signals": zone_signals
    })

news_js = enriched_news

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
    for rule in coupling_rules:
        src = rule["source"]
        src_zone = state.get("trackers", {}).get(src, {}).get("zone", "deterrent")
        min_zone = rule["min_zone"]
        if zone_rank.get(src_zone, 0) >= zone_rank.get(min_zone, 0):
            for tgt, boost in rule["targets"].items():
                if tgt in all_probs:
                    old_val = all_probs[tgt]
                    all_probs[tgt] = min(100, old_val + boost)
                    if tgt not in boosts_applied:
                        boosts_applied[tgt] = 0
                    boosts_applied[tgt] += boost

    if boosts_applied:
        boost_log = ", ".join(f"{k}+{v}" for k, v in boosts_applied.items())
        print(f"Coupling boosts applied: {boost_log}")

    # Push boosted probabilities to tracker cards ONLY (not state — coupling is display-only)
    for t in trackers_js:
        boosted = all_probs.get(t["id"], t["prob"])
        t["prob"] = boosted

    weights = {"iran_nuke": 0.14, "iran_conventional": 0.20, "israel_lebanon": 0.16, "russia_ukraine": 0.18, "turkey": 0.07, "india": 0.08, "russia": 0.07, "china": 0.06, "north_korea": 0.07}
    gp = round(sum(all_probs.get(k, 10) * weights.get(k, 0.08) for k in all_probs))
    if gp >= 60: tz = "imminent"
    elif gp >= 30: tz = "critical"
    elif gp >= 15: tz = "elevated"
    else: tz = "deterrent"
    # Update state.json with correct global
    state["global_war_probability"] = gp
    state["global_zone"] = tz
    # Write updated signal timeline
    with open("data/signal_timeline.json", "w") as tf:
        json.dump(timeline, tf, indent=2)

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
        "trackers": {t["id"]: t["prob"] for t in trackers_js}
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
        lines.append('    { id: "' + t["id"] + '", name: "' + t["name"] + '", emoji: "' + t["emoji"] + '", prob: ' + str(t["prob"]) + ', zone: "' + t["zone"] + '", trend: "' + t["trend"] + '", signals: ' + signals_str + ' },')
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
    lines.append("};")
    lines.append("")
    lines.append("// ===== RENDER")

    new_state = "\n".join(lines)
    new_html = html[:start] + new_state + html[end:]

    with open("index.html", "w") as f:
        f.write(new_html)

    print(f"Updated index.html — global: {gp}% ({tz}) — {len(trackers_js)} trackers")

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
