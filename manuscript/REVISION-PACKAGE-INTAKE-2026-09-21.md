# Revision package intake, 21 September 2026

Intake of the external `book-revision-workflow` package (v0.7.4 review, dated
21 September 2026) and its editing matrix, mapped onto this repository.

## The correction that matters most

**The package is wrong about the one thing that decides where the work happens.**

Its README says a title search "found the manuscript PDF and supporting documents
but no original editable manuscript or build assets," and its Workflow 4 is written
for the day the production master turns up. Its Workflow 2 therefore has every edit
going through `edit_book.py` patches against text extracted from the PDF.

The production master was never missing. It is `src/lib/data/book/`, at exactly the
version the package reviewed, v0.7.4. Thirty Markdown files plus `book.json`, with
`sts.py`, the EPUB/PDF builders and the website all reading from it. The package's
own Workflow 4 instruction applies immediately rather than someday: port the
reviewed findings onto the real source with exact anchors, and do not treat the
PDF-extracted baseline as the thing to edit.

Consequences for anyone picking this up:

- **Edit `src/lib/data/book/*.md`.** Not `book-revision-workflow/revisions/`, not
  a `manuscript/StS-Complete-Draft-*.md` export, not the PDF.
- **`edit_book.py` and its `patches/` are not this repo's mechanism.** They operate
  on PDF-extracted text carrying page footers and layout whitespace. Git is our
  revision control and `sts.py id` is our block addressing.
- **Package proposals 003 and 004 are drafted against extracted text.** Re-anchor
  them to Markdown before use. The package says it itself: layout-source wording
  may differ from PDF extraction, so do not force those patches onto Markdown.
- **`SOURCE-001` in the package's revision queue is closed by this finding.**
  Recover-or-reconstruct is not needed. Reconciliation is.

The package keeps its value as a review: 45 parent edits, 155 passage rows, four
audits, 23 historical precedents checked, and author decisions A01-A11 recorded.
That analysis is sound and portable. Only its file mechanics do not apply here.

## Correspondence check

Every package section was matched against its repo file by sampling 12-word
shingles from the repo prose and testing for their presence in the package text.

| Package section | Repo file | PDF pp. | Shingle match |
| --- | --- | --- | --- |
| `introduction` | `02-introduction.md` | 3-9 | 92.7% |
| `preface` | `01-preface.md` | 10-13 | 93.3% |
| `chapter-00` | `00-chapter0.md` | 14-22 | 98.9% |
| `part-i` | `part1-divider.md` | 23 | 100.0% |
| `chapter-01` | `03-chapter1.md` | 24-37 | 93.1% |
| `chapter-02` | `04-chapter2.md` | 38-47 | 98.2% |
| `chapter-03` | `05-chapter3.md` | 48-53 | 96.8% |
| `chapter-04` | `06-chapter4.md` | 54-60 | 96.7% |
| `chapter-05` | `07-chapter5.md` | 61-73 | 92.7% |
| `part-ii` | `part2-divider.md` | 74 | 100.0% |
| `chapter-06` | `08-chapter6.md` | 75-81 | 95.2% |
| `chapter-07` | `09-chapter7.md` | 82-96 | 89.0% |
| `chapter-08` | `10-chapter8.md` | 97-117 | 90.7% |
| `chapter-09` | `11-chapter9.md` | 118-136 | 94.8% |
| `part-iii` | `part3-divider.md` | 137 | 100.0% |
| `chapter-10` | `12-chapter10.md` | 138-148 | 94.7% |
| `chapter-11` | `13-chapter11.md` | 149-162 | 89.7% |
| `chapter-12` | `14-chapter12.md` | 163-175 | 93.0% |
| `chapter-13` | `15-chapter13.md` | 176-191 | 90.1% |
| `chapter-14` | `16-chapter14.md` | 192-206 | 95.8% |
| `chapter-15` | `17-chapter15.md` | 207-217 | 92.8% |
| `chapter-16` | `18-chapter16.md` | 218-227 | 95.0% |
| `chapter-17` | `19-chapter17.md` | 228-242 | 91.2% |
| `chapter-18` | `20-chapter18.md` | 243-250 | 100.0% |
| `conclusion` | `21-conclusion.md` | 251-256 | 94.7% |
| `appendix-a` | `22-appendix-a.md` | 257-261 | 94.1% |
| `appendix-b` | `23-appendix-b.md` | 262-276 | 77.4% |
| `appendix-c` | `24-appendix-c.md` | 277-278 | 100.0% |
| `appendix-d` | `25-appendix-d.md` | 279-283 | 90.2% |
| `appendix-e` | `26-appendix-e.md` | 284-289 | 100.0% |

