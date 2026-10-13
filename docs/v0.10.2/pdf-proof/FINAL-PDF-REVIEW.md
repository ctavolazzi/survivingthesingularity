# Final PDF review: v0.10.2

Completed September 28, 2026. The reading PDF has 408 pages including its cover. The color interior has 407 content pages; the grayscale interior has those pages plus one empty final verso.

## Visual coverage

All 31 revised diagram pages were inspected in both color and grayscale at the original resolution of their 120 dpi page captures. The middle reviewer inspected 25 pairs. Root inspected the remaining six pairs: algae flow, DC power, neighborhood workshop, social provision, conversion ladder and precedent timeline. Those six inspections and their verified capture hashes are recorded in [root-late-figure-review.json](root-late-figure-review.json). The full list of 31 pairs and individual capture hashes is in [revised-diagram-review-receipt.json](revised-diagram-review-receipt.json).

No visible clipping, incomplete captions, label collisions or loss of meaning in grayscale was found in those revised diagrams. The cooling caption on physical page 207 is visibly complete. The algae diagram separates recirculating water from the possible feed contribution. The ladder distinguishes proposed upper rungs with dashed lines; approximate spans in the precedent timeline remain visibly dashed in grayscale. Captions fit below their figures and clear surrounding prose.

An independent reviewer inspected another 26 full-page captures: six cutouts, three scenes and four representative retained charts, each in color and grayscale. No clipping or overlap was found in that selection. [CUTOUT-SCENE-REVIEW.md](CUTOUT-SCENE-REVIEW.md) records every selected page and hash. It also notes a small, faint subtitle in the separate retained ox artwork on page 7, especially in grayscale. That incidental raster-art limitation remains; the adjacent manuscript caption is readable.

The render manifest contains 108 samples covering all 54 registered figures in both editions. The stated visual review covers 44 distinct figure page positions, 88 page captures. It does not claim manual inspection of every book page or every retained raster asset. All 31 revised diagrams also received separate actual-width SVG browser inspection and geometry checks before the book build.

## Automated proof

- All 2,599 checked source text blocks are recovered; no text extends outside the page.
- All 54 registered figures have one complete caption on the same page, at the expected width, without intersection with surrounding prose.
- Source hashes, embedded fonts, internal navigation and referenced resources pass.
- The independent resource audit confirms grayscale rendering and normalized text preservation across all 407 content pages. The additional print page has no content operations or annotations.
- Text, geometry, font, resource, navigation and grayscale checks reject their deliberately corrupted controls.

pypdf plain extraction dropped part of the cooling caption before a combining character. Layout extraction from the same PDF recovered the entire normalized paragraph; the rendered page independently confirms its presence. The fallback uses PDF bytes, never source strings or layout-box text, and rejects an injected deletion. This is an extraction limitation, not omitted visible manuscript content.

See [edition PDF checks](../pdf-checks.json) and [resource audit](../../publication/PDF-RESOURCE-CHECKS.md). Final source hashes remain unchanged.

## Exact render inputs

| Artifact | SHA-256 |
| --- | --- |
| Color interior | `265fdda8df4266e564d284560b2c1bf3894bb9c93703fcf88fae5e34d3260f59` |
| Prepared color render input | `a9e7420e7baa4f124e3458cf3fbd82716770b89bcd463ae2beebabb997175c2b` |
| Grayscale print interior | `c24e729c20d0a3d07ae130627b842aee4ee2aeec34150c09e2d6cdb87410d4bd` |

[final-samples.json](final-samples.json) records each capture, page, caption, rendering source and checksum. Resource preparation preserved page streams and annotation descriptors while pruning unused resources. The renderer confirmed that source PDF hashes stayed unchanged.

This is digital screen proof, not a physical printer proof, color-management certification, factual certification, rights clearance or dedicated-device acceptance. Existing external-publication decisions remain in the publication audits.
