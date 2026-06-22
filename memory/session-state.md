# Nuke Watch Session State

Updated: 2026-06-21T21:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `eed51ab` (`Update 2026-06-21T21:05:12Z — automated`).
- Final deployed dashboard: **62% / imminent**; raw global in state: **62.04%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 98, `israel_palestine` 88, `sudan` 53, `russia` 50, `iran_nuclear` 48, `iran_conventional` 40.
- Main movement vs 18:05Z: `sudan` 51→53 after fresh RSF/Al Obeid pressure; other configured trackers held steady. Hormuz remains mixed: shutdown claims persist, but Fortune/CNN open-flow reporting blocks zero-flow escalation. Israel-Lebanon remains ceiling pressure; Pakistan-Afghanistan remains near ceiling; China/DPRK/Turkey/India no-trigger reviews stayed below configured thresholds.
- Signal hygiene: canonical-only clean. No new canonical signal promoted. Maintained `iran_nuclear:diplomacy_active/iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_closed`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `pakistan_afghanistan:military_buildup`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`.
- Source caveat: `web_search` failed HTTP 432 for required zone queries; fallback used Google News RSS, direct official/source pages, UN Press/UN News/NATO/EIA probes, OilPriceAPI, Polymarket Gamma/cache. IAEA/OPEC returned 403. Public `_meta` sanitized to the standard fallback caveat.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $80.38, WTI $76.54, gasoline $3.00, diesel $3.19, gold $4156.56); Polymarket cache refreshed at `2026-06-21T21:05:56Z`; worst mapped divergence `israel_lebanon` ~99.3pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical active-signal check clean; deploy/push succeeded.

## Recent dashboard repair
- Issue: Intel Brief `Source caveat` exposed internal Tavily/web_search HTTP/provider errors to viewers.
- Fix deployed: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard UI renders `publicSourceCaveat(STATE._meta)`.
- Verification: smoke tests, local pipeline, inline JS, browser/Public Pages checks passed. Fix commits: `cdec2d2`, cleanup `ea376f8`.

## Watch next
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit waterway obstruction, naval escort incidents, or official reversal/denial of the closure claim.
- Israel-Lebanon: additional confirmed strikes/fatalities after the truce arrangement, Hezbollah retaliation, or collapse of the restoration channel.
- Iran/IAEA: official access restoration vs monitoring-denial breakpoint; current reporting remains mixed between talks/technical work and site-access dispute.
- Russia-Ukraine/Russia-NATO: any NATO direct-entry, Article 5, allied combat-role decision, or verified Russia-NATO kinetic incident.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, Pakistani retaliation, or verified Taliban/IEA force movement after contested strike reports.
- DPRK: corroborated South Korean/Japanese/US official confirmation of fresh strategic projectile activity; single-source/commentary items were not enough this run.
- Israel-Palestine: East Jerusalem/holy-site clashes, West Bank settler-attack cycles, or Gaza crisis moves that broaden into multi-front violence.
- Sudan/El Obeid: whether warning/mobilisation reporting turns into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
