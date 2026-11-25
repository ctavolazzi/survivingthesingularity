#!/usr/bin/env python3
"""Build the publication files for the novel from one manuscript file.

    python3 publication/novel/build/build.py SOURCE

SOURCE is the manuscript as a .docx (File > Download > Microsoft Word in Google
Docs) or the JSON the Google Docs connector returns for the Doc. The words are
never edited here: this script only lays them out and then checks every output
against the source text (see check.py, run automatically at the end).

Settings (version label, copyright lines, cover, scene-break mark) are in
book.json next to this file. Outputs go to publication/novel/output/.
"""
import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOVEL = HERE.parent
REPO = NOVEL.parent.parent
WORK = NOVEL / "work"
OUT = NOVEL / "output"
SRC_CACHE = NOVEL / "source"
CFG = json.loads((HERE / "book.json").read_text(encoding="utf-8"))

# KDP minimum inside margin by page count, plus 0.125in so text clears the spine.
GUTTERS = [(150, 0.375), (300, 0.5), (500, 0.625), (700, 0.75), (828, 0.875)]
GUTTER_EXTRA = 0.125


def copyright_lines():
    labels = {"paperback": "paperback", "large_print": "large print paperback", "ebook": "ebook"}
    isbns = [f"ISBN {v} ({labels[k]})" for k, v in CFG.get("isbn", {}).items() if v]
    out = []
    for line in CFG["copyright_page"]:
        out += isbns if line == "{ISBN}" else [line]
    return out


def die(msg):
    sys.exit(f"build: {msg}")


# ---------------------------------------------------------------- ingest

def merge_runs(runs):
    out = []
    for text, it, bd in runs:
        if not text:
            continue
        if out and out[-1][1] == it and out[-1][2] == bd:
            out[-1][0] += text
        else:
            out.append([text, bool(it), bool(bd)])
    return out


def paras_from_google_json(path, imgdir):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    doc = data.get("content", data)
    tab = doc["tabs"][0]["documentTab"] if "tabs" in doc else doc
    objects = tab.get("inlineObjects", {})
    paras = []
    for el in tab["body"]["content"]:
        p = el.get("paragraph")
        if not p:
            continue
        style = p["paragraphStyle"].get("namedStyleType", "NORMAL_TEXT")
        kind = {"HEADING_1": "h1", "HEADING_2": "h2"}.get(style, "p")
        runs, images = [], []
        for e in p["elements"]:
            if "textRun" in e:
                tr = e["textRun"]
                if tr.get("suggestedInsertionIds") or tr.get("suggestedDeletionIds"):
                    die("the Doc has pending suggestions; accept or reject them first")
                ts = tr.get("textStyle", {})
                runs.append([tr["content"].replace("\n", "").replace("\x0b", " "),
                             ts.get("italic", False), ts.get("bold", False)])
            elif "inlineObjectElement" in e:
                oid = e["inlineObjectElement"]["inlineObjectId"]
                cached = SRC_CACHE / "images" / f"{oid}.png"
                if not CFG.get("include_pictures", True):
                    images.append(b"")
                    continue
                if not cached.exists():
                    uri = objects[oid]["inlineObjectProperties"]["embeddedObject"]["imageProperties"]["contentUri"]
                    cached.parent.mkdir(parents=True, exist_ok=True)
                    r = subprocess.run(["curl", "-sS", "-L", "-f", "-o", str(cached), uri])
                    if r.returncode:
                        die(f"could not download picture {oid} (the Doc's picture links expire; read the Doc again)")
                images.append(cached.read_bytes())
        paras.append({"kind": kind, "runs": merge_runs(runs), "images": images})
    return paras


def paras_from_docx(path, imgdir):
    import docx
    from docx.text.run import Run
    d = docx.Document(str(path))
    paras = []
    for p in d.paragraphs:
        name = p.style.name if p.style is not None else ""
        kind = {"Heading 1": "h1", "Heading 2": "h2"}.get(name, "p")
        style_it = bool(p.style.font.italic) if p.style is not None else False
        style_bd = bool(p.style.font.bold) if (p.style is not None and kind == "p") else False
        runs, images = [], []
        for item in p.iter_inner_content():
            for r in ([item] if isinstance(item, Run) else item.runs):
                for rid in r._r.xpath(".//a:blip/@r:embed"):
                    images.append(d.part.related_parts[rid].blob)
                it = r.italic if r.italic is not None else style_it
                bd = r.bold if r.bold is not None else style_bd
                runs.append([r.text.replace("\n", " ").replace("\t", " "), it, bd and kind == "p"])
        paras.append({"kind": kind, "runs": merge_runs(runs), "images": images})
    return paras


def plain(runs):
    return "".join(r[0] for r in runs)


