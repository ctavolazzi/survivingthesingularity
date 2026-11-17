#!/usr/bin/env python3
"""Rebuild the novel's site source from the author's PDF.

    python3 scripts/novel_from_pdf.py path/to/manuscript.pdf [--date YYYY-MM-DD] [--edition "Final rough draft"]

WHY THIS EXISTS

The novel reached the site as a typeset PDF (WeasyPrint, 6 x 9 in), not as
source files. This script reads that PDF and writes what the site's readers
use: src/lib/data/novel/*.md, src/lib/data/novel/book.json,
src/lib/data/novel/image-dimensions.json and static/book-images/novel-p*.webp.
When the author revises the manuscript, run it again on the new PDF and review
the git diff. If the real source files ever arrive, use those instead and
retire this script.

WHAT IT RELIES ON IN THE PDF (checked 2026-11-17 on the 258-page draft)

  - Body text is the "Body" font at 10.8pt; italics are "Body-Italic".
  - A new paragraph starts with an indented line (x about 72 against 58), or
    after a blank line in the Author's Note and Afterword.
  - Chapter pages carry "C H A P T E R  N" in Inter above a 19pt title; act
    pages carry "A C T  O N E" above a 24pt title; the interludes are a 19pt
    italic "Meanwhile"; scene breaks are a small centered row of bullets.
  - A caption is an all-italic line directly under a picture, or at the top of
    the page after a full-page picture.
  - One diagram is drawn with typeset labels (JetBrains Mono). It is captured
    as a picture of that region on a dark ground, because its labels are light.

Line-end hyphens: a word split across lines is rejoined when the joined word
appears elsewhere in the book, kept hyphenated when the hyphenated form does,
and otherwise decided by KEEP / JOIN below. The run prints every undecided
join so a new one can be added to those lists.

Needs: pip install pymupdf pillow
"""
import argparse, datetime, shutil, tempfile
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
_ap = argparse.ArgumentParser()
_ap.add_argument("pdf"); _ap.add_argument("--date", default=datetime.date.today().isoformat())
_ap.add_argument("--edition", default="Final rough draft"); _ap.add_argument("--version", default="1.0.0-draft")
ARGS = _ap.parse_args()
import pymupdf, sys, re, json, os
from collections import Counter
pdf, out = ARGS.pdf, tempfile.mkdtemp(prefix="novel-")
os.makedirs(out + "/md", exist_ok=True); os.makedirs(out + "/img", exist_ok=True)
d = pymupdf.open(pdf)
HY = "‐"

# ---- pass 1: flat list of items ------------------------------------------
items = []   # dicts: kind in line/img/fig, page, x0,x1,y0,y1, spans[(text,italic)], fonts
for pn, p in enumerate(d):
    blocks = p.get_text("dict")["blocks"]
    mono = [b for b in blocks if b["type"] == 0 and any("Mono" in s["font"] for l in b["lines"] for s in l["spans"])]
    if mono:
        # a drawn figure with typeset labels: keep it as a picture of the page region
        ys = [b["bbox"][1] for b in mono] + [b["bbox"][3] for b in mono]
        items.append(dict(kind="fig", page=pn + 1, y0=min(ys), y1=max(ys)))
    for b in blocks:
        if b["type"] == 1:
            items.append(dict(kind="img", page=pn + 1, y0=b["bbox"][1], y1=b["bbox"][3], bbox=b["bbox"]))
            continue
        for l in b["lines"]:
            spans = [(s["text"], "Italic" in s["font"], s["font"], round(s["size"], 1)) for s in l["spans"] if s["text"]]
            if not spans: continue
            text = "".join(s[0] for s in spans)
            if not text.strip(): continue
            if any("Mono" in s[2] for s in spans): continue
            x0, y0, x1, y1 = l["bbox"]
            if y0 > 600 and text.strip().isdigit(): continue      # page number
            items.append(dict(kind="line", page=pn + 1, x0=x0, x1=x1, y0=y0, y1=y1, spans=spans, text=text,
                              font=spans[0][2], size=spans[0][3]))
