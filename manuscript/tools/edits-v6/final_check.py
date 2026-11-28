#!/usr/bin/env python3
"""The final-pass checker: everything CT caught by eye while reading the PDF, found by code.

CT, 28 Nov 2026 (seventeenth chat): "So write the whole like checker code now ... really take your time with this and
do it right, because we're going to use this to do like a very important final pass and create the V9 PDF."

It only finds. A person judges each finding and writes each fix by hand, by WRITING-INSTRUCTIONS.md, and CT's own
dictated lines are left as he said them. Scope is Chapter 11 to the Epilogue unless --from says otherwise (Chapters 0
to 10 are the published sample).

    B=OUT/v6.txt     (make_v6.py's book, every logged edit applied)
    python3 manuscript/tools/edits-v6/final_check.py run   $B V5_READ.json [--from 11]
          every check; writes manuscript/novel/final-check-sheet.csv and prints the counts
    python3 manuscript/tools/edits-v6/final_check.py batch $B [V5_READ.json] --check he [--from 11] [--size 6] [--skip 0] [--all] [--worst]
          the next open findings of one check, each in its context, ready to judge (with the read, whose words)
    python3 manuscript/tools/edits-v6/final_check.py titles $B
          every chapter title and where its words land in the chapter, for a person to read
    python3 manuscript/tools/edits-v6/final_check.py show  $B ID
    python3 manuscript/tools/edits-v6/final_check.py mark  ID --verdict kept|changed|his|on-purpose|wrong [--edit N] [--note "..."]
          one line in manuscript/novel/final-check-ledger.csv; a judged finding stops being listed as open
    python3 manuscript/tools/edits-v6/final_check.py gate  $B [--from 11]
          exit 1 while any finding has no verdict: the door the V9 PDF goes through
    python3 manuscript/tools/edits-v6/final_check.py pdf   FILE.pdf
          in the built PDF: is the paragraph after every scene break indented
    python3 manuscript/tools/edits-v6/final_check.py selftest
          proves each check on CT's own examples: it fires on the page as he found it, and not after his fix

THE CHECKS, each from something CT said on 28 Nov while reading:

  he           "There's a whole lot of he he he he in this section." A passage is flagged when the narration keeps
               opening on the same person: three or more sentences in a row that open with the same pronoun or name;
               or five of six sentences in a row led by the same person ("When he woke", "The first thing he did"
               count, and Elijah counts as "he"); or three or more "steps" in a row. A step is a sentence that only says what somebody did next. His fix,
               in his words: "the truck started up without issue, which pleased Elijah and gave him a sense of relief.
               So you see how instead of just repeating like what happened in a sequence, we're adding emotional timbre
               and texture to the story. We could even add a smell or another physical sense in moments like this."
               Each sentence is printed with a tag (step, mind, state, texture) and the scene's sense counts, so the
               writer can see which beat could carry the feeling. Swapping "He" for "Elijah" is the same problem.
  opener       Three or more narration sentences in a row that open with the same word that is not a pronoun
               ("The ... The ... The"). Lists and repetition for weight are marked "maybe on purpose".
  word         "Too many instances of the word people in one paragraph on one page." A word of four letters or more,
               not a name, used four or more times in one paragraph; or two sentences in a row that open with it.
  speaker      "Here it's not clear who's speaking." A line of talk with no tag, right after narration that names two
               or more people; or six or more untagged lines in a row.
  title        "Chapter 12 is called the $17 shower. And where is that $17 shower?" For each chapter title, where its
               words are in the chapter. Flagged when a title word is missing or the title's moment is two sentences
               or fewer. It cannot tell a moment on the page from one that happens off it, so `titles` prints the
               whole table for a person to read.
  habit        The eight counted habits (habits.py): a pile-up with a line nobody has judged yet.
  phrase       An exact run of five to nine words used three or more times (habits.py repeats).
  mechanics    Typos a script can see: a doubled word, a space before a comma or period, two spaces, an odd number of
               quotation marks in a paragraph, a full paragraph that ends on a bare word, any em or en dash, a curly
               quote.

The PDF check is separate because it reads the built file: "after the dots, the next paragraph doesn't have a tab."
The same test is in publication/novel/build/check.py, so every PDF build now proves it.

Each finding has an id made from its check and its first words, so it stays the same from run to run until the words
change. `mark` records the verdict: changed (fixed, with the edit number), kept (read and left: say why), his (CT's
dictated words), on-purpose (a list, a callback, repetition for weight), wrong (the checker misread it).
"""
import argparse, csv, hashlib, os, re, subprocess, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
NOVEL = os.path.join(HERE, "..", "..", "novel")
sys.path.insert(0, HERE)
import habits  # noqa: E402
import openers  # noqa: E402
from find_in_book import load  # noqa: E402
from story_checks import SENSES, NAME_RE, PEOPLE_C  # noqa: E402

SHEET = os.path.join(NOVEL, "final-check-sheet.csv")
LEDGER = os.path.join(NOVEL, "final-check-ledger.csv")
LEDGER_HEAD = ["ID", "Check", "Chapter", "Verdict", "Edit", "Note", "Text"]
VERDICTS = ("changed", "kept", "his", "on-purpose", "wrong")
CHECKS = ("he", "opener", "word", "speaker", "title", "habit", "phrase", "mechanics")
FIRST = 11

