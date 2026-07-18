# Session State

Last update: 2026-07-18T12:14Z

DoomsdayWatch 12Z morning deep scan is in final deployment verification from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Atomic pre-deploy state is complete at **74% / imminent**; weighted coupled score **73.60%**. No tracker probability, global value or canonical signal changed versus 09Z.
- New evidence: multiple Indian outlets report roughly 90 minutes of small-arms fire across the Rajouri LoC with no casualties. It does not establish India’s configured force-concentration threshold, so India holds **11%**.
- CNBC reports a seventh consecutive U.S. strike night, competing U.S./Iranian vessel-interdiction claims and further Gulf infrastructure attacks; Iran remains capped at **100%**. President Aoun departed for Washington after a sixth U.S.-sponsored negotiating round; Israel-Lebanon remains **94% coupled** with its existing political-channel signal.
- Active canonical signals remain `iran_conventional:{ceasefire_violation,hormuz_controlled_not_closed}`, `israel_lebanon:diplomacy_active`, `iran_nuclear:iaea_access_denied`, `south_sudan_abyei:military_buildup`, and `yemen_red_sea:external_backing`.
- No auto-detected crisis qualified. Myanmar/Kachin produced one current operational report; Ethiopia/Tigray headlines were partisan/political rather than a distinct independently corroborated operation.
- OilPriceAPI: Brent **$88.26**, WTI **$82.49**. Gamma sanity: U.S.-Iran invasion **27.5%**, NATO Article 5 **8.0%**, China-Taiwan clash **5.3%**, Iran device **5.15%**; no market value set a tracker probability.
- All **19 Tavily searches** and **5 extracts** failed HTTP 432. Fallback coverage completed via explicit Google News RSS for all 15 trackers, Bing RSS, direct UN/NATO/EIA, browser, terminal HTTP, OilPriceAPI and Gamma. IAEA remains Cloudflare/403; OPEC 403; configured OCHA/UN Sudan paths 404.
- Evidence artifacts: `data/morning_deep_scan_sources_20260718T120219Z.json` and `data/deep_scan_supplement_20260718T120321Z.json`.
- Pre-deploy JSON/canonical checks pass. `bash scripts/deploy.sh`, post-pipeline false-positive review, tests, marker verification and push verification remain pending in this same run.
