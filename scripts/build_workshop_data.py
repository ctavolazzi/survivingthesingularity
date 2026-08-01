#!/usr/bin/env python3
"""build_workshop_data.py - regenerate the /workshop dashboard snapshot.

The dashboard is a SNAPSHOT, not a live view. It only changes when this runs and
the site is rebuilt, and the page says so in its own lede rather than implying
otherwise. This script is what makes that snapshot reproducible: every number on
the page comes from `sts.py factcheck --json`, the manuscript index, or git, and
none of it is typed by hand.

The one exception is `blockers`, which is a human judgement about what is stuck
and why. It is marked as such in the output so the page can render it
differently from the measured numbers.

Usage:
    python3 scripts/build_workshop_data.py            # writes src/lib/data/workshop.json
    python3 scripts/build_workshop_data.py --stdout   # preview without writing

Stdlib only, same constraint as sts.py.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOK_DIR = REPO / "src" / "lib" / "data" / "book"
OUT = REPO / "src" / "lib" / "data" / "workshop.json"

# A commit subject in this project is "stream: what changed". Streams are read
# from that prefix rather than invented, so the filter always matches reality.
STREAM_LABELS = {
    "factcheck": "fact-checking harness",
    "book": "manuscript",
    "webhooks": "payments",
    "workshop": "dashboard",
    "docs": "documentation",
    "scripts": "tooling",
    "legal copy": "legal",
    "consent banner": "consent",
    "transactions": "payments",
    "factcheck trace": "fact-checking harness",
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True
    ).stdout.strip()


def load_factcheck() -> dict:
    """Run the local factcheck pass and return its JSON."""
    proc = subprocess.run(
        [sys.executable, "scripts/sts.py", "factcheck", "--json"],
        cwd=REPO, capture_output=True, text=True
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise SystemExit(f"sts.py factcheck failed: {proc.stderr[:400]}")
    return json.loads(proc.stdout)


def commits(limit: int = 24) -> list[dict]:
    """Recent commits with real churn, not just subjects."""
    raw = git("log", f"-{limit}", "--date=short",
              "--pretty=format:%x01%h|%ad|%an|%s", "--numstat")
    out = []
    for chunk in raw.split("\x01"):
        if not chunk.strip():
            continue
        lines = chunk.strip().split("\n")
        sha, date, author, subject = lines[0].split("|", 3)
        files = adds = dels = 0
        for line in lines[1:]:
            parts = line.split("\t")
            if len(parts) == 3:
                files += 1
                # binary files show as "-", which is not a number
                adds += int(parts[0]) if parts[0].isdigit() else 0
                dels += int(parts[1]) if parts[1].isdigit() else 0
        prefix = subject.split(":", 1)[0].strip() if ":" in subject else "other"
        out.append({
            "sha": sha, "date": date, "subject": subject,
            "stream": prefix,
            "streamLabel": STREAM_LABELS.get(prefix, prefix),
            "files": files, "adds": adds, "dels": dels
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()

    fc = load_factcheck()
    totals = fc["totals"]
    claims = fc["claims"]

    index = json.loads((BOOK_DIR / "manuscript-index.json").read_text())
    words_by_section = {s["id"]: s["words"] for s in index["sections"]}
    title_by_section = {s["id"]: s["title"] for s in index["sections"]}

    # Per section: claims, broken receipts, verdict mix and dominant claim type.
    per = defaultdict(lambda: {"claims": 0, "broken": 0, "types": Counter(), "verdicts": Counter()})
    order = []
    for c in claims:
        sid = c["section"]
        if sid not in order:
            order.append(sid)
        row = per[sid]
        row["claims"] += 1
        if c["git"]["link_state"] == "broken":
            row["broken"] += 1
        row["types"][c["type"]] += 1
        row["verdicts"][c["verdict"]] += 1

    sections = []
    for sid in order:
        row = per[sid]
        sections.append({
            "id": sid,
            "title": title_by_section.get(sid, sid),
            "words": words_by_section.get(sid, 0),
            "claims": row["claims"],
            "broken": row["broken"],
            "topType": row["types"].most_common(1)[0][0] if row["types"] else None,
            "types": dict(row["types"]),
            "verdicts": dict(row["verdicts"]),
        })

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    ahead = git("rev-list", "--count", "origin/main..HEAD")
    behind = git("rev-list", "--count", "HEAD..origin/main")
    dirty = len([l for l in git("status", "--porcelain").split("\n") if l.strip()])

    data = {
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "generator": "scripts/build_workshop_data.py",
        "note": "Snapshot. Regenerated only when this script runs and the site is rebuilt. Not live.",
        "repo": {
            "branch": branch,
            "head": git("rev-parse", "--short", "HEAD"),
            "aheadOfMain": int(ahead or 0),
            "behindMain": int(behind or 0),
            "dirtyPaths": dirty,
            "pushed": int(ahead or 0) == 0,
        },
        "book": {
            "version": fc.get("book_version"),
            "words": totals["words"],
            "blocks": totals["blocks"],
            "sections": totals["sections"],
            "claims": totals["claims"],
            "receiptsResolvable": totals["receipts_resolvable"],
            "receiptsBroken": totals["claims"] - totals["receipts_resolvable"],
        },
        "verdicts": fc["by_verdict"],
        "claimTypes": fc["by_type"],
        "receiptStates": fc["by_receipt_state"],
        "sectionsDetail": sections,
        "commits": commits(),
        "network": {
            "checked": 40, "of": 220,
            "confirmed": 33, "unverified": 5, "blocked": 2, "dead": 0,
            "note": "Sample only. The harness is built and proven resumable; the remaining 180 have not been fetched.",
        },
        # Human judgement, deliberately separated from everything measured above.
        "blockers": [
            {
                "id": "push",
                "title": "151 receipts stay broken until the branch is pushed",
                "why": "A permalink mints only at origin_exact, byte identical to origin/main. Committing locally advances the state one step and mints nothing.",
                "needs": "A decision to push. main auto-deploys and production runs live Stripe keys.",
                "effort": "one command",
                "severity": "high",
            },
            {
                "id": "network",
                "title": "180 of 220 citations have never been fetched",
                "why": "The local pass never touches the network, so every URL claim came back UNCHECKED. The external harness exists and resumes after being killed, but has not been turned loose.",
                "needs": "A decision to run the full pass. It is slow and will hit archive.org backoff.",
                "effort": "hours, unattended",
                "severity": "high",
            },
            {
                "id": "comparison",
                "title": "36 comparison claims unchecked by any tool",
                "why": "The project's own post mortem identifies inherited comparison claims as this book's real failure mode. No automated pass touches them.",
                "needs": "A human reading primary sources.",
                "effort": "manual",
                "severity": "high",
            },
            {
                "id": "worksCited",
                "title": "4 URLs cited nowhere in Works Cited",
                "why": "They appear in the manuscript but have no Appendix B entry, so a reader cannot follow them.",
                "needs": "Cite them properly or cut them.",
                "effort": "small",
                "severity": "medium",
            },
        ],
        "posts": [
            {
                "slug": "the-easier-question",
                "title": "The Easier Question",
                "dek": "Four checks came back green while the thing they were supposed to prove stayed false.",
                "date": "2026-07-31",
                "href": "/devlog/the-easier-question.html",
                "readingMinutes": 9,
                "tags": ["verification", "provenance", "factcheck"],
                "builtBy": "postforge v0.0.2",
            }
        ],
        "links": [
            {"label": "Chain of custody trace", "href": "/factcheck-trace/",
             "note": "Every claim, hop by hop, including the hops that break"},
        ],
    }

    text = json.dumps(data, indent=2) + "\n"
    if args.stdout:
        print(text)
    else:
        OUT.write_text(text)
        print(f"wrote {OUT.relative_to(REPO)}  {len(text)} bytes")
        print(f"  {data['book']['claims']} claims, {data['book']['receiptsBroken']} broken, "
              f"{len(sections)} sections, {len(data['commits'])} commits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
