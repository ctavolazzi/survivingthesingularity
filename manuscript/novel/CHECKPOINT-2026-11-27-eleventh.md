# Checkpoint: the end of the eleventh logging chat, 27 November 2026

CT: "Make sure the spreadsheet is accessible to the next session. Then output instructions for a continuation of this
work in a new session." The next chat is the smell pass ("Anything else before we pass off to the smell chat?").

## Where the book is

- **In the Google Docs:** "StS v8 draft (Nov 26)" (`1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8`) holds edits 1 to
  223. Its locked twin is "StS v8 BACKUP (Nov 26), do not edit". Neither was touched in this chat.
- **In GitHub only:** edits 224 to 233. `make_v6.py` on the v5 read passes all 233 check rows (591 replacements).
  `verify.py` on the v8 read: 223 "accepted", 224 to 233 "not in the Doc", nothing PARTIAL. **The next edit is 234.**
- **Two chats logged on this branch at once.** The Riemann and Praether chat took 229 and 230
  (`CHECKPOINT-2026-11-26-riemann-praether.md`); this chat's work was renumbered 231 to 233 at the merge.
- **The PDF CT has** is still "StS v8 large print CURRENT (26 Nov, edits 1 to 223, the continuity pass).pdf". It does
  not have edits 224 to 233. A new one is made only when he asks.
- 103,443 words in the chapters (`story_report.py`, after edit 233). `build_gate.py`: NOT READY, 8 open boxes.

## The scene sheet (CT asked for it; keep it reachable)

- **Google Sheet:** "Surviving the Singularity: scene sheet (edits 1 to 233)", in CT's Drive, id
  `1vReMI4VKBIexpMvR8Sx0QpyO8Bde2w2jLOnKFCv0KYY`
  (https://docs.google.com/spreadsheets/d/1vReMI4VKBIexpMvR8Sx0QpyO8Bde2w2jLOnKFCv0KYY/edit). Tabs: "Scenes" (138 rows,
  filter on) and "Numbers to check" (two rows).
- **Copy in the repo:** `manuscript/novel/scene-sheet-2026-11-27.csv`, the same 139 rows (header plus 138), checked
  cell for cell against the Sheet.
- **Columns:** #, Act, Chapter, Scene, Words, When, When (basis), Where, Whose scene, On the page, What happens, What
  turns, Threads, Opens a question, Closes a question, Numbers on the page, Opens with.
- **How it was made:** the built book split at its scene breaks; words counted by script; the other columns filled by
  six readers from the page and checked by one; threads from one fixed list. It is a snapshot of edits 1 to 233 and the
  readers' reading. Check a cell on the page before relying on it. Five scenes read "nothing turns" (rows 1, 24, 32,
  59, 79).
- **Why CT wanted it:** he asked how authors use spreadsheets (Rowling's chapter-by-subplot grid, Heller's
  characters-by-dates chart, Story Grid's "does the scene turn" column, Ingermanson's words-to-cut column). For this
  stage it shows scenes where nothing turns, threads that go quiet and numbers that drift.

## What this chat did

1. Spin-up, then edit 228 (Lou's heavier entrance, end of Ch 16).
2. Seventeen readers over the whole book (six by range, eight by character, three by thread): 108 raw gaps, 69 merged,
   33 verified on the page, a plan judged from three and checked by a critic.
3. Edit 231: CT's held dictation, Grace's talk about the bed and staying for free (Ch 17).
4. Edit 232: Rosa makes Thanksgiving 2026, her first for the farm: his lines about her family and the church kitchen
   (his Spanglish), her grace in Spanish with a rosary (the standard Catholic blessing before meals), the ladle and
   "Please take this to Grace. It's her turn to eat." (Ch 27). First placed at the start of Ch 31; moved on his word.
   Ch 38's "at her first dinner," came out.
5. Edit 233: the finishing pass, 31 line fixes (`drafts/finishing-2026-11-27.md`), including items 1 to 3 of the other
   chat's fix list. A review pass caught three of Claude's slips, fixed the same day.
6. The scene sheet, above. Records: `EDITS.md` (228, 231 to 233), `drafts/edit-228-lou-comes-in.md`,
   `drafts/edit-231-232-grace-and-rosa.md`, `drafts/finishing-2026-11-27.md`; `WRITING-INSTRUCTIONS.md` 15a and Rosa's
   speech; the Drive mirror "StS edit list, edits 1 to 233 (mirror of GitHub)" (`1Dfk8U0O9y10odszpov-S_3G5RNO2YuZrDSjMPvgAbiQ`).

## Open with CT (his to decide; put to him only when he asks)

From this chat:
1. Three of his lines the finishing pass left alone: Ruby's "four thousand ... eight thousand" (Ch 8) four months
   after his "Fifty million views"; "Grace printed your cover page," Priya said. "She prints everything." (Ch 17; not in
   Claude's logs, so maybe his); "Some weeks he signed right under her." (Epilogue; the front-desk book can't do that).
2. Two numbers ("Numbers to check" tab): Elijah is 36 just before he drives north (early March 2025, Ch 15) and 37 in
   May (Ch 20); in October 2026 the narration says the last grant "ran out in June" while the scene means next June
   (Ch 27).
3. Rosa's "You have the heart of a helper" (Ch 27) and Lou's "Your heart is in the right place." (Ch 35).
4. Edits 224 to 233 into the Doc: as suggestions in v8, or a new copy; a new large print PDF when he asks.

From the other chat's list: "wingnut" three times (Priya, Ch 17, Ch 27); "taken aback" twice (Ch 16, and his own in
Ch 27); Praether's "I'll check them myself" and the ordnance threat, which never pay off (he said loose is fine).

