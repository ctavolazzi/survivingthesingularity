# Cutout, scene, and selected chart PDF review

Reviewed by Codex on 2026-09-28T14:08:57.340249+00:00.

Inspected 26 full-page PNG captures with `tools.view_image` at original image detail: six cutout pages, three scene pages, and four representative chart pages, each in the color interior and grayscale print editions. This is 13 distinct page positions in each edition. The selected PNGs are 720 by 1080 pixels, rendered at 120 dpi with Ghostscript 10.04.0. Every selected PNG hash matched the manifest before inspection and again when this report was written.

No visible clipping, missing selected artwork, caption collisions, or overlapping chart/scene labels were found in these 26 captures. This conclusion applies only to the selected renders and the visual checks described here.

One incidental readability limitation appears on physical page 7, folio 3: the separate dark ox artwork below the Atlas cutout has a small, faint subtitle in both editions. Its low contrast is especially evident in the grayscale capture. This is outside the selected cutout itself; this review does not establish whether it is new. The Atlas cutout and its separate caption remain clear.

Evidence provenance:

- Manifest: [final-samples.json](final-samples.json), SHA-256 `11e1f01f9e157d5d76b900e36af8358aa5cbb03313a65b66c90f4c190858970a`; created `2026-09-28T14:03:06.393951+00:00`.
- Color interior PDF: `publication/output/Surviving-the-Singularity-interior.pdf`, SHA-256 `265fdda8df4266e564d284560b2c1bf3894bb9c93703fcf88fae5e34d3260f59`.
- Actual color rendering source: `publication/output/print-prepared.pdf`, SHA-256 `a9e7420e7baa4f124e3458cf3fbd82716770b89bcd463ae2beebabb997175c2b`. The manifest records unchanged page streams and annotation descriptors for this prepared PDF. This review relies on that recorded preparation proof; it did not independently compare PDF streams.
- Grayscale print PDF: `publication/output/Surviving-the-Singularity-print-interior.pdf`, SHA-256 `c24e729c20d0a3d07ae130627b842aee4ee2aeec34150c09e2d6cdb87410d4bd`.
- Layout capture SHA-256: `c66a20a60f37937936548c0f48aa77baf25cbea7ec98cf45e65d2d90ec261152`.
- Build record SHA-256: `156784097528610526f630b8ee89c5f73be7a1b467ccc3256e6ca4e55344d69b`.

Visible findings, each based on both editions:

| Physical PDF page | Printed folio | Selected artwork | Observation |
| --- | --- | --- | --- |
| 7 | 3 | Atlas cutout | Right-side robot silhouette and caption are complete. Body text clears the figure and resumes across the page. Grayscale preserves the outline and visible mechanism detail. |
| 71 | 67 | Rocket cutout | Rocket, plume, and caption fit the left column. Surrounding text clears the plume and caption. The bright center of the plume is pale against white in both editions; its gray edge and base remain visible. |
| 88 | 84 | Sun cutout | Full solar disk, peripheral detail, and caption are visible. Grayscale reduces the bright color contrast but preserves disk texture and the outer silhouette. |
| 166 | 162 | Printer cutout | Printer frame, spool, build plate, and printed object are complete. Caption and adjacent paragraph do not collide. The plate and object remain distinguishable in grayscale. |
| 202 | 198 | Spot cutout | Robot body and all visible legs are complete. Left caption stays below the image; body text clears both. Grayscale retains separation of the light body from dark legs. |
| 286 | 282 | Tools cutout | Wrench, screwdriver, and pliers are complete. Image and caption remain inside the right column without text collisions. Tool edges and handle shading remain visible in grayscale. |
| 174 | 170 | Food-delivery scene | Garden, food partner, people, and five homes are visible with callouts 1 through 4. Legend, route, quantities, and caption are readable. Numbered markers preserve the mapping after color is removed. |
| 266 | 262 | Living-soil scene | Raised bed, roots, plants, water barrel, harvest crate, and arrows are visible. Callouts 1 through 4 and the two-column legend remain readable in both editions. Dark roots and soil detail are denser in grayscale, but the marked elements remain distinguishable. |
| 295 | 291 | Shared-workshop scene | Workshop floor, people, tools, shelves, and result bench remain within the illustration. Callouts 1 through 4, legend, and caption are readable and unclipped. Grayscale preserves the numbered mapping and principal object boundaries. |
| 51 | 47 | Forecast-shift chart | Both milestone rows, year labels, axis ticks, key, source note, and caption are readable. Filled and hollow endpoint markers stay distinct in grayscale; no label collisions are visible. |
| 91 | 87 | Data-centre-demand chart | Values 485 and 950, axis labels, estimate/projection labels, source note, and caption are readable. Solid and hatched bars stay distinct in grayscale. |
| 217 | 213 | Land-values chart | Line, point markers, dollar annotations, axis labels, source note, and caption are readable. Grayscale preserves the line against the lighter grid. Substantial blank space below the caption is present in both editions. |
| 313 | 309 | Meal-response chart | All six numbered steps, accompanying prompts, final note, source line, and caption fit without visible clipping or overlap. Circle outlines and text remain distinguishable in grayscale. |

