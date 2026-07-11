#!/usr/bin/env python3
"""
sts.py — Surviving the Singularity project API.

One tool to inspect, audit, and report on the book and the website.
Stdlib only. Run from anywhere; it finds the repo root on its own.

Commands:
    status    One-screen dashboard: git, book, audit errors, stripe, live drift
    audit     Full site audit: routes, links, assets, meta, sitemap, placeholders
    book      Book manuscript stats: per-chapter word counts, thin chapters
    stripe    Stripe go-live readiness (masks all secrets)
    live      Probe production and compare against local routes (deploy drift)
    sitemap   Check sitemap.xml against real routes; --write regenerates it
    routes    List every route the site actually serves

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
import json
import re
import subprocess
import sys
import urllib.error
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

    p = sub.add_parser("sitemap")
    p.add_argument("--json", action="store_true")
    p.add_argument("--write", action="store_true",
                   help="regenerate static/sitemap.xml from the real route table")
    p.set_defaults(fn=cmd_sitemap)

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
