#!/usr/bin/env python3
"""The free sample as plain text, for the page at thecoffeejesus.com/book-sample.

    python3 manuscript/tools/edits-v6/sample_md.py OUT/v6.docx --before 11 > BODY.md

OUT/v6.docx is make_v6.py's .docx (run with --no-pictures). --before N stops at the heading of Chapter N,
so "--before 11" gives the front matter through Chapter 10 and the "Meanwhile" after it: the same cut as the
sample PDF. The title block and the Contents list are left out (the site builds its own from the headings).

What it writes, one block per paragraph, a blank line between blocks:
  ## Heading       an act, a chapter, a "Meanwhile", the Dedication
  * * *            a scene break (an empty paragraph in the book)
  text             a paragraph; *italic* runs keep their stars

It goes under the second --- line of studio/book-sample-chapters.md in the thecoffeejesus repository; the
site's build (scripts/build_gallery.mjs) turns it into the page. It never changes a word: the last line it
prints to stderr is the word count, to compare with the PDF build's CHECKS.md.
"""
import re
import sys

import docx


def runs_md(p):
    out, buf, it = [], [], False
    for r in p.runs:
        t = r.text.replace("\n", " ").replace("\t", " ")
        if not t:
            continue
        r_it = bool(r.italic)
        if r_it != it and buf:
            out.append(("".join(buf), it))
            buf = []
        it = r_it
        buf.append(t)
    if buf:
        out.append(("".join(buf), it))
    s = ""
    for text, italic in out:
        if italic and text.strip():
            lead = text[: len(text) - len(text.lstrip())]
            trail = text[len(text.rstrip()):]
            s += f"{lead}*{text.strip()}*{trail}"
        else:
            s += text
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    before = None
    if "--before" in sys.argv:
        before = f"Chapter {int(sys.argv[sys.argv.index('--before') + 1])}:"
    d = docx.Document(sys.argv[1])
    blocks, words, state = [], 0, "title"
    for p in d.paragraphs:
        text = p.text.replace("\xa0", " ").strip()
        heading = p.style is not None and p.style.name == "Heading 1"
        if state == "title":            # the title block, up to the Contents heading
            if heading and text == "Contents":
                state = "contents"
            continue
        if state == "contents":         # the Contents list, up to the next heading
            if not heading:
                continue
            state = "body"
        if heading:
            if before and text.startswith(before):
                break
            if "*" in text:
                sys.exit(f"a heading has a star in it: {text!r}")
            blocks.append(f"## {text}")
            words += len(text.split())
            continue
        if not text:
            blocks.append("* * *")
            continue
        if "*" in text:
            sys.exit(f"a paragraph has a star in it, which this format cannot hold: {text[:60]!r}")
        blocks.append(runs_md(p))
        words += len(text.split())
    if state != "body":
        sys.exit("expected a title block, then a 'Contents' heading, then the book")
    while blocks and blocks[-1] == "* * *":
        blocks.pop()
    print("\n\n".join(blocks))
    print(f"{words} words", file=sys.stderr)


if __name__ == "__main__":
    main()
