import json, os, tempfile
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('.').resolve()
DATA = ROOT / 'data'
now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
state = json.loads((DATA / 'current_state.json').read_text())
cfg = json.loads((DATA / 'tracker_config.json').read_text())
timeline = json.loads((DATA / 'signal_timeline.json').read_text())
artifacts = sorted(DATA.glob('morning_deep_scan_sources_*.json'))
artifact = artifacts[-1]
art = json.loads(artifact.read_text())
energy = json.loads((DATA / 'energy_prices.json').read_text()) if (DATA / 'energy_prices.json').exists() else {}
pm = json.loads((DATA / 'polymarket_cache.json').read_text()) if (DATA / 'polymarket_cache.json').exists() else {}

allowed = set(cfg['trackers'])
allowed_sig = {tid: set(t.get('signals', {})) for tid, t in cfg['trackers'].items()}
raw_probs = {
    tid: int((state.get('trackers', {}).get(tid) or state.get('zones', {}).get(tid) or {}).get(
        'current_probability', (state.get('zones', {}).get(tid) or {}).get('current_prob', 0)
    ))
    for tid in allowed
}
active = {}
for tid in allowed:
    tr = state.get('trackers', {}).get(tid) or state.get('zones', {}).get(tid) or {}
    active[tid] = [s for s in tr.get('active_signals', []) if s in allowed_sig[tid]]

notes = {
    'iran_conventional': '00Z scan keeps Iran conventional imminent/rising: Hormuz restricted-transit and tanker-risk reporting persists, while price/flow evidence rejects a full waterway halt; Doha-channel diplomacy remains fragile.',
    'israel_lebanon': '00Z scan keeps Israel-Lebanon imminent: Israeli stay-behind posture in south Lebanon, Hezbollah spoiler rhetoric and renewed south-Lebanon strike/damage reporting persist; no wider alliance-entry breakpoint surfaced.',
    'turkey': '00Z scan keeps Turkey-NATO deterrent: coverage is Ankara NATO-summit and defense-industrial positioning; no fresh configured Turkish strategic-arms event was corroborated.',
    'india': '00Z scan keeps India-Pakistan elevated: Poonch/LoC intruder reports remain border-security friction, not corroborated sustained exchange or major force movement.',
    'russia': '00Z scan keeps Russia-NATO critical raw and imminent after Ukraine coupling: Baltic/Poland hybrid-action warnings remain live, with no treaty invocation, public direct-combat entry decision or verified kinetic incident.',
    'china': '00Z scan keeps China-Taiwan posture-watch critical: Taiwan blockade-tabletop and PRC patrol-pressure coverage remain live; no configured force trigger was corroborated.',
    'north_korea': '00Z scan keeps DPRK elevated: weapons-drill and destructive-posture coverage remains watch-only; no fresh corroborated strategic-weapons threshold event was promoted.',
    'russia_ukraine': '00Z scan keeps Russia-Ukraine ceiling-level: active-war strikes, Belarus pressure and hardline escalation commentary remain live; no NATO direct-entry breakpoint surfaced.',
    'pakistan_afghanistan': '00Z scan keeps Pakistan-Afghanistan critical/rising: cross-border operations, casualty claims and Taliban retaliation language remain corroborated across fallback sources.',
    'iran_nuclear': '00Z scan keeps Iran verification critical: agency-monitoring and Tehran timing/terms disputes remain live; no higher-threshold technical trigger was corroborated.',
    'sudan': '00Z scan keeps Sudan imminent: El Obeid/Kordofan atrocity-risk, encirclement and fortification/offensive-risk reporting remain live; no material easing signal surfaced.',
    'israel_palestine': '00Z scan keeps Israel-Palestine imminent: Gaza fatality, West Bank pressure and UN service-risk reporting remain severe; no wider-regional breakout threshold is promoted.',
    'south_sudan_abyei': '00Z scan keeps South Sudan/Abyei deterrent: thirty-day fallback returned no fresh Abyei force-escalation reporting, only UNISFA/mandate background material.',
}
final_probs = {
    tid: int((state.get('trackers', {}).get(tid) or {}).get(
        'current_probability_with_coupling',
        (state.get('trackers', {}).get(tid) or {}).get('probability', raw_probs[tid])
    ))
    for tid in allowed
}
thresholds = cfg.get('scoring', {}).get('zones', {})
def classify(p):
    for name, pair in thresholds.items():
        lo, hi = pair
        if lo <= p < hi or (name == 'imminent' and p >= lo):
            return name
    return 'deterrent'

