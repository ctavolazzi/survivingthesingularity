# Source-of-truth primer

A paste-in brief for any fresh chat that is going to touch Surviving the
Singularity book content. Same convention as `CHAPTER-AGENT-PRIMER.md`: copy the
block below into a new chat, verbatim.

---

```text
Before you touch any Surviving the Singularity book content, here is how this
project stores the book. Read it fully. Getting this wrong destroys work.

WHERE THE BOOK IS

The book is the Markdown files in src/lib/data/book/, and book.json in that same
folder decides which of those files are the book and in what order.

Both halves matter:
  - The .md files hold the prose. One file per section.
  - book.json is the manifest: which files, what order, what titles, plus the
    version, title and subtitle that become the EPUB and PDF metadata.

Neither one is the book by itself.

BOOK.JSON IS A GATE, NOT A SUGGESTION

If a .md file sits in that folder but is not listed in book.json's "sections"
array, it is not in the book. Not on the website, not in the EPUB, not in the
PDFs. Nothing about it reaches a reader.

This is deliberate. It is what lets craft documents live next to the manuscript
without leaking into it. As of 2026-07-26 there are 33 .md files in the folder
and 30 of them are the book. The three that are not: VOICE-GUIDE.md (the voice
reference, read it before writing), ELIJAH-PROTOCOL.md (the narrative
throughline spec), and README.md.

So "the file is in the book folder" does not mean "the file is in the book".
Check book.json.

EVERYTHING ELSE CONTAINING BOOK TEXT IS OUTPUT

Five things read that folder and turn it into something else. None of them keeps
an editable copy:

  1. src/lib/bookContent.js       -> the website's /book reader and /read
  2. scripts/build-epub.sh        -> the shipping EPUB and the review PDF
  3. scripts/build-pdf-variants.sh-> the PLAIN and DELUXE PDFs
  4. sts.py compile               -> manuscript/StS-Complete-Draft-*.md snapshots
  5. sts.py id build              -> manuscript-index.json

If you hand-edit any of those five outputs to fix book text, your edit is gone
the next time someone runs a build. Fix the source and rebuild.

THE TWO WAYS PEOPLE ACTUALLY GET BURNED

1. Editing a compiled draft. The files in manuscript/ named
   StS-Complete-Draft-*.md look exactly like the manuscript. They are exports.
   Nothing reads them back into the book. Edits there are a dead end.

2. Trusting manuscript-index.json. It is a generated cache, not truth. And
   `sts.py id verify` cannot tell you it has gone stale, because that command
   re-parses the live .md source and checks it against itself rather than
   against the file on disk. A clean `id verify` is not evidence the index is
   current. This has already happened: the committed index claimed 2046 blocks
   while the source parsed to 2029.

THINGS THAT LOOK LIKE SOURCES AND ARE NOT

  - src/lib/data/book-v1-archive/  (nothing imports it)
  - src/lib/data/sample.md         (nothing imports it)
  - src/lib/data/blueprint.js      (orphaned, the /blueprint route was removed)
  - manuscript/StS-Complete-Draft-*.md and the dated -compiled- files
  - Nine other book.json files elsewhere on disk, in other checkouts and
    archives. They are real files with real version numbers, which is exactly
    what makes them dangerous. The canonical working copy is
    ~/Code/active/sts-v0.7.3 on branch v0.7.3.

FOR NUMBERS, MEASURE, DO NOT READ

Word counts and version numbers: the only authorities are book.json and
scripts/sts.py run live.

  python3 scripts/sts.py book      # per-section word counts, from book.json
  python3 scripts/sts.py verify    # math, meta, refs, precedents. Exits non-zero.
  python3 scripts/sts.py id build  # refresh the block index

Any document asserting a word count or a version is making a claim, not a
measurement, and several of them are stale on purpose-free grounds:
AUDITOR-BRIEF.md carries stale version strings, and STRIPE-GO-LIVE.md had a
stale header for ten days.

CROSS-REFERENCES

Do not type "as we saw in Chapter 4" by hand. Write a pointer:

  [](sts:chapter1)              renders "Chapter 1", and follows the chapter if
                                it is ever renumbered
  [the limits](sts:chapter1)    keeps your wording, still checks the pointer

`sts.py verify refs` fails on a pointer that lands nowhere, and so do the EPUB
and PDF builds. Design notes are in REFS-DESIGN.md.

ONE MORE THING

Multiple chats edit this project at once. Before you commit, run `git status`
and commit only the files you actually changed. Do not use `git commit -a`.
Do not merge to main: main auto-deploys production and production runs live
Stripe keys.
```
