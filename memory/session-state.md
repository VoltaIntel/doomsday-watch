# Nuke Watch Session State

Updated: 2026-06-28T12:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 12Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed commit: `12a3fd4` (`Update 2026-06-28T12:06:41Z — automated`).
- Final dashboard/current state: **66% / imminent**; raw global in state: **66.00** after deploy.
- Movement vs 09Z: global **65→66**. `iran_conventional` **86→90** coupled (raw **78→82**) on NPR/Washington Post/USA Today/Al Jazeera/CNBC fresh U.S.-Iran strike-exchange/Gulf-base/Hormuz tanker reporting. `iran_nuclear` **44→46** coupled (raw **37→39**) on stronger agency-visit dispute/verification risk plus Iran-conventional coupling. `pakistan_afghanistan` **28→27** as past-24h and 14d Kunar/Asadabad/TTP searches still had zero fresh hits. `israel_lebanon:ceasefire_violation` expired during deploy; Israel-Lebanon stayed **92** on `diplomacy_active` + `diplomacy_refused` and Iran coupling.
- Coupled tracker table: `russia_ukraine` 98, `israel_lebanon` 92, `iran_conventional` 90, `israel_palestine` 88, `sudan` 86, `russia` 50, `iran_nuclear` 46, `pakistan_afghanistan` 27, `china` 26, `india` 11, `north_korea` 11, `south_sudan_abyei` 8, `turkey` 5.
- Active canonical signals after deploy: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:diplomacy_active`, `israel_lebanon:diplomacy_refused`, `iran_nuclear:diplomacy_active`, `north_korea:missile_range_test`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after deploy. No noncanonical/legacy signal added. `china.active_signals=[]`; `israel_lebanon:ceasefire_violation` cleared by normal decay, not manual cleanup.
- Source caveat: `web_search`/Tavily failed HTTP 432 on required queries. Fallback used Google News RSS, direct UN News/Press/NATO probes, terminal HTTP, OilPriceAPI and Polymarket cache. IAEA news/press returned 403.
- Energy/markets: OilPriceAPI 12Z Brent **$73.08**, WTI **$69.23**, gold **$4080.83**. Energy/RSS coverage shows oil back near prewar/lower as Hormuz flows resume/ease supply fears, rejecting full waterway-stoppage thresholds. Polymarket refreshed `2026-06-28T12:07:21Z`; mapped divergences remain horizon-mismatch sanity flags.
- Emerging review: no tracker added. Thailand-Cambodia remains watch-only despite 30d border-dispute items; Ethiopia-Eritrea low-confidence; Guyana/Venezuela sparse; Kosovo-Serbia quiet.
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
