"""Turn a saved read_doc JSON of the manuscript into sections, and compare with an earlier sections file.

Usage: python3 -I sections_from_read.py READ.json OUT_SECTIONS.json [OLD_SECTIONS.json]
"""
import difflib
import json
import re
import sys

doc = json.load(open(sys.argv[1]))["content"]
body = doc["tabs"][0]["documentTab"]["body"]["content"]


def key_of(t):
    m = re.match(r"Chapter\s+(\d+)", t)
    if m:
        return "ch%02d" % int(m.group(1))
    if t.startswith("Author"):
        return "authors-note"
    if t.startswith("Afterword"):
        return "afterword"
    if t.startswith("Appendix"):
        return "appendix"
    return None


sections, cur, mw, images, sugg = {}, None, 0, 0, 0
for el in body:
    p = el.get("paragraph")
    if not p:
        continue
    text = ""
    for e in p["elements"]:
        if "inlineObjectElement" in e:
            images += 1
        tr = e.get("textRun")
        if not tr:
            continue
        if tr.get("suggestedInsertionIds") or tr.get("suggestedDeletionIds"):
            sugg += 1
        if not tr.get("suggestedDeletionIds"):
            text += tr["content"]
    text = text.rstrip("\n")
    if p["paragraphStyle"].get("namedStyleType") == "HEADING_1":
        t = text.strip()
        if t == "Meanwhile":
            mw += 1
            cur = "meanwhile%d" % mw
        elif t.startswith("Act "):
            cur = None
            continue
        else:
            cur = key_of(t)
        if cur:
            sections[cur] = {"title": t, "paras": []}
        continue
    if cur and text.strip():
        sections[cur]["paras"].append(text)

json.dump(sections, open(sys.argv[2], "w"), ensure_ascii=False)
words = sum(len(q.split()) for s in sections.values() for q in s["paras"])
print("revision:", doc.get("revisionId", "")[:24], "| sections:", len(sections), "| words:", words, "| pictures:", images, "| runs carrying a suggestion:", sugg)

if len(sys.argv) > 3:
    old = json.load(open(sys.argv[3]))
    changed = 0
    for k in sections:
        a, b = old.get(k, {"paras": [], "title": ""}), sections[k]
        if a["title"] != b["title"]:
            print("\nTITLE %s: %r -> %r" % (k, a["title"], b["title"]))
        if a["paras"] == b["paras"]:
            continue
        changed += 1
        print("\n##### %s (%s): %d -> %d words" % (k, b["title"], sum(len(q.split()) for q in a["paras"]), sum(len(q.split()) for q in b["paras"])))
        sm = difflib.SequenceMatcher(None, a["paras"], b["paras"], autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            for q in a["paras"][i1:i2]:
                print("  - " + q)
            for q in b["paras"][j1:j2]:
                print("  + " + q)
    for k in old:
        if k not in sections:
            print("\nMISSING NOW:", k)
    print("\nsections changed since the earlier read:", changed)
