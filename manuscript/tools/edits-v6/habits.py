#!/usr/bin/env python3
"""The habits toolbox: find the repeated habits from Chapter 11 on, and deal ways out of them.

CT, 27 Nov (seventeenth chat): "create for yourself a toolbox so that you're not just building from nothing ... some
code that you could call for like maybe some randomized ideas ... instead of reading through each one of them one by
one, you could just read through all of them at once, but with some sort of code that searches for patterns that
we've already identified." How the pass is run, and its rules, are in manuscript/novel/HABITS-PASS.md.

    B=OUT/v6.txt   (make_v6.py's book, every logged edit applied)
    python3 manuscript/tools/edits-v6/habits.py sheet   $B V5_READ.json     write habits-sheet.csv (every instance)
    python3 manuscript/tools/edits-v6/habits.py piles   $B [--from 12]      the pile-ups, in book order, one line each
    python3 manuscript/tools/edits-v6/habits.py batch   $B --from 12 [--size 8] [--skip 0] [--seed 1]
                                                                            the next pile-ups in full: each line in its
                                                                            paragraph, whose words, and three moves dealt
    python3 manuscript/tools/edits-v6/habits.py deal    "the way ..." [--row 41] [--seed 1] [-n 3]
                                                                            three moves for one habit, at random
    python3 manuscript/tools/edits-v6/habits.py use     --row 41 --move the-way.how --before "..." --after "..." [--status proposed]
                                                                            write one line to the ledger
    python3 manuscript/tools/edits-v6/habits.py count                       how often each move has been used, against its cap
    python3 manuscript/tools/edits-v6/habits.py repeats $B [--min 5] [--top 60]
                                                                            exact phrases the book uses more than once

The habits and their patterns are story_report.py's TICS, less day names. Scope: Chapter 11 to the Epilogue (CT: "0
through 10 are fine, because we did 0 through 10 and we published it already").

A pile-up is two or more of one habit in one scene, counting only narration that is not on the guide's kept list.
A line alone in its scene is fine by the guide's rule ("Each is fine once in a scene") and is never dealt.

Files beside the manuscript (manuscript/novel/):
  habits-sheet.csv     every instance: where, the sentence, the counts, where the words came from. Remade by `sheet`.
  habits-moves.json    the moves for each habit, each with a cap. The only hand-written part. CT's own moves are marked.
  habits-ledger.csv    one line per change proposed, accepted, rejected or logged. `use` appends; `count` reads it.

The dealer is seeded (row number and --seed), so the same call deals the same moves. It never deals a move that is at
its cap, and it leans toward the moves used least, so one way out does not become the next habit.
"""
import argparse, csv, json, os, random, re, sys
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
NOVEL = os.path.join(HERE, "..", "..", "novel")
sys.path.insert(0, HERE)
import scene_sheet  # noqa: E402

SHEET = os.path.join(NOVEL, "habits-sheet.csv")
MOVES = os.path.join(NOVEL, "habits-moves.json")
LEDGER = os.path.join(NOVEL, "habits-ledger.csv")
LEDGER_HEAD = ["Row", "Chapter", "Habit", "Move", "Before", "After", "Status", "Note"]
FIRST_CHAPTER = 11

TICS = OrderedDict([
    ("the way ...", r"\bthe way (you|a|an|he|she|they|it|other|people|men)\b"),
    ("He knew / didn't know", r"\b(He|She|Elijah) (knew|didn't know)\b"),
    ("Then he/she", r"(^|[.!?\"] )Then (he|she)\b"),
    ("not X. It's Y", r"\b(isn't|wasn't|not) [^.?!\"]{2,60}[.,] (It's|It was|That's|That was|This is)\b"),
    ("for a while / a long time", r"for a while|a long time|a long second"),
    ("looked at him/her/it", r"\blooked at (him|her|it)\b"),
    ("nodded / shrugged", r"\b(nodded|shrugged)\b"),
    ("didn't say anything", r"didn't say anything|said nothing"),
])
# WRITING-INSTRUCTIONS.md, section 10, "Kept on purpose"
KEPT = ["Then he snorted, and the snort turned into a laugh", "Then Grace did.",
        "Then she reached out and turned it off", "He read it again, slower", "Then he played something else."]


