#!/usr/bin/env python3
"""
sts.py — Surviving the Singularity project API.

One tool to inspect, audit, and report on the book and the website.
Stdlib only. Run from anywhere; it finds the repo root on its own.

Commands:
    status    One-screen dashboard: git, book, audit errors, stripe, live drift
    audit     Full site audit: routes, links, assets, meta, sitemap, placeholders
    book      Book manuscript stats: per-chapter word counts, thin chapters
    quotes    Inject chapter epigraphs from scripts/chapter_quotes.json
    images    Fetch (Wikimedia Commons, license-gated) + inject chapter header images
    verify    Fact-checking harness. Recomputes every calculation the book
              shows its reader, catches subtitle/price drift across the site
              and the built file, and audits Precedent Ledger integrity.
              `verify links` liveness-checks every Works Cited URL.
    og        Share cards. No args audits every public page for a resolvable
              og:image (a page without one shares as a bare blue link);
              --render rebuilds them from scripts/og_cards.json at 1200x630.
    schema    Which sql/ migrations have actually reached the live database.
              A committed migration file is not an applied migration; the
              app swallows both "table missing" and "column missing", so
              nothing else surfaces the gap.
    stripe    Stripe go-live readiness (masks all secrets); --live probes
              production for live-vs-test mode, webhook health, and whether
              the price charged matches the price advertised
    live      Probe production and compare against local routes (deploy drift)
    sitemap   Check sitemap.xml against real routes; --write regenerates it
    routes    List every route the site actually serves
    research  Search the web (Wikipedia + DuckDuckGo) for sources/examples;
              --save appends results to manuscript/sources/research-log.md
    compile   Concatenate the book source (src/lib/data/book, book.json order)
              into a single manuscript draft markdown file
    scan      Scannability audit: pull-quote candidates, wall-of-text
              paragraphs, heading/emphasis deserts, list opportunities,
              per-chapter texture scores
    id        Manuscript addressing: a stable unique id for every block
              (build|list|get|replace|verify|stress). Non-invasive sidecar
              index (src/lib/data/book/manuscript-index.json); the .md source
              stays clean, so building the index is not a content change.
    flow      Export every manuscript figure into one flat, upload-ready
              folder (SVG diagrams rasterized to opaque PNG), with a
              MANIFEST.md whose per-asset "prompt" is the figure's alt text.
              Built for dropping the book's art into Google Flow.
    art       Enroll every book figure in art-catalog.json (list|sync).
              Data-driven from the manuscript index + credits.json; ids are
              sts.<kind>.<filename-stem> so new art auto-enrolls.
    cover     Keep the website's cover art in sync with the book's. Reports
              which site assets still carry an older cover; --sync
              regenerates every derivative from art-raw/book-cover-final-source.png.

Every command accepts --json for machine-readable output.
`audit` and `sitemap` exit non-zero when errors are found (CI-friendly).

Examples:
    python3 scripts/sts.py status
    python3 scripts/sts.py audit --json
    python3 scripts/sts.py book --thin 1500
    python3 scripts/sts.py sitemap --write
    python3 scripts/sts.py live
"""

import argparse
import collections
import hashlib
import hmac
import html as html_mod
import json
import os
import re
import shutil
import tempfile
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

VERSION = "0.0.1"
SITE = "https://survivingthesingularity.com"

# Routes that existed in old builds and must never be linked again
# (see CLAUDE.md: removed in a past redesign).
DEAD_ROUTES = {
    "/blueprint", "/evidence", "/agi", "/why", "/timeline",
    "/login", "/profile", "/auth", "/sitemap", "/newsletter",
}

# Non-page paths that are legitimately linkable.
API_PREFIXES = ("/api/",)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "svelte.config.js").exists():
            return parent
    sys.exit("sts.py: could not locate repo root (no svelte.config.js above me)")


ROOT = repo_root()
ROUTES_DIR = ROOT / "src" / "routes"
STATIC_DIR = ROOT / "static"
BOOK_DIR = ROOT / "src" / "lib" / "data" / "book"

# How many Precedents the Ledger is supposed to contain. Asserted here on
# purpose rather than counted from Appendix D: the whole point of the check
# is to compare the chapters against an independent number, and deriving it
# from the index would make the comparison a tautology. Bump it when a
# precedent is added, and `verify precedents` will name whichever end of
# the renumber you missed.
LEDGER_SIZE = 23


# ──────────────────────────────────────────────────────────────────────
# Shared collectors
# ──────────────────────────────────────────────────────────────────────

def collect_routes() -> dict:
    """Enumerate real routes from src/routes. Returns {'pages': [...], 'apis': [...]}."""
    pages, apis = [], []
    for marker in ROUTES_DIR.rglob("+page.svelte"):
        rel = marker.parent.relative_to(ROUTES_DIR)
        route = "/" + "/".join(rel.parts) if rel.parts else "/"
        pages.append(route)
    for marker in ROUTES_DIR.rglob("+server.js"):
        rel = marker.parent.relative_to(ROUTES_DIR)
        apis.append("/" + "/".join(rel.parts))
    return {"pages": sorted(set(pages)), "apis": sorted(set(apis))}


def route_matches(path: str, routes: list) -> bool:
    """True if `path` is served by a concrete or [param] route."""
    if path in routes:
        return True
    parts = path.strip("/").split("/")
    for route in routes:
        rparts = route.strip("/").split("/")
        if len(rparts) != len(parts):
            continue
        if all(rp.startswith("[") or rp == p for rp, p in zip(rparts, parts)):
            return True
    return False


def static_serves(path: str) -> bool:
    p = STATIC_DIR / path.lstrip("/")
    return p.exists() or (p / "index.html").exists()


def extract_internal_refs() -> list:
    """Pull every internal href/src/srcset target out of src/**/*.svelte.

    Returns [(file, line_no, path)] with query/hash stripped (fragment-only
    links resolve to their page).
    """
    refs = []
    pattern = re.compile(r'(?:href|src)\s*=\s*"(/[^"{}\s]*)"')
    srcset_pat = re.compile(r'srcset\s*=\s*"([^"{}]+)"')
    for svelte in (ROOT / "src").rglob("*.svelte"):
        rel = str(svelte.relative_to(ROOT))
        for n, line in enumerate(svelte.read_text(encoding="utf-8").splitlines(), 1):
            for m in pattern.finditer(line):
                target = m.group(1).split("#")[0].split("?")[0] or "/"
                refs.append((rel, n, target))
            for m in srcset_pat.finditer(line):
                for candidate in m.group(1).split(","):
                    url = candidate.strip().split(" ")[0]
                    if url.startswith("/"):
                        refs.append((rel, n, url))
    return refs


def git(*args) -> str:
    out = subprocess.run(["git", "-C", str(ROOT), *args],
                         capture_output=True, text=True)
    return out.stdout.strip()


# ──────────────────────────────────────────────────────────────────────
# audit
# ──────────────────────────────────────────────────────────────────────

def cmd_audit(args) -> int:
    routes = collect_routes()
    pages, apis = routes["pages"], routes["apis"]
    errors, warnings = [], []

    # 1. Internal links and asset references
    for rel, n, target in extract_internal_refs():
        base = target.rstrip("/") or "/"
        if base in DEAD_ROUTES or any(base.startswith(d + "/") for d in DEAD_ROUTES):
            errors.append(f"{rel}:{n} links dead route {target}")
        elif base.startswith(API_PREFIXES):
            if not route_matches(base, apis):
                errors.append(f"{rel}:{n} calls missing API {target}")
        elif route_matches(base, pages):
            pass
        elif static_serves(base):
            pass
        else:
            errors.append(f"{rel}:{n} broken internal ref {target}")

    # 2. Static files that shadow SvelteKit routes (adapter serves static first)
    for page in pages:
        if page == "/":
            continue
        shadow = STATIC_DIR / page.lstrip("/")
        if (shadow / "index.html").exists() or shadow.with_suffix(".html").exists():
            errors.append(f"static{page} shadows route {page} — stale page will be served")

    # 3. Per-page head meta. A page may legitimately delegate its head to a
    # layout - routes behind the book gate have to, because the page component
    # only renders once the gate is open and a crawler never gets that far - so
    # walk the layout chain before calling a head missing.
    def layout_supplies_head(page_path: Path) -> bool:
        d = page_path.parent
        while True:
            layout = d / "+layout.svelte"
            if layout.exists() and "<svelte:head>" in layout.read_text(encoding="utf-8"):
                return True
            if d == ROUTES_DIR:
                return False
            d = d.parent

    for marker in ROUTES_DIR.rglob("+page.svelte"):
        rel = str(marker.relative_to(ROOT))
        text = marker.read_text(encoding="utf-8")
        head = re.search(r"<svelte:head>(.*?)</svelte:head>", text, re.DOTALL)
        if not head:
            if not layout_supplies_head(marker):
                warnings.append(f"{rel}: no <svelte:head> (title/description missing)")
            continue
        h = head.group(1)
        if "<title>" not in h:
            warnings.append(f"{rel}: missing <title>")
        if 'name="description"' not in h:
            warnings.append(f"{rel}: missing meta description")
        for m in re.finditer(r'property="og:image"\s+content="([^"]+)"', h):
            if m.group(1).startswith("/"):
                errors.append(f"{rel}: og:image is relative ({m.group(1)}) — social cards will break")

    # 4. $page.url.origin in prerendered heads requires kit.prerender.origin
    config = (ROOT / "svelte.config.js").read_text(encoding="utf-8")
    prerender_origin_set = re.search(r"origin:\s*['\"]https?://", config)
    if not prerender_origin_set:
        for marker in ROUTES_DIR.rglob("+page.svelte"):
            text = marker.read_text(encoding="utf-8")
            head = re.search(r"<svelte:head>(.*?)</svelte:head>", text, re.DOTALL)
            if head and "$page.url" in head.group(1):
                errors.append(
                    f"{marker.relative_to(ROOT)}: $page.url in <svelte:head> but "
                    "kit.prerender.origin is unset — prerendered og tags bake in "
                    "http://sveltekit-prerender"
                )

    # 5. Placeholder debris in shipped markup (input placeholders and CSS
    # ::placeholder are legitimate — only flag genuine leftovers)
    debris = re.compile(r'href="#"|\bTODO\b|\bFIXME\b|lorem ipsum', re.IGNORECASE)
    for svelte in (ROOT / "src").rglob("*.svelte"):
        rel = str(svelte.relative_to(ROOT))
        for n, line in enumerate(svelte.read_text(encoding="utf-8").splitlines(), 1):
            if debris.search(line):
                warnings.append(f"{rel}:{n} placeholder debris: {line.strip()[:90]}")

    # 6. Sitemap coherence (reuses sitemap check)
    sm_errors, _ = check_sitemap(pages)
    errors.extend(sm_errors)

    result = {"errors": errors, "warnings": warnings,
              "pages": len(pages), "apis": len(apis)}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"sts audit — {len(pages)} pages, {len(apis)} API routes")
        for e in errors:
            print(f"  ERROR  {e}")
        for w in warnings:
            print(f"  warn   {w}")
        print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


# ──────────────────────────────────────────────────────────────────────
# sitemap
# ──────────────────────────────────────────────────────────────────────

def sitemap_urls() -> list:
    sm = STATIC_DIR / "sitemap.xml"
    if not sm.exists():
        return []
    return re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8"))


