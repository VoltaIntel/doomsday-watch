# Nuke Watch Session State

Updated: 2026-06-20T00:09:30Z

## Latest cron run
- Job: DoomsdayWatch nuclear escalation morning/deep scan.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Dashboard deploy commit: `e68f3b1` (`Update 2026-06-20T00:04:56Z — automated`).
- Final deployed dashboard: **59% / imminent**; raw global in state: **55.3%**.
- Top coupled trackers: `israel_lebanon` 100, `russia_ukraine` 98, `pakistan_afghanistan` 94, `israel_palestine` 87, `sudan` 51, `russia` 50, `iran_nuclear` 43, `iran_conventional` 28.
- Main movers vs prior deployed state: Sudan **49→51** and critical→imminent on OHCHR/UN El Obeid warnings; Pakistan-Afghanistan **93→94** on disputed strike/drone claims plus Taliban 8,000-strong Pakistan-border unit. Global stayed 59.
- Signal hygiene: canonical-only clean. Refreshed `pakistan_afghanistan:military_buildup` and `sudan:military_buildup`; maintained `israel_lebanon:ceasefire_violation/diplomacy_active`, `iran_conventional:hormuz_controlled_not_closed`, `israel_palestine:holy_site_tension`, and `iran_nuclear:iaea_emergency`. No non-canonical signals used.
- Source caveat: `web_search`/Tavily unavailable with HTTP 432; used Google News RSS, terminal HTTP/direct-source probes, UN/NATO/EIA/OilPriceAPI/Polymarket fallbacks. IAEA/OPEC direct pages blocked 403; Reuters world direct probe blocked/401.
- Market sanity: OilPriceAPI refreshed during deploy (Brent $80.38, WTI $76.51, gas $3.00, gold $4156.56); Polymarket cache refreshed at `2026-06-20T00:05:40Z`, worst mapped divergence `israel_lebanon` ~99.39pp.
- Deploy verification: `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; JSON files valid; deploy/push succeeded.

## Watch next
- Sudan/El Obeid: whether RSF/SAF offensive starts, spreads, or gains external-state involvement.
- Pakistan-Afghanistan: corroborated cross-border strikes, drone losses, or unit movement after the Taliban border-unit report.
- Israel-Lebanon: distinguish renewed halt from continuing strikes; ceasefire-violation plus diplomacy remains the live pair.
- Iran/Hormuz: watch for physical shipping disruption, transit restrictions turning operational, or oil shock; current evidence says flows rising/resumed.
- Iran/IAEA: verify whether delayed talks produce actual agency access or sanctions snapback.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
