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

The public-download release remains v0.7.5. This is a local digital edition. Earlier worktrees and deliveries remain preserved.

This pass verifies new editorial claims and source preservation; it is not a complete reread of inherited claims. Four retained narrative plates depict fiction. Six retained photo-derived cutouts are generated adaptations with separate credits. Existing cover provenance and epigraph questions remain in the [quotation and cover review](../docs/publication/QUOTATIONS-v0.10.0.md). Physical print proof, printer-specific wrap production and dedicated e-reader pagination remain separate from local digital checks.
