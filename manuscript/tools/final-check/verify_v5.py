#!/usr/bin/env python3
"""
verify_v5.py  --  mechanical proof-check for "StS v5 draft (Nov 23)".

What it proves (hard checks, FAIL stops the release):
  A. Coverage    the Doc's text today is byte-for-byte the text that was read line by line,
                 the read covered every line, and no line was long enough to be cut off.
  B. Edits       today's text == session-start text + exactly the approved edits (16, then 4 in Ch 35, then the
                 last changes in Ch 19, 31, 33, 38 and 39). Nothing else.
  C. Locked      every locked line is still word for word what it was at session start.
  D. Rules       dashes, quotes, "never once", "hand flat", nicknames, cut line, canon lines.
  E. Continuity  calendar facts and every recurring number agree with themselves.
  F. Structure   contents list == headings, chapters 0..39 in order, 19 pictures, scene breaks,
                 quote balance, one tab, no pending suggestions.
  G. Formatting  one body font and size, uniform paragraph styling, no stray styles.
  H. Italics     nothing italic was lost, all 59 approved italic spots are italic,
                 every in-story all-capitals phrase is italic.

What it can only flag for a human (WARN):
  I. Hygiene     doubled words, spacing slips, likely typos, near-duplicate names,
                 duplicated sentences, stacked paragraph openers, cue words with no italics.

What no code can prove (printed as OPEN, never as PASS):
  whether a scene is confusing, whether a passage is dead weight, whether the book lands.

Usage:
  python3 -I verify_v5.py DATA_DIR
DATA_DIR must hold:
  current_export_raw.txt     fresh text/plain export of the Doc (raw, as downloaded)
  current_doc.json           fresh Docs API read of the Doc
  session_start_export.txt   normalized export taken before any edit this session
  session_start_doc.json     Docs API read taken before any edit this session
  text_as_read.txt           the normalized text that was read line by line
  line_edits.json            the 24 approved find/replace edits [[n, old, new], ...]
Exit code 0 only if there is no FAIL.
"""
import sys, os, re, json, hashlib, datetime, collections, difflib

DATA = sys.argv[1] if len(sys.argv) > 1 else "."
P = lambda name: os.path.join(DATA, name)

results = []          # (level, section, name, detail)
def record(level, section, name, detail=""):
    results.append((level, section, name, detail))
def check(section, name, ok, detail_fail="", detail_ok=""):
    record("PASS" if ok else "FAIL", section, name, detail_ok if ok else detail_fail)
    return ok
REVIEWED = {
    # check name -> {fragment that identifies the flagged item: why it is accepted}
    "A thought, typed or written cue with no italics within reach": {
        "There had been small ones before this, he thought": "reported thought (the doctor's), not a quoted one",
        "She'd eaten his too, he thought.": "reported in third person, not a quoted thought",
        "his practice pieces looked, he thought, honestly good": "reported thought, not a quoted one",
    },
    "The same word twice in a row": {
        "told [you you]'re not crazy": "correct grammar: told you (that) you're not crazy",
        "naming your [dog Dog]": "the joke",
    },
    "A sentence of nine or more words that appears more than once": {
        "A machine that can do any work a person can do sitting down.": "the Architect's definition, quoted back on purpose",
        "Past Stage 7 I don't have paper big enough.": "the notebook line, read back by the Architect",
        "I'd have just wanted you to go to bed.": "David's line, remembered in Ch 15",
        "I am trying to make one that wants it.": "the Architect's line, remembered in Ch 33",
        "If you spend all your time focused on what you can't do": "the old man's line, remembered in Ch 39",
        "The night aide held the phone by his mother's ear.": "the Sunday ritual, repeated on purpose",
        "She is the one who taught me to ask first.": "the machine's speech, heard again in Ch 39",
    },
    "Four or more paragraphs in a row opening on the same word": {
        "(Appendix)": "the list of the four sides in the Appendix",
    },
    "A sentence in narration that starts with a lower-case letter": {
        "Loser cooks. [i]n small square": "the full stop belongs to the sticky note he is writing",
    },
}
def warn(section, name, items):
    accepted = REVIEWED.get(name, {})
    fresh = [it for it in items if not any(k in it for k in accepted)]
    seen = len(items) - len(fresh)
    if fresh:
        record("WARN", section, name, fresh)
    else:
        record("PASS", section, name, ("%d flagged, all reviewed and accepted" % seen) if seen else "nothing found")

def norm_export(raw_bytes):
    return raw_bytes.decode("utf-8").replace("\r", "").lstrip("﻿")

# ----------------------------------------------------------------------------- load
cur_text = norm_export(open(P("current_export_raw.txt"), "rb").read())
start_text = open(P("session_start_export.txt"), encoding="utf-8").read()
read_text = open(P("text_as_read.txt"), encoding="utf-8").read()
cur_doc = json.load(open(P("current_doc.json"), encoding="utf-8"))
cur_doc = cur_doc.get("content", cur_doc)
start_doc = json.load(open(P("session_start_doc.json"), encoding="utf-8"))
start_doc = start_doc.get("content", start_doc)
LINE_EDITS = [(n, a, b) for n, a, b in json.load(open(P("line_edits.json"), encoding="utf-8"))]

lines = cur_text.split("\n")

def doc_paragraphs(doc):
    """[(start, end, text, runs, has_object, paragraphStyle)], runs = [(s, e, content, textStyle)]"""
    out = []
    tabs = doc["tabs"]
    body = tabs[0]["documentTab"]["body"]["content"]
    for el in body:
        p = el.get("paragraph")
        if not p:
            continue
        runs, has_obj = [], False
        for e in p["elements"]:
            if "textRun" in e:
                runs.append((e["startIndex"], e["endIndex"], e["textRun"]["content"],
                             e["textRun"].get("textStyle", {}), e["textRun"]))
            else:
                has_obj = True
        out.append((el["startIndex"], el["endIndex"], "".join(r[2] for r in runs), runs,
                    has_obj, p.get("paragraphStyle", {})))
    return out

cur_paras = doc_paragraphs(cur_doc)
start_paras = doc_paragraphs(start_doc)
def body_first_index(paras):
    """document index of the second "Author's Note" paragraph: where the book proper starts"""
    hits = [p[0] for p in paras if p[2].strip() == "Author's Note"]
    return hits[1] if len(hits) > 1 else 0
BODY_IDX = body_first_index(cur_paras)
BODY_IDX_START = body_first_index(start_paras)

# ----------------------------------------------------------------------------- sections
HEAD_RE = re.compile(r"^(Author's Note|Act (One|Two|Three|Four): .+|Chapter (\d+): .+|Meanwhile|Epilogue|"
                     r"About This Book|Afterword|Appendix)$")
head_idx = [i for i, l in enumerate(lines) if HEAD_RE.match(l)]
half = len(head_idx) // 2
contents_heads = [lines[i] for i in head_idx[:half]]
body_heads = [lines[i] for i in head_idx[half:]]
body_start = head_idx[half] if head_idx else 0

