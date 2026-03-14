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
        lines.append('    { zone: "' + n.get("zone","") + '", time: "' + n.get("time","") + '", text: "' + n.get("text","").replace('"',"'") + '", impact: "' + n.get("impact","neutral") + '" },')
    lines.append("  ]")
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
