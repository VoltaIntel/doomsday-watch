# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-27 00Z morning deep scan, completed and live-verified at 00:21Z.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**, exact fractional-coupling score **79.516%**, unchanged from 21Z.

## Probability and evidence result
- No tracker probability moved. Highest coupled risks remain `iran_conventional` 100, `russia_ukraine` 99, `israel_lebanon` 97, `sudan` 92, `israel_palestine` 92 and `yemen_red_sea` 87.
- AP confirmed a second straight U.S.-Iran pause day, no newly confirmed Strait attack in 72 hours and Hormuz traffic at a three-week low. The U.S. blockade remains: 12 ships redirected, two disabled and two boarded.
- Al Jazeera reported Mojtaba Khamenei conditioned a U.S.-Iran agreement on ending Israeli attacks in Lebanon; the Lebanese army says pilot-zone withdrawals are obstructed while shelling/combing continue.
- UPI's fresh-indexed Romania report was directly opened and confirmed as the already-counted third drone incident, not a fourth.
- SAF control claims for the Omdurman-El Obeid road and named North Kordofan areas remain unverified. No new confirmed Houthi vessel loss or Aramco damage appeared.

## Signals and auto-detection
- Deploy TTL expired old `iran_conventional:diplomacy_active` and `israel_palestine:holy_site_tension` activations. Both were reactivated with current AP negotiations and mosque-burning evidence; net active set is unchanged at **15 canonical signals**.
- Tracker/zone/top-level/timeline projections align at 15 signals.
- All 22 emerging candidates were reviewed; none met the configured three-mention/two-source gate. Bangladesh-Myanmar had one opinion/security item; Syria/Burkina returns were tracked-war query pollution.

## Sources and markets
- Tavily/web_search: **25/25 HTTP 432**. Tavily extraction: **3/3 HTTP 432**.
- Fallback: **90 Google News RSS queries / 288 items**, **23 Bing lanes / 131 items**, browser/direct AP, Al Jazeera, UPI and NATO, UN/EIA official feeds, terminal HTTP, OilPriceAPI and Gamma exact-slug reads.
- Limits: IAEA/OPEC 403; several official press pages failed; Google times may be indexing/syndication times; the Hormuz mine and SAF gains remain unconfirmed.
- Final energy fetch: Brent **$87.36** and WTI **$84.42**. The vendor printed Brent **$91.99** nine minutes earlier, so the move is treated as feed volatility/sanity-only.
- Exact markets vs 21Z: U.S.-Iran invasion 20.5%, Iran nuclear event 5.2%, Iran test 6.0%, NPT withdrawal 15.8%, NATO Article 5 7.5%, Taiwan invasion 3.45%, China-Taiwan clash 6.95% — all flat; thin DPRK invasion rose 0.05pp to 3.30%.
- Artifacts: `data/morning_deep_scan_sources_20260727T000212Z.json`, `data/deep_scan_full_rss_20260727T000321Z.json`, `data/bing_deep_scan_20260727T000626Z.json`, `data/polymarket_exact_snapshot_20260727T000628Z.json`, `data/direct_source_checks_20260727T000806Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded twice (second run preserved fresh signal activation/alignment).
- Automated commits `dac2d76c` and `5f0d2848`; exact provenance correction `c966ce54` pushed.
- Local HEAD equals `origin/main`; tree clean. Exact-head Pages run `30227224133` succeeded.
- Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, raw **79.516**, 20 trackers/news records, 15 aligned signals and exact HTTP-432 fallback metadata.
- Required local/live markers present: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON, canonical-ID/signal, tracker-zone-timeline and fractional arithmetic checks passed. **31/31 non-smoke tests passed**.

## Next watch
1. Signed U.S.-Iran ceasefire, vessel-flow recovery or blockade relief; alternatively renewed strikes, another boarded/disabled vessel or zero Hormuz traffic.
2. Named-vessel/independent confirmation of the Hormuz mine report and mine-clearance activity.
3. Actual Israeli withdrawal timetable for Lebanon pilot zones or renewed mass-casualty Israel-Hezbollah escalation.
4. Independent confirmation/rebuttal of SAF road and North Kordofan control claims.
5. Confirmed Houthi damage to Saudi oil infrastructure, another damaged/sunk vessel or broader Bab al-Mandeb disruption.
6. NATO Article 4/5 consultation, a fourth Romanian incursion, casualties or recovered-drone attribution.
7. Verified Iran safeguards/weapons threshold, Iranian retaliation against Ukraine, or a distinct emerging lane crossing the configured gate.
