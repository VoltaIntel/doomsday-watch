# Nuke Watch Session State

Updated: 2026-06-26T03:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `7282c61` (`Update 2026-06-26T03:06:49Z — automated`).
- Final dashboard/current state: **61% / imminent**; raw global in state: **61.46**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 92, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 48, `iran_conventional` 32, `china` 24, `india` 11, `north_korea` 6, `turkey` 5, `south_sudan_abyei` 8.
- Movement vs 00Z: **no numeric probability changes**. Active lanes were refreshed/reconfirmed without inflation. DPRK remains watch-only on destroyer/naval strategic messaging; no configured DPRK firing-event/device-event signal activated.
- Active canonical signals: `iran_nuclear:iaea_access_denied`, `iran_nuclear:iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after deploy; no non-canonical signals and no `diplomacy_active` false positives. Notes/news stayed sanitized to avoid broad keyword traps.
- Source caveat: `web_search`/Tavily failed HTTP 432 for required query groups. Fallback used Google News RSS, direct official/public terminal probes, UN Press RSS, NATO HTML, EIA, OilPriceAPI and Polymarket Gamma/cache. UN News RSS parse failed; ISW and IAEA public pages returned 403; South Sudan/Abyei was zero-hit on 30d RSS.
- Energy/markets: deploy OilPriceAPI 03:06Z Brent **$74.20**, WTI **$70.97**, gold **$3986.96**; Polymarket mapped-slug refresh `2026-06-26T03:07:32Z`; worst divergence remains `israel_lebanon` (~99.4pp, horizon mismatch).
- Verification: JSON valid; canonical signals clean; `index.html` contains required command-deck markers; deploy/push succeeded; git status clean.

## Watch next
- Hormuz/oil: repeated ship strikes, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse.
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of site-access modalities; inspector return; board action; verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Durand Line airstrike/shelling/casualty claims, border closures, or official mobilization; downgrade quickly if claims prove single-source/noisy.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Union State/treaty invocation, or allied direct-entry breakpoint.
- Israel-Lebanon and Gaza/West Bank: more confirmed truce-breach fatalities, Hezbollah retaliation, multi-front violence, holy-site tension, or wider regional spillover.
- DPRK: credible official/wire confirmation of a configured strategic firing-event or device-event activity; warship/naval-rhetoric alone is not enough.
- China-Taiwan: whether tabletop/quarantine evidence becomes sea-isolation, blockade execution, amphibious movement, or major PLA force-movement threshold.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in negated/no-trigger notes unless intentionally activating the canonical signal. Especially avoid `ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade` in public notes/news unless you want pipeline keyword triggers.
