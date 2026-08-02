#!/usr/bin/env python3
"""Build the preorder bonus, "The Precedent File", from the manuscript research.

The centrepiece is manuscript/HISTORY-CASEBOOK.md, which is an internal working
document: it carries production notes, chapter placement instructions and a
"do NOT use" blacklist written as an instruction to the author. None of that
can ship to a reader as-is, so this script derives a reader-facing edition from
it rather than anyone maintaining a second copy by hand. Re-run it whenever the
casebook changes.

House rules enforced here, because a customer-facing file is copy:
  - no em dashes anywhere in the prose (see _dedash)
  - no internal production language (see INTERNAL_PATTERNS, asserted at the end)

Stdlib only, matching scripts/sts.py.

Usage:
  python3 scripts/build_bonus.py            # build into manuscript/bonus/dist
  python3 scripts/build_bonus.py --no-pdf   # skip the pandoc/xelatex step
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
import textwrap
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASEBOOK = ROOT / "manuscript" / "HISTORY-CASEBOOK.md"
BONUS = ROOT / "manuscript" / "bonus"
DIST = BONUS / "dist"
STAGE = DIST / "The-Precedent-File"

BOOK_JSON = ROOT / "src" / "lib" / "data" / "book" / "book.json"
APPENDIX_D = ROOT / "src" / "lib" / "data" / "book" / "25-appendix-d.md"
DOWNLOADS = ROOT / "static" / "downloads"
MUNI_PDF = DOWNLOADS / "Municipal-Autonomy-Code.pdf"
ROBOTICS_CSV = ROOT / "static" / "data" / "robotics_companies.csv"

# The cover source is resolved at build time, not asserted here. art-raw/ is
# gitignored (.gitignore:64), so it is absent in any fresh clone and hard-failing
# on it would make this script unrunnable for everyone but the author's laptop.
# The fallback is the same full-size art the /early-access OG tags already use.
COVER_CANDIDATES = [
    ROOT / "art-raw" / "book-cover-final-source.png",
    ROOT / "static" / "Surviving-the-Singularity-Cover.png",
]
COVER_800 = ROOT / "static" / "images" / "optimized" / "surviving_the_singularity_cover_800.png"
COVER_400 = ROOT / "static" / "images" / "optimized" / "surviving_the_singularity_cover_400.png"

# Where the site reads the same facts from. Written by this script, never by hand.
SITE_MANIFEST = ROOT / "src" / "lib" / "data" / "bundleManifest.js"

MANIFEST_SCHEMA = 1

# Anything matching these must not survive into the shipped file. Checked at the
# end so a future edit to the casebook cannot quietly leak production notes.
INTERNAL_PATTERNS = [
    r"Greene register",
    r"Tiffany section",
    r"ammunition",
    r"do not let these into the book",
    r"do NOT use",
    r"Placement map",
    r"transplanted into a chapter",
    r"blacklist",
    r"\bTODO\b",
    r"\bFIXME\b",
]

# Every number below is a {{TOKEN}} filled from a measurement of the document
# this script just built. The hardcoded "29" that used to sit here was never
# measured against anything: the real figure is 31, the ledger it was confused
# with is 23, and the "cases indexed" line this script prints is 27. Four
# numbers, one of them on four live sales surfaces, none of them counted. See
# _count_cases and the header of src/lib/offer.js.
FRONT_MATTER = """---
title: "The Precedent File"
subtitle: "{{CASE_COUNT}} documented cases of people meeting a machine that changed everything"
author: "Companion research to *Surviving the Singularity*"
lang: en-GB
---

# The Precedent File

**{{CASE_COUNT}} documented cases of people meeting a machine that changed
everything, and what they did next.**

Companion research to *Surviving the Singularity* {{BOOK_VERSION}}. Free with
the preorder.

Every case below follows the same three beats: the story, the mechanism (the
reason it happened, not just the fact that it did), and the rule you can carry
out of it. Sources sit under each case. Where a famous version of a story is
embellished or fabricated, that is said plainly instead of quietly using it.

The final section, *Stories that are not true*, exists because the argument
this book makes attracts fake evidence. {{APOCRYPHA_DEBUNKED_WORDS}} of the
most repeated anecdotes about technology panic have no primary source, and one
more is real but routinely overstated. They are listed so you can stop using
them, with the documented alternative in each case.

"""

LEDGER_INTRO = """## The ledger

Every chapter of *Surviving the Singularity* closes with a precedent: a
documented case of people meeting a technological wave. They run P-01 to
P-{{LEDGER_MAX}} in order of appearance, so the weight accumulates as you read.
This table maps each one to its chapter in the book and to its full write-up
below.

Note the two numbers, because they are easy to confuse and this file is about
checking work. The ledger below holds {{LEDGER_COUNT}} precedents, one per
chapter of the book. This file holds {{CASE_COUNT}} cases, because the research
turned up more than the book had room to close chapters with.

