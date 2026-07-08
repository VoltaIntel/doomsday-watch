# Session State

Last update: 2026-07-08T06:10Z

DoomsdayWatch 06Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published state: **70% / imminent**. Required `bash scripts/deploy.sh` succeeded after one cleanup/redeploy pass; final publish commit `b48d03c Update 2026-07-08T06:08:03Z — automated` pushed.
- Numeric movers vs 03Z: **none**. Global remained **70 / imminent**. Iran War **88 raw / 96 coupled**; Israel-Lebanon **88 raw / 98 coupled**; Russia-NATO **42 raw / 52 coupled**; Iran Nuclear **41 raw / 48 coupled**; Pakistan-Afghanistan **46**; Sudan **88**.
- Coupled table: Russia-Ukraine **98**, Israel-Lebanon **98**, Iran War **96**, Israel-Palestine **88**, Sudan **88**, Russia-NATO **52**, Iran Nuclear **48**, Pakistan-Afghanistan **46**, China-Taiwan **27**, DPRK **16**, India-Pakistan **11**, South Sudan/Abyei **8**, Turkey **5**.
- Signals changed: cleared unsupported `diplomacy_active` from Iran conventional, Israel-Lebanon and Israel-Palestine; deploy then exposed a broad-keyword false positive `pakistan_afghanistan:ground_invasion_talk`, which was removed and wording neutralized before final redeploy. Final canonical guard clean: no noncanonical/legacy active signals.
- Active canonical signals after final deploy: Iran conventional (`ceasefire_violation`, `hormuz_controlled_not_closed`); Israel-Lebanon (`ceasefire_violation`); DPRK (`missile_range_test`); Pakistan-Afghanistan (`military_buildup`); Iran Nuclear (`iaea_access_denied`); Sudan (`military_buildup`); Israel-Palestine (`ceasefire_violation`).
- Source mode: `web_search` attempted and returned for required tracker/sector groups, but recall was uneven/stale in several lanes. Fallback/corroboration artifact: `data/morning_deep_scan_sources_20260708T060209Z.json` using Google News RSS plus direct UN/NATO/EIA/IAEA/OPEC/OCHA probes. UN News/Press, NATO pages and EIA RSS reachable; direct IAEA/OPEC and configured OCHA/UN Sudan/OCHA OPT feeds unavailable from this node.
- RSS counts: Iran nuclear 10, Iran conventional 10, Israel-Lebanon 10, Turkey 8, India 4, Russia 10, China 8, DPRK 10, Russia-Ukraine 10, Pakistan-Afghanistan 10, Sudan 10, Israel-Palestine 10, South Sudan/Abyei 1, oil/energy 10, IAEA/UN 10, NATO/allied 10, emerging 0.
- Energy/markets from final deploy output/cache: Brent **$76.64**, WTI **$72.83**, gasoline **$2.99**, natural gas **$3.28**, gold **$4133.21**. Polymarket cache refreshed at **2026-07-08T06:08:42Z**: US invades Iran **13.5%**, Iran Nuke **5.15%**, Iran device-test **4.5%**, NATO Article 5 **6.5%**, China-Taiwan clash **4.35%**, China invasion **3.85%**. Divergence banner expected due DW 24h escalation/intensity vs sparse end-2026 market horizons.
- Auto-detection: no untracked nuclear-escalation/alliance-spillover tracker added. Emerging RSS returned zero qualifying fresh items. South Sudan/Abyei “54 killed” item remains single-source/watch-only pending official corroboration.
- Verification: JSON valid; active signal list canonical; `index.html` markers present (`DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`); deploy/pipeline commit and push succeeded.
