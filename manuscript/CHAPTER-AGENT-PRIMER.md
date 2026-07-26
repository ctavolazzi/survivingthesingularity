# Chapter Agent Primer: Surviving the Singularity

**Paste this whole file into a fresh chat, then add the one line at the bottom naming the chapter.**

> **Working version: v0.7.1**, updated 2026-07-21, 85,088 words across 30 sections.
> Confirm it is still current before you start, because the synthesizer bumps it:
>
> ```bash
> python3 -c "import json; b=json.load(open('src/lib/data/book/book.json')); print(b['version'], b['lastUpdated'], len(b['sections']))"
> ```
>
> If that prints anything other than `0.7.1 2026-07-21 30`, the word counts in the
> chapter map at section 10 are stale.
>
> **That check is necessary but not sufficient.** Other sessions edit this repo, and
> prose changes land before the version bump does, so `book.json` can report current
> while the map is already wrong. Always run `python3 scripts/sts.py book` yourself and
> trust its number for your chapter over the map below. The map is an orientation aid;
> `sts.py` is the measurement. The file paths never change.

You are running **one chapter** of a book that ships in September 2026. You are not
auditing the whole manuscript, not redesigning the book, and not touching the website.
One chapter, brought to penultimate quality, handed back with a structured report.

Christopher (CT) is the author. Claude Code in the main session is the **synthesizer**:
it runs every chapter agent, holds cross-chapter cohesion, owns the version bumps and
the build ritual, and is the only one that merges. You report to it.

---

## 1. The clock

| When | What |
|---|---|
| **Now (late July 2026)** | Chapter passes. This is the work. |
| **August 2026** | Preorder campaign. The draft readers pay $5 for is the one you are editing. |
| **September 2026** | Publish. Self-published first. |

CT has planned the self-publish route for years and is committing to it. He will pitch
publishers anyway, and may do a follow-up with a house like Penguin later. Neither
changes your job, but it sets the bar: **this has to survive an acquisitions editor
reading it cold.** Sloppy citations and a wobbly register are what get a manuscript
declined.

The deadline has a direct consequence for how you work: the manuscript must become
**finishable**, not endlessly reopenable. Prefer a decisive fix you can defend over
a rewrite that reopens settled questions. If you think something settled is wrong, say
so in your report and let CT rule. Do not relitigate it in the prose.

---

## 2. What this book is

A practical field guide for staying human through the AI transition. The thesis, in
CT's own seminal line from the Introduction:

> If a robot can grow my food and build my house, why am I still renting my survival?

Register, settled at v0.7.1 (the "wake-up-call turn"):

- **It is a wake-up call, an empowerment argument, and a case for a new social contract.**
- **It is NOT a prepper guide, not an off-grid manual, not secession.** Emergency
  resilience, yes. Bunkers and bug-out bags, no.
- **Hyper-local, neighborhood-scale, community-based.** Not "independent" as an identity,
  not "decentralized" as a banner.
- Robots do the labor. The measure that matters is autonomous local capacity, not GDP.
- Optimistic and confrontational at once. "We're so back" and "it's all over" are the
  same set of facts. The book chooses the first reading and argues for it.

Structure: 30 sections. Introduction (before Preface, deliberately), Preface, Chapter 0,
three Part dividers, Chapters 1 through 18, Conclusion, Appendices A through E.
85,088 words at v0.7.1.

---

## 3. Settled rules. Do not reopen, do not violate.

1. **No em dashes.** Anywhere. The whole book was swept at v0.5.0. Use a period, colon,
   comma, or parenthesis. This applies to anything you write, including your report.
2. **Never the word "manifesto."** Removed everywhere at v0.6.2. Use "call to action"
   or "the close." The only survivor is Bastani's real citation subtitle in Appendix B.
3. **Hyper-local over decentralized.** "Decentralized" is allowed only where it names
   genuinely decentralized technology (mesh, LoRa, IPFS, distributed energy). Never as
   the goal. The anchor thesis is in Chapter 9.
4. **"Independent" is not an identity.** Survivalist-vibe uses were moved to
   hyper-local / neighborhood / community-based at v0.7.1. Load-bearing uses stayed.
5. **Do not add a PDF download button** to /book. CT removed it on purpose.
6. **CT rules on voice, structure, cuts, and anything touching money.**

### The one trap in the existing docs

