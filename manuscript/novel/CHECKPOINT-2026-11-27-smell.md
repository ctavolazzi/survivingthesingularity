# Checkpoint: the end of the smell chat (twelfth), 27 November 2026

CT: "Get ready to close out this session. The next sense for the next session is taste. Write a continuation prompt."

## Where the book is

- **In the Google Docs:** "StS v8 draft (Nov 26)" (`1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8`) holds edits 1 to
  223. Its locked twin is "StS v8 BACKUP (Nov 26), do not edit". Neither was touched in this chat.
- **In GitHub only:** edits 224 to 236. `make_v6.py` on the v5 read passes all 236 check rows (611 replacements).
  `verify.py` on the v8 read: 223 "accepted", 224 to 236 "not in the Doc", nothing PARTIAL. **The next edit is 237.**
- 103,647 words in the chapters (`story_report.py`). `build_gate.py`: NOT READY, 10 open boxes (the taste pass is one).
- **The PDF CT has** is still the edits 1 to 223 one. A new one is made only when he asks.
- **Drive copy of the edit list:** "StS edit list, edits 1 to 236 (mirror of GitHub)",
  `1YL7Tdov_VVfBSC2OtsUk2frzlw3DnZiHEqyznvVMRSE`. The 1 to 233 copy is "OLD:".
- **Backup** of this branch as it stood before the smell chat: `backup/book-branch-2026-11-27`, both repos.

## What this chat did

1. Spin-up from fresh reads of both Docs (clean), then read the whole built book.
2. `smell-table-2026-11-27.md`: every smell on the page, whose words it is, what it does, CT's call (last column).
3. Edit 235, the smell of the truck (Ch 15), and edit 236, the smell of the high-dollar party (Ch 9), in CT's words
   from `WRITING-INSTRUCTIONS.md` 7a. Record: `drafts/edit-235-236-smell.md`. Edit 235 was corrected in place after he
   approved it (his phrase "the smell of a car you've been living in" restored, "weed" made "smoke"); it was logged
   before he saw the new wording and shown to him after.
