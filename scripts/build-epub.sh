#!/usr/bin/env bash
# Build the Surviving the Singularity EPUB + review PDF from src/lib/data/book.
# Usage: scripts/build-epub.sh [LABEL]   (default label: DRAFT)
# Output: book-build/Surviving-the-Singularity-<LABEL>.epub / .pdf / cover.png
set -euo pipefail

LABEL="${1:-DRAFT}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BOOK="$ROOT/src/lib/data/book"
OUT="$ROOT/book-build"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$OUT"

echo "==> Cover"
if [ -f "$ROOT/scripts/book-cover.png" ]; then
  cp "$ROOT/scripts/book-cover.png" "$TMP/cover.png"
else
  weasyprint "$ROOT/scripts/book-cover.html" "$TMP/cover.pdf" 2>/dev/null
  sips -s format png -z 2560 1600 "$TMP/cover.pdf" --out "$TMP/cover.png" >/dev/null
fi
cp "$TMP/cover.png" "$OUT/cover.png"

echo "==> Sections (from book.json, minus print-style index)"
FILES=$(jq -r '.sections[].file' "$BOOK/book.json" | grep -v '^18-index.md$')

mkdir -p "$TMP/images"
cp "$ROOT/static/book-images/"*.jpg "$ROOT/static/book-images/"*.png "$ROOT/static/book-images/"*.svg "$TMP/images/"

for f in $FILES; do
  prefix="${f%%-*}" # numeric prefix keeps footnote ids unique per chapter
  sed -E -e 's|\]\(/book-images/|](images/|g' \
         -e "s/\[\^([^]]+)\]/[^${prefix}-\1]/g" \
    "$BOOK/$f" > "$TMP/$f"
done

cat > "$TMP/metadata.yaml" <<'YAML'
---
title: Surviving the Singularity
subtitle: Staying agentic while AI rewrites work, money, medicine, and meaning
author: Christopher Tavolazzi
date: 2026
lang: en-US
rights: (c) 2026 Christopher Tavolazzi. All rights reserved.
---
YAML

cd "$TMP"

echo "==> EPUB"
# shellcheck disable=SC2086
pandoc metadata.yaml $FILES \
  -o "$OUT/Surviving-the-Singularity-$LABEL.epub" \
  --toc --toc-depth=1 --split-level=1 \
  --epub-cover-image=cover.png \
  --css="$ROOT/scripts/epub.css"

echo "==> Review PDF"
# shellcheck disable=SC2086
pandoc metadata.yaml $FILES \
  -o "$OUT/Surviving-the-Singularity-$LABEL.pdf" \
  --toc --toc-depth=1 \
  --pdf-engine=weasyprint \
  --css="$ROOT/scripts/book-print.css" 2>/dev/null

ls -lh "$OUT"
