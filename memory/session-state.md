# Session State

Last update: 2026-07-07T00:10Z

DoomsdayWatch 00Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published state: **69% / imminent**. Required `bash scripts/deploy.sh` succeeded and pushed final commit `a29cd1e Update 2026-07-07T00:06:23Z — automated`.
- Numeric movers vs 21Z: **none**. Global remained **69 / imminent**. Iran War stayed **83 raw / 90 coupled**; Israel-Lebanon **88 raw / 98 coupled**; Russia-NATO **42 raw / 52 coupled**; Iran Nuclear **41 raw / 48 coupled**; DPRK **16**; China-Taiwan **24 raw / 27 coupled**.
- Coupled table: Russia-Ukraine **98**, Israel-Lebanon **98**, Iran War **90**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **52**, Iran Nuclear **48**, Pakistan-Afghanistan **44**, China-Taiwan **27**, DPRK **16**, India-Pakistan **11**, South Sudan/Abyei **8**, Turkey **5**.
- Active canonical signals after deploy: Iran conventional (`hormuz_controlled_not_closed`); Israel-Lebanon (`ceasefire_violation`); North Korea (`missile_range_test`); Pakistan-Afghanistan (`military_buildup`); Iran Nuclear (`iaea_access_denied`); Sudan (`military_buildup`); Israel-Palestine (`ceasefire_violation`). Canonical guard clean; no legacy/noncanonical active signals.
- Source mode: `web_search` attempted all required tracker/sector groups and returned, but recall was uneven/stale/noisy in several lanes. Fallback/corroboration artifact: `data/morning_deep_scan_sources_20260707T000219Z.json` using Google News RSS plus direct UN/NATO/EIA/IAEA/OPEC/OCHA probes. UN Press, NATO pages and EIA RSS reachable; direct IAEA/OPEC and configured OCHA/UN Sudan/OCHA OPT feeds unavailable from this node; UN News RSS returned 200 but parser extracted no items.
- RSS counts: Iran nuclear 10, Iran conventional 10, Israel-Lebanon 10, Turkey 8, India 2, Russia 10, China 8, DPRK 10, Russia-Ukraine 10, Pakistan-Afghanistan 10, Sudan 10, Israel-Palestine 10, South Sudan/Abyei 2, oil/energy 10, IAEA/UN 10, NATO/allied 10, emerging 0.
- Energy/markets after final deploy: Brent **$72.01**, WTI **$68.76**, gasoline **$3.00**, natural gas **$3.25**, gold **$4155.55**. Polymarket mapped-cache refreshed during deploy at **2026-07-07T00:07:02Z**; sanity-only due horizon mismatch. Key raw mapped prices: US invades Iran **0.115**, Iran Nuke **0.0435**, Iran device-test **0.045**, NPT withdrawal **0.091**, NATO Article 5 **0.085**, China/Taiwan clash **0.0615**, China invasion **0.0375**, North Korea invades South Korea **0.0335**.
- Auto-detection: no untracked nuclear-escalation/alliance-spillover tracker added. Emerging RSS returned zero qualifying fresh items. A July 6 Abyei “54 killed” RSS item was rejected as stale/recycled because cross-checks matched Jan 2024 UN/BBC/Reuters language and lacked fresh official corroboration.
- Verification: JSON valid; active signal list canonical; `index.html` markers present (`DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`); deploy and push succeeded.
