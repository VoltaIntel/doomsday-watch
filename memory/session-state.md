# Session State

> Last updated: 2026-07-21T00:22:00Z
> Session: DoomsdayWatch 00Z / 03:00 Amman morning deep scan

## Current Task
- **What:** Deepest past-24-hour review of all 17 canonical trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded additive coupled score is **74.52%**.
- **Movers:** No numeric tracker moved.
- **Signals:** No canonical active-set change; all **10** active signals align across trackers, zones and timeline. A negation-triggered `iran_nuclear:iaea_emergency` pipeline false positive was caught, removed and absent from the final local/live state.
- **Repository:** Final exact-source-metadata commit `898acdea` is pushed and equals `origin/main`.
- **Deployment:** GitHub Pages run `29789767714` succeeded for `898acdea`; local and live roots expose all three required command-deck markers and live state timestamp `2026-07-21T00:11:03Z` / `last_updated` `2026-07-21T00:13:29Z`.
- **Tests:** **31 core tests passed**. The stock smoke fixture hit its hard-coded 60-second setup ceiling and reported 11 setup errors; an identical final-state temporary copy with only that ceiling extended passed all **11/11** smoke assertions in **89.05s**.

## Evidence Decisions
- **Iran/Hormuz:** Reuters/DW/Haaretz report another night of strikes; gCaptain and follow-on coverage confirm two Dynacom tanker attacks. Traffic remains near a standstill but not proven literally zero. Iran stays capped at **100%**; no confirmed naval mines or formal total closure.
- **Israel-Lebanon:** The U.S. called pilot operations begun, but direct inspection of The National showed Froun/Srifa already had no Israeli presence and the Lebanese army still awaited the Zawtar withdrawal, reportedly Tuesday. **80% raw / 90% coupled** holds.
- **Russia-Ukraine/NATO:** NATO confirmed Ukraine requested help through the Euro-Atlantic Disaster Response Coordination Centre. This is civilian emergency response, not Article 5 or allied combat entry. Russia-Ukraine holds **99%**.
- **Sudan:** Fresh sanctions reporting concerns alleged earlier chlorine use and does not establish same-day deployment or a distinct new offensive; **90%** holds.
- **Yemen-Red Sea:** Reuters/BBC confirmed the Houthi declaration; no attributable interdiction/attack, broad rerouting, insurance discontinuity or verified Saudi military response followed; **46%** holds.
- **Auto-detection:** No untracked crisis met the configured three-mention/two-source gate. The Gulf of Aden hijack and Myanmar Rakhine strike each had only one current publisher chain; the Haiti UN review exposed no discrete new military threshold.

## Sources and Sanity
- All **22 Tavily searches** and **10 Tavily extraction URLs** failed HTTP 432. Fallback completed through **18 core + 42 targeted + 9 exact-event** Google News RSS queries, browser/direct publisher inspection, official UN/NATO/EIA pages and feeds, terminal HTTP, OilPriceAPI and Gamma exact-slug reads.
- Direct IAEA/OPEC stayed 403; configured OCHA/UN Sudan paths stayed 404; UKMTO was Cloudflare-blocked; Google News did not render the direct Reuters target.
- Final energy: Brent **$88.89 (-2.21%/24h)**; WTI **$82.54 (-1.40%)**.
- Exact sanity: U.S.-Iran invasion **26.5%**, Iran device **5.55%**, Iran test **4.5%**, Iran NPT withdrawal **14.9%**, NATO Article 5 **6.5%**, China invasion **4.35%**, China-Taiwan clash **7.15%**, Ukraine peace deal **21.5%**. Markets were not score inputs.

## Next-Watch Triggers
- Iran/Hormuz: verified naval mines, literally zero passage, formal closure, widened Gulf infrastructure attacks, or an implemented pause.
- Israel-Lebanon: completed/expanded/reversed Zawtar withdrawal, renewed strikes outside the framework, or collapse of the joint mechanism.
- Yemen/Red Sea: attributable vessel interdiction/attack, Saudi military action, broad rerouting, insurance discontinuity or Bab el-Mandeb disruption.
- Iran nuclear: verified 90%-level enrichment, Fordow activity, inspection denial, watchdog emergency action or test evidence.
- Russia/NATO/Ukraine: collective-defence movement, allied combat entry, official nuclear-threshold language or a materially larger strike cluster.
- South China Sea/Taiwan: firearms, death, vessel seizure/collision, sustained force concentration, merchant rerouting, quarantine declaration or alliance consultation.
- Pipeline: keep configured signal-key phrases out of negated prose and audit tracker/timeline alignment after every deploy.
