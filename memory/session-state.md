# Nuke Watch Session State

Updated: 2026-06-19T21:10:28Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `c987787` (`Update 2026-06-19T20:59:30Z — automated`).
- Final deployed dashboard: **59% / imminent**; raw/coupled global in state: **58.86% / 59**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 93, `israel_palestine` 87, `sudan` 49, `iran_nuclear` 43, `russia_nato` 50, `iran_conventional` 28.
- Main mover vs prior saved state: Iran Nuclear **41→43**; global stayed 59. Pakistan-Afghanistan remained 93; Israel-Lebanon/Russia-Ukraine stayed pinned at 100/98.
- Signal hygiene: canonical-only check clean. Removed false/unsupported `iran_nuclear:iaea_access_denied`; final Iran nuclear active signals are `iaea_emergency` only.
- Source caveat: `web_search`/Tavily unavailable with HTTP 432; used Google News RSS, terminal HTTP/direct-source probes, UN/NATO/EIA/OilPriceAPI/Polymarket fallbacks. IAEA/OPEC direct pages blocked 403; Reuters world direct probe blocked/401.
- Market sanity: OilPriceAPI refreshed during deploy (Brent about $80.38, WTI about $77.52, gas $3.28, gold about $4156.56); Polymarket cache refreshed at `2026-06-19T20:59:55Z`.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON files valid; deploy/push succeeded.

## Watch next
- Iran/IAEA: verify whether monitoring/inspection access is actually granted; do not re-add access-denial signal from disputed or negated headlines.
- Hormuz/oil: watch for physical closure, mining, tanker incidents, or Brent/WTI gap shock.
- Israel-Lebanon: distinguish real diplomacy from generic truce/ceasefire wording; ceasefire violations remain active.
- Pakistan-Afghanistan and Sudan: require multi-source corroboration before moving toward ceiling again.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