items.sort(key=lambda i: (i["page"], i["y0"]))

# word list for de-hyphenation
allwords = Counter()
for it in items:
    if it["kind"] == "line":
        for w in re.findall(r"[A-Za-z’']+(?:‐[A-Za-z’']+)*", it["text"].rstrip(HY)):
            allwords[w.lower()] += 1
kept_hyphens = []
# Picture descriptions for readers who cannot see the pictures, keyed by the
# first words of each caption (page numbers move between drafts; captions
# mostly do not). Written by looking at the 2026-11-17 draft's pictures. A
# picture whose caption is not listed here falls back to its caption, and the
# run says so, so a new picture does not ship without a description unnoticed.
ALT = {
    "The Bear Flag.": "Illustration: three men in blazers raise beer glasses at a bar while a fourth man sits beside them at a laptop, not smiling.",
    "Devendra.": "Pixel-art portrait of Devendra, a man in a suit and tie holding a laptop. The picture's own label reads: senior and calm. wrong about the thing that mattered.",
    "The rig.": "Pixel-art drawing of a desktop computer tower with two graphics cards. The picture's own label reads: two GPUs zip-tied in. it throttles by design.",
    "The near end.": "Illustration: a man seen from behind stands at an apartment window at sunrise, looking out over rooftops and trees. An open notebook lies on the desk.",
    "The Fisher.": "Pixel-art drawing of a black cast-iron wood stove with a fire burning inside, labeled The Fisher.",
    "The tool wall.": "Pixel-art drawing of hammers, screwdrivers, a wrench and a saw hung on a board, labeled The Tool Wall.",
    "Pass the beans.": "Illustration: at a long plywood table in a workshop, an older woman passes a bowl to a bearded man while others eat around them.",
    "Gary.": "Pixel-art portrait of Gary, a man in work overalls. The picture's own label reads: stayed informed. couldn't fix a fence.",
    "The controller.": "Pixel-art drawing of a small circuit board inside an open yellow case, labeled The Controller.",
    "Reuben Vance.": "Pixel-art portrait of Reuben Vance, a man in a dark coat holding papers and a briefcase.",
    "The Crucible.": "Pixel-art drawing of three stacked server cabinets beside a salvaged car radiator, labeled The Crucible.",
    "The vise.": "Pixel-art drawing of a bench vise gripping a piece of metal, labeled The Vise.",
    "Frank Kowalski.": "Pixel-art portrait of Frank Kowalski, a bearded man in glasses and a shop apron.",
    "The bell.": "Pixel-art drawing of a hardware store doorway with a brass bell hung beside it, labeled The Bell.",
    "The probe.": "Pixel-art drawing of a soil probe with three prongs of different lengths, labeled The Probe.",
    "Ink for what is funded.": "Diagram titled Ink for What Is Funded. Two calendar pages: one reads Through June with a check mark, labeled Secured; the other reads Continuation, proposed, labeled Not yet promised. Below: Name the cover. Pay for the work. Tell households what is actually secured.",
    "Rosa, with a minute": "Illustration: a woman with a brace on her wrist speaks at a podium microphone in a county meeting room while the audience and the board watch.",
    "The proofs.": "Pixel-art drawing of an open cardboard box holding copies of a book, labeled The Proofs.",
    "One that grows the food": "Pixel-art panel titled The Robots That Grow Your Food and Build Your House: a tracked farming robot watering plants, and a robot assembling the frame of a house.",
}
def alt_for(caption):
    for start, text in ALT.items():
        if caption.startswith(start): return text
    undescribed.append(caption or "(no caption)")
    return caption or "Illustration"
undescribed = []
KEEP = {"polite|but","Commission|brained","eighty|some","in|law","plant|disease","mail|forwarding","fire|lookout","cast|iron","twenty|two","Twenty|two","per|second","load|ins"}
JOIN = {"DE|CLARES"}

