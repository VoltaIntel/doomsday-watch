# Nuke Watch Session State

Updated: 2026-06-30T00:12:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 00Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Published state: **67% / imminent** (raw **67.22**).
- Deploy: succeeded, latest deploy commit `e4a4a4a` (`Update 2026-06-30T00:07:30Z — automated`).
- Mover vs 21Z: **Pakistan-Afghanistan raw/coupled 36→40** after Al Jazeera/PBS/ABC/KabulNow/Los Angeles Times/France24 corroborated Pakistani cross-border actions, civilian casualty claims and Taliban retaliation language. Global stayed rounded at **67**. Other numeric lanes unchanged.
- Current coupled table: Russia-Ukraine **98**, Israel-Lebanon **94**, Iran War **90**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **50**, Iran Nuclear **46**, Pakistan-Afghanistan **40**, China-Taiwan **26**, India-Pakistan **11**, DPRK **10**, South Sudan/Abyei **8**, Turkey **5**.
- Active canonical signals after deploy: Iran conventional (`ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `military_buildup`); Israel-Lebanon (`ceasefire_violation`, `diplomacy_active`, `diplomacy_refused`); Pakistan-Afghanistan (`military_buildup`); Sudan (`military_buildup`). Canonical active-signal check clean.
- Source caveat: `web_search`/Tavily failed HTTP 432 on required searches; fallback used Google News RSS for all trackers + oil/energy + IAEA/UN + NATO/allied + emerging, direct UN/NATO/OCHA/EIA/IAEA/OPEC probes, terminal HTTP, Yahoo/OilPrice local energy feed, and Polymarket cache. Official probe: UN News/Press OK, NATO public pages OK, OCHA oPt OK, EIA RSS OK, IAEA news/press 403, OPEC 403.
- Energy/markets: deploy refreshed Yahoo energy feed: Brent **$73.51**, WTI **$70.16**, gas **$3.176**, gold **$4028.50**. Hormuz/tanker-hit headlines are live, but Reuters/loading and oil-pricing context still reject full-waterway-stoppage pricing. Polymarket refreshed `2026-06-30T00:08:09Z`; mapped markets remain horizon-mismatched sanity flags, worst `russia_ukraine` about **97.5pp**.
- Auto-detection: no tracker added. Emerging fallback for Thailand-Cambodia/Ethiopia-Eritrea/Guyana-Venezuela/Kosovo-Serbia returned zero qualifying fresh items.
- DPRK: DD News surfaced a fresh-indexed ballistic-firing headline, but exact-title crosscheck pointed to older Reuters/Straits Times reporting; treated watch-only and no `north_korea:missile_range_test` was promoted.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction/mining, escort incidents, traffic collapse, insurer/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, monitoring reversal, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: framework implementation/collapse, Hezbollah retaliation, IDF escalation, multi-front spillover.
- India-Pakistan: Poonch/LoC drone or infiltration incidents becoming sustained cross-border fire or force movement.
- Pakistan-Afghanistan: follow-up strikes, confirmed regular-force movement, Kunar/Asadabad/TTP cross-border evidence, Kabul/Islamabad attribution hardening, additional military-base attacks, or Taliban retaliation execution.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, atrocity evidence.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: treat fresh-indexed recycled headlines carefully; promote only corroborated fresh strategic-system/DMZ/device evidence.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write `data/current_state.json` atomically, then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, `nuclear weapon/capability`, `ground operation`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
