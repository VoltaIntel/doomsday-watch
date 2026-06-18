# Session State

## DoomsdayWatch morning deep scan — 2026-06-18 03:08Z
- Ran scheduled morning deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch` using canonical 13 tracker IDs/signals from `data/tracker_config.json`.
- Tavily-backed `web_search` failed HTTP 432 for required zone queries; fallback used Google News RSS past-24h scans, targeted 7d sparse-zone crosschecks, terminal HTTP official/source probes, IAEA/UN/NATO/EIA/OPEC/Polymarket/Reuters checks, and deploy-time OilPriceAPI/Polymarket refresh. IAEA RSS was reachable; IAEA news/press pages and OPEC returned 403; Reuters world returned 401.
- Updated `data/current_state.json` atomically; no command-deck UI files were hand-edited before deploy. `scripts/deploy.sh` rebuilt dashboard, refreshed energy/Polymarket, committed, and pushed.
- Final dashboard global: **62% / imminent**; deploy commit `38e46d1` (`Update 2026-06-18T03:06:20Z — automated`).
- Core coupled probabilities: Iran Nuclear 58, Iran War 36, Israel-Lebanon 98, Turkey 5, India 10, Russia-NATO 53, China-Taiwan 20, DPRK 5, Russia-Ukraine 98, Pakistan-Afghanistan 98, Sudan 52, Israel-Palestine 85, South Sudan-Abyei 8.
- Numeric movers vs 00:06Z: Iran Nuclear 60→58, Iran War 38→36, Sudan 55→52; global 63→62. Qualitative picture: US-Iran preliminary deal and easing oil prices lowered Hormuz/Iran pressure slightly; Lebanon and Pakistan-Afghanistan remain the strongest kinetic lanes; Russia-Ukraine remains pinned; DPRK stayed background.
- Market sanity: OilPriceAPI refreshed at `2026-06-18T03:06:19Z` with Brent $78.53, WTI $75.59, Gold $4329.68, Natural Gas $3.18; Polymarket refreshed at `2026-06-18T03:07:14Z`, worst divergence `russia_ukraine` ~97.5pp.
- Verification passed: `current_state.json` valid; canonical active-signal check clean; local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean after deploy.

Related: [[../Projects/nuke-watch/README]] · [[../Projects/DoomsdayWatch/README]]
