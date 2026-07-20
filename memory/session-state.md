# Session State

> Last updated: 2026-07-20T06:32:02Z
> Session: DoomsdayWatch 06Z morning deep scan

## Active Projects
- DoomsdayWatch / nuke-watch — scheduled 06Z deepest-scan refresh completed, committed, pushed and live-verified.
- Umbraxis Group — preserved paused state from the prior session; this cron did not touch its worktree or processes.

## Current Task
- **What:** Deepest past-24-hour nuclear-escalation scan across all 16 canonical trackers, required sectors and emerging crises.
- **Status:** Complete.
- **Result:** Global remains **75% / imminent**, raw weighted coupled **74.560%**; no tracker probability changed.
- **Signals:** No real activation or clearance; the **9** pre-existing canonical signals remain aligned across trackers, zones and timeline.
- **Repository:** Final deployed data commit is `8d7a4bfc`. Pipeline commits were `a97baf2d` and corrected `a10d70f0`; the mandatory memory-only summary commit follows `8d7a4bfc` and does not alter dashboard data.
- **Verification:** Local and live roots contain all three command-deck markers. Live state exposes `morning_deep_scan_06z`, exact fallback metadata and **75% / imminent**. JSON/canonical/timeline checks pass. **31 core tests passed**; the 11 pipeline-smoke checks hit their shared 60-second fixture timeout in the normal suite but all **11 assertions passed in 66.07s** in an isolated copy with only the fixture timeout extended.
- **Deployment:** GitHub Pages run `29721882977` succeeded for deployed data commit `8d7a4bfc`; live publication is current.

## DoomsdayWatch Watch State
- Iran war: AP confirms a ninth consecutive U.S. strike night, 17 U.S. military deaths since the war began and largely stalled Hormuz traffic. Iran is capped at 100%; traffic remains sparse but nonzero, and tanker-hit/mining claims remain unverified.
- China-Taiwan: Reuters reports Taiwan counted 55 Chinese government-vessel sightings in June versus 30 in May. This is credible grey-zone coercion but retrospective coast-guard/research-vessel data, not a fresh PLA blockade or force concentration; China holds at 24% raw / 28% coupled.
- Israel-Lebanon: reported destruction of Hezbollah underground infrastructure reinforces the existing truce-breach risk while Aoun-Rubio/Trump diplomacy remains active; 84% raw / 94% coupled.
- Israel-Palestine: i24NEWS adds further corroboration of two Deir Jarir deaths; existing indicators are reinforced and the lane stays 88% without inflation.
- Sudan: a new CNN investigation documents pervasive drone threat but no distinct post-cutoff offensive; the realised-war lane remains 90%.
- Auto-detection: no new zone qualified. Syria results are Iran-war spillover; Somalia claims remain under-corroborated; Thailand-Cambodia and South China Sea produced no fresh qualifying kinetic cluster.
- False-recency/source-quality exclusions: 5 July DPRK warship event, March Pakistan-Afghanistan clash headlines, 13 July Yemen-airport cycle, and uncorroborated India border-fire claims.
- Source path: 22 Tavily searches and 5 Tavily extracts failed HTTP 432. Fallback used 18 core + 40 targeted/exact/emerging Google News RSS lanes, direct AP/NATO/IAEA/Reuters-FMT/Taiwan MND inspection, UN/NATO/EIA feeds, terminal HTTP, OilPriceAPI and exact-slug Gamma. IAEA/OPEC remained 403; OCHA/UN Sudan paths remained 404; CNN body access was unavailable.
- Energy: Brent **$90.84 (+2.80%/24h)**; WTI **$84.01 (+1.84%)**. Exact-slug sanity: U.S.-Iran invasion **30.5%**, Ukraine peace-deal Yes **19.5%** (risk inverse 80.5%), China-Taiwan clash **5.8%**; not probability inputs.
- Pipeline guard: the first deploy keyword-matched three negated/ambiguous phrases into false canonical signals (`iran_nuclear:iaea_emergency`, `india:diplomacy_active`, `israel_palestine:diplomacy_active`). All three were removed atomically, prose was hardened, a second deploy produced no additions, and final tracker/timeline alignment is back to 9.

## Next-Watch Triggers
- Iran nuclear: verified `enrichment_90`, `fordow_activation`, `iaea_access_denied`, `iaea_emergency` or `nuclear_test` evidence.
- Iran war/Hormuz: independently verified `hormuz_mining`, `hormuz_zero_traffic` or `hormuz_closed`; a new ceasefire or widened Gulf infrastructure campaign.
- China-Taiwan: a current PLA or coast-guard concentration, merchant rerouting, quarantine/blockade declaration or live interdiction—not retrospective monthly totals.
- Russia/NATO and Ukraine: official nuclear-threshold language, Article 5 movement, allied combat entry or another materially larger ballistic/Black Sea strike cluster.
- Israel-Lebanon/Gaza: collapse of the Washington framework, a distinct mass-casualty strike cluster or broader holy-site mobilisation.
- Emerging: independent corroboration of Somalia's operations/tolls; fresh kinetic Thailand-Cambodia evidence; an Iraq/Syria cluster distinct from the Iran-war lane.
- Pipeline: avoid signal-keyword prose in negated findings; audit tracker/timeline counts after every deploy.

## Preserved Umbraxis Pause State
- Prior Umbraxis state remains in today's vault entry; no Umbraxis action occurred in this cron.
