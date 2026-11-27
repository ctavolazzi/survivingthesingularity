# Reference guide: how the novel gets finished

Written 26 Nov 2026, eighth logging chat, at CT's request ("a reference guide for doing this, policies, procedures,
whatever else you need"). It is the index to everything else, not a copy of it. When a rule here and a rule in a
linked file disagree, CT's words in the chat win, then the linked file, then this one.

The three endgame files: `GOALS.md` (what done is), `TODO.md` (what is next), `REFERENCE.md` (this file, how). Beside
them: `STORY-REPORT-2026-11-26.md` (the evaluation) and `NEXT-BUILD.md` (the structure and the gate for the next build).

## 1. Start of a session (in this order)

1. Both `CLAUDE.md` files (`_workbench` and this repository). Branch `claude/singularity-publication-build-kparqk` in
   both repos; push every commit there, whatever branch the chat was given. No pull requests.
2. `_workbench`: `STATE.md`, and the newest entry in `sessions/LOG.md`.
3. Here, all of each: `WRITING-INSTRUCTIONS.md` (how CT wants it written), `PLAN-CHAPTERS-20-TO-36.md` (what happens;
   sections 10 to 13 are the working plan for 27 to 36), `EDIT-LOGGING-PROCEDURE.md` (mechanics, "What is still open",
   "Where things stand"), `TODO.md` and the checkpoint files its first paragraph names, the accepted chapters in
   `drafts/`.
4. The tools: `manuscript/tools/edits-v6/make_v6.py` and `ops.py`; `manuscript/tools/edits-v5/checks.py` and
   `verify.py`; `manuscript/tools/edits-v6/find_in_book.py`.
5. Read both Docs fresh with the Docs connector (the result is saved to a file; copy it and use it as READ.json):
   - v8, the book since 26 Nov: "StS v8 draft (Nov 26)", id `1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8`. It holds
     every edit, 1 to 223, without the 19 pictures. Run verify.py on it; expect rows 1 to 223 "accepted", nothing
     PARTIAL, and the newer edits (224 to 234 since 27 Nov; `TODO.md` has the current count) "not in the Doc" until CT clears them. Its locked twin is "StS v8 BACKUP (Nov
     26), do not edit" (`18gmZKWiUPyujRkRY_ZSh80ifdchZKtk8oPOpVuycOPM`).
   - v5, the base: "StS v5 draft (Nov 23)", id `1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA`. Run make_v6.py on it;
     every row must pass. Work from its `v6.txt`. (make_v6.py keeps its name; it builds v8.)
   - The old v6 Doc ("StS v6 draft (Nov 25)", `11nzQG2J-FciJ1XvU2LoPNTboL2N7pBVA0Dy-YCxqGuM`) is no longer the book.
     On it verify.py shows the nine old PARTIAL rows (19, 30, 125, 131, 135, 137, 182, 197, 201).
6. Tell CT in one line that you are ready, and the next edit number.

## 2. Where everything is

