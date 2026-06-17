# Session State

## DoomsdayWatch morning deep scan — 18:13Z
- Ran scheduled deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch`; restored missing tracked `data/tracker_config.json` from `HEAD` before acting, then used its canonical 13 tracker IDs/signals only.
- Source caveat: Tavily-backed `web_search` failed HTTP 432 for required zone queries; fallback used Google News RSS past-24h scans, targeted 7d crosschecks, terminal HTTP official/source probes, UN Press/UN News RSS, NATO/EIA/OPEC/Polymarket/Reuters checks, and deploy-time OilPriceAPI/Polymarket refresh. IAEA/OPEC returned 403; Reuters world returned 401.
- Updated `data/current_state.json` atomically; no command-deck UI files were hand-edited before deploy. `scripts/deploy.sh` rebuilt dashboard, refreshed energy/Polymarket, committed, and pushed.
- Final dashboard global: **63% / imminent**; deploy commit `a86aa42` (`Update 2026-06-17T18:10:52Z — automated`).
- Core coupled probabilities: Iran Nuclear 60, Iran War 38, Israel-Lebanon 98, Turkey 5, India 10, Russia-NATO 53, China-Taiwan 20, DPRK 5, Russia-Ukraine 98, Pakistan-Afghanistan 98, Sudan 55, Israel-Palestine 85, South Sudan-Abyei 8.
- Top movers vs 15:10Z: no numeric probability changes. Qualitative watch: Lebanon still the sharpest regional spoiler; Hormuz remains mixed rather than full-stop; DPRK fresh-timestamp missile headline rejected as stale after crosscheck; Pakistan-Afghanistan remains severe but relies mainly on regional/syndicated 7d coverage.
- Market sanity: OilPriceAPI refreshed at `2026-06-17T18:10:49Z` with Brent $79.20, WTI $76.44, Gold $4324.20, Natural Gas $3.15; Polymarket cache refreshed at `2026-06-17T18:12:49Z`, worst divergence still `russia_ukraine` ~97.5pp.
- Verification passed: `current_state.json` valid; local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean after deploy.

Related: [[../Projects/nuke-watch/README]] · [[../Projects/DoomsdayWatch/README]]
