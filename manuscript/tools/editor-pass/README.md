# Editor's pass on v4, 23 November 2026

The scripts behind the Drive Doc "StS v4: Editor's Letter and Readiness Audit (Nov 23)" and the
tracked suggestions placed in "StS Final Draft v4 Surviving the Singularity" that day. They read a
saved `read_doc` JSON of the manuscript. None of them holds a Google Doc id, and none writes to a Doc.

Run them with `python3 -I`. Find the current manuscript through the bridge first
(`node scripts/sts-bridge.mjs status`), and read it fresh.

| File | What it does |
| --- | --- |
| `sections_from_read.py READ.json OUT.json [OLD.json]` | Splits the manuscript into its 47 sections, counts pictures and waiting suggestions, and shows what changed since an earlier read. |
| `prose_audit.py SECTIONS.json OUTDIR` | Sentence length, sentence openings, repeated phrases and small mechanical problems for every section. Also writes one numbered text file per stretch of the book for a read-through. |
| `rulings_check.py SECTIONS.json [group ...]` | Searches for the author's rulings (names, places, the watcher, the machine's lines), dashes and the banned word. |
| `ctx.py SECTIONS.json key:paragraph ...` | Prints the paragraphs around a spot, to check a reader's flag against the text. |
| `build_suggestions.py READ.json OUT.json` | Plans small suggestions. Refuses any passage that does not appear exactly once, spans paragraphs, or carries italics. Whole-paragraph cuts are pinned to the revision that was read. |
| `editor_letter.py SECTIONS.json REPORT.json OUT.html` | Builds the letter. Refuses to write it if any quoted line is not in the manuscript word for word. |
| `suggestions-2026-11-23.json` | The 39 suggestions of that morning, each with its reason. Eight more followed by hand the same day (Chapter 39's beer, and six fixes made around lines the author wants kept). |

Each check that reports a clean result was first shown a made-up passage that it had to reject.
