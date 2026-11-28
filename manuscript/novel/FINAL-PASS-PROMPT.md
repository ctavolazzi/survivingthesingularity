# Prompt for the final pass before pre-release

**Done 28 Nov 2026 (steps 1 to 11; `CHECKPOINT-2026-11-28-final-pass.md`). The next prompt is `FINAL-REVIEW-PROMPT.md`.**

Written 28 Nov 2026 at the end of the seventeenth chat, on CT's ask. First version: "Please create a prompt that would
induce the final pass that does all of those things." This version, the same day, after he caught a run of "He"
openers in Chapter 13 and logged edits 323 to 326 while reading the habits-pass PDF: "Yes, output a continuation prompt
for a new chat that would induce all of this behavior and save it to GitHub." The first version is in git history.
Paste everything in the block below into a new chat.

```
This continues the work on my novel "Surviving the Singularity" toward pre-release: the final pass, and logging my edits while I read. Use a workflow where a step needs many readers, sized to the job.

START
- Repos: ctavolazzi/survivingthesingularity and ctavolazzi/_workbench. Work and push only on the branch claude/singularity-publication-build-kparqk in both. Never push to main, never open or watch a pull request.
- Read, in this order: manuscript/novel/REFERENCE.md, TODO.md, the newest CHECKPOINT-*.md in manuscript/novel/, HABITS-PASS.md, WRITING-INSTRUCTIONS.md (all of it), EDIT-LOGGING-PROCEDURE.md.
- Read the v5 Doc fresh with the Docs connector (id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA), save it as V5_READ.json, and build: python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT --no-docx. Every check row must pass before you change anything. The next edit number is in TODO.md (328 when this was written).
- The Google Docs are not touched. Every change is logged in GitHub by the procedure: an EDITS.md entry, an ops row, a check row, and the scene sheet's word count.

WHERE THINGS STAND (28 Nov)
- I'm reading "StS v8 large print CURRENT (28 Nov, edits 1 to 322, the habits pass).pdf" in Drive, with the before-and-after list beside it.
- Logged since, and not in any PDF yet: edits 323 to 327 (my fixes while reading: "Folks", who asks Gus, Elijah's state of mind in the truck, the shower, "Figures"), and a build fix so the paragraph after a scene break keeps its indent.
- Do not build a new PDF until I say so ("I'll let you know when we're ready to produce a new PDF").

WHILE I READ
- I'll send screenshots and dictation. Each fix I give is the next numbered edit, logged right away by the procedure.
- My words go in word for word. When I restate a line, the last version is the line. Fix only dictation breaks.
- When I give beats rather than lines, write it by the guide, log it, and show me the passage. Mark your own choices.
- Search the book for every new phrase so nothing repeats. Check facts against the page before you write: names, dates, who knows what.
- Answer in a line or two. If I ask a question, answer it; don't act on it.

MY STANDING RULES
- No em dashes or en dashes anywhere.
- Lines that explain something a little confusing, or that carry the intensity of a moment, stay.
- The four questions the book leaves unanswered stay unanswered on purpose: what Grace and Curtis agreed, why Lou had Grace write, Priya's trial next year, and what Priya wrote on the pledge.
- "The way" can become "how", as in "how it usually did." The habits pass used "how" and "like" up to their caps; don't use more of either without asking me.
- Find the middle path. DO NOT OVERDO IT. Plain beats clever. The ending (Chapter 37 on) gets the lightest touch.
- Code before tokens. Count with scripts, send readers only for judgment, and grep every quote a reader returns. The habits pass cost about 6 million tokens for 40 agents; don't spend like that where a script will do.
- One grouped set of questions, only for what the files can't answer.

THE FINAL PASS, IN ORDER (Chapter 11 to the end; 0 to 10 are the published sample). It ends in the V9 PDF.

The checker is manuscript/tools/edits-v6/final_check.py. Read its docstring first: it has my words for each check. It finds; you judge and write. Run `final_check.py selftest` (21 of 21 must pass), then `final_check.py run OUT/v6.txt V5_READ.json`. On 28 Nov, at edit 326, it found 318: he 134, opener 35, word 18, speaker 26, title 6, phrase 99, habit 0, mechanics 0.

How to work a check: `final_check.py batch OUT/v6.txt V5_READ.json --check NAME` prints the next open findings in context, with whose words each sentence is. For each one, either fix it (a logged edit, then `mark ID --verdict changed --edit N`) or leave it and say why (`mark ID --verdict kept|his|on-purpose|wrong --note "..."`). Rebuild and run again after each batch of edits. The pass is done when `final_check.py gate OUT/v6.txt` says READY. Don't mark things kept just to get there: most "maybe on purpose" findings are on purpose, and most of the rest deserve a real look.

1. he (134 passages). My words: "There's a whole lot of he he he he in this section." Each passage is printed with every sentence tagged step, mind, state, texture or other, and with the scene's sense counts. The fix is not reshuffling. My example, Chapter 13: "He needed a charge. He started the truck, plugged the phone into the lighter, and sat there..." becomes "the truck started up without issue, which pleased Elijah and gave him a sense of relief." My words: "instead of just repeating like what happened in a sequence, we're adding emotional timbre and texture to the story. We could even add a smell or another physical sense in moments like this." So find the step that could be about something else (the truck, the air, a smell) and say how it lands on him. Change the fewest sentences that break the run. Swapping "He" for "Elijah" is the same problem. Runs marked "maybe on purpose" ("He said ... He said ... He said") usually stay. Where a passage holds my own dictated lines, show me your version before logging it; the opening of Chapter 13 is mine and I flagged it myself, so that one is cleared. Start with `--worst` to see the heaviest, then go in book order. One edit per chapter.
2. opener (35), word (18), speaker (26). Same way. For speaker, the fix is usually a tag in my plain manner ("Elijah asked." "Gus replied, focused on the road."). For word, keep speech where a person repeats himself on purpose ("really important to me" four times is mine).
3. title (6 flagged), and `final_check.py titles OUT/v6.txt` for the whole table. The checker can't tell a moment on the page from one that happens off it (Chapter 12's shower was there in five sentences and still wasn't on the page), so read the table and tell me which titled moments feel thin. Don't write new scenes for them without asking me.
4. phrase (99 runs of five to nine words used three or more times). Plants and callbacks the book means stay (Priya's pencil, "is my stuff in that thing", "Power or brain. Halve it."). Where a reader would feel it, keep the strongest use and reword the rest.
5. The taste pass. Its prompt is in manuscript/novel/CHECKPOINT-2026-11-27-smell.md. Use senses-2026-11-27.md, the scenes where food is eaten with no taste given. Add taste only where it carries feeling, with a verb that carries the physics (my kitchen example, guide section 7a). It can share edits with step 1, since a sense is one of my fixes for a run of steps.
6. The open smell calls in smell-table-2026-11-27.md that are mine to rule on. Ask me for those in the one grouped question set. Don't invent them.
7. Fact check Priya's lines about the county building code in the shouse scene (Chapter 21, edit 296): a shop and a house under one roof, one inspector for each. If a line is wrong for a real Washington county, propose a fix.
8. A cover-to-cover read by fresh readers, split by chapters, for typos, continuity slips (names, dates, ages, who knows what, who is in the room), anything a first-time reader would trip on, and leftover repetition. Check every finding on the page. Fix clear errors and log them. Anything that is taste or story goes on a list for me.
9. The scene sheet audit, section A (SCENE-SHEET-AUDIT-2026-11-27.md). Apply it to the CSV and the Google Sheet (id 13hXnHxprSx-IGW_-TOFzeJFHIpzWyicHx_NtTgaya7o) together. Rerun scene_sheet.py, every story check and habits.py sheet so the sheets match the book.
10. Drive sync. Remake the edit list mirror at the newest edit, and bring the Google Sheet's scene tab and story-check tabs to the newest edit.
11. Release check, without releasing. Run the paperback and ebook builds and the release checks in CLAUDE.md, and report what passes. The Word build already fails one check ("italics differ: 13777 vs 13781"), which is older than the habits pass; find it and fix it. Do not publish, merge or deploy. List what only I can do: the ISBN, putting the edits into the Google Doc, and the merge to main.
12. When I say so: the V9 PDF. `final_check.py gate` must say READY first. Set "version" to "v9" in publication/novel/build/book.json, then build the large print by "Making the large print PDF" in EDIT-LOGGING-PROCEDURE.md, every check passing (the build now also proves the paragraph after each scene break is indented). Upload it to "StS Publication Files" as "StS v9 large print CURRENT (date, edits 1 to N)", move the old CURRENT to "Older builds" as OLD, put a before-and-after list of every change since edit 322 beside it with PDF page numbers, and send me both files.

CLOSE
- Update TODO.md, REFERENCE.md, EDIT-LOGGING-PROCEDURE.md ("Where things stand") and a new CHECKPOINT file. Add any lesson from my corrections to WRITING-INSTRUCTIONS.md in the same turn I give it.
- In _workbench, update STATE.md and the top entry of sessions/LOG.md.
- Commit in small, plain commits and push both repos.
- Tell me in a few lines what you changed and what is waiting on me.
```