Exact inspected sample files and SHA-256 hashes:

| Edition | Physical PDF page | Printed folio | Sample file | SHA-256 |
| --- | --- | --- | --- | --- |
| interior | 7 | 3 | [final/interior-007-cutout-atlas.png](final/interior-007-cutout-atlas.png) | `164f2faf2fac6f70b83b43d8fd18da766c53d1f77c9999e395bddad2a4fc6c9d` |
| interior | 51 | 47 | [final/interior-051-chart-forecast-shift.png](final/interior-051-chart-forecast-shift.png) | `9355edded50ca1000ad303962913ac952159e6bc70853fc4b170ab51c4b7a38e` |
| interior | 71 | 67 | [final/interior-071-cutout-rocket.png](final/interior-071-cutout-rocket.png) | `ca525dbf972d9cac66bd65122e0987cb8db79a67bc79c46cc9b5e080ceb6888a` |
| interior | 88 | 84 | [final/interior-088-cutout-sun.png](final/interior-088-cutout-sun.png) | `fc5723db34c299c19e5e7e97f4d1ceb61732fb44014efc41c7b8f1997a5ffdbb` |
| interior | 91 | 87 | [final/interior-091-chart-data-centre-demand.png](final/interior-091-chart-data-centre-demand.png) | `1185e2e26504ec24138d2520954e02766ee0ce913bd77536898dc8a9eac1ad5c` |
| interior | 166 | 162 | [final/interior-166-cutout-printer.png](final/interior-166-cutout-printer.png) | `b34f1932d404c3a49c776ab72e0babcb671f596dac921a8b8e46a42cad4d1316` |
| interior | 174 | 170 | [final/interior-174-scene-food-delivery.png](final/interior-174-scene-food-delivery.png) | `8227a4bb431826d9cc81c263a74e70b0f0eed3122c71a62f8c02e76905c98a22` |
| interior | 202 | 198 | [final/interior-202-cutout-spot.png](final/interior-202-cutout-spot.png) | `eb1f9d59bf603076e44bda6217d35beb7016530dacd95df35c11e04232084ba8` |
| interior | 217 | 213 | [final/interior-217-chart-land-values.png](final/interior-217-chart-land-values.png) | `c041369bff425acf03987e314ad31e9735554df6110f0d079c68ab3b20e3092a` |
| interior | 266 | 262 | [final/interior-266-scene-living-soil.png](final/interior-266-scene-living-soil.png) | `06a5508ca59e0b0d451dd92998bb746f989c5c9d051d41b7aff5996898691e3b` |
| interior | 286 | 282 | [final/interior-286-cutout-tools.png](final/interior-286-cutout-tools.png) | `86ee657488c53064abbf39f116f3147f673877949e7acb43135b006cc6e677c3` |
| interior | 295 | 291 | [final/interior-295-scene-shared-workshop.png](final/interior-295-scene-shared-workshop.png) | `d7d452f68e23cebb9f88960f9d65b5c29f8922550434a832ef9c00ea43aa3c64` |
| interior | 313 | 309 | [final/interior-313-chart-meal-response.png](final/interior-313-chart-meal-response.png) | `b2fcc7b45af7210d90a5dba73f87c2d1ce7331aa5a803a21e4093bd31536c74b` |
| print | 7 | 3 | [final/print-007-cutout-atlas.png](final/print-007-cutout-atlas.png) | `43e9f94cb447d69bbfd7422ead536a4d14e11ad8c2c15b58685c5546edceab41` |
| print | 51 | 47 | [final/print-051-chart-forecast-shift.png](final/print-051-chart-forecast-shift.png) | `27af4c7b22fdc3bc88b1df0771c26b9751fa8b43e5cb476e11776e882cdd7521` |
| print | 71 | 67 | [final/print-071-cutout-rocket.png](final/print-071-cutout-rocket.png) | `b689a38d291b664e263edaf014c0c25bab0a92eda4838c27bab0dbb72eb17115` |
| print | 88 | 84 | [final/print-088-cutout-sun.png](final/print-088-cutout-sun.png) | `7b377cf7be9bdb646ffd95f6e92282c62a032d6c3835e54c41d35b0b505a7ca4` |
| print | 91 | 87 | [final/print-091-chart-data-centre-demand.png](final/print-091-chart-data-centre-demand.png) | `0e01aa88006cb8383425b43f3db70866eab0152315b62cfcf8d05c98d1775da2` |
| print | 166 | 162 | [final/print-166-cutout-printer.png](final/print-166-cutout-printer.png) | `be0e58228531960eebeaa8baf31bdb6f19f1e4b29db88a2f33f43fc69a33fff8` |
| print | 174 | 170 | [final/print-174-scene-food-delivery.png](final/print-174-scene-food-delivery.png) | `32937869037502645a66f98cbb894ed245b666e740ff7de7f11d2b3d034d6d08` |
| print | 202 | 198 | [final/print-202-cutout-spot.png](final/print-202-cutout-spot.png) | `69e8ccbf5277c39b5954aaec17e2e64bf2de2f6c12ab9909e317aa2b01a4fcc2` |
| print | 217 | 213 | [final/print-217-chart-land-values.png](final/print-217-chart-land-values.png) | `4886283e7eb547c4d3e4a9fc593ec9b8319a1a38e7365e533951dc5a0795a115` |
| print | 266 | 262 | [final/print-266-scene-living-soil.png](final/print-266-scene-living-soil.png) | `8550a87aebe75e5365ec1f9614f431efe7a73c60c72df7f0951985214d550ad0` |
| print | 286 | 282 | [final/print-286-cutout-tools.png](final/print-286-cutout-tools.png) | `475b20e984aba9aff1517832c67066b1ed5e8f8d1712c59cf0e929782b49fc90` |
| print | 295 | 291 | [final/print-295-scene-shared-workshop.png](final/print-295-scene-shared-workshop.png) | `bc0a2ebd870f3e0744a56610b6e75acdbbe46528d8084e954b48e4f0ae8bcb54` |
| print | 313 | 309 | [final/print-313-chart-meal-response.png](final/print-313-chart-meal-response.png) | `7a20bcf3bc79bfdecba82d3f0e976c5d9fa5e8c41f7096146ebcf3b73191da81` |

