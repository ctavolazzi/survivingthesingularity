"""Preflight for the manuscript: is the Doc clean enough for the author's final pass?

Usage: python3 -I preflight.py READ.json [group ...]
Groups: state structure type spelling names numbers threads. Default: all.
READ.json is a saved read_doc of the current manuscript (read it with commentsIncluded if you can).
Read-only. Every check prints a count and a few examples; a control at the end shows the
checks can fail.
"""
import collections
import json
import re
import sys

doc = json.load(open(sys.argv[1]))["content"]
groups = sys.argv[2:] or ["all"]
want = lambda g: "all" in groups or g in groups
tab = doc["tabs"][0]["documentTab"]
body = tab["body"]["content"]

P = []  # every paragraph: text as it stands, style, section, fonts
sec, mw, in_contents = None, 0, False
for el in body:
    p = el.get("paragraph")
    if not p:
        if "table" in el:
            P.append({"text": "", "style": "TABLE", "sec": sec, "img": 0, "fonts": set(), "sizes": set(), "sugg": 0, "align": None, "italic": False})
        continue
    text, img, fonts, sizes, sugg, ital_runs, runs = "", 0, set(), set(), 0, 0, 0
    for e in p["elements"]:
        if "inlineObjectElement" in e:
            img += 1
        tr = e.get("textRun")
        if not tr:
            continue
        if tr.get("suggestedInsertionIds") or tr.get("suggestedDeletionIds"):
            sugg += 1
        if tr.get("suggestedInsertionIds"):
            continue
        text += tr["content"]
        ts = tr.get("textStyle", {})
        if tr["content"].strip():
            runs += 1
            ital_runs += bool(ts.get("italic"))
            if ts.get("weightedFontFamily"):
                fonts.add(ts["weightedFontFamily"].get("fontFamily"))
            if ts.get("fontSize"):
                sizes.add(ts["fontSize"].get("magnitude"))
    text = text.rstrip("\n")
    style = p["paragraphStyle"].get("namedStyleType", "")
    if style == "HEADING_1":
        t = text.strip()
        in_contents = t == "Contents"
        if t == "Meanwhile":
            mw += 1
            sec = "meanwhile%d" % mw
        elif t.startswith("Act "):
            sec = "act"
        elif re.match(r"Chapter\s+(\d+)", t):
            sec = "ch%02d" % int(re.match(r"Chapter\s+(\d+)", t).group(1))
        elif t.startswith("Author"):
            sec = "authors-note"
        elif t.startswith("Afterword"):
            sec = "afterword"
        elif t.startswith("Appendix"):
            sec = "appendix"
        elif in_contents:
            sec = "contents"
        else:
            sec = "front"
    P.append({"text": text, "style": style, "sec": sec, "img": img, "fonts": fonts, "sizes": sizes, "sugg": sugg,
              "align": p["paragraphStyle"].get("alignment"), "italic": runs > 0 and ital_runs == runs})

STORY = [k for k in dict.fromkeys(x["sec"] for x in P) if k and (k.startswith(("ch", "meanwhile")) or k in ("authors-note", "afterword", "appendix"))]
# captions: the centered italic line right after a picture
for i, x in enumerate(P):
    x["caption"] = i > 0 and P[i - 1]["img"] > 0 and x["style"] != "HEADING_1"
prose = [x for x in P if x["sec"] in STORY and x["style"] != "HEADING_1" and x["text"].strip() and not x["caption"]]
BOOK = "\n".join(x["text"] for x in prose)
FICTION = "\n".join(x["text"] for x in prose if x["sec"].startswith(("ch", "meanwhile")))


def ex(hits, n=5, w=150):
    return "".join("\n      %s: %s" % (s, t[:w].replace("\n", " ")) for s, t in hits[:n])


def scan(label, pat, flags=0, n=5, texts=None, keep=None):
    hits = []
    for x in (texts or prose):
        for m in re.finditer(pat, x["text"], flags):
            if keep and not keep(m, x):
                continue
            hits.append((x["sec"], x["text"][max(0, m.start() - 55):m.end() + 55]))
    print("  %-46s %4d%s" % (label, len(hits), ex(hits, n) if hits else ""))
    return len(hits)


