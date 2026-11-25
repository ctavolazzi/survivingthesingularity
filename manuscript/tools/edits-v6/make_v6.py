"""Make v6 of the novel from a read of the v5 Doc.

    python3 manuscript/tools/edits-v6/make_v6.py V5_READ.json OUT_DIR

1. Takes the v5 Doc as if every pending suggestion were accepted (edits 1 to 86 and the follow-ups).
2. Applies edits 87 onward from ops.py, each one a find (must appear exactly once) and a replacement.
   In a replacement, "\n" starts a new paragraph and *...* is italic.
3. Checks the result against every row of manuscript/tools/edits-v5/checks.py: each edit's words must be there,
   and its removed words must be gone. It stops if any edit fails.
4. Writes OUT_DIR/v6.docx (headings, italics, bold, centered lines, the 19 pictures) to upload to Drive as the
   new Google Doc, OUT_DIR/v6.txt (plain text), and OUT_DIR/v6-read.json (a Docs-like read for verify.py).

It never calls Google. Pictures are fetched from the read's contentUri links, which expire; read the Doc again if
they fail.
--small-pictures makes the pictures 800 pixels wide, so the .docx fits under the Drive connector's limit.
"""
import json, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "edits-v5"))
from ops import OPS
from checks import C


def load(path):
    d = json.load(open(path)); d = d.get("content", d)
    tab = d["tabs"][0]["documentTab"]
    chars, attrs = [], []          # one attr per char: (italic, bold) for text, a paragraph dict for "\n"
    images = {}                    # char index of a "￼" placeholder -> object id
    for el in tab["body"]["content"]:
        p = el.get("paragraph")
        if not p:
            continue
        ps = p["paragraphStyle"]
        pa = {"style": ps.get("namedStyleType", "NORMAL_TEXT"), "align": ps.get("alignment")}
        for e in p["elements"]:
            if "inlineObjectElement" in e:
                images[len(chars)] = e["inlineObjectElement"]["inlineObjectId"]
                chars.append("￼"); attrs.append((False, False))
                continue
            tr = e.get("textRun")
            if not tr or tr.get("suggestedDeletionIds"):
                continue
            ts = tr.get("textStyle", {})
            for ch in tr["content"]:
                if ch == "\n":
                    continue
                chars.append(ch); attrs.append((bool(ts.get("italic")), bool(ts.get("bold"))))
        chars.append("\n"); attrs.append(pa)
    return chars, attrs, images, tab.get("inlineObjects", {})


def parse_markup(s):
    out, it = [], False
    for ch in s:
        if ch == "*":
            it = not it
            continue
        out.append((ch, it))
    if it:
        raise ValueError("unclosed * in: " + s[:60])
    return out


def apply(chars, attrs, images):
    log = []
    for n, find, repl in OPS:
        text = "".join(chars).replace("\xa0", " ")
        k = text.count(find)
        if k != 1:
            sys.exit(f"edit {n}: find appears {k} times: {find[:80]!r}")
        a = text.index(find); b = a + len(find)
        if any(chars[i] == "￼" for i in range(a, b)):
            sys.exit(f"edit {n}: find covers a picture")
        new_c, new_a = [], []
        for ch, it in parse_markup(repl):
            if ch == "\n":
                new_c.append("\n"); new_a.append({"style": "NORMAL_TEXT", "align": None})
            else:
                new_c.append(ch); new_a.append((it, False))
        # a paragraph mark that ends a heading keeps its style if the find ends on it
        chars[a:b] = new_c; attrs[a:b] = new_a
        shift = len(new_c) - (b - a)
        images = {(i + shift if i >= b else i): o for i, o in images.items()}
        log.append(n)
    return chars, attrs, images, log


def flat(s):
    s = re.sub(r"\n[ \t\xa0]*\n", " [break] ", s)
    return re.sub(r"\s+", " ", s)


