# Session state — DoomsdayWatch 15Z morning deep scan

- **As of:** 2026-07-25T15:34Z
- **Repository:** `/home/openclaw/.openclaw/workspace/nuke-watch`
- **Branch:** `main`
- **Automated deploy commit:** `c4b501013cb6f1b5702632b16d0a3e78530ced5e`
- **Final exact-metadata commit:** `1d4bcf04658fc7e17eca5de6398d5fc4c779bcd9` (matched `origin/main` at verification)
- **Pages run:** `30163834037` completed successfully for the exact final commit
- **Live URL:** `https://voltaintel.github.io/doomsday-watch/`

## Final risk state
- Global display: **78% / imminent**.
- Unrounded additive coupled score: **78.496%**, up **0.040pp** from 12Z; display unchanged.
- Canonical tracker set: **20 IDs** from `data/tracker_config.json`.
- Movers:
  - `yemen_red_sea` **80→84** after Ahram/AFP and Yemeni military sources reported government strikes on Houthi launch sites and depots in Marib and Al-Jawf, alleged fighter deaths, and increased preparedness after the Saudi Aramco attacks.
  - `kuwait_iraq_border` **21→19** after Kuwait committed to reopening Abdali to passenger and trade traffic within 48 hours despite material drone damage.
- Activated canonical `yemen_red_sea:military_buildup`; no signal cleared. Tracker/zone/timeline state aligns at **18 canonical signals**.
- `iran_conventional` remains 100: U.S.-Iran messages and a direct dispute-resolution line continue, but the U.S. blockade, a disabled tanker, the Hormuz-routing dispute, and strike threats remain.
- `russia` holds **51 raw / 61 coupled**. Romania officially confirmed the second F-16 shootdown; the second drone remains unattributed and no Article 4/5 step surfaced.
- No emerging tracker qualified. Saudi nuclear coverage exceeded mention/source counts, but the latest terms explicitly remove enrichment and condition or halt the deal.

## Sanity checks
- Energy: Brent **$98.70 (+1.42%/24h)**, WTI **$85.15 (-3.33%)**, natural gas **$2.87 (-2.38%)**, gold **$4,068.00 (+0.11%)**. Markets did not set probabilities.
- Exact Polymarket vs 12Z: U.S.-Iran invasion **24.5% (-3.0pp)**, NATO Article 5 **7.5% (-0.5pp)**, Iran NPT withdrawal **20.4% (-2.05pp)**, Iran nuclear test **8.5% (flat)**. Markets were sanity-only.

## Source coverage
- `web_search`: **25/25 HTTP 432**; `web_extract`: **5/5 targets HTTP 432**.
- Fallback: **63 Google News RSS lanes / 399 returned items**; the full canonical/emerging set contained **249 unique items**, including **30 after 12Z**. Added exact-title RSS, decoded direct URLs, Jina-assisted extraction, official Romanian Defence/NATO/UN/EIA pages, terminal HTTP, OilPriceAPI and exact Gamma.
- IAEA/OPEC returned 403; OCHA and a UN Sudan feed path returned 404; The National direct extraction returned 503; NewsNation required human verification.
- Artifacts: `data/morning_deep_scan_sources_20260725T150805Z.json`, `data/deep_scan_full_rss_20260725T151147Z.json`, `data/direct_source_checks_20260725T152140Z.json`, `data/polymarket_exact_snapshot_20260725T152253Z.json`.

## Deployment and verification
- `bash scripts/deploy.sh` succeeded, committed and pushed `c4b50101`; exact source-fallback metadata was restored atomically and pushed as `1d4bcf04`.
- GitHub Pages run `30163834037` completed successfully for exact commit `1d4bcf04`.
- Live root/state/timeline returned HTTP 200. Live state exposes **78 / imminent**, raw **78.496**, Yemen **84**, Kuwait-Iraq **19**, and exact fallback metadata.
- Local and live `index.html` contain `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`.
- JSON, canonical IDs/signals, tracker-zone-timeline alignment, 20 news records and weighted arithmetic pass.
- Tests: **31/31 non-smoke passed**. The repository smoke fixture again exceeded its hard-coded 60-second subprocess ceiling; the identical **11/11 assertions passed in 93.29s** from an isolated final-state copy with only that timeout extended to 180 seconds.

## Next watch
- Attribution of Romania's second drone, a third NATO-airspace incursion, casualties, Russian response, or Article 4/5 consultation.
- Further Yemen government-Houthi front-line strikes, Saudi damage/casualty confirmation at Jizan or Yanbu, or a verified refinery outage.
- Actual Abdali reopening, repair completion, claim of responsibility, or another Kuwait/Iraq border drone attack.
- Resumption of U.S. attacks on major Iranian cities, formal Hormuz closure/mining/zero traffic, or collapse of contacts.
- IAEA access change, verified weapons-grade threshold, weaponization order, breakout-hardware movement, atomic detonation, or NPT withdrawal.
- A large Russian strike within the warned 48-hour window, direct NATO entry, or nuclear posture change.
- Wider West Bank mobilization; strategic M23 capture/direct Rwanda-DRC clash; new Mali drones; M/T Asana rescue/naval engagement; a fourth Scarborough encounter.
