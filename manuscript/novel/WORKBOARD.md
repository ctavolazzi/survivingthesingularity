# Workboard: who is doing what on the novel, right now

Several Claude sessions work on this book at once: Claude Code on CT's desktop, Claude Duet on his
phone, and cloud sessions. Two of them started the same job on 22 November without knowing. This
page stops that.

**Before you start a task on the manuscript or its notes, read this page and claim the task. When
you finish or stop, say so here.** Times are Pacific.

If your chat cannot write to GitHub, use the block "Who is working on what" at the top of the Google
Doc "v4 scaffold" instead. A copy of this page is also in Drive, as the Doc "StS workboard: who is
doing what", linked from the page "sts-bridge: read this first". Whoever can write here copies the claims across.

Where the files are: [`BRIDGE.md`](BRIDGE.md), or the Drive page "sts-bridge: read this first".

## Working now

**CT is making his own hand pass in "StS v5 draft (Nov 23)"** (from Nov 24, evening). His words: "my
next step is going to be going through manually reading the whole thing, manually editing and
changing anything that I don't want or that I'd like to change myself." **Do not place suggestions or
edits in v5 during his pass unless he asks for one in so many words.** If he does ask, read the Doc
fresh first and go through the bridge.

**"StS Final Draft v4 Surviving the Singularity" is the untouched fallback. Do not edit it.**

No Claude session has a task open.

## Waiting in v5 (Nov 25)

- CT's edit list of 25 November (edits 1 to 86, and the follow-ups) is in v5 as **156 suggestions**, placed on
  his request. None is accepted yet. The list is `EDITS.md`; what is in the Doc, edit by edit, is
  `EDITS-v5-applied.md`, checked against a fresh read on Nov 25 with `manuscript/tools/edits-v5/verify.py`.
- The two Author's Note changes from earlier that day are also still suggestions.
- After CT accepts them: read v5 fresh, run the verifier (every edit should read "accepted"), then rebuild the
  publication files.

## The state of the book (Nov 24, end of day)

- v5 holds the whole book: 53 headings (the Author's Note, Chapters 0 to 39, four acts, four
  Meanwhiles, the Epilogue, About This Book, the Afterword and the Appendix), 3,615 paragraphs, 19
  pictures, 78 scene breaks.
- No suggestions are waiting in it. No em or en dashes. Straight quotation marks, on his rule.
- It was read whole, line by line, on Nov 24 after the final edit: 16 edits to the words and 60
  italic ranges, each on his yes, then four changes to Lou in Chapter 35 and a last set in Chapters 19, 31, 33, 38 and 39, on his word.
  The list is in
  `manuscript/NOVEL-PROCESS-2026-11-23.md`, section 9.
- The checker in `manuscript/tools/final-check/` passes: 93 checks, none failed. Its self-test
  planted 21 faults and caught all 21.
- The Character Bible (Drive, and `manuscript/NOVEL-CHARACTER-BIBLE-2026-11-23.md`) has every
  character, checked against v5.
- Verdict given to CT: nothing more for a Claude session to do before his own pass.

## v4 as it stood on Nov 23, 3:50 PM (now the fallback)

- v4 holds the whole book: 47 sections, 83,564 words, 19 pictures each with a caption.
- No suggestions and no comments are open in it.
- A code preflight (`manuscript/tools/editor-pass/preflight.py`) ran twice and is clean: 40 chapters
  in order, no dashes, no stray spacing, no unbalanced quotes, no placeholders, no misspelled names,
  and the numbers that must agree do agree. Every callback in Chapters 38 and 39 has its setup
  earlier in the book.
- Verdict given to CT: v4 is ready for his final pass.

What v4 has that v3 did not:

- The co-op is outside Ardell, Washington, eight hundred miles north of Ma.
- Every chapter has a new title, from the Doc "StS v4 Chapter Arcs".
- Chapter 9: Elijah stays in the hall and hears the Architect through a door.
- Chapter 20: Lou's question about essays and meat, in CT's words. Curtis walks up during it.
- Chapter 33: a new Friday dinner.
- Chapters 38 and 39: the machine's message, with CT's lines, and its thanks to Nadzieja Czekaj.
- Added by CT on Nov 23, about 4,000 words: the two robot arms (Chapters 15, 17, 34, 37), Grace's
  sister Faith and her father (Chapters 22, 33, 36), the note in the amp's leather pouch (Chapters 5,
  37, 38), Wren asking why the machine would not simply leave (Chapter 26), and a new last page.

## Rules CT gave on Nov 23

- **When his choice collides with other text, fix the other text. Do not argue for undoing his
  choice, and do not raise the same objection twice.**
- Edits go through the bridge.
- Before saying something is missing from the book, read the chapter around its first use. Claude
  Code reported that "the truck song" had no setup. It did: the search had looked for the literal
  words and missed the scene.

## Settled on Nov 23. Do not reopen these

- The first line keeps "a free beer". Chapter 39 fits it: David slides the four ones back, "Your
  money's no good here", and the book ends on the free beer.
- "County commissioner", not "supervisor" (Chapters 17, 26, 29, 30).
- Lou says "My Marianne" (Chapter 33). Lou calls Elijah "college", "professor" or "Thoreau".
- Chapter 9: "He never saw her face straight on."
- Chapter 37: he keeps Ruby's number and renames it "Don't". Chapter 39 agrees.
- The curb scene says three hundred cups both times (Chapter 15).
- After the machine's wink, Tyler asks "Did it just wink?" (Chapter 38). The machine's lines are CT's
  and stay as dictated.
