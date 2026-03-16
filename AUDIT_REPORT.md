# DoomsdayWatch Dashboard — Audit Report
**Date:** 2026-03-16  
**Auditor:** Automated code audit  
**Files examined:** `dashboard.html`, `deploy.sh`, `flight_tracker.py`, `data/*.json`

---

## 1. Critical Bugs (Break Functionality)

### 1.1 Orphaned `</div>` Tags Break DOM Structure
- **File:** `dashboard.html`, ~lines 391-392  
- **What's wrong:** Two stray `</div>` closing tags appear between the BRIEF/PREDICTION BUTTONS section and the GLOBAL PROBABILITY section. There are no matching opening divs at that nesting level. These close the energy section AND the main `.container` div prematurely.  
- **Impact:** Everything from GLOBAL PROBABILITY onwards is **outside** the `.container` div. This breaks the centered layout, max-width constraint, and responsive grid. The trackers-grid, news feed, and footer all render unstyled/full-width.  
- **Suggested fix:** Remove the two orphaned `</div>` tags. Ensure `.container` is closed only at the very end of the page.

### 1.2 State Injection String Mismatch (Predictions Never Appear)
- **File:** `deploy.sh`, inside the PYEOF heredoc  
- **What's wrong:** The prediction injection code searches for the string `"  flights: " + flight_js + "\n};"` to replace with predictions appended. However, the state block built earlier uses `"  flights: " + flight_js` followed by a newline then `"};"`. The string concatenation in Python may produce different whitespace than what's actually in `new_html` at that point.  
- **Impact:** If the string match fails, predictions are silently dropped. The PREDICTIONS modal shows "FORECAST UNAVAILABLE" despite data being generated and saved to files.  
- **Suggested fix:** Use a more robust injection method — e.g., inject predictions as a separate `state.predictions = ...` assignment after the state block, rather than trying to append inside it.

### 1.3 `evaluations.json` Predictions List Always Empty
- **File:** `data/predictions/evaluations.json`  
- **What's wrong:** The evaluations file contains `{"predictions": []}` — an empty array. The deploy script loads this, evaluates expired predictions, then writes it back. But since it starts empty and new predictions are saved to per-hour files (not appended here), evaluations never accumulate.  
- **Impact:** The prediction accuracy tracker (`eval_stats`) always shows `0/0 correct (0% accuracy)`. The "TRACK RECORD" display is meaningless.  
- **Suggested fix:** After evaluating expired predictions, save the updated list back to `evaluations.json`. Or load from the per-hour prediction files when evaluating.

---

## 2. Logic Errors (Produce Wrong Results)

### 2.1 Signal `positive` Flag Is Inverted
- **File:** `deploy.sh`, signal data construction  
- **What's wrong:** Signals are marked `"positive": w < 0` (i.e., negative weight = positive signal). In the dashboard's `sigClass()` function, `s.positive` applies CSS class `"signal active positive"` which renders green (de-escalation). This is semantically backwards — the variable name `positive` is confusing. A signal with negative weight (de-escalation) is called "positive" which is correct from a "good news" perspective, but the naming is ambiguous.  
- **Impact:** Visual display is actually correct (green for de-escalation), but any future developer touching this code will be confused. The naming invites bugs.  
- **Suggested fix:** Rename to `s.is_deescalation` or `s.negative_weight` for clarity.

### 2.2 News Time Block Grouping Always Returns "RECENT"
- **File:** `dashboard.html`, `renderNews()` function  
- **What's wrong:** The time block grouping logic checks `timeStr.indexOf("2026-03-14")` and `timeStr.indexOf("2026-03-13")`. But the deploy script injects news items with time values like `"0H"`, `"1H"`, `"2026-03-16"`, or `"2026-03-15"`. Only items with exact date strings get sorted into time blocks. Items with relative time strings ("0H") and current-date items always fall into "RECENT".  
- **Impact:** All news items appear in a single "RECENT" block, defeating the purpose of time-based grouping.  
- **Suggested fix:** Use ISO timestamps for all news items and parse them properly. Or implement relative-time-based grouping.

