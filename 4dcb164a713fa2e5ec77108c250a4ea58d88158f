# v0.10.4 EPUB review

The EPUB structural proof, browser reflow proof and targeted visual review passed. No publication correction was needed. All six revised ending passages were visually inspected at 390 and 768 pixels. The retained reading-route and first-year diagrams were also inspected at 768 pixels, with complete captions.

Reviewed archive: `book-build/Surviving-the-Singularity-v0.10.4.epub`, 41,851,412 bytes. SHA-256: `780a29d0ab73b5cefcc7eae2faa4a9a34a9ed9a902f67efcf252bd9742fae97c`. The archive and all 36 frozen canonical-source hashes were checked again after capture and visual review.

| Check | Result |
| --- | --- |
| Canonical sections and navigation | 35 checked |
| Spine documents | 38 |
| Freshly rendered source blocks | 2,658; none missing |
| Canonical artwork references | 110 displayed and embedded |
| Registered figures | 62; all required captions present |
| XML documents | 100 checked |
| Browser figure measurements | 124: all 62 at 390 and 768 pixels |
| Figure layout errors and missing resources | 0 |
| Revised ending text | All six passages match at both widths |
| Manual review | 12 changed-text captures and two retained-diagram captures |

The structural checks detected six deliberately introduced defects: deleted embedded image, deleted displayed image with bytes retained, deleted required caption, deleted real paragraph, missing CSS resource, and broken internal anchor. The layout check rejected an actual figure changed to 150vw width and a left float. The ending-text matcher also rejected an actual displayed passage replaced in the browser, then accepted its restored text. All mutations were confined to verification inputs or the browser DOM.

Chrome 150.0.7871.125 rendered the actual packaged XHTML, CSS and images with page JavaScript disabled. Text remained complete and readable at both widths, including the bold action labels, revised tier heading and italic year-plan introduction. No clipping or overlapping lines was observed in the 14 manually inspected captures. All six retained cutout assets still contain transparent and visible pixels.

The layout run saved 18 representative figure captures. Manual artwork review was limited to the two instructional diagrams because this edition changes prose and retains the previous artwork. All 62 registered figures still underwent automated geometry checks at both widths. The six ending passages have 12 additional captures.

The live reader was checked separately at 390 and 1280 pixels: all six changed passages in both individual chapters and continuous reading, for 24 placements. All six mobile chapter captures and all six desktop continuous-reader captures were manually inspected. The [reader proof](epub-proof/ending-reader.json) and [reader visual receipt](epub-proof/ending-reader-review.json) record that scope and its altered-text control.

Reproduce from the worktree root:

```sh
python3 docs/v0.10.4/check_epub.py
python3 docs/v0.10.4/prove_epub_layout.py
python3 docs/v0.10.4/epub-proof/ending-epub.py
```

Receipts: [structural proof](epub-checks.json), [figure reflow proof](epub-proof/checks.json), [ending-text proof](epub-proof/ending-epub.json), and [manual visual review](epub-proof/visual-review-receipt.json). Execution logs: [structural](epub-check.log), [reflow](epub-layout.log), and [ending text](epub-proof/ending-epub.log).

Limits: Chrome reflow establishes browser behavior of the packaged resources. It is not EPUBCheck certification, dedicated e-reader pagination or physical-device acceptance. Passage-element captures do not show outside list markers or complete surrounding pagination. The other retained artworks were measured, not all manually reinspected in this pass.