Limitations: This is a screen review of 120 dpi raster output, not a physical print proof. It does not establish paper/ink behavior, fine-detail reproduction at press resolution, color accuracy, accessibility, link operation, data correctness, or complete source-text recovery. The chart selection is representative; other charts, the revised diagram pages, other page positions, and the reading PDF were not inspected in this task. No source artwork or earlier-release render was used to assert that these figures are unchanged. No PDFs, source files, artwork, captures, or manifests were edited.

## Additional revised-diagram coverage

Added by Codex on 2026-09-28T14:41:01.455625+00:00. This addendum extends the earlier scope and its exclusion of revised diagrams for the six page positions listed below.

Inspected six paired PNGs with `tools.view_image` at original image detail, each showing color on the left and grayscale on the right. This adds 12 edition page images, for a cumulative total of 38 edition page images at 19 distinct page positions. The pair files are 1456 by 1080 pixels, comprising two original 720 by 1080 captures separated by 16 pixels. Source PNG hashes match both the final manifest and the review receipt. Read-only pixel comparison confirmed that the left and right page regions exactly match their original captures without resampling.

No visible clipping, missing labels, or caption collisions were found in these six pairs. The timeline limitation below concerns the visual size of very short periods, not a claim of missing source data.

- Pair receipt: [revised-diagram-review-receipt.json](revised-diagram-review-receipt.json), SHA-256 `84a62ea64b158bad340f798e36970681f3a86b107bfaae05e32d4bd2bfca061a`.
- Final manifest and PDF provenance are the same as recorded above. The 120 dpi screen-review limitations still apply. The other revised diagram pages were reviewed separately by another agent and are outside this reviewer's coverage.

