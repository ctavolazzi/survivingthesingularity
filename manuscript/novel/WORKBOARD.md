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

**CT is making his own final pass in "StS Final Draft v4 Surviving the Singularity"** (Nov 23, evening).
He types in it. **Do not place suggestions or edits in v4 during his pass unless he asks for one in so
many words.** If he does ask, read the Doc fresh first and go through the bridge.

No Claude session has a task open.

## The state of the book (Nov 23, 3:50 PM)

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

## Still open, and CT's to call

- The facts in Chapter 33 have not been source-checked, old or new.
- The contents page says "Afterword" and "Appendix" where the headings carry their full titles.
- Pictures in or out of the Amazon edition. He has not answered.
- The Drive Doc "StS v4: Editor's Letter and Readiness Audit (Nov 23)" lists more calls. They are
  optional, and some describe text that has changed since that morning.

## Next, when CT says go (in this order)

1. **After his pass: run the preflight again** on a fresh read.
2. **Build the Kindle file from v4** and check it against the Doc. The build must turn the 72
   blank-line scene breaks into a visible mark, make the quotation marks curly, add a copyright page,
   and take the 19 captions out if the pictures come out.
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
