# Local digital finalization: v0.10.2

September 28, 2026. All 35 canonical sections were reread; 28 were revised. Thirty-one existing SVGs were corrected and recomposed. All 102 source image references and 24 precedents remain. The preserved v0.10.1 source and six deliveries pass their recorded hashes.

| Output | Result |
| --- | --- |
| Reading PDF | 408 pages including original cover |
| Color interior | 407 pages, 6 by 9 inches |
| Grayscale interior | 407 content pages and one empty final verso |
| EPUB | All 35 sections and 102 canonical image placements |
| Registered figures | 54, each with its complete caption on one PDF page |

PDF proof recovers all 2,599 checked source blocks. No page overflow, missing assets, broken internal links or registered-figure layout errors remain. A pypdf plain-extraction defect omitted part of the cooling caption before a combining glyph. Layout extraction from the same PDF recovered the full normalized paragraph, and a rasterized page confirmed visible content. The alternate extraction path rejects an injected deletion. Source text or layout-capture strings are never substituted for extracted PDF text.

The resource audit passes embedded-font, navigation, grayscale and pagewise text-preservation checks. EPUB checks pass 2,648 source blocks and all image placements, plus actual packaged-resource reflow of the 54 registered figures at 390 and 768 pixels. Final PDF samples and EPUB samples are recorded under docs/v0.10.2 in the source project.

Reader fixes preserve scene-toggle focus, isolate arrow keys on controls, implement modal chapter navigation, restore selected-section focus and render full part-divider content. Before/after browser evidence demonstrates the failures and corrections. The manuscript index was separately reviewed because structural checks cannot identify a semantically misplaced ID: 19 block assignments were repaired, with no further source edits.

All revised SVG labels are at least 9.58 pt at print width. The entire prepared labelled-SVG inventory has no labels below 8 pt by geometry estimate. Source and print hashes prevent generic recoloring of prepared artwork. The legacy resolver now has a read-only --verify mode; its enlargement control uses a fixed fixture rather than a production diagram that may change.

The editable package carries portable HTML, CSS, artwork, fonts and notices, canonical source snapshots, audits and PDFs. The package validator checks source/PDF/resource hashes and local rendering dependencies. Export verifies each directory file and ZIP member. Edition-specific delivery hashes are in docs/v0.10.2/deliverables.json in the source project.

This is local digital verification within the recorded scopes. Targeted source checking does not certify every inherited claim or quotation. Existing original-cover provenance, quotation decisions and physical printer proof remain documented. No commit, deployment or external release occurred.
