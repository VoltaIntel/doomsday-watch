# Session State

> Last updated: 2026-07-19T18:43:42Z
> Session: DoomsdayWatch 18Z morning deep-scan refresh

## Active Projects
- DoomsdayWatch / nuke-watch — scheduled 18Z deep-scan refresh completed, deployed, pushed and live-verified.
- Umbraxis Group — preserved paused state from the prior session; this cron did not touch its worktree or processes.

## Current Task
- **What:** Deepest past-24-hour nuclear-escalation scan across all 16 canonical trackers, required sectors and emerging crises.
- **Status:** Complete.
- **Result:** Global remains **75% / imminent**, raw coupled **74.596%**; no tracker probability changed.
- **Signals:** Configured decay cleared `iran_conventional:ceasefire_violation` and `yemen_red_sea:external_backing`; 9 canonical signals remain. An unsupported pipeline overmatch, `israel_palestine:diplomacy_active`, was removed before the corrective deploy.
- **Deployment:** Corrective deploy commit `010e9f79`; exact metadata/snapshot commit `81a96678`. Local HEAD, upstream and remote main match; Pages run `29699112080` succeeded and live root/state checks pass.
- **Verification:** JSON/canonical/timeline sets align; all command-deck markers pass; 31 fast tests passed. The repository smoke fixture hit its known 60-second ceiling, while the identical 11 assertions passed in 57.79s in an isolated copy with only the harness timeout raised.
- **Next step:** Next scheduled scan should start from `data/tracker_config.json`, re-check the watch triggers below, then repeat atomic state write, deploy and marker verification.

## DoomsdayWatch Watch State
- New verified fact: Iran says the US attacked the unfinished Darkhovin nuclear-power project. The IAEA says it was at a very early stage, held no nuclear material when last visited and is not believed to pose radiological risk. No nuclear signal activated; `iran_nuclear` remains 47% raw / 54% coupled.
- Israel-Lebanon: Rubio backed the trilateral framework after meeting Aoun; Hezbollah still rejects disarmament and negotiations. Existing `diplomacy_active` and `ceasefire_violation` remain active; 94% coupled.
- False recency: a fresh-looking Pakistan-Afghanistan headline claiming 30 Pakistani soldiers killed resolved to a News On AIR body dated 2026-03-06 and was excluded.
- Auto-detection: Somalia force claims and Thailand-Cambodia rhetoric did not produce an independently verified qualifying operational cluster. No zone was added.
- Source path: 22 Tavily searches and 3 extracts failed HTTP 432; fallback used 18 core + 39 targeted + 6 exact-event Google News RSS lanes, direct browser bodies, UN/NATO/EIA, terminal HTTP, OilPriceAPI and exact-slug Gamma. IAEA/OPEC direct pages remained 403.
- Final energy: Brent $88.26; WTI $81.78. Sanity markets: US-Iran invasion 30.5%, NATO Article 5 8.0%, Iran NPT withdrawal 14.9%, China-Taiwan clash 5.25%; not probability inputs.

## Preserved Umbraxis Pause State
- Accepted product master was clean at `265c819b3b39cec85a2359ff96471406d371ebdd`, 6/38 accepted, when last recorded locally.
- Prior Task 6A worktree/candidate details remain in today's memory and vault; no Umbraxis action occurred in this cron.
