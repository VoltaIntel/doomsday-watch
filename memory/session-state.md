# Nuke Watch Session State

Updated: 2026-06-26T00:07:10Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `7f1329b` (`Update 2026-06-26T00:05:45Z — automated`).
- Final dashboard/current state: **61% / imminent**; raw global in state: **61.46**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 92, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 48, `iran_conventional` 32, `china` 24, `india` 11, `north_korea` 6.
- Movement vs 21Z: global held **61**. Only numeric change was `north_korea` **5→6** as a watch-only adjustment on DPRK warship/strategic naval messaging; no configured DPRK firing-event/device-event signal was activated. Other active lanes were refreshed/reconfirmed without inflating probabilities.
- Active canonical signals: `iran_nuclear:iaea_access_denied`, `iran_nuclear:iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after deploy; no non-canonical signals and no `diplomacy_active` false positives. Notes/news kept sanitized to avoid broad keyword traps.
- Source caveat: `web_search`/Tavily failed HTTP 432 for required query groups. Fallback used Google News RSS, direct official/public terminal probes, UN Press RSS, UN News HTML, NATO public HTML pages, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA direct pages returned 403; South Sudan/Abyei and emerging-crisis RSS sparse/zero-hit.
- Energy/markets: deploy OilPriceAPI 00:05Z Brent **$74.84**, WTI **$71.52**, gold **$4032.70**; Polymarket mapped-slug cache refreshed `2026-06-26T00:06:22Z`; worst divergence remains `israel_lebanon` (~99.4pp, horizon mismatch).
- Verification: JSON valid; canonical signals clean; `index.html` contains required command-deck markers; deploy/push succeeded; latest commit `7f1329b`.

## Watch next
- Hormuz/oil: repeated ship strikes, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse.
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of site-access modalities; inspector return; board action; verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Durand Line airstrike/shelling/casualty claims, border closures, or official mobilization; downgrade quickly if claims prove single-source/noisy.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Union State/treaty invocation, or allied direct-entry breakpoint.
- Israel-Lebanon and Gaza/West Bank: more confirmed truce-breach fatalities, Hezbollah retaliation, multi-front violence, holy-site tension, or wider regional spillover.
- DPRK: credible official/wire confirmation of a configured strategic firing-event or device-event activity; warship/naval-rhetoric alone is not enough.
- China-Taiwan: whether carrier/tabletop/quarantine evidence becomes sea-isolation, blockade execution, amphibious movement, or major PLA force-movement threshold.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in negated/no-trigger notes unless intentionally activating the canonical signal. Especially avoid `ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade` in public notes/news unless you want pipeline keyword triggers.
