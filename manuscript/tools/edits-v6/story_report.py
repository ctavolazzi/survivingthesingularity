#!/usr/bin/env python3
"""Measure the story, so an evaluation starts from counts and not from memory.

    python3 manuscript/tools/edits-v6/story_report.py OUT/v6.txt > metrics.md

It prints Markdown tables from make_v6.py's v6.txt: length and dialogue by chapter, who is on the page where, where
each thread opens and closes and its longest silence, the tics CT has ruled on, smells, scenes with only women
speaking, long speeches, and the numbers that have to agree. It judges nothing. A person reads the chapters and judges.
"""
import re, sys
from collections import OrderedDict
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from find_in_book import load

CAST = OrderedDict([
    ("Elijah", r"\bElijah\b"), ("Grace", r"\bGrace\b"), ("Ma", r"\bMa\b|his mother|rose garden"), ("David", r"\bDavid\b|\bDave\b"),
    ("Devendra", r"\bDevendra\b"), ("Lou", r"\bLou\b"), ("Marta", r"\bMarta\b"), ("Curtis", r"\bCurtis\b"),
    ("Priya", r"\bPriya\b"), ("Denny", r"\bDenny\b"), ("Tyler", r"\bTyler\b"), ("Wren", r"\bWren\b"),
    ("Reuben", r"\bReuben\b"), ("Patricia", r"\bPatricia\b"), ("Irene", r"\bIrene\b"), ("Frank", r"\bFrank\b"),
    ("Ochoas", r"\bOchoa|\bLupe\b|\bHector\b"), ("Rosa", r"\bRosa\b"), ("Bidwell", r"\bBidwell\b"), ("Praether", r"\bPraether\b"),
])
THREADS = OrderedDict([
    ("the bet (Thanksgiving 2027, loser cooks)", r"Thanksgiving,? 2027|loser cooks|A bet's a bet|the bet\b"),
    ("the three who were fired", r"three (folks|people|careers)|if they ate|Kelsey|Mateo|the kid who did"),
    ("the amp", r"\bamp\b|Loudbox"),
    ("the Telecaster / playing guitar", r"Telecaster|guitar"),
    ("the notebooks and the stages", r"notebook|\bstages?\b"),
    ("Ma's Sunday call", r"9:40|rose garden"),
    ("Barry", r"\bBarry\b"),
    ("Ma's pot", r"\bpot\b"),
    ("the handout rule / grub", r"handout|hand that feeds|\bgrub\b"),
    ("Melody", r"\bMelody\b|M\. Madrone"),
    ("David and Ray", r"\bDavid\b|\bRay\b"),
    ("Ruby and the lamp", r"\bRuby\b|\blamp\b"),
    ("the Architect / It asked", r"Architect|Czekaj|It asked|asks first"),
    ("Bidwell and his somebody", r"\bBidwell\b|somebody near him"),
    ("the robot arms", r"robot arms|the arms\b|Praether"),
    ("the old man on the curb / the twenty", r"old man|the twenty\b"),
    ("the hose in the glove box", r"\bhose\b"),
    ("the board he hid / the boxes", r"the board\b|circuit board|Iowa|the boxes\b|forty boxes"),
    ("the Ochoas", r"\bOchoa|\bLupe\b|\bHector\b|north houses?"),
    ("the land trust and its payments", r"\btrust\b|Miss three"),
    ("the route and its money", r"\broute\b|a hundred and forty"),
    ("Mrs. Delgado", r"Delgado"),
    ("his pay and the uncashed checks", r"\bchecks?\b|his pay|At half"),
    ("the coupon / became the steel", r"coupon|became the steel"),
    ("the tape / the gate / somebody checked", r"flagging tape|orange tape|Somebody checked|the gate\b"),
    ("you knock", r"\bknock"),
    ("the pond", r"\bpond\b"),
    ("the truck song", r"truck song|The Weight"),
    ("Grace's father and Faith", r"\bFaith\b|her (dad|father)|My dad|Loudbox guy"),
    ("the stove / her fear of fire", r"\bstove\b"),
    ("the pit and the worm", r"\bpit\b|\bworm\b|at thirty"),
    ("Denny's channel and porch", r"channel|the porch\b"),
    ("the welder gap / Marta's shoulder", r"WELDER|shoulder's done|rotator|apprentic"),
    ("the names column / Ship them", r"names column|Ship them"),
    ("the machine on the dairy / since March", r"since March|\bhums?\b|the dairy"),
    ("war and the military", r"military|Ukraine|\bdrones?\b|to find a man in a field|killing"),
    ("the rover", r"\brover\b|gantry"),
    ("the Crucible", r"Crucible"),
    ("node 7 and the mesh", r"node 7|\bmesh\b"),
])
TICS = OrderedDict([
    ("day names", r"\b(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)days?\b"),
    ("the way ...", r"\bthe way (you|a|an|he|she|they|it|other|people|men)\b"),
    ("He knew / didn't know", r"\b(He|She|Elijah) (knew|didn't know)\b"),
    ("Then he/she", r"(^|[.!?\"] )Then (he|she)\b"),
    ("not X. It's Y", r"\b(isn't|wasn't|not) [^.?!\"]{2,60}[.,] (It's|It was|That's|That was|This is)\b"),
    ("for a while / a long time", r"for a while|a long time|a long second"),
    ("looked at him/her/it", r"\blooked at (him|her|it)\b"),
    ("nodded / shrugged", r"\b(nodded|shrugged)\b"),
    ("didn't say anything", r"didn't say anything|said nothing"),
])
SMELL = r"\b(smell\w*|stink\w*|stank|scent\w*|odor\w*|reek\w*|whiff\w*|perfume\w*|cologne)\b"
WOMEN = ["Grace", "Marta", "Priya", "Wren", "Patricia", "Irene", "Rosa", "Lupe", "Lena", "Nina", "Melody", "Faith", "Yvonne", "Mrs. Delgado", "Ruby", "Doreen"]
MEN = ["Elijah", "Lou", "Curtis", "Denny", "Tyler", "Reuben", "Frank", "Hector", "David", "Devendra", "Dale", "Ray", "Praether", "Bidwell", "Manny", "Wes", "Nate"]
NUMBERS = OrderedDict([
    ("households", r"(nineteen|eighteen|twenty|twenty-one) households"), ("people at harvest", r"twenty-two|Twenty people|eighteen people short"),
    ("route boxes", r"a hundred and forty"), ("route money runs to", r"(through|past|in|after) (June|December)\b"),
    ("Elijah's age", r"\b(thirty-(three|four|five|six|seven|eight))\b"), ("Tyler's age", r"(nineteen|twenty|twenty-one|twenty-two)[- ]year[s-]? ?old|was (nineteen|twenty|twenty-one)\b"),
    ("storm outage", r"three days later|overnight"), ("going on N years", r"(going on|almost|for) (two|three|five) years"),
])

