# Surviving the Singularity v0.10.1

Local visual expansion of v0.10.0, September 28, 2026. Author: Christopher
Tavolazzi. Subtitle: *We Don't Have to Live Like This*.

This edition adds 23 figures to the existing manuscript. The previous
v0.10.0 worktree, source, and deliveries remain preserved. No commit,
merge, deployment, public-download swap, or publisher submission is part
of this work. `book.json` identifies source version 0.10.1; its `released`
value remains 0.7.5.

**Publication status:** local digital verification completed September 28.
The reading PDF has 394 pages. The grayscale print interior has 393 content
pages and one blank final verso. EPUB and both web readers passed their
recorded checks. [Delivery files and hashes](deliverables.json) identify
this edition's outputs. The [previous edition notes](../v0.10.0/EDITION-NOTES.md)
and [previous final visual review](../v0.10.0/pdf-proof/FINAL-PDF-REVIEW.md)
remain records of that edition.

## What was added

| Kind | Count | Additions |
| --- | ---: | --- |
| Photo-derived cutouts | 6 | Atlas, Falcon Heavy launch collage, solar illustration, desktop printer, Spot, and hand-tool collage. |
| Charts and worksheets | 8 | Researcher forecast shift, data-centre demand, income and food access, ammonia energy, weights-only memory, farm-real-estate values, wasted-food pathways, and a failed-meal response sequence. |
| Conceptual SVG illustrations | 6 | Access gate, attention ribbon, local copies, operating stack, shared land, and continuity calendar. |
| Three.js scenes with static SVGs | 3 | A five-household food route, a growing-bed cutaway, and a shared workshop's dependencies. |

All 23 additions appear once in canonical source and in the presentation
registry. The manuscript still has 35 manifest sections. A source comparison
against the preserved v0.10.0 worktree found every previous paragraph block
present verbatim and all 79 previous image references retained; the current
source has 102 image references. New captions and Appendix B visual-source
notes accompany the additions. This comparison establishes preservation,
not a new factual review of every existing claim.

The data ledger distinguishes published estimates, forecasts, benchmarks,
calculations, and illustrative material. Six of the eight charts draw on
published quantitative evidence. The memory matrix calculates weights-only
storage and excludes runtime costs; the meal worksheet illustrates a process
without claiming measured service outcomes. Values, units, exact source
locations, and exclusions are in [chart-data.json](chart-data.json).
[Chart integration](CHART-INTEGRATION.md) records placements and the three
new references added to Appendix B.

## Cutouts and provenance

The six raster additions were made with the built-in image-generation tool
using repository photographs as references. They have actual alpha
transparency. They are **generated editorial adaptations**, not exact
photographic extractions. Inspection found regenerated machine details,
recomposed tools and smoke, and altered solar texture and edge detail.
The solar illustration is not an unaltered scientific observation.

[image-prompts.json](image-prompts.json) retains the original prompts,
reference filenames, generated outputs, dimensions, and checksums. A prompt's
request for fidelity describes the request, not a guarantee about the result.
Captions and production credits identify the AI adaptations and retain
source attribution and applicable license notices. Image generation does
not replace source-license requirements or establish external-use clearance.
The [cutout review](cutout-proof/REVIEW.md) shows the original/reference
comparisons, alpha measurements, and the limits of that inspection.

## Read and reproduce

Run from this worktree:

```sh
npm ci
npm run dev -- --port 5189 --strictPort
```

