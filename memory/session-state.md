# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-26 15Z morning deep scan, completed and live-verified at 15:16Z.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**, exact fractional-coupling score **79.716%**, up **0.060pp** from 79.656%.

## Probability changes
- `yemen_red_sea`: **84→87 raw/coupled**. Kpler data reported by The National show no new Saudi west-coast crude loaded for Bab al-Mandeb export since the Houthi embargo; Suez exports doubled to 1.06m bpd. Previously loaded Chinese-operated cargoes still crossed, so this is selective disruption—not zero total strait traffic.
- All other probabilities held. `iran_conventional` remains 100, `russia_ukraine` 99, `israel_lebanon` 87 raw/97 coupled, `israel_palestine` 96, `sudan` 92 and `russia` 56 raw/66 coupled.

## Signals
- Activated canonical `iran_conventional:hormuz_mining` after aligned Mehr/Tasnim reports said a route-deviating unnamed tanker struck a naval mine. No vessel identity, casualty report, UKMTO confirmation or independent attribution was available; the capped tracker did not inflate.
- Reactivated canonical `sudan:military_buildup` after Radio Dabanga reported SAF/Joint Force and field-source claims of fierce fighting and captures at Bara, Jabra El Sheikh and Um Sayala. RSF had not responded; Sudan held at 92.
- Refreshed `yemen_red_sea:ceasefire_violation` on a UKMTO-reported close projectile splash and `south_china_sea:external_backing` on the PLA patrol response.
- Pipeline falsely inferred `iran_nuclear:iaea_access_denied` from runner-site availability language; it was removed atomically from state/timeline and the text was neutralized. Final tracker/zone/top-level/timeline projections align at **16 canonical signals**.

## Evidence review
- South China Sea: the PLA Southern Theater Command announced July 25-26 naval/air patrols while condemning the U.S.-Japan-Philippines drill, but called them routine and reported no encounter; score held at 30.
- NATO: Reuters/Guardian corroborated Romania's third intercept and ambassador summons; no Article 4/5 or force-posture step appeared.
- IAEA/UN: the public IAEA page returned 403 from this runner; exact RSS/UN lanes produced no safeguards or weapons threshold.
- Auto-detection: all 22 candidates reviewed; none added. Post-12Z Kenya-Somalia reports repeated the existing Garissa mast/teacher episode, leaving two distinct current episodes. Nigeria returns were a surrender and a foiled attack in separate theaters.

## Sources and markets
- Tavily/web_search: **25/25 HTTP 432**. Tavily extraction: **4/4 HTTP 432**.
- Fallback: **105 Google News RSS lanes / 1,233 raw items**, **20 Bing lanes / 90 items**, browser/direct official and publisher pages, terminal HTTP, OilPriceAPI and Gamma exact-slug reads.
- Limits: IAEA/OPEC/CENTCOM 403; Google times may be indexing/syndication times; Hormuz mining is not independently confirmed; Kpler figures concern Saudi west-coast crude loadings; Sudan gains remain SAF/ally claims.
- Energy: Brent repriced **$98.70→$91.68 (-7.11% vs 12Z)**; WTI held **$85.15**; heating oil **$4.27**.
- Exact markets vs 12Z: U.S.-Iran invasion **19.5%** flat; Iran test **7.5% (-0.5pp)**; NPT withdrawal **17.7% (-0.7pp)**; NATO Article 5 **8.0%** flat; China-Taiwan clash **6.95%** flat. Sanity-only.
- Artifacts: `data/deep_scan_full_rss_20260726T150411Z.json`, `data/polymarket_exact_snapshot_20260726T150411Z.json`, `data/direct_source_checks_20260726T151207Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded; automated commit `d8c827e4` pushed.
- False-signal correction commit `01aee052` pushed; local HEAD equals `origin/main` and tree is clean.
- Exact-head Pages run `30207806154` succeeded.
- Cache-busted live root/state/timeline returned HTTP 200 and exposed **80 / imminent**, raw **79.716**, 20 trackers, 20 news records and 16 aligned signals.
- Required local/live markers present: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON, canonical-ID/signal, tracker-zone-timeline and arithmetic checks passed. **31/31 non-smoke tests passed**.

## Next watch
1. Named-vessel, UKMTO, satellite or independent confirmation of the Hormuz mine strike; casualties, repeat strikes or systematic mining evidence.
2. Formal U.S.-Iran truce/traffic recovery; alternatively, another tanker disable/boarding or verified zero traffic.
3. More Bab al-Mandeb projectile incidents, vessel damage/loss, Saudi retaliation or selective disruption broadening beyond west-coast loadings.
4. NATO Article 4/5 consultation, fourth Romanian incursion, casualties or recovered-drone attribution.
5. RSF confirmation/counteroffensive after the North Kordofan claims; a strategic M23/direct Rwanda-DRC shift.
6. South China Sea encounter after the PLA patrol; verified Iran safeguards/weapons threshold; or a distinct third Kenya-Somalia episode.