The shortfall from 100% is extraction noise, not divergence: PDF page footers,
hyphenation across page breaks, table and code-block reflow. Appendix B is lowest
at 77% because it is the bibliography, which the layout reflows hardest. Spot
reads of Chapter 11 against `revisions/r002/sections/chapter-11.txt` match word
for word apart from smart quotes.

**`frontmatter` has no repo file and needs none.** The PDF's contents pages are
generated from `book.json`, so a contents entry is changed by changing the title
there. That is why the package counts three title occurrences and this repo has
three source locations that are not the same three.

Page anchors in the matrix are reliable for locating passages. They are the old
PDF's pagination and become meaningless the moment the book is rebuilt, so record
`sts.py id` block ids alongside them when working an item.

## What was applied in this session

**TITLE-001 / E33, author decision A02.** Chapter 11 is now *King and Queen of
Your Own Robotic Court*. This was the only item in the package already decided by
the author and already implemented in its own r002, so it ports with no editorial
judgment left open.

Three source edits:

| File | What |
| --- | --- |
| `src/lib/data/book/13-chapter11.md` | the `#` heading |
| `src/lib/data/book/12-chapter10.md` | the Part III transition naming the chapter |
| `src/lib/data/book/book.json` | the manifest title, which is the contents entry |

Four derived or mirrored files were then brought into line:

| File | How |
| --- | --- |
| `manuscript-index.json` | `sts.py id build` |
| `workshop.json` | title string only, by hand, see below |
| `static/factcheck-trace/index.html` | `sts.py factcheck` then `build_factcheck_trace.py` |
| `art-catalog.json` | by hand, see below |
| `ELIJAH-PROTOCOL.md` | by hand, chapter table row 11 |

Two traps found while doing it, both worth knowing before the next title-shaped edit:

1. **`sts.py art sync --apply` will not fix a stale `section` string.** It only
   appends assets whose id is not already in the catalog; it never refreshes a
   field on an existing entry. `art sync` reported "0 figures to enroll" while
   `art-catalog.json` still carried the old title. Edit that field directly.
2. **`build_workshop_data.py` records git state resolved against `origin/main`,
   so it cannot be regenerated from a feature branch.** Its `receiptsBroken`,
   `dirtyPaths`, `pushed` and `origin_exact` fields describe the worktree against
   `origin/main` at the moment it runs. Two chapters edited on a branch are not
   byte identical to `origin/main`, so every claim in them loses its receipt: a
   regeneration here reported 71 broken receipts and `pushed: false` even with a
   clean tree and the branch pushed. `/workshop` renders that number in red with
   the caption "every claim resolves", so committing it would flip a public page
   to a false failure until merge.

   Only the title string was changed in `workshop.json` here. **Run
   `python3 scripts/build_workshop_data.py` on `main` after this merges** and
   commit the result; the receipts resolve again once the chapters are on
   `origin/main`. The `generatedAt` in the committed file is 2026-08-01 and the
   branch it names is `ship-current`, so it was already a stale snapshot.

`sts.py id build` warned that 2 ids were carried by position rather than content,
in `chapter10` and `chapter11`. Those are the two blocks edited here, and the
warning names in-place edits as the case where position-carry is correct. Checked,
not waved through.

`sts.py id verify` passes: 2,065 blocks, 30 sections, 91,958 words, 85 art links,
no duplicate ids.

## Build status

`npm run build` succeeds and the new title appears in `bookContent.js`, with no
occurrence of the old one.

Two things a future session should not rediscover the hard way:

- **`sharp` is declared in `package.json` but was not installed in this container**,
  and `work_efforts/12_image_optimization_enhancements/image_build_hook.js` imports
  it at build time. The build dies with `ERR_MODULE_NOT_FOUND` before touching
  anything else. Verified pre-existing by stashing all changes and reproducing it.
  `npm install sharp --no-save` clears it.
