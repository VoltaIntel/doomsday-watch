# Session State

Last update: 2026-07-11T00:10Z

DoomsdayWatch 00Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published state: **72% / imminent**; raw global **69.3%**. Automated deploy commit **`7879439`** succeeded; final source-metadata fix commit **`86be977`** is pushed and matches `origin/main`.
- Movers vs 21Z: **none numerically**. New evidence reinforced existing lanes: AP reported additional unclaimed strikes inside Iran after Washington said its operation ended; Reuters documented slow but nonzero Hormuz transit and continued mediation; late south-Lebanon and Gaza/West Bank incidents refreshed existing violation lanes.
- Signal cleanup: removed unsupported stale canonical `north_korea:missile_range_test`. Deploy briefly created false-positive `diplomacy_active` markers for Israel-Lebanon and Israel-Palestine from broad truce wording; both were removed, wording neutralized, timeline cleaned, and redeploy verified. Final active signals are canonical only.
- Full coupled table: Iran War **100**, Russia-Ukraine **99**, Israel-Lebanon **98**, Sudan **90**, Israel-Palestine **88**, Iran Nuclear **54**, Russia-NATO **52**, Pakistan-Afghanistan **46**, China-Taiwan **28**, DPRK **18**, South Sudan/Abyei **17**, India-Pakistan **11**, Turkey **5**.
- Sources: all 17 required search groups attempted successfully; fallback artifact `data/morning_deep_scan_sources_20260711T000413Z.json` contains Google News RSS and official probes. Direct IAEA/OPEC probes returned 403; configured OCHA OPT/UN Sudan paths returned 404. No emerging crisis met auto-add threshold.
- Allied/energy/markets: July 8 NATO Ankara posture remains governing. OilPriceAPI: Brent **$75.22**, WTI **$71.41**, gasoline **$2.98**, diesel/heating oil **$3.55**, natural gas **$2.94**, gold **$4,111.45**. Polymarket sanity: U.S.-Iran invasion **16.5%**, Iran weapon **5.85%**, Iran test **4.5%**, NPT withdrawal **14.2%**, Article 5 **6.5%**, China invasion **3.95%**, China-Taiwan clash **6.55%**, DPRK invasion **3.85%**, Ukraine agreement **21.5%**, Israel-Lebanon normalization **17%**.
- Verification: atomic JSON writes, 13/13 tracker/news coverage, canonical signal/timeline validation, required Command Deck markers, successful deploy/push, clean git status and local/origin parity.
