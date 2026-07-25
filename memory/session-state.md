# Session state — DoomsdayWatch 21Z morning deep scan

- **As of:** 2026-07-25T21:20Z / 2026-07-26 local run date
- **Repository:** `/home/openclaw/.openclaw/workspace/nuke-watch`
- **Branch:** `main`
- **Automated deploy commit:** `8ba20e5ca4dc9c05e97bdb79a5efbea53d9ad09c`
- **Exact-metadata/alignment commit:** `559fb21824ef6ac31ffc29957741952c6aedef7b`
- **Pages run:** `30175360128` completed successfully for the exact commit
- **Live URL:** `https://voltaintel.github.io/doomsday-watch/`

## Final risk state
- Global display: **78% / imminent**.
- Exact weighted coupled score: **78.460%**.
- Canonical tracker set: **20 IDs** from `data/tracker_config.json`.
- No tracker probability moved. Fresh Iran-nuclear syndication repeats the preliminary Mojtaba intent assessment already counted in the 06Z increase to 49 raw / 56 coupled.
- Deploy temporal decay cleared `iran_conventional:hormuz_controlled_not_closed` and `iran_conventional:military_buildup`.
- Pipeline falsely matched `north_korea:missile_range_test` from a launcher-transfer claim; the synthetic signal was removed and the text rewritten. Final tracker/zone/timeline alignment is **16 canonical signals**.
- No emerging tracker qualified. Kenya-Somalia reports describe the same repelled/foiled event; Saudi civil-nuclear coverage does not establish weaponization or unsafeguarded operation.

## Evidence updates
- `iran_conventional`: PBS/USNI reported another tanker disabled during U.S. blockade enforcement; Iranian-media claims of two crew deaths remain independently unverified. Score remains capped at 100.
- `yemen_red_sea`: Reuters verified smoke toward Jizan and cited trading sources reporting some damage; Yanbu-bound missiles were reportedly intercepted and no official refinery outage was announced. Score holds 84.
- `sudan`: local/regional reports claim army/allied recaptures in North Kordofan; independent confirmation is absent. Score holds 92.
- `russia_ukraine`: additional reciprocal strikes caused deaths, without direct NATO entry or nuclear-posture change. Score holds 99.

## Source coverage
- `web_search`: **25/25 HTTP 432**; `web_extract`: **5/5 HTTP 432**.
- Fallback: **88 Google News RSS lanes / 353 returned items**, Bing News RSS, browser/direct/Jina checks, official NATO/UN/EIA pages and feeds, terminal HTTP, OilPriceAPI and exact Gamma.
- Direct IAEA/OPEC/CENTCOM probes returned 403. Google browser search hit a bot challenge. Several claims remain belligerent, secondary, stale-indexed or unquantified.
- Artifacts: `data/morning_deep_scan_sources_20260725T210146Z.json`, `data/deep_scan_full_rss_20260725T210302Z.json`, `data/direct_source_checks_20260725T210557Z.json`, `data/polymarket_exact_snapshot_20260725T210722Z.json`.

## Sanity checks
- Energy: Brent **$96.78 (-1.51%/24h)**; WTI **$85.15 (-5.91%)**; natural gas **$2.87 (-0.69%)**; gold **$4,055.93 (flat)**.
- Exact Polymarket vs 18Z: U.S.-Iran invasion **26.5% (+1.0pp)**; Iran nuke **5.25% (flat)**; Iran test **8.0% (-0.5pp)**; NPT withdrawal **19.75% (-0.7pp)**; NATO Article 5 **7.5% (flat)**; Taiwan invasion **3.85% (flat)**. Markets were sanity-only.

## Deployment and verification
- `bash scripts/deploy.sh` succeeded and pushed `8ba20e5c`; exact source metadata and signal alignment were restored atomically and pushed as `559fb218`.
- Pages run `30175360128` succeeded. Live root/state/timeline returned HTTP 200 and exposed 78/imminent, raw 78.46, 20 trackers/news records, 16 aligned canonical signals and detailed fallback metadata.
- Local/live `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`.
- JSON/canonical/timeline/arithmetic checks passed. **31/31 non-smoke tests passed**. The stock smoke fixture hit its fixed 60-second copied-pipeline timeout; an isolated copy with only that timeout extended passed **11/11 in 79.13s**.

## Next watch
- Iran policy/weaponization order, verified Pickaxe operations or inspector-access change, weapons-grade activity, detonation or NPT withdrawal.
- Another tanker enforcement action, verified casualties/boarding/diversion or material Hormuz traffic interruption.
- Official Jizan damage/outage confirmation, another Yanbu/Jizan attack or Saudi retaliation.
- Attribution/third Romanian incursion, casualties or NATO Article 4/5 consultation.
- Independent Sudan recapture confirmation, El Obeid shift, strategic M23 capture or direct Rwanda-DRC clash.
- Fourth Scarborough encounter; M/T Asana rescue/naval action; Abdali reopening or another border attack; corroborated DPRK transfer or actual launch/test.
