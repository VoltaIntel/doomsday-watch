# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-28 06Z morning deep scan; automated data/UI deploy `80f93ab5` and exact source/final-energy metadata commit `75a4eded` pushed.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact additive coupled score **79.760%**. No tracker probability moved.

## Evidence result
- MarineTraffic counted **29 verified Hormuz crossings from 24-26 July**: 21 outbound and eight inbound. Passage remains severely constrained, but traffic is neither zero nor physically closed. The U.S.-Iran direct-strike pause held; Iran's foreign minister discussed strait security with Saudi Arabia and Oman. No signed settlement or normalized flow appeared.
- A U.S. State Department official told AFP that the next Israel-Lebanon session is set for **4-6 August in Rome**, covering framework implementation, pilot zones and border issues. Lebanon's NNA simultaneously reported Israeli bombing/demolition operations in Majdal Zoun, Mansouri and Bint Jbeil on 28 July.
- BBC confirmed Ukraine's 25 July Caspian strike on the Iranian vessel **Anna**. Ukraine says the cargo was military; Iran and Russia say civilian. Iran reports one sailor killed and several injured and threatened a response. The incident directly links the Ukraine and Iran wars but adds no configured threshold to a lane already at 99%.
- Jordan reported downing an unidentified drone in its eastern desert. No new Kuwait-specific event was verified.
- No emerging tracker qualified. Reuters' ACLED-based Myanmar report records more than a dozen mass killings and over 450 civilian deaths in the first half of 2026, but the current publication cluster remains one Reuters/ACLED evidence chain rather than two independent current streams.

## Signals
- Reactivated canonical `israel_lebanon:diplomacy_active` on the dated Rome session and pilot-zone implementation work.
- Refreshed evidence for `iran_conventional:diplomacy_active`, `iran_conventional:hormuz_controlled_not_closed`, and `israel_lebanon:ceasefire_violation`.
- Tracker, zone and timeline projections align at **14 canonical signals**. No signal was cleared and no numeric score moved because southern Lebanon field violations continue alongside the channel.

## Per-tracker table
| Tracker | Raw | Coupled | Δ vs 03Z | Zone | Active signals |
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
- Tavily failed **10/10 attempted searches** and **5/5 extraction attempts** with HTTP 432 before the repeated backend failure was diagnosed.
- Fallback completed through **47 Google News RSS lanes / 185 items**, **47 Bing News RSS lanes / 240 items**, 15 exact-event follow-ups, browser/direct publisher pages, Jina, nine official/direct targets, OilPriceAPI and exact Gamma. IAEA/OPEC returned HTTP 403.
- A March South Pars article with a fresh RSS timestamp and an uncorroborated resumption-of-strikes headline were inspected and excluded.
- Final energy: Brent **$87.85 (-6.80%/24h)** and WTI **$82.25 (-2.59%/24h)**. Energy remained sanity-only.
- Exact markets: U.S.-Iran invasion **21.5%**, Iran event/test/NPT **5.1% / 5.5% / 15.9%**, NATO Article 5 **7.5%**, Taiwan invasion/clash **3.85% / 6.55%**, DPRK invasion **2.45%**, Israel-Lebanon normalization **15.0%**. Markets did not set tracker scores.
- Artifacts: `data/deep_scan_full_fallback_20260728T060405Z.json`, `data/direct_followups_20260728T060903Z.json`, and `data/polymarket_exact_snapshot_20260728T061137Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` succeeded and pushed `80f93ab5`; exact source and final-energy metadata commit `75a4eded` is pushed.
- Pages run `30334525799` succeeded for the data/UI deploy. Cache-busted live root/state/timeline return HTTP 200 and expose **80 / imminent**, raw **79.76**, `morning_deep_scan_06z`, 20 tracker/news records, exact source metadata and 14 aligned signals.
- Local/live command-deck markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/timeline checks pass. **31/31 non-smoke tests passed.** The stock smoke fixture hit its known 60-second copied-pipeline ceiling; the identical **11/11 smoke assertions passed in 83.27 seconds** in an isolated copy with only that harness timeout raised to 180 seconds.
- No command-deck HTML was hand-edited.

## Next watch
1. Implementation or collapse of the 4-6 August Rome session, verified pilot-zone withdrawals, or a broader Israel-Hezbollah strike sequence.
2. Signed/directly acknowledged U.S.-Iran terms, sustained Hormuz recovery, mine clearance or resumed direct strikes.
3. Iranian retaliation for the Anna strike, another Ukrainian strike on Iranian-linked shipping or convoy changes.
4. Official Saudi/Aramco damage or production confirmation, Baghdad findings or retaliation.
5. Another Romanian incursion, casualties or NATO Article 4/5 consultation.
6. A fresh China-Philippines hostile encounter, casualty, seizure or treaty consultation.
7. Fresh DPRK deployment, launcher movement, operational firing or prohibited detonation.
8. A second Gulf of Aden hijacking, Asana hostage-status change or material maritime-flow shift.
9. Two independent current Myanmar streams or another emerging crisis crossing the configured gate.