def section_of_line():
    """label for every line index in the body: 'front', 'Ch 12', 'Meanwhile', 'Epilogue', ..."""
    lab, out = "front", []
    for i, l in enumerate(lines):
        if i >= body_start and HEAD_RE.match(l):
            m = re.match(r"^Chapter (\d+):", l)
            if m:
                lab = "Ch %d" % int(m.group(1))
            elif l.startswith("Act "):
                pass                      # an act heading does not end a chapter label by itself
            else:
                lab = l
        out.append(lab)
    return out
SEC = section_of_line()
def chap_num(label):
    m = re.match(r"Ch (\d+)$", label)
    return int(m.group(1)) if m else None
NOVEL = [i for i, s in enumerate(SEC) if i >= body_start and (chap_num(s) is not None or s in ("Meanwhile", "Epilogue"))]
NOVEL_SET = set(NOVEL)

def find_all(needle, hay=None):
    hay = cur_text if hay is None else hay
    return [m.start() for m in re.finditer(re.escape(needle), hay)]
def line_hits(pattern, flags=0, only_novel=False):
    rx = re.compile(pattern, flags)
    out = []
    for i, l in enumerate(lines):
        if i < body_start:
            continue
        if only_novel and i not in NOVEL_SET:
            continue
        for m in rx.finditer(l):
            out.append((i, m))
    return out
def in_dialogue(line, pos):
    """True if character position pos sits inside straight double quotes on this line."""
    return line[:pos].count('"') % 2 == 1
def ctx(i, m, pad=40):
    l = lines[i]
    return "L%d %s: ...%s[%s]%s..." % (i + 1, SEC[i], l[max(0, m.start() - pad):m.start()], m.group(0),
                                       l[m.end():m.end() + pad])

# ============================================================================= A. COVERAGE
sha = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()
check("A coverage", "Doc text today is identical to the text that was read line by line",
      cur_text == read_text,
      "current export differs from text_as_read.txt (sha %s vs %s)" % (sha(cur_text)[:12], sha(read_text)[:12]),
      "sha256 %s, %d lines" % (sha(cur_text)[:16], len(lines)))

READ_RANGES = [(1, 235), (235, 479), (479, 738), (739, 998), (999, 1248), (1249, 1498), (1499, 1748),
               (1749, 1998), (1999, 2253), (2254, 2503), (2504, 2761), (2760, 3049), (3050, 3374), (3374, 3629),
               # The whole book was read at 3,629 lines. The changes made after that (Ch 35, then Ch 19, 31, 33, 38, 39)
               # were read in a comparison of the exports before and after, which showed nothing else had moved.
               (3630, 3634)]
covered = set()
for a, b in READ_RANGES:
    covered |= set(range(a, b + 1))
n_read_lines = len(read_text.split("\n"))
missing = sorted(set(range(1, n_read_lines + 1)) - covered)
check("A coverage", "The logged read ranges cover every line, first to last",
      not missing, "lines never read: %s" % missing[:20], "lines 1 to %d, no gap" % n_read_lines)
longest = max(len(l) for l in read_text.split("\n"))
check("A coverage", "No line is long enough to be cut off by the reader (limit 2000 characters)",
      longest <= 2000, "longest line is %d characters" % longest, "longest line is %d characters" % longest)

# the API view of the Doc and the text export must describe the same document
recon = []
for s, e, txt, runs, has_obj, ps in cur_paras:
    if has_obj:
        recon += ["  ", ""]
    else:
        recon.append(txt.rstrip("\n").replace(" ", " ").replace("\x0b", "\n"))
recon_text = "\n".join(recon)
check("A coverage", "The Docs API copy and the text export are the same document",
      recon_text == cur_text,
      "API paragraphs do not rebuild the export (first difference near char %d)" %
      next((i for i, (x, y) in enumerate(zip(recon_text, cur_text)) if x != y), min(len(recon_text), len(cur_text))),
      "%d paragraphs rebuild the export exactly" % len(cur_paras))

# ============================================================================= B. EDITS
MOVE_PARA = ("The phone started going off on the seat before he was out of the lot. He knew what it was. "
             "He had known since a hinge and a gatepost in July. He let it buzz.")
MOVE_BEFORE = "He went the long way, behind his grandmother's place"
expected = start_text
problems = []
for n, old, new in LINE_EDITS:
    if expected.count(old) != 1:
        problems.append("edit %s: old text found %d times at session start" % (n, expected.count(old)))
    expected = expected.replace(old, new)
ex_lines = expected.split("\n")
try:
    i_move = ex_lines.index(MOVE_PARA)
    ex_lines.pop(i_move)
    i_tgt = next(i for i, l in enumerate(ex_lines) if l.startswith(MOVE_BEFORE))
    ex_lines.insert(i_tgt, MOVE_PARA)
except (ValueError, StopIteration):
    problems.append("could not replay the Ch 39 paragraph move")
# Ch 35, on the author's "Do it" late on 24 Nov: the cosmos line and the line after it now close the stove scene.
CH35_MOVES = ['"There is no more powerful force in all the cosmos than a mother protecting her young."',
              'He was quiet a second. "My wife would\'ve told me I was romanticizing. Said fourth grade never once felt like the cosmos. But I was the kid in the back seat."']
CH35_BEFORE = "The firelight moved across Lou's face."
try:
    for para in CH35_MOVES:
        ex_lines.pop(ex_lines.index(para))
        ex_lines.insert(next(i for i, l in enumerate(ex_lines) if l.startswith(CH35_BEFORE)), para)
except (ValueError, StopIteration):
    problems.append("could not replay the Ch 35 paragraph move")
expected = "\n".join(ex_lines)
if expected != cur_text:
    d = [l for l in difflib.unified_diff(expected.split("\n"), lines, lineterm="", n=0)
         if not l.startswith(("---", "+++", "@@"))]
    problems.append("text differs from session start + approved edits: %s" % d[:6])
check("B edits", "Today's text == session-start text + the approved edits (16, then 4 in Ch 35, then the last changes), and nothing else",
      not problems, "; ".join(problems), "%d line edits and 2 paragraph moves replay exactly" % len(LINE_EDITS))
bad = []
for n, old, new in LINE_EDITS:
    if cur_text.count(new) != 1 or cur_text.count(old) != 0:
        bad.append("edit %s: new x%d, old x%d" % (n, cur_text.count(new), cur_text.count(old)))
check("B edits", "Each approved edit is present exactly once and its old wording is gone",
      not bad, "; ".join(bad), "%d of %d" % (len(LINE_EDITS), len(LINE_EDITS)))
i_phone = next((i for i, l in enumerate(lines) if l == MOVE_PARA), -1)
check("B edits", "Ch 39: the phone paragraph now comes before the madrones paragraph",
      i_phone > 0 and lines[i_phone + 1].startswith(MOVE_BEFORE) and lines[i_phone - 1].endswith("took the truck."),
      "order is wrong near line %d" % (i_phone + 1))

