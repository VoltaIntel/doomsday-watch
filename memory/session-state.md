# Nuke Watch Session State

Updated: 2026-06-28T21:10Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 21Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Published state: **66% / imminent** (raw **65.86**).
- Deploy: succeeded after correction redeploy, commit `1492492` (`Update 2026-06-28T21:08:37Z — automated`).
- Movers vs 18Z: global unchanged. Israel-Lebanon **92→94** coupled after renewed truce-breach / southern Lebanon strike reporting; Pakistan-Afghanistan **25→23** and drops **critical→elevated** after the older border force-posture signal was cleared for lack of fresh corroboration.
- Current coupled table: Russia-Ukraine **98**, Israel-Lebanon **94**, Iran War **90**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **50**, Iran Nuclear **46**, China-Taiwan **26**, Pakistan-Afghanistan **23**, India-Pakistan **11**, DPRK **10**, South Sudan/Abyei **8**, Turkey **5**.
- Active canonical signals after deploy: Iran conventional (`ceasefire_violation`, `hormuz_controlled_not_closed`, `military_buildup`); Israel-Lebanon (`ceasefire_violation`, `diplomacy_active`, `diplomacy_refused`); Iran Nuclear (`diplomacy_active`); DPRK (`missile_range_test`); Sudan (`infrastructure_strike`, `military_buildup`); Israel-Palestine (`ceasefire_violation`). Pakistan-Afghanistan and Russia-Ukraine now have no active configured signal.
- Source caveat: `web_search`/Tavily failed HTTP 432; fallback used Google News RSS for all trackers + oil/energy + IAEA/UN + NATO/allied + emerging, direct UN/NATO/IAEA/OPEC probes, terminal HTTP, OilPriceAPI and Polymarket cache. Official probe: UN News/Press OK, NATO news/press OK, IAEA news/press 403, OPEC 403. Sparse lanes contained stale/archival RSS items and were treated as caveats, not fresh triggers.
- Energy/markets: OilPriceAPI Brent **$73.08**, WTI **$69.23**, gold **$4080.83**. Energy headlines show route pressure but no full Hormuz stoppage. Polymarket refreshed `2026-06-28T21:09:16Z`; divergences remain horizon-mismatch sanity flags, worst `russia_ukraine` ~97.5pp.
- Auto-detection: no tracker added. Thailand-Cambodia remains watch-only; Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia below nuclear/alliance-spillover scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction/mining, escort incidents, traffic collapse, insurer/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, monitoring reversal, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: truce/framework collapse, Hezbollah retaliation, IDF escalation, multi-front spillover.
- Pakistan-Afghanistan: revive only on fresh Kunar/Asadabad/TTP border evidence; otherwise maintain elevated rather than critical.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, atrocity evidence.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: prior firing-event signal expiry vs fresh strategic-system/DMZ/device evidence.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write `data/current_state.json` atomically, then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
