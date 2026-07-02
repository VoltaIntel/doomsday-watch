# Session State

Last update: 2026-07-02T09:10:00Z

DoomsdayWatch 09Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published state: **68% / imminent** (raw **67.82**). Deploy succeeded via `bash scripts/deploy.sh`; automated deploy commit `d0640b7 Update 2026-07-02T09:08:22Z — automated` pushed, followed by metadata alignment commit `c0ad6c1 Fix 09Z post-deploy metadata` pushed. Deploy verification passed.
- Numeric movers vs 06Z: **none**. Israel-Lebanon remains the hottest non-Ukraine coupled lane at **96 final**; Pakistan-Afghanistan remains the main non-Mideast rising lane at **44 critical**; Iran conventional remains **90 final** with Hormuz control/traffic-risk but no full-waterway halt.
- Coupled table: Russia-Ukraine **98**, Israel-Lebanon **96**, Iran War **90**, Israel-Palestine **88**, Sudan **86**, Russia-NATO **50**, Iran Nuclear **46**, Pakistan-Afghanistan **44**, China-Taiwan **26**, India-Pakistan **11**, DPRK **10**, South Sudan/Abyei **8**, Turkey **5**.
- Active canonical signals: Iran conventional (`ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`); Israel-Lebanon (`ceasefire_violation`, `diplomacy_active`, `diplomacy_refused`); Pakistan-Afghanistan (`military_buildup`); Sudan (`military_buildup`); Israel-Palestine (`ceasefire_violation`). Canonical-signal audit clean: no noncanonical/legacy active signals.
- Source mode: `web_search` attempted for all 17 required tracker/sector groups and returned results, but recall was uneven/stale; fallback collector succeeded via Google News RSS and direct UN/NATO/EIA/IAEA/OPEC/OCHA probes. Source artifact `data/morning_deep_scan_sources_20260702T090140Z.json`.
- Fallback counts: Iran nuclear 10, Iran conventional 10, Israel-Lebanon 10, Turkey 0, India 7, Russia 10, China 10, DPRK 10, Russia-Ukraine 4, Pakistan-Afghanistan 10, Sudan 7, Israel-Palestine 9, South Sudan/Abyei 0, oil/energy 10, IAEA/UN 10, NATO/allied 10, emerging 0.
- Energy/markets after deploy: Brent **$70.81**, WTI **$67.83**, gas **$3.17**, gold **$4074.26**; Hormuz/tanker-risk remains visible but price/traffic-recovery evidence rejects full-waterway-halt thresholds. Polymarket refreshed `2026-07-02T09:09:19Z`; mapped markets remain horizon-mismatched sanity checks; worst divergence `russia_ukraine` **97.44pp**.
- Auto-detection: no untracked nuclear-escalation/alliance-spillover tracker added; emerging fallback returned zero qualifying fresh items.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; git clean after push.
