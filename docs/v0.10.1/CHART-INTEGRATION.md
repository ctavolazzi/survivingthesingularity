# v0.10.1 chart integration

Integrated 2026-09-27. Eight new figure/caption pairs were inserted in the canonical manuscript at the exact anchors in [chart-placements.json](chart-placements.json). The ledger now records `status: inserted` and image/caption line numbers. Existing narrative, author positions, equations, tables, and figures were preserved. Other v0.10.1 art can shift the recorded line numbers; exact anchor text remains the durable locator.

| Canonical file | Addition | Position |
| --- | --- | --- |
| `03-chapter1.md` | Forecast shift | After the Table 3 caption |
| `07-chapter5.md` | Data-centre electricity demand | Before the paragraph beginning “You burn roughly 2,000 to 2,500 kilocalories” |
| `08-chapter6.md` | Income and food access | After the paragraph beginning “On the sell side” |
| `11-chapter9.md` | Ammonia energy intensity | After the industrial Haber-Bosch energy paragraph |
| `13-chapter11.md` | Weights-only memory matrix | After the definition of the memory equation's variables |
| `14-chapter12.md` | Farm-real-estate values | After the paragraph beginning “That's one route” |
| `16-chapter14.md` | Wasted-food management pathways | After “Turn a leak in the long system into a local reserve” |
| `20-chapter18.md` | Failed-meal response worksheet | After “Test a response before depending on it” |

Appendix B gained **Visual source notes for v0.10.1** with three previously absent references: EPA's corrected 2019 Wasted Food Report, USDA NASS Land Values 2026 Summary, and USDA ERS ERR-358. Existing entries already cover Grace and colleagues' forecast study, both IEA reports, and llama.cpp documentation, so those references were not duplicated. The worksheet comes from Chapter 18's existing record.

The captions retain the evidence types and limits. EPA estimates include inedible material; the combined bio-based-materials/biochemical-processing category is preserved. The source ledger retains the published one-ton rounding discrepancy between EPA's rows and total. Land prices are nominal survey estimates including buildings, not local asking prices. Food-insecurity income groups are selected and non-overlapping; association does not establish causation. Data-centre demand distinguishes the 2025 estimate from the 2030 forecast and includes all data centres. Researcher forecasts are not arrival dates. Ammonia benchmarks differ from the global-average estimate. Memory values are derived weights-only quantities, excluding runtime and the chapter's illustrative allowance. The meal worksheet illustrates a process without claiming measured service performance.

Integration checks read every changed chapter back from disk and confirmed exactly one full figure/caption block, exactly one image reference, an unchanged unique anchor, and the requested adjacency for all eight placements. Duplicate, missing, and misplaced figure blocks were each rejected by deliberately broken in-memory controls. Appendix B's three new source URLs and its new heading each occur once. The affected manuscript files pass `git diff --check`. [chart-proof/REVIEW.md](chart-proof/REVIEW.md) documents source verification, 16 rendered variants, geometry checks, and deliberately failing controls. SVG hashes remain in [chart-proof/checks.json](chart-proof/checks.json).

This task did not modify `book.json`, art catalogs, credits, rights records, baselines, or `visuals.json`. Publication integration and final page proofs remain with the root task. No commit was made.
