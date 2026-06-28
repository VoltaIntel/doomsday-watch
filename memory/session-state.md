# Nuke Watch Session State

Updated: 2026-06-27T21:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 21Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `208772f` (`Update 2026-06-27T21:07:59Z — automated`).
- Final dashboard/current state: **65% / imminent**; raw global in state: **65.02** after deploy.
- Movement vs 18Z: `iran_conventional` **80→82** coupled on Reuters/AP/WSJ/WaPo/CNBC follow-through for tanker/Bahrain/U.S.-Iran exchange coverage; `israel_lebanon` **90→92** coupled after Hezbollah rejection and new south-Lebanon hits; `sudan` **84→86** on UN/DW/NDTV/Sudan Tribune El Obeid/drone/backing pressure; `pakistan_afghanistan` **38→36** on continued zero fresh corroboration.
- Coupled tracker table: `russia_ukraine` 98, `israel_lebanon` 92, `israel_palestine` 88, `sudan` 86, `iran_conventional` 82, `russia` 50, `iran_nuclear` 44, `pakistan_afghanistan` 36, `china` 26, `north_korea` 11, `india` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals after deploy: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:ceasefire_violation`, `israel_lebanon:diplomacy_active`, `israel_lebanon:diplomacy_refused`, `iran_nuclear:diplomacy_active`, `north_korea:missile_range_test`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after deploy. Removed false-positive `iran_nuclear:iaea_access_denied` caused by IAEA inspection/access phrasing; neutralized Iran nuclear notes/latest_news and removed `iran_nuclear:iaea_access_denied` from `data/signal_timeline.json` before final redeploy.
- Source caveat: `web_search`/Tavily failed HTTP 432 on all required queries. Fallback used Google News RSS, direct terminal official/public probes, UN Press RSS, NATO pages, OCHA oPt, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA pages returned 403; ReliefWeb API returned 410; Pakistan-Afghanistan targeted RSS was zero-hit.
- Energy/markets: OilPriceAPI 21Z Brent **$73.08**, WTI **$69.23**, gold **$4080.83**. Energy/RSS coverage remains mixed but still shows tanker passage/traffic recovery, rejecting full waterway-stoppage thresholds. Polymarket mapped cache refreshed `2026-06-27T21:08:38Z`; worst mapped divergence remains `russia_ukraine` (~97.5pp, horizon mismatch).
- Emerging review: no tracker added. Thailand-Cambodia rose to watch-only with multiple 7d dispute/mediation/drill/HIMARS-acquisition hits but no nuclear/alliance-spillover threshold; Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia remain below scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded.

## Watch next
- Iran/Hormuz: repeated ship strikes, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse.
- Iran conventional: whether U.S.-Iran exchanges remain contained or broaden to Bahrain/Gulf targets, U.S. bases, Israel, shipping, or oil infrastructure.
- Israel-Lebanon: framework implementation vs collapse; Hezbollah retaliation, IDF escalation, multi-front spillover, or rejection hardening.
- Iran/agency verification: actual site visit execution, direct agency-page accessibility, verified higher-level enrichment, underground-site restart, device event.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad/TTP border-shelling claim; downgrade further if still unconfirmed.
- Sudan/El Obeid: confirmed RSF entry/offensive, broader drone/infrastructure disruption, external backing, or atrocity reporting.
- Russia/NATO: Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- Thailand-Cambodia: watch-only unless escalation gains nuclear/alliance-spillover relevance or stronger configured trigger evidence.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, `inspection access`, etc.) unless intentionally activating the canonical signal.
