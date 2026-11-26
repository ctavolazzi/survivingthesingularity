#!/usr/bin/env python3
"""The sentence-opening checker CT asked for on 25 Nov 2026.

CT: "Instead of starting everything with a pronoun, you gotta vary the sentence structure, bro ... a checker or
something that will just scan the book for those instances." It lists, chapter by chapter, the places where the
narration's sentences keep opening the same way. It only finds them; a person fixes each one by hand (change the
openings and joins only; every fact, name and line of dialogue stays), and CT's own words are left as he said them.

    python3 manuscript/tools/edits-v6/openers.py OUT/v6.txt [--ch 20-36] [--run 3] [--subject-run 5] [--quiet]

The book is make_v6.py's v6.txt (find_in_book.py reads it the same way). For each sentence of narration (a sentence
that does not open inside quotation marks) it takes the first word. It reports:

  same-word run   three or more narration sentences in a row that open with the same word ("He ... He ... He").
  subject run     five or more in a row that each open with a pronoun or a name ("He ... Grace ... She ... Elijah
                  ... He"): CT, 26 Nov, swapping "She" for "Grace" ten times is the same problem.
  paragraph       a paragraph of four or more narration sentences where one opener starts more than half of them.

A line of dialogue (a sentence that opens with a quotation mark) ends a run, as does a scene break or a heading.
Exit status is 0; the counts are the result.
"""
import re, sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from find_in_book import load, in_range

PRONOUNS = {"he", "she", "they", "it", "i", "we", "you", "his", "her", "their", "its", "him", "them", "my", "our"}
NOT_NAMES = {"the", "a", "an", "and", "but", "so", "then", "when", "there", "this", "that", "these", "those", "by",
             "in", "on", "at", "for", "from", "with", "after", "before", "nobody", "somebody", "everyone", "nothing",
             "something", "one", "two", "three", "if", "once", "now", "out", "up", "down", "all", "some", "most",
             "every", "each", "no", "not", "what", "which", "who", "how", "why", "where", "maybe", "even", "still",
             "just", "only", "back", "over", "under", "behind", "inside", "outside", "around", "across", "through",
             "behind", "beside", "between", "because", "while", "until", "since", "as", "or", "yes", "okay", "half",
             "another", "both", "either", "neither", "none", "few", "many", "much", "more", "less", "here", "today",
             "tonight", "tomorrow", "yesterday", "outside", "upstairs", "downstairs", "later", "soon", "sometimes",
             "nobody's", "everybody", "anybody", "anyone", "someone", "whoever", "whatever", "chapter", "meanwhile"}
QUOTE = "\"“”'‘’*"
SPLIT = re.compile(r'(?<=[.!?])["”’)]*\s+(?=["“‘(*]?[A-Z0-9])')
WORD = re.compile(r"[A-Za-z][A-Za-z'’]*")


def sentences(par):
    """The paragraph's sentences, each as (is_narration, first_word, text). A sentence that opens with a quotation
    mark, or inside a quotation still open from an earlier sentence, is dialogue."""
    out, inside = [], False
    for s in SPLIT.split(par.strip()):
        s = s.strip()
        if not s:
            continue
        if inside or s[0] in QUOTE:
            out.append((False, None, s))
        else:
            m = WORD.match(s)
            out.append((True, m.group(0) if m else s.split()[0], s))
        for c in s:
            if c == '"':
                inside = not inside
            elif c == "\u201c":
                inside = True
            elif c == "\u201d":
                inside = False
    return out


NAMES = set()


def learn_names(book):
    """Names are words the book capitalizes in the middle of a sentence at least three times and almost never
    writes in lower case (Elijah, Grace, Marta, Lou, Praether ...)."""
    mid, low = Counter(), Counter()
    for _, num, _, line in book:
        for s in SPLIT.split(line):
            ws = WORD.findall(s)
            for w in ws[1:]:
                (mid if w[0].isupper() else low)[w.lower()] += 1
    NAMES.update(w for w, k in mid.items() if k >= 3 and low[w] * 10 < k and w not in NOT_NAMES and w not in PRONOUNS)


def subjectish(w):
    lw = w.lower().replace("\u2019", "'")
    return lw in PRONOUNS or lw.split("'")[0] in PRONOUNS or lw.split("'")[0] in NAMES


def scan(book, ch=None, run_min=3, subj_min=5):
    """Yields per-chapter results: (chapter, narration count, Counter, runs, subject runs, paragraphs)."""
    chapters = {}
    order = []
    for n, num, chap, line in book:
        if not in_range(num, ch) or num < 0:
            continue
        if chap not in chapters:
            chapters[chap] = []
            order.append(chap)
        chapters[chap].append((n, line))
    for chap in order:
        seq = []  # (line, word, text) for narration; None breaks a run
        paras = []
        count = Counter()
        for n, line in chapters[chap]:
            if not line.strip() or line.strip() == chap or line.startswith("[picture]"):
                seq.append(None)
                continue
            ss = sentences(line)
            narr = [(w, t) for nar, w, t in ss if nar]
            for nar, w, t in ss:
                if nar:
                    seq.append((n, w, t))
                    count[w] += 1
                else:
                    seq.append(None)
            if len(narr) >= 4:
                c = Counter(w for w, _ in narr)
                w, k = c.most_common(1)[0]
                if k * 2 > len(narr):
                    paras.append((n, w, k, len(narr)))
        runs, subj = [], []
        cur = []
        for x in seq + [None]:
            if x is not None and cur and x[1] == cur[-1][1]:
                cur.append(x)
                continue
            if len(cur) >= run_min:
                runs.append(cur)
            cur = [x] if x is not None else []
        cur = []
        for x in seq + [None]:
            if x is not None and subjectish(x[1]):
                cur.append(x)
                continue
            if len(cur) >= subj_min:
                subj.append(cur)
            cur = []
        yield chap, sum(count.values()), count, runs, subj, paras


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    opt = {"--ch": None, "--run": "3", "--subject-run": "5"}
    for k in list(opt):
        if k in a:
            i = a.index(k); opt[k] = a[i + 1]; del a[i:i + 2]
    quiet = "--quiet" in a
    book = load(a[0])
    learn_names(book)
    tot = {"runs": 0, "subj": 0, "paras": 0}
    for chap, n, count, runs, subj, paras in scan(book, opt["--ch"], int(opt["--run"]), int(opt["--subject-run"])):
        if not n:
            continue
        top = ", ".join(f"{w} {k * 100 // n}%" for w, k in count.most_common(3))
        print(f"\n== {chap}  ({n} narration sentences; top openers: {top})")
        print(f"   same-word runs: {len(runs)}   subject runs: {len(subj)}   paragraphs: {len(paras)}")
        tot["runs"] += len(runs); tot["subj"] += len(subj); tot["paras"] += len(paras)
        if quiet:
            continue
        for r in runs:
            print(f"   run   line {r[0][0]}: {len(r)} x {r[0][1]!r}: " + " | ".join(t[:40] for _, _, t in r))
        for r in subj:
            print(f"   subj  line {r[0][0]}: {len(r)} in a row: " + " | ".join(w for _, w, _ in r))
        for ln, w, k, m in paras:
            print(f"   para  line {ln}: {k} of {m} open with {w!r}")
    print(f"\nTotal: {tot['runs']} same-word runs, {tot['subj']} subject runs, {tot['paras']} paragraphs")


if __name__ == "__main__":
    main()
