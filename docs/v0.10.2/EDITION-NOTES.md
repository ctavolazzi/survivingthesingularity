# Surviving the Singularity v0.10.2

September 28, 2026. A complete reread of the 35-section manuscript, followed by an artwork and reader review. Twenty-eight sections changed. The edition retains all 102 image references and all 24 precedents, and preserves the previous v0.10.1 worktree and its six deliveries.

Open the [408-page reading PDF](../../book-build/Surviving-the-Singularity-v0.10.2.pdf), [EPUB](../../book-build/Surviving-the-Singularity-v0.10.2.epub), or [grayscale print interior](../../book-build/Surviving-the-Singularity-v0.10.2-print-interior.pdf). The [delivery manifest](deliverables.json) records exact files, sizes and hashes.

## Editorial changes

The reread corrected historical dates, units, benchmark boundaries and continuity. Forecasts and speculative stages remain identified as such. Resource and service claims now account for outside inputs, maintenance, paid work, backup and actual delivery. Fiction remains distinct from evidence. Duplicate instructions were removed, and the bibliography includes the sources used for these corrections.

- [Opening review](OPENING-REVIEW.md): introduction through Chapter 5.
- [Middle review](MIDDLE-REVIEW.md): Part II through Chapter 14.
- [Ending review](ENDING-REVIEW.md): Chapters 15–19, conclusion and all appendices.
- [Complete source diff](source-changes.diff) and [verified review receipts](source-review.json).
- [Stable ID review](INDEX-REVIEW.md): 19 index assignments repaired after mixed insertions, removals and revisions. All 2,285 current blocks verify; a subsequent rebuild requires no positional guesses.

This is a complete editorial reread with targeted source checks. It does not recertify every inherited quotation, external link, factual claim or forecast.

## Artwork

Thirty-one existing SVGs were redrawn or corrected, with matching screen and light print variants. All revised explanatory labels are at least 9.58 pt at the book's 4.56-inch image width. The prior edition had 27 labelled SVGs below 8 pt; the prepared variants now have none below 8 pt. The lowest estimate among all 50 labelled SVGs is 8.21 pt in retained scene artwork. These are geometry-based estimates, checked alongside rendered samples.

The food-security and farm-machinery charts preserve all original observations. Diagrams now distinguish conditional scenarios from measurements, show remaining resource inputs, and remove unsupported guarantees about regional self-sufficiency, complete fish feed, network immunity and construction cost. The precedent timeline's approximate spans use visibly dashed lines.

[Baseline art audit](ART-AUDIT.md), [final size inventory](art-release-checks.json), and [integration record](art-integration.json) describe the findings and resolutions. Four editable generators supply the revised SVGs: [opening](figures_opening.py), [middle](figures_middle.py), [ending](figures_ending.py), and [resource diagrams](figures_core.py). They write their owned image pairs; final registry hashes must be synchronized after any further artwork change. Historical generators are retained as evidence and must not be run over these revised assets.

## Reader and publication checks

The [reader review](READER-REVIEW.md) records reproduced failures and fixes for focus loss, control-key interception, chapter-drawer behavior and missing part-divider prose/artwork. The final reader checks cover all 54 registered figures. The three interactive scenes retain their stills, reduced-motion behavior, keyboard controls and unavailable-WebGL fallback.

The PDF interior contains 407 content pages. The reading PDF adds the original cover; the print interior adds one empty final verso. PDF proof recovers all 2,599 checked text blocks, verifies all 54 registered figures and their same-page captions, and finds no text overflow or missing internal resources. The cooling caption required pypdf's layout extraction because its plain mode dropped text before a combining character; the complete caption was also inspected in the rasterized PDF. The fallback reads PDF bytes and has its own missing-text control.

The [PDF visual review](pdf-proof/FINAL-PDF-REVIEW.md) records the final color and grayscale samples. The independent [PDF resource audit](../publication/PDF-RESOURCE-CHECKS.md) checks fonts, page geometry, navigation, grayscale operators and every content page's normalized text.

The [EPUB review](EPUB-REVIEW.md) confirms all 35 sections, 2,648 checked blocks and 102 image placements. All 54 registered figures pass packaged-resource browser checks at 390 and 768 pixels. Small labels on phones may require zoom; tall figures scroll. Dedicated e-reader pagination and EPUBCheck certification were not tested.

The [production instructions](../../publication/README.md) cover rebuilds and the editable publication package. Source preservation, text extraction, layout, resource and package checks include intentionally failing controls. The source manifest remains separate from the public-download release value of 0.7.5. This work creates a local edition; no commit or deployment was made.

Existing cover provenance, quotation-use decisions, printer-specific cover production and physical proof requirements remain recorded in the publication audits.
