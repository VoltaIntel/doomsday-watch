# Session State

> Last updated: 2026-07-21T12:20:41Z
> Session: DoomsdayWatch 12Z / 15:00 Amman morning deep scan

## Current Task
- **What:** Deep rolling past-24-hour review of all configured trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, corrected, deployed, pushed and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded additive coupled score falls **75.14% → 74.58%**.
- **Movers:** `israel_lebanon` fell **80% → 76% raw** and **90% → 86% coupled** after Reuters/BBC confirmed Israeli withdrawal from Zawtar and Lebanese army entry.
- **Trackers/signals:** All **18 canonical IDs** reviewed; no tracker added/removed and no canonical signal activated/cleared. Trackers, zones and timeline align at **11** active signals; three existing signals received fresh evidence.
- **Repository:** Final deploy commit `c35492cb`; exact source-metadata commit `6df2ad0f` is pushed and equals `origin/main`; tree clean before memory logging.
- **Deployment:** GitHub Pages run `29829609569` succeeded. Live root/state return HTTP 200, expose all three command-deck markers, 18 trackers/news items, 11 aligned signals, exact 12Z metadata and state timestamp `2026-07-21T12:16:31Z`.
- **Tests:** **31 focused core tests passed in 0.27s**.

## Evidence Decisions
- **Israel-Lebanon:** Reuters (11:11Z) and BBC confirm the Lebanese army entered Zawtar after Israeli forces withdrew. This satisfies the pilot’s first meaningful operational test. Israel still says it will retain the wider security zone and Hezbollah disarmament remains unresolved, supporting a bounded four-point reduction rather than a larger cut.
- **Iran/Hormuz:** Reuters reports Iranian forces targeted Bahrain and Kuwait while U.S. strikes hit southern Iran. CNBC confirms the IRGC claim against Amazon infrastructure in Bahrain but could not verify damage. Lloyd’s/Kpler show sharply reduced but nonzero Hormuz traffic. The realized-war lane stays capped at 100%.
- **Iran nuclear:** New Pickaxe Mountain headlines describe centrifuges moved last fall after the June 2025 war, not a new transfer. No current canonical threshold was activated.
- **Auto-detection:** No candidate qualified. Myanmar’s Sittwe/Rakhine offensive had two independent current publishers, below the three-mention gate. Bangladesh-Myanmar personnel crossings were non-kinetic. Western Niger is covered by `mali_sahel` and remains largely one state-media-origin chain.
- **QA correction:** The first deployment pass falsely activated `iran_nuclear:fordow_activation` from a negated narrative phrase. The phrase and signal were removed, deploy was rerun, and final local/live state and timeline contain only the 11 pre-existing real signals.

## Sources and Sanity
- All **22 Tavily searches** and both extraction targets failed HTTP 432. Fallback completed through **18 core + 42 targeted/exact/emerging** Google News RSS groups, direct CNBC/BBC/Jerusalem Post/NATO inspection, official UN/NATO sources, terminal HTTP, OilPriceAPI and Gamma exact-slug reads.
- Direct IAEA/OPEC stayed 403; EIA RSS timed out; configured OCHA/UN Sudan paths stayed 404; Reuters direct pages were DataDome-restricted.
- Final energy: Brent **$90.35 (+2.37%/24h)**; WTI **$83.52 (+2.40%)**; natural gas **$2.87 (-0.35%)**; gold **$4,065.00 (+1.27%)**.
- Exact sanity: U.S.-Iran invasion **26.5%**, Iran device **5.55%**, Iran test **4.5%**, NPT withdrawal **14.65%**, NATO Article 5 **8.0%**, China invasion **4.35%**, China-Taiwan clash **6.85%**, DPRK invasion **2.05%**, Ukraine peace deal **21.5%**, Israel-Lebanon normalization **15.5%**. Markets were not score inputs.

## Next-Watch Triggers
- Israel-Lebanon: implementation beyond Zawtar, verified wider withdrawal, Hezbollah/LAF weapons-control mechanism, pilot reversal, renewed strikes or Israeli re-entry.
- Iran/Hormuz: independently verified mine-laying, literally zero passage, legal closure, another crew-casualty vessel attack, widened Gulf infrastructure attacks or an implemented pause.
- Yemen/Red Sea: attributable post-declaration attack/interdiction, Saudi military action, broad rerouting, fresh AIS/Kpler enforcement evidence or a larger insurance discontinuity.
- Iran nuclear: verified weapons-grade enrichment, current underground enrichment operations, denied inspector access, watchdog emergency action or detonation evidence.
- South China Sea: Philippine-U.S. consultation, operational alliance step, new deployment, firearm use, death or vessel seizure/collision.
- Somalia/Gulf of Aden: rescue/interdiction outcome, crew harm, ransom demand, another hijack or sustained multinational naval response.
