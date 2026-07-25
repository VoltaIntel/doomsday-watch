# Session state — DoomsdayWatch 06Z morning deep scan

- **As of:** 2026-07-25T06:26Z
- **Repository:** `/home/openclaw/.openclaw/workspace/nuke-watch`
- **Branch:** `main`
- **Final commit:** `1cd03df2058c63aaef0ee447be20c6ccb925e9c1` (matches `origin/main`)
- **Pages run:** `30147456556` succeeded for the exact final commit
- **Live URL:** `https://voltaintel.github.io/doomsday-watch/`

## Final risk state
- Global display: **78% / imminent**.
- Unrounded additive coupled score: **78.086%**, up **0.476pp** from the 03Z state; display unchanged.
- Canonical tracker set: **20 IDs** from `data/tracker_config.json`.
- Movers: `eastern_drc` **52→56**, `mali_sahel` **36→39**, `yemen_red_sea` **73→76**, `iran_nuclear` **47 raw / 54 coupled → 49 / 56**.
- Activated canonical signals: `eastern_drc:military_buildup`, `mali_sahel:external_backing`, `yemen_red_sea:ceasefire_violation`.
- Cleared two synthetic deploy-time matches (`iran_nuclear:iaea_access_denied`, `yemen_red_sea:diplomacy_active`) caused by broad negative-review keyword matching. Final tracker/zone/timeline state aligns at **17 canonical signals**.

## Evidence summary
- AFP/BBC: Houthis claim a retaliatory missile strike caused fires in Jizan after Saudi strikes. Saudi civil-defence alerts support a launch-risk event, but Riyadh has not confirmed the claimed fires; movement was discounted.
- CTP: renewed M23/Wazalendo clashes, documented fighter/ammunition reinforcement, and an unverified M23 claim of 9,000+ integrated recruits.
- Bellingcat: geolocated two Shahed-136-type attacks in northern Mali; Russian manufacture is likely but unconfirmed in the Africa Corps context.
- NYT-based reporting: U.S. intelligence assesses Iran’s new leader as more open to pursuing a weapon; no Iranian order or technical nuclear threshold was verified.
- WSJ-based reporting says Kuwait/Bahrain struck Iran earlier in July; anonymous-source and non-border nature kept `kuwait_iraq_border` unchanged.
- No emerging tracker qualified. Nigeria-ISWAP remained claim-heavy; Saudi civil-nuclear and Thailand-Cambodia posture remained watch-only.

## Sanity checks
- Energy: Brent **$98.70 (-1.60%/24h)**, WTI **$85.88 (-6.09%)**, gas **$2.87 (-1.37%)**, gold **$4,055.93 (+0.75%)**. Prices did not set probabilities.
- Exact Polymarket vs 03Z: U.S.-Iran invasion **28.5% (-1.0pp)**, NATO Article 5 **7.0% (flat)**, Iran NPT withdrawal **21.6% (+1.1pp; only ~$158 24h volume)**, Iran nuclear test **9.0% (-1.5pp)**. Markets were sanity-only.

## Source coverage
- `web_search`: **25/25 HTTP 432**; `web_extract`: **3/3 targets HTTP 432**.
- Fallback: **97 Google News RSS lanes / 753 items** (697 in rolling 24h), direct BBC/AFP-syndicated/Bellingcat/NATO/UN/EU NAVFOR/publisher pages, official feeds, terminal HTTP, Jina CTP fallback, OilPriceAPI and exact Gamma.
- IAEA/OPEC/UN Security Council returned 403; UKMTO browser access was Cloudflare-blocked; CTP browser access required Jina. Reindexed U.S. casualty reports from July 18-21 were excluded as new developments.
- Artifacts: `data/morning_deep_scan_sources_20260725T060356Z.json`, `data/deep_scan_exact_followups_20260725T061711Z.json`, `data/polymarket_exact_snapshot_20260725T061320Z.json`.

## Deployment and verification
- Automated deploy commits: `4f4afd32`, corrected signal deploy `a33bc102`; exact metadata commit `1cd03df2`.
- `bash scripts/deploy.sh` succeeded twice; the second run removed synthetic signal matches and pushed.
- Pages run `30147456556` succeeded. Live root/state/timeline returned HTTP 200 and expose 78/imminent, raw 78.086, 20 trackers/news items, 17 aligned signals and exact HTTP-432 fallback metadata.
- Local and live `index.html` contain `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`.
- Canonical IDs/signals, tracker-zone-timeline alignment and JSON checks passed. Tests: **31 passed, 11 deselected**.

## Next watch
- Saudi confirmation, independent impact/casualty evidence, or further Saudi-Houthi launches around Jizan/Yanbu/Hodeida.
- IAEA access, verified 90% enrichment, weaponization order, breakout-hardware movement, atomic detonation, or NPT withdrawal.
- M23 recruit confirmation, new reinforcements/position capture, or direct Rwanda-DRC clash.
- Additional Mali Shahed-type strikes, confirmed Russian operator/manufacture, or JNIM strategic seizure.
- Romania attribution/repeat incursion/casualties or Article 4/5 consultation.
- Formal Hormuz closure/mining/zero traffic, another completed U.S. strike night, or collapse of serious Iran contacts.
- Official M/T Asana status and a distinct fourth Scarborough encounter.