latest_news = [
    {'zone':'iran_conventional','time':'00Z/24H','headline':'Iran/Hormuz: restricted transit risk persists while prices reject a full halt','text':'Fallback headlines show Hormuz control/risk reporting, tanker movement, Brent/WTI softness and continuing Doha-channel uncertainty. Flow and price evidence still points to restricted or escorted transit rather than zero traffic.','impact':'watch','sources':['Reuters','CNBC','OilPrice.com','Google News RSS fallback'], 'source_date':'1-2 Jul 2026'},
    {'zone':'israel_lebanon','time':'00Z/24H','headline':'Israel-Lebanon: stay-behind posture and Hezbollah spoiler risk persist','text':'BBC, Al Jazeera and regional fallback items report Israeli strikes in south Lebanon, Israeli forces remaining in Lebanon and Hezbollah rejection/spoiler risk around the US-brokered framework.','impact':'up','sources':['BBC','Al Jazeera','The Times of Israel','Google News RSS fallback'], 'source_date':'29 Jun-2 Jul 2026'},
    {'zone':'pakistan_afghanistan','time':'00Z/14D','headline':'Pakistan-Afghanistan: cross-border operation/casualty lane remains hot','text':'PBS/AP, Al Jazeera and CBS items continue to report Pakistani border operations, claimed militant casualties, civilian casualty claims and Taliban retaliation language. This keeps the force-posture lane active without a wider regional break.','impact':'up','sources':['PBS/AP','Al Jazeera','CBS News','Google News RSS fallback'], 'source_date':'10 Jun-2 Jul 2026'},
    {'zone':'sudan','time':'00Z/7D','headline':'Sudan: El Obeid/Kordofan encirclement and atrocity risk remain severe','text':'UN News and Security Council Report coverage keep El Obeid/Kordofan escalation, RSF pressure, city fortification and atrocity-risk language live. No easing source displaced that signal.','impact':'up','sources':['UN News','Security Council Report','CFR','Google News RSS fallback'], 'source_date':'26 Jun-2 Jul 2026'},
    {'zone':'israel_palestine','time':'00Z/24H','headline':'Israel-Palestine: Gaza fatalities and West Bank pressure remain acute','text':'AP-syndicated, Al Jazeera and OCHA/UN material show fresh Gaza fatality coverage, West Bank pressure and UN service-risk coverage. Severe local conflict continues without a new regional-breakout threshold.','impact':'up','sources':['AP/KCRA','Al Jazeera','OCHA oPt','UN Press','Google News RSS fallback'], 'source_date':'17 Jun-2 Jul 2026'},
    {'zone':'russia','time':'00Z/7D','headline':'Russia-NATO: Baltic/Poland hybrid-action warnings remain the key allied watch item','text':'Guardian, Fox/Latvian-intelligence reporting, NATO public pages and allied commentary keep possible Russian provocation or hybrid activity against Baltic states or Poland in view. There is still no public treaty invocation or verified direct kinetic incident.','impact':'watch','sources':['The Guardian','Fox News','NATO public pages','Google News RSS fallback'], 'source_date':'22 Jun-2 Jul 2026'},
    {'zone':'russia_ukraine','time':'00Z/24H','headline':'Russia-Ukraine: active-war escalation context persists, no NATO direct-entry break','text':'ISW, Reuters and WSJ-style fallback include Russia-Belarus pressure, deep-strike context and Belarus-front concern. The war remains ceiling-level, but no public NATO direct-combat decision surfaced.','impact':'watch','sources':['ISW','Reuters','Wall Street Journal fallback','Google News RSS fallback'], 'source_date':'24 Jun-2 Jul 2026'},
    {'zone':'iran_nuclear','time':'00Z/7D','headline':'Iran nuclear: verification/timing dispute remains central','text':'IAEA chronology, AP, Al Jazeera/RFE-style and institute analysis items continue to say strong agency verification is required while Tehran frames timing as conditional on final terms. No fresh high-threshold technical breakout indicator was corroborated.','impact':'watch','sources':['IAEA chronology','AP','ISIS Online','Google News RSS fallback'], 'source_date':'Jun-2 Jul 2026'},
    {'zone':'china','time':'00Z/7D','headline':'China-Taiwan: blockade-tabletop and patrol-pressure coverage stays live','text':'Reuters archive/fallback, ISW/AEI and Strait-focused reporting show Taiwan simulating a response to Chinese maritime coercion, with PRC patrol-pressure analysis and Western criticism still visible. No fresh configured force trigger was corroborated.','impact':'watch','sources':['Reuters','ISW/AEI','State of the Strait','Google News RSS fallback'], 'source_date':'26 Jun-2 Jul 2026'},
    {'zone':'north_korea','time':'00Z/7D','headline':'DPRK: late-week weapons-drill coverage remains watch-only','text':'Al Jazeera/DW/USNI-style and regional items keep destructive-posture and weapons-drill coverage visible; the 00Z pass found no fresh corroborated strategic-weapons threshold event to promote.','impact':'watch','sources':['Al Jazeera','DW','USNI News','Google News RSS fallback'], 'source_date':'25 Jun-2 Jul 2026'},
    {'zone':'india','time':'00Z/14D','headline':'India-Pakistan: Poonch/LoC intrusions remain friction, not mobilization','text':'Times of India, Rediff/Daily Guardian-style and Al Jazeera background reports show repeated Pakistani national/intruder apprehensions near the LoC/Poonch area. No corroborated sustained exchange or major force movement surfaced.','impact':'neutral','sources':['Times of India','Rediff','Al Jazeera','Google News RSS fallback'], 'source_date':'27 Jun-2 Jul 2026'},
    {'zone':'turkey','time':'00Z/14D','headline':'Turkey-NATO: summit security posture is not a strategic trigger','text':'Fallback returned Ankara summit and defense-industry coverage plus older strategic-systems background. No fresh configured Turkish strategic-arms action was promoted.','impact':'neutral','sources':['NATO','CSIS','TRT World Research Centre','Google News RSS fallback'], 'source_date':'26 Jun-2 Jul 2026'},
    {'zone':'south_sudan_abyei','time':'00Z/30D','headline':'South Sudan/Abyei: no fresh force-escalation item found','text':'Fallback found UNISFA/UNMAS and Security Council mandate material but no fresh Abyei clash or new armed-force buildup meeting tracker-add or signal-promotion criteria.','impact':'neutral','sources':['UNISFA','UNMAS','Security Council Report','Google News RSS fallback'], 'source_date':'May-Jul 2026'},
    {'zone':'oil_energy','time':'00Z/24H','headline':'Energy/oil sanity: Hormuz risk visible, prices and flow headlines still reject full stoppage','text':'Oil coverage shows Brent/WTI below late-June crisis highs, tanker movement through Hormuz and forecasts cut as reopening eases supply fears. This supports restricted-transit risk, not zero-traffic or full-closure thresholds.','impact':'down','sources':['Reuters','CNBC','OilPrice.com','EIA RSS','Google News RSS fallback'], 'source_date':'30 Jun-2 Jul 2026'},
    {'zone':'iaea_un','time':'00Z/7D','headline':'IAEA/UN: verification remains the key Iran nuclear watch item','text':'Official IAEA chronology was reachable via search, while direct IAEA news pages remained blocked to the fallback collector. UN feeds were reachable; public reporting says stronger verification is the active dispute, with no confirmed breakout-threshold event.','impact':'watch','sources':['IAEA chronology','UN News RSS','UN Press RSS','AP','Google News RSS fallback'], 'source_date':'Jun-2 Jul 2026'},
    {'zone':'nato_allied','time':'00Z/7D','headline':'NATO/allied posture: eastern-flank warning persists without alliance activation','text':'NATO public pages were reachable. Allied fallback keeps eastern-flank warning and Ankara-summit deterrence debate live; no Article 5 invocation, public direct-combat entry decision or verified Russia-NATO kinetic incident surfaced.','impact':'watch','sources':['NATO public pages','The Guardian','Belfer Center','Google News RSS fallback'], 'source_date':'22 Jun-2 Jul 2026'},
    {'zone':'emerging_7d','time':'00Z/7D','headline':'Auto-detection: no untracked crisis met add threshold','text':'Emerging-crisis fallback for Thailand-Cambodia, Ethiopia-Eritrea, Guyana-Venezuela and Kosovo-Serbia returned zero qualifying fresh items in this run. No new zone was added.','impact':'neutral','sources':['Google News RSS fallback','CFR conflict watch background'], 'source_date':'2 Jul 2026'},
]

