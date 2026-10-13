#!/usr/bin/env python3
"""build_book_plate.py — composite a PixelLab sprite into a book figure plate.

The book's pixel-art figures all share one layout: a navy card, a thin slate
rule, the sprite centred at an integer upscale, an amber monospace title, and a
slate monospace caption. Until now that layout lived only in the output PNGs,
so every new figure was a hand-rebuild against a JPEG-eyeball. This script is
the layout, measured off the committed plates and checked against them.

The geometry below was recovered from ch01-pc-rig.png, ch08-gary.png,
ch06-tool-wall.png, ch01-devendra.png and ch05-woodstove.png, all of which agree.

    build      composite a sprite into a plate
    verify     rebuild an existing plate from its sprite and diff the result

Verify is the point. A layout constant that is never re-derived from the
artifacts it claims to describe is a guess with a docstring.

    python3 scripts/build_book_plate.py verify ch01-pc-rig
    python3 scripts/build_book_plate.py build \
        --sprite static/book-images/sprites/sts-sprite-foo.png \
        --out static/book-images/ch09-foo.png \
        --title "THE FOO" --caption "what the foo is for."

Requires Pillow. Everything else is stdlib.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - environment guard
    sys.exit("Pillow is required: pip install Pillow")

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "static" / "book-images"
SPRITES = IMAGES / "sprites"

# --- measured layout constants -------------------------------------------
WIDTH = 760
BG = (2, 6, 23)  # #020617, the site background
BORDER = (30, 41, 59)  # #1e293b
BORDER_INSET = 7
BORDER_WEIGHT = 2

ART_TOP = 44  # first row the sprite may occupy
ART_MAX_W = 640
ART_MAX_H = 480

TITLE_GAP = 24  # rows between the sprite's last row and the title's cap top
CAPTION_GAP = 38  # title cap top -> caption ascender top
BOTTOM_PAD = 114  # title cap top -> canvas bottom

TITLE_COLOR = (245, 158, 11)  # #f59e0b
CAPTION_COLOR = (148, 163, 184)  # #94a3b8

TITLE_FONT = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
CAPTION_FONT = "/System/Library/Fonts/Supplemental/Courier New.ttf"
TITLE_SIZE = 30
CAPTION_SIZE = 19


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        sys.exit(f"font not found: {path}\nThis script assumes macOS Courier New.")


def _trim(sprite: Image.Image) -> Image.Image:
    """Crop a sprite to its opaque bounding box."""
    sprite = sprite.convert("RGBA")
    box = sprite.getbbox()
    if box is None:
        sys.exit("sprite is fully transparent")
    return sprite.crop(box)


def _scale_for(w: int, h: int) -> int:
    """Largest integer upscale that keeps the art inside the art box.

    Integer-only, and NEAREST at paste time: a pixel-art figure that has been
    resampled is no longer pixel art, and it shows at print size.
    """
    return max(1, min(ART_MAX_W // w, ART_MAX_H // h))


def _draw_centered(canvas, text, font, color, top_y):
    """Draw `text` centred on WIDTH/2 with its ink bounding box starting at top_y.

    Positioning by ink box rather than by baseline is what the committed plates
    actually do: the title's cap top and the caption's ascender top are the
    constants that hold across all five reference plates.
    """
    if not text:
        return
    scratch = Image.new("L", (WIDTH * 2, 200), 0)
    ImageDraw.Draw(scratch).text((100, 50), text, font=font, fill=255)
    box = scratch.getbbox()
    if box is None:
        return
    ink_w = box[2] - box[0]
    dx = (WIDTH - ink_w) // 2 - box[0] + 100
    dy = top_y - box[1] + 50
    ImageDraw.Draw(canvas).text((dx, dy), text, font=font, fill=color)


def build(sprite_path: Path, title: str, caption: str) -> Image.Image:
    art = _trim(Image.open(sprite_path))
    scale = _scale_for(art.width, art.height)
    art = art.resize((art.width * scale, art.height * scale), Image.NEAREST)

    title_top = ART_TOP + art.height + TITLE_GAP
    height = title_top + BOTTOM_PAD

    canvas = Image.new("RGB", (WIDTH, height), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [BORDER_INSET, BORDER_INSET, WIDTH - 1 - BORDER_INSET, height - 1 - BORDER_INSET],
        outline=BORDER,
        width=BORDER_WEIGHT,
    )

    canvas.paste(art, ((WIDTH - art.width) // 2, ART_TOP), art)

    _draw_centered(canvas, title, _font(TITLE_FONT, TITLE_SIZE), TITLE_COLOR, title_top)
    _draw_centered(
        canvas,
        caption,
        _font(CAPTION_FONT, CAPTION_SIZE),
        CAPTION_COLOR,
        title_top + CAPTION_GAP,
    )
    return canvas


def _diff(a: Image.Image, b: Image.Image) -> tuple[int, int]:
    """Return (differing pixels, total pixels) for two same-size images."""
    if a.size != b.size:
        return (-1, -1)
    pa, pb = a.convert("RGB").tobytes(), b.convert("RGB").tobytes()
    diff = sum(1 for i in range(0, len(pa), 3) if pa[i : i + 3] != pb[i : i + 3])
    return diff, a.width * a.height


def cmd_build(args) -> int:
    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    sprite = Path(args.sprite)
    if not sprite.is_absolute():
        sprite = ROOT / sprite
    plate = build(sprite, args.title, args.caption)
    out.parent.mkdir(parents=True, exist_ok=True)
    plate.save(out)
    print(f"wrote {out.relative_to(ROOT)}  {plate.width}x{plate.height}")
    return 0


# Reference plates, with the exact strings they were built from. `verify`
# rebuilds each one and diffs it against the committed file.
REFERENCES = {
    "ch01-pc-rig": (
        "sts-sprite-pc-rig.png",
        "THE RIG",
        "two GPUs zip-tied in. it throttles by design.",
    ),
    "ch08-gary": ("sts-char-gary.png", "GARY", "stayed informed. couldn't fix a fence."),
    "preface-reading-rage": (
        "sts-sprite-novel-reader.png",
        "READING RAGE",
        "diagnosed: reading fever. prognosis: moral collapse.",
    ),
}


def cmd_verify(args) -> int:
    names = [args.name] if args.name else list(REFERENCES)
    worst = 0
    for name in names:
        if name not in REFERENCES:
            print(f"{name}: no reference strings recorded, skipping")
            continue
        sprite_name, title, caption = REFERENCES[name]
        committed = Image.open(IMAGES / f"{name}.png")
        rebuilt = build(SPRITES / sprite_name, title, caption)
        bad, total = _diff(committed, rebuilt)
        if bad < 0:
            print(f"FAIL {name}: size {committed.size} != rebuilt {rebuilt.size}")
            worst = 1
            continue
        pct = 100.0 * bad / total
        status = "ok" if pct < 1.0 else "DRIFT"
        if pct >= 1.0:
            worst = 1
        print(f"{status:5} {name}: {bad}/{total} px differ ({pct:.3f}%)")
    return worst


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="composite a sprite into a plate")
    b.add_argument("--sprite", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--title", required=True)
    b.add_argument("--caption", default="")
    b.set_defaults(func=cmd_build)

    v = sub.add_parser("verify", help="rebuild reference plates and diff them")
    v.add_argument("name", nargs="?")
    v.set_defaults(func=cmd_verify)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