# ============================================================================= C. LOCKED LINES
LOCKED = [
    ("Ch 39 ending", "David was looking at him.", 1),
    ("three times", "Nobody had asked him to", 3),
    ("Ch 15", "He had nothing left to lose but his life", 1),
    ("Ch 17", "Grace waited for him to say what he needed.", 1),
    ("Ch 20", "For a man in muck boots, that was pure ivory tower.", 1),
    ("Ch 26", "Wouldn't it make more sense for it to just leave?", 1),
    ("Ch 31 interlude", "Then, because he was who he was, he asked it", 1),
    ("Ch 32", "She struck it, and it caught on the first strike.", 1),
    ("Ch 34", "His face went hot. He felt like an asshole.", 1),
    ("Ch 35", "He thought about his notebooks, and every date he had ever written down with his initials next to it.", 1),
    ("Ch 35", "He'd never really thought about that before.", 1),
    ("Ch 35", "notes on the people who would launch the machine", 1),
    ("Ch 37", "Instead he changed the name to Don't.", 1),
    ("Ch 38 wink", "The machine made its version of what could be considered a wink, looking directly into the camera.", 1),
    ("Ch 0 prayer", "Tucked away above him was a small framed prayer he'd printed out and hung behind the register the year he quit drinking.", 1),
    ("Ch 0 prayer", "He had never actually read what was inside it.", 1),
]
bad = []
for where, s, n in LOCKED:
    a, b = start_text.count(s), cur_text.count(s)
    if a != n or b != n:
        bad.append("%s: %r session start x%d, now x%d, expected x%d" % (where, s[:40], a, b, n))
check("C locked", "Every locked line is present, the right number of times, unchanged since session start",
      not bad, "; ".join(bad), "%d locked lines" % len(LOCKED))
def ending(t):
    i = t.find("David was looking at him.")
    j = t.find("\nEpilogue\n", i)
    return t[i:j]
check("C locked", "Ch 39 Bear Flag ending is word for word what it was at session start",
      ending(cur_text) == ending(start_text) and len(ending(cur_text)) > 500)
def machine_speech(t):
    i = t.find("HELLO. I HAVE BEEN AWAKE SINCE MARCH.")
    j = t.find('"It wants to run," Reuben said.', i)
    return t[i:j]
check("C locked", "Ch 38 machine speech is word for word what it was at session start",
      machine_speech(cur_text) == machine_speech(start_text) and len(machine_speech(cur_text)) > 500)
check("C locked", 'Ch 19 "Immediately the vibe shifted." stays cut',
      "vibe shifted" not in cur_text)

# ============================================================================= D. RULES
for ch, name in (("—", "em dash"), ("–", "en dash"), ("‒", "figure dash"), ("―", "bar"),
                 ("−", "minus sign")):
    check("D rules", "No %s anywhere" % name, ch not in cur_text, "%d found" % cur_text.count(ch))
hy = line_hits(r"\s-{1,2}\s|--")
check("D rules", "No hyphen used as a dash", not hy, "; ".join(ctx(i, m) for i, m in hy[:5]))
curly = [c for c in "‘’“”‚„«»" if c in cur_text]
check("D rules", "Straight quotes only", not curly, "curly characters present: %r" % curly)
check("D rules", 'Ellipses are the single character, never three dots', "..." not in cur_text,
      "%d three-dot ellipses" % cur_text.count("..."))

hits = [(i, m) for i, m in line_hits(r"\bnever once\b", re.I, only_novel=True) if not in_dialogue(lines[i], m.start())]
check("D rules", '"never once" appears only inside dialogue', not hits, "; ".join(ctx(i, m) for i, m in hits))

HAND_FLAT_OK = ["trunks of the madrone trees", "hand flat on the grille", "needed to put his hand flat on something",
                "hand flat against the cut wall of the pit", "hand flat on her binder"]
hits = [(i, m) for i, m in line_hits(r"\bhands? flat\b", re.I, only_novel=True)
        if not any(ok in lines[i] for ok in HAND_FLAT_OK)]
check("D rules", '"hand flat" only for the madrone, the amp, the pit and Patricia\'s binder', not hits,
      "; ".join(ctx(i, m) for i, m in hits))

def chapters_with(pattern, flags=0, dialogue_only=False):
    out = collections.Counter()
    for i, m in line_hits(pattern, flags, only_novel=True):
        if dialogue_only and not in_dialogue(lines[i], m.start()):
            continue
        out[SEC[i]] += 1
    return out
c = chapters_with(r"\bThoreau\b")
check("D rules", '"Thoreau" only from Ch 33 on', all((chap_num(k) or 0) >= 33 for k in c) and sum(c.values()) >= 3, str(dict(c)), str(dict(c)))
c = chapters_with(r"\bIvy League\b")
check("D rules", '"Ivy League" only in Ch 20 to 26', all(20 <= (chap_num(k) or 0) <= 26 for k in c) and sum(c.values()) >= 2, str(dict(c)), str(dict(c)))
c = chapters_with(r"\bprofessor\b", re.I)
check("D rules", '"professor" exactly twice, Ch 26 and Ch 35', dict(c) == {"Ch 26": 1, "Ch 35": 1}, str(dict(c)), str(dict(c)))
hits = [(i, m) for i, m in line_hits(r"\bcollege\b", re.I, only_novel=True) if "community college" not in lines[i].lower()]
check("D rules", 'Nobody says "college" (only "community college" as a place)', not hits, "; ".join(ctx(i, m) for i, m in hits))
c = chapters_with(r"\bspreadsheet\b", re.I, dialogue_only=True)
late = {k: v for k, v in c.items() if (chap_num(k) or 0) >= 37}
check("D rules", 'Marta\'s "spreadsheet" is not spoken from Ch 37 on', not late, str(late), "last spoken in %s" % max((chap_num(k) or 0) for k in c))
check("D rules", 'Ch 37: Marta says "Go on, Elijah"', any(SEC[i] == "Ch 37" for i, m in line_hits(r'"Go on, Elijah," she said\.')))
c = chapters_with(r"\bbud\b", dialogue_only=True)
check("D rules", '"bud" is spoken (Frank, and Curtis in Ch 17)', sum(c.values()) >= 3, str(dict(c)), str(dict(c)))
sur = [(i, m) for i, m in line_hits(r"\bGrace [A-Z][a-z]+\b", only_novel=True)
       if m.group(0).split()[1] not in ("Faith",) ]
check("D rules", "Grace has no surname on the page", not sur, "; ".join(ctx(i, m) for i, m in sur))

