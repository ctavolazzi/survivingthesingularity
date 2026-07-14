#!/usr/bin/env python3
"""Sweep the local machine (and optionally merged Google Drive results) for every
file that pertains to the Surviving the Singularity book, and write a manifest.

Local search = Spotlight content search (mdfind) + filename scan (find) over the
home directory, minus noise dirs (node_modules, .git, caches, Library, etc.).

Google Drive cannot be queried from a local script without OAuth credentials, so
Drive results are merged in from a JSON file produced by the Claude Drive
connector (or any other export) with:  --drive-json <path>
Expected shape: [{"name": ..., "id": ..., "mimeType": ..., "modifiedTime": ..., "url": ...}, ...]

Usage:
  python3 scripts/find_book_sources.py                        # local only
  python3 scripts/find_book_sources.py --drive-json drive.json
  python3 scripts/find_book_sources.py --out manuscript/SOURCE-MANIFEST.md
"""

import argparse
import json
import os
import subprocess
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

HOME = Path.home()

# Distinctive book vocabulary. Deliberately skewed toward phrases unique to the
# manuscript so a hit means "this is book material," not "this mentions AI."
CONTENT_PHRASES = [
    "surviving the singularity",
    "shouse protocol",
    "machine exodus",
    "municipal autonomy code",
    "sovereign municipal code",
    "premortem pivot",
    "egalitarian pivot",
    "relational autonomy",
    "create over consume",
    "neighborhood factory",
    "the land strategy",
    "thermodynamics of survival",
    "welcome to the weirdness",
    "uncompromising truth",
    "2027 tipping point",
    "abundance quotient",
    "local biological hub",
    "9 stages of the singularity",
    "nine stages of the singularity",
    "collapse of the long tail",
    "reclaiming soil",
]

# Filename fragments (case-insensitive) worth flagging even without content hits.
FILENAME_FRAGMENTS = [
    "surviving-the-singularity",
    "surviving_the_singularity",
    "survivingthesingularity",
    "sts-",
    "singularity",
    "shouse",
]

EXCLUDE_DIR_PARTS = {
    "node_modules", ".git", ".svelte-kit", "__pycache__", ".venv", "venv",
    ".cache", "Library", ".Trash", ".npm", ".pyenv", "dist", "build",
    ".next", "test-results", "tests/results", "book-build",
}

DOC_EXTENSIONS = {
    ".md", ".txt", ".pdf", ".docx", ".doc", ".epub", ".rtf", ".pages",
    ".odt", ".html", ".json", ".js", ".svelte", ".tex", ".gdoc",
}


def excluded(path: str) -> bool:
    parts = set(Path(path).parts)
    return bool(parts & EXCLUDE_DIR_PARTS)


def mdfind(phrase: str) -> list[str]:
    """Spotlight content search, scoped to the home directory."""
    try:
        out = subprocess.run(
            ["mdfind", "-onlyin", str(HOME), phrase],
            capture_output=True, text=True, timeout=60,
        ).stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []
    return [line for line in out.splitlines() if line.strip()]


def filename_scan() -> list[str]:
    """Find files whose *names* look book-related, regardless of content."""
    hits: list[str] = []
    for frag in FILENAME_FRAGMENTS:
        try:
            out = subprocess.run(
                ["mdfind", "-onlyin", str(HOME), f"kMDItemFSName == '*{frag}*'c"],
                capture_output=True, text=True, timeout=60,
            ).stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
        hits.extend(line for line in out.splitlines() if line.strip())
    return hits


def classify(path: str) -> str:
    p = path.lower()
    if "/manuscript/" in p or "book-build" in p:
        return "manuscript"
    if "/src/lib/data/book/" in p:
        return "canonical chapter source"
    if p.endswith((".pdf", ".epub", ".docx", ".doc", ".pages", ".gdoc")):
        return "document"
    if p.endswith((".md", ".txt", ".rtf", ".odt", ".tex")):
        return "notes/text"
    if p.endswith((".js", ".svelte", ".json", ".html")):
        return "site/code"
    return "other"


