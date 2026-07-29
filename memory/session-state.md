# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-29 12Z morning deep scan; required deploy `d12c357a`, exact-source metadata `1c0a74fe`, and Pages runs `30450656991` / `30450788872` succeeded.
- **Canonical scope:** 22 configured tracker IDs, oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 22 emerging-crisis candidates.
- **Global:** **83% / imminent**; exact additive coupled score **82.900%**, up 0.420 point from 82.480%.

## Evidence result
- `israel_lebanon` rose **87 → 90 raw / 97 → 100 coupled**. The IDF confirmed a Hezbollah drone struck an Israeli military bulldozer in south Lebanon and described the incident as breaking the truce; Israeli reporting says a response is planned. Retrieved coverage identified no casualty.
- Iraqi and regional outlets report Prime Minister Mohammed Shia al-Sudani cancelled his Saudi visit after the joint strikes; no militia retaliation was executed by cutoff.
- Reuters reports the Houthis are considering shipping fees while China negotiates selective vessel passage. This does not establish restored general navigation or a new attack cycle.
- Harder Hormuz rhetoric did not establish closure/zero traffic. Amnesty's Gao report did not establish a new Mali operational threshold. All other tracker scores held; no emerging candidate crossed the configured gate.

## Signals
- No canonical signal activated or cleared.
- Refreshed `israel_lebanon:ceasefire_violation`, `iraq_internal_conflict:external_backing`, `iraq_internal_conflict:infrastructure_strike`, `iraq_internal_conflict:military_buildup` and `yemen_red_sea:diplomacy_active` evidence.
- Tracker, zone, top-level and timeline projections align at **22 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ raw | Zone | Active signals |
|---|---:|---:|---:|---|---|
| `iran_conventional` | 100 | 100 | 0 | imminent | `ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `hormuz_mining`, `military_buildup`, `oil_infrastructure_threat` |
| `israel_lebanon` | 90 | 100 | **+3** | imminent | `ceasefire_violation`, `diplomacy_active` |
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
- Tavily failed **28/28 searches** and **4/4 extracts** with HTTP 432.
- Fallback used an 18-lane Google collector / 121 raw items, 48 deep Google / 144, 48 deep Bing / 145, Google News/browser publisher reads, terminal HTTP/RSS, official UN/NATO/EIA probes, OilPriceAPI and nine exact Gamma reads.
- IAEA/OPEC remained 403/challenge-blocked; Reuters direct pages were device-check blocked. Counts are raw and overlapping.
- Final deploy energy: Brent **$88.00**, WTI **$82.91**, gas **$2.65**, gold **$4,032.26**, heating oil **$4.14**. Vendor snapshots remain outside the model.
- Exact markets: U.S.-Iran invasion **23.5%**; Iran event/test/NPT **5.15% / 5.5% / 14.35%**; NATO Article 5 **7.5%**; Taiwan invasion/clash **3.85% / 7.0%**; DPRK invasion **3%**; Israel-Lebanon normalization **13.5%**. Markets remained sanity-only.
- Artifacts: `data/morning_deep_scan_sources_20260729T120207Z.json`, `data/deep_scan_12z_fallback_20260729T120451Z.json`, `data/polymarket_exact_snapshot_20260729T120716Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` succeeded, regenerated `index.html`, and pushed `d12c357a5e8385528a3fb91931539f78bfbe82e6`.
- Exact fallback metadata commit `1c0a74febeaddc72fcd4a0dfb2f6c1e3e1a4b391`; Pages runs `30450656991` and `30450788872` succeeded.
- Live root/state/timeline HTTP 200 expose **83 / imminent**, raw **82.90**, 22 tracker/news records, Israel-Lebanon 90/100 and 22 signals.
- Required local/live markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/history/timeline checks pass; **31 tests passed and 11 smoke tests were deselected**. No command-deck HTML was hand-edited.

## Next watch
1. The announced Israeli response, Hezbollah attribution or denial, casualties, another drone/rocket incident, or a pilot-zone/4 August talks breakdown.
2. Executed Iraqi militia retaliation, sovereignty measures, casualty reconciliation, or another U.S./Saudi strike after the cancelled al-Sudani visit.
3. Another Iranian missile barrage, casualties, independently verified tanker damage, a U.S. strike response against Iran or an operational ceasefire.
4. Acceptance, rejection or revised terms for the Oman Hormuz mechanism; sustained traffic recovery or verified mine clearance.
5. Implementation of Houthi shipping fees, extension of selective passage beyond Chinese vessels, Saudi/Jazan restart confirmation or verified NCC Ghazal damage.
6. Further Gaza/West Bank attacks or arrests, second-phase talks implementation or collapse.
7. Iranian/Russian retaliation for the Anna strike, another Romanian incursion or NATO Article 4/5 consultation.
8. A kinetic China-Taiwan/China-Philippines encounter or DPRK operational firing/deployment.
9. Any emerging crisis crossing the configured three-mention/two-source gate.
