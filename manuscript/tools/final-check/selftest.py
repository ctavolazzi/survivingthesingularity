#!/usr/bin/env python3
"""
selftest.py  --  proves verify_v5.py can fail.

A checker that only ever prints PASS proves nothing. This script makes 18 damaged copies of the
manuscript, each with one planted fault of a kind that matters, runs verify_v5.py on each, and
requires the named check to FAIL. If any planted fault slips through, this script exits 1.

Usage:  python3 -I selftest.py DATA_DIR WORK_DIR
"""
import sys, os, json, copy, shutil, subprocess

DATA, WORK = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(DATA, "current_doc.json"), encoding="utf-8"))

def body(doc):
    return doc.get("content", doc)["tabs"][0]["documentTab"]["body"]["content"]

def export_of(doc):
    out = []
    for el in body(doc):
        p = el.get("paragraph")
        if not p:
            continue
        if any("textRun" not in e for e in p["elements"]):
            out += ["  ", ""]
        else:
            out.append("".join(e["textRun"]["content"] for e in p["elements"]).rstrip("\n").replace(" ", " "))
    return "\n".join(out)

def runs(doc):
    for el in body(doc):
        p = el.get("paragraph")
        if p:
            for e in p["elements"]:
                if "textRun" in e:
                    yield el, e["textRun"]

def swap(doc, old, new, which=0):
    """replace old with new inside the which-th run that contains it (which=-1 for the last)"""
    hits = [tr for el, tr in runs(doc) if old in tr["content"]]
    assert hits, "selftest could not find %r" % old
    tr = hits[which]
    tr["content"] = tr["content"].replace(old, new, 1)

def unitalic(doc, text, which=0):
    hits = [tr for el, tr in runs(doc) if text in tr["content"] and tr.get("textStyle", {}).get("italic")]
    assert hits, "selftest could not find italic %r" % text
    hits[which]["textStyle"].pop("italic")

def drop_paragraph(doc, startswith):
    b = body(doc)
    i = next(i for i, el in enumerate(b) if el.get("paragraph") and
             "".join(e.get("textRun", {}).get("content", "") for e in el["paragraph"]["elements"]).startswith(startswith))
    b.pop(i)

def drop_scene_break(doc):
    b = body(doc)
    i = next(i for i, el in enumerate(b) if el.get("paragraph") and
             "".join(e.get("textRun", {}).get("content", "") for e in el["paragraph"]["elements"]) == " \n")
    b.pop(i)

def restyle_heading(doc, text):
    hits = [el for el in body(doc) if el.get("paragraph") and
            "".join(e.get("textRun", {}).get("content", "") for e in el["paragraph"]["elements"]).strip() == text]
    hits[-1]["paragraph"]["paragraphStyle"]["namedStyleType"] = "NORMAL_TEXT"

def refont(doc, text):
    tr = next(tr for el, tr in runs(doc) if text in tr["content"])
    tr.setdefault("textStyle", {})["weightedFontFamily"] = {"fontFamily": "Comic Sans MS", "weight": 400}

def suggest(doc, text):
    tr = next(tr for el, tr in runs(doc) if text in tr["content"])
    tr["suggestedInsertionIds"] = ["suggest.x"]

