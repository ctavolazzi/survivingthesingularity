# The novel: the site's book

Since 2026-11-17 *Surviving the Singularity* is a novel, and this directory is
what `/book`, `/read` and `/sample` serve. `book.json` sets the order of the
Markdown files beside it.

## Where these files come from

They are **generated**. The manuscript reached the site as the author's typeset
PDF ("final rough draft", 258 pages), not as source files, so
`scripts/novel_from_pdf.py` reads the PDF and writes:

- `*.md` and `book.json` here
- `image-dimensions.json` here
- `static/book-images/novel-p###.webp` (the number is the PDF page)

Do not hand-edit the Markdown: the next run replaces it. To take a revised
manuscript:

```sh
pip install pymupdf pillow
python3 scripts/novel_from_pdf.py path/to/new.pdf --date YYYY-MM-DD --edition "Final"
git diff --stat src/lib/data/novel
```

Then read the diff, rebuild, and run the checks in the repository guide. If the
chapter titles change, `src/lib/novelActs.js` and the browser tests that name
"Chapter 0: The Demonstration" and "Chapter 1" need the same change.

## What is not here yet

- **Downloads.** The novel has no PDF or EPUB on the site and none in the paid
  bundle. The bundle a buyer is emailed (`src/lib/data/bundleManifest.js`)
  still holds the earlier nonfiction draft and The Precedent File. Replacing it
  is a release step with its own runbook (`publication/PRIVATE-BUNDLE.md`,
  `docs/payment-reliability-rollout.md`).
- **A fact-check trace.** `/factcheck` covers the earlier draft only.

## The earlier draft

The nonfiction draft (v0.11.0) is untouched in `src/lib/data/book/`, with its
publication pipeline and its files in `static/downloads/`. It is served at
`/archive` for the people who preordered it, because the offer told them the
archive stays readable (`src/lib/offer.js`, `evolution` and `foreverScope`).
