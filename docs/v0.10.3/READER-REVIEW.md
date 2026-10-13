# v0.10.3 reader review

The local reader smoke proof passed at 390 × 844 and 1280 × 1000 pixels in Chromium with reduced motion enabled. All 62 registered figures were checked in `/read` at each size. All eight new figures were also checked in their individual section routes at both sizes.

The checks compare every figure's complete alt text, caption text, caption links and reserved dimensions with the canonical source and registry. They verify image decoding, natural aspect ratio, image and caption bounds, and absence of horizontal overflow. Four deliberate defects were rejected before the restored page passed: excess image width, distorted height, a hidden caption, and missing alt text.

The three retained scene illustrations remain stills until requested, with no canvas created by initial display. Their native text details open, and all four rows per scene were separately scrolled into the real viewport at both sizes. That is six scene views and 24 visible rows. This pass does not repeat the earlier WebGL interaction audit.

## New art routes

Every illustration below was checked in [continuous reading](http://127.0.0.1:5191/read) and its corresponding chapter route.

| Figure | Individual route |
| --- | --- |
| `v103-reading-routes.svg` | [`/book/how-to-use`](http://127.0.0.1:5191/book/how-to-use) |
| `v103-service-ledger.svg` | [`/book/appendix-c`](http://127.0.0.1:5191/book/appendix-c) |
| `v103-offline-check.svg` | [`/book/appendix-e`](http://127.0.0.1:5191/book/appendix-e) |
| `v103-first-year-index.svg` | [`/book/appendix-g`](http://127.0.0.1:5191/book/appendix-g) |
| `v103-narrative-bear-flag.png` | [`/book/chapter0`](http://127.0.0.1:5191/book/chapter0) |
| `v103-narrative-near-end.png` | [`/book/chapter4`](http://127.0.0.1:5191/book/chapter4) |
| `v103-narrative-passing-beans.png` | [`/book/chapter7`](http://127.0.0.1:5191/book/chapter7) |
| `v103-narrative-rosa-testimony.png` | [`/book/chapter19`](http://127.0.0.1:5191/book/chapter19) |

## Visual receipts

[reader-smoke.json](reader-proof/reader-smoke.json) contains 124 continuous placements, 16 individual placements, six scene still checks, four negative controls, and exact geometry. [scene-details.json](reader-proof/scene-details.json) records the additional 24 row visibility checks. [review.json](reader-proof/review.json) records source, script and capture hashes.

The reviewer inspected all eight new illustrations on mobile chapter pages and desktop continuous reading, plus all three scene text equivalents in the mobile viewport. Captions are complete, narrative images retain their composition, and practical figure labels remain inside their frames. The SVG labels scale down with the figure on small screens; this is not a guarantee that every label can be read without zoom.

There are 50 captures in `reader-proof/`. Use `chapter-390-*` for the mobile art, `continuous-1280-*` for desktop art, `scene-*-image.png` for retained scene stills, and `scene-*-details-viewport.png` for their real scrollable text. The six earlier `scene-*-still.png` element screenshots include open details and can have blank tails because the reader uses an inner scrolling container. They are retained as diagnostic artifacts, not treated as evidence of absent text.

No browser runtime errors, console errors, HTTP errors, or failed requests were observed. The 54 development console warnings were the existing Svelte `Layout`/`Page` unknown `params` messages. Vite also printed existing unused-CSS, accessibility and Browserslist notices to the server log. No reader application source was changed.

## Reproduce

From the worktree root, run `node docs/v0.10.3/reader-proof/server.mjs`, then `node docs/v0.10.3/reader-proof/reader-smoke.mjs` and `node docs/v0.10.3/reader-proof/scene-details.mjs`. The server uses port 5191 and allows the dependency symlink's real path. The local proof unlocks the draft gate through its existing store. It does not change access behavior or publish a site.

The smoke proof covers this local development server in Chromium. It does not certify every browser, production deployment, physical printing, EPUB layout, or a complete accessibility audit.
