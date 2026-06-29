# Nuke Watch Session State

Updated: 2026-06-29T09:12Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 09Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Published state: **66% / imminent** (raw **66.38**).
- Deploy: succeeded, latest commit `a6cb5fa` (`Update 2026-06-29T09:07:26Z — automated`).
- Movers vs 06Z: **no numeric probability changes**. Fresh evidence adds India/Poonch drone-intrusion watch, DPRK drill-denunciation context, Poland/Russia warning rhetoric, Israel-Lebanon southern-strike/right-to-defend messaging, Gaza/West Bank casualties, and continuing Iran/Hormuz risk with pause claims.
- Current coupled table: Russia-Ukraine **98**, Israel-Lebanon **94**, Iran War **92**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **50**, Iran Nuclear **46**, China-Taiwan **26**, Pakistan-Afghanistan **25**, India-Pakistan **11**, DPRK **10**, South Sudan/Abyei **8**, Turkey **5**.
- Active canonical signals after deploy: Iran conventional (`ceasefire_violation`, `hormuz_controlled_not_closed`, `military_buildup`); Israel-Lebanon (`ceasefire_violation`, `diplomacy_active`, `diplomacy_refused`); Pakistan-Afghanistan (`military_buildup`); Iran Nuclear (`diplomacy_active`); DPRK (`missile_range_test`); Sudan (`infrastructure_strike`, `military_buildup`). Israel-Palestine has no active signal after prior decay. Canonical active-signal check clean.
- Source caveat: `web_search`/Tavily failed HTTP 432 on all 17 required searches; fallback used Google News RSS for all trackers + oil/energy + IAEA/UN + NATO/allied + emerging, direct UN/NATO/EIA/IAEA/OPEC probes, terminal HTTP, OilPriceAPI and Polymarket cache. Official probe: UN News/Press OK, NATO news/press reachable, EIA RSS OK, IAEA news/press 403, OPEC 403. Sparse/low-credibility lanes treated as caveats unless corroborated.
- Energy/markets: deploy OilPriceAPI Brent **$72.44**, WTI **$70.11**, gold **$4056.15**. Hormuz headlines show route pressure/war premium and slower shipping, but visible flows reject full stoppage. Polymarket refreshed `2026-06-29T09:07:58Z`; divergences remain horizon-mismatch sanity flags, worst `russia_ukraine` **97.47pp**.
- Auto-detection: no tracker added. Thailand-Cambodia remains watch-only; Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia below nuclear/alliance-spillover scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction/mining, escort incidents, traffic collapse, insurer/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, monitoring reversal, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: framework implementation/collapse, Hezbollah retaliation, IDF escalation, multi-front spillover.
- India-Pakistan: Poonch/LoC drone or infiltration incidents becoming sustained cross-border fire or force movement.
- Pakistan-Afghanistan: border force movement, Kunar/Asadabad/TTP cross-border evidence, Kabul/Islamabad attribution hardening, or additional military-base attacks.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, atrocity evidence.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: prior firing-event signal expiry vs fresh strategic-system/DMZ/device evidence.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write `data/current_state.json` atomically, then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, `nuclear weapon/capability`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