if want("state"):
    print("== STATE")
    words = sum(len(x["text"].split()) for x in prose)
    print("  title: %s | revision %s" % (doc["title"], doc["revisionId"][:14]))
    print("  sections: %d | words of text: %d | pictures: %d | captions: %d" % (len(STORY), words, sum(x["img"] for x in P), sum(1 for x in P if x["caption"])))
    print("  suggestions still waiting in the text: %d paragraphs" % sum(1 for x in P if x["sugg"]))
    recs = doc.get("suggestions") or []
    print("  suggestion records: %s" % dict(collections.Counter(r.get("status") for r in recs)))
    com = doc.get("comments")
    print("  comments in the read: %s" % ("not included in this read" if com is None else "%d (%s)" % (len(com), dict(collections.Counter(c.get("status") for c in com)))))

if want("structure"):
    print("\n== STRUCTURE")
    heads = [x["text"].strip() for x in P if x["style"] == "HEADING_1"]
    chap = [h for h in heads if h.startswith("Chapter ")]
    nums = [int(re.match(r"Chapter (\d+)", h).group(1)) for h in chap]
    print("  chapters: %d, numbered %d to %d, in order and none missing: %s" % (len(nums), min(nums), max(nums), nums == list(range(0, 40))))
    print("  headings in order: %s" % (" > ".join(re.sub(r"Chapter (\d+).*", r"\1", h)[:10] for h in heads)))
    contents = [x["text"].strip() for x in P if x["sec"] == "contents" and x["style"] != "HEADING_1" and x["text"].strip()]
    body_heads = [h for h in heads if h not in ("Contents",) and not h.startswith("SURVIVING")]
    print("  contents page lines: %d | headings in the body: %d | same list, same order: %s" % (len(contents), len(body_heads), contents == body_heads))
    for a, b in zip(contents, body_heads):
        if a != b:
            print("      contents says %r, heading says %r" % (a, b))
            break
    other = collections.Counter(x["style"] for x in P)
    print("  paragraph styles: %s" % dict(other))
    print("  headings with no text: %d | pictures with no caption after them: %d" % (sum(1 for x in P if x["style"].startswith("HEADING") and not x["text"].strip()), sum(1 for i, x in enumerate(P) if x["img"] and not (i + 1 < len(P) and P[i + 1]["caption"] and P[i + 1]["text"].strip()))))
    empties, run, worst = 0, 0, 0
    for x in P:
        if x["sec"] in STORY and not x["text"].strip() and not x["img"]:
            empties += 1
            run += 1
            worst = max(worst, run)
        else:
            run = 0
    print("  empty paragraphs inside the book: %d (longest run %d)" % (empties, worst))
    fonts = collections.Counter(f for x in prose for f in x["fonts"])
    sizes = collections.Counter(s for x in prose for s in x["sizes"])
    print("  fonts set by hand on runs: %s | sizes set by hand: %s" % (dict(fonts) or "none", dict(sizes) or "none"))
    odd = [(x["sec"], x["text"]) for x in prose if x["style"] not in ("NORMAL_TEXT",)]
    print("  body paragraphs not in the normal style: %d%s" % (len(odd), ex(odd, 4)))
    lens = collections.OrderedDict()
    for x in prose:
        lens[x["sec"]] = lens.get(x["sec"], 0) + len(x["text"].split())
    srt = sorted(lens.items(), key=lambda kv: -kv[1])
    print("  longest sections: %s" % ", ".join("%s %d" % kv for kv in srt[:5]))
    print("  shortest chapters: %s" % ", ".join("%s %d" % kv for kv in [kv for kv in srt if kv[0].startswith("ch")][-4:]))