### 2.3 Deploy Script Tracker Name List Is Stale
- **File:** `deploy.sh`, tracker name tuple list (`tn`)  
- **What's wrong:** The deploy script defines tracker names/emojis in a hardcoded tuple list:
  ```python
  tn = [
      ("iran_nuke", "IRAN NUCLEAR", "🇮🇷"),
      ("iran_conventional", "IRAN WAR", "⚔️"),
      ("israel_lebanon", "ISRAEL-LEBANON", "🇱🇧"),
      ("turkey", "TURKEY", "🇹🇷"),
      ...
  ]
  ```
  But `current_state.json` has tracker `"turkey"` with zone name "TURKEY-NATO" (displayed in zone alerts). The deploy script hardcodes it as "TURKEY". Similarly, `"pakistan_afghanistan"` is auto-detected (not in the list) and gets name `"pakistan afghanistan"` (lowercased/underscored).  
- **Impact:** Zone alert display names are inconsistent. Pakistan-Afghanistan gets a poorly formatted auto-generated name.  
- **Suggested fix:** Read tracker display names from `tracker_config.json` or `current_state.json` instead of hardcoding them.

### 2.4 `russia_ukraine` Missing from Deploy Script Tracker List
- **File:** `deploy.sh`, tracker name tuple  
- **What's wrong:** The `tn` list does NOT include `("russia_ukraine", ...)`. It gets auto-detected via the `known` set check, resulting in name `"russia ukraine"` (lowercase with space) instead of the display name "RUSSIA-UKRAINE".  
- **Impact:** Russia-Ukraine tracker card shows a poorly formatted name.  
- **Suggested fix:** Add `("russia_ukraine", "RUSSIA-UKRAINE", "🇺🇦")` to the tuple list.

### 2.5 Redundant Predictions Cap
- **File:** `deploy.sh`, prediction generation  
- **What's wrong:**
  ```python
  final_predictions = new_predictions[:12]
  final_predictions = new_predictions[:15]  # immediately overrides
  ```
- **Impact:** First line is dead code. Predictions are capped at 15 instead of the apparently intended 12.  
- **Suggested fix:** Remove one of the two lines.

### 2.6 `updateGlobalClock` Ignores State's Pre-computed Zone
- **File:** `dashboard.html`, `updateGlobalClock()`  
- **What's wrong:** The function recalculates the zone from `state.global_war_probability` using `calcZone()` with thresholds {15, 30, 60}. But `state.global_zone` is already computed by the deploy script using the same thresholds. If the thresholds ever diverge, the display and state would disagree.  
- **Impact:** Currently benign (same thresholds), but fragile. If `calcZone()` thresholds change without updating the deploy script (or vice versa), the UI shows one zone while the data says another.  
- **Suggested fix:** Use `state.global_zone` directly instead of recalculating.

---

## 3. Data Inconsistencies (Key Mismatches, Missing Fields)

### 3.1 Flight History Uses Inconsistent Keys Across Entries
- **File:** `data/flight_tracking.json`, `history` array  
- **What's wrong:** Older history entries (from OpenSky `track_flights.py`) use keys `flight_count` and `disruption_pct` with zone IDs like `"persian_gulf"`, `"eastern_mediterranean"`, `"red_sea_south"`, `"red_sea_north"`, `"turkey_syria"`. Newer entries (from Aviationstack `flight_tracker.py`) use keys `active` and `disruption` with zone IDs like `"persian_gulf"`, `"red_sea"`, `"eastern_med"`, `"turkey_south"`, `"iraq"`.  
- **Impact:** Historical chart/trend analysis would need to handle both key formats and zone ID mappings. Currently no code reads this history, but if someone adds charting, it will break.  
- **Suggested fix:** Standardize on one format. Migrate old entries or normalize on read.