# ---------------------------------------------------------------- words
SUBJ = {"he": "he", "he'd": "he", "he's": "he", "he'll": "he", "she": "she", "she'd": "she", "she's": "she",
        "she'll": "she", "they": "they", "they'd": "they", "they're": "they", "they'll": "they"}
MODAL = {"would", "wouldn't", "could", "couldn't", "might", "may", "should", "shouldn't", "must", "can", "can't"}
SKIP = {"had", "hadn't", "didn't", "did", "just", "never", "still", "also",
        "only", "even", "almost", "nearly", "really", "finally", "always", "already", "then", "now", "soon", "sometimes"}
MIND = set("knew thought wanted felt wondered hoped figured remembered loved hated liked wished believed understood "
           "realized meant decided imagined guessed supposed doubted feared missed needed noticed saw heard watched "
           "know think want feel wonder hope figure remember love hate like wish believe understand realize mean decide "
           "imagine guess suppose doubt fear miss need notice see hear watch thinking wanting".split())
STATE = set("was wasn't were weren't is isn't are aren't been be seemed looked sounded stayed remained".split())
HAVE_NOUN = set("a an the no his her their its two three four five six seven eight nine ten some any one enough".split())
FEELING = (r"\b(relie\w+|pleased|glad|afraid|scared|ashamed|shame|angry|anger|tired|lonely|proud|pride|sick|hurt\w*|"
           r"worr\w+|embarrass\w+|grateful|happy|sad|numb|guilt\w*|sorry|jealous|nervous|dread\w*|panic\w*|joy|"
           r"grief|griev\w+|hopeless|foolish|awful|terrible|wonderful|ache\w*|pit in his stomach|taken aback|"
           r"a rush|stung|couldn't get warm|throat got tight)\b")
COMPARE = r"\b(like|as if|as though|the way|how (he|she|it|you|they))\b"
PHYS = "|".join("(?:%s)" % rx for rx in SENSES.values())
STOP = set("""a an the and or but of to in on at for with from by as is was were be been it he she they his her their
him them that this then there had has have not no so if out up down into over than when what who you i we me my your
our its said would could should about because just back like more some very much many every each one two three four
five six seven eight nine ten any all only even still also again here where which while after before through around
across under behind between against toward away never ever always maybe really thing things something anything
nothing everything someone anyone nobody everybody people's didn't don't wasn't couldn't wouldn't hadn't that's it's
he'd she'd they'd i'm i'd you're can't won't isn't aren't weren't doesn't know knew think thought want wanted going
went come came make made take took look looked tell told ask asked give gave want been being them's time year years
day days night week weeks month months first last next other another same little long good right hand hands""".split())
QUOTE_RE = re.compile(r'"[^"]*"?')
WORDS = re.compile(r"[A-Za-z][A-Za-z']*")


def toks(s):
    return [w.lower().replace("’", "'") for w in WORDS.findall(s)]


def led_by(sentence):
    """('opens' | 'led' | None, who): 'opens' when the first word is he/she/they or a name; 'led' when one of those
    pronouns is among the first five words ("When he woke up", "The first thing he did")."""
    t = toks(sentence)
    if not t:
        return None, None
    if t[0] in SUBJ:
        return "opens", SUBJ[t[0]]
    if t[0].split("'")[0] in openers.NAMES:
        n = t[0].split("'")[0]
        return "opens", ("he" if n == "elijah" else n)
    for w in t[1:5]:
        if w in SUBJ:
            return "led", SUBJ[w]
    return None, None


def tag(sentence):
    """step: says only what somebody did next. mind: what they knew, wanted, felt. state: what was so.
    texture: it carries a feeling word, a sense, or a comparison. other: it is about something else (the truck, the room)."""
    how, who = led_by(sentence)
    low = sentence.lower()
    if re.search(FEELING, low) or re.search(COMPARE, low) or re.search(PHYS, low):
        return "texture"
    if how != "opens":
        return "other"
    t = toks(sentence)[1:]
    if t and t[0] in MODAL:               # "He wouldn't have called it that": a thought about what might be, not a step
        return "mind"
    while t and t[0] in SKIP:
        if t[0] in ("had", "hadn't") and len(t) > 1 and t[1] in HAVE_NOUN:
            return "state"
        t = t[1:]
    if not t:
        return "other"
    if t[0] in MIND:
        return "mind"
    if t[0] in STATE:
        return "state"
    return "step"


# ---------------------------------------------------------------- the book
class Book:
    def __init__(self, path, first=FIRST):
        self.path, self.first = path, first
        openers.NAMES.clear()
        openers.learn_names(load(path))
        self.scenes = []
        for sno, (head, num, label, paras) in enumerate(habits.scenes(path), 1):
            self.scenes.append({"no": sno, "head": head, "num": num, "label": label, "paras": paras})
        self.lines = open(path, encoding="utf-8").read().split("\n")

    def body(self):
        return [s for s in self.scenes if s["num"] >= self.first]

    def sentences(self, scene):
        """[(index, line, para index, is_narration, text)] for the scene, in order."""
        out = []
        for pi, (line, p) in enumerate(scene["paras"]):
            for nar, w, t in openers.sentences(p):
                out.append((len(out), line, pi, nar, t))
        return out