- **That same hook rewrites `static/images/optimized/` on every build**, producing
  binary churn across eight tracked files plus new ones, unrelated to whatever you
  changed. Those were reverted here. Check for them before committing.

## The 45 recommendations, mapped to source files

Priority as the workbook gives it: P0 first, then P1, then P2. `Scope disposition`
and `Completion test` for each item are in the `Edit queue` sheet of the workbook.

| ID | P | Recommendation | Source files to edit | PDF pp. |
| --- | --- | --- | --- | --- |
| E05 | P0 | Resolve deprivation as an endorsed enforcement tool | `10-chapter8.md`, `11-chapter9.md`, `14-chapter12.md`, `20-chapter18.md` | 113, 122, 170, 247 |
| E20 | P0 | Replace the food recipe with a bounded capability account | `11-chapter9.md` | 128, 132, 133, 134 |
| E22 | P0 | Make computing serve the task without becoming a security manual | `26-appendix-e.md`, `10-chapter8.md`, `13-chapter11.md`, `14-chapter12.md` | 105, 155, 158, 159, 161, 170 |
| E24 | P0 | Make shelter a later application with a limited example | `15-chapter13.md` | 182, 183, 185, 186, 188, 189 |
| E27 | P0 | Remove the incomplete battery assembly as a reader requirement | `19-chapter17.md` | 233, 234, 235, 241 |
| E01 | P1 | Keep the personal AGI date separate from deployment | `24-appendix-c.md`, `03-chapter1.md`, `04-chapter2.md`, `21-conclusion.md`, `02-introduction.md`, `part3-divider.md` | 7, 31, 254, 277, 278 |
| E02 | P1 | Keep the large future as a conditional horizon | `24-appendix-c.md`, `03-chapter1.md`, `04-chapter2.md`, `05-chapter3.md`, `06-chapter4.md`, `07-chapter5.md`, `02-introduction.md`, `part1-divider.md` | 31, 46, 51, 56, 58, 65, 278 |
| E03 | P1 | State the food-first promise at the opening | `21-conclusion.md`, `02-introduction.md`, `01-preface.md` | 6, 11, 254 |
| E04 | P1 | Explain resistance without assigning moral castes | `25-appendix-d.md`, `05-chapter3.md`, `06-chapter4.md`, `07-chapter5.md`, `09-chapter7.md` | 52, 69, 83, 85, 90 |
| E06 | P1 | Move governance design into collective deliberation | `22-appendix-a.md`, `09-chapter7.md`, `10-chapter8.md`, `11-chapter9.md`, `14-chapter12.md`, `20-chapter18.md` | 90, 116, 121, 122, 164, 244, 257 |
| E07 | P1 | Make free assistance plausible without designing an economy | `03-chapter1.md`, `04-chapter2.md`, `08-chapter6.md`, `13-chapter11.md`, `14-chapter12.md`, `20-chapter18.md`, `02-introduction.md` | 32, 45, 79, 149, 156, 165, 248 |
| E08 | P1 | Keep physical and organizational constraints in view | `07-chapter5.md`, `08-chapter6.md`, `20-chapter18.md` | 65, 79, 245 |
| E09 | P1 | Make participation and thriving accessible | `12-chapter10.md`, `14-chapter12.md`, `21-conclusion.md` | 138, 141 |
| E10 | P1 | Give talk, try, adapt a food-first application | `21-conclusion.md` | 251, 255 |
| E11 | P1 | Let practical results revise optimism and doubt | `25-appendix-d.md`, `03-chapter1.md`, `09-chapter7.md`, `12-chapter10.md`, `13-chapter11.md`, `15-chapter13.md`, `19-chapter17.md`, `21-conclusion.md` | 256, 279, 281 |
| E12 | P1 | Keep scientific evidence within its scope | `26-appendix-e.md`, `03-chapter1.md`, `12-chapter10.md` | 28, 33, 34, 142, 287 |
| E13 | P1 | Separate useful human work from guaranteed income | `12-chapter10.md`, `18-chapter16.md`, `20-chapter18.md` | 143, 222, 246 |
| E14 | P1 | Keep attention advice compatible with useful work | `10-chapter8.md`, `19-chapter17.md` | 102, 106, 109, 229 |
| E15 | P1 | Keep cooperation models explanatory | `10-chapter8.md` | 112, 113, 114 |
| E16 | P1 | Explain resilience as useful capacity with dependencies | `11-chapter9.md`, `16-chapter14.md` | 124, 134, 200 |
| E17 | P1 | Finish the grandmother example already on the page | `11-chapter9.md`, `13-chapter11.md`, `14-chapter12.md`, `21-conclusion.md`, `02-introduction.md` | 166–171 |
| E18 | P1 | Make land access an option, not a prerequisite | `14-chapter12.md`, `17-chapter15.md` | 166, 174, 211 |
| E19 | P1 | Measure useful food and labor without mixing units | `14-chapter12.md`, `17-chapter15.md` | 169, 170, 171, 216 |
| E21 | P1 | Keep soil learning grounded in evidence | `17-chapter15.md` | 207, 208, 215 |
| E23 | P1 | Retain energy principles; bound engineering claims | `11-chapter9.md`, `13-chapter11.md`, `15-chapter13.md` | 134, 156, 161, 187, 188 |
| E25 | P1 | Ground food resilience in the right measures | `22-appendix-a.md`, `16-chapter14.md` | 198, 201, 258 |
| E26 | P1 | Share what works without digital guarantees | `12-chapter10.md`, `18-chapter16.md` | 145, 220, 224, 225 |
| E28 | P1 | Match communication links to a useful task | `26-appendix-e.md`, `10-chapter8.md`, `14-chapter12.md`, `16-chapter14.md`, `19-chapter17.md` | 116, 203, 230 |
| E29 | P1 | Separate cleanup, recovery and closed-loop claims | `19-chapter17.md` | 237, 238, 240 |
| E30 | P1 | Choose computing by task, including devices already owned | `26-appendix-e.md` | 286, 287, 288 |
| E31 | P1 | Turn the municipal code into a discussion brief | `22-appendix-a.md`, `14-chapter12.md`, `17-chapter15.md`, `20-chapter18.md` | 165, 213, 244, 257 |
| E35 | P1 | Use history to normalize uncertainty and improve choices | `25-appendix-d.md`, `00-chapter0.md`, `03-chapter1.md`, `04-chapter2.md`, `05-chapter3.md`, `06-chapter4.md`, `07-chapter5.md`, `08-chapter6.md`, `09-chapter7.md`, `10-chapter8.md`, `11-chapter9.md`, `12-chapter10.md`, `13-chapter11.md`, `14-chapter12.md`, `15-chapter13.md`, `16-chapter14.md`, `17-chapter15.md`, `18-chapter16.md`, `19-chapter17.md`, `20-chapter18.md`, `21-conclusion.md`, `01-preface.md` | 13, 81, 89, 256, 281 |
| E36 | P1 | Repair the most consequential historical shortcuts | `25-appendix-d.md`, `09-chapter7.md`, `14-chapter12.md`, `15-chapter13.md`, `16-chapter14.md` | 95, 174, 190, 204 |
| E39 | P1 | Acknowledge threats without assigning one person the cure | `04-chapter2.md`, `05-chapter3.md`, `07-chapter5.md`, `20-chapter18.md`, `part1-divider.md`, `part2-divider.md` | 38, 243 |
| E40 | P1 | Use the premortem to find the next useful gap | `20-chapter18.md` | 245, 248 |
| E41 | P1 | Verify named examples without making them prerequisites | `03-chapter1.md`, `04-chapter2.md`, `11-chapter9.md`, `02-introduction.md` | 6, 34; 271 |
| E43 | P1 | Show the steps from a need to delivered help | `13-chapter11.md`, `14-chapter12.md`, `19-chapter17.md`, `21-conclusion.md` | 149, 159 |
| E44 | P1 | Keep publication time, fiction and forecast distinct | `16-chapter14.md`, `19-chapter17.md`, `20-chapter18.md` | 198, 231, 246 |
| E45 | P1 | Make the first useful step smaller than the whole system | `02-introduction.md`, `part1-divider.md`, `part2-divider.md`, `part3-divider.md`, `01-preface.md` | 7, 137 |
| E32 | P2 | Reconcile the story calendar and acknowledge skill gaps | `00-chapter0.md`, `08-chapter6.md`, `09-chapter7.md`, `12-chapter10.md`, `15-chapter13.md`, `18-chapter16.md`, `20-chapter18.md`, `21-conclusion.md` | 15, 17, 76, 83, 140, 179, 219, 245, 252 |
| E33 | P2 | Carry the approved title into production | `12-chapter10.md`, `13-chapter11.md`, `book.json (contents is generated)` | 2, 147, 149 |
| E34 | P2 | Repair pointers after the bounded revisions | `13-chapter11.md`, `14-chapter12.md`, `17-chapter15.md`, `19-chapter17.md` | 161, 168, 171, 172, 215, 232 |
| E37 | P2 | Keep precedent counts and callbacks consistent | `25-appendix-d.md`, `21-conclusion.md`, `02-introduction.md` | 8, 256, 283 |
| E38 | P2 | Make retained claims and rights traceable | `23-appendix-b.md`, `25-appendix-d.md`, `book.json (contents is generated)` | 262, 283 |
| E42 | P2 | Proof the final book after substantive work | `23-appendix-b.md`, `13-chapter11.md`, `14-chapter12.md`, `book.json (contents is generated)` | 169, 262 |

