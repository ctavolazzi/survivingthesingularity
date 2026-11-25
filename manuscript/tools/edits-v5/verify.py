#!/usr/bin/env python3
"""Check every edit in the v5 edit list against a fresh read of the v5 Doc.

    python3 manuscript/tools/edits-v5/verify.py READ.json

READ.json is the Docs connector's read_doc output for "StS v5 draft (Nov 23)". For each edit it says whether
the new text is in the Doc and the old text is gone, reading the Doc as if every suggestion were accepted, and
whether the change is still a pending suggestion or already accepted. Exit code 1 if any edit is missing.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from checks import C

def views(path):
    d = json.load(open(path))
    d = d.get("content", d)
    acc, orig, ids = [], [], set()
    for el in d["tabs"][0]["documentTab"]["body"]["content"]:
        p = el.get("paragraph")
        if not p:
            continue
        for e in p["elements"]:
            tr = e.get("textRun")
            if not tr:
                continue
            si, sd = tr.get("suggestedInsertionIds"), tr.get("suggestedDeletionIds")
            ids.update(si or []); ids.update(sd or [])
            if not sd:
                acc.append(tr["content"])
            if not si:
                orig.append(tr["content"])
    return d.get("revisionId", ""), "".join(acc), "".join(orig), len(ids)

def flat(s):
    s = s.replace("’", "'").replace("“", '"').replace("”", '"').replace("\xa0", " ")
    return re.sub(r"\s+", " ", s)

def main():
    rev, acc, orig, nsug = views(sys.argv[1])
    A, O = flat(acc), flat(orig)
    bad = 0
    print(f"revision {rev[:24]}  pending suggestions: {nsug}")
    for n, where, have, gone in sorted(C, key=lambda r: r[0]):
        miss = [h for h in have if flat(h) not in A]
        left = [g for g in gone if flat(g) in A]
        if miss or left:
            bad += 1
            print(f"{n:>3} {where:<16} MISSING {miss} STILL THERE {left}")
            continue
        pending = any(flat(h) not in O for h in have) or any(flat(g) in O for g in gone)
        print(f"{n:>3} {where:<16} in the Doc, {'pending suggestion' if pending else 'accepted'}")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
