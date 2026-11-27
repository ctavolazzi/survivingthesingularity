# Scene sheet audit, 27 Nov 2026 (for the final pass)

CT asked (27 Nov): "Check the scene spreadsheet and make sure it's fully updated, and everything is logically
consistent, timelines are on point, storylines add up ... so nothing slips through the cracks."

Done from a fresh read of v5 (revision AHj4eMResiURoAJEhT0nN-6E), built with `make_v6.py` into the book with edits
1 to 234 (all 234 check rows pass, 608 replacements), then split into scenes and checked against
`scene-sheet-2026-11-27.csv`. Three readers checked rows 1 to 70 and 106 to 138 against the scene text. Two more readers
(rows 71 to 105, and the whole timeline) stopped at a usage limit before reporting, so **rows 71 to 105 and the
end-to-end timeline are not checked here.** The final pass should do those two.

Another chat fixed 30 sheet cells after this audit began (commit f644636, "Scene sheet: 30 cells fixed"). Every item
below was checked against the sheet as it stands after that commit and is still open unless marked. Check each cell on
the page before changing it.

## 1. Mechanical

- Scenes: the sheet's 137 live rows match the book's 137 scenes one for one, plus row 59 (cut by edit 234). Pondwater
  is its own unnumbered chapter; the sheet has it right.
- Word counts the book gives now (sheet in brackets): row 19, 626 (622); row 49, 1567 (1563); row 111, 398 (394).
  Rows 53, 126 and 128 already match after f644636.
- The sheet's title still reads "edits 1 to 233"; its rows now include edit 234.

## 2. Text contradictions (the book disagrees with itself; CT's call)

1. **Ruby's "four thousand" (Ch 8, February 2024).** "Because there's four thousand of them and one of you. And
   tomorrow it'll be eight thousand." Four thousand is the first week's count ("By Friday it was four thousand
   replies and he quit counting", Ch 7, October 2023). By February the video has fifty million views. Smallest fix:
   a February number in Ruby's line.
2. **The squash (Ch 34).** In the tractor scene the squash "has to come in this week" or it will be "mush" in nine
   days, and the first wagon goes out the next morning. Two weeks later, at the October meeting and in festival week,
   "The winter squash had to come in", "We'd have the squash in by Wednesday", and the rows are "still sitting out in
   the field". Either the tractor scene moves to festival week, or its "this week" and "nine days" loosen.
3. **"They've been there since my first week" (Ch 34)**, about the arms at Praether's. Grace asks on his fourth day,
   and Praether is told the arms come Wednesday, so they arrive in his second week. Check this against commit
   2bccf50 (the lien sale corrected to Sunday) before changing it.
4. Known and already on the sheet's second tab: Elijah's age (35, 36, 37), and the route's money ("ran out in June"
   against "money through June").

## 3. Sheet cells still wrong (rows 1 to 70 and 106 to 138)

**On the page (people who speak or appear but aren't listed):**
- Row 1: add "his grandmother (in memory)".
- Row 19: add "Ma's voice on the answering machine; the friend who gave the amp and Nate (in memory)".
- Row 27: add "a man in a quarter-zip, a gray one and a sneakers one".
- Row 37: add "Chat Horizon (on screen), the cooling-company woman (by text)".
- Row 43: add "commenters, the woman in Tulsa, the elevator man, Nate, an illustrator in Petaluma (by message)".
- Row 48: add "Chat Horizon (on screen), Grace (by message)".
- Row 49: Grace is also "by email" (the April email and her reply are quoted).
- Row 69: add "a network engineer (by message)".
- Row 109: add "David and the realtors at the Bear Flag (flashback)".
- Row 112: add "the machine (on screen)".
- Row 136: add "Wes (text)".
- Row 138: add "Priya (by mail), Lou (photo)".

**When:**
- Row 15: the scene runs into that night ("He was back at the same window that night."): "a Sunday, 9:40 a.m. and
  that night, early 2023".
- Row 111, basis: the first of the month is March 1 itself (a Monday in 2027), not "before March".
- Row 121: the date clashes with the festival harvest (contradiction 2). Hold until CT decides.

**Questions (closed but never opened, or opened wrongly):**
- Row 115 opens "What happened at Mrs. Delgado's that Grace didn't tell him?" The thing she held back is the short
  payment to Irene, and she tells him at the pond in the same scene. Proposed: "Will the trust miss another payment?"
- Row 53 opens "Why must the arms stay secret?" The scene answers it itself (Lou: "Grace most of all"). Proposed:
  "Will the secret hold?"
- Row 70 opens a question the scene answers ("Who decides ...": Lou, "A person decides that").
- Row 37 repeats row 34's open question about Trent and the arms.
- Open on the earlier row, so the later close has a match: "Am I crazy?" (row 2, closed in 23); "Will his ninety days
  run out?" (row 31, closed in 34); "What is one robot arm worth?" (row 34, closed in 35); "What happened to Ma?"
  (row 38, closed in 39); "What does Elijah owe for his keep?" (row 52, closed in 58); "Will the engine light get
  fixed?" (row 49, closed in 64); "Will the boxes hold up in real heat?" (row 65, closed in 67); "Will Denny take the
  Spokane offer?" (row 101, closed in 107); "What is in the rubber-banded notebook?" (row 113, closed in 115).
- Closed with no opener anywhere; open earlier or blank the close: rows 9, 16, 29 ("Is his list right?", "Did anybody
  ask?"), 30, 31, 32, 43, 46, 50, 52 ("Where will the arms go..."), 60, 65, 110, 111, 114, 116, 117, 118, 119, 120,
  125, 127, 128, 130, 133 ("Has anyone visited Ma?"), 134 ("Will Elijah come?").
- Answered but never closed; add to the row's Closes: row 22 (match row 21's wording); row 29 ("What does Ruby want
  to show him?"); row 44 ("How will Elijah pay for the room?"); row 69 (rows 61 and 68: the hidden board comes out;
  the leak); row 70 ("How will the co-op answer the leak?"); row 129 ("you called me the lamp"; he still doesn't
  remember; Grace wanted the arms brought in); row 133 ("Will Elijah go home? Yes"); row 134 (Patricia's reports: she
  used the machine; "What did it ask?": for a vote); row 138 ("Will Elijah come back up for the pit? No").
- Opened and never closed (fine if meant): row 119 "Which of them helped him that first spring?", row 121 the dealer,
  row 124 "Who else will leave over the machines?"

**Numbers:**
- Row 52: "Highway 99" is not in this scene (it is in row 48's), and "two crates" is "a couple of big crates" on the
  page.
- Rows 16 and 17: the bill "would show up next Monday", not "due".

## 4. Checked and consistent

Ages (Tyler 19 then 21, Wren 24 in 2025, Lou 61, Denny 51); the bill ($2,011.46); two million dollars for six arms;
downloads (58,000, 66,000, 80,000); the half-pay checks; years on Walt's stove; the visitor book; the last box on Dec 28
(a Tuesday); Bidwell's reader (seven years, then eleven); the lecture's age; Thanksgiving 2027 counted down from 2022
and 2023. After edit 234, no scene before the table finds out has Grace knowing about the arms.
