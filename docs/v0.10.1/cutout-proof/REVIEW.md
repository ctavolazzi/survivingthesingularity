# v0.10.1 cutout proof

Reviewed 2026-09-28. All six generated cutouts have working alpha transparency and render cleanly over white and navy surfaces. No rectangular background, checkerboard, hard subject cutoff, or broad white/black fringe was visible in the browser proofs. These are generated editorial adaptations of source photographs, not exact photographic extractions. Their captions and rights records should preserve that distinction.

The proof uses the actual PNGs through ordinary browser image elements. [White contact sheet](contact-white.png) and [dark contact sheet](contact-dark.png) show the same six files on `#ffffff` and `#020617`. Each `compare-*.png` places the repository source image beside its generated adaptation on both surfaces. All six original source images, all six comparison sheets, and both complete contact sheets were visually inspected.

| Cutout | Fully transparent pixels | Narrowest margin at alpha 16 or higher | Visual result and source comparison |
| --- | ---: | ---: | --- |
| Atlas | 69.06% | 14 px | Complete beacon, hands, feet, and open limb/frame spaces. Metallic edges remain readable on both surfaces. Nameplate lettering and small mechanical details differ from the source; this is a reworked depiction. [Comparison](compare-atlas.png) |
| Printer | 42.90% | 2 px | Open frame and cable loops show the actual page background. No room or tabletop rectangle remains. Left and right margins are only 2 and 5 px, so avoid additional cropping or clipping. Machine/vase detail and perspective have been redrawn. [Comparison](compare-printer.png) |
| Sun | 35.01% | 46 px | Full disk and soft colored limb sit cleanly on both surfaces. The generated rim has more pronounced spiky wisps, and surface detail differs from the source. Do not present it as an unaltered NASA observation or a scientific record of particular flares. [Comparison](compare-sun.png) |
| Tools | 70.85% | 13 px | Tips and handles are intact with clean open spaces. Selected tools have been rearranged; wrench proportions and fine surface markings differ. It is a collage, not a record of the original workbench arrangement. [Comparison](compare-tools.png) |
| Spot | 74.08% | 19 px | All four feet and gaps between legs remain visible. Black legs have lower contrast on navy, while the yellow body stays distinct; white gives the clearest mechanical silhouette. Small geometry/texture details are regenerated. The forest and ground are fully absent. [Comparison](compare-spot.png) |
| Rocket | 76.80% | 14 px | Complete rocket tip, connected exhaust column, and soft smoke base. The white exhaust naturally loses contrast on white, while orange edges and smoke preserve the shape. Smoke is substantially recomposed, as requested; it is a launch collage rather than an intact photograph of the event. [Comparison](compare-rocket.png) |

Suggested caption wording, to accompany source credit and the edition's image-generation disclosure:

- **Atlas:** “Atlas, in an editorial illustration adapted from a photograph.”
- **Printer:** “A desktop 3D printer, reworked from a photograph as an editorial cutout.”
- **Sun:** “Solar illustration adapted from NASA SDO imagery. Surface and edge detail have been reworked.”
- **Tools:** “Hand tools, rearranged and reworked from a workbench photograph.”
- **Spot:** “Spot, in an editorial illustration adapted from a photograph.”
- **Rocket:** “A Falcon Heavy launch collage adapted from a photograph, with exhaust and smoke recomposed.”

[checks.json](checks.json) records natural dimensions, PNG color type, pixel alpha statistics, visible bounding boxes, margins, and SHA-256 hashes for all twelve input files. All PNGs are RGBA (PNG color type 6). Five cutouts have a maximum alpha of 254 rather than 255; much of each subject is effectively opaque at alpha 250 or higher. This does not create a visible rectangular haze in the browser. RGB color stored under alpha 0 is invisible when composited correctly, even if an image-inspection view exposes that hidden color.

[proof.py](proof.py) can reproduce these artifacts. It only reads the source images, reads browser canvas pixels for measurements, and writes browser screenshots plus a JSON report. No PNG was retouched, resized on disk, or rewritten. Input hashes were checked again after the proof. An entirely opaque synthetic control was rejected by the transparency check, and a border-touching synthetic control was detected by the margin check. Both controls exist only in browser memory.

The numerical bounds show that pixels at roughly 6% opacity or higher do not touch any file edge. They cannot establish the authenticity of reconstructed machine parts, scientific texture, or smoke. The visual review found no alpha-related blocker for editorial use with adaptation captions. Final placement, small-screen leg contrast, grayscale printing, and source-license treatment remain part of the publication proof; this report makes no claim of external rights clearance. Manuscript, image files, rights records, and catalogs were not modified by this task.
