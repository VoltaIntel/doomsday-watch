# Session State

Last update: 2026-07-10T15:17Z

DoomsdayWatch 15Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published state: **72% / imminent**; raw global **69.3%**. Final deploy commit **`c084362`** pushed and matches `origin/main`.
- Movers vs 12Z: **none numerically**. Reuters confirmed daily Hormuz tanker passage slowed after the latest U.S.-Iran hostilities; Iran says passage remains on its terms while selective transit continues. Russia-Ukraine, Lebanon, Gaza, El Obeid and Iran safeguards evidence reinforced existing lanes without crossing a probability threshold.
- Final coupled table: Iran War **100**, Russia-Ukraine **99**, Israel-Lebanon **98**, Sudan **90**, Israel-Palestine **88**, Iran Nuclear **54**, Russia-NATO **52**, Pakistan-Afghanistan **46**, China-Taiwan **28**, DPRK **18**, South Sudan/Abyei **17**, India-Pakistan **11**, Turkey **5**.
- Signal handling: `iran_conventional:hormuz_controlled_not_closed` reached temporal expiry during the first deploy and was immediately reactivated at **15:07Z** on fresh Reuters confirmation. Final state/timeline contains only 11 intended canonical signals.
- Sources: Hermes web search returned for all 17 required groups; fallback/corroboration artifact: `data/morning_deep_scan_sources_20260710T150247Z.json`. Reuters, Taiwan MND, NATO, IAEA GOV/2026/33, UN News and Amani Africa were extracted directly. Collector probes to IAEA/OPEC returned 403; configured OCHA/UN Sudan paths returned 404. No emerging crisis met auto-detection threshold.
- Allied/energy/markets: NATO’s Ankara declaration remains the governing allied statement. Final energy: Brent **$76.02**, WTI **$71.83**, gasoline **$2.97**, diesel **$3.57**, heating oil **$3.55**, natural gas **$2.90**, gold **$4,097.16**. Exact-slug Polymarket: U.S. invasion of Iran **16.5%**, Iran weapon **5.65%**, Iran device test **4.5%**, NPT withdrawal **13.45%**, NATO Article 5 **6.5%**, China invasion **3.95%**, China-Taiwan clash **6.55%**, DPRK invasion **3.9%**, Ukraine agreement **21.5%**, Israel-Lebanon normalization **17%**; horizon/definition mismatches make these sanity checks only.
- Verification: atomic JSON writes, 13/13 configured tracker/news coverage, canonical/timeline guards, required Command Deck markers, Python compile, **37 tests passed**, clean working tree, and local/origin HEAD equality all passed.