def structure(paras):
    """Turn the flat paragraph list into title block, contents list and sections."""
    from PIL import Image
    import io
    imgdir = WORK / "images"
    shutil.rmtree(imgdir, ignore_errors=True)
    imgdir.mkdir(parents=True)
    shutil.rmtree(WORK / "epub", ignore_errors=True)
    (WORK / "epub" / "images").mkdir(parents=True)

    blocks, nimg, left_out = [], 0, 0
    for p in paras:
        for blob in p["images"]:
            if not CFG.get("include_pictures", True):
                left_out += 1
                continue
            nimg += 1
            name = f"fig-{nimg:02d}.jpg"
            im = Image.open(io.BytesIO(blob)).convert("RGB")
            im.save(imgdir / name, "JPEG", quality=CFG["image_quality"], optimize=True)
            small = WORK / "epub" / "images"
            small.mkdir(parents=True, exist_ok=True)
            w = min(im.width, CFG["epub_image_width"])
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(
                small / name, "JPEG", quality=CFG["epub_image_quality"], optimize=True)
            blocks.append({"t": "img", "src": name, "w": im.width, "h": im.height})
        text = plain(p["runs"])
        if text.strip(" \xa0") == "":
            if not p["images"] and p["kind"] == "p":
                blocks.append({"t": "break"})
            continue
        blocks.append({"t": p["kind"], "runs": p["runs"]})

    h1s = [i for i, b in enumerate(blocks) if b["t"] == "h1"]
    if len(h1s) < 3 or plain(blocks[h1s[1]]["runs"]).strip() != "Contents":
        die("expected the manuscript to open with a title heading, then a 'Contents' heading")
    title_block = [b for b in blocks[:h1s[1]] if b["t"] in ("h1", "p")]
    if title_block[0]["t"] != "h1" or len(title_block) < 2:
        die("expected the title heading first, then the author line")
    title = plain(title_block[0]["runs"]).strip()
    if title.casefold() != CFG["title"].casefold():
        die(f"manuscript title {title!r} does not match book.json title {CFG['title']!r}")
    author = plain(title_block[-1]["runs"]).strip()
    toc = [{"text": plain(b["runs"]).strip(), "strong": all(r[2] for r in b["runs"])}
           for b in blocks[h1s[1] + 1:h1s[2]] if b["t"] == "p"]

    sections = []
    for n, start in enumerate(h1s[2:]):
        end = h1s[n + 3] if n + 3 < len(h1s) else len(blocks)
        heading = plain(blocks[start]["runs"]).strip()
        m = re.match(r"Chapter (\d+):", heading)
        kind = "chapter" if m else "act" if heading.startswith("Act ") else \
            "meanwhile" if heading == "Meanwhile" else "matter"
        body = blocks[start + 1:end]
        # A blank line next to a heading, or doubled, is not a scene break.
        clean = []
        for b in body:
            if b["t"] == "break" and (not clean or clean[-1]["t"] in ("break", "h2")):
                continue
            if b["t"] == "h2" and clean and clean[-1]["t"] == "break":
                clean.pop()
            clean.append(b)
        while clean and clean[-1]["t"] == "break":
            clean.pop()
        sections.append({"id": f"sec-{n + 1:02d}", "kind": kind, "title": heading,
                         "title_runs": blocks[start]["runs"],
                         "chapter": int(m.group(1)) if m else None, "blocks": clean})
    if [t["text"] for t in toc] != [s["title"] for s in sections]:
        die("the Contents list in the manuscript does not match the headings:\n" + "\n".join(
            f"  list: {a!r}  heading: {b!r}" for a, b in
            zip([t["text"] for t in toc], [s["title"] for s in sections]) if a != b))
    bio = CFG.get("about_author")
    if bio:
        sections.append({"id": f"sec-{len(sections) + 1:02d}", "kind": "matter", "title": bio["title"],
                         "title_runs": [[bio["title"], False, False]], "chapter": None, "added": True,
                         "blocks": [{"t": "p", "runs": [[t, False, False]]} for t in bio["paragraphs"]]})
        toc.append({"text": bio["title"], "strong": False, "added": True})
    return {"copyright_lines": copyright_lines(),
            "title_display": title, "title_block": title_block, "author": author,
            "toc": toc, "sections": sections, "images": nimg, "pictures_left_out": left_out}


def ingest(source):
    source = Path(source)
    if not source.exists():
        die(f"no such file: {source}")
    WORK.mkdir(exist_ok=True)
    reader = paras_from_docx if source.suffix.lower() == ".docx" else paras_from_google_json
    model = structure(reader(source, WORK / "images"))
    model["source"] = str(source)
    (WORK / "model.json").write_text(json.dumps(model, ensure_ascii=False, indent=1), encoding="utf-8")
    return model


# ---------------------------------------------------------------- html

