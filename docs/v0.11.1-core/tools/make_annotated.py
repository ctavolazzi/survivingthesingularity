"""Usage: STS_CORE_WORK=/some/dir python3 make_annotated.py [BOOK_DIR]
Rebuilds the block-annotated working copies the core cut was made from. BOOK_DIR defaults to
src/lib/data/book. Writes $STS_CORE_WORK/annotated/<file> and $STS_CORE_WORK/sections.json.
Run from the repo root at the v0.11.0 source (the index must match the text: this checks it)."""
import json, os, re, sys
book = sys.argv[1] if len(sys.argv) > 1 else 'src/lib/data/book'
out = os.environ.get('STS_CORE_WORK', '/home/user/sts-core-work')
os.makedirs(os.path.join(out, 'annotated'), exist_ok=True)
idx = json.load(open(os.path.join(book, 'manuscript-index.json')))
order = [s['file'] for s in json.load(open(os.path.join(book, 'book.json')))['sections']]
by = {s['file']: s for s in idx['sections']}
summary = []
for f in order:
    lines = open(os.path.join(book, f), encoding='utf-8').read().split('\n'); parts = []; total = 0
    for b in by[f]['blocks']:
        a, z = b['lines']; text = '\n'.join(lines[a - 1:z])
        prev = b.get('preview', '')[:25].strip()
        if prev and prev not in text.replace('\n', ' '): sys.exit(f'index does not match text at {b["id"]}; rebuild the index first')
        w = len(re.findall(r'\S+', text)); total += w
        parts.append(f"<<{b['id']} | {b['type']} | {w}w>>\n{text}")
    open(os.path.join(out, 'annotated', f), 'w', encoding='utf-8').write('\n\n'.join(parts) + '\n')
    summary.append((f, by[f]['id'], len(by[f]['blocks']), total))
json.dump(summary, open(os.path.join(out, 'sections.json'), 'w'))
print('wrote', len(summary), 'sections to', out)