def md_spans(spans):
    o = ""
    for t, ital, *_ in spans:
        if ital and t.strip():
            lead = t[:len(t) - len(t.lstrip())]; trail = t[len(t.rstrip()):]
            o += f"{lead}*{t.strip()}*{trail}"
        else:
            o += t
    return o

def join(a, b):
    """join two line strings of one paragraph"""
    if a.endswith(HY) or a.endswith(HY + "*"):
        star = a.endswith("*")
        a2 = a[:-2] if star else a[:-1]
        left = re.findall(r"[A-Za-z’']+$", a2)
        b2 = b[1:] if (star and b.startswith("*")) else b
        right = re.findall(r"^[A-Za-z’']+", b2)
        merged = (left[0] + right[0]).lower() if left and right else ""
        hyph = (left[0] + HY + right[0]).lower() if left and right else ""
        keep = bool(merged) and allwords[merged] == 0 and allwords[hyph] > 0
        pair = left[0] + "|" + right[0] if left and right else ""
        if pair in KEEP: keep = True; allwords[hyph] += 1
        if pair in JOIN: keep = False; allwords[merged] += 1
        if merged and allwords[merged] == 0 and allwords[hyph] == 0:
            # unknown either way: keep the hyphen only after a capital or a digit-ish compound
            keep = left[0][0].isupper() and right[0][0].isupper()
            kept_hyphens.append(("?" if not keep else "K?") + " " + left[0] + "|" + right[0])
        elif keep:
            kept_hyphens.append("K " + left[0] + "|" + right[0])
        if star and b.startswith("*"):
            return a2 + (HY if keep else "") + b2 if True else None
        return a2 + (HY if keep else "") + b
    if a.endswith("*") and b.startswith("*"):       # italic runs across the line break
        return a[:-1] + " " + b[1:]
    return a + " " + b

# ---- pass 2: sections -----------------------------------------------------
sections = []; cur = None
def start(sid, title, kind):
    global cur
    cur = dict(id=sid, title=title, kind=kind, blocks=[]); sections.append(cur)
def spaced(t): return re.sub(r"\s+", "", t)
ACTS = {"ACTONE": 1, "ACTTWO": 2, "ACTTHREE": 3, "ACTFOUR": 4}
ACTNAME = {1: "One", 2: "Two", 3: "Three", 4: "Four"}
mean_n = 0; pending = None; para = None; last = None; imgn = 0
BLOCKSTYLE = False

deferred = []; lastpic = None
def flush():
    global para
    if para: cur["blocks"].append(("p", para))
    para = None
    while deferred: cur["blocks"].append(deferred.pop(0))

