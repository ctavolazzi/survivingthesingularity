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

    blocks, nimg = [], 0
    for p in paras:
        for blob in p["images"]:
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
    return {"title_display": title, "title_block": title_block, "author": author,
            "toc": toc, "sections": sections, "images": nimg}


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
        if prev_kind == "act" or s["title"] in ("About This Book", "Afterword", "Appendix"):
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
    return "\n".join(f"<p>{esc(line)}</p>" for line in CFG["copyright_lines"])


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
            "-M", "rights=" + " ".join(CFG["copyright_lines"]),
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
    lines = CFG["copyright_lines"]
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
    st("Copyright First", size=10, before=400, page_break=True)
    st("Copyright", size=10)
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
        Image.open(src).convert("RGB").save(target, "JPEG", quality=92, optimize=True)


def default_source():
    for pattern in ("*.docx", "*.json"):
        found = sorted(SRC_CACHE.glob(pattern), key=lambda p: p.stat().st_mtime)
        if found:
            return found[-1]
    die("give the manuscript path: build.py path/to/manuscript.docx")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="?", help=".docx or Google Docs JSON (default: newest file in ../source/)")
    ap.add_argument("--only", help="comma list of: kindle,print,large,reader,docx,sample")
    ap.add_argument("--no-check", action="store_true")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    want = lambda k: only is None or k in only

    OUT.mkdir(exist_ok=True)
    model = ingest(a.source or default_source())
    prepare_cover()
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
    if want("large"):
        print("Large print PDF, 6 x 9")
        s = build_print(model, full, OUT / f"{base}-large-print-6x9.pdf", "large", "16pt", "1.5", "left", "none")
        specs[f"{base}-large-print-6x9.pdf"] = {"kind": "pdf", "layout": "print", "scope": "full", **s}
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
    if not a.no_check:
        sys.exit(subprocess.run([sys.executable, str(HERE / "check.py")]).returncode)


if __name__ == "__main__":
    main()
