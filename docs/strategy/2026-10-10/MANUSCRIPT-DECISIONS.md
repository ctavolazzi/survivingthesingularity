# Manuscript decisions: a concrete starting packet

Prepared 2026-10-10 from local Git refs and source records. This packet proposes assembly and review work. It changes no manuscript, release, or author wording. CT writes v0.12.

**Recommendation:** use PR24's v0.11.0 source as the technical baseline, bring across PR26's editorial documents as working aids, and carry PR27's requested Author's Foreword forward without replacing the newer manuscript with its older branch. Test a reordered opening and one Chapter 9 pilot before expanding the rewrite.

## What is already settled

| Decision to preserve | Evidence and consequence |
|---|---|
| Title is *Surviving the Singularity*; v0.11.0 subtitle is *We Don't Have to Live Like This*. | [Canonical manifest](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/src/lib/data/book/book.json#L2). Do not reopen naming as a prerequisite. |
| Survival means keeping people fed, housed, and cared for, with influence over ownership and benefits. | [Introduction line 33](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/src/lib/data/book/02-introduction.md#L33), block `sts.introduction.b0163`. This is implemented, including in the core cut. |
| Ownership, public participation and solarpunk belong to the v0.11.0 editorial direction. | [Edition notes](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/docs/v0.11.0/EDITION-NOTES.md#L5). Preserve the direction and source work when preparing the rewrite. |
| CT requested the Author's Foreword after Grow Tech Fest, with five dictated passages preserved exactly. | [Foreword scope](https://github.com/ctavolazzi/survivingthesingularity/blob/06097b92df38e8a36bebf2d9d0ec0414c2991a43/V0.7.5-SCOPE.md#L15). Carry it forward; this packet does not ask whether to have a foreword. Its existing placement is before the Introduction. |
| CT writes v0.12. | [Core-cut instructions](https://github.com/ctavolazzi/survivingthesingularity/blob/e797fa1500a4bb9864482ced02bf43c771523dfa/docs/v0.11.1-core/README.md#L5). Agents can assemble comparisons, find evidence and verify continuity. They do not supply replacement prose or bridge the seams. |
| Canonical Markdown plus `book.json` controls the book. | [Source-of-truth rules](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/README.md#L217). A core document under `docs/` does not become the production manuscript by being renamed. |

The core cut is an editorial proposal, including where it removes recent author-directed material. Its ledger marks `sts.conclusion.b0081` (the revised moral call) and solarpunk blocks `b0130`, `b0135`, `b0131`, `b0132`, and `b0133` for removal. It keeps `b0134`. **Do not apply those removals silently.** Keep the accepted v0.11.0 source available in the author packet; CT can rewrite it as part of v0.12. [Decision ledger](https://github.com/ctavolazzi/survivingthesingularity/blob/e797fa1500a4bb9864482ced02bf43c771523dfa/docs/v0.11.1-core/cut-ledger.json).

## Baseline and inclusion list

| Source | Exact reference | Use |
|---|---|---|
| PR24 release integration | `4377394471357ce5660a0cf62d2eeed3e13d8e77` | Base for a future integration checkout. Keep its 35 canonical sections and publication tooling. |
| PR26 core-cut work | `e797fa1500a4bb9864482ced02bf43c771523dfa` | Import `docs/v0.11.1-core/` as editorial material. Use its block choices provisionally, not as approved deletions. |
| PR27 Author's Foreword | `06097b92df38e8a36bebf2d9d0ec0414c2991a43` | Transfer `src/lib/data/book/00-authors-foreword.md` and its provenance/scope. Register it in the selected manifest and rebuild the index when integration is authorized. Preserve the five dictated passages. |
| Current main observed during this packet | `1e9c0f4b51a642148ab3ee0bfcdb5aabe777be48` | Contains a newer homepage change, but book metadata remains v0.7.4 with 30 sections. Preserve/reconcile its homepage work separately from manuscript selection. |

Read-only comparison found PR24 and PR26 have the **same complete `src/lib/data/book/` tree**, `24f3fae53e2f210104a68037876f4254de1c84cb`. That gives the cut's block IDs an exact common source. Main's new commit changed only `src/routes/+page.svelte`; it did not incorporate the foreword or v0.11.0 manuscript.

Exclude from automatic manuscript integration:

- PR27's `book.json` and generated index as whole-file replacements. Those describe its older 31-section line and would discard newer sections/metadata.
- PR21 chapter insertions and PR23 editorial proposals. They require independent inclusion decisions; they are not inherited merely because another branch is merged.
- Generated manuscripts, PDFs and EPUBs as editing inputs. Rebuild them from canonical source after an accepted change.
- The core's universal image removal as an art decision. Its README says images were not judged.
- A new public release number or publication claim. Selecting a working baseline does not publish it.

**Release timing remains a real choice:** an interim v0.11 edition can proceed after its selected source, delivery, evidence and relevant production gates are satisfied. It need not wait for the full v0.12 rewrite. Alternatively, hold the next book edition until CT's rewrite is ready. The first route costs a second integration/proof cycle; the second delays delivery of newer book material. Website correctness can improve under either route.

## Opening: two concrete reader-test candidates

Both candidates preserve the foreword first and its dictated text. They use existing prose only. The proposed core selections remain reversible, and no new transition is supplied.

| Candidate | Reading sequence | Cost and what it tests |
|---|---|---|
| **A: retain the existing relative order** | Full Author's Foreword, core Introduction, core Preface, core Chapter 0, Part I. | Smallest order change. Tests whether shortened existing sections plus CT's new foreword make the purpose clear. The restored 2024 opening still comes after the Introduction. |
| **B: bring the original opening forward, recommended test candidate** | Full Author's Foreword, core Preface, core Introduction, core Chapter 0, Part I. | Moves two existing sections without rewriting. CT's original opening and horse parable arrive immediately after the foreword. The explicit title definition arrives later than in A. Check whether this creates a clearer invitation or delays essential context. |

Exact sources: [Foreword](https://github.com/ctavolazzi/survivingthesingularity/blob/06097b92df38e8a36bebf2d9d0ec0414c2991a43/src/lib/data/book/00-authors-foreword.md), [core manuscript](https://github.com/ctavolazzi/survivingthesingularity/blob/e797fa1500a4bb9864482ced02bf43c771523dfa/docs/v0.11.1-core/Surviving-the-Singularity-v0.11.1-core.md), [original section order](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/src/lib/data/book/book.json#L8).

Protect `sts.preface.b0039`, the original opening; `sts.preface.b0072`, the horse passage; and `sts.introduction.b0163`, the title definition. Core documentation counts 521 words for its Preface, 2,422 for Introduction and 2,994 for Chapter 0. The foreword is additional material outside that cut, so 50,469 words is not the combined candidate's length. These are source-document counts, not a new measurement of an assembled edition.

For the test, omit “How to Use This Book” as proposed by the cut and keep navigation outside the reading passage. Its permanent removal is not implied. Ask readers what the book promises and where they first understand the title; do not tell them which candidate is supposed to win. These sessions can refine the opening decision instead of waiting for a final decision before learning anything.

## Voice and ending: bounded author choices

**Voice baseline:** keep the existing three registers: direct first-person Argument, patient third-person Narrative, and specific Field Manual instruction. Preserve the rule against explaining a scene after it lands. [Voice guide](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/src/lib/data/book/VOICE-GUIDE.md#L14).

**Voice choice A, recommended:** CT rewrites one complete pilot chapter while agents provide side-by-side source, cut decisions and evidence. This gives CT control over cadence and creates an actual sample for later chapters. Cost: one focused authoring pass plus review.

**Voice choice B:** CT first rules on the nine author-voice blocks omitted from the core. Cost: a smaller decision session, but it cannot establish how a whole rewritten chapter sounds. Do not restore every marked passage automatically; some contain factual or contextual problems. Begin with `sts.introduction.b0094`, which the [voice history](https://github.com/ctavolazzi/survivingthesingularity/blob/e797fa1500a4bb9864482ced02bf43c771523dfa/docs/v0.11.1-core/VOICE-HISTORY.md#L112) highlights and the ledger cuts for repetition and attribution concerns.

**Ending choice A, recommended baseline:** retain the accepted v0.11.0 order for now: moral mandate and revised call, P-24, Bear Flag coda. Keep `sts.conclusion.b0019`, “You're holding it.”, last. This preserves existing author work and creates a clean comparison before any structural move.

**Ending choice B, test only:** move the entire existing P-24 block before “The moral mandate,” then run mandate directly into Bear Flag. No new prose and no removal of the accepted moral call. Cost: cross-reference and transition review; benefit to test: one emotional ending without the precedent separating call and coda. [Current conclusion](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/src/lib/data/book/21-conclusion.md#L70).

The foreword's outstanding primary-source checks, two flagged wording issues and sign-off are bounded follow-ups already recorded in its [scope](https://github.com/ctavolazzi/survivingthesingularity/blob/06097b92df38e8a36bebf2d9d0ec0414c2991a43/V0.7.5-SCOPE.md#L50). Resolve factual support before presenting wording choices. The later perceived-value discussion is recorded as deferred; this packet does not invent that passage.

## Recommended pilot: Chapter 9

Use `src/lib/data/book/11-chapter9.md`, “Deglobalization and the Neighborhood Factory.” The cut reduces its documented 4,203 words to 2,146 while retaining a concrete manufacturing scene, repair and ownership choices, food provision and historical precedent. It exposes the book's main editing problems in one bounded chapter. It is a representative editing test, not a request to draft an entire technical manual.

Prepare the pilot from these existing pieces:

| Material | Block or source | Treatment |
|---|---|---|
| Elegant first design and Marta's response | `sts.chapter9.b0010`, `b0011` | Preserve the scene function and callbacks to Chapter 15 and Conclusion; CT repairs the flagged sentence. |
| Supplier test and repairable redesign | `b0177`, `b0178` | Preserve the 11/1/0 lesson. Check whether the hardware choice supports it; the seam report's criticism is a review hypothesis, not new research conducted here. |
| Registration, review and the open county question | `b0179` through `b0184`, in source order, including intervening `b0020` and `b0021` | Preserve the complete scene and its concrete responsibilities, not a numerical slice of IDs. Compare with `b0162`, whose permission claim needs to agree with the scene. |
| Concrete factory image from the cut summary | `b0176` | Show CT the omitted source passage. CT decides whether to reuse its image in the body; the agent does not write the bridge. |
| Food benefit and who receives savings | `b0174`, `b0175` | Repair references to the five-household trial whose setup was removed. Either restore sufficient existing setup or let CT rewrite the reference. |
| Chapter-wide joins and callbacks | Chapter 9 entries in `SEAMS.md` | Track each against the pilot; preserve callbacks when tightening prose. |

Sources: [canonical chapter](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/src/lib/data/book/11-chapter9.md), [seams](https://github.com/ctavolazzi/survivingthesingularity/blob/e797fa1500a4bb9864482ced02bf43c771523dfa/docs/v0.11.1-core/SEAMS.md), [block index](https://github.com/ctavolazzi/survivingthesingularity/blob/4377394471357ce5660a0cf62d2eeed3e13d8e77/src/lib/data/book/manuscript-index.json).

Pilot is complete when CT accepts its voice; every Chapter 9 seam is resolved or deliberately retained with a reason; technical claims have an explicit evidence status; callbacks remain intact; and trial readers can explain both the repair lesson and why a working controller does not by itself ensure dinner. Mechanical checks establish preservation and consistency. Reader sessions establish what those readers understood. Neither proves market demand.

## Next work that does not require new author prose

Prepare reversible A/B reading packets from the pinned source, collect primary evidence for the foreword, and assemble the Chapter 9 source/cut/seam comparison. Preserve author-requested content beside all proposed cuts. Record CT's decisions before changing canonical source. A later implementation must reconcile new main commits, update `book.json` deliberately, regenerate the index, and prove retained IDs still point to their intended content.
