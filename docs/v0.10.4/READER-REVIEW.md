# v0.10.4 local reader review

The local reader passed the browser checks at http://127.0.0.1:5192. The six middle revisions in Chapters 6, 7, 9, 10, 12, and 14 match the revised canonical text on their individual chapter routes at both 390px and 1280px. Each complete paragraph fits inside the checked viewport without horizontal overflow. All artwork is retained from v0.10.3.

## Checks and evidence

- All 62 registered figures were checked in the continuous reader at both widths: 124 figure checks. Captions, caption links, alt text, loaded dimensions, aspect ratio, and horizontal bounds passed.
- The eight retained v0.10.3 illustrations were checked again on individual chapter routes at both widths: 16 checks.
- Three retained scene illustrations remained in still mode under reduced motion at both widths. Their text details opened; all 24 detail-row checks matched the scene catalog and fit the reading viewport.
- All six middle revisions were compared with their canonical Markdown after rendering: 12 paragraph checks. Screenshots cover every checked paragraph at both widths.
- Representative screenshots inspected directly: [mobile Chapter 10](reader-proof/prose-390-chapter10.png) and [desktop Chapter 9](reader-proof/prose-1280-chapter9.png). The revised list item and shorter closing paragraph read clearly with the surrounding material.
- Four existing negative controls deliberately introduced horizontal overflow, aspect distortion, a missing caption, and missing alt text. Each failed for the intended reason and passed after restoration. A fifth control replaced a revised paragraph with missing-text content, observed rejection, restored it, and passed.
- Browser checks recorded no page errors, console errors, failed requests, HTTP errors, or unexpected browser warnings. Existing development compiler warnings remain in the server log.

## Source integrity

All 37 canonical source files checked before and after browser work are unchanged. This set includes every manifest section, `book.json`, and `visuals.json`.

Source-set SHA256 before and after: `3f29739bb5c63c6c2db999d8105fe5bf0e28f8858afddf842208571f24ddbe0b`.

The derived `manuscript-index.json` changed during parallel release work. Root confirmed this was concurrent index reconciliation by another agent. Its observed hashes are recorded separately in the JSON receipt. This review makes no claim that the derived index stayed unchanged. Reader verification made no product edits.

Individual source hashes, proof-script hashes, screenshot hashes, exact scope, and results are in [review.json](reader-proof/review.json). Detailed receipts: [reader smoke](reader-proof/reader-smoke.json), [scene details](reader-proof/scene-details.json), and [revised prose](reader-proof/prose-review.json).

## Limits and server

This is a local Chromium reader check. The other twelve revised paragraphs are outside this focused prose receipt. The registered-figure checks do not cover every image file in the repository. Interactive 3D WebGL, deployed production, physical print, and e-reader behavior were not exercised.

The detached development server remains available on port 5192, PID 14126. Its log is [server.log](reader-proof/server.log). No product source was edited during verification.
