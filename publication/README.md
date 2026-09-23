# Publication production files

This directory typesets manuscript v0.8.2 without editing its canonical files.
The 30-section baseline and image/caption exceptions are recorded under
[`docs/publication`](../docs/publication/). Read the
[design report](../docs/publication/DESIGN-REPORT.md) for delivered files,
verification and external-release decisions.

## Outputs

- `output/Surviving-the-Singularity-reading.pdf`: color reading edition with cover, 229 pages.
- `output/Surviving-the-Singularity-print-interior.pdf`: grayscale, no-bleed 6 x 9 interior, 228 pages.
- `output/Surviving-the-Singularity-front-cover.pdf`: vector front-cover design. A full cover wrap requires the chosen printer, paper and binding.
- `output/Surviving-the-Singularity-interior.pdf`: color interior master used for conversion.
- `output/Surviving-the-Singularity-editable-publication.zip`: portable HTML/CSS/SVG/font/manuscript and PDF handoff.

## Rebuild from this repository

Required commands: Python 3, Pandoc, Ghostscript. Python packages used are
WeasyPrint, Beautiful Soup, pypdf and Pillow. The font files and their original
licenses are included in `assets/fonts`.

```sh
export DAILY_NOTE_AGENT=codex
python3 publication/build.py
python3 publication/production.py
python3 publication/proof.py
python3 publication/check_pdf_resources.py
python3 publication/render_contact_sheets.py
python3 publication/package.py --check
python3 publication/package.py
```

The exporter refuses to overwrite an existing ZIP or altered package. Preserve
previous handoffs under distinct versioned paths before creating a new handoff.
It packages only assets used by the final design and rejects missing resources,
unapproved images and font packages without their notices. The source-rendered
diagnostic copy marks omitted source images explicitly; the manuscript snapshot
itself remains unchanged.

`build.py` retains intermediate HTML, source hashes, layout measurements and
exact caption/image transformations. `proof.py` compares manuscript text with
the rendered PDF and checks geometry, fonts and references. Resource and visual
reviews supplement those checks; they are not substitutes for a physical proof.

## Editable artwork

`book.css` holds the page design. `assets/motifs` contains twelve interior
masters, a separate detailed cover illustration, monochrome counterparts,
generation scripts and proofs. Eleven motifs are placed; the open-gate drawing
is an unused alternative. `assets/cover-art.svg` is the light-on-green palette
variant used by the cover. The two explanatory diagrams remain editable text
and layout in `build.py`.

Original source images, manuscript sections and all previous editions remain
available. Publishing, committing and printer approval are separate actions.