## Author decisions A01-A11, condensed

A01 AGI forecast: Thanksgiving 2027, November 25. Personal, timing explicitly
unpredictable, the joke preserved. Not yet propagated into prose.
A02 Chapter 11 title. **Applied here.**
A03 Mutually assured survival is the organizing conviction. AGI arriving does not
imply a Terminator conflict.
A04 Coercion and conditional access are forecast to persist. Cheaper labor shifts
bargaining power and makes mutual aid more feasible. A forecast, not a policy.
A05 The grandmother facing a yard-maintenance fine is the access example. Develop
the scene already on pp. 166-171; do not add a second setup.
A06 The book is a tool for the optimist. Threats taken seriously, fatalism not the
organizing principle. A bounded threat chapter at the end of Part I is proposed,
not approved, not inserted.
A07 Historical analogies show recurring human motives. Tools are shortening the
distance from an idea to its realization.
A08 Give readers something concrete to evaluate and criticize: talk, try, adapt.
The author's phrase is *Wide lens, narrow focus*.
A09 Application order: food first, then other land management, trash cleanup,
shelter, then further work.
A10 Governance is collective work. The author does not undertake to design food
safety or cybersecurity institutions alone. The book still owns its own claims.
A11 Answer the laziness, dependence, WALL-E and job-displacement objections
directly and briefly, without dismissing them.

