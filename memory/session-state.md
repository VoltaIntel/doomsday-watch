# Session State

> Last updated: 2026-07-21T18:15:02Z
> Session: DoomsdayWatch 18Z / 21:00 Amman morning deep scan

## Current Task
- **What:** Deep rolling past-24-hour review of all configured trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed, tested and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded additive coupled score remains **74.64%**.
- **Numeric movers:** None. The main evidence change is President Trump's explicit statement that the U.S. will hit the Pickaxe Mountain area near Natanz “pretty soon” and “very heavily”; `iran_conventional` is already capped at **100%**, while `iran_nuclear` holds **47% raw / 54% coupled** because no current material, enrichment or detonation threshold was independently established.
- **Trackers/signals:** All **18 canonical IDs** reviewed; no tracker added. `south_sudan_abyei:military_buildup` cleared under its configured 72-hour decay after no fresh qualifying evidence. Trackers, zones and timeline align at **10 canonical signals**.
- **Repository:** Automated deploy commit `c8f84262`; exact source-metadata/alignment commit `2a6a9a0c` is pushed and equals `origin/main`; tree clean before memory logging.
- **Deployment:** GitHub Pages run `29856251781` succeeded. Live root/state return HTTP 200, expose all three command-deck markers, 18 trackers/news items, 10 aligned signals, exact 18Z fallback metadata and state timestamp `2026-07-21T18:10:10Z`.
- **Tests:** **42/42 passed in 60.04s**.

## Evidence Decisions
- **Iran/Hormuz/nuclear:** AP and ABC Australia/Reuters directly confirm Trump's Pickaxe target warning and his refusal of near-term talks absent a meaningful meeting. The announcement sharpens the nuclear-site crisis but is not evidence that Iran moved material or reached a new weapons-development/test threshold. Gulf strikes continue; Iran war remains capped at 100%.
- **Yemen/Red Sea:** AP says Houthi-run SABA claimed six reroutes and Trump threatened a conditional response. Only two Saudi-crude tanker reversals remain independently observed; no attributable enforcement attack or U.S./Saudi counterstrike was verified. `yemen_red_sea` holds **49% / critical**.
- **Israel-Lebanon:** Trump said Israel is redeploying and pledged U.S. support. The Lebanese army reported nearby fire; the IDF described warning shots outside the pilot area. Zawtar implementation persists but is fragile; `israel_lebanon` holds **76% raw / 86% coupled**.
- **Israel-Palestine:** AP's Gaza barrier evidence reinforces territorial entrenchment; later 12-death reporting includes the already-reviewed family-of-six strike. The near-ceiling lane holds **88%** without inflation.
- **Auto-detection:** No candidate qualified. Haiti's multiple publications trace to one UN Security Council warning chain; other candidates remained tracked spillover, stale, analytic, disaster-related or below the three-mention/two-independent-source operational gate.

## Sources and Sanity
- All **22 Tavily searches** and **4 extraction targets** failed HTTP 432. Fallback completed through **18 core + 42 targeted/exact/emerging** Google News RSS groups, Bing News RSS, browser-direct AP/PBS/ABC Australia/NATO, official UN/NATO/EIA feeds, terminal HTTP, OilPriceAPI and Gamma.
- IAEA/OPEC returned 403; configured OCHA/UN Sudan paths returned 404; UN News RSS returned HTTP 200 but parsed zero items; Jewish Insider direct access was Cloudflare-blocked.
- Final energy: Brent **$91.17 (+2.39%/24h)**; WTI **$84.42 (+2.89%)**; natural gas **$2.85 (+0.71%)**; gold **$4,067.46 (+1.68%)**.
- Exact sanity: U.S.-Iran invasion **27.5% (+1.0pp)**, Iran device **5.45% (-0.1pp)**, Iran test **4.5%**, NPT withdrawal **14.95% (+0.3pp)**, NATO Article 5 **7.5% (-0.5pp)**, China invasion **4.15%**, China-Taiwan clash **7.05%**, Ukraine peace deal **21.5%**, Israel-Lebanon normalization **16.5% (+1.0pp)**. Markets were not score inputs.

## Next-Watch Triggers
- Pickaxe/Natanz: strike execution, verified damage, Iranian material dispersal, current enrichment operations, denied inspector access or nuclear retaliation doctrine.
- Iran/Hormuz: independently verified mine-laying, literally zero passage, formal closure, another crew-casualty vessel attack, wider Gulf infrastructure attacks or an implemented pause.
- Yemen/Red Sea: independently verified third-or-larger diversion wave, attributable attack/interdiction, U.S./Saudi military action, Yanbu loading disruption or insurance/AIS discontinuity.
- Israel-Lebanon: implementation beyond Zawtar, warning-shot escalation, pilot reversal, wider verified withdrawal, Hezbollah/LAF weapons-control mechanism or Israeli re-entry.
- South China Sea: Philippine-U.S. consultation, operational alliance step, deployment, firearm use, death or vessel seizure/collision.
- Somalia/Gulf of Aden: rescue/interdiction outcome, crew harm, ransom demand, another hijack or sustained naval response.
