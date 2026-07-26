# Book releases

Ledger of built book artifacts. `book.json` holds the version the source
currently claims; this file records which build is the one to hand someone.

---

## Latest build: v0.7.2 — the cover build

| | |
|---|---|
| **Version** | `0.7.2` |
| **Built** | 2026-07-26 12:12 |
| **From commit** | `dcd80e0` "book: export the art as an upload-ready pack, and name v0.7.1 stable" (2026-07-26), **plus uncommitted chapter edits** |
| **Sections** | 30 |
| **Pages** | 277 (v0.7.1 was 275; +1 cover, +1 reflow) |
| **Formats** | PDF 21.9 MB · EPUB 20.7 MB |

**What changed from v0.7.1:** the book has a real cover — the overgrown robot
under the tree, title and byline set into the art. Final source is
`sts-book-cover-001.jpg` (the pink-flower grade), now `scripts/book-cover.png`,
and it lands in both formats:

- **EPUB** — via the existing `--epub-cover-image` path.
- **PDF** — new. `scripts/book-cover-page.html` is injected with
  `--include-before-body`, styled full-bleed by the `@page cover` / `#cover-page`
  rules in `scripts/book-print.css`. Before v0.7.2 the PDF opened on a text title
  block and had no cover at all.

Two things the source file needed before it could bleed properly:

1. **Baked-in letterbox.** The delivered file ships 1410x2250 with 97px of solid
   black at the top and bottom. Cropped to 1410x2056 on the way in, or those bands
   would have printed as bars across the cover. Every render in this series has
   carried the same bands — crop before installing any future one.
2. **Framing.** The cropped art is 0.686 against letter's 0.773, so cover-fit trims
   ~231px of height. `object-position: top` puts all of that trim in the empty grass
   at the bottom; a centered crop would have left the title only 77px off the trim
   edge. The title occupies 9.3%-22.3% of art height and is untouched.

The cover page also carries a negative margin to cancel the UA default 8px `body`
margin — without it the art stopped short of three page edges. Scoped to the cover
element so the other 276 pages don't reflow.

Verified by rendering page 1: correct spelling, byline intact, image content on all
four page edges.

**Art lineage** (kept in `art-raw/`, which is not tracked):

- `book-cover-final-source.png` — the shipped cover, cropped, 1410x2056. Pink/salmon
  flower grade, from `~/Downloads/sts-book-cover-001.jpg`
- `book-cover-orange-flowers-variant.png` — same composition, orange flower grade,
  from `sts-cover-by-ct.PNG`. Correct title; passed over on colour
- `book-cover-finalist-02-source.png` — earlier pick, 1856x2464; **the title on it
  misspells "SINGULARTY"**, superseded, do not use
- `book-cover-v0.7.1-archived.png` — the red-brain cover this replaced

Note the shipped art is 1410px wide — about 166dpi across a letter page. Fine for a
review build and for EPUB; a print run wants a higher-resolution render.

**Artifacts** (`book-build/` is gitignored):

- `book-build/Surviving-the-Singularity-v0.7.2.pdf`
- `book-build/Surviving-the-Singularity-v0.7.2.epub`

Built from a dirty tree — five chapter files plus the art catalog and manuscript
index carried uncommitted edits at build time, so this build is not reproducible
from `dcd80e0` alone.

---

## Current stable: v0.7.1

| | |
|---|---|
| **Version** | `0.7.1` |
| **Built** | 2026-07-21 08:11 |
| **From commit** | `b85e8a5` "book: illustrated field guide, second wave — 9 chapters + 4 minor cast" (2026-07-21 08:05) |
| **Sections** | 30 |
| **Formats** | PDF 17.9 MB · EPUB 17.0 MB |
| **Marked stable** | 2026-07-26 |

**Artifacts** live in `book-build/`, which is gitignored, so they are not in
this repo:

- `book-build/Surviving-the-Singularity-v0.7.1.pdf`
- `book-build/Surviving-the-Singularity-v0.7.1.epub`
- `manuscript/StS-Complete-Draft-compiled-2026-07-21.md` (tracked; the compiled
  markdown those two were rendered from, written at the same 08:11)

A packaged copy of all three, plus the full art pack, sits at
`~/Desktop/StS-v0.7.1-Package/`.

### Two things to know before treating this as a frozen release

1. **The source has moved past the build.** Four commits touch
   `src/lib/data/book/` after `b85e8a5`, and the working tree usually carries
   further uncommitted chapter edits from chapter-agent sessions. Rebuilding
   today will not reproduce the v0.7.1 artifacts. The compiled markdown above
   is the exact snapshot; the chapter files are not.
2. **The version commit says "wip".** `e611a32` is titled "book: v0.7.1 wip".
   v0.7.1 was declared stable after the fact, on 2026-07-26, because it is the
   build worth handing out, not because the source was frozen at it.

---

## Prior builds

Every build in `book-build/`, by file date. All are PDF plus EPUB unless noted.

| Version | Built |
|---|---|
| v0.7.2 | 2026-07-26 (first build with a real cover in both formats) |
| v0.7.1 | 2026-07-21 |
| v0.7.0 | 2026-07-20 |
| v0.6.2 | 2026-07-19 |
| v0.6.1 | 2026-07-19 |
| v0.6.0 | 2026-07-19 |
| v0.5.2 | 2026-07-19 (also `-DELUXE` and `-PLAIN` PDF cuts) |
| v0.5.1 | 2026-07-19 |
| v0.5.0 | 2026-07-19 |
| v0.3.1 | 2026-07-18 |
| v0.3.0 | 2026-07-18 |
| DRAFT | 2026-07-18 |
| 5.5 | 2026-07-12 |
| 5.4 | 2026-07-12 |
| DRAFT_5.3 | 2026-07-11 |
| DRAFT_5.2 | 2026-07-11 |
| DRAFT_7 | 2026-06-12 |

The pre-v0.3.0 names are inconsistent because they predate the versioning
convention. Do not read `5.4` as newer than `v0.5.0`; it is older.

---

## Art pack

The book's 83 figures export as a flat, upload-ready folder for image and video
tools:

```bash
python3 scripts/sts.py flow --out ~/Desktop/StS-Flow-Assets
```

22 licensed photographs, 19 original pixel-art plates, 3 part banners, and 39
SVG diagrams rasterized to opaque PNG. Ships with a MANIFEST.md whose per-asset
prompt is the figure's alt text, a CREDITS.txt covering the photographs that
carry an attribution obligation, and a machine-readable flow-manifest.json.

The pack is generated, not stored. It is not committed here because the source
images already live in `static/book-images/` and the manifests derive from the
manuscript index plus `credits.json`.