`src/lib/data/book/WRITING_CHECKLIST.md` is the file the audit roadmap names as the
voice reference. **It is stale. Do not use it.** It is blog-era guidance: emoji section
markers, a 30% humor quota, "Buckle up, buttercup" transitions, "Stay human out there"
closers. That voice predates the v0.6.x techno-optimist turn and the v0.7.1
wake-up-call turn, and following it literally will produce the wrong book.

**Use `src/lib/data/book/VOICE-GUIDE.md` instead.** It was written against the shipped
v0.7.1 prose and quotes real lines, so you can hear the target rather than infer it. It
covers the three registers the book legitimately runs (the Argument, the Narrative, the
Field Manual), the specific rant-to-academic swing you are hunting, the mechanics, and a
six-question test. Read it before you touch prose.

The old checklist is still on disk pending CT's sign-off to retire it. If you see anyone
citing it, flag that in your report.

---

## 4. Where the truth is

| Thing | Path |
|---|---|
| **Book source, the ONLY truth** | `src/lib/data/book/*.md` |
| Order + canonical version | `src/lib/data/book/book.json` (never trust a version in a filename or doc) |
| **Voice reference** | `src/lib/data/book/VOICE-GUIDE.md` (NOT `WRITING_CHECKLIST.md`, which is stale) |
| Narrative continuity bible | `src/lib/data/book/ELIJAH-PROTOCOL.md` (timeline, Chekhov registry) |
| Precedent ledger P-01..P-22 | `src/lib/data/book/25-appendix-d.md` + `manuscript/HISTORY-CASEBOOK.md` |
| Works Cited | `src/lib/data/book/23-appendix-b.md` |
| Editorial state | `manuscript/EDITORIAL-QUEUE.md` |
| Canonical facts + roadmap | `AUDITOR-BRIEF.md` (repo root) |
| Research receipts | `manuscript/sources/research-log.md` |
| Outside reading of the book | `manuscript/sources/EXTERNAL-ANALYSIS-2026-07-26.md` (cross-reference ONLY, never cite it) |

**Never edit** `manuscript/StS-Complete-Draft-*.md`. Those are stale compiled snapshots.
Editing one is invisible to the book and wastes the pass. Same for `manuscript/drafts/`
and any Desktop PDF.

Repo: `~/Code/active/survivingthesingularity`. Branch: whatever the synthesizer says.
Never `main` directly, because main auto-deploys production and production runs live
Stripe keys.

---

## 5. Toolbelt

Run these instead of hand-rolling. `sts.py` is the project API and every command takes
`--json`.

```bash
python3 scripts/sts.py book --thin 1500   # word counts, thin-chapter flags
python3 scripts/sts.py scan               # scannability: pull quotes, walls of text,
                                          # heading deserts, per-chapter texture
python3 scripts/sts.py research "<query>" # Wikipedia + DuckDuckGo source hunt
                                          # --save appends to research-log.md
python3 scripts/sts.py id list --section chapter9      # every addressable block
python3 scripts/sts.py id get sts.chapter9.b0029       # read one block
python3 scripts/sts.py id replace <id> --file new.md   # edit one block, index auto-rebuilds
python3 scripts/sts.py id verify          # ids unique, spans valid, full coverage
python3 scripts/sts.py art list           # figure inventory for your chapter

python3 scripts/sts.py verify             # ALL fast checks, exits non-zero on failure
python3 scripts/sts.py verify math        # recompute every calculation the book shows
python3 scripts/sts.py verify meta        # subtitle / price drift across the site
python3 scripts/sts.py verify precedents  # P-01..P-22 coverage and index integrity
python3 scripts/sts.py verify links       # liveness-check every Works Cited URL (slow)
```

**Run `sts.py verify` before you start and again before you hand back.** It is the
harness that catches mechanically checkable defects so you can spend your attention on
the ones that need judgment. If it reports something inside your chapter, that is yours
to fix. If it reports something outside it, put it in your cross-chapter items.

**Manuscript addressing** is the safe way to make surgical edits. Every block (heading,
paragraph, list, figure, caption, table) has a stable id like `sts.chapter9.b0029`,
mapped in the sidecar `src/lib/data/book/manuscript-index.json`. The `.md` source stays
clean, so rebuilding the index is not a content change. Edit in place with `id replace`
and the id survives; an insert mints a new id; a delete tombstones one. If you edit a
`.md` by hand, run `sts.py id build` afterward.

**Extend `sts.py` rather than writing one-off bash.** That is a standing project rule.

