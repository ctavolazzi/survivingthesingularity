# Checkpoint: v8, the night of 26 November 2026

Written at the end of the ninth logging chat. CT: "output a continuation prompt for a cleanup pass where we're tidying
up anything that, you know, still remains, any loose ends or whatever. Just a housekeeping pass."

## Where the book is

- **The book is the Google Doc "StS v8 draft (Nov 26)"**, made from `make_v6.py`'s build: every logged edit, 1 to 223.
  It has no pictures (19 empty paragraphs where they were; CT chose "No pictures" when the .docx with them was over
  the Drive connector's limit). Locked twin: "StS v8 BACKUP (Nov 26), do not edit".
- **The PDF CT reads:** "StS v8 large print CURRENT (26 Nov, edits 1 to 223, the continuity pass).pdf"
  (https://drive.google.com/file/d/1B0nwZM5XXGxfeEjRAjyl0bICQNxsHtGp/view), 738 pages, all build checks passing.
- This chat: 221 (the women weigh the tall rover, Ch 34), 222 (the whole-book continuity pass: eight readers, 79
  findings, 50 fixed), 223 (the held items resolved). Records: `EDITS.md`, `drafts/chapter-34.md`,
  `drafts/pass-2026-11-26.md`. **The next edit is 224.**

## Loose ends (the housekeeping list)

The novel:
1. The 19 pictures: back into v8 (the connector limit is about 3.1 MB a call; `make_v6.py` has `--small-pictures`
   and `--no-pictures`), or the 19 empty paragraphs taken out. CT's call.
2. Two lines CT has not ruled on: the gas cap (Ch 25; his scene ends on "Friday," she said.) and "Marta had heard it
   as a murder" (Ch 39).
3. The eight thin places in `CHECKPOINT-2026-11-26.md`, section 3, one at a time on his yes.
4. `TODO.md`'s open boxes: the Instagram synopsis, the sentence-opening checker, `build_gate.py` READY, the ISBN, the
   release build (PDF and EPUB).
5. The smell pass stays in its own chat.

The files:
6. "OLD:" on the v6 and v7 Docs, which are no longer the book (his Docs; ask once).
7. Stale copies in the bridge map: the site's private reader and compendium hold v2 and v3 (`node scripts/sts-bridge.mjs
   status`). Say what it would take; don't rebuild the site without his word.
8. `NEXT-BUILD.md`, `GOALS.md` and the plan still talk about "the next build" and v6 in places; bring them to v8.
   The story report and the plan's numbers (words, chapter counts) are from before edits 216 to 223.
9. Drive: the publication folder and "Older builds" tidy; nothing trashed without his yes.
10. `_workbench`: STATE.md's book items (launch kit, decisions, release build) checked against what is true now.
11. The branch `claude/singularity-publication-build-kparqk` is not merged; `main` deploys the site. Ask before any
    merge.

## The prompt for the next chat

```
We're finishing my novel, Surviving the Singularity. This is the tenth logging chat, and it's a housekeeping pass:
tidy up whatever still remains, the loose ends, nothing new. Spin up before you do anything else:

1. Work on branch claude/singularity-publication-build-kparqk in both repos (ctavolazzi/survivingthesingularity and
   ctavolazzi/_workbench). Push every commit there, whatever branch this chat was given. Don't open or watch pull
   requests.
2. Read, in this order: manuscript/novel/REFERENCE.md (start at section 1), manuscript/novel/CHECKPOINT-2026-11-26-v8.md,
   manuscript/novel/TODO.md, and all of manuscript/novel/WRITING-INSTRUCTIONS.md. Then STATE.md and the newest entry in
   sessions/LOG.md in _workbench.
3. The book is now the Google Doc "StS v8 draft (Nov 26)", id 1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8. Its base
   is the v5 Doc "StS v5 draft (Nov 23)", id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA. Read both with the Docs
   connector and save the reads to your scratchpad. Do not change either Doc, or the locked "StS v8 BACKUP (Nov 26),
   do not edit"; I haven't cleared that.
4. Run make_v6.py on the v5 read and verify.py on the v8 read. You should get all 223 check rows passing, and every
   row "accepted" in v8 with nothing PARTIAL. If you get anything else, stop and tell me.

Where we are (end of 26 Nov): v8 holds every edit, 1 to 223, without the 19 pictures. The PDF I'm reading is
"StS v8 large print CURRENT (26 Nov, edits 1 to 223, the continuity pass).pdf". The next edit is 224. The loose
ends are in the checkpoint file, "Loose ends".

What I want: go down the loose-ends list and close what you can without me. Ask me in one grouped list only for the
things that are mine to decide (my lines, my Docs, deleting or merging anything). Then do those on my answers.

How I want it done:
- Just do it. Anything that changes the book is logged the usual way (EDITS.md, a check row, ops rows, a record in
  manuscript/novel/drafts/), make_v6.py, commit, push. Then tell me in a few lines what changed, every fact you
  invented, and anything that touches another chapter.
- My words go in word for word and are marked mine. Mark what you worded.
- When I correct you, change the thing I named, keep the rest, and add the lesson to WRITING-INSTRUCTIONS.md in the
  same turn.
- Read the pages before you claim anything about the book. Use the code (find_in_book.py, story_report.py,
  build_gate.py) instead of tokens. Check every quote a reader returns.
- A question from me gets an answer, not an action. Answer first, short. No em dashes.
- The smell pass is its own chat. Don't start it here.
- Nothing gets trashed or deleted without my yes; old copies get "OLD:" in front.
- At the end: update "Where things stand" and "What is still open" in EDIT-LOGGING-PROCEDURE.md, TODO.md,
  WRITING-INSTRUCTIONS.md, and STATE.md and sessions/LOG.md in _workbench, and refresh the Drive mirror of the edit list
  once.

When you're done spinning up, tell me in one line that you're ready and that the next edit is 224.
```
