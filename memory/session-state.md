# Session State

Last update: 2026-07-14T09:31Z

DoomsdayWatch 09Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published assessment remains **74% / imminent** (weighted coupled score **73.62%**); no numeric tracker or global move versus 06Z.
- Evidence-only movers: Reuters/AP confirmed an Iranian retaliatory attempt against a U.S. base in Jordan after the third U.S. attack night; Russia launched 145 aerial weapons overnight and Ukraine struck Russian refineries; Israel-Lebanon talks continued; Sudan gold-financing restrictions advanced.
- Coupled table: Iran War **100**, Russia-Ukraine **99**, Israel-Lebanon **94**, Sudan **90**, Israel-Palestine **88**, Eastern DR Congo **58**, Iran Nuclear **54**, Russia-NATO **52**, Pakistan-Afghanistan **46**, Yemen/Red Sea **38**, China-Taiwan **28**, DPRK **18**, South Sudan/Abyei **12**, India-Pakistan **11**, Turkey **5**.
- No canonical signal changed. A deploy keyword false positive briefly wrote two DPRK timeline entries from an explicitly negative sentence; they were removed before final deploy and DPRK remains 18% with no active signal.
- Deploy-time OilPriceAPI: Brent **$86.31**, WTI **$80.34**, gasoline **$3.24**, Gulf Coast diesel **$3.97**, heating oil **$3.97**, natural gas **$2.88**, gold **$4,021.13**.
- Polymarket returned 11/23 exact mapped markets; U.S.-Iran invasion 18.5%, Iran device 5.35%, Iran test 4.5%, NPT withdrawal 14.25%, NATO Article 5 6.0%, China invasion 3.75%, China-Taiwan clash 6.15%, DPRK invasion 2.0%, Ukraine agreement 18.5%, Israel-Lebanon normalization 14.5%. Sanity-only.
- Auto-detection added no tracker. Ethiopia/Tigray had two relevant warnings, below the three-mention threshold; Thailand-Cambodia, South China Sea, Syria and Sahel lacked a qualifying fresh operational cluster.
- All 19 Tavily searches returned HTTP 432; browser fallback lacked `agent-browser`. Google News RSS, direct UN/NATO/EIA pages, terminal HTTP and market/energy APIs supplied fallback coverage. IAEA/OPEC returned 403; configured OCHA/UN Sudan paths returned 404.
- Atomic write, two deploy/push passes, canonical/timeline validation, all Command Deck markers and origin parity passed at **`c701f76d`**. Non-pipeline tests passed **28/28**; the shared pipeline fixture exceeded its hard 60-second timeout in both the full and isolated run, producing 11 setup errors despite both real deploy pipeline runs completing successfully.
