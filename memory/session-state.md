# Nuke Watch Session State

Updated: 2026-06-26T18:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `c099e41` (`Update 2026-06-26T18:06:41Z — automated`).
- Final dashboard/current state: **62% / imminent**; raw global in state: **62.5**.
- Movement vs 15Z: `iran_conventional` **32→38 / critical** after adding canonical `iran_conventional:ceasefire_violation` on Reuters/NYT/Bloomberg/CNBC ship-strike + official truce-breach reporting; `iran_conventional:hormuz_controlled_not_closed` stayed active. `iran_nuclear` **45→46 / critical** via coupling. `pakistan_afghanistan` **92→88 / imminent** because Kunar/Asadabad shelling remained single-source and did not refresh beyond News On AIR. Global stayed 62 after rounding.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 88, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 46, `iran_conventional` 38, `china` 26, `india` 11, `north_korea` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals: `iran_nuclear:diplomacy_active`, `iran_nuclear:iaea_emergency`, `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`, `north_korea:missile_range_test`.
- Signal hygiene: no non-canonical signals used. Intentional `ceasefire_violation` addition only on `iran_conventional`; no false `diplomacy_active` outside `iran_nuclear`. Continued using truce-breach wording in notes to avoid broad keyword false positives.
- Source caveat: `web_search`/Tavily returned HTTP 432 on all targeted query groups. Fallback used Google News RSS, direct terminal official/public probes, NATO pages, UN RSS endpoints, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA public pages returned 403 from this node; Turkey configured query, South Sudan/Abyei 30d, and emerging-crisis targeted query returned zero RSS hits.
- Energy/markets: deploy OilPriceAPI 18:06Z Brent **$72.08**, WTI **$69.41**, gold **$4077.72**; Polymarket Gamma/cache refreshed `2026-06-26T18:07:27Z` (13 mapped markets in dashboard check); worst divergence remains `israel_lebanon` (~99.4pp, horizon mismatch).
- Verification: JSON valid; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean after deploy.

## Watch next
- Iran/Hormuz: repeated ship strikes, official truce collapse, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse. Current Brent/WTI and traffic coverage still reject full shutdown.
- Iran/IAEA: actual verification visit execution, direct agency-page access returning, any reversal of interim framework, verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad shelling and border force movement. Downgrade further if the single-source claim ages without confirmation.
- DPRK: whether Kim-supervised tests remain tactical/short-range or expand into strategic systems; any configured strategic firing-event confirmation, DMZ escalation, or device event.
- Russia-Ukraine/Russia-NATO: confirmed Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Israel-Lebanon and Gaza/West Bank: more confirmed truce-breach fatalities, Hezbollah retaliation, multi-front violence, holy-site tension, or wider regional spillover.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.
- Emerging watch: no untracked nuclear-escalation crisis met auto-add threshold at 18Z.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, etc.) unless intentionally activating the canonical signal. Use truce-breach language in notes when carrying `ceasefire_violation` to avoid `diplomacy_active` false positives.
