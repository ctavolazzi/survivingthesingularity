# How to log CT's edits (the procedure)

Written 2026-11-25 from the chat where CT read v5 and dictated edits 1 to 128. Read this before logging the next one.

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
1. Find the passage in the latest read of the Doc, so "Book now" is quoted exactly. Do this before writing.
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
   gone; `[break]` means a scene break).
8. Run `python3 manuscript/tools/edits-v5/verify.py READ.json --table manuscript/novel/EDITS-status.md`.
9. Commit (one change, plain message) and push to `claude/singularity-publication-build-kparqk` (CT, 25 Nov:
   "Push to kparqk, like the procedure says"), whatever branch the chat itself was given.
10. Do NOT update the Drive copy after each edit (CT, 25 Nov: it costs tokens). Refresh "StS v6 edit list
   (mirror of GitHub)" (id 1fXM4q_rP40WTSHTYzW-THeVyrXScV48jjnotUBoz5Nc) once, at the end of the session.
   It is remade from a text file (the connector cannot replace a Doc's text without retyping it), so the id
   changes each time: the newest one is here, and the old copy gets "OLD:" in its title and a pointer at the top.
11. Reply in two or three lines: the number, what it says, anything of Claude's wording, one open question at most.

## Things that have gone wrong before
- Rewriting when he said smooth ("you're overdoing it"). Adding things he didn't ask for.
- Putting his context into the page text.
- Check numbers colliding (the follow-ups row was once 90).
- An unquoted heredoc with backticks ran the build. Use quoted heredocs ('EOF').
- Counts drifting: the Totals line must match the latest verify run.

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

## The narration is hybrid (CT, 25 Nov)
CT, planning the Chapter 19 rework: "whose feelings? Elijah's and his observations of others. BUT ... we have a
hybrid narration style going on here." The book sits on Elijah's shoulder, and above him is a storyteller who knows
more than he does ("Although Elijah was quite unaware of it," edit 106), leaves him for a scene (the kitchen
trailer in Chapter 17, Bidwell, Chapter 38), goes into other heads (Tyler in Chapter 26) and talks to the reader
("Most people never do, at moments like that," edit 100). In anything Claude writes for an edit: feelings are
Elijah's, other people's come through what he sees them do, and the storyteller can tell the reader, briefly, what
Elijah cannot know.

## What is still open (26 Nov, end of the fifth logging chat)
Settled since 25 Nov: Grace's April email (edit 159), "He went and looked" and the second "It could be a cult" (edit
138), edit 103 (kept, and edit 180 makes it "then back at Elijah"), edit 108 (kept as "if he wanted to play"), edit
109 (the touch lines kept; edit 181 changes the last line), and the open questions of the Chapter 19 plan.
Open for CT, to ask one at a time with the line quoted and Claude's recommendation in one line:
- Edit 112 (Ch 18): "the co-op's gravel lot" instead of "the gravel lot" (Claude recommends it; no answer yet).
- Ch 31: "On Sunday at 9:40 he called the rose garden." It follows Marta coming by at eight that Sunday, and the
  next line is "The next morning was the first of the month." Same Sunday morning ("Later that morning, at 9:40")?
- Edit 116: "been here before" or "done this before".
- Edit 118: change only "Don't let her," or cut the whole "Grace will carry you" sentence.
- Edit 121: "one thing" (Marta) or "one real thing" (the notebook).
- Ch 13: the "dark out" 9:40 call. Night call or error?
Then, each on CT's go: the eight Chapter 14 sentence-opening fixes (written again from a fresh read, the way edit 133
was done), then "Places to look at" in `EDITS.md` (each shown to CT with a proposed fix before it is
logged).

## v6 (25 Nov)
Edits 1 to 138 are all in v6: the Google Doc "StS v6 draft (Nov 25)", the CURRENT copy in the bridge map, made by
`manuscript/tools/edits-v6/make_v6.py` (see "Applied" in `EDITS.md`). CT reads v6 in the large print PDF
and makes his final edits there. The next edit is 139. Log it the same way (number, where, "Book now," "Change
to"), add a check row in `checks.py` and a find and replace row in `manuscript/tools/edits-v6/ops.py`, and check it
against a fresh read of the v6 Doc. The v5 Doc stays as it is.

## Where things stand (end of the fifth logging chat, 26 Nov)
- The v6 Google Doc "StS v6 draft (Nov 25)" is the book CT is editing (CURRENT in the bridge). In the Doc: edits 1 to
  138, 141 and 151. Logged, not in the Doc yet: 139, 140, 142 to 182 except 151. The next edit is 183. CT has said
  nothing about putting 139 onward into the Doc; log only.
- Done in the fifth chat: 172 to 179 (Claude's recommendations for the second half: sentence openings, beats in the
  table scenes, "It's not X. It's Y." lines, the handout echo in Ch 31, the Ch 26 pond, the birds at the gate,
  packing the truck, Tuesdays); 180 (Denny looks "back at Elijah"); 181 ("Agreed on what?"); 182 (a clarity pass
  through Ch 21 to 39: pronouns, speakers, repeats). Edit 162 lost two beats that repeated a few lines later.
  172 to 179 and 182 are Claude's wording, approved by CT from a summary, not line by line.
- verify.py on a fresh read of the v6 Doc shows 30, 137 and 182 PARTIAL. That is expected: edit 182 changes words of
  30 and 137 that are already in the Doc. make_v6.py on a fresh v5 read passes every row (182).
- Quote "Book now" from make_v6.py's v6.txt (every logged edit applied), not from the raw Doc, which lacks 139 on.
- The Docs reads are too big to show in chat; the connector saves each to a file. Copy it and use it as READ.json.
- Each new edit: log it in `EDITS.md`, add a check row to `manuscript/tools/edits-v5/checks.py` and a
  find and replace row to `manuscript/tools/edits-v6/ops.py` (above the ITALIC list; italics as *...*), run
  `python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT --no-docx` (every row must pass), commit and push.
  A correction to an edit not in the Doc yet replaces it in place; a change to words already in the Doc is a new edit.
- Waiting on CT: the questions above; which of the 16 scene breaks in `SCENE-BREAKS-v6.md` to cut; the dedication
  (who it is to) for v7; the sentence-opening checker (say go).
- The large print PDF CT reads is "StS v6 large print (edits 1 to 183).pdf" in the Drive folder "StS Publication
  Files", made 26 Nov from make_v6.py's v6.docx (`publication/novel/build/build.py v6.docx --only large
  --skip-edit-gate`). Everything older is in that folder's "Older builds". Rebuild only when CT asks.

## v7 (26 Nov): a separate copy
CT: "keep v7 as a totally new, totally separate thing ... I want to keep working on v6." The Google Doc "StS v7
draft (Nov 26)" is v6 through edit 171 plus the v7-only changes in `manuscript/tools/edits-v7/ops_v7.py`
(Dedication, Thank You, "Recognize Your Power" first and last). Record: `manuscript/novel/V7-CHANGES.md`. New edits
go into v6 as before, from 172; v7 does not follow them unless CT asks.

## Later, when CT says go
Apply 87 onward to the Doc as suggestions, re-read, run verify. CT accepts the suggestions. Run
`build.sh` (the gate stops it until every edit is in), then refresh the Drive uploads.
