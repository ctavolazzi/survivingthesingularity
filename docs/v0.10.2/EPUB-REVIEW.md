# EPUB review, v0.10.2

**The scoped structural and browser checks pass. No new blocking defect was found.** Reviewed the actual 30,220,678-byte EPUB, not loose source HTML or replacement images. All evidence below identifies this archive:

`002ca8563a15536f919786b83bfbed34d3b233200d9574df2a20e3eb7a6efd46`

## Confirmed coverage

| Check | Result |
|---|---:|
| Canonical sections and TOC entries | 35 |
| Spine documents, including cover, title and navigation | 38 |
| Freshly rendered canonical text blocks checked | 2,648 |
| Canonical artwork placements | **102** |
| Registered figure placements | **54** |
| Registered figure measurements at 390 / 768 px | 54 / 54 |
| Parseable XML-family documents | 96 |
| Missing text blocks, artwork or package resources | 0 |
| Browser layout errors or missing resource requests | 0 |

The 102 canonical image placements also correspond to 102 distinct source filenames. Registered figures are a subset of those placements; the 54 count is not an additional set of images. Every expected illustration was compared by its embedded-byte hash with the frozen build's chosen source or prepared print variant. Nonempty image alternatives were checked, and all registered figures have the expected figure wrapper and caption.

`python3 docs/v0.10.2/check_epub.py` verified the source freeze, archive CRCs, unique ZIP entries, first uncompressed EPUB mimetype, package metadata, manifest resources, internal navigation targets, section order and text coverage. It freshly rendered canonical sections with resolved references for comparison. Five deliberate mutations were detected: a deleted image resource, a removed displayed image with its bytes retained, a removed real paragraph, a missing CSS resource, and a broken internal anchor. [Structural report](epub-checks.json).

`python3 docs/v0.10.2/prove_epub_layout.py` rendered packaged XHTML, CSS and images in Chrome 150.0.7871.125 with page JavaScript disabled. All 54 registered figures loaded at each width, stayed inside horizontal viewport bounds and stacked their captions below their images. An intentional 150vw figure width with a left float was detected. All six cutouts retained both fully transparent and near-opaque pixels. [Layout report](epub-proof/checks.json).

## Visual inspection

The main layout proof captured sixteen representative 768 px figures. A supplemental read-only [capture script](inspect_epub_samples.py) produced twenty samples of ten figures at **both 390 and 768 px**, using only exact archive resources. All twenty supplemental screenshots were inspected directly. Their archive, image-resource and screenshot hashes are recorded in [samples.json](epub-proof/manual-samples/samples.json); the inspection record is [reviewed.json](epub-proof/manual-samples/reviewed.json).

| Figure | Packaged views | Inspection |
|---|---|---|
| `intro-nine-stages.svg` | [390](epub-proof/manual-samples/intro-nine-stages-390.png) / [768](epub-proof/manual-samples/intro-nine-stages-768.png) | All nine stage names and speculation boundary remain visible. |
| `ch05-horses-tractors.svg` | [390](epub-proof/manual-samples/ch05-horses-tractors-390.png) / [768](epub-proof/manual-samples/ch05-horses-tractors-768.png) | Both charts, units, separate scales and source note remain visible. |
| `ch09-greenhouse-bus.svg` | [390](epub-proof/manual-samples/ch09-greenhouse-bus-390.png) / [768](epub-proof/manual-samples/ch09-greenhouse-bus-768.png) | Sensor labels, grower limits, off state and manual shutoff remain visible. |
| `ch11-cooling-loop.svg` | [390](epub-proof/manual-samples/ch11-cooling-loop-390.png) / [768](epub-proof/manual-samples/ch11-cooling-loop-768.png) | Hot/cool paths, mass-flow equation and units remain visible. |
| `ch12-csa-network.svg` | [390](epub-proof/manual-samples/ch12-csa-network-390.png) / [768](epub-proof/manual-samples/ch12-csa-network-768.png) | Resource inputs, human coordination and delivery boundary remain visible. |
| `ch17-algae-loop.svg` | [390](epub-proof/manual-samples/ch17-algae-loop-390.png) / [768](epub-proof/manual-samples/ch17-algae-loop-768.png) | Water loop and feed branch remain separate; inputs and feed caveat remain visible. |
| `ch19-conversion-ladder.svg` | [390](epub-proof/manual-samples/ch19-conversion-ladder-390.png) / [768](epub-proof/manual-samples/ch19-conversion-ladder-768.png) | Rung order and solid/dashed distinction remain visible. |
| `appd-precedent-timeline.svg` | [390](epub-proof/manual-samples/appd-precedent-timeline-390.png) / [768](epub-proof/manual-samples/appd-precedent-timeline-768.png) | All twenty-four entries remain visible; approximate spans now have visible gaps. |
| `v101-scene-living-soil.svg` | [390](epub-proof/manual-samples/v101-scene-living-soil-390.png) / [768](epub-proof/manual-samples/v101-scene-living-soil-768.png) | Scene, four numbered callouts and explanatory legend remain visible. |
| `v101-cutout-atlas.png` | [390](epub-proof/manual-samples/v101-cutout-atlas-390.png) / [768](epub-proof/manual-samples/v101-cutout-atlas-768.png) | Transparent cutout stacks above its caption and attribution link. |

No sampled figure had clipped labels, missing content, caption collisions or an unwanted box around the cutout. Diagram meanings that distinguish solid/dashed lines or numbered callouts remain visible. The rebuilt timeline's approximate spans visibly retain dash gaps.

## Limits and release notes

This is **not EPUBCheck certification or a dedicated e-reader/device test**. Chrome's scrolling layout does not certify Apple Books, Kobo, Kindle conversion, screen-reader behavior, physical-device contrast, font substitution, or paginated fit. External website destinations were not tested for availability.

At 390 px, the sampled 480-unit SVGs occupy 374 CSS pixels; their smallest 14-unit labels therefore scale to approximately **10.91 CSS pixels**. The living-soil scene's smallest note scales to **9.35 CSS pixels**. These details are small, so some readers will need zoom. SVG labels do not reflow like surrounding HTML text. At 768 px, several tall diagrams occupy about 1,019 CSS pixels before captions and extend below the 1,000-pixel browser viewport; full figure screenshots confirm complete scrolling content, not a guarantee of one-screen or one-page fit.

The text check compares normalized block presence, not exact bytes, every styling decision, or within-section paragraph order. Very short blocks below the checker's threshold and generated image captions are excluded from that text comparison. Figure captions and alternatives are checked structurally and sampled visually, not semantically certified by the automated proof.

The frozen canonical source hashes were rechecked after inspection and still match. No manuscript, artwork, registry, EPUB archive or v0.10.1 evidence was changed by this review.
