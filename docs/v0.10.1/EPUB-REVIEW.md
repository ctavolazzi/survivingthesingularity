# EPUB review: v0.10.1

Reviewed September 28, 2026 by Codex. The existing EPUB passed the structural,
source-preservation, artwork, and bounded browser checks described here. This
review did not rebuild or alter the EPUB, canonical manuscript, or publication
package.

Artifact: `book-build/Surviving-the-Singularity-v0.10.1.epub`, 30,215,141 bytes.
SHA-256: `f6a054c3bdd536aace8fb548bdf0ccb55dd94634f1c5607580564f6ec1bfd15d`.

## Content and resources

[check_epub.py](check_epub.py) verifies the current source hashes against the
frozen publication baseline and renders canonical sections afresh with Pandoc.
The check no longer relies on a potentially stale `source-rendered.html` or
accepts an image merely because its bytes occur somewhere inside the archive.
[Machine evidence](epub-checks.json) and [execution log](epub-check.log) record:

| Check | Result |
| --- | --- |
| Manifest source sections | 35, matching frozen hashes |
| EPUB spine documents | 38: cover, title page, navigation, and 35 source sections |
| Canonical text blocks | 2,573 checked in their corresponding chapters; none missing |
| Source images | All 102 displayed in the correct chapters with matching asset hashes and nonempty alternative text |
| New registered figures | All 23 retain figure structure and captions |
| Navigation | 35 section links, correct spine order, working internal targets |
| XML documents | 96 strictly parsed |
| ZIP/resources | Valid CRCs, correct first uncompressed mimetype member, no missing local resources |
| Static presentation | No packaged JavaScript or leaked scene markers; stacking stylesheet present |

The 23 additions comprise six photo-derived cutouts, eight charts/worksheets,
six conceptual illustrations, and three static scene exports. SVGs match their
prepared light variants; raster additions match their original registered
RGBA PNGs. The art records include each canonical filename, embedded ZIP path,
chapter, and SHA-256 value.

Five intentionally broken in-memory copies failed their corresponding checks:
removing an embedded image, removing its displayed image while retaining the
bytes, removing a real paragraph, referencing a missing CSS resource, and
linking to a missing internal anchor. The previous invented-paragraph absence
check was replaced with an actual deletion from chapter content.

## Packaged visual evidence

[prove_epub_layout.py](prove_epub_layout.py) serves the actual ZIP members to
Chrome 150.0.7871.125 with page JavaScript disabled. It does not substitute
source files. [Browser measurements](epub-proof/checks.json) cover all 23 new
figures at both 390 and 768 CSS pixels: 46 figure measurements, no missing
requests, no unloaded images, no figure/image/caption overflow, no image-caption
intersection, and no floating figures. An injected 150vw figure with a left
float failed the same layout instrument.

Nine saved 768-pixel samples were visually inspected:

- [Atlas](epub-proof/v101-cutout-atlas-768.png), [printer](epub-proof/v101-cutout-printer-768.png), and [Spot](epub-proof/v101-cutout-spot-768.png) retain transparent surroundings and readable attribution captions.
- [Electricity demand](epub-proof/v101-chart-data-centre-demand-768.png), [wasted-food pathways](epub-proof/v101-chart-waste-pathways-768.png), and [weights memory](epub-proof/v101-chart-weights-memory-768.png) retain labels, values, units, explanatory scope, and source captions without clipping.
- [Food delivery](epub-proof/v101-scene-food-delivery-768.png), [living soil](epub-proof/v101-scene-living-soil-768.png), and [shared workshop](epub-proof/v101-scene-shared-workshop-768.png) render complete static illustrations, numbered keys, and captions without JavaScript.

All six embedded cutouts have real alpha transparency, with 35.0% to 76.8%
fully transparent pixels. Five peak at alpha 254; tools peaks at 255. The
instrument records near-opaque pixels rather than incorrectly requiring every
cutout to contain alpha 255. This matches the earlier cutout audit.

An initial browser-control attempt stalled because `add_style_tag` waited for
a page event while page JavaScript was disabled. That run was interrupted,
its owned browser closed, and the control changed to synchronous DevTools
style mutation. The final bounded run completed successfully and closed its
browser. No EPUB change was needed.

## Scope

No EPUB blocker was found in these checks. This is not EPUBCheck certification,
a dedicated e-reader pagination test, or physical-device acceptance. No
EPUBCheck executable was available. Browser geometry does not establish SVG
label readability on every reader setting, and text presence does not certify
factual accuracy or reading order inside every table. The existing artwork
provenance, original-cover, and quotation-use limitations remain as documented
in the publication audit.