state['timestamp'] = now
state['last_updated'] = now
state['latest_news'] = latest_news
state.setdefault('zones', {})
state.setdefault('trackers', {})
for tid in cfg['trackers']:
    z = state['zones'].setdefault(tid, {})
    tr = state['trackers'].setdefault(tid, {})
    for obj in (z, tr):
        obj['name'] = obj.get('name') or tid.upper().replace('_', '-')
        obj['base_prob'] = raw_probs[tid]
        obj['current_prob'] = raw_probs[tid]
        obj['current_probability'] = raw_probs[tid]
        obj['probability'] = raw_probs[tid]
        obj['current_probability_with_coupling'] = final_probs[tid]
        obj['coupling_boost'] = max(0, final_probs[tid] - raw_probs[tid])
        obj['zone'] = classify(final_probs[tid])
        obj['trend'] = 'rising' if tid in ('iran_conventional', 'pakistan_afghanistan') else 'stable'
        obj['active_signals'] = active[tid]
        obj['notes'] = notes[tid]
        obj['last_updated'] = now
        sig_ts = {}
        for s in active[tid]:
            entry = timeline.get('signals', {}).get(f'{tid}:{s}', now)
            sig_ts[s] = entry.get('activated_at', now) if isinstance(entry, dict) else entry
        obj['signal_timestamps'] = sig_ts
