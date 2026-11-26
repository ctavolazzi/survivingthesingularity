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
10. Do NOT update the Drive copy after each edit (CT, 25 Nov: it costs tokens). Refresh "StS v6 edit list
   (mirror of GitHub)" (id 1rVTwjoikmOaTNwbsVJ0L3f9H0nlNykM58MGBRe4T_XE) once, at the end of the session.
   It is remade from a text file (the connector cannot replace a Doc's text without retyping it), so the id
   changes each time: the newest one is here, and the old copy gets "OLD:" in its title and a pointer at the top.
11. Reply in two or three lines: the number, what it says, anything of Claude's wording, one open question at most.

## Things that have gone wrong before
- Rewriting when he said smooth ("you're overdoing it"). Adding things he didn't ask for.
- Putting his context into the page text.
- Check numbers colliding (the follow-ups row was once 90).
- An unquoted heredoc with backticks ran the build. Use quoted heredocs ('EOF').
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

## What is still open (26 Nov, end of the eighth logging chat)
**The endgame runs from three files: `REFERENCE.md` (how), `GOALS.md` (what done is), `TODO.md` (what is next).**
Every question that was open is decided in `PLAN-CHAPTERS-20-TO-36.md`, section 12 (where a decision was CT's and
Claude made it, it says so). What is still CT's is the top of `TODO.md`:
- The rover and the arms: keep the rover as written, with the arms as the machine on the table in Chapter 34?
- Grace's father: left when she was a teenager, or checked out without leaving the porch?
- The ending lines in the plan, section 13, one at a time.
- The Instagram synopsis: fix or leave.
- Cover credit (CT, 26 Nov, for "the book proper"): his words are "cover credit : me, the author, sketches and
  Midjourney", cheeky and without a name. It goes inside, on the copyright page, where other books have it (CT), not
  on the outside of the cover: `copyright_page` in `publication/novel/build/book.json`. Add it at the final build.

## v6 (25 Nov)
Edits 1 to 138 are all in v6: the Google Doc "StS v6 draft (Nov 25)", the CURRENT copy in the bridge map, made by
`manuscript/tools/edits-v6/make_v6.py` (see "Applied" in `EDITS.md`). CT reads v6 in the large print PDF
and makes his final edits there. The next edit is 139. Log it the same way (number, where, "Book now," "Change
to"), add a check row in `checks.py` and a find and replace row in `manuscript/tools/edits-v6/ops.py`, and check it
against a fresh read of the v6 Doc. The v5 Doc stays as it is.

## Where things stand (end of the eighth logging chat, 26 Nov)
- The v6 Google Doc "StS v6 draft (Nov 25)" is the book (CURRENT in the bridge). In the Doc: edits 1 to 138, 141 and
  151. Logged in GitHub only: 139, 140, 142 to 205 except 151. **The next edit is 206, Chapter 27.** Edit 205 is the
  Praether scene in Chapter 17 (the arms kept off the farm; it changes edit 88). Nothing has been
  put into either Doc. Do not change the Doc; CT has not cleared it.
- Chapters 20 to 26 are rewritten and logged: 198 (Ch 25), 199 (Ch 20), 200 (Ch 21), 201 (Ch 22), 202 (Ch 23), 203
  (Ch 24), 204 (Ch 26; the rover also in Ch 32 and 33). Each has its Book now and Change to in `drafts/`. Three readers
  audited 19 to 26 and the ending; their continuity fixes are in place (plan, section 12.3).
- Chapters 27 to 36 are next, in order, to the plan's sections 10 and 11 (targets there; they total 24,084 words now).
  Then the ending lines CT says yes to (section 13). Chapter 37 to the Epilogue otherwise stay.
- make_v6.py on a fresh v5 read passes all 204 rows. verify.py on a fresh v6 read shows 19, 30, 125, 131, 135, 137,
  182, 197 and 201 PARTIAL (expected) and everything from 139 on that isn't in the Doc as "not in the Doc".
- New tool: `manuscript/tools/edits-v6/find_in_book.py` (chapters, find, claims). The Instagram synopsis check is
  `claims-instagram-synopsis.json` beside it.
- The large print PDF CT has is still the one with edits 1 to 186 (link in STATE.md). Make a new one only when he asks.
- A chapter rewrite is one edit with several ops rows; the procedure is `REFERENCE.md`, section 4.1.

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
