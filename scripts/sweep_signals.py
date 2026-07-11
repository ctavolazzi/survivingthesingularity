#!/usr/bin/env python3
"""
sweep_signals.py — arXiv sweep for Surviving the Singularity.

Fetches recent preprints in AI/robotics/agents categories, ranks them by
recency-weighted keyword relevance, applies quality gates, and writes:

  src/lib/data/signals.json   — SSR import for SvelteKit
  static/signals.json         — public JSON for external consumers
  static/signals.xml          — RSS 2.0 feed

No API key required. No third-party deps. Pure stdlib.

Usage:
  python3 scripts/sweep_signals.py           # full sweep, all defaults
  python3 scripts/sweep_signals.py --dry-run # fetch + score, don't write files
  python3 scripts/sweep_signals.py --days 14 # wider lookback window
"""

import argparse
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITE_ROOT = Path(__file__).parent.parent  # project root

CATEGORIES = [
    "cs.AI",   # Artificial Intelligence
    "cs.LG",   # Machine Learning
    "cs.CL",   # Computation and Language
    "cs.MA",   # Multiagent Systems
    "cs.RO",   # Robotics
]

KEYWORDS = {
    # Core AGI / singularity terms (high weight)
    "agi": 5,
    "artificial general intelligence": 5,
    "superintelligence": 5,
    "recursive self-improvement": 5,
    "self-improving": 4,
    "self-replication": 4,
    "takeoff": 4,
    "intelligence explosion": 5,
    "existential risk": 4,
    "x-risk": 4,
    "world model": 4,
    "foundation model": 3,
    # Agentic / autonomous systems (high weight)
    "agent": 3,
    "multi-agent": 4,
    "agentic": 4,
    "autonomous": 3,
    "autonomy": 3,
    "cognitive architecture": 4,
    "tool use": 3,
    "tool-use": 3,
    "planning": 2,
    "reasoning": 3,
    "chain of thought": 2,
    "chain-of-thought": 2,
    # Alignment / safety (high weight)
    "alignment": 4,
    "ai safety": 4,
    "rlhf": 3,
    "reward hacking": 3,
    "value alignment": 4,
    "corrigibility": 4,
    "deceptive": 3,
    "interpretability": 3,
    "interpret": 2,
    # Embodiment / robotics
    "embodied": 3,
    "humanoid": 3,
    "robot": 2,
    "robotics": 2,
    "physical ai": 3,
    # LLM / capability
    "llm": 3,
    "language model": 3,
    "emergent": 2,
    "emergent capabilit": 3,
    "scaling": 2,
    "in-context learning": 2,
    "retrieval": 2,
    "rag": 2,
    # Economic / societal
    "automation": 2,
    "labor displacement": 3,
    "economic impact": 2,
    "job": 1,
}

STRONG_WEIGHT_THRESHOLD = 3   # a keyword must have weight >= this to count as "strong"
MIN_KEYWORD_SCORE = 4          # raw keyword score before recency weighting
DAYS_DEFAULT = 7               # lookback window for fresh items
RECENCY_HALF_LIFE_DAYS = 7     # score halves every N days
WINDOW_DAYS = 30               # items older than this are dropped on merge
MAX_ITEMS = 60                 # cap after merge + sort
PER_CAT_RESULTS = 50           # max results fetched per category from arXiv
REQUEST_DELAY_S = 3            # courtesy delay between arXiv category requests
ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "survivingthesingularity-signals/1.0 (survivingthesingularity.com)"

DENYLIST_PATH = Path(__file__).parent / "signals_denylist.txt"
OUTPUT_SSR = SITE_ROOT / "src" / "lib" / "data" / "signals.json"
OUTPUT_STATIC_JSON = SITE_ROOT / "static" / "signals.json"
OUTPUT_RSS = SITE_ROOT / "static" / "signals.xml"

