# DoomsdayWatch / Nuke-Watch Audit V2

Date: 2026-04-05
Auditor: Codex
Scope: full repo audit of scripts, HTML, JSON/data, docs, and generated artifacts in the project root

## Executive Summary

The system is operational, but it had several production-affecting correctness and safety problems. During this audit I fixed the highest-confidence issues in the deploy path, dashboard rendering, signal timeline hygiene, prediction evaluation plumbing, and state synchronization. The project now rebuilds cleanly through `scripts/pipeline.py`, the dashboard HTML/JS validates, the signal timeline has been pruned back to configured signals, tracker timestamp drift has been repaired, and the pipeline no longer auto-commits or pushes unless explicitly enabled by the deploy wrapper.

The biggest remaining risks are not syntax errors. They are stale-state corruption from `data/update_state.py`, a split and inconsistent `flight_tracking.json` schema caused by two writers, fragile string-based dashboard generation in `scripts/pipeline.py`, and broad exception swallowing that can hide real production failures.

Current post-audit runtime snapshot:
- Global probability: `30%`
- Global zone: `critical`
- Trackers: `10`
- Latest news items in `current_state.json`: `6`
- Current dashboard predictions: `10`
- Evaluation corpus in `data/predictions/evaluations.json`: `2000`
- Evaluated predictions: `1970`
- Correct predictions: `1239`
- Exact evaluated accuracy: `62.89%`
- Current records still missing evaluation metadata: `200`
- Archived predictions missing evaluation metadata: `370 / 3660`
- Signal timeline entries after rerun: `63`
- Unknown timeline entries after rerun: `0`

## What I Read

I inspected the full project tree under the repo root, including:
- `scripts/*.py`, `scripts/deploy.sh`
- `data/*.json`, `data/update_state.py`, and `data/predictions/*.json`
- `dashboard.html`, `index.html`
- project docs and briefing files
- static library assets under `lib/`

I also parse-checked the JSON corpus and validated the generated frontend and Python entrypoints.

## Fixes Applied During This Audit

### Deploy / pipeline

Resolved:
- `scripts/deploy.sh` is no longer a divergent inline-Python copy of the pipeline.
- `scripts/deploy.sh` now computes the repo root dynamically instead of hardcoding `/home/openclaw/.openclaw/workspace/nuke-watch`.
- `scripts/pipeline.py` now changes into the repo root via `Path`, so it can run from any working directory.
- `scripts/pipeline.py` now only runs git commit/push when `NUKE_WATCH_AUTO_GIT=1` is set.
- The deploy wrapper explicitly opts into git behavior; direct pipeline runs do not push.
- `state["last_updated"]` is now synchronized to the pipeline run timestamp.

### State / timeline / predictions

Resolved:
- Signal timeline pruning is now active and was exercised successfully.
- `data/signal_timeline.json` was reduced to configured signals only; it now contains `63` entries with `0` unknown keys.
- Tracker `signal_timestamps` are now rebuilt from active signals, removing the earlier stale timestamp drift.
- Top-level `signal_timestamps` in `data/current_state.json` is now aligned with the current timeline.
- Coupling fields are now synchronized per tracker: `current_probability`, `current_probability_with_coupling`, `coupling_boost`, and `zone`.
- Prediction evaluation now reads the coupled probability field when available, which matches what the dashboard actually shows.
- Prediction records are deduplicated by `(tracker_id, expires_at)` before and after ingest, reducing duplicate-history inflation.

### Dashboard / frontend

Resolved in both `dashboard.html` and `index.html`:
- Removed the extra orphan `</div>`; `<div>` open/close counts now match `110 / 110`.
- Fixed the broken placeholder object typo `trend": "rising"`.
- Corrected the confidence filter label and logic from `developing` to `reported`.
- Fixed source filter behavior by normalizing and inferring source categories more robustly.
- Fixed time-block grouping so ISO timestamps and `0H`-style relative strings both sort correctly.
- Preserved pipeline-computed `global_zone` instead of recomputing it incorrectly on load.
- Added HTML escaping on tracker cards, news items, timeline entries, briefing modal, prediction modal, and map tooltips.
- Energy cards now tolerate missing values and render `N/A` instead of broken formatting.
- All inline script blocks in both HTML files pass `node --check`.

