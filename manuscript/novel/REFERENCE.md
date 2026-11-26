# Reference guide: how the novel gets finished

Written 26 Nov 2026, eighth logging chat, at CT's request ("a reference guide for doing this, policies, procedures,
whatever else you need"). It is the index to everything else, not a copy of it. When a rule here and a rule in a
linked file disagree, CT's words in the chat win, then the linked file, then this one.

The three endgame files: `GOALS.md` (what done is), `TODO.md` (what is next), `REFERENCE.md` (this file, how).

## 1. Start of a session (in this order)

1. Both `CLAUDE.md` files (`_workbench` and this repository). Branch `claude/singularity-publication-build-kparqk` in
   both repos; push every commit there, whatever branch the chat was given. No pull requests.
2. `_workbench`: `STATE.md`, and the newest entry in `sessions/LOG.md`.
3. Here, all of each: `WRITING-INSTRUCTIONS.md` (how CT wants it written), `PLAN-CHAPTERS-20-TO-36.md` (what happens;
   sections 10 to 13 are the working plan for 27 to 36), `EDIT-LOGGING-PROCEDURE.md` (mechanics, "What is still open",
   "Where things stand"), `TODO.md`, the accepted chapters in `drafts/`.
4. The tools: `manuscript/tools/edits-v6/make_v6.py` and `ops.py`; `manuscript/tools/edits-v5/checks.py` and
   `verify.py`; `manuscript/tools/edits-v6/find_in_book.py`.
5. Read both Docs fresh with the Docs connector (the result is saved to a file; copy it and use it as READ.json):
   - v6, the book: "StS v6 draft (Nov 25)", id `11nzQG2J-FciJ1XvU2LoPNTboL2N7pBVA0Dy-YCxqGuM`. Run verify.py on it;
     expect only the known PARTIAL rows (19, 30, 125, 131, 135, 137, 182, 197, 201).
   - v5, the base: "StS v5 draft (Nov 23)", id `1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA`. Run make_v6.py on it;
     every row must pass. Work from its `v6.txt`.
6. Tell CT in one line that you are ready, and the next edit number.

## 2. Where everything is

