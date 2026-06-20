# Nuke Watch Session State

Updated: 2026-06-20T08:10:40Z

## Latest dashboard repair
- Issue: Intel Brief `Source caveat` exposed internal Tavily/web_search HTTP/provider errors to viewers.
- Fix: patched `scripts/pipeline.py` to sanitize public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe` before publishing `data/current_state.json`; patched `dashboard.html`/`index-redesign.html` to render `publicSourceCaveat(STATE._meta)` instead of raw metadata.
- Verification: `pytest tests/test_pipeline_smoke.py -q` passed (11 tests); `NUKE_WATCH_AUTO_GIT=0 python3 scripts/pipeline.py` succeeded; inline JS `node --check` succeeded; local browser Intel Brief showed no Tavily/HTTP/internal error strings; public GitHub Pages `index.html` and `data/current_state.json` verified cache-busted clean.
- Deploy: fix deployed in commit `cdec2d2`; cleanup commit `ea376f8` reverted a pytest bytecode artifact. Pages run `27865209186` completed success.

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `befdadd` (`Update 2026-06-20T03:06:40Z — automated`).
- Final deployed dashboard: **59% / imminent**; raw global in state: **55.3%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 94, `israel_palestine` 87, `sudan` 51, `russia` 50, `iran_nuclear` 43, `iran_conventional` 28.
- Main movers vs 00:09Z deployed state: **none numerically**. Qualitative shift: Israel-Lebanon and Hormuz feeds leaned more ceasefire/open-strait, but residual risk stayed high; global stayed 59.
- Signal hygiene: canonical-only clean. Deploy decay cleared expired `iran_conventional:hormuz_controlled_not_closed`; maintained `iran_nuclear:iaea_emergency`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `pakistan_afghanistan:military_buildup`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`. No non-canonical signals used.
- Source caveat: `web_search`/Tavily unavailable with HTTP 432; used Google News RSS, terminal HTTP/direct-source probes, UN/NATO/EIA/OilPriceAPI/Polymarket fallbacks. IAEA/OPEC direct pages blocked 403; Reuters world direct probe blocked/401.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $80.38, WTI $76.51, gas $3.00, gold $4156.56); Polymarket cache refreshed at `2026-06-20T03:07:19Z`, worst mapped divergence `israel_lebanon` ~99.4pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON files valid; deploy/push succeeded. Memory files were updated after deploy.

## Watch next
- Israel-Lebanon: whether the renewed halt holds; any confirmed strikes despite the halt re-raise the active truce-breach lane.
- Iran/Hormuz: verified closure/mining/zero-traffic, or Gulf-state covert-cell attacks; current stronger sources say open/resumed.
- Iran/IAEA: any official agency access restoration vs sanctions snapback or monitoring-denial breakpoint.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, or force movement after contested Taliban/Pakistan claims.
- Sudan/El Obeid: whether UN/OHCHR warnings turn into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