i = 0
while i < len(items):
    it = items[i]; i += 1
    if it["page"] == 1: continue                        # cover
    if it["page"] == 2: continue                        # title page
    if it["kind"] == "line":
        t = it["text"].strip(); sz = it["size"]; f = it["font"]
        if it["page"] == 3:                               # epigraph page
            if cur is None: start("epigraph", "Epigraph", "front")
            if "Inter" in f: flush(); cur["blocks"].append(("attr", t))
            else:
                s = md_spans(it["spans"]).strip(); para = s if para is None else join(para, s)
            continue
        if "Inter" in f and spaced(t) in ACTS:
            flush(); pending = ("act", ACTS[spaced(t)]); continue
        if "Inter" in f and spaced(t).startswith("CHAPTER"):
            flush(); pending = ("ch", int(spaced(t)[7:])); continue
        if "Inter" in f and spaced(t) == "AFTERWORD":
            flush(); pending = ("after", 0); continue
        if sz >= 19:                                      # a title line
            flush()
            title = t
            while i < len(items) and items[i]["kind"] == "line" and items[i]["size"] == sz and items[i]["page"] == it["page"]:
                title += " " + items[i]["text"].strip(); i += 1
            title = title.replace("'", "’")
            if pending and pending[0] == "act":
                n = pending[1]; start(f"part-{n}", f"Act {ACTNAME[n]}: {title}", "act")
            elif pending and pending[0] == "ch":
                n = pending[1]; start(f"chapter{n}", f"Chapter {n}: {title}", "chapter")
            elif pending and pending[0] == "after":
                start("afterword", f"Afterword: {title}", "back")
            elif "Italic" in f:
                mean_n += 1; start(f"meanwhile-{mean_n}", title, "interlude")
            else:
                start("authors-note", title, "front")
            BLOCKSTYLE = cur["id"] in ("authors-note", "afterword")
            pending = None; last = None; continue
        if sz == 12.0 and "Semi" in f:
            flush(); cur["blocks"].append(("h2", t)); last = None; continue
        if sz == 8.0 and "•" in t:
            flush(); cur["blocks"].append(("break", "")); last = None; continue
        s = md_spans(it["spans"]).strip()
        # caption: an all-italic line sitting directly under a picture
        if lastpic and (lastpic["page"] == it["page"] or (lastpic["page"] == it["page"] - 1 and it["y0"] < 60)) and it["y0"] > lastpic["y1"] - 800 * (lastpic["page"] != it["page"]) and all(sp[1] for sp in it["spans"] if sp[0].strip()):
            cap = t
            while i < len(items) and items[i]["kind"] == "line" and items[i]["page"] == it["page"] and all(sp[1] for sp in items[i]["spans"] if sp[0].strip()) and items[i]["y0"] - items[i-1]["y1"] < 6:
                cap = join(cap, items[i]["text"].strip()); i += 1
            k = max(j for j, b in enumerate(cur["blocks"]) if b[0] == "img")
            cur["blocks"][k] = (cur["blocks"][k][0], cur["blocks"][k][1], cap)
            lastpic = None; continue
        if lastpic and lastpic["page"] < it["page"] - 1: lastpic = None
        newpara = para is None
        if not newpara and last and last["kind"] == "line":
            samepage = last["page"] == it["page"]
            gap = it["y0"] - last["y1"] if samepage else 0
            if it["x0"] > 66: newpara = True                       # indented first line
            elif samepage and gap > 5: newpara = True               # blank line between
            elif not samepage and BLOCKSTYLE and last["x1"] < 350 and re.search(r"[.?!”)]$", last["text"].strip()):
                newpara = True
        elif not newpara:
            newpara = True
        if newpara:
            flush(); para = s
        else:
            para = join(para, s)
        last = it
    else:
        imgn += 1
        name = f"novel-p{it['page']:03d}"
        blk = ("img", dict(name=name, page=it["page"], kind=it["kind"], y0=it["y0"], y1=it["y1"]), "")
        if para and not re.search(r"[.?!\u201d:*)]$", para.strip()):
            deferred.append(blk)                       # mid-sentence: place it after the paragraph
        else:
            flush(); cur["blocks"].append(blk)
        lastpic = it
flush()

# ---- pictures -------------------------------------------------------------
pics = []
for s in sections:
    for b in s["blocks"]:
        if b[0] != "img": continue
        m = b[1]; page = d[m["page"] - 1]
        if m["kind"] == "img":
            info = [x for x in page.get_image_info(xrefs=True) if abs(x["bbox"][1]-m["y0"])<2]
            pix = pymupdf.Pixmap(d, info[0]["xref"])
            if pix.n - pix.alpha >= 4: pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        else:
            dr = [x["rect"] for x in page.get_drawings() if x["rect"].y0 > m["y0"] - 30]
            clip = pymupdf.Rect(min([r.x0 for r in dr] + [80]) - 12, m["y0"] - 8, max([r.x1 for r in dr] + [352]) + 8, max([r.y1 for r in dr] + [m["y1"]]) + 8)
            pix = page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip, alpha=True)
        pix.save(f"{out}/img/{m['name']}.png")
        m["w"], m["h"] = pix.width, pix.height
        pics.append(dict(m, section=s["id"], caption=b[2]))

