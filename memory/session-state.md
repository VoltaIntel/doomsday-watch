# Nuke Watch Session State

Updated: 2026-06-26T12:08:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `3d7a2dc` (`Update 2026-06-26T12:05:00Z — automated`).
- Final dashboard/current state: **62% / imminent**; raw global in state: **61.98**.
- Movement vs 09Z: **no numeric tracker probability changes**. Source refresh reconfirmed DPRK ballistic weapon-test lane, NATO eastern-flank warnings, Israel-Lebanon/Gaza breach reporting, Sudan El Obeid pressure, and Hormuz route-control risk. Oil/Hormuz traffic evidence still blocks Iran conventional escalation.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 92, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 48, `iran_conventional` 32, `china` 26, `india` 11, `north_korea` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals: `iran_nuclear:iaea_access_denied`, `iran_nuclear:iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`, `north_korea:missile_range_test`.
- Signal hygiene: final canonical check clean; no false `diplomacy_active` entries in state or timeline. Continued using truce-breach wording in notes to avoid broad keyword false positives.
- Source caveat: `web_search`/Tavily returned HTTP 432 on all targeted query groups. Fallback used Google News RSS, direct terminal official/public probes, UN Press RSS, UN News RSS, NATO pages, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA public pages returned 403; Turkey and South Sudan/Abyei were sparse/low-signal.
- Energy/markets: deploy OilPriceAPI 12:05Z Brent **$73.22**, WTI **$70.31**, gold **$4059.25**; Polymarket mapped-slug cache refreshed `2026-06-26T12:05:53Z`; worst divergence remains `israel_lebanon` (~99.3pp, horizon mismatch).
- Verification: JSON valid; no false-positive `diplomacy_active`; `index.html` contains required command-deck markers; deploy/push succeeded; deploy commit `3d7a2dc`.

## Watch next
- DPRK: KCNA/wire details on whether tests remain tactical/short-range or expand into strategic systems; any further configured firing-event confirmation, DMZ escalation, or device event.
- Russia-Ukraine/Russia-NATO: eastern-flank warning escalation; confirmed Russian incident in Baltic states/Poland, treaty invocation, Article 5 language, or allied direct-entry breakpoint.
- Hormuz/oil: repeated ship strikes, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse.
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of agency-access modalities; verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad shelling and airstrike claims, border closures, or official mobilization; downgrade quickly if claims prove single-source/noisy.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Israel-Lebanon and Gaza/West Bank: more confirmed truce-breach fatalities, Hezbollah retaliation, multi-front violence, holy-site tension, or wider regional spillover.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.
- Emerging watch: Thailand-Cambodia border and Ethiopia/Eritrea clusters remain watch-only unless cross-border force events intensify or nuclear/escalation relevance rises.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, etc.) unless intentionally activating the canonical signal. Use truce-breach language in notes when carrying `ceasefire_violation` to avoid `diplomacy_active` false positives.
