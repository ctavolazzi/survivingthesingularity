# Publication production files

Current local edition: **v0.10.0**, finalized from the v0.9.2 manuscript on
September 27, 2026. The canonical 35-section source lives in
`src/lib/data/book/` with `book.json` as its manifest. See the
[edition notes](../docs/v0.10.0/EDITION-NOTES.md) for changes and measured results.

## Build and verify

Requirements: Python 3 with WeasyPrint, Beautiful Soup, pypdf, Pillow and
Playwright; Pandoc; Ghostscript; Chrome for the vector proofs. Fonts and their
licenses are bundled in `assets/fonts`. The approved source checksums live in
`docs/publication/baseline.json`. A build refuses unreviewed changes to that
baseline, including the manifest.

```sh
export DAILY_NOTE_AGENT=codex
python3 scripts/sts.py verify
python3 docs/v0.10.0/gates.py
python3 docs/v0.9.2/print_figures.py --check
python3 docs/v0.10.0/proof_figures.py
python3 docs/v0.10.0/build.py
python3 publication/proof.py
python3 publication/check_pdf_resources.py
python3 docs/v0.10.0/check_epub.py
python3 publication/package.py --check
python3 publication/package.py
```

The earlier `print_figures.py` is retained as the shared palette and layout
engine. `docs/v0.10.0/figures.py` is the editable generator for the five
redrawn figures. `docs/v0.10.0/cast_plate.py` regenerates the cast
plate from unchanged portrait sprites. The proof records actual label sizes, collision checks, and
negative controls. `build.py` creates the EPUB, reading and print PDFs, and
compiled Markdown from the same source. It does not publish them.

## Outputs

- `output/Surviving-the-Singularity-reading.pdf`: color reading PDF with original cover.
- `output/Surviving-the-Singularity-print-interior.pdf`: grayscale 6 x 9 interior, without cover; a blank final verso is added when needed.
- `output/Surviving-the-Singularity-front-cover.pdf`: original front cover at 6 x 9, for review.
- `output/Surviving-the-Singularity-interior.pdf`: color interior master.
- `output/Surviving-the-Singularity-v0.10.0-editable-publication.zip`: portable HTML, CSS, artwork, fonts, source snapshots, audits, and PDFs.
- `../book-build/Surviving-the-Singularity-v0.10.0.epub`: EPUB edition.

The versioned reading and print delivery copies and their hashes are recorded
in `docs/v0.10.0/deliverables.json` after proofing. Generated layout, text,
geometry, and source-preservation evidence remain in `output/`.

Package export refuses to overwrite an existing ZIP or an altered package.
Preserve a previous handoff before exporting a new one. Versioned packages
are generated under `publication/package-v<version>/`; the historical
`publication/package/` snapshot is preserved.

## Scope of finalization

Manuscript review, digital typesetting, and build checks are completed locally.
The website's public-release value remains v0.7.5. No deployment, upload,
commit, or publisher submission is part of this edition close.

The four previously unresolved interior image uses now have original
illustrations in canonical source. The author-selected original cover is
retained for this local handoff, with unresolved provenance explicitly recorded.
The current 23-epigraph inventory and external-use questions are in
[QUOTATIONS-v0.10.0.md](../docs/publication/QUOTATIONS-v0.10.0.md).

A printer-specific wrap, binding and paper selection, physical proof, and
external-publication quotation/cover decisions remain. Digital geometry and
font checks do not certify those. The original cover is about 228 pixels per
inch at 6 x 9. No ISBN, publisher, or permission grant has been invented.
