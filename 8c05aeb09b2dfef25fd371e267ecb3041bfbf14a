# SVG art audit for v0.10.2

Read-only review by Codex, 2026-09-28. No image or canonical prose was changed by this audit. Findings capture the labels available during review, while the lead agent was correcting diagrams in parallel. This is an input to that correction pass, not a claim that every finding remains in the final release.

## Coverage and method

All **54 SVG assets referenced by canonical manifest sections** were inventoried and their title, description, visible text, labels and relevant visual encodings read. Four are text-free ornaments. Four substantive diagrams were already assigned to the lead agent for correction: `ch12-csa-network`, `ch14-logistic-shockwave`, `ch15-soil-food-web`, and `ch17-algae-loop`. The other 46 labelled figures received this independent content review. All 54 received baseline print-size inspection.

Evidence is preserved in [art-inventory.json](art-inventory.json), including captured labels, chapter references, viewBoxes, prepared print variants, baseline placement sizes, and minimum font estimates. Print evidence comes from `../sts-v0.10.1/publication/output/interior-layout.json`, `interior-figure-layout.json`, the matching `static/book-images/print/` variants, and the existing 394-page print PDF. Figure width is 4.56 inches in that layout. The print converter enlarges some source fonts and crops viewBoxes, so the raw dark SVG font size alone is not a valid measurement.

Estimated point size = prepared print SVG font size × placed width in inches × 72 / prepared print viewBox width. These are geometry-based estimates before PDF outlining/rasterization, not font sizes extracted from the PDF. The PDF text extractor could not observe the embedded labels. Only three existing PDF pages were rasterized at 144 dpi for visual checking; no new full book was rendered:

- [Page 16: nine stages](art-audit-samples/v0101-page-16.png).
- [Page 270: sneakernet](art-audit-samples/v0101-page-270.png).
- [Page 360: precedent timeline](art-audit-samples/v0101-page-360.png).

Those samples confirmed cramped explanatory labels and the timeline dash defect. This review is not an accessibility certification or a visual proof of every final v0.10.2 page.

## Actionable findings

**L01, print readability, high.** In the baseline, 27 of 50 labelled SVGs contain labels below 8 pt, and 21 contain labels below 6 pt. The smallest estimate is 4.54 pt. Table below identifies every affected asset. Use 8 pt as a practical review target for explanatory labels, not a claimed universal publishing standard. Recompose wide diagrams into stacked panels, reduce repeated wording, or split a dense figure. Enlarging the whole figure cannot solve a page-width constraint, and globally enlarging text inside fixed boxes can introduce collisions. Check the resulting print variants and actual-size pages after reflow. New v0.10.1 charts are mostly 9.23 pt or larger and show that the inherited tiny labels are not required by the book format.

**A01, nine stages, high.** `intro-nine-stages.svg` makes the 2027 ASI leap unconditional and depicts later stages as outgrowing physics. The opening chapters explicitly identify these as speculative stages; AGI arrival is not an observed date or consensus forecast. Label this a speculative sequence, qualify the 2027 scenario, and frame later stages as imagined possibilities. Preserve CT's staged argument without making the chart an empirical forecast. Also L01.

**A02, information architectures, high.** `ch08-info-architectures.svg` assigns depleted working memory and zero strategic capacity to reactive feeds, then high executive function and surplus energy to analog batching. Updated Chapter 8 describes a suggested routine and possible interruption costs, not guaranteed neurological states. Replace guaranteed outcomes with concrete behavior: unscheduled interruptions versus chosen check times; work interrupted versus time protected for a task. Also L01.

**A03, supply lines, medium.** `ch09-hyperlocal-vs-global.svg` says every global link exploits someone while the local loop depends on no distant exploited worker. That universal claim exceeds the chapter's shorter-supply-line argument and conceals imported tools, components and power inputs. Show fewer or shorter dependencies and name those that remain. Local production does not establish fair treatment by itself. Also L01.

**A04, region ring, high.** `ch09-region-ring.svg` says the surrounding region can produce everything and will still eat if trucks stop. Chapter 9 asks how long a particular region could feed people and treats the unknown as work to do. Replace those guarantees with a capacity-building objective and measured duration: local stores, production, water, power, logistics and remaining imports determine coverage. This otherwise legible figure has no L01 flag.

**A05, greenhouse bus, high.** `ch09-greenhouse-bus.svg` labels STEMMA's temperature as soil temperature and promises unattended irrigation precision. Adafruit's product 4026 uses its microcontroller's internal sensor for approximate ambient temperature, not a dedicated soil-temperature probe. Use a moisture-reading label, or explicitly identify board temperature. Include grower settings, run-time limits and fail-off/manual control to match Chapter 9. The figure should be a component map rather than an assurance that a controller safely waters unattended. [Adafruit product 4026](https://www.adafruit.com/product/4026), checked 2026-09-28. Also L01.

