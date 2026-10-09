"""Shared helpers for the v0.11.1 core cut. Reads block-annotated files made from v0.11.0."""
import json, re, os
ROOT = os.environ.get('STS_CORE_WORK', '/home/user/sts-core-work')
ANN = os.path.join(ROOT, 'annotated')
MARK = re.compile(r'^<<(sts\.[^ ]+) \| ([a-z\-]+) \| (\d+)w>>$')

def load_blocks(fname):
    """Return list of (id, type, words, text) for one annotated section file."""
    out, cur = [], None
    for line in open(os.path.join(ANN, fname), encoding='utf-8').read().split('\n'):
        m = MARK.match(line)
        if m:
            if cur: out.append(cur)
            cur = [m.group(1), m.group(2), int(m.group(3)), []]
        elif cur is not None:
            cur[3].append(line)
    if cur: out.append(cur)
    return [(i, t, w, '\n'.join(x).strip('\n')) for i, t, w, x in out]

def load_decisions(path):
    d = json.load(open(path, encoding='utf-8'))
    return {x['block']: bool(x['keep']) for x in d['decisions']}, d

def plan_budgets():
    p = os.path.join(ROOT, 'plan.json')
    if not os.path.exists(p): return {}
    plan = json.load(open(p, encoding='utf-8'))
    return {b['file']: b.get('budget_words') for b in plan.get('budgets', [])}
