# Session State

> Last updated: 2026-07-20T15:46:33Z
> Session: DoomsdayWatch 15Z morning deep scan

## Active Projects
- DoomsdayWatch / nuke-watch — 15Z deep scan completed, deployed, pushed and live-verified.
- Umbraxis Group — preserved paused state; this cron did not touch its worktree or processes.

## Current Task
- **What:** Deepest past-24-hour review of all 17 canonical trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete.
- **Result:** Global remains **75% / imminent**; unrounded weighted coupled score is **74.52%**.
- **Movers:** `israel_lebanon` **84→80 raw / 94→90 coupled**; `yemen_red_sea` **38→46**.
- **Signals:** No activation or clearance. The **10** pre-existing canonical active signals remain aligned across trackers, zones and timeline; pipeline mechanically advanced their `last_confirmed` timestamps.
- **Repository:** Final deployed data commit is `a120189a`; HEAD/upstream/remote were aligned before the mandatory memory-only summary commit that follows.
- **Deployment:** GitHub Pages run `29756549526` succeeded for `a120189a`.
- **Verification:** Local and live roots contain `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`. Live state exposes `morning_deep_scan_followup_15z`, **75% / imminent**, Israel-Lebanon **90**, Yemen-Red Sea **46**, all 17 populated news headlines and 10 active canonical signals.
- **Tests:** **31 core tests passed**. The stock 11-test pipeline-smoke fixture exceeded its hard-coded 60-second setup timeout, producing 11 setup errors; the identical **11 assertions passed in 76.37s** in an isolated copy with only that fixture timeout extended to 180 seconds.

## DoomsdayWatch Watch State
- **Israel-Lebanon:** The U.S. State Department says Trilateral Framework pilot operations began in Froun, Srifa and Zawtar El Gharbiyeh after the Rome talks. Axios/LBCI reports Israeli forces will leave the pilot areas Tuesday. This concrete but narrow implementation step justifies the four-point raw reduction; Iran-war coupling keeps the final lane at 90%.
- **Yemen-Red Sea:** Reuters/Al-Monitor confirms a Houthi declaration of an immediate maritime embargo against Saudi Arabia. No vessel attack, interdiction, Saudi military response or shipping diversion was independently verified at cutoff. Risk rises to 46% without promoting any configured signal.
- **Iran:** The UN called for renewed diplomatic effort and mediated exchanges continue, but no agreed pause exists. Conventional war stays capped at 100%; the nuclear lane stays 47% raw / 54% coupled because no fresh enrichment, inspection-access or test threshold was verified.
- **Russia/Ukraine/NATO:** UN condemned the overnight Kyiv attack. Ukraine invoked NATO's emergency-response assistance mechanism; this is civil/emergency support, not Article 5 or allied combat entry. Russia-Ukraine stays 99%; Russia-NATO stays 42% raw / 52% coupled.
- **South China Sea:** AP directly confirmed competing Philippine and Chinese accounts of the Second Thomas Shoal baton altercation. No firearms or death were reported; the existing lane stays 18%.
- **Auto-detection:** No new zone qualified. Somalia's several official counterterrorism claims did not form one independently corroborated multi-source escalation event; Thailand-Cambodia remained non-kinetic; Haiti produced no fresh military threshold.

## Sources and Sanity Checks
- All **22 Tavily searches** and **5 extracts** failed HTTP 432. Fallback completed through **18 core + 38 supplemental + 7 exact-event** Google News RSS queries, direct AP/LBCI/Al-Monitor/NATO/UN pages, terminal HTTP, exact-slug Gamma and OilPriceAPI.
- Reuters direct HTTP returned 401; the Houthi item was verified through Reuters syndication metadata and the Reuters-branded Al-Monitor page. IAEA exposed no usable same-day item, limiting nuclear absence claims to the reachable archive and RSS review.
- Final energy after deploy: Brent **$88.01 (-0.08%/24h)**; WTI **$81.53 (-0.02%)**. No commodity discontinuity accompanied the Houthi declaration by cutoff.
- Exact-slug market sanity: U.S.-Iran invasion **27.5%** (**+5pp from 12Z**), Iran nuclear test **4.5%**, NATO Article 5 **7.5%**, China-Taiwan clash **5.45%**. Long-horizon/low-liquidity markets were not probability inputs.

## Next-Watch Triggers
- Yemen/Red Sea: verified vessel attack or interdiction, Saudi response, shipping diversion, insurance shock, or Bab el-Mandeb disruption.
- Israel-Lebanon: Tuesday withdrawal completed/expanded/reversed; renewed strikes outside the pilot framework; collapse of the Washington/Rome mechanism.
- Iran/Hormuz: verified mining, zero traffic, closure, widened Gulf infrastructure attacks, or an implemented pause.
- Iran nuclear: verified 90%-level enrichment, Fordow activity, denied inspection access, IAEA emergency action, or test evidence.
- Russia/NATO/Ukraine: Article 5 movement, allied combat entry, official nuclear-threshold language, or a materially larger ballistic/Black Sea strike cluster.
- South China Sea: firearms, death, vessel seizure/collision, sustained force concentration, alliance consultation, or a bilateral deconfliction outcome.
- Pipeline: keep negated signal-key phrases out of news prose and audit tracker/timeline alignment after every deploy.
