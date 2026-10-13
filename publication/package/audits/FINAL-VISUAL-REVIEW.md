# Independent publication visual review

Reviewed 2026-09-22. This is a bounded visual review of the publication design, separate from the full text-preservation and all-page contact-sheet checks.

Final result: no unresolved layout defect remains in the inspected final sample. The earlier orphan ornament and subtitle wrap are corrected. Short, complete chapter endings are retained as a deliberate production choice.

## Reviewed snapshot and coverage

The first inspection used `publication/output/proof-04/Surviving-the-Singularity-interior.pdf`, 229 physical pages, SHA-256 `e2254594f7c9caa6e5cc417dbb28be35d0c967fac95c215ade8f8b63e3438bbc`, and the front-cover PDF in the same directory. Page numbers below are physical PDF page numbers; main-text folios are four lower.

I rendered and visually inspected the cover and interior pages 27, 32, 65, 66, 67, 86, 96, 108, 109, 129, 166, 194, 203, 221, 222 and 223 at 130 dpi. These cover all three part openings, both explanatory diagrams, seven practice blocks, the full precedent ledger and its closing notes. The review renders are retained in `publication/output/proof/final-review/`. `review-snapshot.json` identifies the source used for the initial sample; page 66 was added after inspection of page 65 exposed the possibility of a trailing ornament.

This does not claim that I inspected all 229 pages at reading resolution. It does not establish image-rights clearance, PDF accessibility, correct text extraction or a printer's acceptance of the files. Those require their respective checks.

## Findings on proof 04

| Status | Location | Finding and action |
| --- | --- | --- |
| Correction required | Page 66, printed folio 62 | Only the closing ornament, running head and folio occupy the page. Chapter 5's practice is complete on page 65. Bring the ornament back, keep it with the practice, or suppress the decorative tail when it cannot fit. If a blank verso is intentional before Part II, it should not retain this orphan ornament and running head. |
| Known correction already underway | Front cover | The subtitle leaves “Earth” as a one-word second line. Preserve the subtitle while balancing its line break. This was already identified by the designer before this review. |
| Known reflow already underway | Pages 117, 147 and 205 | The designer has identified sparse endings in Chapters 10 and 13 and Appendix A and is adjusting local spacing. This review does not represent those pending changes as verified. |
| Optional, not a delivery blocker | Page 166, printed folio 162 | Chapter 15 ends with a complete mechanism, rule and three-item practice on a short final page. There is substantial white space, but no split sentence, stranded list item or detached label. Local tightening could recover space if it preserves comfortable type; the complete unit is acceptable as shown. |

The layout record was also searched for main-text pages containing only running heads and folios. Page 66 was the only such page in this snapshot. The visual render, rather than that search alone, confirmed the stranded ornament.

## Revisions that now work

Both diagrams are legible as two-by-two groups. On page 32, each of the four questions has a distinct label and explanatory line, and the note clearly rejects an automatic inference from one answer to another. On page 203, Produce, Prepare, Deliver and Sustain remain separate. The earlier Deliver/Sustain collision is gone; the explanatory note remains inside the same ruled group. Neither diagram requires color to distinguish its meaning.

The ledger on pages 221 and 222 now allocates a narrow column to IDs and useful space to titles and dates. IDs stay intact; longer titles wrap as phrases; dates and chapter references are legible at the rendered size. The continuation repeats the header and does not split a row. The rules and Sources and limits close on page 223 without the formerly isolated ending page.

The practice blocks inspected on pages 65, 86, 96, 108, 129, 166 and 194 retain their labels and all three numbered items together. The defect after page 65 belongs to the trailing ornament, not the list. The two-precedent transition on page 86 also has enough separation to make its change of topic clear.

All three part openings have clean title wraps, clear motifs and readable introductory copy. Their white space acts as a deliberate pause. The more detailed cover illustration remains distinct from the interior ornaments; its grain, roots and articulated arm remain recognizable in the reversed palette. The title remains dominant over the artwork. There is no clipping or artwork/type collision in the inspected cover.

## Final frozen-file recheck

The final files were copied before inspection into `publication/output/proof/final-review/` with the filename prefix `final-`. Independently computed SHA-256 values agree with `publication/output/build.json`:

| Artifact | Pages | SHA-256 |
| --- | --- | --- |
| Color interior | 228 | `554e9988db2d765da6f99b99d16e2f9b67cedba36052f39e160ce67989ad5c7d` |
| Front cover | 1 | `d394a10ace35e566da9b3ba6515b180ee594df5edb051396eb8ac603cf864cb5` |
| Grayscale print interior | 228 | `92de382066ba06acf9eb4ddf088a17fd792895bf7e8af711c879a61c25eab1c0` |

I rendered and visually rechecked the final cover; color-interior pages 32, 65, 66, 67, 117, 147, 203 and 204; and grayscale-interior page 89 at 130 dpi. These renders and `final-review-snapshot.json` remain with the review artifacts.

The cover subtitle now occupies two balanced lines, with “Future of Earth” together. Page 65 retains Chapter 5's full three-item practice; page 66 is now genuinely blank, without an ornament, running head or folio. Part II opens cleanly on the next recto. The defect identified in proof 04 is resolved.

The more compact diagrams on pages 32 and 203 retain distinct cells, readable labels and separation between their explanatory lines. Appendix A now occupies two pages. Its final sentence appears with the preceding discussion on page 204, not alone on a continuation page. Nothing is clipped or pressed into the footer in the inspected ending.

Pages 117 and 147 retain complete mechanism, rule and practice groups on short ending pages. They remain spacious, but neither has a stranded list item or separated label. This is an accepted layout tradeoff, not an unresolved correction. Further compression is not necessary for this bounded visual sign-off.

The grayscale sample on page 89 preserves the Sophia photograph's facial detail and contrast. Its caption, chapter briefing, rules and body text remain readable. The RGB proof render is visually neutral; its maximum channel difference is one level out of 255. This sample supports visual usability after conversion but does not replace a full PDF color-space preflight.

No new collision, clipping or broken grouping was found in this final sample. This sign-off is limited to the pages actually inspected and should be read alongside the separate full-document contact-sheet, source-preservation, font and rights checks. A physical print sample remains appropriate to judge fine cover lines, stock and binding; screen inspection cannot establish those material qualities.
