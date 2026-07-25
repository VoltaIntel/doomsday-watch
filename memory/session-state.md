# Session state — DoomsdayWatch 18Z morning deep scan

- **As of:** 2026-07-25T18:14:50Z
- **Repository:** `/home/openclaw/.openclaw/workspace/nuke-watch`
- **Branch:** `main`
- **Automated deploy commit:** `80013144545fc954edac33cea81ba42255949c58`
- **Exact-metadata commit:** `6a645c53e400bc229f442d4af354ee9007e787aa`
- **Pages run:** `30169245393` completed successfully for the exact-metadata commit
- **Live URL:** `https://voltaintel.github.io/doomsday-watch/`

## Final risk state
- Global display: **78% / imminent**.
- Exact current weighted coupled score: **78.460%**. This normalizes inherited metadata from 78.496 to the reproducible sum of current coupled tracker values times configured weights; no tracker probability moved.
- Canonical tracker set: **20 IDs** from `data/tracker_config.json`.
- No canonical signal activated or cleared. Tracker/zone/timeline state aligns at **18 canonical signals**.
- Evidence-only updates:
  - `iran_conventional`: UKMTO Advisory 096-26 reports a tanker-military-forces incident in the Gulf of Oman, but gives no attack, damage, casualty or attribution. Score remains capped at **100**.
  - `russia_ukraine`: Ukraine reported deep strikes on the Tyumen refinery, a Russian warship and vessels it says support Iran-linked military cargoes. Score remains **99** without direct NATO entry or a nuclear-posture change.
- No emerging tracker qualified. Kenya-Somalia reporting resolved to two current source chains, below the configured three-mention/two-source gate; Syria material was a UN visit or wider Gulf-war spillover.

## Sanity checks
- Latest energy after deploy: Brent **$98.70 (+0.47%/24h)**, WTI **$85.15 (-4.16%)**, natural gas **$2.87 (flat)**, gold **$4,055.93 (-0.20%)**. Markets did not set probabilities.
- Exact Polymarket vs 15Z: U.S.-Iran invasion **25.5% (+1.0pp)**, NATO Article 5 **7.5% (flat)**, Iran NPT withdrawal **20.45% (+0.05pp)**, Iran nuclear test **8.5% (flat)**, Taiwan invasion **3.85% (-0.1pp)**. Sanity-only.

## Source coverage
- `web_search`: **25/25 HTTP 432**; `web_extract`: **3/3 targets HTTP 432**.
- Fallback: **68 Google News RSS lanes / 361 returned items**, exact-event Google/Bing RSS, browser, direct pages, Jina-assisted UKMTO/Al Arabiya extraction, official NATO/UN/EIA pages and feeds, terminal HTTP, OilPriceAPI and exact Gamma.
- IAEA, OPEC and CENTCOM direct probes returned 403. UKMTO did not identify the forces; Saudi facility damage remains unquantified; several Yemen battlefield claims are belligerent/aligned-source reporting.
- Artifacts: `data/morning_deep_scan_sources_20260725T180318Z.json`, `data/deep_scan_full_rss_20260725T180338Z.json`, `data/direct_source_checks_20260725T180351Z.json`, `data/polymarket_exact_snapshot_20260725T180551Z.json`.

## Deployment and verification
- `bash scripts/deploy.sh` succeeded and pushed `80013144`; exact source-fallback metadata was restored atomically and pushed as `6a645c53`.
- Pages run `30169245393` succeeded. Live root/state returned HTTP 200 and exposed **78 / imminent**, raw **78.46**, 20 trackers/news records and exact fallback metadata.
- Local/live `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`.
- JSON, canonical IDs/signals, tracker-zone-timeline alignment, weighted arithmetic and **31/31 non-smoke tests** passed.

## Next watch
- UKMTO identification/update: attack, damage, casualties, boarding, diversion or a verified transit interruption.
- Attribution of Romania's second drone, third NATO-airspace incursion, casualty, Russian response or Article 4/5 consultation.
- Further Ukrainian deep-refinery/maritime strikes; the warned large Russian strike; direct NATO entry or nuclear-posture change.
- More Yemen front-line strikes; Saudi Jizan/Yanbu damage/casualty confirmation or verified refinery outage.
- Abdali reopening/repair completion or another Kuwait/Iraq-border attack.
- IAEA access, weapons-grade activity, weaponization, breakout hardware, detonation or NPT withdrawal.
- Wider West Bank escalation; third independent Kenya-Somalia report; strategic M23 capture/direct Rwanda-DRC clash; new Mali drones; M/T Asana rescue/naval engagement; fourth Scarborough encounter.
