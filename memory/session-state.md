# Session State

Last update: 2026-07-18T15:18:46Z

DoomsdayWatch 15Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Global remains **74% / imminent**; weighted coupled score **73.60%**. No numeric tracker moved.
- Canonical `iran_conventional:oil_infrastructure_threat` activated after Kuwait Petroleum Corporation reported repeated Iranian attacks caused injuries and significant damage at a vital oil facility. The realized-war lane remains capped at **100%**.
- AP reports Tehran stopped implementing last month’s interim commitments; DW carried an official warning of full-scale offensive operations if U.S. attacks continue. No other canonical signal changed.
- Active canonical signals are `iran_conventional:{ceasefire_violation,hormuz_controlled_not_closed,oil_infrastructure_threat}`, `iran_nuclear:iaea_access_denied`, `israel_lebanon:diplomacy_active`, `south_sudan_abyei:military_buildup`, and `yemen_red_sea:external_backing`.
- No auto-detected crisis qualified. Myanmar/Kachin still has one current operational report; Ethiopia/Tigray and all other reviewed emerging lanes lacked one distinct independently corroborated operation meeting the configured gate.
- OilPriceAPI: Brent **$88.10**, WTI **$82.49**. Gamma exact-slug sanity: U.S.-Iran invasion **28.5%**, NATO Article 5 **8.0%**, China-Taiwan clash **5.3%**, Iran device **5.15%**; no market value set a tracker probability.
- All **19 Tavily searches** failed HTTP 432. Fallback completed through Google News RSS, targeted deep/emerging queries, direct UN/NATO/EIA sources, browser, terminal HTTP, Jina Reader, OilPriceAPI and Gamma. IAEA remains Cloudflare/403; OPEC 403; configured OCHA/UN Sudan paths 404. A Google-indexed AsiaNews Kashmir item was verified as a 2013 page and excluded.
- Evidence artifacts: `data/morning_deep_scan_sources_20260718T150145Z.json` and `data/deep_scan_supplement_20260718T150558Z.json`.
- `bash scripts/deploy.sh` succeeded. Automated commit `5eafdbe7` and explicit source-metadata restoration commit `46d3b93d` are pushed; HEAD equals `origin/main`, worktree is clean, post-pipeline JSON/canonical checks and all three required Command Deck markers pass.
- Regression status: **31/31 non-smoke tests passed**.
