# Nuke Watch Session State

Updated: 2026-06-27T09:12:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 09Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `e7241f7` (`Update 2026-06-27T09:07:02Z — automated`).
- Final dashboard/current state: **63% / imminent**; raw global in state: **62.90** after deploy.
- Movement vs 06Z: **no numeric probability changes**. DPRK firing-event signal refreshed on fresh Kim-supervised/ballistic-system coverage; Sudan El Obeid urgency remains high; Israel-Lebanon framework/partial-withdrawal reporting strengthened down-pressure; Iran/Hormuz energy and tanker-flow checks still reject a full waterway stoppage.
- Pipeline signal decay: `iran_nuclear:iaea_emergency` aged out and was cleared by normal temporal decay during deploy. Iran nuclear remains **46 final / critical** on `diplomacy_active` plus Iran-conventional coupling.
- Coupled tracker table: `russia_ukraine` 98, `israel_lebanon` 88, `israel_palestine` 88, `sudan` 82, `iran_conventional` 70, `russia` 50, `iran_nuclear` 46, `pakistan_afghanistan` 42, `china` 26, `north_korea` 11, `india` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals after deploy: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:ceasefire_violation`, `israel_lebanon:diplomacy_active`, `iran_nuclear:diplomacy_active`, `north_korea:missile_range_test`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after deploy; no new canonical signal added; no non-canonical IDs/signals used.
- Source caveat: `web_search`/Tavily failed HTTP 432 on all required queries. Fallback used Google News RSS, direct terminal official/public probes, UN News RSS, UN Press RSS, NATO pages, OCHA oPt, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA public pages returned 403; ReliefWeb API returned 410; Pakistan-Afghanistan, Israel-Palestine and South Sudan/Abyei targeted RSS were sparse/zero-hit.
- Energy/markets: OilPriceAPI 09Z Brent **$73.08** (+0.55% 24h), WTI **$69.23** (-0.23% 24h), gold **$4080.83** (+1.24% 24h). Polymarket mapped cache refreshed `2026-06-27T09:07:50Z`; worst mapped divergence remains `russia_ukraine` (~97.47pp, horizon mismatch).
- Emerging review: no new tracker added. Thailand-Cambodia remains a watch cluster but below nuclear/alliance-spillover threshold; Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia stale/low-confidence for this scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded.

## Watch next
- Iran/Hormuz: repeated ship strikes, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse. Current Brent/WTI and traffic coverage still reject full stoppage.
- Iran conventional: whether U.S. strikes remain limited/self-contained or trigger Iranian retaliation against shipping, U.S. bases, Israel, or Gulf infrastructure.
- Israel-Lebanon: whether the signed framework produces operational de-escalation or is overwhelmed by South Lebanon clashes; any Hezbollah retaliation, IDF escalation, multi-front violence, or framework collapse.
- Iran/IAEA: actual verification visit execution, direct agency-page access returning, any reversal of interim framework, verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad shelling and border force movement. Downgrade further if the single-source claim ages without confirmation.
- DPRK: whether Kim-supervised firings remain tactical/short-range or expand into strategic systems; any configured strategic firing-event confirmation, DMZ escalation, or device event.
- Russia-Ukraine/Russia-NATO: confirmed Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Gaza/West Bank: more confirmed truce-breach fatalities, holy-site tension, or wider regional spillover.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, etc.) unless intentionally activating the canonical signal.
