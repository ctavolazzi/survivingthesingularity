# The next build: structure and readiness

26 November 2026, eighth logging chat. CT: "finalize the structure of the narrative for the v7 build. Get everything
ready to compose into v7 for me please."

**What this file is:** the book in order, chapter by chapter, with the state of each part; what the build is made of;
and the gate it has to pass. The evaluation behind it is `STORY-REPORT-2026-11-26.md`. The order of work is `TODO.md`.

## 1. The name

CT calls the next build v7. There is already a Google Doc called "StS v7 draft (Nov 26)": a frozen side copy he asked
for that morning (v6 through edit 171; `V7-CHANGES.md`, `manuscript/tools/edits-v7/`). So that two things don't share a
name, the new Doc should take a title of its own (for example "StS v7 final (date)") and the old one should get "OLD:"
in front. Renaming his Doc needs his yes. Until then this file says "the next build."

## 2. What it is made of

- **Base:** the Google Doc "StS v5 draft (Nov 23)" with its suggestions accepted.
- **Plus** every row of `manuscript/tools/edits-v6/ops.py`: edits 87 to 215 (430 replacements). Chapters 27 to 36 are
  written (edits 206 to 215).
- **Checked by** every row of `manuscript/tools/edits-v5/checks.py` (215; all pass).
- **Composed by** `python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT` (without `--no-docx`), which writes
  `OUT/v6.docx` with headings, italics and the 19 pictures. That .docx becomes the new Google Doc.
- The v6 Doc "StS v6 draft (Nov 25)" has edits 1 to 138, 141 and 151. It is not the base of the build and is not
  changed by it.

## 3. The book, in order