NOINDEX_RE = re.compile(r'name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)


def route_is_noindex(route: str) -> bool:
    """True if the route declares robots noindex, on its page or a layout above it.

    A page that says noindex has opted out of search on purpose. Listing it in
    sitemap.xml tells a crawler "fetch this" and "do not index this" in the same
    breath, and it hands out the URL of a page that was meant to be shared by
    link only. /exclusive-friends-only is exactly that: the whole book behind one
    password, noindex+nofollow.

    The layout walk is load-bearing, not defensive. The gated routes moved their
    whole head into +layout.svelte, because the page component only renders once
    the password gate opens and a crawler never gets that far. Reading only
    +page.svelte after that move sees no noindex on /book or /read, decides they
    are public, and demands they be added to the sitemap - the exact opposite of
    what those pages ask for.
    """
    def declares(f: Path) -> bool:
        return f.exists() and bool(
            NOINDEX_RE.search(f.read_text(encoding="utf-8", errors="ignore")))

    rel = "" if route == "/" else route.lstrip("/")
    d = (ROUTES_DIR / rel) if rel else ROUTES_DIR
    if not (d / "+page.svelte").exists():
        return False
    # The route's own page, then only the LAYOUTS above it. A parent directory's
    # +page.svelte is a sibling route, not an ancestor - inheriting its noindex
    # would silently drop unrelated pages out of the sitemap.
    if declares(d / "+page.svelte"):
        return True
    while True:
        if declares(d / "+layout.svelte"):
            return True
        if d == ROUTES_DIR:
            return False
        d = d.parent


def public_pages(pages: list) -> list:
    """Pages that belong in the sitemap (skip utility/dynamic/transactional).

    `skip` covers routes with no meta of their own to read. Everything else is
    decided by the page itself via robots noindex, so a new private page stops
    warning the moment it is written, and starts warning again the moment
    someone deletes its noindex - which is the change actually worth flagging.
    """
    skip = {"/unsubscribe", "/early-access/success"}
    return [p for p in pages
            if "[" not in p and p not in skip and not route_is_noindex(p)]


def check_sitemap(pages: list):
    """Three distinct faults, which used to be collapsed into one message.

    A URL with no route behind it is a 404 served to a crawler. A URL whose
    route exists but declares noindex is not a 404 at all - it is the sitemap
    and the page giving a crawler opposite instructions. Reporting the second
    as "no such route exists" sends whoever reads it hunting for a missing file
    that is sitting right there.
    """
    errors, missing = [], []
    listed = {u.replace(SITE, "") or "/" for u in sitemap_urls()}
    real = {p for p in pages if "[" not in p}
    should_list = set(public_pages(pages))

    for ghost in sorted(listed - real):
        errors.append(f"sitemap.xml lists {ghost} but no such route exists (404 to crawlers)")
    for clash in sorted((listed & real) - should_list):
        errors.append(f"sitemap.xml lists {clash}, but that page sets robots noindex "
                      f"- the sitemap invites the crawl the page then refuses")
    for m in sorted(should_list - listed):
        missing.append(m)
    return errors, missing


def cmd_sitemap(args) -> int:
    pages = collect_routes()["pages"]
    errors, missing = check_sitemap(pages)
    if args.write:
        today = date.today().isoformat()
        prio = {"/": "1.0", "/early-access": "0.9", "/book": "0.9",
                "/checklist": "0.8", "/signals": "0.7", "/blog": "0.7"}
        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for p in sorted(public_pages(pages), key=lambda r: (r != "/", r)):
            lines += ["  <url>",
                      f"    <loc>{SITE}{'' if p == '/' else p}</loc>",
                      f"    <lastmod>{today}</lastmod>",
                      f"    <priority>{prio.get(p, '0.5')}</priority>",
                      "  </url>"]
        lines.append("</urlset>")
        (STATIC_DIR / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"sitemap.xml rewritten: {len(public_pages(pages))} URLs")
        return 0
    result = {"ghosts": errors, "missing": missing}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for e in errors:
            print(f"  ERROR  {e}")
        for m in missing:
            print(f"  warn   route {m} not in sitemap.xml")
        if not errors and not missing:
            print("sitemap.xml matches the real route table")
    return 1 if errors else 0


# ──────────────────────────────────────────────────────────────────────
# book
# ──────────────────────────────────────────────────────────────────────

def strip_md(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[#>*_`|-]", " ", text)
    return text


def book_stats() -> dict:
    meta = json.loads((BOOK_DIR / "book.json").read_text(encoding="utf-8"))
    sections = []
    for s in meta["sections"]:
        f = BOOK_DIR / s["file"]
        words = len(strip_md(f.read_text(encoding="utf-8")).split()) if f.exists() else 0
        sections.append({"id": s["id"], "title": s["title"],
                         "file": s["file"], "words": words,
                         "exists": f.exists()})
    return {"title": meta["title"], "version": meta["version"],
            "lastUpdated": meta.get("lastUpdated"),
            "total_words": sum(s["words"] for s in sections),
            "sections": sections}


def cmd_book(args) -> int:
    stats = book_stats()
    if args.json:
        print(json.dumps(stats, indent=2))
        return 0
    print(f"{stats['title']} — v{stats['version']} — "
          f"{stats['total_words']:,} words (updated {stats['lastUpdated']})")
    for s in stats["sections"]:
        chapterish = s["id"].startswith("chapter") or s["id"] in ("conclusion",)
        thin = chapterish and s["words"] < args.thin
        flag = "  <- THIN" if thin else ("  <- MISSING" if not s["exists"] else "")
        print(f"  {s['words']:>7,}  {s['title']}{flag}")
    return 0


# ──────────────────────────────────────────────────────────────────────
# quotes (chapter epigraphs)
# ──────────────────────────────────────────────────────────────────────

def load_quote_registry() -> list:
    reg = json.loads((ROOT / "scripts" / "chapter_quotes.json").read_text(encoding="utf-8"))
    return reg["quotes"]


def epigraph_block(q: dict) -> str:
    attribution = q["author"]
    if q.get("source"):
        attribution += f", *{q['source']}*"
    if q.get("year"):
        attribution += f" ({q['year']})"
    return f'> *"{q["quote"]}"*\n> — {attribution}'


def inject_epigraph(text: str, q: dict) -> tuple:
    """Insert (or refresh) an epigraph blockquote right under the first heading
    matching q['match']. Returns (new_text, action) where action is one of
    'inserted', 'replaced', 'unchanged', 'no-heading'."""
    heading_re = re.compile(q["match"], re.IGNORECASE | re.MULTILINE)
    m = heading_re.search(text)
    if not m:
        return text, "no-heading"
    lines = text.splitlines(keepends=True)
    # locate the heading's line index
    upto = text[:m.start()].count("\n")
    i = upto + 1
    # skip blank lines after the heading
    j = i
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    # skip a chapter header image block (image + optional italic caption):
    # the epigraph slot sits below it
    if j < len(lines) and lines[j].lstrip().startswith("!["):
        j += 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and re.match(r"^\*[^*].*\*\s*$", lines[j].strip()):
            j += 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
        i = j  # if we insert, insert below the image block
    block = epigraph_block(q) + "\n"
    # an existing blockquote right under the title is the epigraph slot
    if j < len(lines) and lines[j].lstrip().startswith(">"):
        k = j
        while k < len(lines) and (lines[k].lstrip().startswith(">") or lines[k].strip() == ""):
            if lines[k].strip() == "" and k + 1 < len(lines) and not lines[k + 1].lstrip().startswith(">"):
                break
            k += 1
        existing = "".join(lines[j:k])
        if existing.strip() == block.strip():
            return text, "unchanged"
        new = "".join(lines[:j]) + block + "".join(lines[k:])
        return new, "replaced"
    new = "".join(lines[:i]) + "\n" + block + "\n" + "".join(lines[i:])
    return new, "inserted"


def load_image_registry() -> list:
    reg = json.loads((ROOT / "scripts" / "chapter_images.json").read_text(encoding="utf-8"))
    return reg["images"]


ALLOWED_LICENSES = re.compile(r"public domain|cc0|^cc.by(.sa)?", re.IGNORECASE)
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
IMAGES_DIR = STATIC_DIR / "book-images"


UA = f"sts.py/{VERSION} (https://survivingthesingularity.com; book tooling; contact: site owner)"


def _polite_open(url: str, timeout: float = 60.0, tries: int = 4):
    """urlopen with backoff — Wikimedia 429s bursty anonymous clients."""
    import time
    delay = 3.0
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < tries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise


def _commons_get(params: dict) -> dict:
    import urllib.parse
    qs = urllib.parse.urlencode({**params, "format": "json"})
    with _polite_open(f"{COMMONS_API}?{qs}", timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _commons_imageinfo(title: str) -> dict:
    data = _commons_get({
        "action": "query", "titles": title, "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "iiurlwidth": "1600",
    })
    pages = data.get("query", {}).get("pages", {})
    for p in pages.values():
        for ii in p.get("imageinfo", []):
            meta = ii.get("extmetadata", {})
            return {
                "title": p.get("title", title),
                "url": ii.get("thumburl") or ii.get("url"),
                "width": ii.get("width", 0),
                "license": meta.get("LicenseShortName", {}).get("value", ""),
                "artist": re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip(),
                "page": ii.get("descriptionurl", ""),
            }
    return {}


def _commons_search(term: str) -> dict:
    data = _commons_get({
        "action": "query", "generator": "search",
        "gsrsearch": f"filetype:bitmap {term}", "gsrnamespace": "6", "gsrlimit": "8",
        "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": "1600",
    })
    pages = data.get("query", {}).get("pages", {})
    best = {}
    for p in sorted(pages.values(), key=lambda x: x.get("index", 99)):
        for ii in p.get("imageinfo", []):
            meta = ii.get("extmetadata", {})
            lic = meta.get("LicenseShortName", {}).get("value", "")
            if not ALLOWED_LICENSES.search(lic):
                continue
            if ii.get("width", 0) < 1000:
                continue
            return {
                "title": p.get("title", ""),
                "url": ii.get("thumburl") or ii.get("url"),
                "width": ii.get("width", 0),
                "license": lic,
                "artist": re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip(),
                "page": ii.get("descriptionurl", ""),
            }
    return best


def fetch_chapter_images(only_missing=True) -> list:
    """Download registry images that don't exist locally; update credits.json."""
    credits_path = IMAGES_DIR / "credits.json"
    credits = json.loads(credits_path.read_text(encoding="utf-8")) if credits_path.exists() else []
    by_file = {c["file"]: c for c in credits}
    report = []
    for entry in load_image_registry():
        dest = IMAGES_DIR / entry["file"]
        if dest.exists() and only_missing:
            report.append({"key": entry["key"], "file": entry["file"], "action": "exists"})
            continue
        info = {}
        if entry.get("commons"):
            info = _commons_imageinfo(entry["commons"])
            if info and not ALLOWED_LICENSES.search(info.get("license", "")):
                report.append({"key": entry["key"], "file": entry["file"],
                               "action": f"license-blocked ({info.get('license')})"})
                continue
        if not info.get("url") and entry.get("search"):
            info = _commons_search(entry["search"])
        if not info.get("url"):
            report.append({"key": entry["key"], "file": entry["file"], "action": "no-source"})
            continue
        import time
        try:
            with _polite_open(info["url"]) as resp:
                dest.write_bytes(resp.read())
        except Exception as e:
            report.append({"key": entry["key"], "file": entry["file"],
                           "action": f"download-failed ({e})"})
            continue
        time.sleep(1.5)  # stay under Wikimedia burst limits
        by_file[entry["file"]] = {
            "file": entry["file"], "source_title": info["title"],
            "page": info["page"], "artist": info["artist"], "license": info["license"],
        }
        report.append({"key": entry["key"], "file": entry["file"],
                       "action": f"downloaded ({info['license']})"})
    credits_path.write_text(json.dumps(sorted(by_file.values(), key=lambda c: c["file"]),
                                       indent=1) + "\n", encoding="utf-8")
    return report


def image_block(entry: dict, credits: dict) -> str:
    c = credits.get(entry["file"], {})
    credit = ""
    if c:
        artist = c.get("artist", "")
        lic = c.get("license", "")
        bits = ", ".join(b for b in (artist, lic) if b)
        credit = f" ({bits}, via Wikimedia Commons)" if bits else ""
    return f'![{entry["alt"]}](/book-images/{entry["file"]})\n\n*{entry["caption"]}{credit}*'


def inject_image(text: str, entry: dict, credits: dict) -> tuple:
    """Insert (or refresh) a header image directly under the chapter heading,
    above the epigraph blockquote."""
    heading_re = re.compile(entry["match"], re.IGNORECASE | re.MULTILINE)
    m = heading_re.search(text)
    if not m:
        return text, "no-heading"
    lines = text.splitlines(keepends=True)
    i = text[:m.start()].count("\n") + 1
    j = i
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    block = image_block(entry, credits) + "\n"
    if j < len(lines) and lines[j].lstrip().startswith("!["):
        k = j + 1
        while k < len(lines) and lines[k].strip() == "":
            k += 1
        if k < len(lines) and re.match(r"^\*[^*].*\*\s*$", lines[k].strip()):
            k += 1
        existing = "".join(lines[j:k])
        if existing.strip() == block.strip():
            return text, "unchanged"
        return "".join(lines[:j]) + block + "".join(lines[k:]), "replaced"
    return "".join(lines[:i]) + "\n" + block + "\n" + "".join(lines[i:]), "inserted"


def cmd_images(args) -> int:
    if args.fetch:
        report = fetch_chapter_images()
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print("sts images --fetch")
            for r in report:
                print(f"  {r['action']:<28} {r['key']:<14} {r['file']}")
        bad = [r for r in report if r["action"] in ("no-source",) or r["action"].startswith("license-")]
        return 1 if bad else 0

    registry = load_image_registry()
    credits_path = IMAGES_DIR / "credits.json"
    credits = {c["file"]: c for c in json.loads(credits_path.read_text(encoding="utf-8"))} \
        if credits_path.exists() else {}
    results = []
    missing = [e for e in registry if not (IMAGES_DIR / e["file"]).exists()]
    if missing and args.apply:
        sys.exit(f"sts images: {len(missing)} image files missing — run `sts.py images --fetch` first "
                 f"({', '.join(e['file'] for e in missing[:4])}…)")
    if args.file:
        target = Path(args.file).expanduser()
        text = target.read_text(encoding="utf-8")
        for e in registry:
            text, action = inject_image(text, e, credits)
            results.append({"key": e["key"], "file": str(target), "action": action})
        if args.apply:
            target.write_text(text, encoding="utf-8")
        elif args.stdout:
            sys.stdout.write(text)
            return 1 if any(r["action"] == "no-heading" for r in results) else 0
    else:
        meta = json.loads((BOOK_DIR / "book.json").read_text(encoding="utf-8"))
        files = {s["id"]: BOOK_DIR / s["file"] for s in meta["sections"]}
        for e in registry:
            f = files.get(e["key"])
            if not f or not f.exists():
                results.append({"key": e["key"], "file": None, "action": "no-file"})
                continue
            text = f.read_text(encoding="utf-8")
            new, action = inject_image(text, e, credits)
            if args.apply and action in ("inserted", "replaced"):
                f.write_text(new, encoding="utf-8")
            results.append({"key": e["key"], "file": str(f.relative_to(ROOT)), "action": action})
    bad = [r for r in results if r["action"] in ("no-heading", "no-file")]
    if args.json:
        print(json.dumps({"applied": args.apply, "results": results}, indent=2))
    else:
        mode = "APPLIED" if args.apply else "dry-run (use --apply to write)"
        print(f"sts images — {len(registry)} header images — {mode}")
        for r in results:
            print(f"  {r['action']:<10} {r['key']:<14} {r['file'] or '-'}")
    return 1 if bad else 0


def cmd_quotes(args) -> int:
    registry = load_quote_registry()
    results = []
    if args.file:
        target = Path(args.file).expanduser()
        text = target.read_text(encoding="utf-8")
        for q in registry:
            text, action = inject_epigraph(text, q)
            results.append({"key": q["key"], "file": str(target), "action": action})
        if args.apply:
            target.write_text(text, encoding="utf-8")
        elif args.stdout:
            sys.stdout.write(text)
            return 1 if any(r["action"] == "no-heading" for r in results) else 0
    else:
        meta = json.loads((BOOK_DIR / "book.json").read_text(encoding="utf-8"))
        files = {s["id"]: BOOK_DIR / s["file"] for s in meta["sections"]}
        for q in registry:
            f = files.get(q["key"])
            if not f or not f.exists():
                results.append({"key": q["key"], "file": None, "action": "no-file"})
                continue
            text = f.read_text(encoding="utf-8")
            new, action = inject_epigraph(text, q)
            if args.apply and action in ("inserted", "replaced"):
                f.write_text(new, encoding="utf-8")
            results.append({"key": q["key"], "file": str(f.relative_to(ROOT)), "action": action})
    bad = [r for r in results if r["action"] in ("no-heading", "no-file")]
    if args.json:
        print(json.dumps({"applied": args.apply, "results": results}, indent=2))
    else:
        mode = "APPLIED" if args.apply else "dry-run (use --apply to write)"
        print(f"sts quotes — {len(registry)} epigraphs — {mode}")
        for r in results:
            print(f"  {r['action']:<10} {r['key']:<14} {r['file'] or '-'}")
    return 1 if bad else 0


# ──────────────────────────────────────────────────────────────────────
# backup — Supabase redundancy
# ──────────────────────────────────────────────────────────────────────
#
# Every customer record the business has - the waitlist, the preorders, the
# fulfilment ledger - lives in exactly one Supabase project, and until this
# command existed there was no second copy of any of it. Supabase's own
# point-in-time recovery is a paid add-on and, either way, a backup you have
# never restored from is a rumour. This writes a plain-text dump you can read
# with `cat`, verify with a hash, and restore with `resolve-artifacts`-free
# ordinary HTTP.
#
# Deliberately not pg_dump: there is no direct Postgres connection string in
# this project (Supabase issues one, but it is not in .env and putting it
# there widens the blast radius of a leaked file), and neither pg_dump nor
# the supabase CLI is installed. PostgREST reaches the same rows with the
# credential the app already uses.

BACKUP_DEFAULT_DIR = Path.home() / "Backups" / "sts-supabase"
BACKUP_STORAGE_BUCKETS = ("downloads",)
BACKUP_PAGE = 1000


def read_env(*names: str) -> dict:
    """Read specific keys out of .env, falling back to the real environment.

    This repo is checked out as several git worktrees, and only one of them
    carries a .env. Reading ROOT/.env alone meant `sts schema` and `sts backup`
    simply could not run from the canonical worktree - the answer was "set it in
    .env", which invites planting a copy of the production service key in a tree
    that has no business holding one. So: .env still wins where it exists (it is
    the per-checkout override), and anything it does not define falls back to
    the process environment, which lets a caller export the credential for one
    command without leaving it on disk.
    """
    out = {}
    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k in names:
                out[k] = v.strip().strip('"').strip("'")
    for name in names:
        if not out.get(name) and os.environ.get(name):
            out[name] = os.environ[name]
    return out


def _sb_creds():
    e = read_env("SUPABASE_URL", "SUPABASE_SECRET_KEY", "SUPABASE_SERVICE_KEY")
    url = e.get("SUPABASE_URL")
    key = e.get("SUPABASE_SECRET_KEY") or e.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        sys.exit("sts backup: SUPABASE_URL and SUPABASE_SECRET_KEY (or "
                 "SUPABASE_SERVICE_KEY) must be set in .env")
    return url.rstrip("/"), key


def _sb_get(url: str, key: str, headers: dict = None, timeout: int = 60):
    req = urllib.request.Request(url)
    req.add_header("apikey", key)
    req.add_header("Authorization", f"Bearer {key}")
    for h, v in (headers or {}).items():
        req.add_header(h, v)
    return urllib.request.urlopen(req, timeout=timeout)


def _sb_tables(url: str, key: str) -> list:
    """Discover every table PostgREST exposes, from its OpenAPI document.

    Discovery rather than a hardcoded list: a table added later (a migration
    nobody told this script about) would otherwise be silently left out of
    every backup, which is the failure mode that makes people trust a backup
    that does not contain their data.
    """
    with _sb_get(f"{url}/rest/v1/", key) as r:
        spec = json.loads(r.read().decode("utf-8"))
    names = []
    for path in spec.get("paths", {}):
        if path.startswith("/") and path != "/" and not path.startswith("/rpc/"):
            names.append(path.lstrip("/"))
    return sorted(set(names))


def _sb_exact_count(url: str, key: str, table: str):
    """The server's own row count, for cross-checking the paginated read.

    Verify rather than assume. A paginated dump that quietly stops short - a
    dropped page, a mid-run error swallowed somewhere - produces a file that
    looks exactly like a complete one, and the gap only surfaces during a
    restore, which is the worst possible moment to discover it. PostgREST will
    state the count itself, so ask it.

    Returns None if the server does not answer with a range, in which case the
    dump is recorded as unverified rather than assumed good.
    """
    req = urllib.request.Request(f"{url}/rest/v1/{table}?select=*", method="HEAD")
    req.add_header("apikey", key)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Prefer", "count=exact")
    req.add_header("Range", "0-0")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            rng = r.headers.get("content-range")
    except Exception:  # noqa: BLE001
        return None
    if not rng or "/" not in rng:
        return None
    total = rng.rsplit("/", 1)[1]
    return int(total) if total.isdigit() else None


def _sb_dump_table(url: str, key: str, table: str, dest: Path) -> dict:
    """Page through one table into NDJSON. Returns a manifest entry."""
    expected = _sb_exact_count(url, key, table)
    rows = 0
    h = hashlib.sha256()
    with dest.open("w", encoding="utf-8") as fh:
        offset = 0
        while True:
            q = f"{url}/rest/v1/{table}?select=*&limit={BACKUP_PAGE}&offset={offset}"
            try:
                with _sb_get(q, key) as r:
                    batch = json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                return {"table": table, "rows": 0, "error": f"HTTP {e.code}"}
            if not batch:
                break
            for row in batch:
                line = json.dumps(row, sort_keys=True, ensure_ascii=False)
                fh.write(line + "\n")
                h.update(line.encode("utf-8"))
                rows += 1
            if len(batch) < BACKUP_PAGE:
                break
            offset += BACKUP_PAGE
    entry = {"table": table, "rows": rows, "sha256": h.hexdigest(),
             "file": dest.name, "bytes": dest.stat().st_size,
             "expected": expected}
    # A short dump is a silent data loss, so it is an error, not a note. The
    # run fails and the manifest says which table, because a backup that
    # reports success while missing rows is worse than one that reports
    # nothing: you stop checking it.
    if expected is not None and rows != expected:
        entry["error"] = f"incomplete: wrote {rows} rows, server says {expected}"
    return entry


def _sb_dump_storage(url: str, key: str, bucket: str, out_dir: Path, fetch: bool) -> dict:
    """Record (and optionally download) every object in a storage bucket."""
    body = json.dumps({"prefix": "", "limit": 1000}).encode("utf-8")
    req = urllib.request.Request(f"{url}/storage/v1/object/list/{bucket}", data=body)
    req.add_header("apikey", key)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            listing = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"bucket": bucket, "objects": 0, "error": f"HTTP {e.code}"}
    if not isinstance(listing, list):
        return {"bucket": bucket, "objects": 0, "error": str(listing)}
    entries, downloaded = [], 0
    files_dir = out_dir / "storage" / bucket
    for obj in listing:
        meta = obj.get("metadata") or {}
        e = {"name": obj["name"], "bytes": meta.get("size"),
             "mimetype": meta.get("mimetype")}
        if fetch:
            files_dir.mkdir(parents=True, exist_ok=True)
            try:
                with _sb_get(f"{url}/storage/v1/object/{bucket}/{obj['name']}", key,
                             timeout=300) as r:
                    blob = r.read()
                (files_dir / obj["name"]).write_bytes(blob)
                e["sha256"] = hashlib.sha256(blob).hexdigest()
                downloaded += 1
            except Exception as ex:  # noqa: BLE001
                e["error"] = str(ex)
        entries.append(e)
    return {"bucket": bucket, "objects": len(entries),
            "downloaded": downloaded, "entries": entries}


# ──────────────────────────────────────────────────────────────────────
# og — share cards
# ──────────────────────────────────────────────────────────────────────
#
# A link with no og:image shares as a bare blue line of text. On
# 2026-07-26 seven of the site's eleven real surfaces did exactly that,
# including /checklist and /blog, the two pages most likely to be passed
# around. The two pages that DID set og:image pointed it at the cover
# art, which is 1410x2056 - portrait, into a slot every scraper crops to
# roughly 1.91:1, so the art got sliced through the middle.
#
# Cards are 1200x630 (the OG slot's own aspect) rendered at 2x, which is
# how static/images/og/exclusive-friends-only.png was already built by
# hand. Nothing generated that file, so this exists to stop the next one
# being hand-built too. Copy lives in scripts/og_cards.json next to the
# other registries, and the house style below is read off that card.

OG_DIR = STATIC_DIR / "images" / "og"
OG_W, OG_H, OG_SCALE = 1200, 630, 2


def load_og_cards() -> list:
    reg = json.loads((ROOT / "scripts" / "og_cards.json").read_text(encoding="utf-8"))
    # {version} resolves from book.json, so a card that quotes the draft version
    # cannot go stale against the book it is advertising.
    version = json.loads((BOOK_DIR / "book.json").read_text(encoding="utf-8"))["version"]
    cards = []
    for c in reg["cards"]:
        c = dict(c)
        for k in ("eyebrow", "headline_lead", "headline_accent", "body", "chip"):
            if isinstance(c.get(k), str):
                c[k] = c[k].replace("{version}", version)
        cards.append(c)
    return cards


def og_html(card: dict, cover_uri: str) -> str:
    e = html_mod.escape
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {OG_W}px; height: {OG_H}px; overflow: hidden;
    background: #020617; color: #f1f5f9;
    font-family: 'Outfit', system-ui, sans-serif;
    display: flex; align-items: center;
    position: relative;
  }}
  /* amber edge, the one bit of chrome the friends-only card already had */
  .edge {{ position: absolute; left: 0; top: 0; bottom: 0; width: 7px; background: #f59e0b; }}
  .glow {{
    position: absolute; right: -140px; top: 50%; transform: translateY(-50%);
    width: 720px; height: 720px; border-radius: 50%;
    background: radial-gradient(circle, rgba(245,158,11,0.16) 0%, transparent 62%);
  }}
  .copy {{ position: relative; padding: 0 0 0 76px; width: 720px; }}
  .eyebrow {{
    font-family: 'JetBrains Mono', monospace; font-weight: 700;
    font-size: 19px; letter-spacing: 0.16em; color: #f59e0b;
    margin-bottom: 22px;
  }}
  h1 {{ font-weight: 900; font-size: 62px; line-height: 1.04; letter-spacing: -0.02em; }}
  h1 .accent {{ color: #f59e0b; display: block; }}
  p {{ font-size: 23px; line-height: 1.5; color: #94a3b8; margin-top: 26px; max-width: 620px; }}
  /* bordered chip, then the domain as plain text beside it - the layout the
     hand-built friends-only card established */
  .chiprow {{
    display: flex; align-items: center; gap: 14px; margin-top: 34px;
    font-family: 'JetBrains Mono', monospace; font-size: 16px; letter-spacing: 0.09em;
  }}
  .chip {{
    font-weight: 500; color: #f59e0b;
    border: 1px solid rgba(245,158,11,0.45); border-radius: 6px;
    padding: 9px 15px;
  }}
  .site {{ color: #64748b; }}
  .cover {{ position: relative; margin-left: auto; margin-right: 76px; }}
  .cover img {{
    display: block; width: 268px; height: auto; border-radius: 9px;
    transform: perspective(1400px) rotateY(-9deg) rotate(1.6deg);
    box-shadow: 0 40px 90px rgba(0,0,0,0.72), 0 0 0 1px rgba(245,158,11,0.22);
  }}
</style></head><body>
  <div class="edge"></div><div class="glow"></div>
  <div class="copy">
    <div class="eyebrow">{e(card['eyebrow'])}</div>
    <h1>{e(card['headline_lead'])}<span class="accent">{e(card['headline_accent'])}</span></h1>
    <p>{e(card['body'])}</p>
    <div class="chiprow"><span class="chip">{e(card['chip'])}</span><span class="site">/ survivingthesingularity.com</span></div>
  </div>
  <div class="cover"><img src="{cover_uri}" alt=""></div>
</body></html>"""


def render_og_card(card: dict, chrome: str, cover_uri: str, out_dir: Path) -> dict:
    """Render one card to PNG with headless Chrome. Returns a report row."""
    out = out_dir / card["out"]
    with tempfile.TemporaryDirectory() as td:
        page = Path(td) / "card.html"
        page.write_text(og_html(card, cover_uri), encoding="utf-8")
        shot = Path(td) / "card.png"
        cmd = [chrome, "--headless", "--disable-gpu", "--no-sandbox",
               "--hide-scrollbars", "--default-background-color=00000000",
               f"--force-device-scale-factor={OG_SCALE}",
               f"--window-size={OG_W},{OG_H}",
               "--virtual-time-budget=12000",
               f"--screenshot={shot}", page.as_uri()]
        try:
            subprocess.run(cmd, capture_output=True, timeout=180)
        except Exception as ex:  # noqa: BLE001
            return {"route": card["route"], "out": card["out"], "action": f"render-failed ({ex})"}
        if not shot.exists():
            return {"route": card["route"], "out": card["out"], "action": "render-failed (no output)"}
        out_dir.mkdir(parents=True, exist_ok=True)
        blob = shot.read_bytes()
        same = out.exists() and out.read_bytes() == blob
        out.write_bytes(blob)
    return {"route": card["route"], "out": card["out"],
            "action": "unchanged" if same else "written",
            "bytes": out.stat().st_size}


def _og_image_in(path: Path):
    """The og:image a single .svelte file declares in its head, or None."""
    if not path.exists():
        return None
    head = re.search(r"<svelte:head>(.*?)</svelte:head>",
                     path.read_text(encoding="utf-8"), re.DOTALL)
    if not head:
        return None
    m = re.search(r'property="og:image"\s+content=(?:"([^"]*)"|\{([^}]*)\})',
                  head.group(1))
    if not m:
        return None
    # content={post.image} is a real declaration whose value only exists at
    # runtime; record it as dynamic rather than calling it missing.
    return m.group(1) if m.group(1) is not None else f"{{{m.group(2)}}}"


def og_declared() -> dict:
    """{route: og:image content} for every route that declares one.

    Walks the layout chain, not just +page.svelte. The gated routes (/book,
    /read) have to put their head in a +layout.svelte, because the page
    component only renders once the password gate opens and a crawler never
    gets that far - that is the whole point of the layouts e0ff6a8 added. A
    checker that reads only +page.svelte reports those two as bare links while
    they are in fact correctly tagged, which is a check contradicting the fix
    it is supposed to be verifying.
    """
    found = {}
    for marker in ROUTES_DIR.rglob("+page.svelte"):
        rel = marker.parent.relative_to(ROUTES_DIR)
        route = "/" + "/".join(rel.parts) if rel.parts else "/"
        img = _og_image_in(marker)
        d = marker.parent
        while img is None:
            img = _og_image_in(d / "+layout.svelte")
            if d == ROUTES_DIR:
                break
            d = d.parent
        if img is not None:
            found[route] = img
    return found


def cmd_og(args) -> int:
    cards = load_og_cards()
    if args.render:
        chrome = find_chrome()
        if not chrome:
            sys.exit("sts og: Chrome/Chromium not found - cards are rendered in a real browser "
                     "(web fonts, gradients), so there is no fallback path here.")
        cover = STATIC_DIR / "images" / "surviving_the_singularity_cover_1200.png"
        if not cover.exists():
            sys.exit(f"sts og: cover art missing at {cover} - run `sts.py cover --sync` first")
        only = set(args.only.split(",")) if args.only else None
        rows = [render_og_card(c, chrome, cover.as_uri(), OG_DIR)
                for c in cards if not only or c["route"] in only]
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            print(f"sts og --render — {len(rows)} card(s) at {OG_W}x{OG_H} @{OG_SCALE}x")
            for r in rows:
                size = f"{r['bytes']:,}b" if r.get("bytes") else ""
                print(f"  {r['action']:<12} {r['route']:<18} {r['out']:<20} {size}")
        return 1 if any("failed" in r["action"] for r in rows) else 0

    # check mode: every public page should declare an og:image that exists
    declared = og_declared()
    pages = public_pages(collect_routes()["pages"])
    problems, dynamic, ok = [], [], []
    for p in pages:
        img = declared.get(p)
        if not img:
            problems.append(f"{p} declares no og:image — shares as a bare link")
            continue
        if img.startswith("{"):
            dynamic.append(f"{p} og:image is {img} — resolved at runtime, not checkable here")
            continue
        # {$page.url.origin}/foo.png -> /foo.png
        local = img.split("survivingthesingularity.com", 1)[-1]
        if "}" in local:
            local = local.split("}", 1)[-1]
        if local.startswith("/") and not (STATIC_DIR / local.lstrip("/")).exists():
            problems.append(f"{p} og:image points at {local}, which is not in static/ "
                            "(scrapers will fall back to no image)")
        else:
            ok.append(p)
    if args.json:
        print(json.dumps({"ok": ok, "dynamic": dynamic, "problems": problems,
                          "declared": declared}, indent=2))
        return 1 if problems else 0
    print(f"sts og — {len(pages)} public pages")
    for p in problems:
        print(f"  ERROR  {p}")
    for d in dynamic:
        print(f"  warn   {d}")
    print(f"\n  {len(ok)}/{len(pages)} pages have a static share card that resolves"
          + (f", {len(dynamic)} set one at runtime" if dynamic else ""))
    if problems:
        print("  `sts.py og --render` builds the cards in scripts/og_cards.json.")
    return 1 if problems else 0


# ──────────────────────────────────────────────────────────────────────
# schema — which migrations have actually reached the live database
# ──────────────────────────────────────────────────────────────────────
#
# sql/ is a directory of files. That is not the same thing as a database.
# On 2026-07-26 migrations 008 and 009 had been written, committed, and
# forgotten: the discord endpoint was 500ing against a table that did not
# exist, and every preorder confirmation went out with no discount code
# while the whole pitch was "50% off at launch". Nothing surfaced it,
# because the app catches both failures and carries on.
#
# There is no psql and no supabase CLI on this machine, so this asks
# PostgREST the only question it can answer cheaply: select the thing and
# see whether the schema cache knows about it. A missing table answers
# PGRST205, a missing column answers 42703, and either way the migration
# has not run.

# (migration file, human name, table, column or None for a whole-table check)
SCHEMA_EXPECTATIONS = [
    ("001_waitlist.sql",                 "waitlist",              "waitlist",             None),
    ("002_waitlist_unsubscribe.sql",     "unsubscribe token",     "waitlist",             "unsubscribe_token"),
    ("003_preorders.sql",                "preorders",             "preorders",            None),
    ("004_fulfilled_sessions.sql",       "fulfilment ledger",     "fulfilled_sessions",   None),
    ("005_preorders_copy_lock.sql",      "copy numbering",        "preorders",            "copy_number"),
    ("006_preorders_standard_edition.sql", "standard edition",    "preorders",            "edition_type"),
    ("008_discord_applications.sql",     "discord applications",  "discord_applications", None),
    ("009_preorder_discount_code.sql",   "per-buyer discount code", "preorders",          "discount_code"),
    # 010 ships two columns via two separate ALTER statements. Probe both: the
    # SQL Editor stops at the first error, so a half-applied run can leave one
    # present and the other missing, and probing only one would call that done.
    ("010_waitlist_consent.sql",         "newsletter consent",    "waitlist",             "newsletter_consent"),
    ("010_waitlist_consent.sql",         "book release consent",  "waitlist",             "book_release_consent"),
    ("011_email_deliveries.sql",         "email delivery ledger", "email_deliveries",     None),
    # 013 adds four columns to fulfilled_sessions in one ALTER. Probe the two
    # that carry meaning on their own: `status` is what makes a half-finished
    # fulfilment visible, and `attempts` is what makes a retry loop visible.
    # Without these the durability work is invisible to this checker.
    ("013_checkout_durability.sql",      "fulfilment status",     "fulfilled_sessions",   "status"),
    ("013_checkout_durability.sql",      "fulfilment attempts",   "fulfilled_sessions",   "attempts"),
    ("013_checkout_durability.sql",      "checkout durability",   "checkout_transactions", None),
]

# Migrations that exist in sql/ but deliberately have nothing this checker can
# probe. Listing them here is not a free pass: it is the difference between
# "we looked and there is nothing table-shaped to look at" and the silent
# omission described in _schema_unexpected below.
SCHEMA_UNPROBED_OK: set = {
    # Replaces a trigger FUNCTION (assign_authors_copy_number). No table and no
    # column changes, so table/column presence cannot see it either way.
    # Verifying it means inserting an authors-edition row and reading back the
    # assigned copy_number, which writes to production and is not something a
    # read-only status command should do.
    "007_authors_edition_no_cap.sql",
    # Revokes grants and enables RLS. Again nothing table-shaped: the tables it
    # protects exist both before and after it runs. It is NOT unchecked, it is
    # checked differently - see the lockdown probe below, which is the only
    # thing in this file that verifies the most important security migration in
    # the project.
    "012_lockdown_public_grants.sql",
}

# Tables sql/012 revokes from anon. A lockdown regression here re-exposes
# customer email addresses to the key that ships in every browser.
LOCKDOWN_TABLES = ["waitlist", "preorders", "fulfilled_sessions",
                   "discord_applications", "email_deliveries", "preorder_counts"]


def _anon_probe(url: str, anon_key: str, table: str):
    """Attempt an anon SELECT. Returns (denied: bool, detail: str).

    A 401 alone is ambiguous: a dead key denies everything too, which would make
    a broken key look like a successful lockdown. The caller establishes a
    key-validity control first, so by the time this runs a 401 means the grant
    layer refused a WORKING key.
    """
    req = urllib.request.Request(
        f"{url}/rest/v1/{table}?select=*&limit=1",
        headers={"apikey": anon_key, "Authorization": f"Bearer {anon_key}",
                 "User-Agent": f"sts.py/{VERSION}"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", "replace")[:120]
            return False, f"READABLE by anon (HTTP {resp.status}) {body}"
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        code = ""
        try:
            code = json.loads(body).get("code", "")
        except Exception:
            pass
        if e.code in (401, 403) or code == "42501":
            return True, f"denied (HTTP {e.code}{', ' + code if code else ''})"
        if e.code == 404:
            return True, "not exposed (HTTP 404)"
        return False, f"unexpected HTTP {e.code}: {body[:100]}"
    except Exception as e:
        return False, f"probe failed: {e}"


def _lockdown_report(url: str) -> list:
    """Verify sql/012 behaviourally, with a key-validity control.

    Returns a list of row dicts; an empty list means the anon key was not
    available and nothing could be concluded.
    """
    e = read_env("PUBLIC_SUPABASE_ANON_KEY", "SUPABASE_PUBLISHABLE_KEY")
    anon = e.get("PUBLIC_SUPABASE_ANON_KEY") or e.get("SUPABASE_PUBLISHABLE_KEY")
    if not anon:
        return []

    # CONTROL FIRST. A valid publishable key on /rest/v1/ answers "Secret API
    # key required"; a bogus one answers "Invalid API key". Without this the
    # whole table below is worthless.
    control_ok = False
    try:
        req = urllib.request.Request(
            f"{url}/rest/v1/", headers={"apikey": anon, "User-Agent": f"sts.py/{VERSION}"})
        urllib.request.urlopen(req, timeout=20)
        control_ok = True
    except urllib.error.HTTPError as ce:
        control_ok = "Invalid API key" not in ce.read().decode("utf-8", "replace")
    except Exception:
        control_ok = False

    rows = [{"table": "(key-validity control)", "denied": control_ok,
             "detail": "anon key is live" if control_ok
                       else "ANON KEY IS DEAD - every denial below is meaningless"}]
    if not control_ok:
        return rows
    for t in LOCKDOWN_TABLES:
        denied, detail = _anon_probe(url, anon, t)
        rows.append({"table": t, "denied": denied, "detail": detail})
    return rows


def _schema_unexpected() -> list:
    """Migration files in sql/ that no expectation covers.

    This checker's failure mode is silence: a migration nobody added to
    SCHEMA_EXPECTATIONS is not reported as pending, it is not reported at all,
    and `sts schema` then prints "every migration is live" while the column it
    adds is missing. That is not hypothetical - 010 was written, committed and
    left uncovered, so the checker gave this project a clean bill of health on a
    database that had never seen the consent columns. Compare the directory
    against the table so the next omission is loud.
    """
    sql_dir = ROOT / "sql"
    if not sql_dir.is_dir():
        return []
    covered = {m for m, _, _, _ in SCHEMA_EXPECTATIONS} | SCHEMA_UNPROBED_OK
    return sorted(p.name for p in sql_dir.glob("*.sql") if p.name not in covered)


def _schema_probe(url: str, key: str, table: str, column: str = None):
    """Ask PostgREST whether a table (or column) exists. Returns (ok, detail)."""
    sel = column or "*"
    q = f"{url}/rest/v1/{table}?select={urllib.parse.quote(sel)}&limit=1"
    try:
        with _sb_get(q, key, timeout=20):
            return True, "present"
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            return False, f"HTTP {e.code}"
        code = payload.get("code", "")
        msg = payload.get("message", "")
        if code == "PGRST205":
            return False, "table does not exist"
        if code == "42703":
            return False, "column does not exist"
        return False, f"{code}: {msg}"[:80]
    except Exception as e:  # noqa: BLE001
        return False, str(e)[:80]


def cmd_schema(args) -> int:
    url, key = _sb_creds()
    rows, pending = [], []
    for migration, label, table, column in SCHEMA_EXPECTATIONS:
        target = f"{table}.{column}" if column else table
        ok, detail = _schema_probe(url, key, table, column)
        rows.append({"migration": migration, "label": label,
                     "target": target, "applied": ok, "detail": detail})
        if not ok:
            pending.append(migration)

    unexpected = _schema_unexpected()

    # --bundle: emit exactly the migrations that are still pending, concatenated
    # in filename order, ready to paste into the Supabase SQL Editor in one go.
    # Applying them one file at a time is where this project loses track - the
    # tab gets closed halfway, and `sts schema` is then the only thing that says
    # so. Generated from the live probe rather than kept as a checked-in file, so
    # it cannot drift: an already-applied migration simply stops appearing.
    if getattr(args, "bundle", False):
        uniq = sorted(set(pending))
        if not uniq:
            print("-- Nothing pending: every migration in sql/ is already live.")
            return 0
        print("-- Pending Supabase migrations, generated by `sts schema --bundle`.")
        print(f"-- Project: {url}")
        print("-- Paste the whole thing into the Supabase SQL Editor and Run.")
        print("-- Every file here is idempotent; re-running an applied one is safe.")
        for name in uniq:
            path = ROOT / "sql" / name
            print(f"\n\n-- ═══════════════════════════════════════════════════")
            print(f"-- {name}")
            print(f"-- ═══════════════════════════════════════════════════\n")
            print(path.read_text(encoding="utf-8").rstrip())
        print("\n\n-- Then re-run `python3 scripts/sts.py schema` to confirm.")
        return 0

    if args.json:
        print(json.dumps({"project": url, "rows": rows,
                          "pending": sorted(set(pending)),
                          "uncovered": unexpected}, indent=2))
        return 1 if (pending or unexpected) else 0

    print(f"sts schema — {url}")
    for r in rows:
        mark = "ok     " if r["applied"] else "MISSING"
        print(f"  {mark}  {r['migration']:<38} {r['target']:<28} {r['detail']}")

    # sql/012 is the most important security migration in the project and is not
    # table-shaped, so presence probing cannot see it. Verify it behaviourally.
    lockdown = _lockdown_report(url)
    if lockdown:
        print("\n  sql/012 lockdown (anon must be denied on every table below):")
        for r in lockdown:
            mark = "ok     " if r["denied"] else "EXPOSED"
            print(f"  {mark}  {r['table']:<38} {r['detail']}")
        exposed = [r["table"] for r in lockdown if not r["denied"]]
        if exposed:
            print(f"\n  LOCKDOWN REGRESSION: {', '.join(exposed)}")
            pending.append("012_lockdown_public_grants.sql")
    else:
        print("\n  sql/012 lockdown: NOT CHECKED (no anon key in .env), state UNKNOWN.")

    if unexpected:
        print(f"\n  {len(unexpected)} migration(s) in sql/ are not covered by this check,")
        print("  so their state is UNKNOWN, not clean:")
        for m in unexpected:
            print(f"    sql/{m}")
        print("  Add each to SCHEMA_EXPECTATIONS in scripts/sts.py.")

    if pending:
        uniq = sorted(set(pending))
        print(f"\n  {len(uniq)} migration(s) have not reached the database:")
        for m in uniq:
            print(f"    sql/{m}")
        print("\n  There is no psql or supabase CLI here, so run them by hand:")
        print("  Supabase dashboard > SQL Editor > paste the file > Run.")
        print("  Every one of these files is idempotent; re-running an applied one is safe.")

    if pending or unexpected:
        return 1
    print("\n  Every migration in sql/ is live in the database.")
    return 0


def _sb_schema_snapshot(url: str, key: str) -> dict:
    """Capture the live column layout of every exposed table.

    The backup this replaced was rows only. Rows do not describe the table they
    came from, and sql/ is missing 001, 003, 004, 006 and 007 entirely, so there
    was no path from a blank Supabase project back to a working one - the NDJSON
    would have had nowhere to land. PostgREST publishes an OpenAPI document
    describing every table it exposes, which gives real column names, types,
    formats and required-ness read off the live database rather than guessed
    from the endpoints that write to it.

    Honest about its limits: this captures COLUMNS. It does not capture indexes,
    unique constraints, check constraints, defaults, foreign keys, RLS policies,
    triggers or functions - so it is a reconstruction aid, not a restore script.
    A real `pg_dump --schema-only` (or the dashboard's schema export) is still
    the thing to get, and `restore_gaps` in the manifest says so rather than
    letting the file imply more coverage than it has.
    """
    try:
        with _sb_get(f"{url}/rest/v1/", key, timeout=30) as r:
            spec = json.loads(r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}

    tables = {}
    for name, defn in sorted((spec.get("definitions") or {}).items()):
        required = set(defn.get("required") or [])
        cols = []
        for col, meta in (defn.get("properties") or {}).items():
            cols.append({
                "column": col,
                "type": meta.get("type"),
                "format": meta.get("format"),
                "required": col in required,
                "description": meta.get("description"),
            })
        tables[name] = cols
    return {"captured_from": "PostgREST OpenAPI (/rest/v1/)", "tables": tables}


def cmd_backup(args) -> int:
    url, key = _sb_creds()
    stamp = date.today().isoformat()
    root = (Path(args.out).expanduser() if args.out else BACKUP_DEFAULT_DIR).resolve()

    # These files hold customer email addresses and payment references. A
    # backup that lands inside a git worktree is one `git add -A` away from
    # being published to a public GitHub repo.
    if root == ROOT or ROOT in root.parents:
        sys.exit(f"sts backup: refusing to write customer data inside the "
                 f"git worktree ({root}). Pass --out somewhere else.")

    # Never overwrite yesterday's good backup with today's broken one, and
    # never let a second run of the day silently replace the first. An
    # overwritten backup is an undetectable loss of the history the backup
    # exists to preserve.
    out_dir = root / stamp
    if (out_dir / "manifest.json").exists():
        n = 2
        while (root / f"{stamp}-{n}" / "manifest.json").exists():
            n += 1
        out_dir = root / f"{stamp}-{n}"
    (out_dir / "tables").mkdir(parents=True, exist_ok=True)

    tables = _sb_tables(url, key)
    dumped = [_sb_dump_table(url, key, t, out_dir / "tables" / f"{t}.ndjson")
              for t in tables]
    storage = [_sb_dump_storage(url, key, b, out_dir, not args.no_files)
               for b in BACKUP_STORAGE_BUCKETS]

    schema = _sb_schema_snapshot(url, key)
    (out_dir / "schema.json").write_text(
        json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "taken": stamp,
        "project_url": url,
        "tables": dumped,
        "storage": storage,
        "schema": {"file": "schema.json",
                   "tables": sorted((schema.get("tables") or {}).keys()),
                   "error": schema.get("error")},
        "total_rows": sum(d.get("rows", 0) for d in dumped),
        "restore_gaps": "schema.json lists COLUMNS only. Indexes, unique and check "
                        "constraints, defaults, foreign keys, RLS policies, triggers "
                        "and functions are NOT captured, and sql/ is missing 001, 003, "
                        "004, 006 and 007 - so this is a reconstruction aid, not a "
                        "restore script. Get a real pg_dump --schema-only (or the "
                        "Supabase dashboard schema export) before trusting any of this "
                        "as disaster recovery.",
        "restore": "Each tables/<name>.ndjson is one JSON object per line, exactly "
                   "the shape PostgREST accepts. To restore a table: POST the lines "
                   "(batched) to <project_url>/rest/v1/<name> with the service key and "
                   "Content-Type: application/json. Storage objects under storage/<bucket>/ "
                   "go back via POST <project_url>/storage/v1/object/<bucket>/<name>.",
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    errors = [d for d in dumped if d.get("error")] + \
             [s for s in storage if s.get("error")]
    if args.json:
        print(json.dumps(manifest, indent=2))
        return 1 if errors else 0
    print(f"sts backup — {url}")
    print(f"  -> {out_dir}")
    for d in dumped:
        if d.get("error"):
            print(f"  ERROR  {d['table']:<24} {d['error']}")
        else:
            mark = "verified" if d.get("expected") is not None else "UNVERIFIED"
            print(f"  {d['rows']:>6} rows  {d['table']:<24} {d['sha256'][:12]}  {mark}")
    for s in storage:
        if s.get("error"):
            print(f"  ERROR  bucket {s['bucket']}: {s['error']}")
        else:
            print(f"  {s['objects']:>6} objs  storage/{s['bucket']:<17}"
                  f" {s['downloaded']} downloaded")
    if schema.get("error"):
        print(f"  ERROR  schema.json                {schema['error']}")
    else:
        ncols = sum(len(c) for c in schema["tables"].values())
        print(f"  {ncols:>6} cols  schema.json              "
              f"{len(schema['tables'])} tables (columns only — see restore_gaps)")
    print(f"\n  {manifest['total_rows']} rows across {len(dumped)} tables.")
    if errors:
        print(f"  {len(errors)} target(s) failed — backup is INCOMPLETE.")
        return 1
    print("  Copy this directory somewhere that is not this machine "
          "(a backup with one copy is not a backup).")
    return 0


# ──────────────────────────────────────────────────────────────────────
# stripe
# ──────────────────────────────────────────────────────────────────────

def stripe_state() -> dict:
    envfile = ROOT / ".env"
    key_mode = "absent"
    prices = {}
    if envfile.exists():
        for line in envfile.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("STRIPE_SECRET_KEY="):
                v = line.split("=", 1)[1]
                key_mode = ("live" if v.startswith(("sk_live_", "rk_live_"))
                            else "test" if v.startswith(("sk_test_", "rk_test_"))
                            else "placeholder")
            for var in ("STRIPE_PRICE_ID", "STRIPE_PRICE_ID_STANDARD", "STRIPE_PRICE_ID_AUTHORS"):
                if line.startswith(var + "="):
                    v = line.split("=", 1)[1]
                    prices[var] = v[:14] + "…" if len(v) > 14 else v
    server = (ROOT / "src/routes/api/stripe-checkout/+server.js").read_text(encoding="utf-8")
    mock_branch = "mock_session" in server
    mock_dev_gated = "if (!dev)" in server
    return {"local_key_mode": key_mode, "local_prices_masked": prices,
            "mock_branch_present": mock_branch,
            "mock_gated_to_dev": mock_dev_gated,
            "golive_doc": "STRIPE-GO-LIVE.md" if (ROOT / "STRIPE-GO-LIVE.md").exists() else None}


# ── live drift: what we charge vs what we advertise ───────────────────
#
# Reading .env tells you nothing about production. On 2026-07-26 the live
# site was charging $9 while every page promised $5, and it had been doing so
# for ten days, because the only thing anyone checked was a status line in a
# markdown file. Everything below probes the real site instead.

# Lines that mention the offer are the only place a preorder price can live.
# The manuscript and blog quote plenty of unrelated money ($100K salaries,
# $1.25 widgets), so an unscoped scan for "$N" is pure noise.
OFFER_KEYWORDS = ("preorder", "early access", "full kit", "gets you")
PRICE_RE = re.compile(r"\$([0-9][0-9,]*(?:\.[0-9]{2})?)")

CHROME_PATHS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
)


def money_to_cents(s: str) -> int:
    return int(round(float(s.replace(",", "")) * 100))


def fmt_cents(c: int) -> str:
    return f"${c / 100:,.2f}"


def advertised_prices() -> dict:
    """Every preorder price the site quotes, as {cents: [files]}."""
    found = {}
    for root in (ROOT / "src/routes", ROOT / "src/lib/components"):
        if not root.exists():
            continue
        for f in sorted(root.rglob("*.svelte")):
            rel = f.relative_to(ROOT).as_posix()
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                low = line.lower()
                if not any(k in low for k in OFFER_KEYWORDS):
                    continue
                for m in PRICE_RE.finditer(line):
                    files = found.setdefault(money_to_cents(m.group(1)), [])
                    if rel not in files:
                        files.append(rel)
    return found


def post_json(url: str, payload: dict, timeout: float = 20.0, headers: dict = None):
    """POST JSON. Returns (status, body). Never raises; 0 means no response.

    `headers` is merged over the defaults. The checkout endpoints enforce
    same-origin and fail CLOSED, so a probe that sends no Origin gets a 403 and
    looks exactly like a broken checkout. Callers hitting those routes must pass
    one; see cmd_stripe_live.
    """
    hdrs = {"Content-Type": "application/json", "User-Agent": f"sts.py/{VERSION}"}
    hdrs.update(headers or {})
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST",
        headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


# Address used by the checkout probe. On our own domain and never sold to, so
# it cannot collide with a real customer and cannot be read as one.
STRIPE_PROBE_EMAIL = "sts-probe@survivingthesingularity.com"


# A benign event type the webhook handler does not act on. Deliberate: this
# probe carries a REAL signature, so it must be a payload that cannot fulfil an
# order even when verification succeeds. Never probe with
# checkout.session.completed.
WEBHOOK_PROBE_EVENT = {
    "id": "evt_sts_probe",
    "object": "event",
    "type": "payment_intent.created",
    "data": {"object": {"id": "pi_sts_probe"}},
}


def post_signed_webhook(url: str, secret: str, timeout: float = 20.0):
    """POST a correctly signed Stripe event. Returns (status, body).

    Signs exactly the bytes that are sent, the way Stripe does:
    HMAC-SHA256 over "<timestamp>.<raw body>" keyed by the endpoint secret.
    """
    payload = json.dumps(WEBHOOK_PROBE_EVENT, separators=(",", ":"))
    ts = str(int(time.time()))
    sig = hmac.new(secret.encode("utf-8"),
                   f"{ts}.{payload}".encode("utf-8"),
                   hashlib.sha256).hexdigest()
    req = urllib.request.Request(
        url, data=payload.encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json",
                 "User-Agent": f"sts.py/{VERSION}",
                 "Stripe-Signature": f"t={ts},v1={sig}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


def find_chrome():
    for p in CHROME_PATHS:
        if Path(p).exists():
            return p
    return shutil.which("google-chrome") or shutil.which("chromium")


def charged_cents(session_url: str, chrome: str):
    """Read the amount a Stripe Checkout session will actually charge.

    Stripe's checkout page is client-rendered — the amount is nowhere in the
    HTML that a plain GET returns — so this needs a real browser.
    Returns (cents, error).
    """
    try:
        out = subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom",
             "--virtual-time-budget=15000", session_url],
            capture_output=True, text=True, timeout=120).stdout
    except Exception as e:
        return None, f"render failed: {e}"
    amounts = [money_to_cents(m) for m in re.findall(r"\$([0-9][0-9,]*\.[0-9]{2})", out)]
    if not amounts:
        return None, "no dollar amount in the rendered checkout page"
    # Stripe prints the total in several places (line item, subtotal, total);
    # the most repeated value is the one being charged.
    return max(set(amounts), key=amounts.count), None


def stripe_live_state(check_price: bool = True) -> dict:
    """Probe production: live-vs-test, webhook health, price truthfulness."""
    st = {"site": SITE, "errors": [], "warnings": []}

    # 1. What happens when a real customer clicks buy?
    # Origin is REQUIRED here. /api/stripe-checkout enforces same-origin and
    # fails closed as of 2f28645, so a probe without it gets 403 and this
    # command then reports "ERROR checkout returned 403" against a checkout that
    # works perfectly. That false alarm stood for a full session before anyone
    # traced it back to the probe rather than the app.
    #
    # The body needs an `email` too. Since 332fdfd the address is collected
    # before the session is created, so a body carrying only edition_type is
    # rejected 400 "Enter a valid email address." Use a dedicated probe address
    # on our own domain: it is obviously not a customer, it will never appear in
    # `preorders`, so the duplicate check always takes the new-buyer path and
    # this probe keeps measuring the thing it is meant to measure.
    status, body = post_json(f"{SITE}/api/stripe-checkout",
                             {"edition_type": "standard", "email": STRIPE_PROBE_EMAIL},
                             headers={"Origin": SITE})
    st["checkout_status"] = status
    session_url = ""
    if status == 200:
        try:
            session_url = json.loads(body).get("url") or ""
        except Exception:
            session_url = ""
        st["mode"] = ("live" if "cs_live_" in session_url else
                      "test" if "cs_test_" in session_url else "unknown")
        if st["mode"] == "unknown":
            st["errors"].append("no cs_live_/cs_test_ in the session url — cannot tell "
                                "whether real cards are being charged")
    elif status == 429:
        # Self-inflicted when probing repeatedly; not a production fault.
        st["mode"] = "unknown"
        st["warnings"].append("checkout rate-limited (429); 5 requests per 10 min "
                              "per IP, retry later")
    else:
        st["mode"] = "unknown"
        st["errors"].append(f"checkout returned {status}, expected 200")

    # 2. Does the fulfillment webhook actually WORK?
    #
    #    An unsigned POST answering 400 proves only that STRIPE_WEBHOOK_SECRET is
    #    set. It does NOT prove signature verification runs. This check used to
    #    print "HTTP 400 <- OK: configured" and treat that as health, which is
    #    exactly what a webhook whose verifier cannot run returns, so for weeks
    #    it certified as healthy an endpoint that rejected every event Stripe ever
    #    sent, including correctly signed ones (the synchronous constructEvent /
    #    Workers SubtleCrypto fault, fixed in aea146e). Three audits repeated that
    #    reading. A status code that looks identical whether the thing works or is
    #    completely broken is not evidence.
    #
    #    The only proof is a correctly signed event coming back 200. So: unsigned
    #    POST to tell "configured" from 503, then a signed probe to tell "verifies"
    #    from "rejects everything".
    wh_status, _ = post_json(f"{SITE}/api/webhooks/stripe", {})
    st["webhook_status"] = wh_status
    st["webhook_secret_set"] = wh_status not in (503, 0)
    st["webhook_verified"] = None  # None = could not be proven either way
    st["webhook_signed_status"] = None
    if wh_status == 503:
        st["errors"].append("webhook 503 — STRIPE_WEBHOOK_SECRET unset in prod; a paid "
                            "order is lost whenever the browser never reaches /success")
    elif wh_status != 400:
        st["warnings"].append(f"unsigned webhook POST returned {wh_status}; expected 400 "
                              "(secret set) or 503 (not configured)")

    secret = read_env("STRIPE_WEBHOOK_SECRET").get("STRIPE_WEBHOOK_SECRET", "")
    if wh_status == 503:
        pass  # already an error; a signed probe adds nothing
    elif not secret:
        st["warnings"].append(
            "webhook NOT PROVEN: no STRIPE_WEBHOOK_SECRET available locally, so a "
            "signed event could not be sent. 'HTTP 400' alone cannot distinguish a "
            "working verifier from one that rejects every event. Re-run with the "
            "secret exported, or read the runtime's own log line "
            "(wrangler pages deployment tail <id> --project-name survivingthesingularity)")
    else:
        sg_status, _ = post_signed_webhook(f"{SITE}/api/webhooks/stripe", secret)
        st["webhook_signed_status"] = sg_status
        if sg_status == 200:
            st["webhook_verified"] = True
        elif sg_status == 400:
            st["webhook_verified"] = False
            st["errors"].append(
                "webhook REJECTED a correctly signed event (400). Either the local "
                "secret differs from production's, or verification cannot run at all. "
                "Those are indistinguishable from out here. Settle it from the "
                "runtime log: 'verification could not run' means the handler is "
                "broken for EVERY event and no order is ever fulfilled by webhook; "
                "'signature rejected' means it is only the secret")
        else:
            st["warnings"].append(f"signed webhook probe returned {sg_status}; expected "
                                  "200 (verified) or 400 (rejected)")

    # Keep the old key, but redefine it honestly: ok now means proven, not
    # 'answered with a status code that was easy to misread'.
    st["webhook_ok"] = st["webhook_verified"] is True

    # 3. Does what we charge match what we promise?
    ads = advertised_prices()
    st["advertised_cents"] = sorted(ads)
    st["advertised_in"] = {str(c): ads[c] for c in sorted(ads)}
    if not ads:
        st["warnings"].append("found no advertised preorder price in the site source")
    elif len(ads) > 1:
        st["errors"].append("site advertises conflicting preorder prices: "
                            + ", ".join(fmt_cents(c) for c in sorted(ads)))

    st["charged_cents"] = None
    chrome = find_chrome() if check_price else None
    if check_price:
        if not session_url:
            st["warnings"].append("no checkout session, so the charged price was "
                                  "not verified")
        elif not chrome:
            st["warnings"].append("Chrome/Chromium not found, so the charged price was "
                                  "NOT verified — this is the check that catches "
                                  "advertising one price and billing another")
        else:
            cents, err = charged_cents(session_url, chrome)
            st["charged_cents"] = cents
            if err:
                st["warnings"].append(err)
            elif len(ads) == 1 and cents != sorted(ads)[0]:
                st["errors"].append(
                    f"PRICE MISMATCH: checkout charges {fmt_cents(cents)} but the site "
                    f"advertises {fmt_cents(sorted(ads)[0])} — fix the live price or the "
                    "prod STRIPE_PRICE_ID_STANDARD, not the app code (STRIPE-GO-LIVE.md)")
    return st


def cmd_stripe_live(args) -> int:
    st = stripe_live_state(check_price=not args.no_price)
    if args.json:
        print(json.dumps(st, indent=2))
        return 1 if st["errors"] else 0
    print(f"Stripe live probe of {st['site']}")
    print(f"  checkout:   HTTP {st['checkout_status']} · mode {st['mode']}"
          + ("  <- REAL CARDS" if st["mode"] == "live" else ""))
    if st["webhook_verified"] is True:
        wh_note = "  <- VERIFIED: a signed event was accepted"
    elif st["webhook_verified"] is False:
        wh_note = "  <- BROKEN: a correctly signed event was rejected"
    elif st["webhook_secret_set"]:
        wh_note = "  <- secret set, but verification NOT PROVEN"
    else:
        wh_note = "  <- NOT CONFIGURED"
    signed = st["webhook_signed_status"]
    print(f"  webhook:    HTTP {st['webhook_status']}"
          + (f" · signed HTTP {signed}" if signed is not None else "")
          + wh_note)
    adv = ", ".join(fmt_cents(c) for c in st["advertised_cents"]) or "none found"
    print(f"  advertised: {adv}")
    print(f"  charged:    {fmt_cents(st['charged_cents']) if st['charged_cents'] is not None else 'not verified'}")
    for w in st["warnings"]:
        print(f"  WARN   {w}")
    for e in st["errors"]:
        print(f"  ERROR  {e}")
    if not st["errors"]:
        print("\n  No drift: production charges what the site advertises.")
    return 1 if st["errors"] else 0


def cmd_stripe(args) -> int:
    if getattr(args, "live", False):
        return cmd_stripe_live(args)
    st = stripe_state()
    if args.json:
        print(json.dumps(st, indent=2))
        return 0
    print("Stripe go-live readiness")
    print(f"  local key mode:        {st['local_key_mode']} (local should stay test)")
    for k, v in st["local_prices_masked"].items():
        print(f"  {k}: {v}")
    print(f"  mock branch present:   {st['mock_branch_present']}")
    print(f"  mock gated to dev:     {st['mock_gated_to_dev']}"
          + ("  <- OK: prod fails loudly" if st["mock_gated_to_dev"] else "  <- RISK"))
    print(f"  cutover checklist:     {st['golive_doc']}")
    print("\n  Cutover = set live env vars in the production host (see STRIPE-GO-LIVE.md),")
    print("  then one real purchase per edition.")
    return 0


# ──────────────────────────────────────────────────────────────────────
# live
# ──────────────────────────────────────────────────────────────────────

def probe(url: str, timeout: float = 10.0) -> int:
    req = urllib.request.Request(url, method="GET",
                                 headers={"User-Agent": f"sts.py/{VERSION}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def cmd_live(args) -> int:
    pages = collect_routes()["pages"]
    targets = [p for p in public_pages(pages)]
    drift, ok = [], []
    for p in targets:
        code = probe(SITE + ("" if p == "/" else p))
        (ok if code == 200 else drift).append((p, code))
    stale = []
    for p in sorted(DEAD_ROUTES):
        code = probe(SITE + p)
        if code == 200:
            stale.append((p, code))
    result = {"ok": ok, "missing_live": drift, "stale_live": stale}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"live probe of {SITE}")
        for p, c in drift:
            print(f"  DRIFT  {p} -> {c} (exists locally, not deployed)")
        for p, c in stale:
            print(f"  STALE  {p} -> {c} (dead route still live — old build deployed)")
        print(f"  {len(ok)}/{len(targets)} local routes live"
              + ("" if not (drift or stale) else " — deploy is out of date"))
    return 1 if (drift or stale) else 0


# ──────────────────────────────────────────────────────────────────────
# routes / status
# ──────────────────────────────────────────────────────────────────────

def cmd_routes(args) -> int:
    routes = collect_routes()
    if args.json:
        print(json.dumps(routes, indent=2))
        return 0
    for p in routes["pages"]:
        print(f"  page  {p}")
    for a in routes["apis"]:
        print(f"  api   {a}")
    return 0


def cmd_status(args) -> int:
    branch = git("branch", "--show-current")
    dirty = len([l for l in git("status", "--porcelain").splitlines() if l])
    # Against origin/main, not main. The local `main` ref in this checkout is
    # 61 commits stale and nothing updates it, so `main..HEAD` reported "61
    # ahead" for a branch that was in fact fully pushed and 0/0 with the remote.
    # A number that large reads as "you have a pile of unpushed work" and sent
    # at least one session hunting for commits that were already on the remote.
    # Fall back to the local ref only when there is no remote-tracking one.
    base = "origin/main" if git("rev-parse", "--verify", "-q", "origin/main") else "main"
    ahead = git("rev-list", "--count", f"{base}..HEAD") or "?"
    book = book_stats()
    stripe = stripe_state()
    pages = collect_routes()["pages"]
    sm_errors, sm_missing = check_sitemap(pages)
    status = {
        "git": {"branch": branch, "dirty_paths": dirty,
                "ahead_of_main": ahead, "ahead_of": base},
        "book": {"version": book["version"], "words": book["total_words"],
                 "updated": book["lastUpdated"]},
        "site": {"pages": len(pages), "sitemap_ghosts": len(sm_errors),
                 "sitemap_missing": len(sm_missing)},
        "stripe": {"local_key": stripe["local_key_mode"],
                   "mock_gated_to_dev": stripe["mock_gated_to_dev"]},
    }
    if args.json:
        print(json.dumps(status, indent=2))
        return 0
    print(f"Surviving the Singularity — sts.py v{VERSION}")
    print(f"  git:     {branch} · {dirty} dirty paths · {ahead} ahead of {base}")
    print(f"  book:    v{book['version']} · {book['total_words']:,} words · updated {book['lastUpdated']}")
    print(f"  site:    {len(pages)} pages · sitemap ghosts {len(sm_errors)} · unlisted {len(sm_missing)}")
    print(f"  stripe:  local key {stripe['local_key_mode']} · prod-fail-loud "
          f"{'yes' if stripe['mock_gated_to_dev'] else 'NO'}")
    print("\n  run `sts.py audit` for the full sweep · `sts.py live` to check the deploy")
    return 0


# ──────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────
# compile — concatenate book source into one manuscript draft
# ──────────────────────────────────────────────────────────────────────

def cmd_compile(args) -> int:
    meta = json.loads((BOOK_DIR / "book.json").read_text(encoding="utf-8"))
    tag = args.tag or meta["version"]
    header = (f"# {meta['title'].upper()}\n\n"
              f"## {meta['subtitle']}\n\n"
              f"**Author:** {meta['author']}\n"
              f"**Manuscript:** {tag}\n"
              f"**Compiled:** {date.today().isoformat()} (by sts.py compile, "
              f"book.json section order)\n\n"
              f"## TABLE OF CONTENTS\n\n")
    toc = "\n".join(f"- {s['title']}" for s in meta["sections"])
    chunks = [header + toc + "\n\n---\n"]
    targets = _ref_targets(_live_index())
    for s in meta["sections"]:
        body = (BOOK_DIR / s["file"]).read_text(encoding="utf-8").strip()
        try:
            body = _expand_refs(body, targets, s["file"])
        except KeyError as e:
            sys.exit(f"sts.py compile: {e}\n  a cross-reference points at "
                     f"nothing. Run: sts.py refs list")
        chunks.append(body + "\n\n---\n")
    text = "\n".join(chunks)
    if args.stdout:
        print(text)
        return 0
    out = (Path(args.out) if args.out
           else ROOT / "manuscript" / f"StS-Complete-Draft-compiled-{date.today().isoformat()}.md")
    if out.exists() and not args.force:
        sys.exit(f"sts.py compile: {out} exists (pass --force to overwrite)")
    out.write_text(text, encoding="utf-8")
    words = len(re.findall(r"\b[\w'’-]+\b", text))
    rel = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
    print(f"compiled {len(meta['sections'])} sections -> {rel} ({words:,} words)")
    return 0


# ──────────────────────────────────────────────────────────────────────
# research — web search for sources and historical examples (stdlib only)
# ──────────────────────────────────────────────────────────────────────

RESEARCH_UA = ("sts.py/" + VERSION +
               " (survivingthesingularity.com book research; ctavolazzi@gmail.com)")


def _http_get(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": RESEARCH_UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _strip_tags(fragment: str) -> str:
    return html_mod.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def _wiki_search(query: str, n: int) -> list:
    qs = urllib.parse.urlencode({
        "action": "query", "list": "search", "srsearch": query,
        "srlimit": n, "format": "json", "srprop": "snippet",
    })
    data = json.loads(_http_get("https://en.wikipedia.org/w/api.php?" + qs))
    hits = []
    for it in data.get("query", {}).get("search", []):
        slug = urllib.parse.quote(it["title"].replace(" ", "_"))
        hits.append({"source": "wiki", "title": it["title"],
                     "url": "https://en.wikipedia.org/wiki/" + slug,
                     "snippet": _strip_tags(it.get("snippet", ""))})
    return hits


def _wiki_summary(title: str) -> str:
    slug = urllib.parse.quote(title.replace(" ", "_"))
    try:
        data = json.loads(_http_get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + slug))
        return data.get("extract", "")
    except Exception:
        return ""


BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def _mojeek_search(query: str, n: int) -> list:
    """Mojeek serves parseable HTML without a bot challenge (DDG/Bing do not)."""
    req = urllib.request.Request(
        "https://www.mojeek.com/search?" + urllib.parse.urlencode({"q": query}),
        headers={"User-Agent": BROWSER_UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        page = r.read().decode("utf-8", "replace")
    link_pat = re.compile(
        r'<h2><a class="title"[^>]+href="([^"]+)"[^>]*>(.*?)</a></h2>'
        r'(?:<p class="s">(.*?)</p>)?', re.S)
    hits = []
    for m in link_pat.finditer(page):
        hits.append({"source": "web", "title": _strip_tags(m.group(2)),
                     "url": m.group(1),
                     "snippet": _strip_tags(m.group(3) or "")})
        if len(hits) >= n:
            break
    return hits


def _ddg_search(query: str, n: int) -> list:
    page = _http_get("https://html.duckduckgo.com/html/?" +
                     urllib.parse.urlencode({"q": query}))
    link_pat = re.compile(
        r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.S)
    snip_pat = re.compile(r'class="result__snippet"[^>]*>(.*?)</a>', re.S)
    snippets = [_strip_tags(s) for s in snip_pat.findall(page)]
    hits = []
    for i, m in enumerate(link_pat.finditer(page)):
        href = m.group(1)
        if "uddg=" in href:  # DDG redirect wrapper
            href = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
        if href.startswith("//"):
            href = "https:" + href
        hits.append({"source": "web", "title": _strip_tags(m.group(2)),
                     "url": href,
                     "snippet": snippets[i] if i < len(snippets) else ""})
        if len(hits) >= n:
            break
    return hits


def _web_search(query: str, n: int) -> list:
    """General web search: Mojeek first, DuckDuckGo as fallback.

    Both engines captcha rapid-fire clients. Space calls ~20s apart when
    running batches (see --sleep), and prefer --wiki-only when Wikipedia
    can answer — the Wikipedia API is not rate-limited at this volume.
    """
    for engine in (_mojeek_search, _ddg_search):
        try:
            hits = engine(query, n)
            if hits:
                return hits
        except Exception as e:
            print(f"  {engine.__name__}: failed ({e})", file=sys.stderr)
    return []


def cmd_research(args) -> int:
    query = " ".join(args.query)
    results = []
    if not args.web_only:
        try:
            results += _wiki_search(query, args.n)
        except Exception as e:
            print(f"  wikipedia: search failed ({e})", file=sys.stderr)
    if not args.wiki_only:
        if args.sleep:
            time.sleep(args.sleep)
        results += _web_search(query, args.n)
    if args.summary:
        for r in results:
            if r["source"] == "wiki":
                r["summary"] = _wiki_summary(r["title"])

    if args.json:
        print(json.dumps({"query": query, "results": results}, indent=2))
    else:
        print(f"research: {query} — {len(results)} results\n")
        for r in results:
            print(f"  [{r['source']}] {r['title']}")
            print(f"        {r['url']}")
            if r.get("snippet"):
                print(f"        {r['snippet'][:220]}")
            if r.get("summary"):
                print(f"        | {r['summary'][:400]}")
            print()

    if args.save and results:
        log = ROOT / "manuscript" / "sources" / "research-log.md"
        log.parent.mkdir(parents=True, exist_ok=True)
        new_file = not log.exists()
        with log.open("a", encoding="utf-8") as f:
            if new_file:
                f.write("# Research log — sts.py research --save\n")
            f.write(f"\n## {date.today().isoformat()} — {query}\n\n")
            for r in results:
                f.write(f"- [{r['title']}]({r['url']}) ({r['source']})")
                if r.get("snippet"):
                    f.write(f" — {r['snippet'][:200]}")
                f.write("\n")
        print(f"  saved -> {log.relative_to(ROOT)}")
    return 0 if results else 1


def cmd_scan(args) -> int:
    """Scannability audit over the book source.

    Finds opportunities to make the text scannable at a glance:
      - pull-quote candidates (short, punchy, aphoristic sentences)
      - wall-of-text paragraphs (suggest a split, a list, or bolding)
      - heading deserts (long runs with no subhead)
      - emphasis deserts (long runs with no bold/italic/list/quote texture)
      - list opportunities (enumerations trapped inside prose)
      - per-chapter texture score (formatting events per 1,000 words)
    Report-only: never edits the manuscript.
    """
    book_dir = ROOT / "src" / "lib" / "data" / "book"
    book = json.loads((book_dir / "book.json").read_text())
    top_n = args.top

    aphorism_re = re.compile(
        r"^(The|That|This|You|It|We|Every|Nobody|History|Survival|Power|Panic|Trust)\b")
    enum_re = re.compile(r"\b(First|Second|Third|Fourth)\b[,:]")

    def sentences(text):
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    report = []
    for section in book["sections"]:
        path = book_dir / section["file"]
        raw = path.read_text()
        lines = raw.split("\n")

        # Build paragraph blocks with line anchors, skipping fences/tables/images.
        paras, buf, start, in_fence = [], [], None, False
        for i, ln in enumerate(lines, 1):
            if ln.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            s = ln.strip()
            is_prose = (s and not s.startswith(("#", "|", "!", ">", "-", "*", "1.", "2.",
                                                "3.", "4.", "5.", "  -"))
                        and not re.match(r"^\d+\.\s", s))
            if is_prose:
                if start is None:
                    start = i
                buf.append(s)
            else:
                if buf:
                    paras.append((start, " ".join(buf)))
                buf, start = [], None
        if buf:
            paras.append((start, " ".join(buf)))

        words_total = len(re.findall(r"\S+", raw))
        pulls, walls, list_ops = [], [], []
        for ln_no, para in paras:
            wc = len(para.split())
            if wc > 90:
                walls.append((ln_no, wc, para[:70]))
            if enum_re.search(para) or para.count(";") >= 3:
                list_ops.append((ln_no, para[:70]))
            sents = sentences(para)
            for pos, sent in enumerate(sents):
                sw = len(sent.split())
                if (4 <= sw <= 14 and aphorism_re.match(sent)
                        and sent.endswith(".") and sent.count(",") <= 1
                        and "](" not in sent and "*" not in sent):
                    score = (14 - sw) + (4 if pos == len(sents) - 1 else 0) + \
                            (2 if len(sents) >= 3 else 0)
                    pulls.append((score, ln_no, sent))
        pulls.sort(reverse=True)

        # Texture: formatting events per 1000 words, and deserts.
        events, desert_run, deserts, run_start = 0, 0, [], 1
        heading_gaps, last_heading_wc, wc_seen = [], 0, 0
        for i, ln in enumerate(lines, 1):
            s = ln.strip()
            w = len(s.split())
            wc_seen += w
            if s.startswith("#"):
                if wc_seen - last_heading_wc > 900:
                    heading_gaps.append((i, wc_seen - last_heading_wc))
                last_heading_wc = wc_seen
            if (s.startswith((">", "-", "|")) or re.match(r"^\d+\.", s)
                    or "**" in s or re.search(r"(?<!\*)\*[^*]+\*(?!\*)", s)
                    or s.startswith("#")):
                events += 1
                if desert_run > 500:
                    deserts.append((run_start, desert_run))
                desert_run, run_start = 0, i
            else:
                desert_run += w
        if desert_run > 500:
            deserts.append((run_start, desert_run))
        texture = round(events / max(words_total, 1) * 1000, 1)

        report.append({
            "file": section["file"], "title": section["title"],
            "words": words_total, "texture_per_1k": texture,
            "pull_quote_candidates": [
                {"line": l, "sentence": s, "score": sc} for sc, l, s in pulls[:top_n]],
            "wall_paragraphs": [
                {"line": l, "words": w, "starts": t} for l, w, t in walls[:top_n]],
            "heading_deserts": [
                {"near_line": l, "words_since_heading": w} for l, w in heading_gaps],
            "emphasis_deserts": [
                {"from_line": l, "plain_words": w} for l, w in deserts[:top_n]],
            "list_opportunities": [
                {"line": l, "starts": t} for l, t in list_ops[:top_n]],
        })

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"sts scan — scannability audit · {len(report)} sections "
          f"(top {top_n} findings per category per file)\n")
    for r in sorted(report, key=lambda x: x["texture_per_1k"]):
        flags = (len(r["pull_quote_candidates"]) + len(r["wall_paragraphs"])
                 + len(r["heading_deserts"]) + len(r["emphasis_deserts"])
                 + len(r["list_opportunities"]))
        if not flags and not args.all:
            continue
        print(f"■ {r['file']} — {r['title']}")
        print(f"  {r['words']:,} words · texture {r['texture_per_1k']}/1k")
        for p in r["pull_quote_candidates"]:
            print(f"    PULL  L{p['line']:>4}  \"{p['sentence']}\"")
        for w in r["wall_paragraphs"]:
            print(f"    WALL  L{w['line']:>4}  {w['words']} words: {w['starts']}…")
        for h in r["heading_deserts"]:
            print(f"    HEAD  L{h['near_line']:>4}  {h['words_since_heading']} words since last heading")
        for d in r["emphasis_deserts"]:
            print(f"    FLAT  L{d['from_line']:>4}  {d['plain_words']} words with zero texture")
        for lo in r["list_opportunities"]:
            print(f"    LIST  L{lo['line']:>4}  {lo['starts']}…")
        print()
    lowest = sorted(report, key=lambda x: x["texture_per_1k"])[:5]
    print("Lowest-texture sections (most in need of scannability work):")
    for r in lowest:
        print(f"  {r['texture_per_1k']:>6}/1k  {r['file']} — {r['title']}")
    return 0


# ──────────────────────────────────────────────────────────────────────
# id — manuscript addressing: a stable unique id for every block
# ──────────────────────────────────────────────────────────────────────
#
# Non-invasive by design. The .md source stays clean (no anchors leak into
# the book, the EPUB, or the PDF). The address book lives beside the source in
# src/lib/data/book/manuscript-index.json and maps
#     sts.<section_id>.b<NNNN>  ->  (file, line span, type, content hash)
# Building the index does NOT modify any .md or book.json, so it is not a
# content change and does not trigger the versioning ritual.
#
# IDs are carried forward across rebuilds (a programmatic edit keeps a block's
# identity; inserts mint fresh ids; deletes are tombstoned for audit). Figure
# blocks cross-link to art-catalog.json ids, unifying prose + art under one
# addressable namespace so coursework can join on either.

INDEX_NAME = "manuscript-index.json"
INDEX_SCHEMA = "sts-manuscript-index/v1"

_WORD_RE = re.compile(r"\b[\w'’-]+\b")
_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
_LIST_RE = re.compile(r"^([-*+]\s+|\d+[.)]\s+)")
_HR_RE = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
_ID_RE = re.compile(r"^sts\.[a-z0-9-]+\.b\d{4}$")


def _norm_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _block_hash(btype: str, level: int, text: str) -> str:
    key = f"{btype}:{level}:{_norm_text(text)}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def _classify(first: str, nlines: int):
    """(type, level) for a raw block, from its first line and line count."""
    if first.startswith("#"):
        return "heading", len(first) - len(first.lstrip("#"))
    if first.startswith("!["):
        return "figure", 0
    if first.startswith(("```", "~~~")):
        return "code", 0
    if first.startswith("|"):
        return "table", 0
    if first.startswith(">"):
        return "blockquote", 0
    if _LIST_RE.match(first):
        return "list", 0
    if nlines == 1 and _HR_RE.match(first):
        return "hr", 0
    return "paragraph", 0


def _md_blocks(lines):
    """Split markdown source into typed blocks with 1-indexed inclusive spans.

    Guarantee: every non-blank line belongs to exactly one block; blocks are
    ordered and non-overlapping; the only uncovered lines are blank (or blank
    lines held inside a fenced code block, which are covered by that block).
    """
    blocks, N, i = [], len(lines), 0
    while i < N:
        if lines[i].strip() == "":
            i += 1
            continue
        start = i
        first = lines[i].lstrip()
        if first.startswith("#") or first.startswith("!["):
            end = i                                   # headings / images: one line
        elif first.startswith(("```", "~~~")):
            fence = first[:3]
            j = i + 1
            while j < N and not lines[j].lstrip().startswith(fence):
                j += 1
            end = j if j < N else N - 1               # include the closing fence
        else:
            j = i
            while j < N and lines[j].strip() != "":
                j += 1
            end = j - 1                               # blank-line delimited run
        raw = lines[start:end + 1]
        btype, level = _classify(raw[0].lstrip(), len(raw))
        blocks.append({"type": btype, "level": level,
                       "lines": [start + 1, end + 1], "text": "\n".join(raw)})
        i = end + 1
    # A single-italic paragraph right after a figure is that figure's caption.
    for k in range(1, len(blocks)):
        if blocks[k]["type"] == "paragraph" and blocks[k - 1]["type"] == "figure":
            t = blocks[k]["text"].strip()
            if t.startswith("*") and t.endswith("*") and not t.startswith("**"):
                blocks[k]["type"] = "caption"
    return blocks


def _art_figure_map(book_dir):
    """{source image path -> art-catalog id} for every catalogued figure."""
    p = book_dir / "art-catalog.json"
    if not p.exists():
        return {}
    cat = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    for a in cat.get("assets", []):
        fig = a.get("figure")
        if fig:
            out[fig[len("static"):] if fig.startswith("static/") else fig] = a["id"]
    return out


def _reconcile(old_blocks, new_blocks):
    """Carry stable ids from old_blocks onto new_blocks (mutates new_blocks).

    Pass 1 matches on exact content (unchanged blocks, reorders keep their id).
    Pass 2 pairs residual same-type blocks positionally (an in-place edit keeps
    its id). Unmatched new blocks are left id-less for the caller to mint.

    Returns (tombstones, stats). Pass 1 is provable: the content is identical,
    so the id is certainly the same block's. Pass 2 is a *guess* — correct for
    an in-place edit, wrong when a delete and an insert of the same type land
    in one edit, which slides every id after the delete onto its neighbour.
    stats["positional"] is that guess count, so a caller can surface it.
    """
    from collections import defaultdict, deque
    exact = defaultdict(deque)
    for ob in old_blocks:
        exact[(ob["type"], ob.get("level", 0), ob["hash"])].append(ob)
    used = set()
    n_exact = n_positional = 0
    for nb in new_blocks:
        dq = exact.get((nb["type"], nb["level"], nb["hash"]))
        if dq:
            ob = dq.popleft()
            nb["id"] = ob["id"]
            used.add(ob["id"])
            n_exact += 1
    by_type = defaultdict(deque)
    for ob in old_blocks:
        if ob["id"] not in used:
            by_type[ob["type"]].append(ob)
    for nb in new_blocks:
        if nb.get("id"):
            continue
        dq = by_type.get(nb["type"])
        if dq:
            ob = dq.popleft()
            nb["id"] = ob["id"]
            used.add(ob["id"])
            n_positional += 1
    tombstones = [ob["id"] for ob in old_blocks if ob["id"] not in used]
    return tombstones, {"exact": n_exact, "positional": n_positional}


def _build_index(book_dir, old_index=None):
    """Parse every section into addressed blocks, reconciling ids with old_index."""
    book = json.loads((book_dir / "book.json").read_text(encoding="utf-8"))
    figmap = _art_figure_map(book_dir)
    old_secs = {s["id"]: s for s in (old_index or {}).get("sections", [])}
    sections_out, total_blocks, total_words = [], 0, 0
    recon = {"exact": 0, "positional": 0, "by_section": []}
    for s in book["sections"]:
        sid = s["id"]
        lines = (book_dir / s["file"]).read_text(encoding="utf-8").split("\n")
        blocks = _md_blocks(lines)
        for b in blocks:
            b["hash"] = _block_hash(b["type"], b["level"], b["text"])
        old = old_secs.get(sid, {})
        tombstones, rstats = _reconcile(old.get("blocks", []), blocks)
        recon["exact"] += rstats["exact"]
        recon["positional"] += rstats["positional"]
        if rstats["positional"]:
            recon["by_section"].append({"section": sid,
                                        "positional": rstats["positional"]})
        next_ord = old.get("next_ordinal", 1)
        for b in blocks:
            if not b.get("id"):
                b["id"] = f"sts.{sid}.b{next_ord:04d}"
                next_ord += 1
        recs = []
        for b in blocks:
            rec = {"id": b["id"], "type": b["type"], "lines": b["lines"],
                   "words": len(_WORD_RE.findall(b["text"])), "hash": b["hash"],
                   "preview": _norm_text(b["text"])[:90]}
            if b["type"] == "heading":
                rec["level"] = b["level"]
            if b["type"] == "figure":
                m = _IMG_RE.search(b["text"])
                rec["image"] = m.group(1) if m else None
                rec["art_id"] = figmap.get(rec["image"])
            recs.append(rec)
        sec_words = sum(r["words"] for r in recs)
        total_blocks += len(recs)
        total_words += sec_words
        sections_out.append({
            "id": sid, "title": s["title"], "file": s["file"],
            "next_ordinal": next_ord, "words": sec_words,
            "tombstones": sorted(set(old.get("tombstones", [])) | set(tombstones)),
            "blocks": recs})
    return {"schema": INDEX_SCHEMA, "book_version": book["version"],
            "generated": None,
            "id_scheme": "sts.<section_id>.b<NNNN>  (b = block, 4-digit monotonic ordinal)",
            "totals": {"sections": len(sections_out),
                       "blocks": total_blocks, "words": total_words},
            # How this build reconciled ids against old_index. Describes the
            # *transition*, not the state, so it is never persisted: rebuilding
            # from the written index would report 0 positional and rewrite the
            # file every time. _write_index strips it.
            "_reconcile": recon,
            "sections": sections_out}


def _index_path(book_dir):
    return book_dir / INDEX_NAME


def _load_index(book_dir):
    p = _index_path(book_dir)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _strip_gen(ix):
    return {k: v for k, v in ix.items() if k not in ("generated", "_reconcile")}


def _write_index(book_dir, index, force=False):
    """Write the index. No-op (returns False) when nothing but the date changed."""
    old = _load_index(book_dir)
    if old and not force and _strip_gen(old) == _strip_gen(index):
        return False
    index = dict(index)
    index.pop("_reconcile", None)          # transition stat, not persisted state
    index["generated"] = date.today().isoformat()
    _index_path(book_dir).write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def _live_index():
    """A freshly-parsed index of the current source, ids continued from disk.

    Reads always parse live source so line spans are never stale; the persisted
    index only supplies id continuity.
    """
    return _build_index(BOOK_DIR, _load_index(BOOK_DIR))


def _find_block(index, bid):
    for sec in index["sections"]:
        for blk in sec["blocks"]:
            if blk["id"] == bid:
                return blk, sec
    return None, None


def _splice(path, span, new_text):
    """Replace 1-indexed inclusive line span in a file, preserving final newline."""
    raw = path.read_text(encoding="utf-8")
    final_nl = raw.endswith("\n")
    lines = raw.split("\n")
    if final_nl:
        lines = lines[:-1]
    a, b = span
    lines[a - 1:b] = new_text.rstrip("\n").split("\n") if new_text != "" else []
    path.write_text("\n".join(lines) + ("\n" if final_nl else ""), encoding="utf-8")


def _id_build(args):
    index = _build_index(BOOK_DIR, _load_index(BOOK_DIR))
    changed = _write_index(BOOK_DIR, index, force=args.force)
    t = index["totals"]
    tomb = sum(len(s["tombstones"]) for s in index["sections"])
    rc = index["_reconcile"]
    if args.json:
        print(json.dumps({"changed": changed, "totals": t, "tombstones": tomb,
                          "reconcile": rc}, indent=2))
    else:
        print(f"manuscript-index: {t['blocks']} blocks · {t['sections']} sections · "
              f"{t['words']:,} words" + ("" if changed else " (unchanged)"))
        print(f"  ids carried: {rc['exact']} by content match · "
              f"{rc['positional']} positionally")
        if tomb:
            print(f"  {tomb} tombstoned id(s) retained for audit")
        if rc["positional"]:
            print(f"\n  WARNING  {rc['positional']} id(s) were carried by POSITION, "
                  "not by content.")
            print("           Pass 2 pairs leftover same-type blocks in order. That is "
                  "right for an\n"
                  "           in-place edit and WRONG when a delete and an insert land "
                  "in one edit,\n"
                  "           which slides ids onto neighbouring blocks. Only the "
                  "content matches\n"
                  "           above are provable. Review before trusting these ids:")
            for row in rc["by_section"]:
                print(f"             {row['section']:<16} {row['positional']:>4}")
    return 0


def _id_list(args):
    index = _live_index()
    rows = []
    for sec in index["sections"]:
        if args.section and sec["id"] != args.section:
            continue
        for blk in sec["blocks"]:
            if args.type and blk["type"] != args.type:
                continue
            rows.append((sec["file"], blk))
    if args.json:
        print(json.dumps([{"section_file": f, **b} for f, b in rows],
                         indent=2, ensure_ascii=False))
        return 0
    print(f"manuscript blocks — {len(rows)} shown\n")
    for _, b in rows:
        a, z = b["lines"]
        tag = b["type"][:4].upper()
        art = f"  [{b['art_id']}]" if b.get("art_id") else ""
        print(f"  {b['id']:<26} {tag:<5} L{a}-{z:<5} {b['words']:>4}w  "
              f"{b['preview'][:60]}{art}")
    return 0


def _id_get(args):
    index = _live_index()
    blk, sec = _find_block(index, args.id)
    if not blk:
        sys.exit(f"sts.py id get: no block {args.id}")
    lines = (BOOK_DIR / sec["file"]).read_text(encoding="utf-8").split("\n")
    a, b = blk["lines"]
    text = "\n".join(lines[a - 1:b])
    if args.json:
        print(json.dumps({**blk, "section": sec["id"], "file": sec["file"],
                          "text": text}, indent=2, ensure_ascii=False))
    else:
        print(text)
    return 0


def _id_replace(args):
    if args.file:
        new = Path(args.file).read_text(encoding="utf-8")
    elif args.stdin:
        new = sys.stdin.read()
    elif args.text is not None:
        new = args.text
    else:
        sys.exit("sts.py id replace: provide --text, --file, or --stdin")
    new = new.rstrip("\n")
    index = _live_index()
    blk, sec = _find_block(index, args.id)
    if not blk:
        sys.exit(f"sts.py id replace: no block {args.id}")
    path = BOOK_DIR / sec["file"]
    a, b = blk["lines"]
    if args.dry_run:
        print(f"[dry-run] {args.id}: {sec['file']} L{a}-{b} "
              f"({blk['words']}w) <- {len(new.splitlines())} new line(s)")
        return 0
    _splice(path, (a, b), new)
    rebuilt = _build_index(BOOK_DIR, _load_index(BOOK_DIR))
    _write_index(BOOK_DIR, rebuilt, force=True)
    after, _ = _find_block(rebuilt, args.id)
    aw = after["words"] if after else "gone"
    print(f"replaced {args.id} in {sec['file']} (L{a}-{b}, {blk['words']}w -> {aw}w); "
          f"index rebuilt")
    return 0


def _verify_index(book_dir, index):
    """Return a list of (check, ok, detail). Pure; used by verify and stress."""
    checks = []
    all_ids = [b["id"] for s in index["sections"] for b in s["blocks"]]
    checks.append(("id.count", len(all_ids) > 0, f"{len(all_ids)} blocks"))
    dups = len(all_ids) - len(set(all_ids))
    checks.append(("id.unique", dups == 0, f"{dups} duplicate id(s)"))
    bad_scheme = [i for i in all_ids if not _ID_RE.match(i)]
    checks.append(("id.scheme", not bad_scheme, str(bad_scheme[:3])))
    span_bad, hash_bad, cover_bad = [], [], []
    for s in index["sections"]:
        lines = (book_dir / s["file"]).read_text(encoding="utf-8").split("\n")
        nonblank = {i for i, ln in enumerate(lines, 1) if ln.strip()}
        covered = []
        for b in s["blocks"]:
            a, z = b["lines"]
            if not (1 <= a <= z <= len(lines)):
                span_bad.append(b["id"])
                continue
            covered += list(range(a, z + 1))
            text = "\n".join(lines[a - 1:z])
            lvl = b.get("level", 0)
            if _block_hash(b["type"], lvl, text) != b["hash"]:
                hash_bad.append(b["id"])
        cset = set(covered)
        if len(covered) != len(cset):
            cover_bad.append(s["file"] + ":overlap")
        if nonblank - cset:
            cover_bad.append(s["file"] + ":unaddressed")
        if any(lines[i - 1].strip() for i in (cset - nonblank)):
            cover_bad.append(s["file"] + ":nonblank-gap")
    checks.append(("span.valid", not span_bad, str(span_bad[:3])))
    checks.append(("hash.match", not hash_bad, str(hash_bad[:3])))
    checks.append(("coverage.exact", not cover_bad, str(cover_bad[:3])))
    # art cross-links resolve
    cat_ids = set()
    catp = book_dir / "art-catalog.json"
    if catp.exists():
        cat_ids = {a["id"] for a in
                   json.loads(catp.read_text(encoding="utf-8")).get("assets", [])}
    art_bad = [b["id"] for s in index["sections"] for b in s["blocks"]
               if b.get("art_id") and b["art_id"] not in cat_ids]
    linked = sum(1 for s in index["sections"] for b in s["blocks"] if b.get("art_id"))
    checks.append(("art.links", not art_bad, f"{linked} linked, bad {art_bad[:3]}"))
    return checks


def _id_verify(args):
    index = _live_index()
    checks = _verify_index(BOOK_DIR, index)
    failed = [c for c in checks if not c[1]]
    if args.json:
        print(json.dumps({"ok": not failed,
                          "checks": [{"check": c, "ok": ok, "detail": d}
                                     for c, ok, d in checks]}, indent=2))
    else:
        for c, ok, d in checks:
            print(f"  {'PASS' if ok else 'FAIL'}  {c:<16} {d}")
        t = index["totals"]
        print(f"\n{'OK' if not failed else 'FAILED'}: "
              f"{t['blocks']} blocks, {t['sections']} sections, {t['words']:,} words")
    return 1 if failed else 0


def _ids_of(index):
    return [b["id"] for s in index["sections"] for b in s["blocks"]]


def _id_stress(args):
    """Stress-test programmatic editing on a throwaway copy of the book source.

    Real files are never touched. Exercises: coverage/uniqueness, get-integrity,
    edit-in-place id stability, insert (fresh id), delete (tombstone), and a
    revert that must reproduce the baseline ids exactly.
    """
    results = []

    def check(name, ok, detail=""):
        results.append({"check": name, "ok": bool(ok), "detail": detail})

    tmp = Path(tempfile.mkdtemp(prefix="sts-idstress-"))
    try:
        for f in BOOK_DIR.glob("*.md"):
            shutil.copy2(f, tmp / f.name)
        for extra in ("book.json", "art-catalog.json"):
            if (BOOK_DIR / extra).exists():
                shutil.copy2(BOOK_DIR / extra, tmp / extra)

        import time as _time
        t0 = _time.time()
        base = _build_index(tmp, None)
        build_ms = round((_time.time() - t0) * 1000, 1)
        base_ids = _ids_of(base)

        for c, ok, d in _verify_index(tmp, base):
            check("build." + c, ok, d)
        check("perf.build_under_2s", build_ms < 2000, f"{build_ms} ms")

        # get-by-id integrity across every block
        gi = 0
        for s in base["sections"]:
            lines = (tmp / s["file"]).read_text(encoding="utf-8").split("\n")
            for b in s["blocks"]:
                a, z = b["lines"]
                if "\n".join(lines[a - 1:z]) and \
                   _block_hash(b["type"], b.get("level", 0),
                               "\n".join(lines[a - 1:z])) == b["hash"]:
                    gi += 1
        check("get.integrity_all", gi == len(base_ids), f"{gi}/{len(base_ids)}")

        def first_of(index, sid, btype):
            sec = next(s for s in index["sections"] if s["id"] == sid)
            blk = next(b for b in sec["blocks"] if b["type"] == btype)
            return blk, sec

        prev = base

        # 1. EDIT a paragraph in place -> same id, other ids untouched, no tombstone
        blk, sec = first_of(prev, "chapter9", "paragraph")
        orig = "\n".join((tmp / sec["file"]).read_text().split("\n")[
            blk["lines"][0] - 1:blk["lines"][1]])
        _splice(tmp / sec["file"], tuple(blk["lines"]), orig + " Stress-edit sentinel.")
        cur = _build_index(tmp, prev)
        eblk, _ = _find_block(cur, blk["id"])
        check("edit.id_stable", eblk is not None, blk["id"])
        check("edit.word_grew", eblk and eblk["words"] > blk["words"],
              f"{blk['words']}->{eblk['words'] if eblk else '?'}")
        check("edit.others_unchanged",
              set(_ids_of(cur)) == set(base_ids), "id set preserved")
        check("edit.no_tombstone",
              sum(len(s["tombstones"]) for s in cur["sections"]) == 0)
        prev = cur

        # 2. INSERT a new paragraph -> fresh id minted, all prior ids survive
        blk, sec = first_of(prev, "chapter17", "paragraph")
        body = "\n".join((tmp / sec["file"]).read_text().split("\n")[
            blk["lines"][0] - 1:blk["lines"][1]])
        _splice(tmp / sec["file"], tuple(blk["lines"]),
                body + "\n\nInserted stress paragraph for id-minting.")
        before_ids = set(_ids_of(prev))
        cur = _build_index(tmp, prev)
        now_ids = set(_ids_of(cur))
        check("insert.count_plus1", len(now_ids) == len(before_ids) + 1,
              f"{len(before_ids)}->{len(now_ids)}")
        check("insert.priors_survive", before_ids <= now_ids)
        check("insert.fresh_id", len(now_ids - before_ids) == 1,
              str(sorted(now_ids - before_ids)))
        prev = cur

        # 3. DELETE a paragraph -> its id tombstoned, others untouched
        blk, sec = first_of(prev, "introduction", "paragraph")
        before_ids = set(_ids_of(prev))
        _splice(tmp / sec["file"], tuple(blk["lines"]), "")
        cur = _build_index(tmp, prev)
        now_ids = set(_ids_of(cur))
        tombs = {t for s in cur["sections"] for t in s["tombstones"]}
        check("delete.count_minus1", len(now_ids) == len(before_ids) - 1,
              f"{len(before_ids)}->{len(now_ids)}")
        check("delete.id_tombstoned", blk["id"] in tombs, blk["id"])
        check("delete.others_untouched", now_ids == before_ids - {blk["id"]})
        prev = cur

        # 4. REVERT to pristine source -> a fresh build reproduces baseline ids
        for f in BOOK_DIR.glob("*.md"):
            shutil.copy2(f, tmp / f.name)
        rebuilt = _build_index(tmp, None)
        check("revert.ids_reproduce", _ids_of(rebuilt) == base_ids,
              "deterministic minting")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    passed = sum(1 for r in results if r["ok"])
    failed = [r for r in results if not r["ok"]]
    if args.json:
        print(json.dumps({"ok": not failed, "passed": passed,
                          "total": len(results), "results": results}, indent=2))
    else:
        print(f"sts id stress — programmatic-editing stress test "
              f"({passed}/{len(results)} checks)\n")
        for r in results:
            print(f"  {'PASS' if r['ok'] else 'FAIL'}  {r['check']:<26} {r['detail']}")
        print(f"\n{'ALL PASS' if not failed else str(len(failed)) + ' FAILED'}")
    return 1 if failed else 0


def cmd_id(args):
    return {"build": _id_build, "list": _id_list, "get": _id_get,
            "replace": _id_replace, "verify": _id_verify,
            "stress": _id_stress}[args.action](args)


# ──────────────────────────────────────────────────────────────────────
# refs — internal cross-references that cannot rot
# ──────────────────────────────────────────────────────────────────────
#
# The problem: every internal cross-reference in the book is plain prose --
# "the thermodynamic limits we discussed in Chapter 1", "as detailed in
# Chapter 5". Reorder or renumber a chapter and every one of those sentences
# becomes quietly wrong. Nothing in the build notices, because to a renderer
# they are just words.
#
# The fix is to write the POINTER instead of the number, and generate the
# number at render time:
#
#     [](sts:chapter1)          -> "Chapter 1"        (label generated)
#     [](sts:sts.chapter1.b0003)-> "Chapter 1"        (block-precise pointer)
#     [the limits](sts:chapter1)-> "the limits"       (author's words, checked)
#
# An empty label is generated from book.json, so renumbering a chapter rewrites
# every sentence that points at it. A non-empty label is the author's phrasing
# and is left alone -- but the pointer is still resolved, so deleting the target
# fails the build instead of leaving a sentence that references nothing.
#
# WHY EXPANSION, NOT HYPERLINKS. Three different consumers read the raw .md:
# `sts.py compile`, scripts/build-epub.sh (pandoc, straight off BOOK_DIR), and
# the website (src/lib/bookContent.js, via Vite ?raw). There is no single href
# that is correct in all three -- the site needs /book/<section>, print needs an
# internal anchor, and anchors in the source are exactly what the id subsystem
# exists to avoid. So a ref expands to TEXT, identically everywhere. The edge
# table below is per-target-agnostic, so emitting real hrefs later is a change
# of one function, not a redesign.

# [label](sts:target) -- target is a section id or a full sts.<sec>.b<NNNN> id.
_SREF_RE = re.compile(r"\[([^\]\n]*)\]\(sts:([A-Za-z0-9._-]+)\)")


def _section_label(title: str) -> str:
    """'Chapter 1: The Event Horizon' -> 'Chapter 1'.

    book.json titles are '<short name>: <descriptive tail>'. The short name is
    what prose actually says ("as we saw in Chapter 1"), so that is what a
    generated label expands to. Titles with no colon are used whole.
    """
    return title.split(":", 1)[0].strip() if ":" in title else title.strip()


def _ref_targets(index):
    """{ref target -> {...}} for every addressable thing a ref may point at.

    Two granularities, both legal:
      * section id   ('chapter1')          -- stable across editing, use for prose
      * block id     ('sts.chapter1.b0003')-- precise, but blocks churn
    """
    out = {}
    for sec in index["sections"]:
        out[sec["id"]] = {"kind": "section", "section": sec["id"],
                          "title": sec["title"], "file": sec["file"],
                          "label": _section_label(sec["title"])}
        for blk in sec["blocks"]:
            out[blk["id"]] = {"kind": "block", "section": sec["id"],
                              "title": sec["title"], "file": sec["file"],
                              "label": _section_label(sec["title"]),
                              "block": blk["id"], "lines": blk["lines"]}
    return out


def _ref_edges(index):
    """Every sts: reference in the manuscript, as (source -> target) edges.

    This is the shared substrate: `refs --to` reads it backwards to answer
    "what breaks if I cut this", and the expanders read it forwards to render.
    """
    targets = _ref_targets(index)
    edges = []
    for sec in index["sections"]:
        # line -> owning block id, so an edge knows which block it lives in.
        owner = {}
        for blk in sec["blocks"]:
            a, z = blk["lines"]
            for ln in range(a, z + 1):
                owner[ln] = blk["id"]
        text = (BOOK_DIR / sec["file"]).read_text(encoding="utf-8")
        for lineno, line in enumerate(text.split("\n"), 1):
            for m in _SREF_RE.finditer(line):
                label, target = m.group(1), m.group(2)
                edges.append({
                    "from_section": sec["id"], "from_block": owner.get(lineno),
                    "file": sec["file"], "line": lineno,
                    "label": label, "to": target,
                    "resolved": target in targets,
                    "to_section": targets.get(target, {}).get("section"),
                    "generated": not label.strip(),
                    "raw": m.group(0)})
    return edges


def _expand_refs(text: str, targets: dict, where: str = "") -> str:
    """Replace every sts: ref in `text` with its rendered form. Raises on a
    dangling target -- a broken cross-reference must stop a build, not ship."""
    def sub(m):
        label, target = m.group(1), m.group(2)
        t = targets.get(target)
        if t is None:
            raise KeyError(f"{where}: unresolvable reference sts:{target} "
                           f"in {m.group(0)!r}")
        return label if label.strip() else t["label"]
    return _SREF_RE.sub(sub, text)


def verify_refs() -> list:
    """Dangling sts: cross-references. Empty list means every pointer lands."""
    index = _live_index()
    return [{"kind": "dangling reference",
             "file": e["file"], "line": e["line"],
             "detail": f"sts:{e['to']} matches no section or block  ({e['raw']})"}
            for e in _ref_edges(index) if not e["resolved"]]


def _refs_render(args):
    """Emit one section file with refs expanded (the hook build-epub.sh uses)."""
    index = _live_index()
    targets = _ref_targets(index)
    src = Path(args.file)
    if not src.exists():
        src = BOOK_DIR / args.file
    if not src.exists():
        sys.exit(f"sts.py refs render: no such file {args.file}")
    try:
        out = _expand_refs(src.read_text(encoding="utf-8"), targets, src.name)
    except KeyError as e:
        sys.exit(f"sts.py refs render: {e}")
    sys.stdout.write(out)
    return 0


def _refs_list(args):
    index = _live_index()
    edges = _ref_edges(index)
    if args.to:
        edges = [e for e in edges if e["to"] == args.to
                 or e["to_section"] == args.to]
    if args.json:
        print(json.dumps(edges, indent=2, ensure_ascii=False))
        return 0
    if not edges:
        scope = f" pointing at {args.to}" if args.to else ""
        print(f"no sts: cross-references{scope}")
        return 0
    print(f"cross-references — {len(edges)} shown\n")
    for e in edges:
        mark = "  " if e["resolved"] else "!!"
        shown = e["label"] if e["label"].strip() else "(generated)"
        print(f"  {mark} {e['file']}:{e['line']:<5} -> sts:{e['to']:<28} {shown}")
    bad = [e for e in edges if not e["resolved"]]
    if bad:
        print(f"\n  {len(bad)} dangling (marked !!)")
    return 1 if bad else 0


def _refs_stress(args):
    """Prove the ref machinery on a throwaway copy. Real files are never touched.

    Nothing in the manuscript uses sts: refs yet, so without this the resolver
    would ship untested against real content. Mirrors `id stress`.
    """
    global BOOK_DIR
    results = []

    def check(name, ok, detail=""):
        results.append({"check": name, "ok": bool(ok), "detail": detail})

    real, tmp = BOOK_DIR, Path(tempfile.mkdtemp(prefix="sts-refstress-"))
    try:
        for f in real.glob("*.md"):
            shutil.copy2(f, tmp / f.name)
        for extra in ("book.json", "art-catalog.json"):
            if (real / extra).exists():
                shutil.copy2(real / extra, tmp / extra)
        BOOK_DIR = tmp

        book = json.loads((tmp / "book.json").read_text(encoding="utf-8"))
        sec = book["sections"][0]
        victim = tmp / sec["file"]
        index = _build_index(tmp, None)
        # A block belonging to chapter1, so the block-pointer assertion below
        # actually distinguishes "resolved to its section" from "resolved at all".
        a_block = next(s for s in index["sections"]
                       if s["id"] == "chapter1")["blocks"][0]["id"]

        # A generated label, an author-worded label, a block-precise pointer.
        victim.write_text(victim.read_text(encoding="utf-8") +
                          "\n\nSee [](sts:chapter1), and [the limits](sts:chapter1), "
                          f"and [](sts:{a_block}).\n", encoding="utf-8")

        edges = _ref_edges(_build_index(tmp, None))
        check("scan.finds_all", len(edges) == 3, f"{len(edges)} edge(s)")
        check("scan.all_resolve", all(e["resolved"] for e in edges),
              str([e["to"] for e in edges if not e["resolved"]]))
        check("scan.generated_flagged",
              sum(1 for e in edges if e["generated"]) == 2,
              f"{sum(1 for e in edges if e['generated'])} generated")
        check("scan.block_attributed", all(e["from_block"] for e in edges),
              "every edge knows its owning block")

        targets = _ref_targets(_build_index(tmp, None))
        out = _expand_refs(victim.read_text(encoding="utf-8"), targets, "test")
        ch1 = _section_label(
            next(s["title"] for s in book["sections"] if s["id"] == "chapter1"))
        check("expand.generated_label", f"See {ch1}," in out, f"-> {ch1!r}")
        check("expand.keeps_author_words", "the limits" in out,
              "non-empty label preserved")
        one = _expand_refs(f"[](sts:{a_block})", targets, "test")
        check("expand.block_ref_to_section", one == ch1,
              f"sts:{a_block} -> {one!r} (want {ch1!r})")
        check("expand.no_marker_survives", "](sts:" not in out,
              "no sts: leaks into rendered output")

        # A dangling pointer must stop a build, not ship.
        victim.write_text(victim.read_text(encoding="utf-8") +
                          "\n\nBroken [](sts:chapter99).\n", encoding="utf-8")
        check("dangle.verify_catches",
              len([e for e in _ref_edges(_build_index(tmp, None))
                   if not e["resolved"]]) == 1, "1 dangling found")
        raised = False
        try:
            _expand_refs(victim.read_text(encoding="utf-8"),
                         _ref_targets(_build_index(tmp, None)), "test")
        except KeyError:
            raised = True
        check("dangle.expand_raises", raised, "render refuses to emit a dead ref")

        # Renumbering the target rewrites the prose that points at it.
        bj = json.loads((tmp / "book.json").read_text(encoding="utf-8"))
        for s in bj["sections"]:
            if s["id"] == "chapter1":
                s["title"] = "Chapter 4: The Event Horizon"
        (tmp / "book.json").write_text(json.dumps(bj, indent=2), encoding="utf-8")
        moved = _expand_refs("See [](sts:chapter1).",
                             _ref_targets(_build_index(tmp, None)), "test")
        check("renumber.label_follows", moved == "See Chapter 4.", moved)
    finally:
        BOOK_DIR = real
        shutil.rmtree(tmp, ignore_errors=True)

    passed = sum(1 for r in results if r["ok"])
    failed = [r for r in results if not r["ok"]]
    if args.json:
        print(json.dumps({"ok": not failed, "passed": passed,
                          "total": len(results), "results": results}, indent=2))
    else:
        print(f"sts refs stress — cross-reference resolver "
              f"({passed}/{len(results)} checks)\n")
        for r in results:
            print(f"  {'PASS' if r['ok'] else 'FAIL'}  {r['check']:<28} {r['detail']}")
        print(f"\n{'ALL PASS' if not failed else str(len(failed)) + ' FAILED'}")
    return 1 if failed else 0


def cmd_refs(args):
    return {"list": _refs_list, "render": _refs_render,
            "stress": _refs_stress}[args.action](args)


# ──────────────────────────────────────────────────────────────────────
# art — enroll every book figure in the art catalog (data-driven)
# ──────────────────────────────────────────────────────────────────────
#
# Reads the manuscript index (figure blocks + placement), the .md source (alt +
# caption), and static/book-images/credits.json (photo attribution), and emits a
# catalog entry for every figure not yet in art-catalog.json. Ids are a pure
# function of the file: sts.<kind>.<filename-stem> (kind: photo | diagram |
# banner), so new art auto-enrolls. Concepts are suggested from a controlled
# vocabulary so figures stay queryable by topic. Building the catalog does not
# touch book prose, so it is not a content change (no version bump).

_FIG_ALT_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")

# concept -> lowercase trigger substrings, matched against alt+caption+heading.
CONCEPT_VOCAB = {
    "humanoid-robot": ["atlas", "asimo", "sophia", "humanoid", "spot", "quadruped"],
    "robotics": ["robot", "robots", "robotic", "farmbot", "gantry", "quadruped"],
    "automation": ["automation", "automated", "automatic", "autonomous",
                   "cnc autonomous", "self-tending"],
    "generative-ai": ["ai-generated", "generated by", "edmond", "belamy",
                      "generative adversarial"],
    "model-collapse": ["model collapse", "synthetic slop", "training lineage",
                       "generation 0", "degrading", "degrades", "degenerate spike"],
    "cosmology": ["black hole", "galaxies", "hubble", "deep field",
                  "event horizon telescope", "messier", "m87"],
    "event-horizon": ["event horizon", "no going back", "past a certain line"],
    "spaceflight": ["falcon heavy", "rocket", "kennedy space", "space station",
                    "iss", "from orbit", "sunrise from"],
    "solar-energy": ["sun", "solar", "sdo", "photovoltaic", "rooftop", "5-watt"],
    "thermodynamics": ["thermodynamic", "entropy", "waste heat", "survival cycle",
                       "energy captured", "out-work entropy"],
    "regeneration": ["madrone", "bark", "from the root", "regeneration",
                     "regenerative", "comes back"],
    "soil-health": ["soil", "npk", "microbial", "fungi", "bacteria", "nematode",
                    "protozoa", "food web", "living soil", "substrate"],
    "composting": ["compost", "aerated", "molasses", "kelp", "bioreactor",
                   "dissolved oxygen", " act "],
    "food-independence": ["calorie", "greenhouse", "grow light", "garden", "csa",
                          "farmbot", "raised bed", "harvest", "caloric"],
    "farmbot": ["farmbot", "cnc autonomous bed", "seeds, waters"],
    "closed-loop": ["closed loop", "closed-loop", "cycle", "in return", "feeds the",
                    "back to the", "loop back"],
    "3d-printing": ["3d printer", "3d-print", "reprap", "petg"],
    "cnc": ["cnc", "plasma", "gantry", "router"],
    "fabrication": ["fab lab", "fabricate", "machine core", "tool library",
                    "workbench", "hand tools", "welder"],
    "welding": ["weld", "c-channel", "hss", "header beam", "steel wall", "6 mm weld"],
    "dc-microgrid": ["12v", "24v", "dc-native", "dc water", "fuse block",
                     "fuse panel", "inverter", "conversion loss", "native 12v"],
    "off-grid-energy": ["off-grid", "18650", "battery", "microgrid", "decouple",
                        "no meter", "no bill"],
    "thermal-management": ["cooling", "coolant", "radiator", "water block",
                           "thermal exchange", "split-loop", "waste heat"],
    "thermal-envelope": ["spray foam", "r-21", "insulated", "insulation",
                         "thermal barrier", "vapor-sealed", "closed-cell",
                         "condensation"],
    "shouse": ["shouse", "shop half", "half factory", "one envelope", "shed house"],
    "container-construction": ["container", "shell", "pier", "double-wide",
                               "one-trip", "640 square"],
    "wet-room": ["wet-room", "wet room", "shower", "greywater", "linear drain",
                 "sloped basin"],
    "mesh-networking": ["mesh", "topology", "star topology", "meshtastic", "node"],
    "lora": ["lora", "915", "868 mhz", "esp32"],
    "off-grid-comms": ["sneakernet", "microsd", "courier", "encrypts", "encrypted",
                       "antenna", "no license"],
    "resilience": ["single point of failure", "routing problem", "route around",
                   "buffer", "damage becomes", "redundancy", "redundant"],
    "attention-economy": ["attention", "infinite scroll", "notification",
                          "engagement", "suggestibility", "reactive"],
    "cognitive-autonomy": ["cognitive", "prefrontal", "focus", "deep-focus",
                           "agency", "sovereign", "batch"],
    "digital-leverage": ["algorithm", "viral", "wide reach", "media package",
                         "code and media", "scale while you sleep"],
    "media-strategy": ["algorithmic judo", "trojan", "wrapper", "payload",
                       "narrative hook", "outrage"],
    "supply-chain": ["supply chain", "supply line", "port disruption", "logistic",
                     "just-in-time", "freight", "shelves stripped"],
    "deglobalization": ["deglobal", "neighborhood factory", "hyper-local"],
    "market-collapse": ["stock exchange", "nyse", "trading floor", "dead mall",
                        "abandoned", "shockwave", "systemic panic", "gradually, then"],
    "land-strategy": ["land trust", "clt", "ground lease", "real estate", "title",
                      "perpetuity", "foreclose"],
    "legal-strategy": ["legal shield", "firewall", "civil penalty", "statute",
                       "redirection matrix", "municipal"],
    "commons": ["the commons", "commons loop", "autonomous commons", "community",
                "shared", "steward", "cooperative", "co-op", "trust mesh"],
    "food-security": ["food bank", "municipal kitchen", "surplus", "redirect",
                      "edibility", "calorie deliver"],
    "systems-thinking": ["pipeline", "architecture", "engine", "matrix", "feedback",
                         " bus", "sense-decide-actuate", "flow"],
    "strategy": ["chess", "battle lines", "opening position", "compass", "premortem",
                 "roadmap", "the map"],
    "pixel-art": ["pixel art", "pixel-art"],
}


def _load_credits():
    p = STATIC_DIR / "book-images" / "credits.json"
    if not p.exists():
        return {}
    return {c["file"]: c for c in json.loads(p.read_text(encoding="utf-8"))}


def _clean_caption(cap: str) -> str:
    t = cap.strip()
    if t.startswith("*") and t.endswith("*"):
        t = t[1:-1].strip()
    # Strip a trailing credit parenthetical, tolerating one level of nesting
    # (e.g. "(Photo by (c)2007 Jina Lee, CC BY-SA 3.0, via Wikimedia Commons)").
    m = re.search(r"\s*\((?:[^()]|\([^()]*\))*"
                  r"(?:CC |CC0|Public domain|via Wikimedia)"
                  r"(?:[^()]|\([^()]*\))*\)\s*$", t)
    if m:
        t = t[:m.start()].strip()
    return t


_TRIGGER_CACHE = {}


def _derive_concepts(*texts) -> list:
    """Word-boundary match of the concept vocabulary against the given text.

    Word boundaries (not raw substrings) avoid false hits like 'title' inside
    'entitled', 'gan' inside 'gantry', or 'iss' inside 'dissolved'.
    """
    if not _TRIGGER_CACHE:
        for concept, trigs in CONCEPT_VOCAB.items():
            _TRIGGER_CACHE[concept] = [
                re.compile(r"\b" + re.escape(t.strip()) + r"\b") for t in trigs]
    hay = " ".join(t.lower() for t in texts if t)
    return sorted({c for c, pats in _TRIGGER_CACHE.items()
                   if any(p.search(hay) for p in pats)})


def _figure_records(book_dir, index):
    """Every figure block enriched with alt, cleaned caption, nearest heading."""
    out = []
    for sec in index["sections"]:
        lines = (book_dir / sec["file"]).read_text(encoding="utf-8").split("\n")
        blocks, heading = sec["blocks"], None
        for i, b in enumerate(blocks):
            if b["type"] == "heading":
                a, z = b["lines"]
                heading = "\n".join(lines[a - 1:z]).lstrip("# ").strip()
            if b["type"] != "figure":
                continue
            a, z = b["lines"]
            m = _FIG_ALT_RE.search("\n".join(lines[a - 1:z]))
            alt = m.group(1) if m else ""
            img = m.group(2) if m else b.get("image")
            cap = ""
            if i + 1 < len(blocks) and blocks[i + 1]["type"] == "caption":
                ca, cz = blocks[i + 1]["lines"]
                cap = _clean_caption("\n".join(lines[ca - 1:cz]))
            out.append({"block_id": b["id"], "art_id": b.get("art_id"),
                        "section": sec["id"], "file": sec["file"], "image": img,
                        "alt": alt, "caption": cap, "heading": heading})
    return out


def _figure_kind(image: str):
    stem = Path(image).name.rsplit(".", 1)[0]
    ext = Path(image).suffix.lower()
    if re.match(r"part\d-divider$", stem):
        return "banner", "banner-pixel", stem
    if ext == ".svg":
        return "diagram", "diagram-svg", stem
    return "photo", "photo", stem


def _propose_asset(rec, credits):
    kind, typ, stem = _figure_kind(rec["image"])
    label = rec["alt"].split(":")[0].strip() if ":" in rec["alt"] else rec["alt"]
    asset = {
        "id": f"sts.{kind}.{stem}",
        "type": typ,
        "label": label[:80],
        "concepts": _derive_concepts(rec["alt"], rec["caption"], rec["heading"]),
        "figure": "static" + rec["image"] if rec["image"].startswith("/")
                  else rec["image"],
        "placement": {"chapter": rec["section"], "file": rec["file"],
                      "section": rec["heading"]},
        "alt": rec["alt"],
        "caption": rec["caption"],
    }
    if kind == "photo":
        c = credits.get(Path(rec["image"]).name)
        if c:
            asset["credit"] = {"artist": c.get("artist"),
                               "license": c.get("license"),
                               "source": c.get("page")}
    return asset


def _id_art_records():
    index = _build_index(BOOK_DIR, _load_index(BOOK_DIR))
    return index, _figure_records(BOOK_DIR, index)


def _art_list(args):
    _, figs = _id_art_records()
    done = [f for f in figs if f["art_id"]]
    todo = [f for f in figs if not f["art_id"]]
    if args.json:
        print(json.dumps(figs, indent=2, ensure_ascii=False))
        return 0
    print(f"figures — {len(figs)} total · {len(done)} catalogued · "
          f"{len(todo)} not yet\n")
    for f in figs:
        mark = f["art_id"] or "—"
        print(f"  {'[x]' if f['art_id'] else '[ ]'} {Path(f['image']).name:<28} "
              f"{f['section']:<13} {mark}")
    return 0


def _art_sync(args):
    _, figs = _id_art_records()
    credits = _load_credits()
    todo = [f for f in figs if not f["art_id"]]
    proposed = [_propose_asset(f, credits) for f in todo]
    no_concepts = [a["id"] for a in proposed if not a["concepts"]]

    if not args.apply:
        if args.json:
            print(json.dumps(proposed, indent=2, ensure_ascii=False))
        else:
            print(f"art sync (dry-run) — {len(proposed)} figures to enroll\n")
            for a in proposed:
                print(f"  {a['id']:<34} {a['type']:<12} "
                      f"[{', '.join(a['concepts']) or 'NO CONCEPTS'}]")
            kinds = {}
            for a in proposed:
                kinds[a["type"]] = kinds.get(a["type"], 0) + 1
            print(f"\n  by kind: " + ", ".join(f"{k} {v}" for k, v in kinds.items()))
            if no_concepts:
                print(f"  {len(no_concepts)} with no concepts: {no_concepts}")
            print("\n  pass --apply to merge into art-catalog.json")
        return 0

    catp = BOOK_DIR / "art-catalog.json"
    cat = json.loads(catp.read_text(encoding="utf-8"))
    existing = {a["id"] for a in cat["assets"]}
    added = [a for a in proposed if a["id"] not in existing]
    cat["assets"].extend(added)
    cat["generated"] = date.today().isoformat()
    catp.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    # rebuild the manuscript index so every figure now carries its art_id
    idx = _build_index(BOOK_DIR, _load_index(BOOK_DIR))
    _write_index(BOOK_DIR, idx, force=True)
    linked = sum(1 for s in idx["sections"] for b in s["blocks"]
                 if b["type"] == "figure" and b.get("art_id"))
    total = sum(1 for s in idx["sections"] for b in s["blocks"]
                if b["type"] == "figure")
    print(f"art sync: added {len(added)} assets ({len(cat['assets'])} total); "
          f"manuscript index rebuilt, {linked}/{total} figures linked")
    if no_concepts:
        print(f"  {len(no_concepts)} entries need manual concepts: {no_concepts}")
    return 0


# --- art cut: lossless background removal for plate composites ---------------

ART_RAW_DIR = ROOT / "art-raw"

# A plate is a sprite composited by script onto one flat palette colour (the same
# navy as FLOW_BG below), so its background is exactly one RGB value with no
# anti-aliasing. That makes exact colour keying correct AND lossless: verified on
# char-gary-plate.png, the keyed figure is a 2.000x nearest-neighbour match to the
# authored sprite alpha, IoU 100.00%, 0 differing pixels of 105,728.
#
# An ML matting model (rembg, withoutbg, BiRefNet) can only approximate this, and
# approximation is what feathers edges. Measured on sts-char-gary.png, withoutbg
# turned a perfectly binary authored alpha (0.00% intermediate) into 5.26%
# intermediate, erasing 1.66% of the silhouette. Do not use matting on the art.


def _art_dominant_colour(px):
    """Most common RGB triple, and the share of the image it covers."""
    colour, n = collections.Counter(px).most_common(1)[0]
    return colour, n / len(px)


def _art_largest_component(fg, w, h):
    """8-connected BFS. Returns a mask of the biggest blob and the blob count."""
    seen = bytearray(w * h)
    best = []
    blobs = 0
    for start in range(w * h):
        if not fg[start] or seen[start]:
            continue
        blobs += 1
        comp = []
        q = collections.deque([start])
        seen[start] = 1
        while q:
            i = q.popleft()
            comp.append(i)
            y, x = divmod(i, w)
            for dy in (-1, 0, 1):
                ny = y + dy
                if ny < 0 or ny >= h:
                    continue
                base = ny * w
                for dx in (-1, 0, 1):
                    nx = x + dx
                    if (dx or dy) and 0 <= nx < w:
                        j = base + nx
                        if fg[j] and not seen[j]:
                            seen[j] = 1
                            q.append(j)
        if len(comp) > len(best):
            best = comp
    mask = bytearray(w * h)
    for i in best:
        mask[i] = 1
    return mask, blobs


def _art_key_plate(Image, path: Path, tol: int = 0):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    # getdata() is deprecated for removal in Pillow 14; get_flattened_data() is
    # its replacement and does not exist before Pillow 11.3, so try both.
    reader = getattr(im, "get_flattened_data", None) or im.getdata
    px = list(reader())
    bg, share = _art_dominant_colour(px)

    if tol == 0:
        fg = bytearray(0 if p == bg else 1 for p in px)
    else:
        br, bgc, bb = bg
        fg = bytearray(
            0 if abs(p[0] - br) + abs(p[1] - bgc) + abs(p[2] - bb) <= tol else 1
            for p in px)

    fig, blobs = _art_largest_component(fg, w, h)

    def build(mask):
        out = Image.new("RGBA", (w, h))
        # zero the RGB where transparent, so no navy fringe survives premultiply
        out.putdata([(px[i][0], px[i][1], px[i][2], 255) if mask[i]
                     else (0, 0, 0, 0) for i in range(w * h)])
        hist = out.getchannel("A").histogram()
        mid = 1 - (hist[0] + hist[255]) / sum(hist)
        if mid:
            raise AssertionError(
                f"{path.name}: alpha not binary ({mid * 100:.3f}% intermediate)")
        return out

    return {"bg": bg, "bg_share": share, "blobs": blobs,
            "content": build(fg), "figure": build(fig),
            "kept_content": sum(fg) / len(fg), "kept_figure": sum(fig) / len(fig)}


def _art_cut(args) -> int:
    """Key plate composites to transparency without touching the hard edges."""
    try:
        from PIL import Image
    except ModuleNotFoundError:
        print("art cut needs Pillow (the only non-stdlib dep in this script): "
              "pip install Pillow", file=sys.stderr)
        return 1

    plates = [Path(p) for p in args.plates] if args.plates else \
        sorted(ART_RAW_DIR.glob("*-plate.png"))
    if not plates:
        print(f"no plates found in {ART_RAW_DIR}", file=sys.stderr)
        return 1

    out_dir = Path(args.out).expanduser() if args.out else ART_RAW_DIR / "cut"
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    rows, wrote = [], []
    for p in plates:
        r = _art_key_plate(Image, p, tol=args.tol)
        stem = p.stem.replace("-plate", "")
        # largest-blob is only right for single-subject plates; ch06-pegboard has
        # 97 components and drops the loose tools, so flag it instead of lying.
        multi = r["kept_figure"] < r["kept_content"] * 0.8
        for variant in (("content", "figure") if args.variant == "both"
                        else (args.variant,)):
            if not args.dry_run:
                dest = out_dir / f"{stem}-{variant}.png"
                r[variant].save(dest)
                wrote.append(dest)
        rows.append({"plate": p.name, "bg": "#%02x%02x%02x" % r["bg"],
                     "bg_share": round(r["bg_share"], 4), "blobs": r["blobs"],
                     "kept_content": round(r["kept_content"], 4),
                     "kept_figure": round(r["kept_figure"], 4),
                     "multi_subject": multi})

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print(f"{'plate':32} {'bg':9} {'bg%':>6} {'blobs':>6} "
          f"{'content%':>9} {'figure%':>8}")
    for r in rows:
        flag = "  ← multi-subject: use -content" if r["multi_subject"] else ""
        print(f"{r['plate']:32} {r['bg']:9} {r['bg_share']*100:5.1f}% "
              f"{r['blobs']:6d} {r['kept_content']*100:8.2f}% "
              f"{r['kept_figure']*100:7.2f}%{flag}")
    tail = "(dry run, nothing written)" if args.dry_run else \
        f"-> {out_dir} ({len(wrote)} file(s))"
    print(f"\n{len(rows)} plate(s), all alpha verified binary {tail}")
    return 0


def cmd_art(args):
    return {"list": _art_list, "sync": _art_sync, "cut": _art_cut}[args.action](args)


# --- cover: keep the website's cover art in sync with the book's -------------

COVER_SOURCE = ART_RAW_DIR / "book-cover-final-source.png"

# Every cover asset the website can serve, and the width it is published at.
# width None means "native source width". The `_original` webp variants are
# the higher-fidelity encodes the homepage <picture> prefers; the plain ones
# are the compressed siblings. Both families are listed because leaving a
# stale sibling behind is exactly how the site ended up advertising a cover
# the book no longer had.
COVER_TARGETS = (
    ("static/Surviving-the-Singularity-Cover.png", None, None),
    ("static/images/Surviving-the-Singularity-Cover.png", None, None),
    ("static/images/Surviving-the-Singularity-Cover.webp", None, 82),
    ("static/images/surviving_the_singularity_cover_1200.png", None, None),
    ("static/images/optimized/surviving_the_singularity_cover_400.png", 400, None),
    ("static/images/optimized/surviving_the_singularity_cover_800.png", 800, None),
    ("static/images/optimized/surviving_the_singularity_cover_1200.png", 1200, None),
    ("static/images/optimized/surviving_the_singularity_cover_400.webp", 400, 82),
    ("static/images/optimized/surviving_the_singularity_cover_800.webp", 800, 82),
    ("static/images/optimized/surviving_the_singularity_cover_1200.webp", 1200, 82),
    ("static/images/optimized/surviving_the_singularity_cover_400_original.webp", 400, 92),
    ("static/images/optimized/surviving_the_singularity_cover_800_original.webp", 800, 92),
    ("static/images/optimized/surviving_the_singularity_cover_1200_original.webp", None, 92),
    ("static/images/optimized/surviving_the_singularity_cover_original.webp", None, 92),
    ("src/lib/images/Surviving-the-Singularity-Cover.png", None, None),
    ("src/lib/images/Surviving-the-Singularity-Cover.webp", None, 82),
)

# Written next to the source so a later run can tell "this derivative came
# from the current cover" from "this derivative predates it" without
# re-deriving every encode. Content hash of COVER_SOURCE.
COVER_STAMP = STATIC_DIR / "images" / "optimized" / ".cover-source-sha256"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _img_size(path: Path):
    """(width, height) via sips, or None if unreadable."""
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
                         capture_output=True, text=True)
    nums = re.findall(r"pixel(?:Width|Height):\s*(\d+)", out.stdout)
    return (int(nums[0]), int(nums[1])) if len(nums) == 2 else None


def _cover_render(src: Path, dest: Path, width, quality) -> str:
    """Render one derivative. Returns '' on success, else an error string."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix.lower() == ".webp":
        cmd = ["cwebp", "-quiet", "-q", str(quality or 82)]
        if width:
            cmd += ["-resize", str(width), "0"]
        cmd += [str(src), "-o", str(dest)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return "" if dest.exists() and r.returncode == 0 else (r.stderr or "cwebp failed").strip()

    # PNG. The cover art is painterly, so a straight re-encode lands around
    # 3-4 MB — heavy for a fallback <img> and far too heavy for the og:image
    # social scrapers fetch. An adaptive 256-colour octree palette cuts that
    # ~3.7x with no visible banding, because the art is cel-shaded (flat
    # regions, hard edges) rather than a photograph. Pillow is the same
    # optional dependency `art cut` uses; without it, fall back to sips and
    # accept the larger file rather than failing the sync.
    try:
        from PIL import Image
    except ImportError:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / dest.name
            shutil.copyfile(src, tmp)
            if width:
                r = subprocess.run(["sips", "--resampleWidth", str(width), str(tmp)],
                                   capture_output=True, text=True)
                if r.returncode != 0:
                    return (r.stderr or "sips failed").strip()
            shutil.move(str(tmp), str(dest))
        return ""

    try:
        im = Image.open(src).convert("RGB")
        if width and width != im.width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.quantize(colors=256, method=Image.Quantize.FASTOCTREE,
                    dither=Image.Dither.FLOYDSTEINBERG).save(dest, optimize=True)
    except Exception as e:  # noqa: BLE001 - report, don't crash the whole sync
        return f"{type(e).__name__}: {e}"
    return ""


def cmd_cover(args) -> int:
    if not COVER_SOURCE.exists():
        sys.exit(f"sts cover: source art missing — {COVER_SOURCE.relative_to(ROOT)}")
    src_hash = _sha256(COVER_SOURCE)
    src_size = _img_size(COVER_SOURCE)
    stamped = COVER_STAMP.read_text(encoding="utf-8").strip() if COVER_STAMP.exists() else ""
    in_sync = stamped == src_hash

    results = []
    for rel, width, quality in COVER_TARGETS:
        dest = ROOT / rel
        want_w = width or (src_size[0] if src_size else None)
        if not dest.exists():
            state = "missing"
        elif not in_sync:
            state = "stale"
        else:
            got = _img_size(dest)
            state = "ok" if got and want_w and got[0] == want_w else "stale"
        row = {"file": rel, "width": want_w, "state": state}
        if args.sync:
            err = _cover_render(COVER_SOURCE, dest, width, quality)
            row["state"] = "failed" if err else ("wrote" if state != "ok" else "rewrote")
            row["error"] = err or None
            row["bytes"] = dest.stat().st_size if dest.exists() else 0
        results.append(row)

    if args.sync and not any(r["state"] == "failed" for r in results):
        COVER_STAMP.parent.mkdir(parents=True, exist_ok=True)
        COVER_STAMP.write_text(src_hash + "\n", encoding="utf-8")

    drifted = [r for r in results if r["state"] in ("stale", "missing", "failed")]
    if args.json:
        print(json.dumps({
            "source": str(COVER_SOURCE.relative_to(ROOT)),
            "source_sha256": src_hash,
            "source_size": src_size,
            "synced": bool(args.sync),
            "in_sync": in_sync,
            "results": results,
        }, indent=2))
        return 1 if drifted and not args.sync else 0

    dims = f"{src_size[0]}x{src_size[1]}" if src_size else "?"
    print(f"sts cover — source {COVER_SOURCE.relative_to(ROOT)} ({dims}, {src_hash[:12]})")
    for r in results:
        note = f" — {r['error']}" if r.get("error") else ""
        size = f"  {r['bytes'] / 1024:7.0f} KB" if r.get("bytes") else ""
        print(f"  {r['state']:<8} {str(r['width'] or '-'):>5}w  {r['file']}{size}{note}")
    if args.sync:
        failed = [r for r in results if r["state"] == "failed"]
        print(f"\n  {len(results) - len(failed)}/{len(results)} derivatives written from the current cover.")
        return 1 if failed else 0
    if drifted:
        print(f"\n  {len(drifted)} asset(s) do not match the current cover — run `sts.py cover --sync`.")
        return 1
    print("\n  site cover matches the book cover.")
    return 0


# --- flow: export the manuscript's figures as an upload-ready asset pack -----

FLOW_BG = "#020617"          # book navy, so rasterized diagrams land opaque
FLOW_WIDTH = 1600            # raster width for SVG diagrams
FLOW_KINDS = ("photo", "plate", "banner", "diagram")


def _flow_kind(image: str, credits: dict) -> str:
    """photo (licensed stock) · plate (original pixel art) · banner · diagram.

    Sharper than _figure_kind, which lumps every raster into 'photo'. The
    discriminator is credits.json: a file with a Wikimedia credit is somebody
    else's photograph; a raster without one is art made for this book.
    """
    name = Path(image).name
    stem = name.rsplit(".", 1)[0]
    if Path(image).suffix.lower() == ".svg":
        return "diagram"
    if re.match(r"part\d-divider$", stem):
        return "banner"
    return "photo" if name in credits else "plate"


def _flow_rasterize(chrome, svg: Path, dest: Path, width: int) -> str:
    """SVG -> opaque PNG at the source aspect ratio, via headless Chrome.

    qlmanage also renders SVG but letterboxes into a transparent square, which
    Flow reads as a padded image. Chrome honours the viewBox exactly.
    """
    head = svg.read_text(encoding="utf-8", errors="replace")[:2000]
    m = re.search(r'viewBox="([\d.\-\s]+)"', head)
    ratio = 0.5
    if m:
        nums = m.group(1).split()
        if len(nums) == 4 and float(nums[2]):
            ratio = float(nums[3]) / float(nums[2])
    height = max(1, round(width * ratio))
    with tempfile.TemporaryDirectory() as td:
        page = Path(td) / "page.html"
        page.write_text(
            f"<style>html,body{{margin:0;padding:0;background:{FLOW_BG}}}"
            f"img{{display:block;width:{width}px;height:auto}}</style>"
            f'<img src="{svg.resolve().as_uri()}">', encoding="utf-8")
        out = subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--window-size={width},{height}",
             f"--screenshot={dest}", page.as_uri()],
            capture_output=True, text=True, timeout=90)
    if not dest.exists():
        return (out.stderr or "chrome produced no file").strip().splitlines()[-1:][0]
    return ""


def cmd_flow(args) -> int:
    """Copy every manuscript figure into one flat, upload-ready folder."""
    kinds = {k.strip() for k in args.kinds.split(",")} if args.kinds \
        else set(FLOW_KINDS)
    bad = kinds - set(FLOW_KINDS)
    if bad:
        print(f"unknown kind(s): {sorted(bad)} — pick from {list(FLOW_KINDS)}")
        return 2

    out_dir = Path(args.out).expanduser() if args.out else \
        Path.home() / "Desktop" / "StS-Flow-Assets"
    credits = _load_credits()
    _, figs = _id_art_records()

    items, skipped = [], []
    for n, rec in enumerate(figs, 1):
        kind = _flow_kind(rec["image"], credits)
        src = STATIC_DIR / rec["image"].lstrip("/")
        stem = Path(rec["image"]).name.rsplit(".", 1)[0]
        ext = "png" if kind == "diagram" else Path(rec["image"]).suffix.lstrip(".")
        item = {"n": n, "kind": kind, "source": str(src.relative_to(ROOT)),
                "file": f"{kind}-{n:02d}-{stem}.{ext}",
                "chapter": rec["section"], "section": rec["heading"],
                "prompt": rec["alt"], "caption": rec["caption"],
                "art_id": rec["art_id"]}
        c = credits.get(Path(rec["image"]).name)
        if c:
            item["credit"] = {"artist": c.get("artist"),
                              "license": c.get("license"),
                              "source": c.get("page")}
        if kind not in kinds:
            continue
        if not src.exists():
            skipped.append({**item, "why": "source file missing"})
            continue
        items.append(item)

    if args.dry_run:
        if args.json:
            print(json.dumps({"out": str(out_dir), "assets": items,
                              "skipped": skipped}, indent=2, ensure_ascii=False))
            return 0
        by_kind = collections.Counter(i["kind"] for i in items)
        print(f"flow (dry run) — {len(items)} assets -> {out_dir}")
        for k in FLOW_KINDS:
            if by_kind[k]:
                print(f"  {k:<8} {by_kind[k]:>3}")
        for s in skipped:
            print(f"  ! {s['file']}: {s['why']}")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome() if any(i["kind"] == "diagram" for i in items) else None
    written = []
    for item in items:
        src, dest = ROOT / item["source"], out_dir / item["file"]
        if item["kind"] == "diagram":
            if not chrome:
                skipped.append({**item, "why": "Chrome/Chromium not found, so the "
                                               "SVG could not be rasterized"})
                continue
            err = _flow_rasterize(chrome, src, dest, args.width)
            if err:
                skipped.append({**item, "why": f"rasterize failed: {err}"})
                continue
        else:
            shutil.copy2(src, dest)
        item["bytes"] = dest.stat().st_size
        written.append(item)

    _flow_manifest(out_dir, written, skipped)

    if args.json:
        print(json.dumps({"out": str(out_dir), "written": written,
                          "skipped": skipped}, indent=2, ensure_ascii=False))
        return 1 if skipped else 0
    by_kind = collections.Counter(i["kind"] for i in written)
    total_mb = sum(i["bytes"] for i in written) / 1e6
    print(f"flow — {len(written)} assets ({total_mb:.1f} MB) -> {out_dir}")
    for k in FLOW_KINDS:
        if by_kind[k]:
            print(f"  {k:<8} {by_kind[k]:>3}")
    print("  + MANIFEST.md, flow-manifest.json, CREDITS.txt")
    for s in skipped:
        print(f"  ! {s['file']}: {s['why']}")
    return 1 if skipped else 0


def _flow_manifest(out_dir: Path, written: list, skipped: list) -> None:
    """MANIFEST.md (prompts, human-readable) + JSON + a credits roll-up."""
    (out_dir / "flow-manifest.json").write_text(json.dumps(
        {"schema": "sts-flow-pack/v1", "generated": date.today().isoformat(),
         "project": "Surviving the Singularity (book)",
         "assets": written, "skipped": skipped},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = ["# StS — Google Flow asset pack", "",
             f"Generated {date.today().isoformat()} · {len(written)} assets · "
             "every figure in the manuscript, in book order.", "",
             "Each **prompt** below is the figure's alt text: it already "
             "describes the shot in visual terms, so it drops straight into "
             "Flow as a prompt or as an ingredient caption.", ""]
    for kind in FLOW_KINDS:
        group = [i for i in written if i["kind"] == kind]
        if not group:
            continue
        lines += [f"## {kind} ({len(group)})", ""]
        for i in group:
            lines += [f"### `{i['file']}`", "",
                      f"- **Chapter:** {i['chapter']}"
                      + (f" · {i['section']}" if i["section"] else ""),
                      f"- **Prompt:** {i['prompt']}"]
            if i["caption"]:
                lines.append(f"- **Caption:** {i['caption']}")
            if i.get("credit"):
                c = i["credit"]
                lines.append(f"- **Credit:** {c['artist']} · {c['license']} · "
                             f"{c['source']}")
            lines.append("")
    if skipped:
        lines += ["## Not exported", ""] + \
                 [f"- `{s['file']}` — {s['why']}" for s in skipped] + [""]
    (out_dir / "MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")

    creds = ["Surviving the Singularity — asset credits",
             f"Generated {date.today().isoformat()}", "",
             "Licensed photographs (attribution required on reuse):", ""]
    for i in written:
        if i.get("credit"):
            c = i["credit"]
            creds.append(f"{i['file']}\n  {c['artist']} · {c['license']}\n"
                         f"  {c['source']}\n")
    creds += ["", "Original art (plates, banners, diagrams) is by the author;",
              "pixel-art plates were made with PixelLab and are subject to",
              "PixelLab's Terms of Service (https://pixellab.ai/termsofservice).",
              ""]
    (out_dir / "CREDITS.txt").write_text("\n".join(creds), encoding="utf-8")


# ──────────────────────────────────────────────────────────────────────
# verify — the fact-checking harness
# ──────────────────────────────────────────────────────────────────────
#
# Everything here exists because it was first found by hand, and finding it
# by hand does not scale to 27 sections under a September deadline. On
# 2026-07-26: chapter 9 printed 468/66.6 as 7.02 when it is 7.03, and the
# book shipped three different subtitles across book.json, app.html and the
# cover modal. Both are mechanical, so both should be a command.
#
# Design rule: a check either passes deterministically or it does not run.
# Nothing here asks the reader to trust a judgment call.

BOOK_SECTION_RE = re.compile(r"^\d\d-|^part\d-")

# Only these characters may reach the arithmetic evaluator.
SAFE_ARITH = re.compile(r"^[0-9\s.+\-*/()]+$")
# A stated result: a number, optionally followed by a unit.
STATED_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*([^\s0-9].*)?$")


def _eval_arith(expr: str):
    """Evaluate a pure-arithmetic string. Returns None if not safely evaluable."""
    if not SAFE_ARITH.match(expr) or not any(c.isdigit() for c in expr):
        return None
    import ast
    import operator
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.USub: operator.neg, ast.UAdd: operator.pos}

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in ops:
            return ops[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in ops:
            return ops[type(n.op)](ev(n.operand))
        raise ValueError("unsupported expression")
    try:
        return ev(ast.parse(expr.strip(), mode="eval"))
    except Exception:
        return None


def _strip_markup(line: str) -> str:
    line = re.sub(r"^\s*>+\s*", "", line)
    return line.replace("**", "").replace("`", "").replace("\\", "")


def verify_math() -> list:
    """Recompute every calculation the book shows its reader.

    The book prints its own divisions so a reader can check them. That makes
    them machine-checkable too, and makes a wrong one worse than a typo: the
    one place the text invites verification is the place it fails it.
    """
    problems = []
    for f in sorted(BOOK_DIR.glob("*.md")):
        if not BOOK_SECTION_RE.match(f.name):
            continue
        for lineno, raw in enumerate(f.read_text(encoding="utf-8",
                                                 errors="replace").splitlines(), 1):
            if "=" not in raw and "≈" not in raw:
                continue
            parts = re.split(r"[=≈]", _strip_markup(raw))
            if len(parts) < 2:
                continue
            for lhs, rhs in zip(parts, parts[1:]):
                left = _eval_arith(lhs)
                if left is None:
                    continue
                right_expr = _eval_arith(rhs)
                if right_expr is not None:
                    # expression = expression: compare directly
                    if abs(left - right_expr) > max(1e-9, abs(left) * 1e-9):
                        problems.append({
                            "file": f.name, "line": lineno,
                            "kind": "expression mismatch",
                            "detail": f"{lhs.strip()} = {left:g} but "
                                      f"{rhs.strip()} = {right_expr:g}"})
                    continue
                m = STATED_RE.match(rhs)
                if not m:
                    continue
                stated_s = m.group(1)
                stated = float(stated_s)
                decimals = len(stated_s.split(".")[1]) if "." in stated_s else 0
                if round(left, decimals) != round(stated, decimals):
                    problems.append({
                        "file": f.name, "line": lineno,
                        "kind": "rounding",
                        "detail": f"{lhs.strip()} = {left!r}, which rounds to "
                                  f"{round(left, decimals)}, but the text says {stated_s}"})
    return problems


def _subtitle_sources() -> dict:
    """Every place the book states what it is about."""
    found = {}
    bj = BOOK_DIR / "book.json"
    if bj.exists():
        try:
            found["book.json (EPUB/PDF metadata)"] = json.loads(
                bj.read_text(encoding="utf-8")).get("subtitle", "")
        except Exception:
            pass
    app = ROOT / "src/app.html"
    if app.exists():
        m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"',
                      app.read_text(encoding="utf-8"))
        if m:
            found["src/app.html (social + search)"] = m.group(1)
    modal = ROOT / "src/lib/components/BookCoverModal.svelte"
    if modal.exists():
        m = re.search(r'class="book-subtitle">([^<]+)<',
                      modal.read_text(encoding="utf-8"))
        if m:
            found["BookCoverModal.svelte (what a buyer sees)"] = m.group(1)
    return found


def _normalize_claim(s: str) -> str:
    s = s.lower()
    s = re.sub(r"^surviving the singularity[.:]?\s*", "", s)
    s = re.sub(r"^(a|the)\s+field manual for\s+", "", s)
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    return " ".join(s.split())


def verify_meta() -> list:
    """Catch drift between what the site promises and what the file says."""
    problems = []
    subs = _subtitle_sources()
    # book.json is canonical: it becomes the EPUB/PDF metadata a buyer downloads.
    # Surfaces that render a SUBTITLE must match it exactly. src/app.html holds a
    # meta *description* -- a ~155-char search snippet, a different field with a
    # different job -- so it only has to CONTAIN the subtitle, not equal it.
    # Comparing a description against a subtitle for equality is a category error
    # and made a correct description look like drift.
    DESCRIPTION_SOURCES = {"src/app.html (social + search)"}
    canonical_key = "book.json (EPUB/PDF metadata)"
    canonical = _normalize_claim(subs.get(canonical_key, ""))
    drifted = {}
    for k, v in subs.items():
        if not v or k == canonical_key:
            continue
        got = _normalize_claim(v)
        ok = canonical in got if k in DESCRIPTION_SOURCES else got == canonical
        if not ok:
            drifted[k] = v
    if canonical and drifted:
        problems.append({
            "kind": "subtitle drift",
            "detail": f"{len(drifted) + 1} different subtitles in production: "
                      + " | ".join(f"{k} -> {v!r}"
                                   for k, v in [(canonical_key,
                                                 subs[canonical_key])]
                                   + list(drifted.items()))})
    elif not canonical:
        problems.append({
            "kind": "subtitle missing",
            "detail": "book.json has no subtitle, so nothing can be checked "
                      "against it"})
    ads = advertised_prices()
    if len(ads) > 1:
        problems.append({
            "kind": "price drift",
            "detail": "site advertises conflicting prices: "
                      + ", ".join(fmt_cents(c) for c in sorted(ads))})
    return problems


def verify_precedents() -> dict:
    """Precedent Ledger integrity: P-01..P-23, one per section, all indexed."""
    per_section, all_ids = {}, set()
    for f in sorted(BOOK_DIR.glob("*.md")):
        if not BOOK_SECTION_RE.match(f.name):
            continue
        # Count the precedent a section OWNS (its `## Precedent P-NN:` heading),
        # not every mention. A bare "P-15" in prose is a cross-reference, and
        # counting those reported ch14 as carrying three precedents when it
        # carries two and merely points at P-15 inside the Sears passage.
        ids = sorted(set(re.findall(r"^## Precedent P-(\d{2})",
                                    f.read_text(encoding="utf-8",
                                                errors="replace"), re.M)))
        if ids:
            per_section[f.name] = ids
            all_ids.update(ids)
    expected = {f"{i:02d}" for i in range(1, LEDGER_SIZE + 1)}
    appendix_d = BOOK_DIR / "25-appendix-d.md"
    indexed = set(re.findall(r"P-(\d{2})", appendix_d.read_text(encoding="utf-8")
                             )) if appendix_d.exists() else set()
    # Appendix B (Works Cited) and Appendix D (the Ledger index) reference every
    # precedent by design. Counting them as reuse makes every ID look duplicated
    # and buries the two that actually are.
    INDEXES = {"23-appendix-b.md", "25-appendix-d.md"}
    prose = {s: ids for s, ids in per_section.items() if s not in INDEXES}
    where = {}
    for sec, ids in prose.items():
        for i in ids:
            where.setdefault(i, []).append(sec)
    return {
        "missing_from_book": sorted(expected - all_ids),
        "missing_from_appendix_d": sorted(expected - indexed),
        "unknown_ids": sorted(all_ids - expected),
        "in_multiple_sections": {i: v for i, v in sorted(where.items()) if len(v) > 1},
        "sections_with_multiple": {s: v for s, v in prose.items() if len(v) > 1},
    }


def verify_links(timeout: float = 12.0) -> list:
    """Liveness-check every source URL in Works Cited."""
    ap_b = BOOK_DIR / "23-appendix-b.md"
    if not ap_b.exists():
        return []
    urls, seen = [], set()
    for u in re.findall(r"https?://[^\s)>\]\"']+", ap_b.read_text(encoding="utf-8")):
        u = u.rstrip(".,;")
        if u not in seen:
            seen.add(u)
            urls.append(u)
    # Only a 404/410 is evidence that a source is gone. A 403 or 401 means the
    # host refused an automated request, which many publishers do by IP:
    # Britannica, MDPI and ResearchGate all refuse even with a browser user
    # agent, while the pages themselves are perfectly alive in a real browser.
    # Reporting those as dead sends someone to rewrite a working bibliography.
    dead, blocked, server_error, unreachable = [], [], [], []
    for u in urls:
        status, reason = _probe_url(u, timeout)
        if status == 200:
            continue
        entry = {"url": u, "status": status, "reason": reason}
        if status in (404, 410):
            dead.append(entry)
        elif status in (401, 403, 429):
            blocked.append(entry)
        elif status:
            server_error.append(entry)
        else:
            unreachable.append(entry)
    return {"checked": len(urls), "dead": dead, "blocked": blocked,
            "server_error": server_error, "unreachable": unreachable}


def _probe_url(url: str, timeout: float, attempts: int = 3):
    """Return (http_status, reason). status 0 means no HTTP answer at all.

    Retries network-level failures, because hammering ~200 hosts in a row
    provokes throttling and DNS hiccups that look exactly like a dead link.
    Only an actual HTTP status counts as evidence about the source.
    """
    reason = ""
    for attempt in range(attempts):
        for method in ("HEAD", "GET"):
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": "Mozilla/5.0 (compatible; sts.py link check)",
                "Accept": "*/*"})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return r.status, ""
            except urllib.error.HTTPError as e:
                if e.code in (403, 405, 501) and method == "HEAD":
                    continue  # host refuses HEAD; try GET before judging
                return e.code, f"HTTP {e.code}"
            except urllib.error.URLError as e:
                reason = str(getattr(e, "reason", e))[:90]
            except Exception as e:
                reason = f"{type(e).__name__}: {e}"[:90]
        if attempt < attempts - 1:
            time.sleep(1.5 * (attempt + 1))  # back off, then retry
    return 0, reason or "no response after retries"


def cmd_verify(args) -> int:
    checks = args.check or "all"
    result, failed = {}, 0

    if checks in ("all", "math"):
        result["math"] = verify_math()
        failed += len(result["math"])
    if checks in ("all", "meta"):
        result["meta"] = verify_meta()
        failed += len(result["meta"])
    if checks in ("all", "precedents"):
        p = verify_precedents()
        result["precedents"] = p
        failed += (len(p["missing_from_book"]) + len(p["missing_from_appendix_d"])
                   + len(p["unknown_ids"]))
    if checks in ("all", "refs"):
        result["refs"] = verify_refs()
        failed += len(result["refs"])
    if checks == "links" or (checks == "all" and args.links):
        result["links"] = verify_links()
        failed += len(result["links"]["dead"])

    if args.json:
        print(json.dumps(result, indent=2))
        return 1 if failed else 0

    print(f"Verifying the book against itself — sts.py v{VERSION}")
    if "math" in result:
        bad = result["math"]
        print(f"\n  math        {len(bad)} problem(s) in shown calculations")
        for p in bad:
            print(f"    {p['file']}:{p['line']}  [{p['kind']}] {p['detail']}")
    if "meta" in result:
        bad = result["meta"]
        print(f"\n  meta        {len(bad)} drift problem(s)")
        for p in bad:
            print(f"    [{p['kind']}] {p['detail']}")
    if "refs" in result:
        bad = result["refs"]
        print(f"\n  refs        {len(bad)} dangling cross-reference(s)")
        for p in bad:
            print(f"    {p['file']}:{p['line']}  {p['detail']}")
    if "precedents" in result:
        p = result["precedents"]
        print(f"\n  precedents  P-01..P-{LEDGER_SIZE:02d} ledger integrity")
        for key, label in (("missing_from_book", "never used in any section"),
                           ("missing_from_appendix_d", "not indexed in Appendix D"),
                           ("unknown_ids", "out of range")):
            if p[key]:
                print(f"    ERROR  {label}: {', '.join('P-' + i for i in p[key])}")
        for i, secs in p["in_multiple_sections"].items():
            print(f"    note   P-{i} appears in {len(secs)} sections: {', '.join(secs)}")
        for s, ids in p["sections_with_multiple"].items():
            print(f"    note   {s} carries {len(ids)}: {', '.join('P-' + i for i in ids)}")
        if not any(p[k] for k in ("missing_from_book", "missing_from_appendix_d",
                                  "unknown_ids")):
            print(f"    OK     all {LEDGER_SIZE} present in the book "
                  "and indexed in Appendix D")
    if "links" in result:
        lk = result["links"]
        print(f"\n  links       {lk['checked']} sources checked")
        print(f"    {len(lk['dead'])} dead (404/410) · {len(lk['blocked'])} bot-blocked "
              f"· {len(lk['server_error'])} server error · "
              f"{len(lk['unreachable'])} unreachable")
        for d in lk["dead"]:
            print(f"\n    DEAD {d['status']}  {d['url']}")
        if lk["server_error"]:
            print("\n    Server errors (recheck later, may be transient):")
            for d in lk["server_error"]:
                print(f"      {d['status']}  {d['url'][:80]}")
        if lk["unreachable"]:
            print("\n    No HTTP answer after 3 tries. Could be the source, could be "
                  "this network:")
            for d in lk["unreachable"]:
                print(f"      {d['reason'][:40]:<40}  {d['url'][:60]}")
        if lk["blocked"]:
            print(f"\n    {len(lk['blocked'])} hosts refused an automated request "
                  "(401/403/429). This is NOT evidence the page is gone: Britannica, "
                  "MDPI and ResearchGate refuse by IP even with a browser user agent. "
                  "Spot-check by hand, do not bulk-edit Appendix B from this list.")
            for d in lk["blocked"][:8]:
                print(f"      {d['status']}  {d['url'][:80]}")
            if len(lk["blocked"]) > 8:
                print(f"      ... and {len(lk['blocked']) - 8} more (--json for all)")
    elif checks == "all" and not args.links:
        print("\n  links       skipped (network). Add --links to check Works Cited.")

    print(f"\n  {failed} problem(s) found" if failed else "\n  Clean.")
    return 1 if failed else 0


# ──────────────────────────────────────────────────────────────────────
# factcheck
# ──────────────────────────────────────────────────────────────────────
#
# A chain of custody for every mechanically detectable claim in the book.
#
# Local only by design. This pass makes no network request. Every hop it
# cannot resolve from the working tree plus the git object store is recorded
# BROKEN with a reason, never inferred. A hop that is merely plausible is
# still BROKEN.
#
# The anchor is the block id from `sts id`, not a line number. Line numbers
# rot on the next edit; block ids survive it.

FC_SCHEMA = "sts-factcheck/v1"
FC_REPO = "https://github.com/ctavolazzi/survivingthesingularity"
FC_BOOK_REL = "src/lib/data/book"

# Verdicts. CONTRADICTED is reserved for a claim this pass can actively
# disprove from local evidence, which in a local only run means a broken
# internal reference or a missing asset. An unverified external source is
# UNCHECKED, never UNSUPPORTED: absence of a network pass is not evidence.
FC_SUPPORTED = "SUPPORTED"
FC_PARTIAL = "PARTIAL"
FC_UNSUPPORTED = "UNSUPPORTED"
FC_UNCHECKED = "UNCHECKED"
FC_UNCHECKABLE = "UNCHECKABLE"
FC_CONTRADICTED = "CONTRADICTED"

# ---- the network half, if it has been run.
#
# scripts/factcheck_network.py fetches every Appendix B citation and writes one
# JSON record per URL into .factcheck-cache/. This pass READS that cache; it
# never fetches anything itself, so `sts factcheck` stays offline and instant.
# If the cache is absent the behaviour is exactly what it always was: every URL
# comes back UNCHECKED and the report says no network run informed it.
#
# THE MAPPING IS DELIBERATELY STINGY. Only LIVE_CONFIRMED promotes a claim to
# SUPPORTED, and LIVE_CONFIRMED already means the tool found the citation's own
# title words on the fetched page, not merely that the host answered 200.
# Everything else stays UNCHECKED and carries the real reason:
#
#   BLOCKED           the host refuses automated clients. That is a fact about
#                     the host and is NOT evidence against the citation, so it
#                     must never read as a failure.
#   WALLED            gated, and the cited work was not visible behind the gate.
#   LIVE_UNVERIFIED   live, but the body was never parsed (PDF and other
#                     non-HTML). Live is not the same as verified.
#   LIVE_UNCONFIRMED  live HTML, but the cited title was not on the page.
#
# The temptation is to call the last two PARTIAL because the host did answer.
# Resisted on purpose: a reader scanning the audit reads any non-UNCHECKED
# verdict as "someone checked this", and for these nobody has.
FC_NET_CACHE_REL = ".factcheck-cache"

FC_NET_TO_VERDICT = {
    "LIVE_CONFIRMED": FC_SUPPORTED,
    "LIVE_UNVERIFIED": FC_UNCHECKED,
    "LIVE_UNCONFIRMED": FC_UNCHECKED,
    "BLOCKED": FC_UNCHECKED,
    "WALLED": FC_UNCHECKED,
    "SERVER_ERROR": FC_UNCHECKED,
    "UNREACHABLE": FC_UNCHECKED,
    "OTHER": FC_UNCHECKED,
    # A host that answered 404/410 for a citation the book relies on is the one
    # case the network half can actively disprove.
    "DEAD": FC_UNSUPPORTED,
    "SOFT_404": FC_UNSUPPORTED,
}


def _fc_network_cache() -> dict:
    """Load the network half keyed by URL. Absent cache means an offline run."""
    out = {}
    d = ROOT / FC_NET_CACHE_REL
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.json")):
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue  # a truncated cache entry is a miss, not a crash
        url = r.get("url")
        if url and r.get("state"):
            out[url] = r
    return out

_FC_PCT = re.compile(r"\b\d+(?:\.\d+)?\s?(?:%|percent\b)")
_FC_MONEY = re.compile(
    r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:billion|million|trillion|thousand))?", re.I)
_FC_MAG = re.compile(r"\b\d[\d,]*(?:\.\d+)?\s+(?:billion|million|trillion)\b", re.I)
_FC_YEAR = re.compile(r"\b(?:1[5-9]\d{2}|20\d{2})\b")
_FC_URL = re.compile(r"https?://[^\s)>\]\"']+")
_FC_PREC = re.compile(r"\bP-(\d{2})\b")
_FC_PREC_HEAD = re.compile(r"^##\s+Precedent\s+P-(\d{2})\s*:", re.M)
_FC_CHAP = re.compile(r"\bChapter\s+(\d+)\b")
_FC_APDX = re.compile(r"\bAppendix\s+([A-Z])\b")
_FC_TABLE = re.compile(r"\bTable\s+(\d+)\b")
_FC_ATTRIB = re.compile(
    r"\b(?:said|says|wrote|writes|argued|argues|noted|notes|observed|observes|"
    r"according to|told|declared|predicted|warned|put it|estimated|reported)\b", re.I)
_FC_CAUSAL = re.compile(
    r"\b(?:because|therefore|as a result|led to|leads to|caused|causes|"
    r"results in|resulted in|drove|drives|means that|which is why)\b", re.I)
_FC_COMPARE = re.compile(
    r"\b(?:more than|larger than|greater than|fewer than|less than|the first|"
    r"the largest|the biggest|the only|the worst|the fastest|twice as|"
    r"half as|outnumber(?:ed|s)?)\b", re.I)

# Sentence enders that are abbreviations, not sentence boundaries.
_FC_ABBREV = {"c", "ca", "e.g", "i.e", "vs", "mr", "mrs", "ms", "dr", "st",
              "no", "fig", "approx", "est", "cf", "al", "u.s", "u.k", "b.c",
              "a.d", "jr", "sr", "inc", "ltd", "co"}

# Capitalized tokens that carry no proper noun signal on their own.
_FC_STOPCAP = {
    "The", "A", "An", "And", "But", "Or", "If", "In", "On", "At", "By", "For",
    "From", "To", "With", "As", "It", "This", "That", "These", "Those", "There",
    "When", "Where", "What", "Why", "How", "Who", "We", "You", "They", "He",
    "She", "I", "Not", "No", "Yes", "So", "Then", "Now", "Every", "Each",
    "Most", "More", "Less", "One", "Two", "Three", "Their", "His", "Her",
    "Its", "Our", "Your", "My", "Was", "Were", "Is", "Are", "Be", "Been",
    "Had", "Has", "Have", "Do", "Does", "Did", "Will", "Would", "Can",
    "Could", "Should", "May", "Might", "Must", "Let", "Look", "Think",
    "Consider", "Imagine", "Because", "After", "Before", "During", "While",
    "Until", "Since", "Between", "Under", "Over", "Above", "Below",
}


def _fc_sentences(text: str):
    """Split into sentences, returning (sentence, char_offset) pairs.

    Deliberately simple. It merges a fragment back when the break followed a
    known abbreviation, which is the failure mode that matters here ("c. 1177
    BC", "U.S."). It is not a linguistics engine and does not pretend to be:
    a mis-split shows up as a slightly wide or narrow quote, never as a wrong
    verdict, because verdicts key off the matched span rather than the
    sentence.
    """
    parts, buf, start, pos = [], "", 0, 0
    for chunk in re.split(r"(?<=[.!?])(\s+)", text):
        if chunk.strip() == "" and chunk != "":
            buf += chunk
            pos += len(chunk)
            continue
        if not buf:
            start = pos
        buf += chunk
        pos += len(chunk)
        tail = buf.rstrip()
        last = tail.split()[-1].rstrip(".!?").lower() if tail.split() else ""
        if last in _FC_ABBREV or (len(last) == 1 and last.isalpha()):
            continue
        if tail:
            parts.append((tail, start))
        buf = ""
    if buf.strip():
        parts.append((buf.strip(), start))
    return parts


def _fc_has_proper_noun(sentence: str) -> bool:
    """True if the sentence carries a capitalized token that is not sentence
    initial and is not a common capitalized function word."""
    toks = sentence.split()
    for tok in toks[1:]:
        bare = tok.strip("\"'(),.;:!?*_[]")
        if len(bare) > 2 and bare[0].isupper() and bare not in _FC_STOPCAP:
            return True
    return False


def _fc_line_of(block_start: int, text: str, offset: int) -> int:
    """1-indexed file line for a char offset inside a block's joined source."""
    return block_start + text.count("\n", 0, offset)


def _fc_git_state(files):
    """Receipt state per book file, resolved against what exists on origin.

    Three states, and the distinction is the whole point:

      origin_exact  the working tree file is byte identical to the file at
                    origin/main, so current line numbers are valid at that
                    SHA and a permalink pinned to it resolves for anybody.
      local_only    committed here but not identical to origin, so no SHA a
                    reader can fetch describes this text.
      uncommitted   dirty in the working tree. There is no SHA at all.

    Pinning a receipt to a local only SHA would produce a link that 404s for
    every reader but this machine, so those are recorded BROKEN instead.
    """
    dirty = set()
    porcelain = git("status", "--porcelain", "--", FC_BOOK_REL)
    for line in porcelain.splitlines():
        if len(line) > 3:
            dirty.add(Path(line[3:].strip().strip('"')).name)

    origin_sha = git("rev-parse", "origin/main")
    origin_short = origin_sha[:12] if origin_sha else None
    head_sha = git("rev-parse", "HEAD")

    state = {}
    for fname in files:
        abs_path = BOOK_DIR / fname
        rel = f"{FC_BOOK_REL}/{fname}"
        work_blob = git("hash-object", str(abs_path))
        origin_blob = git("rev-parse", f"origin/main:{rel}")
        blame = {}
        if fname not in dirty:
            blame = _fc_blame(rel)
        if fname in dirty:
            rstate, reason = "uncommitted", (
                "uncommitted working-tree content, no immutable receipt exists yet")
        elif work_blob and origin_blob and work_blob == origin_blob:
            rstate, reason = "origin_exact", None
        else:
            rstate, reason = "local_only", (
                "committed locally but not present on origin, so no SHA a reader "
                "can resolve describes this text")
        state[fname] = {
            "file": fname,
            "rel_path": rel,
            "receipt_state": rstate,
            "reason": reason,
            "origin_sha": origin_sha or None,
            "origin_short": origin_short,
            "head_sha": head_sha or None,
            "work_blob": work_blob or None,
            "origin_blob": origin_blob or None,
            "blame": blame,
        }
    return state


def _fc_blame(rel_path: str):
    """line number -> {sha, author, date, summary} from git blame against HEAD."""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "blame", "--line-porcelain", "HEAD", "--", rel_path],
        capture_output=True, text=True)
    if out.returncode != 0:
        return {}
    blame, sha, author, ts, summary, lineno = {}, None, None, None, None, None
    for line in out.stdout.splitlines():
        m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", line)
        if m:
            sha, lineno = m.group(1), int(m.group(2))
        elif line.startswith("author "):
            author = line[7:]
        elif line.startswith("author-time "):
            ts = int(line[12:])
        elif line.startswith("summary "):
            summary = line[8:]
        elif line.startswith("\t") and sha is not None:
            blame[lineno] = {
                "sha": sha, "short": sha[:12], "author": author,
                "date": (date.fromtimestamp(ts).isoformat() if ts else None),
                "summary": summary,
            }
    return blame


def _fc_targets(index):
    """Everything an internal cross-reference could legitimately point at."""
    chapters, appendices, precedents, tables = set(), set(), set(), set()
    art_ids, images = set(), {}
    for sec in index["sections"]:
        m = re.match(r"^Chapter (\d+)", sec["title"])
        if m:
            chapters.add(int(m.group(1)))
        m = re.match(r"^Appendix ([A-Z])", sec["title"])
        if m:
            appendices.add(m.group(1))
        src = (BOOK_DIR / sec["file"]).read_text(encoding="utf-8")
        for pm in _FC_PREC_HEAD.finditer(src):
            precedents.add(f"P-{pm.group(1)}")
        for blk in sec["blocks"]:
            if blk.get("art_id"):
                art_ids.add(blk["art_id"])
            if blk.get("image"):
                images[blk["image"]] = blk["id"]
    # Tables are numbered in prose, not in markup. A "Table N" reference is
    # resolvable only against the table blocks that actually exist.
    n_tables = sum(1 for sec in index["sections"]
                   for blk in sec["blocks"] if blk["type"] == "table")
    tables = set(range(1, n_tables + 1))

    catalog_ids = set()
    cat_path = BOOK_DIR / "art-catalog.json"
    if cat_path.exists():
        cat = json.loads(cat_path.read_text(encoding="utf-8"))
        catalog_ids = {a["id"] for a in cat.get("assets", [])}
    return {
        "chapters": chapters, "appendices": appendices, "precedents": precedents,
        "tables": tables, "n_tables": n_tables, "art_ids": art_ids,
        "images": images, "catalog_ids": catalog_ids,
    }


def _fc_works_cited():
    """Every URL that appears in the Works Cited appendix, as a set."""
    cited = set()
    for fname in ("23-appendix-b.md",):
        p = BOOK_DIR / fname
        if p.exists():
            cited |= set(_FC_URL.findall(p.read_text(encoding="utf-8")))
    return {u.rstrip(".,);") for u in cited}


def _fc_extract(index, targets, cited, gitstate, net=None):
    """The extraction pass. One record per claim, keyed by block id."""
    claims = []
    stats = collections.Counter()
    seq = 0

    for sec in index["sections"]:
        fname = sec["file"]
        gs = gitstate[fname]
        src_lines = (BOOK_DIR / fname).read_text(encoding="utf-8").split("\n")

        for blk in sec["blocks"]:
            a, b = blk["lines"]
            text = "\n".join(src_lines[a - 1:b])

            def mk(ctype, quote, offset, verdict, note, **extra):
                nonlocal seq
                seq += 1
                line = _fc_line_of(a, text, offset)
                bl = gs["blame"].get(line) or {}
                if gs["receipt_state"] == "origin_exact":
                    permalink = (f"{FC_REPO}/blob/{gs['origin_sha']}/"
                                 f"{gs['rel_path']}#L{line}")
                    link_state = "resolvable"
                else:
                    permalink, link_state = None, "broken"
                rec = {
                    "seq": seq,
                    "claim": quote.strip(),
                    "type": ctype,
                    "section": sec["id"],
                    "section_title": sec["title"],
                    "file": fname,
                    "line": line,
                    "block_id": blk["id"],
                    "block_type": blk["type"],
                    "block_lines": [a, b],
                    "block_hash": blk.get("hash"),
                    "git": {
                        "receipt_state": gs["receipt_state"],
                        "reason": gs["reason"],
                        "sha": bl.get("sha"),
                        "short": bl.get("short"),
                        "author": bl.get("author"),
                        "date": bl.get("date"),
                        "summary": bl.get("summary"),
                        "permalink": permalink,
                        "link_state": link_state,
                    },
                    "verdict": verdict,
                    "note": note,
                }
                rec.update(extra)
                claims.append(rec)
                stats[ctype] += 1
                stats[f"verdict:{verdict}"] += 1
                return rec

            # ---- internal cross references. Exact, and locally decidable.
            for m in _FC_PREC.finditer(text):
                pid = f"P-{m.group(1)}"
                # A precedent's own heading is a definition, not a reference.
                if re.match(r"^##\s+Precedent\s+" + re.escape(pid), text):
                    continue
                ok = pid in targets["precedents"]
                mk("internal_xref", m.group(0), m.start(),
                   FC_SUPPORTED if ok else FC_CONTRADICTED,
                   (f"{pid} resolves to a `## Precedent {pid}:` heading in the book."
                    if ok else
                    f"{pid} is referenced but no `## Precedent {pid}:` heading exists. "
                    "Dangling internal reference."),
                   xref_kind="precedent", target=pid, resolved=ok)

            for m in _FC_CHAP.finditer(text):
                n = int(m.group(1))
                ok = n in targets["chapters"]
                mk("internal_xref", m.group(0), m.start(),
                   FC_SUPPORTED if ok else FC_CONTRADICTED,
                   (f"Chapter {n} exists in book.json running order."
                    if ok else
                    f"Chapter {n} is referenced but the book has no such chapter. "
                    "Dangling internal reference."),
                   xref_kind="chapter", target=f"Chapter {n}", resolved=ok)

            for m in _FC_APDX.finditer(text):
                letter = m.group(1)
                ok = letter in targets["appendices"]
                mk("internal_xref", m.group(0), m.start(),
                   FC_SUPPORTED if ok else FC_CONTRADICTED,
                   (f"Appendix {letter} exists in book.json running order."
                    if ok else
                    f"Appendix {letter} is referenced but no such appendix exists. "
                    "Dangling internal reference."),
                   xref_kind="appendix", target=f"Appendix {letter}", resolved=ok)

            for m in _FC_TABLE.finditer(text):
                n = int(m.group(1))
                ok = n in targets["tables"]
                mk("internal_xref", m.group(0), m.start(),
                   FC_PARTIAL if ok else FC_CONTRADICTED,
                   (f"The book contains {targets['n_tables']} table blocks, so a "
                    f"Table {n} plausibly exists, but table numbering lives in prose "
                    "and nothing binds this reference to a specific table block."
                    if ok else
                    f"Table {n} is referenced but the book has only "
                    f"{targets['n_tables']} table blocks."),
                   xref_kind="table", target=f"Table {n}", resolved=ok)

            # ---- figures. art_id resolution plus the asset actually on disk.
            if blk["type"] == "figure" and blk.get("image"):
                img = blk["image"]
                art_id = blk.get("art_id")
                on_disk = (STATIC_DIR / img.lstrip("/")).exists()
                in_cat = bool(art_id) and art_id in targets["catalog_ids"]
                if not on_disk:
                    v, note = FC_CONTRADICTED, (
                        f"The manuscript renders {img} but no such file exists under "
                        "static/. A reader gets a broken image.")
                elif not art_id:
                    v, note = FC_PARTIAL, (
                        f"{img} is on disk but the block carries no art_id, so it is "
                        "not enrolled in art-catalog.json and nothing tracks its "
                        "provenance or licence.")
                elif not in_cat:
                    v, note = FC_PARTIAL, (
                        f"{img} is on disk and the block declares art_id {art_id}, but "
                        "that id is absent from art-catalog.json.")
                else:
                    v, note = FC_SUPPORTED, (
                        f"{img} exists under static/ and art_id {art_id} resolves in "
                        "art-catalog.json.")
                mk("image", blk["preview"][:200], 0, v, note,
                   image=img, art_id=art_id, on_disk=on_disk, in_catalog=in_cat)

            # ---- URLs. Resolved from the network cache when one exists, and
            # UNCHECKED (never dead) when it does not. Absence of a fetch is
            # not evidence against a citation.
            for m in _FC_URL.finditer(text):
                url = m.group(0).rstrip(".,);")
                host = urllib.parse.urlparse(url).netloc.lower()
                in_cited = url in cited
                bare_wiki = host.endswith("wikipedia.org")

                cited_note = ("The URL also appears in the Appendix B Works Cited list."
                              if in_cited else
                              "This URL does not appear in the Appendix B Works Cited "
                              "list.")
                wiki_note = (" Host is Wikipedia, which the P-09 post mortem flags as "
                             "unverified by default when it is a claim's only citation."
                             if bare_wiki else "")

                hit = (net or {}).get(url)
                if hit:
                    state = hit["state"]
                    verdict = FC_NET_TO_VERDICT.get(state, FC_UNCHECKED)
                    mk("url", url, m.start(), verdict,
                       f"{hit.get('detail', state)} {cited_note}{wiki_note}",
                       url=url, host=host, in_works_cited=in_cited,
                       bare_wikipedia=bare_wiki, source_state=state,
                       source_detail=hit.get("detail", ""),
                       source_status=hit.get("status"),
                       source_final_url=hit.get("final_url"),
                       source_title_match=hit.get("match"),
                       checked_with=hit.get("checked_with"),
                       archive_url=None, archive_date=None)
                else:
                    mk("url", url, m.start(), FC_UNCHECKED,
                       ("Liveness and content were not checked: no network record "
                        "exists for this URL. "
                        + cited_note + wiki_note),
                       url=url, host=host, in_works_cited=in_cited,
                       bare_wikipedia=bare_wiki, source_state="UNCHECKED",
                       archive_url=None, archive_date=None)

            # ---- prose claims. Sentence scoped.
            if blk["type"] in ("paragraph", "list", "blockquote", "caption", "table"):
                for sent, off in _fc_sentences(text):
                    if sent.startswith("!["):
                        continue
                    is_stat = bool(_FC_PCT.search(sent) or _FC_MONEY.search(sent)
                                   or _FC_MAG.search(sent))
                    years = _FC_YEAR.findall(sent)
                    is_attrib = (blk["type"] == "blockquote"
                                 or bool(_FC_ATTRIB.search(sent)))
                    is_causal = bool(_FC_CAUSAL.search(sent))
                    is_compare = bool(_FC_COMPARE.search(sent))
                    has_proper = _fc_has_proper_noun(sent)
                    nearby_url = bool(_FC_URL.search(text))

                    base_note = (
                        "No external source was resolved: this run is local only and "
                        "made no network request. "
                        + ("The enclosing block carries a URL."
                           if nearby_url else
                           "The enclosing block carries no URL, so even a network run "
                           "would have nothing to resolve from the text itself."))

                    if is_stat:
                        mk("statistic", sent, off, FC_UNCHECKED,
                           base_note + (" Comparison language present, which the P-09 "
                                        "post mortem identifies as the book's actual "
                                        "failure mode." if is_compare else ""),
                           has_citation_nearby=nearby_url,
                           comparison_claim=is_compare)
                    # A bare year in prose is context, not an asserted event. It is
                    # promoted to a dated_event claim only when the sentence also
                    # names something. Everything not promoted is counted and
                    # reported rather than silently dropped.
                    if years:
                        if has_proper or is_attrib:
                            mk("dated_event", sent, off, FC_UNCHECKED,
                               base_note, years=sorted(set(years)),
                               has_citation_nearby=nearby_url,
                               comparison_claim=is_compare)
                        else:
                            stats["year_mentions_not_promoted"] += 1
                    if is_attrib and not is_stat:
                        mk("attribution", sent, off, FC_UNCHECKED,
                           base_note, has_citation_nearby=nearby_url,
                           comparison_claim=is_compare)
                    if is_causal and not (is_stat or is_attrib):
                        mk("causal_claim", sent, off, FC_UNCHECKABLE,
                           "Causal claims are not mechanically decidable. This one was "
                           "detected by connective language only and needs a human "
                           "reader; no automated verdict is offered.",
                           has_citation_nearby=nearby_url,
                           comparison_claim=is_compare)
    return claims, stats


# What this pass does NOT cover, stated so the trace cannot imply otherwise.
FC_NOT_COVERED_NET_OFF = {
    "kind": "external source liveness",
    "why": "No network record exists for this run. No URL was fetched, so no source "
           "is known live, dead, paywalled or archived. Run "
           "`python3 scripts/factcheck_network.py` to populate it.",
}

FC_NOT_COVERED_NET_ON = {
    "kind": "external source content, beyond the title",
    "why": "The network half fetched every Works Cited URL and asked whether the "
           "citation's own title words appear on the page, which is why a bare 200 "
           "is never enough to confirm one. It does NOT read the source and check "
           "that it supports the sentence citing it. A LIVE_CONFIRMED citation is a "
           "real page carrying the right title, not a verified argument. PDFs are "
           "fetched but never parsed, so they stay unconfirmed on purpose.",
}

FC_NOT_COVERED = [
    {"kind": "named entity",
     "why": "No entity extraction is implemented. Recognising 'Frank Darvall' as a "
            "person and checking that the person said the thing needs either a "
            "gazetteer or a model, and guessing from capitalisation would produce "
            "confident nonsense."},
    {"kind": "archive.org snapshots",
     "why": "Requires an archive pass that is not built. Every archive hop is "
            "recorded BROKEN."},
    {"kind": "causal claim adjudication",
     "why": "Detected but never adjudicated. A connective word is not a causal claim "
            "and no automated verdict is offered."},
    {"kind": "quotation wording",
     "why": "Attributions are located, but whether the quoted words match the source "
            "text is not checked. That needs the source, which needs network."},
    {"kind": "table numbering",
     "why": "Table numbers live in prose, not in markup. Nothing binds 'Table 2' to a "
            "specific table block, so these resolve only to a plausible range."},
]


def cmd_factcheck(args) -> int:
    index = _live_index()
    targets = _fc_targets(index)
    cited = _fc_works_cited()
    files = [sec["file"] for sec in index["sections"]]
    gitstate = _fc_git_state(files)
    net = _fc_network_cache()
    claims, stats = _fc_extract(index, targets, cited, gitstate, net)

    by_state = collections.Counter(g["receipt_state"] for g in gitstate.values())
    verdicts = collections.Counter(c["verdict"] for c in claims)
    types = collections.Counter(c["type"] for c in claims)
    resolvable = sum(1 for c in claims if c["git"]["link_state"] == "resolvable")

    url_claims = [c for c in claims if c["type"] == "url"]
    net_states = collections.Counter(
        c["source_state"] for c in url_claims if c["source_state"] != "UNCHECKED")
    matched = sum(1 for c in url_claims if c["source_state"] != "UNCHECKED")

    # `network` was a bare False. It is now the receipt for the network half, so
    # a reader can see how many URLs were actually fetched and in what state
    # rather than taking "network: true" on faith.
    network = False if not net else {
        "cache": FC_NET_CACHE_REL,
        "urls_cached": len(net),
        "url_claims": len(url_claims),
        "url_claims_resolved": matched,
        "url_claims_unresolved": len(url_claims) - matched,
        "by_source_state": dict(net_states),
        "confirmed_means": "the citation's own title words were found on the fetched "
                           "page. A bare HTTP 200 is never enough.",
    }

    report = {
        "schema": FC_SCHEMA,
        "generated": date.today().isoformat(),
        "network": network,
        "repo": FC_REPO,
        "repo_public": True,
        "book_version": index.get("book_version"),
        "totals": {
            "sections": len(index["sections"]),
            "blocks": index["totals"]["blocks"],
            "words": index["totals"]["words"],
            "claims": len(claims),
            "receipts_resolvable": resolvable,
            "year_mentions_not_promoted": stats.get("year_mentions_not_promoted", 0),
        },
        "by_type": dict(types),
        "by_verdict": dict(verdicts),
        "by_receipt_state": dict(by_state),
        "targets": {
            "chapters": sorted(targets["chapters"]),
            "appendices": sorted(targets["appendices"]),
            "precedents": sorted(targets["precedents"]),
            "tables": targets["n_tables"],
            "art_ids": len(targets["art_ids"]),
            "catalog_ids": len(targets["catalog_ids"]),
            "works_cited_urls": len(cited),
        },
        "git": {fname: {k: v for k, v in g.items() if k != "blame"}
                for fname, g in gitstate.items()},
        "not_covered": FC_NOT_COVERED + [
            FC_NOT_COVERED_NET_ON if net else FC_NOT_COVERED_NET_OFF],
        "claims": claims,
    }

    if args.out:
        outp = Path(args.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    t = report["totals"]
    print(f"\nfactcheck  {t['claims']:,} claims across {t['sections']} sections "
          f"({t['words']:,} words)")
    if network:
        n = network
        print(f"  network: ON from {n['cache']}/. "
              f"{n['url_claims_resolved']} of {n['url_claims']} URL claims resolved, "
              f"{n['url_claims_unresolved']} with no record.")
        print("    " + "  ".join(f"{k} {v}" for k, v in
                                 sorted(n["by_source_state"].items())))
        print("    Only LIVE_CONFIRMED counts as SUPPORTED. A refusal is not a "
              "failure of the citation.\n")
    else:
        print("  network: OFF. No URL was fetched. External source hops are BROKEN.\n")
    print("  by type")
    for k, v in types.most_common():
        print(f"    {k:<18} {v:>6}")
    print("\n  by verdict")
    for k, v in verdicts.most_common():
        print(f"    {k:<18} {v:>6}")
    print("\n  git receipts")
    for k, v in by_state.most_common():
        print(f"    {k:<18} {v:>6} file(s)")
    print(f"    {'resolvable links':<18} {resolvable:>6} of {t['claims']} claims")
    print(f"\n  {t['year_mentions_not_promoted']} bare year mentions were triaged out "
          "as prose context, not claims.")
    if args.out:
        print(f"\n  wrote {args.out}")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="sts.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name, fn in (("status", cmd_status), ("audit", cmd_audit),
                     ("live", cmd_live), ("routes", cmd_routes)):
        p = sub.add_parser(name)
        p.add_argument("--json", action="store_true")
        p.set_defaults(fn=fn)

    p = sub.add_parser("verify")
    p.add_argument("--json", action="store_true")
    p.add_argument("check", nargs="?",
                   choices=["all", "math", "meta", "precedents", "refs", "links"],
                   help="which check to run (default: all fast checks)")
    p.add_argument("--links", action="store_true",
                   help="with 'all', also liveness-check every Works Cited URL "
                        "(network, slow)")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("factcheck",
                       help="chain of custody for every mechanically detectable "
                            "claim (local only, no network)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--out", help="write the JSON inventory to this path")
    p.set_defaults(fn=cmd_factcheck)

    p = sub.add_parser("stripe")
    p.add_argument("--json", action="store_true")
    p.add_argument("--live", action="store_true",
                   help="probe PRODUCTION instead of local .env: live-vs-test mode, "
                        "webhook health, and whether the price charged matches the "
                        "price advertised. Creates a real (unpaid, expiring) checkout "
                        "session each run. Exits non-zero on drift.")
    p.add_argument("--no-price", action="store_true",
                   help="with --live, skip the browser render that reads the charged "
                        "amount (faster, but stops catching price mismatches)")
    p.set_defaults(fn=cmd_stripe)

    p = sub.add_parser("book")
    p.add_argument("--json", action="store_true")
    p.add_argument("--thin", type=int, default=1500,
                   help="flag chapters under this many words (default 1500)")
    p.set_defaults(fn=cmd_book)

    p = sub.add_parser("images")
    p.add_argument("--json", action="store_true")
    p.add_argument("--fetch", action="store_true",
                   help="download missing registry images from Wikimedia Commons (license-gated)")
    p.add_argument("--apply", action="store_true",
                   help="write changes (default is a dry run)")
    p.add_argument("--file", help="operate on a compiled draft instead of the chapter files")
    p.add_argument("--stdout", action="store_true",
                   help="with --file: print the transformed draft instead of reporting")
    p.set_defaults(fn=cmd_images)

    p = sub.add_parser("quotes")
    p.add_argument("--json", action="store_true")
    p.add_argument("--apply", action="store_true",
                   help="write changes (default is a dry run)")
    p.add_argument("--file", help="operate on a compiled draft instead of the chapter files")
    p.add_argument("--stdout", action="store_true",
                   help="with --file: print the transformed draft instead of reporting")
    p.set_defaults(fn=cmd_quotes)

    p = sub.add_parser("sitemap")
    p.add_argument("--json", action="store_true")
    p.add_argument("--write", action="store_true",
                   help="regenerate static/sitemap.xml from the real route table")
    p.set_defaults(fn=cmd_sitemap)

    p = sub.add_parser("compile",
                       help="concatenate book source into one manuscript draft markdown")
    p.add_argument("--out", help="output path (default manuscript/StS-Complete-Draft-compiled-<date>.md)")
    p.add_argument("--tag", help="manuscript tag for the header (default book.json version)")
    p.add_argument("--stdout", action="store_true", help="print instead of writing")
    p.add_argument("--force", action="store_true", help="overwrite an existing output file")
    p.set_defaults(fn=cmd_compile)

    p = sub.add_parser("scan",
                       help="scannability audit: pull quotes, walls of text, deserts, lists")
    p.add_argument("--json", action="store_true")
    p.add_argument("--top", type=int, default=3,
                   help="findings per category per file (default 3)")
    p.add_argument("--all", action="store_true",
                   help="include sections with zero findings in the report")
    p.set_defaults(fn=cmd_scan)

    p = sub.add_parser("refs",
                       help="internal cross-references: [](sts:chapter1) pointers "
                            "that renumber themselves instead of rotting")
    refsub = p.add_subparsers(dest="action", required=True)
    rl = refsub.add_parser("list", help="every cross-reference, dangling ones marked")
    rl.add_argument("--to", help="only refs pointing at this section or block id")
    rl.add_argument("--json", action="store_true")
    rr = refsub.add_parser("render",
                           help="print one section with refs expanded (build hook)")
    rr.add_argument("file", help="section filename or path")
    rs = refsub.add_parser("stress",
                           help="prove the resolver on a throwaway copy of the book")
    rs.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_refs)

    p = sub.add_parser("research",
                       help="search the web for sources/examples (Wikipedia + DuckDuckGo)")
    p.add_argument("query", nargs="+", help="search terms")
    p.add_argument("--json", action="store_true")
    p.add_argument("-n", type=int, default=5, help="results per engine (default 5)")
    p.add_argument("--wiki-only", action="store_true")
    p.add_argument("--web-only", action="store_true")
    p.add_argument("--summary", action="store_true",
                   help="pull full intro extracts for Wikipedia hits")
    p.add_argument("--sleep", type=int, default=0,
                   help="seconds to wait before the web query (batch politeness; ~20s avoids captchas)")
    p.add_argument("--save", action="store_true",
                   help="append results to manuscript/sources/research-log.md")
    p.set_defaults(fn=cmd_research)

    p = sub.add_parser("id",
                       help="manuscript addressing: a stable unique id for every block")
    p.set_defaults(fn=cmd_id)
    idsub = p.add_subparsers(dest="action", required=True)
    b = idsub.add_parser("build", help="(re)generate manuscript-index.json, carrying ids forward")
    b.add_argument("--json", action="store_true")
    b.add_argument("--force", action="store_true", help="rewrite even if only the date changed")
    ls = idsub.add_parser("list", help="list block ids with type, span, and preview")
    ls.add_argument("--section", help="restrict to one section id (e.g. chapter9)")
    ls.add_argument("--type", help="restrict to one block type (paragraph, heading, figure, ...)")
    ls.add_argument("--json", action="store_true")
    g = idsub.add_parser("get", help="print a block's current source by id")
    g.add_argument("id")
    g.add_argument("--json", action="store_true")
    rp = idsub.add_parser("replace", help="replace a block's source by id (then rebuild the index)")
    rp.add_argument("id")
    rp.add_argument("--text", help="replacement markdown (inline)")
    rp.add_argument("--file", help="read replacement markdown from a file")
    rp.add_argument("--stdin", action="store_true", help="read replacement markdown from stdin")
    rp.add_argument("--dry-run", action="store_true", help="report the edit without writing")
    vf = idsub.add_parser("verify", help="check ids: unique, in-scheme, spans+hashes valid, full coverage")
    vf.add_argument("--json", action="store_true")
    ss = idsub.add_parser("stress", help="stress-test programmatic editing on a throwaway copy")
    ss.add_argument("--json", action="store_true")

    p = sub.add_parser("flow",
                       help="export every manuscript figure as an upload-ready "
                            "asset pack (Google Flow and friends)")
    p.add_argument("--out", help="output folder (default ~/Desktop/StS-Flow-Assets)")
    p.add_argument("--kinds",
                   help="comma-separated subset of photo,plate,banner,diagram "
                        "(default: all)")
    p.add_argument("--width", type=int, default=FLOW_WIDTH,
                   help=f"raster width for SVG diagrams (default {FLOW_WIDTH})")
    p.add_argument("--dry-run", action="store_true",
                   help="report what would be exported without writing")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_flow)

    p = sub.add_parser("og",
                       help="share cards: no args audits every public page for a "
                            "resolvable og:image; --render rebuilds them from "
                            "scripts/og_cards.json")
    p.add_argument("--render", action="store_true",
                   help="render the cards to static/images/og/ (needs Chrome)")
    p.add_argument("--only", help="comma-separated routes to render, e.g. /blog,/about")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_og)

    p = sub.add_parser("schema",
                       help="check which sql/ migrations have actually reached the "
                            "live Supabase database (exits non-zero if any are pending)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--bundle", action="store_true",
                   help="print the still-pending migrations concatenated in order, "
                        "ready to paste into the Supabase SQL Editor in one go")
    p.set_defaults(fn=cmd_schema)

    p = sub.add_parser("backup",
                       help="dump every Supabase table + storage bucket to a local "
                            "directory (NDJSON + manifest with row counts and hashes)")
    p.add_argument("--out", help=f"backup root (default: {BACKUP_DEFAULT_DIR})")
    p.add_argument("--no-files", action="store_true",
                   help="record storage object names/sizes but do not download them")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_backup)

    p = sub.add_parser("cover",
                       help="keep the website's cover art in sync with the book's; "
                            "--sync regenerates every derivative from the source art")
    p.add_argument("--sync", action="store_true",
                   help="regenerate every site cover derivative from "
                        "art-raw/book-cover-final-source.png")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_cover)

    p = sub.add_parser("art",
                       help="enroll every book figure in art-catalog.json (data-driven)")
    p.set_defaults(fn=cmd_art)
    artsub = p.add_subparsers(dest="action", required=True)
    al = artsub.add_parser("list", help="figure inventory: which are catalogued, which are not")
    al.add_argument("--json", action="store_true")
    asy = artsub.add_parser("sync", help="propose (or --apply) catalog entries for uncatalogued figures")
    asy.add_argument("--apply", action="store_true", help="merge into art-catalog.json + rebuild the index")
    asy.add_argument("--json", action="store_true")
    ac = artsub.add_parser("cut",
                           help="key plate backgrounds to transparency, losslessly "
                                "(exact colour match, never ML matting)")
    ac.add_argument("plates", nargs="*",
                    help="plate PNGs (default: every *-plate.png in art-raw/)")
    ac.add_argument("--out", help="output dir (default art-raw/cut)")
    ac.add_argument("--variant", choices=("content", "figure", "both"),
                    default="both",
                    help="content = figure+frame+caption · figure = largest blob "
                         "(single-subject plates only) · both (default)")
    ac.add_argument("--tol", type=int, default=0,
                    help="L1 tolerance around the background colour "
                         "(default 0 = exact, which is what keeps edges hard)")
    ac.add_argument("--dry-run", action="store_true",
                    help="report without writing")
    ac.add_argument("--json", action="store_true")

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