# ---------------------------------------------------------------- the book
def scenes(path):
    """[(heading, chapter number, chapter label, [(line number, paragraph)])] for the body, in book order."""
    lines = open(path, encoding="utf-8").read().split("\n")
    start = [i for i, l in enumerate(lines) if l == "Act One: The Bar"][-1]
    out, head, buf, last = [], None, [], 0

    def flush():
        nonlocal buf
        if head and buf:
            m = re.match(r"Chapter (\d+)", head)
            num = int(m.group(1)) if m else (40 if head == "Epilogue" else last)
            label = ("Ch %d" % num) if m else head
            out.append((head, num, label, buf))
        buf = []

    for i in range(start, len(lines)):
        l = lines[i]
        if l in scene_sheet.STOP:
            break
        if scene_sheet.SECTION.match(l):
            flush()
            if l.startswith("Chapter"):
                last = int(re.match(r"Chapter (\d+)", l).group(1))
            head = ("Meanwhile (after Ch %d)" % last) if l == "Meanwhile" else l
        elif l.startswith("Act ") and len(l) < 40:
            flush()
            head = None
        elif not l.strip():
            flush()
        elif head:
            buf.append((i + 1, l))
    flush()
    return out


def sentence(p, a, b):
    s = max(p.rfind(". ", 0, a), p.rfind("? ", 0, a), p.rfind("! ", 0, a), p.rfind('" ', 0, a))
    s = 0 if s < 0 else s + 2
    e = min([x for x in (p.find(". ", b), p.find("? ", b), p.find("! ", b)) if x >= 0] or [len(p) - 1]) + 1
    return p[s:e].strip()


def find(book):
    """Every instance from FIRST_CHAPTER on, as dicts, in book order, numbered from 1."""
    rows = []
    for sno, (head, num, label, paras) in enumerate(scenes(book), 1):
        if num < FIRST_CHAPTER:
            continue
        for line, p in paras:
            for tic, rx in TICS.items():
                for m in re.finditer(rx, p):
                    a = m.start() + (len(m.group(1)) if tic == "Then he/she" and m.group(1) else 0)
                    sent = sentence(p, a, m.end())
                    rows.append({"chapter": label, "num": num, "scene": sno, "line": line, "habit": tic,
                                 "match": m.group(0).strip(' ."!?'), "speech": p[:a].count('"') % 2 == 1,
                                 "kept": any(k in sent for k in KEPT), "sentence": sent, "para": p, "pos": a})
    rows.sort(key=lambda r: (r["line"], r["pos"]))
    live = Counter((r["scene"], r["habit"]) for r in rows if not r["speech"] and not r["kept"])
    chap = Counter((r["chapter"], r["habit"]) for r in rows)
    for n, r in enumerate(rows, 1):
        r["row"] = n
        r["in_scene"] = live[(r["scene"], r["habit"])]
        r["in_chapter"] = chap[(r["chapter"], r["habit"])]
        r["pile"] = (not r["speech"]) and (not r["kept"]) and r["in_scene"] >= 2
    return rows


# ---------------------------------------------------------------- whose words
class Source:
    def __init__(self, read):
        from whose_words import doc_text
        self.v5 = doc_text(read) if read else ""
        ns = {}
        exec(compile(open(os.path.join(HERE, "ops.py"), encoding="utf-8").read(), "ops.py", "exec"), ns)
        self.ops = [(row[0], row[2].replace("*", "")) for row in ns["OPS"]]
        self.edits = open(os.path.join(NOVEL, "EDITS.md"), encoding="utf-8").read()

    def of(self, sent):
        key = sent[:120]
        hit = sorted({n for n, rep in self.ops if key in rep})
        src = ("edit " + ", ".join(map(str, hit))) if hit else ("base" if key in self.v5 else "unknown")
        ct = ""
        for m in re.finditer(re.escape(key[:60]), self.edits):
            near = self.edits[max(0, m.start() - 200): m.end() + 400]
            if re.search(r"CT's words|\[CT\]|CT:|CT \(", near):
                ct = "yes"
                break
        return src, ct


def read_sheet():
    if not os.path.exists(SHEET):
        return {}
    return {int(r["#"]): r for r in csv.DictReader(open(SHEET, encoding="utf-8"))}


# ---------------------------------------------------------------- the moves and the ledger
def moves():
    return json.load(open(MOVES, encoding="utf-8"))


def ledger():
    if not os.path.exists(LEDGER):
        return []
    return list(csv.DictReader(open(LEDGER, encoding="utf-8")))


def used():
    """How often each move has been used. A rejected line does not count."""
    return Counter(r["Move"] for r in ledger() if not r["Status"].lower().startswith("rejected"))


def deal(habit, row=0, seed=1, n=3):
    """n moves for the habit, at random, leaning to the least used, never one at its cap. The same call, the same deal."""
    ms = moves().get(habit)
    if ms is None:
        sys.exit("No moves for %r. Habits: %s" % (habit, "; ".join(moves())))
    u = used()
    open_ = [m for m in ms if u[m["id"]] < m.get("cap", 6)]
    rng = random.Random("%s|%s|%s" % (habit, row, seed))
    picked = []
    pool = list(open_)
    while pool and len(picked) < n:
        weights = [1 + m.get("cap", 6) - u[m["id"]] for m in pool]
        m = rng.choices(pool, weights=weights)[0]
        picked.append(m)
        pool.remove(m)
    return picked, [m for m in ms if m not in open_]


