# DoomsdayWatch Session State

Last updated: 2026-05-13T17:03:56Z

Current deployed briefing: 2026-05-13 evening nuclear escalation briefing.

Deployment status:
- `bash scripts/deploy.sh` completed, committed, and pushed.
- `data/current_state.json` post-deploy global: 58% imminent; raw analysis global: 52%.
- Polymarket cache fresh at deploy (`stale=false`, age ~0h).
- `index.html` contains latest news items and inline JS passed `node --check`.

Important operational note:
- `data/signal_timeline.json` must use nested schema `{"signals": {"zone:signal": {"activated_at": iso, "last_confirmed": iso}}}`; flat schema crashes deploy with `KeyError: 'signals'`.
