# Checkpoint: the end of the smell chat (twelfth), 27 November 2026

CT: "Get ready to close out this session. The next sense for the next session is taste. Write a continuation prompt."

## Where the book is

- **In the Google Docs:** "StS v8 draft (Nov 26)" (`1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8`) holds edits 1 to
  223. Its locked twin is "StS v8 BACKUP (Nov 26), do not edit". Neither was touched in this chat.
- **In GitHub only:** edits 224 to 241. `make_v6.py` on the v5 read passes all 241 check rows (619 replacements).
  `verify.py` on the v8 read: 223 "accepted", 224 to 241 "not in the Doc", nothing PARTIAL. **The next edit is 242.**
  (Edits 237 to 240 were logged after this checkpoint was first written: three new scenes in Chapter 26, a new
  ending for "Pondwater" and a new scene in Chapter 27. They have not been read in place, in order.)
- 104,977 words in the chapters (`story_report.py`), 142 scenes. `build_gate.py`: NOT READY, 10 open boxes (the taste pass is one).
- **The PDF CT has** is still the edits 1 to 223 one. A new one is made only when he asks.
- **Drive copy of the edit list:** "StS edit list, edits 1 to 236 (mirror of GitHub)",
  `1iMTDBkZeVOphVySnKMBNRHNZO2stZrsaUYi7VgRcZXc`. The 1 to 233 copy is "OLD:".
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

## Everything open with CT at the very end of the chat (27 Nov, late). This list is the current one.

Put to him only when he asks, except the first, which is the first job of the next chat.

1. **Read the end of Chapter 25 through Chapter 27 in place.** Edits 237 to 241 were logged the night he dictated
   them. Look for: who runs the route while Grace is away for the winter; a line that says she came back; whether the
   winter trip and the October festival read as two trips.
2. **The confiding scene** (`next-version-scenes-2026-11-26.md`, section 7): his words are saved; not drafted. He
   liked the haywire rover as the bang, leading into the women's talk in Chapter 34 (October 2027). One thing he has
   not answered: who says "If that little guy only works half the time then maybe it's time we upgraded to something
   more heavy duty." Claude's pick is Marta, with Priya answering from her sheet.
3. **The Hinge profile and "maybe I'll be a spinstress after all"** (section 6): summer 2026, in Chapter 26. Not
   written.
