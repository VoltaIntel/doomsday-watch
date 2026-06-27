# Nuke Watch Session State

Updated: 2026-06-26T21:10:00Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning deep scan refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `ec6ccc9` (`Update 2026-06-26T21:07:00Z — automated`).
- Final dashboard/current state: **62% / imminent**; raw global in state: **62.22** after deploy.
- Movement vs 18Z: `israel_lebanon` **100→98 / imminent** final (raw **95→88**) after adding canonical `israel_lebanon:diplomacy_active` on multiple US-brokered framework-accord reports, while retaining `israel_lebanon:ceasefire_violation` due same-day South Lebanon clash/strike reporting. Global stayed **62 / imminent** after rounding.
- Top coupled trackers: `israel_lebanon` 98, `russia_ukraine` 98, `pakistan_afghanistan` 88, `israel_palestine` 88, `sudan` 82, `russia` 50, `iran_nuclear` 46, `iran_conventional` 38, `china` 26, `india` 11, `north_korea` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals: `iran_nuclear:diplomacy_active`, `iran_nuclear:iaea_emergency`, `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `israel_lebanon:ceasefire_violation`, `israel_lebanon:diplomacy_active`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`, `north_korea:missile_range_test`.
- Signal hygiene: no non-canonical signals used. `israel_lebanon:diplomacy_active` is intentional this run; notes use "framework accord" wording to avoid accidental broad keyword churn. Pakistan-Afghanistan signal was not refreshed beyond the single News On AIR source.
- Source caveat: `web_search`/Tavily and `web_extract` returned HTTP 432. Fallback used Google News RSS, direct terminal official/public probes, UN News RSS, NATO pages, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA public pages returned 403 from this node; narrow Russia-Ukraine 24h RSS query was zero-hit, so a broader fallback query was used.
- Energy/markets: deploy OilPriceAPI 21:07Z Brent **$72.88**, WTI **$70.26**, gold **$4069.02**; Polymarket mapped-slug cache refreshed `2026-06-26T21:07:48Z`; worst divergence is `russia_ukraine` (~97.5pp, horizon mismatch).
- Emerging review: Thailand-Cambodia border-dispute escalation showed a multi-source watch cluster but no nuclear/alliance-spillover auto-add threshold; no tracker_config changes made.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded; git status clean after deploy.

## Watch next
- Israel-Lebanon: whether the framework accord produces operational de-escalation or is overwhelmed by South Lebanon clashes; any Hezbollah retaliation, IDF escalation, multi-front violence, or framework collapse.
- Iran/Hormuz: repeated ship strikes, official truce collapse, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse. Current Brent/WTI and traffic coverage still reject full shutdown.
- Iran/IAEA: actual verification visit execution, direct agency-page access returning, any reversal of interim framework, verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad shelling and border force movement. Downgrade further if the single-source claim ages without confirmation.
- DPRK: whether Kim-supervised tests remain tactical/short-range or expand into strategic systems; any configured strategic firing-event confirmation, DMZ escalation, or device event.
- Russia-Ukraine/Russia-NATO: confirmed Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Gaza/West Bank: more confirmed truce-breach fatalities, holy-site tension, or wider regional spillover.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.
- Emerging watch: Thailand-Cambodia is the only notable watch cluster; no untracked nuclear-escalation crisis auto-added at 21Z.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, etc.) unless intentionally activating the canonical signal. Use truce-breach/framework-accord wording carefully to avoid false positives.
