# Checkpoint: the end of the smell chat (twelfth), 27 November 2026

CT: "Get ready to close out this session. The next sense for the next session is taste. Write a continuation prompt."

## Where the book is

- **In the Google Docs:** "StS v8 draft (Nov 26)" (`1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8`) holds edits 1 to
  223. Its locked twin is "StS v8 BACKUP (Nov 26), do not edit". Neither was touched in this chat.
- **In GitHub only:** edits 224 to 240. `make_v6.py` on the v5 read passes all 240 check rows (618 replacements).
  `verify.py` on the v8 read: 223 "accepted", 224 to 240 "not in the Doc", nothing PARTIAL. **The next edit is 241.**
  (Edits 237 to 240 were logged after this checkpoint was first written: three new scenes in Chapter 26, a new
  ending for "Pondwater" and a new scene in Chapter 27. They have not been read in place, in order.)
- 104,974 words in the chapters (`story_report.py`), 142 scenes. `build_gate.py`: NOT READY, 10 open boxes (the taste pass is one).
- **The PDF CT has** is still the edits 1 to 223 one. A new one is made only when he asks.
- **Drive copy of the edit list:** "StS edit list, edits 1 to 236 (mirror of GitHub)",
  `1wHTtGSP7LjG0xJT5dixGKcXomXNVOPY1559H1dPGT_I`. The 1 to 233 copy is "OLD:".
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
7. After the prompt below was written, CT asked for more:
   - **The knowledge sheet** (who knows what, and when): `knowledge-sheet-2026-11-27.md`, three CSVs, the tool
     `knowledge.py`, and the Google Sheet "Surviving the Singularity: who knows what (edits 1 to 236)"
     (`11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`). 35 secrets, 113 lines of evidence, eight findings for him.
   - **Five story checks** (CT, 27 Nov: "what other spreadsheets could we use ... filling any holes, finding any
     gaps"). Order agreed: the calendar, the money, objects, plants and payoffs, all five senses in one table. Each
     ends in a short findings list with the smallest fix to text already there (CT: "if we need to add more scenes,
     we can. But at this point, I'd rather just revise what we already have"); a hole that only a scene can close is
     flagged for him. **Done: the calendar** (`calendar-2026-11-27.md`, `story_checks.py calendar`, Google Sheet
     `11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`): 23 checks hold, 3 known slips do not, 2 new ones to read, and
     Elijah's age turns out to be consistent and to set his birthday between about 3 March and mid May. **Next: the
     money.** Build each as a new command in `story_checks.py`, from the page, the way `knowledge.py` is built.
   - **The conversation map** (CT, 27 Nov), in two layers. **Layer one is built** (`conversations-2026-11-27.md`,
     `story_checks.py conversations`, Google Sheet `11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`): who speaks in each scene, pairs,
     lines by chapter, and sense words (551 sound, 370 touch, 17 smell, 14 taste; 122 of 137 scenes have no smell
     word). Speaker counts are rough (10% of lines not placed; an unnamed "he" is given to Elijah). **Layer two is for
     the next chat, from a fresh read:** what each conversation that matters does for the two people in it. First
     lead: Grace and Lou barely talk on the page before Chapter 34 tests them. It takes the place of the separate
     senses sheet, and goes ahead of the money and objects sheets.
   - **A new scene from CT, logged as edit 237:** Curtis and Priya argue over the CEO of PorusAI on the screen (fired and
     taken back); Grace and Elijah walk out; her father and the TV; "Elijah, do you personally know a billionaire?"
     His words and what the page gives it are in `next-version-scenes-2026-11-26.md`, section 4. The CEO's name is
     **Miles Renner** (Claude's pick at CT's word, 27 Nov; "Renner" is not in the book). CT decided against adding
     the chips, an IPO or a bought off-grid AI: "we don't need to add more to the story. There's already so much
     here." Also his, same day: the eighteen days should read as a government ban, not an outage (Ch 26, 38, Appendix
     wording).
   - **Two more smell lines drafted and shown, not logged** (he asked for the drafts and has not said to log them):
     Ch 25, after "So did I.": "The heat came out the door at him with celery and butter in it, and a pot of turkey
     necks going for the gravy. Ma put hers on the night before, too." (all Claude's; invented: celery, butter, the
     necks, Ma's habit). Ch 27: "Their coats had soaked up **Rosa's cooking** all afternoon, sage and turkey fat, and
     the little room filled with **the heavenly scent** of it the minute the door shut." (bold is CT's, 27 Nov).
     If he says yes they are edits 237 and 238.
   - **The birthday.** The scene is drafted in `next-version-scenes-2026-11-26.md` (section 2) and is not in the book.
     His new plan for it (27 Nov) is recorded at the end of that section. Open question to him: how Grace finds out.

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

5. The eight findings at the foot of `knowledge-sheet-2026-11-27.md` (first among them: Grace never says "why did
   you pretend to be poor", and the fire never mentions the hiding).
6. The five findings in `calendar-2026-11-27.md` (three known slips with a smallest fix each, two new to read).
7. The Ch 25 and Ch 27 smell drafts (log them or not), and the birthday plan (how Grace finds out; then the scene
   moves to spring 2026).

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
   works the same way. Then manuscript/novel/knowledge-sheet-2026-11-27.md (who knows what, and when); check it
   before you place any line. Then STATE.md and the newest entry in sessions/LOG.md in _workbench.
3. The book is the Google Doc "StS v8 draft (Nov 26)", id 1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8. Its base is the
   v5 Doc "StS v5 draft (Nov 23)", id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA. Read both with the Docs connector
   and save the reads to your scratchpad. Do not change either Doc, or the locked "StS v8 BACKUP (Nov 26), do not
   edit"; I haven't cleared that.
4. Run make_v6.py on the v5 read and verify.py on the v8 read. You should get all 240 check rows passing (618
   replacements), 223 rows "accepted" in v8, edits 224 to 240 "not in the Doc", and nothing PARTIAL. If you get
   anything else, stop and tell me.

Where we are (end of 27 Nov): v8 holds edits 1 to 223. Edits 224 to 240 are logged in GitHub only. The next edit is
241. After this I don't really want to change or add anything: it's about refining, revising, deleting, buffing out
the hard spots, polishing.

The first job, before anything else: read the end of Chapter 25 through Chapter 27 in the built book, in order. Edits
237 to 240 put five new scenes and a new ending for "Pondwater" there in one night and nobody has read them in place.
Look for: who runs the route while Grace is away for the winter; any line that says she came back; whether her
winter trip and the October festival read as two trips; and anything the knowledge sheet says a person shouldn't
know yet. Tell me what you find before changing anything.

Then the job: the taste pass. Taste only someone who was there would know, with a verb that carries the physics, where it
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

When you're done spinning up, tell me in one line that you're ready and that the next edit is 241.
```
