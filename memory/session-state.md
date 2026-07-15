# Session State

Last update: 2026-07-15T03:16Z

DoomsdayWatch 03Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published assessment remains **74% / imminent**; weighted coupled score eased from **73.62% to 73.50%**.
- Numeric mover: **Eastern DR Congo 58% → 52%**. Canonical `eastern_drc:military_buildup` was removed after its configured 72-hour evidence window elapsed without fresh operational corroboration.
- Evidence movers: AP/DW/Al-Monitor/BBC reported another U.S.-Iran attack cycle and tanker damage in Hormuz; Rome Israel-Lebanon talks remained open while attacks continued; UN casualty findings for Ukraine were reinforced; Saudi-Houthi attacks continued; Sudan’s conditional RSF truce acceptance remained unimplemented.
- Coupled table: Iran War **100**, Russia-Ukraine **99**, Israel-Lebanon **94**, Sudan **90**, Israel-Palestine **88**, Iran Nuclear **54**, Russia-NATO **52**, Eastern DR Congo **52**, Pakistan-Afghanistan **46**, Yemen/Red Sea **38**, China-Taiwan **28**, DPRK **18**, South Sudan/Abyei **12**, India-Pakistan **11**, Turkey **5**.
- Active canonical signals now total nine: Iran conventional (`ceasefire_violation`, `diplomacy_refused`, `hormuz_closed`, `oil_infrastructure_threat`); Israel-Lebanon (`diplomacy_active`); Iran nuclear (`iaea_access_denied`); Yemen/Red Sea (`ceasefire_violation`, `external_backing`, `infrastructure_strike`).
- Deploy-time OilPriceAPI: Brent **$85.88 (+2.17% 24h)**, WTI **$80.20 (+1.11%)**, diesel **$4.06 (+4.38%)**, gasoline **$3.26 (+2.52%)**, heating oil **$4.05 (+4.11%)**, gas **$2.91 (+1.04%)**, gold **$4,043.45 (+0.83%)**.
- Exact-slug Polymarket returned **11/23** mapped markets. U.S.-Iran invasion 19.5%, Iran device 5.2%, Iran test 4.5%, NPT withdrawal 16.8%, NATO Article 5 8.0%, China invasion 3.65%, China-Taiwan clash 6.75%, DPRK invasion 1.95%, Ukraine agreement 18.5%, Israel-Lebanon normalization 14.5%. Sanity-only due definition/horizon mismatch.
- Auto-detection added no tracker. Ethiopia/Tigray warnings had only two sources; Thailand-Cambodia, South China Sea, Syria and Sahel did not meet the configured fresh operational cluster threshold.
- All 20 Tavily searches failed HTTP 432; browser fallback failed because `agent-browser` is absent. Google News RSS and direct UN/NATO/EIA HTTP completed fallback coverage. IAEA/OPEC returned 403; OCHA/UN Sudan paths returned 404.
- Atomic state/timeline writes, deploy/push, exact post-deploy source-meta restoration, canonical validation, all three Command Deck markers, and origin parity passed. Final published head **`6c16ed60`**.
- Test caveat: **28 tests passed; 11 pipeline-smoke cases errored at fixture setup because the copied pipeline exceeded its hard-coded 60-second timeout while refreshing mapped Polymarket slugs**. The real deploy pipeline completed successfully; this was a timeout, not an assertion failure.
