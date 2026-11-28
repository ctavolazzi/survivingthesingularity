# The cover-to-cover read, 28 Nov 2026 (the final pass, step 8)

CT asked for "a cover-to-cover read by fresh readers, split by chapters, for typos, continuity slips (names, dates,
ages, who knows what, who is in the room), anything a first-time reader would trip on, and leftover repetition. Check
every finding on the page. Fix clear errors and log them. Anything that is taste or story goes on a list for me."

**What was read:** the book with edits 1 to 347 (`make_v6.py`'s `v6.txt`: 110,540 words from the dedication to the Thank You), every line. Six fresh readers
took it in chapter ranges (front matter to Ch 10, 11 to 16, 17 to 22, 23 to 27, 28 to 33, 34 to the Thank You). A
seventh read the whole book for the timeline only: the Appendix, every 9:40 call, every Tuesday, the ages. Each reader's
findings went to a separate checker, who opened every line, searched the whole book for the other side, and threw
out what did not hold (default: refuted). Claude added a spelling and name sweep of every word (a dictionary check)
and a dialogue-punctuation sweep.

**Result:** 38 findings, 22 refuted on the page, **16 real, all of them taste or story, so all of them are here for
CT. No clear errors: nothing in the book was changed by this step.** The spelling sweep found no misspelled words (every
word the dictionary did not know is meant: the Spanish grace, "jin", "festy", "Madrona" on the lanyard, "manny" in a
text). The punctuation sweep found one action used as a speech tag, item 4 below.

Line numbers are `v6.txt`'s at edit 347. "Whose words" was traced with `whose_words.py` and `EDITS.md`. A fix is given
where the reader had one; it is a suggestion only.

## Chapters 0 to 10 (the published sample: CT said these are fine, so these are for the record)

1. **Ch 0, line 79, "He drew, in the hours nobody paid for."** A new paragraph that names only Nate and Wes, so "He"
   reads as Wes for a moment, and five lines on Wes is the one who makes the flyers. Edit 3's paragraph split (CT's)
   cut it off from Elijah. Fix: "Elijah drew, in the hours nobody paid for." CT's words.
2. **Ch 0, line 104, "he had helped it, a lot faster than he thought possible."** Hard to parse first time: "it" is
   PorusAI's machine while he works at Claypot, and "a lot faster" could belong to either verb. Already flagged and kept
   at edit 252. CT's dictation, Claude's wording.
3. **Ch 5, line 429, "didn't plug anything into it again, as a monument".** Flat about the future, and in Ch 37
   (line 4082) he does plug into this amp. Likely the payoff on purpose. "Again" is Claude's word (edit 145).
4. **Ch 10, line 864, '"Suit yourself, man," Ruby shrugged again,'.** A shrug used as a speech tag. Fix: '"Suit
   yourself, man." Ruby shrugged again,'. CT's words (edit 288).

## Chapters 11 to 39 and the back matter

5. **Ch 14, line 1291, "The engine ticked as it cooled."** He turned the truck off under the madrones in daylight,
   hours before; it would not still tick. The same phrase comes back for the plasma table (1545). CT's base text,
   kept beside his lines in edit 106.
6. **Ch 15, line 1324, "Every twenty he took out came off the far end of her room."** In plain past tense this says
   he took twenties out, and the book says he took none (1168, 1250, 1366). One fix: "Every twenty he took out would
   have come off the far end of her room." CT's base text; edit 55 hangs his million-dollar lines on it.
7. **Ch 16, line 1583, "he had a light step ... Lou's steps were light as a feather."** The same point twice in a row.
   Both are CT's dictation (edit 228), so it may be emphasis. One fix keeps his feather line: "he didn't pound the
   ground like so many men his size. Lou's steps were light as a feather."
8. **Ch 17, lines 1597, 1605, 1612: three raised eyebrows in sixteen lines** ("He raised an eyebrow.", "He raised his
   eyebrows and blinked a few times.", "Elijah turned and raised an eyebrow."). All three are CT's words (edits 231 and
   285). One fix: "Elijah turned." at 1612.
9. **Ch 19, lines 1904 and 1905: Marta ends two speeches in a row on "spreadsheet".** The second was "Elijah" until 26
   Nov, changed because Ch 37 says she never called him that. Fix: "we're starting to see come out." (drop the second).
   The sentence is CT's (edit 124); the word "spreadsheet" there is Claude's correction.
