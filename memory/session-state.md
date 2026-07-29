# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-29 15Z morning deep scan; required deploy commits `3bd3dfb5` then correction `cbb5761b`; final Pages run `30465061747` succeeded.
- **Canonical scope:** 22 configured tracker IDs, oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 22 emerging-crisis candidates.
- **Global:** **83% / imminent**; exact additive coupled score **82.900%**, unchanged from 12Z.

## Evidence result
- No tracker score changed. `iran_conventional` remains capped at 100 after BBC quoted President Trump saying U.S. forces would hit Iran hard; all Iranian missiles in the reported attack were intercepted, and the IRGC’s tanker-damage claims remain unverified.
- `israel_lebanon` remains 90 raw / 100 coupled. Ynet, Yahoo, Shafaq News and Times of Israel broadened corroboration that the bulldozer strike was Hezbollah’s first drone attack since the June 19 truce; no casualty or executed Israeli response was verified.
- Iraq called an urgent security meeting after the joint U.S.-Saudi strikes; no militia retaliation or additional strike was executed by cutoff.
- No emerging candidate crossed the configured gate. Saudi-nuclear results were commentary on the 22 July civilian agreement, and Saudi-Yemen results overlapped `yemen_red_sea`.

## Signals
- No canonical signal activated or cleared. Iran, Lebanon and Iraq evidence was refreshed.
- A pipeline keyword false positive briefly added `south_china_sea:military_buildup` from a naval-posture phrase; it was removed, the phrase was neutralized, and the final deploy/live state verifies **22 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ raw | Zone | Active signals |
|---|---:|---:|---:|---|---|
| `iran_conventional` | 100 | 100 | 0 | imminent | `ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `hormuz_mining`, `military_buildup`, `oil_infrastructure_threat` |
| `israel_lebanon` | 90 | 100 | 0 | imminent | `ceasefire_violation`, `diplomacy_active` |
| `turkey` | 5 | 5 | 0 | deterrent | — |
| `india` | 15 | 15 | 0 | elevated | — |
| `russia` | 58 | 68 | 0 | imminent | — |
| `china` | 24 | 28 | 0 | critical | — |
| `north_korea` | 18 | 18 | 0 | elevated | — |
| `russia_ukraine` | 99 | 99 | 0 | imminent | — |
| `pakistan_afghanistan` | 46 | 46 | 0 | critical | — |
| `iran_nuclear` | 56 | 64 | 0 | imminent | `iaea_access_denied` |
| `sudan` | 94 | 94 | 0 | imminent | `military_buildup` |
| `israel_palestine` | 100 | 100 | 0 | imminent | `ceasefire_violation`, `diplomacy_active`, `holy_site_tension`, `military_buildup` |
| `south_sudan_abyei` | 19 | 19 | 0 | elevated | — |
| `eastern_drc` | 56 | 56 | 0 | imminent | — |
| `yemen_red_sea` | 95 | 95 | 0 | imminent | `ceasefire_violation`, `diplomacy_active`, `infrastructure_strike` |
| `mali_sahel` | 39 | 39 | 0 | critical | — |
| `south_china_sea` | 30 | 30 | 0 | critical | — |
| `somalia_gulf_of_aden` | 28 | 28 | 0 | critical | — |
| `southern_thailand` | 25 | 25 | 0 | critical | — |
| `kuwait_iraq_border` | 17 | 17 | 0 | elevated | — |
| `iraq_internal_conflict` | 40 | 40 | 0 | critical | `external_backing`, `infrastructure_strike`, `military_buildup` |
| `kenya_somalia_border` | 25 | 25 | 0 | critical | `infrastructure_strike`, `military_buildup` |

## Sources, energy and markets
- Tavily failed **27/27 searches** and **4/4 extracts** with HTTP 432.
- Fallback used 18 Google collector lanes / 121 raw items, 48 deep Google / 148, 48 deep Bing / 141, direct BBC browser evidence, terminal HTTP/RSS, official UN/NATO/EIA probes, OilPriceAPI and nine exact Gamma reads.
- IAEA/OPEC remained 403/challenge-blocked; Times of Israel direct access hit Cloudflare. Reuters oil coverage was headline-level and cross-checked against BBC and OilPriceAPI. Counts are raw and overlapping.
- Final deploy energy: Brent **$88.72**, WTI **$85.15**, gas **$2.68**, gold **$3,999.96**, heating oil **$4.34**. An earlier same-run vendor point reached Brent $90.50. Vendor snapshots remain outside the model.
- Exact markets: U.S.-Iran invasion **24.5%** (+1.0); Iran event/test/NPT **5.15% / 5.5% / 14.35%**; NATO Article 5 **7.5%**; Taiwan invasion/clash **3.85% / 7.0%**; DPRK invasion **4.95%** (+1.95); Israel-Lebanon normalization **14.0%** (+0.5). Markets remained sanity-only.
- Artifacts: `data/morning_deep_scan_sources_20260729T150204Z.json`, `data/deep_scan_15z_fallback_20260729T150318Z.json`, `data/polymarket_exact_snapshot_20260729T150505Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` succeeded twice; the second run removed the false-positive SCS signal and pushed `cbb5761bc688c4768d7f91bbaf78f50c003d51a9`.
- Pages run `30465061747` succeeded. Live root/state/timeline HTTP 200 expose 83/imminent, raw 82.90, 22 tracker/news records and 22 signals.
- Required local/live markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/history/timeline checks pass; **31 non-smoke tests passed**. The 11 stock copied-pipeline smoke setups hit their hard-coded 60-second timeout; the actual deploy completed successfully.
- No command-deck HTML was hand-edited.

## Next watch
1. Execution, target set and casualty outcome of Trump’s threatened U.S. response, or another Iranian missile/drone barrage.
2. The announced Israeli response, Hezbollah attribution or denial, casualties, another drone/rocket incident, or a 4 August talks breakdown.
3. Executed Iraqi militia retaliation, sovereignty measures after the urgent security meeting, casualty reconciliation, or another U.S./Saudi strike.
4. Acceptance, rejection or revised terms for the Oman Hormuz mechanism; independently verified tanker damage, sustained traffic recovery or mine clearance.
5. Implementation of Houthi shipping fees, extension of selective passage beyond Chinese vessels, Saudi/Jazan restart confirmation or verified new tanker damage.
6. Further Gaza/West Bank attacks or arrests, second-phase talks implementation or collapse.
7. A NATO Article 4/5 consultation, direct Russia-NATO incident or fresh Russia-Ukraine strategic threshold.
8. A kinetic China-Taiwan/China-Philippines encounter or DPRK operational firing/deployment.
9. Any emerging crisis crossing the configured three-mention/two-source gate.