# ---- write ---------------------------------------------------------------
def clean(t):
    t = t.replace(HY, "-").replace(" ", " ")
    t = re.sub(r"\*\*", "", t)            # adjacent italic runs
    return re.sub(r"[ \t]+", " ", t).strip()
manifest = []
for n, s in enumerate(sections):
    lines = [f"# {s['title']}", ""]
    for b in s["blocks"]:
        if b[0] == "p": lines += [clean(b[1]), ""]
        elif b[0] == "h2": lines += [f"## {clean(b[1])}", ""]
        elif b[0] == "break": lines += ["---", ""]
        elif b[0] == "attr": lines += [f"ATTR::{clean(b[1])}", ""]
        elif b[0] == "img":
            lines += [f"![{alt_for(clean(b[2]))}](/book-images/{b[1]['name']}.webp)", ""]
            if b[2]: lines += [f"*{clean(b[2])}*", ""]
    s["md"] = "\n".join(lines).rstrip() + "\n"
    manifest.append(dict(id=s["id"], title=s["title"], kind=s["kind"], words=len(re.findall(r"\b[\w’'-]+\b", s["md"]))))
    open(f"{out}/md/{n:02d}-{s['id']}.md", "w").write(s["md"])
json.dump(dict(sections=manifest, pics=pics, hyphens=kept_hyphens), open(out + "/manifest.json", "w"), indent=1)


# ---- install into the site ---------------------------------------------------
nd = ROOT / "src/lib/data/novel"; imgdir = ROOT / "static/book-images"
nd.mkdir(parents=True, exist_ok=True)
for old in nd.glob("[0-9][0-9]-*.md"): old.unlink()      # the generated sections only, never README.md
for old in imgdir.glob("novel-p*.webp"): old.unlink()
dims = {}
for p in pics:
    im = Image.open(f"{out}/img/{p['name']}.png")
    if p["kind"] == "fig":                      # light labels: put the drawing on a dark ground
        bg = Image.new("RGBA", (im.width + 60, im.height + 60), (11, 18, 32, 255))
        bg.alpha_composite(im.convert("RGBA"), (30, 30)); im = bg
    im = im.convert("RGB")
    if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    im.save(imgdir / f"{p['name']}.webp", "WEBP", quality=82, method=6)
    dims[f"{p['name']}.webp"] = [im.width, im.height]
by = {s["id"]: s for s in sections}
epi = by["epigraph"]["md"]
q = re.search(r"\*(.+?)\*\n\nATTR::(.+)", epi, re.S)
attr = q.group(2).strip().replace("The Soul of Man under Socialism", "*The Soul of Man under Socialism*")
epiblock = f"> *“{q.group(1).strip()}”*\n> {attr}\n"
secs = []; n = 0
for s in sections:
    if s["id"] == "epigraph": continue
    md = s["md"]
    if s["id"] == "authors-note": md = md.replace("\n\n", "\n\n" + epiblock + "\n", 1)
    fn = f"{n:02d}-{s['id']}.md"; n += 1
    (nd / fn).write_text(md)
    secs.append({"id": s["id"], "title": s["title"], "file": fn})
book = {"title": "Surviving the Singularity", "subtitle": "A Novel", "author": "Christopher Tavolazzi",
        "edition": ARGS.edition, "version": ARGS.version, "released": ARGS.version, "lastUpdated": ARGS.date,
        "source": f"Built by scripts/novel_from_pdf.py from the author's PDF ({d.page_count} pages), received {ARGS.date}.",
        "sections": secs}
(nd / "book.json").write_text(json.dumps(book, indent=2, ensure_ascii=False) + "\n")
(nd / "image-dimensions.json").write_text(json.dumps(dims, indent=2) + "\n")
shutil.rmtree(out)
print(len(secs), "sections,", sum(m["words"] for m in manifest), "words,", len(pics), "pictures")
und = [h for h in kept_hyphens if h.startswith("?") or h.startswith("K?")]
print("pictures with no written description (add to ALT):", undescribed or "none")
print("line-end joins decided by the fallback rule (check, then add to KEEP or JOIN):", und or "none")
