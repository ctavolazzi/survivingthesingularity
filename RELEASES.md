# Book releases

Ledger of built book artifacts. `book.json` holds the version the source
currently claims; this file records which build is the one to hand someone.

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
