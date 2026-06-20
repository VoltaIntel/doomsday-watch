# Nuke Watch Session State

Updated: 2026-06-20T18:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `c5f5e0f` (`Update 2026-06-20T18:06:35Z — automated`).
- Final deployed dashboard: **62% / imminent**; raw global in state: **62.29%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 97, `israel_palestine` 88, `sudan` 51, `iran_nuclear` 50, `russia` 50, `iran_conventional` 40.
- Main movers vs prior deployed state: `israel_lebanon` raw 97→98 on fresh continued-strike/violation reporting after ceasefire; `israel_palestine` raw 87→88 on East Jerusalem/West Bank/Al-Aqsa tension refresh. Global remained **62**. Iran conventional stayed raw 32 / coupled 40: fresh Hormuz closure headlines are still contradicted by traffic-recovery/open-waterway indicators, so no zero-flow or mine-laying signal was promoted.
- Signal hygiene: canonical-only clean. Maintained `iran_conventional:hormuz_closed`, `iran_nuclear:iaea_access_denied/iaea_emergency`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `pakistan_afghanistan:military_buildup`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`. No non-canonical signals used.
- Source caveat: `web_search`/Tavily attempted first and failed HTTP 432; fallback used Google News RSS, terminal HTTP/direct-source probes, UN/NATO/EIA/OilPriceAPI/Polymarket, and MarineTraffic landing-page reachability. IAEA/OPEC direct pages blocked 403; Reuters world direct probe blocked/401. Public state is sanitized by pipeline.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $80.38, WTI $76.51, gasoline $3.00, diesel $3.19, gold $4156.56); Polymarket cache refreshed at `2026-06-20T18:07:13Z`, worst mapped divergence `israel_lebanon` ~99.4pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON files valid; canonical active-signal check clean; deploy/push succeeded; git status was clean after deploy.

## Recent dashboard repair
- Issue: Intel Brief `Source caveat` exposed internal Tavily/web_search HTTP/provider errors to viewers.
- Fix deployed: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard UI renders `publicSourceCaveat(STATE._meta)`.
- Verification: smoke tests, local pipeline, inline JS, browser/Public Pages checks passed. Fix commits: `cdec2d2`, cleanup `ea376f8`.

## Watch next
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit mine/obstruction reports, naval escort incidents, or reversal/denial of the closure claim.
- Israel-Lebanon: additional confirmed strikes/fatalities after the renewed ceasefire, Hezbollah retaliation, or collapse of the restoration channel.
- Iran/IAEA: official agency access restoration vs monitoring-denial breakpoint; current reporting remains access-disputed and direct IAEA pages are blocked from host.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, or force movement after contested Taliban/Pakistan claims.
- Israel-Palestine: East Jerusalem land/seizure escalation, Al-Aqsa clashes, or West Bank settler-attack cycles that broaden into multi-front violence.
- Sudan/El Obeid: whether UN/OHCHR warnings turn into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
