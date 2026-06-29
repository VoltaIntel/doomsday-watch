# Nuke Watch Session State

Updated: 2026-06-29T18:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 18Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Published state: **66% / imminent** (raw **61.98**).
- Deploy: succeeded, latest deploy commit `190449a` (`Update 2026-06-29T18:06:52Z — automated`).
- Mover vs 15Z: **Pakistan-Afghanistan raw/coupled 25→31** after multi-source cross-border strike/operation reporting, Taliban casualty claims and border-clash escalation language. Global stayed 66 after rounding. Other numeric lanes unchanged.
- Current coupled table: Russia-Ukraine **98**, Israel-Lebanon **94**, Iran War **90**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **50**, Iran Nuclear **46**, Pakistan-Afghanistan **31**, China-Taiwan **26**, India-Pakistan **11**, DPRK **10**, South Sudan/Abyei **8**, Turkey **5**.
- Active canonical signals after deploy: Iran conventional (`ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `military_buildup`); Israel-Lebanon (`ceasefire_violation`, `diplomacy_active`, `diplomacy_refused`); Pakistan-Afghanistan (`military_buildup`); DPRK (`missile_range_test`); Sudan (`military_buildup`). Deploy decay cleared expired `iran_nuclear:diplomacy_active` and `sudan:infrastructure_strike`. Canonical active-signal check clean.
- Source caveat: `web_search`/Tavily failed HTTP 432 on required searches; fallback used Google News RSS for all trackers + oil/energy + IAEA/UN + NATO/allied + emerging, direct UN/NATO/EIA/IAEA/OPEC probes, terminal HTTP, OilPriceAPI and Polymarket cache. Official probe: UN News/Press OK, NATO public pages OK, EIA RSS alternate path OK, IAEA news/press 403, OPEC 403.
- Energy/markets: deploy OilPriceAPI Brent **$73.13**, WTI **$70.88**, gold **$4020.21**. Hormuz headlines show route pressure/reduced traffic and risk premium, but resumed-shipment/market-pricing context rejects full stoppage. Polymarket refreshed `2026-06-29T18:07:33Z`; mapped markets remain horizon-mismatched sanity flags, worst `russia_ukraine` about **97.5pp**.
- Auto-detection: no tracker added. Emerging fallback dominated already-tracked lanes; Thailand-Cambodia, Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia remain below nuclear/alliance-spillover scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER` (line shows duplicated marker text but required marker present); deploy/push succeeded; git status clean.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction/mining, escort incidents, traffic collapse, insurer/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, monitoring reversal, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: framework implementation/collapse, Hezbollah retaliation, IDF escalation, multi-front spillover.
- India-Pakistan: Poonch/LoC drone or infiltration incidents becoming sustained cross-border fire or force movement.
- Pakistan-Afghanistan: follow-up strikes, confirmed regular-force movement, Kunar/Asadabad/TTP cross-border evidence, Kabul/Islamabad attribution hardening, or additional military-base attacks.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, atrocity evidence.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: prior firing-event signal expiry vs fresh strategic-system/DMZ/device evidence.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write `data/current_state.json` atomically, then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, `nuclear weapon/capability`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
