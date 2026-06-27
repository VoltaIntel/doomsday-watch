# Nuke Watch Session State

Updated: 2026-06-27T03:09:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `8f9f5b8` (`Update 2026-06-27T03:05:43Z — automated`).
- Final dashboard/current state: **63% / imminent**; raw global in state: **62.90** after deploy.
- Main movement vs 00Z: `iran_conventional` **64→70 / imminent** final (raw **56→62**) after Reuters and New York Times joined CBS/RFE in corroborating U.S. strikes inside Iran after the Hormuz cargo-ship drone attack. Oil/traffic data still reject full Hormuz shutdown.
- Other coupled trackers held numerically: `israel_lebanon` 88, `russia_ukraine` 98, `pakistan_afghanistan` 42, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 46, `china` 26, `india` 11, `north_korea` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:ceasefire_violation`, `israel_lebanon:diplomacy_active`, `iran_nuclear:diplomacy_active`, `iran_nuclear:iaea_emergency`, `north_korea:missile_range_test`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: no non-canonical signals used. No new canonical signal was added; existing signals were retained/reconfirmed. Notes deliberately avoid known broad-keyword false positives.
- Source caveat: `web_search`/Tavily failed HTTP 432 on all attempted required queries. Fallback used Google News RSS, direct terminal official/public probes, UN News RSS, UN Press RSS, NATO pages, OCHA oPt, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA public pages returned 403. Pakistan-Afghanistan and South Sudan/Abyei hits were stale/no-fresh-trigger.
- Energy/markets: OilPriceAPI 03Z Brent **$73.08** (-1.51% 24h), WTI **$69.23** (-2.45% 24h), gold **$4080.83** (+2.35% 24h). Polymarket cache refreshed `2026-06-27T03:06:24Z`; worst mapped divergence remains `russia_ukraine` (~97.5pp, horizon mismatch).
- Emerging review: no new tracker added. Thailand-Cambodia remains a watch cluster but below nuclear/alliance-spillover threshold; Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia stale/low-confidence for this scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded. Post-deploy repo status shows only mandatory memory-log changes (`memory/session-state.md`, `memory/2026-06-27.md`).

## Watch next
- Iran/Hormuz: repeated ship strikes, official truce collapse, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse. Current Brent/WTI and traffic coverage still reject full shutdown.
- Iran conventional: whether U.S. strikes remain limited/self-contained or trigger Iranian retaliation against shipping, U.S. bases, Israel, or Gulf infrastructure.
- Israel-Lebanon: whether the framework accord produces operational de-escalation or is overwhelmed by South Lebanon clashes; any Hezbollah retaliation, IDF escalation, multi-front violence, or framework collapse.
- Iran/IAEA: actual verification visit execution, direct agency-page access returning, any reversal of interim framework, verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad shelling and border force movement. Downgrade further if the single-source claim ages without confirmation.
- DPRK: whether Kim-supervised tests remain tactical/short-range or expand into strategic systems; any configured strategic firing-event confirmation, DMZ escalation, or device event.
- Russia-Ukraine/Russia-NATO: confirmed Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Gaza/West Bank: more confirmed truce-breach fatalities, holy-site tension, or wider regional spillover.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, etc.) unless intentionally activating the canonical signal.
