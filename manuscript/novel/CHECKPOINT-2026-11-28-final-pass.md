# Checkpoint, 28 Nov 2026: the final pass

CT, 28 Nov, same chat as edits 296 to 327: "use the tools at your disposal to perform the requested work on the
manuscript as described here in the chat." The work is `FINAL-PASS-PROMPT.md`, steps 1 to 11. Step 12, the V9 PDF, is
only on his word.

**Where it stands:** edits 1 to 347 logged; **next edit 348**. make_v6.py on the fresh v5 read (revision
AHj4eMResiURoAJEhT0nN-6E...): 801 replacements, all 348 check rows pass. `final_check.py gate`: READY. Neither Google Doc
was changed: edits 224 to 347 are in GitHub only.

## Steps 1 to 7 (edits 328 to 347)

- The checker found, from Chapter 11 on: he 123, opener 33, word 18, speaker 25, title 6, phrase 94 (98 phrase runs
  were judged by two readers first: 56 on purpose, 33 kept, 9 reworded). Every finding has a verdict in
  `final-check-ledger.csv` (kept, on-purpose, his, wrong or changed, with a note).
- 37 changes in 20 edits, one edit per chapter. Each was written by a writer and passed by two checkers (CT's ear; a
  first-time reader), then read by Claude. Two changed on that read: Marta's smell line made plainer (Ch 31), and the
  Chapter 39 "saved under *Don't*" kept, because it pays off Chapter 37. CT's own line is in edit 330 (Ch 13, the truck).
  Entries in `EDITS.md`.
- Tastes (step 5): four, each tied to something set up: the gas station pie (Ch 15), Lou's cider (Ch 26), the cold
  eggs and Curtis's salt (Ch 31); and two smells for runs of steps: welding smoke (Ch 24), the room when Marta opens
  the door (Ch 31).
- **Titles (step 3):** none of the titled moments is thin. Each is on the page: the stain shaped like Ohio (Ch 14), the
  red bin (Ch 16), HANDS at the bottom of the column (Ch 20), OWNER/OCCUPANT (Ch 23), the indignant worm (Ch 26), the
  blueprints of the wall (Ch 27), funded in ink (Ch 29), the tide pools poem (Ch 33), "This is the gate." (Ch 36), the
  new tape on the post (Ch 37), the truck over a cattle guard (Ch 38). Chapter 12's shower is on the page since edit 326.
- **Smell calls (step 6):** CT ruled on seven on 27 Nov ("Go with your leans on all seven"); now in the smell table's
  last column. **Two are still his:** the real smell of Praether's yard and barn (Ch 17; the page has Claude's "smoke lay
  down flat ... cold gear oil and mouse"), and whether Elijah tells Grace what the Thanksgiving coats bring back (Ch 27,
  new material).
- **Fact check (step 7):** Priya's first line is right for Washington (the county adopts the state code; the house
  code and the code for every other building are separate chapters, 51-51 and 51-50 WAC; nothing forbids a home and a
  shop under one roof: mixed occupancies, IBC 508, and live/work units, WAC 51-50-0508). Her second line was wrong: a
  county sends one building inspector for one building, not one per use. Edit 336 keeps her point: "The county still
  holds the whole room to the rules for a house and the rules for a shop, and we have to pass both." Sources in
  `EDITS.md`, entry 336.

## Step 8: the cover-to-cover read

Seven readers (six chapter ranges and the whole-book timeline), a checker for each, a spelling sweep of every word and a
dialogue-punctuation sweep. 38 findings, 22 refuted on the page, **16 real, all taste or story, so none was changed.**
The list for CT, and the audit's section B items still on the page: `cover-to-cover-read-2026-11-28.md`.

## Step 9: the scene sheet audit, section A

Applied to the CSV and the Google Sheet (19 cells; six items already fixed by later chats; old row 35's "about June"
superseded by the calendar's August). Matched by content, because the sheet was renumbered after the audit. Note under
section A in `SCENE-SHEET-AUDIT-2026-11-27.md`. Every story check and `habits.py sheet` rerun; the sheets match the book.

## Step 10: Drive, at edit 347

- "Surviving the Singularity: scene sheet (edits 1 to 347)", `13hXnHxprSx-IGW_-TOFzeJFHIpzWyicHx_NtTgaya7o`: the Scenes
  tab, 0 cells differ from the CSV. The "Numbers to check" tab is hand-written and was left alone.
- "Surviving the Singularity: story checks (edits 1 to 347)", `11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`: all 16 tabs,
  0 cells differ from their CSVs.
- "StS edit list, edits 1 to 347 (mirror of GitHub)", `1ZgZ-h7dP0GwdOlq378SO9A0CjhjN4AZ6fQ-iakGKTok`, checked against
  `EDITS.md` word for word. The 295 copy is "OLD:" with a pointer at its top.
- Staging file left in Drive, not trashed: "OLD: staging copy (story sheets at edit 347, 28 Nov)".

## Step 11: the release check (nothing released, merged or deployed)

- Paperback PDF, 6 x 9: 383 pages, every check passes (text letter for letter, chapters, contents page numbers, fonts,
  margins, running heads, the indent after each of the 83 scene breaks).
- Kindle ebook: every check passes; epubcheck 0 errors, 0 warnings.
- Word file for KDP: every check passes. The old italics failure is fixed (commit 6d03ae3f: pandoc moves a space out of
  an italic run, so the check counts italic letters).
- All three were built from the edit-347 text with `--no-pictures`, because the picture links in the saved v5 read have
  expired; a build with pictures needs a fresh read of the v5 Doc.
- Site, 28 Nov (no site file has changed since): `npm run check` 0 errors (314 warnings), `test:release` 0 failures,
  `build` ok, `test:cloudflare` passed, `test:launch-browser` 100 passed on Chromium (Firefox and WebKit are not in this
  container).
- **Only CT can do:** the ISBN (`isbn` is empty in `publication/novel/build/book.json`), putting edits 224 to 347 into a
  Google Doc, and the merge to `main` (which redeploys the site).

## Waiting on CT

1. The V9 PDF, on his word (`FINAL-PASS-PROMPT.md`, step 12; the gate is READY).
2. The two smell calls above.
3. The 16 items and the open audit items in `cover-to-cover-read-2026-11-28.md`.
