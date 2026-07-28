# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-28 00Z morning deep scan; final TTL data/UI commit `29ba4338` and exact provenance/energy commit `537b2d98` pushed.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact fractional-coupling score **79.796%**, unchanged from 21Z.

## Probability and evidence result
- No tracker probability moved. Newly indexed evidence clarified already-scored events or failed source-date/corroboration thresholds.
- `iran_conventional` remains capped at **100**. The Islamic Resistance in Iraq denied responsibility for the Saudi-bound drones, threatened retaliation if Riyadh responds, and Baghdad opened an investigation. Saudi attribution and the verified energy-site threat remain in place while direct U.S.-Iran strikes stay paused.
- `south_china_sea` remains **30**. Navy Times directly confirms the already-scored 20 July baton injury, 24 July water-cannon confrontation, U.S. assistance and USS George Washington presence; no new post-scan clash occurred.
- `somalia_gulf_of_aden` remains **28**. Gulf News/AFP confirms that the M/T Asana crew remains hostage near Puntland after the 16 July hijacking; this is not a second seizure.
- `israel_palestine` remains **92**. The UN called fast-tracking/legalizing West Bank outposts a flagrant violation amid escalating settler violence, but no new canonical threshold was established.
- Nigeria’s Kaduna village attack produced Reuters and AP-style coverage of one event, not three independent qualifying developments. No emerging tracker was added.

## Signals
- No evidence-backed canonical signal activated or refreshed.
- Cleared on configured TTL: `southern_thailand:military_buildup` crossed 72 hours without independent refresh.
- Final tracker, zone, top-level and timeline projections align at **13 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ vs 21Z | Zone | Active signals |
|---|---:|---:|---:|---|---|
| `iran_conventional` | 100 | 100 | 0 | imminent | `ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `hormuz_mining`, `military_buildup`, `oil_infrastructure_threat` |
| `israel_lebanon` | 87 | 97 | 0 | imminent | `ceasefire_violation` |
| `turkey` | 5 | 5 | 0 | deterrent | — |
| `india` | 15 | 15 | 0 | elevated | — |
| `russia` | 58 | 68 | 0 | imminent | — |
| `china` | 24 | 28 | 0 | critical | — |
| `north_korea` | 18 | 18 | 0 | elevated | — |
| `russia_ukraine` | 99 | 99 | 0 | imminent | — |
| `pakistan_afghanistan` | 46 | 46 | 0 | critical | — |
| `iran_nuclear` | 49 | 56 | 0 | imminent | — |
| `sudan` | 94 | 94 | 0 | imminent | `military_buildup` |
| `israel_palestine` | 92 | 92 | 0 | imminent | `diplomacy_active`, `holy_site_tension` |
| `south_sudan_abyei` | 19 | 19 | 0 | elevated | — |
| `eastern_drc` | 56 | 56 | 0 | imminent | — |
| `yemen_red_sea` | 92 | 92 | 0 | imminent | `ceasefire_violation`, `infrastructure_strike`, `military_buildup` |
| `mali_sahel` | 39 | 39 | 0 | critical | — |
| `south_china_sea` | 30 | 30 | 0 | critical | — |
| `somalia_gulf_of_aden` | 28 | 28 | 0 | critical | — |
| `southern_thailand` | 25 | 25 | 0 | critical | — |
| `kuwait_iraq_border` | 17 | 17 | 0 | elevated | — |

## Sources, energy and markets
- Tavily failed **25/25 searches** and **4/4 extracts** with HTTP 432.
- Fallback: 18 base Google lanes / **127 items**, 48 deep Google lanes / **441 items**, 48 deep Bing lanes / **142 items**, 22 auto-detection Google lanes / **108 items**, 10 direct-source targets, official feeds/pages, redirect decoding, terminal HTTP, OilPriceAPI and exact Gamma.
- Limits: IAEA/OPEC 403; OCHA/configured UN Sudan 404; Reuters HTML 401; France 24 HTML 403; Washington Post timeout. Two News On AIR results indexed on 27 July resolved to 9 April articles and were rejected.
- Final deploy energy: Brent **$87.73** (**-4.42%/24h**, -$0.21 vs 21Z) and WTI **$82.10** (**-2.45%/24h**, +$0.21). OilPriceAPI moved Brent $85.29→$87.73 in eight minutes, so energy remained sanity-only.
- Exact markets: U.S.-Iran invasion **22.5%**, Iran event **5.15%**, Iran test **5.5%**, NPT withdrawal **15.85%**, NATO Article 5 **7.5%**, Taiwan invasion **3.85%** (+0.1pp), China-Taiwan clash **6.60%** (+0.3pp), DPRK invasion **2.45%**, Israel-Lebanon normalization **12.5%**. Markets did not set scores.
- Artifacts: `data/morning_deep_scan_sources_20260728T000208Z.json`, `data/deep_scan_full_fallback_20260728T000306Z.json`, `data/direct_source_checks_20260728T000548Z.json`, `data/auto_detection_review_20260728T000330Z.json`, `data/polymarket_exact_snapshot_20260728T000729Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded; no command-deck HTML was hand-edited.
- Final TTL data/UI commit `29ba4338`; exact provenance/energy commit `537b2d98`; data-head Pages run `30317232466` succeeded.
- Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, exact **79.796**, 20 trackers/news records and 13 aligned canonical signals.
- Required local/live markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- Canonical JSON/timeline checks and **31/31 non-smoke tests** passed; HEAD and `origin/main` match.

## Next watch
1. Official Saudi/Aramco damage or production confirmation, satellite quantification, Baghdad investigation findings or retaliation.
2. Signed/directly acknowledged U.S.-Iran terms, Hormuz traffic recovery, mine clearance or resumed direct strikes.
3. Another Romanian incursion, concrete Russian retaliation, casualties or NATO Article 4/5 consultation.
4. A new China-Philippines hostile encounter, casualty, vessel seizure or treaty consultation beyond the July 20–24 incidents.
5. ISF entry into Gaza, implemented withdrawal, organized settler mobilization or collapse of the plan.
6. Independent Khartoum–El Obeid route control confirmation, RSF reversal or El Obeid drone casualties.
7. Fresh DPRK deployment, launcher movement, prohibited firing/detonation or allied countermeasure.
8. A second Gulf of Aden hijacking, change in Asana hostage status or material Bab el-Mandeb/Hormuz traffic shift.
9. A fresh southern Thailand attack, casualty cluster or verified security deployment sufficient to reactivate the cleared marker.
10. An emerging crisis crossing the configured three-mention/two-independent-source gate.
