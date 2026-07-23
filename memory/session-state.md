# Session State

> Last updated: 2026-07-23T15:20:50Z
> Session: DoomsdayWatch 15Z morning deep scan

## Current Task
- **What:** Deep rolling past-24-hour review of all configured trackers, required sectors, allied posture, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed and live-verified.
- **Result:** Global remains **76% / imminent**; unrounded additive coupled score rose **75.62% → 75.70%**.
- **Numeric movers:** `yemen_red_sea` rose **62% → 66% / imminent**. The other 18 configured tracker scores held.
- **Signals:** Canonical `iran_conventional:diplomacy_active` and `yemen_red_sea:external_backing` activated. Trackers, zones and timeline align at **11 canonical signals**.
- **Auto-detection:** Reviewed 23 untracked lanes; none met the configured three-mention/two-source gate. No tracker was added.
- **Repository:** Deploy commit `4f1ae1b0`; exact source-fallback metadata commit `51fda4ed`; pushed to `origin/main`.
- **Deployment:** GitHub Pages run `30020079573` succeeded for exact commit `51fda4ed`. Live root/state returned HTTP 200 and expose all command-deck markers, `morning_deep_scan_15z`, **76% / imminent**, raw **75.70**, 19 trackers/news items and the aligned 11-signal set.
- **Tests:** JSON/canonical/timeline and local/live checks passed. **31/31 non-smoke tests passed**. The stock smoke fixture hit its fixed 60-second copied-pipeline ceiling; the identical **11/11 assertions passed in 62.37s** from an isolated copy with only that harness timeout extended.

## Evidence Decisions
- **Yemen/Red Sea:** Reuters reported at 14:23Z that Iran flew IRGC commanders and missile equipment to the Houthis. This activated canonical `external_backing` at its configured +4 weight. It remains one wire source chain despite broad syndication. Saudi authorities still confirm only `Encelia` hit with crew safe; `Layla` remains unverified.
- **Iran/Hormuz:** The IMO told UN News that traffic is almost completely halted, with very few ships if any transiting and about 6,000 seafarers stranded aboard roughly 500 ships. The report says the parties are talking and last month’s memorandum remains a basis for negotiations, supporting canonical `diplomacy_active`. It does not establish literal zero traffic, formal closure, verified mining or a ceasefire. Risk stays capped at 100%.
- **Energy:** OilPriceAPI reached Brent **$100.60** and WTI **$92.08** during final deploy. Energy remains sanity-only.
- **Russia-Ukraine:** Reuters says shipowners halted some Ukrainian Black Sea port calls over Russian strike risk. No NATO-entry, Belarus-entry or nuclear-use threshold followed; risk holds 99%.
- **South China Sea:** Fresh international headlines resolve to the already-scored Bajo and Ayungin incidents; no third distinct encounter or treaty consultation surfaced. Risk holds 22%.
- **Southern Thailand:** Follow-ons concern the suspect hunt after the configured Narathiwat assault; no second attack, emergency decree or Malaysia spillover surfaced. Risk holds 18%.
- **Iran nuclear:** No independent enrichment, inspector-access, reprocessing or detonation threshold surfaced. IAEA remained security-gated. Risk holds 47% raw / 54% coupled.
- **Saudi nuclear:** The signed civil-nuclear agreement remains the leading untracked proliferation watch; no operating or authorized enrichment/reprocessing plant, fissile production or weaponization step exists.

## Sources and Sanity
- All **24 Tavily searches** and **10 extraction targets** failed HTTP 432. Fallback used **64 Google News RSS coverage queries plus nine exact-event follow-ups**, direct UN/NATO browser inspection, official UN/NATO/EIA pages and feeds, terminal HTTP, OilPriceAPI and exact Gamma.
- IAEA, UKMTO, CENTCOM and OPEC returned HTTP 403; OCHA/UN Sudan paths returned 404; Reuters direct was DataDome/403 and was checked through RSS/syndication.
- Final deploy energy: Brent **$100.60**, WTI **$92.08**, natural gas **$2.95**, gold **$4,059.74**.
- Exact market sanity: U.S.-Iran invasion **29.5%**, Iran nuke **5.75%**, Iran test **5.5%**, NPT withdrawal **16.9%**, NATO Article 5 **7.0%**, China invasion **3.85%**, China-Taiwan clash **6.85%**, DPRK invasion **2.9%** on thin volume and Israel-Lebanon normalization **15.0%**. Markets were not score inputs.

## Next-Watch Triggers
- **Yemen/Red Sea:** independent confirmation or operational detail for the Iranian transfer; confirmation of `Layla`; crew harm/pollution; another verified attack; Saudi/U.S. retaliation; formal closure or naval escort.
- **Iran/Hormuz:** thirteenth numbered strike night or new target class; literal zero traffic or formal closure; independently verified mine deployment; implemented ceasefire or detailed negotiating round; bridge/power-plant strike.
- **Russia-Ukraine:** wider Black Sea port shutdown, vessel casualty, nuclear-use step, Belarusian entry or NATO combat entry.
- **South China Sea:** third distinct coercive encounter, injury/major damage, firearm use/death/seizure, treaty consultation or implemented confidence-building measure.
- **Southern Thailand:** second coordinated attack or additional security-force deaths; responsibility claim; large force sweep/emergency decree; Malaysia spillover; government-BRN talks resume or break down.
- **Iran nuclear:** IAEA/satellite confirmation of current underground operations, new enrichment result, inspector exclusion or detonation.
- **Saudi nuclear:** congressional action, safeguards text, enrichment/reprocessing authorization or construction, Additional Protocol decision or weapons rhetoric.
- **Russia/NATO:** attributed armed attack on alliance territory or Article 4/5 consultation.
- **Mali/Sahel:** official U.S. order/deployment, mass-casualty JNIM attack or external-state strike.
