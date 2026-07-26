# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-26 09Z morning deep scan, completed and live-verified at 09:20Z.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **79% / imminent**, exact pipeline score **78.516%**, up **0.020pp** from 78.496%. The display crossed 78→79 solely because the exact fractional-coupling score passed the rounding boundary.

## Probability changes
- `south_china_sea`: **27→30** raw/coupled. Reuters reported U.S., Japanese and Philippine ships, coast guard units, surveillance aircraft and fighters completed five days of South China Sea exercises amid the Second Thomas and Scarborough confrontations.
- `kuwait_iraq_border`: **19→17** raw/coupled. Reuters, citing Iraq's border authority, confirmed Abdali reopened to passenger and commercial traffic after the drone strike caused material damage but no casualties.
- All other tracker probabilities held. `iran_conventional` remains 100/100; `russia_ukraine` 99/99; `israel_palestine` 96/96; `sudan` 92/92; `israel_lebanon` 81/91; `yemen_red_sea` 84/84.

## Signals
- Activated canonical `south_china_sea:external_backing`.
- Deploy temporal decay cleared `israel_lebanon:ceasefire_violation` and `yemen_red_sea:infrastructure_strike`.
- Refreshed `iran_conventional:diplomacy_active`: Iran said Oman talks made progress on Hormuz safe-passage mechanisms while explicitly saying traffic had not changed.
- Final tracker/zone/top-level/timeline projections align at **13 canonical signals**.

## Evidence review
- Iran/Oman: AA directly exposed the Foreign Ministry statement on productive safe-passage consultations; no formal truce, mining, zero traffic or new boarding was verified.
- NATO/allied: official NATO latest-news still led with the 24 July Qatar solidarity visit; no new Article 4/5 or Romania collective-response step. The trilateral South China Sea exercise supplied concrete allied backing.
- IAEA/UN: IAEA direct access remained Cloudflare-blocked and exact RSS lanes produced no fresh technical/safeguards threshold. UN feeds contained no newer operational measure.
- DPRK: the alleged 30,000 additional troop transfer gained syndication but no independent confirmation; no launch/test signal activated.
- Auto-detection: all 22 candidates reviewed; none added. Fresh Syria-lane items were misclassified Iran stories; Saudi-nuclear items concerned a civil pact; one Myanmar soldier plus two police crossing into Bangladesh was below the sustained-crisis threshold. Kenya-Somalia remains at two distinct episodes, below the three-event quality gate.

## Sources and markets
- Tavily/web_search: **25/25 HTTP 432**. Tavily extraction: **5/5 HTTP 432**.
- Fallback: **91 Google News RSS lanes / 404 items**, **20 Bing lanes / 163 items**, browser/direct/Jina pages, official NATO/UN/EIA checks, terminal HTTP, OilPriceAPI and Polymarket Gamma exact slugs.
- Limitations: IAEA Cloudflare; OPEC 403; OCHA OPT and UN Sudan feed 404; Reuters direct DataDome (syndications used); CENTCOM release page did not expose latest social posts. Google dates may be index/syndication times.
- Oil: Brent **$98.70**, WTI **$85.15**, both flat vs 06Z; no newly verified sustained physical supply loss.
- Exact markets vs 06Z: key Iran, NATO and Taiwan contracts flat; thin DPRK invasion **3.30% (+0.05pp)**. Markets remained sanity-only.
- Artifacts: `data/morning_deep_scan_sources_20260726T090240Z.json`, `data/deep_scan_full_rss_20260726T090421Z.json`, `data/direct_source_checks_20260726T091017Z.json`, `data/polymarket_exact_snapshot_20260726T090902Z.json`.

## Deploy and verification
- `bash scripts/deploy.sh` succeeded; automated commit `8d52860b` pushed.
- Post-deploy duplicate-signal/global-score alignment commit `21edc987` pushed and equals `origin/main` at verification.
- GitHub Pages run `30196225476` succeeded for `21edc987`.
- Cache-busted live root/state/timeline returned HTTP 200 and exposed **79 / imminent**, raw **78.516**, 20 trackers, 20 news records, 13 aligned signals and exact fallback metadata.
- Required local and live command-deck markers present: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON, canonical-ID/signal, tracker-zone-timeline and arithmetic checks passed. **31/31 non-smoke tests passed**.

## Next watch
1. Formal U.S.-Iran truce or published Hormuz transit mechanism; alternatively, a boarding/disable, mining or zero traffic.
2. New South China Sea confrontation after the allied exercise, casualty/vessel loss, Chinese counter-exercise or treaty consultation.
3. Iranian safeguards exclusion, weapons-grade production, weaponization order, detonation or NPT withdrawal.
4. Official Jizan damage/outage, another Yanbu/Jizan attack, Saudi retaliation or Bab al-Mandeb closure attempt.
5. Romania attribution, third NATO-airspace incursion, casualty or Article 4/5 consultation.
6. Independent DPRK troop confirmation; strategic M23/direct Rwanda-DRC shift; Sudan territorial shift; another Abdali strike; or a third Kenya-Somalia episode.
