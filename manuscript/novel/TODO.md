# To do: the novel, from here to done

Updated 27 Nov 2026, end of the eleventh logging chat. Top item first. Tick a box in the same commit that does the work.
What "done" means is in `GOALS.md`; how each step is done is in `REFERENCE.md`.

**Next edit: 235.** Edit 234 was logged on 27 Nov, after the smell pass prompt was written (CT's dictation in the Riemann
chat: Grace doesn't know about the arms until the table finds out; Ch 17, 18, 34, 35, 36;
`drafts/edit-234-grace-doesnt-know.md`). So a spin-up now shows **234 check rows passing (608 replacements), 223
accepted in v8 and 224 to 234 not in the Doc**; that is right. Next chat: the smell pass (section 3; prompt in `CHECKPOINT-2026-11-27-eleventh.md`). That prompt was run once on
27 Nov inside the Riemann chat: spin-up clean, nothing shown or logged, so the smell pass is still to do. That chat's
closing notes (what is done, what is open, CT's words, the stakes answer) are the first section of
`CHECKPOINT-2026-11-26-riemann-praether.md`. The scene
sheet, one row per scene: Google Sheet id `1vReMI4VKBIexpMvR8Sx0QpyO8Bde2w2jLOnKFCv0KYY`, copy in `scene-sheet-2026-11-27.csv`. Two chats logged on this branch on 26 and 27 Nov. One: edit 229, Curtis and the Riemann
hypothesis at Friday dinner, RSI, and Grace's promise (Ch 27); edit 230, Praether's terms and Lou at the barn (Ch 17,
18); its fix list and prompt are in `CHECKPOINT-2026-11-26-riemann-praether.md`. The other (eleventh): edit 228, Lou's
heavier entrance (end of Ch 16); edits 231 and 232, CT's held dictation placed (Grace's talk about the bed in Ch 17,
Rosa's grace and the ladle at Thanksgiving 2026 in Ch 27, `drafts/edit-231-232-grace-and-rosa.md`); edit 233, the finishing pass, 30 line
fixes from seventeen readers (`drafts/finishing-2026-11-27.md`), which also does items 1 to 3 of that fix list. CT:
"After this, if possible, I don't really want to change or add anything. It's now about more just refining, revising,
deleting, buffing out the hard spots, polishing." The book in the Docs is "StS v8 draft (Nov 26)" (edits 1 to 223; no pictures), with a locked
backup. Edits 224 to 233 are logged in GitHub only. Tenth chat (26 Nov): the laser weeder and the brain organoid
("Pondwater"); the panel, "overwhelmed", fifty million views and Ruby's pitch (Ch 8 to 10); why Elijah waits after the
pond (Ch 26; "under 6 months" held for CT); the polish pass at key moments. The "Open with CT" list is in `CHECKPOINT-2026-11-26-tenth.md`; it is put to him
only when he asks.

## 1. Waiting on CT (ask only when the step needs it; one question at a time)

- [x] **Where the arms are kept.** CT, 26 Nov: at Richard Praether's (plan, 10.5). To write: the Praether scene in
      Chapter 17 (changes his edit 88), Grace telling Marta (Ch 26), the reveal in Chapter 34, one line in Chapter 37
      on his yes.
- [x] **What Praether says.** CT: "More of course lol, but that's his message, and it foreshadows the stuff about
      Ukraine and the people leaving the farm." The Chapter 17 scene is written (edit 205); the rest of Praether's
      lines are Claude's and his to correct. The smell of that barn is marked for him.
- [x] **Scenes with just the women** (plan, 10.6). CT, 26 Nov: "Priya and Grace need to talk. Marta and some of the
      other women from the co-op the extended families." To write with their chapters: Priya and Grace the night
      before the county meeting (Ch 29 into 30); Marta, Yvonne and the women in the grange hall kitchen (Ch 29); Grace
      and Lupe (Ch 23); Grace and Mrs. Delgado (Ch 32).
- [x] **Praether's wound** (plan, 10.7). CT, 26 Nov: "yes gulf war vet." Said at his mailbox in Chapter 26 (edit 204);
      Chapter 17 stays cryptic so the VA letter is still the reveal.
- [x] **The rover and the arms.** CT, 26 Nov: "Yes". The rover stays as written; the arms are the machine the table
      says no to in Chapter 34. His addition: "I had originally envisioned Elijah storing the arms on the farm to sort
      of prove his value and save money. A moment he would have longed for since the electrical bill." With his line,
      "No bills, except my phone, which at this point more or less pays for itself with the Creator Fund." It goes in
      Chapter 17, where the crates go into the equipment shed; waiting on one word from him ("Creator Fund" or "creator
      fund").
- [x] **Grace's father.** CT, 26 Nov: checked out on the porch, "numb, barely himself anymore ... a husk, a shell, a
      container for her father's soul, one she grieved and let go of long ago. That's all she really needs to say about
      it." She says it on the blanket in "Pondwater" (edit 204).
- [x] **The women and the tall rover** (CT, 26 Nov): written as edit 221 (Irene's kitchen; the treasurer stays Reuben). A scene in Chapter 34, before the meeting, where the women weigh
      the taller machine and the yield against pushback from the community and decide for it, with an older woman's
      advice on people who tell you what they think without being asked ("Not ABOUT men, but PEOPLE"). Asked and not yet
      answered: does he have her line, and is the treasurer Reuben or a woman.
- [x] **The ending lines** (plan, section 13): done in edit 223, except the gas cap (his scene) and "heard it as a
      murder". Was: "It should have felt like traveling light" (Ch 37); the gas
      cap (Ch 25, his scene); the Appendix; the Ch 37 to 39 line flags. Done: the rover in Ch 38 (216), the arms at
      Praether's in Ch 37 (217), Devendra's text in Ch 39 (218). Bidwell's "somebody" is never named (CT).
- [ ] **The Instagram synopsis**: fix the four things the book doesn't do, or leave it. Claude's answer is in the chat
      of 26 Nov; the check reruns with `find_in_book.py ... claims claims-instagram-synopsis.json`.
- [ ] **From the tenth chat** (all in `CHECKPOINT-2026-11-26-tenth.md`, "Open with CT"): edit 226's held line; Grace's
      winter away; five lines from the polish pass; edits 224 to 227 into the Doc; and the carried-over list (the gas
      cap, "heard it as a murder", the "Creator Fund" line, the 19 empty paragraphs, the thin places, the Docs' names,
      Drive's duplicates, the site's reader, the merge, the ISBN and the release build).

## 2. Chapters (one at a time; each is one edit with several ops rows)

Words are measured by `story_report.py` (27 Nov correction: the first table here counted line numbers and a
"Meanwhile"; the ten chapters hold 22,590 words, not 24,084). Targets total 22,050.

| Box | Chapter | Edit | Words now | Target | What it has to do (plan, section 11) |
|---|---|---|---|---|---|
| [x] | 27 Blueprints of a Wall | 206 | 2,046 | 2,010 | farmers market line; Grace on the $49 knockoff; the pledge with the Ochoas' greenhouse behind it; Thanksgiving 2026 letter to Ma; "Every winter there's somebody" fixed; Grace's room in Ardell placed |
| [x] | 28 Hello, Ridge | 207 | 1,125 | 1,105 | overnight, not three days; power when it counts; the Ochoas' house drops off the map; Lupe on the radio |
| [x] | 29 Ink and Pencil | 208 | 1,821 | 1,885 | Denny argues ("I'm not burned out. I'm unpaid."); Lupe: "Somebody quits"; Tyler says yes; Priya logs the 3 a.m. address; the welder gap |
| [x] | 30 Item Seven | 209 | 2,074 | 2,030 | Denny films his last one; Lou's "my man" |
| [x] | 31 Six Eggs on the Floor | 210 | 2,996 | 2,910 | Denny's goodbye on his porch; "Nothing that mattered" on the page |
| [x] | 32 The Rubber Band | 211 | 2,100 | 2,670 | the late payment, the missed stop, the April quarrel, frozen yogurt, the coffee can on the table (plan, 10.3); Denny out of the juniper; Frank's chart |
| [x] | 33 A Poem About Tide Pools | 212 | 4,255 | 3,550 | Denny comes back; "I sold it to them"; the tomato dinner cut by a third |
| [x] | 34 A Guy With Arms | 213 | 2,320 | 2,410 | Curtis's wound; the Ukraine footage; Curtis the Trekkie and Marta's "Commander Data" (CT's words); Hector and Lupe by name; they leave |
| [x] | 35 Two Walnuts in One Fist | 214 | 1,686 | 1,305 | night scene cut to the walnut, "The man who refuses to launch it" and ALC; "They can. They just won't." fixed |
| [x] | 36 This Is the Gate | 215 | 2,167 | 2,175 | festival week as one scene; Lou's knee; Elijah picks the squash row; the fire kept whole |
| [x] | "Pondwater" (was the end of 26) | 204 | 1,175 | | her father and her festival years, said on the blanket; his pause about festival girls after Marta's line (CT's words, 26 Nov) |

## 2a. From the story report (`STORY-REPORT-2026-11-26.md`, section 9)

No decision needed (corrections to chapters already rewritten):
- [x] Ch 22: play the board confession (his words, Marta's answer, Tyler cleared in front of Patricia).
- [x] Ch 23 or 24: Elijah carries the new board to the Ochoas; Hector and Lupe each get a line.
- [x] Ch 26: the year's obstacle, said once. Ma's fall stays open overnight.
- [ ] Praether twice more before Chapter 34 (he mows there). One done (Ch 26, at his mailbox); one to go (Ch 29 or 32).
Need CT's yes:
- [x] Ch 25: one line of logic at the truck stop (his scene). CT: "yes."
- [x] Split Chapter 26 at the October night: "Pondwater" (CT's title), unnumbered.
- [x] ~~Ch 13: the sale of the farm as a scene.~~ Withdrawn: on reading, it already is one (CT's words).
- [x] The continuity items in the report, section 6 (edit 219, and "parade" in 204). "For three years he had told her
      there wasn't one" (Ch 37) holds: the stroke is fall 2024 (Ch 13, "There isn't any Barry."), and Chapter 37 is 25
      November 2027 (checked in the tenth chat).
- [x] ~~Fold Chapter 4 into 3; cut the essay half of Chapter 20's debate.~~ Withdrawn (CT: "I don't care how long it gets I want
      it to be good"; both read and both earn their place).
- [x] ~~Chapter 33's tomato dinner: cut the cotton gin numbers, the saber-tooth and the rent, and "Pull apart what it takes
      to stay alive" (they say the Afterword's argument a second time; about 400 words). They may be CT's own words, so
      not cut without his yes.
- [x] The name of the next build: v8 (CT, 26 Nov). Still open: "OLD:" on the frozen v6 and v7 Docs (his Docs, his yes).

## 3. After Chapter 36

- [x] The ending lines, logged (edit 223; CT: "resolve as many of these as you can without my help").
- [x] The Appendix brought up to date (edit 223).
- [ ] The smell pass, **in a new chat just for smell** (CT, 26 Nov: "I'll do this with you later in a new chat dedicated
      just to smell"; `WRITING-INSTRUCTIONS.md`, section 7a). From Chapter 27 on it is part of writing each
      chapter. For the rest of the book: his two places first, in his words (the truck he lives in, Chapters 14 and 15;
      the high-dollar party, Chapters 9 and 10), then any scene where a smell would carry the feeling. Each one shown to
      CT, since Chapters 0 to 19 are done.
      Not started (27 Nov): the prompt was run once in the Riemann chat and stopped at "ready". Scene sheet rows for
      his two places: 29 to 32 (the party) and 47 to 49 (the truck).
- [x] The sentence-opening checker CT asked for (25 Nov), run on Chapters 20 to 36 only. Built in the tenth chat:
      `manuscript/tools/edits-v6/openers.py OUT/v6.txt --ch 20-36`. After edit 223 it finds 35 runs of three or more
      sentences opening with the same word, 38 runs of five pronoun-or-name openers, 21 paragraphs (Ch 0 to 19: 72, 59,
      47). About a dozen of the 35 are real pronoun stacks; the rest are lists and repeats on purpose ("The horse. The
      rifle. The radio."). Fixing them is on CT's go (the procedure, "Asked for the future").
- [x] A last readers' pass over the whole book for continuity, every quote grep-checked; fix what it finds. Done 26 Nov
      (edit 222): 50 fixed; 10 held for CT in `drafts/pass-2026-11-26.md`, "Held for CT".
- [x] ~~Words: Chapters 27 to 36 at or under 22,590 in total.~~ Dropped: length is not the measure (CT, 26 Nov).
- [ ] `build_gate.py OUT/v6.txt --todo manuscript/novel/TODO.md` says READY.
- [x] v8 made on CT's word (26 Nov): a new Doc from make_v6.py's .docx, no pictures, plus a locked backup; bridge map
      updated. Was: Ask CT how the final copy is made (a new Doc from make_v6.py's .docx, or the edits as suggestions in the v6
      Doc), then do it on his go and update the bridge map.
- [x] The cover credit on the copyright page (in book.json, 26 Nov: "Cover credit: me, the author, sketches and Midjourney.")
      Was: The cover credit on the copyright page (`copyright_page` in `publication/novel/build/book.json`), his words.
- [ ] The ISBN, when CT has it.
- [ ] The large print PDF and the release build, when CT asks.

## 4. Every session (start and end)

Not boxes, so `build_gate.py` can say READY when the real work is done:
- Start: `REFERENCE.md`, section 1.
- End: `REFERENCE.md`, section 4.7 (this file, the procedure's "Where things stand", STATE.md and LOG.md in
  `_workbench`, the Drive mirror once).

## Done

- 26 Nov, tenth chat: the housekeeping list (the opening checker, the files brought to v8); edits 224 to 227; the
  checkpoint and the prompt for the eleventh chat; the Drive mirror remade (edits 1 to 227).

- 26 Nov, ninth chat: edits 221 to 223; v8 Doc and its backup; the v8 large print PDF; the bridge remade.

- 26 Nov, eighth chat: CT's eight choices (edits 217 to 219; "Pondwater"; corrections to 198 and 204).
- 26 Nov, eighth chat: Chapter 17's Praether scene (edit 205).
- 26 Nov, eighth chat: the story report, `NEXT-BUILD.md`, `story_report.py` and `build_gate.py`.
- 26 Nov, eighth chat: Chapters 23 (edit 202), 24 (203) and 26 (204) rewritten and logged; continuity fixes to edits
  198 to 204 from three readers' audit; the endgame plan (plan, sections 10 to 13); `find_in_book.py`; the cover credit
  noted; these three files.
- 26 Nov, seventh chat: Chapters 20, 21, 22 and 25 (edits 198 to 201); `WRITING-INSTRUCTIONS.md`; the plan.
- 25 and 26 Nov: edits 1 to 197; v6 made (edits 1 to 138 in the Doc).

- [ ] **Scene sheet audit (27 Nov):** apply `SCENE-SHEET-AUDIT-2026-11-27.md` section A to the Sheet and CSV, put section B to CT, and finish the timeline, 9:40 and Tuesday checks it lists.