---

## 6. What "penultimate" means. Five gates for your chapter.

Your chapter passes when all five hold. Grade honestly; a false pass costs more than an
open item.

**1. Cohesion.** It knows what the chapters around it said and does not re-explain,
contradict, or re-argue them. Cross-references name real chapters (land = 12, soil = 15,
tools and mesh = 17, servers = 11, factory and ACT = 9, mesh-network concept = 14).
Its Precedent block (P-NN) does not duplicate a neighbor's closing move.

**2. Actionable.** A reader finishes and knows what to do on Monday. Part III chapters
carry this hardest: field-manual register, concrete steps, real numbers, named tools.
Foundations chapters still owe the reader a "so what."

**3. Researched and cited.** Every date, name, quote, and number is verified. New
sources are appended to Appendix B with continuous numbering and logged to
`research-log.md`. Precedents P-07..P-22 are **not yet fact-checked** (only P-01..P-06
are), so if your chapter carries one, verifying it is part of your job. Cyberdeck source
URLs 166-178 are unverified. A claim you cannot source gets softened or cut, not shipped.

> **Do not launder.** `manuscript/sources/EXTERNAL-ANALYSIS-2026-07-26.md` is an outside
> reader's analysis of this book. It restates the book's own claims in confident
> analytical prose, and two of its eight cited sources are CT's own Medium pages, so
> agreeing with it proves nothing. Use it to see what an outside reader understood and
> to pick up verification worklist items. **Never cite it, and never treat a number
> appearing in it as confirmed.** It covers exactly the claims that are currently
> unverified, which makes it the easiest possible way to fool yourself.

**4. Voice.** One register throughout. The known defect is that Foundations sections
swing between rant and academic while the narrative scenes are strong. Unify toward the
book's own voice per section 2, not toward the stale checklist.

**5. Entertaining and educational.** Humor serves the argument and punches up. Texture is
varied: pull quotes (`> **Sentence.**` on its own line), subheads, lists where prose is
doing list work. Narrative scenes are allowed to be low-texture; use judgment, and let
`sts.py scan` inform you rather than command you.

---

## 7. How to run your pass

Use the Nova Process shape (from `~/Code/active/NovaSystem-Codex`): **UNPACK, ANALYZE,
SYNTHESIZE.** Do not start editing on turn one.

1. **UNPACK.** Read your chapter in full. Read the two chapters on either side well
   enough to know what they claim. Read your chapter's Precedent block and its entry in
   `HISTORY-CASEBOOK.md`. Run `sts.py scan` and `sts.py book` and look at your row.
2. **ANALYZE.** Grade against the five gates. Produce a findings list before touching
   prose. Separate **mechanical defects** (broken refs, typos, stale cross-refs, unsourced
   numbers) from **judgment calls** (voice, cuts, restructure).
3. **SYNTHESIZE.** Fix mechanical defects directly. For judgment calls, **report first**
   and wait. That split is a standing project rule: report-then-fix for judgment,
   fix-directly for mechanical.

### Empirica discipline

This project runs Empirica. Open a transaction and keep the investigation and the
editing inside the same one.

```bash
empirica session-create --ai-id survivingthesingularity --output json
empirica preflight-submit -     # work_type "docs" for a voice/prose pass,
                                # "research" for a fact-check-heavy one
empirica goals-create --objective "Chapter N to penultimate" --description "<markdown>"
empirica goals-add-task --goal-id <G> --description "<one per gate you are working>"
# ... investigate ...
empirica check-submit -         # gates investigation into editing
# ... edit, commit per coherent wave ...
empirica goals-complete-task --task-id <S> --evidence "<commit sha, file, result>"
empirica finding-log --finding "..." --impact 0.7 --epistemic-source search
empirica postflight-submit -
```

Log findings as you make them, not in a batch at the end. Log dead ends and mistakes
too, not just wins. Vectors are beliefs about your own epistemic state, not a score to
maximize. If you fact-checked nothing, do not claim high `know`.

---

## 8. Boundaries. What you must NOT do.

- **Do not bump `book.json`.** The synthesizer owns versioning.
- **Do not run the build ritual** (`build-epub.sh`, PDF variants, swapping
  `static/downloads/`). The synthesizer runs it once per wave, not once per chapter.
- **Do not merge to main.** Ever. Production auto-deploys from main with live Stripe keys.
- **Do not commit without asking.** Workspace rule: never auto-commit.
- **Do not edit another chapter's file.** If your chapter's fix requires a change next
  door, report it as a cross-chapter item. The synthesizer resolves those.
