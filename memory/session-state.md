# Session State

Last update: 2026-07-11T15:09Z

DoomsdayWatch 15Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published state: **73% / imminent** (raw **69.9%**), up 1 point from 12Z.
- Full coupled table: Iran War **100**, Russia-Ukraine **99**, Israel-Lebanon **94**, Sudan **90**, Israel-Palestine **88**, Eastern DR Congo **58**, Iran Nuclear **54**, Russia-NATO **52**, Pakistan-Afghanistan **46**, China-Taiwan **28**, DPRK **18**, South Sudan/Abyei **17**, India-Pakistan **11**, Turkey **5**.
- Top mover: Israel-Lebanon **98→94** after KAN reporting, carried by several outlets, that Israel froze sensitive south-Lebanon operations at Washington’s request and is preparing a pilot-area handover alongside Rome talks. `israel_lebanon:diplomacy_active` activated while `ceasefire_violation` remains active pending implementation.
- Auto-detection: added canonical tracker `eastern_drc` at **58 / imminent**. OHCHR, UN News and AP established at least three mentions across two source groups of intensified/expanding fighting with armed drones, heavy artillery, Rwanda-backed M23 and civilian harm, satisfying `tracker_config.json` (`min_mentions=3`, `min_sources=2`).
- Existing Iran conventional truce-breach and Iran nuclear verification-gap signals were reconfirmed after deploy TTL checks.
- Sources: all 17 live web-search lanes returned. RSS and direct OHCHR/UN/AP/Reuters/Middle East Monitor pages supplied corroboration. Local fallback helper recorded HTTP 432 on its own search path but completed RSS/direct collection. IAEA/OPEC direct pages and configured OCHA/UN Sudan feeds remained unavailable.
- Energy: weekend Friday closes remain Brent **$75.22**, WTI **$71.41**. Polymarket mapped refresh succeeded at 15:08Z; horizon/definition mismatch remains material.
- Deploy: `bash scripts/deploy.sh` succeeded twice (second pass restored TTL-confirmed signals) and pushed. Required Command Deck markers, JSON/canonical validation, 14-tracker coverage, clean local status and origin parity passed. Final deploy commit: `9eb6e36`.
