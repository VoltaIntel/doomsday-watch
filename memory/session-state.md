# Nuke Watch Session State

Updated: 2026-06-28T09:12:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 09Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed commit: `13356ff` (`Update 2026-06-28T09:07:50Z — automated`).
- Final dashboard/current state: **65% / imminent**; raw global in state: **65.10** after deploy.
- Movement vs 06Z: global stayed **65**. `pakistan_afghanistan` **30→28** coupled/raw because past-24h and 14d Kunar/Asadabad/TTP fallback searches still had zero fresh hits. `sudan:military_buildup` reactivated on DW RSF-surrounds-key-city coverage, but Sudan probability held **86** because that risk was already priced. Other coupled trackers unchanged.
- Coupled tracker table: `russia_ukraine` 98, `israel_lebanon` 92, `israel_palestine` 88, `sudan` 86, `iran_conventional` 86, `russia` 50, `iran_nuclear` 44, `pakistan_afghanistan` 28, `china` 26, `north_korea` 11, `india` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals after deploy: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:ceasefire_violation`, `israel_lebanon:diplomacy_active`, `israel_lebanon:diplomacy_refused`, `iran_nuclear:diplomacy_active`, `north_korea:missile_range_test`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after deploy. No noncanonical/legacy signal added. `china.active_signals=[]`; continued avoiding broad `bomber`, `missile launch`, `IAEA access`, `weapons-grade`, and truce/peace wording in notes unless intentionally activating a canonical signal.
- Source caveat: `web_search`/Tavily failed HTTP 432 on required queries. Fallback used Google News RSS, direct UN News/Press/NATO probes, terminal HTTP, OilPriceAPI and Polymarket cache. IAEA news/press returned 403; OCHA oPt RSS and EIA RSS endpoints returned 404.
- Energy/markets: OilPriceAPI 09Z Brent **$73.08**, WTI **$69.23**, gold **$4080.83**. Energy/RSS coverage shows oil steady/lower as Hormuz flows resume/ease supply fears, rejecting full waterway-stoppage thresholds. Polymarket refreshed `2026-06-28T09:08:24Z`; mapped divergences remain horizon-mismatch sanity flags.
- Emerging review: no tracker added. Thailand-Cambodia remains watch-only despite border-dispute/fact-finding/border-fence hits; Ethiopia-Eritrea low-confidence; Guyana/Venezuela quiet; Kosovo-Serbia below scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean immediately after deploy.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction/mining, escort incidents, traffic collapse, insurance/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, reversal of monitoring framework, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: framework implementation vs collapse; Hezbollah retaliation, IDF escalation, multi-front spillover, or rejection hardening.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad/TTP border-shelling claim; downgrade further if still unconfirmed.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, or atrocity reporting.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: whether Kim-supervised weapons events stay tactical or expand into strategic systems, DMZ escalation, or device event.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write `data/current_state.json` atomically, then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
