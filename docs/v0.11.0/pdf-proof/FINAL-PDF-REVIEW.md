# v0.11.0 PDF review

Reviewed 2026-10-07 from the final production PDF bytes identified in `final-samples.json`. Reading PDF: 416 pages including cover. Color interior: 415 pages. Grayscale print interior: 416 pages including the added blank final verso. Source preservation covers 35 sections and 296 inherited asset files.

## Automated checks

`pdf-checks.json` binds the PDF text and geometry proof to current source, output, and layout hashes. It checks 2,641 text blocks, all section headings, internal destinations, embedded fonts, and figure geometry. No missing blocks, broken destinations, or layout errors remain. The inherited combining-mark cooling caption is recovered from the matching PDF page using layout extraction; deliberate middle-text removal is rejected.

`docs/publication/PDF-RESOURCE-CHECKS.json` verifies the actual PDF resources, embedded fonts, grayscale conversion, and text preservation. Its negative controls pass. Source/print SVG hash verification and three static scene checks also pass.

`final-samples.json` records 79 raster samples at 150 DPI. Finalization checks their PDF and geometry hashes, page coverage, and every PNG hash. Seven altered-receipt controls are rejected. Raster selection alone is not visual inspection.

## Visual inspection

Root reviewer inspected color and grayscale images with sample numbers 005, 015, 016, 032, 033: physical interior pages 7, 116, 117, 342, 346. These cover the complete title paragraph, ownership insertion including its page break, complete solarpunk insertion, and revised moral call. Text, captions, and the nearby Atlas cutout are legible, with no overlap or clipping. Grayscale sample 040 is the intentionally blank final verso, physical page 416.

Second reviewer inspected color and grayscale images with sample numbers 030, 031, 037, 038, 035, 036: physical interior pages 337, 338, 374, 375, 348, 349. These cover the complete participation insertion, all new Appendix B records, and the retained Bear Flag opening pages. Text is readable and unclipped. The Pima entry continues normally onto page 375. The inherited small lettering inside the box illustration remains low contrast, with a clear external caption.

All new and revised prose is represented in the inspected pages. The other generated samples were not individually inspected in this pass. This review does not claim a page-by-page visual inspection of the full book, physical print acceptance, or new rights clearance.
