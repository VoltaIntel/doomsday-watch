# Session state — DoomsdayWatch 12Z morning deep scan

- **As of:** 2026-07-25T12:19Z
- **Repository:** `/home/openclaw/.openclaw/workspace/nuke-watch`
- **Branch:** `main`
- **Final commit:** `caabae7bea46fb417ff052bcc2820868affb479b` (matches `origin/main`)
- **Pages run:** `30157783387` for the exact final commit remained **queued** as of the last check; the prior automated run `30157712962` was cancelled when the exact-metadata commit superseded it
- **Live URL:** `https://voltaintel.github.io/doomsday-watch/`

## Final risk state
- Global display: **78% / imminent**.
- Unrounded additive coupled score: **78.456%**, up **0.370pp** from 06Z; display unchanged.
- Canonical tracker set: **20 IDs** from `data/tracker_config.json`.
- Movers:
  - `russia` **47 raw / 57 coupled → 51 / 61** after Romania downed a second drone in two days; Friday wreckage was identified as Russian, while Saturday origin remains under analysis.
  - `yemen_red_sea` **76→80** after Reuters verified smoke near the Jizan Aramco refinery and Greek sources confirmed interception of projectiles aimed at Yanbu refineries; Saudi damage confirmation remains incomplete.
  - `israel_palestine` **95→96** after Reuters and Al Jazeera documented dozens detained, about 70 Tal homes raided and village movement curtailed during the expanded West Bank operation.
- No canonical signal activated or cleared. Tracker/zone/timeline state remains aligned at **17 canonical signals**.
- The first U.S.-Iran night without a new strike announcement after 13 consecutive nights is a meaningful diplomatic pause, but Washington retained explicit strike threats and the already-realized `iran_conventional` lane remains capped at 100.
- No emerging tracker qualified.

## Sanity checks
- Energy: Brent **$98.70 (+0.86%/24h)**, WTI **$85.15 (-5.24%)**, gas **$2.87 (-1.37%)**, gold **$4,055.93 (+0.08%)**. Markets did not set probabilities.
- Exact Polymarket vs 06Z: U.S.-Iran invasion **27.5% (-1.0pp)**, NATO Article 5 **8.0% (+1.0pp)**, Iran NPT withdrawal **22.45% (+0.85pp; about $195 reported 24h volume)**, Iran nuclear test **8.5% (-0.5pp)**. Markets were sanity-only.

## Source coverage
- `web_search`: **25/25 HTTP 432**; `web_extract`: **5/5 targets HTTP 432**.
- Fallback: **45 Google News RSS lanes / 333 items / 297 unique**, 64 unique items after the 06Z cutoff, targeted exact-event RSS, accessible Reuters syndication, direct ABC/Al Jazeera/Euronews/Gulf News/Daily Sabah pages, official UN/SPA checks, terminal HTTP, OilPriceAPI and exact Gamma.
- IAEA/OPEC/Allied Air Command/CENTCOM/U.S. Defense returned 403; Al Arabiya required a security check; the EU NAVFOR newsroom path returned 404; SPA bodies were not extractable.
- Artifacts: `data/morning_deep_scan_sources_20260725T120443Z.json`, `data/deep_scan_exact_followups_20260725T120703Z.json`, `data/official_source_checks_20260725T120930Z.json`, `data/polymarket_exact_snapshot_20260725T120924Z.json`.

## Deployment and verification
- Automated deploy commit: `7c6193be`; exact source-fallback metadata commit: `caabae7b`.
- `bash scripts/deploy.sh` succeeded and pushed; local HEAD equals `origin/main` and the tree was clean before session-summary logging.
- Exact-commit Pages run `30157783387` remained queued after more than ten minutes. Do not claim live final-state deployment until it completes.
- Local `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`.
- JSON, canonical IDs/signals, tracker-zone-timeline alignment and weighted arithmetic pass.
- Tests: **31/31 non-smoke passed**. The repository smoke fixture hit its hard-coded 60-second subprocess ceiling; the identical **11/11 assertions passed in 88.49s** from an isolated final-state copy with only that harness timeout extended.

## Next watch
- Romanian wreckage attribution, a third NATO-airspace incursion, casualties, Russian response, or Article 4/5 consultation.
- Saudi damage/casualty confirmation at Jizan or Yanbu, additional Saudi-Houthi launches, or a verified refinery outage.
- Further West Bank mass arrests, village closures, additional killings, settlement acceleration, or a wider armed uprising.
- Resumption of U.S.-Iran strikes, formal Hormuz closure/mining/zero traffic, or collapse of current contacts.
- IAEA access change, verified weapons-grade threshold, weaponization order, breakout-hardware movement, atomic detonation, or NPT withdrawal.
- Independent M23 recruit confirmation, strategic capture, or direct Rwanda-DRC clash; additional Mali Shahed-type strikes or confirmed Russian operator role.
- Official M/T Asana rescue/naval-engagement update or a distinct fourth Scarborough encounter.
