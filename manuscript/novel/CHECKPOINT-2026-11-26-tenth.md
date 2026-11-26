# Checkpoint: the end of the tenth logging chat, 26 November 2026

CT: "This is a checkpoint and conversation prompt. This is the end of this session and the beginning of the next. An
opportunity to do some housekeeping, button it all up, and then let's move on into a fresh conversation."

## Where the book is

- **In the Google Docs:** "StS v8 draft (Nov 26)" (`1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8`) holds edits 1 to
  223. Its locked twin is "StS v8 BACKUP (Nov 26), do not edit". Neither was touched in this chat.
- **In GitHub only:** edits 224 to 227. `make_v6.py` on the v5 read builds the book with all of them and passes all
  227 check rows. `verify.py` on the v8 read: 223 "accepted", and 224, 225, 226 and 227 "not in the Doc". **The next
  edit is 228.**
- **The PDF CT has** is still "StS v8 large print CURRENT (26 Nov, edits 1 to 223, the continuity pass).pdf". It does
  not have edits 224 to 227. A new one is made only when he asks.
- 101,092 words in the chapters (`story_report.py`, after edit 227).

## What this chat did

1. The housekeeping list from `CHECKPOINT-2026-11-26-v8.md`: the sentence-opening checker CT asked for on 25 Nov
   (`manuscript/tools/edits-v6/openers.py`); `NEXT-BUILD.md`, `GOALS.md`, the plan, the story report's numbers, the
   `EDITS.md` header, the status table and the writing instructions' debts brought up to v8; `STATE.md`'s book items
   checked. The build gate's lines all pass; it waits only on open boxes in `TODO.md`.
2. Edit 224: Curtis shows the table a laser weeder run by a brain organoid, in "Pondwater" (CT's scene).
3. Edit 225: Chapters 8 to 10. The panel goes further ("That's what the math says"), Elijah tells Ruby he is
   overwhelmed, fifty million views, Ruby's pitch before the offer (CT's dictation).
