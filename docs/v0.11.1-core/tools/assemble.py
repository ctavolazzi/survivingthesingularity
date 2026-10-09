"""Usage: python3 assemble.py DECISIONS.json OUT.md FILE.md [FILE.md ...]
Writes the kept blocks, verbatim and in order, to OUT.md. Each cut run is marked with a
one-line [CUT: n blocks, w words, first..last id] note so a reader can see the seams."""
import sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from cutlib import load_blocks
dec_path, out, files = sys.argv[1], sys.argv[2], sys.argv[3:]
keep = {x['block']: bool(x['keep']) for x in json.load(open(dec_path, encoding='utf-8'))['decisions']}
parts = []
for f in files:
    run = []
    def flush():
        if run: parts.append(f'[CUT: {len(run)} blocks, {sum(r[2] for r in run)} words, {run[0][0]} .. {run[-1][0]}]'); run.clear()
    for b in load_blocks(f):
        if keep.get(b[0]): flush(); parts.append(b[3])
        else: run.append(b)
    flush()
open(out, 'w', encoding='utf-8').write('\n\n'.join(parts) + '\n')
print('wrote', out)
