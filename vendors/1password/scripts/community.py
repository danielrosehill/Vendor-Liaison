#!/usr/bin/env python3
"""Read-only helper for the 1Password Community (Gainsight / inSided platform).

The forum's own search (/search?q=...) renders client-side, so a plain fetch
returns no results. Two things are readable without JavaScript or login:

  * /sitemap-topics-1.xml  - every topic URL with a lastmod date
  * each topic page        - schema.org QAPage JSON-LD (title, body, date,
                             author, upvoteCount, answerCount)

Subcommands (all print JSON):
  search <terms...> [--limit N] [--category home|work|developers|product-updates]
      Rank topics whose URL slug contains the terms. Slugs are titles, so this
      is a title search, not a body search. Cached for 6 h.
  topic <url>
      Summarise one topic from its JSON-LD.
  recent [--days N] [--category ...]
      Topics modified in the last N days (default 7).

Stdlib only. Never posts anything.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.request

BASE = "https://www.1password.community"
SITEMAP = f"{BASE}/sitemap-topics-1.xml"
UA = "Mozilla/5.0 (X11; Linux x86_64) onepassword-feedback-plugin"
CATEGORIES = {
    "home": "1password-at-home-31",
    "work": "1password-at-work-58",
    "developers": "developers-69",
    "product-updates": "product-updates",
}
DATA_ROOT = os.path.join(
    os.environ.get("CLAUDE_USER_DATA")
    or os.path.join(os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share"), "claude-plugins"),
    "onepassword-feedback",
)
CACHE = os.path.join(DATA_ROOT, "cache", "sitemap-topics.xml")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def sitemap(max_age=6 * 3600):
    if os.path.exists(CACHE) and time.time() - os.path.getmtime(CACHE) < max_age:
        return open(CACHE, encoding="utf-8").read()
    xml = fetch(SITEMAP)
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        f.write(xml)
    return xml


def entries(category=None):
    out = []
    for loc, lastmod in re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", sitemap()):
        path = loc[len(BASE) + 1:]
        cat, _, slug = path.partition("/")
        if category and cat != CATEGORIES.get(category, category):
            continue
        slug = re.sub(r"-\d+$", "", slug)
        out.append({"url": loc, "category": cat, "title_slug": slug, "lastmod": lastmod})
    return out


def cmd_search(a):
    terms = [t.lower() for t in a.terms]
    hits = []
    for e in entries(a.category):
        words = e["title_slug"].split("-")
        slug = " ".join(words)
        score = sum(2 if t in words else 1 for t in terms if t in slug)
        if score:
            hits.append({**e, "score": score})
    hits.sort(key=lambda h: (h["score"], h["lastmod"]), reverse=True)
    print(json.dumps({"query": terms, "total": len(hits), "results": hits[: a.limit],
                      "note": "title-slug match only; confirm in the browser tag search"}, indent=1))


def cmd_topic(a):
    html = fetch(a.url)
    q = None
    crumbs = []
    for block in re.findall(r'ld\+json"[^>]*>(.*?)</script>', html, re.S):
        try:
            d = json.loads(block)
        except ValueError:
            continue
        if d.get("@type") == "QAPage":
            q = d["mainEntity"]
        elif d.get("@type") == "BreadcrumbList":
            crumbs = [i["name"] for i in d["itemListElement"]]
    if not q:
        print(json.dumps({"url": a.url, "error": "no QAPage JSON-LD; open it in the browser"}))
        return
    print(json.dumps({
        "url": a.url,
        "category": crumbs[3] if len(crumbs) > 3 else None,
        "title": q.get("name"),
        "created": q.get("dateCreated"),
        "author": (q.get("author") or {}).get("name"),
        "upvotes": q.get("upvoteCount"),
        "replies": q.get("answerCount"),
        "accepted_answer": bool(q.get("acceptedAnswer")),
        "body": q.get("text"),
        "note": "JSON-LD carries the opening post only; read replies and tags in the browser",
    }, indent=1))


def cmd_recent(a):
    since = (dt.date.today() - dt.timedelta(days=a.days)).isoformat()
    rows = sorted((e for e in entries(a.category) if e["lastmod"] >= since),
                  key=lambda e: e["lastmod"], reverse=True)
    print(json.dumps({"since": since, "total": len(rows), "results": rows}, indent=1))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("search"); s.add_argument("terms", nargs="+"); s.add_argument("--limit", type=int, default=20)
    s.add_argument("--category"); s.set_defaults(fn=cmd_search)
    t = sp.add_parser("topic"); t.add_argument("url"); t.set_defaults(fn=cmd_topic)
    r = sp.add_parser("recent"); r.add_argument("--days", type=int, default=7); r.add_argument("--category")
    r.set_defaults(fn=cmd_recent)
    a = p.parse_args()
    try:
        a.fn(a)
    except Exception as e:  # network or parse failure: report, don't traceback
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