### Other fixes

Resolved:
- `data/source_credibility.json` key normalization issue (`" Downing street"`) was corrected.
- `data/update_state.py` no longer uses hardcoded absolute paths.
- `scripts/track_flights.py` now clamps `disruption_pct >= 0`.
- `scripts/track_flights.py` no longer suppresses full-closure signaling just because `flight_count == 0`.

## Open Findings

### High

#### 1. `data/update_state.py` can still corrupt live state with stale and invalid content

File: `data/update_state.py`

This script still hardcodes tracker probabilities, trends, notes, `top_signals`, `outlook`, `de_escalation_watch`, and `latest_news`. More importantly, it appends signal names that do not exist in the current tracker config, including:
- `trump_hasnt_started_destroying`
- `karaj_b1_bridge_struck`
- `iran_oman_hormuz_protocol`
- `unsc_hormuz_vote_today`
- `iran_crushing_actions_warning`
- `pentagon_army_chief_fired`

If this script runs from cron before the main pipeline, it can reintroduce stale probabilities and invalid active signals into `data/current_state.json`. The pipeline now cleans much of that up, but the script itself is still a live source of state corruption.

Impact:
- Divergence between manual cron state and computed state
- Invalid signals can appear transiently in active state
- Human-readable notes can contradict actual probabilities
- Any consumer reading `current_state.json` between runs can see false state

Recommendation:
- Decommission this script, or reduce it to a thin wrapper that invokes `scripts/pipeline.py` or writes only fields that are truly external inputs.
- Do not let it write probabilities, zones, notes, or signals directly.

#### 2. `flight_tracking.json` remains a mixed-schema file with two competing writers

Files:
- `scripts/flight_tracker.py`
- `scripts/track_flights.py`
- `data/flight_tracking.json`

There are still two producers for the same file:
- `scripts/flight_tracker.py` writes Aviationstack-style airport data with keys like `active_flights`, `cancelled_flights`, `baseline_daily_flights`, `api_used`, `requests_this_run`
- `scripts/track_flights.py` writes OpenSky-style zone data with keys like `flight_count`, `baseline_flights`, `military`, `high_speed`

Current `data/flight_tracking.json` is a hybrid:
- top-level keys include `api_used` and `requests_this_run`, which come from the Aviationstack writer
- zone records currently use `flight_count`, `baseline_flights`, `military`, `high_speed`, which come from the OpenSky writer
- `api_used` currently says `aviationstack`, but the zone schema is OpenSky-shaped

Impact:
- Consumers cannot trust the schema of `flight_tracking.json`
- Any downstream logic keyed on one schema will fail or misread fields
- Operational provenance is ambiguous

Recommendation:
- Pick one canonical schema and one writer.
- If both sources are needed, write separate files such as `flight_tracking_opensky.json` and `flight_tracking_aviationstack.json`, then merge into a normalized canonical output.

#### 3. Dashboard rebuild in `scripts/pipeline.py` is still fragile because it relies on string markers

File: `scripts/pipeline.py`

The pipeline still rebuilds the page by searching for literal string markers such as:
- `const state = {`
- `// ===== RENDER`

If those markers move or the template is refactored, the pipeline can skip regeneration logic without raising a hard failure. This is materially better than the earlier divergent deploy path, but it is still brittle production plumbing.

Impact:
- Silent stale `index.html`
- Template edits can break deploys without a nonzero exit status
- Tight coupling between one HTML formatting style and the pipeline implementation

Recommendation:
- Fail hard if markers are not found.
- Replace string surgery with a small templating step or explicit placeholder tokens.

#### 4. Broad exception swallowing still hides operational failures

Files:
- `scripts/pipeline.py`
- `scripts/flight_tracker.py`
- `scripts/fetch_oil_prices.py`
- `scripts/track_flights.py`
- `scripts/deploy.sh`

There are still many bare `except:` blocks and silent `except Exception: continue/pass` branches. `scripts/deploy.sh` also suppresses oil-fetch stderr with `2>/dev/null`.

Impact:
- Partial failures can look like successful runs
- Data quality regressions become difficult to diagnose
- Broken API responses, malformed JSON, and template issues can be masked