| What | Where |
|---|---|
| The book as it stands (every logged edit applied) | make_v6.py's `OUT/v6.txt` (rebuilt each session from the v5 read) |
| Each edit: who said what, Book now, Change to | `EDITS.md` (summary) and `drafts/chapter-NN.md` (full text, CT's words in bold) |
| Edit status against the Doc | `EDITS-status.md` (written by verify.py) |
| Who knows what, and when (the secrets) | `knowledge-sheet-2026-11-27.md` and its three CSVs; Google Sheet "Surviving the Singularity: who knows what (edits 1 to 236)" (`11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`). Rebuilt by `knowledge.py` |
| When every scene happens, and what a calendar can test | `calendar-2026-11-27.md` and its two CSVs; Google Sheet `11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`. Rebuilt by `story_checks.py calendar` |
| Who talks to whom, how much, and the sense words in each scene (layer one, rough) | `conversations-2026-11-27.md` and its three CSVs; Google Sheet `11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`. Rebuilt by `story_checks.py conversations` |
| What each person wants, when we meet them and by the end; what each person is after in each scene | `desires-2026-11-27.md` and its CSVs (characters, scenes); tabs in the story checks workbook (`11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`). Rebuilt by `story_checks.py desires` |
| The conversations that matter: what each wants from the other, what changes, what it sets up or pays off (layer two) | `conversations-layer-two-2026-11-27.csv` (notes in `desires-2026-11-27.md`); workbook tab. Rebuilt by `story_checks.py conversations2` |
| Every money figure on the page, and whether the money adds up | `money-2026-11-27.md` and its two CSVs; workbook tabs. Rebuilt by `story_checks.py money` |
| Where each object is, every time it appears (the amp, the pot, the notebooks, the Telecaster, the tape, the hose, the receipt, the checks, the arms) | `objects-2026-11-27.md` and its CSV; workbook tab. Rebuilt by `story_checks.py objects` |
| Everything set up, and where it pays off or "never" | `plants-payoffs-2026-11-27.md` and its CSV; workbook tab. Rebuilt by `story_checks.py plants` |
| What happens in each chapter | `PLAN-CHAPTERS-20-TO-36.md`, sections 6 and 11 (11 wins for 27 to 36) |
| Arcs, quarrels, the chain of cause | the plan, section 10 |
| Every open question and its decision | the plan, section 12; anything still CT's is in `TODO.md`, section 1 |
| Ending lines waiting on CT | the plan, section 13 |
| The evaluation of the whole story | `STORY-REPORT-2026-11-26.md` |
| The next build: the book in order, what it is made of, its gate | `NEXT-BUILD.md` |
| What the ending depends on | the plan, section 7 |
| How CT writes, each character's voice | `WRITING-INSTRUCTIONS.md`, sections 5 and 12 |
| Character notes | `characters/<name>/` (gathered by `manuscript/tools/book.py cast`) |
| Which Doc is the book | `BRIDGE.md` (generated: `node scripts/sts-bridge.mjs export md`) |
| The PDF CT has | "StS v8 large print CURRENT (27 Nov, edits 1 to 243).pdf" (`14MdeTNd1djyhORwqpP422I-XZq42j7kj`); it has neither edit 244 (the Dedication) nor 245 (Ch 0) in Drive folder "StS Publication Files" (`1QmqU-MsDcqfh1sC5Q_DsGeqcdyf_kLB_`); older builds in `12CbC-hEUy_5rArVtz8v393rc_ciV9Ltv` |
| The Doc of Chapters 0 to 5 | "StS v9 draft, Chapters 0 to 5 (Nov 27, edits 1 to 270)" (`1EIYyOWtzeRjW6S_XO510lOZ3gnIX7Fts3uOLO7_OcY0`), made on CT's ask from `make_v6.py ... --no-pictures`, cut after Chapter 5 (front matter, contents to Ch 5); checked word for word against the built book. A reading copy, not the manuscript; edits still go in GitHub |
| The Doc of Chapters 0 to 11 | "StS v9 draft, Chapters 0 to 11 (Nov 27, edits 1 to 283)" (`1izsflJitkJ08R04aA7vfGnDRQ7dTqmzgUmXYjVlLEsE`), made the same way, through Chapter 11 (both Bidwell "Meanwhile" sections are inside it); checked word for word. A reading copy |
| The PDF of Chapters 0 to 11 | "StS large print, Chapters 0 to 11 (27 Nov, edits 1 to 287).pdf" (`1l31NmLl0HxKGL2lpffz2mtVj-iL90U0U`) in "StS Publication Files", on CT's ask: the make_v6.py --no-pictures .docx cut after Chapter 11, then `build.py ... --only large --skip-edit-gate`; 166 pages, every build check passes |
| The free sample PDF, Chapters 0 to 10 | Large print, 151 pages, edits 1 to 291, every build check passes (27 Nov, fifteenth chat, CT: "Recompose the 0-11 PDF ... Before chapter 11"). The make_v6.py --no-pictures .docx cut before the Chapter 11 heading (the second Meanwhile stays in) and its Contents entries from Chapter 11 on, then `build.py ... --only large --skip-edit-gate`. On the sites, replacing the 0 to 11 file another chat put up the same day: survivingthesingularity `static/downloads/Surviving-the-Singularity-Chapters-0-10.pdf`, linked from /sample (`main` 5c0c68b9); thecoffeejesus `studio/files/Surviving-the-Singularity-Chapters-0-10.pdf`, linked from the book's "Can I read some first?" answer (`main` b88dbde). The old 0-11 files are still on both sites, unlinked |
| Drive copy of the edit list | "StS edit list, edits 1 to N (mirror of GitHub)"; its current id is in `EDIT-LOGGING-PROCEDURE.md`, step 10 |
| Build settings (copyright page, cover) | `publication/novel/build/book.json`; build steps in `publication/README.md` |

## 3. Policies (CT's standing rules)

- **Nothing goes into the Google Docs** until CT clears it. Log in GitHub only. (v8 was made on his word, 26 Nov.)
- **His words go in word for word** and are marked his. Smooth only what dictation broke. Mark what Claude worded.
  His notes that aren't for the page never go in the text.
- **Flag every fact Claude invents**, in the report for that chapter.
- **Good, not short.** CT, 26 Nov: "I don't care how long it gets I want it to be good." Cut summary, repeated
  lessons and filler because they are weak, never to hit a count. Still report words in and out so he can see it.
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
   dates). Check the knowledge sheet (`knowledge-sheet-2026-11-27.md`) for every secret the new lines touch: who
   knows it by then, and who must still not know.
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
    lines of what changed and whose words, and "Logged only; not in the v8 Doc yet."
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
5. The Drive mirror of the edit list, once: upload `EDITS.md` as text/plain (a file reference, not typed) titled
   "StS edit list, edits 1 to N (mirror of GitHub)"; rename the old one with "OLD:" in front and put a pointer to the new one
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
| `python3 manuscript/tools/edits-v6/story_report.py OUT/v6.txt` | Measures the story: length and talk by chapter, who is on the page, where each thread opens and closes, tics, smells, scenes with only women, long speeches, numbers that must agree |
| `python3 manuscript/tools/edits-v6/build_gate.py OUT/v6.txt [--todo TODO.md]` | What must be gone and what must be there before the next build (`build-gate.json`), and the unticked boxes |
| `python3 manuscript/tools/edits-v6/openers.py OUT/v6.txt [--ch 20-36]` | The sentence-opening checker: runs of sentences that open with the same word, runs of pronoun-or-name openers, paragraphs one opener dominates |
| `python3 manuscript/tools/edits-v6/whose_words.py V5_READ.json "phrase" ["phrase"]` | Where a line came from: the v5 Doc, an ops row, which edit in `EDITS.md` quotes it, which `drafts/` files. Run it before calling a line CT's or Claude's |
| `python3 manuscript/tools/edits-v6/knowledge.py OUT/v6.txt manuscript/novel --date YYYY-MM-DD` | The knowledge sheet: who knows, suspects or has wrong each of 35 secrets, by chapter and by phase. Its `FACTS` list is the only hand-written part; a quote no longer in the book stops the run |
| `python3 manuscript/tools/edits-v6/story_checks.py calendar OUT/v6.txt manuscript/novel --date YYYY-MM-DD` | The calendar: a date for each of the 137 scenes, the time words on the page, and 28 checks (weekdays, intervals, ages). It stops if the scene count changes or a quoted line is gone. Money, objects, plants and payoffs, and the senses are to be added as further commands |
| `python3 manuscript/tools/edits-v6/story_checks.py desires OUT/v6.txt manuscript/novel` | The desires sheet: one row per person (the script finds the first line naming them; the wants are Claude's reading, each with its line) and one per scene (fourteen readers' pass, from `desires-scenes-data-2026-11-27.json`) |
| `... story_checks.py conversations2 OUT/v6.txt manuscript/novel` | Layer two of the conversation map: 22 conversations, what each wants, what changes, the line it pays off |
| `... story_checks.py money OUT/v6.txt manuscript/novel` | Every money figure on the page (counted) and 12 checks with the lines they rest on |
| `... story_checks.py objects OUT/v6.txt manuscript/novel` | Where each object is at every sighting, sorted into book order by the script |
| `... story_checks.py plants OUT/v6.txt manuscript/novel` | Every question in the scene sheet's "Opens a question" column with a verdict and the line that pays it; for "never", the words searched and the hits. A sheet question with no verdict stops the run |
| `python3 manuscript/tools/book.py cast` | Rebuilds the character folders |
| `node scripts/sts-bridge.mjs status` | Which Doc is CURRENT |

