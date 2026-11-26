"""Make v7 of the novel: v6 (every logged v6 edit) plus the v7-only changes in ops_v7.py.

    python3 manuscript/tools/edits-v7/make_v7.py V5_READ.json OUT_DIR [--small-pictures]

v6 stays the book CT is editing; v7 is a separate copy (CT, 26 Nov).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "edits-v6"))
import make_v6 as m
from ops_v7 import OPS_V7, NOTE_START, NOTE_END, DEDICATION


def main():
    src, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    chars, attrs, images, objects = m.load(src)
    chars, attrs, images, _ = m.apply(chars, attrs, images)
    bad = m.check("".join(chars))
    if bad:
        sys.exit(f"v6 edits fail: {bad[:3]}")
    text = "".join(chars)
    a = text.index(NOTE_START); b = text.index(NOTE_END, a) + len(NOTE_END)
    note = text[a:b]
    ops = []
    for n, f, r in OPS_V7:
        if f == "":
            chars[0:0] = list(r) + ["\n"]
            attrs[0:0] = [(False, False)] * len(r) + [{"style": "NORMAL_TEXT", "align": "CENTER"}]
            images = {k + len(r) + 1: o for k, o in images.items()}
            continue
        if f is None:
            f, r = note, "Appendix\nThank You\n§H1 Dedication\n§C " + DEDICATION
        ops.append((n, f, r))
    chars, attrs, images, _ = m.apply(chars, attrs, images, ops)
    # markers: set the style of the paragraph they open, then drop them
    i = 0
    while i < len(chars):
        start = i == 0 or chars[i - 1] == "\n"
        for mark, key, val in (("§H1 ", "style", "HEADING_1"), ("§C ", "align", "CENTER")):
            if start and "".join(chars[i:i + len(mark)]) == mark:
                j = chars.index("\n", i)
                attrs[j] = dict(attrs[j]); attrs[j][key] = val
                del chars[i:i + len(mark)]; del attrs[i:i + len(mark)]
                images = {(k - len(mark) if k > i else k): o for k, o in images.items()}
        i += 1
    text = "".join(chars)
    assert "§" not in text
    (out / "v7.txt").write_text(text.replace("￼", "[picture]"))
    paras = m.paragraphs(chars, attrs)
    if "--no-docx" not in sys.argv:
        m.write_docx(paras, images, objects, out / "v7.docx", out / "images")
        print("wrote", out / "v7.docx")
    print("v7: v6 edits all pass; v7 changes applied:", ", ".join(n for n, _, _ in OPS_V7))


if __name__ == "__main__":
    main()
