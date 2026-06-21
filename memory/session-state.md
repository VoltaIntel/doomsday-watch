# Nuke Watch Session State

Updated: 2026-06-21T15:12:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `f308313` (`Update 2026-06-21T15:06:07Z — automated`).
- Final deployed dashboard: **62% / imminent**; raw global in state: **61.98%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 98, `israel_palestine` 88, `sudan` 51, `russia` 50, `iran_nuclear` 48, `iran_conventional` 40.
- Main movement vs 12:04Z: no numeric probability changes. Qualitative reinforcement: Hormuz closure claims strengthened in public feeds (NYT/WaPo/DW/CNBC/TOI) but US/open-flow/shipping contradiction blocked upgrade; Sudan/El Obeid atrocity-risk warning refreshed via UN/UNSC and regional feeds; Pakistan-Afghanistan strike claims were broader but still no new configured signal; Israel-Lebanon remains truce-breach/strike pressure.
- Signal hygiene: canonical-only clean. No new canonical signal promoted. Maintained `iran_nuclear:diplomacy_active/iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_closed`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `pakistan_afghanistan:military_buildup`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`.
- Source caveat: `web_search` failed HTTP 432 for required zone queries; fallback used Google News RSS, targeted 7d/30d RSS crosschecks, UN News/UN Press, EIA RSS, OilPriceAPI, Polymarket Gamma/cache, and terminal HTTP probes. Direct IAEA/OPEC returned 403; NATO XML returned 404. Public `_meta` sanitized to the standard fallback caveat.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $80.38, WTI $76.54, gasoline $3.00, diesel $3.19, gold $4156.56); Polymarket cache refreshed at `2026-06-21T15:06:39Z`; worst mapped divergence `israel_lebanon` ~99.3pp; DPRK aligned.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical active-signal check clean; deploy/push succeeded.

## Recent dashboard repair
- Issue: Intel Brief `Source caveat` exposed internal Tavily/web_search HTTP/provider errors to viewers.
- Fix deployed: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard UI renders `publicSourceCaveat(STATE._meta)`.
- Verification: smoke tests, local pipeline, inline JS, browser/Public Pages checks passed. Fix commits: `cdec2d2`, cleanup `ea376f8`.

## Watch next
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit waterway obstruction, naval escort incidents, or official reversal/denial of the closure claim.
- Israel-Lebanon: additional confirmed strikes/fatalities after the ceasefire arrangement, Hezbollah retaliation, or collapse of the restoration channel.
- Iran/IAEA: official access restoration vs monitoring-denial breakpoint; current reporting remains mixed between talks/technical work and site-access dispute.
- Russia-Ukraine/Russia-NATO: whether warned strike wave materializes; any NATO direct-entry, Article 5, allied combat-role decision, or verified Russia-NATO kinetic incident.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, Pakistani retaliation, or verified Taliban/IEA force movement after contested outpost reports.
- DPRK: corroborated South Korean/Japanese/US official confirmation of fresh strategic projectile activity; single-source/commentary items were not enough this run.
- Israel-Palestine: East Jerusalem/holy-site clashes, West Bank settler-attack cycles, or Gaza crisis moves that broaden into multi-front violence.
- Sudan/El Obeid: whether UN/OHCHR warnings turn into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