CASES = [
    ("a number changed in one place", lambda d: swap(d, "Nineteen households.", "Eighteen households."), "No stray household count"),
    ("an em dash", lambda d: swap(d, "He drank half.", "He drank half—"), "No em dash anywhere"),
    ("a curly quote", lambda d: swap(d, '"What\'ll it be, Mad?"', '“What\'ll it be, Mad?"'), "Straight quotes only"),
    ("a locked line reworded", lambda d: swap(d, "He felt like an asshole.", "He felt like a jerk."), "Every locked line is present"),
    ("the locked ending reworded", lambda d: swap(d, "But he could still get a free beer at the Bear Flag.", "But he could still get a beer at the Bear Flag."), "Ch 39 Bear Flag ending"),
    ('"never once" in narration', lambda d: swap(d, "He drank half.", "He never once drank half."), '"never once" appears only inside dialogue'),
    ('"hand flat" where it is not allowed', lambda d: swap(d, "her palm pressed to the table", "her hand flat on the table"), '"hand flat" only for'),
    ("a nickname in the wrong chapter", lambda d: swap(d, '"Hey," he said. "What the fuck was all of that?"', '"Hey, Thoreau," Lou had said once, in Ch 20.', 0) or swap(d, "Lou put him on drip tape in May", "Thoreau, Lou called him. Lou put him on drip tape in May"), '"Thoreau" only from Ch 33 on'),
    ("a paragraph silently deleted", lambda d: drop_paragraph(d, "Curtis was in the gravel with the hood of the Ranger up."), "Today's text == session-start text"),
    ("an approved edit undone", lambda d: swap(d, "That one went back to the first spring.", "That one went back to the first November."), "Each approved edit is present exactly once"),
    ("a scene break removed", lambda d: drop_scene_break(d), "Scene breaks: same count"),
    ("a misspelled word", lambda d: swap(d, "refrigerator", "refridgerator"), "Spelling: every distinct word"),
    ("the Sunday call at the wrong time", lambda d: swap(d, "At 9:40 that night he called the rose garden.", "At 9:30 that night he called the rose garden."), "The Sunday call is always 9:40"),
    ("italics lost on an old italic line", lambda d: unitalic(d, "Am I crazy?", 1), "Nothing that was italic at session start"),
    ("italics lost on a line fixed today", lambda d: unitalic(d, "Come home."), "thought, typed and remembered spots"),
    ("capitals left plain", lambda d: unitalic(d, "DECEMBER."), "Every in-story all-capitals phrase is italic"),
    ("a chapter heading turned into body text", lambda d: restyle_heading(d, "Chapter 12: The Seventeen-Dollar Shower"), "Every one of the 53 headings is a real heading"),
    ("a chapter title that no longer matches the contents", lambda d: swap(d, "Chapter 5: The Tenant Who Paid No Rent", "Chapter 5: The Tenant", -1), "The contents list matches the headings"),
    ("a different font on one line", lambda d: refont(d, "He drank half."), "Body text is in one font"),
    ("an unanswered suggestion left in the Doc", lambda d: suggest(d, "He drank half."), "No pending suggestions"),
    ("an unclosed quotation mark", lambda d: swap(d, '"No, I didn\'t."', '"No, I didn\'t.'), "Every quotation mark is closed"),
]

static = ["session_start_export.txt", "session_start_doc.json", "text_as_read.txt", "line_edits.json", "reviewed_vocabulary.txt"]
ok_all = True
print("SELF-TEST: %d planted faults" % len(CASES))
for k, (label, mutate, must_fail) in enumerate(CASES, 1):
    d = os.path.join(WORK, "case%02d" % k)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in static:
        os.symlink(os.path.abspath(os.path.join(DATA, f)), os.path.join(d, f))
    doc = copy.deepcopy(base)
    mutate(doc)
    json.dump(doc, open(os.path.join(d, "current_doc.json"), "w", encoding="utf-8"))
    open(os.path.join(d, "current_export_raw.txt"), "w", encoding="utf-8", newline="").write(export_of(doc))
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "verify_v5.py"), d], capture_output=True, text=True)
    fails = [l.strip() for l in r.stdout.split("\n") if l.strip().startswith("FAIL")]
    caught = r.returncode == 1 and any(must_fail in l for l in fails)
    ok_all &= caught
    print("  %s  %-52s -> %s" % ("CAUGHT" if caught else "MISSED", label, must_fail if caught else "exit %d, fails: %s" % (r.returncode, [f[:60] for f in fails][:4])))

# and the undamaged copy must still pass
d = os.path.join(WORK, "case00_clean")
shutil.rmtree(d, ignore_errors=True)
os.makedirs(d)
for f in static:
    os.symlink(os.path.abspath(os.path.join(DATA, f)), os.path.join(d, f))
json.dump(base, open(os.path.join(d, "current_doc.json"), "w", encoding="utf-8"))
open(os.path.join(d, "current_export_raw.txt"), "w", encoding="utf-8", newline="").write(export_of(base))
r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "verify_v5.py"), d], capture_output=True, text=True)
clean = r.returncode == 0
print("  %s  the undamaged manuscript passes" % ("OK    " if clean else "BROKEN"))
print("SELF-TEST %s" % ("PASSED: every planted fault was caught" if ok_all and clean else "FAILED"))
sys.exit(0 if ok_all and clean else 1)
