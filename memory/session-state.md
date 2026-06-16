# Session State

## DoomsdayWatch morning deep scan — 2026-06-16 09:10Z
- Ran the scheduled morning deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch` using canonical tracker IDs/signals from `data/tracker_config.json`.
- Tavily-backed `web_search`/`web_extract` failed HTTP 432; fallback used Google News RSS, terminal HTTP official probes, UN Press RSS, OilPriceAPI, and deploy-time Polymarket Gamma refresh. IAEA direct pages returned 403.
- Updated `data/current_state.json` atomically; no command-deck UI files were hand-edited before deploy.
- Deployed through `bash scripts/deploy.sh`; dashboard deploy commit `f1c160c` (`Update 2026-06-16T09:09:51Z — automated`) pushed.
- Final dashboard global: **65% / imminent**. Coupled probabilities: Iran Nuclear 71, Iran War 30, Israel-Lebanon 91, Turkey 5, India 11, Pakistan-Afghanistan 97, Russia-Ukraine 98, Russia-NATO 55, China-Taiwan 28, DPRK 34, Sudan 58, Israel-Palestine 87, South Sudan-Abyei 8.
- Top changes vs 06:06Z: India 12→11 and China 29→28; global unchanged at 65. Pakistan-Afghanistan remains the main upward watch item; oil/Hormuz signal leans down.
- Verification passed: local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; canonical active-signal validation clean; Polymarket cache fresh at `2026-06-16T09:10:24Z`.
