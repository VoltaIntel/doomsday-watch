# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-29 09Z morning deep scan; required deploy `05bddc8b`, exact-source metadata `3a3dbee1`, and Pages runs `30438772670` / `30438908454` succeeded.
- **Canonical scope:** 22 configured tracker IDs, oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 22 emerging-crisis candidates.
- **Global:** **82% / imminent**; exact additive coupled score **82.480%**, up 0.200 point from 82.280%.

## Evidence result
- `iraq_internal_conflict` rose **30 → 40 raw/coupled / critical**. BBC’s updated direct report says the PMF reports at least 20 fighters killed and 32 wounded in joint U.S.-Saudi strikes on several bases. Al Jazeera/Reuters separately reports PMF condemnation and an Iran-backed group’s threat of a harsh response. No executed retaliation was verified by cutoff.
- `israel_palestine` received evidence-only reinforcement from more than 70 reported West Bank detentions and further Gaza mosque-strike syndication, but remains capped at 100.
- Iran’s renewed missile attack on U.S. forces remains confirmed; CENTCOM says every missile was intercepted. IRGC/Houthi tanker-hit claims still lack independent damage confirmation.
- All other tracker scores held. No emerging candidate crossed the configured three-mention/two-source crisis gate.

## Signals
- No canonical signal activated or cleared.
- Refreshed `iraq_internal_conflict:external_backing`, `iraq_internal_conflict:infrastructure_strike`, `iraq_internal_conflict:military_buildup` and `israel_palestine:ceasefire_violation` evidence.
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
| `iraq_internal_conflict` | 40 | 40 | **+10** | critical | `external_backing`, `infrastructure_strike`, `military_buildup` |
| `kenya_somalia_border` | 25 | 25 | 0 | critical | `infrastructure_strike`, `military_buildup` |

## Sources, energy and markets
- Tavily failed **26/26 searches** and **2/2 extracts** with HTTP 432.
- Fallback used 18 collector Google lanes / 119 items, 48 deep Google lanes / 151, 48 deep Bing lanes / 153, direct browser reads of BBC/Al Jazeera, terminal HTTP/RSS, official UN/NATO/EIA probes, OilPriceAPI and nine exact Gamma reads.
- IAEA/OPEC returned 403; IAEA browser access remained challenge-blocked; OCHA OPT and the UN Sudan-tag feed returned 404. Counts are raw and overlapping.
- Final deploy energy: Brent **$86.92**, WTI **$82.12**, gas **$2.65**, gold **$4,039.25**, heating oil **$4.26**. Vendor snapshots remain outside the model.
- Exact markets: U.S.-Iran invasion **23.5%**; Iran event/test/NPT **5.15% / 5.5% / 14.4%**; NATO Article 5 **7.5%**; Taiwan invasion/clash **3.9% / 6.85%**; DPRK invasion **3%**; Israel-Lebanon normalization **13.5%**. Markets remained sanity-only.
- Artifacts: `data/morning_deep_scan_sources_20260729T090253Z.json`, `data/deep_scan_09z_fallback_20260729T090437Z.json`, `data/polymarket_exact_snapshot_20260729T090841Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` succeeded, regenerated `index.html`, and pushed `05bddc8b95b601a43e2c0d34915eda7dacef3bc3`.
- Exact fallback metadata commit `3a3dbee1eeee8603f322c76fd3780ed49a3012e5`; Pages runs `30438772670` and `30438908454` succeeded.
- Cache-busted live root/state/timeline HTTP 200 expose **82 / imminent**, raw **82.48**, 22 tracker/news records, Iraq 40 and 22 signals.
- Required local/live markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/history/timeline checks pass; **31 tests passed and 11 smoke tests were deselected**. No command-deck HTML was hand-edited.

## Next watch
1. Executed militia retaliation, Iraqi government/PMF casualty reconciliation, sovereignty measures, the prime minister’s Saudi visit or another U.S./Saudi strike.
2. Another Iranian missile barrage, casualties, independently verified tanker damage, a U.S. strike response against Iran or an operational ceasefire.
3. Acceptance, rejection or revised terms for the Oman Hormuz mechanism; sustained traffic recovery or verified mine clearance.
4. Further Gaza/West Bank attacks or arrests, implementation of second-phase talks, or a Lebanon withdrawal/disarmament step or talks failure.
5. Saudi Aramco/Jazan restart confirmation, attribution of UKMTO 098-26 or verified NCC Ghazal damage.
6. Kenyan casualty/investigation updates, another Mandera/Garissa attack, a confirmed cross-border pursuit or KDF posture change.
7. Iranian/Russian retaliation for Anna, another Romanian incursion or NATO Article 4/5 consultation.
8. A kinetic China-Taiwan/China-Philippines encounter or DPRK operational firing/deployment.
9. Release or harm of the eight reported Egyptian sailors or another Gulf of Aden hijacking.
10. Any other emerging crisis crossing the configured three-mention/two-source gate.