def gather_local() -> "OrderedDict[str, dict]":
    found: "OrderedDict[str, dict]" = OrderedDict()

    def add(path: str, reason: str):
        if excluded(path) or not os.path.isfile(path):
            return
        if Path(path).name == "SOURCE-MANIFEST.md":
            return
        ext = Path(path).suffix.lower()
        if ext and ext not in DOC_EXTENSIONS and "manuscript" not in path.lower():
            return
        entry = found.setdefault(path, {
            "path": path,
            "reasons": [],
            "kind": classify(path),
            "modified": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(timespec="seconds"),
            "size_kb": round(os.path.getsize(path) / 1024, 1),
        })
        if reason not in entry["reasons"]:
            entry["reasons"].append(reason)

    for phrase in CONTENT_PHRASES:
        for p in mdfind(f'"{phrase}"'):
            add(p, f"content: {phrase}")

    for p in filename_scan():
        add(p, "filename match")

    return found


def write_manifest(local: dict, drive: list[dict], out_path: Path):
    lines = [
        "# Surviving the Singularity — Source File Manifest",
        "",
        f"**Generated:** {datetime.now().isoformat(timespec='seconds')} by `scripts/find_book_sources.py`",
        f"**Local files:** {len(local)} · **Google Drive files:** {len(drive)}",
        "",
        "Sweep of every file on this machine (Spotlight content + filename search, home dir,",
        "noise dirs excluded) plus merged Google Drive results, matching the book's",
        "distinctive vocabulary and naming patterns.",
        "",
    ]

    by_kind: dict[str, list[dict]] = {}
    for e in local.values():
        by_kind.setdefault(e["kind"], []).append(e)

    kind_order = ["canonical chapter source", "manuscript", "document", "notes/text", "site/code", "other"]
    lines.append("## Local machine")
    lines.append("")
    for kind in kind_order:
        entries = by_kind.get(kind)
        if not entries:
            continue
        lines.append(f"### {kind.title()} ({len(entries)})")
        lines.append("")
        for e in sorted(entries, key=lambda x: x["modified"], reverse=True):
            rel = e["path"].replace(str(HOME), "~")
            reasons = "; ".join(e["reasons"][:3])
            lines.append(f"- `{rel}` — {e['size_kb']} KB, modified {e['modified'][:10]} ({reasons})")
        lines.append("")

    lines.append("## Google Drive")
    lines.append("")
    if drive:
        for f in drive:
            name = f.get("name") or f.get("title") or "untitled"
            url = f.get("url") or f.get("webViewLink") or ""
            mod = (f.get("modifiedTime") or "")[:10]
            mime = (f.get("mimeType") or "").split(".")[-1]
            link = f"[{name}]({url})" if url else f"`{name}`"
            lines.append(f"- {link} — {mime}{', modified ' + mod if mod else ''}")
    else:
        lines.append("*No Drive results merged. Re-run with `--drive-json <file>` after exporting*")
        lines.append("*Drive search results via the Claude Google Drive connector.*")
    lines.append("")

    out_path.write_text("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drive-json", type=Path, help="JSON list of Drive file dicts to merge")
    ap.add_argument("--out", type=Path,
                    default=Path(__file__).resolve().parent.parent / "manuscript" / "SOURCE-MANIFEST.md")
    ap.add_argument("--json-out", type=Path, help="also dump raw results as JSON")
    args = ap.parse_args()

    print("Searching local machine (Spotlight)...")
    local = gather_local()
    print(f"  {len(local)} local files")

    drive: list[dict] = []
    if args.drive_json and args.drive_json.exists():
        drive = json.loads(args.drive_json.read_text())
        print(f"  {len(drive)} Drive files merged from {args.drive_json}")

    write_manifest(local, drive, args.out)
    print(f"Wrote {args.out}")

    if args.json_out:
        args.json_out.write_text(json.dumps(
            {"local": list(local.values()), "drive": drive}, indent=2))
        print(f"Wrote {args.json_out}")


if __name__ == "__main__":
    main()