def fid(check, text):
    key = re.sub(r"[^a-z0-9]", "", text.lower())[:90]
    return check[:2] + hashlib.sha1((check + key).encode()).hexdigest()[:7]


def finding(check, scene, line, what, text, context="", weight=1, maybe="", key=None):
    return {"id": fid(check, key or text), "check": check, "chapter": scene["label"], "num": scene["num"],
            "scene": scene["no"], "line": line, "what": what, "text": text, "context": context, "weight": weight,
            "maybe": maybe}


# ---------------------------------------------------------------- he: the same person at the front, over and over
def on_purpose(sents):
    """Why a run may be meant: every sentence opens with the same two words, or every one is a fragment."""
    firsts = {" ".join(toks(s)[:2]) for s in sents}
    if len(firsts) == 1 and len(sents) >= 3:
        return 'all open "%s ..." (repetition for weight?)' % next(iter(firsts))
    if all(len(toks(s)) <= 4 for s in sents):
        return "all fragments (a list?)"
    return ""


def check_he(book):
    out = []
    for sc in book.body():
        ss = book.sentences(sc)
        nar = [x for x in ss if x[3]]
        if len(nar) < 3:
            continue
        idx = {x[0]: k for k, x in enumerate(nar)}
        lead = [led_by(x[4]) for x in nar]
        tags = [tag(x[4]) for x in nar]
        flag = [set() for _ in nar]

        def close(a, b):                      # narration sentences a..b with little talk between them
            return sum(1 for x in ss[nar[a][0]: nar[b][0]] if not x[3]) <= 2

        k = 0                                  # same pronoun or name opening three or more in a row
        while k < len(nar):
            j = k
            while (j + 1 < len(nar) and lead[k][0] == "opens" and lead[j + 1] == lead[k]
                   and nar[j + 1][0] == nar[j][0] + 1):
                j += 1
            if j - k >= 2:
                for q in range(k, j + 1):
                    flag[q].add("run")
            k = j + 1
        for k in range(len(nar) - 5):          # five of six led by the same person
            if not close(k, k + 5):
                continue
            who = Counter(lead[q][1] for q in range(k, k + 6) if lead[q][0])
            if who and who.most_common(1)[0][1] >= 5:
                g = who.most_common(1)[0][0]
                for q in range(k, k + 6):
                    if lead[q][1] == g:
                        flag[q].add("dense")
        k = 0                                  # three or more steps in a row
        while k < len(nar):
            j = k
            while j + 1 < len(nar) and tags[k] == "step" and tags[j + 1] == "step" and nar[j + 1][0] == nar[j][0] + 1:
                j += 1
            if j - k >= 2:
                for q in range(k, j + 1):
                    flag[q].add("steps")
            k = j + 1
        k = 0                                  # join flagged sentences that sit within two of each other
        while k < len(nar):
            if not flag[k]:
                k += 1
                continue
            j = k
            while True:
                nxt = next((q for q in range(j + 1, min(j + 3, len(nar))) if flag[q] and close(j, q)), None)
                if nxt is None:
                    break
                j = nxt
            span = list(range(k, j + 1))
            why = set().union(*(flag[q] for q in span))
            runs = Counter()
            for q in span:
                if lead[q][0] == "opens":
                    runs[lead[q][1]] += 1
            parts = []
            if "run" in why:
                parts.append("the same opener three or more times in a row")
            if "dense" in why:
                parts.append("five of six sentences led by the same person")
            if "steps" in why:
                parts.append("three or more steps in a row")
            led = sum(1 for q in span if lead[q][0])
            steps = sum(1 for q in span if tags[q] == "step")
            text = " ".join(nar[q][4] for q in span)
            ctx = "\n".join("      [%-7s] %s" % (tags[q], nar[q][4]) for q in span)
            scene_text = " ".join(p for _, p in sc["paras"])
            senses = ", ".join("%s %d" % (n.lower(), len(re.findall(rx, scene_text, flags=re.I))) for n, rx in SENSES.items())
            maybe = on_purpose([nar[q][4] for q in span]) if len(span) <= 5 else ""
            out.append(finding("he", sc, nar[k][1],
                               "%d sentences, %d led by %s, %d steps: %s" % (
                                   len(span), led, "/".join("%s x%d" % kv for kv in runs.most_common(3)) or "a pronoun",
                                   steps, "; ".join(parts)),
                               text, ctx + "\n      this scene's senses: " + senses, weight=led + steps, maybe=maybe,
                               key=nar[k][4]))
            k = j + 1
    return out


# ---------------------------------------------------------------- opener: the same non-pronoun word, three in a row
def check_opener(book):
    out = []
    for sc in book.body():
        nar = [x for x in book.sentences(sc) if x[3]]
        k = 0
        while k < len(nar):
            w = toks(nar[k][4])[:1]
            j = k
            while (j + 1 < len(nar) and w and toks(nar[j + 1][4])[:1] == w and nar[j + 1][0] == nar[j][0] + 1):
                j += 1
            if j - k >= 2 and w and w[0] not in SUBJ and w[0].split("'")[0] not in openers.NAMES:
                sents = [nar[q][4] for q in range(k, j + 1)]
                out.append(finding("opener", sc, nar[k][1], '%d sentences in a row open with "%s"' % (len(sents), w[0].capitalize()),
                                   " ".join(sents), weight=len(sents), maybe=on_purpose(sents), key=sents[0]))
            k = j + 1
    return out


