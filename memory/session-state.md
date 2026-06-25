# Nuke Watch Session State

Updated: 2026-06-25T18:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `63d78d9` (`Update 2026-06-25T18:07:37Z — automated`).
- Final dashboard/current state: **60% / imminent**; raw global in state: **60.45**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 88, `israel_palestine` 87, `sudan` 80, `russia` 50, `iran_nuclear` 48, `iran_conventional` 30.
- Movement vs 15Z: global held **60** after rounding. `sudan` 78→80, `israel_palestine` 86→87, `china` 23→24. Hormuz/oil de-risking continues; Pakistan-Afghanistan remains quiet/falling.
- Active canonical signals: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `sudan:infrastructure_strike/military_buildup`, `israel_palestine:ceasefire_violation`.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 query groups. Fallback used Google News RSS, direct official/public terminal probes, UN/NATO/EIA/ISW/UN Press pages, OilPriceAPI and Polymarket Gamma/cache. IAEA/OPEC direct pages returned 403.
- Energy/markets: Brent **$74.87**, WTI **$71.61**, gold **$4036.17**; Polymarket cache refreshed `2026-06-25T18:08:12Z`; worst divergence remains `israel_lebanon` (~99.35pp).
- Verification: JSON valid; `index.html` contains required markers; deploy/push succeeded.

## Watch next
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of site-access modalities; inspector return; board action; verified higher-level enrichment, underground-site restart, or device event.
- Hormuz/oil: sustained ship-flow recovery vs vessel attack claims; insurer/charterer suspensions; explicit waterway obstruction; route-control escalation; naval escort incidents.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Union State/treaty invocation, or allied direct-entry breakpoint.
- Sudan/El Obeid/Kordofan: confirmed RSF offensive/entry into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or full-front breakout.
- Gaza/West Bank: whether continuing pressure becomes wider multi-front violence, holy-site tension, or regional spillover.
- China-Taiwan: whether authority/law-enforcement assertions become sea-isolation, blockade execution, amphibious movement, or major PLA force-movement threshold.
- DPRK: corroborated South Korean/Japanese/U.S. official confirmation of fresh configured firing-event or device-event activity; rhetoric/shipbuilding alone is not enough.
- Turkey, Pakistan-Afghanistan, South Sudan/Abyei: currently quiet/sparse; keep checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in negated/no-trigger notes unless intentionally activating the canonical signal.
