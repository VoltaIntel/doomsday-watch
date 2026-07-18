# Session State

Last update: 2026-07-18T06:15Z

DoomsdayWatch 06Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published assessment remains **74% / imminent**; weighted coupled score **73.54%**. No tracker probability or canonical signal moved.
- Fresh evidence: Middle East Eye added a post-03Z report of three more southern Lebanese schools destroyed, corroborating the Lebanese ministry claim carried by Al Jazeera and Anadolu. The UN says escalating eastern Congo insecurity is hampering humanitarian and Ebola work. Neither crossed a configured numeric or signal threshold.
- Coupled table: Iran War **100**, Russia-Ukraine **99**, Israel-Lebanon **94**, Sudan **90**, Israel-Palestine **88**, Iran Nuclear **54**, Russia-NATO **52**, Eastern DR Congo **52**, Pakistan-Afghanistan **46**, Yemen/Red Sea **38**, China-Taiwan **28**, DPRK **18**, South Sudan/Abyei **12**, India-Pakistan **11**, Turkey **5**.
- Active canonical signals: `iran_conventional:{ceasefire_violation,hormuz_controlled_not_closed}`, `israel_lebanon:diplomacy_active`, `iran_nuclear:iaea_access_denied`, `yemen_red_sea:external_backing`.
- Auto-detection added no tracker. Myanmar/Kachin still has two qualifying outlets for one fresh event but only two mentions, one short of the configured three-mention/two-source gate.
- OilPriceAPI deploy snapshot: Brent **$88.10**, WTI **$82.47**, gasoline **$3.39**, diesel **$4.08**, heating oil **$4.05**, natural gas **$2.91**, gold **$4,010.56**. Brent/WTI remain **30.7%/29.3%** above pre-conflict baselines.
- Exact-slug Polymarket sanity: U.S.-Iran invasion **27.5%**, NATO Article 5 **8.0%**, China-Taiwan clash **5.15%**, China invasion **3.95%**, Iran weapon **5.15%**, Iran test **4.5%**, NPT withdrawal **13.5%**, Israel-Lebanon normalization **17.0%**. Horizon/definition mismatch; sanity-only.
- All **19 Tavily searches** and **5 web extraction attempts** failed HTTP 432. Coverage continued through Google News RSS for all configured trackers, 28 targeted deep queries, direct UN/NATO/EIA, browser, terminal HTTP, OilPriceAPI and Gamma. IAEA remained Cloudflare/403; OPEC 403; configured OCHA/UN Sudan paths 404. A newly indexed Sudan casualty story resolved to 8 July AP reporting and was excluded as stale.
- Evidence artifacts: `data/morning_deep_scan_sources_20260718T060234Z.json` and `data/deep_scan_supplement_20260718T060331Z.json`.
- Atomic state update and `bash scripts/deploy.sh` succeeded. Automated deploy commit `3a6f103d`; explicit source-metadata restoration `21f453e9`. HEAD equals origin, worktree is clean, JSON/canonical checks and required Command Deck markers passed.
- Tests: **31 passed** (non-smoke unit/forecast/Polymarket suites).
