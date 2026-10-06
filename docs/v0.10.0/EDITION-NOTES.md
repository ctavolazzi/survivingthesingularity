# Surviving the Singularity v0.10.0

Final local manuscript edition, September 27, 2026. Author: Christopher
Tavolazzi. Subtitle: *We Don't Have to Live Like This*.

The user selected the standard minor release **v0.10.0** from the latest
actual source version, **v0.9.2**. The v0.9.3 worktree had the same v0.9.2
manifest and commit, not a later manuscript. Work is isolated in
`active/sts-v0.10.0`, branch `book-v0.10.0`, based on `3d29215`.
The previous worktrees and their source files are preserved. No commit,
merge, deployment, public-download swap, or publisher submission was made.
The public-release manifest remains v0.7.5.

## Manuscript

All 35 manifest sections were read: opening material, Chapters 0 through 19,
three part dividers, the Conclusion, and Appendices A through H. The final
source is 95,052 words by `sts book --json`; the block index counts 99,184
words including its broader treatment of markup and references. These are
separate instruments, not interchangeable estimates. All 24 precedents
remain present and indexed.

The review used the repository's voice guide, character protocol, source
rules, prior edition notes, editorial decisions, research and citation
records, artwork catalog, and publication audits. Current author decisions
take precedence over earlier abandoned proposals. The food-first position,
three registers, money-optional proposal, Thanksgiving 2027 forecast and its
test, and three-year Elijah narrative remain. No new first-person mission
or motive was supplied for the author.

The material corrections are documented in three coverage reports:

- [Opening review](OPENING-REVIEW.md): animal labor, Transformer training and
  generation, model-access chronology, electricity versus communications,
  thermodynamics, energy estimates, food-insecurity categories, Sousa's
  recording history, and unsupported attention and recovery mechanisms.
- [Manual and Conclusion review](MANUAL-REVIEW.md): model-collapse scope,
  hardware-memory and cooling assumptions, building-envelope promises,
  donation law, mesh routing and key handling, land-trust limits, DC losses,
  eligibility for counsel, proposed versus implemented services, and the
  route-funding deadline. The character protocol now follows the current
  three-year narrative and December funding decision.
- [Appendix review](APPENDIX-REVIEW.md): glossary alignment, bounded cyberdeck
  instructions, encryption and radio limits, precedent lessons, seasonal
  practice guidance, and integration of the new primary references into
  Works Cited.

This is an editorial and targeted factual review informed by prior evidence
work. It is not an independent re-verification of every historical citation
or an engineering validation of the projects described.

## Figures and production

Five formerly undersized diagrams were redrawn as editable SVGs: regional
production, cooling loop, fabrication lab, mesh node, and food insecurity.
At the book's 4.56-inch content width, their minimum print labels are now
9.50 to 10.89 points, compared with approximately 3.78 to 4.52 points before.
Both screen and print versions were measured and visually reviewed. The
mesh diagram explicitly uses a matched charger and protected battery pack.
See [figure review](FIGURE-REVIEW.md) for the measurements and controls.

Eleven other diagrams received corrections alongside their prose. Four
unresolved interior image uses were replaced with existing original line
illustrations in canonical source, so PDF and EPUB share the replacements.
The previous image files remain in the repository. All 79 manuscript figures
are linked to catalog entries, and catalog alt text and captions now match
the canonical text. The co-op cast now uses the four unchanged portrait sprites in an editable
SVG plate. Its role labels are at least 9.23 points at print width, including
Denny's corrected logistics role. The prior PNG is preserved. Part III's
spacing now keeps its introduction on one divider page. Only the three
part-divider banners receive the established print motifs.

The reading PDF uses the author-selected original cover. The print interior
is 6 by 9 inches, grayscale, with embedded fonts and an optional empty final
verso. EPUB and compiled Markdown come from the same frozen source. The
portable editable package includes the source snapshot, HTML, CSS, artwork,
fonts and licenses, audits, and PDFs. Historical packages are preserved;
the new package uses a versioned directory and ZIP.

## Reproduction and evidence

[Production instructions](../../publication/README.md) contain the build
commands. `baseline.json` records v0.9.2 before editing; `final-source.json`
records the reviewed v0.10.0 source. The production baseline includes all
35 sections and `book.json`, and refuses drift before a build. Editable
figure generators and proof scripts are retained here rather than in a
temporary directory.

Grayscale preparation removes only unused page-level image/form resource
references, leaving the color master and nested resources unchanged. The
final preparation removed 214,230 redundant references, preserved all 371
page streams and annotation descriptors, and reduced Ghostscript conversion
to 36.58 seconds. See [production review](PRINT-PRODUCTION.md).

Known-defect checks include intentional faults: unfinished copy, missing
images and links, text omission and corruption, caption collisions, undersized
labels, missing font programs, wrong page geometry, unexpected extra pages,
and color remaining in a grayscale interior. Their scope and limitations
are recorded with their results. A green structural check is not presented
as evidence of factual accuracy, visual quality, or physical print quality.

Final delivery paths, file sizes and SHA-256 hashes are in
[deliverables.json](deliverables.json). The PDF visual review and resource
reports identify the exact files checked.

## External-release decisions still open

The retained original cover has unresolved provenance in the historical
image audit and is about 228 pixels per inch at 6 by 9. The local package
records its exact checksum and a narrow local-review exception, not a license.
The current [quotation inventory](../publication/QUOTATIONS-v0.10.0.md)
covers 23 opening epigraphs; modern quotation permissions and applicable-use
decisions are not silently treated as cleared. Attribution is not permission.

A printer-specific cover wrap, binding and paper choice, and physical proof
remain outside this local digital finalization. No ISBN, publisher, rights
grant, PDF/X certification, EPUBCheck certification, or physical-device
acceptance has been invented.


## Final digital verification

- PDF: 35 sections and 2497 source text blocks preserved across 371 interior pages; no missing text, overflow, broken internal links, or missing images. The manifest and all section hashes match the frozen source.
- EPUB: 2546 source text blocks present across 38 spine documents; metadata, ZIP integrity, local resources and anchors pass. See [EPUB checks](epub-checks.json).
- PDF resources: all fonts embedded, navigation targets preserved, and all 371 content pages have identical normalized text in color and grayscale. One genuinely empty final print page is accounted for. See [resource checks](../publication/PDF-RESOURCE-CHECKS.md).
- Five redrawn diagrams and the new cast plate appear at the intended 4.56-inch width. Part III's old two-page layout was reproduced as a failing control; the corrected divider fits one page.
- Package validation: portable assets, font notices, source snapshots, current PDF hashes, and the exact local-review cover exception pass before export.

The first visual pass and its two corrections are preserved in `pdf-proof/`.
The final visual report distinguishes the original 35-page sample from the
corrected edition's targeted recheck and grayscale samples. This is sampled
visual inspection, not a claim that every page was individually inspected.


[Final visual sign-off](pdf-proof/FINAL-PDF-REVIEW.md) inspected 18 pages of the
corrected edition. The cast roles and label sizes, one-page Part III divider,
updated contents, selected grayscale diagrams, and empty final verso passed.
The earlier 35-page sample and its resolved findings remain separately dated.