Recommendation:
- Replace bare `except:` with `except Exception as e:` plus structured logging.
- In the deploy wrapper, log fetch failures instead of discarding stderr entirely.

### Medium

#### 5. Legacy prediction metadata gaps still reduce forecasting accountability

Files:
- `data/predictions/evaluations.json`
- `data/predictions/*.json`

After deduplication and reevaluation:
- `2000` prediction records are retained in `evaluations.json`
- `1970` are evaluated
- `1239` are correct
- exact evaluated accuracy is `62.89%`
- `200` current records still lack `eval_type` or `eval_value`
- archived files contain `370 / 3660` predictions missing eval metadata

The pipeline is now materially better than before, but old records still prevent complete and consistent back-evaluation.

Recommendation:
- Backfill legacy records with an explicit migration pass.
- Add a schema version to prediction files.
- Reject writing new prediction records unless evaluation metadata is present.

#### 6. State semantics are clearer now, but still redundant at the top level

File: `data/current_state.json`

Current tracker state is improved and internally consistent, but the top level still carries redundant or ambiguous fields:
- `global_probability`
- `global_war_probability`
- `global_zone`
- `signal_timestamps`

The dashboard uses coupled tracker probabilities, while `current_probability` remains the uncoupled base value and `current_probability_with_coupling` is the displayed value. That distinction is now real and useful, but it should be documented and enforced more cleanly.

Recommendation:
- Keep one canonical global probability field.
- Document base vs coupled probability semantics explicitly.
- Consider removing redundant top-level derived fields from `current_state.json` if they are not external inputs.

#### 7. Residual HTML injection risk remains a maintenance concern

Files:
- `scripts/pipeline.py`
- `dashboard.html`
- `index.html`

Most direct rendering surfaces are now escaped correctly. That was the main security defect and it has been mitigated. The residual issue is architectural: the frontend still uses many `innerHTML` writes and inline `onclick` attributes. The current paths are defensively escaped, but the pattern is easy to regress.

Recommendation:
- Prefer DOM construction over string-built HTML for newly touched UI.
- Treat all future state-derived strings as untrusted by default.

#### 8. Energy panel has dead code and no rendered chart container

Files:
- `dashboard.html`
- `index.html`

The JS looks up `document.getElementById('energyChart')`, but there is no `id="energyChart"` element in either page. The current code does not crash because the variable is unused, but it indicates unfinished UI logic.

Recommendation:
- Either remove the dead reference or add a real chart container and render historical energy data.

#### 9. Deploy still rewrites local git identity on every auto-git run

File: `scripts/pipeline.py`

When auto-git is enabled, the pipeline sets repo git config to:
- user.name `VoltaIntel`
- user.email `cryptocybrog1337@proton.me`

This is not a direct code-execution vulnerability, but it is an operational and auditability concern.

Recommendation:
- Move git identity configuration out of the pipeline.
- Use environment-provided identity or CI configuration instead.

### Low

#### 10. Dead or stale frontend bits remain

Files:
- `dashboard.html`
- `index.html`

Residual low-severity cleanup items:
- CSS still contains `.news-confidence.developing` even though the live filter now normalizes to `reported`
- `chartEl` in `renderEnergy()` is unused
- Zone-filter UI state is only partial when a user filters via tracker/news click rather than a visible filter button
- Dismissing the zone-alert banner is client-side only; refreshing restores pending alerts from state

These are cleanup tasks, not active production blockers.

## Security Review

### Fixed or improved

- Dashboard state-derived text is now escaped before HTML insertion in the main rendering surfaces.
- The pipeline no longer auto-commits/pushes unless explicitly enabled.
- No secrets are embedded in the dashboard HTML.
- `scripts/flight_tracker.py` reads the Aviationstack key from env or a local secrets file rather than embedding it in repo code.

### Still notable

- The frontend architecture still relies heavily on `innerHTML` and inline event handlers.
- The pipeline mutates local git identity when auto-git is enabled.
- `scripts/deploy.sh` still hides oil-fetch stderr.
- Secret path assumptions in `scripts/flight_tracker.py` are environment-specific and should be treated as deployment-coupled behavior, not portable app logic.

