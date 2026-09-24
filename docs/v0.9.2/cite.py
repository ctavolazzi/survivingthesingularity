"""Apply inline citations and text corrections to the manuscript from a JSON list.

Each edit is one of:
  {"file": "03-chapter1.md", "after": "<exact text ending a sentence>",
   "label": "Source title", "url": "https://...", "note": "what was verified"}
      -> inserts " [label](url)" immediately after `after`
  {"file": ..., "replace": "<exact old text>", "with": "<new text>", "note": ...}
      -> literal replacement

Every anchor must occur exactly once in its file, or nothing is written.
Every applied edit is appended to docs/v0.9.2/claims-ledger.jsonl.

Usage: python3 docs/v0.9.2/cite.py edits.json [--dry-run]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / 'src/lib/data/book'
LEDGER = Path(__file__).resolve().parent / 'claims-ledger.jsonl'

edits = json.loads(Path(sys.argv[1]).read_text())
dry = '--dry-run' in sys.argv
texts, problems = {}, []
for e in edits:
    f = e['file']
    texts.setdefault(f, (BOOK / f).read_text())
    anchor = e.get('after') or e.get('replace')
    n = texts[f].count(anchor)
    if n != 1:
        problems.append(f'{f}: anchor found {n} times: {anchor[:70]!r}')
        continue
    if 'after' in e:
        if e['url'] in texts[f][texts[f].index(anchor):texts[f].index(anchor) + len(anchor) + 400]:
            problems.append(f'{f}: already cited right after anchor: {anchor[:50]!r}')
            continue
        new = f"{anchor} [{e['label']}]({e['url']})"
    else:
        new = e['with']
    texts[f] = texts[f].replace(anchor, new)
if problems:
    print('\n'.join(problems))
    sys.exit(1)
if dry:
    print(f'{len(edits)} edits OK (dry run)')
    sys.exit(0)
for f, t in texts.items():
    (BOOK / f).write_text(t)
with LEDGER.open('a') as out:
    for e in edits:
        out.write(json.dumps(e, ensure_ascii=False) + '\n')
print(f'{len(edits)} edits applied to {len(texts)} file(s)')
