#!/usr/bin/env python3
"""bible_to_md.py READ.json  ->  Markdown on stdout.

Turns a Docs read of "Surviving the Singularity: Character Bible" into the repository copy.
Headings become # and ##, a paragraph that is bold from end to end becomes **label**, disc
bullets become "- " (indented two spaces for each nesting level) and numbered lists restart
at 1 for each list. The lines under "Real lines from v5:" are indented one level whether or
not the Doc nests them. Empty paragraphs are dropped and blank lines are put back by rule, so
the output does not depend on how the Doc was spaced.
"""
import json, sys

def main(path):
    d = json.load(open(path, encoding="utf-8"))
    d = d.get("content", d)
    tab = d["tabs"][0]["documentTab"]
    lists = tab.get("lists", {})
    out, prev, counters, under_real = [], None, {}, False
    for el in tab["body"]["content"]:
        p = el.get("paragraph")
        if not p:
            continue
        runs = [e["textRun"] for e in p["elements"] if "textRun" in e]
        text = "".join(r["content"] for r in runs).rstrip("\n")
        if not text.strip():
            continue
        style = p["paragraphStyle"].get("namedStyleType", "NORMAL_TEXT")
        bullet = p.get("bullet")
        solid = [r for r in runs if r["content"].strip()]
        bold = bool(solid) and all(r.get("textStyle", {}).get("bold") for r in solid)
        if style == "HEADING_1":
            kind, line = "h", "# " + text
        elif style == "HEADING_2":
            kind, line = "h", "## " + text
        elif bullet:
            lid, lvl = bullet["listId"], bullet.get("nestingLevel", 0)
            glyph = lists[lid]["listProperties"]["nestingLevels"][lvl]
            if glyph.get("glyphType", "").startswith("DECIMAL") or "glyphSymbol" not in glyph:
                counters[(lid, lvl)] = counters.get((lid, lvl), 0) + 1
                mark = "%d. " % counters[(lid, lvl)]
            else:
                mark = "- "
            pad = lvl + (1 if under_real and lvl == 0 else 0)
            kind, line = "li", "  " * pad + mark + text
            if lvl == 0 and text.strip() == "Real lines from v5:":
                under_real = True
        elif bold:
            kind, line = "label", "**" + text + "**"
        else:
            kind, line = "p", text
        if kind != "li":
            under_real = False
        if prev is not None and not (kind == "li" and prev in ("li", "label")):
            out.append("")
        out.append(line)
        prev = kind
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main(sys.argv[1])