4. His correction and lesson: "which had held on to just about every order ... only a Sith deals in absolutes"
   (`WRITING-INSTRUCTIONS.md` 15c, with two of Claude's own lessons beside it).
5. A tool: `manuscript/tools/edits-v6/whose_words.py` (where a line came from). It finds the record; it does not
   judge it.
6. Lessons for the next chat in `REFERENCE.md`, section 6 ("Learned in the smell chat").

## Open with CT (his to decide; put to him only when he asks)

From this chat:
1. The corrected wording of edit 235 (not ruled on), and Claude's invented details in 235 and 236 (smoke, a wet
   jacket, the delivery bag; the two men behind the woman's chair; fish and butter).
2. The open rows of the smell table: the cooked plugs (Ch 21) and Priya's pits (Ch 26), which need the smell from
   him; woodsmoke reaching Grace at the door before the gate story (Ch 24, one line); Elijah telling Grace what the
   Thanksgiving coats bring back (Ch 27, a short exchange, new material).
3. The scene sheet's word counts for rows 29 and 48 (100 and 48 words short) and its title ("edits 1 to 233").
4. `main`'s `BRIDGE.md` and `WORKBOARD.md` still say v4, so a chat that starts on `main` is misled. Fixing them means
   a merge to `main`, which redeploys the site: his call.

Everything older is in `CHECKPOINT-2026-11-27-eleventh.md`, "Open with CT".

## Taste in the book now (measured 27 Nov, `find_in_book.py`, edits 1 to 236)

Seven real tastes, nearly all "tasted like X": the beer "tasted like nothing" (Ch 0, the toast); the cigarette
"tasted like the best nights of his twenties" (Ch 10, which starts a memory he shares); the peanut butter sandwich
"so fast he barely tasted it" (Ch 15); Rosa's tamales "don't taste too good" if over-prepared (Ch 27); the tea "tasted
like dirt and ginger" and "He could still taste the tea" (Ch 31). Food is everywhere and almost never tasted: Ma's
ice cream, Grace's soup, the frozen yogurt, Lou's tomatoes, Rosa's conchas and tamales, the lamb of the bet, the
free beer at the end. Whose words each one is has not been checked.

## The prompt for the next chat (the taste pass)

```
We're finishing my novel, Surviving the Singularity. This is the thirteenth chat: the taste pass. Spin up before you
do anything else:

1. Work on branch claude/singularity-publication-build-kparqk in both repos (ctavolazzi/survivingthesingularity and
   ctavolazzi/_workbench). Push every commit there, whatever branch this chat was given; I've said yes to that. Don't
   open or watch pull requests. Another chat may be logging on the same branch: fetch it first, read the "Next edit"
   line in manuscript/novel/TODO.md before you number anything, fetch again before every commit, and merge, never
   force-push. Ignore BRIDGE.md and WORKBOARD.md on main; they're out of date.
2. Read, in this order: manuscript/novel/REFERENCE.md (start at section 1, and read section 6), manuscript/novel/
   CHECKPOINT-2026-11-27-smell.md, manuscript/novel/TODO.md, and all of manuscript/novel/WRITING-INSTRUCTIONS.md
   (7a is the senses, 4a is how I work a line, 15c is the newest lessons). Then manuscript/novel/
   smell-table-2026-11-27.md and drafts/edit-235-236-smell.md: that's how the smell pass was done, and the taste pass
   works the same way. Then STATE.md and the newest entry in sessions/LOG.md in _workbench.
3. The book is the Google Doc "StS v8 draft (Nov 26)", id 1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8. Its base is the
   v5 Doc "StS v5 draft (Nov 23)", id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA. Read both with the Docs connector
   and save the reads to your scratchpad. Do not change either Doc, or the locked "StS v8 BACKUP (Nov 26), do not
   edit"; I haven't cleared that.
4. Run make_v6.py on the v5 read and verify.py on the v8 read. You should get all 236 check rows passing (611
   replacements), 223 rows "accepted" in v8, edits 224 to 236 "not in the Doc", and nothing PARTIAL. If you get
   anything else, stop and tell me.

Where we are (end of 27 Nov): v8 holds edits 1 to 223. Edits 224 to 236 are logged in GitHub only. The next edit is
237. After this I don't really want to change or add anything: it's about refining, revising, deleting, buffing out
the hard spots, polishing.

The job: the taste pass. Taste only someone who was there would know, with a verb that carries the physics, where it
carries the feeling or tells you something about the person, not one per page. If I haven't given you my own taste
lines, ask me for them in one short question before you propose any of yours; the smell pass worked because the two
lines that went in were mine. Then read the whole built book and make a short taste table like the smell table: only
the scenes with a taste on the page now, plus a few real candidates, with whose words each one is
(whose_words.py, then the record). Cut the candidates down before you show me. Show me every line before it's logged,
and show me again if you change it after I've said yes.

How I want it done:
- What I say in the chat is the job, even when a file says something different.
- A question from me gets an answer, not an action. Answer first, short. No em dashes.
- I dictate, you log. My words go in word for word and are marked mine; keep my phrase whole when you place it. Take
  the dictation fillers out. Mark what you worded, and list every fact you invented.
- No absolutes where one can't be true (15c).
- Read the pages before you claim anything about the book, and check a doubt against the page before acting on it
  too. Use the code (find_in_book.py, story_report.py, openers.py, whose_words.py) instead of tokens.
- Push back on continuity errors, contradictions and anything that confuses the reader. Not on my taste or my
  decisions.
- When I correct you, change the thing I named, keep the rest, and add the lesson to WRITING-INSTRUCTIONS.md in the
  same turn.
- Stay on the novel. Nothing gets trashed or deleted without my yes; old copies get "OLD:" in front. Make a PDF only
  when I ask.
- The smell table's open rows and the rest of "Open with CT" wait until I ask for them.
- At the end: update "Where things stand" and "What is still open" in EDIT-LOGGING-PROCEDURE.md, TODO.md,
  WRITING-INSTRUCTIONS.md, and STATE.md and sessions/LOG.md in _workbench; refresh the Drive mirror of the edit list
  once (upload EDITS.md as text/plain); write the next checkpoint and prompt.

When you're done spinning up, tell me in one line that you're ready and that the next edit is 237.
```
