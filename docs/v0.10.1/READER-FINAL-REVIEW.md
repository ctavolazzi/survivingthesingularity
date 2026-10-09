# Final reader verification, v0.10.1

Reviewed September 28, 2026 against the existing local server at
`http://localhost:5189`, using installed Chrome on macOS. The three interactive
scenes and the six final cutouts pass the bounded reader checks below. No reader
implementation change was needed during this review.

| Check rerun | Result | Evidence |
| --- | --- | --- |
| `node docs/v0.10.1/scenes/check-scenes.mjs` | All three substantial models, source preservation, current input/output hashes, six vector exports, minimum label size and annotation bounds pass. | [Scene checks](scenes/scene-checks.json) |
| `node scripts/render-book-scenes.mjs --check` | All three dark stills and three light stills reproduce byte for byte. | [Render manifest](scenes/render-manifest.json) |
| `node docs/v0.10.1/scenes/browser-proof.mjs` | All three real chapter scenes render with WebGL2; the continuous reader mounts its food-route scene once. Keyboard opening, changed camera pixels, selected descriptions, closing/disposal, lazy loading and no continuing render loop pass. | [Browser results](scenes/browser-proof.json) |
| `node docs/v0.10.1/scenes/navigation-proof.mjs` | Chapter 9 to Chapter 15 client navigation disposes the previous context, starts with the correct still, and opens the new model. | [Navigation results](scenes/navigation-proof.json) |
| `node docs/v0.10.1/scenes/static-fallback-proof.mjs` | All three server-rendered images and native details work with JavaScript disabled; each table exposes four explanatory rows. | [Static fallback results](scenes/static-fallback-proof.json) |
| `python3 docs/v0.10.1/prove_cutout_chapters.py` | All 24 cases pass: six cutouts in both `/book` and `/read`, at widths of 1280 and 390 pixels. Intrinsic sizes, captions, alternative text, float/stack behavior, transparent styling, content bounds and adjacent prose all pass. | [Cutout route results](visual-proof/cutout-chapters/checks.json) |

The scene run reports zero page errors. At a 390-pixel viewport, its tested
310-pixel-wide figure has no internal overflow, no animations, and all nine
buttons have a height of 46.09 pixels. The cutout run separately reports zero
page errors, root overflow and figure/prose intersections across all 24 cases.

Deliberate failures were exercised in these reruns: stale-artifact hashes were
rejected; unknown enhancement markers and mismatched still filenames preserved
their original Markdown; unavailable WebGL and an actively lost context restored
the illustration; and moving a real cutout into the gutter made the bounds check
fail before the temporary DOM mutation was restored. The navigation proof's
original failing case and keyed-component correction remain documented in
[scene review](scenes/SCENE-REVIEW.md).

The first browser-proof invocation reached its 30-second timeout while loading
the initial Chapter 9 page. A serial rerun, without implementation changes,
completed every assertion. Other actual-route checks also completed. This is
recorded as an initial navigation timeout, not counted as a scene assertion
failure or silently treated as a successful first run.

Visual inspection covered all three live chapter scenes; the food route's
selected connection and rotated overhead camera; the small-screen reduced-motion
scene; denied-WebGL and JavaScript-disabled fallback; desktop Atlas and tools
cutouts; and mobile rocket and printer cutouts. The models, annotations, controls,
captions and prose stayed within their intended areas. The mobile scene's SVG
labels are necessarily compact; full-size descriptions and native expandable
text remain available below the illustration. Desktop cutouts allow prose to
wrap, and narrow screens stack them with their captions.

Representative retained screenshots:

- [Food route in 3D](scenes/food-delivery-reader-3d.png), [growing bed in 3D](scenes/living-soil-reader-3d.png), [workshop in 3D](scenes/shared-workshop-reader-3d.png).
- [Selected connection and overhead view](scenes/food-delivery-reader-selected.png), [mobile reduced-motion scene](scenes/mobile-reduced-motion-3d.png).
- [Unavailable-WebGL fallback](scenes/webgl-unavailable-fallback.png), [workshop without JavaScript](scenes/shared-workshop-no-javascript.png).
- [Desktop Atlas](visual-proof/cutout-chapters/book-atlas-1280.png), [mobile rocket](visual-proof/cutout-chapters/book-rocket-390.png), [mobile continuous-reader printer](visual-proof/cutout-chapters/read-printer-390.png), [desktop continuous-reader tools](visual-proof/cutout-chapters/read-tools-1280.png).

This review covers the local web reader in Chrome. It does not establish Safari,
Firefox, physical-device or screen-reader acceptance. The full reader's existing
draft-password gate requires JavaScript; the disabled-JavaScript result covers
the new standalone components. It does not reopen source-image fidelity or
license conclusions, certify every existing illustration, or sign off PDF/EPUB
pagination and packaging. Those have separate edition evidence.
