# Nuke Watch Session State

Updated: 2026-06-24T00:09:30Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Final pushed HEAD: `f7520a1` (`Align morning scan metadata`), after deploy commit `1f58f69` (`Update 2026-06-24T00:08:22Z — automated`). Superseded first deploy: `5b869ac`.
- Final dashboard/current state: **62% / imminent**; raw global in state: **58.0%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 96, `israel_palestine` 86, `sudan` 76, `russia` 50, `iran_nuclear` 48, `iran_conventional` 34.
- Main movement vs 2026-06-23 21Z: global **61→62**. `iran_nuclear` **46→48** on access-rejection coverage; `pakistan_afghanistan` **94→96** on Durand Line casualty/open-war reports; `sudan` **74→76** on UN/El Obeid infrastructure/service evidence; `israel_palestine` **84→86** on UN commission finding; `china` **21→23** on carrier/drill evidence; `iran_conventional` **36→34** on improved Hormuz traffic.
- Signal hygiene: canonical-only clean after final deploy. Active: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike/military_buildup`. Removed/de-emphasized `pakistan_afghanistan:diplomacy_active`; removed false `israel_palestine:diplomacy_active` caused by “negotiations” wording.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 required zone/topic queries; fallback used Google News RSS, 7d/30d sparse RSS, direct official/public terminal probes, UN News/NATO/EIA, OilPriceAPI, and Polymarket Gamma/cache. IAEA/OPEC direct pages returned access-denied; UN press RSS path returned not found.
- Market sanity: final deploy refreshed Brent $77.00, WTI $72.80, gold $4122.59; Polymarket mapped cache refreshed at `2026-06-24T00:08:54Z`; worst mapped divergence remains `israel_lebanon` (~99.3pp, horizon mismatch).
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; signal timeline clean; deploy/push succeeded; git status clean immediately after final commit before memory/vault logging.

## Watch next
- Iran/IAEA: official confirmation/refutation of struck-site access; inspector return; agency board action; verified higher-level enrichment, underground-site restart, or device event.
- Hormuz/oil: sustained AIS/ship-flow recovery vs quota/control claims; insurer/charterer suspensions; explicit waterway obstruction; naval escort incidents; or official reversal/denial of traffic recovery.
- Pakistan-Afghanistan: corroborated Durand Line casualty reports, Pakistani retaliation, cross-border strikes, drone losses, or confirmed force movement.
- Sudan/El Obeid/Kordofan: confirmed RSF offensive, broader infrastructure strike wave, external backing, or atrocity reporting.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or collapse of the political channel.
- Gaza/West Bank: whether the UN commission finding translates into wider diplomatic/kinetic escalation, holy-site tension, or multi-front violence.
- China-Taiwan: whether carrier transit/drills become a blockade/sea-isolation, amphibious movement, or major PLA force-movement threshold.
- Russia-Ukraine/Russia-NATO: Article 5, allied direct-entry, combat-role decision, or verified Russia-NATO kinetic incident.
- DPRK: corroborated South Korean/Japanese/U.S. official confirmation of a fresh configured firing-event or device-event activity; rhetoric/shipbuilding alone is not enough.
- Turkey and South Sudan/Abyei: currently quiet; keep sparse checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid `ceasefire`, `negotiat`, `peace talk`, `diplomatic talk`, `missile launch`, `weapon-grade`, and other broad `ZONE_SIGNAL_KEYWORDS` in negated/no-trigger notes unless intentionally activating the canonical signal.