Open [the chapter reader](http://localhost:5189/book) or
[the continuous reader](http://localhost:5189/read). Both retain the existing
draft-password gate. The new interactive figures are in
[Chapter 9](http://localhost:5189/book/chapter9),
[Chapter 15](http://localhost:5189/book/chapter15), and
[Chapter 17](http://localhost:5189/book/chapter17).

Each scene begins with a complete static illustration. **Explore in 3D**
loads Three.js only when requested. Keyboard-accessible buttons change the
camera or highlight a connection; prose and an expandable table provide
the same relationships in text. There is no autoplay. Failed or lost WebGL
restores the still, and changing chapters disposes the previous scene.
The full reader's existing password gate requires JavaScript; standalone
figure fallback has also been checked with JavaScript disabled.

PDF and EPUB contain the static SVG stills. They do not execute the scenes
or depend on JavaScript. The live view and exported vector illustration
share actual Three.js geometry and an orthographic camera. Dark originals
and prepared light print variants are generated deterministically; the
publication bridge verifies their hashes before use.

The source and proof entrypoints are:

- [Scene implementation and proof](scenes/SCENE-REVIEW.md), including `node scripts/render-book-scenes.mjs --check` and the six still hashes in [render-manifest.json](scenes/render-manifest.json).
- [Chart review](chart-proof/REVIEW.md), [data ledger](chart-data.json), and `python3 docs/v0.10.1/charts.py`.
- [Conceptual art and presentation review](FIGURE-REVIEW.md), [placement guide](VISUAL-PLACEMENTS.md), and `python3 docs/v0.10.1/vignettes.py --proof`.
- [Publication builder](build.py) and [EPUB checker](check_epub.py), used with the frozen source and the [production pipeline](../../publication/README.md).

`src/lib/data/book/visuals.json` controls registered presentation. Cutouts
wrap beside prose where the web/PDF column permits it and stack on narrow
screens and in EPUB. Prepared light artwork is protected from the older
generic diagram recoloring step. Ordinary image references and captions
remain in the manuscript; scene comments are enhancement markers, not
printable content.

## Verification

The [editorial gate results](gate-results.json) report no inherited or new
errors in the 35 sections, with deliberately failing controls for known
regressions. These checks do not certify every factual claim.

Chart and conceptual-art reviews record source transcription or illustrative
scope, vector-label geometry, screen/print samples, and intentional defects
that the checks rejected. The cutout proof verifies real alpha and shows
all six adaptations against white and navy backgrounds. The prepared-art
bridge verifies source/print hashes and rejects stale artwork.

The [scene browser report](scenes/browser-proof.json) records real WebGL2
rendering in the chapter and continuous readers, keyboard controls, changed
camera pixels, selected explanations, lazy loading, no animation loop,
mobile layout, reduced motion, and deliberately denied or lost WebGL.
[Navigation proof](scenes/navigation-proof.json) verifies disposal when a
chapter changes. [Static fallback proof](scenes/static-fallback-proof.json)
checks the server-rendered figures with JavaScript disabled. Production
web compilation passed; browser evidence is local Chrome, not a claim of
Safari, Firefox, or physical-device acceptance.

The complete PDF proof recovered all 2,524 source text blocks and all 35
sections, with no missing assets, broken internal links, text outside the page,
or registered-figure geometry errors. All 23 additions have complete captions
on the same page. The first build exposed a split tool collage and cramped
caption bounds; [the layout correction](pdf-proof/LAYOUT-CORRECTION.md)
records the failure, CSS fix, and deliberately failing controls.

The independent PDF resource audit verified embedded fonts, 6 by 9 page boxes,
navigation, grayscale resources and identical normalized text on all 393
content pages. Its one extra print page is empty. See
[resource checks](../publication/PDF-RESOURCE-CHECKS.md) and
[final visual review](pdf-proof/FINAL-PDF-REVIEW.md), which covers all 23 new
figures in color and grayscale.

[EPUB review](EPUB-REVIEW.md) verified 2,573 freshly rendered source blocks,
all 102 images in their chapters, 35 TOC sections and 96 XML documents.
All 23 new figures passed layout checks at 390 and 768 pixels with JavaScript
disabled. Five structural defects and one real layout defect were rejected.
[Final reader review](READER-FINAL-REVIEW.md) records the three interactive
scenes and 24 cutout route/viewport cases.

The portable package validator checked all referenced resources, source
snapshots, current PDF hashes and font notices. Its deliberately invalid
in-memory plans rejected a missing image, absent font notices, an external
rendering dependency and an unsafe destination. Export verifies every file
again from disk and inside the ZIP. Delivery measurements are in
[deliverables.json](deliverables.json).

The existing cover-provenance and quotation-use questions remain recorded
in the publication audits; this visual expansion does not grant new rights
or replace a printer-specific physical proof.
