# Original interior motifs and cover illustration

Source reviewed: v0.8.2 manifest, all 30 section files, existing illustrations, chapter arguments and recurring objects. This map proposes placements for the publication renderer; it does not edit the manuscript or replace inherited images.

## Design and production

Twelve original SVG line illustrations are in `publication/assets/motifs/`. Geometry was authored for this book, without tracing an existing image or borrowing an icon library. Transparent 400 × 260 viewBoxes contain no visible text, fonts, bitmap payloads, scripts or external dependencies. SVG titles and descriptions provide accessible metadata.

The palette is ink `#202c28` and muted olive `#66764e`. The corresponding files in `publication/assets/motifs/monochrome/` use only `#000000`; they are separate production assets, not grayscale previews. Main strokes are 4.2 SVG units, or 1.51 points when the drawing is placed 2 inches wide. Round joins keep the small shapes readable. These are conceptual illustrations, not engineering plans, agricultural instructions or claims about an existing machine's capability.

Use a 2-inch width and natural 1.3-inch height. Preserve the viewBox and internal white space. Do not crop the SVG to its visible paths or enlarge it to the full text width. Give the motif at least 12 points of surrounding space. Place it as a block on a chapter or part opening, or immediately before the specified subsection. Avoid wrapping body text around these small drawings. The visual language should be quiet enough to sit with the prose.

The preferred program uses all twelve designs at fourteen placements. Two purposeful returns connect the argument: the grain and gripper recur when assistance becomes a service; the table returns in the conclusion. Other chapters keep their existing image or their words as the primary visual event. If a chapter-opening photograph already occupies the proposed space, move the motif to the specified internal anchor or omit it. Do not stack a motif, a photograph, an epigraph and a summary on one opening merely to use every asset.

## Exact asset names

| File, relative to `publication/assets/motifs/` | Primary use | What the drawing contributes |
| --- | --- | --- |
| `01-grain-and-gripper.svg` | Introduction; return in Chapter 11 | A receptive machine beside living grain makes the food-first assignment visible. |
| `02-event-horizon.svg` | Part I divider | Open orbital curves frame an uncertain center. This is a speculative metaphor, not a black-hole diagram. |
| `03-centrifugal-governor.svg` | Chapter 5 | Weighted arms and a sliding collar connect mechanical power with regulation and feedback. |
| `04-seed-and-root.svg` | Part III divider | A seed crosses the ground line into growth and roots: useful work needs a place and continuing support. |
| `05-roof-and-joint.svg` | Chapter 13 | Open framing draws attention to the load-bearing work and joints beneath a finished roof. |
| `06-shared-table.svg` | Part II divider; return in Conclusion | Distinct bowls and open seats emphasize provision and a place among other people. |
| `07-pamphlet-and-thread.svg` | Chapter 16 | Folded sheets and exposed stitching make the shared record a made, revisable object. |
| `08-water-pump.svg` | Chapter 6 | A pump and a small ripple connect repair with the useful result, echoing the chapter's practical lesson. |
| `09-repair-tools.svg` | Chapter 17 | Hand tools and a loose washer form a working still life for the inventory of useful capacity. |
| `10-open-gate.svg` | Chapter 12 | A gate opens toward a path; access and negotiated boundaries appear together. |
| `11-soil-profile.svg` | Chapter 15 | Roots and a three-level probe cross the soil profile, echoing the mismatch between the surface reading and the root zone. |
| `12-continuity-route.svg` | Chapter 18 | Two paths share endpoints, with a break in one. The picture introduces the need to verify an alternative route. |

## Section-by-section placement

The first column uses exact manifest IDs. “None” is an intentional editorial choice. All inherited images and captions remain subject to the separate publication art and rights review.