"""


def _dedash_sentence(s: str) -> str:
    """Apply the voice guide's rule to one sentence.

    VOICE-GUIDE.md line 108: "No em dashes anywhere. Use a period, colon, comma,
    or parenthesis." Which of the four is right depends on what the dash is
    doing, so this picks per case instead of flattening everything to a comma:

      A -- B -- C   parenthetical aside   ->  A (B) C
      **Label** -- X   label gloss        ->  **Label**, X
      A -- short punch.   sentence-final  ->  A: short punch.
      anything else                       ->  comma
    """
    if "—" not in s:
        return s

    # Paired dashes are an aside. Parentheses keep the aside legible where a
    # second comma would just join an already comma-heavy list.
    while s.count("—") >= 2:
        s = re.sub(r"\s+—\s+(.+?)\s+—\s+", r" (\1) ", s, count=1)
        if s.count("—") >= 2 and " (" not in s:
            break

    # A dash right after a bold label is glossing the label.
    s = re.sub(r"(\*\*[^*]+\*\*)\s*—\s*", r"\1, ", s)

    # A single dash introducing the tail of the sentence is doing a colon's job,
    # and the colon preserves the punch that made a dash attractive there.
    m = re.search(r"\s+—\s+", s)
    if m:
        tail = s[m.end():]
        if "—" not in tail and len(tail) <= 70 and tail.rstrip().endswith((".", ".*", '."', ".)")):
            s = s[: m.start()] + ": " + tail
        else:
            s = s[: m.start()] + ", " + tail

    return re.sub(r"\s*—\s*", ", ", s)


def _dedash_flow(text: str) -> str:
    """Sentence-aware pass over a run of prose."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(_dedash_sentence(p) for p in parts)


def _dedash(text: str) -> str:
    """Remove em dashes (U+2014) block by block.

    U+2013 is left alone: it is doing legitimate work in ranges like 1780-1800.
    Prose is unwrapped so sentence rules can see whole sentences, then rewrapped.
    """
    blocks = text.split("\n\n")
    out_blocks = []
    for block in blocks:
        if "—" not in block:
            out_blocks.append(block)
            continue
        stripped = block.lstrip()
        if stripped.startswith("#"):
            block = block.replace(" — ", ": ", 1)
            block = re.sub(r"\s*—\s*", ", ", block)
        elif stripped.startswith("|"):
            block = re.sub(r"\s*—\s*", ", ", block)
        elif stripped.startswith(("- ", "* ")):
            # Join each bullet's wrapped continuation lines, then treat as prose.
            items, cur = [], []
            for line in block.split("\n"):
                if re.match(r"\s*[-*] ", line) and cur:
                    items.append(" ".join(cur))
                    cur = [line.strip()]
                else:
                    cur.append(line.strip())
            if cur:
                items.append(" ".join(cur))
            block = "\n".join(_dedash_flow(i) for i in items)
        elif stripped.startswith("Sources:"):
            # Inside link text a colon reads as a subtitle, which is what the
            # dash was standing in for: "Forbes - How Kodak Failed".
            block = re.sub(r"(\[[^\]]*?)\s+—\s+", r"\1: ", block)
            block = re.sub(r"\s*—\s*", ", ", block)
        else:
            joined = " ".join(l.strip() for l in block.split("\n"))
            joined = _dedash_flow(joined)
            block = "\n".join(textwrap.wrap(joined, width=88)) if "](http" not in joined else joined
        out_blocks.append(block)
    return "\n\n".join(out_blocks)


