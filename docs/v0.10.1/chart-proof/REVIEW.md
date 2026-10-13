# v0.10.1 chart proof

Reviewed 2026-09-27. Eight new graphics are ready for canonical placement: six graphics of published quantitative evidence, one memory calculation matrix, and one illustrative meal-response worksheet. Each has a dark source SVG and a matching light print SVG. No existing figure was replaced.

Run `python3 docs/v0.10.1/charts.py` from the repository. The generator reads [chart-data.json](../chart-data.json), uses the repository's JetBrains Mono fonts for browser proofs, and reuses the established path-crossing audit from `docs/v0.9.2/print_figures.py`. It requires Python Playwright and Chrome. [chart-placements.json](../chart-placements.json) supplies exact canonical paragraph anchors, placement direction, source and print paths, descriptive alt text, and sourced captions. Manuscript and catalog integration belongs to the root task.

## Data review

All primary sources were reopened and the plotted rows checked on 2026-09-27. PDF values were cross-checked against the extracted table and chart labels. The JSON preserves exact source locations, values, units, evidence types, exclusions, and the distinction between reported and calculated quantities. The abbreviated EPA label “Bio-based / biochemical” retains its full combined source category in the data ledger and alt text.

| New graphic | Evidence and treatment | Source checked |
| --- | --- | --- |
| Waste pathways | Nine EPA management estimates for 2019. Percentages total 100.00. Published integer tonnage rows sum to one ton more than the published total; both are preserved. Manufacturing is excluded, and wasted food includes inedible material. Donation excludes food banks' undistributed portion. | [EPA, Table 5, printed page 12, PDF page 19](https://www.epa.gov/system/files/documents/2024-04/2019-wasted-food-report_508_opt_ec_4.23correction.pdf) |
| Land values | All 15 annual labels, 2012 through 2026, transcribed. Nominal national farm-real-estate survey estimates include buildings. The line joins annual estimates; no extra values were invented. | [USDA NASS, Land Values 2026, page 5](https://www.nass.usda.gov/Publications/Todays_Reports/reports/land0726.pdf) |
| Income and food access | Selected disjoint income groups: 39.4% below the poverty threshold and 7.9% at or above 185% of it. The 13.7% national rate is a reference, not a third income group. Middle and unknown income categories are excluded. | [USDA ERS, ERR-358, Table 2, printed page 20, PDF page 26](https://www.ers.usda.gov/media/9161/err-358.pdf?v=35619) |
| Data-centre demand | 485 TWh in 2025 is an estimate; 950 TWh in 2030 is a forecast. Two columns only. Hatched forecast differs visibly from solid estimate. The scope is all data centres worldwide, not AI alone. | [IEA, Key Questions on Energy and AI, 2026](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) |
| Forecast shift | Aggregate 50% forecast dates in two researcher surveys. Date differences of 13 and 48 years are checked arithmetically. Respondent forecasts are not observed technical progress or arrival dates. | [Grace et al., arXiv:2401.02843v3, abstract](https://arxiv.org/abs/2401.02843v3) |
| Ammonia energy | The 2021 global-average estimate is 41 GJ/t, net basis. Natural-gas and coal best-available benchmarks are 28 and 36 GJ/t. Different fill patterns distinguish estimate and benchmarks. | [IEA, Ammonia Technology Roadmap, executive summary](https://www.iea.org/reports/ammonia-technology-roadmap/executive-summary) |
| Weights memory | Six derived values use billions of parameters multiplied by bits per weight, divided by eight, yielding decimal GB. The chapter's illustrative allowance and all runtime costs are excluded. This is not measured VRAM use. | Canonical Chapter 11 equation and [llama.cpp server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) |
| Meal response | Six illustrative prompts paraphrase Chapter 18's failed-meal record. No measured service outcomes or risk probabilities are implied. Private personal details remain outside the public board. | Canonical Chapter 18, “Put the failed meal on the board” |

## Geometry and visual review

[checks.json](checks.json) records both variants' SHA-256 hashes and actual browser measurements. Every SVG was XML-parsed, written, and read back byte-for-byte. The browser was given a 4.56-inch figure width with the actual regular and semibold fonts loaded before measurement and screenshots.

All 16 final variants pass:

- Minimum effective label size: 9.23 points, exceeding the 8-point requirement.
- Figure heights: 4.79 to 6.42 inches, within the 7-inch check.
- No labels outside the SVG frame, overlapping text boxes, or path/box crossings through labels.

Five deliberately broken controls were observed failing before accepting the checks: a changed percentage total, a forecast relabeled as an estimate, duplicated overlapping text, a one-pixel label, and a line drawn through a label. These mutations existed only in memory and the test browser.

Visual review covered all eight dark screenshots and all eight light screenshots. Earlier proofs exposed a polyline crossing the first land-value label and grid lines crossing values in the ammonia and electricity charts. The final layouts relocate the land label with a leader and leave real gaps around affected bar labels. Timeline connectors are separate segments between numbered circles. These fixes also pass the stronger path-crossing detector; they do not rely on painting over hidden lines.

Forms vary with the comparison: sorted horizontal bars, an annual line plot, paired lollipops, estimate/forecast columns, paired forecast dates, estimate/benchmark columns, a ruled memory matrix, and a numbered response sequence. Direct labels, patterns, and distinct marker fills preserve the distinctions without requiring color perception alone.

This proof verifies digital geometry and source transcription, not physical printing, independent replication of the original surveys, causal inference, or forecast accuracy. Root still needs to place the figures, update the publication records, and review the generated book pages at their final dimensions.