Full text in the package's `AUTHOR-DECISIONS.md`. Where a recommendation and a
decision disagree, the decision governs.

## Protected material

Do not edit these out while working an adjacent item: Elijah's uncertainty,
Denny's mixed motives, grandma's dignity, the exposure consequences, Priya's
willingness to revise, the annual meeting.

## What comes next

The package's own stopping rule is worth keeping in view: correct what the book
claims and what it tells readers to do, and do not expand that into a requirement
that one author solve governance, food safety, employment or a complete autonomous
settlement.

Suggested order, smallest dependency first:

1. **The five P0 items.** Each is a publication claim or a reader instruction that
   is unsupported as written: E05, E20, E22, E24, E27. Narrowing or removing an
   unsupported instruction is a valid resolution. Four of the five sit in three
   files, so they are tractable.
2. **E01 and E03 together.** They fix the forecast vocabulary and the food-first
   promise at the front of the book. Every later item inherits that vocabulary, so
   doing them out of order means doing them twice.
3. **E17, the grandmother example.** Author decision A05 is specific, the scene
   already exists, and the work is finishing it rather than inventing it.
4. Everything else, per the workbook.

Before any of it: decide with the author whether these changes land as v0.7.5 on
this branch, since `book.json` carries the version that becomes EPUB and PDF
metadata. It still says 0.7.4.

## Where the package lives

The package and workbook were unpacked to a scratch directory for this session and
are not committed here. Re-unpack from the originals when needed. The files worth
reading first are `REVISION-QUEUE.md`, `AUTHOR-DECISIONS.md`,
`audit/food-first-review.md` and the `Edit queue` sheet of the workbook.
