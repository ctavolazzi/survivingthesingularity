# First final-build visual review

Reviewed September 27, 2026. This records the first completed v0.10.0 reading
PDF before the two corrections below. It is not the visual sign-off for a
later rebuild.

Reading PDF SHA-256:
`5dc7c96f2225a9abd3c4ddd75fb713229ec7c9f57bcba412ccce2a8208854281`.
The reading, interior, and build-record hashes and all rendering hashes are
recorded in `reading-samples.json`. Ghostscript rendered the samples at 140 dpi.
The source reading PDF hash was unchanged throughout the render batch.

## Corrections required

1. **Co-op portrait's baked-in role text is stale and too small.** Reading page
   99, interior page 98, printed folio 94, displays `coop-cast.png` with Denny
   labeled “network engineer, streamer.” The corrected canonical alt text says
   former logistics worker. The bitmap's role labels are approximately 3pt at
   the placed width and are difficult to read. Correct the visible label and
   provide readable type; preserving the old raster in the repository is
   compatible with replacing its publication use. Evidence:
   `reading-099-cooperative-portraits.png`.

2. **Part III divider spills a sentence onto a mostly empty second page.**
   Reading page 166, interior page 165, printed folio 161, ends with “a dinner
   they.” Reading page 167 begins “can use, a place to live” and contains only
   six continuation lines. The generic `.part` styling in
   `publication/book.css`, lines 95-99 at review time, reserves 0.85in of top
   padding, 0.45in above and below a 2.08in motif, and 11.5pt prose with 1.5
   leading. A compact override for `#sec-part-3` can recover the needed space
   without cutting prose. Evidence: `reading-166-part-3.png` and
   `reading-167-part-3-continuation.png`.

## Inspected coverage

All page numbers below are physical pages of the **reading** PDF. Subtract one
for interior-PDF physical pages; printed Arabic folios start at reading page 6.

| Reading pages | Content inspected |
| --- | --- |
| 1-5 | Cover, title, copyright, both contents pages. |
| 12-13 | Food-insecurity chart, its caption, and following prose. |
| 38 | Part I divider. |
| 98-99 | Part II divider and co-op portrait. |
| 156-157 | Regional-production diagram, caption, and nitrogen equation context. |
| 166-167 | Part III divider and its continuation. |
| 190-193 | Chapter 11 memory and heat equations, cooling diagram, caption, and following prose. |
| 267-268 | Mesh-node diagram and following instructions. The corrected matched-charger/protected-pack labels are present. |
| 271-272 | Fabrication diagram, caption, and following prose. |
| 305 | Conclusion opening. |
| 312-314 | Conclusion's closing narrative, illustration, and last page. |
| 330, 334, 336 | Dense bibliography, epigraph references, and bibliography ending. |
| 344 | Dense Precedent Ledger table with repeated heading and long cell text. |
| 366 | Appendix H discussion questions. |
| 370-373 | All illustration-credit pages and font/design credits. |

Apart from the two listed corrections, these samples show no clipped or
overlapping text, missing mathematical glyphs, detached figure captions, or
unreadable labels in the five redrawn diagrams. Memory subscripts, multiplication
symbols, heat-flow overdots, units, and the heat equation are visibly intact.
Long bibliography and credit links wrap within the page. The ledger's row IDs,
titles, dates, and chapter references remain distinct.

The final bibliography page contains one complete citation entry and substantial
white space. This is a layout tradeoff, not lost or clipped content. Complete
short endings were not treated as failures merely because they were short.

This is a 35-page representative visual review of a 373-page reading PDF, not a
claim to have inspected every page at reading resolution. Grayscale review was
pending when this record was written. Text preservation, navigation, image
rights, accessibility, physical printing, and external-release permissions
require their respective checks. No canonical source, publication output, or
stylesheet was changed by this review.
