# v0.10.3 EPUB review

Final EPUB structural proof, browser layout proof and targeted visual review passed. No EPUB correction was needed. The four new diagrams and four new narrative plates were manually inspected at both 390 and 768 px, including their complete captions.

Reviewed artifact: `book-build/Surviving-the-Singularity-v0.10.3.epub`, 41,851,429 bytes. SHA-256: `35518ada9f32a2655e690f02e936b4b053b789f208bdada7a5fef9ae7a557521`. The archive hash was checked again after capture and review. All 36 frozen source hashes, including book metadata, and the artwork registry hash still match the structural proof. Frozen source receipt: [final-source.json](final-source.json).

`python3 docs/v0.10.3/check_epub.py` and `python3 docs/v0.10.3/prove_epub_layout.py` both exited successfully against this archive. The layout script was adapted to capture every newly registered asset at both widths; it serves the actual packaged XHTML, CSS and images, without substituting source artwork.

| Check | Final result |
| --- | --- |
| Canonical sections and section navigation | 35 checked |
| Spine documents | 38 |
| Source blocks checked against fresh Pandoc reference | 2,656; none missing |
| Canonical image references and distinct assets | 110 displayed and embedded |
| Registered figures | 62, all with required source captions |
| XML documents | 100 checked |
| ZIP structure, metadata, links and local resources | Passed |
| Browser figure measurements | 124: all 62 at each width |
| Layout defects and missing browser resource requests | 0 |
| Retained cutout alpha channels | All 6 preserve transparency and visible pixels |
| Captures saved | 32: 16 new-art captures plus 16 retained representatives at 768 px |
| Targeted manual coverage | All 8 new artworks, 16 captures |

Structural checks detected six deliberately introduced defects: deleted embedded image; deleted displayed image with bytes retained; deleted required caption; deleted real paragraph; missing CSS resource; and broken internal anchor. Browser layout checks also rejected an actual EPUB figure changed to 150vw width and a left float. These mutations were confined to verification inputs or the browser DOM.

Chrome 150.0.7871.125 rendered the archive with page JavaScript disabled. At a 390 px viewport, the new figures occupy 374 px; at 768 px they occupy 752 px. Images load, remain within the viewport and stack above their captions without overlap.

| New artwork, reviewed at 390 and 768 px | Observed result |
| --- | --- |
| `v103-reading-routes.svg` | Three routes, section labels, nodes and arrow fit. Caption is complete. |
| `v103-service-ledger.svg` | Both ledger columns and all four cost labels fit. Checkmarks, footer and caption remain separate. |
| `v103-offline-check.svg` | Four numbered steps and detail lines fit beside the phone. Footer and caption are complete. |
| `v103-first-year-index.svg` | All twelve actions fit. The final action uses an intentional second line without colliding with the border or footer. |
| `v103-narrative-bear-flag.png` | Three toasting men, Elijah's subdued posture and laptop remain visible. |
| `v103-narrative-near-end.png` | Coffee cup, closed laptop, window and horizon remain visible. |
| `v103-narrative-passing-beans.png` | Bowl exchange, adult diners and dog beneath the table remain visible. |
| `v103-narrative-rosa-testimony.png` | Rosa, microphone, wrist brace and meeting setting remain visible. |

No clipping, responsive cropping, stretching, missing caption text or caption collision was observed in these captures. Narrative captions occupy two lines at 390 px and one line at 768 px. All 16 captures were inspected by `/root/v102_middle`; `/root/v102_middle/v103_epub_checks` independently inspected the eight narrative captures and checked their packaged alternatives and captions against integration metadata. Caption text matches; the passing-beans alternative differs only by Pandoc's typographic apostrophe.

Machine receipts: [structural checks](epub-checks.json), [layout checks](epub-proof/checks.json), and [visual review with SHA-256 hashes for all 16 inspected captures](epub-proof/visual-review-receipt.json). Execution logs: [structural](epub-check.log) and [layout](epub-layout.log).

Limits: this is Chrome reflow of packaged EPUB content, not EPUBCheck certification, dedicated e-reader pagination or physical-device acceptance. Figure captures establish artwork and caption layout, not the full placement of surrounding paragraphs or screen-reader usability. At 390 px, fine facial, hand and wrist-brace details are naturally smaller; the main actions remain clear. All registered figures were measured, but this manual review covers the eight additions, not every retained artwork.
