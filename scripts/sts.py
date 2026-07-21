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
    stripe    Stripe go-live readiness (masks all secrets)
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
    art       Enroll every book figure in art-catalog.json (list|sync).
              Data-driven from the manuscript index + credits.json; ids are
              sts.<kind>.<filename-stem> so new art auto-enrolls.

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
import hashlib
import html as html_mod
import json
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

    # 3. Per-page head meta
    for marker in ROUTES_DIR.rglob("+page.svelte"):
        rel = str(marker.relative_to(ROOT))
        text = marker.read_text(encoding="utf-8")
        head = re.search(r"<svelte:head>(.*?)</svelte:head>", text, re.DOTALL)
        if not head:
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


def public_pages(pages: list) -> list:
    """Pages that belong in the sitemap (skip utility/dynamic/transactional)."""
    skip = {"/unsubscribe", "/early-access/success"}
    return [p for p in pages if "[" not in p and p not in skip]


def check_sitemap(pages: list):
    errors, missing = [], []
    listed = {u.replace(SITE, "") or "/" for u in sitemap_urls()}
    real = set(public_pages(pages))
    for ghost in sorted(listed - real):
        errors.append(f"sitemap.xml lists {ghost} but no such route exists (404 to crawlers)")
    for m in sorted(real - listed):
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


def cmd_stripe(args) -> int:
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
    ahead = git("rev-list", "--count", "main..HEAD") or "?"
    book = book_stats()
    stripe = stripe_state()
    pages = collect_routes()["pages"]
    sm_errors, sm_missing = check_sitemap(pages)
    status = {
        "git": {"branch": branch, "dirty_paths": dirty, "ahead_of_main": ahead},
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
    print(f"  git:     {branch} · {dirty} dirty paths · {ahead} ahead of main")
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
    for s in meta["sections"]:
        body = (BOOK_DIR / s["file"]).read_text(encoding="utf-8").strip()
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
    Returns the list of old ids that vanished (tombstones).
    """
    from collections import defaultdict, deque
    exact = defaultdict(deque)
    for ob in old_blocks:
        exact[(ob["type"], ob.get("level", 0), ob["hash"])].append(ob)
    used = set()
    for nb in new_blocks:
        dq = exact.get((nb["type"], nb["level"], nb["hash"]))
        if dq:
            ob = dq.popleft()
            nb["id"] = ob["id"]
            used.add(ob["id"])
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
    return [ob["id"] for ob in old_blocks if ob["id"] not in used]


def _build_index(book_dir, old_index=None):
    """Parse every section into addressed blocks, reconciling ids with old_index."""
    book = json.loads((book_dir / "book.json").read_text(encoding="utf-8"))
    figmap = _art_figure_map(book_dir)
    old_secs = {s["id"]: s for s in (old_index or {}).get("sections", [])}
    sections_out, total_blocks, total_words = [], 0, 0
    for s in book["sections"]:
        sid = s["id"]
        lines = (book_dir / s["file"]).read_text(encoding="utf-8").split("\n")
        blocks = _md_blocks(lines)
        for b in blocks:
            b["hash"] = _block_hash(b["type"], b["level"], b["text"])
        old = old_secs.get(sid, {})
        tombstones = _reconcile(old.get("blocks", []), blocks)
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
            "sections": sections_out}


def _index_path(book_dir):
    return book_dir / INDEX_NAME


def _load_index(book_dir):
    p = _index_path(book_dir)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _strip_gen(ix):
    return {k: v for k, v in ix.items() if k != "generated"}


def _write_index(book_dir, index, force=False):
    """Write the index. No-op (returns False) when nothing but the date changed."""
    old = _load_index(book_dir)
    if old and not force and _strip_gen(old) == _strip_gen(index):
        return False
    index = dict(index)
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
    if args.json:
        print(json.dumps({"changed": changed, "totals": t, "tombstones": tomb}, indent=2))
    else:
        print(f"manuscript-index: {t['blocks']} blocks · {t['sections']} sections · "
              f"{t['words']:,} words" + ("" if changed else " (unchanged)"))
        if tomb:
            print(f"  {tomb} tombstoned id(s) retained for audit")
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


def cmd_art(args):
    return {"list": _art_list, "sync": _art_sync}[args.action](args)


def main():
    ap = argparse.ArgumentParser(prog="sts.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name, fn in (("status", cmd_status), ("audit", cmd_audit),
                     ("stripe", cmd_stripe), ("live", cmd_live),
                     ("routes", cmd_routes)):
        p = sub.add_parser(name)
        p.add_argument("--json", action="store_true")
        p.set_defaults(fn=fn)

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

    p = sub.add_parser("art",
                       help="enroll every book figure in art-catalog.json (data-driven)")
    p.set_defaults(fn=cmd_art)
    artsub = p.add_subparsers(dest="action", required=True)
    al = artsub.add_parser("list", help="figure inventory: which are catalogued, which are not")
    al.add_argument("--json", action="store_true")
    asy = artsub.add_parser("sync", help="propose (or --apply) catalog entries for uncatalogued figures")
    asy.add_argument("--apply", action="store_true", help="merge into art-catalog.json + rebuild the index")
    asy.add_argument("--json", action="store_true")

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
