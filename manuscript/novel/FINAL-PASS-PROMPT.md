# Prompt for the final pass before pre-release

Written 28 Nov 2026 at the end of the seventeenth chat, on CT's ask: "Please create a prompt that would induce the final
pass that does all of those things", after asking whether the book would be polished once the habits pass finished.
Paste everything in the block below into a new chat once the habits pass is done and its PDF is in Drive.

```
This is the final pass on the novel "Surviving the Singularity" before pre-release. Use a workflow where a step needs many readers.

START
- Repos: ctavolazzi/survivingthesingularity and ctavolazzi/_workbench. Work and push only on the branch claude/singularity-publication-build-kparqk in both. Never push to main, never open or watch a pull request.
- Read, in this order: manuscript/novel/REFERENCE.md, TODO.md, the newest CHECKPOINT-*.md in manuscript/novel/, HABITS-PASS.md, WRITING-INSTRUCTIONS.md (all of it), EDIT-LOGGING-PROCEDURE.md.
- Read the v5 Doc fresh with the Docs connector (id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA), save it as V5_READ.json, and build: python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT --no-docx. Every check row must pass before you change anything. The next edit number is in TODO.md.
- The Google Docs are not touched. Every change is logged in GitHub by the procedure (EDITS.md entry, ops row, check row) and reaches me in the PDF.

MY STANDING RULES
- No em dashes or en dashes anywhere.
- My dictated words stay word for word.
- Lines that explain something a little confusing, or that carry the intensity of a moment, stay.
- The four questions the book leaves unanswered stay unanswered on purpose: what Grace and Curtis agreed, why Lou had Grace write, Priya's trial next year, and what Priya wrote on the pledge.
- "The way" can become "how", as in "how it usually did."
- Find the middle path. DO NOT OVERDO IT. Plain beats clever.
- Use code before tokens. Count with scripts, and send readers only for judgment. Grep every quote a reader returns.
- Answer me first, in a line or two. One grouped set of questions, only for what the files can't answer.

THE WORK, IN ORDER
1. Repeated phrases. Run habits.py repeats OUT/v6.txt and judge every run used three or more times, Chapter 11 on. Plants and callbacks the book means stay (Priya's pencil, "is my stuff in that thing", "Power or brain. Halve it."). Where a reader would feel it, keep the strongest use and reword the rest with the same toolbox and rules as the habits pass. Log one edit per chapter.
2. The taste pass. Its prompt is in manuscript/novel/CHECKPOINT-2026-11-27-smell.md. Use senses-2026-11-27.md: the 40 scenes where food is eaten with no taste given. Add taste only where it carries feeling, with a verb that carries the physics (my kitchen example in the guide, section 7a). Log what you add.
3. The open smell calls in smell-table-2026-11-27.md that are mine to rule on. Ask me for those in the one grouped question set. Don't invent the smells.
4. Fact check Priya's lines about the county building code in the shouse scene (Chapter 21, edit 296): a shop and a house under one roof, one inspector for each. If a line is wrong for a real Washington county, propose a fix in plain words.
5. A cover-to-cover read of the whole built book by fresh readers, split by chapters. They look for typos, continuity slips (names, dates, ages, who knows what, who is in the room), anything a first-time reader would trip on, and leftover repetition. Check every finding on the page. Fix clear errors and log them. Anything that is taste or story goes on a list for me, not into the book.
6. The scene sheet audit, section A (SCENE-SHEET-AUDIT-2026-11-27.md). Apply it to the CSV and the Google Sheet (id 13hXnHxprSx-IGW_-TOFzeJFHIpzWyicHx_NtTgaya7o) together. Rerun scene_sheet.py and every story check so the sheets match the book.
7. Build the large print PDF by "Making the large print PDF" in EDIT-LOGGING-PROCEDURE.md, with every check passing. Upload it to "StS Publication Files" as CURRENT, with the date and the edit range in the title. Rename the old CURRENT to OLD and move it to "Older builds". Put a before-and-after list of every change in this pass beside it as a Google Doc, and send me both files.
8. Drive sync. Remake the edit list mirror at the newest edit, and bring the Google Sheet's scene tab and story-check tabs to the newest edit.
9. Release check, without releasing. Run the paperback and ebook builds and the release checks in CLAUDE.md, and report what passes. Do not publish, merge or deploy. List what only I can do: the ISBN, putting the edits into the Google Doc, and the merge to main.

CLOSE
- Update TODO.md, REFERENCE.md, EDIT-LOGGING-PROCEDURE.md ("Where things stand") and a new CHECKPOINT file.
- In _workbench, update STATE.md and the top entry of sessions/LOG.md.
- Commit in small, plain commits and push both repos.
- Tell me in a few lines: the PDF link, the change list link, what you fixed, and what is waiting on me.
```
