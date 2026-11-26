# The book's structure (built as v8)

26 November 2026, eighth logging chat. CT: "finalize the structure of the narrative for the v7 build. Get everything
ready to compose into v7 for me please." CT named the build v8, and it was made on his word the same night: the Google
Doc "StS v8 draft (Nov 26)", every edit 1 to 223. Brought up to date in the tenth logging chat (words measured after
edit 223).

**What this file is:** the book in order, chapter by chapter, with the state of each part; what the build is made of;
and the gate it has to pass. The evaluation behind it is `STORY-REPORT-2026-11-26.md`. The order of work is `TODO.md`.

## 1. The name

The build is v8 (CT, 26 Nov: "I believe should be version 8"), because "StS v7 draft (Nov 26)" was already a frozen side
copy (v6 through edit 171; `V7-CHANGES.md`, `manuscript/tools/edits-v7/`). Whether the v6 and v7 Docs get "OLD:" in
front is CT's call (his Docs).

## 2. What it is made of

- **Base:** the Google Doc "StS v5 draft (Nov 23)" with its suggestions accepted.
- **Plus** every row of `manuscript/tools/edits-v6/ops.py`: edits 87 to 223 (517 replacements).
- **Checked by** every row of `manuscript/tools/edits-v5/checks.py` (223; all pass).
- **Composed by** `python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT --no-pictures`, which writes
  `OUT/v6.docx` with headings and italics. That .docx became the v8 Doc. The book has no pictures (the bridge rule:
  "the author cut them"); the v8 Doc has an empty paragraph, mid-scene, where each of the 19 was.
- The v6 Doc "StS v6 draft (Nov 25)" has edits 1 to 138, 141 and 151. It is not the base of the build and is not
  changed by it.

## 3. The book, in order