4. **The birthday** (section 2): it passes unmarked in spring 2025, Grace finds out, the party is spring 2026. Open:
   how Grace finds out (Claude's suggestion: his letter to Ma in Chapter 25). Not moved or logged.
5. **Two smell drafts, shown and not logged:** Chapter 25 (the heat out the kitchen trailer door) and Chapter 27
   ("Rosa's cooking", "the heavenly scent"). And the open rows of `smell-table-2026-11-27.md`.
6. **Small fixes with a wording ready:** the three calendar slips ("since my first week", the squash, "ran out in
   June"), the two to read (`calendar-2026-11-27.md`), and the eighteen days reading as a ban, not an outage.
7. **The findings in `knowledge-sheet-2026-11-27.md`**, first among them that Grace never says "why did you pretend to
   be poor" and the fire never mentions the hiding (held since edit 234).
8. **Layer two of the conversation map and the desires sheet** (one reader's pass; CT asked for the desires sheet
   at the very end of the chat: "what the characters want, like maybe when they're introduced, how they're introduced,
   what they desire, what they're after"), then the money, objects, and plants and payoffs sheets.
9. **The taste pass.**
10. Claude's wording and invented details in edits 235 to 241, each listed in its record in `drafts/`.
11. Edits 224 to 241 into the Doc, and a new PDF, when he says. `main`'s `BRIDGE.md` and `WORKBOARD.md` still say v4.

## Taste in the book now (measured 27 Nov, `find_in_book.py`, edits 1 to 236)

Seven real tastes, nearly all "tasted like X": the beer "tasted like nothing" (Ch 0, the toast); the cigarette
"tasted like the best nights of his twenties" (Ch 10, which starts a memory he shares); the peanut butter sandwich
"so fast he barely tasted it" (Ch 15); Rosa's tamales "don't taste too good" if over-prepared (Ch 27); the tea "tasted
like dirt and ginger" and "He could still taste the tea" (Ch 31). Food is everywhere and almost never tasted: Ma's
ice cream, Grace's soup, the frozen yogurt, Lou's tomatoes, Rosa's conchas and tamales, the lamb of the bet, the
free beer at the end. Whose words each one is has not been checked.

## The prompt for the next chat (the thirteenth)

Written at the very end of the smell chat, on CT's word ("Write the continuation prompt for the next session"). It
replaces the earlier taste-pass prompt that stood here.

```
We're finishing my novel, Surviving the Singularity. This is the thirteenth chat. Spin up before you do anything else:

1. Work on branch claude/singularity-publication-build-kparqk in both repos (ctavolazzi/survivingthesingularity and
   ctavolazzi/_workbench). Push every commit there, whatever branch this chat was given; I've said yes to that. Don't
   open or watch pull requests. Another chat may be logging on the same branch: fetch it first, read the "Next edit"
   line in manuscript/novel/TODO.md before you number anything, fetch again before every commit, and merge, never
   force-push. Ignore BRIDGE.md and WORKBOARD.md on main; they're out of date.
2. Read, in this order: manuscript/novel/REFERENCE.md (section 1, then section 6), manuscript/novel/
   CHECKPOINT-2026-11-27-smell.md (its list "Everything open with CT at the very end of the chat" is the current one),
   manuscript/novel/TODO.md, and all of manuscript/novel/WRITING-INSTRUCTIONS.md (7a is the senses, 4a is how I work
   a line, 15c is the newest lessons, including "place it; don't audit it" and "move the people"). Then
   manuscript/novel/knowledge-sheet-2026-11-27.md (who knows what, and when) and
   manuscript/novel/next-version-scenes-2026-11-26.md, sections 4 to 8 (my dictation from 27 Nov, word for word).
   Then STATE.md and the newest entry in sessions/LOG.md in _workbench.
3. The book is the Google Doc "StS v8 draft (Nov 26)", id 1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8. Its base is the
   v5 Doc "StS v5 draft (Nov 23)", id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA. Read both with the Docs connector
   and save the reads to your scratchpad. Do not change either Doc, or the locked "StS v8 BACKUP (Nov 26), do not
   edit"; I haven't cleared that.
4. Run make_v6.py on the v5 read and verify.py on the v8 read. You should get all 242 check rows passing (621
   replacements), 223 rows "accepted" in v8, edits 224 to 242 "not in the Doc", and nothing PARTIAL. Then
   scene_sheet.py check against manuscript/novel/scene-sheet-2026-11-27.csv: 142 scenes, nothing different. If you
   get anything else, stop and tell me.

Where we are (end of 27 Nov): v8 holds edits 1 to 223. Edits 224 to 242 are logged in GitHub only. The next edit is
243. 105,307 words in 142 scenes. In Drive: the scene sheet (13hXnHxprSx-IGW_-TOFzeJFHIpzWyicHx_NtTgaya7o), the
story checks workbook (11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8: who knows what, the calendar, the conversation
map) and the edit list (1iMTDBkZeVOphVySnKMBNRHNZO2stZrsaUYi7VgRcZXc). I'd rather revise what we have than add, but
if a scene needs adding, we can.

The work, in this order:

1. Read the end of Chapter 25 through Chapter 27 in the built book, in order, and the truck scene in Chapter 17 (edit
   242). Edits 237 to 241 put five new scenes
   there in one night (Lou and Grace at the fence; Grace leaves for the winter; Miles Renner on the big screen; the
   pond ending on the near kiss; the weeks after, the pillow talk and Marta in the shop) and nobody has read them in
   place. Look for: who runs the route while Grace is away for the winter; any line that says she came back; whether
   her winter trip and the October festival read as two trips; anything the knowledge sheet says a person shouldn't
   know yet. Tell me what you find before changing anything.

2. Draft the scene I dictated where Elijah confides in Grace about his mother, the farm and Melody ("Nobody talks
   about my man like that"; her whisper, "I wish I could help you love yourself as much as I do"). My words are in
   next-version-scenes-2026-11-26.md, section 7. It goes in the week of Chapter 34, October 2027: the bang that wakes
   them is the little rover going haywire, and it leads into the women's talk about upgrading in Irene's kitchen.
   Still open: who says "If that little guy only works half the time then maybe it's time we upgraded to something
   more heavy duty." Ask me in one short question if I haven't said. Place it as I gave it; don't audit it. Show me
   the draft before it's logged.

3. One reading pass, from a fresh read of the whole book, for two sheets:
   - Layer two of the conversation map (conversations-2026-11-27.md): for each conversation that matters, what each
     person wants, what changes between them, and what it sets up or pays off. Start from the leads in that file
     (first: Grace and Lou barely talk before Chapter 34, now with the fence scene added).
   - The desires sheet I asked for. Two tabs. Characters: one row per person, with where and how they are introduced
     (the chapter, the scene and the first line that names them; a script can find those), what they want when we
     meet them, what they want by the end and the scene where it changes, and whether they get it. Scenes: one row
     per scene, for what each person in it is after. Start from manuscript/NOVEL-CHARACTER-BIBLE-2026-11-23.md
     ("surface want" and "real want" for 28 people) but check every want against the built book; it was written
     before Chapters 20 to 36 were rewritten and before tonight's edits.
   A quoted line for every want, found by the script, the way knowledge.py works. Add both as commands in
   manuscript/tools/edits-v6/story_checks.py, add them to the story checks workbook as more tabs, and end with a short
   list: a want set up and never paid, a person who wants nothing on the page, a change with no scene behind it. Each
   with a fix to text already there, or flagged for me if only a scene would close it.

4. Then whatever I pick from the open list in the checkpoint (the small calendar fixes, the eighteen days as a ban,
   the two smell drafts, the birthday, the Hinge profile, the taste pass, the money, objects and plants sheets). Don't
   put the list to me unless I ask for it.

How I want it done:
- What I say in the chat is the job, even when a file says something different.
- A question from me gets an answer, not an action. Answer first, short. No em dashes.
- I dictate, you log. My words go in word for word and are marked mine; keep my phrase whole and keep my order of
  events. Take the dictation fillers out. Mark what you worded, and list every fact you invented.
- When I hand you a scene I'm pleased with, place it. If it collides with the page, say so in one line with the fix.
- Say the time and how people got there before the image (WRITING-INSTRUCTIONS 15c, "move the people").
- No absolutes where one can't be true.
- Read the pages before you claim anything about the book, and check a doubt against the page before acting on it.
  Use the code (find_in_book.py, story_report.py, openers.py, whose_words.py, knowledge.py, story_checks.py,
  scene_sheet.py) instead of tokens.
- Show me every line before it's logged, and show me again if you change it after I've said yes.
- After every edit: make_v6.py, verify.py, and rebuild the sheets (scene_sheet.py check, story_checks.py calendar and
  conversations, knowledge.py). A new scene needs a scene sheet row and a calendar date.
- Push back on continuity errors, contradictions and anything that confuses the reader. Not on my taste or my
  decisions.
- When I correct you, change the thing I named, keep the rest, and add the lesson to WRITING-INSTRUCTIONS.md in the
  same turn.
- Stay on the novel. Nothing gets trashed or deleted without my yes; old copies get "OLD:" in front. Make a PDF only
  when I ask.
- At the end: update "Where things stand" and "What is still open" in EDIT-LOGGING-PROCEDURE.md, TODO.md,
  WRITING-INSTRUCTIONS.md, and STATE.md and sessions/LOG.md in _workbench; refresh the Drive copies once (the edit
  list as text/plain, the scene sheet, the story checks); write the next checkpoint and prompt.

When you're done spinning up, tell me in one line that you're ready and that the next edit is 243.
```