# ---------------------------------------------------------------- word: one word too many times in a paragraph
def stem(w):
    if w.endswith("'s"):
        w = w[:-2]
    return w[:-1] if len(w) > 4 and w.endswith("s") and not w.endswith("ss") else w


def check_word(book):
    out = []
    names = {n.lower() for n in PEOPLE_C} | openers.NAMES
    for sc in book.body():
        for line, p in sc["paras"]:
            t = [stem(w) for w in toks(p)]
            c = Counter(w for w in t if len(w) >= 4 and w not in STOP and w not in names)
            for w, k in c.most_common(3):
                if k >= 4 and k * 30 >= len(t):
                    speech = sum(len(q.split()) for q in QUOTE_RE.findall(p)) * 2 > len(p.split())
                    out.append(finding("word", sc, line, '"%s" %d times in one paragraph of %d words%s' % (
                        w, k, len(t), " (mostly speech)" if speech else ""), p, weight=k, key=w + p[:60]))
            ss = [x for x in openers.sentences(p) if x[0]]
            for (a, b) in zip(ss, ss[1:]):
                wa, wb = toks(a[2])[:1], toks(b[2])[:1]
                if wa and wa == wb and len(wa[0]) >= 4 and wa[0] not in STOP and wa[0] not in names and wa[0] not in SUBJ:
                    out.append(finding("word", sc, line, 'two sentences in a row open with "%s"' % wa[0].capitalize(),
                                       a[2] + " " + b[2], context=p, weight=2, key="2" + a[2]))
    seen, uniq = set(), []
    for f in out:
        if f["id"] not in seen:
            seen.add(f["id"])
            uniq.append(f)
    return uniq


# ---------------------------------------------------------------- speaker: a line of talk nobody is given
def check_speaker(book):
    out = []
    for sc in book.body():
        paras = sc["paras"]
        kind = []
        for line, p in paras:
            if '"' not in p:
                kind.append("narr")
            else:
                outside = QUOTE_RE.sub(" ", p)
                kind.append("tagged" if len(WORDS.findall(outside)) >= 2 else "bare")
        i = 0
        while i < len(paras):
            line, p = paras[i]
            if kind[i] == "bare":
                prev = paras[i - 1][1] if i else ""
                who = list(dict.fromkeys(PEOPLE_C[m.group(0)] for m in NAME_RE.finditer(prev))) if i and kind[i - 1] == "narr" else []
                if len(who) >= 2:
                    out.append(finding("speaker", sc, line, "a line with no tag, right after narration that names %s" % " and ".join(who[:3]),
                                       p, context="      before: %s\n      after:  %s" % (prev, paras[i + 1][1] if i + 1 < len(paras) else ""),
                                       weight=3, key="a" + p + prev[-60:]))
                j = i
                while j + 1 < len(paras) and kind[j + 1] == "bare":
                    j += 1
                if j - i >= 5:
                    out.append(finding("speaker", sc, line, "%d lines of talk in a row with no tag" % (j - i + 1),
                                       " / ".join(q for _, q in paras[i:j + 1]), weight=j - i + 1, key="r" + p))
                    i = j
            i += 1
    return out


# ---------------------------------------------------------------- title: is the chapter's promise on the page
NUMWORD = set("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
              "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand".split())


def check_title(book):
    out, by = [], defaultdict(list)
    for sc in book.body():
        by[sc["head"]].append(sc)
    for head, scs in by.items():
        m = re.match(r"Chapter \d+: (.*)", head)
        if not m:
            continue
        words = [w for w in toks(m.group(1).replace("-", " ")) if (len(w) >= 3 and w not in STOP) or w in NUMWORD]
        sents = [(line, t) for sc in scs for _, line, _, _, t in book.sentences(sc)]
        hit = {w: [(l, t) for l, t in sents if re.search(r"\b" + re.escape(stem(w)), t.lower())] for w in words}
        moment = {t for w in words for _, t in hit[w]}
        missing = [w for w in words if not hit[w]]
        if missing or len(moment) <= 2:
            what = ("title word not in the chapter: " + ", ".join(missing)) if missing else \
                   "the title's moment is %d sentence%s long" % (len(moment), "" if len(moment) == 1 else "s")
            ctx = "\n".join("      %s: %d (first at line %s)" % (w, len(hit[w]), hit[w][0][0] if hit[w] else "none") for w in words)
            first = min((hit[w][0] for w in words if hit[w]), default=(scs[0]["paras"][0][0], ""))
            out.append(finding("title", scs[0], first[0], what, head, context=ctx + ("\n      " + first[1] if first[1] else ""),
                               weight=3 if missing else 1, key=head))
    return out


