# Session State

## DoomsdayWatch morning deep scan — 2026-06-18 00:08Z
- Ran scheduled deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch` using canonical 13 tracker IDs/signals from `data/tracker_config.json`.
- Tavily-backed `web_search` failed HTTP 432 for required zone queries; fallback used Google News RSS past-24h scans, targeted 7d sparse-zone crosschecks, terminal HTTP official/source probes, UN Press/UN News RSS, NATO/EIA/OPEC/Polymarket/Reuters checks, and deploy-time OilPriceAPI/Polymarket refresh. IAEA news/press/RSS and OPEC returned 403; Reuters world returned 401.
- Updated `data/current_state.json` atomically; no command-deck UI files were hand-edited before deploy. `scripts/deploy.sh` rebuilt dashboard, refreshed energy/Polymarket, committed, and pushed.
- Final dashboard global: **63% / imminent**; deploy commit `12b03fe` (`Update 2026-06-18T00:06:36Z — automated`).
- Core coupled probabilities: Iran Nuclear 60, Iran War 38, Israel-Lebanon 98, Turkey 5, India 10, Russia-NATO 53, China-Taiwan 20, DPRK 5, Russia-Ukraine 98, Pakistan-Afghanistan 98, Sudan 55, Israel-Palestine 85, South Sudan-Abyei 8.
- Top movers vs 21:05Z: no numeric probability changes. Qualitative reinforcement: Lebanon remains the sharpest regional spoiler; Pakistan-Afghanistan remains severe on 24h evidence; Hormuz/oil moved mixed-to-easing rather than full-stop; Russia-NATO direct-friction uncorroborated beyond Ukraine spillover; DPRK stayed background.
- Market sanity: OilPriceAPI refreshed at `2026-06-18T00:06:35Z` with Brent $78.66, WTI $75.98, Gold $4282.92, Natural Gas $3.16; Polymarket refreshed at `2026-06-18T00:07:41Z`, worst divergence `russia_ukraine` ~97.5pp.
- Verification passed: `current_state.json` valid; canonical active-signal check clean; local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean after deploy.

Related: [[../Projects/nuke-watch/README]] · [[../Projects/DoomsdayWatch/README]]
