# v0.11.0 EPUB review

Reviewed 2026-10-07 by Codex. Targeted visual inspection passes for the ten
screenshots listed below. These captures use the actual packaged XHTML, CSS and
resources in Chrome 150.0.7871.125, with page JavaScript disabled.

EPUB SHA-256: `b759dd2a23bdc0bb739a4dcc7ea8b25617cdc0cb63fff8be8176ab6d4c64048d`.

| Addition inspected | 390 px screenshot | 768 px screenshot |
| --- | --- | --- |
| Introduction: immediate survival and ownership definition | [Introduction, phone](epub-proof/02-introduction-additions-390.png) | [Introduction, tablet](epub-proof/02-introduction-additions-768.png) |
| Chapter 6: Whose robots? | [Ownership, phone](epub-proof/08-chapter6-additions-390.png) | [Ownership, tablet](epub-proof/08-chapter6-additions-768.png) |
| Chapter 19: Get involved | [Participation, phone](epub-proof/27-chapter19-additions-390.png) | [Participation, tablet](epub-proof/27-chapter19-additions-768.png) |
| Conclusion: A future called solarpunk | [Solarpunk, phone](epub-proof/21-conclusion-additions-390.png) | [Solarpunk, tablet](epub-proof/21-conclusion-additions-768.png) |
| Appendix B: Ownership, participation, and solarpunk | [Sources, phone](epub-proof/23-appendix-b-additions-390.png) | [Sources, tablet](epub-proof/23-appendix-b-additions-768.png) |

The inspected text is legible, headings clearly separate the additions from their
preceding passages, and paragraph spacing follows the existing edition. Links
wrap within the available width. The new Appendix B heading occupies two lines
at phone width without collisions. No horizontal clipping, overlapping text or
broken glyphs are visible in these captures. Content above or below each viewport
is outside that screenshot's visual coverage.

Independent automated coverage is broader than the screenshots. The
[structural report](epub-checks.json) checks all 35 sections, 2,690 freshly
rendered source blocks and 110 source artwork placements. It finds no missing
text, artwork or resource references. Six deliberately broken in-memory inputs
are rejected, including a deleted real paragraph and missing artwork.

The [artwork reflow report](epub-proof/checks.json) measures all 62 registered
figures at both widths and rejects a deliberately oversized, floating figure.
The [addition report](epub-proof/additions.json) measures 35 new or revised text
nodes at each width, including the updated closing imperative. All 70 measurements
have visible text within horizontal bounds. Replacing a real new paragraph in
the browser causes the content check to fail; restoring it passes.

This review covers the ten displayed viewport captures. Remaining paragraphs and
the revised closing imperative received automated content and bounds checks,
not separate visual inspection here. The eighteen retained-art screenshots were
generated but were not visually reviewed in this pass. Chrome reflow does not
establish dedicated EPUB-reader pagination, physical-device acceptance or a
visual review of every page. No manuscript or artwork was changed during proof.
