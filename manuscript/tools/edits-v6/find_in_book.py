#!/usr/bin/env python3
"""Look things up in the current book without reading it.

The book is make_v6.py's v6.txt (the v5 Doc plus every logged edit). Each hit is printed with its chapter and line.

    python3 manuscript/tools/edits-v6/find_in_book.py OUT/v6.txt find "regex" ["regex" ...] [--ch 0-19] [--width 160]
    python3 manuscript/tools/edits-v6/find_in_book.py OUT/v6.txt claims CLAIMS.json
    python3 manuscript/tools/edits-v6/find_in_book.py OUT/v6.txt chapters

find     every line that matches every regex given (case ignored), trimmed around the first match.
claims   CLAIMS.json is a list of {"claim": "...", "look": ["regex", ...], "ch": "0-19" (optional)}.
         For each claim it prints the lines that match any of its regexes, so a blurb, a synopsis or a plan
         can be checked against the page. It finds evidence; a person still judges it.
chapters the chapter list with line numbers and word counts.
"""
import json, re, sys

def load(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    # skip the table of contents: the book starts at the last "Chapter 0:" heading
    starts = [i for i, l in enumerate(lines) if re.match(r"Chapter 0:", l)]
    body = starts[-1] if starts else 0
    head = re.compile(r"^(Chapter (\d+): .*|Meanwhile|Epilogue|Appendix|Afterword|About This Book|Act \w+: .*)$")
    chap, num, out = "front", -1, []
    for i, l in enumerate(lines):
        m = head.match(l) if i >= body else None
        if m:
            chap = l.strip()
            if m.group(2):
                num = int(m.group(2))
            elif chap in ("Epilogue", "Appendix", "Afterword", "About This Book"):
                num = 40
        out.append((i + 1, num, chap, l))
    return out

def in_range(num, spec):
    if not spec:
        return True
    a, _, b = spec.partition("-")
    return int(a) <= num <= int(b or a)

def trim(line, m, width):
    a = max(0, m.start() - width // 2); b = min(len(line), m.end() + width // 2)
    return ("…" if a else "") + line[a:b] + ("…" if b < len(line) else "")

def find(book, pats, ch=None, width=160, every=True):
    rx = [re.compile(p, re.I) for p in pats]
    for n, num, chap, l in book:
        if not in_range(num, ch):
            continue
        ms = [r.search(l) for r in rx]
        if (all(ms) if every else any(ms)):
            m = next(x for x in ms if x)
            yield n, chap, trim(l, m, width)

def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    book, cmd, rest = load(a[0]), a[1], a[2:]
    opt = {}
    for k in ("--ch", "--width"):
        if k in rest:
            i = rest.index(k); opt[k] = rest[i + 1]; del rest[i:i + 2]
    if cmd == "chapters":
        seen = {}
        for n, num, chap, l in book:
            seen.setdefault((num, chap), [n, 0]); seen[(num, chap)][1] += len(l.split())
        for (num, chap), (n, w) in seen.items():
            print(f"{n:>5}  {w:>6} words  {chap}")
    elif cmd == "find":
        for n, chap, t in find(book, rest, opt.get("--ch"), int(opt.get("--width", 160))):
            print(f"{n:>5}  [{chap[:28]}]  {t}")
    elif cmd == "claims":
        for c in json.load(open(rest[0], encoding="utf-8")):
            hits = list(find(book, c["look"], c.get("ch"), int(opt.get("--width", 200)), every=False))
            print(f"\n== {c['claim']}  ({len(hits)} lines)")
            for n, chap, t in hits[: c.get("max", 8)]:
                print(f"   {n:>5}  [{chap[:24]}]  {t}")
    else:
        sys.exit(__doc__)

if __name__ == "__main__":
    main()
