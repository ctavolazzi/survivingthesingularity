import importlib.util, sys
spec = importlib.util.spec_from_file_location("ps", "print_sourcing.py"); ps = importlib.util.module_from_spec(spec); spec.loader.exec_module(ps)
src = open("sample.md", encoding="utf-8").read().split("\n")
out, st, led, flags, missing = ps.convert(src, "print", "Chapter 2"); out = [l[1:] if l.startswith("\x04") else l for l in out]
text = "\n".join(out)
want = [
 'on the planet." (Source: United Nations Global Issues: Food) In this country, 30 to 40 percent goes uneaten. (Source: CDFA, Food Recovery)',
 "In 1970 the median home cost $17,000. (Source: Census, Historical Census of Housing; Census, Income Tables)",
 "The IEA estimate is 485 TWh. (Source: IEA, Key Questions on Energy and AI, 2026)",
 "As Yudkowsky, 2007 argued, intelligence is a process.",
 "*Atlas, outside the room. AI-adapted cutout from DARPA, public domain.*",
 "Money is a ritual. (Stanford AI Index 2025, chapter 1)",                      # no 'Source:' after Chapter 1
 "- Aneurin Bevan, In Place of Fear (1952). The man who launched the NHS. Chapter 5, transcribed",
 "- **Food security:** FAO, An Introduction to the Basic Concepts of Food Security (2008). The guide distinguishes availability. https://www.fao.org/4/al936e.pdf",
 "- Sellafield Ltd, Sellafield Robotics (2023), with the 2025 update. An account. https://www.gov.uk/sell https://www.gov.uk/up",
 "## Additional sources cited in the text", "## Image credits",
 "Done by hand already. (Source: CDFA again)",
 "Also by hand. (Stanford again)",
 "- CDFA, Food Recovery. https://www.cdfa.ca.gov/is/foodrecovery/",
]
def check(expected, label):
    miss = [w for w in expected if w not in text]
    print(f"{label}: {'ok' if not miss else 'FAILED'}  ({len(expected) - len(miss)}/{len(expected)} expected lines present)")
    for m in miss: print("   missing:", m[:100])
    return not miss
ok = check(want, "expected output")
bad = ps.selfcheck(src, "print", "Chapter 2")[0]; print("self-check, lines changed outside an edit:", bad)
print("links left in print output:", len(ps.LINK.findall(text)), "(want 0)")
eb, *_ = ps.convert(src, "ebook", "Chapter 2"); eb = "\n".join(eb)
print("ebook keeps every link:", len(ps.LINK.findall(eb)) == len(ps.LINK.findall("\n".join(src))), "| ebook citation:", "(Source: [CDFA, Food Recovery](https://www.cdfa.ca.gov/is/foodrecovery/))" in eb)
print()
control = check(["Money is a ritual. (Source: Stanford AI Index 2025, chapter 1)"], "CONTROL (deliberately wrong expectation, must FAIL)")
print("\nTEST RESULT:", "PASS" if ok and not bad and not control else "FAIL")
sys.exit(0 if ok and not bad and not control else 1)
