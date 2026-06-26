# Nuke Watch Session State

Updated: 2026-06-26T15:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `5eed041` (`Update 2026-06-26T15:07:00Z — automated`).
- Final dashboard/current state: **62% / imminent**; raw global in state: **61.62**.
- Movement vs 12Z: `iran_nuclear` **48→45 / critical** after 15Z wire/established reporting indicated UN nuclear watchdog verification visits will happen under the interim framework. Cleared `iran_nuclear:iaea_access_denied`; added canonical `iran_nuclear:diplomacy_active`; kept `iran_nuclear:iaea_emergency`. Global stayed 62 after rounding.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 92, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 45, `iran_conventional` 32, `china` 26, `india` 11, `north_korea` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals: `iran_nuclear:diplomacy_active`, `iran_nuclear:iaea_emergency`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`, `north_korea:missile_range_test`.
- Signal hygiene: final canonical check clean; only intentional `diplomacy_active` is on `iran_nuclear`. `iaea_access_denied` no longer appears in `data/signal_timeline.json` or active tracker signals. Continued using truce-breach wording for Israel lanes to avoid broad false positives.
- Source caveat: `web_search`/Tavily returned HTTP 432 on all targeted query groups. Fallback used Google News RSS, direct terminal official/public probes, UN Press RSS, NATO pages, EIA, OilPriceAPI and Polymarket Gamma/cache. Direct IAEA public pages returned 403; UN News RSS parse failed from this node; South Sudan/Abyei returned zero hits.
- Energy/markets: deploy OilPriceAPI 15:07Z Brent **$72.16**, WTI **$69.08**, gold **$4090.18**; Polymarket Gamma/cache refreshed `2026-06-26T15:07:39Z` (13 mapped markets in dashboard check); worst divergence remains `israel_lebanon` (~99.3pp, horizon mismatch).
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; deploy commit `5eed041`.

## Watch next
- Iran/IAEA: direct agency-page access returning; official confirmation/refutation of actual verification visit timing; any reversal of the interim framework; verified higher-level enrichment, underground-site restart, or device event.
- Hormuz/oil: repeated ship strikes, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse. Current Brent/WTI still argue against full shutdown.
- DPRK: KCNA/wire details on whether tests remain tactical/short-range or expand into strategic systems; any further configured firing-event confirmation, DMZ escalation, or device event.
- Russia-Ukraine/Russia-NATO: eastern-flank warning escalation; confirmed Russian incident in Baltic states/Poland, treaty invocation, Article 5 language, or allied direct-entry breakpoint.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad shelling and airstrike claims, border closures, or official mobilization; downgrade quickly if claims do not refresh beyond the single-source window.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Israel-Lebanon and Gaza/West Bank: more confirmed truce-breach fatalities, Hezbollah retaliation, multi-front violence, holy-site tension, or wider regional spillover.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.
- Emerging watch: Thailand-Cambodia border and Ethiopia/Eritrea clusters remain watch-only unless cross-border force events intensify or nuclear/escalation relevance rises.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, etc.) unless intentionally activating the canonical signal. Use truce-breach language in notes when carrying `ceasefire_violation` to avoid `diplomacy_active` false positives.