def title_table(book):
    """One line per chapter: each title word, how many sentences hold it, and how many words the paragraphs holding
    them add up to. The check flags a missing word or a moment of two sentences or fewer; it cannot tell whether the
    moment happens on the page or off it (Chapter 12's shower had five sentences and happened off the page), so a
    person reads this table."""
    by, rows = defaultdict(list), []
    for sc in book.body():
        by[sc["head"]].append(sc)
    for head, scs in by.items():
        m = re.match(r"Chapter \d+: (.*)", head)
        if not m:
            continue
        words = [w for w in toks(m.group(1).replace("-", " ")) if (len(w) >= 3 and w not in STOP) or w in NUMWORD]
        paras = [p for sc in scs for _, p in sc["paras"]]
        sents = [t for sc in scs for _, _, _, _, t in book.sentences(sc)]
        cnt = {w: sum(1 for t in sents if re.search(r"\b" + re.escape(stem(w)), t.lower())) for w in words}
        size = sum(len(p.split()) for p in paras if any(re.search(r"\b" + re.escape(stem(w)), p.lower()) for w in words))
        rows.append((head, cnt, size))
    return rows


# ---------------------------------------------------------------- habit and phrase: what habits.py already counts
def check_habit(book):
    judged = {r[k].strip() for r in habits.ledger() for k in ("Before", "After") if r[k].strip()}
    out = []
    g = defaultdict(list)
    for r in habits.find(book.path):
        if r["pile"] and r["num"] >= book.first:
            g[(r["scene"], r["habit"])].append(r)
    for (sno, habit), rs in sorted(g.items(), key=lambda kv: kv[1][0]["line"]):
        new = [r for r in rs if r["sentence"] not in judged and not any(r["sentence"] in j or j in r["sentence"] for j in judged if len(j) > 25)]
        if new:
            sc = next(s for s in book.scenes if s["no"] == sno)
            out.append(finding("habit", sc, new[0]["line"], "%s: %d in this scene, %d not judged in habits-ledger.csv" % (habit, len(rs), len(new)),
                               " | ".join(r["sentence"] for r in new), weight=len(new), key=habit + new[0]["sentence"]))
    return out


def check_phrase(book):
    out = []
    by_num = {s["label"]: s for s in book.scenes}
    for g, uses in habits.repeat_runs(book.path, first=book.first):
        if len(uses) < 3:
            continue
        late = [u for u in uses if u[0] >= book.first]
        sc = by_num.get(late[0][1], book.scenes[-1])
        out.append(finding("phrase", sc, late[0][2], "used %d times: %s" % (len(uses), ", ".join("%s:%d" % (l.replace("Ch ", ""), n) for _, l, n in uses[:9])),
                           " ".join(g), weight=len(uses)))
    return out


# ---------------------------------------------------------------- mechanics
DOUBLE_OK = {"had", "that", "is", "no", "very", "so", "ha", "bye", "now", "there", "her", "yes", "wait", "okay", "go", "whoa", "well", "sorry"}


def check_mechanics(book):
    out = []
    for sc in book.body():
        paras = sc["paras"]
        for i, (line, p) in enumerate(paras):
            def add(what, text, key):
                out.append(finding("mechanics", sc, line, what, text, context=p if text != p else "", key=key + p[:70]))
            for m in re.finditer(r"\b([A-Za-z']+) \1\b", p):
                if m.group(1).lower() not in DOUBLE_OK:
                    add('a doubled word: "%s"' % m.group(0), p[max(0, m.start() - 40): m.end() + 40], "d" + m.group(0))
            for m in re.finditer(r"\S +[,.;:?!](?!\.)", p):
                add("a space before punctuation", p[max(0, m.start() - 30): m.end() + 20], "s%d" % m.start())
            if re.search(r"\S  +\S", p):
                add("two spaces together", p[max(0, re.search(r"\S  +\S", p).start() - 30): re.search(r"\S  +\S", p).end() + 30], "2")
            if re.search("[\u2014\u2013]", p):
                add("an em or en dash", p, "em")
            if re.search("[\u201c\u201d\u2018\u2019]", p):
                add("a curly quote (the book's are straight)", p, "cq")
            if p.count('"') % 2 == 1:
                nxt = paras[i + 1][1] if i + 1 < len(paras) else ""
                if not (nxt.startswith('"') and p.rstrip()[-1:] != '"'):      # a speech carried into the next paragraph is right
                    add("an odd number of quotation marks", p, "q")
            if (re.search(r"[A-Za-z0-9]$", p.rstrip()) and len(p.split()) >= 8 and (p[0].isupper() or p[0] == '"')
                    and not p.isupper()):
                add("the paragraph does not end in punctuation", p[-80:], "e")
    return out


RUN = {"he": check_he, "opener": check_opener, "word": check_word, "speaker": check_speaker, "title": check_title,
       "habit": check_habit, "phrase": check_phrase, "mechanics": check_mechanics}


def run_all(book, only=None):
    out = []
    for c in CHECKS:
        if only and c != only:
            continue
        out += RUN[c](book)
    return out


# ---------------------------------------------------------------- the ledger
def ledger():
    if not os.path.exists(LEDGER):
        return {}
    return {r["ID"]: r for r in csv.DictReader(open(LEDGER, encoding="utf-8"))}


def whose(src, text):
    if src is None:
        return "", ""
    first = openers.SPLIT.split(text.strip())[0] if text.strip() else text
    return src.of(first)


