# Session State

> Last updated: 2026-07-22T03:17:41Z
> Session: DoomsdayWatch 03Z / 06:00 Amman morning deep scan

## Current Task
- **What:** Deep rolling past-24-hour review of all configured trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed, tested and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded coupled score remains **74.64%**.
- **Numeric movers:** None. Post-cutoff evidence did not cross a distinct modeled endpoint.
- **Trackers/signals:** All **18 canonical IDs** reviewed; no tracker added and no signal changed. Trackers, zones and timeline align at **9 canonical signals**: `iran_conventional:{diplomacy_active,diplomacy_refused,oil_infrastructure_threat}`, `israel_lebanon:{ceasefire_violation,diplomacy_active}`, `israel_palestine:{ceasefire_violation,holy_site_tension}`, `mali_sahel:military_buildup`, and `south_china_sea:external_backing`.
- **Repository:** Automated deploy commit `e3c52651`; exact metadata commit `8279ea54`; both pushed.
- **Deployment:** GitHub Pages run `29887983123` succeeded for exact metadata commit `8279ea54`. Live root/state returned HTTP 200 and exposed all three command-deck markers, `morning_deep_scan_03z`, 18 trackers/news items and exact source caveats.
- **Tests:** Final application state passed **42/42 tests** in 59.04 seconds. JSON/canonical/timeline and local/live marker checks passed.

## Evidence Decisions
- **Yemen/Red Sea:** Direct Guardian inspection distinguishes two independently observed Saudi-crude tanker U-turns from the Houthi claim of six. The additional four are unverified; no enforcement attack, formal Bab el-Mandeb closure, or U.S./Saudi counterstrike was established. Risk holds **49% / critical**.
- **Pakistan-Afghanistan false recency:** Google News fresh-indexed a claim that Taliban forces killed 30 Pakistani soldiers. Resolving the article directly to News On AIR proved it was dated **6 March 2026**, not July; it was excluded. Risk holds **46%**.
- **North Korea:** Nikkei reports renewed Trump outreach may reopen talks, but no meeting, negotiation round, launch or detonation is confirmed. Risk holds **18%** and no signal maps to the item.
- **Russia-NATO / Black Sea:** No firmer attribution or allied response followed the *Gas Lisbon* strike outside Romanian territorial waters. NATO still shows no consultation, collective-defence activation or allied combat entry; Russia-NATO holds **42% raw / 52% coupled**.
- **Iran nuclear:** Trump repeated a threat against active Iranian nuclear sites; Pickaxe Mountain remains an Israeli-intelligence claim without IAEA/independent technical confirmation. Iran nuclear holds **47% raw / 54% coupled**.
- **Sudan:** The Sahara reinforcement report remains uncorroborated; wider sources corroborate pressure around El Obeid, not the fresh movement claim. Sudan holds **90%**.
- **Auto-detection:** No candidate qualified across 22 reviewed lanes. Fresh items were analysis, diplomacy, accidents, humanitarian reporting, polluted by configured conflicts, or below the configured three-mention/two-independent-source operational gate.

## Sources and Sanity
- All **22 Tavily searches** and **4 extraction targets** failed HTTP 432. Fallback completed through **18 core + 44 targeted/exact/emerging** Google News RSS groups, seven Bing exact checks, direct Guardian/NATO/News On AIR/Nikkei inspection, official feeds, terminal HTTP, OilPriceAPI and Gamma.
- IAEA/OPEC probes returned 403; configured OCHA/UN Sudan paths returned 404; UN News RSS returned HTTP 200 but the local parser extracted no items; Washington Post direct failed with an HTTP/2 protocol error; Google consent/redirect handling impeded some browser resolutions while RSS remained available.
- Final energy: Brent **$91.96 (+3.55%/24h)**; WTI **$85.23 (+3.57%)**; gold **$4,126.71 (+2.24%)**.
- Exact market sanity: U.S.-Iran invasion **27.5% (-1.0pp)**, Iran device **5.55%**, Iran test **5.5%**, Iran NPT withdrawal **18.25% (+2.3pp)**, NATO Article 5 **7.5%**, China invasion **4.15% (-0.1pp)**, China-Taiwan clash **6.85% (-0.05pp)**, Ukraine peace deal **21.5%**, Israel-Lebanon normalization **15.0% (+0.5pp)**. Markets were not score inputs.

## Next-Watch Triggers
- **Iran/Hormuz:** independently verified mine-laying, literal zero passage, formal closure, another crew-casualty vessel attack, wider Gulf infrastructure attacks or an implemented pause.
- **Yemen/Red Sea:** independent verification of a third-or-larger diversion wave, attributable attack/interdiction, U.S./Saudi action, Yanbu loading disruption or insurance/AIS discontinuity.
- **Pickaxe/Natanz/Darkhovin:** independent satellite/IAEA confirmation of transferred centrifuges or fissile material, current underground operations, a new enrichment result, inspector exclusion, verified strike execution/damage or nuclear retaliation doctrine.
- **Romania/Black Sea:** firm attribution, a strike inside Romanian territorial waters, NATO-flagged/state vessel involvement, Romanian military response, Article 4/5 consultation or repeat attacks approaching NATO territory.
- **DPRK:** confirmed negotiation round, new launch, nuclear test or material force deployment.
- **Sudan:** independent confirmation of the Sahara reinforcement, a resulting battle/supply-line cutoff, chemical-use verification or Red Sea spillover.
- **Israel-Lebanon:** implementation beyond the pilot, pilot reversal, wider verified withdrawal, weapons-control mechanism or Israeli re-entry.
- **South China Sea:** Philippine-U.S. consultation, operational alliance step, deployment, firearm use, death or vessel seizure/collision.
- **Somalia/Gulf of Aden:** Asana rescue/interdiction outcome, crew harm, ransom demand, another hijack or sustained naval response.
