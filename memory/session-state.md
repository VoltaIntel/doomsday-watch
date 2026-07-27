# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-27 21Z morning deep scan; final data/UI commit `a6d4c166` deployed and Pages run `30306980123` succeeded.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact fractional-coupling score **79.796%**, up **0.100 point** from 18Z.

## Probability and evidence result
- `yemen_red_sea` rose **87 → 92 raw/coupled**. The Maritime Executive reported satellite-indicated damage near Abqaiq and a continuing Jizan refinery fire; Bloomberg separately indexed satellite-observed tank fire at Jazan. This crossed the canonical `infrastructure_strike` evidence threshold.
- `iran_conventional` remains capped at **100**. The same facility evidence activated `oil_infrastructure_threat`; Reuters says Trump describes U.S.-Iran talks as good while retaining the threat of resumed strikes.
- `sudan` remains **94**. Radio Dabanga says local sources dispute SAF claims that the Omdurman–El Obeid road reopened, reports continuing fighting and says a new RSF drone attack hit El Obeid without an immediate casualty/damage figure.
- `israel_lebanon` remains **87 raw / 97 coupled**. UN News says Israeli attacks and Hezbollah fighting continue after the 17 April conditional truce; national authorities report 4,300+ killed and 12,200 injured since 2 March.
- `israel_palestine` remains **92**. Israel approved the ISF framework and legal immunities, but no force entry or withdrawal has been implemented.
- No emerging candidate crossed the configured three-mention/two-independent-source escalation gate.

## Signals
- Activated: `iran_conventional:oil_infrastructure_threat`, `yemen_red_sea:infrastructure_strike`.
- Cleared on TTL/no refresh: `eastern_drc:military_buildup`, `israel_palestine:military_buildup`.
- Reactivated: `yemen_red_sea:ceasefire_violation` on the fresh attack cycle.
- Removed two pipeline contextual false positives: `israel_lebanon:diplomacy_active`, `yemen_red_sea:diplomacy_active`.
- Final tracker, zone, top-level and timeline projections align at **14 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ vs 18Z | Zone | Active signals |
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
| `yemen_red_sea` | 92 | 92 | +5 | imminent | `ceasefire_violation`, `infrastructure_strike`, `military_buildup` |
| `mali_sahel` | 39 | 39 | 0 | critical | — |
| `south_china_sea` | 30 | 30 | 0 | critical | — |
| `somalia_gulf_of_aden` | 28 | 28 | 0 | critical | — |
| `southern_thailand` | 25 | 25 | 0 | critical | `military_buildup` |
| `kuwait_iraq_border` | 17 | 17 | 0 | elevated | — |

## Sources, energy and markets
- Tavily failed **26/26 searches** and **3/3 extracts** with HTTP 432.
- Fallback: 51 Google lanes / **1,010 items**, 51 Bing lanes / **130 items**, 22 auto-detection Google lanes / **121 items**, 18 supplemental Google lanes / **127 items**, plus browser redirects, direct UN/Radio Dabanga/Jerusalem Post/Maritime Executive pages, terminal HTTP, OilPriceAPI and exact Gamma.
- Limits: IAEA/OPEC 403; OCHA/configured UN Sudan 404; Reuters HTML 401; Taiwan News HTML 403. RSS timestamps can be indexing/syndication times.
- Final deploy energy: Brent **$87.94** (**-11.23%/24h**, -$0.60 vs 18Z) and WTI **$81.89** (**-3.92%/24h**, -$0.86). Brent varied $85.39→$87.94; energy remained sanity-only.
- Exact markets: U.S.-Iran invasion **22.5%** (+1.0pp), Iran event **5.15%**, Iran test **5.5%**, NPT withdrawal **15.85%**, NATO Article 5 **7.5%**, Taiwan invasion **3.75%** (+0.1pp), China-Taiwan clash **6.30%**, DPRK invasion **2.45%**, Israel-Lebanon normalization **12.5%** (+1.0pp). Markets did not set scores.
- Artifacts: `data/morning_deep_scan_sources_20260727T210400Z.json`, `data/deep_scan_full_fallback_20260727T210612Z.json`, `data/direct_source_checks_20260727T210923Z.json`, `data/auto_detection_review_20260727T211350Z.json`, `data/polymarket_exact_snapshot_20260727T211105Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded; final metadata alignment was regenerated through `scripts/pipeline.py`, never by hand-editing command-deck HTML.
- Data/UI commit `a6d4c166`; Pages run `30306980123` succeeded.
- Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, exact **79.796**, 20 trackers/news records and 14 aligned canonical signals.
- Required local/live markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- Canonical ID/signal checks passed; **31/31 non-smoke tests** passed; HEAD/upstream/`origin/main` matched before session-summary logging.

## Next watch
1. Official Saudi/Aramco damage or production confirmation, independent satellite quantification, or retaliation against attributed Iraqi groups.
2. Signed/directly acknowledged U.S.-Iran terms, Hormuz traffic recovery, mine clearance or resumed direct strikes.
3. Another Romanian incursion, concrete Russian retaliation, casualties or NATO Article 4/5 consultation.
4. ISF personnel entering Gaza, an implemented Israeli withdrawal step or collapse of the plan.
5. Renewed Israel-Hezbollah strategic attacks, an Israeli withdrawal timetable or UNIFIL posture change.
6. Independent Omdurman–El Obeid control confirmation, RSF reversal or casualties from the new drone attack.
7. Fresh DPRK deployment, launcher movement, prohibited firing/detonation or allied countermeasure.
8. Another damaged/sunk Red Sea vessel or a material Bab el-Mandeb/Hormuz traffic shift.
9. An emerging crisis crossing the configured three-mention/two-independent-source escalation gate.
