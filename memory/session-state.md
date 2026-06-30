# Nuke Watch Session State

Updated: 2026-06-30T18:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 18Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Published state: **67% / imminent** (raw **67.40**).
- Deploy: succeeded via `bash scripts/deploy.sh`; final deploy commit `05e4528` (`Update 2026-06-30T18:06:39Z — automated`). Final git status clean.
- Mover vs 15Z: **no numeric probability moves**. Iran conventional remains raw **83** / coupled **90** after continued Hormuz restricted-corridor/tanker-slowdown reporting; Pakistan-Afghanistan remains **40 critical/rising**. Global stayed rounded **67/imminent**.
- Current coupled table: Russia-Ukraine **98**, Israel-Lebanon **94**, Iran War **90**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **50**, Iran Nuclear **46**, Pakistan-Afghanistan **40**, China-Taiwan **26**, India-Pakistan **11**, DPRK **10**, South Sudan/Abyei **8**, Turkey **5**.
- Active canonical signals after deploy: Iran conventional (`ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`); Israel-Lebanon (`ceasefire_violation`, `diplomacy_active`, `diplomacy_refused`); Pakistan-Afghanistan (`military_buildup`); Sudan (`military_buildup`). Canonical active-signal/timeline checks clean; no new signal names added.
- Source caveat: `web_search`/Tavily failed HTTP 432 on 10/10 initial required searches; fallback used Google News RSS for all trackers + oil/energy + IAEA/UN + NATO/allied + emerging, direct UN/NATO/EIA/IAEA/OPEC/OCHA probes, terminal HTTP, energy feed and Polymarket cache/deploy refresh. Source artifact: `data/morning_deep_scan_sources_20260630T180115Z.json`.
- Source counts: Iran nuclear 10, Iran conventional 10, Israel-Lebanon 10, Turkey 0, India 9, Russia 10, China 10, DPRK 10, Russia-Ukraine 10, Pakistan-Afghanistan 10, Sudan 9, Israel-Palestine 10, South Sudan/Abyei 0, oil/energy 10, IAEA/UN 10, NATO/allied 10, emerging 0.
- Energy/markets: latest deploy refresh showed Brent **$72.98**, WTI **$69.70**, gas **$3.28**, gold **$4030.01**. Hormuz/tanker-risk remains visible, but price/flow reports still reject full-waterway-halt pricing. Polymarket refreshed `2026-06-30T18:07:20Z`; mapped markets remain horizon-mismatched sanity flags, worst `russia_ukraine` about **97.5pp**.
- Auto-detection: no tracker added. Emerging fallback for Thailand-Cambodia/Ethiopia-Eritrea/Guyana-Venezuela/Kosovo-Serbia returned zero qualifying fresh items.
- DPRK: late-week weapons-drill/naval-posture coverage treated watch-only in the 24h pass; no `north_korea` canonical signal promoted.
- Verification: JSON valid; zones/trackers signal lists synced; canonical signal/timeline check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; latest commit `05e4528`.

## Watch next
- Iran/Hormuz: restricted corridors becoming sustained traffic collapse, waterway obstruction/mining, ship strikes, escort incidents, insurer/charterer suspensions, oil shock, or U.S./Iran retaliation loop broadening.
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
