#!/usr/bin/env python3
"""Crawl a locally served build and record what each page actually renders.

Reads rendered HTML only. For every internal page it records status, title,
meta description, canonical, Open Graph tags, heading outline, images, and
every link. Then it resolves every internal link (and its #fragment) against
the pages it fetched.

Usage: crawl_site.py BASE_URL OUT_JSON [extra start paths...]
"""
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

BASE = sys.argv[1].rstrip("/")
OUT = sys.argv[2]
START = ["/", "/sitemap.xml"] + sys.argv[3:]
HOST = urllib.parse.urlsplit(BASE).netloc
SKIP_EXT = (".pdf", ".epub", ".zip", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif",
            ".ico", ".xml", ".json", ".txt", ".css", ".js", ".mp4", ".webm", ".woff2")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(path, method="GET"):
    """Returns (status, headers, body_text). Redirects are reported, not followed."""
    req = urllib.request.Request(BASE + path, method=method,
                                 headers={"User-Agent": "site-crawl/1.0"})
    try:
        with OPENER.open(req, timeout=30) as r:
            body = r.read() if method == "GET" else b""
            return r.status, dict(r.headers), body.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = e.read() if method == "GET" else b""
        return e.code, dict(e.headers), body.decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return 0, {}, f"{type(e).__name__}: {e}"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = {}
        self.links = []          # (href, text, rel, target)
        self.images = []         # (src, alt or None, loading, width, height)
        self.headings = []       # (level, text)
        self.ids = set()
        self.canonical = None
        self.iframes = []
        self.scripts = []
        self.stylesheets = []
        self.lang = None
        self.buttons_without_name = 0
        self.inputs = []         # (type, id, name, aria-label, has placeholder)
        self.labels_for = set()
        self._stack = []
        self._cap = None
        self._cur_link = None
        self._cur_button = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._cap = ("title", [])
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            if a.get("rel") == "canonical":
                self.canonical = a.get("href")
            if a.get("rel") == "stylesheet":
                self.stylesheets.append(a.get("href", ""))
        elif tag == "a":
            self._cur_link = {"href": a.get("href"), "text": [], "rel": a.get("rel", ""),
                              "target": a.get("target", ""), "aria": a.get("aria-label", "")}
        elif tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt"),
                                "loading": a.get("loading"), "w": a.get("width"),
                                "h": a.get("height")})
            if self._cur_link is not None and a.get("alt"):
                self._cur_link["text"].append(a["alt"])
        elif tag in ("h1", "h2", "h3", "h4"):
            self._cap = (tag, [])
        elif tag == "iframe":
            self.iframes.append({"src": a.get("src", ""), "title": a.get("title")})
        elif tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        elif tag == "button":
            self._cur_button = {"text": [], "aria": a.get("aria-label", "") or a.get("title", "")}
        elif tag in ("input", "textarea", "select"):
            self.inputs.append({"type": a.get("type", tag), "id": a.get("id"),
                                "name": a.get("name"), "aria": a.get("aria-label")
                                or a.get("aria-labelledby"), "hidden": a.get("type") == "hidden"})
        elif tag == "label" and a.get("for"):
            self.labels_for.add(a["for"])

    def handle_endtag(self, tag):
        if self._cap and tag == self._cap[0]:
            text = re.sub(r"\s+", " ", "".join(self._cap[1])).strip()
            if tag == "title":
                self.title = text
            else:
                self.headings.append((int(tag[1]), text))
            self._cap = None
        if tag == "a" and self._cur_link is not None:
            L = self._cur_link
            L["text"] = re.sub(r"\s+", " ", " ".join(L["text"])).strip()
            self.links.append(L)
            self._cur_link = None
        if tag == "button" and self._cur_button is not None:
            name = re.sub(r"\s+", " ", " ".join(self._cur_button["text"])).strip()
            if not name and not self._cur_button["aria"]:
                self.buttons_without_name += 1
            self._cur_button = None

    def handle_data(self, data):
        if self._cap:
            self._cap[1].append(data)
        if self._cur_link is not None:
            self._cur_link["text"].append(data)
        if self._cur_button is not None:
            self._cur_button["text"].append(data)


def norm(path):
    p = urllib.parse.urlsplit(path)
    out = p.path or "/"
    if len(out) > 1 and out.endswith("/"):
        out = out[:-1]
    return out