| Physical PDF page | Printed folio | Diagram | Visible findings in both editions |
| --- | --- | --- | --- |
| 288 | 284 | Algae loop | Both flow sections, fish-tank and grow-bed boxes, return-water arrow, feed-branch arrow, limitation text, and caption are readable. Arrowheads remain visible in grayscale; no label or caption collisions are visible. |
| 292 | 288 | DC routes | Solar, charge-control, battery, inverter/adapter route, regulated DC route, and both load boxes are readable. Conversion arrows and the notes retain separation from text in grayscale. Caption is complete and clear of body copy. |
| 294 | 290 | Fab lab | Printer, metalwork, tractor, and output-part outlines remain visible in grayscale. Three tool labels, shared-input line, output label, final note, and caption are readable without clipping or overlap. |
| 308 | 304 | Social contract | Both columns, central divider, document/envelope symbols, arrows, provision labels, final note, and caption are readable. The proposed document outline remains visibly dashed in grayscale. |
| 320 | 316 | Conversion ladder | All nine numbered rungs and their two-line explanations are readable. Lower seven solid rungs and upper two dashed rungs match their visible key in both editions. The instruction to start below, limitation note, and caption are complete; no rung labels collide. |
| 374 | 370 | Precedent timeline | Nineteen plotted row labels and five earlier-case labels are readable, as are year ticks, legend, earlier dates, Appendix D pointer, and caption. Longer dashed periods, solid spans, and round single-date dots are visibly distinct in grayscale. Very short approximate periods become single square marks or tiny ticks at this 120 dpi scale, so repeated dash structure cannot be resolved for those short marks. P-19 Victory gardens is particularly small. Exact-date interpretation requires the Appendix D text, as the caption states. |

Exact additional source capture records:

