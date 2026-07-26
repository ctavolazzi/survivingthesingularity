#!/usr/bin/env python3
"""Record the pixel dimensions of every chapter image.

Why this exists: the book's markdown carries no image dimensions, so the
browser cannot reserve space for a chapter image until it has downloaded it.
Every image that arrives shifts the prose below it. That is a cosmetic annoyance
while reading forward, but it makes "put me back where I was" unreliable - the
reader scrolls to a computed offset, then images above finish loading, and the
target slides thousands of pixels further down.

Emitting width/height attributes fixes it at the source: the browser reserves
the correct box before the bytes arrive, so nothing moves.

Usage:
    python3 scripts/book_image_dimensions.py          # write the JSON map
    python3 scripts/book_image_dimensions.py --check  # verify it is current

Output: src/lib/data/book/image-dimensions.json  ({ "filename.webp": [w, h] })
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "static" / "book-images"
OUT = ROOT / "src" / "lib" / "data" / "book" / "image-dimensions.json"

# SVGs are vector and already scale; they carry their own viewBox, so the
# browser sizes them without a download-and-reflow round trip.
RASTER = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def dimensions(path: Path) -> tuple[int, int] | None:
    """Pixel size via sips, which reads every raster format macOS ships with."""
    try:
        out = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
            capture_output=True, text=True, timeout=30,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    w = re.search(r"pixelWidth:\s*(\d+)", out)
    h = re.search(r"pixelHeight:\s*(\d+)", out)
    return (int(w.group(1)), int(h.group(1))) if w and h else None


def build() -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}
    for path in sorted(IMAGES.iterdir()):
        if path.suffix.lower() not in RASTER:
            continue
        size = dimensions(path)
        if size:
            result[path.name] = [size[0], size[1]]
        else:
            print(f"  warn: could not read {path.name}", file=sys.stderr)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="exit non-zero if the committed map is stale")
    args = parser.parse_args()

    fresh = build()

    if args.check:
        if not OUT.exists():
            print("image-dimensions.json is missing; run this script", file=sys.stderr)
            return 1
        current = json.loads(OUT.read_text())
        if current != fresh:
            missing = sorted(set(fresh) - set(current))
            stale = sorted(k for k in set(fresh) & set(current) if current[k] != fresh[k])
            print("image-dimensions.json is out of date", file=sys.stderr)
            if missing:
                print(f"  not recorded: {', '.join(missing)}", file=sys.stderr)
            if stale:
                print(f"  changed size: {', '.join(stale)}", file=sys.stderr)
            return 1
        print(f"image-dimensions.json is current ({len(fresh)} images)")
        return 0

    OUT.write_text(json.dumps(fresh, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(fresh)} images)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
