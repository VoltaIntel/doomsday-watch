# Session State

## DoomsdayWatch morning deep scan — 2026-06-17 00:14Z
- Ran scheduled morning deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch` using canonical tracker IDs/signals from `data/tracker_config.json`.
- Source caveat: Tavily-backed `web_search` failed HTTP 432 for required zone queries and `web_extract` also failed HTTP 432; fallback used Google News RSS past-24h scans, sparse 7d crosschecks, terminal HTTP probes of UN/NATO/EIA/OilPriceAPI/Polymarket and direct official-page probes. IAEA and OPEC official pages returned 403.
- Updated `data/current_state.json` and `data/signal_timeline.json` atomically; no command-deck UI shell files were hand-edited.
- Corrected North Korea false positive: removed `north_korea:missile_range_test`, neutralized negated missile-keyword wording in DPRK notes/news, and reset DPRK to configured base 5% / deterrent because no active canonical signal remains.
- Deployed through `bash scripts/deploy.sh`; dashboard deploy commit `e998e30` (`Update 2026-06-17T00:14:17Z — automated`) pushed.
- Final dashboard global: **62% / imminent**. Coupled probabilities: Iran Nuclear 62, Iran War 34, Israel-Lebanon 94, Turkey 5, India 10, Russia-NATO 55, China-Taiwan 20, DPRK 5, Russia-Ukraine 98, Pakistan-Afghanistan 98, Sudan 55, Israel-Palestine 85, South Sudan-Abyei 8.
- Top movers vs prior automated state: DPRK 34→5 and China-Taiwan 25→20 after DPRK false-positive cleanup removed cross-coupling; global 65→62. Pakistan-Afghanistan and Russia-Ukraine remain pinned at 98; South Lebanon remains the main fresh kinetic spoiler.
- Active canonical signals after deploy: Iran Nuclear `diplomacy_active`, `enrichment_60`, `iaea_emergency`; Iran War `diplomacy_active`, `hormuz_controlled_not_closed`; Israel-Lebanon `ceasefire_violation`, `diplomacy_active`; Russia-NATO `nuclear_rhetoric_official`; China `military_buildup`; Russia-Ukraine `military_buildup`; Pakistan-Afghanistan `military_buildup`; Sudan `external_backing`, `military_buildup`; Israel-Palestine `ceasefire_violation`, `diplomacy_active`, `military_buildup`.
- Market sanity: OilPriceAPI refreshed at deploy with Brent $79.40, WTI $76.52, Gold $4343.27; Polymarket cache refreshed at `2026-06-17T00:14:46Z`, worst divergence remains `russia_ukraine` ~97.5pp.
- Verification passed: `current_state.json` and `signal_timeline.json` JSON-valid; canonical active-signal check clean; local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; git status clean after push.
