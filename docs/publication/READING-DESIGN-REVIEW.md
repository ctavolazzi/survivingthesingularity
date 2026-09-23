# Reader design review of v0.8.2

Reviewed 2026-09-22. This review concerns reading design and production behavior, not another edit of the manuscript. The 6 by 9 inch publication edition is a separate rendering of the preserved v0.8.2 source.

## What the current proof establishes

The existing PDF is 175 US Letter pages, with a 612 by 792 point media box. It has legible prose, functioning image credits, repeated table headers, clear chapter starts, and useful navigation. Its layout is still a review copy. The long lines, generous paragraph gaps, prominent colored headings, and blue underlined citations make it feel closer to a formatted report than a trade book.

I inspected current PDF pages 3, 4, 19, 22, 27, 61, 97, 148, 167, 171, and 172. These cover contents, image-led chapter openings, narrative, historical cases, bibliography, and the precedent ledger. I also read the active print stylesheet, publication plan, build overrides, and source image-caption patterns. Existing proof images and PDF page numbers refer to the Letter edition, not to the forthcoming publication edition.

The image-led openings need the most restraint. On page 61, the chess photograph occupies most of the page before the chapter briefing. Page 22 fits only one sentence of narrative beneath its image, epigraph, and briefing. This leaves an attractive photograph in charge of the reading rhythm. At 6 by 9 inches, these images must become smaller or more selective if the reader is to enter the argument promptly.

## Proposed reading system

These are starting values to test in the actual proof, not universal publishing rules or a substitute for a printer's specifications.

| Element | Recommended starting treatment |
| --- | --- |
| Trim | 6 by 9 inches; keep the reading cover separate from the print interior. |
| Margins | Mirrored 0.8 inch inside, 0.65 inch outside, about 0.7 inch top and 0.75 inch bottom. Reassess inside margin once page count and binding are known. |
| Prose | Source Serif 4 Regular, about 11 points with 15 points leading. Start ragged right with controlled hyphenation, then judge full pages. Do not compress type to meet an arbitrary page count. |
| Paragraphs | A modest first-line indent and small or zero paragraph gap in sustained prose. No indent immediately after headings, images, lists, or deliberate section breaks. Preserve real scene breaks. Avoid both large indentation and large paragraph gaps. |
| Emphasis | Genuine italic and semibold font faces, not synthesized styles. Keep existing emphasis; do not add decoration to persuasive sentences. |
| Chapter label | Source Sans Pro Semibold, small and distinct from the title. The existing chapter number and title wording should remain available in navigation and text extraction. |
| Chapter title | Source Serif 4 Semibold around 23 to 25 points, comfortable line spacing, natural wrapping. Avoid all-capital treatment of long titles. |
| Foundations | A clear transition into explanatory material, established through space and a consistent label. Its internal subsections should be visibly quieter. |
| Historical cases | Distinct heading and modest top rule or space. Keep title with its opening paragraph; do not force every case onto a fresh page. |
| Running heads and folios | Source Sans Pro, about 8 to 8.5 points, strong enough for print. Short heads that cannot collide with folios. Suppress heads on part and chapter opening pages. |
| Color | Near-black prose and headings in the print interior. A subdued accent can remain in the reading edition, but no distinction should depend on color alone. |

Source Serif 4 and Source Sans Pro form a coherent pairing without imitating a particular publisher. Adobe describes Source Serif as a companion to Source Sans. The packaged Source Serif 4 assets provide static regular, italic, and semibold faces. Source Sans Pro 3.006 provides regular, italic, semibold, and semibold italic. Source Sans 3 was the initial preference, but repeated official download attempts stalled. The licensed local Source Sans Pro distribution supplies a complete, verifiable alternative without relying on a system fallback. Do not synthesize a semibold italic serif face if the matching asset is unavailable. See the packaged [font provenance and licenses](../../publication/assets/fonts/SOURCES.md).

