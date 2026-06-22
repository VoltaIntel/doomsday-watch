# Nuke Watch Session State

Updated: 2026-06-22T12:11:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `209fe3c` (`Update 2026-06-22T12:06:15Z — automated`).
- Final deployed dashboard: **63% / imminent**; raw global in state: **63.09%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 98, `israel_palestine` 88, `sudan` 55, `russia` 50, `iran_nuclear` 46, `iran_conventional` 46.
- Main movement vs 09:05Z: **no numeric probability changes**. Qualitative reinforcement: CNBC/Al Jazeera/Reuters/CBC kept Hormuz shipping-stall-but-not-zero-flow picture alive; DD News kept Pakistan-Afghanistan open-war/airstrike pressure visible; Dabanga/UN-linked Sudan El Obeid atrocity warnings amplified; India-Pakistan Indus rhetoric stayed elevated.
- Signal hygiene: canonical-only clean. No new configured signal promoted. Maintained `iran_nuclear:diplomacy_active/iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_closed`, `israel_lebanon:ceasefire_violation/diplomacy_active`, `pakistan_afghanistan:military_buildup`, `sudan:military_buildup`, and `israel_palestine:holy_site_tension`. No other configured signal active.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all required zone queries; fallback used Google News RSS, direct public-source pages, UN/NATO public-site probes, local energy cache/OilPriceAPI, and Polymarket Gamma/cache. UN/IAEA/OPEC/NATO RSS feeds were partially blocked/malformed; IAEA direct news returned 403.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $79.03, WTI $75.17, gasoline $2.99, diesel $3.15, gold $4206.04); Polymarket cache refreshed at `2026-06-22T12:06:55Z`; worst mapped divergence remains `israel_lebanon` ~99.3pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical active-signal check clean; deploy/push succeeded.

## Previous important state
- 06:08Z run deployed commit `95687f2`; dashboard **63% / imminent**. Final cleanup removed transient false positives `china:nuclear_rhetoric_official` and `israel_palestine:diplomacy_active`.
- Intel Brief source-caveat repair remains in place: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard renders public-safe caveat.

## Watch next
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit waterway obstruction, naval escort incidents, or official reversal/denial of the shut-waterway claim.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or collapse of restoration channel.
- Iran/IAEA: official access restoration vs monitoring-denial breakpoint; current reporting remains mixed between talks/technical work and site-access dispute.
- Russia-Ukraine/Russia-NATO: NATO direct-entry, Article 5, allied combat-role decision, or verified Russia-NATO kinetic incident.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, Pakistani retaliation, or verified Taliban/IEA force movement after contested claims.
- DPRK: corroborated South Korean/Japanese/US official confirmation of fresh strategic projectile activity; single-source/commentary items are not enough.
- India-Pakistan: whether Indus Waters threat rhetoric turns into force movement or cross-border incident.
- Israel-Palestine: East Jerusalem/holy-site clashes, West Bank settler-attack cycles, or Gaza crisis moves that broaden into multi-front violence.
- Sudan/El Obeid: whether warning/mobilisation reporting turns into confirmed offensive, infrastructure strike, or external-state involvement.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
