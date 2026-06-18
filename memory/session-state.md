# Session State

## DoomsdayWatch morning deep scan — 18:10Z
- Completed scheduled morning deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch` using canonical 13 tracker IDs/signals from `data/tracker_config.json`.
- Tavily-backed `web_search` failed HTTP 432 for required zone queries; fallback used Google News RSS 24h/7d scans, terminal HTTP official/source probes, UN/NATO/EIA/OilPriceAPI/Polymarket, and headline-level crosschecks. IAEA news/press returned 403; OPEC returned 403; Reuters world returned 401; UN News/Press, NATO, EIA, and Polymarket Gamma were reachable.
- Atomically updated `data/current_state.json`; no command-deck UI files were hand-edited before deploy.
- Deployed via `bash scripts/deploy.sh`; deploy refreshed OilPriceAPI and Polymarket, rebuilt dashboard, committed, and pushed `6bc213e` (`Update 2026-06-18T18:10:31Z — automated`).
- Final dashboard global: **58% / imminent**.
- Coupled probabilities: Iran Nuclear 43, Iran War 30, Israel-Lebanon 97, Turkey 5, India 10, Russia-NATO 50, China-Taiwan 19, DPRK 5, Russia-Ukraine 98, Pakistan-Afghanistan 92, Sudan 41, Israel-Palestine 85, South Sudan-Abyei 8.
- Numeric movers vs 15:18Z final/coupled state: global 59→58; Iran Nuclear 45→43; China-Taiwan 20→19; Pakistan-Afghanistan 94→92; Sudan 44→41. Iran conventional, Israel-Lebanon, Russia-NATO, Russia-Ukraine, Gaza/Israel-Palestine, Turkey, India, DPRK, and South Sudan/Abyei held after coupling.
- Signal changes: no intended canonical active-signal additions/removals. Pipeline briefly added `israel_lebanon:diplomacy_active` from broad ceasefire/truce wording; it was removed, wording was neutralized, and the timeline entry was removed before final deploy. No non-canonical signals used.
- Market/source sanity: energy/oil tape remained de-escalatory vs earlier spike; Polymarket Gamma/cache available but used only as horizon-mismatched sanity check. Auto-detection found no untracked emerging crisis meeting tracker-config threshold.
- Verification passed: `current_state.json` valid; canonical active-signal check clean; local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded.

Related: [[../Projects/nuke-watch/README]] · [[../Projects/DoomsdayWatch/README]]
