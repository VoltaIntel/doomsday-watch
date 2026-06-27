# Nuke Watch Session State

Updated: 2026-06-27T18:18:15Z

## Latest Kabul Watch cron run
- Job: Kenan daily Afghanistan/Kabul Watch summary.
- Time: 2026-06-27T18:18:15Z.
- Result: delivered platform-split Discord + Telegram summary.
- Bottom line: no major confirmed Kabul security incident in the last 24h; main fresh confirmed development was the Hindu Kush earthquake felt in Kabul with no immediate casualties/damage reported.
- Kabul posture: IEA-linked Ariana quoted Shahabuddin Delawar in Kabul saying Ashura passed peacefully under full security and Afghanistan had achieved security/unity; treated as official messaging only.
- Pakistan/civil disruption: WFP said Pakistan border closures plus the Middle East crisis are worsening food security and have pushed ~60% of trade through Iran; Ariana reported Torkham trade/pedestrian closure continuing with stranded drivers/vehicles and protest threats after Eid.
- Aviation: no material KBL disruption found. Live OAKB/OAKX NOTAM decode showed standing 2026-06-25 operating notices, not a new closure; Safe Airspace baseline still lists OAKX open but uncontrolled Class G; Kam Air's latest notice is added Kabul-Tashkent frequency from 2026-07-02.
- Reachability caveat: KIA flights page, Flydubai updates, and Turkish announcements timed out from this environment.

## Latest cron run
- Job: DoomsdayWatch nuclear escalation MORNING DEEP SCAN 12Z refresh.
- Repo: `/home/openclaw/.openclaw/workspace/nuke-watch`
- Deploy pushed HEAD: `8c04797` (`Update 2026-06-27T12:06:24Z — automated`).
- Final dashboard/current state: **63% / imminent**; raw global in state: **63.20** after deploy.
- Movement vs 09Z: `iran_conventional` **70→74** final on fresh U.S. strike/vessel-disruption/regional drone reporting; `israel_lebanon` **88→86** final on framework/talks down-pressure; `iran_nuclear` **46→44** final after deploy/coupling math on access-positive verification reporting. Global stayed **63 / imminent**.
- Coupled tracker table: `russia_ukraine` 98, `israel_palestine` 88, `israel_lebanon` 86, `sudan` 82, `iran_conventional` 74, `russia` 50, `iran_nuclear` 44, `pakistan_afghanistan` 42, `china` 26, `north_korea` 11, `india` 11, `turkey` 5, `south_sudan_abyei` 8.
- Active canonical signals after deploy: `iran_conventional:ceasefire_violation`, `iran_conventional:hormuz_controlled_not_closed`, `iran_conventional:military_buildup`, `israel_lebanon:ceasefire_violation`, `israel_lebanon:diplomacy_active`, `iran_nuclear:diplomacy_active`, `north_korea:missile_range_test`, `russia_ukraine:military_buildup`, `pakistan_afghanistan:military_buildup`, `sudan:infrastructure_strike`, `sudan:military_buildup`, `israel_palestine:ceasefire_violation`.
- Signal hygiene: canonical check clean after deploy; no new canonical signal added; no non-canonical IDs/signals used.
- Source caveat: `web_search`/Tavily failed HTTP 432 on all required queries. Fallback used Google News RSS, direct terminal official/public probes, UN News RSS, UN Press RSS, NATO pages, OCHA oPt, EIA, OilPriceAPI and Polymarket Gamma/cache. IAEA public pages returned 403; Pakistan-Afghanistan/Russia/Turkey targeted RSS were sparse or zero-hit.
- Energy/markets: OilPriceAPI 12Z Brent **$73.08**, WTI **$69.23**, gold **$4080.83**. Oil/RSS coverage says Hormuz tanker traffic rebounded/restarted, rejecting full waterway-stoppage thresholds. Polymarket mapped cache refreshed `2026-06-27T12:07:04Z`; worst mapped divergence remains `russia_ukraine` (~97.47pp, horizon mismatch).
- Emerging review: no tracker added. Thailand-Cambodia remains a watch cluster but below nuclear/alliance-spillover threshold; Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia stale/low-confidence for this scope.
- Verification: JSON valid; canonical signal check clean; `index.html` contains `DoomsdayWatch // Command Deck`, `const state = {`, and `// ===== RENDER`; deploy/push succeeded.

## Watch next
- Iran/Hormuz: repeated ship strikes, explicit waterway obstruction, insurer/charterer suspensions, naval escort incidents, mining, or sustained traffic collapse. Current Brent/WTI and traffic coverage still reject full stoppage.
- Iran conventional: whether U.S. strikes remain limited/self-contained or trigger Iranian retaliation against shipping, U.S. bases, Israel, Bahrain/Gulf targets, or oil infrastructure.
- Israel-Lebanon: whether the reported framework/talks produce operational de-escalation or are overwhelmed by South Lebanon clashes; any Hezbollah retaliation, IDF escalation, multi-front violence, or framework collapse.
- Iran/IAEA: actual verification visit execution, direct agency-page access returning, any reversal of interim framework, verified higher-level enrichment, underground-site restart, or device event.
- Pakistan-Afghanistan: corroboration/refutation of Kunar/Asadabad shelling and border force movement. Downgrade further if the single-source claim ages without confirmation.
- DPRK: whether Kim-supervised firings remain tactical/short-range or expand into strategic systems; any configured strategic firing-event confirmation, DMZ escalation, or device event.
- Russia-Ukraine/Russia-NATO: confirmed Baltic/Poland incident, treaty invocation, Article 5 language, allied direct-entry breakpoint, or Russian hybrid action moving from warning to event.
- Sudan/El Obeid/Kordofan: confirmed RSF entry/offensive into El Obeid, broader infrastructure/service disruption wave, external backing, or atrocity reporting.
- Gaza/West Bank: more confirmed truce-breach fatalities, holy-site tension, or wider regional spillover.
- Turkey, India-Pakistan, South Sudan/Abyei: currently sparse/no configured triggers; keep checks.

## Operational reminders
- Always read `data/tracker_config.json` first and use canonical tracker IDs/signals only.
- If Tavily/web_search returns HTTP 432, continue via RSS/direct/official/terminal fallbacks and record caveat in `_meta`/briefing.
- Do not hand-edit command-deck UI shells during cron; write state atomically then run `bash scripts/deploy.sh`.
- Avoid broad signal keywords in zone notes (`ceasefire`, `negotiat`, `peace talk`, `missile launch`, `weapons-grade`, `IAEA access`, etc.) unless intentionally activating the canonical signal.
