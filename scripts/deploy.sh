#!/bin/bash
cd /home/openclaw/.openclaw/workspace/nuke-watch

# Update index.html with latest state
python3 << 'PYEOF'
import json

with open("data/current_state.json") as f:
    state = json.load(f)

with open("dashboard.html") as f:
    html = f.read()

trackers_js = []
tn = {
    "iran_nuke": {"name": "IRAN NUCLEAR", "emoji": "\U0001f1ee\U0001f1f7"},
    "iran_conventional": {"name": "IRAN WAR", "emoji": "\u2694\ufe0f"},
    "israel_lebanon": {"name": "ISRAEL-LEBANON", "emoji": "\U0001f1f1\U0001f1e7"},
    "turkey": {"name": "TURKEY", "emoji": "\U0001f1f9\U0001f1f7"},
    "india": {"name": "INDIA-PAKISTAN", "emoji": "\U0001f1ee\U0001f1f3"},
    "russia": {"name": "RUSSIA-NATO", "emoji": "\U0001f1f7\U0001f1fa"},
    "china": {"name": "CHINA-TAIWAN", "emoji": "\U0001f1e8\U0001f1f3"}
}

for tid, tinfo in tn.items():
    t = state.get("trackers", {}).get(tid, {})
    trackers_js.append({
        "id": tid,
        "name": tinfo["name"],
        "emoji": tinfo["emoji"],
        "prob": t.get("current_probability", t.get("base_rate", 0)),
        "zone": t.get("zone", "deterrent"),
        "trend": t.get("trend", "stable"),
        "signals": t.get("active_signals", [])
    })

news_js = state.get("latest_news", [
    {"zone": "iran", "time": "LIVE", "text": "Monitoring active", "impact": "neutral"}
])

new_state = json.dumps({
    "last_updated": state.get("last_updated", "2026-03-13"),
    "trackers": trackers_js,
    "news": news_js
}, indent=2)

# String replacement instead of regex (avoids unicode escape issues)
start_marker = "const state = {"
end_marker = "// ===== RENDER"
start_idx = html.find(start_marker)
end_idx = html.find(end_marker)
if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + "const state = " + new_state + ";\n\n" + html[end_idx:]

with open("index.html", "w") as f:
    f.write(html)

gp = state.get('global_war_probability', '?')
print(f"Updated index.html — global: {gp}%")
PYEOF

# Commit and push
git config user.name "VoltaIntel"
git config user.email "cryptocybrog1337@proton.me"
git add -A
git commit -m "$(date -u '+%Y-%m-%d %H:%M UTC') — automated update" 2>/dev/null
git push origin main 2>&1 | tail -3
echo "Deployed: https://voltaintel.github.io/doomsday-watch/"