if want("type"):
    print("\n== TYPOGRAPHY AND LEFTOVERS")
    scan("en or em dash", "[\u2013\u2014]")
    scan("double space inside a line", r"\S  +\S")
    scan("space before , . ; : ! ?", r"\s[,.;:!?](?:\s|$)")
    scan("no space after a sentence end", r"[a-z][.!?][A-Z][a-z]", keep=lambda m, x: not re.search(r"\b(a\.m|p\.m|U\.S|e\.g|i\.e)", x["text"][max(0, m.start() - 4):m.end()]))
    scan("no space after a comma", r",[A-Za-z]")
    scan("word repeated back to back", r"\b([A-Za-z']+) \1\b", keep=lambda m, x: m.group(1).lower() not in ("had", "that", "no", "so", "very", "ha", "bye", "now", "her", "take", "modeled", "yeah", "well", "okay", "go", "wait", "down", "me", "out", "on", "in"))
    sq, cq = len(re.findall('"', BOOK)), len(re.findall("[\u201c\u201d]", BOOK))
    sa, ca = len(re.findall(r"\w'\w", BOOK)), len(re.findall("\\w\u2019\\w", BOOK))
    print("  %-46s straight %d, curly %d" % ("double quotation marks", sq, cq))
    print("  %-46s straight %d, curly %d" % ("apostrophes", sa, ca))
    if cq:
        scan("  paragraphs with curly quotes", "[\u201c\u201d]", n=6)
    if ca:
        scan("  paragraphs with curly apostrophes", "\\w\u2019\\w", n=6)
    scan("three dots typed as dots", r"\.\.\.")
    scan("odd number of quote marks in a paragraph", r"^.*$", flags=re.S, keep=lambda m, x: x["text"].count('"') % 2 == 1, n=8)
    scan("paragraph ends without . ! ? \" or …", r"^.*$", flags=re.S, n=10, keep=lambda m, x: x["sec"] != "appendix" and len(x["text"].split()) > 6 and not re.search(r"[.!?\"\u2026:)\u201d']$", x["text"].rstrip()) and not x["italic"])
    scan("paragraph starts with a small letter", r"^[a-z]", n=10, keep=lambda m, x: not x["italic"])
    scan("placeholder or note left in", r"\[[^\]]{0,80}\]|\bTODO\b|\bTK\b|\bXXX\b|Open for v4|\bFIXME\b|lorem|INSERT|\?\?\?")
    scan("markdown or code marks", r"\*\*|__|^#+ |</?[a-z]+>|```|https?://", flags=re.M, keep=lambda m, x: x["sec"] not in ("authors-note", "afterword"))
    scan("banned word", r"manifesto", flags=re.I)
    scan("OK instead of okay", r"\bOK\b|\bOk\b")
    scan("grey", r"\bgr[e]y\b", flags=re.I)
    scan("alright", r"\balright\b", flags=re.I)
    scan("t-shirt in lower case", r"\bt-shirt\b")
    scan("digits where the book spells numbers out (1 to 9)", r"(?<![\d:$.,#/-])\b[1-9]\b(?![\d:.,%/-]|\s*(a\.m|p\.m|cm|percent|x\b))", n=8, keep=lambda m, x: x["sec"].startswith(("ch", "meanwhile")))
    dup = collections.Counter(x["text"] for x in prose if len(x["text"].split()) >= 9)
    d2 = [(next(y["sec"] for y in prose if y["text"] == t), t) for t, c in dup.items() if c > 1]
    print("  %-46s %4d%s" % ("same paragraph twice (9+ words)", len(d2), ex(d2, 6)))

if want("spelling"):
    print("\n== SPELLING (words not in the system dictionary that appear once or twice)")
    try:
        words = set(w.strip().lower() for w in open("/usr/share/dict/words", encoding="utf-8", errors="ignore"))
    except OSError:
        words = set()
    if not words:
        print("  no system dictionary found; skipped")
    else:
        def known(w):
            w = w.lower()
            if w in words:
                return True
            for suf, rep in (("'s", ""), ("s", ""), ("es", ""), ("ed", ""), ("ed", "e"), ("d", ""), ("ing", ""), ("ing", "e"), ("ies", "y"), ("ied", "y"), ("er", ""), ("er", "e"), ("est", ""), ("ly", ""), ("n't", ""), ("'d", ""), ("'ll", ""), ("'ve", ""), ("'re", ""), ("ier", "y"), ("iest", "y"), ("ily", "y"), ("ness", ""), ("less", ""), ("ful", ""), ("ers", ""), ("ings", ""), ("ment", ""), ("able", ""), ("able", "e")):
                if w.endswith(suf) and (w[: len(w) - len(suf)] + rep) in words:
                    return True
            for suf in ("ped", "ping", "ted", "ting", "ned", "ning", "bed", "bing", "ged", "ging", "med", "ming", "red", "ring", "led", "ling", "ded", "ding"):
                if w.endswith(suf) and w[: len(w) - len(suf) + 1] in words:
                    return True
            return False

        toks = re.findall(r"[A-Za-z][A-Za-z'\u2019]*[A-Za-z]|[A-Za-z]", FICTION.replace("\u2019", "'"))
        low = collections.Counter(t.lower() for t in toks)
        capped = collections.Counter(t for t in toks if t[0].isupper())
        lower_seen = set(t for t in toks if t[0].islower())
        unknown = []
        for w, c in low.items():
            if c > 2 or len(w) < 4 or known(w):
                continue
            if "-" in w or (w.capitalize() in capped and w not in lower_seen):
                continue  # a name
            unknown.append(w)
        unknown.sort()
        print("  %d candidates:" % len(unknown))
        line = "    "
        for w in unknown:
            if len(line) + len(w) > 150:
                print(line)
                line = "    "
            line += w + "  "
        print(line)

