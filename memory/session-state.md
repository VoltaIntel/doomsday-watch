# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-29 06Z morning deep refresh; required deploy `07d4dd29`, exact-source/final metadata `75ac3c1e`, and Pages runs `30427695877` / `30427797498` succeeded.
- **Canonical scope:** 22 tracker IDs after one evidence-gated auto-detection, oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 21 emerging-crisis candidates.
- **Global:** **82% / imminent**; exact additive coupled score **82.280%**, up 0.500 point from 81.780%.

## Evidence result
- Auto-detection added canonical `kenya_somalia_border` at **25 raw / 25 coupled / critical**. Direct police-sourced reporting by The Star and The Eastleigh Voice confirms five Kenyan security officers were killed in a 28 July IED ambush near the Somalia border and a responding armoured vehicle was destroyed without further casualties. The same police account documents a telecom-mast attack on 26 July and an RPG attack on Arabia Police Station on 24 July. AFP supplied a third publisher chain.
- BBC directly corroborated Iran's multiple-ballistic-missile attack on U.S. forces. CENTCOM said all missiles were intercepted; Iran said it targeted a U.S. base in Jordan. The IRGC separately claimed three tanker hits in Hormuz, but no independent damage confirmation was found. `iran_conventional` remains capped at 100.
- BBC/DW broadened corroboration of the coordinated U.S.-Saudi Iraq strike cluster. No independently verified militia retaliation, casualty total or new strike cycle appeared by cutoff; `iraq_internal_conflict` holds at 30.
- All other pre-existing tracker scores held. Other emerging candidates were stale, analysis, false matches, de-escalatory monitoring, rewrites or below the configured gate.

## Signals
- Activated `kenya_somalia_border:infrastructure_strike` and `kenya_somalia_border:military_buildup`.
- Refreshed canonical Iran conventional and Iraq internal-conflict evidence. No existing signal cleared.
- Tracker, zone, top-level and timeline projections align at **22 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ raw | Zone | Active signals |
|---|---:|---:|---:|---|---|
| `iran_conventional` | 100 | 100 | 0 | imminent | `ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `hormuz_mining`, `military_buildup`, `oil_infrastructure_threat` |
| `israel_lebanon` | 87 | 97 | 0 | imminent | `ceasefire_violation`, `diplomacy_active` |
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
| `iraq_internal_conflict` | 30 | 30 | 0 | critical | `external_backing`, `infrastructure_strike`, `military_buildup` |
| `kenya_somalia_border` | 25 | 25 | **new** | critical | `infrastructure_strike`, `military_buildup` |

## Sources, energy and markets
- Tavily failed **25/25 searches** with HTTP 432. Three extraction URLs also returned 432; one PDF extraction was URL-safety blocked.
- Fallback used 18 collector Google lanes / 120 items, 46 deep Google lanes / 190, 46 deep Bing lanes / 107, browser/direct BBC and Kenyan pages, terminal HTTP/RSS, official UN/NATO/EIA pages and feeds, OilPriceAPI and nine exact Gamma reads.
- IAEA news/press and OPEC returned HTTP 403; the IAEA browser remained challenge-blocked; OCHA and the UN Sudan tag feed returned 404. Counts are raw and overlapping.
- Final deploy energy: Brent **$87.31**, WTI **$82.25**, gas **$2.65**, gold **$4,034.76**, heating oil **$4.24**. Price checks are vendor-volatile and outside the model.
- Exact markets: U.S.-Iran invasion **23.5%**; Iran event/test/NPT **5.15% / 5.5% / 14.2%**; NATO Article 5 **7.5%**; Taiwan invasion/clash **3.95% / 7.0%**; DPRK invasion **3%**; Israel-Lebanon normalization **14%**. Since 03Z, NPT withdrawal fell 1.35 points; the other moves were 0.5 point or less. Markets remained sanity-only.
- Artifacts: `data/morning_deep_scan_sources_20260729T060321Z.json`, `data/deep_scan_06z_fallback_20260729T060428Z.json`, `data/polymarket_exact_snapshot_20260729T060837Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` succeeded, regenerated `index.html`, committed/pushed `07d4dd29fd39498c6ba03ea56dce30f690a37b8f`.
- Exact fallback/deploy metadata commit `75ac3c1eeba4dbb19cd5558e69762c86a9cf9650`; Pages runs `30427695877` and `30427797498` succeeded.
- Cache-busted live root/state/timeline HTTP 200 expose **82 / imminent**, raw **82.28**, 22 tracker/news records, `kenya_somalia_border` 25, 22 signals and exact fallback metadata.
- Required local/live markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/history/timeline checks pass; **31/31 non-smoke tests passed**. No command-deck HTML was hand-edited.

## Next watch
1. Kenyan casualty/investigation updates, another Mandera/Garissa attack, a confirmed cross-border pursuit or KDF posture change.
2. Another Iranian missile barrage, casualties, independently verified tanker damage, a U.S. strike response against Iran or an operational ceasefire.
3. Militia retaliation, Iraqi government/PMF casualty findings, a sovereignty response or another U.S./Saudi strike in Iraq.
4. Acceptance, rejection or revised terms for the Oman Hormuz mechanism; sustained traffic recovery or verified mine clearance.
5. Further Gaza attacks, implementation of second-phase talks, or a Lebanon withdrawal/disarmament step or talks failure.
6. Saudi Aramco/Jazan restart confirmation, attribution of UKMTO 098-26 or verified NCC Ghazal damage.
7. Iranian/Russian retaliation for Anna, another Romanian incursion or NATO Article 4/5 consultation.
8. A kinetic China-Taiwan/China-Philippines encounter or DPRK operational firing/deployment.
9. Release or harm of the eight reported Egyptian sailors or another Gulf of Aden hijacking.
10. Any other emerging crisis crossing the configured three-mention/two-source gate.
