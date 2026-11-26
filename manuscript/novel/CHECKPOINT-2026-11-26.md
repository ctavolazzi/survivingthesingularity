# Checkpoint: the novel on the night of 26 November 2026

Written at CT's request at the end of the eighth logging chat: "let's create a checkpoint, a moment in time to really
pause and reflect, and then a continuation prompt for a new chat." Sections 1 to 4 are the pause. Section 5 is the
prompt to paste into the new chat.

## 1. Where the book is

- The book is still the Google Doc "StS v6 draft (Nov 25)". Edits 1 to 138, 141 and 151 are in it. Edits 139, 140 and
  142 to 220 (except 151) are logged in GitHub only. Neither Doc has been changed.
- `make_v6.py` builds the whole book from the v5 Doc and passes all 220 check rows. `verify.py` on the v6 Doc shows the
  nine expected PARTIAL rows (19, 30, 125, 131, 135, 137, 182, 197, 201). `build_gate.py` says READY for its lines.
- 99,399 words. CT, 26 Nov: "I don't care how long it gets I want it to be good."
- **The next edit is 221.**

## 2. What happened today, in order

1. Chapters 23, 24 and 26 written (202 to 204), then the plan for the endgame (plan, sections 10 to 13).
2. CT's direction on Grace's father, the war on the phones, Curtis the Trekkie, and the arms kept at Richard Praether's.
   The Praether scene went into Chapter 17 (205).
3. Chapters 27 to 36 written (206 to 215). Scenes with only women: the grange hall kitchen (Ch 29), Priya and Grace
   (Ch 30).
4. The story measured with code (`story_report.py`) and read by five readers; the report is
   `STORY-REPORT-2026-11-26.md`. About 23 continuity errors fixed.
5. The two rovers: the small one bought in Chapter 26, the tall one voted in in Chapter 34, CT's kitchen scene to end
   that chapter, "the new rover" in Chapter 38 (216).
6. CT's eight choices: the arms at Praether's in Chapter 37 (217), Devendra's "Dinner's on me!" in Chapter 39 (218),
   continuity in Chapters 11, 13, 15 and 19 (219), "Pondwater" as its own chapter with Grace's father said on the
   blanket, Praether's war at his mailbox, one line at the truck stop.
7. CT's last direction: Praether's lines as a pop-culture homage with the twist at the mailbox (205, corrected), and
   Lou's "ace in the hole" scene opening Chapter 18 (220).

## 3. Reflection: what is strong, and what is still thin

Measured from the text of this commit (`story_report.py`, `find_in_book.py`), then read.

**Strong now.** Every chapter from 20 to 36 costs somebody something, and the next one opens on it. Denny leaves and
comes back. The Ochoas leave and don't. The fire's lines all have setups. Elijah and Grace have a first kiss that was
waited for, in a chapter with its own name.

**Still thin, in order of how much a reader would feel it:**

1. **Praether.** He now has the loudest entrance in the book, and after his mailbox in Chapter 26 he is never on the
   page again. His warning comes true in Chapter 34 and he isn't there. Elijah leaves the arms in his barn in Chapter
   37 without a word between them.
2. **Mrs. Delgado.** The fire is fought over her insulin. She is on the page once before it and never after it. The
   reader never learns whether her box came.
3. **Aaron Bidwell.** Four "Meanwhile" sections, the last after Chapter 31, and no last beat. He is not in Chapters 37
   to 39. That he and Lou are cousins is only in the Appendix.
4. **Marta's shoulder and the welder gap.** It opens in Chapter 29 ("WELDER FOR THE GAP: UNRESOLVED"), runs to Chapter
   31, and is closed only by implication when Tyler bends his weld in Chapter 37.
5. **Faith,** Grace's sister: named twice (Chapters 22 and 33). Now that Grace has said her father aloud, Faith is the
   name left hanging.
6. **The Telecaster.** Pawned in Chapter 15, "still in a pawnshop window" in Chapter 25, remembered in "Pondwater."
   He plays a borrowed guitar in Chapter 37. His own never comes back.
7. **Wren.** Nine mentions in Chapter 20, then one in the next ten chapters, then she matters at the table in
   Chapter 38.
8. **"For three years he had told her there wasn't one"** (Chapter 37, about Barry) holds only from Chapter 13.

