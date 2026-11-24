# The final check on v5, 24 November 2026

The code behind the last editing session on "StS v5 draft (Nov 23)" before the author's own hand
pass. He asked for proof that the whole manuscript had been read and that every agreed change was in
it: "Write code to ensure this is the case. I need this to be ironclad."

None of these files holds a Google Doc id, and none writes to a Doc. Run them with `python3 -I`.
Find the current manuscript through the bridge first (`node scripts/sts-bridge.mjs status`).

| File | What it does |
| --- | --- |
| `verify_v5.py DATA_DIR` | The checker. 93 checks in nine groups (below). Writes `verify_report.txt` into DATA_DIR. Exits 1 on any FAIL. |
| `selftest.py DATA_DIR WORK_DIR` | Shows the checker can fail. It plants 21 faults, one at a time, in copies of the manuscript and requires the named check to catch each one. |
| `line_edits.json` | The 24 edits of the session that can be written as find and replace, each with the words before and after: 15 from the final edit, 3 in Chapter 35, and 6 from the last changes (Chapters 19, 31, 33, 38 and 39). The two paragraph moves (Chapter 39, and the close of the stove scene in Chapter 35) are written into the checker. |
| `reviewed_vocabulary.txt` | Every distinct word in v5 (5,403), read through by eye. The spelling check fails on any word that is not in it. There was no dictionary on the machine. |
| `verify_report-2026-11-24.txt` | The last run: 93 pass, 0 fail, 0 warnings, 7 open items. |
| `bible_entries.py V5.txt OUT.json` | Built the 21 new Character Bible entries and the minor characters list. It looks up every quotation in the v5 text, takes the chapter from the text, and stops if a quotation is not there word for word. |
| `bible_to_md.py READ.json` | Turns a Docs read of the Character Bible into `manuscript/NOVEL-CHARACTER-BIBLE-2026-11-23.md`. |

## What the checker checks

- **A. Coverage.** The Doc's text today is, byte for byte, the text that was read line by line. The
  read covered lines 1 to 3,629 (3,634 after the last changes). No line was long enough to be cut off.
- **B. Edits.** Today's text is the text at the start of the session plus exactly the agreed edits
  (16, then 4 in Chapter 35, then the last changes). Nothing else changed.
- **C. Locked lines.** Each is still word for word what it was.
- **D. Rules.** No dashes, straight quotes only, "never once" only in speech, "hand flat" only where
  he allows it, the nicknames in their chapters, the canon lines.
- **E. Continuity.** The calendar, the recurring numbers, the ages, the visitor book, the Appendix dates.
- **F. Structure.** The contents list against the 53 headings, Chapters 0 to 39, one tab, no
  suggestions waiting, 19 pictures, 78 scene breaks, quotation marks and parentheses closed.
- **G. Formatting.** One font and size, no stray styles, headings are real heading paragraphs.
- **H. Italics.** Nothing that was italic lost its italics, and every spot fixed in the session is italic.
- **I. Hygiene.** Doubled words, spacing slips, spelling, repeated sentences, stacked paragraph
  openers. A flag that was read and accepted is listed in `REVIEWED` in the code, with the reason.

Seven things are printed as OPEN and never counted as passed, because code cannot settle them. They
are the author's calls and the things nobody has looked at yet (how the file renders on a Kindle).

## The data it needs, and why it is not here

DATA_DIR must hold six files. `line_edits.json` and `reviewed_vocabulary.txt` are in this folder. The
other four are the full text of the novel, so they are not in this public repository:

| File | What it is | sha256, first 16 |
| --- | --- | --- |
| `current_export_raw.txt` | A plain text export of the Doc, as downloaded after the last changes. (At the end of the whole-book read it was `50569d5afaaeff33`.) | `630868ac0d45bbea` |
| `text_as_read.txt` | The same text with carriage returns and the byte order mark removed. The whole book was read at `3384929ad6b10ecd`; the later changes were then read in comparisons of the exports before and after, which showed no other difference. | `272b61cfc2b25567` |
| `session_start_export.txt` | The export from before the session's first edit. | `468f949d131d6e1b` |
| `current_doc.json`, `session_start_doc.json` | Docs reads at the same two moments, for formatting and italics. | |

The Doc's version history for 24 November 2026 should hold both moments. That was not checked.

## After the author's hand pass

Groups A, B, G and H compare the Doc with this session, so they will report his changes as
differences. That is what they are for. Groups C to F and I still apply to any later text, and so
does `manuscript/tools/editor-pass/preflight.py`. To check a later text against a new starting
point, give the checker that day's files as the session start and an empty `line_edits.json`, and
take the Chapter 39 move out of group B.