4. Edit 226: why Elijah waits after the pond, Chapter 26 (CT's words).
5. Edit 227: the polish pass at key moments. Four readers, 50 candidates, 20 places fixed, all Claude's wording.
6. `WRITING-INSTRUCTIONS.md`, section 4a: how CT works a line.

Records: `EDITS.md` (224 to 227), `drafts/edit-224-organoids.md`, `drafts/edit-225-panel-and-ruby.md`, the foot of
`drafts/chapter-26.md`, `drafts/polish-2026-11-26.md`.

## Open with CT (ask in one grouped list; each is his)

From this chat's edits:
1. **Edit 226's held line.** "It took under 6 months for him to change his mind." The pond is November 2025 and the
   amp night is October 2026 (eleven months), fixed by Grace's festival, Marta's "a year ago", the June and July scenes
   and Chapter 27. Should it say "under a year", or stay out?
2. **Grace goes away that winter** (his idea, not written). The book has nothing between Thanksgiving 2025 and the
   spring beds, so a few weeks away opens Chapter 26 with no dates moved. His lines: "for real? Like, you're the one
   that's leaving?" / "I'm just going away for a little while, like I do every year. I'm gonna hang out with my girls.
   I'm gonna see my family, my sister ..." The sister is Faith (Ch 22). Claude's recommendation on the father: one line
   that she won't be stopping at her dad's, and the full story stays on the blanket in "Pondwater" (his own words there
   say she let go of him long ago). Waiting on his go.
3. **Five lines from the polish pass** (`drafts/polish-2026-11-26.md`, "Left as it is"): four mirrored lines in done
   chapters (Ch 0 "it wasn't a client. It was the tide."; Ch 4 "The error wasn't the units. The error was the ladder."
   and "a mural of knowledge"; Ch 5 "Intelligence wasn't magic. Intelligence was energy, arranged."; Ch 16 Marta's
   "That's not a limitation, spreadsheet. That's the load-bearing wall."), and Ch 36 "didn't know which one of them
   he'd helped" (who is "them"?).
4. **Edits 224 to 227 into the Doc.** They are logged only. When he clears them: as suggestions in the v8 Doc, or a new
   copy; and a new large print PDF when he asks.

Carried over from the housekeeping list (asked in this chat, not answered):
5. The gas cap line (Ch 25): add it, or keep the scene ending on "Friday," she said.
6. "Marta had heard it as a murder" (Ch 39): keep, or "Marta had told him he told it like a murder."
7. "No bills, except my phone, which at this point more or less pays for itself with the Creator Fund." His line, not in
   the book since the arms moved to Praether's. Drop it or place it.
8. The 19 empty paragraphs in the v8 Doc where the pictures were (the book has no pictures). They would each print as a
   stray scene break if anything were built from that Doc. The PDF he has is clean. Take them out, or leave v8 alone.
9. The thin places still open: Praether after Chapter 26, Mrs. Delgado after the fire, Bidwell's last beat, the welder
   gap, the Telecaster. (Faith closes if item 2 is written.)
10. The Instagram synopsis: neither the synopsis nor the "four things" is saved in the repo. If he wants it fixed, he
    pastes it.
11. "OLD:" on the v6 and v7 Docs.
12. Drive, "Older builds": about 52 unlabeled v5 build files from 25 Nov, roughly seven copies of each. Trash the extra
    copies, or leave them.
13. The site's private reader holds v2 and its compendium v3. Updating them needs a new export script from the v8 text,
    six compendium entries rewritten, the site checks, and a merge to `main`, which goes live.
14. Whether the branch goes to `main` (406 commits ahead at the start of this chat; merging deploys the site).
15. The ISBN, and the release build (print, large print, EPUB).

Not for this list: the smell pass is its own chat.

## The prompt for the next chat

```
We're finishing my novel, Surviving the Singularity. This is the eleventh logging chat. Spin up before you do anything
else:

1. Work on branch claude/singularity-publication-build-kparqk in both repos (ctavolazzi/survivingthesingularity and
   ctavolazzi/_workbench). Push every commit there, whatever branch this chat was given. Don't open or watch pull
   requests.
2. Read, in this order: manuscript/novel/REFERENCE.md (start at section 1), manuscript/novel/CHECKPOINT-2026-11-26-tenth.md,
   manuscript/novel/TODO.md, and all of manuscript/novel/WRITING-INSTRUCTIONS.md. Then STATE.md and the newest entry in
   sessions/LOG.md in _workbench.
3. The book is the Google Doc "StS v8 draft (Nov 26)", id 1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8. Its base is the
   v5 Doc "StS v5 draft (Nov 23)", id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA. Read both with the Docs connector
   and save the reads to your scratchpad. Do not change either Doc, or the locked "StS v8 BACKUP (Nov 26), do not
   edit"; I haven't cleared that.
4. Run make_v6.py on the v5 read and verify.py on the v8 read. You should get all 227 check rows passing, 223 rows
   "accepted" in v8, edits 224 to 227 "not in the Doc", and nothing PARTIAL. If you get anything else, stop and tell me.

Where we are (end of 26 Nov): v8 holds edits 1 to 223. Edits 224 to 227 are logged in GitHub only (the laser weeder and
the brain organoid, the panel and Ruby, why Elijah waits, the polish pass). The PDF I have is "StS v8 large print
CURRENT (26 Nov, edits 1 to 223, the continuity pass).pdf"; it doesn't have 224 to 227. The next edit is 228. What is
open with me is in the checkpoint file, "Open with CT".

First: show me the "Open with CT" list in one grouped message, short, and wait for my answers. Then do what I answer.

How I want it done:
- Just do it. Anything that changes the book is logged the usual way (EDITS.md, a check row, ops rows, a record in
  manuscript/novel/drafts/), make_v6.py, commit, push. Then tell me in a few lines what changed, every fact you
  invented, and anything that touches another chapter.
- My words go in word for word and are marked mine. When I restate a line, the last version is the line. Take the
  dictation fillers out. Mark what you worded.
- When something I ask depends on a condition, check the pages for it, tell me what's in the way, log the rest and hold
  the one line.
- When I correct you, change the thing I named, keep the rest, and add the lesson to WRITING-INSTRUCTIONS.md in the
  same turn.
- Read the pages before you claim anything about the book. Use the code (find_in_book.py, story_report.py,
  build_gate.py, openers.py) instead of tokens. Check every quote a reader returns.
- A question from me gets an answer, not an action. Answer first, short. No em dashes.
- The smell pass is its own chat. Don't start it here.
- Nothing gets trashed or deleted without my yes; old copies get "OLD:" in front.
- Make a PDF only when I ask.
- At the end: update "Where things stand" and "What is still open" in EDIT-LOGGING-PROCEDURE.md, TODO.md,
  WRITING-INSTRUCTIONS.md, and STATE.md and sessions/LOG.md in _workbench, and refresh the Drive mirror of the edit list
  once.

When you're done spinning up, tell me in one line that you're ready and that the next edit is 228.
```
