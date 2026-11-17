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

## The download a buyer gets

`scripts/build_novel_downloads.py <the same PDF>` builds it, under
`book-build/novel-<version>/` (git-ignored):

- an **EPUB** made from these chapter files with pandoc (pictures as JPEG, a
  written description on every picture, accessibility metadata, checked with
  W3C EPUBCheck);
- the **author's PDF**, byte for byte;
- a short **START-HERE** page;
- the **ZIP** that holds them, plus `manifest.json`, a candidate
  `bundleManifest.js`, and `build.json` (what was checked, what is left).

The build is deterministic: the same inputs give the same SHA-256.

`src/lib/data/bundleManifest.js` on this branch is the candidate from the
2026-11-17 draft. **The ZIP it describes has not been uploaded anywhere.**
Checkout refuses to take money unless the hosting settings name the same
object, version and SHA-256 (`src/lib/bundleRelease.js`), so a deploy without
the upload fails closed: the buy button reports that checkout is unavailable.

### Releasing a draft or the finished book

1. `python3 scripts/novel_from_pdf.py new.pdf --date YYYY-MM-DD --edition "..."`
   (add `--version 1.0.0` for the finished book), review the diff.
2. `python3 scripts/build_novel_downloads.py new.pdf`, read `build.json`.
3. Open the EPUB on a phone and an e-reader. EPUBCheck proves the file is
   well-formed, not that it reads well.
4. Upload the ZIP to the private `downloads` bucket; confirm the stored bytes
   match the SHA-256 (`node scripts/deploy-book-bundle.mjs`, read-only by default).
5. Copy the candidate `bundleManifest.js` over `src/lib/data/bundleManifest.js`.
6. Set `DOWNLOAD_BUNDLE_PATH`, `DOWNLOAD_BUNDLE_SHA256` and
   `DOWNLOAD_BUNDLE_BOOK_VERSION` in the hosting settings to the same values.
7. Run the release checks, deploy, make one test-mode purchase and open the
   files from the email.

Buyers who already have a link get the new bundle from it: the receipt page
mints a fresh link to whatever bundle is current.

### Not done

- **No screen reader has been used on the EPUB**, and the PDF is not tagged.
  The EPUB's metadata says so and claims no conformance.
- **`/factcheck`** covers the earlier draft only.
- The book has **no copyright page**; the EPUB carries a rights line in its
  metadata only.

## The earlier draft

The nonfiction draft (v0.11.0) is untouched in `src/lib/data/book/`, with its
publication pipeline and its files in `static/downloads/`. It is served at
`/archive` for the people who preordered it, because the offer told them the
archive stays readable (`src/lib/offer.js`, `evolution` and `foreverScope`).
The bonus file they were delivered, The Precedent File, is on `/archive` too,
from `src/lib/data/archive/`.
