# Workboard: who is doing what on the novel, right now

Several Claude sessions work on this book at once: Claude Code on CT's desktop, Claude Duet on his
phone, and cloud sessions. Two of them started the same job on 22 November without knowing. This
page stops that.

**Before you start a task on the manuscript or its notes, read this page and claim the task. When
you finish or stop, say so here.** Times are Pacific.

If your chat cannot write to GitHub, use the block "Who is working on what" at the top of the Google
Doc "v4 scaffold" instead. It holds the same claims, and every session reads it. Whoever can write
here copies the claims across.

Where the files are: [`BRIDGE.md`](BRIDGE.md), or the Drive page "sts-bridge: read this first".

## Working now

**CT is making his final pass in "StS Final Draft v4 Surviving the Singularity"**, as of 8:42 PM on
Nov 22. He is typing in it. Read it fresh before any edit, make edits as suggestions, and do not
touch a paragraph he is in.

No Claude session has a task open.

**No suggestions or comments are open in v4** (checked Nov 23, 3 PM). CT settled all 47 of this morning's
suggestions and added about 4,000 words: the two robot arms, Grace's sister Faith and her father, the
note in the amp's pouch, and a new ending. The Doc is at about 83,500 words.

**A code preflight passed at 3 PM** (`manuscript/tools/editor-pass/preflight.py`): 40 chapters in order,
19 pictures each with a caption, no dashes, no stray spacing, no unbalanced quotes, no placeholders, no
misspelled names, numbers that must agree do agree. v4 is ready for CT's own final pass.
**Do not place new suggestions in v4 during his pass unless he asks.**