**A06, CNC bed, medium.** `ch09-cnc-bed.svg` claims no wasted bed and names an OpenCV rotary weeder without identifying a hardware/software version. Replace the absolute density claim with reduced walking space and make tooling model-specific or generic. The manufacturer's [tools page](https://farm.bot/pages/tools) describes a blade/spike weeder while the current [main product page](https://farm.bot/) also lists a rotary attachment. Therefore this review does **not** claim rotary tooling does not exist; the unsupported conflation and unpinned version are the issues. Both checked 2026-09-28. Also L01.

**A07, container shell, high.** `ch13-shell-architecture.svg` presents chaining/welding with a specified rod as a structural recipe and promises 640 square feet of open space for about $25,000 all-in. Chapter 13 now distinguishes a fictional budget from real engineered construction. Use a conceptual plan, nominal exterior footprint rather than usable floor area, and site-specific engineered connections/reinforcement. Remove the welding recipe and general all-in cost; the caption can refer to the story's budget and scope. The reference to a center-seam figure should be rechecked after final ordering. Also L01.

**A08, sneakernet, high.** `ch16-sneakernet.svg` describes an unhackable network immune to surveillance, shutdown and electromagnetic interference. Updated Chapter 16 explicitly discusses copying, damage, loss, encryption and backups. Replace immunity with the bounded benefit: a hand-carried file does not require a live network link. Endpoints and media still need trusted handling and compatible software; encryption does not guarantee secrecy or recoverability. Also L01.

**A09, social contract, high.** `ch18-social-contract.svg` states that robots perform the toil and closed loops feed them, presenting local abundance as achieved. Chapter 18 tests a proposed service through supplies, paid labor, backup, eligibility and continuity. Label the right-hand column as a proposed arrangement, retain human work and replenishment, and make adequacy a delivery commitment that must be funded and checked. This preserves the author's policy position without claiming a complete technical implementation. Also L01.

**A10, ladder precedents, medium.** `ch19-conversion-ladder.svg` compresses France's 2016 rules into a ban on destroying all edible food and maps that to a universal free meal. Updated Chapter 19 distinguishes restrictions on deliberately spoiling surplus and donation agreements from universal free access. Suggested label: “France, 2016: surplus-food recovery rules.” Add that precedents support parts of the proposal, not its complete implementation. Change categorical 99-year CLT leases to “long-term ground leases” or “often 99-year leases,” consistent with the chapter. These are consistency corrections to already sourced canonical prose; this audit did not independently redo legal research. Also L01.

**A11, cooling equation, medium.** `ch11-cooling-loop.svg` uses “flow × Cp × ΔT” without stating mass flow, while Chapter 11's calculation correctly uses kg/s. Replace “flow” with “mass flow” so the equation is dimensionally clear. Existing illustrative-components and compatible-system caveats are useful and should remain.

**A12, fab lab, medium.** `ch17-fab-lab.svg` groups a BCS-type tractor under open-source machine cores and labels generic output as seals, valves and structural steel. Chapter 17 now describes a shared walk-behind tractor and validates the actual task, materials, maintenance and remaining work. Use “shared walk-behind tractor” unless a specific open design is identified; do not conflate a commercial product form with the GVCS design library. The manufacturer's [tractor catalogue](https://www.bcsamerica.com/products/tractors) identifies model-specific commercial equipment but does not establish an open-design license; absence on that page is not proof that no licensed design exists. Checked 2026-09-28. Describe outputs as suitable, checked replacement parts and fabricated components, not universal replacements for safety-critical parts. Match “Neighborhood Fab Lab” in prose/caption unless CT specifically wants a different title.

**A13, timeline dash semantics, medium.** `appd-precedent-timeline.svg` says dashed bars identify approximate spans, but its round-capped 6-unit strokes with a 5/4 dash pattern bridge the 4-unit gap. Each rounded end extends about 3 units, so neighboring ends overlap; the baseline PDF sample visibly shows solid bars. Use butt caps or a gap greater than stroke width, and inspect at final print size. This is an encoding defect even though the deep-history labels contain explicit approximate dates. Also L01.

**A14, food-insecurity headline, optional editorial clarification.** `intro-food-insecurity.svg` has correctly labelled series and recession association, but the jobs-to-dinner headline can be read as a causal finding from the chart. The plotted household series does not isolate job loss as the sole cause. A more evidence-specific headline would separate the observed recession trend from CT's access argument in the surrounding prose. This is lower priority than correcting erroneous values or forecasts; no data correction was identified.

## Meaning beyond color

The source review found no additional meaning conveyed solely by color that requires a new encoding. Food-insecurity series use solid/dashed lines and text labels; forecast markers use hollow/filled forms and labelled years; estimate/projection and benchmark charts use direct labels and/or patterns. Ladder precedent categories use solid/dashed borders with a legend. Network comparisons use headings, node layouts and explanatory labels. Cooling paths are named and arrowed. Isometric scenes use numbered callouts with matching text. The timeline's intended non-color distinction is broken as described in A13. Final grayscale proofs still need inspection after edits, especially where line weight or collisions may erase these distinctions.

## Complete inventory

Pages are physical pages in the baseline v0.10.1 PDF, not folio labels. “No new defect” means no additional semantic or label-size defect was identified in this bounded review; it does not certify every numerical dataset or rendering. “Root correction” records ownership, not a pass.

