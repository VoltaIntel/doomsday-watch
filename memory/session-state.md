# Session State

> Last updated: 2026-07-22T00:14:13Z
> Session: DoomsdayWatch 00Z / 03:00 Amman morning deep scan

## Current Task
- **What:** Deep rolling past-24-hour review of all configured trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed, tested and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded coupled score remains **74.64%**.
- **Numeric movers:** None. New evidence did not cross a distinct modeled endpoint.
- **Trackers/signals:** All **18 canonical IDs** reviewed; no tracker added and no signal changed. Trackers, zones and timeline align at **9 canonical signals**: `iran_conventional:{diplomacy_active,diplomacy_refused,oil_infrastructure_threat}`, `israel_lebanon:{ceasefire_violation,diplomacy_active}`, `israel_palestine:{ceasefire_violation,holy_site_tension}`, `mali_sahel:military_buildup`, and `south_china_sea:external_backing`.
- **Repository:** Automated deploy commit `ca7b3547`; exact metadata commit `c5c3d126`; both pushed before session logging. The session-log commit follows this state update.
- **Deployment:** GitHub Pages run `29879648523` succeeded for the exact metadata state. Live root/state returned HTTP 200 and exposed all three command-deck markers, `morning_deep_scan_00z`, 18 trackers and exact source caveats.
- **Tests:** Final application state passed **42/42 tests** in 44.54 seconds. JSON/canonical/timeline and local/live marker checks passed.

## Evidence Decisions
- **Russia-NATO / Black Sea:** Direct Euronews/AP inspection confirms the propane tanker *Gas Lisbon* was struck about 20 nautical miles off Romania, injuring three and forcing a full evacuation. Romania's president said Russia was the most likely perpetrator, but the vessel was outside Romanian territorial waters and the investigation remains open. No NATO treaty or allied-combat step followed; Russia-NATO holds **42% raw / 52% coupled**.
- **Iran nuclear:** WSJ reports Israeli intelligence believes centrifuges moved into Pickaxe Mountain. No IAEA or independent source verified fissile-material transfer, a new enrichment level, access change, reprocessing or detonation. Iran nuclear holds **47% raw / 54% coupled** and no signal activated.
- **Sudan:** Sudan Tribune reports army reinforcements into the Sahara to cut RSF supply lines; direct access was Cloudflare-blocked and no independent source matched the operational detail. DW/Christian Science Monitor corroborate pressure around El Obeid, not the fresh reinforcement claim. Sudan holds **90%** without a new signal.
- **Yemen/Red Sea:** Reuters, Guardian and CBC reconfirm only two Saudi-crude tanker reversals after the Houthi warning. No attributable enforcement attack, formal Bab el-Mandeb closure or U.S./Saudi counterstrike was verified; risk holds **49% / critical**.
- **Israel-Lebanon:** Post-cutoff Washington Post/CBC coverage confirms Trump pledged support during President Aoun's White House visit. The southern pilot remains in force without a wider withdrawal or weapons-control mechanism; risk holds **76% raw / 86% coupled**.
- **Russia-Ukraine:** The Gas Lisbon strike, continuing barrages and commander-in-chief replacement after protests are material war developments but not a separate nuclear or allied-entry endpoint; the realized-war lane holds **99%**.
- **Auto-detection:** No candidate qualified across 22 reviewed lanes. Syria's 65-attack/50-death figure traced to one cumulative SOHR report; the Bangladesh custody of three Myanmar security personnel had multiple local publications but no clash; Thailand-Cambodia reporting showed a closed border and political tension without a fresh kinetic event.

## Sources and Sanity
- All **22 Tavily searches** and **4 extraction targets** failed HTTP 432. Fallback completed through **18 core + 44 targeted/exact/emerging** Google News RSS groups, 12 Google/Bing exact checks, direct UN Press/NATO/Euronews/Al Jazeera/Jerusalem Post/ABC inspection, official feeds, terminal HTTP, OilPriceAPI and Gamma.
- IAEA/OPEC probes returned 403; configured OCHA/UN Sudan paths returned 404; UN News RSS returned HTTP 200 but the local parser extracted no items; Sudan Tribune direct was Cloudflare-blocked; Google browser exact searches triggered CAPTCHA while RSS remained available.
- Final energy: Brent **$91.64 (+3.09%/24h)**; WTI **$84.68 (+2.74%)**.
- Exact sanity: U.S.-Iran invasion **28.5% (+1.0pp)**, Iran device **5.55% (+0.15pp)**, Iran test **5.5% (+1.0pp)**, NPT withdrawal **15.95% (+1.0pp)**, NATO Article 5 **7.5%**, China invasion **4.25%**, China-Taiwan clash **6.9% (+0.05pp)**, Ukraine peace deal **21.5%**, Israel-Lebanon normalization **14.5% (-0.5pp)**. Markets were not score inputs.

## Next-Watch Triggers
- **Romania/Black Sea:** firm attribution, a strike inside Romanian territorial waters, NATO-flagged/state vessel involvement, Romanian military response, Article 4/5 consultation or repeat attacks approaching NATO territory.
- **Pickaxe/Natanz/Darkhovin:** independent satellite/IAEA confirmation of transferred centrifuges or fissile material, current underground operations, a new enrichment result, inspector exclusion, verified strike execution/damage or nuclear retaliation doctrine.
- **Iran/Hormuz:** independently verified mine-laying, literal zero passage, formal closure, another crew-casualty vessel attack, wider Gulf infrastructure attacks or an implemented pause.
- **Yemen/Red Sea:** independently verified third-or-larger diversion wave, attributable attack/interdiction, U.S./Saudi action, Yanbu loading disruption or insurance/AIS discontinuity.
- **Sudan:** independent confirmation of the Sahara reinforcement, a resulting battle/supply-line cutoff, chemical-use verification or Red Sea spillover.
- **Israel-Lebanon:** implementation beyond the pilot, pilot reversal, wider verified withdrawal, weapons-control mechanism or Israeli re-entry.
- **South China Sea:** Philippine-U.S. consultation, operational alliance step, deployment, firearm use, death or vessel seizure/collision.
- **Somalia/Gulf of Aden:** Asana rescue/interdiction outcome, crew harm, ransom demand, another hijack or sustained naval response.