| What | Where |
|---|---|
| The book as it stands (every logged edit applied) | make_v6.py's `OUT/v6.txt` (rebuilt each session from the v5 read) |
| Each edit: who said what, Book now, Change to | `EDITS.md` (summary) and `drafts/chapter-NN.md` (full text, CT's words in bold) |
| Edit status against the Doc | `EDITS-status.md` (written by verify.py) |
| What happens in each chapter | `PLAN-CHAPTERS-20-TO-36.md`, sections 6 and 11 (11 wins for 27 to 36) |
| Arcs, quarrels, the chain of cause | the plan, section 10 |
| Every open question and its decision | the plan, section 12; anything still CT's is in `TODO.md`, section 1 |
| Ending lines waiting on CT | the plan, section 13 |
| What the ending depends on | the plan, section 7 |
| How CT writes, each character's voice | `WRITING-INSTRUCTIONS.md`, sections 5 and 12 |
| Character notes | `characters/<name>/` (gathered by `manuscript/tools/book.py cast`) |
| Which Doc is the book | `BRIDGE.md` (generated: `node scripts/sts-bridge.mjs export md`) |
| The PDF CT has | "StS v6 large print CURRENT (26 Nov, edits 1 to 186 ...)" in Drive folder "StS Publication Files" (`1QmqU-MsDcqfh1sC5Q_DsGeqcdyf_kLB_`); older builds in `12CbC-hEUy_5rArVtz8v393rc_ciV9Ltv` |
| Drive copy of the edit list | "StS v6 edit list (mirror of GitHub)"; its current id is in `EDIT-LOGGING-PROCEDURE.md`, step 10 |
| Build settings (copyright page, cover) | `publication/novel/build/book.json`; build steps in `publication/README.md` |

## 3. Policies (CT's standing rules)

- **Nothing goes into either Google Doc** until CT clears it. Log in GitHub only.
- **His words go in word for word** and are marked his. Smooth only what dictation broke. Mark what Claude worded.
  His notes that aren't for the page never go in the text.
- **Flag every fact Claude invents**, in the report for that chapter.
- **Reduce.** "The book is long enough." Count words in and out for each chapter; cut summary, repeated lessons and
  filler to pay for what is added. Targets: the plan, section 11.
- **Push back on** continuity errors, contradictions, logistics that can't happen and anything that confuses the
  reader. **Not** on his taste or a decision he has made.
- **A question from CT gets an answer, not an action.** Answer first, short. "Think about" and "let's figure out" mean
  plan with him.
- **"Just do it."** Write the chapter, check it, log it, push it, report in a few lines, start the next. Don't fish for
  approval at each step.
- **A correction replaces the edit in place** when the edit isn't in the Doc, and the lesson goes into
  `WRITING-INSTRUCTIONS.md` in the same turn.
- **Read before you claim.** To say whether something is true of the book, read the chapters it covers (use
  `find_in_book.py` to find them), not one grepped line. CT, 26 Nov: "you're just giving me what you think I want ...
  actually read the book ... give me a real answer."
- **No em dashes**, anywhere.
- **Code before tokens.** Grep `v6.txt` and the saved reads; a reader (subagent) is for judgment and sweeps, and every
  quote a reader returns gets grep-checked.
- **Make a PDF only when CT asks.** Refresh the Drive mirror of the edit list once, at the end of a session.
- **Ma's calls** are Sunday at 9:40 in the morning; exactly one is at night (Ch 13). He does not go home before
  Chapter 37.

## 4. Procedures

### 4.1 One chapter, start to finish

1. Read the chapter whole in `v6.txt` (`find_in_book.py OUT/v6.txt chapters` gives the line numbers), its rows in
   the plan (sections 10 and 11), and `WRITING-INSTRUCTIONS.md` sections 5 to 12.
2. Read the lines in other chapters it depends on or feeds (the plan's sections 7 and 12.3; grep for names, objects,
   dates).
3. Search the book for each new key phrase (`find_in_book.py OUT/v6.txt find "phrase"`) so nothing repeats.
4. Write the changes as ops rows in `manuscript/tools/edits-v6/ops.py`, above the `ITALIC` list, under a comment line
   `# NNN, Ch NN: what (drafts/chapter-NN.md)`. A find must appear exactly once; a `(start, end)` pair replaces a span.
   In a replacement, a newline starts a paragraph, an empty line is a scene break, `*...*` is italic. Check the span
   for italics first (verify.py can't see them; a replaced span loses them unless wrapped in `*...*`).
5. Add a check row to `manuscript/tools/edits-v5/checks.py`: words that must be there, words that must be gone. Use
   only gone-words that are in the Doc now or came in through a logged edit; never a line that is already in the Doc
   as a must-have (both of those make the row show PARTIAL).
6. Run `python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT --no-docx`. If an earlier row fails because this
   edit changed its words, narrow that row or update it to the new words; never delete it.
7. Run the checklist in `WRITING-INSTRUCTIONS.md`, section 13, on the new text in `OUT/v6.txt`: openers counted, no
   mirrored lines, no counting pattern, no day names that only mark time, messages in italics, numbers in words, who
   is speaking, everyone introduced.
8. Count words in and out (difflib over the old and new `v6.txt`) and the chapter's total against its target.
9. Write `drafts/chapter-NN.md`: a short header (sources, words), each change as Book now and Change to (CT's words in
   bold), the facts Claude invented, what touches another chapter. The scratchpad script used on 26 Nov builds the
   Book now and Change to blocks from the ops rows; it is easy to rewrite.
10. Add the edit to `EDITS.md`, above the line "Corrected in place, 26 Nov ...", with the number, a bold title, a few
    lines of what changed and whose words, and "Logged only; not in the v6 Doc yet."
11. Run `python3 manuscript/tools/edits-v5/verify.py V6_READ.json --table manuscript/novel/EDITS-status.md`. The
    PARTIAL list must not grow.
12. Tick the chapter in `TODO.md`. Commit (one change, plain message), push to the branch.
13. Report to CT in a few lines: what changed, every invented fact, what touches another chapter, the words. Then the
    next chapter.

### 4.2 A correction from CT

Change what he named and keep the rest. Edit the edit's ops rows in place (a correction to an edit not in the Doc
replaces it), update its check row and `drafts/` file, add the lesson to `WRITING-INSTRUCTIONS.md` (section 16 table,
and the rule it belongs under), rebuild, verify, commit, push, report in a line or two.

### 4.3 A continuity fix in a logged chapter

Same as 4.2. If the text came in through an edit, change that edit's ops row. If it is the book's old text, add a row
under the edit number it belongs with. Record it at the foot of that chapter's `drafts/` file and in `EDITS.md`.

### 4.4 Checking a claim against the book (a blurb, a synopsis, a plan)

Write the claims to a JSON file (see `manuscript/tools/edits-v6/claims-instagram-synopsis.json`), run
`find_in_book.py OUT/v6.txt claims FILE.json`, then read the chapters the hits are in. Answer claim by claim: true,
not true (with the line that says otherwise), or not in the book.

### 4.5 Large print PDF (only when CT asks)

`EDIT-LOGGING-PROCEDURE.md`, "Making the large print PDF".

### 4.6 The final copy (only on CT's go)

Ask which way: a new Google Doc from make_v6.py's .docx (without `--no-docx`; a fresh v5 read, since picture links
expire), or the logged edits as suggestions in the v6 Doc. Then update `src/lib/data/novel/instances.json`, run
`node scripts/sts-bridge.mjs export md > manuscript/novel/BRIDGE.md`, and remake the Drive bridge page. Name the copy
for what it is ("v7" is taken by a frozen side copy).

