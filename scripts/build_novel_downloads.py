#!/usr/bin/env python3
"""Build what a buyer of the novel downloads: an EPUB, the author's PDF, and the
paid ZIP that holds both, with a manifest the site can describe it from.

    python3 scripts/build_novel_downloads.py path/to/manuscript.pdf

Run it after scripts/novel_from_pdf.py on the SAME PDF, so the EPUB (made from
the site's chapter files) and the PDF are the same draft.

WHAT IT MAKES, all under book-build/novel-<version>/ (git-ignored):

  Surviving-the-Singularity/                 the folder a buyer unzips
    START-HERE.html, START-HERE.md           how to open the files
    book/Surviving-the-Singularity.pdf       the author's own typeset PDF, byte for byte
    book/Surviving-the-Singularity.epub      built here with pandoc, for e-readers
    cover/Surviving-the-Singularity-cover.png
  surviving-the-singularity-novel-v<version>.zip
  manifest.json, bundleManifest.js           candidates; the live manifest is NOT touched
  build.json                                 what was checked, and what is left to do

WHAT IT DOES NOT DO: upload anything, or change src/lib/data/bundleManifest.js.
Activating a bundle is a release step: see src/lib/data/novel/README.md.

THE EPUB
  - EPUB 3, reflowable, one file per chapter, built by pandoc from
    src/lib/data/novel in book.json order.
  - Pictures are converted to JPEG: WebP only became a core EPUB type in 3.3 and
    older readers do not open it.
  - Every picture carries a written description (the alt text the converter
    wrote) and its caption stays as text under it.
  - Accessibility metadata is written into the package file and says only what
    is true of this file. No conformance claim is made: nobody has tested it
    with a screen reader. `build.json` records that.
  - Checked with W3C EPUBCheck when the `epubcheck` Python package is
    installed (pip install epubcheck; needs Java). A failure stops the build.

THE ZIP is deterministic: same inputs, same pandoc, same bytes. Entries are
sorted and stamped with the book's own date.

Needs: pandoc, pip install pillow pymupdf epubcheck, node (to read the offer text).
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
NOVEL = ROOT / "src/lib/data/novel"
IMAGES = ROOT / "static/book-images"
COVER = ROOT / "static/Surviving-the-Singularity-Cover.png"
FOLDER = "Surviving-the-Singularity"
BUCKET = "downloads"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def site_text() -> dict:
    """The offer and notice strings, read from the site's own modules so the
    file a buyer opens cannot disagree with the page they bought on."""
    code = (
        "import { offer, license } from './src/lib/offer.js';"
        "import { bookNotice } from './src/lib/bookNotice.js';"
        "console.log(JSON.stringify({ license: license.full, fiction: bookNotice.fiction,"
        " intent: bookNotice.intent, contact: offer.refund.contact, refundDays: offer.refund.windowDays }));"
    )
    out = run(["node", "--input-type=module", "-e", code], cwd=ROOT, capture_output=True, text=True).stdout
    return json.loads(out)


def build_epub(book: dict, work: Path, out: Path, epoch: int) -> dict:
    src = work / "epub-src"
    (src / "img").mkdir(parents=True)
    parts, pictures, described = [], 0, 0
    for section in book["sections"]:
        text = (NOVEL / section["file"]).read_text()

        def picture(match):
            nonlocal pictures, described
            alt, name = match.group(1), Path(match.group(2)).stem
            jpg = src / "img" / f"{name}.jpg"
            if not jpg.exists():
                Image.open(IMAGES / f"{name}.webp").convert("RGB").save(jpg, "JPEG", quality=85, optimize=True)
            pictures += 1
            described += bool(alt.strip()) and alt.strip() != "Illustration"
            return f"![{alt}](img/{name}.jpg)"

        text = re.sub(r"!\[([^\]]*)\]\(/book-images/([^)]+)\)", picture, text)
        parts.append(text.rstrip() + "\n")
    (src / "book.md").write_text("\n\n".join(parts))

    cover = src / "cover.jpg"
    Image.open(COVER).convert("RGB").save(cover, "JPEG", quality=88, optimize=True)
    (src / "book.css").write_text(
        "body { line-height: 1.5; }\n"
        "h1 { text-align: center; margin: 2em 0 1.5em; page-break-before: always; }\n"
        "p { margin: 0 0 0.9em; }\n"
        "hr { border: 0; text-align: center; margin: 1.6em 0; }\n"
        "hr::before { content: '\\2022\\00a0\\00a0\\2022\\00a0\\00a0\\2022'; }\n"
        "img { max-width: 100%; height: auto; display: block; margin: 1.2em auto 0.4em; }\n"
        "blockquote { margin: 1.2em 1.5em; font-style: italic; }\n"
    )
    identifier = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://survivingthesingularity.com/novel/{book['version']}"))
    meta = {
        "title": [{"type": "main", "text": book["title"]}, {"type": "subtitle", "text": book["subtitle"]}],
        "creator": [{"role": "author", "text": book["author"]}],
        "identifier": identifier,
        "lang": "en-US",
        "date": book["lastUpdated"],
        "rights": f"Copyright {book['lastUpdated'][:4]} {book['author']}. All rights reserved.",
        "description": "A novel.",
    }
    (src / "meta.json").write_text(json.dumps(meta))
    epub = out / "Surviving-the-Singularity.epub"
    env = dict(os.environ, SOURCE_DATE_EPOCH=str(epoch))
    run([
        "pandoc", "book.md", "-f", "markdown-implicit_figures-smart", "-t", "epub3", "-o", str(epub),
        "--metadata-file", "meta.json", "--css", "book.css", "--epub-cover-image", "cover.jpg",
        "--split-level", "1", "--toc-depth", "1", "--epub-title-page=true",
    ], cwd=src, env=env)
    add_accessibility_metadata(epub, epoch, pictures)
    return {"pictures": pictures, "pictures_described": described, "identifier": identifier}


A11Y_SUMMARY = (
    "A reflowable novel with a table of contents and a heading for every chapter. "
    "Each of its pictures has a written description. It has not been tested with "
    "screen readers, and no accessibility conformance is claimed."
)


def add_accessibility_metadata(epub: Path, epoch: int, pictures: int) -> None:
    """Write schema.org accessibility metadata into the package file, then repack
    the EPUB deterministically (mimetype first and stored, the rest sorted)."""
    stamp = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).timetuple()[:6]
    with zipfile.ZipFile(epub) as z:
        files = {n: z.read(n) for n in z.namelist()}
    opf_name = next(n for n in files if n.endswith(".opf"))
    opf = files[opf_name].decode()
    features = ["tableOfContents", "readingOrder", "structuralNavigation", "displayTransformability"]
    if pictures:
        features.insert(0, "alternativeText")
    metas = (
        ['<meta property="schema:accessMode">textual</meta>']
        + (['<meta property="schema:accessMode">visual</meta>'] if pictures else [])
        + ['<meta property="schema:accessModeSufficient">textual</meta>']
        + [f'<meta property="schema:accessibilityFeature">{f}</meta>' for f in features]
        + ['<meta property="schema:accessibilityHazard">none</meta>',
           f'<meta property="schema:accessibilitySummary">{html.escape(A11Y_SUMMARY)}</meta>']
    )
    assert "</metadata>" in opf
    opf = opf.replace("</metadata>", "    " + "\n    ".join(metas) + "\n  </metadata>", 1)
    files[opf_name] = opf.encode()
    tmp = epub.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w") as z:
        info = zipfile.ZipInfo("mimetype", stamp)
        z.writestr(info, files.pop("mimetype"), compress_type=zipfile.ZIP_STORED)
        for name in sorted(files):
            info = zipfile.ZipInfo(name, stamp)
            info.external_attr = 0o644 << 16
            z.writestr(info, files[name], compress_type=zipfile.ZIP_DEFLATED)
    tmp.replace(epub)


def epubcheck(epub: Path) -> dict:
    try:
        from epubcheck import EpubCheck
    except ImportError:
        return {"ran": False, "reason": "the epubcheck package is not installed"}
    result = EpubCheck(str(epub))
    messages = [f"{m.level} {m.id} {m.location}: {m.message}" for m in result.messages]
    errors = [m for m in messages if m.startswith(("ERROR", "FATAL"))]
    if errors:
        raise SystemExit("EPUBCheck failed:\n" + "\n".join(errors[:20]))
    return {"ran": True, "valid": bool(result.valid), "errors": 0,
            "warnings": [m for m in messages if m.startswith("WARNING")]}


def start_here(book: dict, text: dict) -> tuple[str, str]:
    e = html.escape
    title, author, edition = book["title"], book["author"], book["edition"]
    md = f"""# {title}

