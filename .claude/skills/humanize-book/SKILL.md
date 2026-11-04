---
name: humanize-book
description: |
  Run the vendored humanizer skill on Surviving the Singularity without flattening the
  book's voice. Use when CT asks to humanize, de-AI, or clean AI tells out of a chapter,
  section, appendix, the sample, a blog post, or book marketing copy; asks "which chapters
  sound most like AI"; or says "run humanizer on the book". Scans first, edits one section
  per pass in canonical source only, treats VOICE-GUIDE.md as the voice sample, protects
  refrains, dialogue, epigraphs and citations, and re-runs the book's checks after.
---

# Humanize the book

This wraps `.claude/skills/humanizer/SKILL.md` (blader/humanizer, vendored and unmodified;
see `VENDORED.md` there). Read that file first and follow its process. Everything below
is how it applies to this book, and where this file and humanizer disagree, this file wins,
because humanizer itself says a writing sample overrides its patterns.

## 1. What you may edit

- **Only canonical source:** a `*.md` file in `src/lib/data/book/` that `book.json` lists.
  Never `manuscript/` exports, PDFs, EPUBs, `book-v1-archive/`, `sample.md`, or anything
  generated (README, "Book content: the single source of truth").
- **Never these, even if listed:** Appendix B (Works Cited, `23-appendix-b.md`), epigraphs
  (the `> *"..."*` block and its attribution line), captions and license credits under
  images, table rows of data, anything inside quotation marks that a real person said or
  wrote, link targets, image paths, and block ids.
- **Blog posts** (`src/routes/blog/**/+page.svelte`) and site copy may be humanized on
  request. Change prose only, never markup, and keep `src/lib/offer.js` promises intact.

## 2. The voice sample is VOICE-GUIDE.md

Read `src/lib/data/book/VOICE-GUIDE.md` before every pass. Give humanizer the guide's
quoted lines as the writing sample. Then identify the register of the passage you are on:

| Register | Where | What humanizer may touch | What it must leave |
|---|---|---|---|
| A. Argument | Introduction, Preface, Parts I and II Foundations | Repeated hammers, stiff uncontracted lines, stock words, staged run-ups that delay the point | A long argument that lands on one short line that carries a new claim. Profanity on budget. |
| B. Narrative | Chapter 0, chapter-opening scenes | A sentence after a scene that explains what it meant (humanizer §2 and VOICE-GUIDE §1B agree: cut it) | Dialogue, physical detail, rhythm, the characters' own speech habits |
| C. Field Manual | Part III, chapters 10 to 18 | Vague advice with no number, part or action; inflated significance | Imperatives, numbered steps, real numbers |

## 3. Where humanizer's rules bend for this book

- **§1 Not X but Y.** The book's refrains are deliberate and stay: "Not abolished.
  Optional." and anything else CT names as a refrain. Keep any contrast whose negative
  half corrects a belief the reader really holds (humanizer's own exception). Cut the
  ones where nobody claimed the negative half, and cut repeats: the same move twice on a
  page is the tell even when once is the voice.
- **§2 One-line closers.** VOICE-GUIDE says land the paragraph on a short line and
  "do not explain the hammer after you swing it." So keep a hammer that adds a claim;
  cut the sentence that explains it, and cut a hammer that only restates the paragraph.
- **§8 Dashes.** The book already has zero em dashes (no-em-dash rule, v0.5.0). En dashes
  in number ranges (`1–5`, `2001–2024`) are correct typography; leave them.
- **§12 Stock words.** "Quietly" is the book's most frequent stock word (23 hits in
  prose at v0.11.0, `docs/humanizer/scan-2026-11-01.md`). Treat each one as a question: does the
  quiet carry information (a thing hidden, unnoticed, unannounced)? Keep those. Replace
  or cut the rest with the specific thing that happened.
- **§17 Borrowed authority / §23 hedges.** Do not fix by inventing a source. If a claim
  needs a citation, flag it for CT and FACTCHECK; do not add a name, number, date or
  quote. Every fact stays exactly as written (VOICE-GUIDE §6.6).
- **§19 Bold.** `> **Sentence.**` is pull-quote syntax with real rendering behavior
  (VOICE-GUIDE §3). Keep it. "**In this chapter:**" and the Precedent block labels are
  structure; keep them.
- **§20 Headings.** Chapter titles live in `book.json` too and are CT's titles. Do not
  recase or rename them.
- **§21 Curly quotes.** The book uses straight quotes in prose; curly ones survive mostly
  in cited titles. Leave quotes inside citations alone.
- **Contractions on** (VOICE-GUIDE §3): uncontracted lines in A or C are drift; contract.
- **Never** introduce the word "manifesto", "decentralized" as a goal, or an em dash.

## 4. How a pass runs

1. **Scan.** `python3 scripts/humanizer_scan.py` ranks every section. For one section:
   `python3 scripts/humanizer_scan.py --file 07-chapter5.md --lines`. Hits are
   candidates, not verdicts. The scanner cannot see structural tells (§6 triads, §7
   repeated openings, §26), so read the whole section anyway.
2. **Mark, do not edit yet.** Produce a findings list for the section: line, pattern
   number, the phrase, keep or change, and why in one clause. Group by register.
3. **Show CT before writing to the book** unless he already said "just do it" for this
   pass. One grouped question set if anything is his call (a refrain, a profanity, a
   claim that needs a source).
4. **Edit one section per commit.** Prefer `python3 scripts/sts.py id replace <block-id>
   --file <tmp.md>` for paragraph edits (find ids with `sts.py id list` or `sts.py ask`),
   so the manuscript index stays coherent; then `python3 scripts/sts.py id build`. Plain
   edits to the `.md` are fine if you rebuild the index after.
5. **Check the claim did not change.** For every changed block, diff old and new and list
   each number, name, date, quote and citation in both. They must match.
6. **Run the book's checks:**
   ```bash
   python3 scripts/humanizer_scan.py --selftest
   python3 scripts/sts.py id verify
   python3 scripts/sts.py verify
   python3 scripts/humanizer_scan.py --file <file> --lines   # the hits you meant to fix are gone
   git diff --stat                                           # only the files you meant
   ```
7. **Record.** Add a line to `docs/humanizer/LOG.md`: date, section, findings count, kept
   vs changed, commit. Save a fresh scan with `--out docs/humanizer/scan-YYYY-MM-DD.md`
   when a pass finishes a chapter.

## 5. What not to claim

Humanizer edits for human readers. Its own README says detectors still flag most of its
output. Never tell CT, a buyer or a reader that the book "passes AI detection" or is
"human-verified" because of this pass. The honest description: "edited against Wikipedia's
Signs of AI writing list, by section, with every fact held fixed."
