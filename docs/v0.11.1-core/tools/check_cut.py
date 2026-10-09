"""Usage: python3 check_cut.py DECISIONS.json FILE.md [FILE.md ...]
Prints, per section file: total words, kept words, budget (from plan.json), and any
block ids that are missing a decision, unknown, or duplicated. Exit 1 if coverage is incomplete."""
import sys, json, collections
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from cutlib import load_blocks, plan_budgets
dec_path, files = sys.argv[1], sys.argv[2:]
d = json.load(open(dec_path, encoding='utf-8'))
ids = [x['block'] for x in d['decisions']]
dups = [k for k, v in collections.Counter(ids).items() if v > 1]
keep = {x['block']: bool(x['keep']) for x in d['decisions']}
budgets = plan_budgets(); known = set(); bad = False; tk = tt = tb = 0
for f in files:
    blocks = load_blocks(f); known |= {b[0] for b in blocks}
    total = sum(b[2] for b in blocks); kept = sum(b[2] for b in blocks if keep.get(b[0]))
    missing = [b[0] for b in blocks if b[0] not in keep]
    bud = budgets.get(f); tk += kept; tt += total; tb += (bud or 0)
    flag = '' if bud is None else f'  budget {bud}  diff {kept - bud:+d}'
    print(f'{f:22s} total {total:5d}  kept {kept:5d}{flag}  missing {len(missing)}')
    if missing: bad = True; print('   missing:', ' '.join(missing[:20]))
unknown = [i for i in ids if i not in known]
if unknown: bad = True; print('unknown ids:', unknown[:20])
if dups: bad = True; print('duplicate ids:', dups[:20])
print(f'ALL: total {tt}  kept {tk}  budget {tb}  diff {tk - tb:+d}')
sys.exit(1 if bad else 0)