def esc(s):
    return html.escape(s, quote=False).replace("\xa0", "&#160;")


def inline(runs):
    out = []
    for text, it, bd in runs:
        s = esc(text)
        if it:
            s = f"<em>{s}</em>"
        if bd:
            s = f"<strong>{s}</strong>"
        out.append(s)
    return "".join(out)


def sample_sections(model):
    last = max(i for i, s in enumerate(model["sections"])
               if s["chapter"] is not None and s["chapter"] < CFG["sample_chapters"])
    return model["sections"][:last + 1]


def toc_pairs(model, sections):
    """Pair each line of the manuscript's Contents list with its section, in order."""
    titles = [s["title"] for s in model["sections"]]
    if [t["text"] for t in model["toc"]] != titles:
        die("the Contents list in the manuscript does not match the headings:\n" + "\n".join(
            f"  list: {a!r}  heading: {b!r}" for a, b in
            zip([t["text"] for t in model["toc"]], titles) if a != b))
    keep = {s["id"] for s in sections}
    return [(t, s) for t, s in zip(model["toc"], model["sections"]) if s["id"] in keep]


def body_html(sections, with_classes=True):
    out = []
    prev_kind = None
    first = True
    for s in sections:
        cls = [s["kind"]]
        if prev_kind == "act" or s["title"] in ("About This Book", "Afterword", "Appendix", "About the Author"):
            cls.append("recto")
        if first:
            cls += ["recto", "pageone"]
            first = False
        out.append(f'<section class="{" ".join(cls)}">' if with_classes else "")
        out.append(f'<h1 class="sec" id="{s["id"]}">{inline(s["title_runs"])}</h1>')
        for b in s["blocks"]:
            if b["t"] == "p":
                out.append(f"<p>{inline(b['runs'])}</p>")
            elif b["t"] == "h2":
                out.append(f"<h2>{inline(b['runs'])}</h2>")
            elif b["t"] == "break":
                out.append(f'<div class="break"><p>{esc(CFG["scene_break"])}</p></div>')
            elif b["t"] == "img":
                out.append(f'<div class="art"><p><img src="images/{b["src"]}" alt="" /></p></div>')
        out.append("</section>" if with_classes else "")
        prev_kind = s["kind"]
    return "\n".join(out)


def title_html(model):
    tb = model["title_block"]
    out = [f'<h1 class="book-title">{inline(tb[0]["runs"])}</h1>']
    for b in tb[1:-1]:
        out.append(f'<p class="subtitle">{inline(b["runs"])}</p>')
    out.append(f'<p class="author">{inline(tb[-1]["runs"])}</p>')
    return "\n".join(out)


def copyright_html():
    return "\n".join(f"<p>{esc(line)}</p>" for line in copyright_lines())


def css(names, **vars):
    text = "\n".join((HERE / "css" / n).read_text(encoding="utf-8") for n in names)
    vars.setdefault("FONTS", (REPO / CFG["fonts"]).as_uri())
    vars.setdefault("TITLE", CFG["title"])
    for k, v in vars.items():
        text = text.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{\w+\}\}", text)
    if left:
        die(f"unset stylesheet values: {sorted(set(left))}")
    return text


def pdf_html(model, sections, style, cover=None):
    toc = "\n".join(
        f'<li class="{"strong" if t["strong"] else ""}"><a href="#{s["id"]}">{esc(t["text"])}</a></li>'
        for t, s in toc_pairs(model, sections))
    cover_html = f'<section class="cover"><img src="{cover}" alt="" /></section>' if cover else ""
    return f"""<!DOCTYPE html>
<html lang="{CFG['language']}"><head><meta charset="utf-8" />
<title>{esc(CFG['title'])}</title>
<meta name="author" content="{esc(model['author'])}" />
<style>{style}</style></head><body>
{cover_html}
<section class="titlepage">{title_html(model)}</section>
<section class="copyright">{copyright_html()}</section>
<section class="contents"><h1>Contents</h1><ul class="toc">{toc}</ul></section>
{body_html(sections)}
</body></html>"""


# ---------------------------------------------------------------- pdf

def render_pdf(html_text, target, name):
    from weasyprint import HTML
    src = WORK / f"{name}.html"
    src.write_text(html_text, encoding="utf-8")
    doc = HTML(filename=str(src)).render()
    doc.write_pdf(str(target))
    return len(doc.pages)


def gutter_for(pages):
    for limit, inch in GUTTERS:
        if pages <= limit:
            return inch + GUTTER_EXTRA
    die(f"{pages} pages is over KDP's 828-page limit for this trim")