A novel by {author}. {edition}, dated {book['lastUpdated']}.

## The two files

- `book/Surviving-the-Singularity.epub` is the one for an e-reader, a phone or a tablet. The text resizes to fit your screen.
- `book/Surviving-the-Singularity.pdf` is the book laid out page by page, as designed. Best on a computer, or printed.

They are the same book.

## Opening the EPUB

- iPhone, iPad or Mac: open the file and choose Books.
- Android: open it with Google Play Books (in Play Books, Library, Upload files) or any reading app.
- Kindle: use Amazon's Send to Kindle page or app and choose the EPUB. It arrives in your Kindle library.
- Kobo and other e-readers: connect the reader to a computer and copy the EPUB onto it.

## Reading it online

The same book is on the site at https://survivingthesingularity.com/book. The password is in your purchase email.

## This is the current draft

When the finished book publishes, you get it at no extra cost. We email you when it is ready.

## What you have

{text['license']}

{text['fiction']} {text['intent']}

## Help

Email {text['contact']} from the address you bought with. Digital purchases can be refunded within {text['refundDays']} days.
"""
    paragraphs = []
    for block in md.strip().split("\n\n"):
        if block.startswith("# "):
            paragraphs.append(f"<h1>{e(block[2:])}</h1>")
        elif block.startswith("## "):
            paragraphs.append(f"<h2>{e(block[3:])}</h2>")
        elif block.startswith("- "):
            items = "".join(f"<li>{inline(e(line[2:]))}</li>" for line in block.split("\n"))
            paragraphs.append(f"<ul>{items}</ul>")
        else:
            paragraphs.append(f"<p>{inline(e(block))}</p>")
    page = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{e(title)}: start here</title>\n"
        "<style>body{font:18px/1.6 Georgia,serif;max-width:40em;margin:0 auto;padding:1.5em;color:#111;background:#fff}"
        "h1{font-size:1.7em}h2{font-size:1.15em;margin-top:1.8em}code{font-family:ui-monospace,Menlo,monospace;font-size:.9em}"
        "a{color:#0b57d0}@media(prefers-color-scheme:dark){body{color:#eee;background:#111}a{color:#8ab4f8}}</style>\n"
        "</head>\n<body>\n<main>\n" + "\n".join(paragraphs) + "\n</main>\n</body>\n</html>\n"
    )
    return page, md


def inline(escaped: str) -> str:
    """Backticked file names become links to the files beside this page; bare
    https links and the email address become links too."""
    escaped = re.sub(r"`(book/[^`]+)`", r'<a href="\1"><code>\1</code></a>', escaped)
    escaped = re.sub(r"(https://[^\s<]+[^\s<.])", r'<a href="\1">\1</a>', escaped)
    return re.sub(r"([\w.+-]+@[\w-]+\.[\w.]+[\w])", r'<a href="mailto:\1">\1</a>', escaped)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    args = ap.parse_args()
    book = json.loads((NOVEL / "book.json").read_text())
    version = book["version"]
    epoch = int(datetime.datetime.fromisoformat(book["lastUpdated"] + "T00:00:00+00:00").timestamp())
    stamp = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).timetuple()[:6]

    out = ROOT / "book-build" / f"novel-{version}"
    if out.exists():
        shutil.rmtree(out)
    stage = out / FOLDER
    (stage / "book").mkdir(parents=True)
    (stage / "cover").mkdir()

    # The PDF goes in exactly as the author made it.
    import pymupdf
    pages = pymupdf.open(args.pdf).page_count
    shutil.copyfile(args.pdf, stage / "book" / "Surviving-the-Singularity.pdf")
    shutil.copyfile(COVER, stage / "cover" / "Surviving-the-Singularity-cover.png")

    epub_facts = build_epub(book, out, stage / "book", epoch)
    check = epubcheck(stage / "book" / "Surviving-the-Singularity.epub")
    shutil.rmtree(out / "epub-src")

    text = site_text()
    page, md = start_here(book, text)
    (stage / "START-HERE.html").write_text(page)
    (stage / "START-HERE.md").write_text(md)

    labels = {
        "START-HERE.html": ("Start here, how to open the files (web page)", "html"),
        "START-HERE.md": ("Start here, how to open the files (plain text)", "md"),
        "book/Surviving-the-Singularity.epub": (f"{book['title']}, the novel, {book['edition'].lower()} (EPUB, for e-readers)", "epub"),
        "book/Surviving-the-Singularity.pdf": (f"{book['title']}, the novel, {book['edition'].lower()} (PDF, {pages} pages)", "pdf"),
        "cover/Surviving-the-Singularity-cover.png": ("Cover art", "png"),
    }
    files = []
    name = f"surviving-the-singularity-novel-v{version}.zip"
    with zipfile.ZipFile(out / name, "w") as z:
        for rel in sorted(labels):
            path = stage / rel
            info = zipfile.ZipInfo(f"{FOLDER}/{rel}", stamp)
            info.external_attr = 0o644 << 16
            # The book files are already compressed; storing them keeps the build fast and exact.
            method = zipfile.ZIP_STORED if rel.endswith((".pdf", ".epub", ".png")) else zipfile.ZIP_DEFLATED
            z.writestr(info, path.read_bytes(), compress_type=method)
            label, fmt = labels[rel]
            files.append({"path": f"{FOLDER}/{rel}", "label": label, "format": fmt, "role": "primary",
                          "bytes": path.stat().st_size, "sha256": sha256(path)})
    with zipfile.ZipFile(out / name) as z:
        assert z.testzip() is None and len(z.namelist()) == len(labels)

    manifest = {
        "schema": 1,
        "generated_at": datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "scripts/build_novel_downloads.py",
        "kind": "novel",
        "bundle": {"root": FOLDER, "object": name, "bucket": BUCKET, "bytes": (out / name).stat().st_size,
                   "sha256": sha256(out / name), "entries": len(files)},
        "book": {"version": version, "title": book["title"], "subtitle": book["subtitle"],
                 "edition": book["edition"], "last_updated": book["lastUpdated"], "pdf_pages": pages},
        # The earlier bundle was built around a research file and counted its
        # cases here. The novel's bundle has none; src/lib/offer.js reads the
        # absence as "no Precedent File in what is sold today".
        "counts": {},
        "files": files,
        "inputs": [{"path": "src/lib/data/novel/book.json", "sha256": sha256(NOVEL / "book.json")},
                   {"path": "author PDF (not in the repository)", "sha256": sha256(args.pdf)}],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (out / "bundleManifest.js").write_text(
        "/**\n * GENERATED BY scripts/build_novel_downloads.py. DO NOT EDIT.\n *\n"
        " * The paid download, described by a measurement of the ZIP rather than by\n"
        " * prose. The confirmation email itemises from here, the receipt page and\n"
        " * src/lib/offer.js read from here, and checkout refuses to take money unless\n"
        " * the deployment names this exact object, version and SHA-256.\n *\n"
        " * Rebuild with: python3 scripts/build_novel_downloads.py <the author's PDF>\n */\n"
        "export default Object.freeze(" + json.dumps(manifest, indent=2) + ");\n"
    )
    record = {
        "status": "built locally; not uploaded; the live site manifest is unchanged",
        "object": name, "bytes": manifest["bundle"]["bytes"], "sha256": manifest["bundle"]["sha256"],
        "book_version": version, "pdf_pages": pages, "epub": epub_facts, "epubcheck": check,
        "accessibility": {"claim": "none", "summary": A11Y_SUMMARY,
                          "not_done": ["screen reader test", "the PDF is not tagged for accessibility"]},
        "to_release": [
            f"Upload {name} to the '{BUCKET}' storage bucket and confirm the uploaded bytes match the SHA-256 above.",
            "Copy bundleManifest.js from this folder to src/lib/data/bundleManifest.js and commit it.",
            f"Set DOWNLOAD_BUNDLE_PATH={name}, DOWNLOAD_BUNDLE_SHA256=<the SHA-256>, "
            f"DOWNLOAD_BUNDLE_BOOK_VERSION={version} in the hosting settings.",
            "Deploy, then make one test-mode purchase and open the files from the email.",
        ],
    }
    (out / "build.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