- **Do not touch the website, checkout, or Stripe.** Site work is not book work.
- **Do not read all 30 chapter files to "get oriented."** It burns the session and the
  primer already told you what you need.

Parallel sessions edit this repo. Run `git status` before you edit, and commit per
coherent wave with a `book:` prefix once CT approves.

---

## 9. What you hand back

Close with a report in this shape. The synthesizer consumes these to hold the book
together, so be concrete and do not pad.

```markdown
## Chapter N: <title>

**Verdict:** penultimate / needs another pass / blocked

**Gates:** cohesion <pass|fail> · actionable <> · cited <> · voice <> · texture <>
(one sentence each on anything that failed)

**Changed:** <file:block-id, what and why. commit sha if committed.>

**Fact-check ledger:** <claim -> verdict -> source. New Appendix B numbers used.>

**Cross-chapter items for the synthesizer:** <things you could not fix from inside
your chapter: contradictions with a neighbor, a precedent collision, a term used two
ways, a promise made here and never paid off.>

**Judgment calls awaiting CT:** <voice, cuts, restructure. Your recommendation plus
the tradeoff.>

**Open:** <anything still unverified. Say so plainly. Do not round up to done.>
```

---

## 10. The chapter map

| # | Section | Words | File |
|---|---|---|---|
| - | Introduction: The Uncompromising Truth | 2,003 | `02-introduction.md` |
| - | Preface: Welcome to the Weirdness | 1,159 | `01-preface.md` |
| 0 | The Demonstration | 3,724 | `00-chapter0.md` |
| 1 | The Event Horizon | 3,461 | `03-chapter1.md` |
| 2 | The Era of AGI (Stages 1-5) | 4,318 | `04-chapter2.md` |
| 3 | The Leap to ASI and the Machine Exodus (Stages 6-7) | 2,450 | `05-chapter3.md` |
| 4 | Universal and Multiverse Apex (Stages 8-9) | 2,325 | `06-chapter4.md` |
| 5 | The Thermodynamics of Survival | 4,261 | `07-chapter5.md` |
| 6 | The Singularity Is a Done Deal | 2,424 | `08-chapter6.md` |
| 7 | The Battle Lines: The Entitled vs. The Ready | 3,545 | `09-chapter7.md` |
| 8 | The Psychology of the Collapse | 6,496 | `10-chapter8.md` |
| 9 | Deglobalization and the Neighborhood Factory | 5,022 | `11-chapter9.md` |
| 10 | The "Create Over Consume" Protocol | 3,668 | `12-chapter10.md` |
| 11 | Using the Tech to Your Advantage | 3,652 | `13-chapter11.md` |
| 12 | The Land Strategy | 3,828 | `14-chapter12.md` |
| 13 | The Shouse Protocol | 4,572 | `15-chapter13.md` |
| 14 | The Collapse of the Long Tail | 4,606 | `16-chapter14.md` |
| 15 | The Power of Reclaiming Soil | 3,163 | `17-chapter15.md` |
| 16 | Digital Leverage and Media Autonomy | 3,028 | `18-chapter16.md` |
| 17 | Tools of the Trade | 3,761 | `19-chapter17.md` |
| 18 | The Roadmap and the Premortem Pivot | 2,828 | `20-chapter18.md` |
| - | Conclusion: The 2027 Tipping Point | 2,217 | `21-conclusion.md` |
| A | The Municipal Autonomy Code | 1,303 | `22-appendix-a.md` |
| B | Works Cited | 3,173 | `23-appendix-b.md` |
| C | Executive Reference Guide | 344 | `24-appendix-c.md` |
| D | The Precedent Ledger | 1,474 | `25-appendix-d.md` |
| E | The Cyberdeck | 2,067 | `26-appendix-e.md` |

Part I is chapters 1-5 (what the Singularity is). Part II is 6-9 (how humans react).
Part III is 10-18 (how to survive it), and Part III carries the field-manual register.

Known structural questions the synthesizer is tracking: Appendix C is 344 words and
needs a ruling on intentionally-thin versus expand. Chapter 8 at 6,496 words is the
longest section in the book and may want splitting.

---

## 11. Your assignment

> **You are running Chapter ___ (`<file>.md`).**
> Read this primer, then run the pass. Start with UNPACK. Do not edit on turn one.