- Chapter 19: Tyler is "the Tyler who had found Elijah's email for Grace". Chapter 25: "It was the
  truck song from then on." Both were direct edits by Claude Code on CT's instruction.
- CT rejected the tracked suggestions as records and put the changes he wanted into the text
  himself. The text is what counts.

## Settled on Nov 24. Do not reopen these

- Chapter 38: Grace sings "The Weight" with the amp off. She does not play. Elijah does not hear the song.
- Chapter 39: the number Elijah does not call is Ruby's. He turns Wes down for now.
- Chapter 37: "Instead he changed the name to Don't." Chapter 19: "Immediately the vibe shifted."
  stays cut.
- Melody flies in from Miami and signs the visitor book "M. Madrone". Ray's Sundays in that book go
  back to the first spring.
- The amp rides on the floor of the truck with the seat belt through its handle.
- Yvonne is Denny's wife. The Architect is Nadzieja Czekaj. The stove is Walt's.
- Lou calls Elijah "Ivy League", "professor", "Thoreau" and "son". Nobody says "college" (this
  replaces the Nov 23 line above). Marta calls him "spreadsheet". Frank says "bud".
- No "never once" in narration. "Hand flat" only for Elijah's madrone, the amp and the pit, and
  Patricia's binder.
- The locked lines are listed in `manuscript/NOVEL-PROCESS-2026-11-23.md`.

## Still open, and CT's to call

- (Closed Nov 25: the two held lines in Chapter 36 stay as written, his call. The Chapter 8 title
  "Elijah Madrona" stays.)
- Chapter 39: the stream cuts from the prayer straight to Grace's face.
- The parade joke (Chapters 19 and 25), a "looked at" pass on Chapters 15 and 17, and the repeats
  "forty", "nine days" and "like a kid".
- The Afterword's United Nations quotation matches the UN page by web search. The page itself was
  not opened.
- The facts in Chapter 33 have not been source-checked, old or new.
- (Closed Nov 24: the contents list now matches all 53 headings.)
- Pictures in or out of the Amazon edition. He has not answered.
- The Drive Doc "StS v4: Editor's Letter and Readiness Audit (Nov 23)" lists more calls. They are
  optional, and some describe text that has changed since that morning.

## Next, when CT says go (in this order)

1. **After his pass: run the preflight again** on a fresh read, with groups C to F and I of
   `manuscript/tools/final-check/verify_v5.py`.
2. **Build the Kindle file from v5** and check it against the Doc. The build must turn the 78 scene
   breaks (each a paragraph holding one non-breaking space) into a visible mark, add a copyright
   page, and take the 19 captions out if the pictures come out. Curly quotation marks are a choice
   for the build; in the Doc the straight ones stay.
3. **Amazon (KDP)**: a Kindle ebook needs no ISBN. A first book cannot be a pre-order with
   Thanksgiving as release day (the final file is due 5 days before), so publish directly; review
   takes up to 72 hours. The answer to Amazon's question about AI is his.
4. **A source check of Chapter 33's facts.**
5. **The branch `novel/v4-arcs-titles-prompt`** (pull request 41) is not merged. CT has not said.
6. **The website**: every Cloudflare deploy of `main` has failed since at least Nov 9. The likely
   cause is the hosted deployment gate (`scripts/check-hosted-deployment.mjs`). Not confirmed: the
   Cloudflare log needs CT's login. The live site still sells the old non-fiction draft and does not
   mention the novel. The hourly payment check has failed for days and only CT's admin report can say
   why. The private reader still holds v2, and the draft compendium still says Second Crop.

## Done

- **Nov 25**: CT's edit list (edits 1 to 86) logged in `EDITS.md` and placed in v5 as suggestions by
  a second session; checked edit by edit against a fresh read (`EDITS-v5-applied.md`); a verifier added in
  `manuscript/tools/edits-v5/`. Left: CT accepting the suggestions, then a rebuild.
- **Nov 24, later**: v5 read whole; 16 edits and 60 italic ranges applied on CT's yes; the checker
  and its self-test written and run; the Character Bible corrected and completed (27 entries and the
  minor characters); the process file, the map, this page and the Drive bridge page brought up to
  date. Left alone on his instruction: v4, the Drive Canon record, the Change log and the Story
  Structure article.
- **Nov 24, early**: v5 copied from v4; six project scenes, the polish passes, the Chapter 25
  exchange, the nicknames, Grace's beats, his calls on the ending and the Epilogue. The record is
  `manuscript/NOVEL-PROCESS-2026-11-23.md` and `manuscript/NOVEL-CANON-AND-CHANGE-RECORD.md`.
- **Nov 23, afternoon**: preflight written and run twice; two gaps closed; this page and the map
  brought up to date and pushed; the Drive bridge page remade.
- **Nov 23, morning**: all 46 sections of v4 read for the Editor's Letter (124 quoted lines checked);
  47 suggestions placed in v4 and read back. The scripts are in `manuscript/tools/editor-pass/`.
- **Nov 22**: v4 built by Claude Duet from v3 and CT's rulings; reviewed by Claude Code against v3;
  chapter arcs and titles written by another session; the v4 scaffold filled by Duet and checked;
  the bridge built and merged to main; dossiers for Ma, the Architect and the machine updated.

## How to claim

Add a row under "Working now" before you start: the task, who you are, the time, "In progress". Name
the exact chapters or files. If a row already covers what you want to do, do something else or ask CT.
When you stop, move the row to "Done" with one line on what you finished and what you left.
