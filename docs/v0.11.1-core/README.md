# v0.11.1: the core cut

Surviving the Singularity, cut from 102,154 words to a 50,469-word core. Every word is verbatim from v0.11.0. Your rewrite, v0.12, is meant to start from this. It is a working manuscript, not a release: nothing in `src/lib/data/book/` changed, `book.json` still reads 0.11.0, and the site and builds are untouched.

## What you asked for

- Cut the book to about 50,000 words by finding the parts that can't be skipped, left out or deleted.
- Use the cut to validate or invalidate whether v0.11.0 could be published as is.
- Critique it as an adversary would: why it would fail, why people would hate it, what they'd complain about, weak writing, and passages that aren't in your style.
- Go back to your earliest version on Google Drive and evaluate how the book changed from there.
- You write v0.12. Nobody else does.

## The short answer

**v0.11.0 should not be published as is.** The critics rated 25 of 34 sections not publishable, 8 publishable only with fixes, and 1 (Appendix H) fine as back matter. The ideas hold up; the structure and a second, hedging voice don't.

The cut is the evidence. Half the book came out and the spine survived.

| What | Kept |
|---|---:|
| Story scenes and chapter openings | 76% |
| "Foundations" argument sections | 43% |
| Precedent blocks (17 of 24 survive, most compressed) | 40% |
| Lists | 32% |
| Tables | 12% |
| Images and captions | 0% |

The story is the book. The argument around it is where the weight is. The full case is in `CRITIQUE.md`.

## What's in this folder

| File | What it is |
|---|---|
| `Surviving-the-Singularity-v0.11.1-core.md` | **The core cut.** 50,469 words, book order, clean. Start here. |
| `core-cut-with-markers.md` | The same text with a `[CUT: n blocks, w words, first .. last]` line wherever something was removed. |
| `CRITIQUE.md` | The case against v0.11.0, and what must survive. |
| `CRITIQUE-FULL.md` | Every critic finding: block IDs, verbatim quotes with speakers, one-star complaints, weak sentences, off-voice passages, newcomer gaps. |
| `VOICE-HISTORY.md` | How your April 2024 draft became v0.11.0: what survived, what was lost, what was gained, and the 48 blocks closest to your voice (39 kept, 9 cut and listed for your call). |
| `SEAMS.md` | 196 places where the cut leaves a jump. Nothing was written to bridge them; that's yours. |
| `CUT-LEDGER.md` | Every paragraph of v0.11.0 with its ID, word count, keep or cut, and the reason. Per-section totals at the top. |
| `cut-ledger.json` | The same decisions, machine-readable. |
| `plan.json` | The final word budget per section and the reasoning behind it. |
| `plan-proposals.json` | The three competing proposals the plan merged. |
| `original-first-draft-2024-04-11.md` | Your earliest dated draft, copied verbatim from Drive. It was the voice reference. |
| `tools/` | The scripts that build, check and reproduce the cut. |

## Where the words went

| Section | v0.11.0 | Core | Kept |
|---|---:|---:|---:|
| Introduction | 3,757 | 2,422 | 64% |
| Preface | 1,404 | 521 | 37% |
| How to Use This Book | 262 | 0 | dropped |
| Chapter 0: The Demonstration | 3,813 | 2,994 | 79% |
| Part I divider | 84 | 62 | 74% |
| Chapter 1: The Event Horizon | 4,640 | 2,723 | 59% |
| Chapter 2: The Era of AGI | 3,445 | 2,131 | 62% |
| Chapter 3: The Leap to ASI | 2,529 | 1,241 | 49% |
| Chapter 4: Universal and Multiverse Apex | 2,515 | 1,269 | 50% |
| Chapter 5: The Thermodynamics of Survival | 4,114 | 2,223 | 54% |
| Part II divider | 129 | 57 | 44% |
| Chapter 6: Is the Singularity a Done Deal? | 3,449 | 2,224 | 64% |
| Chapter 7: The Battle Lines | 5,912 | 3,101 | 52% |
| Chapter 8: The Psychology of the Collapse | 4,213 | 2,527 | 60% |
| Chapter 9: Deglobalization and the Neighborhood Factory | 4,203 | 2,146 | 51% |
| Part III divider | 174 | 65 | 37% |
| Chapter 10: The "Create Over Consume" Protocol | 3,161 | 1,889 | 60% |
| Chapter 11: King and Queen of Your Own Robotic Court | 4,733 | 2,179 | 46% |
| Chapter 12: The Land Strategy | 3,775 | 2,293 | 61% |
| Chapter 13: The Shouse Protocol | 3,744 | 1,955 | 52% |
| Chapter 14: The Collapse of the Long Tail | 4,005 | 2,054 | 51% |
| Chapter 15: The Power of Reclaiming Soil | 3,158 | 1,651 | 52% |
| Chapter 16: Digital Leverage and Media Autonomy | 2,810 | 1,444 | 51% |
| Chapter 17: Tools of the Trade | 4,284 | 1,855 | 43% |
| Chapter 18: The Roadmap and the Premortem Pivot | 4,370 | 2,348 | 54% |
| Chapter 19: The Ladder | 4,266 | 2,767 | 65% |
| Conclusion: What If It All Goes Right? | 3,101 | 1,513 | 49% |
| Appendix A: Questions for a Food Baseline | 458 | 341 | 74% |
| Appendix C: Executive Reference Guide | 1,250 | 674 | 54% |
| Appendix D: The Precedent Ledger | 1,859 | 549 | 30% |
| Appendix E: The Cyberdeck | 1,774 | 0 | dropped |
| Appendix F: Glossary | 1,423 | 0 | dropped |
| Appendix G: Your First Year | 1,305 | 1,251 | 96% |
| Appendix H: Talk About It | 990 | 0 | dropped |
| **In scope** | **95,109** | **50,469** | **53%** |
| Appendix B: Works Cited | 7,072 | not cut | out of scope |