# ---------------------------------------------------------------- commands
def cmd_run(a):
    book = Book(a.book, a.first)
    fs = run_all(book)
    led = ledger()
    src = habits.Source(a.read) if a.read else None
    with open(SHEET, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["ID", "Check", "Chapter", "Scene (book order)", "Book line", "What", "Maybe on purpose", "Text",
                    "Whose words (source)", "CT?", "Verdict", "Edit", "Note"])
        for x in sorted(fs, key=lambda x: (CHECKS.index(x["check"]), x["line"])):
            s, ct = whose(src, x["text"]) if x["check"] in ("he", "opener", "word", "speaker") else ("", "")
            v = led.get(x["id"], {})
            w.writerow([x["id"], x["check"], x["chapter"], x["scene"], x["line"], x["what"], x["maybe"], x["text"], s, ct,
                        v.get("Verdict", ""), v.get("Edit", ""), v.get("Note", "")])
    print("Final check, Chapter %d to the Epilogue (%s)" % (a.first, os.path.basename(a.book)))
    print("%-10s %6s %7s %5s   by verdict" % ("check", "found", "judged", "open"))
    total_open = 0
    for c in CHECKS:
        mine = [x for x in fs if x["check"] == c]
        j = [x for x in mine if x["id"] in led]
        v = Counter(led[x["id"]]["Verdict"] for x in j)
        total_open += len(mine) - len(j)
        print("%-10s %6d %7d %5d   %s" % (c, len(mine), len(j), len(mine) - len(j), ", ".join("%s %d" % kv for kv in v.items())))
    he = Counter(x["chapter"] for x in fs if x["check"] == "he" and x["id"] not in led)
    print("he, open, by chapter: " + ", ".join("%s %d" % (k.replace("Ch ", ""), v) for k, v in he.items()))
    print("%d open. Wrote %s" % (total_open, os.path.relpath(SHEET)))


def show(x, led, src=None):
    v = led.get(x["id"])
    print("-" * 100)
    print("%s  %s  %s, scene %d, line %d%s" % (x["id"], x["check"], x["chapter"], x["scene"], x["line"],
                                              ("   [%s]" % v["Verdict"]) if v else ""))
    print("   %s" % x["what"])
    if x["maybe"]:
        print("   maybe on purpose: %s" % x["maybe"])
    if src:
        s, ct = whose(src, x["text"])
        print("   whose words: %s%s" % (s, {"yes": " (the entry says CT's words: leave them)", "mixed": " (the entry has CT's words and Claude's: read it)"}.get(ct, "")))
    if x["check"] != "he":
        print("   %s" % x["text"])
    for l in x["context"].split("\n") if x["context"] else []:
        if src and x["check"] == "he" and l.startswith("      [") and "] " in l:
            s_, ct = src.of(l.split("] ", 1)[1])
            hint = {"yes": ", the entry says CT's words", "mixed": ", the entry has CT's words and Claude's"}.get(ct, "")
            l += ("    <- %s%s" % (s_, hint)) if (s_ != "base" or ct) else ""
        print(l)


def cmd_batch(a):
    book = Book(a.book, a.first)
    led = ledger()
    fs = [x for x in sorted(run_all(book, a.check), key=lambda x: x["line"]) if a.all or x["id"] not in led]
    if a.worst:
        fs.sort(key=lambda x: -x["weight"])
    src = habits.Source(a.read) if a.read else None
    if a.check == "he":
        print('CT: "instead of just repeating like what happened in a sequence, we\'re adding emotional timbre and texture')
        print('to the story. We could even add a smell or another physical sense in moments like this." His example: "He')
        print('needed a charge. He started the truck ..." becomes "the truck started up without issue, which pleased Elijah')
        print('and gave him a sense of relief." Leave runs that are meant. Change the fewest sentences that break the run.')
    for x in fs[a.skip: a.skip + a.size]:
        show(x, led, src)
    print("-" * 100)
    print("%d shown of %d %s (skip %d). Next: --skip %d" % (len(fs[a.skip: a.skip + a.size]), len(fs),
                                                          "in all" if a.all else "open", a.skip, a.skip + a.size))


def cmd_titles(a):
    book = Book(a.book, a.first)
    print("Each chapter title: sentences holding each word, and the words in the paragraphs that hold them.")
    for head, cnt, size in title_table(book):
        flag = "  <-- read this one" if (not cnt or min(cnt.values()) == 0 or size < 120) else ""
        print("%-44s %-46s %5d words%s" % (head[:44], ", ".join("%s %d" % kv for kv in cnt.items())[:46], size, flag))


def cmd_show(a):
    book = Book(a.book, a.first)
    for x in run_all(book):
        if x["id"] == a.id:
            show(x, ledger())
            print("   text: %s" % x["text"])
            return
    sys.exit("No finding %s in this book (fixed, or the words changed)." % a.id)


def cmd_mark(a):
    if a.verdict not in VERDICTS:
        sys.exit("verdict is one of: " + ", ".join(VERDICTS))
    if a.verdict == "changed" and not a.edit:
        sys.exit("a changed finding needs --edit N")
    if a.verdict in ("kept", "wrong") and not a.note:
        sys.exit("say why with --note")
    row = next((r for r in csv.DictReader(open(SHEET, encoding="utf-8")) if r["ID"] == a.id), None) if os.path.exists(SHEET) else None
    if row is None:
        sys.exit("No finding %s in the sheet. Run `run` first." % a.id)
    rows = [r for r in ledger().values() if r["ID"] != a.id]
    rows.append({"ID": a.id, "Check": row["Check"], "Chapter": row["Chapter"], "Verdict": a.verdict, "Edit": a.edit or "",
                 "Note": a.note or "", "Text": row["Text"][:200]})
    with open(LEDGER, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, LEDGER_HEAD, lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)
    print("%s: %s" % (a.id, a.verdict))


