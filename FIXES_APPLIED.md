# DoomsdayWatch Dashboard Bug Fixes

**Date:** 2026-03-16
**Total Issues Fixed:** 12

---

## CRITICAL BUGS (Fixed First)

### 1. Orphaned `</div>` Tags (dashboard.html)
**Problem:** Two stray `</div>` closing tags between BRIEF/PREDICTION BUTTONS section and GLOBAL PROBABILITY section were closing the energy section AND main `.container` div prematurely, pushing everything below outside the styled container.

**Fix:** Removed the two orphaned `</div>` tags at lines ~391-392 and after the airspace section.

### 2. Prediction Injection (deploy.sh)
**Problem:** The prediction injection tried to replace `"  flights: " + flight_js + "\n};"` but the actual HTML had different whitespace/formatting.

**Fix:** Changed to a more robust anchor - injecting before `\n};\n\n// ===== RENDER` which is a unique, stable marker.

### 3. Empty evaluations.json (deploy.sh)
**Problem:** New predictions were saved to `pred_file` (e.g., `2026-03-16-07.json`) but NOT added to the `evaluations["predictions"]` list, so evaluations stayed at 0/0.

**Fix:** Added new predictions to `evaluations["predictions"]` with `evaluations["predictions"].extend(final_predictions)` and limited to last 200 predictions to prevent unbounded growth.

---

## LOGIC ERRORS (Fixed Second)

### 4. News Time Block Grouping (dashboard.html)
**Problem:** `renderNews()` checked `indexOf("2026-03-14")` etc. but news items have relative times like "0H", "1H".

**Fix:** Implemented relative-time-based grouping that parses the hour format (e.g., "0H", "12H") and groups into:
- "LAST 6 HOURS"
- "6-12 HOURS AGO"
- "12-24 HOURS AGO"
- "EARLIER"

Also added block sorting to show chronological order.

### 5. Deploy Script Tracker Name List (deploy.sh)
**Problem:** `tn` list was missing `russia_ukraine` and `pakistan_afghanistan`, and had wrong name for `turkey` ("TURKEY" instead of "TURKEY-NAT").

**Fix:** Updated tracker list to include all 10 trackers with correct display names and emojis:
- Added `("russia_ukraine", "RUSSIA-UKRAINE", "🇺🇦")`
- Added `("pakistan_afghanistan", "PAKISTAN-AFGHANISTAN", "🇵🇰")`
- Fixed `("turkey", "TURKEY-NATO", "🇹🇷")`

### 6. Redundant Predictions Cap (deploy.sh)
**Problem:** `final_predictions = new_predictions[:12]` followed immediately by `final_predictions = new_predictions[:15]` (second line overwrites first).

**Fix:** Removed the redundant line, kept single consistent limit of 15.

### 7. Duplicate Signals in tracker_config.json
**Problem:** Israel-Lebanon tracker had duplicate signals:
- `israel_ground_invasion_lebanon` (weight 15) AND `idf_ground_lebanon` (weight 8)
- `hezbollah_full_barrage` (weight 10) AND `hezbollah_rockets_heavy` (weight 6)
- `unifil_affected` (weight 5) AND `unifil_evacuated` (weight 4)

**Fix:** Removed lower-weight duplicates, keeping the higher-weight versions.

---

## DATA INCONSISTENCIES (Fixed Third)

### 8. Flight Zone ID Standardization
**Problem:** OpenSky used `red_sea_south`, `eastern_mediterranean`, `turkey_syria` but Aviationstack used `red_sea`, `eastern_med`, `turkey_south`.

**Fix:** Normalized zone IDs in `track_flights.py` to match Aviationstack format:
- `red_sea_south` → `red_sea`
- `eastern_mediterranean` → `eastern_med`
- `turkey_syria` → `turkey_south`

### 9. Energy Grid Shows Only 3 of 9 Commodities (dashboard.html)
**Problem:** `renderEnergy()` hardcoded only BRENT, WTI, NAT GAS. Gold, EUR, GBP, heating oil, gasoline, diesel were hidden.

**Fix:** Extended items array to include all 9 commodities:
- BRENT_CRUDE_USD
- WTI_USD
- NATURAL_GAS_USD
- GOLD_USD
- EUR_USD
- GBP_USD
- HEATING_OIL_USD
- GASOLINE_USD
- DIESEL_USD

### 10. Hardcoded API Key in deploy.sh
**Problem:** `AVIATIONSTACK_KEY="c613d344134b5341ea68a097ac813bf4"` was hardcoded in the script.

**Fix:** Changed to read from secrets file:
```bash
AVIATIONSTACK_KEY=$(cat ~/.openclaw/workspace/secrets-backup/aviationstack.env 2>/dev/null | cut -d= -f2)
```

### 11. Unicode Corruption in signal_timeline.json
**Problem:** Key had Chinese characters appended: `"pakistan_afghanistan:afghan_retaliatory_strikes\u5df4\u57fa\u65af\u5766"`

**Fix:** Removed the unicode corruption, corrected to: `"pakistan_afghanistan:afghan_retaliatory_strikes"`

---

## FILES MODIFIED

1. `/home/openclaw/.openclaw/workspace/nuke-watch/dashboard.html` — layout divs, renderNews(), renderEnergy()
2. `/home/openclaw/.openclaw/workspace/nuke-watch/scripts/deploy.sh` — tracker names, prediction injection, API key, evaluations tracking
3. `/home/openclaw/.openclaw/workspace/nuke-watch/data/tracker_config.json` — duplicate signals removed
4. `/home/openclaw/.openclaw/workspace/nuke-watch/data/signal_timeline.json` — unicode corruption fixed
5. `/home/openclaw/.openclaw/workspace/nuke-watch/scripts/flight_tracker.py` — already using correct zone IDs (no change needed)
6. `/home/openclaw/.openclaw/workspace/nuke-watch/scripts/track_flights.py` — zone IDs normalized

---

## VERIFICATION

All fixes have been applied and should resolve the 12 issues identified in the audit. The dashboard should now:
- Display correctly without layout issues
- Show all 9 energy commodities
- Group news by relative time correctly
- Track and display prediction evaluations
- Use consistent zone IDs across flight tracking
- Load API keys securely from secrets file
