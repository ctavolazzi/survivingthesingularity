#!/usr/bin/env python3
"""Is the book ready to be composed into the next build?

    python3 manuscript/tools/edits-v6/build_gate.py OUT/v6.txt [--todo manuscript/novel/TODO.md]

Reads build-gate.json (beside this file): lines that must be gone from the text and lines that must be in it before
the next build is made, each with the chapter and the reason. Prints what is still open and exits 1 if anything is.
With --todo it also lists the unticked boxes in the to-do list. It never changes anything.
"""
import json, re, sys
from pathlib import Path

def flat(s):
    return re.sub(r"\s+", " ", s)

def main():
    text = flat(Path(sys.argv[1]).read_text(encoding="utf-8"))
    gate = json.loads((Path(__file__).parent / "build-gate.json").read_text(encoding="utf-8"))
    bad = 0
    print("Must be gone:")
    for g in gate["gone"]:
        there = flat(g["text"]) in text
        bad += there
        print(f"  [{'STILL THERE' if there else 'gone'}] Ch {g['ch']}: \"{g['text']}\" ({g['why']})")
    print("Must be there:")
    for g in gate["there"]:
        there = flat(g["text"]) in text
        bad += (not there)
        print(f"  [{'there' if there else 'MISSING'}] Ch {g['ch']}: \"{g['text']}\" ({g['why']})")
    if "--todo" in sys.argv:
        todo = Path(sys.argv[sys.argv.index("--todo") + 1]).read_text(encoding="utf-8")
        boxes = re.findall(r"^(?:- |\| )\[ \] ?\|? ?(.{0,90})", todo, re.M)
        print(f"Unticked boxes in the to-do list: {len(boxes)}")
        for b in boxes:
            print("  [ ]", b.strip().replace("**", ""))
        bad += len(boxes)
    print("READY" if not bad else f"NOT READY: {bad} open")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