def chapters(book):
    """Chapters, the Epilogue, and each "Meanwhile" as a unit of its own (M1, M2, ...)."""
    ch = OrderedDict(); mw = 0; last = None
    for n, num, chap, l in book:
        if not (0 <= num <= 40):
            continue
        if chap.startswith("Chapter") or chap == "Epilogue":
            key = chap
        elif chap == "Meanwhile":
            if last != "Meanwhile" or l.strip() == "Meanwhile":
                if l.strip() == "Meanwhile":
                    mw += 1
            key = f"Meanwhile {mw}"
        else:
            last = chap; continue
        last = chap
        ch.setdefault(key, []).append((n, l))
    return ch

def short(c):
    m = re.match(r"Chapter (\d+)", c)
    if m:
        return m.group(1)
    return "M" + c.split()[-1] if c.startswith("Meanwhile") else "Ep"

def number(c):
    return int(short(c)) if short(c).isdigit() else None

def main():
    book = load(sys.argv[1]); ch = chapters(book); names = list(ch)
    total = sum(len(l.split()) for c in ch for _, l in ch[c])
    print(f"Measured from `{sys.argv[1].split('/')[-1]}`: {total:,} words in Chapters 0 to 39, the four \"Meanwhile\" sections and the Epilogue.\n")
    print("### Length, talk and scenes\n\n| Ch | Title | Words | In quotes | Scenes | Smells |\n|---|---|---|---|---|---|")
    for c in names:
        text = "\n".join(l for _, l in ch[c]); w = len(text.split())
        q = sum(len(x.split()) for x in re.findall(r'"([^"]*)"', text))
        scenes = 1 + sum(1 for _, l in ch[c] if l.strip() == "")
        sm = len(re.findall(SMELL, text, re.I))
        print(f"| {short(c)} | {c.split(': ',1)[-1][:34]} | {w:,} | {100*q//max(w,1)}% | {scenes} | {sm} |")
    print("\n### Who is on the page (mentions per chapter; blank is none)\n")
    print("| Who | " + " | ".join(short(c) for c in names) + " |\n|---|" + "---|" * len(names))
    for who, rx in CAST.items():
        row = [len(re.findall(rx, "\n".join(l for _, l in ch[c]))) for c in names]
        print(f"| {who} | " + " | ".join(str(x) if x else "" for x in row) + " |")
    print("\n### Threads: where each opens, where it is last seen, and its longest silence\n")
    print("| Thread | First | Last | Chapters it is in | Longest gap (chapters) |\n|---|---|---|---|---|")
    for t, rx in THREADS.items():
        hit = [i for i, c in enumerate(names) if re.search(rx, "\n".join(l for _, l in ch[c]))]
        if not hit:
            print(f"| {t} | none | | 0 | |"); continue
        gaps = [(b - a - 1, names[a], names[b]) for a, b in zip(hit, hit[1:])]
        g = max(gaps) if gaps else (0, "", "")
        gap = f"{g[0]} (after Ch {short(g[1])})" if g[0] else "0"
        print(f"| {t} | {short(names[hit[0]])} | {short(names[hit[-1]])} | {len(hit)} | {gap} |")
    print("\n### Tics CT has ruled on (count per 1,000 words, by block of chapters)\n")
    blocks = [("0 to 19", 0, 19), ("20 to 26", 20, 26), ("27 to 36", 27, 36), ("37 to Epilogue", 37, 40)]
    print("| Tic | " + " | ".join(b[0] for b in blocks) + " | Whole book (count) |\n|---|" + "---|" * (len(blocks) + 1))
    def block_text(a, b):
        out, cur = [], 0
        for c in names:
            cur = 40 if c == "Epilogue" else (number(c) if number(c) is not None else cur)
            if a <= cur <= b:
                out += [l for _, l in ch[c]]
        return "\n".join(out)
    for t, rx in TICS.items():
        cells, tot = [], 0
        for _, a, b in blocks:
            tx = block_text(a, b); k = len(re.findall(rx, tx, re.M)); tot += k
            cells.append(f"{1000*k/max(len(tx.split()),1):.1f}")
        print(f"| {t} | " + " | ".join(cells) + f" | {tot} |")
    print("\n### Scenes where two or more women speak\n")
    print("| Line | Chapter | Women speaking | Men speaking |\n|---|---|---|---|")
    only = 0
    for c in names:
        sc, cur = [], []
        for n, l in ch[c]:
            if l.strip() == "":
                sc.append(cur); cur = []
            else:
                cur.append((n, l))
        sc.append(cur)
        for s in sc:
            if not s:
                continue
            sp = set()
            for _, l in s:
                for w in WOMEN + MEN:
                    if re.search(r"\b" + re.escape(w) + r" (said|asked)\b", l):
                        sp.add(w)
            wo = sorted(x for x in sp if x in WOMEN); me = sorted(x for x in sp if x in MEN)
            if len(wo) >= 2:
                only += (not me)
                print(f"| {s[0][0]} | {short(c)} | {', '.join(wo)} | {', '.join(me) or 'none tagged'} |")
    print(f"\nScenes with two or more women tagged as speaking and no man tagged: {only} (check each by reading; a man can be in the room untagged).")
    print("\n### Speeches over 90 words in one paragraph\n\n| Line | Ch | Words in quotes | Opens |\n|---|---|---|---|")
    for c in names:
        for n, l in ch[c]:
            q = re.findall(r'"([^"]*)"', l); w = sum(len(x.split()) for x in q)
            if w > 90:
                print(f"| {n} | {short(c)} | {w} | {q[0][:44]} |")
    print("\n### Numbers that have to agree\n\n| What | Where (chapter: words) |\n|---|---|")
    for t, rx in NUMBERS.items():
        seen = []
        for c in names:
            for _, l in ch[c]:
                for m in re.finditer(rx, l):
                    seen.append(f"{short(c)}: {m.group(0)}")
        print(f"| {t} | {'; '.join(seen[:40])} |")

if __name__ == "__main__":
    main()