A real-size printed spread is still necessary. Screen inspection can find collisions and hierarchy problems, but it cannot establish comfort in a bound paperback.

## Hierarchy and navigation

The current contents page gives part dividers and ordinary chapters almost the same visual importance. Give each part a restrained, distinct row and space above it. Keep chapters subordinate, with a hanging entry when a title wraps and page numbers consistently aligned at the outside edge. Long chapter names should wrap naturally rather than push the folio outside the text block.

Chapter openings can start on the next available page. Reserving right-hand pages for parts is sufficient for this book unless the eventual design deliberately calls for more blank versos. Avoid creating empty pages merely to signal importance already established by a heading.

Do not treat every level-two Markdown heading as equally important. The Foundations label, an argument subsection, and a precedent title perform different jobs for a reader even when their source heading level is the same. A publication transformation can assign presentation classes without changing the manuscript's words or order.

The alternating narrative and explanatory sections are already the book's organizing feature. Make those transitions clear through spacing and typography before adding any new graphic treatment. Large shaded boxes around all historical material would add bulk and fragment sustained reading.

## Images, captions, and credits

The existing source supplies a Markdown image followed by a separate italic caption paragraph. The build hides Pandoc's generated figcaption, avoiding a second caption made from the alt description. The actual caption and credit do remain visible. The problem to solve is grouping, sizing, and typographic treatment, not restoring missing text.

In the publication transformation, combine each image with its real adjacent caption and credit into one figure group. Keep the group together when it fits a page. A tall illustration must have a sensible maximum height so that an unbreakable figure cannot overflow the available area. Preserve aspect ratio and the complete subject; do not stretch photographs to fit a template.

Start ordinary chapter-opening images at no more than roughly 2.5 to 3 inches high, with smaller limits where a long heading and epigraph also need room. This is a ceiling to test, not a command to make every image equally large. Narrative illustrations should appear near the passage they illustrate without consuming a whole page unless that pause is intentional.

Set captions in Source Sans Pro around 9 points with about 12 points leading, left aligned, with a small gap above. Caption meaning comes first, followed by the original credit and license information at readable size. A license credit is not decorative microtype. Do not italicize a long block of source and licensing information merely because the Markdown paragraph uses emphasis.

Do not expose alt text as a duplicate printed caption. Retain useful alt descriptions in the HTML output. Do not imply PDF accessibility solely because HTML alt attributes exist; PDF tagging and reading order need their own validation.

A separate rights audit determines whether each inherited image may remain, needs a replacement, or needs revised attribution. Reading design should preserve the current source caption and the audit's required credit in the publication output. Any substitution belongs in a recorded transformation, not an unannounced manuscript edit.

Inspect monochrome proofs of dark machinery, space photographs, diagrams, and small labels. A grayscale conversion alone does not prove that important distinctions remain visible. New diagrams should clarify the book's existing distinctions and should not introduce unsupported process arrows, quantitative claims, or promised outcomes.

## Tables and lists

Appendix D is the clearest current defect to fix before shrinking the trim. On pages 171 and 172, four equal-width columns devote as much space to a short precedent ID as to a title or date range. The table remains readable on Letter paper but spends width where there is almost no content.

Start its column proportions near 11 percent ID, 44 percent precedent, 27 percent date, and 18 percent chapter reference. Test the longest title and date cells. Keep IDs intact, allow real phrases to wrap, and avoid arbitrary character breaks inside ordinary words. The exact proportions may change after inspection.

Use Source Sans Pro around 9.5 points with 12 to 13 points leading for dense reference tables. Repeat headers on continuations. Keep each row together when it fits, but permit a long table to span pages. Do not apply an unbreakable rule to the entire table. Horizontal rules and padding can carry the structure with less visual noise than a full grid.

If four columns remain cramped, change the table presentation in the publication layer before reducing its type further. A compact stacked entry can preserve the same data. Other tables need their own widths; the precedent ledger's solution should not become a global fixed-width rule.

