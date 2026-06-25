# Nuke Watch Session State

Updated: 2026-06-25T12:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `060b8d0` (`Update 2026-06-25T12:04:42Z — automated`).
- Final dashboard/current state: **61% / imminent**; raw global in state: **61.06**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 96, `israel_palestine` 86, `sudan` 78, `russia` 50, `iran_nuclear` 48, `iran_conventional` 30.
- Movement vs 09Z: global **61→61** and all final coupled tracker probabilities unchanged. Oil/Hormuz de-risking continues but CNBC/WSJ route-control coverage keeps `iran_conventional:hormuz_controlled_not_closed` alive. Iran agency-site access dispute persists. Israel-Lebanon breach lane remains active. Russia-Ukraine/Belarus pressure persists despite Moscow denial. Sudan/El Obeid/Kordofan pressure remains acute. China and DPRK remain rising/watch without configured trigger.
- Signal hygiene: canonical-only clean after deploy. Active: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike/military_buildup`. No noncanonical signals found.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 required query groups. Fallback used Google News RSS, direct official/public terminal probes, UN/NATO/EIA/ISW pages, Polymarket Gamma/cache, and OilPriceAPI. IAEA/OPEC direct pages returned 403/access-denied; Turkey, IAEA_UN, South Sudan/Abyei, and broad emerging feeds were sparse/empty.
- Energy/markets: deploy refreshed OilPriceAPI Brent **$73.17**, WTI **$69.76**, gold **$3996.20**; Polymarket cache refreshed `2026-06-25T12:05:19Z`; worst mapped divergence remains `israel_lebanon` (~99.4pp, horizon mismatch).
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; canonical signal check clean; deploy/push succeeded; git status clean after push.

## Watch next
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of site-access modalities; inspector return; board action; verified higher-level enrichment, underground-site restart, or device-event.
- Hormuz/oil: sustained AIS/ship-flow recovery vs tanker/vessel attack claims; insurer/charterer suspensions; explicit waterway obstruction; route-control escalation; naval escort incidents; or official reversal/denial of traffic recovery.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Union State/treaty invocation, or allied direct-entry breakpoint.
- Pakistan-Afghanistan: corroborated Durand Line casualty reports, Pakistani retaliation, cross-border strikes, drone losses, or confirmed force movement; current claims remain narrow-source/noisy.
- Sudan/El Obeid/Kordofan: confirmed RSF offensive/entry into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Israel-Lebanon: additional confirmed strikes/fatalities after truce arrangements, Hezbollah retaliation, or collapse of political channel.
- Gaza/West Bank: whether continuing pressure translates into wider diplomatic/kinetic escalation, holy-site tension, or multi-front violence.
- China-Taiwan: whether Strait warnings/Fujian carrier watch become sea-isolation, blockade execution, amphibious movement, or major PLA force-movement threshold.
- DPRK: corroborated South Korean/Japanese/U.S. official confirmation of a fresh configured firing-event or device-event activity; rhetoric/shipbuilding alone is not enough.
- Turkey and South Sudan/Abyei: currently quiet; keep sparse checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid `ceasefire`, `negotiat`, `peace talk`, `diplomatic talk`, `missile launch`, `weapon-grade`, and other broad `ZONE_SIGNAL_KEYWORDS` in negated/no-trigger notes unless intentionally activating the canonical signal.