pages, queue, seen = {}, list(START), set()
external = {}
while queue:
    path = queue.pop(0)
    key = norm(path)
    if key in seen:
        continue
    seen.add(key)
    status, headers, body = fetch(key)
    rec = {"status": status, "location": headers.get("Location") or headers.get("location")}
    ctype = (headers.get("Content-Type") or headers.get("content-type") or "")
    if key == "/sitemap.xml" and status == 200:
        locs = re.findall(r"<loc>([^<]+)</loc>", body)
        rec["sitemap_locs"] = locs
        for loc in locs:
            queue.append(norm(urllib.parse.urlsplit(html.unescape(loc)).path))
        pages[key] = rec
        continue
    if status in (301, 302, 307, 308) and rec["location"]:
        tgt = urllib.parse.urljoin(BASE + key, rec["location"])
        if urllib.parse.urlsplit(tgt).netloc == HOST:
            queue.append(norm(tgt))
        pages[key] = rec
        continue
    if status != 200 or "html" not in ctype:
        rec["ctype"] = ctype
        pages[key] = rec
        continue
    p = Page()
    p.feed(body)
    text = re.sub(r"\s+", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S))
    text = re.sub(r"<[^>]+>", " ", text)
    rec.update({
        "bytes": len(body), "title": p.title, "lang": p.lang,
        "description": p.meta.get("description"), "canonical": p.canonical,
        "og": {k: v for k, v in p.meta.items() if k.startswith("og:") or k.startswith("twitter:")},
        "robots": p.meta.get("robots"),
        "headings": p.headings, "ids": sorted(p.ids), "images": p.images,
        "iframes": p.iframes, "scripts": p.scripts, "stylesheets": p.stylesheets,
        "buttons_without_name": p.buttons_without_name,
        "inputs": p.inputs, "labels_for": sorted(p.labels_for),
        "words": len(html.unescape(text).split()),
        "links": [],
    })
    for L in p.links:
        href = (L["href"] or "").strip()
        if not href or href.startswith(("mailto:", "tel:", "javascript:")):
            rec["links"].append({**L, "kind": "other"})
            continue
        absu = urllib.parse.urljoin(BASE + key, href)
        sp = urllib.parse.urlsplit(absu)
        if sp.netloc == HOST:
            target = norm(sp.path)
            rec["links"].append({**L, "kind": "internal", "path": target, "frag": sp.fragment})
            if not target.lower().endswith(SKIP_EXT):
                queue.append(target)
        else:
            rec["links"].append({**L, "kind": "external", "url": absu})
            external.setdefault(absu, []).append(key)
    pages[key] = rec

# Resolve every internal link against what was fetched.
problems = []
import os
if os.environ.get('CRAWL_CONTROL') and '/' in pages:
    # Two links known to be bad, so a clean result can be trusted.
    pages['/']['links'] += [
        {'kind': 'internal', 'path': '/__control_missing__', 'frag': '', 'text': 'control: missing page'},
        {'kind': 'internal', 'path': '/about', 'frag': '__no_such_anchor__', 'text': 'control: dead anchor'}]
for src, rec in list(pages.items()):
    for L in rec.get("links", []):
        if L["kind"] != "internal":
            continue
        tgt = L["path"]
        if tgt not in pages:
            st, hd, _ = fetch(tgt, "GET")
            pages[tgt] = {"status": st, "location": hd.get("Location") or hd.get("location"),
                          "asset": True}
        t = pages[tgt]
        if t["status"] >= 400 or t["status"] == 0:
            problems.append({"type": "broken_link", "from": src, "to": tgt,
                             "status": t["status"], "text": L["text"][:60]})
        elif L["frag"] and "ids" in t and L["frag"] not in t["ids"]:
            problems.append({"type": "dead_anchor", "from": src, "to": f"{tgt}#{L['frag']}",
                             "text": L["text"][:60]})

json.dump({"base": BASE, "pages": pages, "external": external, "problems": problems},
          open(OUT, "w"), indent=1)
html_pages = [k for k, v in pages.items() if "title" in v]
print(f"fetched {len(pages)} urls, {len(html_pages)} html pages, "
      f"{len(external)} distinct external links, {len(problems)} internal link problems")
