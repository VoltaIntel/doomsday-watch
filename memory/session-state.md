# Nuke Watch Session State

Updated: 2026-06-25T15:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `f20efab` (`Update 2026-06-25T15:07:11Z — automated`).
- Final dashboard/current state: **60% / imminent**; raw global in state: **60.42**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 88, `israel_palestine` 86, `sudan` 78, `russia` 50, `iran_nuclear` 48, `iran_conventional` 30.
- Movement vs 12Z: global **61→60**. Main mover: `pakistan_afghanistan` **96→88** after targeted 24h/7d fallback found no fresh corroboration for the prior cross-border force-pressure item; cleared `pakistan_afghanistan:military_buildup`. Hormuz/oil de-risking continues but route-control reporting keeps `iran_conventional:hormuz_controlled_not_closed` alive. Iran verification dispute persists. Israel-Lebanon truce-breach lane remains active. Russia-Ukraine/Belarus pressure persists despite Moscow denial. Sudan/El Obeid/Kordofan pressure remains acute. China and DPRK remain rising/watch without configured trigger.
- Signal hygiene: canonical-only clean after deploy. Active: `iran_nuclear:iaea_access_denied/iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `sudan:infrastructure_strike/military_buildup`. Cleared: `pakistan_afghanistan:military_buildup`. No noncanonical signals found.
- Source caveat: `web_search`/Tavily failed HTTP 432 for all 17 required query groups. Fallback used Google News RSS, direct official/public terminal probes, UN/NATO/EIA/ISW/UN Press pages, Polymarket Gamma/cache, and OilPriceAPI. IAEA/OPEC direct pages returned 403/access-denied; Turkey/Russia-NATO/China/Pakistan-Afghanistan/South Sudan-Abyei/emerging feeds were sparse.
- Energy/markets: deploy refreshed OilPriceAPI Brent **$73.84**, WTI **$70.64**, gold **$4012.98**; Polymarket cache refreshed `2026-06-25T15:07:51Z`; worst mapped divergence remains `israel_lebanon` (~99.4pp, horizon mismatch).
- Verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON valid; deploy/push succeeded. Post-deploy memory files were updated locally for continuity.

## Watch next
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of site-access modalities; inspector return; board action; verified higher-level enrichment, underground-site restart, or device event.
- Hormuz/oil: sustained AIS/ship-flow recovery vs tanker/vessel attack claims; insurer/charterer suspensions; explicit waterway obstruction; route-control escalation; naval escort incidents; or official reversal/denial of traffic recovery.
- Russia-Ukraine/Belarus: confirmed Belarus-front activation, larger call-up, border assembly, Union State/treaty invocation, or allied direct-entry breakpoint.
- Pakistan-Afghanistan: corroborated Durand Line casualty reports, Pakistani retaliation, cross-border strikes, drone losses, or confirmed force movement; prior configured force-pressure signal was cleared at 15Z due no fresh corroboration.
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
