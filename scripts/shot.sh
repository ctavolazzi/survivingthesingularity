#!/usr/bin/env bash
# Headless screenshot helper.
#
# Usage: ./scripts/shot.sh <url-or-path> <out.png> [width] [height]
#
# Two rules learned the hard way and encoded here so they are not relearned:
#
#   1. Never pass --disable-gpu. It changes rendering enough to hide real
#      layout bugs and to invent fake ones.
#   2. --window-size clamps to a 500px minimum on this macOS version, so a
#      narrow value silently produces a 500px shot and fakes mobile overflow.
#      For viewports under 500px use scripts/shot-narrow.mjs, which drives
#      Playwright to set an exact viewport with no clamp, and measures overflow
#      from inside the page rather than guessing at it.
#
# file:// CSP warnings in the console are almost always noise, not a defect.

set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TARGET="${1:?usage: shot.sh <url-or-path> <out.png> [width] [height]}"
OUT="${2:?usage: shot.sh <url-or-path> <out.png> [width] [height]}"
W="${3:-1440}"
H="${4:-1800}"

if [ "$W" -lt 500 ]; then
  echo "refusing: width $W is below the 500px clamp and would produce a false result." >&2
  echo "use scripts/shot-narrow.mjs for narrow viewports." >&2
  exit 2
fi

# Accept a bare path as well as a URL.
case "$TARGET" in
  http://*|https://*|file://*) URL="$TARGET" ;;
  *) URL="file://$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")" ;;
esac

mkdir -p "$(dirname "$OUT")"

"$CHROME" \
  --headless=new \
  --hide-scrollbars \
  --force-device-scale-factor=1 \
  --window-size="${W},${H}" \
  --screenshot="$OUT" \
  --virtual-time-budget=4000 \
  "$URL" >/dev/null 2>&1

if [ ! -s "$OUT" ]; then
  echo "FAIL: no screenshot produced for $URL" >&2
  exit 1
fi

echo "shot: $OUT  ($(sips -g pixelWidth -g pixelHeight "$OUT" 2>/dev/null | awk '/pixel/{printf "%s ", $2}'))  <- $URL"
