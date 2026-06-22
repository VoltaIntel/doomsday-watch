# Nuke Watch Session State

Updated: 2026-06-22T06:14:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `95687f2` (`Update 2026-06-22T06:07:42Z — automated`).
- Final deployed dashboard: **63% / imminent**; raw global in state: **63.33%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 98, `israel_palestine` 88, `sudan` 55, `russia` 50, `iran_nuclear` 48, `iran_conventional` 46.
- Main movement vs 03:05Z: **no numeric probability changes**. Qualitative reinforcement: Hormuz shipping-stall reports persisted, Sudan/El Obeid atrocity-risk warning remained strong, India-Pakistan Indus rhetoric broadened, and Pakistan-Afghanistan border casualty claims stayed visible.
- Signal hygiene: canonical-only clean after cleanup/redeploy. No new configured signal promoted. Maintained `iran_nuclear:diplomacy_active/iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_closed`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`. `pakistan_afghanistan:military_buildup` decayed out under the configured 72h rule. Removed transient false positives `china:nuclear_rhetoric_official` and `israel_palestine:diplomacy_active` caused by note keywords, then redeployed.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all required zone queries; fallback used Google News RSS, UN News/UN Press RSS, NATO/EIA terminal HTTP probes, public energy headlines, OilPriceAPI, and Polymarket Gamma/cache. IAEA/OPEC direct pages returned 403; NATO XML returned 404. Public `_meta` sanitized by pipeline.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $78.97, WTI $75.19, gasoline $2.95, diesel $3.14, gold $4194.51); Polymarket cache refreshed at `2026-06-22T06:08:15Z`; worst mapped divergence remains `israel_lebanon` ~99.3pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical active-signal check clean; `pytest tests/test_pipeline_smoke.py -q` passed 11/11; deploy/push succeeded; git status clean.

## Recent dashboard repair
- Issue: Intel Brief `Source caveat` exposed internal Tavily/web_search HTTP/provider errors to viewers.
- Fix deployed: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard UI renders `publicSourceCaveat(STATE._meta)`.
- Verification: smoke tests, local pipeline, inline JS, browser/Public Pages checks passed. Fix commits: `cdec2d2`, cleanup `ea376f8`.

## Watch next
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit waterway obstruction, naval escort incidents, or official reversal/denial of the shut-waterway claim.
- Israel-Lebanon: additional confirmed strikes/fatalities after the truce arrangement, Hezbollah retaliation, or collapse of the restoration channel.
- Iran/IAEA: official access restoration vs monitoring-denial breakpoint; current reporting remains mixed between talks/technical work and site-access dispute.
- Russia-Ukraine/Russia-NATO: any NATO direct-entry, Article 5, allied combat-role decision, or verified Russia-NATO kinetic incident.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, Pakistani retaliation, or verified Taliban/IEA force movement after contested casualty claims.
- DPRK: corroborated South Korean/Japanese/US official confirmation of fresh strategic projectile activity; single-source/commentary items were not enough this run.
- India-Pakistan: whether Indus Waters threat rhetoric turns into force movement or cross-border incident.
- Israel-Palestine: East Jerusalem/holy-site clashes, West Bank settler-attack cycles, or Gaza crisis moves that broaden into multi-front violence.
- Sudan/El Obeid: whether warning/mobilisation reporting turns into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
