# The novel: start here

This folder is the book as it is being written, with its history. If you are a new session, read
this page first. It tells you where the current version is and how to work on it.

CT, 19 November 2026: "I'd like you to have version changes and the most current up-to-date
version in the GitHub repository with like a version history as well." "We need to have a version
branch, just like version control for any software, but version control for a book."

## Read this first: the book moved on 20 November

**As of the evening of 22 November 2026 the current text is the Google Doc "StS Final Draft v4
Surviving the Singularity."** It is not "FINAL StS Manuscript," and the copy in this folder is five
versions behind it. "Revised Manuscript v3" is the version before it and is left as it was. The Doc
"v4 scaffold" holds the plan and the notes waiting on the author, with no prose. The rest of this
page describes how things stood on 19 November and is kept as the record of that method.

**Read `BRIDGE.md` in this folder next.** It lists every copy of the book and gives the one way to
change the manuscript. From the command line:

```bash
node scripts/sts-bridge.mjs status     # every copy, and which one is the book right now
node scripts/sts-bridge.mjs check      # is the map sound?
node scripts/sts-bridge.mjs edit READ.json --find "old words" --replace "new words"
node scripts/sts-bridge.mjs suggestions READ.json   # what is waiting on the author
```

The map is `src/lib/data/novel/instances.json`. Change it when a copy changes. The code that
reads it is `src/lib/novel/bridge.js` ("the bridge"), which also holds the compendium at
`/novel/<key>/compendium`. On your own machine, `STS_NO_WORKERD=1 npm run dev` and
`/novel/draft/` open the reader without the private link.

## Where the current book was, on 19 November

- **CT writes in his Google Doc, "FINAL StS Manuscript."** That is the one he edits.
- **The copy here is `FINAL-StS-Manuscript.md`.** It is the whole Doc, pulled in and checked
  against the Doc paragraph by paragraph. Its commit history is the version history.
- **The newest copy is on the version branch, `book/<version>`.** `VERSION` holds the name. `main`
  holds the last checkpoint and can be behind.

To see where everything stands, run this from anywhere in the repository:

```bash
python3 manuscript/tools/book.py status
```

## Before you change anything

The Doc can have moved since the last copy was made, because CT edits it by hand.

1. Get onto the current book: `git fetch origin book/$(cat manuscript/novel/VERSION)` and bring
   that branch's work onto yours.
2. Read the Doc with the Docs connector's `read_doc`. The result is saved to a file.
3. `python3 manuscript/tools/book.py verify <saved-read.json>` says whether the Doc and the copy
   here match. If they do not, pull first (below). Never work from a copy that is behind the Doc.

## The branches

| Branch | What it is |
|---|---|
| `main` | The last checkpoint, and the live site. Every push to `main` redeploys the site, so the book is merged into `main` only when CT says. |
| `book/<version>` | The version being written. The current book. Every pull from the Doc is one commit here. |
| `character/<name>` | One character's work that is waiting on CT: their folder, and changes proposed for the book. Cut from the version branch. When CT says go, the changes go into the Doc, the Doc is pulled, and the branch is merged into the version branch. |
| `claude/...` | One session's own working branch. |

A character branch that has nothing waiting is kept even with the book by
`python3 manuscript/tools/book.py catchup`. One that is behind and has work waiting must have the
version branch merged into it before anyone works on it. `status` shows which is which.

## Making a new version

1. Read the Doc with `read_doc`.
2. `python3 manuscript/tools/book.py pull <saved-read.json> "why it changed"` writes the
   manuscript, counts what changed in each chapter, and adds an entry at the top of `CHANGES.md`.
3. Read the entry and fix its wording. Say who made the change and why.
4. Commit `FINAL-StS-Manuscript.md` and `CHANGES.md` together, with nothing else, on the version
   branch. One version is one commit.

`python3 manuscript/tools/book.py changes <commit>` shows what changed since any earlier version.

## Changing the book from here

Writing to the Doc needs CT's say-so in so many words, every time. So a session does not edit
`FINAL-StS-Manuscript.md` and call it the book. It works like this:

1. Put the proposed change on the character's branch: the reason in their folder, and the new
   words as an edit to the manuscript file there.
2. Show CT. He rules.
3. When he says to write it to the Doc, do it the way `manuscript/NOVEL-METHOD-2026-11-19.md`
   describes, then pull the Doc and check that the two match.

## What is in this folder

| Path | What it is |
|---|---|
| `FINAL-StS-Manuscript.md` | The whole Doc: his planning notes, the novel, and the notes for the next book. |
| `VERSION` | The name of the version being written. |
| `CHANGES.md` | One entry for each version, newest first, then the full record of the pass of 19 November. |
| `characters/` | A folder for each character. `characters/README.md` lists them. |
| `dictation-2026-11-19-morning.md` | CT's dictation of that morning, word for word. None of it is in the book yet. |
| `readers/` | Eight of the ten readers' reports on the whole book, 19 November. The other two are in Elijah's and Grace's folders. |

The readers cite line numbers. In the six Grace reports, line N is paragraph N of the Doc. The ten
earlier reports were made before the last changes of 19 November, so their numbers run up to 18
lines low.

## Where the rest is

| What | Where |
|---|---|
| What to do next, and how CT wants to be worked with | `manuscript/CONTINUATION-2026-11-19-B.md` |
| How Elijah's arc was strengthened, the readers, and writing to the Doc | `manuscript/NOVEL-METHOD-2026-11-19.md` |
| Every change of 19 November as the instruction that made it | `manuscript/tools/consistency-pass/ops.py` |
| The reading page CT reads on his phone | A private artifact. CT has the link. `manuscript/tools/reading-page/README.md` |
| The book the live site sells now, v0.11 | `src/lib/data/book/`. It is a different text. See the root `README.md`. |

Not here, on purpose: CT's personal journal material, his social media export, and the Drive doc
"Trauma and Boundary Reflection." What an earlier search of his Drive found for the book is in
`manuscript/NOVEL-DRIVE-FINDINGS-2026-11-19.md`.
