# Final PDF visual review: v0.10.0

Reviewed September 27, 2026. **No blocking visual defect remains in the inspected
final samples.** Both defects found in the first build were corrected and
visually rechecked in the delivered PDFs.

## Exact artifacts

| PDF | Pages | SHA-256 |
| --- | ---: | --- |
| `Surviving-the-Singularity-reading.pdf` | 372 | `b9c0c84bab4b4f981ed06b47ce7f6f476f899c0a761734e7dba0bb4c47e4e0d9` |
| `Surviving-the-Singularity-interior.pdf` | 371 | `897183981e282cf32d219a67256d794572ab59f9bce257ded27d630f09384fec` |
| `Surviving-the-Singularity-print-interior.pdf` | 372 | `4f5e2b7da63b7f63c5a37034094430fd44b6fdf362bc7d0167f38822bf9cf569` |

The grayscale file has 371 content pages and a final blank verso. All three
hashes remained unchanged during sample rendering. `final-samples.json` records
these hashes, the sample image hashes, and the mapping of earlier reviewed
pages onto final pagination. Final renders are in `final/` at 140 dpi.

## Resolved defects

- **Co-op portrait:** reading page 99, interior/print page 98, folio 94, now uses
  `coop-cast.svg`. Four readable portraits have separate live labels. Denny is
  correctly described as a former logistics worker and co-op media operator.
  The caption stays on the same page. Both color and grayscale were inspected.
- **Part III divider:** reading page 166, interior page 165, folio 161, now
  contains its heading, motif, and all three prose paragraphs on one page.
  Reading page 167 begins Chapter 10, with no stranded divider continuation.
  The contents now points to Chapter 10 at folio 162; subsequent entries reflect
  the one-page reduction.

## Final samples inspected

These are physical PDF pages, not printed folios.

| Edition | Pages | Content |
| --- | --- | --- |
| Reading | 1, 4, 5 | Cover and both contents pages. |
| Reading | 99 | Corrected co-op portraits and caption. |
| Reading | 166, 167 | Complete Part III divider and following Chapter 10 opening. |
| Reading | 189, 190, 191 | Chapter 11 memory and heat equations, cooling circuit and caption. |
| Reading | 266, 270 | Corrected mesh-node and fabrication diagrams. |
| Reading | 304 | Conclusion opening. |
| Reading | 343 | Dense Precedent Ledger table. |
| Reading | 369 | Illustration and font-credit opening. |
| Grayscale print | 11, 98, 190 | Food-insecurity chart, corrected portraits, cooling circuit. |
| Grayscale print | 372 | Visibly blank final verso. |

All eighteen final samples were visually inspected. The chart's solid and dashed
series remain distinguishable in grayscale. Cooling arrows retain clear paths
and text labels without relying on their color. Math subscripts, overdots,
operators, and units remain intact. Dense table cells and credit URLs wrap
within the page. No caption in this sample is detached from its image.

The preceding 35-page inspection covered all five redrawn diagrams, all three
part openings, chapter and appendix flow, the Conclusion's closing narrative,
and all credit pages. Its evidence is retained in `FIRST-PDF-REVIEW.md` and
`reading-samples.json` under the earlier PDF's hash. The final remapping does
not claim those unchanged pages were all rendered again. The complete short
bibliography ending remains an accepted whitespace tradeoff.

This is a bounded digital visual review. It does not claim a reading-resolution
inspection of every final page, certify physical print quality or accessibility,
or settle quotation and image rights. Full text, image, navigation, resource,
and packaging checks are recorded by their separate production instruments.
No manuscript, stylesheet, or publication output was changed by this reviewer.