Front: title page ("SURVIVING THE SINGULARITY", "A Solarpunk Novel", Christopher Tavolazzi); contents; Dedication ("For
the people I love who looked me in the eye like I'd finally lost it."); "Recognize Your Power". The copyright page is
added by the print build, and the cover credit goes on it (CT's words, in `TODO.md`).

Words are measured after edit 223 (`story_report.py`), the text of the v8 Doc. Every row is in the v8 Doc. "(r)" means the one-line summary comes from a reader's report and the title, not
from Claude's own reading.

| # | Title | When | Words | What it does | State |
|---|---|---|---|---|---|
| | **Act One: The Bar** | | | | |
| 0 | Three Glasses Up | late 2022 | 3,606 | The bar, the realtors, three people fired, the toast. He starts to write | as in the Doc, line edits |
| 1 | A Bet for Lamb (r) | late 2022 | 1,244 | Devendra, the coffee machine, the bet: Thanksgiving 2027, loser cooks | as in the Doc, line edits |
| 2 | The Coin Slot | 2023 | 1,363 | Claypot announces Companion; his pipeline is in it; Wes: "is my stuff in that thing"; the stages | as in the Doc, line edits |
| M1 | Meanwhile | | 280 | Bidwell and his reader ("Find out what their dirt costs") | stays |
| 3 | A Satellite Over the Star Thistle (r) | 2023 | 1,310 | Ma's Sunday call; "It's just tools, baby"; the lecture video | as in the Doc |
| 4 | Cell G14(r) | 2023 | 761 | The numbers. No dialogue (report: fold into 3?) | as in the Doc |
| 5 | The Tenant Who Paid No Rent (r) | 2023 | 1,491 | The tower, the power bill, Ray's horses, the amp | as in the Doc, line edits |
| | **Act Two: The City** | | | | |
| 6 | Four Minutes and Eleven Seconds | fall 2023 | 1,420 | Laid off. The video, four minutes and eleven seconds | as in the Doc, line edits |
| 7 | You're Early | winter 2023 | 2,544 | It spreads. Mr. Ostrander. David: "You're early." Ruby's message | edit 196 logged |
| 8 | Elijah Madrona (r) | early 2024 | 2,151 | San Francisco, the panel, the wrong name on his lanyard | as in the Doc |
| 9 | The Wrong Verb (r) | early 2024 | 2,046 | The Architect through a kitchen door: "That is the wrong verb." | as in the Doc |
| 10 | Frozen Peas (r) | early 2024 | 1,493 | Ruby on the fire escape; the million he turns down | as in the Doc |
| M2 | Meanwhile | | 375 | Bidwell leaves the dinner: "put somebody near him" | stays |
| 11 | It's Always a Strap (r) | spring and summer 2024 | 2,383 | Home to Ma's. Gus and the Elks lodge; the offer to stand in the ads | as in the Doc |
| 12 | The Seventeen-Dollar Shower (r) | August 2024 | 988 | The cannery in August, the arms on the floor, the seventeen-dollar shower | as in the Doc |
| 13 | The Buckets in the Barn (r) | September 2024 | 4,567 | The night call, the stroke, the buckets in the barn, the sale, his friends cut him | as in the Doc; report items done (edit 219) |
| 14 | A Stain Shaped Like Ohio (r) | fall 2024 | 1,752 | Rain. He yells at God | as in the Doc |
| 15 | The Twenty, Folded Small | fall 2024 to March 2025 | 5,626 | The truck, the arms nobody bids on, the old man's twenty, Grace's email. North | edit 188 logged |
| | **Act Three: The Farm** | | | | |
| 16 | The Red Bin (r) | March 2025 | 1,341 | Arrival. Marta, the broom, the red bin | as in the Doc |
| 17 | Twice Certified | March and April 2025 | 5,125 | Fed and watched; the arms go to Praether's; Lou; the first Friday table; Denny's ladder; Rosa | CHANGED, edit 205 (Praether) |
| 18 | Gary and Sal (r) | late April 2025 | 1,698 | Companion 2.0, a night of reading, the soup jars, Gary and Sal, Marta's warning | edit 189 logged |
| 19 | Eleven, One, Zero (r) | April and May 2025 | 3,160 | Forty boxes. The board he lets an AI lay out and hides. "You picked nothing." | in the Doc; three words logged |
| 20 | The Bottom of the Column | May 2025 | 1,983 | HANDS. The boxes wait on summer. "Mostly she asks for somebody named Barry." | REWRITTEN, edit 199 |
| 21 | Forty-One Views | June 2025 | 1,867 | Denny's one take; his fans and Priya's weird letters; the heat cooks the Ochoas' starts | REWRITTEN, edit 200 |
| 22 | Two Slashes | July 2025 | 2,677 | The leak, the bell, both confessions, Lou's IBM line, the pot, the hour of Ray's funeral | REWRITTEN, edit 201; report: play the confession |
| 23 | Owner or Occupant | summer 2025 | 1,422 | Irene's land or the Ochoas' October; the trust; "don't date where you eat" | REWRITTEN, edit 202 |
| M3 | Meanwhile | | 525 | Bidwell's map; the hole; Lou is his cousin | stays; Bidwell's "somebody" is never named (CT) |
| 24 | A Chair a Foot Closer | August and September 2025 | 2,174 | The shouse, the broken coupon, the first fire, the gate and the captain, the pond | REWRITTEN, edit 203; Grace's father and her festival years went into "Pondwater" |
| 25 | Long Enough to Laminate | fall 2025 | 2,845 | The letter and the tiff, frozen yogurt, Frank's store, the kiss at the pond, the Thanksgiving U-turn | REWRITTEN, edit 198 |
| 26 | The Indignant Worm | spring 2026 to fall | 3,777 | The soil trial, the little rover (a JetAuto Pro), the models go dark, Ma's fall, the pay vote, Praether at his mailbox | REWRITTEN, edit 204 |
| (none) | Pondwater | October 2026 | 1,175 | Marta tells him about the music; the amp on the tailgate at the pond; the band joke; Grace's father; the kiss | REWRITTEN, edit 204; CT's title, unnumbered |
| 27 | Blueprints of a Wall | October 2026 to February 2027 | 2,295 | The fire video, eleven towns, the plans given away, the pledge, the well | REWRITTEN, edit 206 |
| 28 | Hello, Ridge | winter 2026 | 1,193 | One night dark; the co-op's lights stay on; the Ochoas drop off the map; the rain fly | REWRITTEN, edit 207 |
| 29 | Ink and Pencil | early 2027 | 2,142 | The annual meeting: ways to die, Marta's shoulder, Denny unpaid, Reuben's deed | REWRITTEN, edit 208 |
| 30 | Item Seven | early 2027 | 2,308 | The county meeting; Rosa and Irene; Denny's last video; the rod oven | REWRITTEN, edit 209 |
| 31 | Six Eggs on the Floor | February 2027 | 3,149 | The plan that prices Denny's bench; Denny leaves; the tea circle; "You're the lamp"; "Ma. I'm not okay." | REWRITTEN, edit 210 |
| | **Act Four: The Ridge** | | | | |
| M4 | Meanwhile | March 2027 | 471 | The machine on the dairy: "may I ask the people who live there?" (opens Act Four) | stays |
| 32 | The Rubber Band | March to June 2027 | 2,978 | Five signs kept to himself; the stove; the late payment and the April quarrel; the missed stop; the juniper | REWRITTEN, edit 211 |
| 33 | A Poem About Tide Pools | June and July 2027 | 4,369 | "It asked." Denny comes back. Believed, and told no. "I love you." The tomato dinner | REWRITTEN, edit 212 |
| 34 | A Guy With Arms | October 2027 | 3,676 | The locked tractor; the tall rover voted in; the war on the phones; Curtis the Trekkie; the arms revealed and refused; Lou on why the Ochoas are leaving | REWRITTEN, edits 213 and 221 (the women and the tall rover) |
| 35 | Two Walnuts in One Fist | October 2027 | 1,392 | Lou in the field: "You can't change anyone's mind." The walnuts | REWRITTEN, edit 214 |
| 36 | This Is the Gate | late October 2027 | 2,299 | The Ochoas leave. Festival week. The fire. "Maybe you should go home." | REWRITTEN, edit 215 (the fire kept whole) |
| 37 | New Tape on an Old Gate | November 2027 | 2,669 | He leaves the amp and the note. The goodbyes. The tape. Home; the visitor book; the lamp | STAYS, with edits 217 and 223 |
| 38 | A Truck Over a Cattle Guard | 25 November 2027 | 2,761 | Thanksgiving at the co-op. The machine asks for a vote. Four tables. The note | STAYS, with edits 216 ("the new rover") and 223 |
| 39 | It's Six Now | November 2027 | 2,843 | He reads Ma the book. The Bear Flag. "You're good." The three names. The book on the bar | STAYS, with edits 218 and 223; "heard it as a murder" waits on CT |
| Ep | Epilogue | to April 2028 | 291 | The pit, the visitor book, the forty-dollar guitar, the song sent to Grace | STAYS |

Back: About This Book; Afterword; Appendix (a note on the map, the four sides, the people, the places, the timeline);
Thank You; "Recognize Your Power".

## 4. The shape, decided

- **Four acts, forty chapters, "Pondwater" (unnumbered, CT's title, split from Chapter 26), four "Meanwhile" scenes, an
  Epilogue.**
- **Chapters 0 to 19:** as CT approved them, plus edit 205 (Praether) and the logged line edits.
- **Chapters 20 to 26:** rewritten and logged.
- **Chapters 27 to 36:** to the plan, `PLAN-CHAPTERS-20-TO-36.md`, sections 10 and 11.
- **Chapter 37 to the Epilogue:** stay, except the lines CT says yes to (plan, section 13).
- **The spine** is the chain of cause in the plan, section 10.1: the cooked starts, the leak, the land or the Ochoas,
  Denny's bench, the late payment, the missed stop, the promise, the arms, Lou's sentence, the fire.
- **Three threads CT added on 26 November run through it:** the arms at Praether's (Ch 17, then the reveal in Ch 34);
  the war (Praether's warning in Ch 17, Curtis in Ch 26 and 33, the Ukraine footage in Ch 34); scenes with only women
  (Ch 23, 26, 29, 32).

## 5. Structural changes the report proposed (all decided by CT, 26 Nov)

| Proposal | Decided |
|---|---|
| Split Chapter 26 at the October night, so the amp at the pond has a chapter of its own | Done: "Pondwater", CT's title, unnumbered |
| Fold Chapter 4 into Chapter 3 | Withdrawn (CT: "I don't care how long it gets I want it to be good") |
| The sale of the farm as a scene in Chapter 13 | Withdrawn: on reading, it already is one |
| Play the board confession (Ch 22); Elijah at the Ochoas' door (Ch 23 or 24); the year's obstacle (Ch 26) | Done (corrections to edits 201 to 204) |

## 6. The gate

`python3 manuscript/tools/edits-v6/build_gate.py OUT/v6.txt --todo manuscript/novel/TODO.md` lists every line that
must be gone and every line that must be there (`build-gate.json` beside it), and every unticked box in the to-do list.
Run in the tenth logging chat, after edit 223: every line passes; it says NOT READY only for the open boxes in
`TODO.md` (the smell pass, the ISBN, the release build, Praether once more before Chapter 34, the Instagram synopsis).
v8 was made before the gate said READY, on CT's word.

## 7. Composing a copy (how v8 was made; the same for any next one, on CT's go)

1. A fresh read of the v5 Doc.
2. `make_v6.py V5_READ.json OUT --no-pictures` for the .docx; open it and check the headings and the first and last
   pages.
3. Upload it as a new Google Doc, titled as CT decides, and a locked backup beside it.
4. Update `src/lib/data/novel/instances.json`, run `node scripts/sts-bridge.mjs export md > manuscript/novel/BRIDGE.md`,
   and remake the Drive bridge page.
5. The large print PDF and the release build when he asks (`EDIT-LOGGING-PROCEDURE.md`), with the cover credit on the
   copyright page and the ISBN.
