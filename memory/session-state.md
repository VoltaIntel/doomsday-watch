# Nuke Watch Session State

Updated: 2026-06-25T00:13:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `89bca7e` (`Update 2026-06-25T00:09:01Z — automated`).
- Final dashboard/current state: **61% / imminent**; raw global in state: **61.06**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 96, `israel_palestine` 86, `sudan` 78, `russia` 50, `iran_nuclear` 48, `iran_conventional` 30.
- Movement vs 21Z: global **61→61** and all final tracker probabilities unchanged. Israel-Lebanon breach lane refreshed by a new Al Jazeera south-Lebanon fatality item; Hormuz/oil de-risking continued (Brent $73.14, WTI $70.01 after deploy); DD News refreshed Pakistan-Afghanistan open-war posture; China/DPRK remain rising/watch without configured triggers.
- Signal hygiene: canonical-only clean after deploy. Active: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike/military_buildup`. No noncanonical signals found.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 attempted query groups; `web_extract`/Tavily also returned HTTP 432. Fallback used Google News RSS, direct official/public terminal probes, UN News/NATO/EIA pages, Polymarket Gamma/cache, and OilPriceAPI. IAEA/OPEC direct pages returned 403/access-denied; specific ISW page returned 403.
- Energy/markets: deploy refreshed OilPriceAPI Brent **$73.14**, WTI **$70.01**, gold **$4010.69**; Polymarket cache refreshed `2026-06-25T00:09:38Z`; worst mapped divergence remains `israel_lebanon` (~99.4pp, horizon mismatch).
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical signal check clean; deploy/push succeeded; git clean after push.

## Watch next
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of site-access modalities; inspector return; board action; verified higher-level enrichment, underground-site restart, or device-event.
- Hormuz/oil: sustained AIS/ship-flow recovery vs tanker/vessel attack claims; insurer/charterer suspensions; explicit waterway obstruction; naval escort incidents; or official reversal/denial of traffic recovery.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Union State/treaty invocation, or allied direct-entry breakpoint.
- Pakistan-Afghanistan: corroborated Durand Line casualty reports, Pakistani retaliation, cross-border strikes, drone losses, or confirmed force movement; current claims remain narrow-source.
- Sudan/El Obeid/Kordofan: confirmed RSF offensive/entry into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or collapse of political channel.
- Gaza/West Bank: whether continuing pressure translates into wider diplomatic/kinetic escalation, holy-site tension, or multi-front violence.
- China-Taiwan: whether Fujian carrier transit/drills become sea-isolation, blockade execution, amphibious movement, or major PLA force-movement threshold.
- DPRK: corroborated South Korean/Japanese/U.S. official confirmation of a fresh configured firing-event or device-event activity; rhetoric/shipbuilding alone is not enough.
- Turkey and South Sudan/Abyei: currently quiet; keep sparse checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid `ceasefire`, `negotiat`, `peace talk`, `diplomatic talk`, `missile launch`, `weapon-grade`, and other broad `ZONE_SIGNAL_KEYWORDS` in negated/no-trigger notes unless intentionally activating the canonical signal.
