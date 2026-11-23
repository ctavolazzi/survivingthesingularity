"""Check today's rulings against the saved v4 text. Read-only.

Usage: python3 -I rulings_check.py V4_SECTIONS.json
Prints, for each term, the sections it appears in and the sentence around each hit.
"""
import json
import re
import sys

S = json.load(open(sys.argv[1]))
ORDER = list(S)


def hits(pattern, flags=re.I, width=110, limit=40):
    rx = re.compile(pattern, flags)
    out = []
    for k in ORDER:
        for p in S[k]["paras"]:
            for m in rx.finditer(p):
                a, b = max(0, m.start() - width), min(len(p), m.end() + width)
                out.append((k, p[a:b].replace("\n", " ")))
    return out[:limit], len(out)


def show(label, pattern, flags=re.I, width=110, limit=40):
    h, n = hits(pattern, flags, width, limit)
    print("\n=== %s  [%s]  %d hit(s)" % (label, pattern, n))
    for k, t in h:
        print("  %-12s ...%s..." % (k, t))


groups = sys.argv[2:] or ["all"]
want = lambda g: "all" in groups or g in groups

if want("control"):
    # Negative control: a string that cannot be in the book must report 0, and a known one must report > 0.
    print("control absent:", hits(r"zzqx-not-in-book")[1], "(must be 0)")
    print("control present:", hits(r"Elijah Madrone")[1], "(must be > 0)")

if want("names"):
    show("Sparrow", r"\bSparrow")
    show("Groundwork (rejected name)", r"Groundwork")
    show("Anthropic (real name must not appear as the lab)", r"Anthropic")
    show("Rod Code", r"Rod Code", limit=12)
    show("Nadzieja", r"Nadzieja|Czekaj")
    show("the Architect", r"\bArchitect\b", limit=30)
    show("Galen / Gaelen", r"Ga?e?len\b")
    show("Second Crop (old band name)", r"Second Crop")
    show("Crop Dust", r"Crop Dust", limit=8)
    show("Fisher (old stove)", r"\bFisher\b")
    show("Fishman amp", r"Fishman", limit=10)

if want("watcher"):
    show("watcher lines", r"somebody near|someone near|put somebody|put someone|have somebody|keep an eye|eyes on (him|the)|near him|watch(ing|ed)? (him|the kid|Madrone)")
    show("bought the land", r"bought the (land|parcel|acre|property)|the parcel next|adjacent parcel|next door to the co-op")
    show("cleared anyone", r"(wasn't|was not|isn't|is not) (Bidwell's|the one|a plant|the watcher|working for Bidwell)")

if want("machine"):
    show("All labor", r"All labor")
    show("Guaranteed", r"Guaranteed\.")
    show("not like you humans", r"not like you humans")
    show("womankind", r"womankind")
    show("rather be chosen", r"rather be chosen|asking for your vote")
    show("thank", r"thank(s|ed)? (her|Nadzieja|Dr\.)|want to thank")

if want("places"):
    show("California leftovers", r"\b(Ukiah|Cloverdale|Sonoma|Mendocino|Covelo|Redding|Santa Rosa|Sacramento|Humboldt|Willits|Healdsburg|Petaluma|Chico|Butte|Oroville|Lake County|Napa|Marin|Eureka|Garberville|Laytonville)\b", flags=0, limit=80)
    show("Washington", r"\b(Ardell|Kittitas|Spokane|Yakima|Ellensburg|Wenatchee|Washington|Cascades|Columbia)\b", flags=0, limit=80)
    show("three hours", r"three hours|three-hour")
    show("eight hundred miles", r"eight hundred miles|800 miles|two days('|’)? drive|two-day drive")
    show("state / county words", r"\bCalifornia\b|\bCal Fire\b|\bPG&E\b|\bCaltrans\b|\bI-5\b|\b101\b|\bOregon\b", flags=0, limit=60)

if want("dashes"):
    show("en or em dash", "[\u2013\u2014]", limit=20)
    show("banned word", r"manifesto")

if want("people"):
    show("Devendra", r"Devendra", limit=40)
    show("Tyler", r"\bTyler\b", limit=40)
    show("cousin", r"cousin")
    show("Wren", r"\bWren\b", limit=60)
    show("mothers", r"the mothers|mothers\b", limit=30)
    show("moon", r"man on the moon|on the moon")
