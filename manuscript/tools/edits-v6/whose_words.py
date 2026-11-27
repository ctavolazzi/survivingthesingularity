#!/usr/bin/env python3
"""Whose words is a line? Trace a phrase from the built book back to where it came from.

    python3 manuscript/tools/edits-v6/whose_words.py V5_READ.json "phrase" ["phrase" ...]

For each phrase it says whether it is in the v5 Doc (the base text), in an ops row (so a logged edit
put it there), which edit in EDITS.md quotes it and whether that entry is marked [CT], and which
files in drafts/ quote it. It finds the record; read the record before saying whose words a line is
(an entry can be "CT's beats and dialogue, narration Claude's", as edit 45 is). The v5 Doc holds CT's
edits 1 to 86 as suggestions, so "in the v5 Doc" does not by itself mean the older text: check EDITS.md.
It finds; it does not judge. On "He could smell her perfume" it reports "[CT" near edit 45, but that entry
says the narration around his beats is Claude's. The answer is in the entry, not in this output.

Written in the smell chat, 27 Nov 2026, after a line was called CT's wording from memory and was not.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOVEL = os.path.join(HERE, "..", "..", "novel")


def doc_text(read_path):
    d = json.load(open(read_path))
    out = []

    def walk(x):
        if isinstance(x, dict):
            if "textRun" in x:
                out.append(x["textRun"].get("content", ""))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(d.get("content", d))
    return "".join(out)


def nearest_edit(edits, i):
    """The numbered entry the position sits in: the last 'N. ' at a line start before it."""
    nums = re.findall(r"\n\s{0,4}(\d{1,3})\. ", edits[:i])
    return nums[-1] if nums else "?"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    v5 = doc_text(sys.argv[1])
    ops = open(os.path.join(HERE, "ops.py")).read()
    edits = open(os.path.join(NOVEL, "EDITS.md")).read()
    drafts = {os.path.basename(f): open(f).read() for f in sorted(glob.glob(os.path.join(NOVEL, "drafts", "*.md")))}
    for p in sys.argv[2:]:
        print(repr(p))
        print("  in the v5 Doc (base text):", "yes" if p in v5 else "no")
        print("  in an ops row (a logged edit):", "yes" if p in ops else "no")
        hits = [m.start() for m in re.finditer(re.escape(p), edits)]
        if hits:
            for i in hits[:5]:
                print(f"  EDITS.md: in or after entry {nearest_edit(edits, i)}; "
                      f"'[CT' within 600 characters after: {'yes' if '[CT' in edits[i:i + 600] else 'no'}")
        else:
            print("  EDITS.md: not quoted")
        files = [f for f, t in drafts.items() if p in t]
        print("  drafts/:", ", ".join(files) if files else "not quoted")


if __name__ == "__main__":
    main()
