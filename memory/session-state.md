# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-27 06Z morning deep scan, completed and live-verified at 06:23Z.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact fractional-coupling score **79.576%**, up 0.060pp from 03Z.

## Probability and evidence result
- **Top mover:** `sudan` **92% → 94%**. Al Jazeera directly reported the Sudanese army’s claimed full control of the Al Sadarat highway and towns between Khartoum and el-Obeid after two days of fierce fighting, calling it the first major army offensive in months and a restored strategic supply route. Field control and loss claims remain army-sourced.
- `russia_ukraine` stays **99%** after Kyiv Post reported overnight Russian attacks killed one and injured dozens.
- `north_korea` stays **18%**. Zelensky says Russia prepared to receive another 30,000 DPRK troops; SCMP called the claim plausible but still rumoured, and no actual deployment, launch or test was verified.
- `india` stays **15%** after Pakistan rejected Indian Kashmir remarks and warned against adventurism without force movement or a clash.
- The second-day U.S.-Iran pause holds; the Hormuz blockade/traffic constraint remains. The 26 July tanker-mine story still lacks a named vessel or independent wire confirmation.

## Signals and auto-detection
- No canonical signal state activated or cleared. The already-active `sudan:military_buildup` assessment gained fresh supporting evidence.
- Deploy introduced one contextual `israel_lebanon:diplomacy_active` match through the word “ceasefire”. It was removed atomically from tracker/timeline state and the trigger wording was neutralized before final publication.
- Tracker, zone, top-level and timeline projections align at **15 canonical signals**.
- No emerging tracker qualified. Myanmar had two current conflict-themed headlines from one publisher plus an unrelated BBC Iran result; other nonzero lanes were mostly Iran/Ukraine query pollution.

## Sources and markets
- Tavily/web_search: **24/24 HTTP 432**. Tavily extraction: **5/5 HTTP 432**.
- Fallback: **92 Google News RSS queries / 675 items**, **24 Bing lanes / 130 items**, browser/direct AP, Al Jazeera, SCMP, Kyiv Post and NATO checks, official UN/EIA feeds, terminal HTTP, OilPriceAPI and exact Gamma.
- Limits: IAEA/OPEC 403; OCHA/configured UN Sudan paths 404; Google times may be indexing/syndication times and Bing resurfaced older material.
- Final deploy OilPriceAPI: Brent **$91.62** (-5.25%/24h), WTI **$84.25** (-0.63%).
- Exact markets: U.S.-Iran invasion 20.5%, Iran event 5.2%, Iran test 6.0%, NPT withdrawal 15.8%, NATO Article 5 7.5%, Taiwan invasion 3.55%, China-Taiwan clash 6.95%, Israel-Lebanon normalization 12.5%; DPRK invasion fell 0.20pp to 3.10%. Markets did not set scores.
- Artifacts: `data/morning_deep_scan_sources_20260727T060237Z.json`, `data/deep_scan_full_rss_20260727T060423Z.json`, `data/bing_deep_scan_20260727T060423Z.json`, `data/deep_scan_summary_20260727T060423Z.json`, `data/polymarket_exact_snapshot_20260727T060946Z.json`, `data/direct_source_checks_20260727T060946Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded. Initial deploy commit: `4ebff7f5`; exact signal/energy correction: `d9c1c15d`.
- GitHub Pages run `30242386539` succeeded for the final data head.
- Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, exact **79.576**, Sudan **94**, 20 trackers/news records and 15 aligned signals.
- Required local/live markers are present: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/timeline/fractional-arithmetic checks pass. **31/31 non-smoke tests** passed. The repository smoke fixture hit its known hard-coded 60-second subprocess ceiling; the identical **11/11 assertions passed in 79.31s** from an isolated copy with only that harness timeout extended. No command-deck HTML was hand-edited.

## Next watch
1. Independent field confirmation of Sudan army control along the Khartoum-el-Obeid route, an RSF counterattack or sustained humanitarian access through the corridor.
2. Signed U.S.-Iran ceasefire, verified vessel-flow recovery or blockade relief; alternatively renewed strikes, another boarded/disabled vessel or zero Hormuz traffic.
3. Named-vessel/independent confirmation of the Hormuz mine claim and mine-clearance activity.
4. Verified movement of the reported 30,000 additional DPRK troops, a DPRK launch/test or allied countermeasure.
5. Independent confirmation and consequences of the reported Hezbollah-drone interception, an Israeli withdrawal timetable or renewed mass-casualty escalation.
6. NATO Article 4/5 consultation, a fourth Romanian incursion, casualties or recovered-drone attribution.
7. Confirmed Houthi damage to Saudi oil infrastructure, another damaged/sunk vessel or broader Bab al-Mandeb disruption.
8. Verified Iran safeguards/weapons threshold, Iranian retaliation against Ukraine or an emerging lane crossing the configured gate.