Lists should retain obvious hanging indents and modest space between items. Keep a short lead-in with at least the first item. A three-item chapter briefing should be easy to scan and visually subordinate to the prose it introduces.

## Bibliography and source links

On page 167, long blue underlined source titles repeatedly pull attention away from the annotations. Set print links in the same dark color as surrounding text and remove the underline, while retaining the actual link annotations in the digital PDF. This changes appearance, not citation content.

Start bibliography prose near 10 points with 13 points leading. Give entries enough separation to distinguish one source from the next. Use hanging indents where an entry's structure supports them, without turning a multi-paragraph annotation into a narrow indented block. Keep a subsection heading with its first entry; keep a short citation together when practical, but allow long annotations to continue naturally.

Maintain source titles, author and institutional identities, dates, and the existing bibliography groupings. Do not replace them with bare hyperlinks, tiny footnote numbers, or an undocumented new citation system. Clicking is useful in a PDF; a printed reader must still be able to identify the source.

## Proof acceptance questions

1. At actual reading size, do the prose and captions remain comfortable without zooming?
2. Does every chapter opening admit the reader to the book rather than spend its page on a generic illustration?
3. Are figure captions and required credits attached to their images, with no duplicated alt captions?
4. Can the contents page, long chapter titles, and ledger be read without compressed letters or awkward broken words?
5. Do chapter, Foundations, subsection, and precedent headings have distinct and consistent roles?
6. Are short headings kept with meaningful text, with no stranded list lead-ins or one-line narrative starts where they can reasonably be avoided?
7. Are the provided font faces actually embedded in the final PDF, without accidental fallback fonts?
8. Do the print and reading editions preserve all manuscript prose and references, with any rights substitutions explicitly recorded?
9. Do diagrams, images, rules, and credits remain intelligible in the print edition's monochrome treatment?
10. Have all pages been scanned as contact sheets and representative difficult pages examined at full size, rather than trusting text extraction alone?

## Limits of the initial review

These recommendations are based on the existing Letter proof and source behavior. They are not approval of a 6 by 9 inch PDF that has not yet been built. Final line lengths, image balance, gutter adequacy, page turns, typography, and font embedding must be assessed on the new artifact. Publisher or printer-specific bleed, cover wrap, paper, binding, and production requirements remain separate from this reading-design review.


## Independent critique of the publication proof

The initial 230-page second proof was inspected for page flow and short ending pages. The build then advanced during review. To avoid mixing artifacts, I made a stable 228-page snapshot of the updated interior and rendered selected pages at 120 dpi with Ghostscript. The detailed findings below use **physical PDF page numbers in that 228-page snapshot**. Printed folios are four lower after the four frontmatter pages. Later builds must be checked again at the changed locations.

Snapshot SHA-256: `fd629fa738fe49b07506a7594944453484582fd94b1fe9bc75bcd91daded7389`.

High-resolution pages inspected: 3, 4, 5, 6, 14, 28, 52, 65, 66, 89, 118, 139, 166, 203, 205, 207, 211, 221, 222, 224, 227, and 228. I also inspected preliminary contact thumbnails and the renderer's layout records. This is a representative-page review, not a claim that I personally inspected all 228 pages at reading resolution.

### What is working

The serif has a comfortable reading texture at the selected measure. Chapter titles wrap cleanly, paragraph rhythm is consistent, and chapter labels are easy to distinguish from titles. The two-page contents is balanced and the page-number column remains clear. Roman frontmatter and Arabic main-text folios are coherent. The smaller chapter photographs leave room to begin the narrative on the same page. The briefings inspected on pages 28, 52, 89, 118, and 139 remain together and do not leave isolated headings behind.

Captions remain attached to their images in the inspected openings. The title, photograph, credit, quotation where present, briefing, ornament, and opening prose form a repeatable sequence. The chapter 4 opening has relatively little narrative beneath that sequence, but enough to read as an opening rather than a stranded single sentence. Do not shrink every opener to fix a few end-of-chapter fragments.

