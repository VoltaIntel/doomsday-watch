# Nuke Watch Session State

Updated: 2026-06-25T21:12:30Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `710878a` (`Update 2026-06-25T21:07:47Z — automated`).
- Final dashboard/current state: **61% / imminent**; raw global in state: **61.38**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 92, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 48, `iran_conventional` 32.
- Movement vs 18Z: global **60→61**. `pakistan_afghanistan` **88→92** with fresh cross-border clash/airstrike/shelling reports and canonical `military_buildup` reactivated; `sudan` **80→82**; `israel_palestine` **87→88**; `iran_conventional` coupled **30→32**; `israel_lebanon` raw **94→95** but capped at 100.
- Active canonical signals: `iran_nuclear:iaea_access_denied`, `iran_nuclear:iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: post-deploy check caught false-positive `israel_lebanon:diplomacy_active` and `israel_palestine:diplomacy_active` from broad `ceasefire` keyword matching. Removed both, neutralized wording, redeployed, and verified no diplomacy-active timeline keys remain.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 required query groups. Fallback used Google News RSS, direct official/public terminal probes, UN Press RSS, NATO public HTML pages, UN News HTML, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA direct pages returned 403; NATO RSS endpoints returned 404 while HTML pages were reachable; ISW direct page returned 403 but ISW headlines were visible via Google News RSS.
- Energy/markets: deploy OilPriceAPI 21:07Z Brent **$74.68**, WTI **$71.40**, gold **$4026.48**; Polymarket cache refreshed `2026-06-25T21:08:21Z`; worst divergence remains `israel_lebanon` (~99.36pp, horizon mismatch).
- Verification: JSON valid; canonical signals clean; `index.html` contains required command-deck markers; deploy/push succeeded; latest commit `710878a`.

## Watch next
- Pakistan-Afghanistan: corroboration/refutation of reported Durand Line clashes, Pakistani airstrikes/shelling, casualty claims, border closures, or official mobilization; downgrade quickly if reports prove single-source/noisy.
- Hormuz/oil: whether ship-hit story becomes a pattern, insurer/charterer suspensions, explicit waterway obstruction, route-control escalation, naval escort incidents, or actual sustained traffic collapse.
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of site-access modalities; inspector return; board action; verified higher-level enrichment, underground-site restart, or device event.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Union State/treaty invocation, or allied direct-entry breakpoint.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Israel-Lebanon and Gaza/West Bank: more confirmed truce-breach fatalities, Hezbollah retaliation, multi-front violence, holy-site tension, or wider regional spillover.
- China-Taiwan: whether authority/law-enforcement or tabletop-drill evidence becomes sea-isolation, blockade execution, amphibious movement, or major PLA force-movement threshold.
- DPRK: credible official/wire confirmation of a fresh configured firing-event or device-event activity; shipbuilding/social repost noise is not enough.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in negated/no-trigger notes unless intentionally activating the canonical signal. Especially avoid `ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade` in public notes/news unless you want pipeline keyword triggers.