None of these is fixed. Each is CT's to rule on.

## 4. What is open with CT

- The women's scene about the tall rover (Chapter 34). His direction is in `TODO.md`, section 1. Two things were asked
  and not answered: does he have the older woman's line, and is the treasurer Reuben or a woman. Claude said it would
  write her line and keep Reuben unless told otherwise.
- The eight thin places above.
- The ending lines still open (plan, section 13): "It should have felt like traveling light," the gas cap at
  Thanksgiving, the Appendix (cast and timeline), the line flags in Chapters 37 to 39.
- The Instagram synopsis: four things it says that the book doesn't do.
- The name of the next Doc ("v7" is taken by a frozen side copy), and how the final copy is made.
- The smell pass: CT will do it in a new chat just for smell.
- Offered and not chosen: Grace and Lupe on the page (Ch 23), Grace and Mrs. Delgado on the page (Ch 32), the year of
  waiting as two short scenes (Ch 26).

## 5. The prompt for the next chat

```
We're finishing my novel, Surviving the Singularity. This is the ninth logging chat. Spin up before you do anything else:

1. Work on branch claude/singularity-publication-build-kparqk in both repos (ctavolazzi/survivingthesingularity and
   ctavolazzi/_workbench). Push every commit there, whatever branch this chat was given. Don't open or watch pull
   requests.
2. Read, in this order: manuscript/novel/REFERENCE.md (start at section 1), manuscript/novel/CHECKPOINT-2026-11-26.md,
   manuscript/novel/TODO.md, and all of manuscript/novel/WRITING-INSTRUCTIONS.md. Then STATE.md and the newest entry in
   sessions/LOG.md in _workbench.
3. The book is the Google Doc "StS v6 draft (Nov 25)", id 11nzQG2J-FciJ1XvU2LoPNTboL2N7pBVA0Dy-YCxqGuM. Its base is the
   v5 Doc "StS v5 draft (Nov 23)", id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA. Read both with the Docs connector and
   save the reads to your scratchpad. Do not change either Doc; I haven't cleared that.
4. Run make_v6.py on the v5 read and verify.py on the v6 read. You should get all 220 check rows passing and nine
   PARTIAL rows (19, 30, 125, 131, 135, 137, 182, 197, 201). If you get anything else, stop and tell me.

Where we are (end of 26 Nov): Chapters 20 to 36 are rewritten and logged in GitHub only (edits 198 to 220). My eight
choices are in. "Pondwater" is its own chapter. The arms are in Praether's barn. The next edit is 221. What is thin and
what is open is in the checkpoint file, sections 3 and 4.

Next up: the scene in Chapter 34 where the women weigh the taller rover (my direction is in TODO.md, section 1). After
that, the thin places in the checkpoint, one at a time, each on my yes.

How I want it done:
- Just do it. Write the chapter or the scene, run the checklist in WRITING-INSTRUCTIONS.md, log it (EDITS.md, a check
  row, ops rows, a record in manuscript/novel/drafts/), run make_v6.py, commit, push. Then tell me in a few lines what
  changed, every fact you invented, and anything that touches another chapter.
- My words go in word for word and are marked mine. Mark what you worded. My notes that aren't for the page never go in
  the text.
- When I correct you, change the thing I named, keep the rest, and add the lesson to WRITING-INSTRUCTIONS.md in the same
  turn. A correction to an edit that isn't in the Doc replaces it in place. An edit that is in the Doc gets a new row.
- Push back on continuity errors, contradictions and anything that confuses the reader. Not on my taste or my decisions.
- Read the pages before you claim anything about the book. Use the code (find_in_book.py, story_report.py,
  build_gate.py) instead of tokens. Use readers for sweeps and audits, and check every quote they return.
- Length is not the measure. I want it to be good.
- A question from me gets an answer, not an action. Answer first, short. No em dashes.
- The smell pass is its own chat. Don't start it here.
- The PDF I have is still the one with edits 1 to 186. Make a new one only when I ask.
- At the end: update "Where things stand" and "What is still open" in EDIT-LOGGING-PROCEDURE.md, TODO.md,
  WRITING-INSTRUCTIONS.md, and STATE.md and sessions/LOG.md in _workbench, and refresh the Drive mirror of the edit list
  once.

When you're done spinning up, tell me in one line that you're ready and that the next edit is 221.
```
