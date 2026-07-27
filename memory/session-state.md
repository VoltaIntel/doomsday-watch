# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-27 03Z morning deep scan, completed and live-verified at 03:19Z.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**, exact fractional-coupling score **79.516%**, unchanged from 00Z.

## Probability and evidence result
- No tracker probability moved. Highest coupled risks remain `iran_conventional` 100, `russia_ukraine` 99, `israel_lebanon` 97, `sudan` 92, `israel_palestine` 92 and `yemen_red_sea` 87.
- A Jerusalem Post report said the IDF shot down a Hezbollah drone in southern Lebanon. It remains a belligerent claim without separately verified casualties or strategic change; the existing violation assessment already covers the exchange.
- Taiwan reporting counted seven PLAN vessels and four Chinese official ships without a blockade, clash or unusual concentration. Yonhap says Seoul is monitoring reported Russian preparation for more DPRK troops; actual deployment remains unverified.
- AP syndication reported two deaths in Ukraine from Russian attacks and four in Russian-held territory from Ukrainian drones. Iranian retaliation threats over the Caspian vessel remain unexecuted.
- Ynet and follow-on reporting described a sharp Bab al-Mandeb traffic decline after already-counted Houthi attacks; no new independently confirmed Saudi damage, vessel loss or additional strike appeared.
- The 26 July tanker-mine story remains a Tasnim-origin claim without a named vessel or independent wire confirmation.

## Signals and auto-detection
- No evidence-backed canonical signal activated or cleared; final tracker, zone, top-level and timeline projections align at **15 canonical signals**.
- Deploy initially carried two contextual `diplomacy_active` matches in tracker/timeline projections. Both were removed across every projection before the final deploy; no numeric or evidence state changed.
- All 22 emerging candidates were reviewed. Nonzero returns were overwhelmingly Iran/Ukraine query pollution; none met the configured three-mention/two-source gate.

## Sources and markets
- Tavily/web_search: **24/24 HTTP 432**. Tavily extraction: **3/3 HTTP 432**.
- Fallback: **107 Google News RSS queries / 801 items**, **24 Bing lanes / 82 items**, browser/direct AP, Al Jazeera, NATO and Tasnim-claim inspection, official UN/EIA feeds, terminal HTTP, OilPriceAPI and Gamma exact-slug reads.
- Limits: IAEA/OPEC 403; OCHA/configured UN Sudan paths 404; Google times may be indexing/syndication times and Bing returned stale material.
- Final OilPriceAPI: Brent **$93.01**, WTI **$85.34**. Brent oscillated **$93.12 → $88.20 → $93.01** during the run, so prices remain sanity-only.
- Exact markets: U.S.-Iran invasion 20.5%, Iran event 5.2%, Iran test 6.0%, NPT withdrawal 15.8%, NATO Article 5 7.5%, China-Taiwan clash 6.95%, DPRK invasion 3.3%, Israel-Lebanon normalization 12.5%; Taiwan invasion rose 0.10pp to 3.55%. Markets did not set scores.
- Artifacts: `data/morning_deep_scan_sources_20260727T030218Z.json`, `data/deep_scan_full_rss_20260727T030328Z.json`, `data/bing_deep_scan_20260727T030350Z.json`, `data/polymarket_exact_snapshot_20260727T030604Z.json`, `data/direct_source_checks_20260727T030605Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded; the final clean-data deploy commit is `ea9cf867` and exact provenance correction is `faa05c30`.
- Local HEAD equals `origin/main`; final-head Pages run `30234299329` succeeded.
- Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, raw **79.516**, 20 trackers/news records, 15 aligned signals and exact HTTP-432 fallback metadata.
- Required local/live markers present: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/timeline/fractional-arithmetic checks and **31/31 non-smoke tests** passed. No command-deck HTML was hand-edited.

## Next watch
1. Signed U.S.-Iran ceasefire, vessel-flow recovery or blockade relief; alternatively renewed strikes, another boarded/disabled vessel or zero Hormuz traffic.
2. Named-vessel/independent confirmation of the Hormuz mine claim and mine-clearance activity.
3. Independent confirmation and consequences of the reported Hezbollah-drone interception, an Israeli withdrawal timetable or renewed mass-casualty escalation.
4. Verified deployment of additional DPRK troops, a DPRK launch/test or allied countermeasure.
5. NATO Article 4/5 consultation, a fourth Romanian incursion, casualties or recovered-drone attribution.
6. Confirmed Houthi damage to Saudi oil infrastructure, another damaged/sunk vessel or broader Bab al-Mandeb disruption.
7. Verified Iran safeguards/weapons threshold, Iranian retaliation against Ukraine or an emerging lane crossing the configured gate.
