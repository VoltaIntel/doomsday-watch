# Nuke Watch Session State

Updated: 2026-06-24T15:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `2b46f65` (`Update 2026-06-24T15:06:41Z — automated`).
- Final dashboard/current state: **61% / imminent**; raw global in state: **61.06**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 96, `israel_palestine` 86, `sudan` 78, `russia` 50, `iran_nuclear` 48, `iran_conventional` 30.
- Movement vs 12Z: global **61→61**. Final coupled values unchanged; `iran_conventional` raw **23→22** on additional Hormuz/oil de-risking but final remains 30 after coupling. Israel-Lebanon remains capped at 100; China/DPRK remain rising/watch without canonical signal; Sudan holds 78.
- Signal hygiene: canonical-only clean after deploy. Active: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike/military_buildup`. No noncanonical signals added; canonical signal check clean.
- Source caveat: `web_search`/Tavily failed HTTP 432 for 15/15 attempted query groups; fallback used Google News RSS for all configured trackers/topics, 7d/30d sparse checks, direct official/public terminal probes, UN News/NATO/EIA, Yahoo Finance, and Polymarket Gamma/cache. IAEA/OPEC direct pages returned 403/access-denied.
- Energy/markets: deploy refreshed Brent **$73.43**, WTI **$69.84**, gold **$4007.80**; independent Yahoo probe showed Brent **$73.50**, WTI **$69.84**, gold **$4024.80**; Polymarket cache refreshed `2026-06-24T15:07:18Z`; worst mapped divergence remains `israel_lebanon` (~99.4pp, horizon mismatch).
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical signal check clean; deploy/push succeeded.

## Watch next
- Iran/IAEA: official confirmation/refutation of struck-site access; inspector return; agency board action; verified higher-level enrichment, underground-site restart, or device event.
- Hormuz/oil: sustained AIS/ship-flow recovery vs quota/control claims; insurer/charterer suspensions; explicit waterway obstruction; naval escort incidents; or official reversal/denial of traffic recovery.
- Pakistan-Afghanistan: corroborated Durand Line casualty reports, Pakistani retaliation, cross-border strikes, drone losses, or confirmed force movement; current claims remain narrow-source.
- Sudan/El Obeid/Kordofan: confirmed RSF offensive/entry into El Obeid, broader infrastructure strike wave, external backing, or atrocity reporting.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or collapse of the political channel.
- Gaza/West Bank: whether the UN commission finding translates into wider diplomatic/kinetic escalation, holy-site tension, or multi-front violence.
- China-Taiwan: whether Fujian carrier transit/drills become blockade/sea-isolation, amphibious movement, or major PLA force-movement threshold.
- Russia-Ukraine/Russia-NATO: Article 5, allied direct-entry, combat-role decision, verified Russia-NATO kinetic incident, or Belarus-front activation.
- DPRK: corroborated South Korean/Japanese/U.S. official confirmation of a fresh configured firing-event or device-event activity; rhetoric/shipbuilding alone is not enough.
- Turkey and South Sudan/Abyei: currently quiet; keep sparse checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid `ceasefire`, `negotiat`, `peace talk`, `diplomatic talk`, `missile launch`, `weapon-grade`, and other broad `ZONE_SIGNAL_KEYWORDS` in negated/no-trigger notes unless intentionally activating the canonical signal.
