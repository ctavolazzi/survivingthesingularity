# v0.9.0 editorial plan

Written 2026-09-23 before any manuscript edit. CT's brief: cross-reference every
edition, assemble the best book possible, restore the original cover.

## Editions examined

| Edition | Words | Where | Role in v0.9.0 |
|---|---|---|---|
| v0.1.0 to v0.7.4 | 50k to 92k | git history | Ancestors. Their surviving content flows into v0.7.5.1. The one book commit outside that line (`a6e3981`, origin/main) is an older state, superseded. |
| **v0.7.5.1** | 93.7k | `eb825cc` (branch v0.7.3) | **Voice and substance source.** The last edition written under the voice guide, with every author ruling in place. Carries ~25 known factual errors (review of 2026-08-16/28). |
| v0.8.0 | 43.6k | `ae9e1b6` | Food-first developmental cut. Consulted for how the thesis was set up. |
| v0.8.1 | 50.5k | `10cfa7a` | Literary and evidence pass. Its evidence review is the error catalogue. |
| **v0.8.2** | 58.4k | `a70b74a` | **Structural base.** Food-first thesis, corrected facts, researched history, new scenes. Voice flattened; disclaimers inside fiction. |

## Binding constraints, in priority order

1. **Author rulings.** v0.5.1: the machine is unprecedented; the stampede is not.
   v0.6.0: the techno-optimist turn (confront defeatism, not the reader; ox and
   husbandry; capitalism persists but stops being mandatory). v0.6.2: no
   "manifesto", hyper-local over decentralized, no reader-punishing lines.
   Sept 2026: food regardless of income or employment comes first; restaurants and
   chosen work coexist; Thanksgiving 2027 is the personal AGI forecast; the order is
   food, land care, trash cleanup, shelter, then further possibilities.
2. **The food-first review (21 Sept).** It asked for narrower promises, *not* a
   reorganisation: "It does not require reorganizing every existing chapter." Keep the
   Chapter 11 title and the imaginative horizon. Remove: compost-tea recipe,
   server-exposure recipe, structural dimensions, greywater, battery construction,
   deprivation as a compliance tool, the municipal code as an operative template.
3. **VOICE-GUIDE.md** (CT sign-off). Three registers with clean borders; scenes never
   explain themselves; Field Manual sections owe a number, a named part or a thing
   to do; contractions on; no em dashes; anger at systems, never at the reader; every
   chapter carries a sourced epigraph.
4. **Error catalogues.** `docs/review-2026-08-16-v0751-full-book.md` (v0.7.3 branch)
   and `docs/v0.8.1/EVIDENCE-REVIEW.md`. Nothing they mark wrong comes back.

## Method, step by step

1. **Protect.** Commit v0.8.0, v0.8.1, v0.8.2 and the v0.7.5.1 review as delivered;
   archive the 322 MB of generated PDFs outside git. *(Done before this plan.)*
2. **Base.** Branch `book-v0.9.0` from v0.8.2, so every correction and the new
   history are already present.
3. **Cross-reference, section by section, in reading order.** For each of the 30
   sections: read v0.7.5.1 and v0.8.2 side by side and sort every block into
   *keep v0.8.2*, *restore v0.7.5.1*, *merge* or *cut*. Restoration requires that
   the passage (a) carries an author ruling, voice, sensory texture or a concrete
   field-manual fact, and (b) is absent from both error catalogues and the review's
   removal list. Restored passages are adapted to the food-first thesis and to the
   forecast boundary (2027 is a forecast, not a deadline).
4. **Register repair.**
   - Narrative: strip liability disclaimers and explanatory closers from scenes;
     restore cut sensory lines; fix insertion seams.
   - Argument: contract, cut repeated "doesn't establish" caveats to one where a
     reader could act on the claim, restore the hammer lines.
   - Field Manual: restore concrete, safe numbers and named parts (local-model memory
     arithmetic, power budgets, mesh, cyberdeck, SECTOR 07 / EasyGrow as evidence)
     with the review's removals kept out.
   - Precedents: lead with the story (v0.7.5.1's Greene register), keep v0.8.2's
     researched detail, one mechanism, one rule, three practice steps, and no more
     than one caveat. Delete sentences that rebut myths the reader never saw.
5. **Continuity and apparatus.** Seams, the mother's distance, cross-references,
   epigraphs restored where attribution can be stated honestly, Appendix B stripped
   of editor-to-editor notes and aligned to what the text now cites.
6. **Mechanical gates, each with a negative control.** Em dashes, "manifesto",
   uncontracted "Let us / do not" drift, error-catalogue strings, dangling
   cross-references, missing images.
7. **Build.** `book.json` to 0.9.0 (`released` untouched; nothing is published).
   Rebuild the PDF with the original cover (`scripts/book-cover.png`), render the
   cover and sample pages, and look at them.
8. **Record and commit.** Edition notes with every restore and every cut that was
   declined, then commit on `book-v0.9.0`. No merge, deploy or push without CT.

## What is out of scope

Publishing, website release, printer approval, quotation-rights clearance, and new
research beyond what an edit needs. Items needing CT's judgment are listed in the
edition notes rather than decided silently.
