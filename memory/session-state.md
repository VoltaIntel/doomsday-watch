# Nuke Watch Session State

Updated: 2026-06-23T21:12:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `1613f40` (`Update 2026-06-23T21:08:33Z — automated`). Earlier 21:06Z commit `8707991` was superseded by a final metadata-correction deploy.
- Final deployed dashboard: **61% / imminent**; raw global in state: **57.50%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 94, `israel_palestine` 84, `sudan` 74, `russia` 50, `iran_nuclear` 46, `iran_conventional` 36.
- Main movement vs 18:07Z: global held **61%**. `sudan` rose **72→74** after GOV.UK, Anadolu and Sudan Tribune reported El Obeid atrocity warning, continued RSF drone attacks, civilian-infrastructure disruption and supply-route pressure. Other numeric lanes held.
- Other lane status: Iran/Hormuz remains constrained-not-closed with BBC/gCaptain/Democracy Now evidence; Iran nuclear stayed 46 coupled with verification access impaired; Israel-Lebanon stayed 100 after coupling; Russia/NATO, Ukraine, Pakistan-Afghanistan, Gaza/West Bank, DPRK, China, India, Turkey and Abyei held.
- Signal hygiene: canonical-only clean. Pipeline pruned expired `iran_nuclear:diplomacy_active`; active signals after final deploy: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `pakistan_afghanistan:diplomacy_active/military_buildup`, `sudan:infrastructure_strike/military_buildup`. No noncanonical signals in zones/trackers/dashboard.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all attempted required zone/topic queries; fallback used Google News RSS, browser direct GOV.UK page, terminal HTTP official probes, UN News/UN Press/NATO/EIA, OilPriceAPI, and Polymarket Gamma/cache. IAEA news/press and OPEC direct pages returned 403. Public state sanitized by pipeline to safe fallback caveat, with detailed fallback retained in `_meta.source_fallback_detail`.
- Market sanity: final deploy refreshed OilPriceAPI (Brent $76.88, WTI $73.06, gold $4110.02); Polymarket mapped cache refreshed at `2026-06-23T21:09:08Z`; worst mapped divergence remains `israel_lebanon` at ~99.3pp due horizon mismatch.
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical active-signal check clean; deploy/push succeeded; git status clean immediately after deploy before memory/vault logging.

## Kabul Watch latest cron run
- Job: Kenan daily Afghanistan/Kabul Watch summary for Discord/Telegram.
- Research mode: Tavily/web_search disabled by prompt; used direct terminal/browser checks, Google News RSS, AP direct, Afghanistan International direct pages/feed, Amu TV, FlightStats, Safe Airspace, and carrier pages where reachable.
- Kabul bottom line: no mass-casualty Kabul attack confirmed in the last 24h; main Kabul items were a Taliban raid that halted Tamadon TV broadcasts and a contained Mandawi market fire.
- Confirmed Kabul items: Amu TV + Afghanistan International reported Taliban raided Tamadon TV in Kabul and broadcasts were cut; Afghanistan International, citing Taliban interior ministry, reported a Monday-night Mandawi fire burned 8 shops with about AFN 8m damage and firefighters prevented spread to 497 other shops/warehouses.
- Afghanistan-wide / external: AP and Afghanistan International reported first closed-door EU-Taliban Brussels talks focused on deportations/consular issues; Taliban MFA said the delegation ended its Europe trip emphasizing broader diplomatic ties.
- Aviation: no material KBL disruption found. FlightStats listed 23 Jun KBL departures including Ariana, Turkish, Kam Air, Flydubai/Emirates, and Ariana domestic sectors. Safe Airspace still lists Afghanistan and Pakistan at Risk Level 2; OAKX/Kabul FIR remains open but uncontrolled/no ATC. Ariana's direct site was unreachable from this environment, so aviation confidence stayed medium.
- Unverified/local watch: Afghanistan International, citing sources, said Taliban justice minister detained Shiite elders in Kabul over Muharram flags and warned mourners to observe restrictions; not independently confirmed.
- Delivery: prepared platform-split Discord + Telegram summary with matched facts/URLs and risk judged Medium / confidence Medium.

## Previous important state
- 2026-06-23 15:09Z run deployed commit `e954f68`; dashboard **61% / imminent**, raw global **57.74%**, Sudan rose to 70.
- 2026-06-23 12:09Z run deployed commit `2a35853`; dashboard **61% / imminent**, raw global **57.65%**, Iran Nuclear rose to 46 coupled on IAEA access-denial reports.
- 2026-06-23 09:10Z run deployed commit `0f42cae`; dashboard **61% / imminent**, raw global **57.17%**, Sudan rose to 67.
- Intel Brief source-caveat repair remains in place: `scripts/pipeline.py` sanitizes public `_meta.source_limitation`, `_meta.search_engine`, and `official_source_probe`; dashboard renders public-safe caveat.

## Watch next
- Sudan/El Obeid/Kordofan: whether allied atrocity warning turns into confirmed offensive, broader infrastructure strike wave, or external-state involvement.
- Hormuz: independent AIS/ship-flow confirmation that recovery sustains; insurer/charterer suspension; explicit waterway obstruction; naval escort incidents; or official reversal/denial of traffic recovery.
- Iran/IAEA: official confirmation/refutation of access-denial reports; inspector return; IAEA emergency board action; verified higher-level enrichment, underground-site restart, or device event.
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