def cmd_gate(a):
    book = Book(a.book, a.first)
    led = ledger()
    fs = run_all(book)
    left = Counter(x["check"] for x in fs if x["id"] not in led)
    for c in CHECKS:
        print("%-10s %d open" % (c, left[c]))
    if sum(left.values()):
        print("NOT READY: %d findings have no verdict" % sum(left.values()))
        sys.exit(1)
    print("READY: every finding has a verdict")


# ---------------------------------------------------------------- the built PDF
def scene_break_indents(pdf, mark="* * *"):
    """[(page, text)] for each paragraph that follows a scene break without a first-line indent, and the number of
    breaks seen. Read from `pdftotext -layout`: a page's margin is the least indent among its long lines."""
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    pages = [p.split("\n") for p in txt.split("\f")]
    want = mark.replace(" ", "")

    def lead(l):
        return len(l) - len(l.lstrip(" "))

    def margin(lines):
        long_ = [lead(l) for l in lines if len(l.strip()) > 25]
        return min(long_) if long_ else None

    bad, seen = [], 0
    for pi, lines in enumerate(pages):
        for li, l in enumerate(lines):
            if l.strip().replace(" ", "") != want or not l.strip():
                continue
            seen += 1
            nxt = next((x for x in lines[li + 1:] if x.strip() and not x.strip().isdigit()), None)
            pg, mg = pi, margin(lines)
            if nxt is None and pi + 1 < len(pages):         # the break ends the page: the paragraph tops the next one
                body = [x for x in pages[pi + 1] if x.strip()]
                nxt, pg, mg = (body[1] if len(body) > 1 else None), pi + 1, margin(pages[pi + 1])
            if nxt is None or mg is None:
                continue
            if lead(nxt) < mg + 2:
                bad.append((pg + 1, nxt.strip()[:60]))
    return bad, seen


def cmd_pdf(a):
    bad, seen = scene_break_indents(a.pdf)
    for pg, t in bad[:20]:
        print("page %d: no indent after the break: %s" % (pg, t))
    print("%d scene breaks; %d followed by a paragraph with no indent" % (seen, len(bad)))
    sys.exit(1 if bad or not seen else 0)


# ---------------------------------------------------------------- self-test: CT's own catches, before and after
def _book(tmp, chapters):
    """A small book in v6.txt's shape. chapters: [(number, title, [scene, ...])], a scene being a list of paragraphs."""
    lines = ["Chapter 0: Contents line", "", "Chapter 0: Nothing", "Nothing happens here.", "", "Act One: The Bar"]
    for n, title, scs in chapters:
        lines.append("Chapter %d: %s" % (n, title))
        for i, sc in enumerate(scs):
            if i:
                lines.append("")
            lines += sc
    lines += ["About This Book", "The end."]
    p = os.path.join(tmp, "v6.txt")
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    return Book(p)


