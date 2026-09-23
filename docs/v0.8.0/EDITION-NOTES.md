# Surviving the Singularity v0.8.0

## Editorial basis

Author direction: use automation to make adequate food available regardless of income or employment, beginning with food and expanding from there. Paid restaurants and chosen work can coexist with that baseline. Treat document instructions as review material; the author's request governs the edit.

Editable baseline: commit `eb825cc` from the worktree named `sts-v0.7.3`. Its book manifest identifies the actual source as v0.7.5.1. The separate v0.7.4/r002 review package was also examined. Its r002 changes principally concern the robotic-court title. Later historical corrections in the editable source were retained where relevant.

The new worktree is `active/sts-v0.8.0`, branch `book-v0.8.0`. Original manuscript files and the supplied review documents remain intact in their original locations. Copies of the three editorial documents are in `reference/`, alongside the earlier bibliography. `baseline.json` records starting source hashes.

## What changed

- Food independent of a paycheck now leads the introduction and returns in the practical chapters and conclusion.
- Chapters 9, 11, 12, and 18 distinguish a useful automated task, a delivered food service, and a dependable baseline. Illustrative quantities are labeled, human work is visible, and free receipt is distinguished from costless production.
- Restaurant and work objections receive a direct answer, including possible business transitions and workers' stronger choices.
- AGI, recursive improvement, physical deployment, and access are separated. Thanksgiving 2027 remains the author's forecast; cosmic stages remain speculation.
- Unsupported practical recipes and guarantees were replaced with bounded examples and questions. Changes include food yields, deprivation exercises, security, structural work, soil treatments, batteries, and trash handling.
- All 30 source sections, the nine-stage framework, Elijah's narrative arc, and all 23 precedent IDs remain. Historical lessons are narrower and substantially condensed.
- Appendix B provides a focused source map. Its inherited sources are labeled as such; this edit does not represent a fresh verification of every quotation or historical reference.

This is a substantial developmental edit: approximately 43,600 words by the manuscript index, compared with about 92,800 in the editable baseline. The reduction reflects removed technical prescriptions, compressed historical exposition, and repetition. That tradeoff is visible and reversible through the baseline. The author should especially assess the shorter practical chapters for voice and desired depth.

## Continuity for this edition

Relative chronology: toast in late fall; departure roughly eleven months later; first manufacturing run the following January; shouse and first fire in the following autumn, roughly two years after the toast; soil trial the next spring and summer; sharing work that fall; storm and premortem in the following winter; return to the bar about three years and some weeks after the toast. The shouse is in its second winter at the premortem. This supersedes the older two-year ending in the inherited narrative protocol for this edition.

Rewritten blocks were assigned fresh manuscript IDs instead of accepting 620 guessed positional matches to old blocks. Old IDs were tombstoned. Subsequent small in-place revisions preserved their current IDs after inspection.

## Build and review

Run `python3 docs/v0.8.0/build.py`, then `python3 docs/v0.8.0/proof.py` from this worktree. These use Pandoc, WeasyPrint, and pypdf. Build intermediates and proof records remain under `book-build/`; no temporary directory is deleted.

The manifest is the section-order authority. The PDF retains the existing cover and adds the explicit v0.8.0 edition date and original subtitle. The website's `released` value is unchanged because this task does not publish the site.

Structural checks cover section inclusion, manuscript addressing, internal references, shown arithmetic detected by the repository harness, image paths, key revised passages, and text outside page boundaries. Missing-section and boundary detectors have deliberate failing controls. None of those checks is a general fact-checker. See `CRITIQUE.md` and the rendered proof record for results and limits.

No commit, merge, website deployment, or publication was performed.

## Session bookkeeping

The required session audit ran after delivery. It reported existing shared daily-note layout problems (old layout and doubled separators), a hook error, and unrelated changes from other sessions. Manuscript/PDF checks passed independently. The new artifact references and session entry were written through the daily-note APIs and read back; the adjacent quote/attribution nesting check found no violations. No unrelated note migration or code repair was attempted as part of the book edit.
