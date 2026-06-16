# Session State

## DoomsdayWatch morning deep scan — 2026-06-16 18:06Z
- Ran the scheduled morning deep scan from `/home/openclaw/.openclaw/workspace/nuke-watch` using canonical tracker IDs/signals from `data/tracker_config.json`.
- Source caveat: Tavily-backed `web_search`/`web_extract` remained degraded/failing HTTP 432; fallback used Google News RSS past-24h scans, terminal HTTP official/source probes, UN Press/NATO/EIA checks, OilPriceAPI energy refresh, and deploy-time Polymarket Gamma refresh. IAEA official pages returned 403.
- Updated `data/current_state.json` and `data/signal_timeline.json` atomically; no command-deck UI files were hand-edited before deploy.
- Deployed through `bash scripts/deploy.sh`; dashboard deploy commit `e4b221b` (`Update 2026-06-16T18:05:56Z — automated`) pushed.
- Final dashboard global: **64% / imminent**. Coupled probabilities: Iran Nuclear 64, Iran War 30, Israel-Lebanon 91, Turkey 5, India 10, Russia-NATO 53, China-Taiwan 26, DPRK 34, Russia-Ukraine 98, Pakistan-Afghanistan 98, Sudan 56, Israel-Palestine 86, South Sudan-Abyei 8.
- Top movers vs 15:08Z: Iran Nuclear 65→64, Israel-Lebanon 89→91; global unchanged at 64. Pakistan-Afghanistan and Russia-Ukraine remain pinned at 98; oil/Hormuz remains lower than prior peak but coupling keeps Iran conventional critical.
- Active canonical signals after deploy: Iran Nuclear `diplomacy_active`, `enrichment_60`, `iaea_emergency`; Iran War `diplomacy_active`; Israel-Lebanon `ceasefire_violation`, `diplomacy_active`; Russia-NATO `nuclear_rhetoric_official`; China `military_buildup`; Russia-Ukraine `military_buildup`; Pakistan-Afghanistan `military_buildup`; Sudan `external_backing`, `military_buildup`; Israel-Palestine `ceasefire_violation`, `diplomacy_active`, `military_buildup`.
- Market sanity checks: OilPriceAPI refreshed at `2026-06-16T18:05:55Z`; Brent $78.84, WTI $75.86, Gold $4360.70, Natural Gas $3.23. Polymarket cache refreshed at `2026-06-16T18:06:42Z`; worst divergence `russia_ukraine` ~97.5pp.
- Verification passed: local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; dashboard deploy/push succeeded.
