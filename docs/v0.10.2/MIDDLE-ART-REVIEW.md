# Middle-chapter figure review for v0.10.2

Codex, 2026-09-28. Seven native SVGs and their seven white print variants were rebuilt. The preserved v0.10.1 edition was read for baseline evidence and was not changed. Shared registries, rights records, manuscripts and publication output were not edited by this task.

## Corrections

| Asset | Meaning and presentation revised |
|---|---|
| `ch09-hyperlocal-vs-global.svg` | Shorter supply lines retain imported tools and materials, people, energy and upkeep. Removed universal exploitation and independence claims; made the repair return visible. |
| `ch09-region-ring.svg` | Regional provision is an objective to measure. Stores, seasonal production, water, power, delivery and remaining imports determine coverage. Nondirectional spokes avoid implying that households generate all power or water. |
| `ch09-cnc-bed.svg` | Generic gantry with model-dependent tooling; people inspect, maintain and harvest. A crossed circle marks Z motion into the top-view bed, distinct from in-plane X and Y motion. Removed unpinned software/tool claims and absolute space-efficiency claims. |
| `ch09-greenhouse-bus.svg` | STEMMA 4026 supplies a capacitive moisture reading, not a dedicated soil-temperature measurement. The component map includes grower settings, run-time and water limits, manual shutoff and irrigation fail-off that must be tested. This does not prescribe every actuator's safe state or promise unattended operation. |
| `ch10-model-collapse.svg` | One possible recursive-training lineage, with rare-case loss and possible narrowing or drift. Curves are conceptual, without measured axes or a generation timetable. |
| `ch10-algorithm-unlock.svg` | Four illustrated stages keep useful work, truthful storytelling, consent, correction and archives visible. Distribution may bring readers; no audience or income is promised. |
| `ch11-cooling-loop.svg` | A simpler serial coolant loop names hot and cool paths and uses mass flow in kg/s in the heat-rate equation. Retains compatibility and verification limits without making salvaged components a general recipe. |

The sensor correction follows [Adafruit product 4026](https://www.adafruit.com/product/4026), which distinguishes capacitive sensing from its microcontroller's approximate ambient-temperature reading. FarmBot's [tools page](https://farm.bot/pages/tools) describes blade/spike weeding, while its [current product specifications](https://farm.bot/) also list a rotary tool. The revision therefore stays generic rather than declaring rotary tooling nonexistent. The collapse schematic follows the recursive-sampling failure studied by [Shumailov et al., Nature (2024)](https://www.nature.com/articles/s41586-024-07566-y); it is not a newly plotted dataset. These primary pages were checked on 2026-09-28.

## Reproduction and proof

- Generator: [figures_middle.py](figures_middle.py). Uses the existing `Art` primitive from `docs/v0.10.1/vignettes.py`; importing that module does not run its generator.
- Integration handoff: [art-middle-changes.json](art-middle-changes.json). Includes filenames, dimensions, generator/provenance, old and new screen/print SHA-256 hashes, sources, changes, and recommended alt text and captions.
- Browser proof: [prove_middle_figures.py](prove_middle_figures.py) and [middle-figure-proof/checks.json](middle-figure-proof/checks.json). All fourteen PNG proofs and four deliberate failure screenshots are in that directory.

Run from the repository root:

```sh
export DAILY_NOTE_AGENT=codex
python3 docs/v0.10.2/figures_middle.py
python3 docs/v0.10.2/prove_middle_figures.py
```

All figures are 480 units wide and 588 to 650 high, with labels at least 14 units. The proof embeds the publication's JetBrains Mono font. Screen variants are rendered at 480 CSS pixels; print variants at the actual 4.56-inch placement width. The smallest revised printed label is **9.58 pt**. For comparison, baseline print minima were 6.12 pt for supply lines, 4.81 pt for CNC, 5.33 pt for the greenhouse, 4.95 pt for model collapse and 5.17 pt for storytelling. Region and cooling labels were already above the audit's 8 pt target.

All fourteen final variants pass label-bounds, full label-box intersection and sampled path-crossing checks. Screen/print layout structures match after excluding palette attributes and print's white background. Every final SVG was read back and compared with freshly generated output and the recorded hash. All seven figures received visual inspection at actual screenshot width; region, CNC and greenhouse were inspected again after semantic refinements.

Four deliberate mutations are rejected for the intended reason: a four-unit label, overlapping text, a label outside the frame and a path through a label. The proof saves the failing measurements and screenshots before inspecting the intact output. Baseline measurements are preserved separately; full text-box intersections are conservative and do not, by themselves, prove visible ink overlap.

These checks do not certify physical printer contrast, every reader's font substitution, engineering safety or final pagination. Root still needs to integrate the recommended captions/alt text and hash metadata and review the final compiled book. No full book was built here. Existing v0.10.2 reader server on port 5190 remains running.