if want("names"):
    print("\n== NAMES")
    toks = re.findall(r"(?<![.!?\"\u201c] )(?<!^)\b[A-Z][a-z]{2,}(?:[A-Z][a-z]+)?\b", FICTION, flags=re.M)
    c = collections.Counter(toks)
    names = [w for w, n in c.items() if n >= 1]

    def near(a, b):
        if a == b or abs(len(a) - len(b)) > 1 or a[0] != b[0] or min(len(a), len(b)) < 5:
            return False
        if len(a) == len(b):
            return sum(x != y for x, y in zip(a, b)) == 1
        s, l = (a, b) if len(a) < len(b) else (b, a)
        return any(l[:i] + l[i + 1:] == s for i in range(len(l)))

    pairs = sorted({tuple(sorted((a, b))) for a in names for b in names if near(a, b) and not (a + "s" == b or b + "s" == a)})
    print("  names one letter apart (possible misspellings): %d" % len(pairs))
    for a, b in pairs:
        print("      %s (%d)  /  %s (%d)" % (a, c[a], b, c[b]))
    for label, pat in (("PorusAI spelled another way", r"Porous ?AI|Porus AI|PorousAI"), ("Gaelen spelled Galen", r"\bGalen\b"), ("Czekaj or Nadzieja spelled another way", r"Nadz[a-z]*\b(?<!Nadzieja)|Cz[a-z]*j\b(?<!Czekaj)"), ("Okonkwo, Kowalski, Cudworth spelled another way", r"\bOkonk(?!wo\b)\w+|\bKowals(?!ki\b)\w+|\bCudw(?!orth\b)\w+"), ("Second Crop / Fisher / Groundwork (old names)", r"Second Crop|\bFisher\b|Groundwork")):
        scan(label, pat)
    first = collections.OrderedDict()
    for x in prose:
        if not x["sec"].startswith(("ch", "meanwhile")):
            continue
        for n in ("Grace", "Marta", "Denny", "Lou", "Curtis", "Priya", "Reuben", "Frank", "Tyler", "Patricia", "Wren", "Irene", "Rosa", "Ruby", "Gus", "Trent", "Melody", "Faith", "Greg Holt", "Marianne", "Manny", "Devendra", "Bidwell", "Nadzieja"):
            if n not in first and re.search(r"\b%s\b" % n, x["text"]):
                first[n] = x["sec"]
    print("  first appearance: " + ", ".join("%s %s" % kv for kv in first.items()))

