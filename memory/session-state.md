# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-27 18Z morning deep scan; final-head Pages deployment completed at 18:21Z and live verification passed.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact fractional-coupling score **79.696%**, unchanged from 15Z.

## Probability and evidence result
- **No numeric tracker moved.** The strongest evidence changes were mixed rather than sufficient for a score revision.
- `iran_conventional` remains capped at **100**. Reuters directly quoted Trump saying the U.S. is having “good talks” and will resume strikes if they fail; Tehran says it is not seeking resumed direct talks. Saudi Arabia attributes the petroleum-site drone wave to Iran-backed Iraqi groups and reserves the right to respond.
- `russia` remains **58 raw / 68 coupled**. The Russian Embassy denied targeting Romania, threatened an unspecified response to the diplomatic expulsion and warned against Romanian cross-border air-defence action. Romania issued a short Tulcea alert for targets near the Ukrainian river border, but reported no fifth incursion.
- `israel_lebanon` remains **87 / 97** after the UN human rights chief called for Israeli withdrawal and an end to demolitions; no implementation commitment followed.
- `yemen_red_sea` remains **87**. Reuters directly carried the Houthi claim that it targeted the Saudi East-West Pipeline, but no damage or new vessel loss was verified.
- All 22 emerging candidates were reviewed. Myanmar remained one Reuters/ACLED source chain plus rewrites; no candidate crossed the three-mention/two-independent-source gate.

## Signals
- No evidence-backed canonical signal activated.
- Deploy TTL cleared `mali_sahel:external_backing` and `south_china_sea:external_backing`.
- Pipeline contextual wording briefly overmatched `iran_nuclear:enrichment_90`; it was neutralized and removed atomically from tracker/timeline projections before the final deploy.
- Final tracker, zone, top-level and timeline projections align at **14 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ vs 15Z | Zone | Active signals |
|---|---:|---:|---:|---|---|
| `iran_conventional` | 100 | 100 | 0 | imminent | `ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `hormuz_mining`, `military_buildup` |
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
| `israel_palestine` | 92 | 92 | 0 | imminent | `diplomacy_active`, `holy_site_tension`, `military_buildup` |
| `south_sudan_abyei` | 19 | 19 | 0 | elevated | — |
| `eastern_drc` | 56 | 56 | 0 | imminent | `military_buildup` |
| `yemen_red_sea` | 87 | 87 | 0 | imminent | `ceasefire_violation`, `military_buildup` |
| `mali_sahel` | 39 | 39 | 0 | critical | — |
| `south_china_sea` | 30 | 30 | 0 | critical | — |
| `somalia_gulf_of_aden` | 28 | 28 | 0 | critical | — |
| `southern_thailand` | 25 | 25 | 0 | critical | `military_buildup` |
| `kuwait_iraq_border` | 17 | 17 | 0 | elevated | — |

## Sources and markets
- Tavily failed **26/26 searches + 14/14 extracts** with HTTP 432.
- Fallback: **71 Google News RSS queries / 798 items**, **25 Bing lanes / 176 items**, browser/direct Reuters-Al-Monitor and Agerpres inspection, NATO/UN/EIA/UKMTO checks, terminal HTTP, OilPriceAPI and exact Gamma.
- Limits: IAEA/OPEC 403; NATO press/OCHA/configured UN Sudan paths 404; Google browser search CAPTCHA and Bing browser challenge; RSS timestamps can be indexing/syndication times.
- Final deploy energy: Brent **$88.54** (-3.03%/24h; -$1.16 vs 15Z) and WTI **$82.75** (-2.82%; -$0.92). Brent moved $85.71→$88.54 across the two deploys, so energy remained sanity-only.
- Exact markets: U.S.-Iran invasion **21.5%**, Iran event **5.15%**, Iran test **5.5%**, NPT withdrawal **15.85%**, NATO Article 5 **7.5%**, Taiwan invasion **3.65%**, China-Taiwan clash **6.30%**, DPRK invasion **2.45%** (-0.60pp), Israel-Lebanon normalization **11.5%** (-1.0pp). Markets did not set scores.
- Artifacts: `data/deep_scan_full_fallback_20260727T180514Z.json`, `data/deep_scan_summary_20260727T180514Z.json`, `data/direct_source_checks_20260727T181300Z.json`, `data/polymarket_exact_snapshot_20260727T181032Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded twice. Deploy commits: `1f27fdc8`, corrected alignment `3af59163`, exact metadata `8634985f`.
- Final-head GitHub Pages run **30293354486** succeeded.
- Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, exact **79.696**, 20 trackers/news records and 14 aligned canonical signals.
- Required local/live markers are present: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/timeline checks and **31/31 non-smoke assertions** passed. The stock smoke fixture hit its fixed 60-second ceiling; identical **11/11 smoke assertions passed in 73.44s** from an isolated copy with only that harness timeout extended.
- HEAD, upstream and `origin/main` match; the tree was clean before this session-summary update. No command-deck HTML was hand-edited.

## Next watch
1. A concrete Russian retaliatory step, a fifth confirmed Romanian incursion, casualties or NATO Article 4/5 consultation.
2. A signed or directly acknowledged U.S.-Iran arrangement, verified Hormuz vessel-flow recovery, or resumed direct strikes after Trump’s warning.
3. Saudi retaliation, independent attribution of the Gulf drone wave or confirmed petroleum-site damage.
4. Implementation of an Iran-Oman transit mechanism, blockade relief, mine-clearance activity or verified zero commercial traffic.
5. A detailed, implemented Israeli Gaza concession or withdrawal timetable; alternatively collapse of the stabilization-force plan.
6. Independent confirmation of Sudan highway control or an RSF counterattack.
7. Verified additional North Korean movement, launcher relocation, prohibited firing/detonation or allied countermeasure.
8. Another damaged/sunk Red Sea vessel, verified Saudi pipeline damage or material Bab el-Mandeb traffic change.
9. An emerging crisis crossing the configured three-mention/two-independent-source gate.