| Edition | Physical PDF page | Printed folio | Source capture | SHA-256 |
| --- | --- | --- | --- | --- |
| interior | 288 | 284 | [final/interior-288-ch17-algae-loop.png](final/interior-288-ch17-algae-loop.png) | `661374e94daaa23efbcef8da3267a130f00db5bf211732552487111d11486d6d` |
| interior | 292 | 288 | [final/interior-292-ch17-dc-native.png](final/interior-292-ch17-dc-native.png) | `5f7144a6a4ea0144694ffa6d50863dd26ae0e5f7df7e86fe76392e33539e1e2f` |
| interior | 294 | 290 | [final/interior-294-ch17-fab-lab.png](final/interior-294-ch17-fab-lab.png) | `93de2069ddafb90340fa5973165eaa9f31d8e3e3629dd8b5bdb1001caf575dc9` |
| interior | 308 | 304 | [final/interior-308-ch18-social-contract.png](final/interior-308-ch18-social-contract.png) | `100c565d295fc88e77cac650df381fbeec866d1df9a5ba1890e524203318fc70` |
| interior | 320 | 316 | [final/interior-320-ch19-conversion-ladder.png](final/interior-320-ch19-conversion-ladder.png) | `5e4b67009a49bfe0211de971d3a3c06837f4798ceee6f1f1d40b098e32e8a51c` |
| interior | 374 | 370 | [final/interior-374-appd-precedent-timeline.png](final/interior-374-appd-precedent-timeline.png) | `e34414d6c938de587886c318833dba3f8ec6e1355aadbb8bf14cb38e261c4358` |
| print | 288 | 284 | [final/print-288-ch17-algae-loop.png](final/print-288-ch17-algae-loop.png) | `e9ea86249765c84f8ae650e178c9c37f34d2c9e2a170fd9ee3e07a6a73f5dc80` |
| print | 292 | 288 | [final/print-292-ch17-dc-native.png](final/print-292-ch17-dc-native.png) | `94eda63603ce1406f1a3d0894485002997d0a4dea60dbbc2a37e40b95c11703a` |
| print | 294 | 290 | [final/print-294-ch17-fab-lab.png](final/print-294-ch17-fab-lab.png) | `17efce570f9d521f66601ca057fe6ec02460e224deacd4394d47c925127003a0` |
| print | 308 | 304 | [final/print-308-ch18-social-contract.png](final/print-308-ch18-social-contract.png) | `5183027b0cb1a6a6b62336b3904824b3050cacca9232510151b777b328099c7f` |
| print | 320 | 316 | [final/print-320-ch19-conversion-ladder.png](final/print-320-ch19-conversion-ladder.png) | `03ed4260ddc2c498030d4fd0cdf0f444e32bb427c83d8ea85829c8658e2098f1` |
| print | 374 | 370 | [final/print-374-appd-precedent-timeline.png](final/print-374-appd-precedent-timeline.png) | `40916f82f3280d5869bd3ea22e373d13bd50a4dda5d1bc1ffcfc4790fe8e76e3` |

Exact paired PNGs inspected:

| Physical PDF page | Pair file | SHA-256 |
| --- | --- | --- |
| 288 | [review-pairs/288-ch17-algae-loop-color-gray.png](review-pairs/288-ch17-algae-loop-color-gray.png) | `b81e8172e4dec26ee7ea361dfb2c2e22439fb9a0ef0abeb2b1d34adb07feac9c` |
| 292 | [review-pairs/292-ch17-dc-native-color-gray.png](review-pairs/292-ch17-dc-native-color-gray.png) | `d4f942016b9f33cbbed6af9afd893d7d27b404ebc2f5fd1613d4ac350731d3bf` |
| 294 | [review-pairs/294-ch17-fab-lab-color-gray.png](review-pairs/294-ch17-fab-lab-color-gray.png) | `a4c6bf13783c7f7fefb5043764e8a2e4dd58e84d8ccda6d69007631b871b48ec` |
| 308 | [review-pairs/308-ch18-social-contract-color-gray.png](review-pairs/308-ch18-social-contract-color-gray.png) | `7bdf91a3dbf9f872ca46db3d0c1d8d3cb1c24c0eec4806f011de7ff05a6d35da` |
| 320 | [review-pairs/320-ch19-conversion-ladder-color-gray.png](review-pairs/320-ch19-conversion-ladder-color-gray.png) | `c9ac643ed478c78053f192669a3edacc59324d7bff02799b4ae3f88c86ed66b6` |
| 374 | [review-pairs/374-appd-precedent-timeline-color-gray.png](review-pairs/374-appd-precedent-timeline-color-gray.png) | `5d0042deb39d6f5364942dd04465e5cd3fc91364e7cd74df8ee6976205d456d5` |