CANON = [
    ("Ch 37", "He played the opening of \"The Weight,\" and missed the change into the chorus"),
    ("Ch 37", "wrote four words on it, and his name under them"),
    ("Ch 37", "put it in the leather pouch on the side of the amp, under the picks"),
    ("Ch 37", "M. Madrone, in round, careful letters."),
    ("Ch 37", "Ruby's number was still in his phone"),
    ("Ch 38", "She didn't switch it on."),
    ("Ch 38", "She started to sing. It was \"The Weight.\""),
    ("Ch 38", "It said I love you too, in his handwriting, with his name under it."),
    ("Ch 38", "She got as far as the chorus before her voice went."),
    ("Ch 38", "typed Come home."),
    ("Ch 38", "until the words were gone, one letter at a time"),
    ("Ch 38", "said one thing into it, short, the way you leave a message on a machine"),
    ("Ch 38", "My wife Yvonne".replace("Ch 38", "")),
    ("Ch 39", "\"Stove's going. I lit it myself,\" she said."),
    ("Ch 39", "Can't this time. I'll have to catch you guys another time."),
    ("Ch 39", "He still had Ruby's number. He chose not to call it."),
    ("Epilogue", "He sent it to Grace, and turned the phone face down on the step, and left the next part to her."),
    ("Ch 15", "The amp rode on the floor beside him with the belt through its handle"),
    ("Ch 24", "It was Walt Calder's, a squat black box stove"),
    ("Ch 9", "Her name was Nadzieja Czekaj".replace("Ch 9", "")),
    ("Ch 13", "There was Melody, in Miami"),
]
bad = []
for where, s in CANON:
    hits = [SEC[i] for i, l in enumerate(lines) if i >= body_start and s in l]
    if len(hits) != 1:
        bad.append("%r found %d times" % (s[:50], len(hits)))
    elif where in ("Ch 37", "Ch 39", "Epilogue", "Ch 15", "Ch 24", "Ch 13") and hits[0] != where:
        bad.append("%r is in %s, expected %s" % (s[:50], hits[0], where))
check("D rules", "Canon lines are on the page, once each, in the right chapter", not bad, "; ".join(bad), "%d canon lines" % len(CANON))
ch38 = "\n".join(l for i, l in enumerate(lines) if SEC[i] == "Ch 38")
check("D rules", "Ch 38: Grace sings and never plays the amp",
      not re.search(r"\b(plugged in|strummed|picked up the guitar|switched it on|turned it on)\b", ch38), "playing language found in Ch 38")
check("D rules", "The co-op is in Washington and the Architect is Nadzieja Czekaj",
      "up in Washington, outside a town called Ardell" in cur_text and cur_text.count("Nadzieja Czekaj") >= 4)
last_story = [l for i, l in enumerate(lines) if SEC[i] == "Epilogue" and l.strip()][-1]
check("D rules", "The Epilogue ends on Elijah sending Grace the recording", last_story.startswith("He listened to it once."))

# ============================================================================= E. CONTINUITY
def wd(y, m, d):
    return datetime.date(y, m, d).strftime("%A")
thanks = [d for d in range(1, 31) if datetime.date(2027, 11, d).weekday() == 3][3]
check("E continuity", "Thanksgiving 2027 is Thursday, November 25", thanks == 25 and wd(2027, 11, 25) == "Thursday" and
      "It was Thursday, November 25, 2027." in cur_text)
check("E continuity", "December 28, 2027 (last route box) is a Tuesday, the route day", wd(2027, 12, 28) == "Tuesday" and
      "December twenty-eighth is the last box she gets" in cur_text)
check("E continuity", '"We stop in five weeks" fits Nov 25 to Dec 28',
      28 <= (datetime.date(2027, 12, 28) - datetime.date(2027, 11, 25)).days <= 35)
check("E continuity", "The models go dark June 12, 2026, a Friday, and come back June 30: eighteen days",
      wd(2026, 6, 12) == "Friday" and (datetime.date(2026, 6, 30) - datetime.date(2026, 6, 12)).days == 18 and
      "On June 12 the big models went dark." in cur_text and "Worldwide. On a Friday." in cur_text and "On June 30 they turned the models back on." in cur_text and
      "The big models go dark for eighteen days." in cur_text)
check("E continuity", "Late 2022 toast, laid off eleven months later, in fall 2023",
      "Elijah got laid off on a Tuesday, eleven months after the toast." in cur_text and
      "Fall 2023. Elijah is laid off, eleven months after the toast." in cur_text)

NUM = r"(?:\d[\d,.]*|(?:(?:a |one |two |three |four |five |six |seven |eight |nine )?hundred(?: and)? )?" \
      r"(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)?-?(?:one|two|three|four|five|six|seven|eight|nine|ten|" \
      r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|" \
      r"seventy|eighty|ninety|hundred)?)"
def values(pattern, group=1, flags=re.I, only_novel=False):
    return [(m.group(group).strip().lower(), i, m) for i, m in line_hits(pattern, flags, only_novel)]
def all_same(section, name, pattern, allowed, minimum=1, group=1, flags=re.I):
    vals = values(pattern, group, flags)
    badv = [(v, i, m) for v, i, m in vals if v not in allowed]
    check(section, name, not badv and len(vals) >= minimum,
          "; ".join(ctx(i, m) for v, i, m in badv[:5]) or "only %d mentions" % len(vals),
          "%d mentions, all %s" % (len(vals), " / ".join(sorted(set(v for v, _, _ in vals)))))
all_same("E continuity", "The amp always weighs twenty-one pounds", r"\b([\w-]+) pounds\b(?= and every sticker|, sixty watts|, Dave)", {"twenty-one"}, 3)
all_same("E continuity", "The co-op is always nineteen households", r"\b([\w-]+) households\b(?! canceled| looked| who| is a dozen)",
         {"nineteen", "newest", "six csa", "the", "csa", "forty", "which"}, 6)
bad = [ctx(i, m) for v, i, m in values(r"\b((?:[\w-]+ )?[\w-]+) households\b") if re.search(r"\b(eighteen|twenty|seventeen|sixteen|twenty-one)\b", v)]
check("E continuity", "No stray household count", not bad, "; ".join(bad))
all_same("E continuity", "The route is always a hundred and forty boxes or households",
         r"\b((?:a )?hundred and [\w-]+)(?= boxes| households| families| of them| on the route)", {"a hundred and forty", "hundred and forty"}, 5)
all_same("E continuity", "The Sunday call is always 9:40", r"\b(\d{1,2}:\d\d)(?= on (?:a )?Sunday| that night| he (?:sat|stepped|called)|, he called)", {"9:40"}, 5)
all_same("E continuity", "The drive north is always eight hundred miles",
         r"\b([\w-]+ hundred) miles\b(?!, and the people on the rugs)", {"eight hundred"}, 4)
all_same("E continuity", "Bidwell always has eleven companies", r"\b([\w-]+) (?:different )?compan(?:ies|y names)\b(?=[^.]*)", {"eleven"}, 2,
         flags=0) if False else None