| Section ID and source | Preferred motif and anchor | Reason or restraint |
| --- | --- | --- |
| `introduction`, `02-introduction.md` | `01-grain-and-gripper.svg`, opening ornament beneath title | Establish the food-and-machine relationship once, before the main argument. If the existing opening image is retained there, use the ornament before `## Food first`. |
| `preface`, `01-preface.md` | None | A second preliminary ornament would repeat the introduction before the reader reaches the story. |
| `chapter0`, `00-chapter0.md` | None | Let the bar scene and existing image establish the narrative world. |
| `part-1`, `part1-divider.md` | `02-event-horizon.svg`, between part title and introductory paragraph | A measured visual pause before the speculative stages. Use alongside the existing art only if the page remains spare; no automatic replacement is authorized by this map. |
| `chapter1`, `03-chapter1.md` | None | The chapter already has a diagram and illustration; another astronomical symbol adds little. |
| `chapter2`, `04-chapter2.md` | None | Stage explanations benefit more from the separate substantive diagram program. |
| `chapter3`, `05-chapter3.md` | None | Avoid turning a speculative machine exodus into a graphic that looks like an established trajectory. |
| `chapter4`, `06-chapter4.md` | None | Preserve the distinction between an imaginative horizon and a measured model. |
| `chapter5`, `07-chapter5.md` | `03-centrifugal-governor.svg`, just before the P07 precedent | Connect the historical engine discussion to mechanical regulation without illustrating a numerical claim. |
| `part-2`, `part2-divider.md` | `06-shared-table.svg`, between title and introductory paragraph | Shift scale from distant speculation to the people sharing necessities. |
| `chapter6`, `08-chapter6.md` | `08-water-pump.svg`, immediately before `## The Foundations` | A small practical object gives the transition from story to argument a physical anchor. |
| `chapter7`, `09-chapter7.md` | None | Denny's and Rosa's experiences need space; they should not become decorative symbols of hardship. |
| `chapter8`, `10-chapter8.md` | None | Avoid generic head, brain, or mindset imagery that would reduce the institutional argument to individual attitude. |
| `chapter9`, `11-chapter9.md` | None | Existing controller and workshop illustrations already carry the material detail. |
| `part-3`, `part3-divider.md` | `04-seed-and-root.svg`, between title and introductory paragraph | Open the practical section with growth supported from below. |
| `chapter10`, `12-chapter10.md` | None | The camera and Denny's voice are the visual and human focus; save the pamphlet for the chapter about distribution. |
| `chapter11`, `13-chapter11.md` | `01-grain-and-gripper.svg`, immediately before `## Useful help within reach` | Return to the introduction's assignment when the book explains a funded, usable service. |
| `chapter12`, `14-chapter12.md` | `10-open-gate.svg`, immediately before `## A place the promise can stand` | Reinforce access and the terms that govern it, without a triumphalist property symbol. |
| `chapter13`, `15-chapter13.md` | `05-roof-and-joint.svg`, immediately before `## A door you can close` | Set the lived promise of shelter beside the work supporting it. Avoid placing beside the broken-weld image. |
| `chapter14`, `16-chapter14.md` | None | Frank's bell is already the chapter's strongest small visual object. |
| `chapter15`, `17-chapter15.md` | `11-soil-profile.svg`, immediately before `## What we want the ground to do` | Reinforce measurement at different depths while remaining unnumbered and nonprescriptive. |
| `chapter16`, `18-chapter16.md` | `07-pamphlet-and-thread.svg`, immediately before P20 | Prepare the reader for the printed pamphlet, version history and corrections that must travel. |
| `chapter17`, `19-chapter17.md` | `09-repair-tools.svg`, immediately before `## Give the machines a worthwhile assignment` | Make the workbench feel usable and material before considering larger machines. |
| `chapter18`, `20-chapter18.md` | `12-continuity-route.svg`, immediately before `## Put the failed meal on the board` | Introduce continuity planning. The picture suggests a second route; the prose still requires confirming that it works. |
| `conclusion`, `21-conclusion.md` | `06-shared-table.svg`, immediately before `## A future worth wanting` | Return to the ordinary life the argument wants to protect. Add nothing after `You're holding it.` |
| `appendix-a`, `22-appendix-a.md` | None | Keep the proposal questions easy to find and reproduce. |
| `appendix-b`, `23-appendix-b.md` | None | References need typographic hierarchy and working links. |
| `appendix-c`, `24-appendix-c.md` | None | Preserve the compact reference format. |
| `appendix-d`, `25-appendix-d.md` | None | Do not reduce space for the precedent table. |
| `appendix-e`, `26-appendix-e.md` | None | Keep the practical checks direct; a decorative computer would imply more technical complexity than the prose requires. |

## Reproduction and review

Regenerate the SVG masters and black-only alternatives:

```sh
python3 publication/assets/motifs/generate_motifs.py
```

Render the contact sheets and measure geometry using the existing Playwright/Chromium installation:

```sh
python3 publication/assets/motifs/proof_motifs.py
```

`manifest.json` contains titles, accessible descriptions, palette and stroke information. `contact-sheet.html` and `contact-sheet.png` show the full family. `print-size-proof.html`, `.png` and `.pdf` pair each color drawing with its black-only counterpart at 2-inch width. `proof-results.json` records the geometric extents checked during rendering.

Self-critique and revisions: the first grain silhouette could be read as a leafy branch, so distinct awns were added. The first continuity contour sat too close to the bottom of its viewBox; the geometry check caught it, and the contour was raised. The pamphlet, table, gate and pump retain their distinct shapes in one ink. The motifs deliberately simplify mechanical and botanical forms and should remain small literary illustrations, not be enlarged or labeled as technical diagrams.

No source text, source image, caption, chapter title, build script or older edition was changed for this work. The original artwork has no external asset license dependency; final copyright and edition credits remain the publisher's production decision.

## Separate cover illustration

`publication/assets/motifs/cover-harvest.svg` is a separate, more detailed 480 × 340 original composition. Three mature grain heads, smaller plants and branching roots occupy a cultivated plot beside an articulated mechanical arm. Open fingers reach toward the grain; pin joints, structural plates, cables and restrained hatching give the machine a material presence. The composition expresses useful tending without suggesting a technical specification or claiming that this particular machine exists.

Use the cover art at 4.8 inches wide, with its natural 3.4-inch height. It contains no typography or frame. Main strokes reproduce at approximately 1.3 points; the finest hatch lines reproduce at 0.43 points. The fine lines are appropriate to this larger cover use and should not be reduced to the interior motifs' 2-inch size. A black-only version is provided at `monochrome/cover-harvest.svg`. The cream background visible in the enlarged preview belongs only to the proof, not the transparent SVG.

The cover is deliberately distinct from the small grain-and-gripper motif. Its field, root system, multiple grain heads and detailed mechanism were composed separately. First-pass self-review removed joint-crossing construction lines so the arm's outline remains readable.

Regenerate and proof it with:

```sh
python3 publication/assets/motifs/generate_cover.py
python3 publication/assets/motifs/proof_cover.py
```

`cover-harvest-proof.png` is the enlarged color preview. `cover-print-proof.html`, `.png` and `.pdf` show both palettes at the intended 4.8-inch width. `cover-proof-results.json` records measured geometry and line weights. The cover is intentionally separate from the twelve-item interior `manifest.json` so an interior placement loop will not accidentally use it as a chapter ornament.