### 3.2 Dashboard Energy Section Only Shows 3 of 9 Available Commodities
- **File:** `dashboard.html`, `renderEnergy()`  
- **What's wrong:** The energy grid hardcodes three items: `BRENT_CRUDE_USD`, `WTI_USD`, `NATURAL_GAS_USD`. But `energy_prices.json` also tracks `GOLD_USD`, `EUR_USD`, `GBP_USD`, `HEATING_OIL_USD`, `GASOLINE_USD`, `DIESEL_USD`.  
- **Impact:** Gold at $5,019 (74% above pre-conflict) is a major conflict indicator that's hidden from the dashboard.  
- **Suggested fix:** Either add more commodities to the grid or make it configurable.

### 3.3 Energy Data Missing `changes` for Gasoline and Diesel
- **File:** `data/energy_prices.json`  
- **What's wrong:** The `changes` section only includes `BRENT_CRUDE_USD`, `WTI_USD`, and `NATURAL_GAS_USD`. Gasoline, Diesel, Gold, etc. have no baseline comparison data.  
- **Impact:** If the energy grid were expanded, these commodities would show no change data.  
- **Suggested fix:** Add baselines for all tracked commodities in the `baselines` section.

### 3.4 Tracker Config Has Duplicate Signal Definitions
- **File:** `data/tracker_config.json`, `israel_lebanon` tracker  
- **What's wrong:** Two separate signals cover the same event: `israel_ground_invasion_lebanon` (weight 15) and `idf_ground_lebanon` (weight 8). Both describe IDF ground forces crossing into Lebanon. Similarly, `hezbollah_full_barrage` (weight 10) and `hezbollah_rockets_heavy` (weight 6) both describe heavy rocket barrages.  
- **Impact:** Double-counting of the same event inflates the probability score for Israel-Lebanon. The `active_signals` in `current_state.json` only includes one of each, so the duplicate is dormant — but if both triggered simultaneously, the weight would be 23 instead of 15.  
- **Suggested fix:** Remove duplicate signals. Keep the higher-weight one.

### 3.5 `state.history` Injected But Never Rendered
- **File:** `dashboard.html` (deployed) and `deploy.sh`  
- **What's wrong:** The deploy script injects `history: [...]` (last 48 probability entries) into the state block. But the dashboard's probability chart uses a hardcoded placeholder `<div id="probChart">` that gets replaced by the deploy script with a static SVG. The `state.history` array is loaded into memory but never read by any JavaScript function.  
- **Impact:** Wasted bandwidth (~1-2KB of unused JSON in every page load). Confusing for developers who see history data but no chart using it.  
- **Suggested fix:** Either remove the history injection from the state block, or use `state.history` to render the chart dynamically in JavaScript instead of pre-rendering SVG in the deploy script.

### 3.6 Prediction Limit Double-Cap
- **File:** `deploy.sh`, prediction generation  
- **What's wrong:** The code sets `final_predictions = new_predictions[:12]` then immediately overwrites with `final_predictions = new_predictions[:15]`. The first line is dead code.  
- **Impact:** No functional bug (15 predictions are generated), but indicates confusion about the intended limit.  
- **Suggested fix:** Remove the dead line or change to a single consistent limit.

---

## 3. Data Inconsistencies (Key Mismatches, Missing Fields)

### 3.1 Flight Count Key Name Inconsistency
- **File:** `dashboard.html`, `renderFlights()`  
- **What's wrong:** The rendering code reads `z.active_flights || z.flight_count || 0`. Aviationstack script produces `active_flights`; OpenSky script (`track_flights.py`) produces `flight_count`. The fallback handles both, but the naming inconsistency makes the code fragile.  
- **Impact:** Works correctly due to fallback, but future data sources must know to use one of these exact key names.  
- **Suggested fix:** Normalize to a single key name in both scripts.

### 3.2 Baseline Key Name Inconsistency
- **File:** `dashboard.html`, `renderFlights()`  
- **What's wrong:** Code reads `z.baseline_flights || z.baseline_daily_flights || 0`. Aviationstack uses `baseline_daily_flights`; OpenSky uses `baseline_flights`.  
- **Impact:** Same as above — works due to fallback but fragile.  
- **Suggested fix:** Standardize key name across both scripts.

