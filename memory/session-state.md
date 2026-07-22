# Session State

> Last updated: 2026-07-22T09:27:04Z
> Session: DoomsdayWatch 09Z / 12:00 Amman morning deep-scan refresh

## Current Task
- **What:** Deep rolling past-24-hour review of all configured trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded additive coupled score remains **74.70%**.
- **Numeric movers:** None from 06Z.
- **Evidence mover:** Direct AP reporting, updated 08:35Z, says Iran attacked a tanker in the Strait on 21 July and forced the crew to abandon ship; gCaptain separately reported a second tanker abandonment within 24 hours. `iran_conventional:oil_infrastructure_threat` was renewed, while the realized-war lane remains capped at **100%**.
- **Regional widening:** AP reports Jordan intercepted four Iranian missiles and two fell in uninhabited areas; AP also reports Iranian attacks on Bahrain and Kuwait. This remains spillover inside the configured Iran-war lane, not a new auto-detected tracker.
- **Signals:** Deploy temporal decay cleared `iran_conventional:diplomacy_refused`, `israel_lebanon:ceasefire_violation`, and `south_china_sea:external_backing`. Final trackers/zones/timeline align at **6 active canonical signals**.
- **Repository:** Automated deploy commit `a4b6a5b5`; exact metadata/signal-alignment commit `978d6ae4`; both pushed and HEAD equals `origin/main`.
- **Deployment:** GitHub Pages run `29907888751` succeeded for exact commit `978d6ae4`. Live root/state returned HTTP 200 and exposed all three command-deck markers, `morning_deep_scan_09z`, 18 trackers/news items, global 75/imminent and renewed `oil_infrastructure_threat`.
- **Tests:** JSON, canonical-ID, signal-alignment, local/live marker and Pages checks passed. **31 non-smoke tests passed**.

## Evidence Decisions
- **Iran conventional/Hormuz:** AP direct inspection confirmed the fresh tanker attack/abandonment and the Jordan/Bahrain/Kuwait salvos. The `oil_infrastructure_threat` signal was renewed, but no `hormuz_mining`, `hormuz_zero_traffic`, `hormuz_closed`, total closure or mine-laying evidence appeared.
- **Yemen/Red Sea:** A Washington Post item surfaced after 06Z, but Bing dates its underlying publication to 21 July 16:54Z. It describes the already-scored reversal wave, not a fourth ship or enforcement attack. `yemen_red_sea` holds **52% / imminent**.
- **Iran nuclear:** Fresh results were a separate U.S.-Saudi civil-nuclear agreement and Pickaxe explainers, not new technical evidence. Holds **47% raw / 54% coupled**.
- **Russia-NATO:** Direct NATO inspection still showed no Article 4/5 consultation or allied combat response to the *Gas Lisbon* strike outside Romanian territorial waters. Holds **42% raw / 52% coupled**.
- **South China Sea:** A single Philippine outlet reported rare high-level talks over the Ayungin clash; the direct page was country-blocked and no second-source implementation or treaty consultation surfaced. Holds **21%**; expired `external_backing` cleared.
- **Auto-detection:** No candidate qualified across 22 reviewed lanes. Jordan was treated as configured Iran-war spillover; Nigeria, Egypt/Libya, Syria and Sahel hits were domestic operations, institutional developments, travel advice, analysis or below the three-mention/two-source gate.

## Sources and Sanity
- All **22 Tavily searches** and **5 extraction targets** failed HTTP 432. Fallback used **18 core + 44 supplemental** Google News RSS groups, 13 Bing exact checks, direct AP/NATO browser inspection, official feeds, terminal HTTP, OilPriceAPI and Gamma.
- IAEA/OPEC returned 403; configured OCHA/UN Sudan paths returned 404; Google consent and Politiko country blocking limited direct access; Washington Post remained index-level. AP and NATO were directly accessible. Exact limitations are live in `_meta`.
- Final energy: Brent **$94.49 (+6.30%/24h)**; WTI **$87.60 (+6.78%)**; gold **$4,120.21 (+1.19%)**.
- Exact market sanity: U.S.-Iran invasion **29.5% (+1.0pp)**, Iran device **5.6%**, Iran test **5.5%**, Iran NPT withdrawal **18.3% (+0.05pp)**, NATO Article 5 **7.5%**, China invasion **4.05%**, China-Taiwan clash **6.8% (-0.05pp)**, DPRK invasion **2.05% (+0.05pp)**, Ukraine peace deal **21.5%**, Israel-Lebanon normalization **15.5% (+1.0pp)**. Markets were not score inputs.

## Next-Watch Triggers
- **Iran/Hormuz:** independently verified `hormuz_mining`, `hormuz_zero_traffic` or `hormuz_closed`; crew casualties or loss of another tanker; widening Gulf infrastructure attacks; implemented pause.
- **Jordan/Gulf:** additional Iranian salvos, casualties/infrastructure damage, Jordanian or Gulf counterstrikes, or new U.S. force entry.
- **Yemen/Red Sea:** attributable attack/interdiction, a fourth independently verified reversal, Yanbu loading disruption, insurance/AIS discontinuity or formal closure.
- **Pickaxe/Natanz/Darkhovin:** independent satellite/IAEA confirmation of current operations or material movement, new enrichment result, inspector exclusion, verified strike damage or `nuclear_test`.
- **Romania/Black Sea:** firm attribution, strike inside Romanian territorial waters, NATO-flagged/state-vessel involvement, Romanian response or Article 4/5 consultation.
- **South China Sea:** official outcome of high-level talks, Philippine-U.S. consultation, operational alliance step, firearm use, death or vessel seizure/collision.
- **Somalia/Gulf of Aden:** MT Asana rescue/interdiction outcome, crew harm, ransom demand, another hijack or sustained naval response.
