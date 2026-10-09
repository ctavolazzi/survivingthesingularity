# Final PDF art review: v0.10.1

Reviewed September 28, 2026. No blocking visual defect was found in the eight
new charts, six conceptual illustrations, or three scene stills in the final
color and grayscale interior pages. The production reviewer independently
inspected the six photo-derived cutouts in both renditions with the same
result. Together these reviews cover all twenty-three additions through
forty-six final page samples.

## Exact artifacts and sampling

| Artifact | Pages | SHA-256 |
| --- | ---: | --- |
| Color interior | 393 | `8c47246769808fffdb1a47bf0e6c038624aea94039911d6d34721f2a3690c946` |
| Grayscale print interior | 394 | `81a2bde3407457df9ff157ce1380a2e89cb0899b6d5dd641accd9062752709b9` |
| Resource-pruned color rendering input | 393 | `f71696f64094cb003a89c0db4b7352b56b1f824530ca3ceb729944c22d7865b8` |

The grayscale edition has a final blank verso. The reading edition adds its
cover to the color interior; its corresponding physical figure pages are one
greater than those below. This review does not claim a separate raster pass
over the reading edition.

[final-samples.json](final-samples.json) records all thirty-four sample hashes,
physical pages, printed folios, PDF hashes, layout-capture hash, and build hash.
The 140 dpi full-page images are in [final/](final/). The color raster input is
`print-prepared.pdf`, whose unused resource references were pruned without
changing any page content streams or annotation descriptors. The sampler
verifies its current hash, original-interior hash, and production's successful
preservation controls before using it. All source hashes stayed unchanged
through the final raster pass.

Reproduce from the repository root:

```sh
python3 docs/v0.10.1/pdf-proof/render_samples.py --stage final --non-cutouts --prepared-color
```

The script makes one Ghostscript `PageList` call per edition. Earlier sampling
reloaded the large unpruned resource dictionary for every color page and was
stopped before the publication rebuild. Those partial images in `initial/`
are preliminary evidence, not a complete earlier certification. Fourteen
already inspected preliminary rasters proved byte-identical to the final
samples; the remaining twenty final samples were inspected directly. The
comparison record is [reviewed-samples.json](reviewed-samples.json).

The production reviewer's twelve additional cutout samples and inspection
are recorded in [cutouts-final/samples.json](cutouts-final/samples.json).
Its original color, prepared color, and grayscale PDF hashes match the
artifacts above. All twelve samples were inspected directly after the fix.

## Pages inspected

Page numbers in this table are physical interior/print pages, followed by
printed folios. Every listed figure was inspected in both color and grayscale.

| Figure | Physical page | Folio | Review finding |
| --- | ---: | ---: | --- |
| Researcher forecast shift | 53 | 49 | Open and filled markers, dates, and distinct milestones remain clear. |
| Local copies | 64 | 60 | Broken connection, local file, and power limitation remain readable. |
| Data-centre demand | 92 | 88 | Solid estimate and hatched projection remain distinct without color. |
| Income and food access | 111 | 107 | Direct percentages and dotted national reference remain legible. |
| Access gate | 113 | 109 | Capability, terms, and access read in sequence with unbroken arrows. |
| Attention ribbon | 147 | 143 | Interrupted and continuous forms remain distinct; caption stays attached. |
| Ammonia energy | 164 | 160 | Estimate and benchmark hatching survive conversion; units stay clear. |
| Food-delivery scene | 170 | 166 | Five homes, garden, partner, people, numeric pins, and arithmetic remain visible. |
| Operating stack | 198 | 194 | All four operating requirements and the license boundary remain legible. |
| Weights memory | 200 | 196 | Six values, units, and runtime exclusions are clear; following equation stays intact. |
| Land values | 212 | 208 | Endpoint labels and leader avoid the plot; annual markers remain distinguishable. |
| Shared land | 213 | 209 | Owner, users, and neighbors retain equal visibility with the consent note. |
| Waste pathways | 243 | 239 | All nine categories and percentages fit; the smallest bar retains its numeric value. |
| Living-soil scene | 259 | 255 | Roots, inputs, harvest, water losses, and conceptual-scope note remain visible. |
| Shared-workshop scene | 288 | 284 | People, tools, supplies, and useful output remain identifiable. |
| Continuity calendar | 297 | 293 | Solid secured period and dashed proposed continuation remain distinct. |
| Meal-response worksheet | 305 | 301 | Six numbered prompts and the privacy note remain clear; complete caption fits. |

All seventeen complete captions remain on their figure's page. The inspected
pages show no cropped SVG lettering, labels colliding with one another,
prose painted over a figure, or figure intrusion into a margin. Large chart
pages retain intentional lower whitespace where the next block does not fit.

## Cutout inspection and resolved layout defects

The production reviewer inspected Atlas on physical page 7 (folio 3), Falcon
Heavy on 73 (69), the sun on 90 (86), the printer on 163 (159), Spot on 197
(193), and tools on 278 (274), in color and grayscale. The final rasters show
clean transparent edges, complete credits on the image's page, readable
adjacent prose, and no gutter intrusion or prose collision.

The first whole-book capture found captions extending beyond their figure
containers and the tools caption splitting onto the following page. A floated
flex container now keeps each image and caption together, and increased
caption line height contains the complete glyph bounds. The tools image and
credit now share page 278. The first failing layout capture/checks are
retained alongside this report as `first-build-*.json`; the successful final
whole-book geometry and resource checks are recorded by the production proof.

## Static scene equivalence

The three static scenes communicate the relationships described in their
canonical alternative text and captions without an interactive camera. Each
has four numbered pins and an explicit text key. Food delivery retains the
eight-plus-two kilogram inputs and five recipient homes; the soil cutaway
retains exchanges across the bed boundary; the workshop retains the people,
supplies, operation/maintenance, and resulting repair. In grayscale, roofs
and machinery lose their color distinctions, but geometry, pins, and text
continue to identify those relationships. None requires color alone to
recover its intended explanation.

The illustrations remain readable in these digital full-page rasters. This
does not certify physical ink or paper contrast, every page of the book,
assistive-technology behavior, scene interaction, source factual accuracy,
or image rights. The separate scene browser proof and production checks
cover their stated scopes. No manuscript, artwork, or publication output
was changed by this reviewer.