### 3.3 News Items Have Inconsistent Schema
- **File:** `data/current_state.json`, `latest_news`  
- **What's wrong:** News items in `current_state.json` use keys: `headline`, `source` (string), `text`, `zone`, `signal`, `impact`. The deploy script's enrichment adds: `sources` (array), `source_types`, `confidence`, `severity`, `signals` (array of objects). The dashboard rendering uses the enriched schema but falls back to `n.text || n.headline` and `n.confidence || 'developing'`. Items that don't go through enrichment (e.g., if deploy fails) lack these fields.  
- **Impact:** If deploy script fails partway, some news items render with missing fields. The severity dots and confidence badges may show default values.  
- **Suggested fix:** Ensure all news items are enriched in the deploy script, with sensible defaults for all fields.

---

## 4. Code Quality Issues

### 4.1 `dashboard.html` Contains Stale Hardcoded State
- **File:** `dashboard.html`  
- **What's wrong:** The template file contains a complete hardcoded `const state = {...}` with data from 2026-03-15 and `global_war_probability: 86`. This gets overwritten during deploy, but it's confusing for maintenance and makes the template 3x larger than necessary.  
- **Impact:** Developers editing `dashboard.html` may edit the wrong data. The file is ~400 lines longer than needed.  
- **Suggested fix:** Replace the state block in the template with a minimal placeholder: `const state = /*STATE_INJECTED*/ {};`

### 4.2 Mixed Naming Conventions in Flight Tracking
- **File:** `flight_tracker.py` and `track_flights.py`  
- **What's wrong:** The two flight tracking scripts use different zone identifiers: `eastern_mediterranean` vs `eastern_med`, `red_sea_south`/`red_sea_north` vs `red_sea`, `turkey_syria` vs `turkey_south`. The dashboard can only display zones from the most recent script run.  
- **Impact:** If OpenSky runs (fallback), the dashboard shows different zone names than when Aviationstack runs. History data becomes inconsistent.  
- **Suggested fix:** Define a canonical zone ID mapping that both scripts use.

### 4.3 Shell Script Has Embedded Python (Large Heredoc)
- **File:** `deploy.sh`  
- **What's wrong:** The deploy script contains a ~400-line Python heredoc (PYEOF). This makes the script hard to read, debug, and test. Error handling is minimal — most operations use bare `try/except: pass`.  
- **Impact:** Errors are silently swallowed. Debugging requires adding print statements to a 400-line embedded script.  
- **Suggested fix:** Extract the Python logic to a separate `build_dashboard.py` script. Add proper logging and error reporting.

### 4.4 Signal Timeline Has Unicode Corruption
- **File:** `data/signal_timeline.json`  
- **What's wrong:** The key `"pakistan_afghanistan:afghan_retaliatory_strikes\u5df4\u5766\u57af\u65af\u5766"` contains Chinese characters (巴基斯坦 = "Pakistan") appended to a signal name. This appears to be a data entry error.  
- **Impact:** This malformed key will never match any signal lookup. The associated signal is effectively dead.  
- **Suggested fix:** Remove or correct the malformed key.

### 4.5 No Input Validation on State JSON
- **File:** `deploy.sh`, Python state loading  
- **What's wrong:** The script loads `current_state.json` with `json.load()` but doesn't validate required fields exist. If the JSON is malformed or missing keys, the script crashes with an unhelpful Python traceback.  
- **Impact:** A single corrupted data file prevents all dashboard updates.  
- **Suggested fix:** Add validation: check that `state["trackers"]` exists, has expected keys, and each tracker has `current_probability` and `active_signals`.

