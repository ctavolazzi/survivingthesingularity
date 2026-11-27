# How to log CT's edits (the procedure)

Written 2026-11-25 from the chat where CT read v5 and dictated edits 1 to 128, and kept up to date by every logging
chat since (seven by 26 Nov). Read all of it before logging the next edit: it is the whole method, and "Where things
stand" near the end says exactly where the book is.

**Since 26 Nov the work is also writing, not only logging.** Before writing any line for the book, read
`WRITING-INSTRUCTIONS.md` (how CT wants it written) and `PLAN-CHAPTERS-20-TO-36.md` (what happens). This file is the
mechanics: how an edit is logged and checked, and where things stand.

## What CT is doing
CT reads the v5 manuscript and dictates changes by voice. Claude logs them. Claude does not change the Google Doc
unless CT clears it (a change goes in only as a suggestion). CT's standing words: "I just want you to log the edits."
"Stop asking for permission. You can just do it." "Don't push back. Don't overthink. Just roll with the punches."
Then, the same day: "you're welcome to push back when there's continuity errors, when there's conflict that makes
the story more confusing ... contradictions, problems, things that'll confuse the reader ... I encourage it."

## When to push back, and when not to
Push back on: continuity errors, contradictions, logistics that can't happen (who is in the room, who is driving),
anything that makes the story more confusing, and anything that brings back a problem already edited out.
Don't push back on: his taste, his word choices, his style, or a decision he has already made. Log those as given.

## Sort every message into one of four kinds
1. **An edit**: text for the page. Log it.
2. **Context**: why, or what the reader should feel ("for our notes," "I don't want you to put this in," "context
   for you"). Log it under the edit as "Context from CT, NOT for the page." Never put it in the page text.
3. **A correction to an edit**: the newest wording wins. Replace it in place. Git history keeps the older versions.
4. **A question or "think it through"**: answer in chat. Build and log nothing until he settles it.

## Procedure for each edit
1. Find the passage in make_v6.py's `v6.txt` (every logged edit applied; grep it, don't read the whole file), so
   "Book now" is quoted exactly as the book stands now. Not from the raw Doc: it lacks every edit not put in yet.
2. Write it in `EDITS.md` with the next number: where, "Book now," "Change to."
3. Use CT's words word for word. Mark anything Claude worded ("Claude's wording"). Smooth only dictation breaks.
   Never rewrite what he did not ask to rewrite ("merge, don't rewrite").
