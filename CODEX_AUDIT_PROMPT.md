You are auditing and debugging the "nuke-watch" / DoomsdayWatch project — a real-time geopolitical conflict escalation monitor.

PROJECT STRUCTURE:
- scripts/pipeline.py — main pipeline: signal processing, probability calc, coupling, dashboard rebuild
- scripts/deploy.sh — bash wrapper that calls pipeline.py inline
- scripts/flight_tracker.py — OpenSky flight tracking (airspace closures)
- scripts/fetch_oil_prices.py — oil/energy price fetching (OilPriceAPI + Yahoo fallback)
- data/update_state.py — cron agent state updater
- dashboard.html — full dashboard with JS (1949 lines, 70KB)
- index.html — deployed copy of dashboard
- data/tracker_config.json — signal weights, base rates, coupling rules
- data/current_state.json — live state (trackers, signals, news)
- data/signal_timeline.json — signal activation timestamps
- data/source_credibility.json — source tier classification
- data/predictions/ — hourly prediction JSON files + evaluations.json
- lib/ — Leaflet.js for map

EXISTING AUDIT FINDINGS (from AUDIT_REPORT.md):
1. Orphaned </div> tags in dashboard.html ~lines 391-392 break DOM structure
2. State injection string mismatch — predictions never appear in dashboard
3. evaluations.json predictions list always empty — track record shows 0/0
4. Signal positive flag is semantically inverted (w < 0 = positive = good news)
5. News time block grouping always returns "RECENT"
6. Stale tracker name list — auto-detected trackers get ugly names
7. Redundant predictions cap (12 then 15)
8. updateGlobalClock ignores pre-computed zone

FROM POST_MORTEM.md:
- Stale notes don't match auto-calculated numbers
- No-news decay uses median (improved from newest)
- Confidence dimension added

YOUR TASK — DO A COMPLETE A-to-Z AUDIT:

1. READ every file in the project
2. Find ALL bugs — syntax errors, logic errors, broken imports, dead code, race conditions
3. Find security issues (API key handling, injection risks in HTML)
4. Check all JSON data files for consistency
5. Check the dashboard.html for JS errors, broken DOM, missing event handlers
6. Check coupling logic for correctness
7. Check prediction evaluation pipeline
8. Identify missing error handling
9. Suggest concrete enhancements for both the bot logic AND the dashboard
10. Write a comprehensive report to AUDIT_REPORT_V2.md in the project root

For enhancements, suggest:
- Dashboard UX improvements
- New data sources or signals
- Better probability calibration
- Mobile responsiveness
- Alert/notification system
- Historical trend visualization
- Prediction accuracy tracking

Be thorough. This is a production monitoring system. Read every file. Fix what you can. Report everything.