## 6. Pitfalls learned

- The newest checkpoint is `CHECKPOINT-2026-11-27-smell.md` (the end of the smell chat; the prompt for the taste
  pass). Before it: `CHECKPOINT-2026-11-27-eleventh.md` (what is open with CT, and the prompt for the smell
  pass). **That prompt has been run** (the smell chat, 27 Nov: edits 235 and 236); don't run it again. Where the
  smell pass stands is in `TODO.md` section 3 and `smell-table-2026-11-27.md`. The other chat of 26 Nov left `CHECKPOINT-2026-11-26-riemann-praether.md`.
- Learned in the smell chat (27 Nov):
  - A new chat is given its own branch (that one got `claude/hello-azhytd`) and `main`'s `BRIDGE.md` and
    `WORKBOARD.md` still say v4. Both are stale. This branch, its `instances.json` and the Drive page "sts-bridge: read
    this first" are right. Ask CT before pushing to this branch if the chat was told to push somewhere else; he said
    yes ("that's the main branch we've been working on").
  - A Docs read comes back as a 1.5 MB file under the session's `tool-results` folder, wrapped in `{"content": ...}`.
    Copy it as it is; make_v6.py and verify.py read it that way. The book is about 106,000 words (140,000 tokens), so
    it can be read whole in the chat from `OUT/v6.txt` in chunks of about 400 lines.
  - Say whose words a line is only after `whose_words.py` and the record. The perfume line in Chapter 8 was called
    CT's wording, then "the flat one he named"; both were wrong (edit 45: his beats and dialogue, Claude's narration).
  - When CT describes the job in the chat, that is the job, even when a prompt file says it differently. He asked for
    "a pass over all the scenes to determine which ones need to have their smell described"; the file said to start
    with the truck.
  - A list of candidates gets cut before he sees it. The first answer gave eight scenes that "need" a smell; two did
    (his). Mark the rest as optional or drop them.
