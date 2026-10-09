# PDF resource checks

Result: **PASS** for the frozen publication PDFs.

Reproduce with `python3 publication/check_pdf_resources.py` from repository root. Dependencies are pypdf, Pillow, and Ghostscript. No network access or source-PDF changes occur. Exact hashes and complete results are in [PDF-RESOURCE-CHECKS.json](PDF-RESOURCE-CHECKS.json).

| Check | Result |
| --- | --- |
| Page geometry | Every media and crop box is 432 by 648 points, equivalent to 6 by 9 inches. |
| Page counts | 228 color interior, 229 reading, 228 grayscale print interior, 1 front cover. |
| Fonts | Every discovered page/form/pattern font resource has a nonempty embedded font program. Resource counts: interior: 5, reading: 7, print-interior: 5, front-cover: 2. |
| Annotations | All 378 annotations survive in reading and print. Reading per-page rectangles and targets match after the one-page cover offset. Print target multisets match without assuming annotation order. |
| Destinations | All 62 internal destinations resolve in each applicable PDF; 316 external URI annotations are retained. Remote URL availability was not tested. |
| Grayscale streams | All inspected print streams use gray operators: 920 fill and 139 stroke operations. All 28 referenced image resources are gray. No chromatic operations or non-gray image/shading spaces were found. |
| Grayscale render | Pages 1, 5, 28, and 139 pass the one-level 8-bit RGB neutrality tolerance. Photographs show at most one level of channel rounding during Ghostscript conversion; gray PDF resources independently establish grayscale representation. |
| Text | All 228 pages match after NFKC and removal of whitespace and soft hyphens. Punctuation and text order are retained. |
| Prior ligature defect | No previous ft corruption remains. Both files contain 50 instances of after and 9 of shift. The phrase silence after the first one extracts correctly. |
| Navigation metadata | Reading labels begin Cover, i, ii, iii, iv, 1, 2. Print begins i, ii, iii, iv, 1, 2, 3. Title and author agree. Color interior retains default physical-page labels. |

## Negative controls

The checking functions reject a font missing its program, a page one point too wide, an unresolved destination, a removed annotation, a red vector instruction, an RGB image color space, the previous aƤer text corruption, and a deliberately red raster pixel. All eight controls rejected their defective input without modifying the final PDFs.

## Limits

This audit verifies resource, navigation, grayscale, and text-layer properties. It does not certify literary accuracy, image permissions, printed appearance, PDF/X conformance, a printer's color profile, or accessibility tagging. Font licenses are packaged separately. Manuscript preservation and visual layout are checked by the main proof process.