TAG_MAP = {
    "cs.RO": "Robotics",
    "cs.MA": "Agents",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _strip_version(arxiv_id: str) -> str:
    """'2406.12345v2' -> '2406.12345'"""
    if "v" in arxiv_id:
        return arxiv_id.rsplit("v", 1)[0]
    return arxiv_id


def _recency_decay(published_at: str, half_life: float = RECENCY_HALF_LIFE_DAYS) -> float:
    """Exponential decay: score *= 2^(-age/half_life). Returns multiplier 0..1."""
    try:
        pub = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        age_days = (datetime.now(timezone.utc) - pub).days
        return math.pow(2.0, -max(0, age_days) / half_life)
    except Exception:
        return 0.5


def _score_item(item: dict) -> tuple:
    """Return (raw_score, final_score, matched_keywords, has_strong_match)."""
    text = (item.get("title", "") + " " + item.get("summary", "")).lower()
    matched = []
    raw = 0
    has_strong = False
    for kw, weight in KEYWORDS.items():
        if kw.lower() in text:
            raw += weight
            matched.append(kw)
            if weight >= STRONG_WEIGHT_THRESHOLD:
                has_strong = True
    decay = _recency_decay(item.get("published_at", ""))
    final = round(raw * decay, 2)
    return raw, final, matched, has_strong


def _derive_tag(category: str) -> str:
    return TAG_MAP.get(category, "Research")


def _load_denylist() -> set:
    if DENYLIST_PATH.exists():
        lines = DENYLIST_PATH.read_text().splitlines()
        return {l.strip() for l in lines if l.strip() and not l.startswith("#")}
    return set()

# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_category(cat: str, days: int, max_results: int) -> list:
    """Fetch one arXiv category. Returns list of normalized item dicts."""
    start_dt = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y%m%d")
    end_dt = datetime.now(timezone.utc).strftime("%Y%m%d")
    query = f"cat:{cat} AND submittedDate:[{start_dt}000000 TO {end_dt}235959]"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = ARXIV_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            xml = r.read().decode("utf-8")
    except Exception as e:
        print(f"  [warn] fetch failed for {cat}: {e}", file=sys.stderr)
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        print(f"  [warn] XML parse error for {cat}: {e}", file=sys.stderr)
        return []

    items = []
    for entry in root.findall("atom:entry", ns):
        raw_id = entry.findtext("atom:id", namespaces=ns) or ""
        paper_id = raw_id.split("/abs/")[-1] if "/abs/" in raw_id else raw_id
        paper_id = _strip_version(paper_id)

        authors_el = entry.findall("atom:author", ns)
        authors = [a.findtext("atom:name", namespaces=ns) or "?" for a in authors_el]

        published = entry.findtext("atom:published", namespaces=ns) or ""
        pub_date = published[:10] if published else ""  # YYYY-MM-DD

        items.append({
            "id": paper_id,
            "source": "arxiv",
            "title": (entry.findtext("atom:title", namespaces=ns) or "").strip().replace("\n", " "),
            "url": f"https://arxiv.org/abs/{paper_id}",
            "authors": authors[:4],
            "summary": (entry.findtext("atom:summary", namespaces=ns) or "").strip()[:600],
            "category": cat,
            "tag": _derive_tag(cat),
            "published_at": pub_date,
        })
    return items


def fetch_all(days: int = DAYS_DEFAULT) -> list:
    """Fetch all categories with courtesy delay. Returns deduped list."""
    all_items = []
    for i, cat in enumerate(CATEGORIES):
        if i > 0:
            time.sleep(REQUEST_DELAY_S)
        print(f"  fetching {cat}...", end=" ", flush=True)
        items = fetch_category(cat, days, PER_CAT_RESULTS)
        print(f"{len(items)} papers")
        all_items.extend(items)

    # Dedup by id, keeping first occurrence (most recent category sort)
    seen = set()
    unique = []
    for item in all_items:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique.append(item)
    return unique

# ---------------------------------------------------------------------------
# Score + gate
# ---------------------------------------------------------------------------

def score_and_gate(items: list, denylist: set) -> list:
    """Score items, apply quality gates, return gated list sorted by final score."""
    results = []
    for item in items:
        if item["id"] in denylist:
            continue
        raw, final, matched, has_strong = _score_item(item)
        if raw < MIN_KEYWORD_SCORE or not has_strong:
            continue
        item["score"] = final
        item["raw_score"] = raw
        item["matched_keywords"] = matched
        results.append(item)
    results.sort(key=lambda x: (x["score"], x["published_at"]), reverse=True)
    return results

# ---------------------------------------------------------------------------
# Merge + window
# ---------------------------------------------------------------------------

def merge_with_existing(new_items: list) -> list:
    """Union with existing signals.json, apply 30-day window, cap at MAX_ITEMS."""
    existing = []
    if OUTPUT_SSR.exists():
        try:
            data = json.loads(OUTPUT_SSR.read_text())
            existing = data.get("items", [])
        except Exception:
            pass

    by_id = {item["id"]: item for item in existing}
    for item in new_items:
        by_id[item["id"]] = item  # new items overwrite (fresher scores)

    cutoff = (datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%d")
    windowed = [item for item in by_id.values()
                if item.get("published_at", "") >= cutoff]
    windowed.sort(key=lambda x: (x.get("score", 0), x.get("published_at", "")), reverse=True)
    return windowed[:MAX_ITEMS]

# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_json(items: list, generated_at: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": generated_at,
        "source": "arxiv",
        "item_count": len(items),
        "items": items,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def write_rss(items: list, generated_at: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    now_rfc = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        '    <title>Surviving the Singularity — Research Signals</title>',
        '    <link>https://survivingthesingularity.com/signals</link>',
        '    <description>Algorithmically swept arXiv research ranked by singularity relevance. Not human-curated.</description>',
        '    <language>en-us</language>',
        f'   <lastBuildDate>{now_rfc}</lastBuildDate>',
        '    <atom:link href="https://survivingthesingularity.com/signals.xml" rel="self" type="application/rss+xml"/>',
    ]
    for item in items[:30]:  # RSS cap at 30 for reader compat
        pub = item.get("published_at", "")
        try:
            pub_rfc = datetime.strptime(pub, "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000")
        except ValueError:
            pub_rfc = now_rfc
        authors_str = ", ".join(item.get("authors", [])[:2])
        if len(item.get("authors", [])) > 2:
            authors_str += ", et al."
        kws = ", ".join(item.get("matched_keywords", [])[:5])
        desc = (
            f"{item.get('summary', '')[:300]}... "
            f"[Score: {item.get('score', 0)} | Flagged for: {kws}] "
            f"Authors: {authors_str}"
        )
        title = item.get("title", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        desc = desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        url = item.get("url", "")
        lines += [
            "    <item>",
            f"      <title>{title}</title>",
            f"      <link>{url}</link>",
            f"      <guid isPermaLink=\"true\">{url}</guid>",
            f"      <pubDate>{pub_rfc}</pubDate>",
            f"      <description>{desc}</description>",
            "    </item>",
        ]
    lines += ["  </channel>", "</rss>"]
    path.write_text("\n".join(lines), encoding="utf-8")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sweep arXiv for singularity-relevant research.")
    parser.add_argument("--days", type=int, default=DAYS_DEFAULT, help="Lookback window in days")
    parser.add_argument("--dry-run", action="store_true", help="Score and print, don't write files")
    args = parser.parse_args()

    print(f"[sweep] Starting signals sweep — {args.days}d lookback")
    denylist = _load_denylist()
    if denylist:
        print(f"[sweep] Denylist: {len(denylist)} ids blocked")

    print("[sweep] Fetching arXiv categories...")
    raw = fetch_all(days=args.days)
    print(f"[sweep] Fetched {len(raw)} unique papers")

    gated = score_and_gate(raw, denylist)
    print(f"[sweep] {len(gated)} passed quality gates (min_score={MIN_KEYWORD_SCORE}, strong_kw required)")

    if not gated:
        print("[sweep] No items passed gates — nothing to write. Check lookback window or gates.")
        sys.exit(0)

    merged = merge_with_existing(gated)
    # Apply denylist to merged set too — catches items carried over from existing JSON
    if denylist:
        merged = [it for it in merged if it["id"] not in denylist]
    print(f"[sweep] {len(merged)} items after merge+window+cap")

    if args.dry_run:
        print("\n[dry-run] Top 5 items:")
        for item in merged[:5]:
            print(f"  [{item['score']:.1f}] {item['title'][:80]}...")
            print(f"         matched: {', '.join(item['matched_keywords'][:4])}")
        print("[dry-run] No files written.")
        return

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    write_json(merged, generated_at, OUTPUT_SSR)
    write_json(merged, generated_at, OUTPUT_STATIC_JSON)
    write_rss(merged, generated_at, OUTPUT_RSS)

    print(f"[sweep] Done. Wrote {len(merged)} items to:")
    print(f"  {OUTPUT_SSR}")
    print(f"  {OUTPUT_STATIC_JSON}")
    print(f"  {OUTPUT_RSS}")


if __name__ == "__main__":
    main()
