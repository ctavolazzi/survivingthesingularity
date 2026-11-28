# The habits pass: Chapter 11 to the Epilogue

## Done, 28 Nov 2026 (seventeenth chat)

CT: "Prepare the next PDF version of the manuscript by correcting these habits with the variety I'm looking for, as
discussed and documented." Asked whether to approve each batch first or review inside the PDF: "Inside it." So every
change went in, and he reviews them in "StS v8 large print CURRENT (28 Nov, edits 1 to 322, the habits pass).pdf" (`1SS145ExuGZIvprNmiIKC-brau1aSOx8D`) with "StS habits pass: before and after (28 Nov, edits 301 to 322)" (`1S6IsTQmP6b8NQYhBTblI_3z839OJ_8orgPXCctZi7co`) beside it, both in "StS Publication Files". The old CURRENT
(edits 1 to 295) is "OLD: StS v8 large print (27 Nov, edits 1 to 295).pdf" in "Older builds".

- Before the pass the toolbox's "the way" pattern was widened (it missed 21 comparisons, the pie among them), and the
  moves were cut as Claude reasoned on 27 Nov: "like" capped at 3, "Give a real amount" and "Say how long" out, the
  clever "checked him for ripeness" example out.
- Scope with the wider pattern: 348 instances from Chapter 11 on, 159 in 69 pile-ups. Run as one workflow: a writer per
  batch of chapters (7), two checkers each (CT's ear; a first-time reader in the scene), one retry, then a recheck; a
  change went in only if both checkers passed it. 40 agents, about 6 million tokens, 74 minutes. Then Claude read every
  approved change in its paragraph and changed four calls (Grace "like she always did", David "like he had", the porch
  "how he used to", and "He knew what it was" in Chapter 39 kept as CT wrote it: the ending gets the lightest touch).
- Result: 48 changes, logged as edits 301 to 322, one per chapter, plus edit 297 corrected in place. 105 lines kept,
  with a reason each, and 7 rewrites turned down. Every line is in `habits-ledger.csv` (its rows number the sheet as it
  stood before the pass, saved as `habits-sheet-before-pass.csv`). After: 295 instances, 76 in 35 pile-ups, every one of
  those 76 judged and kept.
- Moves used: "how" 10 of 10 (at its cap), "same as" 4, "like" 3 of 3 (at its cap); the rest spread thin. A next pass
  should not deal "how" or "like" again without CT raising the cap.
- Checks: all 323 check rows pass; every changed paragraph traces to a listed change; no new opener runs; no new phrase
  repeats except "looked at him like" (three uses in the book, Ch 6, 11, 39). The PDF passes every build check (786
  pages, text letter for letter). The scene sheet, story checks and their data were brought to the new text.
- The before-and-after list is also `habits-pass-before-and-after-2026-11-28.md`.


Started 27 Nov 2026 in the seventeenth chat. **The first batch has not been run.** CT: "Don't run the first batch.
We're going to have a different model than you run the first batch. But you can build it." This file is for that
model. Read it, then `WRITING-INSTRUCTIONS.md` sections 4 to 12, before touching a line.

## What CT asked for (his words)

- "make a plan to go through all of this line by line and in context of the section, determine if it's fine. And then
  in context of the book and reader fatigue, going through it with repetition, determine if maybe there's a different
  word choice or a different way to phrase it. Remember the example that I gave you about the smell from the kitchen
  and how it conveys meaning, how it almost personifies something? That's kind of what I'm looking for."
- Scope: "0 through 10 are fine, because we did 0 through 10 and we published it already. So 11 through the rest of the
  book is what I'm asking you to look at." Start at Chapter 11 and go in book order. (Claude proposed starting at the
  densest chapter; he had said 11. Follow the order he gives.)
- After the Chapter 11 trial: "The way can change to \"how\". As in \"how it usually did\". Think of some other ways
  to add variety, because I'm not convinced by your first attempt."
- Then: "create for yourself a toolbox so that you're not just building from nothing and going from nowhere. Create
  like some code that you could call for like maybe some randomized ideas, because there's only so many permutations in
  the English language that we could use to convey meaning ... Instead of reading through each one of them one by one,
  you could just read through all of them at once, but with some sort of code that searches for patterns that we've
  already identified. And I think that would do the trick of like knocking out some of the repetitiveness in one fell
  swoop without consuming a billion fucking tokens."

His kitchen example (`WRITING-INSTRUCTIONS.md`, 7a): the perfume "acts like a lightning rod for knuckleheads and more
or less behaves like a slime mold, expanding out in every direction, but how it is utterly decimated by the ferocity of
the air from the kitchen." The thing itself acts, and the verb carries the physics.

## The numbers (book at edit 300)