def _clean_body(raw: str) -> tuple[str, str]:
    lines = raw.split("\n")

    # 1. Drop the internal header block, keep from the ledger heading onward.
    start = next(i for i, l in enumerate(lines) if l.startswith("## THE PRECEDENT LEDGER"))
    lines = lines[start:]

    # 2. Cut the superseded placement map entirely, and hold the apocrypha
    #    section aside so it can be reframed rather than deleted.
    text = "\n".join(lines)
    text = re.sub(r"\n## Placement map.*?(?=\n## )", "\n", text, flags=re.S)

    apoc_match = re.search(r"\n## Apocrypha blacklist[^\n]*\n(.*)$", text, flags=re.S)
    apocrypha = apoc_match.group(1).strip() if apoc_match else ""
    text = text[: apoc_match.start()] if apoc_match else text

    # 3. Reframe the ledger heading and its versioned internal title.
    text = re.sub(r"## THE PRECEDENT LEDGER[^\n]*\n+", LEDGER_INTRO, text, count=1)
    text = re.sub(
        r"Every chapter of the book closes with a \*\*Precedent\*\*.*?in Appendix D\.\n+",
        "",
        text,
        flags=re.S,
    )

    # 4. Strip production-only language from the prose.
    text = text.replace("**Lesson (Greene register):**", "**Lesson:**")
    text = text.replace(
        "**Lesson for the whole section (Greene register):**",
        "**Lesson for the whole section:**",
    )
    text = text.replace(" This is the Tiffany section's ammunition.", "")
    text = text.replace(
        "## E. Cyberdecks — the current chapter of the same story (for Ch. 5)",
        "## E. Cyberdecks: the current chapter of the same story",
    )
    text = text.replace("**Why it belongs in this book:**", "**Why it matters:**")
    # Source-line warnings are written as instructions to the author.
    text = text.replace(
        "(Do NOT use Pedro II \"My God, it talks!\" — embellished; Kelvin's praise is the documented beat.)",
        "(Note: the Pedro II \"My God, it talks!\" line is embellished. Kelvin's praise is the documented moment.)",
    )
    text = text.replace(
        "(Do NOT use the 1894 \"nine feet of manure\" Times quote — unsourced.)",
        "(Note: the 1894 \"nine feet of manure\" quote is unsourced. Use the horse-population figures instead.)",
    )

    # 5. Precedent IDs read better in parentheses than trailing off a heading.
    text = re.sub(r"^(### .*?) — (P-\d+)$", r"\1 (Precedent \2)", text, flags=re.M)

    return text.strip(), apocrypha


# Written by hand rather than derived. The source version of this section is a
# terse instruction list to the author ("do NOT use", "avoid"), and this is the
# part of the file readers are most likely to quote at somebody, so it needs to
# be right and it needs to give the replacement, not just the prohibition.
APOCRYPHA = """## Stories that are not true

The argument this book makes attracts fake evidence. Every item below gets
repeated constantly by people arguing that technology panics are always wrong,
and not one of them survives a look for a primary source.

Using a fabricated quote to make a true point hands the other side a free win.
Each entry gives you the documented version to use instead.

### The Western Union memo (1876)

*"The telephone has too many shortcomings to be seriously considered as a means
of communication."* Presented as an internal Western Union memo. No primary
source has ever surfaced and it is widely considered fabricated.

**Use instead:** the documented fact that Western Union turned down Bell's
patents and then lost the telephone war it started. The behaviour is real. The
memo is not.

### The teachers-against-slates quote chain

*"Students today depend upon paper too much..."* attributed variously to 1815,
1907 and 1928 teachers' conferences. A fabricated internet meme with no primary
source at any of those dates.

**Use instead:** cases D1 to D5 in this file. The real panic lineage runs from
novels in the 1790s through the waltz, the bicycle, the phonograph and the
comic book, and every link in it is sourced. It is a stronger argument than the
fake one, because it is true.

### "640K ought to be enough for anybody"

Attributed to Bill Gates. Gates has denied saying it, repeatedly, and no source
has ever been produced.

**Use instead:** nothing. The point it is normally used to make is better served
by G1, G2 or G3, all of which are documented predictions by named people in
print.

### Nathan Rothschild's Waterloo pigeons

The story that Rothschild used carrier pigeons to learn the outcome of Waterloo
early and cornered the market. Heavily embellished legend built on a much
smaller kernel.

**Use instead:** treat it as folklore, not finance history.

### Pedro II and the telephone (Centennial Exhibition, 1876)

*"My God, it talks!"* The emperor was at the exhibition and the telephone was
demonstrated. The exclamation is an embellishment.

**Use instead:** Lord Kelvin's documented praise of the device, which is the
recorded moment and is in case F1.

### The 1894 Times manure prediction

*"In fifty years every street in London will be buried under nine feet of
manure."* No primary source has ever been produced. The Great Horse Manure
Crisis framing traces to a 2004 essay, not to an 1894 newspaper.

**Use instead:** the horse population figures in F4. The United States horse
population peaked above 25 million in the 1910s and had collapsed by 1960. The
real numbers make the point without the invented quote.

### "Everything that can be invented has been invented"

Attributed to Charles Duell, Commissioner of the US Patent Office, 1899.
Fabricated. Duell said close to the opposite.

**Use instead:** G1, the New York Times editorial of 1903 declaring powered
flight roughly a million years away, sixty-nine days before Kitty Hawk. Same
point, real citation.

### One that is real, with a caveat

**Blockbuster laughing Netflix out of the room (2000).** The meeting is
documented. The laughing is Marc Randolph and Reed Hastings' own account, and
John Antioco has disputed that there were serious talks. Case A3 states it that
way on purpose. Attribute it to the founders' account and acknowledge the
denial, and it holds. Assert it flatly as fact and it does not.

"""


def _rewrite_apocrypha(_block: str) -> str:
    return APOCRYPHA


