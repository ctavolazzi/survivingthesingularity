# Publication design report

Manuscript: Surviving the Singularity v0.8.2. Design completed 22 September 2026. Author: Christopher Tavolazzi.

## Delivered design

A 6 x 9 inch trade-book layout with a new forest-green illustrated cover, Source Serif 4 reading typography, Source Sans Pro labels, mirrored margins, running heads, roman-numbered front matter, a balanced two-page contents list, and restrained botanical and mechanical artwork. Color is retained in the digital reading copy; the separate print interior is genuinely grayscale.

- Reading PDF: 229 pages including the front cover.
- Print interior: 228 pages, 432 x 648 points, no bleed.
- Front-cover design: one 6 x 9 inch vector PDF.
- Typography: 10.6-point body with 14.84-point leading, 0.8-inch inner margin, 0.64-inch outer margin, 0.68-inch top and 0.7-inch bottom. Some reference and closing material uses a deliberately smaller setting.
- Artwork: 12 original interior SVG masters and a separate detailed harvest illustration. Eleven interior motifs are placed in the book; the open-gate alternative remains in the master art library. Two explanatory diagrams clarify capability versus access and the work between production and a usable meal.
- Retained art: 18 photographs or scientific images with documented commercial-use/public-domain bases, and ten narrative illustrations with PixelLab generation provenance. Reused photographs reproduce at a minimum of approximately 301 pixels per inch in the final layout.
- Editable production: HTML, CSS, SVG, packaged fonts and licenses, unchanged manuscript files, build scripts, source records, and a portable ZIP.

The design follows the book's expressed position: useful machines should help make ordinary life more secure. Grain, roots, tables, repair tools and structures supply its visual vocabulary. Space and ornament distinguish fiction, argument, historical cases and practical reflection without adding a competing graphic narrative.

## Preservation and exact exceptions

All 30 canonical manuscript files still match their baseline SHA-256 values. Narrative, arguments, history, references and retained epigraphs are unchanged. The publication transformation replaces three old part-divider images, four photographs or artworks with unresolved reuse questions, and the old cover. The originals remain on disk.

Four image captions are omitted with the corresponding replaced image. Six additional image captions receive identification or attribution corrections. The factory photograph depicts a museum exhibit; the Haifa photograph depicts an abandoned bar within a shopping mall. Other corrections restore required names, edit credits or license information. Exact old/new captions and asset substitutions are in `publication/output/build.json`, supported by `asset-rights.json` and `RIGHTS-AUDIT.md`.

## Critique and revision

Independent typography, illustration and image-rights reviews informed the design. The proofing cycle found and corrected:

1. A real font text-layer defect: an ft ligature looked correct but extracted as an unrelated character. Disabling the relevant ligatures preserves correct searchable/copyable text.
2. A PDF-merging route that dropped link annotations. The reading copy now clones the complete interior and inserts the cover, preserving its destinations.
3. Crowded four-column explanatory diagrams. They now use two columns and two rows with an explicit gutter.
4. Pandoc column widths overriding the precedent ledger's proportions. The conflicting colgroup is removed, and the ledger is set at nine points with repeated headers.
5. A practice item and an ornament stranded on separate pages. Closing practices stay together, and decorative end rules cannot create orphan pages. The blank verso before Part II is intentional and has no ornament, running head or folio.
6. An isolated Appendix A closing sentence and a one-word cover subtitle line. Both are resolved.
7. Incorrect or incomplete inherited image identifications and attributions, as detailed in the rights audit.

Short, complete closing practice passages remain on some chapter-ending pages. They are intentional stopping points, rather than a reason to compress the surrounding text excessively. Print and screen proofing cannot establish paper opacity, binding behavior or press output; a physical proof remains the next production check.

## Verification

The rendered proof recovers 1,483 source or corrected-caption text blocks with zero missing blocks, confirms all 30 sections, finds no text outside a page, resolves all internal HTML links and finds every included image. All actual PDF font resources are embedded. All 378 annotations are preserved in the reading edition, including 62 internal destinations and 316 external links. Print and color text match across all 228 interior pages; grayscale was verified in PDF resources, content operators and rendered pixels. Retained image sources were individually checked, and all 18 third-party files match source pixels.

All pages were examined in full-book contact sheets during design. Independent reviews inspected the cover, all three part openings, diagrams, caption/image groupings, exercises, bibliography, ledger and grayscale reproduction at reading size. Final altered layouts were revisited against recorded PDF hashes. See `FINAL-VISUAL-REVIEW.md`, `READING-DESIGN-REVIEW.md`, `PDF-RESOURCE-CHECKS.md`, and `publication/output/proof/checks.json` for coverage and limits.

Proof checks were tested against deliberately absent text, a removed known paragraph, invalid bounds, missing resources and excluded assets. The early failing proofs and the corrected outputs distinguish actual defects from limitations of the extraction instrument. In particular, generated list counters and running folios are excluded from paragraph-preservation comparisons; actual years and prose are retained.

## Remaining external-publication decisions

The layout work is complete. This delivery is a publication design proof, not a claim that a printer or publisher has accepted it.

- Select the printer, binding and paper before sizing a full back/spine/front cover wrap. The front-cover artwork is supplied; an ISBN, barcode, imprint and printer-specific spine have not been invented.
- Resolve the external-release basis for modern or still-protected epigraphs, especially Vinge, Good and Mitchell. They remain in this private proof. Attribution was checked, but permission was not established. The rights report identifies all eleven retained epigraphs individually.
- Review a physical proof for reproduction and binding before approving a print run.

The generic trim and margins exceed the relevant minimums in [KDP's trim, bleed and margins guidance](https://kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6). That is a dimensional reference, not a claim of vendor upload acceptance. [KDP's paperback-format guidance](https://kdp.amazon.com/en_US/help/topic/G201834190) describes the separate interior and full-wrap cover files required for that route.

No files were published, uploaded, committed or deleted. Earlier manuscript versions and PDFs remain intact.
