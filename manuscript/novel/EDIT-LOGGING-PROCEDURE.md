# How to log CT's v5 edits (the procedure)

Written 2026-11-25 from the chat where CT read v5 and dictated edits 1 to 111. Read this before logging the next one.

## What CT is doing
CT reads the v5 manuscript and dictates changes by voice. Claude logs them. Claude does not change the Google Doc
unless CT clears it (a change goes in only as a suggestion). CT's standing words: "I just want you to log the edits."
"Stop asking for permission. You can just do it." "Don't push back. Don't overthink. Just roll with the punches."

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
4. Fix dictation errors silently when the meaning is plain (Blue = Lou, Martha = Marta). When a fix would change
   the meaning ("bleed out" vs "bug-out"), log it as he said it and ask one short question.
5. If something he asks cannot work in the book as it stands (Grace is only on speaker, Curtis is driving), say
   it in one line, give one recommendation, and wait. Once he decides, log his decision without arguing.
6. Add a check row to `manuscript/tools/edits-v5/checks.py` (words that must be in the book, words that must be
   gone; `[break]` means a scene break).
7. Run `python3 manuscript/tools/edits-v5/verify.py READ.json --table manuscript/novel/EDITS-v5-status.md`.
8. Commit (one change, plain message) and push to `claude/singularity-publication-build-kparqk`.
9. Update the Drive copy "StS v5 edit list (mirror of GitHub)" (id 1XRD8m-UJXxFkrJS0qqkuE1ftrsm_p9XzLSkWkAcqghA):
   the edit text, the Totals line, and the "Edits 104 to N" line.
10. Reply in two or three lines: the number, what it says, anything of Claude's wording, one open question at most.

## Things that have gone wrong before
- Rewriting when he said smooth ("you're overdoing it"). Adding things he didn't ask for.
- Putting his context into the page text.
- Check numbers colliding (the follow-ups row was once 90).
- An unquoted heredoc with backticks ran the build. Use quoted heredocs ('EOF').
- Counts drifting: the Totals line must match the latest verify run.

## What is still open (25 Nov)
Edits 87 to 111 are logged but not yet in the Doc. Eight Chapter 14 sentence-opening changes were given in chat and
never logged. Open for CT: Grace's April email (edit 100), "He went and looked. It was there, from April," the
duplicate "It could be a cult," "He looked around the table, then back," and edit 108 ("if he wanted to play").

## Later, when CT says go
Apply 87 onward to the Doc as suggestions, re-read, run verify. CT accepts the suggestions. Run
`build.sh` (the gate stops it until every edit is in), then refresh the Drive uploads.
