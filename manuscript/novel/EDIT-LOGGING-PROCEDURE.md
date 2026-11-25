# How to log CT's v5 edits (the procedure)

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
2. Write it in `EDITS-v5-pending.md` with the next number: where, "Book now," "Change to."
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
8. Run `python3 manuscript/tools/edits-v5/verify.py READ.json --table manuscript/novel/EDITS-v5-status.md`.
9. Commit (one change, plain message) and push to `claude/singularity-publication-build-kparqk` (CT, 25 Nov:
   "Push to kparqk, like the procedure says"), whatever branch the chat itself was given.
10. Do NOT update the Drive copy after each edit (CT, 25 Nov: it costs tokens). Refresh "StS v5 edit list
   (mirror of GitHub)" (id 1YIxK_1g68UoFJs00cCAbdsGOMaEMvDM9ojj5XnNs7tM) once, at the end of the session.
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
  (shows she is confused, not alarming). See the end of edit 122 in `EDITS-v5-pending.md` for the list.
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
  logged, in "Places to look at" in `EDITS-v5-pending.md`), and the other runs listed there.
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

## What is still open (25 Nov, end of the second logging chat)
Edits 87 to 136 are logged but not yet in the Doc (edit 57 was never used). The next edit is 137; CT has finished
Chapter 19. Before more Chapter 19 edits, read "Direction from CT, 25 Nov: stakes and personality conflict" at the
top of `EDITS-v5-pending.md`. Third logging chat, 25 Nov: the plan is written there ("The plan for Chapter 19");
edits 131, 132, 133, 135 and 136 get reworked in place, to that plan, when CT says go. Its section 9 lists what is
open for him. Eight Chapter 14 sentence-opening changes were given in chat and
never logged. Open for CT: Grace's April email (edit 100), "He went and looked. It was there, from April," the
duplicate "It could be a cult," "He looked around the table, then back" (edit 103), edit 108 ("if he wanted to
play"), edit 109 (the touch lines), edit 112 (gravel lot or a store), edit 116 ("been here" or "done this"), edit
118, edit 121 ("one thing" or "one real thing"), and the Chapter 13 "dark out" 9:40 call.

## v6 (25 Nov)
Edits 1 to 137 are all in v6 (`manuscript/tools/edits-v6/`, see "Applied" in `EDITS-v5-pending.md`). CT reads v6 in
the large print PDF and makes his final edits there. New edits go on from 138, as find and replace rows in
`manuscript/tools/edits-v6/ops.py` plus a check row, against the v6 text. Once the v6 Google Doc exists, it is the
CURRENT copy in the bridge map and edits are made against a fresh read of it.

## Later, when CT says go
Apply 87 onward to the Doc as suggestions, re-read, run verify. CT accepts the suggestions. Run
`build.sh` (the gate stops it until every edit is in), then refresh the Drive uploads.
