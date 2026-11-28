# Prompt for the final editorial review, then V9

Written 28 Nov 2026 at the close of the seventeenth chat, after the final pass (`FINAL-PASS-PROMPT.md`, steps 1 to 11,
done) and edit 348. CT: "Make the FINAL prompt for the FINAL session of editorial review before generating v9 and
showing me. It will be used to start a new conversation in a new chat." Paste everything in the block below into a new
chat.

```
This is the final session of editorial review on my novel "Surviving the Singularity" before V9. I rule on what is still open, I may give fixes while I review, and when I say go you build the V9 PDF and show it to me.

START
- Repos: ctavolazzi/survivingthesingularity and ctavolazzi/_workbench. Work and push only on the branch claude/singularity-publication-build-kparqk in both. Never push to main, never open or watch a pull request.
- Read, in this order: manuscript/novel/TODO.md, CHECKPOINT-2026-11-28-final-pass.md, cover-to-cover-read-2026-11-28.md, WRITING-INSTRUCTIONS.md (all of it), EDIT-LOGGING-PROCEDURE.md, REFERENCE.md.
- Read the v5 Doc fresh with the Docs connector (id 1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA), save it as V5_READ.json, and build: python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT --no-docx. Every check row must pass (349 rows at edit 348). Then python3 manuscript/tools/edits-v6/final_check.py selftest (21 of 21) and final_check.py gate OUT/v6.txt (READY). The next edit number is in TODO.md (349 when this was written).
- The Google Docs are not touched. Every change is logged in GitHub by the procedure: an EDITS.md entry, an ops row, a check row, and the scene sheet's word count.
- Tell me in one line that you are ready and what the next edit number is, then show me the first three or four items of step 1.

WHERE THINGS STAND (28 Nov)
- Edits 1 to 348 are logged in GitHub. The v8 Doc holds edits 1 to 223; edits 224 to 348 are in GitHub only. The final pass is done: every checker finding has a verdict, final_check.py gate is READY, the paperback, ebook and Word builds pass, and Drive is at edit 348 (the scene sheet, the story checks, and the edit list mirror "StS edit list, edits 1 to 348 (mirror of GitHub)", id 1xi1nPtyBXSWrqqoUQurS609msWcjXKr20HFVmixXGlU).
- The PDF I have is "StS v8 large print CURRENT (28 Nov, edits 1 to 322, the habits pass).pdf" (Drive id 1SS145ExuGZIvprNmiIKC-brau1aSOx8D). Nothing since edit 322 is in a PDF.
- Do not build a PDF until I say go.

THIS SESSION, IN ORDER
1. The open list. Walk me through manuscript/novel/cover-to-cover-read-2026-11-28.md in book order, three or four items at a time. For each: the chapter, the line as it stands now (grep it in OUT/v6.txt), the problem in one sentence, whose words it is, and the suggested fix if the list has one. Then the audit items still on the page (the list's last section; its numbers are the audit's own, not the list's), the same way: for each, give the reason it was left on 27 Nov (the table in CHECKPOINT-2026-11-27-seventeenth.md) and trace whose words with manuscript/tools/edits-v6/whose_words.py. I rule on each one. After each batch, stop until I have ruled on every item in it.
   - If I change it, log it as the next numbered edit. My words go in word for word. If I say "use your fix", log the list's fix.
   - If I leave it, write my ruling beside the item in the list (for example "CT, date: leave").
   - Items 1 to 4 of the list, and audit items 1, 2 and 3 (Ruby's count, the Chat Horizon price, the paperback's word), are in Chapters 0 to 10, the published sample. I said those chapters are fine, so show them for the record and change one only on my word. If I change one, add a line to TODO.md that the free sample on the site has to be remade. Don't touch the site.
   - Don't change anything on the list without my word. Don't start new passes or sweeps.
2. Two more things that are mine to rule on. The last smell call: whether Elijah tells Grace what the Thanksgiving coats bring back for him (Chapter 27, new material). And two of your lines in edit 296 (Chapter 21, the shouse) that were flagged as saying too much and that I never ruled on: "Two orange robot arms were sitting in crates in Richard Praether's pole barn, doing nothing. An idea had started up in Elijah, and he let it run." and "Nobody had ever told him you were allowed to put them together." Show me each in its paragraph. Ask me; write and change nothing unless I say.
3. While I review I may send fixes, screenshots or dictation. Each fix is the next numbered edit, logged right away. When I restate a line, the last version is the line. Fix only dictation breaks. When I give beats instead of lines, write it by the guide, show me the passage, mark your own choices, and log it when I say.
4. After each batch of edits: rebuild (every row must pass), run final_check.py run OUT/v6.txt V5_READ.json and give any new finding a verdict (fix it only with my word), confirm final_check.py gate says READY, update the scene sheet's word counts (scene_sheet.py check must pass), and rerun the story checks. Each story check stops on a quote that an edit removed: move that quote to the new words. Commit and push.
5. When I say go: V9.
   - final_check.py gate must say READY (not build_gate.py, whose open boxes in TODO.md are old) and every check row must pass.
   - Set "version" to "v9" in publication/novel/build/book.json.
   - Build the large print by "Making the large print PDF" in EDIT-LOGGING-PROCEDURE.md: in this container first pip install -r publication/novel/build/requirements.txt and mkdir -p publication/novel/work, then make_v6.py V5_READ.json OUT --no-pictures (the large print has no pictures, the picture links in a read expire, and --no-pictures drops the picture-only paragraphs so none prints as a scene break), then python3 publication/novel/build/build.py OUT/v6.docx --only large --skip-edit-gate. Every check in publication/novel/output/CHECKS.md must pass, including the indent after every scene break. Run final_check.py pdf on the PDF too. Look at the first five and last five pages.
   - The before-and-after list: every change since edit 322 (edits 323 to the last one, and the scene-break indent fix), in book order, each with its chapter, the V9 page number, the words before, the words after, and whose words they are. Find each page by searching the PDF's page text for the new words. Make it the way manuscript/novel/habits-pass-before-and-after-2026-11-28.md was made, and save it in GitHub beside that file.
   - Upload the PDF to the Drive folder "StS Publication Files" (id 1QmqU-MsDcqfh1sC5Q_DsGeqcdyf_kLB_) as "StS v9 large print CURRENT (date, edits 1 to N, the final review).pdf". Rename the v8 CURRENT "OLD: StS v8 large print (28 Nov, edits 1 to 322, the habits pass).pdf" and move it to "Older builds" (id 12CbC-hEUy_5rArVtz8v393rc_ciV9Ltv). Upload the before-and-after list beside the PDF as a Google Doc (text/plain).
   - Show me: send me both files and both Drive links.

MY STANDING RULES
- No em dashes or en dashes anywhere.
- Do exactly what I ask. Add nothing: no extra passes, files, lines or pull requests. If something else matters, say it in one line at the end.
- Answer in a line or two. If I ask a question, answer it; don't act on it.
- Lines that explain something a little confusing, or that carry the intensity of a moment, stay.
- The four questions the book leaves unanswered stay unanswered on purpose: what Grace and Curtis agreed, why Lou had Grace write, Priya's trial next year, and what Priya wrote on the pledge.
- Plain beats clever. Find the middle path; DO NOT OVERDO IT. The ending (Chapter 37 on) gets the lightest touch.
- Search the book for every new phrase so nothing repeats. Check facts against the page before you write: names, dates, who knows what.
- "How" and "like" in place of "the way" are at their caps; don't use more of either without asking me.
- Code before tokens: count with scripts, grep every quote, and send readers only where judgment is needed.
- Outside the open list, the two rulings in step 2 and my fixes: one grouped set of questions, only for what the files can't answer.

CLOSE
- Update TODO.md, EDIT-LOGGING-PROCEDURE.md ("Where things stand"), and a new CHECKPOINT file; REFERENCE.md only if a procedure changed. Add any lesson from my corrections to WRITING-INSTRUCTIONS.md in the same turn I give it.
- Drive, once, at the end: remake the edit list mirror at the newest edit (upload EDITS.md as text/plain to "StS Publication Files"; the current mirror, id 1xi1nPtyBXSWrqqoUQurS609msWcjXKr20HFVmixXGlU, gets "OLD:" in its title and a pointer at its top), and bring the scene sheet's Scenes tab and the story checks tabs to the newest edit. Retitle both spreadsheets with the edit range.
- In _workbench, update STATE.md and add one entry for this chat to the top of sessions/LOG.md.
- Commit in small, plain commits and push both repos.
- Tell me in a few lines what you changed and what is waiting on me.
```
