# Session State

## DoomsdayWatch morning deep scan — 2026-06-16 12:13Z
- Ran the scheduled morning deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch` using canonical tracker IDs/signals from `data/tracker_config.json`.
- Tavily-backed `web_search` failed HTTP 432; fallback used Google News RSS past-24h scans plus 7d empty-zone crosschecks, terminal HTTP official probes, UN Press RSS, OilPriceAPI energy data, and deploy-time Polymarket Gamma refresh. IAEA direct pages returned 403.
- Updated `data/current_state.json` atomically; no command-deck UI files were hand-edited before deploy.
- Deployed through `bash scripts/deploy.sh`; dashboard deploy commit `5e80ac2` (`Update 2026-06-16T12:12:52Z — automated`) pushed.
- Final dashboard global: **65% / imminent**. Coupled probabilities: Iran Nuclear 71, Iran War 30, Israel-Lebanon 91, Turkey 5, India 11, Pakistan-Afghanistan 97, Russia-Ukraine 98, Russia-NATO 55, China-Taiwan 28, DPRK 34, Sudan 58, Israel-Palestine 87, South Sudan-Abyei 8.
- Top movers vs 09:10Z: no probability changes. Narrative movers: Pakistan-Afghanistan remains rising/near-ceiling; South Lebanon spoiler risk persists; oil/energy leans de-escalatory with one uncorroborated severe outlier.
- Verification passed: local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; Polymarket cache fresh at `2026-06-16T12:13:26Z`; git status clean after push.
