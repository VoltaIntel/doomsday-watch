# Nuke Watch Session State

Updated: 2026-06-26T06:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `4ec76e0` (`Update 2026-06-26T06:05:57Z — automated`).
- Final dashboard/current state: **62% / imminent**; raw global in state: **61.98**.
- Movement vs 03Z: global **61→62**. `north_korea` **6→11 / elevated** after Reuters/Politico/DW/Google News RSS reported Kim overseeing ballistic weapon tests; canonical `north_korea:missile_range_test` activated. `china` **24→26 / critical** from DPRK coupling. Other tracker numbers held.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 92, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 48, `iran_conventional` 32, `china` 26, `india` 11, `north_korea` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals: `iran_nuclear:iaea_access_denied`, `iran_nuclear:iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`, `north_korea:missile_range_test`.
- Signal hygiene: canonical check clean after deploy; no non-canonical signals. China/DPRK zone alerts generated normally.
- Source caveat: `web_search` and `web_extract` returned Tavily/API HTTP 432. Fallback used Google News RSS, direct terminal HTTP probes, UN Press RSS, NATO public pages, OilPriceAPI and Polymarket cache. Reuters/Politico direct pages blocked 401/403; IAEA pages 403; UN Press/NATO reachable; South Sudan/Abyei zero-hit on 30d RSS.
- Energy/markets: deploy OilPriceAPI 06:05Z Brent **$74.29**, WTI **$70.83**, gold **$4014.16**; Polymarket cache refreshed `2026-06-26T06:06:42Z`; worst divergence remains `israel_lebanon` (~99.3pp, horizon mismatch).
- Verification: JSON valid; canonical signals clean; `index.html` contains required command-deck markers; deploy/push succeeded; git status clean.

## Watch next
- DPRK: KCNA/wire details on whether the ballistic weapon tests were short-range artillery/rocket systems or strategic systems; any further configured `missile_range_test` confirmation, escalation across the DMZ, or device event.
- China-Taiwan: whether DPRK coupling plus Taiwan maritime-quarantine tabletop becomes sea-isolation, blockade execution, amphibious movement, or major PLA force-movement threshold.
- Hormuz/oil: repeated ship strikes, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse.
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of site-access modalities; inspector return; board action; verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Durand Line airstrike/shelling/casualty claims, border closures, or official mobilization; downgrade quickly if claims prove single-source/noisy.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Union State/treaty invocation, or allied direct-entry breakpoint.
- Israel-Lebanon and Gaza/West Bank: more confirmed truce-breach fatalities, Hezbollah retaliation, multi-front violence, holy-site tension, or wider regional spillover.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in negated/no-trigger notes unless intentionally activating the canonical signal. Especially avoid `ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade` in public notes/news unless you want pipeline keyword triggers.