The bibliography is readable and its subsection labels are useful. It does not need another wholesale design. Quieting the underlined source titles remains an optional improvement for the print interior; preserving working digital links matters more than removing every underline.

### Corrections needed before calling the interior finished

| Priority | Location | Finding | Practical correction |
| --- | --- | --- | --- |
| Required | Page 6, printed folio 2, and other prose | The visible word “after” is correct, but pypdf extracts “aƤer” in “silence aƤer the ﬁrst one.” This is not normal Unicode presentation-ligature normalization. | Investigate the font's PDF ToUnicode mapping or disable the affected ligatures in the PDF typesetting. Retest copied and extracted text using the same phrase. A visual proof cannot detect this defect. |
| Required | Pages 65 to 66, printed 61 to 62 | The final numbered practice item alone moves onto a mostly empty page, separate from its lead-in and first two items. | Keep each short practice block together, then use a modest local spacing adjustment to avoid the extra leaf where possible. Do not move just the third item back by reducing all body type. |
| Required | Page 205, printed 201 | Appendix A's last two-line sentence occupies a page by itself. | Pull the sentence back through a small appendix-specific spacing adjustment, or rebalance the section. Preserve the sentence. |
| Required | Page 203, printed 199 | The four-part food diagram gives Deliver and Sustain too little separation. “Access the person” visually runs into “People, repairs and…” in the next cell. | Establish a real gap between cells and allow their text to wrap. A two-by-two layout is another option, but assess its effect on Appendix A's page count. |
| Required | Pages 221 to 222, printed 217 to 218 | The ledger still renders four equal-width columns. A short ID receives the same width as a long title or date. This is visible despite intended width rules in the CSS. | Change the emitted colgroup widths or remove that colgroup before assigning explicit widths. Check the actual result after increasing table type. The table's titles should gain width and its IDs should lose it. |
| Required if delivered as monochrome | Pages 28, 89, 118, and 139; credits 227 to 228 | The inspected interior contains colored photos and green rules, while its credit text says grayscale conversion occurred in the print interior. | Apply a verified print conversion or correct the claim. Inspect the actual final interior; a stylesheet declaration alone is not proof of monochrome output. |
| Improve | Page 166, printed 162 | A complete but very short practice block occupies a nearly empty ending page. | Try a small local spacing reduction to pull the block back. Keeping the complete block together is already preferable to the split on page 66. |
| Improve | Page 224, printed 220 | The short Sources and limits section occupies its own mostly empty final ledger page. | Improved ledger column widths may recover enough space. Check again after that fix before adding another special page rule. |
| Optional | Cover and title-page subtitle | “Earth” was stranded as a one-word second line in the initial cover/title treatment. | Preserve the subtitle wording but use a balanced line break, keeping “Future of Earth” together if necessary. Reassess the new cover art before finalizing. |

Some short ending pages, such as the roughly third-page closing material at page 14, are reasonable chapter endings. The goal is not to fill every page. The specific defects above are separated from normal whitespace because they split a short unit or strand a very small continuation.

### Colophon and glyph check

The colophon correctly names **Source Serif 4** and **Source Sans Pro**. The font binaries' designer metadata names **Frank Grießhammer** and **Paul D. Hunt**, respectively. Both names, including the ß in Grießhammer, render correctly in the inspected credit page. Adobe and SIL Open Font License 1.1 are correctly identified. The packaged font names, copyright notices, original licenses, and provenance manifest agree with those statements.

This check does not certify the separate image-rights claims. The publisher's production record must agree with whichever images, adaptations, and credits survive the rights pass. In particular, the claimed grayscale adaptation must match the delivered print artifact.

### Recheck after revision

Render the affected practice endings, Appendix A diagram and last page, both ledger pages, and the final image credits again. Confirm that any ligature change preserves both appearance and text extraction. Verify actual monochrome output if that is the delivered print interior. A final PDF with the wrong text layer or a falsely described color treatment should not receive a passing grade merely because its typography looks good.