### 4.7 End of a session

1. `TODO.md`: boxes ticked, the next edit and chapter at the top, the "Done" line for this session.
2. `EDIT-LOGGING-PROCEDURE.md`: "What is still open" and "Where things stand".
3. `WRITING-INSTRUCTIONS.md`: any new lesson from CT's corrections.
4. `_workbench`: `STATE.md` (Next moves, item 0) and a new entry at the top of `sessions/LOG.md`.
5. The Drive mirror of the edit list, once: create a new Google Doc from `EDITS.md`'s text titled "StS v6 edit list
   (mirror of GitHub)"; rename the old one "OLD: StS v6 edit list (mirror of GitHub)" and put a pointer to the new one
   at its top; write the new id into `EDIT-LOGGING-PROCEDURE.md` (step 10) and `EDITS.md`.
6. Commit and push both repos.

## 5. Tools

| Command | What it does |
|---|---|
| `python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT [--no-docx]` | The v5 Doc with its suggestions accepted, then every ops row, then every check row. Writes `v6.txt`, `v6-read.json`, and the .docx without `--no-docx` |
| `python3 manuscript/tools/edits-v5/verify.py READ.json [--table FILE]` | Where each edit stands in a Doc |
| `python3 manuscript/tools/edits-v6/find_in_book.py OUT/v6.txt chapters` | Chapter list with line numbers and word counts |
| `... find_in_book.py OUT/v6.txt find "regex" ["regex"] [--ch 27-36]` | Every line matching all the regexes, with its chapter |
| `... find_in_book.py OUT/v6.txt claims FILE.json` | Evidence for each claim in a list |
| `python3 manuscript/tools/book.py cast` | Rebuilds the character folders |
| `node scripts/sts-bridge.mjs status` | Which Doc is CURRENT |

## 6. Pitfalls learned

- A check row's must-have that is already in the Doc, or a gone-word that never was, makes verify.py show PARTIAL.
- The same find string can sit in two ops rows (an old row and a correction). Change the newest one, and check
  `s.count()` before any scripted replace.
- An ops row's text and its check row must be changed together.
- A replaced span loses italics unless the replacement wraps them in `*...*`.
- Day names, "the way", "He knew", "Then he" chains and mirrored lines creep back in; count them before logging.
- A plan written from grepped lines missed facts the chapters had (Ray quit drinking, Chapter 5). Read the chapter.
- Readers are good at sweeps and bad at judgment calls about CT's taste. Grep every quote they return.
