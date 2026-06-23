# Nuke Watch Session State

Updated: 2026-06-23T15:09:30Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `e954f68` (`Update 2026-06-23T15:08:56Z — automated`). A superseded 15:07Z commit (`daf6ba3`) was corrected for meta/global wording before final deploy.
- Final deployed dashboard: **61% / imminent**; raw global in state: **57.74%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 94, `israel_palestine` 84, `sudan` 70, `russia` 50, `iran_nuclear` 46, `iran_conventional` 38.
- Main movement vs 12:09Z: global held **61%**. `sudan` rose **67→70** after UN News, Sudan Tribune, GOV.UK/allied statement, and Channel Africa reported El Obeid/Kordofan drone/service disruption plus warnings/demands around an imminent RSF assault. No new canonical signal added.
- Other lane status: Iran nuclear held at 46 coupled with IAEA access disputed/denied in fallback reporting; Hormuz remains constrained/half-open but not zero-flow; Israel-Lebanon stays 100 after coupling with mixed strike/breach + talk-channel evidence; Russia/NATO, Ukraine, Pakistan-Afghanistan, Gaza, DPRK, China, India, Turkey and Abyei held.
- Signal hygiene: canonical-only clean. Active signals after final deploy: `iran_nuclear:diplomacy_active/iaea_emergency/iaea_access_denied`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `pakistan_afghanistan:diplomacy_active/military_buildup`, `sudan:infrastructure_strike/military_buildup`. No noncanonical signals in zones/trackers/dashboard.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all attempted required zone/topic queries; fallback used Google News RSS, terminal HTTP official probes, UN News/UN Press/NATO/EIA, OilPriceAPI, and Polymarket Gamma/cache. IAEA news/press and OPEC direct pages returned 403. Public state sanitized by pipeline to safe fallback caveat, with detailed fallback retained in `_meta.source_fallback_detail`.
- Market sanity: final deploy refreshed OilPriceAPI (Brent $76.93, WTI $73.38, gold $4129.00); Polymarket mapped cache refreshed at `2026-06-23T15:09:30Z`; worst mapped divergence remains `israel_lebanon` at ~99.3pp due horizon mismatch.
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical active-signal check clean; deploy/push succeeded; git status clean immediately after deploy before memory/vault logging.

## Previous important state
- 2026-06-23 12:09Z run deployed commit `2a35853`; dashboard **61% / imminent**, raw global **57.65%**, Iran Nuclear rose to 46 coupled on IAEA access-denial reports.
- 2026-06-23 09:10Z run deployed commit `0f42cae`; dashboard **61% / imminent**, raw global **57.17%**, Sudan rose to 67.
- 2026-06-23 06:09Z run deployed commit `dab968e`; dashboard **61% / imminent**, raw global **57.11%**, Iran War eased to 38 and Sudan rose to 65.
- Intel Brief source-caveat repair remains in place: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard renders public-safe caveat.

## Watch next
- Sudan/El Obeid/Kordofan: whether warnings turn into confirmed offensive, broader infrastructure strike wave, or external-state involvement.
- Iran/IAEA: official confirmation/refutation of access-denial reports; inspector return; IAEA emergency board action; verified higher-level enrichment, underground-site restart, or device event.
- Hormuz: independent AIS/ship-flow confirmation, insurer/charterer suspension, explicit waterway obstruction, naval escort incidents, or official reversal/denial of the waterway-closure claim.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or collapse of restoration channel.
- Russia-Ukraine/Russia-NATO: NATO direct-entry, Article 5, allied combat-role decision, or verified Russia-NATO kinetic incident.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, Pakistani retaliation, or verified Taliban/IEA force movement after contested claims.
- DPRK: corroborated South Korean/Japanese/US official confirmation of fresh configured firing-event or device-event activity; launcher-system/rhetoric items alone are not enough.
- India-Pakistan: whether Indus Waters threat rhetoric turns into force movement or cross-border incident.
- Israel-Palestine: East Jerusalem/holy-site clashes, West Bank settler-attack cycles, or Gaza crisis moves that broaden into multi-front violence.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only; if missing in worktree, restore tracked `data/tracker_config.json` from `HEAD` before acting.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid putting `ceasefire`, `negotiat`, or full signal-keyword wording in Israel-Lebanon notes; `extract_signals_from_notes` has broad fallback keywords that can create false `diplomacy_active` unless wording is neutralized.
