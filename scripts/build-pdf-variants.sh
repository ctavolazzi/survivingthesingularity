#!/usr/bin/env bash
# Build the PLAIN and DELUXE PDF variants of Surviving the Singularity.
#
#   PLAIN  — pure text: no images, no color, no decoration. The reading floor.
#   DELUXE — everything weasyprint can do: running chapter headers, drop caps,
#            styled pull quotes, TOC dot leaders with live page numbers,
#            tinted code/tables, ornamental rules. The design ceiling.
#
# The shipping draft (scripts/build-epub.sh) sits between the two on purpose.
#
# Usage: scripts/build-pdf-variants.sh [LABEL]     (default label: DRAFT)
# Output: book-build/Surviving-the-Singularity-<LABEL>-PLAIN.pdf / -DELUXE.pdf
set -euo pipefail

LABEL="${1:-DRAFT}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BOOK="$ROOT/src/lib/data/book"
OUT="$ROOT/book-build"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$OUT" "$TMP/plain" "$TMP/deluxe" "$TMP/deluxe/images"

FILES=$(jq -r '.sections[].file' "$BOOK/book.json")

cp "$ROOT/static/book-images/"*.jpg "$ROOT/static/book-images/"*.png \
   "$ROOT/static/book-images/"*.svg "$TMP/deluxe/images/"

# Per-file transforms:
#   both:   unique footnote ids per chapter (numeric prefix)
#   deluxe: /book-images/ -> images/ ; standalone "> **text**" -> pull-quote div
#   plain:  images + their italic caption lines stripped ;
#           standalone "> **text**" -> its own emphatic plain paragraph
for f in $FILES; do
  prefix="${f%%-*}"
  python3 - "$BOOK/$f" "$TMP" "$f" "$prefix" <<'PY'
import re, sys
src, tmp, name, prefix = sys.argv[1:5]
raw = open(src).read()
raw = re.sub(r"\[\^([^\]]+)\]", lambda m: f"[^{prefix}-{m.group(1)}]", raw)

pull = re.compile(r"^> \*\*(.+)\*\*\s*$", re.M)

deluxe = raw.replace("](/book-images/", "](images/")
deluxe = pull.sub(lambda m: f'<div class="pullquote">{m.group(1)}</div>', deluxe)
open(f"{tmp}/deluxe/{name}", "w").write(deluxe)

lines, out, skip_caption = raw.split("\n"), [], False
for ln in lines:
    if re.match(r"^!\[.*\]\(.*\)\s*$", ln):
        skip_caption = True
        continue
    if skip_caption and re.match(r"^\*[^*].*\*\s*$", ln.strip()):
        skip_caption = False
        continue
    if ln.strip():
        skip_caption = False
    out.append(ln)
plain = "\n".join(out)
plain = pull.sub(lambda m: m.group(1), plain)
open(f"{tmp}/plain/{name}", "w").write(plain)
PY
done

for variant in plain deluxe; do
  VUP=$(printf '%s' "$variant" | tr '[:lower:]' '[:upper:]')
  cat > "$TMP/$variant/metadata.yaml" <<YAML
---
title: Surviving the Singularity
subtitle: Staying agentic while AI rewrites work, money, medicine, and meaning
author: Christopher Tavolazzi
date: '2026 &middot; <span class="version-stamp">$LABEL-$VUP</span>'
lang: en-US
rights: (c) 2026 Christopher Tavolazzi. All rights reserved.
---
YAML
  sed "s/BOOK_VERSION/$LABEL/g" "$ROOT/scripts/book-print-$variant.css" \
    > "$TMP/$variant/book-print.css"
done

LOG="$OUT/.variant-build.log"
: > "$LOG"

echo "==> PLAIN PDF"
# shellcheck disable=SC2086
(cd "$TMP/plain" && pandoc metadata.yaml $FILES \
  -o "$OUT/Surviving-the-Singularity-$LABEL-PLAIN.pdf" \
  --toc --toc-depth=1 \
  --pdf-engine=weasyprint \
  --css="$TMP/plain/book-print.css" 2>>"$LOG") \
  || { echo "PLAIN build failed; last lines of $LOG:"; tail -5 "$LOG"; exit 1; }

echo "==> DELUXE PDF"
# shellcheck disable=SC2086
(cd "$TMP/deluxe" && pandoc metadata.yaml $FILES \
  -o "$OUT/Surviving-the-Singularity-$LABEL-DELUXE.pdf" \
  --toc --toc-depth=1 \
  --pdf-engine=weasyprint \
  --css="$TMP/deluxe/book-print.css" 2>>"$LOG") \
  || { echo "DELUXE build failed; last lines of $LOG:"; tail -5 "$LOG"; exit 1; }

ls -lh "$OUT"/Surviving-the-Singularity-"$LABEL"-*.pdf
