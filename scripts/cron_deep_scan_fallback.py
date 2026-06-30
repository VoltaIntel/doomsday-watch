#!/usr/bin/env python3
"""DoomsdayWatch cron fallback evidence collector.

Uses public Google News RSS plus direct official/feed probes when Tavily/web_search
is quota-blocked. Writes a compact JSON artifact under data/.
"""
from __future__ import annotations

import email.utils
import html
import json
import re
import sys
import urllib.parse
import urllib.request
try:
    from defusedxml import ElementTree as ET
except ImportError:  # pragma: no cover - fallback in minimal cron environments
    import xml.etree.ElementTree as ET  # nosec: RSS from public feeds only; no entity expansion used
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 DoomsdayWatch/1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_url(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(250_000)
            text = raw.decode(r.headers.get_content_charset() or "utf-8", errors="replace")
            return {
                "ok": True,
                "status": getattr(r, "status", None),
                "content_type": r.headers.get("content-type"),
                "url": url,
                "bytes": len(raw),
                "text": text,
            }
    except Exception as e:
        return {"ok": False, "url": url, "error": repr(e)}


def parse_google_rss(xml_text: str, limit: int = 10) -> list[dict]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    out = []
    for item in root.findall(".//item")[:limit]:
        title = html.unescape(item.findtext("title") or "").strip()
        link = item.findtext("link") or ""
        pub = item.findtext("pubDate") or ""
        source = item.findtext("source") or ""
        if not source and " - " in title:
            source = title.rsplit(" - ", 1)[-1].strip()
        headline = title
        if source and title.endswith(" - " + source):
            headline = title[: -(len(source) + 3)].strip()
        published_iso = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                published_iso = dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                published_iso = pub
        out.append({
            "headline": headline,
            "source": source or "Google News RSS",
            "published": published_iso,
            "link": link,
        })
    return out


def google_news(query: str, limit: int = 10) -> dict:
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({
        "q": query,
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en",
    })
    res = fetch_url(url)
    items = parse_google_rss(res.get("text", ""), limit=limit) if res.get("ok") else []
    return {"query": query, "url": url, "ok": bool(res.get("ok")), "error": res.get("error"), "count": len(items), "items": items}


def page_title(text: str) -> str | None:
    m = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
    if not m:
        return None
    return re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()


def parse_rss_titles(xml_text: str, limit: int = 10) -> list[dict]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    items = []
    for item in root.findall(".//item")[:limit]:
        pub = item.findtext("pubDate") or ""
        published_iso = pub
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                published_iso = dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                pass
        items.append({
            "title": html.unescape(item.findtext("title") or "").strip(),
            "published": published_iso,
            "link": item.findtext("link") or "",
        })
    return items


def main() -> int:
    cfg = json.loads((DATA / "tracker_config.json").read_text())
    ts = now_iso()
    queries = {
        "iran_nuclear": "Iran nuclear IAEA monitoring enrichment Tehran when:7d",
        "iran_conventional": "Iran Strait of Hormuz tanker traffic oil military buildup when:1d",
        "israel_lebanon": "Israel Lebanon Hezbollah south Lebanon strikes when:1d",
        "turkey": "Turkey NATO nuclear rhetoric missile test when:14d",
        "india": "India Pakistan Line of Control Poonch military buildup when:14d",
        "russia": "Russia NATO Article 5 Poland Baltic hybrid threat when:7d",
        "china": "China Taiwan military drills blockade patrols when:7d",
        "north_korea": "North Korea missile launch nuclear test military drill when:7d",
        "russia_ukraine": "Russia Ukraine war escalation Belarus NATO strikes when:1d",
        "pakistan_afghanistan": "Pakistan Afghanistan border clashes airstrikes Taliban retaliation when:14d",
        "sudan": "Sudan Kordofan El Obeid RSF SAF fighting humanitarian when:7d",
        "israel_palestine": "Gaza West Bank Israel Palestine casualties strike when:1d",
        "south_sudan_abyei": "South Sudan Abyei clashes military buildup UNISFA when:30d",
        "oil_energy": "oil prices Strait of Hormuz Brent WTI tanker risk when:1d",
        "iaea_un": "IAEA UN Iran nuclear monitoring official when:7d",
        "nato_allied": "NATO allies Poland Baltic Russia Ukraine Article 5 official when:7d",
        "emerging_7d": "Thailand Cambodia Ethiopia Eritrea Guyana Venezuela Kosovo Serbia military escalation when:7d",
    }
    rss = {k: google_news(q, limit=10) for k, q in queries.items()}

    official_urls = {
        "un_news_rss": "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
        "un_press_rss": "https://press.un.org/en/rss.xml",
        "nato_news": "https://www.nato.int/cps/en/natohq/news.htm",
        "nato_press": "https://www.nato.int/cps/en/natohq/press_releases.htm",
        "iaea_news": "https://www.iaea.org/newscenter/news",
        "iaea_press": "https://www.iaea.org/newscenter/pressreleases",
        "eia_rss": "https://www.eia.gov/rss/todayinenergy.xml",
        "opec_news": "https://www.opec.org/opec_web/en/press_room/news.xml",
        "ocha_opt": "https://www.ochaopt.org/updates/feed",
        "un_sudan": "https://news.un.org/en/tags/sudan/feed",
    }
    official = {}
    for key, url in official_urls.items():
        res = fetch_url(url)
        entry = {"ok": bool(res.get("ok")), "status": res.get("status"), "url": url, "error": res.get("error"), "content_type": res.get("content_type")}
        text = res.get("text", "")
        if res.get("ok"):
            if "xml" in (res.get("content_type") or "").lower() or text.lstrip().startswith("<rss"):
                entry["items"] = parse_rss_titles(text, limit=5)
                entry["title"] = entry["items"][0]["title"] if entry.get("items") else key
            else:
                entry["title"] = page_title(text) or key
        official[key] = entry

    artifact = {
        "generated_at": ts,
        "canonical_tracker_ids": list(cfg.get("trackers", {}).keys()),
        "source_mode": "web_search_failed_http_432_then_google_news_rss_and_direct_official_feed_fallback",
        "rss": rss,
        "official": official,
        "counts": {k: v.get("count", 0) for k, v in rss.items()},
    }
    out = DATA / f"morning_deep_scan_sources_{ts.replace(':','').replace('-','')}.json"
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(json.dumps(artifact, indent=2, ensure_ascii=False))
    tmp.replace(out)
    print(json.dumps({
        "generated_at": ts,
        "artifact": str(out),
        "counts": artifact["counts"],
        "official_ok": {k: v.get("ok") for k, v in official.items()},
        "sample_heads": {k: [i.get("headline") for i in v.get("items", [])[:3]] for k, v in rss.items()},
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