4. When CT restates a line inside one message ("the truth. Was reality. So ... something that resembled
   consensus"), the restatement is his correction while dictating. Keep the last version, drop the first; don't
   log both and don't flag it as a repeat.
5. Fix dictation errors silently when the meaning is plain (Blue = Lou, Martha = Marta). When a fix would change
   the meaning ("bleed out" vs "bug-out"), log it as he said it and ask one short question.
6. If something he asks cannot work in the book as it stands (Grace is only on speaker, Curtis is driving), say
   it in one line, give one recommendation, and wait. Once he decides, log his decision without arguing.
7. Add a check row to `manuscript/tools/edits-v5/checks.py` (words that must be in the book, words that must be
   gone; `[break]` means a scene break) and a find and replace row to `manuscript/tools/edits-v6/ops.py` (above the
   ITALIC list). See "The tools" below for what a row can do.
8. Run `python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT --no-docx`: every row must pass. Then
   `python3 manuscript/tools/edits-v5/verify.py V6_READ.json --table manuscript/novel/EDITS-status.md` for the status
   table (new edits show "not in the Doc", which is right until CT says to put them in).
9. Commit (one change, plain message) and push to `claude/singularity-publication-build-kparqk` (CT, 25 Nov:
   "Push to kparqk, like the procedure says"), whatever branch the chat itself was given.
10. Do NOT update the Drive copy after each edit (CT, 25 Nov: it costs tokens). Refresh "StS edit list, edits 1 to N
   (mirror of GitHub)" (id 1YL7Tdov_VVfBSC2OtsUk2frzlw3DnZiHEqyznvVMRSE, edits 1 to 236; https://docs.google.com/document/d/1YL7Tdov_VVfBSC2OtsUk2frzlw3DnZiHEqyznvVMRSE) once, at the end of the session. Upload EDITS.md as text/plain: a markdown upload turns the edit numbers into an auto-numbered list (27 Nov).
   It is remade from a text file (the connector cannot replace a Doc's text without retyping it), so the id
   changes each time: the newest one is here, and the old copy gets "OLD:" in its title and a pointer at the top.
11. Reply in two or three lines: the number, what it says, anything of Claude's wording, one open question at most.

## Things that have gone wrong before
- Rewriting when he said smooth ("you're overdoing it"). Adding things he didn't ask for.
- Putting his context into the page text.
- Check numbers colliding (the follow-ups row was once 90).
- An unquoted heredoc with backticks ran the build. Use quoted heredocs ('EOF').
- Two chats logged on the same branch at once (26 and 27 Nov) and both took edits 229 and 230. Fetch the branch and read
  TODO.md's "Next edit" before numbering, and fetch again before every commit; merge, never force-push.
- A broken check row was committed and pushed (26 Nov, e9862f96; fixed in b992f584). A script that edits several
  files stopped on an assert after changing two of them, and the shell line went on to commit and push because its
  steps were joined with `;`. Join the build, the commit and the push with `&&`, so nothing is committed unless
  make_v6.py has just passed.
- Counts drifting: the Totals line must match the latest verify run.
- A later edit that changes words of an earlier one breaks the earlier check row. Narrow the earlier row to the words
  that still hold (row 113 for edit 183) or update it to the new words (row 137 for edit 182); never delete it.
- An edit that replaces a whole section (185, the Author's Note) leaves the older rows nothing to find. Their "where"
  says "replaced by 185" and their "must be there" list is empty; keep any "must be gone" words.
- A find that covers italic text gets retyped, and the paragraph it touches can lose its heading style (edit 184 first
  turned the title into body text, because "A Solarpunk Novel" is italic). Keep finds off italics where you can, and
  after a structural edit open the .docx and check the styles of the paragraphs it touched.
- The build adds pages of its own (copyright, and until 26 Nov "About the Author" after the last line). After a build,
  look at the first and last pages of the PDF, not only the checks.
- Naming: CT got lost between v5 and v6 names (26 Nov: "The naming system is confusing me"). Name things for what they
  are now: the edit list is `EDITS.md`; the PDF to read has CURRENT, the date and the edit range in its title; old
  copies say "OLD:" and go in "Older builds". Don't leave an old version number on something current.
- Tokens: CT asked (26 Nov) "Are you trying to conserve tokens when you can?" Use code: grep `v6.txt` and the saved
  Doc reads instead of reading them; ask Drive for `excludeContentSnippets` and small pages; don't print big JSON.

## The tools
- `manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT [--no-docx]`: the v5 Doc with its suggestions accepted, then
  every row of `ops.py`, then every check row. Writes `OUT/v6.txt`, `OUT/v6-read.json` and (without `--no-docx`)
  `OUT/v6.docx` with the 19 pictures. It never calls Google.
- An `ops.py` row is (edit number, find, replace). The find must appear exactly once. In the replacement a newline
  starts a paragraph, an empty line is a scene break, `*...*` is italic, and at the start of a paragraph `§H1 ` makes
  it a heading and `§C ` centers it. A find of `""` inserts at the very start of the book (edit 184); a find of
  `(start, end)` replaces the span from the one start to the first end after it (edit 185). The build gives any line
  before the title a page of its own; nothing uses that now (CT: the title page comes first).
- `ITALIC` in `ops.py`: lines that must be italic end to end (verify.py cannot see italics).
- `manuscript/tools/edits-v5/verify.py READ.json`: where each edit stands in a Doc (accepted, suggested, not in the
  Doc, PARTIAL).
- `manuscript/tools/edits-v7/make_v7.py`: remakes the separate v7 copy (v6 through edit 171 plus `ops_v7.py`). Leave
  it alone unless CT asks about v7.

## Making the large print PDF (only when CT asks)
1. In a fresh container: `pip install -r publication/novel/build/requirements.txt` and `mkdir -p publication/novel/work`.
2. `python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT` (with the .docx; the picture links in a read
   expire, so use a fresh v5 read).
3. `python3 publication/novel/build/build.py OUT/v6.docx --only large --skip-edit-gate`. Every check in
   `publication/novel/output/CHECKS.md` must pass. The PDF has no pictures (`include_pictures: false` in book.json)
   and no About the Author page (`about_author_in_book: false`, so "Recognize Your Power" is the last line).
4. Look at the first and last pages (`pdftotext -f 1 -l 5`, and the last five).
5. Upload to the Drive folder "StS Publication Files" (id 1QmqU-MsDcqfh1sC5Q_DsGeqcdyf_kLB_) titled "StS v6 large
   print CURRENT (date, edits 1 to N, what is new).pdf". Rename the one it replaces "OLD: StS v6 large print (edits
   1 to M).pdf" and move it to "Older builds" (id 12CbC-hEUy_5rArVtz8v393rc_ciV9Ltv). Give CT the link.

## Final-pass checks (CT's standing list)
- Every call to his mother: after the stroke, Elijah calls Sunday 9:40 in the MORNING. Exactly one call is at night
  (shows she is confused, not alarming). See the end of edit 122 in `EDITS.md` for the list.
- Day-of-week tics: "Tuesday" appears 31 times. Cut the ones that only mark time (see after edit 125).
- Sentences that all open with "He" (or another pronoun). See "Asked for the future" below.

## Asked for the future (CT, 25 Nov): a checker for sentence openings
CT, after edits 131 to 133 (Chapter 19, where most sentences in Elijah's silence opened with "He"): "Instead of
starting everything with a pronoun, you gotta vary the sentence structure, bro." Then: "This is something that I want
you to more or less just scan the book for. Instead of me like manually fixing this every time, there's an opportunity
for us to create a new bit of code, a checker or something that will just scan the book for those instances and fix
them. We don't need to do it now, but I do want you to update whatever document we're using to drive the editing
process. And I want it to show that this is something that I'm asking you to do in the future."

Not built yet. When CT says go:
- Write a checker in `manuscript/tools/` that reads a fresh read of the Doc and lists every paragraph where too many
  sentences open with the same pronoun, chapter by chapter.
- Fix each one the way edit 133 was done: change only the openings and joins; every fact, name and line of dialogue
  stays. Each fix is logged as an edit with a check row, like any other, and goes into the Doc only as a suggestion.
- Known so far: Chapter 14, where 50 of 193 sentences open with "He" (the eight changes given in chat and never
  logged, in "Places to look at" in `EDITS.md`), and the other runs listed there.
- Until then, vary the openings in every line Claude writes for an edit.

## Short lines out of context (CT, 25 Nov)
"Short sentences like that can be confusing if taken out of context. So we need to add a little bit of redundancy in
those moments, but not every time. It's kind of like dealer's choice here." Example: edit 134, "Marta hadn't said a
word either, not since Grace walked Patricia down the line." Claude's judgment where; not every short line.

## Writing a beat for CT (learned 26 Nov, edit 188, the laugh)
Three tries before CT took one: the first echoed his own phrase from another chapter, the second was "really dry",
the third "a little too much". What the one he took does:
- Before writing, grep v6.txt for the key word and its cousins (laugh, chuckle), so the new line doesn't repeat a
  construction the book already has.
- Show the thing happening in two or three small steps (snort, laugh, it gets away from him). Not one flat
  statement, and not a pile of detail (ribs, blurry road, a summary of his life).
- One beat, one short run of sentences. Don't explain why it matters; the reader has the chapter for that.
- Leave room for CT's line. He added the feeling himself ("All his pent-up pain started rolling out of his lungs at
  once."). Claude writes the action plainly; the sentence that names the emotion is his to give.
- Offer one version, sized in the middle. If he says dry, add one step, not five.
- No beat-counting pattern: "He read it twice. Then he wrote back." (edit 196). CT: "Don't do the pattern." The book
  already leans on reading or watching a thing a counted number of times, and on a short fact followed by "Then he
  ...". Go straight to the action.
- Prose tics measured in the book (26 Nov, make_v6.py's v6.txt, 93,742 words; counts by script): "the way you/a/she
  ..." similes 76; "He knew" / "he didn't know" 69; X, Y, and Z lists 73; runs of three or more very short sentences
  63; "looked at him/her/it" 59; "for a while" / "a long time" 50; "didn't say anything" / "said nothing" 39; "nodded" /
  "shrugged" 29; "That was all/it/the ..." closers 28; "He" opens 16% of sentences. In anything Claude writes: no
  filter words where the thing itself can be shown (knew, thought, saw, watched, felt, realized, noticed); no leading
  words that walk the reader step by step (then, so, soon, suddenly); body beats only when the next few lines don't
  already have one; don't end a paragraph by summing it up ("That was all there was."); vary sentence length, and
  never three clipped sentences where one would do. From fiction line-editing guides (filter words, leading words,
  repeated gestures, sentence rhythm) and Wikipedia's "Signs of AI writing" (summary closers, commentary).
- Measure openings before showing CT a draft (26 Nov, Ch 25 draft 1: "You're still overusing pronouns and not varying
  the sentence structure."). Count the first words of the narration's sentences; no one opener (He, She, a name)
  should carry a run, and swapping "She" for "Grace" ten times is the same problem.
- Fixing openings with tricks is the same failure (Ch 25 draft 2; CT: "I've told you to change this a dozen times and
  you keep doing it ... We just looked up information about signs of AI writing"). Draft 2 traded pronouns for
  inversions ("Off she went," "Around she turned again"), quips that close a paragraph ("The corner of her mouth
  didn't get the message," "Her face did what it wanted anyway"), stacked fragments ("Gas down, gas back, food: that
  much he had. A tow, no."), "like a man who ... the way he said it would," and lines built to be quoted ("The money
  for the room by the window was the room by the window"). Draft 3 is plain: a subject, a verb, the concrete thing,
  varied lengths.
- The middle path (CT, 26 Nov, after Ch 25 draft 3): "I do like the quips, though. They are welcome ... wearing his shirt
  is good. You're changing too much. You're doing too much. Find the middle path ... this is better, but it's lost some
  of its charm ... Little jokes at the end of the paragraph, the corner of her mouth didn't get the message. That's
  great. I love that. But not when it cheapens the emotional weight of the scenes. When it adds levity, sure. When it
  feels literary, absolutely. But not at the cost of the message." Agreed in full: vary sentences by what they're
  about, not by tricks; cut the extras. So a quip, an inversion or a dry closing line is welcome where it adds levity
  or reads literary, one at a time; never in a heavy moment (shame, grief, the truck stop, the fire), and never as a
  way to dodge a pronoun.
- One idea per sentence. Ch 20 draft 1 packed the boxes, the AI board, the secret, the missing heat test and a joke into
  one sentence ("Every one of those boxes had Elijah's board inside it, the one an Iowa company's machine had laid out
  at midnight, and nobody had tested a single one in July yet, because it was May."). CT: "What the fuck is that,
  bro?" A quip has to be funny on its own and sit at the end of something light, not ride on the back of a clause.
- Plain is not flat. Seed what is coming (CT, 26 Nov, on "It hadn't been very hot yet."): "This is foreshadowing, right?
  Like you're seeding, we're planting ideas, we're writing, we're doing the work of creating a story. We're not just
  laying out a sequence of events. We are writing." A short line that points at what's coming stays; cutting tics must
  not cut the story's setups.
  Then: "But we can combine them together, right? It was still a cool spring. It hadn't been very hot yet ... you
  know what to do, so just do it." When a correction cuts something, keep what was good in the old line and build on
  it. Write the first draft as the craft, not as the safe version.
- Make it clear. A line that leaves the reader asking "what kind?" gets the word that answers it (CT, 26 Nov, on
  Priya's "I still get letters": "we don't know what kind of letters they are. It's not clear. You need to make
  things clear ... Stop hedging. Stop hesitating. Stop fishing for what I want, and just do it."). Read each new line
  as a stranger would before showing it, and finish the work without asking permission at each step.
- Don't bring back a problem already fixed. The mirrored contrast line ("It's not X. It's Y."; "They can. They just
  won't."; Claude's own "He's on this side of the fence. His friends aren't.", 26 Nov) was edited out in 119 and 174.
  CT: "I don't want you to introduce like previous problems that we've already overcome ... We've already established
  that we can do better than this." Before showing any line, check it against every lesson in this file and in
  EDITS.md (the "He" openings, the "Tuesday" tics, the 9:40 calls, naming who "he" is).

## The narration is hybrid (CT, 25 Nov)
CT, planning the Chapter 19 rework: "whose feelings? Elijah's and his observations of others. BUT ... we have a
hybrid narration style going on here." The book sits on Elijah's shoulder, and above him is a storyteller who knows
more than he does ("Although Elijah was quite unaware of it," edit 106), leaves him for a scene (the kitchen
trailer in Chapter 17, Bidwell, Chapter 38), goes into other heads (Tyler in Chapter 26) and talks to the reader
("Most people never do, at moments like that," edit 100). In anything Claude writes for an edit: feelings are
Elijah's, other people's come through what he sees them do, and the storyteller can tell the reader, briefly, what
Elijah cannot know.

## What is still open (27 Nov, end of the eleventh logging chat)
**The endgame runs from `REFERENCE.md` (how), `GOALS.md` (what done is), `TODO.md` (what is next).** The prompt for
the next chat (the smell pass) and the grouped list of what is CT's are in `CHECKPOINT-2026-11-27-eleventh.md`. In
short, what is still CT's:
- From the eleventh chat: three of his lines the finishing pass left alone (Ruby's "four thousand" in Ch 8, "Grace
  printed your cover page" in Ch 17, "signed right under her" in the Epilogue); two numbers that may not hold (Elijah
  36 to 37 in two months, Ch 15 and 20; the route's "ran out in June" in October 2026, Ch 27); Rosa's "heart of a
  helper" (Ch 27) and Lou's "Your heart is in the right place." (Ch 35); edits 224 to 233 into the Doc.
- From the other chat's list (`CHECKPOINT-2026-11-26-riemann-praether.md`): "wingnut" three times, "taken aback"
  twice, Praether's ordnance threat that never pays off.
- Carried over: edit 226's held line; Grace's winter away; the five polish-pass lines; the gas cap (Ch 25); "Marta had
  heard it as a murder" (Ch 39); the "Creator Fund" line; the 19 empty paragraphs in the v8 Doc; the thin places; the
  Instagram synopsis; "OLD:" on the v6 and v7 Docs; Drive's duplicate builds; the site's private reader and
  compendium; the merge to `main`; the ISBN and the release build.
- **The taste pass is next** (CT, 27 Nov), in its own chat; the prompt is in `CHECKPOINT-2026-11-27-smell.md`.
- The smell pass (27 Nov, the smell chat): his two places are logged (edits 235 and 236). Still his to rule on, in
  the last column of `smell-table-2026-11-27.md`: a smell for the cooked plugs (Ch 21) and for Priya's two pits
  (Ch 26), which need the smell from him; woodsmoke reaching Grace at the door before the gate story (Ch 24, one
  line); and Elijah telling Grace what the Thanksgiving coats bring back (Ch 27, a short exchange, new material).
  Also his: the corrected wording of edit 235 (logged before he saw it, shown to him after; he has not ruled on it), and Claude's invented details in both edits
  (`drafts/edit-235-236-smell.md`).
- From the close of the Riemann and Praether chat (27 Nov; `CHECKPOINT-2026-11-26-riemann-praether.md`, first
  section): the smell pass prompt was run once there (clean spin-up, nothing shown or logged, next edit still 234), and
  one idea of Claude's is with CT unanswered (a line at the gate in Chapter 36 that picks up Grace's "put humans first"
  promise from Chapter 27). That section also holds his words about what the Riemann scene is for, the answer to his
  question about the stakes, and the source links.
- From edit 234: one question held for him (should the fight at the fire in Chapter 36 name the three years he hid
  the arms from her), and his lines from edits 220 and 230 that came out, kept in
  `drafts/edit-234-grace-doesnt-know.md` in case he wants them placed elsewhere.

## v6 (25 Nov)
Edits 1 to 138 are all in v6: the Google Doc "StS v6 draft (Nov 25)", the CURRENT copy in the bridge map, made by
`manuscript/tools/edits-v6/make_v6.py` (see "Applied" in `EDITS.md`). CT reads v6 in the large print PDF
and makes his final edits there. The next edit is 139. Log it the same way (number, where, "Book now," "Change
to"), add a check row in `checks.py` and a find and replace row in `manuscript/tools/edits-v6/ops.py`, and check it
against a fresh read of the v6 Doc. The v5 Doc stays as it is.

## Where things stand (end of the eleventh logging chat, 27 Nov)
- **The book is the Google Doc "StS v8 draft (Nov 26)"** (CURRENT in the bridge map): the v5 Doc with its suggestions
  accepted plus edits 1 to 223, without pictures. Its locked backup: "StS v8 BACKUP (Nov 26), do not edit". Neither was
  changed in the eleventh chat or the Riemann and Praether chat.
- **Edits 224 to 233 are logged in GitHub only.** Tenth chat: 224 to 227. Riemann and Praether chat: 229 (the Riemann
  dinner, Ch 27) and 230 (Praether's terms and Lou at the barn, Ch 17, 18). Eleventh chat: 228 (Lou's entrance, Ch 16),
  231 (Grace's talk about the bed, Ch 17), 232 (Rosa makes Thanksgiving 2026, her grace and the ladle, Ch 27, 38), 233
  (the finishing pass, 31 line fixes). verify.py on a v8 read shows 223 "accepted" and 224 to 233 "not in the Doc",
  nothing PARTIAL. **The next edit is 234.**
- make_v6.py on a fresh v5 read passes all 233 rows (591 replacements). 103,443 words in the chapters
  (`story_report.py`). build_gate.py: NOT READY, 8 open boxes in `TODO.md`.
- **The scene sheet:** "Surviving the Singularity: scene sheet (edits 1 to 233)", a Google Sheet in CT's Drive, id
  `1vReMI4VKBIexpMvR8Sx0QpyO8Bde2w2jLOnKFCv0KYY` (https://docs.google.com/spreadsheets/d/1vReMI4VKBIexpMvR8Sx0QpyO8Bde2w2jLOnKFCv0KYY/edit). One row per scene (138),
  with a "Numbers to check" tab. A full copy is in this folder: `scene-sheet-2026-11-27.csv`.
- **The PDF CT reads** is still "StS v8 large print CURRENT (26 Nov, edits 1 to 223, the continuity pass).pdf"
  (https://drive.google.com/file/d/1B0nwZM5XXGxfeEjRAjyl0bICQNxsHtGp/view). It does not have edits 224 to 233.
- The Drive copy of the edit list is "StS edit list, edits 1 to 233 (mirror of GitHub)" (step 10); the 1 to 227 copy,
  and a markdown upload that renumbered the edits, are "OLD:" with the new id in their titles.
- The bridge map, BRIDGE.md and the Drive bridge page still say v8, which is right.
- Checked again on 27 Nov at the close of the Riemann and Praether chat, on fresh reads of both Docs: the same counts
  (233 rows pass, 591 replacements; 223 accepted, 224 to 233 not in the Doc, nothing PARTIAL).
- **Since then, edit 234 (27 Nov, the Riemann chat, CT's dictation):** Grace doesn't know about the arms until the
  table finds out (Ch 17, 18, 34, 35, 36). make_v6.py now passes **234 rows (608 replacements)**; verify.py on v8 shows
  223 accepted and **224 to 234 not in the Doc**, nothing PARTIAL; 103,503 words. **The next edit is 235.** The lines
  above this one describe the end of the eleventh chat and are one edit behind.
- The Drive copy of the edit list is still "edits 1 to 233": edit 234 and the context notes added under 229 and 230
  on 27 Nov are not in it. Refresh it at the end of the next session (step 10).
- **Since then, edits 235 and 236 (27 Nov, the smell chat, CT's words from `WRITING-INSTRUCTIONS.md` 7a):** the smell
  of the truck (Ch 15) and the smell of the high-dollar party (Ch 9). On fresh reads of both Docs that day,
  make_v6.py passes **236 rows (611 replacements)**; verify.py on v8 shows 223 accepted and **224 to 236 not in the
  Doc**, nothing PARTIAL; 103,647 words; build_gate.py NOT READY, 10 open boxes once the taste pass box was added at the close. **The next edit is 237.** Neither Doc
  was changed. The Drive copy of the edit list was refreshed at the end of the smell chat, on CT's word: "StS edit
  list, edits 1 to 236 (mirror of GitHub)", id `1YL7Tdov_VVfBSC2OtsUk2frzlw3DnZiHEqyznvVMRSE`, uploaded as text/plain and checked against `EDITS.md` (the
  same text, edit numbers intact). The 1 to 233 copy is "OLD:" with the new id in its title and a pointer at its
  top. The scene sheet (Sheet and CSV) was not changed: rows 29
  and 48 are 100 and 48 words short, and its title still says edits 1 to 233. **The knowledge sheet** (who knows
  what, and when; CT asked for it at the close of the smell chat): `knowledge-sheet-2026-11-27.md` and three CSVs
  here, built by `manuscript/tools/edits-v6/knowledge.py`, and in Drive as the Google Sheet "Surviving the
  Singularity: who knows what (edits 1 to 236)", id `1KEqKBYo45ULGnSR9eNx4VcwIYNbbGuMOmln3N8eIyZU`
  (https://docs.google.com/spreadsheets/d/1KEqKBYo45ULGnSR9eNx4VcwIYNbbGuMOmln3N8eIyZU/edit), three tabs. A backup of this branch as it stood
  before the smell chat is the branch `backup/book-branch-2026-11-27`, in both repos.
- **Then edit 237 (27 Nov, the same chat, CT's dictation):** Miles Renner on the big screen, a new scene in Chapter
  26. make_v6.py passes **237 rows (612 replacements)**; verify.py on v8 shows 223 accepted and **224 to 237 not in
  the Doc**; 104,129 words; 138 scenes. **The next edit is 238.** The Drive copy of the edit list (edits 1 to 236)
  does not have it. The scene sheet (137 rows) does not have the new scene, so `scene_sheet.py check` will report a
  structure difference until a row is added.
- **Then edits 238 and 239 (27 Nov, the same chat, CT's dictation):** Lou and Grace at the fence with cider, and
  Grace leaving for the winter, the two new scenes that open Chapter 26. make_v6.py passes **239 rows (614
  replacements)**; verify.py on v8 shows 223 accepted and **224 to 239 not in the Doc**; 104,647 words; 140 scenes.
  **The next edit is 240.** "Grace's winter away" is settled. Still his, from the same dictation and not written:
  Grace's Hinge profile and "maybe I'll be a spinstress after all", and the coworkers exchange for the night they
  get together (`next-version-scenes-2026-11-26.md`, section 6).
- **Then edit 240 (27 Nov, the same chat, CT's dictation):** "Pondwater" ends on the near kiss; a new scene in
  Chapter 27 has the weeks after and the pillow talk; one sentence is out of the fire in Chapter 36. make_v6.py passes
  **240 rows (617 replacements)**; verify.py on v8 shows 223 accepted and **224 to 240 not in the Doc**; 104,868
  words; 142 scenes. **The next edit is 241.** Edits 237 to 240 have not been read in place, in order: that is the
  first job of the next chat.

## One branch, and what to check before the final pass (27 Nov, close of the sixth logging chat)
- **The one branch for the novel is `claude/singularity-publication-build-kparqk`**, in both repos (the book repo and
  _workbench). Every chat logs there, whatever branch it was given. Checked 27 Nov: no other branch in either repo
  holds newer novel edits. One side branch, `claude/surviving-singularity-curtis-scene-kjesg6`, held notes and drafts
  for three scenes (Curtis and the robot OS, Elijah's birthday, Priya's ankle) that were never brought over; the file
  is now here as `next-version-scenes-2026-11-26.md`. Nothing in it is logged as an edit. Ask CT whether any of it
  goes in. The birthday draft bears on the age question below.
- Before starting: `git fetch` and `git pull --ff-only` on that branch in both repos, since several chats push to it.
- **The scene sheet was checked against the book built with edits 1 to 234** (27 Nov): every scene lines up, every
  word count matches, every number and weekday listed is in its scene, the dated days fall on the right weekdays,
  and the Google Sheet matches `scene-sheet-2026-11-27.csv` cell for cell. Rows 52, 53, 126 and 128 were brought up
  to edit 234. Not re-read: the "What happens" and "What turns" summaries outside those rows.
- **Left for CT from that check:** Elijah is 36 in early March 2025 and 37 in May (no birthday on the page); in
  October 2026 the narration says the last grant "ran out in June" while the scene means the coming June; these
  questions are opened in the sheet and never marked closed (some may be answered on the page): will Elijah ever
  call Ruby, what Grace and Curtis agreed on, whose name Grace wrote on her hand, what he said to Grace the night
  of the tea, what happened at Mrs. Delgado's, who helped him that first spring, who the Sacramento LLC is. Row
  138's word count covers the Epilogue, About This Book and the Afterword, not the Appendix or Thank You. The
  Sheet's title still says "edits 1 to 233".
- **A second, full read of the scene sheet (27 Nov, later, the Curtis-scene chat):** six readers checked every cell
  of all 137 live rows against the book built with edits 1 to 234 (including the Sunday lien sale), and every finding
  was checked on the page. 30 cells were fixed, in the repo copy and in the Google Sheet, and the two match cell for
  cell. The fixes: who is on the page (Ma by voicemail in row 47, Patricia by phone in 89, Marta in 71 and 99, the
  machine in 134 and 137, Grace on the stream in 137, the lamp in 133; Reuben out of 120), number phrases quoted as
  written (40, 52, 61), dates and places (15, 16, 17, 24, 26, 46, 77, 92, 121), what turns (53, 101), row 60 is scene 1
  of Chapter 18 now that row 59 is cut, and row 138 covers only the Epilogue (290 words; the back matter came out of its
  cells). Three new rows on the Sheet's "Numbers to check" tab (not in the repo copy, which holds only "Scenes"): how
  long Reuben has had the deed (Ch 29, "a year and a half"), "Took you a month" (Ch 24, about seven weeks by the book's
  dates), and "Three years" said in October 2027 (Ch 34, 35; two years and seven months; the narration says "going on
  three years"). For CT, not changed.
- **Thirteen more cells for the scene sheet, rows 1 to 24**, each with the line from the page that proves it:
  `scene-sheet-fixes-rows-1-24.md` (from the tenth chat; not applied, so the CSV and the Google Sheet stay in step).
- **Unchecked since the sixth chat changed the build code** (a page for a line before the title, no About the
  Author page): the paperback, ebook and docx builds, and the site's own tests after the edit list was renamed
  `EDITS.md`. Run them before a release.


## Four things in the book for CT, from a third check of the scene sheet (27 Nov, the fifth logging chat)
Found by four readers against the book built with edits 1 to 234 and confirmed on the page in that build's v6.txt.
Not yet in the lists above. For CT; nothing changed. (The sheet fixes this check found were already made by the
second full read above; the "four thousand" replies and the Sunday lien sale are already recorded.)
- **Who sent Ma the video.** Ch 6: Elijah sends the link to her chat, and she writes at 6:10, "I watched it. You look
  thin." Ch 7: "I watched your video," she said. "The Hollis girl sent it to me." Both can be true, but the page
  doesn't say so.
- **The squash.** Ch 34, scene 1: Lou says "the squash has to come in this week" and Curtis pulls the first wagon.
  Two weeks or more later, at the October meeting: "The winter squash had to come in," and the next morning rows of
  squash still sit in the field.
- **Phones face up.** Ch 38: Patricia's "phone was face up. For the first time anybody could remember." Weeks earlier,
  Ch 34: "Lupe Ochoa had her phone face up on the plywood, which nobody did at that table." The Ch 38 line can mean
  Patricia's phone; the reader may hear "anybody's".
- **Melody's visits.** Ch 37: "A Saturday in April. One in May. Two in August. The last one was three weeks ago." Three
  weeks before early November is October, which the list leaves out.

## Which copy is the most current (CT, 26 Nov)
"I want the v6 that I'm reading in large print to be the most current version." Everything goes into v6, including
anything first made for v7 (edits 184 to 186). v7 is a frozen side copy; nothing goes into it unless CT asks. The next
version of the book (CT hopes the last) will be made from v6 with every logged edit: when he says go, the logged
edits go into the v6 Doc as suggestions (see "Later, when CT says go"), or a new Doc is made from make_v6.py's .docx
the way v6 was made from v5. Ask him which before doing either, then add the new copy to the bridge map.

## v7 (26 Nov): a separate copy
CT: "keep v7 as a totally new, totally separate thing ... I want to keep working on v6." The Google Doc "StS v7
draft (Nov 26)" is v6 through edit 171 plus the v7-only changes in `manuscript/tools/edits-v7/ops_v7.py`
(Dedication, Thank You, "Recognize Your Power" first and last; v6 has its own versions of these). Record: `manuscript/novel/V7-CHANGES.md`. New edits
go into v6 as before, from 172; v7 does not follow them unless CT asks.
Since 26 Nov the same v7 changes are also in v6 (edits 184 to 186); the v7 Doc itself is unchanged.

## Later, when CT says go
Apply 87 onward to the Doc as suggestions, re-read, run verify. CT accepts the suggestions. Run
`build.sh` (the gate stops it until every edit is in), then refresh the Drive uploads.

## Readers' notes on the book text, for the final pass (27 Nov, from the chat of edits 217 to 220)

Two readers checked Chapters 0 to 9 and 16 to 21 against edit 234's build. No hard contradiction. The scene sheet
fixes they found are covered by the sheet's full read (commit f644636e). Tensions in the text, each quoted and
grep-checked; none is fixed, each is CT's to rule on:
- Ch 6 and 8: "By Friday it was four thousand replies" (October 2023) and Ruby in February 2024, after "Fifty million
  views": "Because there's four thousand of them and one of you. And tomorrow it'll be eight thousand."
- Ch 8: "He hadn't known he was a speaker until a young man with a tablet took him there." and later "A seat on the
  four o'clock panel, because someone's flight from Austin had been canceled."
- Ch 17 and 19: Curtis's tractor story, "the laptop says twelve hundred dollars and a week. I knew it was two dollars
  of hose.", and Elijah's truck: "A dealership had quoted him twelve hundred dollars and a week." An echo, or a
  leftover.
- Ch 17 and 19: Tyler sent Elijah to Praether's with "a couple of big crates", and he is on the farm every build
  weekend, so a fourth person could connect the arms to the barn.
- Ch 19: an April order, most of a month on the first design, a redesign, three build weekends and a field week, all
  done in time for "The forty units shipped in May" and a week of laying tape still in May. It only fits if the order
  came in the first days of April.
- Ch 17 and 19: Grace's offer came "in her message on his page"; Tyler "had found Elijah's email for Grace".
Chapters 10 to 15 and 22 to the Epilogue were not re-read by this chat; its readers stopped at a usage limit.

## The site branch from the first novel chat (27 Nov)
`claude/manuscript-review-sts-updates-gu5849` rebuilt the site from the 17 Nov draft of the novel. Its book text is
superseded by v8 plus edits 224 to 234 on this branch. Do not merge it as is. Parts that may be worth porting after the
final pass: the legal pages and fiction notice (`src/lib/bookNotice.js`), the refund and license lines in
`src/lib/offer.js`, the EPUB and download builder (`scripts/build_novel_downloads.py`), and the hope copy
(`src/lib/stance.js`). The scene sheet audit that chat ran on 27 Nov found nothing that the full read above and the
four items above do not already cover.
