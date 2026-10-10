#!/usr/bin/env python3
"""Compare two sets of tiles written by audit_tiles.mjs.

Usage: compare_tiles.py TILES_DIR BEFORE_LABEL AFTER_LABEL [--boxes boxes.json]

For every page view it reports how many tiles differ, how many pixels, and
where. A pixel "differs" when any channel moves by more than 12 of 255, which
ignores compression-level noise and keeps real changes.

--boxes takes {"<viewport> <path>": [[x, y, w, h], ...]} in DOCUMENT coordinates
(the scroll position of each tile is added back). Differing pixels inside one of
those boxes are counted as expected, the rest as unexplained. Use it for regions
you changed on purpose, such as a video player or a date.
"""
import json
import sys
from PIL import Image, ImageChops

root, before, after = sys.argv[1:4]
boxes = {}
if "--boxes" in sys.argv:
    boxes = json.load(open(sys.argv[sys.argv.index("--boxes") + 1]))


def index(label):
    return {(r["path"], r["viewport"]): r["tiles"] for r in json.load(open(f"{root}/{label}/index.json"))}


def slug(p):
    return "home" if p == "/" else p.strip("/").replace("/", "-")


B, A = index(before), index(after)
total_tiles = total_diff = total_unexplained = 0
print(f"{'page':40s} {'view':8s} {'tiles':7s} {'stops':6s} differing tiles: pixels inside expected boxes / elsewhere")
for (path, vp), tb in B.items():
    ta = A.get((path, vp))
    if ta is None:
        print(f"{path:40s} {vp:8s} missing in {after}")
        continue
    n = min(len(tb), len(ta))
    known = boxes.get(f"{vp} {path}", [])
    inside = outside = tiles_differing = 0
    where = []
    for i in range(n):
        a = Image.open(f"{root}/{before}/{vp}/{slug(path)}/{i:02d}.png").convert("RGB")
        b = Image.open(f"{root}/{after}/{vp}/{slug(path)}/{i:02d}.png").convert("RGB")
        if a.size != b.size:
            where.append(f"t{i}:size")
            tiles_differing += 1
            continue
        d = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 12 else 0)
        box = d.getbbox()
        if not box:
            continue
        tiles_differing += 1
        px = d.load()
        t_in = t_out = 0
        for y in range(box[1], box[3]):
            for x in range(box[0], box[2]):
                if not px[x, y]:
                    continue
                dy = y + tb[i]
                if any(k[0] - 2 <= x <= k[0] + k[2] + 2 and k[1] - 2 <= dy <= k[1] + k[3] + 2 for k in known):
                    t_in += 1
                else:
                    t_out += 1
        inside += t_in
        outside += t_out
        if t_out:
            where.append(f"t{i}@{tb[i]}:{t_out}px x{box[0]}-{box[2]} y{box[1]}-{box[3]}")
    total_tiles += n
    total_diff += tiles_differing
    total_unexplained += outside
    same_stops = "same" if tb == ta else f"{len(tb)}/{len(ta)}"
    print(f"{path[:39]:40s} {vp:8s} {n:<7d} {same_stops:6s} {tiles_differing:2d}: {inside} / {outside}  " + " ".join(where[:4]))
print(f"\n{total_tiles} tiles compared, {total_diff} differ, {total_unexplained} differing pixels outside expected boxes")