def show_moves(picked, closed, indent="    "):
    u = used()
    for m in picked:
        print("%s[%s] %s (used %d of %d)%s" % (indent, m["id"], m["name"], u[m["id"]], m.get("cap", 6),
                                              "  CT's" if m.get("ct") else ""))
        print("%s    %s" % (indent, m["how"]))
        if m.get("before"):
            print("%s    e.g. %s" % (indent, m["before"]))
            print("%s      -> %s" % (indent, m["after"]))
    if closed:
        print("%sat their cap, not dealt: %s" % (indent, ", ".join(m["id"] for m in closed)))


# ---------------------------------------------------------------- commands
def cmd_sheet(a):
    rows, src = find(a.book), Source(a.read)
    with open(SHEET, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["#", "Chapter", "Scene (book order)", "Book line", "Habit", "Match", "In speech", "Kept on purpose",
                    "Same habit in this scene", "Same habit in this chapter", "Pile-up", "Whose words (source)", "CT?",
                    "Sentence"])
        for r in rows:
            s, ct = src.of(r["sentence"])
            w.writerow([r["row"], r["chapter"], r["scene"], r["line"], r["habit"], r["match"],
                        "yes" if r["speech"] else "", "kept" if r["kept"] else "", r["in_scene"], r["in_chapter"],
                        "yes" if r["pile"] else "", s, ct, r["sentence"]])
    pile = [r for r in rows if r["pile"]]
    print("%d instances from Chapter %d on: %d in speech, %d kept on purpose, %d alone in their scene, %d in %d pile-ups"
          % (len(rows), FIRST_CHAPTER, sum(r["speech"] for r in rows), sum(r["kept"] for r in rows),
             sum(1 for r in rows if not r["speech"] and not r["kept"] and not r["pile"]), len(pile),
             len({(r["scene"], r["habit"]) for r in pile})))
    print("wrote", os.path.relpath(SHEET))


def piles_of(book, first):
    """[(scene, habit, [rows])] in book order, from chapter `first` on."""
    g = defaultdict(list)
    for r in find(book):
        if r["pile"] and r["num"] >= first:
            g[(r["scene"], r["habit"])].append(r)
    return sorted(g.items(), key=lambda kv: kv[1][0]["line"])


def cmd_piles(a):
    ps = piles_of(a.book, a.first)
    done = {int(r["Row"]) for r in ledger() if r["Row"].isdigit()}
    for i, ((scene, habit), rs) in enumerate(ps):
        mark = "done" if all(r["row"] in done for r in rs) else ("part" if any(r["row"] in done for r in rs) else "")
        print("%3d  %-22s scene %-3d %-26s %d lines (rows %s) %s" % (
            i, rs[0]["chapter"], scene, habit, len(rs), ", ".join(str(r["row"]) for r in rs), mark))
    print("%d pile-ups, %d lines, from Chapter %d on" % (len(ps), sum(len(rs) for _, rs in ps), a.first))


def cmd_batch(a):
    ps = piles_of(a.book, a.first)[a.skip: a.skip + a.size]
    sheet = read_sheet()
    for (scene, habit), rs in ps:
        print("=" * 100)
        print("%s, scene %d (book order): %s, %d in this scene. One stays; reword only the weaker ones."
              % (rs[0]["chapter"], scene, habit, len(rs)))
        for r in rs:
            s = sheet.get(r["row"], {})
            print("\n  row %d, line %d. Whose words: %s%s" % (
                r["row"], r["line"], s.get("Whose words (source)", "run `sheet` first"),
                " (EDITS.md has CT near it: check before touching)" if s.get("CT?") else ""))
            print("  sentence: %s" % r["sentence"])
            print("  paragraph: %s" % r["para"])
            picked, closed = deal(habit, r["row"], a.seed)
            show_moves(picked, closed)
    print("=" * 100)
    print("%d pile-ups shown (skip %d). Next: --skip %d" % (len(ps), a.skip, a.skip + a.size))


def cmd_deal(a):
    picked, closed = deal(a.habit, a.row, a.seed, a.n)
    print("%s, row %s, seed %s:" % (a.habit, a.row, a.seed))
    show_moves(picked, closed, "  ")


