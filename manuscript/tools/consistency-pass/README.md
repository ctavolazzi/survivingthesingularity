# The consistency pass

One job: make the manuscript agree with itself and with CT's rulings of 19 November, so that his
read-through can be about style and not about fixing contradictions.

- `ops.py` is the list of single-spot changes: the audit's line fixes and everything the stroke
  changes outside chapters 13 to 15. Each has a short quote to find, the new text, and why.
- `apply.py` runs that list against a plain-text copy of the Doc, rebuilds chapters 13 to 15 from
  `drafts/draft-elijah-crash-out-arc.md` plus CT's own scenes, checks that every change lands in
  exactly one paragraph, and writes the result and a report to `drafts/_private/`.

`drafts/_private/` is ignored by git. It holds manuscript text, and this repo is public.

Nothing here writes to the Google Doc. Applying the pass to the Doc is a separate step that CT
has to ask for.

```bash
python3 manuscript/tools/consistency-pass/apply.py /path/to/doc-paragraphs.txt manuscript/drafts/_private
```

The input is the Doc's text with one paragraph per line, taken from a read of the Doc.

## The rest of the tools

- `ops.py` holds every change in stages (`OPS`, `OPS2`, `OPS3`, `OPS4`), the story decisions
  (`DECIDED`), the ideas turned down (`REJECTED`) and what was left alone on purpose (`LEFT`).
- `doc_sync.py` is for putting a stage into the Google Doc once CT has said to write there:
  `dump` turns a saved read of the Doc into one paragraph per line, `emit` simulates the stage
  against the Doc and writes the request batches, `fixup` writes the batch that sets italics
  and deletes marked paragraphs, and `verify` compares the Doc with `book.json` paragraph by
  paragraph. It never calls the connector. The steps are in `NOVEL-METHOD-2026-11-19.md`.
- `make_pdf.py` and `make_pdf.cjs` print `book.json` to a PDF: cover art first, then text only.
  The PDF holds the manuscript, so it stays in `drafts/_private/`.