def build_print(model, sections, target, name, size, lead, align, hyphens):
    """6 x 9 in paperback interior. Re-renders until the gutter fits the page count."""
    gutter, spec = 0.75, None
    for _ in range(4):
        spec = dict(W="6in", H="9in", TOP="0.8in", BOTTOM="0.8in", OUTER="0.55in",
                    INNER=f"{gutter}in", SIZE=size, LEAD=lead, ALIGN=align,
                    HYPHENS=hyphens, ARTW="88%")
        pages = render_pdf(pdf_html(model, sections, css(["common.css", "print.css"], **spec)), target, name)
        need = gutter_for(pages)
        if abs(need - gutter) < 1e-6:
            break
        gutter = need
    spec["pages"] = pages
    spec["kdp_min_inner_in"] = gutter - GUTTER_EXTRA
    return spec


def build_reader(model, sections, target, name):
    cover = (WORK / "cover.jpg").as_uri() if (WORK / "cover.jpg").exists() else None
    style = css(["common.css", "reader.css"], SIZE="12pt", LEAD="1.5", ALIGN="justify",
                HYPHENS="auto", ARTW="80%")
    pages = render_pdf(pdf_html(model, sections, style, cover), target, name)
    return {"pages": pages}


# ---------------------------------------------------------------- epub / docx

def pandoc(args):
    r = subprocess.run(["pandoc", *args], capture_output=True, text=True)
    if r.returncode:
        die("pandoc failed:\n" + r.stderr)
    if r.stderr.strip():
        print(r.stderr.strip())


def build_epub(model, sections, target, name, ident):
    src = WORK / f"{name}.html"
    src.write_text(f'<!DOCTYPE html><html lang="{CFG["language"]}"><head><meta charset="utf-8" />'
                   f"<title>{esc(CFG['title'])}</title></head><body>\n"
                   f"{body_html(sections, with_classes=False)}\n</body></html>", encoding="utf-8")
    # pandoc's own EPUB page template, with the title page replaced by the
    # manuscript's title block followed by the copyright page.
    tpl = subprocess.run(["pandoc", "-D", "epub3"], capture_output=True, text=True, check=True).stdout
    front = (f'<section epub:type="titlepage" class="titlepage">\n{title_html(model)}\n'
             f'<div class="copyright" epub:type="copyright-page">\n{copyright_html()}\n</div>\n</section>')
    start = tpl.index('<section epub:type="titlepage"')
    end = tpl.index("</section>", start) + len("</section>")
    tpl = tpl[:start] + front.replace("$", "$$") + tpl[end:]
    (WORK / "epub-template.html").write_text(tpl, encoding="utf-8")
    args = [str(src), "-f", "html", "-t", "epub3", "-o", str(target),
            "--toc", "--toc-depth=1", "--split-level=1",
            "--template", str(WORK / "epub-template.html"),
            "--css", str(HERE / "css" / "epub.css"),
            "--resource-path", str(WORK / "epub"),
            "-M", f"title={CFG['title']}", "-M", f"author={model['author']}",
            "-M", f"lang={CFG['language']}", "-M", "toc-title=Contents",
            "-M", "rights=" + CFG["copyright_page"][1] + ". All rights reserved.",
            "-M", f"identifier=urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, ident)}"]
    if (WORK / "cover.jpg").exists():
        args += ["--epub-cover-image", str(WORK / "cover.jpg")]
    pandoc(args)


def build_docx(model, sections, target, name):
    toc = "\n".join(
        f'<p>{"<strong>" if t["strong"] else ""}<a href="#{s["id"]}">{esc(t["text"])}</a>'
        f'{"</strong>" if t["strong"] else ""}</p>' for t, s in toc_pairs(model, sections))
    tb = model["title_block"]
    front = [f'<div custom-style="Title"><p>{inline(tb[0]["runs"])}</p></div>']
    front += [f'<div custom-style="Subtitle"><p>{inline(b["runs"])}</p></div>' for b in tb[1:-1]]
    front.append(f'<div custom-style="Author"><p>{inline(tb[-1]["runs"])}</p></div>')
    lines = copyright_lines()
    front.append(f'<div custom-style="Copyright First"><p>{esc(lines[0])}</p></div>')
    front += [f'<div custom-style="Copyright"><p>{esc(l)}</p></div>' for l in lines[1:]]
    body = body_html(sections, with_classes=False)
    body = body.replace('<div class="break">', '<div custom-style="Scene Break">')
    body = body.replace('<div class="art">', '<div custom-style="Picture">')
    src = WORK / f"{name}.html"
    src.write_text(f'<!DOCTYPE html><html lang="{CFG["language"]}"><head><meta charset="utf-8" />'
                   "</head><body>\n" + "\n".join(front) +
                   f"\n<h1>Contents</h1>\n{toc}\n{body}\n</body></html>", encoding="utf-8")
    pandoc([str(src), "-f", "html", "-t", "docx", "-o", str(target), "--resource-path", str(WORK),
            "-M", f"lang={CFG['language']}"])
    style_docx(target, model["author"])


