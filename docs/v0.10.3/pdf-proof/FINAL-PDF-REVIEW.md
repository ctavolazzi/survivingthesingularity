# Final PDF visual review, v0.10.3

All eight new graphics and all five targeted typography and pagination refinements pass the final review. Captions are complete, remain with their images, and stay clear of prose and folios. The final credits correction removes the short provenance leaf without dropping text or reducing font sizes.

## Reviewed artifacts

This review uses the actual 407-page color interior and 408-page grayscale print interior, which adds an empty final verso. The reading PDF adds the original cover to the color interior, for 408 pages. Pages below are physical interior pages; add one for the reading PDF. Printed Arabic folios are four less than the interior page number.

| Artifact | SHA-256 |
| --- | --- |
| Color interior | `caa4a051f63c31ef04d6e3084c5e995aaf16b02b956e46c36520b8e2c5856782` |
| Grayscale print interior | `4795bea3392ac2a45409fb2cf185f57914d466ec9b2cac179d3a10cafe5e284b` |
| Reading PDF | `bc7a867a3ba359ffc4bb07b7112fd84705eea5b0748e93de17dc95fca6f46171` |

Color rasterization used the resource-pruned prepared PDF, whose page streams and annotations were checked against the color interior by the separate production proof. Its SHA-256 is `c5383ed817145e618a6ca7e2f473eddacec1169d3bbc2f3491eff40efdaa2538`. All inspected rasters were generated at 120 dpi. Exact source, layout and image hashes are in [final-review.json](final-review.json), [final-samples.json](final-samples.json), and [extra-page capture receipts](final-polish-extra/samples.json).

## Eight new graphics

Every row was inspected as a color/grayscale pair. After the final credits rebuild, all sixteen new-art PNGs were byte-for-byte identical to those inspected images. [Comparison images](review-pairs-v103/) preserve the actual page around each graphic, including captions and following text.

| Interior page | Graphic | Visual result |
| --- | --- | --- |
| 24 | Reading routes | Numbered routes, chapter labels and arrows remain readable in grayscale. The page has one main title and a complete caption. |
| 34 | Bear Flag toast | Raised glasses, laptop and Elijah's expression remain distinct in grayscale. The fictional-scene caption and subsequent narrative fit comfortably. |
| 80 | The near end | Window, coffee, closed laptop and notebook remain distinct. The caption fits below the image near the page bottom without entering the folio. |
| 122 | Passing the beans | Bowl exchange, people, table and dog retain readable separation in grayscale. Caption and continuing narrative remain together. |
| 322 | Rosa's testimony | Rosa, wrist brace and microphone remain distinct from the audience. Caption and narrative fit below the illustration. |
| 369 | Continuing service ledger | All four cost labels remain legible. Column structure and check marks carry meaning independently of color. |
| 386 | Offline-copy check | Four steps, numerals and device illustration remain legible. Caption and the Tier 1 and Tier 2 text fit below. |
| 394 | First-year index | All twelve labels fit. The final wrapped label stays within its column. Caption and the Month 1 opening remain on the page. |

The new graphics do not create a title-only opening in their sections. The illustrated reference openings on pages 24, 369 and 394 combine titles, explanatory prose and art. Grayscale preserves the illustrations' principal gestures and objects; the four SVGs use direct labels and shapes rather than color alone.

## Changed transitions

The final extra captures include color/grayscale pages 173, 319, 320, 374, 403, 404 and 407, plus the print edition's empty page 408, retained in [final-polish-extra](final-polish-extra/). The unchanged transition pages and final credit-entry page match the prior inspected rasters byte for byte. The revised credits opening, first entry page, ending and blank verso were inspected again.

- **How to Use This Book, page 24:** the duplicate eyebrow is gone. The new route map follows the existing route list.
- **Greenhouse explanation, page 173:** the heading, sensors, actuators, installation instructions, PID equation and manual-control explanation occupy a coherent 264-word page. The component map and full caption follow on page 174. The former 34-word page stub is gone.
- **Chapter 19, pages 319 to 320:** the previous chapter's closing practice occupies page 319; Chapter 19 starts on the next page with title, quote, summary and story, totaling 259 body words. No intervening empty or title-only page remains. The ladder and caption now occupy page 326 after the plan introduction.
- **Appendix D, page 374:** its 347-word opening reaches the operating procedure. The full timeline and caption appear after the ledger on page 377. The timeline's approximate spans remain visibly dashed in grayscale.
- **Credits, pages 403 to 407:** provider attribution correctly distinguishes the four new image_gen illustrations from nineteen earlier PixelLab plates. Both unchanged provenance paragraphs now appear with the credits introduction on page 403; individual entries begin on 404. The book ends on page 407 with 272 body words of credit entries. The prior 57-word provenance leaf is gone. All 26 entries and links are retained, and type sizes are unchanged. The print-only page 408 is visibly empty, including running head and folio.

The relocated greenhouse, ladder and timeline figures were also inspected in their final positions. Their labels and captions remain complete and readable.

The [superseded review](PRE-CREDITS-FIX-REVIEW.md), [prior receipt](pre-credits-fix-review.json) and [old ending rasters](polish-extra/) retain the observed 57-word leaf as failing-control evidence. They do not describe the final PDFs. The [bounded credits proof](credits-fix/bounded-check.json) established text/link preservation before the full rebuild.

## Review limits

This is a targeted visual review of all eight new graphics and selected changed transitions. It does not claim inspection of every book page. Full-text coverage, font resources, link destinations, page geometry and grayscale-operator checks are separate production proofs. On-screen raster review does not replace a physical proof from the intended printer.
