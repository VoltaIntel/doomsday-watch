# Nuke Watch Session State

Updated: 2026-06-21T03:09:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `bbe96f2` (`Update 2026-06-21T03:05:09Z — automated`).
- Final deployed dashboard: **62% / imminent**; raw global in state: **61.98%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 98, `israel_palestine` 88, `sudan` 51, `russia` 50, `iran_nuclear` 48, `iran_conventional` 40.
- Main movement vs 00:07Z: no numeric probability changes. Qualitative pressure persisted in Israel-Lebanon strike/casualty reporting, renewed Hormuz closure claims with traffic-flow contradiction, Russia-Ukraine/Russia warning rhetoric, Pakistan-Afghanistan outpost claims, and Sudan/El Obeid warnings.
- Signal hygiene: canonical-only clean. No new canonical signal promoted. Maintained `iran_nuclear:diplomacy_active/iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_closed`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `pakistan_afghanistan:military_buildup`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`. DPRK projectile reporting was not promoted due thin fresh corroboration.
- Source caveat: `web_search` and `web_extract` failed HTTP 432; fallback used Google News RSS 24h scans, 7d/30d sparse-zone crosschecks, terminal HTTP official/source probes, UN/NATO/EIA/OilPriceAPI/Polymarket. IAEA/OPEC direct pages returned 403; Reuters world returned 401/forbidden.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $80.38, WTI $76.51, gasoline $3.00, diesel $3.19, gold $4156.56); Polymarket cache refreshed at `2026-06-21T03:05:33Z`, worst mapped divergence `israel_lebanon` ~99.4pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON files valid; canonical active-signal check clean; deploy/push succeeded; git status clean before memory logging.

## Recent dashboard repair
- Issue: Intel Brief `Source caveat` exposed internal Tavily/web_search HTTP/provider errors to viewers.
- Fix deployed: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard UI renders `publicSourceCaveat(STATE._meta)`.
- Verification: smoke tests, local pipeline, inline JS, browser/Public Pages checks passed. Fix commits: `cdec2d2`, cleanup `ea376f8`.

## Watch next
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit mine/obstruction reports, naval escort incidents, or reversal/denial of the closure claim.
- Israel-Lebanon: additional confirmed strikes/fatalities after the ceasefire arrangement, Hezbollah retaliation, or collapse of the restoration channel.
- Iran/IAEA: official access restoration vs monitoring-denial breakpoint; current reporting remains mixed between access-restoration/talks and site-access dispute.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, Pakistani retaliation, or verified Taliban/IEA force movement after contested outpost reports.
- DPRK: corroborated South Korean/Japanese/US official confirmation of fresh strategic projectile activity; single-source MSN-style items were not enough this run.
- Israel-Palestine: East Jerusalem land/seizure escalation, Al-Aqsa clashes, or West Bank settler-attack cycles that broaden into multi-front violence.
- Sudan/El Obeid: whether UN/OHCHR warnings turn into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
