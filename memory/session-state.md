# DoomsdayWatch Session State

## Last completed scan
- **Run:** 2026-07-27 15Z morning deep scan, completed and live-verified at 15:21Z.
- **Canonical scope:** all 20 tracker IDs from `data/tracker_config.json`, plus oil/energy, IAEA/UN, NATO/allied positions, exact-slug Polymarket sanity and 22 emerging-crisis candidates.
- **Global:** **80% / imminent**; exact fractional-coupling score **79.696%**, up **0.120pp** from 12Z.

## Probability and evidence result
- **Top mover:** `russia` **56→58 raw / 66→68 coupled**. Romania's defence ministry reported a drone briefly entered Romanian airspace on a fourth consecutive day; two F-16s scrambled, but it returned toward Ukraine and was not shot down. Romania then summoned Russia's ambassador, expelled an embassy employee and recalled its own ambassador after Russian-origin debris attribution. NATO announced no Article 4/5 action.
- `iran_conventional` remains capped at **100**. Reuters reported Saudi Arabia, Jordan and Iraq recorded drone attacks during the direct U.S.-Iran pause; Saudi Arabia attributed some petroleum-targeting drones to an Iran-backed Iraqi militia. Iranian state media claimed six unauthorized ships were turned back in Hormuz. A third strike-free night and Oman mediation continue, but no direct U.S.-Iran talks are underway.
- `yemen_red_sea` remains **87**. Houthis claimed a fresh attempt against Yanbu-linked transit sites and Reuters reported reduced Bab el-Mandeb traffic, but no new damage or vessel loss was verified.
- `southern_thailand` remains **25**. Four gunmen wounded an off-duty police sergeant in Pattani; the expanded security dragnet confirms persistence, not a strategic shift.
- All 22 emerging candidates were reviewed. Myanmar remains one Reuters/ACLED reporting chain; no candidate crossed the configured three-mention/two-independent-source gate.

## Signals
- No evidence-backed canonical signal activated or cleared.
- Evidence refreshed for `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `yemen_red_sea:ceasefire_violation` and `southern_thailand:military_buildup`.
- Deploy briefly introduced the contextual false match `north_korea:nuclear_test`; it was removed atomically from tracker, zone, top-level and timeline projections and the triggering wording was corrected.
- Final tracker, zone, top-level and timeline projections align at **16 canonical signals**.

## Per-tracker table
| Tracker | Raw | Coupled | Zone | Active signals |
|---|---:|---:|---|---|
| `iran_conventional` | 100 | 100 | imminent | `ceasefire_violation`, `diplomacy_active`, `hormuz_controlled_not_closed`, `hormuz_mining`, `military_buildup` |
| `israel_lebanon` | 87 | 97 | imminent | `ceasefire_violation` |
| `turkey` | 5 | 5 | deterrent | — |
| `india` | 15 | 15 | elevated | — |
| `russia` | 58 | 68 | imminent | — |
| `china` | 24 | 28 | critical | — |
| `north_korea` | 18 | 18 | elevated | — |
| `russia_ukraine` | 99 | 99 | imminent | — |
| `pakistan_afghanistan` | 46 | 46 | critical | — |
| `iran_nuclear` | 49 | 56 | imminent | — |
| `sudan` | 94 | 94 | imminent | `military_buildup` |
| `israel_palestine` | 92 | 92 | imminent | `diplomacy_active`, `holy_site_tension`, `military_buildup` |
| `south_sudan_abyei` | 19 | 19 | elevated | — |
| `eastern_drc` | 56 | 56 | imminent | `military_buildup` |
| `yemen_red_sea` | 87 | 87 | imminent | `ceasefire_violation`, `military_buildup` |
| `mali_sahel` | 39 | 39 | critical | `external_backing` |
| `south_china_sea` | 30 | 30 | critical | `external_backing` |
| `somalia_gulf_of_aden` | 28 | 28 | critical | — |
| `southern_thailand` | 25 | 25 | critical | `military_buildup` |
| `kuwait_iraq_border` | 17 | 17 | elevated | — |

## Sources and markets
- Tavily failed **25/25 searches + 5/5 extracts** with HTTP 432.
- Fallback: **78 Google News RSS queries / 778 items**, **24 Bing lanes / 137 items**, browser/direct Reuters syndication, Romanian defence/foreign-ministry reporting, NATO/UN checks, terminal HTTP/text extraction, OilPriceAPI and exact Gamma.
- Limits: IAEA/OPEC 403; OCHA/configured UN Sudan paths 404; Google browser search hit CAPTCHA and Bing browser search a Cloudflare challenge; RSS dates can be indexing/syndication times.
- Final deploy OilPriceAPI: Brent **$89.70** (-1.64%/24h; +$1.35 vs 12Z), WTI **$83.67** (-1.74%; -$0.05).
- Exact markets: U.S.-Iran invasion **21.5%**, Iran event **5.15%**, Iran test **5.5%**, NPT withdrawal **15.85%** (+0.05pp), NATO Article 5 **7.5%**, Taiwan invasion **3.65%**, China-Taiwan clash **6.30%** (+0.10pp), DPRK invasion **3.05%** (+0.15pp), Israel-Lebanon normalization **12.5%**. Markets did not set scores.
- Artifacts: `data/deep_scan_full_rss_20260727T150241Z.json`, `data/bing_deep_scan_20260727T150241Z.json`, `data/deep_scan_summary_20260727T150241Z.json`, `data/direct_source_checks_20260727T150241Z.json`, `data/polymarket_exact_snapshot_20260727T150704Z.json`.

## Deploy and verification
- Required `bash scripts/deploy.sh` succeeded twice; final exact energy correction/pipeline commit: `6ab1c50b`.
- GitHub Pages run `30279475126` succeeded for `6ab1c50b`.
- Cache-busted live root/state/timeline returned HTTP 200 and expose **80 / imminent**, exact **79.696**, Russia **58/68**, 20 trackers/news records and 16 aligned signals.
- Required local/live markers are present: `DoomsdayWatch // Command Deck`, `const state = {`, `// ===== RENDER`.
- JSON/canonical/timeline/fractional checks pass; **31/31 non-smoke assertions** passed. No command-deck HTML was hand-edited.
- Data HEAD matched `origin/main` and the repository tree was clean before this session-summary update.

## Next watch
1. A fifth Romanian incursion, casualties, recovered-drone attribution, Russian retaliation to the diplomatic expulsion or NATO Article 4/5 consultation.
2. Direct U.S.-Iran talks, a signed arrangement or verified Hormuz vessel-flow recovery; alternatively resumed direct strikes or an operational order tied to moving U.S. assets.
3. Further Saudi/Jordan/Iraq drone attacks, verified attribution to Iran or its proxies, Saudi retaliation or confirmed petroleum-infrastructure damage.
4. Implementation of an Iran-Oman transit mechanism, blockade relief, mine-clearance activity or verified zero commercial traffic.
5. Independent confirmation of Sudan highway control, an RSF counterattack or sustained humanitarian access.
6. Verified movement of additional North Korean troops or launchers, a DPRK missile/device event or an allied countermeasure.
7. Another damaged/sunk Red Sea vessel, verified Saudi oil damage or a material Bab el-Mandeb traffic shift.
8. An emerging crisis crossing the configured three-mention/two-independent-source gate.
