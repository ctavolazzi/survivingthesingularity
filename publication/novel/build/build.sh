#!/usr/bin/env bash
# One command to rebuild every publication file for the novel:
#
#   publication/novel/build/build.sh path/to/manuscript.docx
#
# Needs pandoc, Java (for epubcheck), poppler-utils (pdftotext, pdffonts,
# pdfimages) and the Python packages in requirements.txt:
#   pip install -r publication/novel/build/requirements.txt
#
# Files land in publication/novel/output/ with the check report CHECKS.md.
# Settings are in book.json. With no path, the newest file in
# publication/novel/source/ is used.
set -euo pipefail
exec python3 "$(dirname "$0")/build.py" "$@"