## JSON / Data Consistency Review

Validated:
- JSON parse check passed across the repository data corpus.
- `data/tracker_config.json`: `10` trackers, `9` coupling rules.
- `data/current_state.json`: `10` trackers, `6` latest news items, `10` current predictions.
- `data/probability_history.json`: `336` entries.
- `data/flight_tracking.json`: `5` zones, `5` signals, `15` history entries.
- `data/source_credibility.json`: key normalization issue fixed.

Current consistency state after rerunning the pipeline:
- `signal_timeline.json` now contains `63` entries and `0` unknown keys.
- Tracker `signal_timestamps` counts now match active signal counts across all trackers.
- Top-level `signal_timestamps` contains `63` entries and matches the timeline.

Remaining data problems:
- `data/update_state.py` can reintroduce invalid signal names.
- `flight_tracking.json` remains schema-mixed.
- Prediction archives still have legacy metadata gaps.

## Dashboard Audit

### Validated working

- Both `dashboard.html` and `index.html` now have balanced `<div>` structure: `110 / 110`.
- All inline JS blocks in both pages pass `node --check`.
- Tracker rendering works with escaped content.
- News filters for `confirmed`, `reported`, and source categories are wired to normalized data.
- Signal timeline loader and renderer parse the current `signal_timeline.json` shape.
- Global zone rendering honors `state.global_zone`.
- Prediction modal now has live data because the state injection mismatch was fixed earlier.

### Remaining frontend gaps

- No meaningful mobile-first layout; the dashboard is still desktop-biased.
- Energy history visualization is unfinished.
- Many interactions still use inline `onclick` or `innerHTML` strings.
- No live refresh beyond page reload patterns.
- No persistent acknowledgment flow for alerts.

## Coupling Logic Audit

Current behavior after fixes:
- Base probabilities are computed from tracker base rate, decayed active signals, and no-news decay.
- Coupling is applied proportionally from source probability.
- Per-target coupling is capped at `+25`.
- Tracker `current_probability` stores base probability.
- Tracker `current_probability_with_coupling` stores displayed coupled probability.
- Tracker `zone` is now based on the coupled probability.
- Global probability is the weighted aggregate of coupled tracker probabilities.

Assessment:
- The coupling math is internally coherent now.
- The main remaining issue is semantic clarity, not arithmetic correctness.

Recommendation:
- Document this explicitly in code comments and in the README or operator docs:
  - base probability = intrinsic tracker score before cross-conflict effects
  - coupled probability = what the dashboard displays and what global aggregation uses

## Prediction Evaluation Audit

Current state:
- The earlier “0/0 accuracy” failure mode is resolved.
- Predictions are now present in the dashboard and state.
- The evaluation store is populated and rolling.
- The pipeline now evaluates against coupled probability when available.
- Duplicate prediction records are deduplicated by identity.

Current exact metrics:
- total retained prediction records: `2000`
- evaluated: `1970`
- correct: `1239`
- exact evaluated accuracy: `62.89%`
- state-rounded accuracy shown to UI: `63%`
- unevaluated records: `30`
- expired-but-unevaluated records: `0`

Open issue:
- Historical records still lack metadata, so the long-run record is better than before but still incomplete.

## Missing Error Handling

Most important error-handling gaps still open:
- `scripts/pipeline.py` uses many bare `except:` branches around file loads, timestamp parsing, and evaluation recovery.
- `scripts/flight_tracker.py` suppresses secret-file read failures and load failures.
- `scripts/fetch_oil_prices.py` suppresses load failures and silently skips Yahoo symbol failures.
- `scripts/track_flights.py` returns `None` on fetch failure without logging the exception body.
- `scripts/deploy.sh` discards oil-fetch stderr.

Recommendation:
- Emit one structured line per failure with file/source/context.
- Fail closed on template marker failure and state write failure.
- Keep silent fallback only where it is truly noncritical and explicitly documented.

## Validation Performed

Executed during this audit:
- `python3 -m py_compile scripts/pipeline.py scripts/fetch_oil_prices.py scripts/flight_tracker.py scripts/track_flights.py data/update_state.py`
- `python3 scripts/pipeline.py`
- `node --check` against each extracted inline script block from both `dashboard.html` and `index.html`
- JSON parse validation across the project data corpus
- structural checks for HTML `<div>` balancing
- post-run consistency checks for signal timeline, tracker timestamps, prediction counts, and evaluation stats