def cmd_use(a):
    ids = {m["id"]: h for h, ms in moves().items() for m in ms}
    if a.move not in ids and a.move != "keep":
        sys.exit("No move %r. Run `count` for the list." % a.move)
    new = not os.path.exists(LEDGER)
    sheet = read_sheet().get(a.row, {})
    with open(LEDGER, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        if new:
            w.writerow(LEDGER_HEAD)
        w.writerow([a.row, sheet.get("Chapter", ""), sheet.get("Habit", ids.get(a.move, "")), a.move, a.before, a.after,
                    a.status, a.note])
    print("ledger: row %d, %s, %s" % (a.row, a.move, a.status))


def cmd_count(a):
    u = used()
    for habit, ms in moves().items():
        print(habit)
        for m in ms:
            print("  %-28s %2d of %2d  %s%s" % (m["id"], u[m["id"]], m.get("cap", 6), m["name"],
                                              "  (CT's)" if m.get("ct") else ""))
    st = Counter(r["Status"].split(":")[0].split(";")[0].strip() for r in ledger())
    print("ledger: %d lines. %s" % (sum(st.values()), "; ".join("%s %d" % kv for kv in st.items())))


STOPWORDS = set("a an the and or but of to in on at for with from by as is was were be been it he she they his her "
                "their him them that this then there had has have not no so if out up down into over than when what "
                "who you i we me my your our its s t d ll re ve said didn don".split())


def cmd_repeats(a):
    """Exact word runs used more than once, at least once from FIRST_CHAPTER on. Longest first; a run inside a longer
    run with the same count is dropped. It finds repetition nobody has named yet; a person judges which are callbacks."""
    paras = []
    for head, num, label, ps in scenes(a.book):
        for line, p in ps:
            paras.append((num, label, line, re.findall(r"[a-z']+", p.lower().replace("’", "'"))))
    where = defaultdict(list)
    for num, label, line, w in paras:
        seen = set()
        for n in range(a.min, a.max + 1):
            for i in range(len(w) - n + 1):
                g = tuple(w[i:i + n])
                if g in seen:
                    continue
                seen.add(g)
                where[g].append((num, label, line))
    keep = {g: v for g, v in where.items() if len(v) >= 2 and any(n >= FIRST_CHAPTER for n, _, _ in v)
            and sum(1 for x in g if x not in STOPWORDS) >= a.content}
    out = []
    for g in sorted(keep, key=lambda g: (-len(g), -len(keep[g]))):
        s = " ".join(g)
        if any(s in " ".join(h) and len(keep[h]) >= len(keep[g]) for h, _ in out):
            continue
        out.append((g, keep[g]))
    out.sort(key=lambda x: (-len(x[1]), -len(x[0])))
    for g, v in out[: a.top]:
        print("%2dx  %-52s %s" % (len(v), " ".join(g), ", ".join("%s:%d" % (lab.replace("Ch ", ""), ln) for _, lab, ln in v[:8])
                                  + (" ..." if len(v) > 8 else "")))
    print("%d repeated runs of %d to %d words (showing %d); chapter:line for each use" % (len(out), a.min, a.max, min(a.top, len(out))))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("sheet"); p.add_argument("book"); p.add_argument("read"); p.set_defaults(f=cmd_sheet)
    p = sp.add_parser("piles"); p.add_argument("book"); p.add_argument("--from", dest="first", type=int, default=FIRST_CHAPTER); p.set_defaults(f=cmd_piles)
    p = sp.add_parser("batch"); p.add_argument("book"); p.add_argument("--from", dest="first", type=int, default=FIRST_CHAPTER)
    p.add_argument("--size", type=int, default=8); p.add_argument("--skip", type=int, default=0); p.add_argument("--seed", type=int, default=1); p.set_defaults(f=cmd_batch)
    p = sp.add_parser("deal"); p.add_argument("habit"); p.add_argument("--row", type=int, default=0); p.add_argument("--seed", type=int, default=1)
    p.add_argument("-n", type=int, default=3); p.set_defaults(f=cmd_deal)
    p = sp.add_parser("use"); p.add_argument("--row", type=int, required=True); p.add_argument("--move", required=True)
    p.add_argument("--before", default=""); p.add_argument("--after", default=""); p.add_argument("--status", default="proposed")
    p.add_argument("--note", default=""); p.set_defaults(f=cmd_use)
    p = sp.add_parser("count"); p.set_defaults(f=cmd_count)
    p = sp.add_parser("repeats"); p.add_argument("book"); p.add_argument("--min", type=int, default=5); p.add_argument("--max", type=int, default=9)
    p.add_argument("--content", type=int, default=2, help="least number of words that are not little words")
    p.add_argument("--top", type=int, default=60); p.set_defaults(f=cmd_repeats)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
