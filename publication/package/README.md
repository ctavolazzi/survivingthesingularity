# Surviving the Singularity: editable publication package

Manuscript v0.8.2, publication design 01.
This is an editable production handoff and review copy. It is not an approval
for public sale or a substitute for the publisher's production and rights review.

## Edit and regenerate

Edit `interior.html`, `front-cover.html`, `book.css`, or the SVGs in `assets/`.
All rendering assets are included. The HTML has relative local resource URLs.
The bundled static fonts are Adobe Source Serif 4 and Source Sans Pro.
Keep their licenses, copyright notices and provenance with any redistribution.

From this directory, with WeasyPrint 68.1 and its system dependencies
installed, generate new PDFs under new names so the supplied proofs stay intact:

```sh
weasyprint --full-fonts interior.html regenerated-interior.pdf
weasyprint --full-fonts front-cover.html regenerated-front-cover.pdf
```

These commands regenerate the layout PDFs. They do not impose printer pages,
convert to a printer color profile, create a wraparound cover, or certify PDF/X.
The supplied reading PDF includes the cover and interior, with page labels.
Printer-specific conversion, stock, binding, bleed and spine dimensions remain
production decisions. See the companion production and review notes below.

The 30 Markdown sections and `book.json` in `manuscript/` are unchanged source
snapshots. `manuscript/baseline-sha256.json` records their checksums. Editing them
does not automatically update the included HTML. The original repository build
performs manuscript-to-layout transformations; this portable package provides
the fully editable final HTML and CSS independently of that repository.

`source-rendered.html` is a diagnostic rendering of the original manuscript,
not the publication interior. Its 7 excluded image elements have
been replaced with explicit placeholders. Original surrounding captions remain
as source evidence. No excluded raster artwork is bundled. Publication image
substitutions and caption corrections are recorded in `build.json` and the audits.
The original cover was also replaced in this design.

## Supplied PDFs

- [Surviving-the-Singularity-front-cover.pdf](pdfs/Surviving-the-Singularity-front-cover.pdf)
- [Surviving-the-Singularity-interior.pdf](pdfs/Surviving-the-Singularity-interior.pdf)
- [Surviving-the-Singularity-print-interior.pdf](pdfs/Surviving-the-Singularity-print-interior.pdf)
- [Surviving-the-Singularity-reading.pdf](pdfs/Surviving-the-Singularity-reading.pdf)

## Publisher production and review notes

- [DESIGN-REPORT.md](audits/DESIGN-REPORT.md)
- [FINAL-VISUAL-REVIEW.md](audits/FINAL-VISUAL-REVIEW.md)
- [PDF-RESOURCE-CHECKS.md](audits/PDF-RESOURCE-CHECKS.md)
- [PLAN.md](audits/PLAN.md)
- [READING-DESIGN-REVIEW.md](audits/READING-DESIGN-REVIEW.md)
- [RIGHTS-AUDIT.md](audits/RIGHTS-AUDIT.md)
- [VISUAL-MAP.md](audits/VISUAL-MAP.md)

`audits/asset-rights.json` records authors, sources, license URLs, modifications
and unresolved limitations. Image licenses apply to the relevant images, not
the manuscript. The epigraph review in the rights audit identifies remaining
publication decisions. Generated narrative plates are fictional illustrations;
their provenance does not establish exclusive copyright in every output.

## Package verification

`package-manifest.json` records every bundled file's SHA-256, size and source,
except the manifest itself. `build.json` preserves PDF hashes and source hashes;
its PDF paths are portable. External citation and license links require network
access, but page rendering does not. Font and artwork provenance may retain
historical source-location text; those locations are not rendering dependencies.
Only explicitly selected publication files are included. No credentials,
environment files, repository history, excluded images or proof-sheet clutter
are copied.