if want("numbers"):
    print("\n== NUMBERS THAT MUST AGREE")
    def variants(label, pat, group=1, flags=re.I):
        c = collections.Counter()
        where = collections.defaultdict(set)
        for x in prose:
            for m in re.finditer(pat, x["text"], flags):
                v = m.group(group).lower()
                c[v] += 1
                where[v].add(x["sec"])
        print("  %-34s %s" % (label, "; ".join("%s x%d (%s)" % (v, n, ",".join(sorted(where[v]))[:44]) for v, n in c.most_common()) or "none"))
    num = r"((?:[a-z]+-)?[a-z]+|\d[\d,]*)"
    variants("households", num + r" households")
    variants("Irene's acres", num + r" acres")
    variants("the amp's weight", num + r" pounds")
    variants("the lamp's price a month", r"(twenty-nine|\$?\d+)(?: dollars)? a month")
    variants("parcels", num + r" parcels")
    variants("boxes on the route", r"(a hundred and forty|\d+|[a-z]+-?[a-z]*) boxes")
    variants("the Sunday call time", r"\b(\d{1,2}:\d\d)\b(?= (?:that |on |every )?(?:Sunday|on Sunday)|, when her day)")
    variants("times of day used", r"\b(\d{1,2}:\d\d)\b")
    variants("years named", r"\b((?:19|20)\d\d)\b")
    variants("stated ages", r"\b((?:thirty|twenty|nineteen|sixty|fifty|forty|seventy)(?:-[a-z]+)?)(?: years old|-year-old)")
    variants("Elijah's age", r"(?:He|Elijah) was (thirty-[a-z]+)\b")
    variants("notebooks", num + r" notebooks")
    variants("copies of the book", num + r" copies")
    variants("stages", r"\b(five|six|seven|eight|nine) stages")
    variants("miles to Ma", r"(eight hundred|three hundred|\d+) miles")
    variants("the price of a beer", r"(four|five|six|seven) dollars|(?:it's|It's) (six|seven|five) now", group=0)
    variants("cups on the curb", r"((?:three |a )?hundred)(?: fucking)? cups")

if want("threads"):
    print("\n== THREADS (new or changed on 23 November): where each one appears")
    def where(label, pat, flags=re.I):
        c = collections.OrderedDict()
        for x in prose:
            n = len(re.findall(pat, x["text"], flags))
            if n:
                c[x["sec"]] = c.get(x["sec"], 0) + n
        print("  %-30s %s" % (label, " ".join("%s:%d" % kv for kv in c.items()) or "NOWHERE"))
    where("the two robot arms", r"robot arms?|\bthe arms\b|\bthe crates\b")
    where("lien sale / storage unit", r"lien sale|storage (place|unit)|the unit\b")
    where("the leather pouch", r"leather pouch|\bthe pouch\b")
    where("set list folded in quarters", r"folded (it )?in quarters")
    where("the truck song", r"truck song")
    where("porch light", r"porch light")
    where("Faith (Grace's sister)", r"\bFaith\b", flags=0)
    where("Grace's father", r"(Grace's|her|my|your) (dad|father)\b|Loudbox guy")
    where("Melody / grub", r"\bMelody\b|\bgrub\b")
    where("Greg Holt / who started the place", r"Greg Holt|started (the|this) place|first roster")
    where("Curtis and the movies", r"\bmovies?\b|Skynet|Matrix|Judgment Day")
    where("it leaves (Stage 7)", r"\bIt leaves\b|just leave\?|does not leave|hadn't left")
    where("college / professor / Thoreau", r"\bcollege\b(?! with| program)|\bprofessor\b|Thoreau")
    where("what's a job for", r"What's a job for|what's it for")
    where("people land where they put", r"land where they put themselves")
    where("your money's no good here", r"money's no good here")
    where("free beer / four dollars / six now", r"free beer|four dollars|six now|four ones")
    where("I love you / said it back", r"I love you|said it back|say it back")
    where("Ruby's number", r"Ruby's number|one number he could have called|to Don't")
    where("ALC", r"\bALC\b|[Aa]dequate level of care")
    where("Trent", r"\bTrent\b", flags=0)
    where("supervisor (should be none)", r"supervisor")
    where("the watcher", r"somebody near him|put somebody near")
    where("Sparrow", r"\bSparrow\b", flags=0)
    where("Ardell / Washington", r"\bArdell\b|\bWashington\b", flags=0)
    where("three hours (old distance)", r"three hours")

print("\n== CONTROL: these checks can fail")
bad = "He said  it \u2014 OK ,then.He left."
print("  on a planted bad line:", {"dash": bool(re.search("[\u2013\u2014]", bad)), "double space": bool(re.search(r"\S  +\S", bad)), "OK": bool(re.search(r"\bOK\b", bad)), "space before comma": bool(re.search(r"\s[,.;:!?]", bad)), "no space after period": bool(re.search(r"[a-z][.!?][A-Z][a-z]", bad))})