Eight habits, the ones `story_report.py` counts, less day names. From Chapter 11 on: 338 instances. 26 are in
someone's speech and 3 are on the guide's kept list. 159 are alone in their scene, which the guide says is fine ("Each
is fine once in a scene"). **150 sit in 66 pile-ups** (two or more of one habit in one scene). Those are the work.
From Chapter 12 on: 143 lines in 63 pile-ups.

## The toolbox

`manuscript/tools/edits-v6/habits.py` (its docstring lists every command). Build the book first, as every chat does:
read the v5 Doc fresh, `make_v6.py V5_READ.json OUT --no-docx`.

| Command | What it gives |
|---|---|
| `habits.py sheet OUT/v6.txt V5_READ.json` | `habits-sheet.csv`: every instance, its line, counts, and where the words came from. Run it first, and again after any logged edit (row numbers follow the book) |
| `habits.py piles OUT/v6.txt --from 12` | The pile-ups in book order, one line each, marked done or part from the ledger |
| `habits.py batch OUT/v6.txt --from 12 --size 8 --skip 0` | The next pile-ups in full: each line in its paragraph, whose words, and three moves dealt for it |
| `habits.py deal "the way ..." --row 41 --seed 2` | Three other moves for one line, if the first deal does not fit |
| `habits.py use --row 41 --move the-way.how --before "..." --after "..." --status proposed` | One line in `habits-ledger.csv` |
| `habits.py count` | How often each move has been used, against its cap |
| `habits.py repeats OUT/v6.txt` | Exact phrases the book uses more than once, which nobody has named yet |

`habits-moves.json` is the only hand-written part: for each habit, the ways out, each with a cap. CT's own move ("how")
is marked. Add a move when he gives one, in his words. The dealer is seeded, never deals a move at its cap, and leans
to the least used, so one fix does not become the next habit.

## How to run a batch

1. `batch` prints the next pile-ups. For each, read the paragraph it prints. Open the scene in `OUT/v6.txt` only when
   the paragraph is not enough. Do not send readers; the Chapter 11 trial used nine agents and about 1.3 million tokens
   for 16 lines, which is what CT wants to stop.
2. **One stays.** In each pile-up keep the strongest instance and reword only the weaker ones. A pile-up of two usually
   means one change.
3. **Check whose words** before touching a line: the sheet's source column, then `whose_words.py`, then the entry in
   `EDITS.md`. CT's dictated lines stay as he said them. So does anything on the guide's kept list.
4. Write one version with a dealt move. Say it, hear what is off, try it again, keep the last. If nothing beats the
   original, it stays: record it with `use --move keep`.
5. Search the book for the new words (`find_in_book.py OUT/v6.txt find "phrase"`) so the fix repeats nothing.
6. Record each with `use` (status `proposed`).
7. **Show CT before and after, in book order, a batch at a time.** Nothing is logged without his yes. On his yes, log
   one edit per chapter by `EDIT-LOGGING-PROCEDURE.md` (EDITS.md, an ops row and a check row for each change, the scene
   sheet's word counts) and set the ledger lines to `logged (edit N)`. On his no, `rejected`, with his words in Note.
8. No em dashes or en dashes. No mirrored contrast in new wording. Do not make a line cleverer or tighter (guide,
   section 6). CT: "DO NOT OVERDO IT."

## What CT has already ruled on (27 Nov)

- He asked whether Claude had been heavy-handed where a thing could be implied. Of six explaining lines he kept five
  and reworded one (edit 300). A line that explains "something that's maybe a little bit confusing" stays, and so does
  one that "helps explain the intensity of the moment". Do not cut an explaining line on Claude's taste.
- "The way" can become "how": "how it usually did".

## Where Chapter 11 stands

Run as a trial with readers (their notes: `drafts/habits-ch11-readers-2026-11-27.json`). 16 lines, 12 judged fine.
Nothing from it is logged. In the ledger:

- Row 3, the kitchen: CT's wording, "Then she smiled, and the whole kitchen came up a notch, how it usually did."
  **Not logged.** He gave the wording and did not say log it; ask once, or log it with the first batch he approves.
- Rows 10, 11, 12 and 14 (the arms, the thermos, Gus): Claude's proposals. CT: "I'm not convinced by your first
  attempt." Not accepted. Claude then offered other moves for each (now in `habits-moves.json`) and asked which sound
  right; he has not said. Put them to him again with the Chapter 12 and 13 batch, or leave them.
- Left alone on purpose: the melon ("the way she looked over a melon at the market") and the pie a page later ("the way
  Elijah's mother looked at a pie"). Two of three readers took the pie as a callback.

## From the repeat finder (not acted on)

`repeats` turns up phrases outside the eight habits. Some are plants the book means ("is my stuff in that thing",
Priya's pencil, "Power or brain. Halve it."). Others are worth CT's eye when the habits are done: "looked down the
table at" (5), "didn't have an answer for that" (4), "he heard how it sounded" (4), "put his hand flat on" (4),
"for the first time in" (6). Nothing here has been shown to him yet.
