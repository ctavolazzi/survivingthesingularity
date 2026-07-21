# Art Catalog — Surviving the Singularity

Human-readable index of the book's illustration assets. The machine-readable source
of truth is **`src/lib/data/book/art-catalog.json`** (schema `sts-art-catalog/v1`) —
build coursework and tooling against that file, not this one.

- **ID scheme:** `sts.<kind>.<slug>` where kind is `sprite` (object), `char`
  (character), `plate` (composite figure placed in the book), `diagram` (SVG).
- **Palette:** navy `#020617`, amber `#f59e0b`, blue `#3b82f6`, slate `#94a3b8`, ink `#f1f5f9`.
- **Raw sprites** (transparent PNG, reusable for recomposition): `static/book-images/sprites/<id-with-hyphens>.png`.
- **Provenance / license:** PixelLab (Tier 1) generations + Python(Pillow) compositing;
  SVG diagrams hand-authored. PixelLab assets are subject to PixelLab ToS
  (https://pixellab.ai/termsofservice) — confirm rights before external/commercial coursework reuse.
- Introduced at book **v0.7.0** (2026-07-20).

## Object sprites (`sts.sprite.*`)

| ID | Label | Concepts | PixelLab object (review → selected frame) | Chapter |
|---|---|---|---|---|
| sts.sprite.photobioreactor | DIY Photobioreactor | algae, aquaponics, closed-loop, 3d-printing | be66341d → 518e9f04 (alt 24995ad3) | ch17 |
| sts.sprite.grow-tower | Vertical Grow Tower | vertical-hydroponics, food, water-efficiency | b54c09a3 → da227fbd | ch17 |
| sts.sprite.lora-node | LoRa Mesh Node | mesh, lora, off-grid-comms, meshtastic | 3a25f932 → 2e70c977 | ch17 |
| sts.sprite.solar-battery | Solar + Battery Rig | solar, off-grid-energy, dc-microgrid | aa08d2ec → 7628f606 | ch17 |
| sts.sprite.printer-3d | Desktop 3D Printer | 3d-printing, reprap, distributed-mfg | 60426470 → bef728c7 | ch17 |
| sts.sprite.plasma-table | CNC Plasma Table | cnc, metal-fab, maker-shop | c4ea7230 → 9fc3df01 | ch17 |
| sts.sprite.walk-behind-tractor | Walk-Behind Tractor | appropriate-tech, tillage, bcs | 6ecd5de2 → 3328f7fb | ch17 |
| sts.sprite.cyberdeck | Homemade Cyberdeck | cyberdeck, offline-computing, autonomy | c2e1e7b0 → 15546138 | appendix-e |
| sts.sprite.ox-and-plow | Ox and Plow | husbandry, delegated-labor, AI-analogy | f2ebbf38 → 1f525619 (alt 101a601f) | introduction |

## Character sprites (`sts.char.*`) — 8-direction PixelLab v3, south view used

| ID | Label | Role | PixelLab character_id |
|---|---|---|---|
| sts.char.elijah | Elijah | narrator; ex-tech, learning to build | ae2178a9-ccd3-4d71-92a3-b3e8d7f17f88 |
| sts.char.marta | Marta | fabricator; runs the shop | f4b231e5-f2f6-4a0c-b8e2-81827243af59 |
| sts.char.priya | Priya | soil scientist | 21b9fdab-12ea-48f8-a0a6-1dad48fdf422 |
| sts.char.denny | Denny | network engineer; livestreamer | 6889a96a-3ab5-4884-b7bf-89bec3bddf03 |

Character sprites have all 8 rotations available on PixelLab (and 40+ template animations)
if future coursework wants motion or alternate angles.

## Composite plates & diagrams (placed figures)

| ID | Label | Figure file | Placed in |
|---|---|---|---|
| sts.plate.field-kit | The Field Kit (8 objects) | ch17-field-kit.png | 19-chapter17.md, Foundations intro |
| sts.plate.co-op-cast | The Co-op (4 characters) | coop-cast.png | part2-divider.md |
| sts.plate.photobioreactor | Photobioreactor (solo) | ch17-photobioreactor.png | 19-chapter17.md, SECTOR 07 |
| sts.plate.cyberdeck | Cyberdeck (solo) | appe-cyberdeck.png | 26-appendix-e.md |
| sts.plate.ox-and-plow | You Do Not Program an Ox | intro-ox-plow.png | 02-introduction.md |
| sts.diagram.hyperlocal-vs-global | Two Supply Lines | ch09-hyperlocal-vs-global.svg | 11-chapter9.md |
| sts.diagram.algae-loop | Closed Algae Fish-Food Loop | ch17-algae-loop.svg | 19-chapter17.md, SECTOR 07 |

## Manuscript addressing (every block, not just art)

As of 2026-07-20 every block of the book carries a stable unique id via the
manuscript index — `src/lib/data/book/manuscript-index.json` (schema
`sts-manuscript-index/v1`, built by `sts.py id build`). Ids look like
`sts.chapter9.b0029`; figure blocks cross-link back to this catalog through an
`art_id` field. So the two namespaces join cleanly:

- **art id** (`sts.plate.*` / `sts.diagram.*` / `sts.sprite.*`): the semantic
  asset, with concept tags — this file.
- **block id** (`sts.<section>.b<NNNN>`): where that asset (or any paragraph) is
  placed in the manuscript — the index.

`sts.py id list --type figure` enumerates all 66 figures and shows which already
have an `art_id`. That is the worklist for the cataloguing task below.

## Not yet catalogued (future work)

The 33 pre-existing hand-authored SVG figures (`ch*-*.svg`), the photo headers
(`ch*.jpg/.webp`), and the three pixel-art part-divider banners
(`part{1,2,3}-divider.png`) are **not yet** in `art-catalog.json` (7 of the 66
figures are catalogued; 59 are not). Extending the catalog to every book figure
(with concept tags) is the prerequisite for chapter-complete programmatic
coursework. Every one of those 59 already has a stable block id in the manuscript
index, so the join target exists — only the concept tags are missing. See the
continuation prompt.
