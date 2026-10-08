# PDF resource checks

Result: **PASS** for the publication PDFs.

Reproduce with `python3 publication/check_pdf_resources.py` from repository root. Dependencies are pypdf, Pillow, and Ghostscript. No network access or source-PDF changes occur. Exact hashes and complete results are in [PDF-RESOURCE-CHECKS.json](PDF-RESOURCE-CHECKS.json).

| Check | Measured result |
| --- | --- |
| Page geometry | All media and crop boxes are 432 by 648 points: True. |
| Page counts | interior: 415, reading: 416, print-interior: 416, front-cover: 1. |
| Print page parity | One empty final print page excluded. Pass: True. |
| Fonts | All discovered page/form/pattern fonts have a nonempty embedded program: True. Resource counts: interior: 10, reading: 10, print-interior: 10, front-cover: 0. |
| Annotations | interior: 817, reading: 817, print: 817. Reading rectangles and targets match after the cover offset: True. Print target multisets match on all interior pages: True. |
| Destinations | Internal: interior: 74, reading: 74, print: 74. External URI annotations: interior: 743, reading: 743, print: 743. All internal destinations resolve: True. Remote URL availability was not tested. |
| Grayscale streams | Fill-gray operators: 9394; stroke-gray operators: 675. Referenced images: 63. Chromatic operations: 0; non-gray spaces: 0. |
| Grayscale render | Pages 1, 5, 28, 139; every sample passes one-level 8-bit RGB neutrality: True. |
| Text | 415 interior pages compared; 0 mismatches. One permitted final empty print page excluded: True. NFKC normalization removes whitespace and soft hyphens while retaining punctuation and text order. |
| Prior ligature defect | Previous ft corruption present: {'interior': False, 'print-interior': False}. Counts of after: {'interior': 77, 'print-interior': 78}; shift: {'interior': 16, 'print-interior': 16}. Example phrase preserved: {'interior': True, 'print-interior': True}. |
| Navigation metadata | Reading labels correct: True. Print labels correct: True. Title and author agree: True. |

## Controls

13 of 13 controls passed. These include accepting equal page counts and one empty final print page; rejecting a truncated print PDF, two extra pages, and a final page carrying a painted rectangle even when it has no extractable text. The font, geometry, annotation, destination, grayscale and text-corruption controls run without modifying the final PDFs. The JSON report lists each outcome separately.

## Limits

This audit verifies resource, navigation, grayscale, and text-layer properties. It does not certify literary accuracy, image permissions, printed appearance, PDF/X conformance, a printer's color profile, or accessibility tagging. Font licenses are packaged separately. Manuscript preservation and visual layout are checked by the main proof process.
