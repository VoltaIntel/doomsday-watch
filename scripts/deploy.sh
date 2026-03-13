#!/bin/bash
cd /home/openclaw/.openclaw/workspace/nuke-watch

# Update index.html with latest state
python3 << 'PYEOF'
import json

with open("data/current_state.json") as f:
    state = json.load(f)

with open("dashboard.html") as f:
    html = f.read()

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
    trackers_js.append({
        "id": tid,
        "name": name,
        "emoji": emoji,
        "prob": t.get("current_probability", t.get("base_rate", 0)),
        "zone": t.get("zone", "deterrent"),
        "trend": t.get("trend", "stable"),
        "signals": t.get("active_signals", [])
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
    lines = []
    lines.append("const state = {")
    lines.append('  last_updated: "' + state.get("last_updated", "") + '",')
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

    gp = state.get("global_war_probability", "?")
    tz = state.get("global_zone", "?")
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