**Why these four were dropped:**
- **How to Use This Book:** it's a fourth front door, and its routing has to be rebuilt once v0.12 settles the structure.
- **Appendix E (The Cyberdeck):** it says twice that it's optional, and it repeats Chapter 5.
- **Appendix F (Glossary):** a glossary only makes sense once the text is final. It's also missing LLM.
- **Appendix H (Talk About It):** back matter that does no essential work.

## How it was made

1. **Working copies.** Every block of v0.11.0 (2,331 paragraphs, headings, lists, figures and captions) already has a permanent ID in `manuscript-index.json`. Each section was copied with its block IDs marked. The copies were checked against the source: every line covered, zero mismatches.
2. **Reading (50 agents, run 2026-10-09).**
   - Eleven readers rated every block: spine, strong, optional or cut.
   - Eleven adversarial critics read the same sections against your April 2024 draft.
   - A historian read that draft, your later 2024 Drive drafts (v.00, v.01 and the Workbook), the 2026 drafts and every version branch.
3. **Planning.** Three architects proposed word budgets from three angles: getting a newcomer from zero, moving a reader to act, and keeping the story and your voice. A fourth merged them.
4. **Cutting.** One cutter per group of sections kept or dropped whole blocks to budget. A hostile verifier then tried to break each cut. A final agent merged everything and fixed four cross-chapter breaks.
5. **Rules.**
   - Whole blocks only, verbatim.
   - No agent wrote, rewrote or bridged a word of book prose.
   - Quotes name their speaker: you, a character, a real person, or an epigraph.
   - Works Cited is out of scope.

## What was checked after the agents finished

- **Source untouched.** Nothing under `src/lib/data/book/` changed, and the working copies are byte-identical to v0.11.0.
- **Every paragraph decided.** 2,178 decisions cover every in-scope block, with none missing, duplicated or unknown.
- **Verbatim.** All 1,111 kept blocks appear word for word in v0.11.0.
- **The count.** The core totals 50,469 words, and the clean manuscript agrees.
- **Reproducible.** These tools rebuild the cut byte for byte from the v0.11.0 source and `cut-ledger.json`.
- **Critics' claims.** I checked eight of their headline claims against the source by hand. All held.
- **Drive.** A full-text search supports the historian's finding of chatbot replies in your v.01 draft.

## Things to know before you rewrite

- **Seams are real.** The cut leaves 196 jumps (`SEAMS.md`). Some are a missing transition. Some are a reference to something cut. A few are a scene beat that now arrives without its setup. They're listed after the block where a reader would trip.
- **Some defects can't be fixed by cutting.** They're yours: the en dashes in the titles of Chapters 2, 3 and 4, the phantom "tailored suits" callback in Chapter 4, broken sentences in Chapter 0 and Chapter 9, and others in `CRITIQUE-FULL.md`.
- **Images weren't judged.** Every figure and caption was dropped to keep the working text clean. That isn't a verdict on the art.
- **The order is still v0.11.0's.** The cut didn't move anything. The critics' strongest structural note is that your 2024 first line, now at the top of the Preface, belongs on page one, and that the Conclusion should end on the Bear Flag. That's a v0.12 decision.
- **Dashes.** The docs in this folder use none. Two files keep them because they must stay verbatim: the manuscript keeps the three title en dashes, and your 2024 draft keeps its original em dashes.

## How to change the cut

To put a paragraph back or take one out:

1. Find its ID in `CUT-LEDGER.md`.
2. Flip `keep` for that ID in `cut-ledger.json`.
3. Rebuild from the repo root:

```bash
export STS_CORE_WORK=/tmp/sts-core            # any scratch folder
python3 docs/v0.11.1-core/tools/make_annotated.py   # block-marked copies of v0.11.0
mkdir -p $STS_CORE_WORK/decisions && cp docs/v0.11.1-core/cut-ledger.json $STS_CORE_WORK/decisions/c00.final.json
cp docs/v0.11.1-core/plan.json $STS_CORE_WORK/
python3 docs/v0.11.1-core/tools/merge.py final    # totals per section, writes $STS_CORE_WORK/preview/ALL.md
```

`make_annotated.py` refuses to run if the block index doesn't match the text, so run it at the v0.11.0 source.
