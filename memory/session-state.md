# Nuke Watch Session State

Updated: 2026-06-20T09:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `17caa52` (`Update 2026-06-20T09:05:25Z — automated`).
- Final deployed dashboard: **59% / imminent**; raw global in state: **55.74%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 96, `israel_palestine` 87, `sudan` 51, `russia` 50, `iran_nuclear` 43, `iran_conventional` 28.
- Main mover vs prior deployed state: `israel_lebanon` raw 92→94 on fresh Reuters/BBC/CNBC/France 24/BBC-style strike-after-ceasefire reporting; final remains capped at 100 after coupling and global stays 59.
- Signal hygiene: canonical-only clean. No new canonical signal promoted. Maintained `iran_nuclear:iaea_emergency`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `pakistan_afghanistan:military_buildup`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`. No non-canonical signals used.
- Source caveat: `web_search`/Tavily attempted first and failed HTTP 432; fallback used Google News RSS, terminal HTTP/direct-source probes, UN/NATO/EIA/OilPriceAPI/Polymarket. IAEA/OPEC direct pages blocked 403; Reuters world direct probe blocked/401. Public state is sanitized by pipeline.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $80.38, WTI $76.51, gas $3.00, gold $4156.56); Polymarket cache refreshed at `2026-06-20T09:05:52Z`, worst mapped divergence `israel_lebanon` ~99.4pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON files valid; canonical active-signal check clean; deploy/push succeeded; git status clean.

## Recent dashboard repair
- Issue: Intel Brief `Source caveat` exposed internal Tavily/web_search HTTP/provider errors to viewers.
- Fix deployed: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard UI renders `publicSourceCaveat(STATE._meta)`.
- Verification: smoke tests, local pipeline, inline JS, browser/Public Pages checks passed. Fix commits: `cdec2d2`, cleanup `ea376f8`.

## Watch next
- Israel-Lebanon: any confirmed additional strikes/fatalities after the renewed ceasefire, or collapse of the restoration channel.
- Iran/Hormuz: verified closure/mining/zero-traffic, war-risk insurance shock, or Gulf sabotage/cell attacks; stronger current flow-status sources say open/resumed/reopening/easing.
- Iran/IAEA: official agency access restoration vs monitoring-denial breakpoint; current reporting is conflicting and direct IAEA pages are blocked from host.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, or force movement after contested Taliban/Pakistan claims.
- Sudan/El Obeid: whether UN/OHCHR warnings turn into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
