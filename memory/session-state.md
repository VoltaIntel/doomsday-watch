# Nuke Watch Session State

Updated: 2026-06-28T18:08Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 18Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed commit: `9f5ac38` (`Update 2026-06-28T18:05:37Z — automated`).
- Final dashboard/current state: **66% / imminent**; raw global in state: **66.00** after deploy.
- Movement vs 15Z: global unchanged. `pakistan_afghanistan` **27→25** and `north_korea` **11→10** on lack of fresh corroboration/decay; `russia_ukraine:military_buildup` aged out but Russia-Ukraine remains **98** on continuing war context.
- Coupled tracker table: `russia_ukraine` 98, `israel_lebanon` 92, `iran_conventional` 90, `israel_palestine` 88, `sudan` 86, `russia` 50, `iran_nuclear` 46, `china` 26, `pakistan_afghanistan` 25, `india` 11, `north_korea` 10, `south_sudan_abyei` 8, `turkey` 5.
- Active canonical signals after deploy: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:diplomacy_active`, `israel_lebanon:diplomacy_refused`, `iran_nuclear:diplomacy_active`, `north_korea:missile_range_test`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`. `russia_ukraine:military_buildup` removed/expired.
- Signal hygiene: canonical check clean after deploy. No noncanonical/legacy signal added. `china.active_signals=[]`; `russia_ukraine.active_signals=[]`.
- Source caveat: `web_search`/Tavily failed HTTP 432 on required queries. Fallback used Google News RSS for all tracker zones, direct UN/NATO probes, terminal HTTP, OilPriceAPI and Polymarket cache. Official probe: UN News RSS OK, UN Press RSS OK, NATO news/press OK, IAEA news/press 403.
- Energy/markets: OilPriceAPI 18Z Brent **$73.08**, WTI **$69.23**, gold **$4080.83**. Energy RSS shows route pressure but no full Hormuz stoppage. Polymarket refreshed `2026-06-28T18:06:21Z`; mapped divergences remain horizon-mismatch sanity flags, worst `russia_ukraine` 97.47pp.
- Emerging review: no tracker added. Thailand-Cambodia, Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia did not cross nuclear-escalation/alliance-spillover threshold.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean after deploy.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction/mining, escort incidents, traffic collapse, insurance/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, reversal of monitoring framework, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: framework implementation vs collapse; Hezbollah retaliation, IDF escalation, multi-front spillover, or rejection hardening.
- Pakistan-Afghanistan: older `military_buildup` signal is near age-out; downgrade if still unconfirmed after expiry, revive only on fresh Kunar/Asadabad/TTP corroboration.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, or atrocity reporting.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: older firing-event signal is decaying; watch for fresh strategic systems, DMZ escalation, or device event.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write `data/current_state.json` atomically, then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
