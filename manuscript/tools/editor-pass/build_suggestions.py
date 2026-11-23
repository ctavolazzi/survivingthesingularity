"""Plan the small suggestions for v4 from a fresh read, and refuse anything unsafe.

Usage: python3 -I build_suggestions.py READ.json OUT_REQUEST.json
Every replacement must match exactly once in the whole Doc and sit inside one paragraph.
Whole-paragraph cuts are deleted by position and are only valid for the revision that was read,
so the request carries requiredRevisionId: if anyone has typed since, Google refuses the batch.
"""
import json
import re
import sys

doc = json.load(open(sys.argv[1]))["content"]
body = doc["tabs"][0]["documentTab"]["body"]["content"]
paras = []
for el in body:
    p = el.get("paragraph")
    if not p:
        continue
    text = "".join(e.get("textRun", {}).get("content", "") for e in p["elements"])
    styled = any(e.get("textRun", {}).get("textStyle", {}).get(k) for e in p["elements"] for k in ("italic", "bold", "link"))
    paras.append({"text": text, "start": el["startIndex"], "end": el["endIndex"], "styled": styled, "els": p["elements"]})
full = "".join(p["text"] for p in paras)

# (chapter, find, replace, why)
REPLACE = [
    ("Ch 17", "had run for county supervisor once", "had run for county commissioner once", "Washington counties have commissioners"),
    ("Ch 26", "made a county supervisor cry", "made a county commissioner cry", "Washington counties have commissioners"),
    ("Ch 29", "a hostile county supervisor", "a hostile county commissioner", "Washington counties have commissioners"),
    ("Ch 30", "what that supervisor was scared of", "what that commissioner was scared of", "Washington counties have commissioners"),
    ("Ch 30", "The supervisors had been sitting", "The commissioners had been sitting", "Washington counties have commissioners"),
    ("Ch 30", "the supervisor with the almonds", "the commissioner with the almonds", "Washington counties have commissioners"),
    ("Ch 17", "wanna play, OK?", "wanna play, okay?", "the book spells it okay 52 times and OK once"),
    ("Ch 17", "whole system's...", "whole system's…", "the book uses the single ellipsis character 36 times, three dots twice"),
    ("Ch 36", "doesn't have to...", "doesn't have to…", "same"),
    ("Ch 30", "wrist brace grey", "wrist brace gray", "gray 17 times, grey once"),
    ("Ch 4", "in a t-shirt he'd", "in a T-shirt he'd", "T-shirt elsewhere"),
    ("Ch 0", "Elijah turned the laptop toward the realtors", "He turned the laptop toward the realtors", "three sentences in a row open on Elijah"),
    ("Ch 0", "self-taught data science who'd wandered", "self-taught data science, who'd wandered", "without the comma, who'd attaches to data science"),
    ("Ch 1", "He hadn't planned to walk back into the Bear Flag so soon.", "Elijah hadn't planned to walk back into the Bear Flag so soon.", "the he before the break is Devendra"),
    ("Ch 2", "That night he sat at the kitchen table", "That night Elijah sat at the kitchen table", "the he before it is Devendra"),
    ("Ch 3", "It would look like this.", "It will look like this.", "the thought is in the future tense one sentence earlier"),
    ("Ch 7", "He took the bill and zipped his jacket.", "Elijah took the bill and zipped his jacket.", "the he before it is David"),
    ("Ch 9", "the same way she'd read the rest, every word", "the same way she'd read the list, every word", "the rest twice in one sentence"),
    ("Ch 13", "He went down it twice, to be sure.", "He went down the list twice, to be sure.", "it has no noun"),
    ("Ch 19", "He thought they were both right.", "Elijah thought they were both right.", "the last he was Tyler"),
    ("Ch 24", "It went up on the co-op's lease", "The house went up on the co-op's lease", "It has no noun yet"),
    ("Ch 25", "He said nothing, and he had his reasons.", "Elijah said nothing, and he had his reasons.", "the paragraph before is about Tyler"),
    ("Ch 26", "tomorrow? Your basement?\"", "tomorrow?\" Lou said. \"Your basement?\"", "two Curtis lines come before it, so the speaker is unclear"),
    ("Ch 32", "He had said so out loud, at a Friday table,", "He had said out loud, at a Friday table,", "so and that double up"),
    ("Ch 33", "She looked at it, and took it back.", "Grace looked at it, and took it back.", "Wren has just spoken, so She is unclear"),
    ("Ch 39", "told you to sit down.\"", "told you to sit down,\" David said.", "David spoke the line before too, so this reads as Elijah"),
    # single sentences that explain what the line before already showed
    ("Ch 8", " He knew he was out of his league.", "", "the misspelled badge says it"),
    ("Ch 10", " He meant it. Elijah could tell.", " He meant it.", "tells"),
    ("Ch 11", "the kind one, and he didn't know why.", "the kind one.", "tells"),
    ("Ch 13", " He could not make it make sense.", "", "the next sentence shows it"),
    ("Ch 19", "Immediately the vibe shifted. ", "", "a word this narrator never uses; her hands show it"),
    ("Ch 32", " It caught on the first strike.", "", "the sentence before already says it took"),
    ("Ch 34", " His face went hot. He felt like an asshole.", " His face went hot.", "tells"),
    ("Ch 37", "\"I'd rather it was here.\" He meant it.", "\"I'd rather it was here.\"", "tells"),
    ("Meanwhile 4", "Then, because he was who he was, he asked it", "Then he asked it", "tells"),
]
# whole paragraphs to cut
CUT = [
    ("Ch 7", "It broke his heart.", "the paragraph before has already broken it"),
    ("Ch 7", "David was the last person he had really trusted. Even David thought he was nuts.", "restates the scene"),
    ("Ch 15", "Those were dark days.", "cliche; the paragraph before shows them"),
    ("Ch 35", "He'd never really thought about that before.", "the paragraph before shows him thinking it"),
]

