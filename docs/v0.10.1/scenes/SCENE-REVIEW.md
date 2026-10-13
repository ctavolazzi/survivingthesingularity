# Three-dimensional book scenes, v0.10.1

Three new scenes extend the existing examples in Chapters 9, 15, and 17. They use original Three.js geometry, not imported models or textures. `placements.json` records the exact source anchors, alternative text, captions, and inserted comment/image pairs. No existing prose was replaced.

| Scene | What the spatial view explains | Canonical source |
| --- | --- | --- |
| One harvest, five doors | Garden, food partner, packing, transport, and five distinct recipient doors remain connected. The existing illustrative arithmetic is eight usable kilograms plus two from the partner. | `11-chapter9.md` |
| A growing bed has an outside | A soil cutaway distinguishes activity within the bed from sunlight, water, replenishment, harvest, and losses crossing its boundary. | `17-chapter15.md` |
| What keeps a workshop useful | Shared machines depend on people, materials, maintenance, spares, and a useful result leaving the bench. | `19-chapter17.md` |

The geometry includes greenhouse ribs and individual crops; house roofs, doors, crates, a packing counter and cargo cart; roots, soil activity, a compost bin, water barrel and harvest crate; a printer gantry, tools, repair bench, stock rack, walk-behind tractor, and people. Proportions and arrows are illustrative. These are not yield models, engineering plans, or new claims of self-sufficiency.

## Rendering and preservation

`src/lib/bookScenes/geometry.js` is the shared model and orthographic camera. The interactive reader uses WebGL2. The deterministic exporter uses the pinned Three.js 0.168.0 [SVGRenderer source](https://raw.githubusercontent.com/mrdoob/three.js/r168/examples/jsm/renderers/SVGRenderer.js), which renders the same meshes and lines to vector paths. Annotations remain real SVG text. Neither export uses a clock, random numbers, remote fonts, models, textures, or GPU screenshots.

`node scripts/render-book-scenes.mjs --proof` writes three dark originals, three independently rendered light print variants, six inspection PNGs, and `render-manifest.json`. The manifest identifies input and output SHA-256 hashes. `--check` reproduces both palettes and rejects a byte mismatch. The print copies are prepared variants, not generic palette remaps.

Every annotation is at least 24 SVG units in a 960-unit figure, equivalent to 8.2 points at the publication's 4.56-inch text width. Numeric pin labels and descriptive legend text preserve meaning in grayscale. Ordinary Markdown images and captions remain the EPUB/PDF source. HTML comment markers are invisible to ordinary exporters; unknown or malformed enhancement markers preserve their adjacent source content.

Both `/book/[sectionId]` and `/read` use the same source splitter and registry. Three and its runtime load only after the reader chooses **Explore in 3D**. Camera and connection controls are ordinary keyboard-accessible buttons; equivalent explanations and a native expandable table are also available. There is no autoplay, transition animation, animation loop, pointer lock, drag requirement, or keyboard capture. Rendering responds to an action, visibility change, or resize. Closing, navigation, and component disposal release geometry, materials, observers, canvas, and WebGL context. A failed or lost WebGL context restores the illustration.

## Verification

- `node docs/v0.10.1/scenes/check-scenes.mjs`: source preservation, deliberate stale-artifact rejection, substantive geometry, current file hashes, vector-only exports, minimum label size, and text bounds. Results: `scene-checks.json`.
- `node scripts/render-book-scenes.mjs --check`: byte-identical regeneration of all six SVGs.
- `node docs/v0.10.1/scenes/browser-proof.mjs`: actual chapter routes and continuous reader, WebGL2 drawing, keyboard opening, camera changes verified in rendered pixels, connection descriptions, lazy loading, no continuing render loop, canvas disposal, deliberate WebGL denial and active context loss, keyboard exit from controls, mobile width, reduced motion, and annotation bounds. Results and screenshots are retained here.
- `node docs/v0.10.1/scenes/navigation-proof.mjs`: client-side chapter navigation releases the old WebGL context, starts the new chapter on its still, and opens the correct new model. This check first failed on the unkeyed component reuse and passed after the reader keyed figures by scene ID.
- `node docs/v0.10.1/scenes/static-fallback-proof.mjs`: actual server rendering of the new components, then a browser with JavaScript disabled. All three illustrations load, captions remain, and native details reveal all four explanatory rows. The standalone proof is `static-fallback.html`.
- `npx vite build`: complete production compilation, with output retained in `vite-build.log`. This isolates compilation from release preflight, which depends on the edition's final downloads and remains part of root's release checks.

The first visual inspection found SVG painter ordering that let a large floor triangle obscure objects. Explicit floor order and subdivision fixed it. The live-browser inspection found the bottom note clipped by a fixed-ratio HTML layout. The final live view uses the same vector annotation positions as the still, and the new text-bounds check covers that surface. A final client-side navigation probe caught Svelte reusing an active model under a new chapter caption; keyed scene components now destroy the previous model on chapter changes.

Inspection includes the six palette stills, all three live chapter figures and their selected states, the continuous reader, small-screen reduced-motion view, denied-WebGL fallback, and all three JavaScript-disabled figures. Local browser proof uses installed Chrome on macOS. It does not claim Safari or Firefox coverage. The pre-existing password gate on the full reader requires JavaScript; the no-JavaScript check verifies the new figures and their standalone fallback without changing that gate.
