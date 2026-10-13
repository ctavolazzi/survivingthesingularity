# Local digital finalization: v0.10.1

Completed September 28, 2026. This edition preserves the 35-section v0.10.0
manuscript and adds 23 figures: six photo-derived cutouts, eight charts and
worksheets, six conceptual SVGs, and three Three.js scenes with static exports.
The previous edition remains preserved. No commit or external release occurred.

| Output | Measured result |
| --- | --- |
| Reading PDF | 394 pages, including original cover |
| Color interior | 393 pages, 6 by 9 inches |
| Grayscale print interior | 393 content pages and one empty final verso |
| EPUB | 38 spine documents containing all 35 sections and all 102 source images |
| Web readers | Three interactive scenes and all 24 tested cutout route/viewport cases pass |

The PDF proof recovered all 2,524 checked source text blocks, with no missing
assets, broken internal links, text outside the page or registered-figure
layout errors. All 23 added figures retain a complete caption on the same
page. The first build's split tools cutout was corrected by keeping cutout
floats together and increasing caption line height. The failed capture and
correction are preserved under `docs/v0.10.1/pdf-proof/` in the source project.

The independent PDF resource audit passed embedded-font, page-box, navigation,
grayscale and normalized-text checks. All 393 content pages match between
color and grayscale. The additional print page is empty. The resource report
records exact output hashes, page labels and deliberately failing controls.

EPUB proof checked 2,573 freshly rendered source blocks, image placement and
hashes, internal resources, navigation, XML and ZIP integrity. Browser proof
of actual packaged XHTML checked all 23 additions at 390 and 768 pixels with
JavaScript disabled. Removed text, removed or undisplayed images, missing
resources, broken anchors and an overflowing figure were correctly rejected.

Source preservation verified every one of the 2,217 prior paragraph-delimited
blocks in order and all 79 prior images. The new source has 102 images. These
checks establish preservation and presentation within their recorded scope;
they are not a fresh factual review of every claim.

The editable package contains portable HTML, CSS, artwork, fonts and notices,
source snapshots, audits and PDFs. The validator checks resources, source and
PDF hashes, font provenance and the exact local-review cover exception.
Export reads every packaged file back and verifies every ZIP member. The
source project's `docs/v0.10.1/deliverables.json` records final delivery sizes
and SHA-256 values; the package has its own `package-manifest.json`.

Cutouts are credited generated adaptations. Original-cover provenance,
quotation-use decisions, physical printer proof and printer-specific cover
production remain as documented in the existing audits. No public rights
clearance, EPUBCheck certification or physical-device acceptance is implied.
