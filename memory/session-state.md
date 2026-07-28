# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-28 18Z morning deep scan; data/UI deploy `d5c4393c`, exact source/deploy metadata `c60b1fdd`, and Pages run `30386923768` succeeded.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, oil/energy, IAEA/UN, NATO/allied positions, nine exact Polymarket contracts and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact additive coupled score **79.860%**, up 0.100 point from 15Z.

## Evidence result
- `israel_palestine` rose **92 → 94 raw/coupled** after Haaretz and The Jerusalem Post reported that Defence Minister Katz ordered the IDF to prepare a West Bank refugee-camp takeover and expulsion. Reporting had not established execution or identified the camp, so the increase was limited to two points.
- Reuters reports China opened direct Houthi talks for individual oil-tanker passage through the southern Red Sea. This is a selective commercial-security channel, not a general end to the 20 July blockade.
- Reuters also reports Oman presented Iran with a Gulf-backed Hormuz management proposal involving voluntary usage fees. Core Iran-U.S. disagreements remain and no signed arrangement, normalized traffic or mine clearance was announced.
- Sudan army gains, a Goma third-term protest and continued Iran/Lebanon/Yemen reporting reinforced existing lanes without meeting a second numeric threshold.
- No emerging tracker qualified. The apparent Thailand-Cambodia item concerned scam-centre trafficking, and Myanmar-Bangladesh remained below the configured three-mention/two-independent-source gate.

## Signals
- Activated `israel_palestine:military_buildup` on the explicit IDF preparation order.
- Activated `yemen_red_sea:diplomacy_active` on direct China-Houthi tanker negotiations.
- Refreshed `iran_conventional:diplomacy_active` on the Oman proposal.
- No canonical signal cleared. Tracker, zone, top-level and timeline projections align at **16 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Δ vs 15Z | Zone | Active signals |
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
| `israel_palestine` | 94 | 94 | **+2** | imminent | `diplomacy_active`, `holy_site_tension`, `military_buildup` |
| `south_sudan_abyei` | 19 | 19 | 0 | elevated | — |
| `eastern_drc` | 56 | 56 | 0 | imminent | — |
| `yemen_red_sea` | 92 | 92 | 0 | imminent | `ceasefire_violation`, `diplomacy_active`, `infrastructure_strike`, `military_buildup` |
| `mali_sahel` | 39 | 39 | 0 | critical | — |
| `south_china_sea` | 30 | 30 | 0 | critical | — |
| `somalia_gulf_of_aden` | 28 | 28 | 0 | critical | — |
| `southern_thailand` | 25 | 25 | 0 | critical | — |
| `kuwait_iraq_border` | 17 | 17 | 0 | elevated | — |

## Sources, energy and markets
- Tavily failed **25/25 searches** and **5/5 extract URLs** with HTTP 432.
- Fallback used 25 Google primary lanes / 150 items, 25 Bing primary lanes / 158 items, 22 emerging lanes per engine / 28 Google + 92 Bing items, 25 targeted lanes per engine / 411 Google + 71 Bing items, direct/browser pages, terminal HTTP, official feeds/pages, OilPriceAPI and exact Gamma.
- IAEA news/press and OPEC returned HTTP 403; IAEA browser access remained on a verification challenge. Reuters direct access was DataDome-blocked, so Reuters claims were checked through headline indexes and accessible agency syndication.
- Final energy: Brent **$84.27 (-5.07%/24h)** and WTI **$79.55 (-3.90%)**; versus 15Z they fell **$2.35 / $1.82**. Price relief does not prove restored physical chokepoint flows.
- Exact markets: U.S.-Iran invasion **21.5%**; Iran event/test/NPT **5.2% / 5.5% / 15.5%**; NATO Article 5 **7.5%**; Taiwan invasion/clash **3.75% / 6.55%**; DPRK invasion **3.0%** on $52 daily volume; Israel-Lebanon normalization **13.5%**. Markets remained sanity-only.
- Artifacts: `data/deep_scan_18z_fallback_20260728T180333Z.json`, `data/targeted_followups_18z_20260728T180456Z.json`, `data/polymarket_exact_snapshot_20260728T180836Z.json`.

## Deployment and verification
- Required `bash scripts/deploy.sh` succeeded and pushed data/UI commit `d5c4393c19488c7cd64723d41ad858fad848993f`.
- Exact source/deploy metadata commit `c60b1fdda7921e0240a6a91f65f09ee1d4637461`; Pages run `30386923768` succeeded.
- Cache-busted live root/state/timeline return HTTP 200 and expose **80 / imminent**, raw **79.86**, `morning_deep_scan_18z`, 20 tracker/news records, Israel-Palestine 94 and 16 aligned signals.
- Required markers pass locally and live: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/history/timeline checks pass. **31/31 non-smoke tests passed.** The stock copied-pipeline fixture hit its known 60-second ceiling; the identical **11/11 smoke assertions passed in 82.75 seconds** in an isolated copy with only that timeout raised to 180 seconds.
- No command-deck HTML was hand-edited.

## Next watch
1. Execution, named location, force movement, displacement or resistance after Katz’s camp order; or cancellation/clarification.
2. Whether China-Houthi clearances broaden, fail or are followed by another tanker attack.
3. Acceptance/rejection of Oman’s Hormuz plan; signed terms, sustained traffic recovery or mine clearance.
4. Any fresh U.S., Israeli or Iranian strike or U.S. approval shift on energy targets.
5. Verified Lebanon pilot withdrawals/disarmament, framework collapse or wider strikes.
6. Saudi/Aramco damage confirmation, production loss or another Houthi/Saudi strike.
7. Another Romanian incursion, casualties or NATO Article 4/5 consultation.
8. Russia/Iran retaliation for the Anna strike or formal operational coordination.
9. A new China-Philippines encounter or DPRK operational firing/deployment.
10. Any emerging crisis crossing the configured three-mention/two-independent-source gate.