def _extract_sources(text: str) -> tuple[str, int, int]:
    """Pull every citation into a standalone index, grouped by case."""
    out = [
        "# Sources and Citations",
        "",
        "Every source cited in *The Precedent File*, grouped by case, in the order",
        "they appear. Links are to the material itself wherever possible rather than",
        "to a summary of it.",
        "",
        "Where a source is a fact-check or a correction, that is the point: the case",
        "is stronger for having survived it.",
        "",
        "---",
        "",
    ]
    current = None
    n_cases = 0
    n_links = 0
    for line in text.split("\n"):
        m = re.match(r"^#{2,3} (.+)$", line)
        if m:
            current = m.group(1).strip()
            continue
        if line.startswith("Sources:") and current:
            links = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", line)
            if not links:
                continue
            n_cases += 1
            out.append(f"## {current}")
            out.append("")
            for label, url in links:
                out.append(f"- [{label}]({url})")
                n_links += 1
            out.append("")
    out.append("---")
    out.append("")
    # "headings", not "cases". This counts headings that carry a Sources line,
    # which includes one section-level heading and excludes the cases that have
    # no sources yet. Calling it a case count is how the wrong number spread.
    out.append(f"*{n_links} sources across {n_cases} headings.*")
    return "\n".join(out), n_cases, n_links


# ---------------------------------------------------------------------------
# Measurement. Everything below counts the artifact rather than asserting about
# it, because every wrong number this file has ever shipped was asserted.
# ---------------------------------------------------------------------------

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = ("", "", "twenty", "thirty", "forty", "fifty",
         "sixty", "seventy", "eighty", "ninety")


def _spell(n: int) -> str:
    """Spell an integer 0-99. The voice deliberately writes counts out in prose."""
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    return _TENS[tens] + (f"-{_ONES[ones]}" if ones else "")


def _fill(text: str, tokens: dict) -> str:
    """Substitute {{TOKEN}} placeholders.

    Deliberately not str.format: these templates are prose that may grow a
    literal brace, and format would raise on it. The build refuses to ship any
    surviving {{ (see the leak guard in main), so a typo cannot pass silently.
    """
    for k, v in tokens.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


# A case is anchored on its ID, not on the heading level. "### A1. " can only be
# a case; "### The Western Union memo (1876)" in the apocrypha never can, even if
# somebody later moves that block above the split point.
CASE_RE = re.compile(r"^### ([A-G])(\d+)\. (.+)$", re.M)
GROUP_RE = re.compile(r"^## ([A-G])\. (.+)$", re.M)


def _count_cases(body: str) -> dict:
    """Count what the emitted document actually contains, and assert its shape.

    Returns the counts block that goes into the manifest. Raises SystemExit on a
    structural problem, because a bundle whose own index is wrong is worse than
    no bundle: the entire pitch of this file is that you can check the work.
    """
    cases = CASE_RE.findall(body)
    groups = GROUP_RE.findall(body)

    ids = [f"{letter}{num}" for letter, num, _ in cases]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise SystemExit(f"build_bonus: duplicate case ids {dupes}")

    per_group = {}
    for letter, num, _ in cases:
        per_group.setdefault(letter, []).append(int(num))

    for letter, nums in per_group.items():
        expected = list(range(1, len(nums) + 1))
        if sorted(nums) != expected:
            raise SystemExit(
                f"build_bonus: group {letter} is not contiguous from 1: "
                f"found {sorted(nums)}, expected {expected}"
            )

    # Which cases carry no Sources line. Reported, never hidden: a case without a
    # source is the one thing a reader of this file is entitled to know about.
    without = []
    for letter, num, _ in cases:
        cid = f"{letter}{num}"
        start = body.index(f"### {cid}. ")
        nxt = body.find("\n### ", start + 1)
        chunk = body[start:nxt if nxt != -1 else len(body)]
        if "Sources:" not in chunk:
            without.append(cid)

    declared = [letter for letter, _ in groups]
    return {
        "precedent_file_cases": len(cases),
        "cases_with_sources": len(cases) - len(without),
        "cases_without_sources": without,
        "case_groups": [
            {"letter": letter, "title": title, "cases": len(per_group.get(letter, []))}
            for letter, title in groups
        ],
        "sections_without_cases": [g for g in declared if g not in per_group],
    }


def _count_apocrypha(block: str) -> tuple[int, int]:
    """(entries, debunked). The last entry is 'One that is real, with a caveat',
    which is why the old 'Eight have no primary source' line was false."""
    entries = re.findall(r"^### (.+)$", block, re.M)
    real = [e for e in entries if re.search(r"\breal\b", e, re.I)]
    return len(entries), len(entries) - len(real)