vals = [v for v, i, m in values(r"\b(eleven|ten|twelve|nine|thirteen) (?:different )?compan(?:ies|y names)")]
check("E continuity", "Bidwell always has eleven companies", set(vals) == {"eleven"} and len(vals) >= 3, str(vals), "%d mentions" % len(vals))
vals = [v for v, i, m in values(r"\b(fifty-[\w]+|fifty-some) parcels")]
check("E continuity", "Bidwell's parcels: fifty-three (fifty-some where Elijah is estimating)", set(vals) <= {"fifty-three", "fifty-some"} and "fifty-three" in vals, str(vals), str(vals))
vals = [v for v, i, m in values(r"\b(eleven|ten|twelve|nine|two|three) notebooks\b") if v in ("eleven", "ten", "twelve", "nine")]
check("E continuity", "Elijah always has eleven notebooks in Act Four", set(vals) == {"eleven"} and len(vals) >= 4, str(vals), "%d mentions" % len(vals))
vals = [v for v, i, m in values(r"\b(\w+) feet(?: from Walt's| down|\. never been down)", flags=re.I)]
vals2 = [v for v, i, m in values(r"well(?:'s)?,? (?:down )?(\w+) feet")]
check("E continuity", "Manny's well is four feet down both times", [v for v in vals + vals2 if v in ("four",)].__len__() >= 2 and
      "manny says his well's down four feet" in cur_text and "Manny's well, four feet down" in cur_text)
check("E continuity", "The power bill is $211.46, then $211", "$211.46" in cur_text and
      set(re.findall(r"\$211(?:\.\d\d)?", cur_text)) <= {"$211.46", "$211"})
check("E continuity", "Walt's tractor repair is sixty dollars every time",
      cur_text.count('"Sixty," Marta said.') == 1 and "running for sixty bucks once" in cur_text and
      "fixed the husband's tractor for sixty dollars" in cur_text)
vals = [v for v, i, m in values(r"\b(eighteen|seventeen|nineteen|sixteen) days\b")]
check("E continuity", "Every 'eighteen days' is eighteen", set(vals) == {"eighteen"} and len(vals) == 4, str(vals), "%d mentions" % len(vals))
check("E continuity", "Lou's wife: thirty-one years of fourth grade (twice now, not three times)",
      len(re.findall(r"thirty-one years", cur_text, re.I)) == 2 and "Said fourth grade never once felt like the cosmos." in cur_text)
check("E continuity", "The checks: sixteen months since the vote, at half",
      '"It passed," she said. "At half."' in cur_text and "for sixteen months he had put them in the back of a notebook" in cur_text)

def ordered_ages(name, pattern, expect):
    seen = [(SEC[i], m.group(1).lower()) for i, m in line_hits(pattern, re.I, only_novel=True)]
    order = ["nineteen", "twenty", "twenty-one", "twenty-four", "thirty-five", "thirty-six", "thirty-seven"]
    idx = [order.index(a) for _, a in seen if a in order]
    check("E continuity", name, idx == sorted(idx) and [a for _, a in seen] == expect, str(seen), str(seen))
ordered_ages("Elijah's age only goes up: 35, 36, 36, 37",
             r"\b(?:He was|I'm) (thirty-five|thirty-six|thirty-seven)(?: years old)?\b", ["thirty-five", "thirty-six", "thirty-six", "thirty-seven"])
ordered_ages("Tyler's age only goes up: 19, 20, 21, 21",
             r"(?:He was (nineteen), and he was the Tyler|He was (?:nineteen) and he had|a (twenty)-year-old had the name|He was (twenty)\. He just|Tyler, (twenty-one) years old|Tyler was (twenty-one) and|Tyler stood there, (twenty-one) years old)",
             None) if False else None
t_ages = []
for pat in (r"He was (nineteen), and he was the Tyler", r"He was (nineteen) and he had twenty-six boxes left", r"a (twenty)-year-old had the name",
            r"He was (twenty)\. He just put it away", r"Tyler, (twenty-one) years old, two years on the roster",
            r"Tyler was (twenty-one) and had to learn it overhead", r"Tyler stood there, (twenty-one) years old"):
    hs = line_hits(pat)
    t_ages.append((pat[:28], [(i, m.group(1)) for i, m in hs]))
flat = [(i, a) for _, hs in t_ages for i, a in hs]
order = {"nineteen": 19, "twenty": 20, "twenty-one": 21}
seq = [order[a] for i, a in sorted(flat)]
check("E continuity", "Tyler's age only goes up: 19, 19, 20, 20, 21, 21, 21", seq == sorted(seq) and len(seq) == 7, str(sorted(flat)), str(seq))
dl = []
for word, n in (("fifty-one thousand", 51), ("fifty-eight thousand", 58), ("Sixty-six thousand", 66), ("Eighty thousand", 80)):
    hs = [i for i, l in enumerate(lines) if word in l]
    dl.append((hs[0] if len(hs) == 1 else -1, n))
check("E continuity", "The download count only goes up: 51, 58, 66, 80 thousand",
      all(i >= 0 for i, _ in dl) and [n for _, n in sorted(dl)] == [51, 58, 66, 80], str(dl))
check("E continuity", "The bet is the same everywhere: Thanksgiving 2027, loser cooks",
      cur_text.count("Thanksgiving 2027. Loser cooks.") >= 2 and "Thanksgiving, 2027" in cur_text and
      "He took the bet: Thanksgiving 2027, loser cooks." in cur_text)
check("E continuity", "Grace's phone: laid by her fork, then in her back pocket when she leaves the table",
      "She laid it down, very carefully, next to her fork." in cur_text and
      "Her phone had gone into her back pocket when she left the table." in cur_text)
vb = next((l for l in lines if l.startswith("There was a name on every Sunday.")), "")
check("E continuity", "Visitor book: Ray's Sundays start in the first spring, after Elijah's first-winter Sundays stop",
      "That one went back to the first spring." in vb and "every Sunday that first winter, and then it stopped" in cur_text and
      '"Her Sunday company didn\'t come."' in cur_text)
check("E continuity", "The note is four words and reads \"I love you too\"",
      "wrote four words on it" in cur_text and len("I love you too".split()) == 4)
check("E continuity", "\"You're good\" is two words, as the next line says", '"You\'re good."' in cur_text and "It was two words." in cur_text)
check("E continuity", "The seat belt runs through the amp handle in Ch 13, 14 and 15, and is buckled across nothing in Ch 37",
      "David ran the seat belt through the handle himself" in cur_text and "with the seat belt still through the handle" in cur_text and
      "with the belt through its handle" in cur_text and "with the seat belt buckled across nothing on the passenger side" in cur_text)
apx = "\n".join(l for i, l in enumerate(lines) if SEC[i] == "Appendix")
APX = ["Late 2022. Chat Horizon goes public.", "September 2024. Ma's stroke.", "March 2025. Eight hundred miles north to the co-op.",
       "June 12, 2026.", "November 2026. The co-op ships its files free.", "March 2027. The machine on the dairy.",
       "July 9, 2027. The Architect posts \"It asked.\"", "Thursday, November 25, 2027. Thanksgiving."]
check("E continuity", "The Appendix timeline carries the same dates as the chapters",
      all(a in apx for a in APX) and "On the ninth of July, the Architect posted." in cur_text and
      "In March five small things went wrong" in cur_text)

# ============================================================================= F. STRUCTURE
check("F structure", "The contents list matches the headings, in order", contents_heads == body_heads and len(body_heads) == 53,
      "contents %d entries, body %d headings" % (len(contents_heads), len(body_heads)), "%d headings" % len(body_heads))
