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

BOOK_PDF = ROOT / "static" / "downloads" / "Surviving-the-Singularity-v0.7.2.pdf"
BOOK_EPUB = ROOT / "static" / "downloads" / "Surviving-the-Singularity-v0.7.2.epub"
MUNI_PDF = ROOT / "static" / "downloads" / "Municipal-Autonomy-Code.pdf"
COVER_FULL = ROOT / "art-raw" / "book-cover-final-source.png"
COVER_800 = ROOT / "static" / "images" / "optimized" / "surviving_the_singularity_cover_800.png"
COVER_400 = ROOT / "static" / "images" / "optimized" / "surviving_the_singularity_cover_400.png"

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

FRONT_MATTER = """---
title: "The Precedent File"
subtitle: "29 documented cases of people meeting a machine that changed everything"
author: "Companion research to *Surviving the Singularity*"
lang: en-GB
---

# The Precedent File

**29 documented cases of people meeting a machine that changed everything, and
what they did next.**

Companion research to *Surviving the Singularity*. Free with the preorder.

Every case below follows the same three beats: the story, the mechanism (the
reason it happened, not just the fact that it did), and the rule you can carry
out of it. Sources sit under each case. Where a famous version of a story is
embellished or fabricated, that is said plainly instead of quietly using it.

The final section, *Stories that are not true*, exists because the argument
this book makes attracts fake evidence. Eight of the most repeated anecdotes
about technology panic have no primary source. They are listed so you can stop
using them, with the documented alternative in each case.

"""

LEDGER_INTRO = """## The ledger

Every chapter of *Surviving the Singularity* closes with a precedent: a
documented case of people meeting a technological wave. They run P-01 to P-22
in order of appearance, so the weight accumulates as you read. This table maps
each one to its chapter in the book and to its full write-up below.

"""

APOCRYPHA_INTRO = """## Stories that are not true

These circulate constantly, usually in service of exactly the argument this
book is making. Every one of them is fabricated, unsourced, or materially
embellished. They are listed here so you can recognise them and reach for the
documented version instead, which is given in each entry.

Using a fake quote to make a true point hands the other side a free win. Do not
do it.

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


def _clean_body(raw: str) -> str:
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


def _extract_sources(text: str) -> str:
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
    out.append(f"*{n_links} sources across {n_cases} cases.*")
    return "\n".join(out), n_cases, n_links


def main() -> int:
    if not CASEBOOK.exists():
        print(f"error: {CASEBOOK} not found", file=sys.stderr)
        return 1

    raw = CASEBOOK.read_text(encoding="utf8")
    body, apocrypha = _clean_body(raw)
    apocrypha = _rewrite_apocrypha(apocrypha)

    document = FRONT_MATTER + body + "\n\n---\n\n" + apocrypha + "\n"
    document = _dedash(document)

    sources_md, n_cases, n_links = _extract_sources(document)
    sources_md = _dedash(sources_md)

    # Guard: nothing internal may ship.
    leaks = []
    for pat in INTERNAL_PATTERNS:
        for m in re.finditer(pat, document, flags=re.I):
            leaks.append(f"{pat!r} at char {m.start()}: ...{document[max(0,m.start()-60):m.start()+60]!r}...")
    if "—" in document or "—" in sources_md:
        leaks.append("em dash survived the de-dash pass")
    if leaks:
        print("REFUSING TO BUILD, internal content would leak:", file=sys.stderr)
        for l in leaks:
            print("  -", l, file=sys.stderr)
        return 1

    if STAGE.exists():
        shutil.rmtree(STAGE)
    (STAGE / "book").mkdir(parents=True)
    (STAGE / "extras").mkdir()
    (STAGE / "cover").mkdir()

    (STAGE / "The-Precedent-File.md").write_text(document, encoding="utf8")
    (STAGE / "Sources-and-Citations.md").write_text(sources_md, encoding="utf8")
    shutil.copy2(BONUS / "START-HERE.md", STAGE / "START-HERE.md")

    copies = [
        (BOOK_PDF, STAGE / "book" / "Surviving-the-Singularity.pdf"),
        (BOOK_EPUB, STAGE / "book" / "Surviving-the-Singularity.epub"),
        (MUNI_PDF, STAGE / "extras" / "Municipal-Autonomy-Code.pdf"),
        (COVER_FULL, STAGE / "cover" / "Surviving-the-Singularity-cover-full.png"),
        (COVER_800, STAGE / "cover" / "Surviving-the-Singularity-cover-800.png"),
        (COVER_400, STAGE / "cover" / "Surviving-the-Singularity-cover-400.png"),
    ]
    for src, dst in copies:
        if not src.exists():
            print(f"error: missing required asset {src}", file=sys.stderr)
            return 1
        shutil.copy2(src, dst)

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

    zip_path = DIST / "research-bundle-v1.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(STAGE.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(STAGE.parent))

    print()
    print(f"cases indexed : {n_cases}")
    print(f"sources        : {n_links}")
    print(f"precedent file : {len(document):,} chars")
    print(f"bundle         : {zip_path}  ({zip_path.stat().st_size:,} bytes)")
    print()
    with zipfile.ZipFile(zip_path) as z:
        for i in z.infolist():
            print(f"  {i.file_size:>12,}  {i.filename}")

    if "--upload" in sys.argv:
        return _upload(zip_path)
    print("\n(dry run. pass --upload to publish to Supabase Storage)")
    return 0


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
