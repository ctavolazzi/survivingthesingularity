"""Measure the prose of v4 and write one numbered text file per part, for a read-through.

Usage: python3 -I prose_audit.py V4_SECTIONS.json OUTDIR
Read-only on the manuscript. Writes OUTDIR/part*.txt and OUTDIR/metrics.json.
"""
import collections
import json
import os
import re
import sys

S = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
ORDER = list(S)

# ---- parts for the read-through, in book order
cuts = {"part1": ("authors-note", "ch05"), "part2": ("ch06", "ch15"), "part3": ("ch16", "ch23x"), "part4": ("ch24", "ch31"), "part5": ("meanwhile4", "appendix")}
bounds = [ORDER.index("authors-note"), ORDER.index("ch06"), ORDER.index("ch16"), ORDER.index("ch24"), ORDER.index("meanwhile4"), len(ORDER)]
parts = {}
for n in range(5):
    keys = ORDER[bounds[n]:bounds[n + 1]]
    if n == 2:
        # the third Meanwhile sits after Chapter 23 in the book
        assert "meanwhile3" in keys, keys
    if n == 4:
        keys = [k for k in keys if k != "appendix"]
    parts["part%d" % (n + 1)] = keys
    lines = []
    for k in keys:
        lines.append("\n\n===== %s  [%s] =====\n" % (S[k]["title"], k))
        for i, p in enumerate(S[k]["paras"], 1):
            lines.append("[%s ¶%d] %s" % (k, i, p))
    open(os.path.join(out, "part%d.txt" % (n + 1)), "w", encoding="utf-8").write("\n".join(lines))
    print("part%d: %s .. %s | %d sections | %d words" % (n + 1, keys[0], keys[-1], len(keys), sum(len(p.split()) for k in keys for p in S[k]["paras"])))

# ---- sentences
ABBR = re.compile(r"\b(Mr|Mrs|Ms|Dr|St|vs|a\.m|p\.m)\.$")


def sentences(par):
    """Split a paragraph into sentences. Dialogue stays attached to its tag."""
    bits = re.split(r"(?<=[.!?])[\"”']?\s+(?=[\"“']?[A-Z])", par)
    res, buf = [], ""
    for b in bits:
        buf = (buf + " " + b).strip() if buf else b
        if ABBR.search(buf):
            continue
        res.append(buf)
        buf = ""
    if buf:
        res.append(buf)
    return res


def first_word(s):
    m = re.match(r"[\"“'‘]?([A-Za-z’']+)", s)
    return m.group(1) if m else ""