Observed results:
- Python compilation passed.
- All extracted inline JS blocks passed syntax check.
- Direct pipeline execution completed successfully and skipped git commit/push by default.
- Timeline drift was repaired after rerun.
- Tracker timestamp drift was repaired after rerun.

## Enhancements

### Dashboard UX

Recommended:
- Add a compact mobile layout with stacked tracker cards and a shorter map.
- Add sticky summary chips for `global zone`, `global probability`, and `top 3 rising trackers`.
- Add persistent visual distinction between base probability and coupled probability on tracker cards.
- Replace inline style-heavy sections with reusable CSS classes.
- Add a small “data freshness” panel showing last update per subsystem: pipeline, flight, energy, predictions.

### New data sources / signals

Recommended:
- AIS/shipping traffic for Hormuz, Bab el-Mandeb, and Eastern Mediterranean chokepoints.
- NOTAM / airspace restriction feeds rather than only flight counts.
- Satellite fire / thermal anomaly feeds for infrastructure hits.
- Sanctions / export-control events as separate escalation or de-escalation signals.
- FX volatility and sovereign CDS as additional market stress signals.
- Official military exercise notices and reserve call-up feeds.

### Better probability calibration

Recommended:
- Backtest signal weights against historical tracker outcomes.
- Add calibration curves by tracker rather than one global heuristic.
- Record both predicted probability and realized probability bin for Brier-style scoring.
- Separate event likelihood from conflict intensity likelihood where relevant.
- Consider decay based on `last_confirmed` rather than only `activated_at` for some signal classes.

### Mobile responsiveness

Recommended:
- Add a single-column layout under a tablet breakpoint.
- Reduce typography density and tracker card padding on phones.
- Collapse the map and narrative sections into accordions on narrow screens.
- Make the energy grid `2xN` or `1xN` on mobile.

### Alerts / notifications

Recommended:
- Persist alert acknowledgments in data rather than only in browser memory.
- Add webhook outputs for Telegram, Discord, Slack, or email.
- Allow alert rules on zone changes, probability deltas, and newly activated high-weight signals.
- Add rate limiting and digest mode to avoid alert floods.

### Historical trend visualization

Recommended:
- Render `probability_history.json` as real multi-series sparklines, not just a static global SVG.
- Add tracker-level history overlays and zone-threshold bands.
- Add a replay mode for key dates and prediction windows.
- Add energy and flight mini-charts beside the current cards.

### Prediction accuracy tracking

Recommended:
- Show per-tracker hit rate and sample size.
- Separate accuracy by prediction type: `probability_above`, `probability_below`, `zone_change`, `signal_triggered`.
- Track rolling 7-day and 30-day accuracy.
- Add calibration buckets and Brier score, not just raw accuracy.
- Display how many records are excluded due to missing eval metadata.

## Status of Original Audit Findings

Original findings from `AUDIT_REPORT.md`, reevaluated now:
- Orphaned `</div>` in dashboard: fixed.
- Predictions not appearing in dashboard: fixed.
- Empty/unused evaluation history: fixed.
- Semantically inverted `positive` flag naming: still confusing, but the logic now behaves correctly; rename remains advisable.
- News time grouping always returning `RECENT`: fixed.
- Stale tracker names for auto-detected trackers: fixed in the pipeline label map.
- Redundant predictions cap: fixed by current pipeline path.
- `updateGlobalClock` ignoring precomputed zone: fixed.

## Priority Next Steps

1. Remove or redesign `data/update_state.py` so it cannot write hardcoded probabilities or invalid signals.
2. Consolidate flight tracking into one canonical schema and one canonical output file.
3. Replace fragile string-based HTML regeneration with explicit template placeholders and hard failure on mismatch.
4. Replace bare exception swallowing with structured logging.
5. Migrate old prediction records so every retained prediction has evaluation metadata.
6. Add mobile-responsive dashboard layouts and real historical visualizations.
7. Add persistent notifications and per-tracker forecast scoring.

