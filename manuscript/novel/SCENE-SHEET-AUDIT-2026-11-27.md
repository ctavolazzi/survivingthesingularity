# Scene sheet audit, 27 November (for the final pass)

Written by the v5 edit-logging chat (edits 104 to 128) at CT's request: "Check the scene spreadsheet and make sure it's
fully updated, and everything is logically consistent." Read-only: the Sheet and the book were NOT changed. The final
pass applies these. If a later edit (235 on) already fixed one, it is superseded; check the page first.

Method: fresh read of v5, `make_v6.py` (all 234 rows pass, 608 replacements), book split at its scene breaks and
matched to the Sheet's 137 live rows (row 59 is the cut placeholder), then four readers checked every cell against
its scene text. A fifth reader (whole-book timeline, the 9:40 calls, the Tuesdays) stopped on a usage limit and did not
report: **that check is still to do.**

## Verified mechanically
- Google Sheet `1vReMI4VKBIexpMvR8Sx0QpyO8Bde2w2jLOnKFCv0KYY` equals `scene-sheet-2026-11-27.csv`, cell for cell.
- 136 of 137 scenes match the Sheet on Words and Opens with. Exceptions: **row 128** Words 324 is now 333 (edit 234
  added "She had hardly spoken to him since the meeting."; the 234 update missed this row); **row 138** Words 1933
  counts the back matter (the Epilogue alone is 290). Row 112: 470 vs 471 (trivial).
- The Sheet's title says "edits 1 to 233"; it has 234 in rows 52, 53, 59, 123. Retitle after the fixes.

## A) Sheet fixes (cell corrections)
- Row 18 When (basis): "inferred: 'on a Wednesday', some time after the meter audit".
- Row 22 Closes: "How will people react to the video? (partly: Ma, David and Nate answer; Wes silent)".
- Row 23 Numbers: "around four one morning in December (Am I crazy?)".
- Row 27 On the page: add "the man from Washington (flag pin)".
- Rows 29, 31 Closes: questions no row opened ("Is his list right?", "Why did they bring Elijah to the dinner?"); add
  the Opens earlier or reword.
- Row 35 When: "late spring or early summer 2024, within three weeks of meeting Trent (estimate: about June)".
- Row 37 On the page: add "the woman with the cooling company (by text)".
- Row 48 On the page: add "Grace (by message), a woman from Trent's office (by message)".
- Row 69 On the page: add "a network engineer, one of Denny's subscribers (by message)".
- Row 70: "Who decides when the machine is better?" is answered in the same scene; move to Closes.
- Row 71 On the page: add Marta. Row 73 What happens: Bidwell "realizes Lou Parker is likely his half-cousin" (not
  "learns"). Row 77 When (basis): the Sunday after he mailed the print. Row 80: add Frank lets Tyler go. Row 82 Where:
  add the shouse shelf. Row 84 Threads: add the arms. Row 98 When: add the coda, monthly readings through March 2027.
  Row 99: Marta in person, then radio. Row 101: Rosa (by note). Row 102: add six the next morning, the east bed.
- Row 123 Closes (edit 234): "Does Grace know about the arms? No: she learns here, and that Lou helped move them".
- Row 126 Opens (edit 234): "Will Grace speak to him again?" (the arms are not in the scene).
- Row 128 Words: 333.

**Applied 28 Nov (the final pass, step 9)**, to `scene-sheet-2026-11-27.csv` and the Google Sheet together. The sheet
was renumbered after this audit (129 scenes now), so each item was matched to its current row by the scene's opening
words, and each cell was checked on the page first. Old row to current #: 18 to 14, 22 to 17, 23 to 18, 27 to 22, 29 to
23, 31 to 24, 35 to 27, 37 to 28, 48 to 39, 69 and 70 to 57 (merged), 71 to 58, 73 to 60, 77 to 64, 80 to 67, 82 to 69,
84 to 71, 98 to 90, 99 to 91, 101 to 93, 102 to 94, 123 to 115, 126 to 117, 128 to 119.
- Applied (19 cells): #14 When (basis), and "Is his list right?" opened there ("Then tell me I'm wrong."); #17 Closes;
  #23 opens "Why did they bring Elijah to the dinner?" ("I brought you one," Ruby said ... "The guy with the list.");
  #28, #39, #57 and #93 On the page; #57 "Who decides when the machine is better than we are?" moved to Closes (Lou: "A
  person decides that"); #60 What happens; #64 When (basis); #67 Frank lets Tyler go; #69 Where; #71 Threads; #90 When;
  #94 When and Where; #115 Closes ("Here, and that Lou helped move them", kept in the words #42 opens it with). The two
  new questions have verdicts in `story_checks.py` PLANTS.