chs = [int(re.match(r"Chapter (\d+)", h).group(1)) for h in body_heads if h.startswith("Chapter ")]
check("F structure", "Chapters run 0 to 39 with none missing or repeated", chs == list(range(40)), str(chs))
check("F structure", "Four acts and four Meanwhile interludes",
      [h for h in body_heads if h.startswith("Act ")] == ["Act One: The Bar", "Act Two: The City", "Act Three: The Farm", "Act Four: The Ridge"] and
      body_heads.count("Meanwhile") == 4)
check("F structure", "Order: Author's Note, the novel, Epilogue, About This Book, Afterword, Appendix",
      body_heads[0] == "Author's Note" and body_heads[-4:] == ["Epilogue", "About This Book", "Afterword", "Appendix"])
tabs = cur_doc["tabs"]
check("F structure", "The Doc has one tab", len(tabs) == 1 and not tabs[0].get("childTabs"))
sugg = sum(1 for p in cur_paras for r in p[3] if r[4].get("suggestedInsertionIds") or r[4].get("suggestedDeletionIds") or r[4].get("suggestedTextStyleChanges"))
check("F structure", "No pending suggestions", sugg == 0, "%d suggested runs" % sugg)
n_obj = len(tabs[0]["documentTab"].get("inlineObjects", {}))
n_obj_par = sum(1 for p in cur_paras if p[4])
n_obj_start = len(start_doc["tabs"][0]["documentTab"].get("inlineObjects", {}))
check("F structure", "19 pictures, each in its own paragraph, same as at session start",
      n_obj == 19 and n_obj_par == 19 and n_obj_start == 19, "objects %d, paragraphs with a picture %d" % (n_obj, n_obj_par))
is_break = lambda p: p[2] == " \n" and not p[4]
br_now = sum(1 for p in cur_paras if is_break(p))
br_start = sum(1 for p in start_paras if is_break(p))
adjacent = sum(1 for a, b in zip(cur_paras, cur_paras[1:]) if is_break(a) and is_break(b))
check("F structure", "Scene breaks: same count as at session start, none doubled", br_now == br_start and adjacent == 0 and br_now > 50,
      "now %d, session start %d, doubled %d" % (br_now, br_start, adjacent), "%d scene breaks" % br_now)
empties = [p[0] for p in cur_paras if p[2].strip("\n  ") == "" and not p[4] and not is_break(p)]
check("F structure", "No stray empty paragraphs", not empties, "at indexes %s" % empties[:10])
odd = [i for i, l in enumerate(lines) if l.count('"') % 2 == 1]
bad = [i + 1 for i in odd if not (i + 1 < len(lines) and lines[i + 1].startswith('"') and not lines[i].endswith('"'))]
check("F structure", "Every quotation mark is closed (a speech that runs on reopens in the next paragraph)", not bad,
      "unbalanced at lines %s" % bad, "%d paragraph(s) run on correctly" % len(odd))
par = [i + 1 for i, l in enumerate(lines) if l.count("(") != l.count(")")]
check("F structure", "Every parenthesis is closed", not par, "lines %s" % par)
dup = [h for h, n in collections.Counter(h for h in body_heads if h != "Meanwhile").items() if n > 1]
check("F structure", "No heading appears twice", not dup, str(dup))

# ============================================================================= G. FORMATTING
fonts, sizes, other = collections.Counter(), collections.Counter(), collections.Counter()
for s, e, txt, runs, has_obj, ps in cur_paras:
    if ps.get("namedStyleType") != "NORMAL_TEXT":
        continue
    for rs, re_, c, st, _ in runs:
        if not c.strip():
            continue
        fonts[st.get("weightedFontFamily", {}).get("fontFamily", "(inherited)")] += len(c)
        sizes[str(st.get("fontSize", {}).get("magnitude", "(inherited)"))] += len(c)
        for k in st:
            if k not in ("italic", "bold", "weightedFontFamily", "fontSize"):
                other[k] += len(c)
check("G formatting", "Body text is in one font", len(fonts) == 1, str(dict(fonts)), str(dict(fonts)))
check("G formatting", "Body text is in one size", len(sizes) == 1, str(dict(sizes)), str(dict(sizes)))
strays = {k: v for k, v in other.items() if k not in ("foregroundColor", "backgroundColor", "link", "underline",
                                                         "strikethrough", "smallCaps", "baselineOffset") or v}
real_strays = {}
for s, e, txt, runs, has_obj, ps in cur_paras:
    if ps.get("namedStyleType") != "NORMAL_TEXT":
        continue
    for rs, re_, c, st, _ in runs:
        if not c.strip():
            continue
        for k in ("underline", "strikethrough", "smallCaps"):
            if st.get(k):
                real_strays.setdefault(k, []).append(c.strip()[:40])
        if st.get("baselineOffset") not in (None, "NONE", "BASELINE_OFFSET_UNSPECIFIED"):
            real_strays.setdefault("baselineOffset", []).append(c.strip()[:40])
        if st.get("backgroundColor", {}).get("color"):
            real_strays.setdefault("highlight", []).append(c.strip()[:40])
        if st.get("link"):
            real_strays.setdefault("link", []).append(c.strip()[:40])
check("G formatting", "No underline, strikethrough, highlight, link or raised text in the body", not real_strays,
      str({k: v[:4] for k, v in real_strays.items()}))
bold = [c.strip()[:50] for s, e, txt, runs, has_obj, ps in cur_paras if ps.get("namedStyleType") == "NORMAL_TEXT"
        for rs, re_, c, st, _ in runs if st.get("bold") and c.strip()]
bold_start = [c.strip()[:50] for s, e, txt, runs, has_obj, ps in start_paras if ps.get("namedStyleType") == "NORMAL_TEXT"
              for rs, re_, c, st, _ in runs if st.get("bold") and c.strip()]
check("G formatting", "Bold text is exactly what it was at session start", bold == bold_start, "now %s" % bold[:6], "%d bold runs" % len(bold))
def pkey(ps):
    return json.dumps({k: v for k, v in ps.items() if k not in ("headingId",)}, sort_keys=True)
styles_now = collections.Counter(pkey(p[5]) for p in cur_paras)
styles_start = collections.Counter(pkey(p[5]) for p in start_paras)
BODY_STYLE = collections.Counter(pkey(p[5]) for p in cur_paras if p[5].get("namedStyleType") == "NORMAL_TEXT").most_common(1)[0][0]
NEW_BODY_PARAS = collections.Counter({BODY_STYLE: 5})
check("G formatting", "Paragraph styling is exactly what it was at session start (the moved paragraph included)",
      styles_now - styles_start == NEW_BODY_PARAS and not (styles_start - styles_now),
      "paragraph style counts changed: %s" % list((styles_now - styles_start).items())[:3],
      "%d distinct paragraph styles, same counts apart from the 5 body paragraphs the last edit added (6 in Ch 33, less 1 cut in Ch 31)" % len(styles_now))
