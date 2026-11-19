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