metrics, runs, longs, allsent = {}, [], [], []
for k in ORDER:
    if k == "appendix":
        continue
    sents = []
    for i, p in enumerate(S[k]["paras"], 1):
        narr = not p.lstrip().startswith(('"', "“"))
        for s in sentences(p):
            sents.append((i, s, narr))
    lens = [len(s.split()) for _, s, _ in sents]
    starts = collections.Counter(first_word(s) for _, s, narr in sents if narr)
    nn = sum(starts.values()) or 1
    # runs of narration sentences opening on the same word
    run, best = [], []
    for i, s, narr in sents:
        w = first_word(s)
        if narr and run and w == first_word(run[-1][1]):
            run.append((i, s))
        else:
            if len(run) >= 4:
                runs.append((k, len(run), first_word(run[0][1]), run[0][0], " ".join(x[1] for x in run)[:420]))
            run = [(i, s)] if narr else []
        if len(run) > len(best):
            best = list(run)
    if len(run) >= 4:
        runs.append((k, len(run), first_word(run[0][1]), run[0][0], " ".join(x[1] for x in run)[:420]))
    for i, s, narr in sents:
        n = len(s.split())
        if n >= 55:
            longs.append((k, i, n, s[:300]))
    srt = sorted(lens)
    metrics[k] = {
        "title": S[k]["title"], "words": sum(lens), "sentences": len(lens),
        "mean": round(sum(lens) / max(1, len(lens)), 1), "median": srt[len(srt) // 2] if srt else 0,
        "short_le5": round(100 * sum(1 for x in lens if x <= 5) / max(1, len(lens))),
        "long_ge30": round(100 * sum(1 for x in lens if x >= 30) / max(1, len(lens))),
        "he_pct": round(100 * (starts["He"] + starts["Elijah"]) / nn),
        "top_starts": starts.most_common(5), "longest_run": len(best),
    }
    allsent += [(k, i, s) for i, s, _ in sents]

json.dump({"metrics": metrics, "runs": runs, "longs": longs}, open(os.path.join(out, "metrics.json"), "w"), ensure_ascii=False, indent=1)

print("\nsection      words sent mean med  <=5w%  >=30w%  He/Elijah%  longest same-start run")
for k, m in metrics.items():
    print("%-12s %5d %4d %4.1f %3d %5d%% %6d%% %9d%% %6d   %s" % (k, m["words"], m["sentences"], m["mean"], m["median"], m["short_le5"], m["long_ge30"], m["he_pct"], m["longest_run"], " ".join("%s:%d" % t for t in m["top_starts"][:4])))

tot = [len(s.split()) for _, _, s in allsent]
print("\nBOOK: %d sentences, mean %.1f words, %d%% are 5 words or fewer, %d%% are 30 or more" % (len(tot), sum(tot) / len(tot), 100 * sum(1 for x in tot if x <= 5) / len(tot), 100 * sum(1 for x in tot if x >= 30) / len(tot)))

print("\nRUNS of 4+ narration sentences opening on the same word: %d" % len(runs))
for k, n, w, i, t in sorted(runs, key=lambda r: -r[1])[:25]:
    print("  %-11s ¶%-3d %dx %-6s %s" % (k, i, n, w, t[:230]))

print("\nSENTENCES of 55+ words: %d" % len(longs))
for k, i, n, t in sorted(longs, key=lambda r: -r[2])[:14]:
    print("  %-11s ¶%-3d %3dw  %s" % (k, i, n, t[:200]))

# ---- repeated phrases across the book
text = " ".join(p for k in ORDER if k != "appendix" for p in S[k]["paras"])
low = re.sub(r"[^a-z' ]", " ", text.lower().replace("’", "'"))
toks = low.split()
for n, floor, top in ((4, 12, 28), (5, 8, 22), (6, 6, 14)):
    c = collections.Counter(" ".join(toks[i:i + n]) for i in range(len(toks) - n))
    print("\nmost repeated %d-word phrases:" % n, "; ".join("%s (%d)" % kv for kv in c.most_common(top) if kv[1] >= floor))

print("\nTICS (count in the book):")
for label, pat in (("like a / like an", r"\blike an? "), ("the way (simile)", r"\bthe way (you|he|she|a|some|other|people|men|it)\b"), ("for a long time / a long time", r"\ba long (time|moment|while)\b"),
                   ("didn't say anything/a word", r"didn't say (anything|a word|a thing)"), ("looked at", r"\blooked at\b"), ("nodded", r"\bnodded\b"), ("He didn't", r"\bHe didn't\b"),
                   ("It was", r"(?<![a-z] )\bIt was\b"), ("There was/were", r"\bThere (was|were)\b"), ("just", r"\bjust\b"), ("a little", r"\ba little\b"), ("kind of", r"\bkind of\b"),
                   ("quarter turn", r"quarter turn"), ("something", r"\bsomething\b"), ("suddenly", r"\bsuddenly\b"), ("very", r"\bvery\b"), ("really", r"\breally\b"), ("And then", r"\bAnd then\b"), ("Then ", r"(?<=[.!?] )Then\b")):
    print("  %-34s %d" % (label, len(re.findall(pat, text))))

# ---- small mechanical problems
print("\nMECHANICAL:")
checks = (("double space", r"\S  +\S"), ("space before punctuation", r"\s[,.;:!?](?:\s|$)"), ("repeated word", r"\b(\w+) \1\b"), ("straight double quote", r'"'), ("curly double quote", r"[“”]"),
          ("straight apostrophe", r"\w'\w"), ("curly apostrophe", r"\w’\w"), ("three dots", r"\.\.\."), ("ellipsis char", r"…"), ("OK/Ok/ok", r"\b(OK|Ok)\b"), ("okay", r"\b[Oo]kay\b"),
          ("PorusAI", r"PorusAI"), ("Porous", r"Porous ?AI|Porus AI"), ("grey", r"\bgrey\b"), ("gray", r"\bgray\b"), ("alright", r"\b[Aa]lright\b"), ("all right", r"\b[Aa]ll right\b"),
          ("co-op", r"\bco-op\b"), ("coop/co op", r"\b(coop|co op)\b"), ("T-shirt variants", r"\b(t-shirt|tee shirt|T shirt)\b"), ("unbalanced quote paragraphs", None))
for label, pat in checks:
    hits = []
    for k in ORDER:
        for i, p in enumerate(S[k]["paras"], 1):
            if pat is None:
                if p.count('"') % 2 == 1 and not p.rstrip().endswith(('.', '?', '!', ',')) :
                    hits.append((k, i, p[:110]))
                continue
            for m in re.finditer(pat, p):
                if label == "repeated word" and m.group(1).lower() in ("that", "had", "ha", "no", "so", "very", "bye", "now", "her", "in", "on"):
                    pass
                hits.append((k, i, p[max(0, m.start() - 40):m.end() + 40]))
    line = "  %-28s %d" % (label, len(hits))
    if label in ("double space", "space before punctuation", "repeated word", "curly double quote", "curly apostrophe", "three dots", "OK/Ok/ok", "Porous", "grey", "alright", "coop/co op", "T-shirt variants", "unbalanced quote paragraphs") and hits:
        line += "  e.g. " + " | ".join("%s ¶%d: …%s…" % h for h in hits[:6])
    print(line)
