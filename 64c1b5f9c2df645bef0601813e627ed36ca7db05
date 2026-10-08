# Publication production files

Current local edition: **v0.10.3**. Eight additional graphics and five page-design refinements preserve the prose and artwork of v0.10.2. Reading PDF: 408 pages. Print interior: 407 content pages plus one blank final verso. See [edition notes](../docs/v0.10.3/EDITION-NOTES.md) and [delivery hashes](../docs/v0.10.3/deliverables.json).

## Build and verify

Requirements: Node dependencies from `npm ci`; Python 3 with WeasyPrint, Beautiful Soup, pypdf, Pillow and Playwright; Pandoc; Ghostscript; Chrome. Fonts and licenses are bundled in `assets/fonts`.

Canonical source is `src/lib/data/book/`, ordered by `book.json`. Frozen hashes in `docs/publication/baseline.json` must match all 35 sections and the manifest. `docs/v0.10.3/baseline.json` separately records the preserved v0.10.2 reference edition. Review and record source changes before updating the freeze.

Run from the repository root:

```sh
export DAILY_NOTE_AGENT=codex
python3 scripts/sts.py verify
python3 scripts/sts.py id verify
python3 docs/v0.10.3/check_source.py
python3 docs/v0.10.3/gates.py
node scripts/render-book-scenes.mjs --check
python3 docs/v0.9.2/print_figures.py --verify
python3 docs/v0.10.3/build.py
python3 publication/proof.py
python3 publication/check_pdf_resources.py
python3 docs/v0.10.3/check_epub.py
python3 docs/v0.10.3/prove_epub_layout.py
python3 docs/v0.10.3/pdf-proof/render_samples.py --prepared-color --dpi 120
python3 docs/v0.10.3/check_package.py
python3 publication/package.py --check
python3 publication/package.py
python3 docs/v0.10.3/finalize.py
```

The package exporter refuses to overwrite an existing ZIP. A PDF rebuild changes output hashes: repeat output proofs and visual review, and preserve the existing package before preparing a separate handoff. Finalization requires current review receipts. Its six deliveries include reading PDF, grayscale interior, front cover, EPUB, compiled Markdown and editable ZIP.

The print resolver's `--verify` mode checks source/print hashes and a deliberate collision fixture without writing files. Its older default and `--check` modes regenerate legacy variants with browser-dependent font fitting. Final production uses `--verify` to preserve reviewed artwork.

## Editable artwork and source preservation

The eight additions are registered in `src/lib/data/book/visuals.json` and `docs/v0.10.3/art-integration.json`:

- `docs/v0.10.3/figures_practical.py`: four practical SVG pairs. The generator owns its new diagrams; insertion is guarded.
- `docs/v0.10.3/narrative-art/generation.json`: prompts and original image_gen paths for four narrative PNGs. Prompts record requests and are not deterministic reproduction instructions.
- `docs/v0.10.2/figures_{opening,middle,ending,core}.py`: 31 retained diagram revisions.
- `docs/v0.10.1/charts.py`, `chart-data.json` and `vignettes.py`: earlier chart and conceptual sources. Do not run historical generators over subsequently revised assets.
- `scripts/render-book-scenes.mjs`: retained Three.js scene stills and corresponding reader geometry.

After an intentional artwork edit, synchronize print hashes, canonical alt text/caption, the art catalog and rights record. Prepared artwork bypasses generic recoloring. PDF and EPUB retain static scene illustrations.

The v0.10.3 source check compares exact existing blocks and their order, allowing only the three documented figure relocations and eight new image/caption pairs. It also verifies prior artwork bytes and all six v0.10.2 deliveries. All 2,285 previous block IDs were retained by content, with no positional guesses. Further mixed edits require reviewing ID assignments again.

## Proof and handoff

[PDF review](../docs/v0.10.3/pdf-proof/FINAL-PDF-REVIEW.md), [EPUB review](../docs/v0.10.3/EPUB-REVIEW.md), [reader review](../docs/v0.10.3/READER-REVIEW.md) and [layout review](../docs/v0.10.3/LAYOUT-REVIEW.md) record coverage and limits. Automated PDF checks are in `output/proof/checks.json`; resource checks are in `docs/publication/PDF-RESOURCE-CHECKS.json`.

PDF proof uses plain extraction first and layout extraction from matching PDF pages for otherwise missing blocks. A combining glyph in the cooling caption requires that fallback. The method reads only PDF bytes and rejects deliberately removed middle text. Separate raster inspection checks visible appearance.

Publication outputs include `output/Surviving-the-Singularity-{reading,interior,print-interior,front-cover}.pdf`, the versioned editable ZIP, and `package-v0.10.3/`. Versioned delivery copies are in `book-build/`; compiled Markdown is in `manuscript/`. The package includes portable HTML/CSS, artwork, fonts and notices, canonical source snapshots, audits and PDFs. Repository history, environment files and proof-image clutter are excluded.

## Scope

The public-download release remains v0.7.5. This is a local digital edition; see [finalization](../docs/publication/FINALIZATION-v0.10.3.md). All previous deliveries remain preserved.

Four new narrative plates depict fiction. Six retained photo-derived cutouts are generated adaptations with separate credits. Existing cover provenance and epigraph questions remain in the [quotation and cover review](../docs/publication/QUOTATIONS-v0.10.0.md). Physical print proof, printer-specific wrap production and dedicated e-reader pagination remain separate from the completed digital checks.