def style_docx(path, author):
    """Plain, KDP-friendly Word styles: one font, real headings, page break per chapter."""
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
    from docx.shared import Pt, Inches, RGBColor
    d = docx.Document(str(path))
    black = RGBColor(0, 0, 0)

    def st(name, size=12, bold=None, italic=None, align=None, indent=None, before=0, after=0,
           page_break=None, keep=None):
        try:
            s = d.styles[name]
        except KeyError:
            return
        s.font.name, s.font.size, s.font.color.rgb = "Times New Roman", Pt(size), black
        rpr = s.element.get_or_add_rPr()
        for f in rpr.findall(docx.oxml.ns.qn("w:rFonts")):
            for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
                f.set(docx.oxml.ns.qn(a), "Times New Roman")
            for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
                f.attrib.pop(docx.oxml.ns.qn(a), None)
        if bold is not None:
            s.font.bold = bold
        if italic is not None:
            s.font.italic = italic
        pf = s.paragraph_format
        pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), 1.15
        if align is not None:
            pf.alignment = align
        if indent is not None:
            pf.first_line_indent = Inches(indent)
        if page_break is not None:
            pf.page_break_before = page_break
        if keep is not None:
            pf.keep_with_next = keep

    st("Normal")
    st("Body Text", indent=0.3)
    st("First Paragraph", indent=0)
    st("Compact", indent=0)
    st("Heading 1", size=18, bold=True, italic=False, align=AL.CENTER, before=72, after=36,
       page_break=True, keep=True)
    st("Heading 2", size=13, bold=True, italic=False, before=18, after=8, keep=True)
    st("Title", size=28, bold=True, align=AL.CENTER, before=180, after=12)
    st("Subtitle", size=14, align=AL.CENTER, after=72)
    st("Author", size=14, align=AL.CENTER)
    st("Copyright First", size=10, before=200, after=8, page_break=True)
    st("Copyright", size=10, after=8)
    st("Scene Break", align=AL.CENTER, before=12, after=12, keep=True)
    st("Picture", align=AL.CENTER, before=12, after=12)
    for name in ("Hyperlink",):
        try:
            d.styles[name].font.color.rgb = black
            d.styles[name].font.underline = False
        except KeyError:
            pass
    d.core_properties.title, d.core_properties.author = CFG["title"], author
    d.save(str(path))


# ---------------------------------------------------------------- main

def prepare_cover():
    from PIL import Image
    src = REPO / CFG["cover"] if CFG.get("cover") else None
    target = WORK / "cover.jpg"
    target.unlink(missing_ok=True)
    if src and src.exists():
        im = Image.open(src).convert("RGB")
        im.save(WORK / "cover-art.jpg", "JPEG", quality=95)
        w, h = CFG["kindle_cover_px"]
        # Kindle's recommended size. The title sits at the left edge of the art,
        # so the art is scaled to full height and any extra width comes off the right.
        scaled = im.resize((max(w, round(im.width * h / im.height)), h), Image.LANCZOS)
        scaled.crop((0, 0, w, h)).save(target, "JPEG", quality=92, optimize=True)
        shutil.copy(target, OUT / f"{CFG['slug']}-{CFG['version']}-kindle-cover.jpg")


def spine_title_image(ink):
    """Cut the title's own letters out of the cover art and set them on one line.

    The front title is part of the picture, so there is no font file to reuse. This keeps
    the spine in the same lettering. Returns the image path, or None when not configured.
    """
    import numpy as np
    from PIL import Image
    cfg = CFG.get("spine_title_from_art")
    if not cfg:
        return None
    box, k = cfg["box"], 4
    art = Image.open(REPO / CFG["cover"]).convert("RGB").crop(box)
    big = np.asarray(art.resize((art.width * k, art.height * k), Image.LANCZOS)).astype(float)
    r, g, b = big[..., 0], big[..., 1], big[..., 2]
    alpha = np.clip((r - 195) / 40, 0, 1) * np.clip((g - 185) / 40, 0, 1) * np.clip((b - 120) / 50, 0, 1)
    rows = alpha.sum(1)
    ys = np.where(rows > rows.max() * 0.02)[0]
    lo = ys.min() + (ys.max() - ys.min()) // 4
    hi = ys.min() + (ys.max() - ys.min()) * 3 // 5
    split = lo + int(np.argmin(rows[lo:hi]))

    def line(y0, y1):
        m = alpha[y0:y1]
        cols, rws = np.where(m.sum(0) > 2)[0], np.where(m.sum(1) > 2)[0]
        return m[rws.min():rws.max() + 1, cols.min():cols.max() + 1]

    def cap(m):
        t = np.where(m.sum(1) > m.sum(1).max() * 0.25)[0]
        return t.max() - t.min()

    l1, l2 = line(ys.min(), split), line(split, ys.max() + 1)
    scale = cap(l2) / cap(l1)
    a = Image.fromarray((l1 * 255).astype("uint8")).resize(
        (int(l1.shape[1] * scale), int(l1.shape[0] * scale)), Image.LANCZOS)
    c = Image.fromarray((l2 * 255).astype("uint8"))
    gap = int(cap(l2) * 0.75)
    mask = Image.new("L", (a.width + gap + c.width, max(a.height, c.height)), 0)
    mask.paste(a, (0, 0))
    mask.paste(c, (a.width + gap, 0))
    rgb = tuple(int(ink[i:i + 2], 16) for i in (1, 3, 5))
    out = Image.new("RGBA", mask.size, rgb + (255,))
    out.putalpha(mask)
    path = WORK / "spine-title.png"
    out.save(path)
    return path, mask.width / mask.height


