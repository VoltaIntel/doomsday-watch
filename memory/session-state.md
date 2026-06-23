# Nuke Watch Session State

Updated: 2026-06-23T00:09:14Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `e95a8c9` (`Update 2026-06-23T00:08:36Z — automated`).
- Final deployed dashboard: **61% / imminent**; raw global in state: **57.94%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 94, `israel_palestine` 84, `sudan` 62, `russia` 50, `iran_nuclear` 42, `iran_conventional` 40.
- Main movement vs 21:05Z: global held **61%**; Sudan raw/final **60→62** after UN News El Obeid drone/critical-services report and Al Jazeera/U.S. RSF encirclement concern. Other numeric lanes held: Hormuz remains restricted/not zero-flow, Iran nuclear remains mixed with inspector-access claims disputed by Tehran, Lebanon remains near ceiling with fresh combat-breach reporting but truce framework not fully collapsed.
- Signal hygiene: canonical-only clean. Refreshed `israel_lebanon:ceasefire_violation`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `iran_conventional:hormuz_controlled_not_closed`, `pakistan_afghanistan:military_buildup/diplomacy_active`, and `iran_nuclear:diplomacy_active/iaea_emergency`. No DPRK, Turkey, China, India, Russia-NATO, Russia-Ukraine, Israel-Palestine, or Abyei canonical signal promoted.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 required zone/topic queries; fallback used Google News RSS, UN News/UN Press/NATO/EIA public-site probes, local OilPriceAPI energy refresh, and Polymarket Gamma/cache. IAEA news/press/RSS and OPEC direct pages returned 403.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $78.15, WTI $74.19, gold $4189.22); Polymarket cache refreshed at `2026-06-23T00:09:14Z`; mapped markets remain horizon-mismatched divergence checks only.
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical active-signal check clean; deploy/push succeeded; git status clean immediately after deploy.

## Previous important state
- 2026-06-22 21:05Z run deployed commit `b21522b`; dashboard **61% / imminent**, raw global **57.88%**, Sudan rose to 60 on El Obeid infrastructure/service disruption.
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
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only; if missing in worktree, restore tracked `data/tracker_config.json` from `HEAD` before acting.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
