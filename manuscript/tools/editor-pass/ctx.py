"""Print the paragraphs around tagged spots, to check a reader's flag against the text.

Usage: python3 -I ctx.py SECTIONS.json "ch07:66:1:1" "ch13:109" ...
Each spot is key:paragraph[:before[:after]] (paragraph numbers start at 1).
"""
import json
import sys

S = json.load(open(sys.argv[1]))
for spot in sys.argv[2:]:
    bits = spot.split(":")
    k, n = bits[0], int(bits[1])
    before = int(bits[2]) if len(bits) > 2 else 1
    after = int(bits[3]) if len(bits) > 3 else 1
    P = S[k]["paras"]
    print("\n--- %s ¶%d (%s)" % (k, n, S[k]["title"]))
    for i in range(max(1, n - before), min(len(P), n + after) + 1):
        print("  %s¶%d %s" % (">" if i == n else " ", i, P[i - 1][:520]))