| Referenced SVG | Baseline page | Smallest estimated pt | Review result |
|---|---:|---:|---|
| `intro-food-insecurity.svg` | 12 | 10.89 | A14 |
| `intro-nine-stages.svg` | 16 | 5.84 | A01, L01 |
| `v101-chart-forecast-shift.svg` | 53 | 9.23 | No new defect |
| `ch02-eighteen-days.svg` | 63 | 4.61 | L01 |
| `v101-visual-local-copies.svg` | 64 | 9.58 | No new defect |
| `v101-chart-data-centre-demand.svg` | 92 | 9.23 | No new defect |
| `ch05-horses-tractors.svg` | 99 | 4.54 | L01 |
| `coop-cast.svg` | 102 | 9.23 | No new defect |
| `original-09-repair-tools.svg` | 103 | no labels | Ornament |
| `ch06-capability-access.svg` | 108 | 4.63 | L01 |
| `v101-chart-income-food-access.svg` | 111 | 9.23 | No new defect |
| `v101-visual-access-gate.svg` | 113 | 9.58 | No new defect |
| `ch08-cognitive-extraction.svg` | 142 | 6.66 | L01 |
| `ch08-focus-recovery.svg` | 143 | 5.53 | L01 |
| `ch08-firewall-pipeline.svg` | 144 | 5.61 | L01 |
| `ch08-info-architectures.svg` | 146 | 5.55 | A02, L01 |
| `v101-visual-attention-ribbon.svg` | 147 | 9.58 | No new defect |
| `ch08-star-vs-mesh.svg` | 150 | 4.98 | L01 |
| `ch09-hyperlocal-vs-global.svg` | 160 | 6.12 | A03, L01 |
| `ch09-region-ring.svg` | 162 | 9.94 | A04 |
| `v101-chart-ammonia-energy.svg` | 164 | 9.23 | No new defect |
| `ch09-cnc-bed.svg` | 166 | 4.81 | A06, L01 |
| `ch09-greenhouse-bus.svg` | 167 | 5.33 | A05, L01 |
| `v101-scene-food-delivery.svg` | 170 | 8.21 | No new defect |
| `original-07-pamphlet-and-thread.svg` | 176 | no labels | Ornament |
| `ch10-model-collapse.svg` | 183 | 4.95 | L01 |
| `ch10-algorithm-unlock.svg` | 184 | 5.17 | L01 |
| `v101-visual-operating-stack.svg` | 198 | 9.58 | No new defect |
| `v101-chart-weights-memory.svg` | 200 | 9.23 | No new defect |
| `ch11-cooling-loop.svg` | 202 | 10.28 | A11 |
| `original-04-seed-and-root.svg` | 206 | no labels | Ornament |
| `v101-chart-land-values.svg` | 212 | 9.23 | No new defect |
| `v101-visual-shared-land.svg` | 213 | 9.58 | No new defect |
| `ch12-csa-network.svg` | 216 | 4.55 | Root correction |
| `ch13-shell-architecture.svg` | 228 | 6.21 | A07, L01 |
| `ch13-thermal-seal.svg` | 229 | 4.77 | L01 |
| `ch14-logistic-shockwave.svg` | 239 | 6.22 | Root correction |
| `v101-chart-waste-pathways.svg` | 243 | 9.23 | No new defect |
| `ch14-mesh-comms.svg` | 245 | 7.06 | L01 |
| `original-11-soil-profile.svg` | 251 | no labels | Ornament |
| `ch15-clt-firewall.svg` | 256 | 5.53 | L01 |
| `ch15-soil-food-web.svg` | 258 | 5.34 | Root correction |
| `v101-scene-living-soil.svg` | 259 | 8.21 | No new defect |
| `ch16-sneakernet.svg` | 270 | 5.04 | A08, L01 |
| `ch17-algae-loop.svg` | 280 | 5.64 | Root correction |
| `ch17-lora-node.svg` | 282 | 9.50 | No new defect |
| `ch17-dc-native.svg` | 284 | 6.16 | L01 |
| `ch17-fab-lab.svg` | 286 | 10.37 | A12 |
| `v101-scene-shared-workshop.svg` | 288 | 8.21 | No new defect |
| `v101-visual-continuity-calendar.svg` | 297 | 9.58 | No new defect |
| `ch18-social-contract.svg` | 300 | 5.37 | A09, L01 |
| `v101-chart-meal-response.svg` | 305 | 9.23 | No new defect |
| `ch19-conversion-ladder.svg` | 310 | 4.92 | A10, L01 |
| `appd-precedent-timeline.svg` | 360 | 4.95 | A13, L01 |

## Release handoff

Urgent findings were sent to the lead agent during review. Four independently assigned corrections remain under that agent's ownership; their old labels are preserved in the inventory for traceability. Reconcile the issue list against the final SVGs, regenerate their print variants and visual metadata, and then inspect actual-size output. Update canonical alt text and captions when meaning changes, including the old “open-source tractor” alt text in Chapter 17. Do not report this baseline audit as proof that revised output has been inspected.
