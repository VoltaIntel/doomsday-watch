# Session State

> Last updated: 2026-07-21T21:16:45Z
> Session: DoomsdayWatch 21Z / 00:00 Amman morning deep scan

## Current Task
- **What:** Deep rolling past-24-hour review of all configured trackers, required sectors, market/energy sanity and emerging-crisis lanes.
- **Status:** Complete, deployed, pushed, tested and live-verified.
- **Result:** Global remains **75% / imminent**; unrounded additive coupled score remains **74.64%**.
- **Numeric movers:** None. Direct review confirmed 17 reported Tuesday Gaza deaths, the weekend U.S. strike on the safeguarded but unfinished Darkhovin power plant and the Houthi Saudi-port tanker threat/two tanker U-turns; all remain within already-scored high-risk lanes.
- **Trackers/signals:** All **18 canonical IDs** reviewed; no tracker added. `iran_conventional:hormuz_controlled_not_closed` expired under temporal decay after no fresh qualifying traffic-control evidence. A pipeline-added `israel_palestine:diplomacy_active` was caught and removed because the October truce was background rather than a fresh diplomatic development. Final trackers, zones and timeline align at **9 canonical signals**.
- **Repository:** Final automated deploy commit `4a9ed71f`; exact metadata/signal-audit commit `a4e29ee7` is pushed and equals `origin/main`; tree clean.
- **Deployment:** GitHub Pages run `29869318368` succeeded. Live root/state return HTTP 200, expose all three command-deck markers, 18 trackers/news items, 9 aligned signals, exact fallback metadata and state timestamp `2026-07-21T21:10:46Z`.
- **Tests:** Final stock run passed **31 non-smoke tests**; its fixed 60-second smoke setup timed out for 11 cases. A source-identical final-state isolated copy with only that harness timeout raised passed **11/11 in 54.35s**.

## Evidence Decisions
- **Iran/Hormuz/nuclear:** Guardian and UN confirm a tenth strike day, Gulf attacks and damage to vital civilian infrastructure. Direct Tehran Times inspection says the safeguarded but unfinished Darkhovin plant was struck over the weekend and the Iranian UN letter was delivered Monday; this is newly indexed context, not a fresh post-cutoff attack or a new weapons-development threshold. Iran conventional remains capped at **100%**; Iran nuclear holds **47% raw / 54% coupled**.
- **Israel-Palestine:** Direct IMEMC inspection reports 17 Tuesday deaths: the already-reviewed al-Masri family of six plus eleven other reported deaths. OHCHR/UN reports 57 killed from 13-20 July. The lane remains **88%** without near-ceiling inflation.
- **Yemen/Red Sea:** Guardian directly confirms the threat against tankers using Saudi ports, two independently observed Saudi-crude U-turns, a Houthi claim of six reroutes and no formal Bab el-Mandeb closure. No attributable enforcement attack or U.S./Saudi counterstrike was verified; `yemen_red_sea` holds **49% / critical**.
- **Israel-Lebanon:** Aoun-Trump talks on Hezbollah disarmament add political support to the pilot. Zawtar implementation remains in force without wider withdrawal or reversal; `israel_lebanon` holds **76% raw / 86% coupled**.
- **Auto-detection:** No candidate qualified across 18 reviewed lanes. Syria/Iraq remained localized or Iran-war spillover; other candidates were stale, analytic, humanitarian/disaster-related or below the three-mention/two-independent-source operational gate.

## Sources and Sanity
- All **22 Tavily searches** and **3 extraction targets** failed HTTP 432. Fallback completed through **18 core + 42 targeted/exact/emerging** Google News RSS groups, 10 Bing RSS checks, direct Guardian/IMEMC/Tehran Times/UN/NATO inspection, official feeds, terminal HTTP, OilPriceAPI and Gamma.
- IAEA/OPEC terminal probes returned 403; browser IAEA was Cloudflare-blocked; configured OCHA/UN Sudan paths returned 404; UN Press RSS returned 200 but parsed no items.
- Final energy: Brent **$91.51 (+2.62%/24h)**; WTI **$84.42 (+2.43%)**; natural gas **$2.89 (+2.12%)**; gold **$4,077.95 (+1.78%)**.
- Exact sanity: U.S.-Iran invasion **27.5%**, Iran device **5.4% (-0.05pp)**, Iran test **4.5%**, NPT withdrawal **14.95%**, NATO Article 5 **7.5%**, China invasion **4.25% (+0.1pp)**, China-Taiwan clash **6.85% (-0.2pp)**, Ukraine peace deal **21.5%**, Israel-Lebanon normalization **15.0% (-1.5pp)**. Markets were not score inputs.

## Next-Watch Triggers
- Darkhovin/Pickaxe/Natanz: verified new strike execution or damage, Iranian material dispersal, current underground operations, new enrichment result, inspector exclusion or nuclear retaliation doctrine.
- Iran/Hormuz: independently verified mine-laying, literal zero passage, formal closure, another crew-casualty vessel attack, wider Gulf infrastructure attacks or an implemented pause.
- Yemen/Red Sea: independently verified third-or-larger diversion wave, attributable attack/interdiction, U.S./Saudi action, Yanbu loading disruption or insurance/AIS discontinuity.
- Israel-Lebanon: implementation beyond Zawtar, pilot reversal, wider verified withdrawal, weapons-control mechanism or Israeli re-entry.
- Gaza/West Bank: sustained multi-day casualty acceleration, truce collapse, mass displacement order or wider regional combat entry.
- South China Sea: Philippine-U.S. consultation, operational alliance step, deployment, firearm use, death or vessel seizure/collision.
- Somalia/Gulf of Aden: rescue/interdiction outcome, crew harm, ransom demand, another hijack or sustained naval response.
