# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-27 12Z morning deep scan, completed and live-verified at 12:17Z.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact fractional-coupling score **79.576%**, unchanged from 09Z.

## Probability and evidence result
- **No numeric tracker moved.** AP now reports three strike-free days and significant intermediary progress toward restoring an interim arrangement. Iran says intermediaries are relaying messages and Iran-Oman work is focused on a vessel-transit mechanism, but there are no direct U.S.-Iran talks, Hormuz remains closed and the U.S. blockade remains in force.
- `sudan` remains **94%**. Saudi Gazette and Türkiye Today syndicated the army's highway-control claim, but no independent field confirmation or RSF counterattack appeared; a current humanitarian report says roughly half a million people around el-Obeid remain at risk.
- `north_korea` remains **18%**. South Korea is monitoring the reported 30,000-troop plan, while the Kremlin rejected Zelensky's account; no actual movement was verified.
- `russia` remains **56% raw / 66% coupled**. Fresh Romania coverage still resolves to the third drone shootdown, not a fourth; NATO announced no Article 4/5 action.
- All 22 emerging candidates were reviewed. Myanmar remains one Reuters/ACLED reporting chain; no candidate crossed the configured three-mention/two-independent-source gate.

## Signals
- No canonical signal activated or cleared. Evidence refreshed for `iran_conventional:diplomacy_active` and `iran_conventional:hormuz_controlled_not_closed`.
- Tracker, zone, top-level and timeline projections align at **16 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Zone | Active signals |
|---|---:|---:|---|---|
| `iran_conventional` | 100 | 100 | imminent | `ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `hormuz_mining`, `military_buildup` |
| `israel_lebanon` | 87 | 97 | imminent | `ceasefire_violation` |
| `turkey` | 5 | 5 | deterrent | — |
| `india` | 15 | 15 | elevated | — |
| `russia` | 56 | 66 | imminent | — |
| `china` | 24 | 28 | critical | — |
| `north_korea` | 18 | 18 | elevated | — |
| `russia_ukraine` | 99 | 99 | imminent | — |
| `pakistan_afghanistan` | 46 | 46 | critical | — |
| `iran_nuclear` | 49 | 56 | imminent | — |
| `sudan` | 94 | 94 | imminent | `military_buildup` |
| `israel_palestine` | 92 | 92 | imminent | `diplomacy_active`, `holy_site_tension`, `military_buildup` |
| `south_sudan_abyei` | 19 | 19 | elevated | — |
| `eastern_drc` | 56 | 56 | imminent | `military_buildup` |
| `yemen_red_sea` | 87 | 87 | imminent | `ceasefire_violation`, `military_buildup` |
| `mali_sahel` | 39 | 39 | critical | `external_backing` |
| `south_china_sea` | 30 | 30 | critical | `external_backing` |
| `somalia_gulf_of_aden` | 28 | 28 | critical | — |
| `southern_thailand` | 25 | 25 | critical | `military_buildup` |
| `kuwait_iraq_border` | 17 | 17 | elevated | — |

## Sources and markets
- Tavily failed **24/24 searches + 7/7 extracts** with HTTP 432.
- Fallback: **96 Google News RSS queries / 1,049 items**, **24 Bing lanes / 128 items** with one lane failure, browser/direct AP/NATO/UN checks, terminal HTTP, OilPriceAPI and exact Gamma.
- Limits: IAEA/OPEC 403; EIA direct retry 406 although the first feed fetch succeeded; OCHA/configured UN Sudan paths 404; RSS dates can be indexing/syndication times.
- Final deploy OilPriceAPI: Brent **$88.35** (-9.45%/24h), WTI **$83.72** (-2.14%).
- Exact markets: U.S.-Iran invasion **21.5%** (+1.00pp vs 09Z), Iran event **5.15%**, Iran test **5.5%**, NPT withdrawal **15.8%**, NATO Article 5 **7.5%**, Taiwan invasion **3.65%**, China-Taiwan clash **6.20%** (-0.05pp), DPRK invasion **2.90%** (+0.45pp), Israel-Lebanon normalization **12.5%**. Markets did not set scores.
- Artifacts: `data/morning_deep_scan_sources_20260727T120316Z.json`, `data/deep_scan_full_rss_20260727T120314Z.json`, `data/bing_deep_scan_20260727T120314Z.json`, `data/deep_scan_summary_20260727T120314Z.json`, `data/polymarket_exact_snapshot_20260727T120526Z.json`, `data/direct_source_checks_20260727T120538Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded. Initial deploy commit: `c2e15118`; exact energy correction/pipeline commit: `91f8ae73`.
- GitHub Pages run `30265134910` succeeded for final HEAD `91f8ae73`.
- Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, exact **79.576**, 20 trackers/news records and 16 aligned signals.
- Required local/live markers are present: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/timeline/fractional checks pass. **31/31 non-smoke assertions** passed; the stock fixture hit its known fixed 60-second subprocess ceiling, while identical isolated **11/11 smoke assertions passed in 86.07 seconds** with only the harness ceiling extended. No command-deck HTML was hand-edited.
- Local HEAD equals `origin/main`; repository tree is clean.

## Next watch
1. A fourth strike-free U.S.-Iran day, direct talks, a signed arrangement or verified Hormuz vessel-flow recovery; alternatively resumed strikes or an operational order tied to moving U.S. assets.
2. Implementation of an Iran-Oman transit mechanism, blockade relief, mine-clearance activity or verified zero commercial traffic.
3. Independent field confirmation of Sudan army control along the Khartoum-el-Obeid route, an RSF counterattack or sustained humanitarian access.
4. Verified movement of additional North Korean troops or launchers, a DPRK missile/nuclear test or an allied countermeasure.
5. A fourth Romanian incursion, casualties, recovered-drone attribution or NATO Article 4/5 consultation.
6. Confirmed new Houthi damage to Saudi oil infrastructure, another damaged/sunk vessel or a verified change in Bab el-Mandeb traffic.
7. A verified Iranian safeguards/weapons threshold, direct retaliation against Ukraine or an emerging lane crossing the configured gate.
