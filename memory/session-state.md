# Nuke Watch Session State

Updated: 2026-06-28T06:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 06Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `7377032` (`Update 2026-06-28T06:06:40Z — automated`).
- Final dashboard/current state: **65% / imminent**; raw global in state: **65.24** after deploy.
- Movement vs 03Z: global stayed **65**; `pakistan_afghanistan` **32→30** coupled/raw because targeted Kunar/Asadabad/TTP searches again lacked fresh corroboration and the older border signal continues to decay. Iran War held **86** coupled (raw **78**) after Axios/WSJ/USA Today reconfirmed the strike/tanker cycle but oil/Hormuz traffic checks rejected full stoppage. All other coupled tracker probabilities unchanged.
- Coupled tracker table: `russia_ukraine` 98, `israel_lebanon` 92, `israel_palestine` 88, `sudan` 86, `iran_conventional` 86, `russia` 50, `iran_nuclear` 44, `pakistan_afghanistan` 30, `china` 26, `north_korea` 11, `india` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals after deploy: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:ceasefire_violation`, `israel_lebanon:diplomacy_active`, `israel_lebanon:diplomacy_refused`, `iran_nuclear:diplomacy_active`, `north_korea:missile_range_test`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after final redeploy. `sudan:military_buildup` expired during deploy. A transient `china:bomber_redeployment` note-keyword false positive was introduced by “bomber-drill framing” wording, then removed/neutralized and redeployed; final state has `china.active_signals=[]`.
- Source caveat: `web_search`/Tavily failed HTTP 432 on required queries. Fallback used Google News RSS, direct UN News/Press/NATO probes, terminal HTTP, OilPriceAPI and Polymarket cache. IAEA news/press returned 403; OCHA oPt RSS and EIA RSS endpoints returned 404.
- Energy/markets: OilPriceAPI 06Z Brent **$73.08**, WTI **$69.23**, gold **$4080.83**. Energy/RSS coverage shows oil steady/lower as Hormuz tanker flows resume/ease supply fears, rejecting full waterway-stoppage thresholds. Polymarket refreshed `2026-06-28T06:07:16Z`; mapped divergences remain horizon-mismatch sanity flags.
- Emerging review: no tracker added. Thailand-Cambodia remains watch-only despite multiple border-dispute/military-activity hits; Ethiopia-Eritrea remains low-confidence; Guyana/Venezuela and Kosovo-Serbia remain stale/low-confidence for dashboard scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction, mining, escort incidents, traffic collapse, insurance/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, reversal of monitoring framework, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: framework implementation vs collapse; Hezbollah retaliation, IDF escalation, multi-front spillover, or rejection hardening.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad/TTP border-shelling claim; downgrade further if still unconfirmed.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, or atrocity reporting.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: whether Kim-supervised weapons events stay tactical or expand into strategic systems, DMZ escalation, or device event.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