- Learned in the story sheets chat (fourteenth, 27 Nov):
  - The scene sheet numbers its own rows, and its row 59 is a cut scene ("(cut)"), so from scene 59 on its "#" is one
    more than the scene's place in the book. `story_checks.py`'s `Book` class reads the sheet's numbers; use it.
  - A tab too big to type into a call (the scenes tab is 128 KB) goes up by file reference: upload the CSV to Drive as a
    Sheet (`create_file` with `sha256:<hash>:<path>`), copy its tab into the workbook (`copy_sheet_to_another_spreadsheet`),
    rename the tab, and title the staging file "OLD: staging copy". Nothing is typed, so nothing is mistyped.
  - The scene sheet's "Opens a question" and "Closes a question" columns word the same question differently: matching
    them by script found 9 of 126. The pairings in `PLANTS` are read, not matched.
- Two chats can log on this branch at once. Fetch it and read TODO.md's "Next edit" before numbering; fetch again
  before every commit, and merge (never force-push). On 27 Nov both chats had taken 229 and 230.
- The scene sheet (27 Nov): one row per scene with date, place, whose scene, who is on the page, what turns, threads,
  questions and numbers. Google Sheet id `13hXnHxprSx-IGW_-TOFzeJFHIpzWyicHx_NtTgaya7o`; copy in `scene-sheet-2026-11-27.csv`. It is a snapshot of
  edits 1 to 233, filled by readers; check a cell on the page before relying on it.
- When the current copy changes in the bridge map, two site tests name it and must change too:
  `tests/unit/novel-bridge.test.mjs` and `tests/unit/novel-doc-edit.test.mjs` (they kept "build guard" red from v8's
  making until the tenth chat). Run `npm run test:release` after any change to `instances.json`.
- A polish pass (edit 227): readers return candidates, every quote is machine-matched, and each is read on the page and
  checked for whose words it is before anything changes. Of 50 candidates, 20 were changed. CT's dictated lines, the
  done chapters, the ending and the fire were left; repetition on purpose and quips in light moments are not faults.
- A check row's must-have that a later edit rewrites makes make_v6.py fail on the older row; take that string out of
  the older row (rows 172 and 204 were narrowed this way for edits 226 and 227).

- A check row's must-have that is already in the Doc, or a gone-word that never was, makes verify.py show PARTIAL.
  Exactly: a row reads "not in the Doc" only if every gone-word is still in the Doc being checked (v8 from 26 Nov). A gone-word that came in
  through a logged edit (so is not in the Doc) makes PARTIAL; leave it out of the row (learned 26 Nov, edit 222).
- The same find string can sit in two ops rows (an old row and a correction). Change the newest one, and check
  `s.count()` before any scripted replace.
- An ops row's text and its check row must be changed together.
- A replaced span loses italics unless the replacement wraps them in `*...*`.
- Day names, "the way", "He knew", "Then he" chains and mirrored lines creep back in; count them before logging.
- A plan written from grepped lines missed facts the chapters had (Ray quit drinking, Chapter 5). Read the chapter.
- Readers are good at sweeps and bad at judgment calls about CT's taste. Grep every quote they return.
- Count words from `v6.txt` with `story_report.py`, never from a file with line numbers in it (the first targets
  were 1,500 words off for that reason).
- An edit that is in the Doc is never changed in place. Add a new row that finds its words and replaces them.
- The Drive connector refuses any call over about 3.1 MB of files. The .docx with its 19 pictures is 5.6 MB, so v8
  was made with `make_v6.py ... --no-pictures` (CT's choice, 26 Nov). The PDF (0.9 MB) and the edit list fit.
- A shell heredoc that is not quoted runs anything in backticks (`make_v6.py` vanished from a record this way on 26 Nov).
  Quote the heredoc ('EOF').