10. **Ch 23, line 2265 against 2305: the parcel count.** Elijah searches his own county and two neighbors, all in
    Washington, and finds "Fifty-some parcels"; Bidwell's map has fifty-three in all, over three California counties
    and two Washington ones. That leaves almost none for California, where the Hollis place and Ma's farm are. Soft, but
    the book makes a point of the numbers. Both are CT's base text.
11. **Ch 23, line 2285: "Phoenix" twice** ("Dale on speakerphone from Phoenix", then Dale's "I'm in Phoenix", after 2263
    already said it). Fix: "with Dale on speakerphone, and". Claude's rewording (edit 202) of CT's sentence.
12. **Ch 26, lines 2615 to 2623: four arms-in-water pictures in nine lines,** two of them nearly the same ("their arms
    in cold water up to the elbow"; "Nine people with their arms in cold water turned to her"). 2615 and 2623 are CT's;
    2621's "the cold water" is Claude's (edit 162) and is the easy one to drop.
13. **Ch 27, line 2908, "Topics crossed intellectual property lines".** A reader stops on the legal term in a list of
    talk topics. CT's own sentence (edit 292): only he knows what he meant.
14. **Ch 28, line 3069: "trailer" and "road" twice each in two sentences** ("out of the kitchen trailer ... out of the
    back of the trailer, under the one light on the road"). Claude's words (edit 207). Fix: "out of the back of it, under
    the one light for miles".
15. **Ch 37, lines 4097 to 4099: three Lou paragraphs in a row,** two opening with a quote and "Lou said". His "I'll keep
    the stove going" answers Elijah's line at 4092, two Lou paragraphs back. The 4099 tag is Claude's (edit 182, item 26).
16. **Ch 39, line 4374, "He couldn't take his name back off a page on a kitchen table."** Left over from an older draft
    where the notary came to the kitchen; the book now has him sign at the bank (line 1166). Fix: "take his name back
    off a page at the bank". CT's base text.

## The audit's list of 27 Nov (section B of `SCENE-SHEET-AUDIT-2026-11-27.md`), checked again on the page

Fixed since: 4 (who sent Ma the video: line 518 now frames it as her memory) and 6 (the lien sale days all hold:
Wednesday 26 Feb, eleven days to Sunday 9 March, the arms on Wednesday 12 March).

Still on the page, for CT:
- 1 (partly). Ruby, February 2024: "there's four thousand of them ... maybe it's eight thousand" (line 677), still
  October's first-week count after fifty million views.
- 2. Chat Horizon "for free" (105) and "twenty dollars a month" (154), with no paid tier between.
- 3. "SURVIVING THE FINAL TURNING ... the last two words ... belonged to Nate's paperback" (796); the paperback's word
  is only "turning" (170).
- 5 (partly). Oakland and Fremont now agree. But six arms are loaded (924) and "all six" are lit at the launch (1018),
  and later "The two spare arms were still sitting on the cannery dock in their crates, never unpacked" (1309).
- 7. "Half the table thinks you're right" (1360) against the April email's "Everyone here at the farm agrees" (1477)
  and Marta's "Did the table invite a person?" (1570).
- 8. "Wes had sent nothing" (2115) in the band chat, where Wes sent two messages (257, 262).
- 9. "He ate the crackers." (1366), then "A sleeve of crackers with two left" (1768).
- 10. Ma in a chair by the window Thursday (1221) before the place is first paid Friday (1167).
- 11. The board's April: it holds only if the order came in the first days of April (1898, 1912, 2198).
- 12. The squash "has to come in this week" (3754), still in the field at the October meeting and after (3787, 3811,
  3925).
- 13. Route boxes built "on the Wednesday of festival week" (3957) though the route runs Tuesdays (3787).
- 14. The Epilogue's visitor book: David's Sunday sits between Melody's Saturday and Elijah's Wednesday, so "Some weeks
  he signed right under her" (4441) needs David to skip.
- 15. Whether Grace knew who bought Ma's place: she knows of the sale from Ch 24 (2415); the page never says about the
  buyer.
- 16. "They've been there since my first week" (3811): the arms come in his second week (1658).
- 17. Where his pocket money comes from on the farm: none is named from March 2025 to November 2027.