def _ledger_count() -> tuple[int, int]:
    """(count, max) of the book's own precedent ledger, read from Appendix D."""
    rows = re.findall(r"^\| P-(\d+)", APPENDIX_D.read_text(encoding="utf8"), re.M)
    if not rows:
        raise SystemExit(f"build_bonus: no P-NN rows found in {APPENDIX_D}")
    nums = [int(r) for r in rows]
    return len(nums), max(nums)


def _book_meta() -> dict:
    meta = json.loads(BOOK_JSON.read_text(encoding="utf8"))
    return {
        "version": meta["version"],
        "title": meta["title"],
        "last_updated": meta.get("lastUpdated"),
    }


def _book_artifacts(version: str) -> dict:
    """Locate the shipped book files by glob, then assert they are this version.

    Deliberately NOT a second implementation of the filename rule. That rule
    lives in src/lib/bookManifest.js and nowhere else. Globbing and asserting
    fails loudly on a rename; a copy of the rule would quietly build the wrong
    name, which is the failure this repo keeps legislating against.
    """
    out = {}
    for ext in ("pdf", "epub"):
        hits = sorted(DOWNLOADS.glob(f"Surviving-the-Singularity-v*.{ext}"))
        if len(hits) != 1:
            raise SystemExit(
                f"build_bonus: expected exactly one {ext} in {DOWNLOADS}, "
                f"found {[h.name for h in hits]}. Run scripts/publish-book-downloads.mjs."
            )
        if f"-v{version}." not in hits[0].name:
            raise SystemExit(
                f"build_bonus: book.json says v{version} but {DOWNLOADS} holds "
                f"{hits[0].name}. Rebuild the book before building the bundle."
            )
        out[ext] = hits[0]
    return out


def _resolve_cover() -> tuple[Path, bool]:
    """First existing cover source, and whether it is the fallback."""
    for i, cand in enumerate(COVER_CANDIDATES):
        if cand.exists():
            return cand, i > 0
    raise SystemExit(
        "build_bonus: no cover source found. Tried: "
        + ", ".join(str(c) for c in COVER_CANDIDATES)
    )


