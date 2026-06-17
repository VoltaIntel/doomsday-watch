# Session State

## DoomsdayWatch morning deep scan — 2026-06-16 21:08Z
- Ran scheduled morning deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch` using canonical tracker IDs/signals from `data/tracker_config.json`.
- Source caveat: Tavily-backed `web_search` failed HTTP 432 for required zone queries; fallback used Google News RSS past-24h scans, 7d sparse-zone crosschecks, terminal HTTP probes of UN Press/NATO/EIA/OilPriceAPI/Polymarket, and direct official-page probes. IAEA direct news/press returned 403; OPEC news returned 403.
- Updated `data/current_state.json` and `data/signal_timeline.json` atomically; no command-deck UI files were hand-edited.
- Deployed through `bash scripts/deploy.sh`; dashboard deploy commit `da76271` (`Update 2026-06-16T21:06:48Z — automated`) pushed.
- Final dashboard global: **64% / imminent**. Coupled probabilities: Iran Nuclear 64, Iran War 30, Israel-Lebanon 91, Turkey 5, India 10, Russia-NATO 53, China-Taiwan 25, DPRK 34, Russia-Ukraine 98, Pakistan-Afghanistan 98, Sudan 56, Israel-Palestine 85, South Sudan-Abyei 8.
- Top movers vs 18:06Z: China 26→25 and Israel-Palestine 86→85; global unchanged at 64. Pakistan-Afghanistan and Russia-Ukraine remain pinned at 98; Lebanon remains the main regional spoiler.
- Active canonical signals after deploy: Iran Nuclear `diplomacy_active`, `enrichment_60`, `iaea_emergency`; Iran War `diplomacy_active`; Israel-Lebanon `ceasefire_violation`, `diplomacy_active`; Russia-NATO `nuclear_rhetoric_official`; China `military_buildup`; Russia-Ukraine `military_buildup`; Pakistan-Afghanistan `military_buildup`; Sudan `external_backing`, `military_buildup`; Israel-Palestine `ceasefire_violation`, `diplomacy_active`, `military_buildup`.
- Market sanity: OilPriceAPI refreshed at `2026-06-16T21:06:47Z` with Brent $79.45 and WTI $76.59, both down on 24h; Polymarket cache refreshed at `2026-06-16T21:07:51Z`, worst divergence `russia_ukraine` ~97.54pp.
- Verification passed: canonical active-signal check clean; local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; git status clean after push.
