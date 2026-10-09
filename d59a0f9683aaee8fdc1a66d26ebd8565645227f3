# Publication production files

Current local edition: **v0.10.4**. A complete reread led to 18 small revisions in 16 sections. All scenes and artwork remain. Reading PDF: 411 pages. Print interior: 410 pages, with no extra final verso. See [edition notes](../docs/v0.10.4/EDITION-NOTES.md) and [delivery hashes](../docs/v0.10.4/deliverables.json).

## Build and verify

Requirements: Node dependencies from `npm ci`; Python 3 with WeasyPrint, Beautiful Soup, pypdf, Pillow and Playwright; Pandoc; Ghostscript; Chrome. Fonts and licenses are bundled in `assets/fonts`.

Canonical source is `src/lib/data/book/`, ordered by `book.json`. Frozen hashes in `docs/publication/baseline.json` must match all 35 sections and the manifest. `docs/v0.10.4/baseline.json` separately records the preserved v0.10.3 reference edition. Review and record source changes before updating the freeze.

Run from the repository root:

```sh
export DAILY_NOTE_AGENT=codex
python3 scripts/sts.py verify
python3 scripts/sts.py id verify
python3 docs/v0.10.4/check_review.py
python3 docs/v0.10.4/gates.py
node scripts/render-book-scenes.mjs --check
python3 docs/v0.9.2/print_figures.py --verify
python3 docs/v0.10.4/build.py
python3 publication/proof.py
python3 publication/check_pdf_resources.py
python3 docs/v0.10.4/check_epub.py
python3 docs/v0.10.4/prove_epub_layout.py
python3 docs/v0.10.4/render_samples.py
python3 docs/v0.10.4/check_package.py
python3 publication/package.py --check
python3 publication/package.py
python3 docs/v0.10.4/finalize.py
```

The package exporter refuses to overwrite an existing ZIP. A PDF rebuild changes output hashes: repeat output proofs and visual review, and preserve the existing package before preparing a separate handoff. Finalization requires current review receipts. Its six deliveries include reading PDF, grayscale interior, front cover, EPUB, compiled Markdown and editable ZIP.

The print resolver's `--verify` mode checks source/print hashes and a deliberate collision fixture without writing files. Its older default and `--check` modes regenerate legacy variants with browser-dependent font fitting. Final production uses `--verify` to preserve reviewed artwork.

## Editable artwork and source preservation

All 110 image references and 62 registered figures are retained. The asset source and generation records remain under `docs/v0.10.1/`, `docs/v0.10.2/` and `docs/v0.10.3/`. Do not run historical artwork generators over reviewed assets. No image or caption changed in v0.10.4.

`docs/v0.10.4/check_review.py` replays every exact approved replacement from the three review JSON files against preserved v0.10.3. It verifies complete coverage, original image and external citation links, asset bytes and previous deliveries. The 18 edits and all 35 section receipts are recorded in the source review. [Gentle critique](../docs/v0.10.4/CRITIQUE.md) explains the changes.

All 2,301 inherited block IDs remain, with two new IDs for intentional splits. [Index review](../docs/v0.10.4/INDEX-REVIEW.md) records semantic checks for all 17 positional assignments and the deliberate wrong-ID control. Further mixed edits require reviewing assignments again.

## Proof and handoff

[PDF review](../docs/v0.10.4/pdf-proof/FINAL-PDF-REVIEW.md), [EPUB review](../docs/v0.10.4/EPUB-REVIEW.md), [reader review](../docs/v0.10.4/READER-REVIEW.md) record coverage and limits. Automated PDF checks are in `output/proof/checks.json`; resource checks are in `docs/publication/PDF-RESOURCE-CHECKS.json`.

PDF proof uses plain extraction first and layout extraction from matching PDF pages for otherwise missing blocks. A combining glyph in the cooling caption requires that fallback. The method reads only PDF bytes and rejects deliberately removed middle text. Separate raster inspection checks visible appearance.

Publication outputs include `output/Surviving-the-Singularity-{reading,interior,print-interior,front-cover}.pdf`, the versioned editable ZIP, and `package-v0.10.4/`. Versioned delivery copies are in `book-build/`; compiled Markdown is in `manuscript/`. The package includes portable HTML/CSS, artwork, fonts and notices, canonical source snapshots, audits and PDFs. Repository history, environment files and proof-image clutter are excluded.

## Scope

The public-download release remains v0.7.5. This is a local digital edition; see [finalization](../docs/publication/FINALIZATION-v0.10.4.md). All previous deliveries remain preserved.

Four retained narrative plates depict fiction. Six retained photo-derived cutouts are generated adaptations with separate credits. Existing cover provenance and epigraph questions remain in the [quotation and cover review](../docs/publication/QUOTATIONS-v0.10.0.md). Physical print proof, printer-specific wrap production and dedicated e-reader pagination remain separate from the completed digital checks.