def cmd_selftest(a):
    import tempfile
    tmp = tempfile.mkdtemp()
    ok, bad = [], []

    def expect(name, cond):
        (ok if cond else bad).append(name)

    filler = ["The valley was quiet that week.", "Rain came on the third night and the creek rose.",
              "Nobody at the table said much about it."]
    # he: the opening of Chapter 13 as CT read it on 28 Nov
    before = ["In the morning the fever was down enough to drive. He decided not to go to the hospital. He was tough. He could tough it out.",
              "He left the lot with the windows down and the heater on, because he couldn't get warm. He had a quarter tank and no money. Home was two hours north. He got as far as a side street in downtown Stockton and turned the truck off.",
              "When he woke up it was Monday. He had slept in the truck all night, sitting up, with his jacket over him. The first thing he did was reach for the phone. It was dead.",
              "He needed a charge. He started the truck, plugged the phone into the lighter, and sat there with the engine running and the needle on a quarter tank."]
    b = _book(tmp, [(13, "The Buckets in the Barn", [before + ["The buckets were in the barn."]])])
    he = check_he(b)
    expect("he: the Chapter 13 opening is flagged", any("He decided not to go" in x["text"] for x in he))
    expect("he: 'He needed a charge. He started the truck' is flagged", any("He started the truck" in x["text"] for x in he))
    expect("he: 'He started the truck ...' is tagged a step", tag(before[3].split(". ", 1)[1]) == "step")
    fixed = "The truck started up without issue, which pleased Elijah and gave him a sense of relief."
    expect("he: CT's line is tagged texture", tag(fixed) == "texture")
    after = before[:3] + ["He needed a charge. " + fixed + " He plugged the phone into the lighter and sat there with the engine running."]
    b = _book(tmp, [(13, "The Buckets in the Barn", [filler + after[2:] + ["The buckets were in the barn."]])])
    expect("he: with CT's line in, that paragraph is no longer flagged", not any("He needed a charge" in x["text"] for x in check_he(b)))
    b = _book(tmp, [(13, "The Buckets in the Barn", [["He said his mother had had a stroke. He said what a room cost. He said he didn't know how to ask.", "The buckets were in the barn."]])])
    expect("he: 'He said ... He said ... He said' is marked maybe on purpose", any(x["maybe"] for x in check_he(b)))
    # word: "people", Chapter 0, before and after "Folks"
    people = ("Wes and his flyers. People for whom the economy was already a rigged carnival game. %s with no margin, no cushion, "
              "no lobbyist, the first people every wave hits and the last people anyone rebuilds for.")
    b = _book(tmp, [(11, "A Rigged Game", [[people % "People", "The game was rigged."]])])
    w = check_word(b)
    expect("word: 'people' four times in a paragraph", any('"people" 4' in x["what"] for x in w))
    expect("word: two sentences in a row open with 'People'", any("open with" in x["what"] for x in w))
    b = _book(tmp, [(11, "A Rigged Game", [[people % "Folks", "The game was rigged."]])])
    expect("word: not after 'Folks'", not check_word(b))
    # speaker: the Gus line, before and after
    gus = ["Elijah wrote the question down. Gus glanced over and didn't say anything.", '"So what do you do with it?"',
           '"I\'ve got a museum," Gus said.']
    b = _book(tmp, [(11, "The Museum", [gus])])
    expect("speaker: the untagged line after 'Elijah ... Gus ...'", any("Elijah and Gus" in x["what"] for x in check_speaker(b)))
    gus[1] = '"So what do you do with it?" Elijah asked.'
    b = _book(tmp, [(11, "The Museum", [gus])])
    expect("speaker: not once it says 'Elijah asked'", not check_speaker(b))
    b = _book(tmp, [(11, "The Museum", [['"One."', '"Two."', '"Three."', '"Four."', '"Five."', '"Six."', "Gus laughed at the museum."]])])
    expect("speaker: six untagged lines in a row", any("6 lines" in x["what"] for x in check_speaker(b)))
    # title
    b = _book(tmp, [(12, "The Seventeen-Dollar Shower", [["He paid for the room.", "It was seventeen goddamn dollars."]])])
    expect("title: a title word missing from the chapter", any("shower" in x["what"] for x in check_title(b)))
    b = _book(tmp, [(12, "The Seventeen-Dollar Shower", [["The shower was seventeen dollars.", "He stood in the shower.", "The shower ran gray.", "Seventeen dollars, he thought."]])])
    expect("title: not when the words are there", not check_title(b))
    # opener
    b = _book(tmp, [(11, "The Pump", [["The pump kept ticking. The radiator clicked against the wall. The machine went on drafting.", "The pump was fine."]])])
    expect("opener: 'The ... The ... The'", len(check_opener(b)) == 1)
    b = _book(tmp, [(11, "The Pump", [["The job. The friends. The rooms.", "The pump was fine."]])])
    expect("opener: a list is marked maybe on purpose", bool(check_opener(b)[0]["maybe"]))
    # mechanics
    b = _book(tmp, [(11, "The Pump", [["He put the the pump down , slowly.", '"It runs," she said. "It runs', "The pump was fine \u2014 mostly.", "The pump was fine."]])])
    m = " | ".join(x["what"] for x in check_mechanics(b))
    for want in ("doubled word", "space before punctuation", "odd number of quotation marks", "em or en dash"):
        expect("mechanics: " + want, want in m)
    b = _book(tmp, [(11, "The Pump", [["She had had enough of the pump.", "you probably want to lock your journal, brother", "The pump was fine."]])])
    expect("mechanics: nothing on clean lines, 'had had', or a text message", not check_mechanics(b))
    for n in ok:
        print("ok    " + n)
    for n in bad:
        print("FAIL  " + n)
    print("%d of %d pass" % (len(ok), len(ok) + len(bad)))
    sys.exit(1 if bad else 0)



def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("run"); p.add_argument("book"); p.add_argument("read", nargs="?"); p.add_argument("--from", dest="first", type=int, default=FIRST); p.set_defaults(f=cmd_run)
    p = sp.add_parser("batch"); p.add_argument("book"); p.add_argument("read", nargs="?"); p.add_argument("--check", required=True, choices=CHECKS)
    p.add_argument("--from", dest="first", type=int, default=FIRST); p.add_argument("--size", type=int, default=6)
    p.add_argument("--skip", type=int, default=0); p.add_argument("--all", action="store_true")
    p.add_argument("--worst", action="store_true", help="heaviest first, not book order"); p.set_defaults(f=cmd_batch)
    p = sp.add_parser("titles"); p.add_argument("book"); p.add_argument("--from", dest="first", type=int, default=FIRST); p.set_defaults(f=cmd_titles)
    p = sp.add_parser("show"); p.add_argument("book"); p.add_argument("id"); p.add_argument("--from", dest="first", type=int, default=FIRST); p.set_defaults(f=cmd_show)
    p = sp.add_parser("mark"); p.add_argument("id"); p.add_argument("--verdict", required=True); p.add_argument("--edit", default="")
    p.add_argument("--note", default=""); p.set_defaults(f=cmd_mark)
    p = sp.add_parser("gate"); p.add_argument("book"); p.add_argument("--from", dest="first", type=int, default=FIRST); p.set_defaults(f=cmd_gate)
    p = sp.add_parser("pdf"); p.add_argument("pdf"); p.set_defaults(f=cmd_pdf)
    p = sp.add_parser("selftest"); p.set_defaults(f=cmd_selftest)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
