# Session State

> Last updated: 2026-07-22T18:46:00Z
> Session: DoomsdayWatch 18Z / 21:00 Amman morning deep-scan refresh

## Current Task
- **What:** Deep rolling past-24-hour review of all 18 canonical trackers, required sectors, allied posture, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded additive coupled score rose **74.74% → 75.02%**.
- **Numeric mover:** `israel_lebanon` **76% → 78% raw / 86% → 88% coupled** after fresh NNA/Anadolu reporting of artillery, a drone strike, ground incursions and overnight explosions during the pilot withdrawal. Reuters-confirmed withdrawal and 4 August talks capped the move at +2.
- **Signals:** Activated canonical `israel_lebanon:ceasefire_violation`; cleared `iran_conventional:diplomacy_active`; trackers, zones and timeline align at **5 canonical signals**.
- **Auto-detection:** No new tracker qualified across 23 reviewed emerging lanes; the reported U.S.-Saudi civil-nuclear deal remains a watch item, not an operational crisis lane.
- **Repository:** Deploy commit `06166e01`; exact metadata commit `939b23cf`; both pushed to `origin/main`.
- **Deployment:** GitHub Pages run `29947893615` succeeded for exact commit `939b23cf`. Live root/state returned HTTP 200 and expose all command-deck markers, `morning_deep_scan_18z`, **75% / imminent**, raw **75.02**, Israel-Lebanon **78% raw / 88% coupled** and the five-signal set.
- **Tests:** JSON, canonical-ID, signal-alignment and local/live checks passed; **31/31 non-smoke tests passed**. The stock full/smoke path timed out after 600 seconds after two tests, while the real deploy/pipeline itself completed successfully.

## Evidence Decisions
- **Israel-Lebanon:** Current state reporting from Lebanon's NNA, carried by Anadolu, described artillery, a drone strike, ground incursions and explosions on 22 July. This supports `ceasefire_violation`; the implemented first withdrawal and scheduled talks keep the probability move conservative.
- **Iran/Hormuz:** The U.S. bridge/power-plant threat and Tasnim-cited Iranian threat against regional energy facilities refresh `oil_infrastructure_threat`. No implemented pause or active negotiating round survived, so `diplomacy_active` was cleared; the war lane remains capped at 100%.
- **Yemen/Red Sea:** Late Reuters and Washington Post reporting corroborated the already-scored seven route reversals but supplied no attributable enforcement attack, Yanbu halt or formal closure; the lane holds 57%.
- **False recency/unconfirmed:** A fresh-indexed South China Sea sailor-injury story described the already-scored Ayungin encounter; Pickaxe items remained explainers/prior intelligence; the North Darfur 21-death claim remained one late source chain.

## Sources and Sanity
- All **22 Tavily searches** and **7 extracts** failed HTTP 432; browser navigation failed code 101. Fallback used 18 core + 44 targeted Google News RSS groups, nine Bing checks, direct terminal/Jina inspection, official UN/NATO/EIA feeds, OilPriceAPI and exact Gamma reads.
- IAEA/OPEC returned 403; configured OCHA/UN Sudan paths returned 404. Reuters Red Sea body access returned 403, so its headline was corroborative only. Exact caveats were restored to live `_meta` after deploy sanitization.
- Final energy: Brent **$94.20 (+3.63%/24h)**; WTI **$86.78 (+2.77%)**; natural gas **$2.94 (+3.16%)**; gold **$4,139.28 (+1.89%)**.
- Exact market sanity: U.S.-Iran invasion **28.5%**, Iran NPT withdrawal **16.75%**, NATO Article 5 **7.5%**, Israel-Lebanon normalization **14.5%**. Markets were not score inputs.

## Next-Watch Triggers
- **Iran/Hormuz:** arrival/operation of the authorized KC-135 force; verified mining, literal zero traffic or formal closure; implemented pause or active negotiating round.
- **Israel-Lebanon:** additional pilot withdrawals, implementation of the 4 August talks, a casualty-bearing strike, Lebanese-army obstruction or Hezbollah rearmament.
- **Yemen/Red Sea:** attributable enforcement attack, Yanbu loading disruption, formal closure or naval convoy/escort activation.
- **Iran nuclear:** independent IAEA/satellite confirmation at Pickaxe, new enrichment/access evidence, verified strike damage or `nuclear_test`.
- **Russia/NATO:** firm *Gas Lisbon* attribution, strike inside Romanian territorial waters or Article 4/5 consultation.
- **South China Sea:** confidence-building implementation, treaty consultation, firearm use, death or vessel seizure.
- **Somalia/Gulf of Aden:** MT ASANA crew/ransom outcome, rescue/interdiction, crew harm or second hijack.
- **Saudi nuclear:** final agreement/safeguard text, authorization or construction of an enrichment plant, or weapons-related official rhetoric.

## Operational Caveat
- `/tmp` tmpfs remains **100% full (5.9 GiB)**. This did not block the actual deploy or in-memory local/live checks, but it coincided with the stock smoke path timing out. No unrelated temporary data was deleted.
