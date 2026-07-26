# Session state — DoomsdayWatch 00Z morning deep scan

- **As of:** 2026-07-26T00:17Z
- **Repository:** `/home/openclaw/.openclaw/workspace/nuke-watch`
- **Branch:** `main`
- **Automated deploy commit:** `276cc3d76135cbaa0f764bfc84062ecc19eb67ca`
- **Exact-metadata/alignment commit:** `782467fc7ac5f875fe9ea36c6f8bd3bfbb2ba73d`
- **Pages run:** `30180878521` completed successfully for the exact commit
- **Live URL:** `https://voltaintel.github.io/doomsday-watch/`

## Final risk state
- Global display: **78% / imminent**.
- Exact weighted coupled score: **78.460%**.
- Canonical tracker set: **20 IDs** from `data/tracker_config.json`.
- No tracker probability moved.
- Deploy temporal decay cleared `iran_conventional:oil_infrastructure_threat`; final tracker/zone/timeline state aligns at **15 canonical signals**.

## Evidence updates
- `iran_conventional`: official DVIDS material and follow-up reporting say a second tanker was disabled and **12 vessels** were redirected under continuing blockade enforcement. The lane remains capped at 100; no mining or zero-traffic threshold was verified.
- `yemen_red_sea`: late Washington Post/wire returns repeat the already-counted Jizan/Yanbu event; no Aramco/SPA outage statement surfaced. Score holds 84.
- `russia`: Ukraine alleged Russian intelligence support for Iran, but this remains one unverified claim chain without direct NATO engagement. Score holds 51 raw / 61 coupled.
- `pakistan_afghanistan`: a fresh-indexed 30-soldier headline was browser-verified as a **March 6** News On AIR article and excluded. Score holds 46.
- No emerging tracker qualified. Kenya-Somalia remains one foiled/repelled event; Saudi nuclear coverage remains civil-policy commentary; other candidates missed the configured three-mention/two-source and distinct-event gate.

## Source coverage
- `web_search`: **25/25 HTTP 432**; `web_extract`: **5/5 HTTP 432**.
- Fallback: **88 Google News RSS lanes / 333 returned items**, Bing News RSS, browser inspection, direct/official NATO/UN/EIA pages and feeds, terminal HTTP, OilPriceAPI and exact Gamma.
- Direct IAEA/CENTCOM/UKMTO/OPEC probes returned 403. Google publication times may be indexing times; Saudi refinery damage, Sudan territorial claims and the Russia-Iran intelligence allegation remain unconfirmed or unquantified.
- Artifacts: `data/morning_deep_scan_sources_20260726T000136Z.json`, `data/deep_scan_full_rss_20260726T000221Z.json`, `data/direct_source_checks_20260726T000415Z.json`, `data/polymarket_exact_snapshot_20260726T000404Z.json`.

## Sanity checks
- Energy after final deploy: Brent **$98.70 (flat cached 24h)**; WTI **$85.15 (-0.85%)**; natural gas **$2.87 (flat)**; gold **$4,055.93 (flat)**. Weekend refined-product values may be stale.
- Exact Polymarket vs 21Z: U.S.-Iran invasion **24.5% (-2.0pp)**; Iran nuke **5.2% (-0.05pp)**; Iran test **8.0% (flat)**; NPT withdrawal **19.65% (-0.1pp)**; NATO Article 5 **7.5% (flat)**; Taiwan invasion **3.85% (flat)**. Markets were sanity-only.

## Deployment and verification
- `bash scripts/deploy.sh` succeeded and pushed `276cc3d7`; exact source metadata and signal alignment were restored atomically and pushed as `782467fc`.
- Pages run `30180878521` succeeded. Cache-busted live root/state/timeline returned HTTP 200 and exposed 78/imminent, raw 78.46, 20 trackers/news records, 15 aligned canonical signals and detailed HTTP-432 fallback metadata.
- Local/live `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`.
- JSON/canonical/timeline/arithmetic checks passed. **31/31 non-smoke tests passed**. HEAD, `origin/main` and remote main match.

## Next watch
- Iran policy/weaponization order, safeguards exclusion, verified Pickaxe operation, weapons-grade activity, detonation or NPT withdrawal.
- Third tanker enforcement action, verified casualties/boarding/diversion, measured Hormuz interruption, mining or zero traffic.
- Official Jizan outage/damage confirmation, another Yanbu/Jizan attack or Saudi retaliation.
- Attribution/third Romanian incursion, casualties or NATO Article 4/5 consultation.
- Independent Sudan recapture confirmation, El Obeid shift, strategic M23 capture or direct Rwanda-DRC clash.
- Fourth Scarborough encounter; M/T Asana rescue/naval action; Abdali reopening/another border attack; actual DPRK launch/test; verified fresh Pakistan-Afghanistan interstate fighting.
