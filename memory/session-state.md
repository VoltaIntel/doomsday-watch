# Nuke Watch Session State

Updated: 2026-06-29T00:10Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 00Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Published state: **66% / imminent** (raw **66.38**).
- Deploy: succeeded after false-positive cleanup redeploy, commit `58de30f` (`Update 2026-06-29T00:07:47Z — automated`). A first deploy produced commit `6b43717`, then the cleanup redeploy neutralized an invalid DPRK note-trigger.
- Movers vs 21Z: global unchanged at 66. Iran conventional **90→92** coupled on renewed U.S.-Iran strike / tanker-Hormuz route-pressure reporting. Pakistan-Afghanistan **23→25** and **elevated→critical** after force-formation + Karachi military-base attack coverage restored canonical `military_buildup`.
- Current coupled table: Russia-Ukraine **98**, Israel-Lebanon **94**, Iran War **92**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **50**, Iran Nuclear **46**, China-Taiwan **26**, Pakistan-Afghanistan **25**, India-Pakistan **11**, DPRK **10**, South Sudan/Abyei **8**, Turkey **5**.
- Active canonical signals after deploy: Iran conventional (`ceasefire_violation`, `hormuz_controlled_not_closed`, `military_buildup`); Israel-Lebanon (`ceasefire_violation`, `diplomacy_active`, `diplomacy_refused`); Pakistan-Afghanistan (`military_buildup`); Iran Nuclear (`diplomacy_active`); DPRK (`missile_range_test`); Sudan (`infrastructure_strike`, `military_buildup`); Israel-Palestine (`ceasefire_violation`). Canonical active-signal check clean.
- Source caveat: `web_search`/Tavily failed HTTP 432 on required searches; fallback used Google News RSS for all trackers + oil/energy + IAEA/UN + NATO/allied + emerging, direct UN/NATO/EIA/IAEA/OPEC probes, terminal HTTP, OilPriceAPI and Polymarket cache. Official probe: UN News/Press OK, NATO news/press OK, EIA RSS OK, IAEA news/press 403, OPEC 403. Sparse/low-credibility lanes treated as caveats unless corroborated.
- Energy/markets: OilPriceAPI Brent **$72.19**, WTI **$69.73**, gold **$4063.61**. Energy headlines show renewed war premium but traffic/crossings through Hormuz still visible, rejecting full stoppage. Polymarket refreshed `2026-06-29T00:08:31Z`; divergences remain horizon-mismatch sanity flags, worst `russia_ukraine` **97.46pp**.
- Auto-detection: no tracker added. Thailand-Cambodia remains watch-only; Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia below nuclear/alliance-spillover scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean.

## Watch next
- Iran/Hormuz: repeated ship strikes, waterway obstruction/mining, escort incidents, traffic collapse, insurer/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
- Iran/agency verification: actual site visit execution, monitoring reversal, verified higher-level enrichment, underground restart, device event.
- Israel-Lebanon: truce/framework collapse, Hezbollah retaliation, IDF escalation, multi-front spillover.
- Pakistan-Afghanistan: border force movement, Kunar/Asadabad/TTP cross-border evidence, Kabul/Islamabad attribution hardening, or additional military-base attacks.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, atrocity evidence.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- DPRK: prior firing-event signal expiry vs fresh strategic-system/DMZ/device evidence.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write `data/current_state.json` atomically, then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, `bomber`, `nuclear weapon/capability`, etc.) unless intentionally activating a canonical signal that exists for that tracker.