def build_wrap(pages, target, name, model):
    """Full paperback cover for KDP: back, spine, front on one sheet with 0.125in bleed.

    The back and spine sit on the front art mirrored, blurred and tinted, so the colour
    runs round the spine. The white box at the lower right of the back is left empty:
    KDP prints the ISBN barcode there.
    """
    from PIL import Image, ImageFilter, ImageOps
    from weasyprint import HTML
    per_page = {"white": 0.002252, "cream": 0.0025}[CFG["paper"]]
    spine = round(pages * per_page, 4)
    bleed, tw, th = 0.125, 6.0, 9.0
    width, height = bleed + tw + spine + tw + bleed, th + 2 * bleed
    col, bc = CFG["cover_colors"], CFG["back_cover"]
    fonts = (REPO / CFG["fonts"]).as_uri()

    art = Image.open(WORK / "cover-art.jpg")
    px_h = 1400
    px_w = round(px_h * (bleed + tw + spine) / height)
    bg = ImageOps.mirror(art)
    bg = bg.resize((max(px_w, round(bg.width * px_h / bg.height)), px_h))
    bg = bg.crop((bg.width - px_w, 0, bg.width, px_h)).filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(bg, Image.new("RGB", bg.size, tuple(col["tint"])), 0.80)
    bg.save(WORK / f"{name}-back.jpg", quality=92)

    cls = {"p": "", "turn": ' class="turn"', "close": ' class="close"'}
    body = "".join(f"<p{cls[k]}>{esc(t)}</p>" for k, t in bc["blocks"])
    photo = REPO / bc["author_photo"]
    photo_html = f'<img src="{photo.as_uri()}" alt="" />' if photo.exists() else ""
    cut = spine_title_image(col["spine_title"])
    title_h = min(0.30, spine - 0.2)
    if cut:
        title_html = (f'<img class="st" src="{cut[0].as_uri()}" alt="{esc(CFG["title"])}" '
                      f'style="height:{title_h}in;top:{(spine - title_h) / 2}in" />')
    else:
        title_html = f'<span class="st">{esc(CFG["title"])}</span>'
    spine_html = (f'<div class="spine">{title_html}<span class="sa">{esc(model["author"])}</span></div>'
                  if pages >= 80 else "")
    doc = f"""<!DOCTYPE html><html lang="{CFG['language']}"><head><meta charset="utf-8" />
<title>{esc(CFG['title'])} cover</title><style>
@font-face {{ font-family: S; src: url("{fonts}/SourceSerif4-Regular.otf"); }}
@font-face {{ font-family: S; font-style: italic; src: url("{fonts}/SourceSerif4-It.otf"); }}
@font-face {{ font-family: S; font-weight: 600; src: url("{fonts}/SourceSerif4-Semibold.otf"); }}
@font-face {{ font-family: S; font-weight: 700; src: url("{(HERE / 'fonts').as_uri()}/SourceSerif4-Bold.otf"); }}
@font-face {{ font-family: N; src: url("{fonts}/SourceSansPro-Regular.otf"); }}
@font-face {{ font-family: N; font-weight: 600; src: url("{fonts}/SourceSansPro-Semibold.otf"); }}
@page {{ size: {width}in {height}in; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
body {{ width: {width}in; height: {height}in; position: relative; overflow: hidden; font-family: S; color: {col['ink']}; }}
.bg {{ position: absolute; left: 0; top: 0; width: {bleed + tw + spine}in; height: {height}in; }}
.front {{ position: absolute; top: 0; left: {bleed + tw + spine}in; width: {tw + bleed}in; height: {height}in; overflow: hidden; }}
.front img {{ height: {height}in; display: block; }}
.back {{ position: absolute; left: {bleed + 0.62}in; top: {bleed + 0.62}in; width: {tw - 1.24}in; }}
.label {{ font-family: N; font-weight: 600; font-size: 8.5pt; letter-spacing: 0.22em; text-transform: uppercase;
          color: {col['accent']}; margin-bottom: 0.2in; }}
.hl {{ font-weight: 600; font-size: 23pt; line-height: 1.16; margin-bottom: 0.22in; white-space: nowrap; }}
.rule {{ width: 0.9in; height: 2.5pt; background: {col['accent']}; margin-bottom: 0.24in; }}
p {{ font-size: 10.8pt; line-height: 1.5; margin: 0 0 0.7em; }}
p.turn {{ font-weight: 600; font-size: 16pt; line-height: 1.25; margin: 0.75em 0 0.8em; color: {col['accent']}; }}
p.close {{ font-style: italic; font-size: 13pt; line-height: 1.4; margin-top: 1em; }}
p.close + p.close {{ margin-top: 0.35em; }}
p.turn + p.turn {{ margin-top: -0.35em; }}
.foot {{ position: absolute; left: {bleed + 0.62}in; bottom: {bleed + 0.38}in; width: 2.7in; min-height: 0.8in;
         padding-left: 0.95in; box-sizing: border-box; font-family: N; font-size: 8.3pt; line-height: 1.4; color: {col['soft']}; }}
.foot img {{ position: absolute; left: 0; top: 0.02in; width: 0.8in; height: 0.8in; border-radius: 50%; }}
.foot b {{ font-weight: 600; color: {col['ink']}; font-size: 9pt; letter-spacing: 0.04em; text-transform: uppercase; }}
.foot .web {{ margin-top: 0.07in; color: {col['accent']}; font-weight: 600; letter-spacing: 0.05em; }}
.code {{ position: absolute; left: {bleed + tw - 0.25 - 2.0}in; bottom: {bleed + 0.25}in; width: 2in; height: 1.2in; background: #fff; }}
.spine {{ position: absolute; left: {bleed + tw + spine}in; top: 0; width: {height}in; height: {spine}in;
          transform-origin: 0 0; transform: rotate(90deg); background: {col['spine_band']}; line-height: {spine}in;
          white-space: nowrap; }}
.spine img.st {{ position: absolute; left: {bleed + 0.55}in; }}
.spine span.st {{ position: absolute; left: {bleed + 0.55}in; top: 0; font-weight: 700; text-transform: uppercase;
              font-size: {min(21, round((spine - 0.14) * 72 * 0.55, 1))}pt; letter-spacing: 0.1em; color: {col['spine_title']}; }}
.spine .sa {{ position: absolute; right: {bleed + 0.55}in; top: 0; font-family: N; font-weight: 600;
              font-size: {min(9.5, round((spine - 0.14) * 72 * 0.26, 1))}pt; letter-spacing: 0.2em; text-transform: uppercase;
              color: {col['spine_author']}; }}
</style></head><body>
<img class="bg" src="{(WORK / f'{name}-back.jpg').as_uri()}" alt="" />
<div class="back">
<div class="label">{esc(bc['label'])}</div>
<div class="hl">{'<br />'.join(esc(l) for l in bc['headline'])}</div>
<div class="rule"></div>
{body}
</div>
<div class="foot">{photo_html}<b>{esc(bc['author_name'])}</b><br />{esc(bc['author_line'])}<div class="web">{esc(bc['website'])}</div></div>
<div class="code"></div>
{spine_html}
<div class="front"><img src="{(WORK / 'cover-art.jpg').as_uri()}" alt="" /></div>
</body></html>"""
    src = WORK / f"{name}.html"
    src.write_text(doc, encoding="utf-8")
    HTML(filename=str(src)).write_pdf(str(target))
    return {"kind": "cover", "pages": pages, "spine_in": spine, "width_in": round(width, 4), "height_in": height}


