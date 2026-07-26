# Session state — DoomsdayWatch 06Z morning deep scan

- **As of:** 2026-07-26T06:25Z
- **Repository:** `/home/openclaw/.openclaw/workspace/nuke-watch`
- **Branch:** `main`
- **Automated deploy commit:** `41b61e2fe2b09951c188f6c20ac15df07df9896a`
- **Exact alignment/source commit:** `70983152a736bff8c336cea7fcb27fd653a8b1d9`
- **Pages run:** `30190957033` completed successfully for the exact commit
- **Live URL:** `https://voltaintel.github.io/doomsday-watch/`

## Final risk state
- Global display: **78% / imminent**.
- Exact additive weighted coupled score: **78.460%**.
- Canonical tracker set: **20 IDs** from `data/tracker_config.json`.
- No tracker probability moved.
- Deploy temporal decay cleared `sudan:infrastructure_strike`; no signal activated.
- Tracker/zone/timeline state aligns at **14 canonical signals**.

## Evidence updates
- `iran_conventional`: a July 26 report quoting CENTCOM confirms a verification boarding of M/T Charminar. The published aggregate remains 12 ships turned back, two disabled and two verification boardings. Score remains capped at 100; no mining or zero-traffic condition was verified.
- U.S.-Iran: Al Jazeera/AP/Reuters report two nights without new U.S. strikes and continued mediated messages, but no agreement. Existing `diplomacy_active` evidence was refreshed.
- `russia_ukraine`: Iran blamed Ukraine for a Caspian vessel strike that killed one and wounded another; Zelensky claimed hits on military-cargo vessels. Score holds 99 near ceiling; no matching canonical signal, direct NATO entry or nuclear-posture shift.
- `yemen_red_sea`: follow-up corroborated the counted Jizan/Yanbu episode and two Greek-operated Patriot interceptions. Saudi damage remains unquantified and Aramco published no outage notice; score holds 84.
- `israel_lebanon`: Reuters confirmed resident return after Israeli withdrawal and Lebanese army deployment in Zawtar al-Gharbiyeh, reinforcing the existing diplomatic pilot without a new combat threshold.
- North Korea: Kyiv cited Ukrainian intelligence claiming preparations for 30,000 more DPRK troops and new launchers in Russia; no independent confirmation or DPRK launch/test was found.
- No emerging tracker qualified. Kenya-Somalia strengthened with a second distinct episode: two sources reported a Garissa mast attack and missing teacher after the Mandera attack. It remains below the three-distinct-event quality gate used with the configured three-mention/two-source minimum.

## Source coverage
- `web_search`: **25/25 HTTP 432**; `web_extract`: **5/5 HTTP 432**.
- Fallback: **91 Google News RSS lanes / 413 items** plus **20 Bing lanes / 162 items**, browser inspection, direct/Jina-backed pages, official NATO/UN/EIA checks, terminal HTTP, OilPriceAPI and exact Gamma.
- 35 Google lane results (27 unique) indexed after 03Z; no Bing result did. Publication times can be indexing/syndication times.
- Direct IAEA remained blocked by HTTP 403/Cloudflare and Jina exposed only verification; OPEC returned 403; OCHA OPT and the UN Sudan feed returned 404. The latest CENTCOM social post was not exposed on the release page, so Charminar details rely on a secondary report carrying a direct CENTCOM quotation.
- Artifacts: `data/morning_deep_scan_sources_20260726T060254Z.json`, `data/deep_scan_full_rss_20260726T060428Z.json`, `data/direct_source_checks_20260726T061037Z.json`, `data/polymarket_exact_snapshot_20260726T061249.json`.

## Sanity checks
- Energy: Brent **$98.70** and WTI **$85.15**, both unchanged from 03Z; natural gas **$2.87**; gold **$4,055.93**. Weekend refined-product values remain stale/thin.
- Exact Polymarket vs 03Z: U.S.-Iran invasion **23.5%**, Iran nuke **5.2%**, Iran test **8.0%**, NPT withdrawal **19.6%**, NATO Article 5 **7.5%**, Taiwan invasion **3.65%** — all flat. The thin DPRK invasion contract eased **0.05pp to 3.25%**. Markets were sanity-only.

## Deployment and verification
- `bash scripts/deploy.sh` succeeded, committing and pushing `41b61e2f`.
- Post-deploy inspection caught a real duplicated-state defect: decay removed `sudan:infrastructure_strike` from timeline/trackers but left it in `zones`. The exact atomic repair also restored contract-required fallback metadata and was pushed as `70983152`.
- Pages run `30190957033` succeeded. Cache-busted live root/state/timeline returned HTTP 200 and exposed 78/imminent, raw 78.46, 20 trackers/news records, 14 aligned canonical signals and exact fallback metadata.
- Local/live `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`.
- JSON, canonical-ID/signal, timeline-alignment and additive-weight arithmetic checks passed. **31/31 non-smoke tests passed**.
- The stock smoke fixture timed out at its fixed 60-second copied-pipeline ceiling, producing 11 setup errors; an isolated copy with only that ceiling extended to 180 seconds passed **11/11 in 73.07s**.
- HEAD, upstream and remote main matched at the exact deployment commit before session logging.

## Next watch
- Iran policy/weaponization order, safeguards exclusion, verified Pickaxe operation, weapons-grade activity, detonation or NPT withdrawal.
- Another tanker disable/boarding with casualties or diversion; measured Hormuz interruption, mining or zero traffic; or a formal U.S.-Iran truce.
- Official Jizan outage/damage confirmation, another Yanbu/Jizan attack, Saudi retaliation or a Bab al-Mandeb closure attempt.
- Attribution/third Romanian incursion, casualties or NATO Article 4/5 consultation.
- Independent confirmation of the 30,000 DPRK troop deployment; a strategic M23 capture/direct Rwanda-DRC clash; or a new Sudan territorial shift.
- Confirmed Abdali reopening/another border attack; a third distinct Kenya-Somalia episode; M/T Asana rescue/naval action; actual DPRK launch/detonation.
