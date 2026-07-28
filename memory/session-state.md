# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-28 03Z morning deep scan; corrected deploy commit `6763e4c1` and exact provenance/energy commit `e35aa4b4` pushed.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact additive coupled score **79.760%**. No tracker probability moved.

## Evidence result
- U.S.-Iran direct strikes remain paused. Fresh AFP syndication repeated Trump's view that talks have a “good chance,” while Tehran disputes that direct talks are under way. No signed terms, verified Hormuz reopening, mine-clearance activity or resumed strike appeared.
- Fresh DPRK coverage was analysis of the existing missile-supply pipeline to Russia, not a new shipment, launch, troop movement or prohibited detonation.
- Fresh Yemen reports repeated the already-scored Houthi Saudi energy-site claim and government readiness rhetoric; no independently verified new launch, deployment or merchant-vessel loss appeared.
- India's MV Ruen piracy convictions concern a historical case. The M/T Asana hostage situation remains unchanged; no second hijacking occurred.
- No emerging tracker qualified. Post-00Z candidates were analysis, economic-corridor or force-structure commentary; Myanmar remains one monitor chain plus rewrites, Kaduna remains one attack event, and Saudi nuclear reporting concerns the civil program.

## Signals
- No evidence-backed canonical signal activated or cleared.
- The first deploy briefly overmatched a negated DPRK phrase into canonical `north_korea:nuclear_test`; the phrase and false projection were removed atomically, and the corrected deploy contains no DPRK signal.
- Tracker, zone, top-level and timeline projections align at **13 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ vs 00Z | Zone | Active signals |
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
| `yemen_red_sea` | 92 | 92 | 0 | imminent | `ceasefire_violation`, `infrastructure_strike`, `military_buildup` |
| `mali_sahel` | 39 | 39 | 0 | critical | — |
| `south_china_sea` | 30 | 30 | 0 | critical | — |
| `somalia_gulf_of_aden` | 28 | 28 | 0 | critical | — |
| `southern_thailand` | 25 | 25 | 0 | critical | — |
| `kuwait_iraq_border` | 17 | 17 | 0 | elevated | — |

## Sources, energy and markets
- Tavily failed **26/26 required searches** with HTTP 432.
- Fallback completed through **47 Google News RSS lanes / 294 items**, **47 Bing News RSS lanes / 242 items**, nine official/direct targets, terminal HTTP, OilPriceAPI and exact Gamma. IAEA/OPEC returned HTTP 403; RSS timestamps were treated as indexing dates unless the underlying event changed.
- Final deploy energy: Brent **$86.52 (-7.11%/24h)** and WTI **$80.81 (-4.99%/24h)**. Both extended the pause-driven decline; energy remained sanity-only.
- Exact markets: U.S.-Iran invasion **21.5%**, Iran event/test/NPT **5.1% / 5.5% / 15.9%**, NATO Article 5 **7.5%**, Taiwan invasion/clash **3.85% / 6.60%**, DPRK invasion **2.45%**, Israel-Lebanon normalization **14.5%**. Markets did not set tracker scores.
- Artifacts: `data/deep_scan_full_fallback_20260728T030319Z.json` and `data/polymarket_exact_snapshot_20260728T031453Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` ran twice: initial commit `a9bbeff5`; corrected final data/UI commit `6763e4c1`. Exact source/final-energy metadata commit `e35aa4b4` is pushed.
- GitHub Pages run `30325426700` succeeded. Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, raw **79.76**, 20 trackers/news records, exact fallback metadata and 13 aligned signals; the false DPRK signal is absent.
- Local/live command-deck markers pass: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/timeline checks pass. **31/31 non-smoke tests passed.** The stock combined run hit the known smoke fixture's 60-second pipeline ceiling (31 passed, 11 setup errors); the identical **11/11 smoke assertions passed in 87.90s** from an isolated copy with only that harness timeout raised to 180 seconds.
- HEAD/upstream/remote match at `e35aa4b4`; tree was clean before final memory logging. No command-deck HTML was hand-edited.

## Next watch
1. Signed/directly acknowledged U.S.-Iran terms, Hormuz traffic recovery, mine clearance or resumed direct strikes.
2. Official Saudi/Aramco damage or production confirmation, Baghdad investigation findings or retaliation.
3. Another Romanian incursion, concrete Russian retaliation, casualties or NATO Article 4/5 consultation.
4. A fresh China-Philippines hostile encounter, casualty, vessel seizure or formal treaty consultation.
5. Fresh DPRK deployment, launcher movement, operational missile firing, prohibited detonation or allied countermeasure.
6. Independent Khartoum-El Obeid route-control confirmation, an RSF reversal or verified drone-attack casualties.
7. A second Gulf of Aden hijacking, change in Asana hostage status or material Bab el-Mandeb/Hormuz traffic shift.
8. A fresh southern Thailand attack or verified deployment sufficient to reactivate a canonical marker.
9. Any emerging crisis crossing the configured three-mention/two-independent-source gate.
