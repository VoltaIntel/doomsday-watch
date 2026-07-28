# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-28 15Z morning deep scan; corrected data/UI deploy `ff1fec3a`, final metadata commit `df71666c`, and metadata-head Pages run `30373274880` succeeded.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact additive coupled score **79.760%**. No tracker probability moved.

## Evidence result
- Israeli Defence Minister Katz confirmed U.S. aircraft operated from Israeli bases against Iran in recent weeks and reiterated conditional readiness. Multiple reports on the same interview say Washington is still withholding approval for Iranian energy/power-site strikes. This is retrospective/conditional; the direct U.S.-Iran strike pause held at the 15Z cutoff.
- Senior U.S. officials said the IDF began pilot redeployment in Zawtar al-Gharbiyeh and Washington will pursue implementation, but full withdrawal remains conditional on Hezbollah disarmament and restored Lebanese sovereignty. Same-day strikes prevent a numeric de-escalation.
- Reuters reports the Kremlin now calls Ukraine's Caspian strike on the Iranian vessel Anna an assault on Iran itself and accuses Kyiv of widening the geography of attacks. No Russian retaliation was announced.
- Marine Insight newly covered the Houthi claim, first carried by Reuters on 27 July, against Yanbu/east-west oil infrastructure. Saudi Arabia and Aramco still have not confirmed a hit or production loss; the event was already scored.
- No emerging tracker qualified. A Myanmar soldier and two police officers crossing into Bangladesh produced one current source, below the configured gate.

## Signals
- No canonical signal activated or cleared.
- Refreshed evidence for `iran_conventional:diplomacy_active`, `israel_lebanon:diplomacy_active`, and `yemen_red_sea:infrastructure_strike`.
- The first deploy overmatched retrospective source wording into `iran_conventional:bomber_redeployment`; that false projection was removed before the corrected final deploy.
- Tracker, zone, top-level and timeline projections align at **14 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ vs 12Z | Zone | Active signals |
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
- Tavily failed **27/27 searches** and **5/5 extract URLs** with HTTP 432.
- Fallback completed through 47 Google lanes / 155 items, 47 Bing lanes / 245 items, 16 exact-event lanes / 83 raw items, two direct JPost RSS feeds, browser/direct pages, terminal HTTP, ten official/direct targets, OilPriceAPI and exact Gamma.
- IAEA news/press and OPEC returned HTTP 403; the IAEA browser path presented a verification challenge. RSS recency and source-chain caveats were audited.
- Final energy: Brent **$86.62 (-3.69%/24h)** and WTI **$81.37 (-2.28%/24h)**. Energy remained sanity-only.
- Exact markets: U.S.-Iran invasion **21.5%**; Iran event/test/NPT **5.2% / 5.5% / 15.9%**; NATO Article 5 **7.5%**; Taiwan invasion/clash **3.75% / 6.65%**; DPRK invasion **3.10%**; Israel-Lebanon normalization **15.0%**. The DPRK move was +0.65pp on only $52 reported 24h volume and did not affect scores.
- Artifacts: `data/deep_scan_15z_fallback_20260728T150248Z.json`, `data/targeted_followups_20260728T150411Z.json`, and `data/polymarket_exact_snapshot_20260728T150821Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` succeeded. Initial commit `875191fa` contained the retrospective phrase overmatch; corrected deploy `ff1fec3a` removed it and is pushed.
- Pages run `30372860739` succeeded for corrected commit `ff1fec3a39b832d7a8678e2baf98ba441a968e2c`.
- Cache-busted live root/state/timeline return HTTP 200 and expose **80 / imminent**, raw **79.76**, `morning_deep_scan_15z`, 20 tracker/news records and 14 aligned signals; the false bomber signal is absent.
- Local/live command-deck markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/timeline checks pass. **31/31 non-smoke tests passed.** The stock smoke fixture hit its known 60-second copied-pipeline ceiling; the identical **11/11 smoke assertions passed in 74.81 seconds** in an isolated copy with only that harness timeout raised to 180 seconds.
- No command-deck HTML was hand-edited.

## Next watch
1. Any fresh U.S., Israeli or Iranian strike, change in U.S. approval for Iranian energy targets, or a verified Iranian-backed drone impact.
2. Signed U.S.-Iran terms, sustained Hormuz recovery, mine clearance or collapse of the direct-strike pause.
3. Verified Lebanon pilot withdrawals, Hezbollah disarmament steps, framework collapse or widened field strikes.
4. Russian or Iranian retaliation for the Anna strike or formal Russia-Iran operational coordination.
5. Saudi/Aramco damage or production confirmation, another Houthi/Saudi strike or announced Pakistani involvement.
6. Another Romanian incursion, casualties or NATO Article 4/5 consultation.
7. A fresh China-Philippines encounter, casualty, seizure or treaty consultation.
8. Fresh DPRK deployment, launcher movement, operational firing or prohibited detonation; ignore low-volume market noise absent evidence.
9. A second Gulf of Aden hijacking or material Asana status change.
10. A second independent Myanmar-Bangladesh border stream or another emerging crisis crossing the configured gate.
