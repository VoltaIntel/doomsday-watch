# Nuke Watch Session State

Updated: 2026-06-24T06:11:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Final pushed HEAD: `c6d69ce` (`Update 2026-06-24T06:07:22Z — automated`).
- Final dashboard/current state: **62% / imminent**; raw global in state: **58.0%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 96, `israel_palestine` 86, `sudan` 76, `russia` 50, `iran_nuclear` 48, `iran_conventional` 34.
- Movement vs 03Z: **no probability changes**. Meaningful watch changes: DPRK naval-modernization/rhetoric feed intensified but no configured DPRK signal was promoted; Hormuz/oil evidence continued to ease; Pakistan-Afghanistan heavy-casualty claim keeps the existing high-risk lane active; Sudan/El Obeid remains the clearest non-nuclear conventional escalation pressure.
- Signal hygiene: canonical-only clean after deploy. Active: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike/military_buildup`. No noncanonical signals added.
- Source caveat: `web_search`/Tavily failed HTTP 432 for 14/14 attempted query groups and `web_extract` failed HTTP 432 for 9/9 extracts; fallback used Google News RSS for all configured trackers/topics, 7d/30d sparse RSS checks, direct official/public terminal probes, UN News/NATO/EIA, Yahoo/OilPriceAPI, and Polymarket Gamma/cache. IAEA/OPEC direct pages returned 403/access-denied.
- Energy/markets: deploy refreshed Brent **$76.35**, WTI **$72.47**, gold **$4073.49**; independent Yahoo probe showed Brent **$76.38**, WTI **$72.48**; Polymarket cache refreshed at `2026-06-24T06:08:00Z`; worst mapped divergence remains `israel_lebanon` (~99.3pp, horizon mismatch).
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical signal check clean; deploy/push succeeded.

## Watch next
- Iran/IAEA: official confirmation/refutation of struck-site access; inspector return; agency board action; verified higher-level enrichment, underground-site restart, or device event.
- Hormuz/oil: sustained AIS/ship-flow recovery vs quota/control claims; insurer/charterer suspensions; explicit waterway obstruction; naval escort incidents; or official reversal/denial of traffic recovery.
- Pakistan-Afghanistan: corroborated Durand Line casualty reports, Pakistani retaliation, cross-border strikes, drone losses, or confirmed force movement; 06Z source includes one fresh heavy-casualty claim, but do not inflate without corroboration.
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
