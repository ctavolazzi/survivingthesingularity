"""Usage: python3 merge.py SUFFIX   (e.g. final  -> merges decisions/*.final.json)
Merges per-cluster decision files into decisions/ALL.SUFFIX.json, then checks coverage and
budget for every section in book order (Works Cited excluded) and writes preview/ALL.md."""
import sys, json, glob, os, subprocess
ROOT = os.environ.get('STS_CORE_WORK', '/home/user/sts-core-work')
suffix = sys.argv[1] if len(sys.argv) > 1 else 'final'
order = [f for f, _id, _n, _w in json.load(open(f'{ROOT}/sections.json')) if f != '23-appendix-b.md']
dec, seams = [], []
for p in sorted(glob.glob(f'{ROOT}/decisions/*.{suffix}.json')):
    if os.path.basename(p).startswith('ALL.'): continue
    d = json.load(open(p, encoding='utf-8')); dec += d['decisions']; seams += d.get('seams', [])
os.makedirs(f'{ROOT}/preview', exist_ok=True)
out = f'{ROOT}/decisions/ALL.{suffix}.json'
json.dump({'decisions': dec, 'seams': seams}, open(out, 'w', encoding='utf-8'), indent=0)
r = subprocess.run(['python3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check_cut.py'), out, *order], capture_output=True, text=True)
print(r.stdout[-6000:], r.stderr[-2000:])
subprocess.run(['python3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assemble.py'), out, f'{ROOT}/preview/ALL.md', *order])
