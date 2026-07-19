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
import html as html_mod
import json
import re
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

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
