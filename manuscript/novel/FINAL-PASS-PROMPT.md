# Prompt for the final pass before pre-release

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
- Read the v5 Doc fresh with the Docs connector (id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA), save it as V5_READ.json, and build: python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT --no-docx. Every check row must pass before you change anything. The next edit number is in TODO.md (327 when this was written).
- The Google Docs are not touched. Every change is logged in GitHub by the procedure: an EDITS.md entry, an ops row, a check row, and the scene sheet's word count.

WHERE THINGS STAND (28 Nov)
- I'm reading "StS v8 large print CURRENT (28 Nov, edits 1 to 322, the habits pass).pdf" in Drive, with the before-and-after list beside it.
- Logged since, and not in any PDF yet: edits 323 to 326 (my fixes while reading: "Folks", who asks Gus, Elijah's state of mind in the truck, the shower), and a build fix so the paragraph after a scene break keeps its indent.
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

THE FINAL PASS, IN ORDER (Chapter 11 to the end; 0 to 10 are the published sample)
1. Sentence openers. My words: "There's a whole lot of he he he he in this section." The check exists and nothing has ever fixed what it finds. Run python3 manuscript/tools/edits-v6/openers.py OUT/v6.txt --ch 11-40. My example is the opening of Chapter 13: "He decided not to go to the hospital. He was tough. He could tough it out. He left the lot... He had a quarter tank and no money." Keep runs that are deliberate (lists like "The horse. The rifle. The radio." and repetition for weight). Vary the rest with the guide's section 10: start a sentence with whatever it is about. Swapping "He" for "Elijah" ten times is the same problem. Same rules as the habits pass (HABITS-PASS.md): only what the check flags, your best version, my dictated lines left alone, one edit per chapter.
2. Repeated phrases. Run habits.py repeats OUT/v6.txt and judge every run used three or more times. Plants and callbacks the book means stay (Priya's pencil, "is my stuff in that thing", "Power or brain. Halve it."). Where a reader would feel it, keep the strongest use and reword the rest. Log one edit per chapter.
3. The taste pass. Its prompt is in manuscript/novel/CHECKPOINT-2026-11-27-smell.md. Use senses-2026-11-27.md, the scenes where food is eaten with no taste given. Add taste only where it carries feeling, with a verb that carries the physics (my kitchen example, guide section 7a).
4. The open smell calls in smell-table-2026-11-27.md that are mine to rule on. Ask me for those in the one grouped question set. Don't invent them.
5. Fact check Priya's lines about the county building code in the shouse scene (Chapter 21, edit 296): a shop and a house under one roof, one inspector for each. If a line is wrong for a real Washington county, propose a fix.
6. A cover-to-cover read by fresh readers, split by chapters, for typos, continuity slips (names, dates, ages, who knows what, who is in the room), anything a first-time reader would trip on, and leftover repetition. Check every finding on the page. Fix clear errors and log them. Anything that is taste or story goes on a list for me.
7. The scene sheet audit, section A (SCENE-SHEET-AUDIT-2026-11-27.md). Apply it to the CSV and the Google Sheet (id 13hXnHxprSx-IGW_-TOFzeJFHIpzWyicHx_NtTgaya7o) together. Rerun scene_sheet.py and every story check so the sheets match the book.
8. Drive sync. Remake the edit list mirror at the newest edit, and bring the Google Sheet's scene tab and story-check tabs to the newest edit.
9. Release check, without releasing. Run the paperback and ebook builds and the release checks in CLAUDE.md, and report what passes. The Word build already fails one check ("italics differ: 13777 vs 13781"), which is older than the habits pass; find it and fix it. Do not publish, merge or deploy. List what only I can do: the ISBN, putting the edits into the Google Doc, and the merge to main.
10. When I say so: the PDF. Build the large print by "Making the large print PDF" in EDIT-LOGGING-PROCEDURE.md, every check passing. Upload it to "StS Publication Files" as CURRENT with the date and edit range, move the old CURRENT to "Older builds" as OLD, put a before-and-after list of every change since edit 322 beside it with PDF page numbers, and send me both files.

CLOSE
- Update TODO.md, REFERENCE.md, EDIT-LOGGING-PROCEDURE.md ("Where things stand") and a new CHECKPOINT file. Add any lesson from my corrections to WRITING-INSTRUCTIONS.md in the same turn I give it.
- In _workbench, update STATE.md and the top entry of sessions/LOG.md.
- Commit in small, plain commits and push both repos.
- Tell me in a few lines what you changed and what is waiting on me.
```
