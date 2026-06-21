# Nuke Watch Session State

Updated: 2026-06-20T21:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `add10aa` (`Update 2026-06-20T21:05:45Z — automated`).
- Final deployed dashboard: **62% / imminent**; raw global in state: **61.98%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 98, `israel_palestine` 88, `sudan` 51, `russia` 50, `iran_nuclear` 48, `iran_conventional` 40.
- Main movers vs 18:10Z: `iran_nuclear` raw 42→40 / coupled 50→48 on renewed diplomacy/access reporting; `israel_lebanon` raw 98→99 on continued strikes and casualties despite ceasefire channel; `pakistan_afghanistan` raw 97→98 on contested outpost-capture/border-unit reporting. Global remained **62**.
- Signal hygiene: canonical-only clean. Added `iran_nuclear:diplomacy_active`; maintained `iran_conventional:hormuz_closed`, `iran_nuclear:iaea_access_denied/iaea_emergency`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `pakistan_afghanistan:military_buildup`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`. No non-canonical signals used. DPRK launch reports were not promoted due thin fresh corroboration.
- Source caveat: `web_search`/`web_extract` attempted first and failed HTTP 432; fallback used Google News RSS, terminal HTTP/direct-source probes, UN/NATO/EIA/OilPriceAPI/Polymarket, and MarineTraffic landing-page reachability. IAEA/OPEC direct pages blocked 403; Reuters world direct probe blocked/401. Public state is sanitized by pipeline.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $80.38, WTI $76.51, gasoline $3.00, diesel $3.19, gold $4156.56); Polymarket cache refreshed at `2026-06-20T21:06:10Z`, worst mapped divergence `israel_lebanon` ~99.4pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON files valid; canonical active-signal check clean; deploy/push succeeded.

## Recent dashboard repair
- Issue: Intel Brief `Source caveat` exposed internal Tavily/web_search HTTP/provider errors to viewers.
- Fix deployed: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard UI renders `publicSourceCaveat(STATE._meta)`.
- Verification: smoke tests, local pipeline, inline JS, browser/Public Pages checks passed. Fix commits: `cdec2d2`, cleanup `ea376f8`.

## Watch next
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit mine/obstruction reports, naval escort incidents, or reversal/denial of the closure claim.
- Israel-Lebanon: additional confirmed strikes/fatalities after the renewed ceasefire, Hezbollah retaliation, or collapse of the restoration channel.
- Iran/IAEA: official agency access restoration vs monitoring-denial breakpoint; current reporting is mixed between access-restoration claims and site-access dispute.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, Pakistani retaliation, or verified Taliban/IEA force movement after contested outpost/border-unit claims.
- DPRK: corroborated South Korean/Japanese/US official confirmation of fresh launches; single-source MSN/projectile items were not enough this run.
- Israel-Palestine: East Jerusalem land/seizure escalation, Al-Aqsa clashes, or West Bank settler-attack cycles that broaden into multi-front violence.
- Sudan/El Obeid: whether UN/OHCHR warnings turn into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