def write_listing(specs, base):
    """KDP-LISTING.md: the listing copy from listing.md with this build's numbers filled in."""
    tpl = HERE / "listing.md"
    pb, lp = specs.get(f"{base}-print-6x9.pdf"), specs.get(f"{base}-large-print-6x9.pdf")
    cv, lcv = specs.get(f"{base}-paperback-cover.pdf"), specs.get(f"{base}-large-print-cover.pdf")
    if not (tpl.exists() and pb and lp and cv and lcv):
        return
    cost = lambda n: 1.00 + 0.012 * n  # KDP US black ink, 110 to 828 pages
    vals = {"PAGES": pb["pages"], "LP_PAGES": lp["pages"], "SPINE": f"{cv['spine_in']:.3f}",
            "LP_SPINE": f"{lcv['spine_in']:.3f}", "WRAP": f"{cv['width_in']:.3f} x {cv['height_in']}",
            "COST": f"{cost(pb['pages']):.2f}", "MIN": f"{cost(pb['pages']) / 0.6:.2f}",
            "LP_COST": f"{cost(lp['pages']):.2f}", "LP_MIN": f"{cost(lp['pages']) / 0.6:.2f}",
            "PAPER": CFG["paper"],
            "BACK": "\n\n".join([" ".join(CFG["back_cover"]["headline"])] + [t for _, t in CFG["back_cover"]["blocks"]]), "BIO": "\n\n".join(CFG["about_author"]["paragraphs"]),
            "VERSION": CFG["version"]}
    text = tpl.read_text(encoding="utf-8")
    for k, v in vals.items():
        text = text.replace("{{" + k + "}}", str(v))
    (OUT / "KDP-LISTING.md").write_text(text, encoding="utf-8")


