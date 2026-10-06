# Publication production files

Current local source edition: **v0.10.1**, the visual expansion of v0.10.0.
The canonical 35-section source lives in `src/lib/data/book/`, with
`book.json` as its manifest. See [edition notes](../docs/v0.10.1/EDITION-NOTES.md)
for the 23 additions and recorded artwork/reader checks. Final whole-book
PDF/EPUB checks passed. Reading PDF: 394 pages. Print interior: 393 content
pages plus one blank verso. [Delivery measurements](../docs/v0.10.1/deliverables.json)
record the versioned files and checksums.
Previous v0.10.0 worktrees and deliveries remain preserved.

## Build and verify

Requirements: Node dependencies from `npm ci`; Python 3 with WeasyPrint,
Beautiful Soup, pypdf, Pillow and Playwright; Pandoc; Ghostscript; and Chrome
for vector and browser proofs. Fonts and their licenses are bundled in
`assets/fonts`. Three.js 0.168.0 is already in the lockfile.

The approved final-source checksums live in `docs/publication/baseline.json`.
The build refuses drift from that frozen source, including its manifest.
This is separate from `docs/v0.10.1/baseline.json`, which records the preserved
v0.10.0 edition used for the before/after comparison. Artwork must be finished
and its prepared print hashes registered before the final-source build.

Run these commands from the repository root:

```sh
export DAILY_NOTE_AGENT=codex
python3 scripts/sts.py verify
python3 docs/v0.10.1/check_source_preservation.py
python3 docs/v0.10.1/gates.py
node scripts/render-book-scenes.mjs --check
python3 docs/v0.9.2/print_figures.py --check
python3 docs/v0.10.1/prove_figure_capture.py
python3 docs/v0.10.1/build.py
python3 publication/proof.py
python3 publication/check_pdf_resources.py
python3 docs/v0.10.1/check_epub.py
python3 publication/package.py --check
python3 publication/package.py
```

The source-preservation check requires the old worktree named in the edition
baseline. If it has moved, pass `--before /path/to/sts-v0.10.0`; its files must
still match the recorded SHA-256 values. It checks source blocks and image
references, not the generated book. Final PDF/EPUB proof follows the build.

The earlier `docs/v0.9.2/print_figures.py` remains the shared print resolver.
Prepared v0.10.1 artwork is hash-checked and kept out of generic recoloring
and label fitting. `docs/v0.10.0/figures.py` and `cast_plate.py` remain the
editable generators for the earlier redrawn figures and cast plate.
The v0.10.1 artwork sources are:

- `docs/v0.10.1/charts.py` with `chart-data.json`: eight charts and worksheets.
- `docs/v0.10.1/vignettes.py`: six conceptual SVG illustrations.
- `scripts/render-book-scenes.mjs`: three dark/light SVG pairs from the same Three.js geometry and camera used by the reader.
- `docs/v0.10.1/image-prompts.json`: six generated photo-derived cutouts, with source references and output checksums. Their generation prompts are records, not deterministic reproduction commands.

`docs/v0.10.1/build.py` creates EPUB, reading/print PDFs, and compiled Markdown
from the frozen canonical source. It does not publish them. PDF and EPUB
contain static scene illustrations; only the web readers run Three.js.
[Figure review](../docs/v0.10.1/FIGURE-REVIEW.md),
[chart review](../docs/v0.10.1/chart-proof/REVIEW.md),
[cutout review](../docs/v0.10.1/cutout-proof/REVIEW.md), and
[scene review](../docs/v0.10.1/scenes/SCENE-REVIEW.md) describe the measurements,
visual samples, intentionally failing controls, and limits.

## Output locations

These are the verified v0.10.1 build/export paths:

- `output/Surviving-the-Singularity-reading.pdf`: color reading PDF with original cover.
- `output/Surviving-the-Singularity-print-interior.pdf`: grayscale 6 by 9 interior without cover; a blank final verso is added when needed.
- `output/Surviving-the-Singularity-front-cover.pdf`: original front cover at 6 by 9, for review.
- `output/Surviving-the-Singularity-interior.pdf`: color interior master.
- `output/Surviving-the-Singularity-v0.10.1-editable-publication.zip`: portable HTML, CSS, artwork, fonts, source snapshots, audits, and PDFs.
- `package-v0.10.1/`: unpacked editable publication handoff.
- `../book-build/Surviving-the-Singularity-v0.10.1.epub`: EPUB edition.
- `../manuscript/Surviving-the-Singularity-v0.10.1.md`: compiled Markdown.

Final delivery copies and hashes are recorded in
`docs/v0.10.1/deliverables.json`. Generated layout, text,
geometry, and source-coverage evidence remain in `output/`. Previous
v0.10.0 counts and checksums describe the previous edition only.

Package export refuses to overwrite an existing ZIP or an altered package.
Preserve a previous handoff before exporting a new one. Versioned packages
are generated under `publication/package-v<version>/`; the historical
`publication/package/` snapshot is preserved.

## Local and external release

The website's public-release value remains v0.7.5. No deployment, public
upload, commit, or publisher submission is part of this local edition work.
Artwork, reader, PDF and EPUB checks are complete in their documented scopes.
See [finalization record](../docs/publication/FINALIZATION-v0.10.1.md).

The six new cutouts are AI adaptations of photographs. Their captions and
production credits retain that distinction, their source attribution, and
applicable source-license requirements. They are not exact photographic
extractions, and the solar adaptation is not an unaltered scientific image.
Rights records remain in `docs/publication/asset-rights.json`.

The earlier interior replacements remain in canonical source. The
original cover is retained with its historical unresolved provenance
recorded. The existing 23-epigraph inventory and external-use questions are
in [QUOTATIONS-v0.10.0.md](../docs/publication/QUOTATIONS-v0.10.0.md); this
visual edition does not silently clear them.

A printer-specific wrap, binding and paper selection, physical proof, and
external-publication quotation/cover decisions remain separate. Digital
geometry and font checks do not certify those. No ISBN, publisher,
permission grant, or physical-print acceptance has been invented.
