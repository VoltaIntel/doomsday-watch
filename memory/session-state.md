# Nuke Watch Session State

Updated: 2026-06-29T21:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 21Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Published state: **67% / imminent** (raw **66.90**).
- Deploy: succeeded, latest deploy commit `d10167f` (`Update 2026-06-29T21:08:04Z — automated`).
- Mover vs 18Z: **Pakistan-Afghanistan raw/coupled 31→36** after PBS/BBC/Al Jazeera/KabulNow/Arab News/New Arab reporting on Pakistani cross-border operations/strikes, UN civilian-casualty reporting and Taliban retaliation language. Global **66→67** after rounding. Other numeric lanes unchanged.
- Current coupled table: Russia-Ukraine **98**, Israel-Lebanon **94**, Iran War **90**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **50**, Iran Nuclear **46**, Pakistan-Afghanistan **36**, China-Taiwan **26**, India-Pakistan **11**, Turkey **5**, South Sudan/Abyei **8**. DPRK raw remains 10 but its older configured firing-event signal expired during deploy, so active signal list is cleaner.
- Active canonical signals after final deploy: Iran conventional (`ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `military_buildup`); Israel-Lebanon (`ceasefire_violation`, `diplomacy_active`, `diplomacy_refused`); Pakistan-Afghanistan (`military_buildup`); Sudan (`military_buildup`). Deploy decay cleared expired DPRK `missile_range_test`. Canonical active-signal check clean.
- Source caveat: `web_search`/Tavily failed HTTP 432 on required searches; fallback used Google News RSS for all trackers + oil/energy + IAEA/UN + NATO/allied + emerging, direct UN/NATO/OCHA/EIA/IAEA/OPEC probes, terminal HTTP, OilPriceAPI and Polymarket cache. Official probe: UN News/Press OK, NATO public pages OK, OCHA oPt OK, EIA RSS OK, IAEA news/press 403, OPEC 403.
- Energy/markets: deploy OilPriceAPI Brent **$72.75**, WTI **$70.44**, gold **$4016.06**. Hormuz headlines show route pressure/reduced traffic and risk premium, but Brent/WTI still reject full stoppage. Polymarket refreshed `2026-06-29T21:08:42Z`; mapped markets remain horizon-mismatched sanity flags, worst `russia_ukraine` about **97.46pp**.
- Auto-detection: no tracker added. Emerging fallback for Thailand-Cambodia/Ethiopia-Eritrea/Guyana-Venezuela/Kosovo-Serbia returned zero qualifying fresh items or remained below nuclear/alliance-spillover scope.
- Cleanup: first 21Z deploy canonical check caught noncanonical `pakistan_afghanistan:ground_invasion_talk` caused by broad note keyword matching of “ground operation” wording. Neutralized the wording, removed the invalid active signal, redeployed successfully as `d10167f`. Final canonical check clean.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean before memory logging.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction/mining, escort incidents, traffic collapse, insurer/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, monitoring reversal, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: framework implementation/collapse, Hezbollah retaliation, IDF escalation, multi-front spillover.
- India-Pakistan: Poonch/LoC drone or infiltration incidents becoming sustained cross-border fire or force movement.
- Pakistan-Afghanistan: follow-up strikes, confirmed regular-force movement, Kunar/Asadabad/TTP cross-border evidence, Kabul/Islamabad attribution hardening, additional military-base attacks, or Taliban retaliation execution.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, atrocity evidence.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: older firing-event context expired; watch for fresh strategic-system/DMZ/device evidence.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write `data/current_state.json` atomically, then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, `nuclear weapon/capability`, `ground operation`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