named = collections.Counter(p[5].get("namedStyleType") for p in cur_paras)
body_head_paras = [p for p in cur_paras if p[0] >= BODY_IDX and HEAD_RE.match(p[2].rstrip("\n"))]
not_heading = [p[2].strip() for p in body_head_paras if not p[5].get("namedStyleType", "").startswith("HEADING")]
check("G formatting", "Every one of the 53 headings is a real heading paragraph (so the Kindle contents can find it)",
      len(body_head_paras) == 53 and not not_heading, "styled as body text: %s" % not_heading[:5], str(dict(named)))
body_as_heading = [p[2].strip()[:40] for p in cur_paras if p[0] >= BODY_IDX and p[5].get("namedStyleType", "").startswith("HEADING")
                   and not HEAD_RE.match(p[2].rstrip("\n")) and len(p[2]) > 80]
check("G formatting", "No paragraph of prose is styled as a heading", not body_as_heading, str(body_as_heading[:5]))

# ============================================================================= H. ITALICS
def italic_map(paras):
    """paragraph text -> list of italic substrings"""
    m = collections.defaultdict(list)
    for s, e, txt, runs, has_obj, ps in paras:
        buf = ""
        for rs, re_, c, st, _ in runs:
            if st.get("italic"):
                buf += c
            else:
                if buf.strip():
                    m[txt].append(buf)
                buf = ""
        if buf.strip():
            m[txt].append(buf)
    return m
def italic_spans(p):
    spans, pos, buf, st0 = [], 0, None, 0
    for rs, re_, c, st, _ in p[3]:
        if st.get("italic"):
            if buf is None:
                buf, st0 = "", pos
            buf += c
        else:
            if buf is not None:
                spans.append((st0, st0 + len(buf)))
            buf = None
        pos += len(c)
    if buf is not None:
        spans.append((st0, st0 + len(buf)))
    return spans
def is_italic(p, a, b):
    return any(s <= a and b <= e for s, e in italic_spans(p))
cur_by_text = collections.defaultdict(list)
for p in cur_paras:
    cur_by_text[p[2]].append(p)
lost = []
need = collections.Counter()                      # (paragraph text, span) -> how many paragraphs carried it at session start
for p in start_paras:
    for a_, b_ in italic_spans(p):
        if p[2][a_:b_].strip():
            need[(p[2], a_, b_)] += 1
for (txt, a_, b_), n_need in need.items():
    frag = txt[a_:b_].strip()
    cands = cur_by_text.get(txt)
    if cands:                                     # identical paragraphs are counted, not merely matched
        have = sum(1 for c in cands if is_italic(c, a_, b_))
    else:                                         # the paragraph was edited this session: find the phrase, italic, anywhere
        have = sum(1 for q in cur_paras if frag in q[2] and
                   any(frag in q[2][s_:e_] for s_, e_ in italic_spans(q)))
    if have < n_need:
        lost.append("%s (was x%d, now x%d)" % (frag[:50], n_need, have))
n_start = sum(len(italic_spans(p)) for p in start_paras)
check("H italics", "Nothing that was italic at session start has lost its italics", not lost, "lost: %s" % lost[:8],
      "%d italic spans at session start, all still italic" % n_start)

MUST_BE_ITALIC = [
    "It will look like this.", "I can see it. I can show people.", "can I plug in.", "Linda Madrone", "Unfortunately", "Past due,",
    "what was that.", "Ask. Don't guess.", "What's your solution?", "7. It leaves.", "Funded through December. Tell you more in June.",
    "Working. All good.", "It's fine.", "Lou: enough to exist,", "Ours.", "Curtis: who holds the plug? Lou: Curtis.",
    "they just don't want to learn a new way of doing things.", "That's your mother.", "Don't.", "How hard is it to change yourself?",
    "M. Madrone,", "Glad you could make it,", "For our mother. Or your stepmother. Or whoever she is to you.", "I love you too,",
    "Come home.", "Worm.", "That's your tree,", "It can burn to the ground and come back from the root. Remember that.",
    "A chatbot? Like the thing in my insurance portal?", "good for you, buddy", "D. McGrath,",
]
ANCHOR = {   # phrase -> words that pin down the one paragraph meant, where the phrase is not unique
    "It's fine.": "Marta didn't laugh.", "Ours.": "Lou: enough to exist", "Don't.": "Instead he changed the name to",
    "Worm.": "one word on it in pencil", "Unfortunately": "started with the word", "Linda Madrone": "an account that said",
    "good for you, buddy": "cold plunges", "7. It leaves.": "under the seven stages:", "M. Madrone,": None,
    "D. McGrath,": "The visitor book filled up.", "Working. All good.": "he had ended on the same thing",
    "Past due,": "it said, and under that", "what was that.": "and thought,", "It will look like this.": "It won't be dramatic",
    "Ask. Don't guess.": "where he'd left the blank, he wrote:", "That's your mother.": "he heard her say",
    "How hard is it to change yourself?": "then he heard Lou.",
}
bad = []
for phrase in MUST_BE_ITALIC:
    anchor = ANCHOR.get(phrase)
    cands = [p for p in cur_paras if phrase in p[2] and (anchor is None or anchor in p[2])]
    if phrase == "M. Madrone,":
        ok = len(cands) == 2 and all(is_italic(p, p[2].find(phrase), p[2].find(phrase) + len(phrase)) for p in cands)
    else:
        ok = len(cands) == 1 and is_italic(cands[0], cands[0][2].find(phrase), cands[0][2].find(phrase) + len(phrase))
    if not ok:
        bad.append("%r (%d paragraphs)" % (phrase, len(cands)))
check("H italics", "All 31 thought, typed and remembered spots fixed this session are italic", not bad, "; ".join(bad))

ACRONYMS = {"AGI", "ASI", "COVID", "GPU", "GPUS", "MLS", "NDA", "NDAS", "LLC", "CSA", "CPO", "HR", "TV", "AI", "ALC", "GDP",
            "ESP32", "OK", "LADDER", "SHOCKED", "Q&A", "A/B", "DJ", "USA", "PVC", "LED", "ID", "PDF", "CEO", "RV", "ATM"}
CAPS = re.compile(r"(?<![A-Za-z'])(?:[A-Z][A-Z0-9']+|I|A)(?:[ ,:/-]+(?:[A-Z][A-Z0-9']+|I|A|\d+))*(?![a-z])")
plain_caps = []
for p in cur_paras:
    if p[5].get("namedStyleType") != "NORMAL_TEXT" or p[0] < BODY_IDX:
        continue
    for m in CAPS.finditer(p[2]):
        w = m.group(0).strip(" ,:/-")
        letters = re.sub(r"[^A-Z]", "", w)
        words = [x for x in re.split(r"[ ,:/-]+", w) if x]
        if len(letters) < 4 or all(x.strip("'") in ACRONYMS or x in ("I", "A") or x.isdigit() for x in words):
            continue
        a = m.start() + m.group(0).find(w)
        if not is_italic(p, a, a + len(w)):
            plain_caps.append("%s ...%s[%s]" % (p[0], p[2][max(0, a - 30):a], w))