def check(text):
    A = flat(text.replace("￼", "")); bad = []
    for n, where, have, gone in C:
        miss = [h for h in have if flat(h) not in A]
        left = [g for g in gone if flat(g) in A]
        if miss or left:
            bad.append((n, where, miss, left))
    return bad


def paragraphs(chars, attrs):
    paras, cur = [], []
    for i, (ch, at) in enumerate(zip(chars, attrs)):
        if ch == "\n":
            paras.append((at, cur)); cur = []
        else:
            cur.append((i, ch, at))
    return paras


def write_docx(paras, images, objects, out, imgdir):
    import docx
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(11)
    imgdir.mkdir(parents=True, exist_ok=True)
    for pa, runs in paras:
        style = {"HEADING_1": "Heading 1", "HEADING_2": "Heading 2"}.get(pa["style"], "Normal")
        p = d.add_paragraph(style=style)
        if pa.get("align") == "CENTER":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        groups = []
        for i, ch, at in runs:
            if ch == "￼":
                groups.append(("img", images[i])); continue
            if groups and groups[-1][0] == "txt" and groups[-1][2] == at:
                groups[-1][1].append(ch)
            else:
                groups.append(("txt", [ch], at))
        for g in groups:
            if g[0] == "img":
                oid = g[1]
                f = imgdir / f"{oid}.png"
                if not f.exists():
                    uri = objects[oid]["inlineObjectProperties"]["embeddedObject"]["imageProperties"]["contentUri"]
                    if subprocess.run(["curl", "-sS", "-L", "-f", "-o", str(f), uri]).returncode:
                        sys.exit(f"could not fetch picture {oid}; read the v5 Doc again")
                wmax, q = (800, 70) if "--small-pictures" in sys.argv else (1400, 82)
                j = imgdir / f"{oid}-{wmax}.jpg"
                if not j.exists():
                    from PIL import Image
                    im = Image.open(f).convert("RGB")
                    if im.width > wmax:
                        im = im.resize((wmax, round(im.height * wmax / im.width)), Image.LANCZOS)
                    im.save(j, "JPEG", quality=q, optimize=True)
                p.add_run().add_picture(str(j), width=Inches(6))
            else:
                r = p.add_run("".join(g[1])); r.italic = g[2][0] or None; r.bold = g[2][1] or None
    d.save(out)


def fake_read(paras):
    content = []
    for pa, runs in paras:
        els, cur, at0 = [], [], None
        for i, ch, at in runs:
            if ch == "￼":
                continue
            if cur and at != at0:
                els.append({"textRun": {"content": "".join(cur), "textStyle": {"italic": at0[0], "bold": at0[1]}}}); cur = []
            cur.append(ch); at0 = at
        if cur:
            els.append({"textRun": {"content": "".join(cur), "textStyle": {"italic": at0[0], "bold": at0[1]}}})
        els.append({"textRun": {"content": "\n", "textStyle": {}}})
        content.append({"paragraph": {"elements": els, "paragraphStyle": {"namedStyleType": pa["style"]}}})
    return {"revisionId": "local-v6", "tabs": [{"documentTab": {"body": {"content": content}}}]}


def main():
    src, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    chars, attrs, images, objects = load(src)
    chars, attrs, images, log = apply(chars, attrs, images)
    text = "".join(chars)
    bad = check(text)
    for n, where, miss, left in bad:
        print(f"FAIL {n} ({where}): missing {miss} still there {left}")
    if bad:
        sys.exit(f"{len(bad)} edits fail; nothing written")
    print(f"applied {len(log)} replacements for edits {sorted(set(log))[0]} to {sorted(set(log))[-1]}; "
          f"all {len(C)} check rows pass")
    (out / "v6.txt").write_text(text.replace("￼", "[picture]"))
    paras = paragraphs(chars, attrs)
    json.dump(fake_read(paras), open(out / "v6-read.json", "w"))
    if "--no-docx" not in sys.argv:
        write_docx(paras, images, objects, out / "v6.docx", out / "images")
        print("wrote", out / "v6.docx")


if __name__ == "__main__":
    main()
