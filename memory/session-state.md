# Session State

> Last updated: 2026-07-22T06:21:43Z
> Session: DoomsdayWatch 06Z / 09:00 Amman morning deep-scan refresh

## Current Task
- **What:** Deep rolling past-24-hour review of all configured trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded additive coupled score rises from **74.64% to 74.70%**.
- **Numeric mover:** `yemen_red_sea` **49% → 52% (+3)** and **critical → imminent** after Reuters updated its independently observed tanker-reversal count to three; the Houthi six-vessel claim and formal/enforced closure remain unverified.
- **Trackers/signals:** All **18 canonical IDs** reviewed; no tracker added. The pipeline expired `iran_conventional:oil_infrastructure_threat`, leaving **8 canonical signals** aligned across trackers, zones and timeline.
- **Repository:** Automated deploy commit `c3ebf449`; exact metadata/signal-alignment commit `5b01c894`; both pushed and HEAD equals `origin/main`.
- **Deployment:** GitHub Pages run `29896409506` succeeded for exact commit `5b01c894`. Live root/state returned HTTP 200 and exposed all three command-deck markers, `morning_deep_scan_06z`, 18 trackers/news items, global 75/imminent and `yemen_red_sea` 52/imminent.
- **Tests:** JSON, canonical-ID, signal-alignment, local/live marker and Pages checks passed. **31 non-smoke tests passed**; the stock smoke fixture timed out after its fixed 60-second pipeline limit, producing 11 setup errors on two attempts. Deploy/pipeline itself completed successfully.

## Evidence Decisions
- **Yemen/Red Sea:** Bing exposed Reuters' updated description: three Saudi-crude tankers made U-turns. A Washington Post item indexed at 05:55Z independently reports multiple ships turning around, but its direct page was inaccessible. This crosses the predeclared third-diversion watch trigger, so risk rises to **52% / imminent** without claiming six ships or activating a non-existent signal.
- **Iran conventional:** Reuters reported Rubio remains willing to negotiate but doubts Tehran's seriousness; 11th-night strike reporting continued. `diplomacy_active` and `diplomacy_refused` remain, while `oil_infrastructure_threat` expired under temporal decay. The realized-war lane stays **100%**.
- **Iran nuclear:** Pickaxe Mountain remains an Israeli-intelligence claim without IAEA/independent technical confirmation. The post-cutoff nuclear query mainly surfaced the separate U.S.-Saudi civil-nuclear agreement. Holds **47% raw / 54% coupled**.
- **Russia-NATO:** Direct NATO inspection still showed no Article 4/5 consultation or allied combat response to the *Gas Lisbon* strike outside Romanian territorial waters. Holds **42% raw / 52% coupled**.
- **Mali:** SOFX's 03:15Z convoy item is follow-on to the already-scored 18 July Anefis-Gao ambush, not a second post-cutoff attack. Holds **36%**.
- **Auto-detection:** No candidate qualified across 22 reviewed lanes; fresh items were configured-conflict spillover, border-control reporting, analysis, or isolated reports below the three-mention/two-source gate.

## Sources and Sanity
- All **22 Tavily searches** and **8 extraction targets** failed HTTP 432. Fallback used **18 core + 44 supplemental** Google News RSS groups, ten Bing exact checks, direct Guardian/NATO browser inspection, official feeds, terminal HTTP, OilPriceAPI and Gamma.
- IAEA/OPEC returned 403; IAEA browser access hit Cloudflare; configured OCHA/UN Sudan paths returned 404; Washington Post direct access failed by HTTP/2 and timeout; Reuters direct access hit DataDome. Exact limitations are restored in live `_meta`.
- Final energy: Brent **$92.10 (+4.31%/24h)**; WTI **$85.27 (+4.26%)**; gold **$4,129.10 (+1.64%)**.
- Exact market sanity: U.S.-Iran invasion **28.5% (+1.0pp)**, Iran device **5.6%**, Iran test **5.5%**, Iran NPT withdrawal **18.25%**, NATO Article 5 **7.5%**, China invasion **4.05% (-0.1pp)**, Ukraine peace deal **21.5%**, Israel-Lebanon normalization **14.5% (-0.5pp)**. Markets were not score inputs.

## Next-Watch Triggers
- **Yemen/Red Sea:** attributable attack/interdiction, a fourth independently verified reversal, U.S./Saudi military action, Yanbu loading disruption, insurance/AIS discontinuity or formal closure.
- **Iran/Hormuz:** independently verified `hormuz_mining`, `hormuz_zero_traffic` or `hormuz_closed`; another crew-casualty vessel attack, wider Gulf infrastructure attacks or an implemented pause.
- **Pickaxe/Natanz/Darkhovin:** independent satellite/IAEA confirmation of transferred centrifuges or fissile material, current underground operations, new enrichment result, inspector exclusion, verified strike execution/damage or a detonation.
- **Romania/Black Sea:** firm attribution, strike inside Romanian territorial waters, NATO-flagged/state vessel involvement, Romanian military response, Article 4/5 consultation or repeat attacks near NATO territory.
- **Israel-Lebanon:** implementation beyond the pilot, pilot reversal, wider withdrawal, weapons-control mechanism or Israeli re-entry.
- **South China Sea:** Philippine-U.S. consultation, operational alliance step, deployment, firearm use, death or vessel seizure/collision.
- **Somalia/Gulf of Aden:** MT Asana rescue/interdiction outcome, crew harm, ransom demand, another hijack or sustained naval response.
