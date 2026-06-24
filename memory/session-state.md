# Nuke Watch Session State

Updated: 2026-06-24T18:11:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `8b0d18a` (`Update 2026-06-24T18:07:37Z — automated`).
- Final dashboard/current state: **61% / imminent**; raw global in state: **61.06**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 96, `israel_palestine` 86, `sudan` 78, `russia` 50, `iran_nuclear` 48, `iran_conventional` 30.
- Movement vs 15Z: global **61→61**. Final probabilities unchanged except trend/signal posture: `russia_ukraine` promoted canonical `military_buildup` on Belarus-front pressure/conscription reporting but stayed 98; `iran_conventional` remained 30 after mixed Hormuz traffic recovery plus tanker/standoff items; `china`/`north_korea` remain rising/watch without configured triggers.
- Signal hygiene: canonical-only clean after deploy. Active: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike/military_buildup`. No noncanonical signals found.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 attempted query groups; fallback used Google News RSS for all configured trackers/topics, 7d/30d sparse checks, direct official/public terminal probes, UN News/NATO/EIA/ISW, Yahoo Finance, and Polymarket Gamma/cache. IAEA/OPEC direct pages returned 403/access-denied.
- Energy/markets: deploy refreshed OilPriceAPI Brent **$73.94**, WTI **$70.38**, gold **$3969.66**; independent Yahoo probe showed Brent **$73.97**, WTI **$70.47**, gold **$3995.90**; Polymarket cache refreshed `2026-06-24T18:08:08Z`; worst mapped divergence remains `israel_lebanon` (~99.4pp, horizon mismatch).
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical signal check clean; deploy/push succeeded.

## Watch next
- Iran/IAEA: official confirmation/refutation of struck-site access; inspector return; agency board action; verified higher-level enrichment, underground-site restart, or device event.
- Hormuz/oil: sustained AIS/ship-flow recovery vs tanker/vessel attack claims; insurer/charterer suspensions; explicit waterway obstruction; naval escort incidents; or official reversal/denial of traffic recovery.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Russian-Belarus treaty invocation, or allied direct-entry breakpoint.
- Pakistan-Afghanistan: corroborated Durand Line casualty reports, Pakistani retaliation, cross-border strikes, drone losses, or confirmed force movement; current claims remain narrow-source.
- Sudan/El Obeid/Kordofan: confirmed RSF offensive/entry into El Obeid, broader infrastructure strike wave, external backing, or atrocity reporting.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or collapse of the political channel.
- Gaza/West Bank: whether the UN commission finding translates into wider diplomatic/kinetic escalation, holy-site tension, or multi-front violence.
- China-Taiwan: whether ship-authority assertions/Fujian carrier transit/drills become blockade/sea-isolation, amphibious movement, or major PLA force-movement threshold.
- DPRK: corroborated South Korean/Japanese/U.S. official confirmation of a fresh configured firing-event or device-event activity; rhetoric/shipbuilding alone is not enough.
- Turkey and South Sudan/Abyei: currently quiet; keep sparse checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid `ceasefire`, `negotiat`, `peace talk`, `diplomatic talk`, `missile launch`, `weapon-grade`, and other broad `ZONE_SIGNAL_KEYWORDS` in negated/no-trigger notes unless intentionally activating the canonical signal.
