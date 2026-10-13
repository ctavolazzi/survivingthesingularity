# Publication production files

Current local edition: **v0.11.0**. Five sections clarify the title, ownership, participation, and solarpunk, with new source notes. All scenes and artwork remain. See [edition notes](../docs/v0.11.0/EDITION-NOTES.md), [source preservation](../docs/v0.11.0/source-preservation.json), and [delivery hashes](../docs/v0.11.0/deliverables.json).

## Build and verify

Requirements: Node dependencies from `npm ci`; Python 3 with WeasyPrint, Beautiful Soup, pypdf, Pillow and Playwright; Pandoc; Ghostscript; Chrome. Fonts and licenses are bundled in `assets/fonts`.

Canonical source is `src/lib/data/book/`, ordered by `book.json`. Frozen hashes in `docs/publication/baseline.json` must match all 35 sections and the manifest. Source preservation compares this edition against `book-v0.10.4` at `bdf0584`. Review source changes and permanent block-ID assignments before updating the freeze. Historical production scripts are reused through small wrappers; previous-edition findings are not new verification.

Run from the repository root:

```sh
export DAILY_NOTE_AGENT=codex
python3 scripts/sts.py verify
python3 scripts/sts.py id verify
python3 docs/v0.11.0/check_source_preservation.py
node scripts/render-book-scenes.mjs --check
python3 docs/v0.9.2/print_figures.py --verify
python3 docs/v0.11.0/build.py
python3 docs/v0.11.0/check_pdf.py
python3 publication/check_pdf_resources.py
python3 docs/v0.11.0/check_epub.py
python3 docs/v0.11.0/prove_epub_layout.py
python3 docs/v0.11.0/prove_epub_additions.py
python3 docs/v0.11.0/render_samples.py
# Inspect the fresh PDF raster samples and EPUB screenshots before acceptance.
python3 docs/v0.11.0/finalize.py
```

For an additional editable package, run the following after finalizing the audit notes:

```sh
python3 docs/v0.11.0/check_package.py
python3 publication/package.py --check
python3 publication/package.py
python3 docs/v0.11.0/finalize.py --include-package
```

The package exporter refuses to overwrite an existing ZIP. A PDF rebuild changes output hashes: repeat output proofs and visual review before preparing a new handoff. Finalization preserves existing differing delivery files. Its normal deliveries are reading PDF, grayscale interior, front cover, EPUB, and compiled Markdown. The optional sixth delivery is the editable ZIP.

The print resolver's `--verify` mode checks source/print hashes and a deliberate collision fixture without writing files. Its older default and `--check` modes regenerate legacy variants with browser-dependent font fitting. Final production uses `--verify` to preserve reviewed artwork.

## Artwork, prose, and permanent IDs

All 110 image references and 62 registered figures remain. No image or caption changes in this edition. The asset source and generation records remain under `docs/v0.10.1/`, `docs/v0.10.2/` and `docs/v0.10.3/`. Do not run historical artwork generators over reviewed assets.

The source check verifies unchanged original blocks in order, with the exact approved moral-call replacement as its sole exception. It also verifies citation continuity, scene markers, asset bytes, and permanent IDs independently of the live parser. All 2,303 inherited IDs remain, including `sts.conclusion.b0081` on the revised moral call. Twenty-eight new IDs bring the total to 2,331. The corrected positional-assignment defect is documented in the edition notes.

## Proof and handoff

Current automated receipts are under `docs/v0.11.0/`: `source-preservation.json`, `pdf-checks.json`, `epub-checks.json`, `epub-proof/checks.json`, and `epub-proof/additions.json`. Raster sample mapping is `pdf-proof/final-samples.json`. [Edition notes](../docs/v0.11.0/EDITION-NOTES.md) link the visual and browser findings. Automated PDF geometry/text checks are in `output/proof/checks.json`; resource checks are in `docs/publication/PDF-RESOURCE-CHECKS.json`.

PDF proof uses plain extraction first and layout extraction from matching PDF pages for otherwise missing blocks. A combining glyph in the cooling caption requires that fallback. The method reads only PDF bytes and rejects deliberately removed middle text. Separate raster inspection checks visible appearance.

Publication outputs include `output/Surviving-the-Singularity-{reading,interior,print-interior,front-cover}.pdf`, and, when prepared, the versioned editable ZIP and `package-v0.11.0/`. Versioned delivery copies are in `book-build/`; compiled Markdown is in `manuscript/`. The package includes portable HTML/CSS, artwork, fonts and notices, canonical source snapshots, audits and PDFs. Repository history, environment files and proof-image clutter are excluded.

## Scope

### Public digital downloads

The launch branch publishes v0.11.0 as compact digital reading copies. Run:

```sh
python3 scripts/prepare-book-downloads.py
node --test scripts/book-downloads.test.mjs
npm run book:release
```

For an EPUB stylesheet correction after a proved release, use
`python3 scripts/prepare-book-downloads.py --epub-only`. It rebuilds and proves
the EPUB from canonical source and retains the exact PDF bytes only when the
prior source, PDF master, artwork and PDF layout hashes still match. Recheck
the resulting EPUB with EPUBCheck and inspect narrow-screen and enlarged-text
reading before running `npm run book:release` and rebuilding the private ZIP.
`node scripts/check-epub-reflow.mjs` renders all shipped chapters at 320 and
768 pixels with 18 and 28 pixel text, and fails on horizontal page overflow or
missing images. It requires the installed Playwright Chromium browser and
Python's standard library. An optional first argument selects a candidate EPUB;
`EPUB_REFLOW_BROWSER=firefox` or `EPUB_REFLOW_BROWSER=webkit` selects another
installed browser engine. Contained table panning is checked separately from
whole-page overflow. Browser rendering does not certify paginated e-reader apps.

Python package versions used for this release are in `requirements.txt`.
The preparation script builds the existing publication masters and EPUB from
the frozen canonical source, proves their text and resources, and creates
distribution copies under `book-build/downloads/`. The PDF uses 160 dpi raster
images with selectable text and retained links; EPUB photographs use a maximum
1600-pixel edge and JPEG quality 85. Vector diagrams and transparent artwork
remain unchanged in the EPUB. Original source artwork and full-size masters
are preserved. This is a digital reading format, not a print master.

`publication/book-downloads.json` binds the shipped files to their exact hashes,
source edition, artwork and layout inputs. The prebuild guard rejects altered/stale files, files at
the 25 MiB Pages ceiling, and leftover public book editions. The `released`
field is ignored only for the manifest's content hash, because publishing
changes that distribution pointer. Versioned old URLs and stable aliases
redirect to the current files; previous bytes remain in git history.

After a rebuild, inspect representative pages, including diagrams, photos,
transparent art and links. Passing automated checks does not constitute a
physical print proof or a device-specific e-reader test. These public downloads
do **not** update the paid Supabase ZIP: rebuild, separately publish and verify
that storage object before claiming its convenience copies are current. To
prepare an isolated versioned ZIP and candidate manifest without changing
the site's active bundle manifest, run `python3 scripts/prepare-book-bundle.py`.
It requires Pandoc and XeLaTeX and embeds the bundled Source Sans Pro font.
Its `preparation.json` records the remaining review and storage deployment gates.

This pass verifies new editorial claims and source preservation; it is not a complete reread of inherited claims. Four retained narrative plates depict fiction. Six retained photo-derived cutouts are generated adaptations with separate credits. Existing cover provenance and epigraph questions remain in the [quotation and cover review](../docs/publication/QUOTATIONS-v0.10.0.md). Physical print proof, printer-specific wrap production and dedicated e-reader pagination remain separate from local digital checks.