def _png_dimensions(path: Path) -> tuple[int, int] | None:
    """Width and height straight out of the PNG IHDR chunk. Stdlib only.

    Read rather than asserted so the manifest can state the real pixel size of
    the cover art instead of calling it "high resolution", which is an adjective
    a buyer cannot check.
    """
    with path.open("rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not CASEBOOK.exists():
        print(f"error: {CASEBOOK} not found", file=sys.stderr)
        return 1

    raw = CASEBOOK.read_text(encoding="utf8")
    body, apocrypha = _clean_body(raw)
    apocrypha = _rewrite_apocrypha(apocrypha)

    # Measure first, then write the numbers into the prose. Never the reverse.
    counts = _count_cases(body)
    apoc_entries, apoc_debunked = _count_apocrypha(apocrypha)
    ledger_count, ledger_max = _ledger_count()
    book = _book_meta()

    counts["apocrypha_entries"] = apoc_entries
    counts["apocrypha_debunked"] = apoc_debunked
    counts["ledger_precedents"] = ledger_count

    tokens = {
        "CASE_COUNT": counts["precedent_file_cases"],
        "CASE_COUNT_WORDS": _spell(counts["precedent_file_cases"]),
        "LEDGER_COUNT": ledger_count,
        "LEDGER_MAX": f"{ledger_max:02d}",
        "APOCRYPHA_DEBUNKED": apoc_debunked,
        "APOCRYPHA_ENTRIES": apoc_entries,
        "APOCRYPHA_DEBUNKED_WORDS": _spell(apoc_debunked).capitalize(),
        "APOCRYPHA_DEBUNKED_WORDS_LC": _spell(apoc_debunked),
        "BOOK_VERSION": f"v{book['version']}",
    }

    document = FRONT_MATTER + body + "\n\n---\n\n" + apocrypha + "\n"
    # Fill before the de-dash pass so its rewrapping measures the final text.
    document = _fill(document, tokens)
    document = _dedash(document)

    sources_md, n_sourced_cases, n_links = _extract_sources(document)
    sources_md = _dedash(sources_md)
    counts["source_links"] = n_links

    # Guard: nothing internal may ship.
    leaks = []
    for pat in INTERNAL_PATTERNS:
        for m in re.finditer(pat, document, flags=re.I):
            leaks.append(f"{pat!r} at char {m.start()}: ...{document[max(0,m.start()-60):m.start()+60]!r}...")
    if "—" in document or "—" in sources_md:
        leaks.append("em dash survived the de-dash pass")
    # An unfilled placeholder is a build bug that would ship as literal braces.
    for m in re.finditer(r"\{\{[A-Z_]+\}\}", document):
        leaks.append(f"unfilled placeholder {m.group(0)} at char {m.start()}")
    # Regression guard on the number this file shipped wrong for months. Only
    # trips when it is being used AS a case count, so a year like 1929 is safe.
    for m in re.finditer(r"\b(29|twenty-nine)\b(?=[^.]{0,40}\b(cases?|documented|precedents?)\b)",
                         document, flags=re.I):
        leaks.append(f"stale case count {m.group(1)!r} at char {m.start()}")
    if leaks:
        print("REFUSING TO BUILD, internal content would leak:", file=sys.stderr)
        for l in leaks:
            print("  -", l, file=sys.stderr)
        return 1

    art = _book_artifacts(book["version"])
    cover_full, cover_is_fallback = _resolve_cover()
    cover_dims = _png_dimensions(cover_full)

    if STAGE.exists():
        shutil.rmtree(STAGE)
    (STAGE / "book").mkdir(parents=True)
    (STAGE / "extras").mkdir()
    (STAGE / "cover").mkdir()
    (STAGE / "research").mkdir()

    (STAGE / "The-Precedent-File.md").write_text(document, encoding="utf8")
    (STAGE / "Sources-and-Citations.md").write_text(sources_md, encoding="utf8")

    # `role` is the field that makes decision two enforceable. A file marked
    # convenience-copy is one the reader can already download for free, and the
    # page and the email render that fact FROM HERE rather than from an adjective
    # somebody typed. Nobody can quietly promote it back to a selling point.
    copies = [
        (art["pdf"], STAGE / "book" / "Surviving-the-Singularity.pdf",
         f"Surviving the Singularity, v{book['version']} (PDF)", "convenience-copy",
         f"/downloads/{art['pdf'].name}"),
        (art["epub"], STAGE / "book" / "Surviving-the-Singularity.epub",
         f"Surviving the Singularity, v{book['version']} (EPUB)", "convenience-copy",
         f"/downloads/{art['epub'].name}"),
        (MUNI_PDF, STAGE / "extras" / "Municipal-Autonomy-Code.pdf",
         "The Municipal Autonomy Code (Appendix A)", "convenience-copy",
         "/downloads/Municipal-Autonomy-Code.pdf"),
        (cover_full, STAGE / "cover" / "Surviving-the-Singularity-cover-full.png",
         f"Cover art, {cover_dims[0]}x{cover_dims[1]}" if cover_dims else "Cover art",
         "primary", None),
        (COVER_800, STAGE / "cover" / "Surviving-the-Singularity-cover-800.png",
         "Cover art, 800px wide", "primary", None),
        (COVER_400, STAGE / "cover" / "Surviving-the-Singularity-cover-400.png",
         "Cover art, 400px wide", "primary", None),
        (ROBOTICS_CSV, STAGE / "research" / "Robotics-Company-Index.csv",
         "The Robotics Company Index (CSV)", "primary", None),
    ]
    labels = {}
    for src, dst, label, role, free_at in copies:
        if not src.exists():
            print(f"error: missing required asset {src}", file=sys.stderr)
            return 1
        shutil.copy2(src, dst)
        labels[dst] = (label, role, free_at)

    labels[STAGE / "The-Precedent-File.md"] = (
        f"The Precedent File, {counts['precedent_file_cases']} cases (Markdown)", "primary", None)
    labels[STAGE / "Sources-and-Citations.md"] = (
        f"Sources and Citations, {n_links} links", "primary", None)

    if "--no-pdf" not in sys.argv:
        pandoc = shutil.which("pandoc")
        if pandoc:
            cmd = [
                pandoc, str(STAGE / "The-Precedent-File.md"),
                "-o", str(STAGE / "The-Precedent-File.pdf"),
                "--pdf-engine=xelatex", "--toc", "--toc-depth=2",
                "-V", "geometry:margin=1in", "-V", "linkcolor:blue",
                "-V", "mainfont=Helvetica Neue", "-V", "fontsize=11pt",
            ]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print("warning: PDF build failed, shipping markdown only")
                print("  ", (r.stderr or "").strip().splitlines()[-1:] or "")
            else:
                print(f"  PDF: {(STAGE / 'The-Precedent-File.pdf').stat().st_size:,} bytes")
                labels[STAGE / "The-Precedent-File.pdf"] = (
                    f"The Precedent File, {counts['precedent_file_cases']} cases (PDF)",
                    "primary", None)

    # START-HERE is a template so the reader-facing README cannot describe a
    # bundle other than the one it ships inside. Its "What is inside" table is
    # generated from the staged files for the same reason.
    staged_now = sorted(p for p in STAGE.rglob("*") if p.is_file())
    inside_rows = ["| File | What it is |", "| --- | --- |"]
    for p in staged_now:
        rel = p.relative_to(STAGE).as_posix()
        label, role, free_at = labels.get(p, (rel, "primary", None))
        note = f"{label}. Also free at `{free_at}`." if free_at else f"{label}."
        inside_rows.append(f"| `{rel}` | {note} |")

    start_here = (BONUS / "START-HERE.md").read_text(encoding="utf8")
    # The template's own instructions are for whoever edits it, not for a reader.
    start_here = re.sub(r"<!--.*?-->\n*", "", start_here, flags=re.S)
    start_here = _fill(start_here, {**tokens, "INSIDE_TABLE": "\n".join(inside_rows)})
    start_here = _dedash(start_here)
    if "{{" in start_here:
        print("error: START-HERE.md has unfilled placeholders", file=sys.stderr)
        return 1
    (STAGE / "START-HERE.md").write_text(start_here, encoding="utf8")
    labels[STAGE / "START-HERE.md"] = ("Start here", "primary", None)

    # ONE list feeds both the archive and the manifest. That is what makes
    # "the manifest is generated, never hand-written" a property of the code
    # rather than a promise in a comment: there is no second enumeration to
    # forget to update.
    staged = sorted(p for p in STAGE.rglob("*") if p.is_file())

    zip_path = DIST / "research-bundle-v1.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in staged:
            z.write(f, f.relative_to(STAGE.parent))

    files = []
    for p in staged:
        label, role, free_at = labels.get(p, (p.name, "primary", None))
        rec = {
            "path": p.relative_to(STAGE.parent).as_posix(),
            "label": label,
            "format": p.suffix.lstrip(".").lower(),
            "role": role,
            "bytes": p.stat().st_size,
            "sha256": _sha256(p),
        }
        if free_at:
            rec["also_free_at"] = free_at
        files.append(rec)

    manifest = {
        "schema": MANIFEST_SCHEMA,
        # Second resolution, UTC, no microseconds. The zip is not byte
        # reproducible anyway (copy2 carries mtimes in), so bundle.sha256
        # describes THIS artifact and `sts.py bundle verify --remote` is what
        # compares the live object against the manifest that shipped with it.
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
                                 .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "generator": "scripts/build_bonus.py",
        "bundle": {
            "root": STAGE.name,
            "object": "research-bundle-v1.zip",
            "bucket": "downloads",
            "bytes": zip_path.stat().st_size,
            "sha256": _sha256(zip_path),
            "entries": len(files),
        },
        "book": book,
        "counts": counts,
        "cover": {
            "source": str(cover_full.relative_to(ROOT)),
            "fallback": cover_is_fallback,
            "width": cover_dims[0] if cover_dims else None,
            "height": cover_dims[1] if cover_dims else None,
        },
        "files": files,
        # Input hashes are what let `bundle verify` say "the committed site
        # manifest is stale relative to the casebook" instead of only "the
        # numbers match themselves".
        "inputs": {
            "casebook": {"path": str(CASEBOOK.relative_to(ROOT)), "sha256": _sha256(CASEBOOK)},
            "start_here": {"path": str((BONUS / "START-HERE.md").relative_to(ROOT)),
                           "sha256": _sha256(BONUS / "START-HERE.md")},
            "book_json": {"path": str(BOOK_JSON.relative_to(ROOT)), "sha256": _sha256(BOOK_JSON)},
            "appendix_d": {"path": str(APPENDIX_D.relative_to(ROOT)), "sha256": _sha256(APPENDIX_D)},
        },
    }

    # Beside the zip, never inside it: inside would make bundle.sha256
    # self-referential and force a two-pass build for no gain.
    (DIST / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf8")

    _write_site_manifest(manifest)

    print()
    print(f"cases              : {counts['precedent_file_cases']}")
    print(f"  with sources     : {counts['cases_with_sources']}")
    if counts["cases_without_sources"]:
        print(f"  WITHOUT sources  : {', '.join(counts['cases_without_sources'])}")
    if counts["sections_without_cases"]:
        print(f"  sections with no numbered cases: {', '.join(counts['sections_without_cases'])}")
    print(f"apocrypha          : {apoc_entries} entries, {apoc_debunked} debunked")
    print(f"book ledger        : {ledger_count} precedents, P-01 to P-{ledger_max:02d}")
    print(f"source links       : {n_links} across {n_sourced_cases} headings")
    print(f"precedent file     : {len(document):,} chars")
    print(f"cover              : {cover_full.relative_to(ROOT)}"
          + (f" ({cover_dims[0]}x{cover_dims[1]})" if cover_dims else "")
          + (" [FALLBACK]" if cover_is_fallback else ""))
    print(f"bundle             : {zip_path}  ({zip_path.stat().st_size:,} bytes)")
    print(f"manifest           : {DIST / 'manifest.json'}")
    print(f"site manifest      : {SITE_MANIFEST.relative_to(ROOT)}")
    print()
    for f in files:
        print(f"  {f['bytes']:>12,}  {f['path']}")

    if "--upload" in sys.argv:
        return _upload(zip_path)
    print("\n(dry run. pass --upload to publish to Supabase Storage)")
    return 0


def _write_site_manifest(manifest: dict) -> None:
    """Project the manifest into an ESM module the site can import.

    Deliberately .js and not .json. scripts/check-offer-drift.mjs imports
    src/lib/offer.js in PLAIN NODE, not through Vite, and plain-Node ESM cannot
    import JSON without an import attribute. offer.js reads this file, so this
    file has to be a module. Same dict, one generator, so the two cannot
    disagree at generation time.
    """
    body = json.dumps(manifest, indent=2)
    SITE_MANIFEST.write_text(
        "/**\n"
        " * GENERATED BY scripts/build_bonus.py. DO NOT EDIT.\n"
        " *\n"
        " * The preorder bundle, described by a measurement of the bundle rather\n"
        " * than by prose. src/lib/offer.js derives its case count from here, the\n"
        " * /early-access page renders its file list from here, and the\n"
        " * confirmation email itemises from here. Regenerate with:\n"
        " *\n"
        " *   python3 scripts/sts.py bundle build\n"
        " *\n"
        " * This is the DEPLOY-TIME view of the bundle. It can only be stale\n"
        " * against the live object if someone uploads without deploying;\n"
        " * `python3 scripts/sts.py bundle verify --remote` is the check for that.\n"
        " */\n"
        f"export default Object.freeze({body});\n",
        encoding="utf8",
    )


def _env() -> dict:
    out = {}
    for line in (ROOT / ".env").read_text(encoding="utf8").split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _upload(zip_path: Path) -> int:
    """Replace the live bundle in place, keeping a dated backup.

    The storage path must not change: DOWNLOAD_BUNDLE_PATH in the production
    environment points at it, and every signed URL already in a customer's inbox
    resolves through it.
    """
    import datetime
    import json
    import urllib.error
    import urllib.request

    env = _env()
    base = env["SUPABASE_URL"]
    key = env.get("SUPABASE_SERVICE_KEY") or env["SUPABASE_SECRET_KEY"]
    bucket = env.get("DOWNLOAD_BUCKET", "downloads")
    name = env.get("DOWNLOAD_BUNDLE_PATH", "research-bundle-v1.zip")
    hdr = {"apikey": key, "Authorization": f"Bearer {key}"}

    def call(method, path, data=None, ctype=None, extra=None):
        h = dict(hdr)
        if ctype:
            h["Content-Type"] = ctype
        if extra:
            h.update(extra)
        req = urllib.request.Request(base + path, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    # 1. Pull the live bundle down and shelve a dated copy of it.
    status, current = call("GET", f"/storage/v1/object/{bucket}/{name}")
    if status != 200:
        print(f"error: could not download live bundle ({status})", file=sys.stderr)
        return 1
    stamp = datetime.datetime.now().strftime("%Y%m%d")
    backup = name.replace(".zip", f"-backup-{stamp}.zip")
    status, body = call(
        "POST", f"/storage/v1/object/{bucket}/{backup}", current,
        "application/zip", {"x-upsert": "true"},
    )
    print(f"backup {backup}: HTTP {status} ({len(current):,} bytes preserved)")
    if status not in (200, 201):
        print("  refusing to overwrite without a backup:", body[:200], file=sys.stderr)
        return 1

    # 2. Replace in place.
    new = zip_path.read_bytes()
    status, body = call(
        "POST", f"/storage/v1/object/{bucket}/{name}", new,
        "application/zip", {"x-upsert": "true"},
    )
    print(f"upload {name}: HTTP {status} ({len(new):,} bytes)")
    if status not in (200, 201):
        print("  upload failed:", body[:300], file=sys.stderr)
        return 1

    # 3. Prove it by fetching it back through a signed URL, exactly as a
    #    customer would, and opening the zip.
    status, body = call(
        "POST", f"/storage/v1/object/sign/{bucket}/{name}",
        json.dumps({"expiresIn": 300}).encode(), "application/json",
    )
    if status != 200:
        print("  signed url failed:", body[:200], file=sys.stderr)
        return 1
    signed = base + "/storage/v1" + json.loads(body)["signedURL"]
    with urllib.request.urlopen(signed, timeout=300) as r:
        fetched = r.read()
    check = DIST / "verify-roundtrip.zip"
    check.write_bytes(fetched)
    with zipfile.ZipFile(check) as z:
        bad = z.testzip()
        names = z.namelist()
    check.unlink()
    print(f"verified via signed URL: {len(fetched):,} bytes, {len(names)} entries, "
          f"integrity {'OK' if bad is None else 'CORRUPT: ' + bad}")
    return 0 if bad is None and len(fetched) == len(new) else 1


if __name__ == "__main__":
    sys.exit(main())
