#!/usr/bin/env python3
"""Rank the book's sections by candidate AI-writing tells.

Reads the manifest (src/lib/data/book/book.json), scans only the files it lists,
and counts phrases from the humanizer skill's watch lists
(.claude/skills/humanizer/SKILL.md, patterns numbered as there).

Every hit is a CANDIDATE, not a verdict. The book's Argument register uses
short hammer lines on purpose ("Not abolished. Optional."), and the humanizer
skill itself says one tell alone proves nothing. Use this report to pick which
section to run the humanize-book skill on first, and where to look inside it.

Skipped before matching: fenced code, HTML, image lines, captions that are a
whole italic line, headings, table rows, blockquotes (epigraphs) and anything
inside quotation marks (dialogue and cited titles are not CT's narration). Pull quotes (`> **...**`) are counted
separately, because they are CT's prose.

Usage:
  python3 scripts/humanizer_scan.py                 # all sections, ranked
  python3 scripts/humanizer_scan.py --file 07-chapter5.md --lines
  python3 scripts/humanizer_scan.py --out docs/humanizer/baseline.md
  python3 scripts/humanizer_scan.py --selftest       # planted controls, exit 1 on failure
Standard library only. A scan always exits 0: it is a triage tool, not a gate.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "src" / "lib" / "data" / "book"

I = re.IGNORECASE

# (pattern number in SKILL.md, short name, strength, regex)
# strength: "strong" = the skill acts on one sighting (patterns 1 to 5);
#           "weak" = only meaningful when several tells share a passage.
RULES: list[tuple[int, str, str, re.Pattern]] = [
    (1, "not X but Y", "strong", re.compile(
        r"\bnot (?:just|only|merely|simply)\b[^.?!]{1,80}?\bbut\b"
        r"|\b(?:it|this|that)(?:'s| is) not\b[^.?!]{1,60}?[,;:] (?:it|this|that)(?:'s| is)\b"
        r"|\b(?:it|this|that) isn't\b[^.?!]{1,60}?[,;:] (?:it|this|that)(?:'s| is)\b"
        r"|\b(?:does not|doesn't) mean\b[^.?!]{1,80}[.?!]\s+(?:It|This) means\b", I)),
    (1, "Not X. Y. (split hammer)", "weak", re.compile(
        r"(?:^|[.?!]\s+)(?:Not|Never) [^.?!]{1,40}\.\s+[A-Z][^.?!\s]*(?: [^.?!\s]+){0,3}\.")),
    (2, "stock closer", "strong", re.compile(
        r"\b(?:let that sink in|read that again|that distinction matters|that is the real|"
        r"that's the real|full stop\.|and that changes everything|"
        r"the message was clear|this shows the importance)", I)),
    (2, "fragment row", "weak", re.compile(
        r"(?:\b(?:No|Not) [^.?!]{1,25}\.\s+){2,}(?:No|Not) [^.?!]{1,25}\.")),
    (2, "spaced emphasis (every. single.)", "strong", re.compile(
        r"\b[a-z]+\. [a-z]+\. [a-z]+\.")),
    (3, "deep-sounding saying", "strong", re.compile(
        r"\b(?:the real question is|at its core|in reality,|what really matters|"
        r"fundamentally,|the deeper issue|the heart of the matter|"
        r"the (?:language|currency|architecture) of\b)", I)),
    (4, "staged run-up", "strong", re.compile(
        r"\b(?:let's dive in|let's explore|let's break (?:this|it) down|"
        r"here's what you need to know|now let's look at|without further ado|"
        r"here's the thing|the thing is,|let's be honest|real talk|"
        r"here's the kicker|the kicker\?)|(?:^|[.!?]\s+)(?:Honestly|Look)[?,]", I)),
    (5, "arguing with no one", "strong", re.compile(
        r"\b(?:I'm not saying|I am not saying|to be clear,|don't get me wrong|"
        r"this is not to say|one might be tempted|you might think\b[^.?!]{0,60}\bbut\b|"
        r"it would be easy to just)", I)),
    (8, "em dash", "strong", re.compile(chr(0x2014))),
    (8, "en dash outside a range", "weak", re.compile(r"(?<![0-9A-Za-z])–|–(?![0-9])")),
    (9, "stacked qualifier", "weak", re.compile(
        r"\b(?:could potentially|might arguably|it's also possible|in some cases it may)\b", I)),
    (12, "overused AI word", "weak", re.compile(
        r"\b(?:additionally|align(?:s|ed)? with|bolster(?:ed|s)?|crucial|deep dive|delv(?:e|es|ing)|"
        r"enduring|enhanc(?:e|es|ed|ing)|garner(?:ed|s)?|interplay|intricac(?:y|ies)|intricate|"
        r"meticulous(?:ly)?|pivotal|quietly|showcas(?:e|es|ed|ing)|tapestry|testament|"
        r"underscor(?:e|es|ed|ing)|vibrant)\b", I)),
    (13, "inflated significance", "weak", re.compile(
        r"\b(?:stands as a testament|a (?:pivotal|crucial) moment|plays? a (?:key|vital|crucial) role|"
        r"reflects a broader|lasting legacy|setting the stage for|evolving landscape|indelible mark|"
        r"the future looks bright|exciting times ahead|a step in the right direction)\b", I)),
    (15, "-ing rider", "weak", re.compile(
        r", (?:highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|"
        r"contributing to|cultivating|fostering|encompassing|showcasing)\b", I)),
    (16, "sales language", "weak", re.compile(
        r"\b(?:profound|exemplif(?:y|ies)|commitment to|nestled|in the heart of|groundbreaking|"
        r"renowned|diverse array|breathtaking|must-visit|stunning)\b", I)),
    (17, "borrowed authority", "weak", re.compile(
        r"\b(?:experts (?:argue|say|agree)|observers have|industry reports|some critics|"
        r"several publications|studies show|research shows)\b", I)),
    (18, "avoiding is/has", "weak", re.compile(
        r"\b(?:serves as|stands as|functions as|boasts)\b", I)),
    (21, "curly quote", "weak", re.compile("[“”‘’]")),
    (22, "chatbot residue", "strong", re.compile(
        r"\b(?:I hope this helps|great question|you're absolutely right|let me know|"
        r"would you like (?:me|to)|should I continue)\b|\bCertainly!|\bOf course!", I)),
    (23, "knowledge-limit hedge", "strong", re.compile(
        r"\b(?:as of my|my last training|while specific details are limited|based on available information|"
        r"not widely documented|it is believed that)\b", I)),
]

FENCE = re.compile(r"^\s*(```|~~~)")
SKIP_LINE = re.compile(r"^\s*(?:!\[|<|#|\||\*[^*].*\*\s*$|_[^_].*_\s*$|-{3,}\s*$|\*{3,}\s*$)")
PULL_QUOTE = re.compile(r"^\s*>\s*\*\*.+\*\*\s*$")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
WORD = re.compile(r"[A-Za-z0-9']+")
# Quoted spans are dialogue or cited words, not CT's narration.
QUOTED = re.compile(r'"[^"]{0,400}"|\u201c[^\u201d]{0,400}\u201d')


def prose_lines(text: str):
    """Yield (line_no, text, kind) for lines that are CT's prose."""
    in_fence = False
    for n, raw in enumerate(text.splitlines(), 1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence or not raw.strip():
            continue
        if PULL_QUOTE.match(raw):
            yield n, raw.strip().lstrip(">").strip().strip("*"), "pull"
            continue
        if raw.lstrip().startswith(">") or SKIP_LINE.match(raw):
            continue
        line = QUOTED.sub('""', LINK_TARGET.sub("]", INLINE_CODE.sub("", raw)))
        line = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", line)
        yield n, line, "prose"


def scan_file(path: Path):
    text = path.read_text(encoding="utf-8")
    words = 0
    hits: list[tuple[int, int, str, str, str]] = []  # line, rule#, name, strength, excerpt
    pulls = 0
    for n, line, kind in prose_lines(text):
        if kind == "pull":
            pulls += 1
        words += len(WORD.findall(line))
        for num, name, strength, rx in RULES:
            for m in rx.finditer(line):
                a, b = max(0, m.start() - 30), min(len(line), m.end() + 30)
                hits.append((n, num, name, strength, line[a:b].strip()))
    return words, hits, pulls


def manifest():
    data = json.loads((BOOK / "book.json").read_text(encoding="utf-8"))
    return data, [(s["id"], s["title"], s["file"]) for s in data["sections"]]


def git_head() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


SELFTEST = [
    # (text, rule number that must fire, or None for "must stay silent")
    ("It's not just a tool, it's a shift in how we work.", 1),
    ("Let that sink in.", 2),
    ("Here's the thing about soil.", 4),
    ("I'm not saying you should quit.", 5),
    ("The bill came\u2014and it was huge.", 8),
    ("The co-op quietly bought the lot.", 12),
    ('"Great question," the CPO said.', None),
    ("> *\"It's not just X, it's Y.\"*", None),
    ("![It's not just a picture, it's art](/x.jpg)", None),
    ("Stages 1\u20135 cover the AGI era.", None),
]


def selftest() -> int:
    bad = 0
    for text, want in SELFTEST:
        fired = {num for _, line, _ in prose_lines(text)
                 for num, _, _, rx in RULES if rx.search(line)}
        ok = (want in fired) if want else not fired
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} want={want} fired={sorted(fired)} :: {text}")
    print("selftest passed" if not bad else f"selftest FAILED ({bad})")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true", help="run planted good and bad lines")
    ap.add_argument("--file", help="scan one manifest file, e.g. 07-chapter5.md")
    ap.add_argument("--lines", action="store_true", help="list every hit with its line number")
    ap.add_argument("--out", help="write the report to this path instead of stdout")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    data, sections = manifest()
    if args.file:
        sections = [s for s in sections if s[2] == args.file]
        if not sections:
            raise SystemExit(f"{args.file} is not listed in book.json, so it is not in the book.")

    rows = []
    for sid, title, fname in sections:
        words, hits, pulls = scan_file(BOOK / fname)
        strong = sum(1 for h in hits if h[3] == "strong")
        weak = len(hits) - strong
        per_k = (strong * 2 + weak) / max(words, 1) * 1000
        rows.append((per_k, sid, title, fname, words, strong, weak, pulls, hits))

    out: list[str] = []
    today = dt.date.today().isoformat()
    out.append(f"# Humanizer scan, {today}")
    out.append("")
    out.append(f"Book {data.get('version')} at commit `{git_head()}`. Made by "
               "`python3 scripts/humanizer_scan.py`. Counts are measured; whether a hit is a "
               "real tell is a judgment the scan cannot make. Score = (2 x strong + weak) per "
               "1,000 prose words.")
    out.append("")
    out.append("| Rank | Section | File | Prose words | Strong | Weak | Pull quotes | Score |")
    out.append("|---:|---|---|---:|---:|---:|---:|---:|")
    ranked = sorted(rows, key=lambda r: -r[0])
    for i, (per_k, sid, title, fname, words, strong, weak, pulls, _) in enumerate(ranked, 1):
        out.append(f"| {i} | {title} | `{fname}` | {words:,} | {strong} | {weak} | {pulls} | {per_k:.1f} |")

    totals: dict[tuple[int, str], int] = {}
    for r in rows:
        for h in r[8]:
            totals[(h[1], h[2])] = totals.get((h[1], h[2]), 0) + 1
    out.append("")
    out.append("## Hits by pattern (whole scan)")
    out.append("")
    out.append("| Skill section | Pattern | Hits |")
    out.append("|---:|---|---:|")
    for (num, name), c in sorted(totals.items(), key=lambda kv: (kv[0][0], -kv[1])):
        out.append(f"| {num} | {name} | {c} |")

    if args.lines or args.file:
        for _, sid, title, fname, *_rest, hits in ranked:
            out.append("")
            out.append(f"## {title} (`{fname}`)")
            out.append("")
            for n, num, name, strength, ex in hits:
                out.append(f"- L{n} section {num} {name} ({strength}): {ex}")

    report = "\n".join(out) + "\n"
    if args.out:
        p = Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(report, encoding="utf-8")
        print(f"wrote {p}")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