problems, reqs, report = [], [], []
for ch, find, rep, why in REPLACE:
    n = full.count(find)
    holders = [p for p in paras if find in p["text"]]
    if n != 1 or len(holders) != 1:
        problems.append("%s: %r appears %d times" % (ch, find, n))
        continue
    if re.search("[\u2013\u2014]", rep) or find == rep:
        problems.append("%s: bad replacement %r" % (ch, rep))
        continue
    # does the matched span carry italics or a link? a suggestion would drop them
    p = holders[0]
    off = p["start"] + p["text"].index(find)
    span_styled = any(e.get("textRun", {}).get("textStyle", {}).get(k) for e in p["els"] for k in ("italic", "bold", "link") if e["startIndex"] < off + len(find.encode("utf-16-le")) // 2 and e["endIndex"] > off)
    if span_styled:
        problems.append("%s: %r touches italic or linked text" % (ch, find))
        continue
    reqs.append({"replaceAllText": {"containsText": {"text": find, "matchCase": True}, "replaceText": rep}})
    report.append((ch, find.strip(), rep.strip() or "(cut)", why))

cuts = []
for ch, text, why in CUT:
    holders = [p for p in paras if p["text"].rstrip("\n") == text]
    if len(holders) != 1:
        problems.append("%s: paragraph %r found %d times" % (ch, text, len(holders)))
        continue
    cuts.append((holders[0]["start"], holders[0]["end"], ch, text, why))
cuts.sort(reverse=True)
del_reqs = [{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}} for s, e, _, _, _ in cuts]
for s, e, ch, text, why in sorted(cuts):
    report.append((ch, text, "(cut the paragraph)", why))

out = {"documentId": doc["documentId"], "writeControl": {"writeMode": "SUGGEST", "requiredRevisionId": doc["revisionId"]}, "requests": del_reqs + reqs}
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
json.dump(report, open(sys.argv[2].replace(".json", "_report.json"), "w"), ensure_ascii=False, indent=1)
print("planned: %d replacements, %d paragraph cuts | problems: %d" % (len(reqs), len(del_reqs), len(problems)))
for p in problems:
    print("  PROBLEM", p)
print("control (a made-up passage must count 0):", full.count("zzqx heron radio tower"))
