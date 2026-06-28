# Nuke Watch Session State

Updated: 2026-06-28T03:11:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 03Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `c848595` (`Update 2026-06-28T03:05:09Z — automated`).
- Final dashboard/current state: **65% / imminent**; raw global in state: **65.42** after deploy.
- Movement vs 00Z: global stayed **65**; `iran_conventional` **84→86** coupled (raw **76→78**) after Reuters/CNBC/CBC/Open/Jerusalem Post/Times of India second-night U.S. strike/tanker coverage; `pakistan_afghanistan` **34→32** as targeted Kunar/Asadabad/TTP searches remained empty and the older border signal decayed. All other coupled tracker probabilities unchanged.
- Coupled tracker table: `russia_ukraine` 98, `israel_lebanon` 92, `israel_palestine` 88, `sudan` 86, `iran_conventional` 86, `russia` 50, `iran_nuclear` 44, `pakistan_afghanistan` 32, `china` 26, `north_korea` 11, `india` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals after deploy: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:ceasefire_violation`, `israel_lebanon:diplomacy_active`, `israel_lebanon:diplomacy_refused`, `iran_nuclear:diplomacy_active`, `north_korea:missile_range_test`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after deploy. No new canonical signal added at 03Z. Existing signals retained/reconfirmed where supported; Pakistan-Afghanistan was not reconfirmed and continues to decay.
- Source caveat: `web_search`/Tavily failed HTTP 432 on all required queries. Fallback used Google News RSS, direct terminal official/public probes, UN News/Press RSS, NATO pages, OilPriceAPI and Polymarket Gamma/cache. IAEA pages returned 403; OCHA oPt RSS and EIA RSS endpoints returned 404 in the 03Z probe.
- Energy/markets: OilPriceAPI 03Z Brent **$73.08**, WTI **$69.23**, gold **$4080.83**. Energy/RSS coverage shows oil sliding/erasing wartime gains as Hormuz traffic resumes/improves, rejecting full waterway-stoppage thresholds. Polymarket cache refreshed `2026-06-28T03:05:47Z`; mapped divergences remain horizon-mismatch sanity flags.
- Emerging review: no tracker added. Thailand-Cambodia has multiple border-dispute/military-activity hits but remains watch-only; Ethiopia-Eritrea remains low-confidence; Guyana/Venezuela and Kosovo-Serbia remain stale/low-confidence for dashboard scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded.

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
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, etc.) unless intentionally activating the canonical signal.