Carried over (tenth checkpoint): edit 226's "under 6 months"; Grace's winter away and Faith; the five polish-pass
lines; the gas cap (Ch 25); "Marta had heard it as a murder" (Ch 39); "Creator Fund"; the 19 empty paragraphs in v8;
the thin places (Praether after Ch 26, Mrs. Delgado after the fire, Bidwell's last beat, the welder gap, the
Telecaster); Grace telling Marta about the arms (plan 10.5); the Instagram synopsis; "OLD:" on v6 and v7; Drive's
duplicate builds; the site's private reader and compendium; the merge to `main`; the ISBN and the release build.

## The prompt for the next chat (the smell pass)

```
We're finishing my novel, Surviving the Singularity. This is the twelfth chat: the smell pass. Spin up before you do
anything else:

1. Work on branch claude/singularity-publication-build-kparqk in both repos (ctavolazzi/survivingthesingularity and
   ctavolazzi/_workbench). Push every commit there, whatever branch this chat was given. Don't open or watch pull
   requests. Another chat may be logging on the same branch: fetch it first, read the "Next edit" line in
   manuscript/novel/TODO.md before you number anything, fetch again before every commit, and merge, never force-push.
2. Read, in this order: manuscript/novel/REFERENCE.md (start at section 1), manuscript/novel/CHECKPOINT-2026-11-27-eleventh.md,
   manuscript/novel/TODO.md, and all of manuscript/novel/WRITING-INSTRUCTIONS.md (section 7a is the smell rules, 4a is
   how I work a line, 15a is the newest lessons). Then STATE.md and the newest entry in sessions/LOG.md in _workbench.
3. The book is the Google Doc "StS v8 draft (Nov 26)", id 1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8. Its base is the
   v5 Doc "StS v5 draft (Nov 23)", id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA. Read both with the Docs connector
   and save the reads to your scratchpad. Do not change either Doc, or the locked "StS v8 BACKUP (Nov 26), do not
   edit"; I haven't cleared that.
4. Run make_v6.py on the v5 read and verify.py on the v8 read. You should get all 233 check rows passing, 223 rows
   "accepted" in v8, edits 224 to 233 "not in the Doc", and nothing PARTIAL. If you get anything else, stop and tell me.
5. The scene sheet: Google Sheet "Surviving the Singularity: scene sheet (edits 1 to 233)", id
   1vReMI4VKBIexpMvR8Sx0QpyO8Bde2w2jLOnKFCv0KYY, with a full copy at manuscript/novel/scene-sheet-2026-11-27.csv. One
   row per scene: when, where, whose scene, who's on the page, what turns, threads, numbers. Use it to find the places;
   check a cell on the page before you rely on it.

Where we are (end of 27 Nov): v8 holds edits 1 to 223. Edits 224 to 233 are logged in GitHub only. The PDF I have is
"StS v8 large print CURRENT (26 Nov, edits 1 to 223, the continuity pass).pdf"; it doesn't have 224 to 233. The next
edit is 234. After this I don't really want to change or add anything: it's about refining, revising, deleting,
buffing out the hard spots, polishing.

The job: the smell pass (TODO.md section 3, WRITING-INSTRUCTIONS.md 7a). My two places first, in my words: the truck
he lives in (Chapters 14 and 15) and the high-dollar party (Chapters 9 and 10). Then any scene where a smell would carry
the feeling. A smell only someone who was there would know, with a verb that carries the physics. Don't overdo it:
where it carries feeling, not one per page. Show me each one before it's logged, since Chapters 0 to 19 are done.

Waiting on my word, in the checkpoint file under "Open with CT". Don't put that list to me unless I ask for it. If an
edit I dictate settles one of them, mark it settled.

How I want it done:
- I dictate, you log. Find the passage in the built book, put my words in, log it the usual way (EDITS.md, a check row,
  ops rows, a record in manuscript/novel/drafts/), run make_v6.py, commit, push. Then tell me in a few lines what
  changed, every fact you invented, and anything that touches another chapter.
- My words go in word for word and are marked mine. When I restate a line, the last version is the line; "there we go"
  marks the keeper. Take the dictation fillers out ("like", "well", "he's like"). Mark what you worded.
- When I say where my words stop ("you can connect it", "carry this through"), write the rest to the writing
  instructions and tell me which words are yours.
- When something I ask depends on a condition, check the pages for it, tell me what's in the way, log the rest and hold
  the one line.
- Push back on continuity errors, contradictions and anything that confuses the reader. Not on my taste or my
  decisions.
- When I correct you, change the thing I named, keep the rest, and add the lesson to WRITING-INSTRUCTIONS.md in the
  same turn.
- Read the pages before you claim anything about the book. Use the code (find_in_book.py, story_report.py,
  build_gate.py, openers.py) instead of tokens. Check every quote a reader returns.
- A question from me gets an answer, not an action. Answer first, short. No em dashes.
- Stay on the novel. Don't touch the site's code or tests unless I ask.
- Nothing gets trashed or deleted without my yes; old copies get "OLD:" in front.
- Make a PDF only when I ask.
- At the end: update "Where things stand" and "What is still open" in EDIT-LOGGING-PROCEDURE.md, TODO.md,
  WRITING-INSTRUCTIONS.md, and STATE.md and sessions/LOG.md in _workbench, and refresh the Drive mirror of the edit list
  once (upload EDITS.md as text/plain; a markdown upload renumbers the edits).

When you're done spinning up, tell me in one line that you're ready and that the next edit is 234.
```
