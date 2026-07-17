# Session State

Last update: 2026-07-17T18:33Z

DoomsdayWatch 18Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published assessment remains **74% / imminent**; weighted coupled score remains **73.50%**. No tracker probability moved.
- Fresh evidence: AP reported seven killed and 22 wounded at a Gaza funeral; Al Jazeera reported a wider daily toll of 14. Lebanon’s planned trilateral implementation meeting was postponed for stated technical preparation, while a single-chain report said Tehran told Hezbollah and other allies to prepare for wider conflict. Sudan’s army claimed 205 RSF vehicles and four drones destroyed during July operations.
- None of those items crossed a new configured probability threshold. `israel_lebanon:diplomacy_active` was revalidated from fresh implementation-meeting reporting after its prior activation aged out; the final five-signal set is semantically unchanged from 15Z.
- Coupled table: Iran War **100**, Russia-Ukraine **99**, Israel-Lebanon **94**, Sudan **90**, Israel-Palestine **88**, Iran Nuclear **54**, Russia-NATO **52**, Eastern DR Congo **52**, Pakistan-Afghanistan **46**, Yemen/Red Sea **38**, China-Taiwan **28**, DPRK **18**, South Sudan/Abyei **12**, India-Pakistan **11**, Turkey **5**.
- Active canonical signals: `iran_conventional:{ceasefire_violation,hormuz_controlled_not_closed}`, `israel_lebanon:diplomacy_active`, `iran_nuclear:iaea_access_denied`, `yemen_red_sea:external_backing`.
- Final OilPriceAPI: Brent **$88.06**, WTI **$82.23**, gasoline **$3.40**, diesel **$4.05**.
- Exact-slug Polymarket sanity: U.S.-Iran invasion **26.5%**, NATO Article 5 **8.5%**, China-Taiwan clash **4.85%**, China invasion **3.75%**, Iran weapon **5.4%**, Iran test **4.5%**, NPT withdrawal **14.0%**. Horizon/definition mismatch; no tracker probability was market-set.
- Auto-detection added no tracker. Gulf incidents remained spillover of `iran_conventional`; Ethiopia/Tigray, Thailand-Cambodia, South China Sea, Syria, Sahel, Kosovo-Serbia, Guyana-Venezuela and Armenia-Azerbaijan did not meet the distinct fresh-event gate.
- All **20 Tavily searches** and four extracts failed HTTP 432; browser fallback failed because `agent-browser` is absent. Google/Bing News RSS, direct UN/NATO/EIA, terminal HTTP, OilPriceAPI and Gamma completed coverage. IAEA/OPEC returned 403; configured OCHA/UN Sudan paths returned 404.
- Atomic state update, three deploy/push passes (including temporal-decay correction), exact source-metadata restoration, canonical/timeline alignment, Command Deck markers, origin parity and **42 tests** passed. Automated deploy head before metadata/session-log commit: **`e37875e3`**.