Front: title page ("SURVIVING THE SINGULARITY", "A Solarpunk Novel", Christopher Tavolazzi); contents; Dedication ("For
the people I love who looked me in the eye like I'd finally lost it."); "Recognize Your Power". The copyright page is
added by the print build, and the cover credit goes on it (CT's words, in `TODO.md`).

Words are measured from today's text. "(r)" means the one-line summary comes from a reader's report and the title, not
from Claude's own reading.

| # | Title | When | Words | What it does | State |
|---|---|---|---|---|---|
| | **Act One: The Bar** | | | | |
| 0 | Three Glasses Up | late 2022 | 3,606 | The bar, the realtors, three people fired, the toast. He starts to write | as in the Doc, line edits |
| 1 | A Bet for Lamb (r) | late 2022 | 1,246 | Devendra, the coffee machine, the bet: Thanksgiving 2027, loser cooks | as in the Doc, line edits |
| 2 | The Coin Slot | 2023 | 1,363 | Claypot announces Companion; his pipeline is in it; Wes: "is my stuff in that thing"; the stages | as in the Doc, line edits |
| M1 | Meanwhile | | 280 | Bidwell and his reader ("Find out what their dirt costs") | stays |
| 3 | A Satellite Over the Star Thistle (r) | 2023 | 1,307 | Ma's Sunday call; "It's just tools, baby"; the lecture video | as in the Doc |
| 4 | Cell G14(r) | 2023 | 761 | The numbers. No dialogue (report: fold into 3?) | as in the Doc |
| 5 | The Tenant Who Paid No Rent (r) | 2023 | 1,474 | The tower, the power bill, Ray's horses, the amp | as in the Doc, line edits |
| | **Act Two: The City** | | | | |
| 6 | Four Minutes and Eleven Seconds | fall 2023 | 1,420 | Laid off. The video, four minutes and eleven seconds | as in the Doc, line edits |
| 7 | You're Early | winter 2023 | 2,544 | It spreads. Mr. Ostrander. David: "You're early." Ruby's message | edit 196 logged |
| 8 | Elijah Madrona (r) | early 2024 | 2,151 | San Francisco, the panel, the wrong name on his lanyard | as in the Doc |
| 9 | The Wrong Verb (r) | early 2024 | 2,041 | The Architect through a kitchen door: "That is the wrong verb." | as in the Doc |
| 10 | Frozen Peas (r) | early 2024 | 1,484 | Ruby on the fire escape; the million he turns down | as in the Doc |
| M2 | Meanwhile | | 375 | Bidwell leaves the dinner: "put somebody near him" | stays |
| 11 | It's Always a Strap (r) | spring and summer 2024 | 2,366 | Home to Ma's. Gus and the Elks lodge; the offer to stand in the ads | as in the Doc |
| 12 | The Seventeen-Dollar Shower (r) | August 2024 | 988 | The cannery in August, the arms on the floor, the seventeen-dollar shower | as in the Doc |
| 13 | The Buckets in the Barn (r) | September 2024 | 4,559 | The night call, the stroke, the buckets in the barn, the sale, his friends cut him | as in the Doc; report items need CT |
| 14 | A Stain Shaped Like Ohio (r) | fall 2024 | 1,752 | Rain. He yells at God | as in the Doc |
| 15 | The Twenty, Folded Small | fall 2024 to March 2025 | 5,637 | The truck, the arms nobody bids on, the old man's twenty, Grace's email. North | edit 188 logged |
| | **Act Three: The Farm** | | | | |
| 16 | The Red Bin (r) | March 2025 | 1,341 | Arrival. Marta, the broom, the red bin | as in the Doc |
| 17 | Twice Certified | March and April 2025 | 5,040 | Fed and watched; the arms go to Praether's; Lou; the first Friday table; Denny's ladder; Rosa | CHANGED, edit 205 (Praether) |
| 18 | Gary and Sal (r) | late April 2025 | 1,486 | Companion 2.0, a night of reading, the soup jars, Gary and Sal, Marta's warning | edit 189 logged |
| 19 | Eleven, One, Zero (r) | April and May 2025 | 3,182 | Forty boxes. The board he lets an AI lay out and hides. "You picked nothing." | in the Doc; three words logged |
| 20 | The Bottom of the Column | May 2025 | 1,982 | HANDS. The boxes wait on summer. "Mostly she asks for somebody named Barry." | REWRITTEN, edit 199 |
| 21 | Forty-One Views | June 2025 | 1,867 | Denny's one take; his fans and Priya's weird letters; the heat cooks the Ochoas' starts | REWRITTEN, edit 200 |
| 22 | Two Slashes | July 2025 | 2,687 | The leak, the bell, both confessions, Lou's IBM line, the pot, the hour of Ray's funeral | REWRITTEN, edit 201; report: play the confession |
| 23 | Owner or Occupant | summer 2025 | 1,421 | Irene's land or the Ochoas' October; the trust; "don't date where you eat" | REWRITTEN, edit 202 |
| M3 | Meanwhile | | 525 | Bidwell's map; the hole; Lou is his cousin | one line waits on CT |
| 24 | A Chair a Foot Closer | August and September 2025 | 2,174 | The shouse, the broken coupon, the first fire, the gate and the captain, the pond | REWRITTEN, edit 203; one addition waits on CT |
| 25 | Long Enough to Laminate | fall 2025 | 2,820 | The letter and the tiff, frozen yogurt, Frank's store, the kiss at the pond, the Thanksgiving U-turn | REWRITTEN, edit 198 |
| 26 | The Indignant Worm | spring to October 2026 | 4,525 | The soil trial, the little rover (a JetAuto Pro), the models go dark, Ma's fall, the pay vote, the amp at the pond | REWRITTEN, edit 204; report: split at October? |
| 27 | Blueprints of a Wall | October 2026 to February 2027 | 2,294 | The fire video, eleven towns, the plans given away, the pledge, the well | REWRITTEN, edit 206 |
| 28 | Hello, Ridge | winter 2026 | 1,194 | One night dark; the co-op's lights stay on; the Ochoas drop off the map; the rain fly | REWRITTEN, edit 207 |
| 29 | Ink and Pencil | early 2027 | 2,141 | The annual meeting: ways to die, Marta's shoulder, Denny unpaid, Reuben's deed | REWRITTEN, edit 208 |
| 30 | Item Seven | early 2027 | 2,307 | The county meeting; Rosa and Irene; Denny's last video; the rod oven | REWRITTEN, edit 209 |
| 31 | Six Eggs on the Floor | February 2027 | 3,146 | The plan that prices Denny's bench; Denny leaves; the tea circle; "You're the lamp"; "Ma. I'm not okay." | REWRITTEN, edit 210 |
| | **Act Four: The Ridge** | | | | |
| M4 | Meanwhile | March 2027 | 471 | The machine on the dairy: "may I ask the people who live there?" (opens Act Four) | stays |
| 32 | The Rubber Band | March to June 2027 | 2,989 | Five signs kept to himself; the stove; the late payment and the April quarrel; the missed stop; the juniper | REWRITTEN, edit 211 |
| 33 | A Poem About Tide Pools | June and July 2027 | 4,363 | "It asked." Denny comes back. Believed, and told no. "I love you." The tomato dinner | REWRITTEN, edit 212 |
| 34 | A Guy With Arms | October 2027 | 2,669 | The locked tractor; the tall rover voted in; the war on the phones; Curtis the Trekkie; the arms revealed and refused; Lou on why the Ochoas are leaving | REWRITTEN, edit 213 |
| 35 | Two Walnuts in One Fist | October 2027 | 1,392 | Lou in the field: "You can't change anyone's mind." The walnuts | REWRITTEN, edit 214 |
| 36 | This Is the Gate | late October 2027 | 2,208 | The Ochoas leave. Festival week. The fire. "Maybe you should go home." | REWRITTEN, edit 215 (the fire kept whole) |
| 37 | New Tape on an Old Gate | November 2027 | 2,677 | He leaves the amp and the note. The goodbyes. The tape. Home; the visitor book; the lamp | STAYS; lines in plan section 13 need CT |
| 38 | A Truck Over a Cattle Guard | 25 November 2027 | 2,766 | Thanksgiving at the co-op. The machine asks for a vote. Four tables. The note | STAYS; one word needs CT |
| 39 | It's Six Now | November 2027 | 2,826 | He reads Ma the book. The Bear Flag. "You're good." The three names. The book on the bar | STAYS |
| Ep | Epilogue | to April 2028 | 291 | The pit, the visitor book, the forty-dollar guitar, the song sent to Grace | STAYS |

Back: About This Book; Afterword; Appendix (a note on the map, the four sides, the people, the places, the timeline);
Thank You; "Recognize Your Power".

## 4. The shape, decided

- **Four acts, forty chapters, four "Meanwhile" scenes, an Epilogue.** No chapter is added, removed or moved by
  anything decided so far.
- **Chapters 0 to 19:** as CT approved them, plus edit 205 (Praether) and the logged line edits.
- **Chapters 20 to 26:** rewritten and logged.
- **Chapters 27 to 36:** to the plan, `PLAN-CHAPTERS-20-TO-36.md`, sections 10 and 11.
- **Chapter 37 to the Epilogue:** stay, except the lines CT says yes to (plan, section 13).
- **The spine** is the chain of cause in the plan, section 10.1: the cooked starts, the leak, the land or the Ochoas,
  Denny's bench, the late payment, the missed stop, the promise, the arms, Lou's sentence, the fire.
- **Three threads CT added on 26 November run through it:** the arms at Praether's (Ch 17, then the reveal in Ch 34);
  the war (Praether's warning in Ch 17, Curtis in Ch 26 and 33, the Ukraine footage in Ch 34); scenes with only women
  (Ch 23, 26, 29, 32).

## 5. Structural changes the report proposes (none decided; each needs CT's yes)

| Proposal | Effect on the structure |
|---|---|
| Split Chapter 26 at the October night, so the amp at the pond has a chapter of its own | Forty-one chapters; one new title, his to give |
| Fold Chapter 4 into Chapter 3 | Thirty-nine chapters (or forty with the split) |
| The sale of the farm as a scene in Chapter 13 | Same structure; about 140 words more |
| Play the board confession (Ch 22); Elijah at the Ochoas' door (Ch 23 or 24); the year's obstacle (Ch 26) | Same structure; corrections to edits 201 to 204 |

## 6. The gate

`python3 manuscript/tools/edits-v6/build_gate.py OUT/v6.txt --todo manuscript/novel/TODO.md` lists every line that
must be gone and every line that must be there before the build is made (`build-gate.json` beside it), and every
unticked box in the to-do list. On 26 Nov, after Chapters 27 to 36, it reports one line still to go, in the ending and
waiting on CT's yes (Ch 37's "equipment shed"; Ch 38's "gantry" is done, edit 216), plus the to-do list's open boxes. The build is ready when:

1. ~~Chapters 27 to 36 are written and logged (edits 206 to 215).~~ Done 26 Nov.
2. The corrections to Chapters 22 to 26 from the report are in, or CT has said no to them.
3. CT has answered the ending lines (plan, section 13) and the done-chapter items (report, section 6).
4. make_v6.py passes every row, and build_gate.py says READY.
5. A last readers' pass finds no continuity error.

## 7. Composing it, on CT's go

1. A fresh read of the v5 Doc (picture links expire).
2. `make_v6.py V5_READ.json OUT` for the .docx; open it and check the headings and the first and last pages.
3. Upload it as a new Google Doc, titled as CT decides.
4. Update `src/lib/data/novel/instances.json`, run `node scripts/sts-bridge.mjs export md > manuscript/novel/BRIDGE.md`,
   and remake the Drive bridge page.
5. The large print PDF and the release build when he asks (`EDIT-LOGGING-PROCEDURE.md`), with the cover credit on the
   copyright page and the ISBN.
