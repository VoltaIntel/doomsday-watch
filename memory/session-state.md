# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-29 03Z morning deep scan; data/UI deploy `fa0d3346`, exact source/deploy metadata `8890f6e0`, and Pages runs `30419224667` / `30419312551` succeeded.
- **Canonical scope:** 21 tracker IDs after one evidence-gated auto-detection, oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 22 emerging-crisis candidates.
- **Global:** **82% / imminent**; exact additive coupled score **81.780%**, up 0.600 point from 81.180%.

## Evidence result
- Auto-detection added canonical `iraq_internal_conflict` at **30 raw / 30 coupled / critical**. AP, Al Jazeera/Reuters and directly accessible official CENTCOM and Saudi Defense Ministry statements confirm coordinated U.S.-Saudi strikes on multiple militia logistics/weapons sites in eastern Iraq after more than 30 IRGC-directed drone attacks in 72 hours.
- Iraq ordered an investigation and said its territory must not be used to attack partners. The Islamic Resistance in Iraq denied responsibility and threatened a response; no casualty total was available.
- Iran's surprise missile barrage against U.S. forces preceded and was unrelated to the Iraq strikes, according to CENTCOM; all missiles were intercepted. `iran_conventional` remains capped at 100.
- Al Jazeera/Reuters reinforced the 28 July Gaza attack cycle: at least one Palestinian killed, more than 20 wounded, a mosque destroyed and displaced-person tents hit. `israel_palestine` remains capped at 100.
- A U.S.-Taiwan coast-guard cooperation image after Beijing patrols was a posture item, not a blockade or kinetic threshold. Other existing tracker scores held.
- The other 21 emerging candidates did not cross the configured gate after stale hits, analysis, false matches, rewrites and already-covered spillover were removed.

## Signals
- Activated `iraq_internal_conflict:external_backing`, `iraq_internal_conflict:infrastructure_strike` and `iraq_internal_conflict:military_buildup`.
- Refreshed existing Iran conventional, Israel-Palestine and Yemen/Red Sea evidence. No canonical signal cleared.
- Tracker, zone, top-level and timeline projections align at **20 canonical signals**.

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
| `iraq_internal_conflict` | 30 | 30 | **new** | critical | `external_backing`, `infrastructure_strike`, `military_buildup` |

## Sources, energy and markets
- Tavily failed **25/25 searches** and **5/5 extraction URLs** with HTTP 432.
- Fallback used 18 collector Google lanes / 121 items, 69 deep Google lanes / 623, 69 deep Bing lanes / 220, browser/direct publisher pages, terminal HTTP/RSS, UN/NATO/EIA official pages and feeds, official CENTCOM/Saudi statements, OilPriceAPI and nine exact Gamma reads.
- IAEA news/press and OPEC returned HTTP 403; UKMTO was Cloudflare-blocked; the CENTCOM website denied access while its official X statement loaded; Reuters direct access remained DataDome-blocked. Counts are raw and overlapping.
- Final deploy energy: Brent **$87.49**, WTI **$82.24**, gas **$2.65**, gold **$4,033.77**, heating oil **$4.26**. Price checks are vendor-volatile and outside the model.
- Exact markets: U.S.-Iran invasion **23.5%** (-1 point from 00Z); Iran event/test/NPT **5.15% / 5.5% / 15.55%**; NATO Article 5 **7.5%**; Taiwan invasion/clash **3.75% / 6.6%**; DPRK invasion **3%**; Israel-Lebanon normalization **13.5%**. Markets remained sanity-only.
- Artifacts: `data/morning_deep_scan_sources_20260729T030158Z.json`, `data/deep_scan_03z_fallback_20260729T030345Z.json`, `data/polymarket_exact_snapshot_20260729T030854Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` succeeded, regenerated `index.html`, committed/pushed `fa0d334640a1ef91f439ddee6a71e442aeb51d70`.
- Exact metadata commit `8890f6e06506d3460afb00f866ae442d3e5f0d52`; Pages runs `30419224667` and `30419312551` succeeded.
- Cache-busted live root/state/timeline HTTP 200 expose **82 / imminent**, raw **81.78**, 21 tracker/news records, `iraq_internal_conflict` 30, 20 signals and exact fallback metadata.
- Required local/live markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/history/timeline checks pass; **31/31 non-smoke tests passed**. No command-deck HTML was hand-edited.

## Next watch
1. Iraqi government/PMF casualty or damage findings, a sovereignty response, militia retaliation or another U.S./Saudi strike.
2. Another Iranian missile barrage, casualties, a U.S. strike response against Iran or an operational ceasefire.
3. Acceptance, rejection or revised terms for the Oman Hormuz mechanism; sustained traffic recovery, mine clearance or new tanker damage.
4. Further Gaza attacks, execution/cancellation of the West Bank camp order or second-phase talks.
5. Saudi Aramco/Jazan confirmation, attribution of UKMTO 098-26 or verified NCC Ghazal damage.
6. Lebanon pilot withdrawals/disarmament, failure of the 4 August Rome talks or widened strikes.
7. Iranian/Russian retaliation for Anna, another Romanian incursion or NATO Article 4/5 consultation.
8. A kinetic China-Taiwan/China-Philippines encounter or DPRK operational firing/deployment.
9. Release or harm of the eight Egyptian sailors or another Gulf of Aden hijacking.
10. Any other emerging crisis crossing the configured three-mention/two-source gate.