### 4.6 Aviationstack API Key Hardcoded in Deploy Script
- **File:** `deploy.sh`, line ~12  
- **What's wrong:** `AVIATIONSTACK_KEY="c613d344134b5341ea68a097ac813bf4"` is embedded in plaintext in the script. While this is in a private workspace, if the repo is ever made public or the script is shared, the key is exposed.  
- **Impact:** API key theft, quota exhaustion, potential billing if the plan is upgraded.  
- **Suggested fix:** Read the key from an environment variable or secrets file only. Remove the hardcoded default.

---

## 5. Security Concerns

### 5.1 XSS Risk: Unsanitized Data Injection
- **File:** `deploy.sh` → `dashboard.html`  
- **What's wrong:** News text, tracker signals, and zone names are injected into the HTML via string concatenation without HTML entity encoding. The deploy script uses `json.dumps()` for some fields (which escapes quotes) but renders others directly. In the dashboard, `innerHTML` is used throughout (e.g., `card.innerHTML = ...`, `feed.innerHTML = ...`). If any data source is compromised, malicious HTML/JS could be injected.  
- **Impact:** Low risk currently (data comes from controlled scripts), but if an external news source or API is compromised, XSS is possible.  
- **Suggested fix:** Use `textContent` instead of `innerHTML` for all user-controllable data. Or sanitize all strings before injection.

### 5.2 API Key in Version-Controlled Script
- **File:** `deploy.sh`  
- **What's wrong:** The Aviationstack API key is committed to the git repository in plaintext.  
- **Impact:** If the GitHub repo is ever made public (or a fork is), the key is exposed.  
- **Suggested fix:** Move to environment variables or a `.env` file excluded by `.gitignore`.

### 5.3 No Content Security Policy
- **File:** `dashboard.html`  
- **What's wrong:** No CSP meta tag or HTTP header. The page loads external resources (Google Fonts, CartoDB tiles, Leaflet CDN) without restriction.  
- **Impact:** If any external resource is compromised, arbitrary code could execute.  
- **Suggested fix:** Add a `<meta http-equiv="Content-Security-Policy" ...>` tag.

---

## 6. Recommendations

### Immediate (Fix Today)
1. **Remove orphaned `</div>` tags** in `dashboard.html` (lines ~391-392) — this is breaking the entire page layout.
2. **Fix prediction injection** in `deploy.sh` — use a more robust method than string replacement.
3. **Add `russia_ukraine` to the deploy script's tracker tuple list** to fix display name.

### Short-Term (This Week)
4. **Extract the Python heredoc** from `deploy.sh` into a standalone `build_dashboard.py` script.
5. **Standardize flight tracking zone IDs and key names** across both flight scripts.
6. **Remove duplicate signals** in `tracker_config.json` (Israel-Lebanon ground invasion and rocket barrage).
7. **Fix the Unicode corruption** in `signal_timeline.json`.
8. **Move the API key** to environment variables.

### Medium-Term (This Month)
9. **Replace hardcoded state** in `dashboard.html` template with a placeholder.
10. **Add state validation** to the deploy script.
11. **Sanitize all injected data** — switch from `innerHTML` to `textContent` where possible.
12. **Add CSP headers** to the dashboard.
13. **Build a probability history chart** that actually uses `state.history` dynamically.
14. **Fix the news time block grouping** to use proper timestamps.

### Long-Term
15. **Consider a proper build system** (Node.js, Hugo, or a Python static site generator) instead of string replacement.
16. **Add unit tests** for the scoring logic (coupling, zone calculation, signal weighting).
17. **Implement prediction evaluation properly** — save evaluated predictions back to the evaluations file.
18. **Create a unified data schema** with validation for all JSON files.

---

## Summary

| Category | Count |
|----------|-------|
| Critical bugs | 3 |
| Logic errors | 6 |
| Data inconsistencies | 6 |
| Code quality issues | 6 |
| Security concerns | 3 |
| **Total issues** | **24** |

**Most urgent:** The orphaned `</div>` tags in `dashboard.html` are breaking the page layout on every deploy. The prediction system is completely non-functional due to injection failures and empty evaluation data. These two issues should be addressed immediately.