state['signal_timestamps'] = {
    f'{tid}:{s}': state['trackers'][tid]['signal_timestamps'].get(s, now)
    for tid in cfg['trackers'] for s in active[tid]
}
state['global_probability'] = 67
state['global_war_probability'] = 67
state['global_zone'] = 'imminent'
state['raw_global_probability'] = 67.4
state['global_uncertainty_index'] = 48

meta = state.setdefault('_meta', {})
counts = art.get('counts', {})
official = art.get('official', {})
cur = energy.get('current', {})
def price(k):
    v = cur.get(k, {})
    return v.get('price') if isinstance(v, dict) else None
pm_markets = pm.get('markets', {}) or {}
pm_focus = {k: {'yes_price': v.get('yes_price'), 'updated_at': v.get('updated_at')} for k, v in pm_markets.items() if k in ['will-the-us-invade-iran-before-2027','iran-nuke-before-2027','iran-nuclear-test-before-2027','nato-article-5-before-2027','will-china-invade-taiwan-before-2027','china-x-taiwan-military-clash-before-2027']}
meta.update({
    'last_writer':'doomsdaywatch_00z_morning_deep_scan_cron',
    'last_scan':now,
    'scan_time_utc':now,
    'analysis_window':'00z_morning_deep_scan_past_24h_with_7d_14d_30d_sparse_crosschecks_web_search_google_news_rss_official_feed_energy_polymarket_sanity_checks',
    'search_engine':'web_search_succeeded_plus_public_safe_multi_source_fallback',
    'source_limitation':'web_search returned results for all required tracker/sector groups, but recall was uneven/stale in several lanes; fallback used Google News RSS, direct UN/NATO/EIA/IAEA/OPEC/OCHA probes, terminal HTTP, energy cache and Polymarket cache/deploy refresh where available. Treat single-source claims as watch items until confirmed.',
    'source_fallback_detail_00z':f'web_search attempted for 17/17 required tracker/sector groups and returned results; fallback artifact {artifact.as_posix()} used Google News RSS plus direct official/feed probes.',
    'latest_source_artifact_00z':artifact.relative_to(ROOT).as_posix(),
    'latest_rss_scan_keys_00z':list(counts.keys()),
    'rss_headline_counts_00z':counts,
    'official_source_probe_00z':{k:{'ok':bool(v.get('ok')), 'status':v.get('status'), 'url':v.get('url'), 'title':v.get('title')} for k, v in official.items()},
    'morning_deep_scan_movers_00z':'00Z change vs 21Z: no numeric probability moves. Iran conventional remains the top rising Iran lane after continued Hormuz restricted-transit/tanker-risk reporting; Pakistan-Afghanistan remains the main non-Mideast rising lane at 40 critical. Global remains rounded at 67/imminent.',
    'signals_changed_00z':'Canonical signals only. No new signal names added. Existing Iran/Hormuz, Israel-Lebanon, Pakistan-Afghanistan, Sudan and Israel-Palestine active lanes were preserved/reconfirmed from fresh fallback evidence; no DPRK configured signal was promoted. No untracked zone was auto-added.',
    'auto_detection_00z':'No untracked nuclear-escalation/alliance-spillover zone auto-added. Emerging-crisis fallback for Thailand-Cambodia/Ethiopia-Eritrea/Guyana-Venezuela/Kosovo-Serbia returned zero qualifying fresh items in this run.',
    'energy_oil_00z':f"00Z pre-deploy cache: Brent ${price('BRENT_CRUDE_USD')} and WTI ${price('WTI_USD')}; gas ${price('NATURAL_GAS_USD') or price('GASOLINE_USD')}, gold ${price('GOLD_USD')}. Hormuz/tanker-risk headlines remain visible, but price and flow reports still reject full-waterway-halt thresholds.",
    'allied_positions_00z':'NATO public pages reachable; allied fallback keeps eastern-flank warning and Ankara-summit deterrence debate live. No Article 5 invocation, public direct-combat entry decision or verified Russia-NATO kinetic incident surfaced.',
    'polymarket_sanity_00z':f"Pre-deploy Polymarket cache fetched_at={pm.get('fetched_at')}; mapped markets remain horizon-mismatched sanity checks, not direct probability setters.",
    'polymarket_probe_00z':pm_focus,
    'old_probabilities_raw_00z':{tid: raw_probs[tid] for tid in cfg['trackers']},
    'old_probabilities_coupled_00z':{tid: final_probs[tid] for tid in cfg['trackers']},
    'raw_probabilities_before_coupling_00z':{tid: raw_probs[tid] for tid in cfg['trackers']},
    'expected_final_probabilities_after_coupling_00z':{tid: final_probs[tid] for tid in cfg['trackers']},
    'raw_global_probability_00z':67.4,
})

bad = []
for tid, tr in state['trackers'].items():
    if tid in cfg['trackers']:
        for s in tr.get('active_signals', []):
            if s not in allowed_sig[tid]:
                bad.append((tid, s))
if bad:
    raise SystemExit(f'noncanonical active signals: {bad}')

out = DATA / 'current_state.json'
fd, tmp = tempfile.mkstemp(prefix='current_state.', suffix='.json.tmp', dir=DATA)
with os.fdopen(fd, 'w') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
    f.write('\n')
os.replace(tmp, out)
json.loads(out.read_text())
print(json.dumps({'updated': str(out), 'now': now, 'artifact': artifact.relative_to(ROOT).as_posix(), 'global': state['global_probability'], 'bad_signals': bad, 'news_count': len(latest_news)}, indent=2))