def default_source():
    for pattern in ("*.docx", "*.json"):
        found = sorted(SRC_CACHE.glob(pattern), key=lambda p: p.stat().st_mtime)
        if found:
            return found[-1]
    die("give the manuscript path: build.py path/to/manuscript.docx")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="?", help=".docx or Google Docs JSON (default: newest file in ../source/)")
    ap.add_argument("--only", help="comma list of: kindle,print,large,reader,docx,sample; or just: cover")
    ap.add_argument("--no-check", action="store_true")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    want = lambda k: only is None or k in only

    OUT.mkdir(exist_ok=True)
    prepare_cover()
    model = ingest(a.source or default_source())
    base = f"{CFG['slug']}-{CFG['version']}"
    full, sample = model["sections"], sample_sections(model)
    specs = {}
    spec_file = WORK / "specs.json"
    if spec_file.exists() and only:
        specs = json.loads(spec_file.read_text())

    if want("kindle"):
        print("EPUB for Kindle")
        build_epub(model, full, OUT / f"{base}-kindle.epub", "kindle", base)
        specs[f"{base}-kindle.epub"] = {"kind": "epub", "scope": "full"}
    if want("print"):
        print("Print PDF, 6 x 9")
        s = build_print(model, full, OUT / f"{base}-print-6x9.pdf", "print", "11pt", "1.42", "justify", "auto")
        specs[f"{base}-print-6x9.pdf"] = {"kind": "pdf", "layout": "print", "scope": "full", **s}
        if (WORK / "cover-art.jpg").exists():
            specs[f"{base}-paperback-cover.pdf"] = build_wrap(
                s["pages"], OUT / f"{base}-paperback-cover.pdf", "cover-paperback", model)
    if want("large"):
        print("Large print PDF, 6 x 9")
        s = build_print(model, full, OUT / f"{base}-large-print-6x9.pdf", "large", "16pt", "1.5", "left", "none")
        specs[f"{base}-large-print-6x9.pdf"] = {"kind": "pdf", "layout": "print", "scope": "full", **s}
        if (WORK / "cover-art.jpg").exists():
            specs[f"{base}-large-print-cover.pdf"] = build_wrap(
                s["pages"], OUT / f"{base}-large-print-cover.pdf", "cover-large-print", model)
    if only == {"cover"}:
        for kind, nm in (("print-6x9", "paperback"), ("large-print-6x9", "large-print")):
            interior = specs.get(f"{base}-{kind}.pdf")
            if interior:
                specs[f"{base}-{nm}-cover.pdf"] = build_wrap(
                    interior["pages"], OUT / f"{base}-{nm}-cover.pdf", f"cover-{nm}", model)
        spec_file.write_text(json.dumps(specs, indent=1))
        write_listing(specs, base)
        return
    if want("reader"):
        print("Reader PDF, letter")
        s = build_reader(model, full, OUT / f"{base}-reader-letter.pdf", "reader")
        specs[f"{base}-reader-letter.pdf"] = {"kind": "pdf", "layout": "reader", "scope": "full", **s}
    if want("docx"):
        print("DOCX for KDP")
        build_docx(model, full, OUT / f"{base}-kdp.docx", "docx")
        specs[f"{base}-kdp.docx"] = {"kind": "docx", "scope": "full"}
    if want("sample"):
        n = CFG["sample_chapters"]
        print(f"Sample, first {n} chapters")
        s = build_reader(model, sample, OUT / f"{base}-sample-first-{n}-chapters.pdf", "sample")
        specs[f"{base}-sample-first-{n}-chapters.pdf"] = {"kind": "pdf", "layout": "reader", "scope": "sample", **s}
        build_epub(model, sample, OUT / f"{base}-sample-first-{n}-chapters.epub", "sample-epub", base + "-sample")
        specs[f"{base}-sample-first-{n}-chapters.epub"] = {"kind": "epub", "scope": "sample"}

    spec_file.write_text(json.dumps(specs, indent=1))
    write_listing(specs, base)
    if not a.no_check:
        sys.exit(subprocess.run([sys.executable, str(HERE / "check.py")]).returncode)


if __name__ == "__main__":
    main()
