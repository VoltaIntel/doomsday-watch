# Nuke Watch Session State

Updated: 2026-06-22T18:09:07Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `4b34ee3` (`Update 2026-06-22T18:08:22Z — automated`).
- Final deployed dashboard: **61% / imminent**; raw global in state: **58.05%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 94, `israel_palestine` 84, `sudan` 55, `russia` 50, `iran_nuclear` 42, `iran_conventional` 40.
- Main movement vs 15:08Z: global held **61%**; Iran War final eased **42→40** as Reuters/Bloomberg/Insurance Journal showed Hormuz traffic picking up; Israel-Palestine eased **86→84** after stale Jerusalem-specific `holy_site_tension` aged out; Iran Nuclear stayed 42 but monitor-return claim is now disputed.
- Signal hygiene: canonical-only clean. Refreshed `iran_conventional:hormuz_controlled_not_closed` and `sudan:military_buildup`; maintained `iran_nuclear:diplomacy_active/iaea_emergency`, `israel_lebanon:ceasefire_violation/diplomacy_active`, and `pakistan_afghanistan:military_buildup/diplomacy_active`. Removed `israel_palestine:holy_site_tension`; no DPRK signal promoted from launcher-system reporting.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 required zone/topic queries; fallback used direct Google News RSS, UN News/NATO public-site probes, local OilPriceAPI energy refresh, and Polymarket Gamma/cache. IAEA/OPEC direct pages returned 403; UN Press returned client challenge.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $77.45, WTI $73.34, gold $4182.66); Polymarket cache refreshed at `2026-06-22T18:09:07Z`; worst mapped divergence remains `israel_lebanon` ~99.3pp.
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical active-signal check clean; deploy/push succeeded.

## Previous important state
- 12:06Z run deployed commit `209fe3c`; dashboard **63% / imminent**; later 15:08Z run had **61% / imminent** after Iran/Hormuz and Israel-Palestine easing.
- Intel Brief source-caveat repair remains in place: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard renders public-safe caveat.

## Watch next
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit waterway obstruction, naval escort incidents, or official reversal/denial of the waterway-closure claim.
- Iran/IAEA: official access restoration vs monitoring-denial breakpoint; current reporting is mixed between U.S. claims and Iranian contradiction.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or collapse of restoration channel.
- Russia-Ukraine/Russia-NATO: NATO direct-entry, Article 5, allied combat-role decision, or verified Russia-NATO kinetic incident.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, Pakistani retaliation, or verified Taliban/IEA force movement after contested claims.
- DPRK: corroborated South Korean/Japanese/US official confirmation of fresh strategic projectile activity; launcher-system items alone are not enough.
- India-Pakistan: whether Indus Waters threat rhetoric turns into force movement or cross-border incident.
- Israel-Palestine: East Jerusalem/holy-site clashes, West Bank settler-attack cycles, or Gaza crisis moves that broaden into multi-front violence.
- Sudan/El Obeid: whether warning/mobilisation reporting turns into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
