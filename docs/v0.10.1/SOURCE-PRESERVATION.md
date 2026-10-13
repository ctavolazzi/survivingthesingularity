# v0.10.1 source preservation

Checked against the preserved v0.10.0 source. Before reading that source as
reference material, the check verified all 36 files against
`docs/v0.10.1/baseline.json`. Its file map also exactly matches the preserved
v0.10.0 `final-source.json`. The old worktree was read only.

- Sections and manifest order: 35, unchanged.
- Paragraph-delimited source blocks: 2217 before, 2268 after.
- Original blocks preserved verbatim and in order: 2217 of 2217.
- Image references: 79 before, 102 after.
- Unique referenced images: 79 before, 102 after.
- Added image references: 23, each present once and matching the presentation registry.
- Missing or reordered source blocks and removed image occurrences: 0 affected sections.

[Machine report](source-preservation.json) records exact before/after file
SHA-256 values, both baseline-ledger hashes, metadata changes, per-section
counts, and the added image list. Rerun after any canonical source change:

```sh
python3 docs/v0.10.1/check_source_preservation.py
```

For a relocated reference worktree, pass `--before /path/to/sts-v0.10.0`.
That override changes only where the reference is read; all expected hashes
must still match.

The blocks are separated by blank lines and include headings, tables,
images, captions, citations, and prose. Each original block must occur in
order in the new source, and repeated blocks need distinct occurrences.
This does not claim byte-identical source files: additions are expected,
and blank paragraph separators are not part of the block comparison.

Intentional in-memory controls rejected changed reference bytes, deletion
of a real source block, loss of a repeated block, and reordered image
references. The report verifies source preservation only. Final PDF/EPUB
coverage and visual checks remain separate.

| Source file | Blocks before | Blocks after | Original blocks preserved | Image refs before / after |
| --- | ---: | ---: | ---: | ---: |
| 02-introduction.md | 83 | 85 | 83 | 5 / 6 |
| 01-preface.md | 38 | 38 | 38 | 2 / 2 |
| 31-how-to-use.md | 7 | 7 | 7 | 0 / 0 |
| 00-chapter0.md | 88 | 88 | 88 | 1 / 1 |
| part1-divider.md | 3 | 3 | 3 | 1 / 1 |
| 03-chapter1.md | 100 | 102 | 100 | 3 / 4 |
| 04-chapter2.md | 76 | 78 | 76 | 2 / 3 |
| 05-chapter3.md | 58 | 60 | 58 | 1 / 2 |
| 06-chapter4.md | 61 | 61 | 61 | 1 / 1 |
| 07-chapter5.md | 86 | 90 | 86 | 3 / 5 |
| part2-divider.md | 5 | 5 | 5 | 2 / 2 |
| 08-chapter6.md | 73 | 77 | 73 | 3 / 5 |
| 09-chapter7.md | 122 | 122 | 122 | 3 / 3 |
| 10-chapter8.md | 105 | 107 | 105 | 7 / 8 |
| 11-chapter9.md | 93 | 100 | 93 | 7 / 10 |
| part3-divider.md | 5 | 5 | 5 | 1 / 1 |
| 12-chapter10.md | 77 | 77 | 77 | 3 / 3 |
| 13-chapter11.md | 98 | 104 | 98 | 3 / 6 |
| 14-chapter12.md | 78 | 82 | 78 | 2 / 4 |
| 15-chapter13.md | 73 | 73 | 73 | 4 / 4 |
| 16-chapter14.md | 85 | 87 | 85 | 5 / 6 |
| 17-chapter15.md | 70 | 73 | 70 | 4 / 5 |
| 18-chapter16.md | 63 | 63 | 63 | 2 / 2 |
| 19-chapter17.md | 86 | 91 | 86 | 7 / 9 |
| 20-chapter18.md | 104 | 108 | 104 | 2 / 4 |
| 27-chapter19.md | 100 | 100 | 100 | 1 / 1 |
| 21-conclusion.md | 65 | 65 | 65 | 2 / 2 |
| 22-appendix-a.md | 12 | 12 | 12 | 0 / 0 |
| 23-appendix-b.md | 131 | 133 | 131 | 0 / 0 |
| 24-appendix-c.md | 29 | 29 | 29 | 0 / 0 |
| 25-appendix-d.md | 17 | 17 | 17 | 1 / 1 |
| 26-appendix-e.md | 36 | 36 | 36 | 1 / 1 |
| 28-appendix-f.md | 48 | 48 | 48 | 0 / 0 |
| 29-appendix-g.md | 27 | 27 | 27 | 0 / 0 |
| 30-appendix-h.md | 15 | 15 | 15 | 0 / 0 |