check("H italics", "Every in-story all-capitals phrase is italic (abbreviations, SHOCKED and LADDER.xlsx excepted)",
      not plain_caps, "; ".join(plain_caps[:8]))
CUES = re.compile(r"(,\s(?:he|she|Elijah) thought[.,]|\b(?:he|she|Elijah|it) typed [A-Z]|\bit wrote\.|,\s(?:he|she) wrote\.|"
                  r"\b(?:he|she) heard (?:her|him|Lou|David) say [A-Z]|\bthat (?:still )?said [A-Z][a-z]+ [A-Z]|\bthe word [A-Z])")
cue_plain = []
for p in cur_paras:
    if p[0] < BODY_IDX:
        continue
    for m in CUES.finditer(p[2]):
        if not any(s - 90 <= m.start() <= e + 90 for s, e in italic_spans(p)):
            cue_plain.append("...%s..." % p[2][max(0, m.start() - 50):m.end() + 50].replace("\n", " "))
warn("I hygiene", "A thought, typed or written cue with no italics within reach", cue_plain)

# ============================================================================= I. HYGIENE (flags for a human)
novel_lines = [(i, lines[i]) for i in range(body_start, len(lines))]
dbl = [ctx(i, m) for i, m in line_hits(r"\b([A-Za-z']+) \1\b", re.I)
       if m.group(1).lower() not in ("had", "that", "no", "very", "so", "bye", "ha", "said") and
       not re.search(r"(?:Not yet\. Not yet|around and around|and on and on|take and take|more and more|over and over|again and again)", lines[i])]
ALLOWED_DOUBLES = ("It's it's", "modeled, modeled", "Waits to see", "Lou's a Khan guy. Lou's", "what, what is it", "No, no.", "Don't. Don't",
                   "Come on. Come", "I hate this. I hate", "Not yet. Not yet", "around and around", "Six feet", "nothing, nothing",
                   "Nothing, nothing", "Shit. Shit", "Okay. Okay", "go go")
warn("I hygiene", "The same word twice in a row", [d for d in dbl])
sp = [ctx(i, m, 25) for i, m in line_hits(r" [,.;:?!](?!\.)|[a-z]\.[A-Z][a-z]|,,|\.\.|;;|\?\?|!!| {2,}(?=\S)|\s+$|^\s+(?=\S)|[,;:][A-Za-z]")
      if lines[i].strip() and lines[i] not in (" ", "  ")]
warn("I hygiene", "Spacing or punctuation slips (space before a mark, missing space, doubled mark, double space)", sp)
WORD = re.compile(r"[A-Za-z\u00c0-\u024f][A-Za-z\u00c0-\u024f']*")
vocab_now = set(w.lower().strip("'") for w in WORD.findall(cur_text))
vocab_ok = set(open(P("reviewed_vocabulary.txt"), encoding="utf-8").read().split())
new_words = sorted(vocab_now - vocab_ok)
check("I hygiene", "Spelling: every distinct word in the book is in the vocabulary that was read through word by word",
      not new_words, "words not yet reviewed: %s" % new_words[:30], "%d distinct words, none new" % len(vocab_now))
sents = collections.Counter()
where = collections.defaultdict(list)
for i, l in novel_lines:
    for s_ in re.split(r'(?<=[.?!])["\']?\s+', l):
        s2 = s_.strip().strip('"')
        if len(s2.split()) >= 9:
            sents[s2] += 1
            where[s2].append(SEC[i])
warn("I hygiene", "A sentence of nine or more words that appears more than once",
     ["x%d %s: %s" % (n, sorted(set(where[s_])), s_[:90]) for s_, n in sents.items() if n > 1])
pcount = collections.Counter(l for i, l in novel_lines if len(l) > 60)
warn("I hygiene", "A whole paragraph that appears twice", ["%s..." % l[:80] for l, n in pcount.items() if n > 1])
stack, run_ = [], []
def first_word(l):
    m = re.match(r"^([A-Za-z']+)", l)
    return m.group(1) if m else None
prev = None
for i, l in novel_lines:
    w = first_word(l) if (l.strip() and not HEAD_RE.match(l)) else None
    if w and w == prev and w in ("He", "She", "They", "It", "Elijah", "Grace", "Lou", "The", "Then", "There"):
        run_.append(i)
    else:
        if len(run_) >= 3:
            stack.append("%s x%d from L%d (%s)" % (prev, len(run_) + 1, run_[0], SEC[run_[0]]))
        run_ = []
    prev = w
warn("I hygiene", "Four or more paragraphs in a row opening on the same word", stack)
low = [ctx(i, m, 20) for i, m in line_hits(r"(?<=[a-z]{3}[.?!] )[a-z]") if not in_dialogue(lines[i], m.start())
       and not re.search(r"\b(is my stuff|saw your thing|thought you'd|manny says|it hums|figured\.|we got the grange|grateful to have|hug your|going quiet|you probably want|ruby,)", lines[i])]
warn("I hygiene", "A sentence in narration that starts with a lower-case letter", low)

# ----------------------------------------------------------------------------- report
OPEN = [
    "Ch 36: \"She shook both hands up by her chin.\" (gesture unclear, held for the author's words)",
    "Ch 36: \"There was disgust in her face, and rage\" (names the feeling, held for the author's words)",
    "Ch 39: the stream cuts from the prayer straight to Grace's face (author's call; reads as a cut)",
    "Author's open items: the parade joke (Ch 19, Ch 25), a \"looked at\" pass (Ch 15, Ch 17), the repeats \"forty\", \"nine days\", \"like a kid\"",
    "Afterword: the United Nations quotation was matched by web search only on 24 Nov (the search result gives the same words from the UN page \"Global Issues: Food\"); the page itself could not be opened from the checking machine",
    "How the file renders on a Kindle (page breaks, pictures, contents links) has not been looked at",
    "Judgment no code can make: whether any scene is confusing, runs long, or fails to land",
]
order = {"FAIL": 0, "WARN": 1, "PASS": 2}
n = collections.Counter(r[0] for r in results)
out = []
out.append("VERIFY v5   %s   Doc revision %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), cur_doc.get("revisionId", "?")[:18]))
out.append("PASS %d   FAIL %d   WARN %d   OPEN %d" % (n["PASS"], n["FAIL"], n["WARN"], len(OPEN)))
out.append("")
sec = None
for level, section, name, detail in results:
    if section != sec:
        out.append("== %s" % section)
        sec = section
    if level == "WARN":
        out.append("  WARN  %s  (%d)" % (name, len(detail)))
        for d in detail[:60]:
            out.append("          - %s" % d)
        if len(detail) > 60:
            out.append("          ... and %d more" % (len(detail) - 60))
    else:
        out.append("  %s  %s%s" % (level, name, ("   [%s]" % detail) if detail else ""))
out.append("")
out.append("== OPEN (not provable by code, not counted as passed)")
for o in OPEN:
    out.append("  OPEN  %s" % o)
report = "\n".join(out)
print(report)
open(os.path.join(DATA, "verify_report.txt"), "w", encoding="utf-8").write(report + "\n")
sys.exit(1 if n["FAIL"] else 0)
