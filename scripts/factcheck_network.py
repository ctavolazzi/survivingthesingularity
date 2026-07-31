#!/usr/bin/env python3
"""factcheck_network.py - the external half of the factcheck audit.

`sts.py factcheck` resolves every claim back to the commit that wrote it, but it
never leaves the machine, so all 227 URL claims come back UNCHECKED and the
source_state and archive hops are broken by construction. This module does the
network half.

WHY THIS IS NOT `sts.py verify --links`. That verb already does liveness well
and is deliberately reused here, not rewritten: its 404-versus-403 judgement is
correct and hard won. But it answers a weaker question. It asks "did the host
answer 200", and a 200 is not a live source. Soft 404s, parked domains, consent
walls, paywalls and login interstitials all answer 200 with a page that does not
contain the cited work at all. Confirming those as good citations would be a
hollow check, and a hollow check is worse than no check, because it launders an
unverified bibliography into a verified-looking one.

So every fetch here is also asked: is the cited work actually ON this page?
The citation's own title, from Appendix B, is the probe. The result records the
matched token fraction rather than a bare boolean, so a human can audit the
judgement instead of trusting it.

WHAT IS DELIBERATELY NOT CLAIMED. A PDF is fetched and its liveness judged, but
its text is not parsed (stdlib only, no PDF dependency), so it is reported as
LIVE_UNVERIFIED and never as confirmed. Same for any 200 whose body is not HTML.
The point of this tool is to be honest about which citations remain unproven.

RESUMABILITY IS THE POINT. archive.org and several publishers throttle hard, so
a pass that cannot resume will never finish. Every response is cached to disk
keyed by URL, and a re-run skips anything already cached. Kill it and restart it
freely.

Usage:
    python3 scripts/factcheck_network.py --limit 20        # sample run
    python3 scripts/factcheck_network.py                   # full pass, resumable
    python3 scripts/factcheck_network.py --json            # machine-readable
    python3 scripts/factcheck_network.py --refresh         # ignore cache
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

VERSION = "0.0.1"

REPO = Path(__file__).resolve().parent.parent
BOOK_DIR = REPO / "src" / "lib" / "data" / "book"
APPENDIX_B = BOOK_DIR / "23-appendix-b.md"
CACHE_DIR = REPO / ".factcheck-cache"

# Match the browser-ish agent sts.py already uses. Publishers that refuse this
# refuse every automated client, which is a fact about them and not about the
# citation.
UA = "Mozilla/5.0 (compatible; sts.py link check)"

# A 200 carrying any of these, with little else, is a soft 404 or a wall rather
# than the cited work. Checked against visible text, not raw markup.
SOFT_404_MARKERS = (
    "page not found",
    "404 not found",
    "the page you requested could not be found",
    "this page does not exist",
    "no longer available",
    "content not found",
    "sorry, we can't find",
    "domain is for sale",
    "buy this domain",
    "parked domain",
)

WALL_MARKERS = (
    "enable javascript",
    "please enable cookies",
    "verify you are a human",
    "checking your browser",
    "captcha",
    "access denied",
    "subscribe to continue",
    "subscribers only",
    "sign in to continue",
    "create a free account to continue",
    "consent to the use of cookies",
)

# Words too common to prove a page carries a specific cited work.
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "for", "to", "with", "from",
    "by", "at", "as", "is", "are", "was", "were", "be", "this", "that", "it",
    "its", "how", "what", "why", "who", "when", "not", "no", "pdf", "review",
    "using", "via", "new", "our", "we", "you", "your", "about", "into", "over",
    "more", "most", "can", "will", "has", "have", "had", "but", "all", "one",
}


# ---------------------------------------------------------------- citations


def parse_appendix_b() -> list[dict]:
    """Pull (number, title, url) out of the Works Cited list.

    Entries look like `12. Some Title - Publisher, https://host/path`, and the
    file packs many of them onto a single line, so this splits on the numbering
    rather than on newlines.
    """
    if not APPENDIX_B.exists():
        return []
    text = APPENDIX_B.read_text(encoding="utf-8")

    # Split ahead of `<n>. ` so each chunk holds exactly one citation.
    chunks = re.split(r"(?m)(?=\b\d{1,3}\.\s)", text)
    out, seen = [], set()
    for chunk in chunks:
        m = re.match(r"\s*(\d{1,3})\.\s+(.*)", chunk, re.S)
        if not m:
            continue
        number, body = int(m.group(1)), m.group(2)
        urls = re.findall(r"https?://[^\s)>\]\"']+", body)
        if not urls:
            continue
        url = urls[0].rstrip(".,;")
        # The title is everything before the URL, minus the trailing publisher.
        title = body[: body.index(urls[0])].strip().rstrip(",").strip()
        if url in seen:
            continue
        seen.add(url)
        out.append({"n": number, "title": title, "url": url})
    return out


def title_tokens(title: str) -> list[str]:
    """Distinctive lowercase words from a citation title."""
    words = re.findall(r"[A-Za-z0-9']{3,}", title.lower())
    return [w for w in words if w not in STOPWORDS]


# ---------------------------------------------------------------- fetching


def cache_path(url: str) -> Path:
    return CACHE_DIR / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".json")


def load_cached(url: str) -> dict | None:
    p = cache_path(url)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None  # a truncated cache entry is a cache miss, not a crash


def save_cached(url: str, record: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = cache_path(url).with_suffix(".tmp")
    tmp.write_text(json.dumps(record, indent=2), encoding="utf-8")
    tmp.replace(cache_path(url))  # atomic, so a kill cannot leave half a file


def fetch(url: str, timeout: float = 15.0, attempts: int = 3) -> dict:
    """GET a URL and return status, final url, content type and body text.

    Mirrors sts.py's _probe_url retry discipline, because hammering a couple of
    hundred hosts in a row provokes throttling that looks exactly like a dead
    link. GET rather than HEAD, since the body is the whole point here.
    """
    reason = ""
    for attempt in range(attempts):
        req = urllib.request.Request(
            url, method="GET", headers={"User-Agent": UA, "Accept": "*/*"}
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read(400_000)  # enough to judge content, bounded on disk
                ctype = r.headers.get("Content-Type", "")
                charset = r.headers.get_content_charset() or "utf-8"
                body = raw.decode(charset, errors="replace")
                return {
                    "status": r.status,
                    "final_url": r.geturl(),
                    "content_type": ctype,
                    "body": body,
                    "reason": "",
                }
        except urllib.error.HTTPError as e:
            return {
                "status": e.code,
                "final_url": url,
                "content_type": e.headers.get("Content-Type", "") if e.headers else "",
                "body": "",
                "reason": f"HTTP {e.code}",
            }
        except urllib.error.URLError as e:
            reason = str(getattr(e, "reason", e))[:90]
        except Exception as e:
            reason = f"{type(e).__name__}: {e}"[:90]
        if attempt < attempts - 1:
            time.sleep(1.5 * (attempt + 1))
    return {
        "status": 0,
        "final_url": url,
        "content_type": "",
        "body": "",
        "reason": reason or "no response after retries",
    }


def visible_text(body: str) -> str:
    """Strip markup so marker and token matching sees what a reader sees."""
    body = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body)).strip().lower()


# ---------------------------------------------------------------- verdicts


def classify(citation: dict, resp: dict) -> dict:
    """Turn one response into an auditable verdict.

    The ordering matters: a host that refused us is never called dead, and a 200
    is never called confirmed until the cited work is actually found on the page.
    """
    status = resp["status"]
    url = citation["url"]

    if status in (404, 410):
        return {"state": "DEAD", "detail": f"HTTP {status}", "match": None}
    if status in (401, 403, 429):
        return {
            "state": "BLOCKED",
            "detail": f"HTTP {status}, host refused an automated request. "
                      "Not evidence the source is gone.",
            "match": None,
        }
    if status == 0:
        return {"state": "UNREACHABLE", "detail": resp["reason"], "match": None}
    if status >= 500:
        return {"state": "SERVER_ERROR", "detail": f"HTTP {status}", "match": None}
    if status != 200:
        return {"state": "OTHER", "detail": f"HTTP {status}", "match": None}

    ctype = (resp.get("content_type") or "").lower()
    text = visible_text(resp.get("body") or "")

    # Non-HTML (PDF above all) is live, but its text is not parsed here, so it
    # must not be reported as confirmed. Saying so is the honest answer.
    if "html" not in ctype:
        kind = "PDF" if "pdf" in ctype else (ctype.split(";")[0] or "unknown type")
        return {
            "state": "LIVE_UNVERIFIED",
            "detail": f"200, {kind}. Body not parsed, so the cited content is unconfirmed.",
            "match": None,
        }

    for marker in SOFT_404_MARKERS:
        if marker in text:
            return {
                "state": "SOFT_404",
                "detail": f"200 but the page reads as missing: '{marker}'",
                "match": None,
            }

    tokens = title_tokens(citation["title"])
    hits = [t for t in tokens if t in text]
    frac = (len(hits) / len(tokens)) if tokens else 0.0
    match = {"matched": len(hits), "of": len(tokens), "fraction": round(frac, 2)}

    # A wall only matters when the cited work is also absent. Many real articles
    # carry a cookie banner and the full text underneath it.
    if frac < 0.5:
        for marker in WALL_MARKERS:
            if marker in text:
                return {
                    "state": "WALLED",
                    "detail": f"200 but gated ('{marker}') and the cited title is not on the page",
                    "match": match,
                }

    if not tokens:
        return {"state": "LIVE_UNVERIFIED", "detail": "no distinctive title to match on", "match": match}
    if frac >= 0.5:
        return {"state": "LIVE_CONFIRMED",
                "detail": f"200 and {len(hits)} of {len(tokens)} title words are on the page",
                "match": match}
    return {"state": "LIVE_UNCONFIRMED",
            "detail": f"200 but only {len(hits)} of {len(tokens)} title words are on the page. "
                      "Could be a redirect to a section front, a wall, or a moved article.",
            "match": match}


# ---------------------------------------------------------------- driver


def run(limit: int | None, refresh: bool, delay: float, only: str | None) -> dict:
    citations = parse_appendix_b()
    if only:
        citations = [c for c in citations if only in c["url"]]
    if limit:
        citations = citations[:limit]

    results, fetched, from_cache = [], 0, 0
    for i, c in enumerate(citations, 1):
        cached = None if refresh else load_cached(c["url"])
        if cached:
            from_cache += 1
            record = cached
        else:
            resp = fetch(c["url"])
            verdict = classify(c, resp)
            record = {
                "n": c["n"],
                "title": c["title"],
                "url": c["url"],
                "status": resp["status"],
                "final_url": resp["final_url"],
                "content_type": resp["content_type"],
                "state": verdict["state"],
                "detail": verdict["detail"],
                "match": verdict["match"],
                "checked_with": f"factcheck_network.py v{VERSION}",
            }
            save_cached(c["url"], record)
            fetched += 1
            if delay:
                time.sleep(delay)
        results.append(record)
        if sys.stderr.isatty():
            print(f"  [{i}/{len(citations)}] {record['state']:<17} {record['url'][:70]}",
                  file=sys.stderr)

    return {
        "checked": len(results),
        "fetched": fetched,
        "from_cache": from_cache,
        "by_state": dict(Counter(r["state"] for r in results)),
        "results": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, help="check only the first N citations")
    ap.add_argument("--only", help="only URLs containing this substring")
    ap.add_argument("--refresh", action="store_true", help="ignore the disk cache")
    ap.add_argument("--delay", type=float, default=1.0,
                    help="seconds between live fetches (default 1.0)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    report = run(args.limit, args.refresh, args.delay, args.only)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"\nfactcheck network  {report['checked']} citation(s) "
          f"({report['fetched']} fetched, {report['from_cache']} from cache)\n")

    order = ["LIVE_CONFIRMED", "LIVE_UNVERIFIED", "LIVE_UNCONFIRMED", "WALLED",
             "SOFT_404", "BLOCKED", "SERVER_ERROR", "UNREACHABLE", "DEAD", "OTHER"]
    for state in order:
        n = report["by_state"].get(state)
        if n:
            print(f"    {state:<18} {n:>4}")

    problems = [r for r in report["results"]
                if r["state"] in ("DEAD", "SOFT_404", "UNREACHABLE", "SERVER_ERROR")]
    if problems:
        print("\n  needs a human:")
        for r in problems:
            print(f"    [{r['n']}] {r['state']}  {r['url']}")
            print(f"         {r['detail']}")

    print("\n  Cache: .factcheck-cache/. Re-running skips what is already there,")
    print("  so this pass is resumable. Nothing here is a claim about a source")
    print("  the tool did not actually read: PDFs and non-HTML come back")
    print("  LIVE_UNVERIFIED on purpose.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