- Already fixed by a later chat: #18 Numbers, #22 (the man from Washington), #58 (Marta), #91 (Marta in person, then
  radio), #117 ("Will Grace talk to him again?"), #119 Words (333).
- Superseded: old row 35's "about June". The calendar sheet and Chapter 12 ("three weeks in August 2024"; the stroke is
  the Sunday after the launch, 31 August) put the ride with Gus in August, as #27 already says.

## B) Book continuity issues found (for CT; none changed)
1. Replies go backward: Ch 7/8 "By Friday it was four thousand replies" (October) vs Ruby in February "there's four
   thousand of them ... tomorrow it'll be eight thousand" with fifty million views.
2. Chat Horizon "for free" (row 3) vs "twenty dollars a month" five weeks later (row 5); no paid tier set up.
3. Nate's paperback: only "Turning" is its word (row 6), but row 30 says "the last two words ... belonged to Nate's
   paperback".
4. Who sent Ma the video: Elijah sent it to her chat and she replied at 6:10 (rows 21, 22), then "The Hollis girl sent
   it to me" (row 24). Deliberate irony or a contradiction.
5. Trent's "six robot arms coming down from Oakland" / "two spare ... with your name on 'em" (row 34) vs Gus's arms from
   Fremont (row 35): whose arms are they.
6. Lien sale days: "eleven days out" from a Wednesday, arrive Tuesday (day 6), "the fourth day", "This Friday", arms due
   "on Wednesday": the count and "This Friday" can't both hold (rows 48 to 52). Also open in the Riemann checkpoint.
7. Grace's April email says "Everyone here at the farm agrees ... formal invitation" (row 49) vs her later message
   "Half the table thinks you're right" and Marta's "Did the table invite a person?" (rows 48, 51).
8. Wes "had sent nothing" (row 66) though he sent "is my stuff in that thing" and "is this true" (row 45).
9. Crackers: "He ate the crackers." (row 48) then "A sleeve of crackers with two left" in the truck (row 56).
10. Ma is in the rose-garden chair on Thursday (row 46) before the place is first paid on Friday (row 44).
11. Board timing (soft): order "Earlier that April", a month on the first design, plus the late-April spiral, vs
    "In April Marta had run her finger along the drawing" (rows 60, 61, 69, 70).
12. Squash harvest: under way in Ch 34's first scene (row 121) but still ahead at the mid-October meeting and after
    it (rows 123, 125).
13. Route boxes packed on "the Wednesday of festival week" (row 128) though the route runs Tuesdays (rows 120, 123, 131).
14. Epilogue visitor book: David every Sunday sits between Melody's second Saturday and Elijah's Wednesday, so "Some
    weeks he signed right under her" needs David to skip.
15. Grace and the house sale: row 78's "two pages" may mean she knew he sold; then row 101's secret is the buyer (the
    LLC), not the sale. The page doesn't say which.
Checked and fine: edit 234 holds everywhere (no line has Grace knowing about the arms before Ch 34); ages of Elijah,
Lou, Tyler; June 12 2026 a Friday; 1 March 2027 a Monday; the 800 miles; the pawn ticket in May.

## Still to do in the final pass
- The whole-book timeline against the Appendix, every 9:40 call (one at night on purpose; Ch 13 "It was dark out"),
  and the 31 "Tuesday"s.
- Apply section A to the Sheet and the CSV together, then retitle the Sheet.