Two small gaps were closed at 3:50 PM on CT's instruction, as direct edits through the bridge: Ch 19 now
says Tyler is "the Tyler who had found Elijah's email for Grace", and Ch 25 names the nickname ("It was
the truck song from then on.") right after Grace mocks "The Weight". One spelling was made American
("canceled", Ch 22). The preflight was run again afterwards and is clean, and every callback in
Chapters 38 and 39 has its setup earlier in the book.

A lesson for the next session: Claude Code first reported that the truck song was never set up. It was.
The search had looked for the literal words. Before saying a thing is missing from the book, read the
chapter around its first use.

For the Kindle build (Claude Code's job, not CT's): 72 scene breaks are blank lines and need a visible
mark; straight quotes become curly; the 19 captions come out if the pictures do; a copyright page.

## The book is in v4 now

"StS Final Draft v4 Surviving the Singularity" holds the whole book: 47 sections, 80,264 words, 19
pictures. Claude Duet built it from v3 with CT's rulings of Nov 22 and 23. "Revised Manuscript v3" is
the version before it and is left as it was. What changed from v3:

- The co-op is outside Ardell, Washington, eight hundred miles north of Ma (v3 said three hours).
- Every chapter has a new title, from the Doc "StS v4 Chapter Arcs".
- Chapter 9: Elijah stays in the hall and hears the Architect through a door.
- Chapter 20: Lou's exchange with Elijah about essays and meat, in CT's words.
- Chapter 33: a new Friday dinner. The chapter grew from 1,404 words to 3,856.
- Chapters 38 and 39: the machine's message, with CT's lines, and its thanks to Nadzieja Czekaj.
- Gaelen, Sparrow Systems, Bidwell's watcher, Crop Dust and the amp are all in.

## Waiting on CT (from the review of v4, Nov 22, about 9 PM)

Claude Code read v4 against v3, the arcs Doc and the rulings. The stories hold together and v4 is
ready for his final pass. These are his to rule on. The same list is at the top of the v4 scaffold.
Nothing here has been changed in v4.

1. **Chapter 0 and Chapter 39.** Settled Nov 23: the first line keeps "a free beer". Chapter 39 is
   rewritten to fit it, in CT's words ("It's six now." ... "God, inflation's a bitch"), as a suggestion.
   **The rule he gave with it: when his choice collides with other text, fix the other text. Do not
   argue for undoing his choice.**
2. **Chapter 20.** Wren is the one who hears Lou's essay and meat exchange. CT asked for "the Critical
   guy who disagrees with Lou a lot". The man who fights Lou at every dinner is Curtis, and he is not
   in this scene.
3. **Chapters 17, 26, 29 and 30** said "county supervisor". Now six suggestions in v4 change it to
   "commissioner".
4. **Chapter 33.** Marianne is named twice and never called Lou's wife. The only other mention is "my
   wife's nephew" in Chapter 17.
5. **Chapter 33's facts** were written after the fact-check of Nov 20 and nobody has looked them up:
   the cotton gin, Jevons, Stockton, the thousand-a-month study, a third of food thrown out, seven in
   ten people in jail not convicted, the Pentagon drone program, the "best behavior" quotation.
6. **Chapter 33's length.** The arcs Doc marks it "not fully standing alone". Claude Code's view: it
   works as it is.
7. **Chapters 8 and 9.** He sees her profile in the lobby, and Chapter 9 says "He never saw her face."

## Next, when CT says go

1. **Apply his answers to the list above**, as suggestions in v4.
2. **A source check of Chapter 33's facts**, the way the Nov 20 fact-check was done.
3. **The branch `novel/v4-arcs-titles-prompt`** holds the instructions the arcs were written from. It
   is not merged. CT has not said whether to merge it.
4. **Amazon (KDP)**: a Kindle ebook needs no ISBN. A first book cannot be a pre-order with
   Thanksgiving as release day (the final file is due 5 days before), so publish directly; review
   takes up to 72 hours. Build the Kindle file from v4 once CT's pass is done, and check it against
   the Doc. The answer to Amazon's question about AI is his.
5. **The website**: every Cloudflare deploy of `main` has failed since at least Nov 9. The likely
   cause is the hosted deployment gate (`scripts/check-hosted-deployment.mjs`), which stops the build
   until payment prerequisites are verified (see `docs/launch-readiness-2026-10-13/README.md`). Not
   confirmed: the Cloudflare log needs CT's login. The live site still serves an old version. The
   private reader still holds v2, and the draft compendium still says Second Crop and the Fisher.

## Done (Nov 23)

- **Editor's pass**: all 46 sections of v4 read; the Drive Doc "StS v4: Editor's Letter and Readiness
  Audit (Nov 23)" written, with 124 quoted lines checked against v4; 47 suggestions placed in v4 and
  read back. The scripts are in `manuscript/tools/editor-pass/`.

## Done (Nov 22)

- **v4 draft**: built by Claude Duet from v3 and CT's rulings. Reviewed by Claude Code in the evening:
  all 47 sections compared with v3 and every changed paragraph read (32 sections changed; Chapters 9 and
  33 read whole), every ruling of the day found in the text, 426 quotations in the
  arcs Doc checked (6 are not word for word), no dashes, no place left in the wrong state apart from
  the "supervisor" lines above.
- **Chapter arcs and titles**: the Doc "StS v4 Chapter Arcs", by another session. The titles are in
  v4's contents and headings, and match the Doc.
- **v4 scaffold**: created by Claude Code; filled by Duet; checked by Claude Code against v3 (Checks
  section); then updated by Duet to match v4.
- **The bridge**: `BRIDGE.md`, `scripts/sts-bridge.mjs` (status, check, where, edit, suggestions,
  verify, export), the Drive page, and this workboard. Merged to main. The map now marks v4 as the
  book.
- **v3**: many edits by Duet; suggestions by Claude Code (Sparrow, Nadzieja, Bidwell's watcher, the
  machine's speech). All of it was carried into v4.
- **Notes in Drive**: the Ma dossier (800 miles), the Architect's dossier (her name, CT's direction),
  the machine's dossier (a full bio).

## How to claim

Add a row under "Working now" before you start: the task, who you are, the time, "In progress". Name
the exact chapters or files. If a row already covers what you want to do, do something else or ask CT.
When you stop, move the row to "Done" with one line on what you finished and what you left.
