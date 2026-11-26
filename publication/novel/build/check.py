#!/usr/bin/env python3
"""Check every file in ../output/ against the manuscript text. Writes output/CHECKS.md.

Run by build.py after a build; can also be run alone. Exit code 1 if anything fails.
"""
import difflib
import json
import re
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOVEL = HERE.parent
WORK, OUT = NOVEL / "work", NOVEL / "output"
CFG = json.loads((HERE / "book.json").read_text(encoding="utf-8"))
MODEL = json.loads((WORK / "model.json").read_text(encoding="utf-8"))
SPECS = json.loads((WORK / "specs.json").read_text(encoding="utf-8"))
BREAK = CFG["scene_break"]
BAD = {"—": "em dash", "–": "en dash", "‘": "curly quote", "’": "curly quote",
       "“": "curly quote", "”": "curly quote"}


def plain(runs):
    return "".join(r[0] for r in runs)


def sections_for(scope):
    secs = MODEL["sections"]
    if scope == "sample":
        last = max(i for i, s in enumerate(secs)
                   if s["chapter"] is not None and s["chapter"] < CFG["sample_chapters"])
        secs = secs[:last + 1]
    return secs


def expected_lines(scope):
    """The manuscript text in output order. The copyright page is the one addition."""
    secs = sections_for(scope)
    keep = {s["title"] + s["id"] for s in secs}
    lines = [plain(b["runs"]) for b in MODEL.get("opening", [])]
    lines += [plain(b["runs"]) for b in MODEL["title_block"]]
    lines += MODEL["copyright_lines"]
    lines.append("Contents")
    lines += [t["text"] for t, s in zip(MODEL["toc"], MODEL["sections"]) if s["title"] + s["id"] in keep]
    for s in secs:
        lines.append(s["title"])
        lines += [plain(b["runs"]) for b in s["blocks"] if b["t"] in ("p", "h2")]
    return lines


def norm(s):
    return unicodedata.normalize("NFKC", s).replace("\xa0", " ")


def words(lines):
    return norm("\n".join(lines)).split()


def word_diff(exp, got, limit=40):
    if exp == got:
        return []
    out = []
    sm = difflib.SequenceMatcher(None, exp, got, autojunk=False)
    for tag, a, b, c, d in sm.get_opcodes():
        if tag != "equal":
            ctx = " ".join(exp[max(0, a - 4):a])
            out.append(f"after \"...{ctx}\": manuscript has [{' '.join(exp[a:b])}], file has [{' '.join(got[c:d])}]")
            if len(out) >= limit:
                out.append("(more differences not shown)")
                break
    return out


# ------------------------------------------------------------ extractors

BLOCK = {"p", "h1", "h2", "h3", "div", "li", "section", "body", "nav", "ol", "ul", "title", "br"}


def xhtml_lines(data):
    from lxml import etree
    root = etree.fromstring(data)
    lines, buf, counts = [], [], {"em": 0, "img": 0, "h1": []}

    def flush():
        t = "".join(buf).strip()
        buf.clear()
        if t:
            lines.append(t)

    def walk(el):
        if not isinstance(el.tag, str):
            return
        tag = etree.QName(el).localname
        if tag == "head" or el.get("hidden") is not None or "break" in (el.get("class") or "").split():
            return
        if tag in BLOCK:
            flush()
        if tag == "img" or tag == "image":
            counts["img"] += 1
        if tag == "em":
            counts["em"] += len("".join(el.itertext()))
        if tag == "h1":
            counts["h1"].append("".join(el.itertext()).strip())
        buf.append(el.text or "")
        for ch in el:
            walk(ch)
            buf.append(ch.tail or "")
        if tag in BLOCK:
            flush()

    walk(root)
    return lines, counts


def read_epub(path):
    from lxml import etree
    z = zipfile.ZipFile(path)
    opf_path = etree.fromstring(z.read("META-INF/container.xml")).find(".//{*}rootfile").get("full-path")
    opf = etree.fromstring(z.read(opf_path))
    base = opf_path.rsplit("/", 1)[0] + "/" if "/" in opf_path else ""
    items = {i.get("id"): i for i in opf.findall(".//{*}item")}
    lines, em, imgs, h1s, nav, order = [], 0, 0, [], [], []
    for ref in opf.findall(".//{*}itemref"):
        item = items[ref.get("idref")]
        data = z.read(base + item.get("href"))
        l, c = xhtml_lines(data)
        if "nav" in (item.get("properties") or ""):
            nav = l[1:]
            order.append("contents")
        elif b"titlepage" in data:
            order.append("title page")
        elif "cover" in item.get("href"):
            order.append("cover")
        lines += l
        em += c["em"]
        imgs += c["img"]
        h1s += c["h1"]
    cover = any("cover-image" in (i.get("properties") or "") for i in items.values())
    meta = {k: (opf.find(".//{*}" + k).text if opf.find(".//{*}" + k) is not None else None)
            for k in ("title", "creator", "language", "rights")}
    return {"lines": lines, "italic_chars": em, "images": imgs, "headings": h1s, "toc": nav,
            "cover": cover, "front_order": order, "meta": meta}


def read_docx(path):
    import docx
    d = docx.Document(str(path))
    lines, heads, em = [], [], 0
    for p in d.paragraphs:
        t = p.text.strip()
        if t and t != BREAK:
            lines.append(p.text)
        if p.style.name == "Heading 1":
            heads.append(t)
        for item in p.iter_inner_content():
            for r in ([item] if hasattr(item, "italic") else item.runs):
                if r.italic or (r.style is not None and r.style.font.italic):
                    em += len(r.text)
    z = zipfile.ZipFile(path)
    xml = z.read("word/document.xml").decode("utf-8")
    links = re.findall(r'<w:hyperlink [^>]*w:anchor="([^"]+)"', xml)
    marks = set(re.findall(r'<w:bookmarkStart [^>]*w:name="([^"]+)"', xml))
    toc_start = heads.index("Contents") if "Contents" in heads else None
    return {"lines": lines, "headings": heads, "italic_chars": em, "images": len(d.inline_shapes),
            "toc_links": len(links), "toc_links_resolve": all(a in marks for a in links)}


def read_pdf(path, layout):
    from pypdf import PdfReader
    r = PdfReader(str(path))
    n = len(r.pages)
    w, h = float(r.pages[n // 2].mediabox.width), float(r.pages[n // 2].mediabox.height)
    # Text of the body area only, so running heads and page numbers stay out.
    top, bottom = (0.8 * 72 - 6, 0.8 * 72 - 6) if layout == "print" else (0, 0.9 * 72)
    txt = subprocess.run(["pdftotext", "-x", "0", "-y", str(int(top)), "-W", str(int(w) + 1),
                          "-H", str(int(h - top - bottom)), str(path), "-"],
                         capture_output=True, text=True, check=True).stdout
    full = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, check=True).stdout
    pages = txt.split("\f")
    first_title = MODEL["sections"][0]["title"]
    lines, in_toc, toc_nums = [], False, []
    toc_titles = {norm(t["text"]) for t in MODEL["toc"]}
    for pg in pages:
        pl = [l for l in pg.split("\n")]
        head = next((l.strip() for l in pl if l.strip()), "")
        if head == "Contents":
            in_toc = True
        elif in_toc and head == first_title:
            in_toc = False
        for l in pl:
            if l.strip() and l.replace(" ", "") == BREAK.replace(" ", ""):
                continue
            if in_toc:  # drop the page numbers the contents page adds
                t = norm(l).strip()
                if t.isdigit():
                    toc_nums.append(int(t))
                    continue
                m = re.match(r"(.*\S)\s+(\d+)$", t)
                if t not in toc_titles and m and m.group(1) in toc_titles:
                    toc_nums.append(int(m.group(2)))
                if t not in toc_titles and m and m.group(1) in toc_titles:
                    l = m.group(1)
            lines.append(l)

    def flat(o, depth=0):
        out = []
        for x in o:
            if isinstance(x, list):
                out += flat(x, depth + 1)
            else:
                out.append((depth, x.title, r.get_destination_page_number(x)))
        return out

    marks = flat(r.outline)
    fonts = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True).stdout.splitlines()[2:]
    not_embedded = [f for f in fonts if f.split()[-5] != "yes"]
    listing = subprocess.run(["pdfimages", "-list", str(path)], capture_output=True, text=True).stdout
    imgs = len([l for l in listing.splitlines()[2:] if l.split()[2:3] == ["image"]])
    link_count = sum(1 for p in r.pages for a in (p.get("/Annots") or []) if a.get_object().get("/Subtype") == "/Link")
    heads_text = [norm(l).strip() for l in full.split("\n")]
    return {"lines": lines, "pages": n, "size_in": (round(w / 72, 3), round(h / 72, 3)),
            "bookmarks": marks, "fonts": len(fonts), "fonts_not_embedded": not_embedded,
            "images": imgs, "links": link_count, "toc_nums": toc_nums, "full": full, "page_text": full.split("\f")}


def squeeze(lines):
    """Letters only: drops spaces, line-end hyphens and hyphens, which page layout moves."""
    s = norm("\n".join(lines))
    return re.sub(r"[\s\-­‐‑]+", "", s)


# ------------------------------------------------------------ checks

def structure_expect(scope):
    secs = sections_for(scope)
    return [s["title"] for s in secs]


def check_file(name, spec):
    path = OUT / name
    res = {"file": name, "size": path.stat().st_size, "pass": [], "fail": [], "note": []}
    ok = lambda cond, good, bad=None: (res["pass"] if cond else res["fail"]).append(good if cond else (bad or good))
    exp = expected_lines(spec["scope"])
    titles = structure_expect(spec["scope"])
    chapters = [t for t in titles if t.startswith("Chapter ")]
    nums = [int(re.match(r"Chapter (\d+)", t).group(1)) for t in chapters]
    n_img = sum(1 for s in sections_for(spec["scope"]) for b in s["blocks"] if b["t"] == "img")
    src_em = sum(len(r[0]) for s in sections_for(spec["scope"]) for b in s["blocks"]
                 if b["t"] in ("p", "h2") for r in b["runs"] if r[1])
    src_em += sum(len(r[0]) for b in MODEL["title_block"] for r in b["runs"] if r[1])
    chap_label = f"chapters {nums[0]} to {nums[-1]} ({len(nums)}), in order"

    if spec["kind"] == "epub":
        e = read_epub(path)
        got = [l for l in e["lines"]]
        diffs = word_diff(words(exp), words(got))
        ok(not diffs, f"text matches the manuscript word for word ({len(words(exp)):,} words)",
           "TEXT DIFFERS: " + " | ".join(diffs))
        ok(e["toc"] == titles, f"clickable contents: {len(e['toc'])} entries, same as the manuscript's list",
           f"contents list differs: {e['toc'][:5]}")
        ok(e["headings"][-len(titles):] == titles and nums == list(range(nums[0], nums[-1] + 1)),
           f"{chap_label}; each section is its own file (chapter break)", "headings differ from manuscript")
        ok(e["italic_chars"] == src_em, f"italics kept ({src_em:,} italic characters)",
           f"italics differ: {e['italic_chars']} vs {src_em}")
        ok(e["images"] - (1 if e["cover"] else 0) == n_img, (f"{n_img} pictures in place" if n_img else "no pictures inside the book"),
           f"pictures: {e['images']} found, {n_img} expected")
        ok(e["cover"], "cover embedded", "no cover embedded")
        ok(e["front_order"][:3] == ["cover", "title page", "contents"], "order: cover, title page, copyright page, contents")
        ok(all(l in e["lines"] for l in MODEL["copyright_lines"]), "copyright page present")
        res["note"].append(f"metadata: {e['meta']}")
        text = "\n".join(got)
        try:
            from epubcheck import EpubCheck
            r = EpubCheck(str(path))
            errs = [m for m in r.messages if m.level in ("ERROR", "FATAL")]
            warns = [m for m in r.messages if m.level == "WARNING"]
            ok(not errs, f"epubcheck: 0 errors, {len(warns)} warnings",
               "epubcheck errors: " + " | ".join(f"{m.id} {m.message}" for m in errs[:10]))
            for m in warns[:10]:
                res["note"].append(f"epubcheck warning {m.id}: {m.message}")
        except Exception as ex:  # epubcheck missing or Java missing
            res["fail"].append(f"epubcheck did not run: {ex}")
    elif spec["kind"] == "docx":
        d = read_docx(path)
        diffs = word_diff(words(exp), words(d["lines"]))
        ok(not diffs, f"text matches the manuscript word for word ({len(words(exp)):,} words)",
           "TEXT DIFFERS: " + " | ".join(diffs))
        ok(d["headings"] == ["Contents"] + titles and nums == list(range(nums[0], nums[-1] + 1)),
           f"{chap_label}, as Heading 1 with a page break before each", "headings differ from manuscript")
        ok(d["toc_links"] == len(titles) and d["toc_links_resolve"],
           f"clickable contents: {d['toc_links']} links, all land on a heading",
           f"contents links: {d['toc_links']} of {len(titles)}")
        ok(d["italic_chars"] == src_em, f"italics kept ({src_em:,} italic characters)",
           f"italics differ: {d['italic_chars']} vs {src_em}")
        ok(d["images"] == n_img, (f"{n_img} pictures in place" if n_img else "no pictures inside the book"), f"pictures: {d['images']} of {n_img}")
        ok(all(l in d["lines"] for l in MODEL["copyright_lines"]), "title page and copyright page present")
        text = "\n".join(d["lines"])
    else:
        p = read_pdf(path, spec["layout"])
        a, b = squeeze(exp), squeeze(p["lines"])
        if a == b:
            res["pass"].append(f"text matches the manuscript letter for letter ({len(a):,} characters; "
                               "spaces and line-end hyphens ignored)")
        else:
            i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            res["fail"].append(f"TEXT DIFFERS near: manuscript \"{a[max(0, i - 40):i + 40]}\" / file \"{b[max(0, i - 40):i + 40]}\"")
        marks = [t for _, t, _ in p["bookmarks"] if t in titles or t == "Contents"]
        tops = [t for d_, t, _ in p["bookmarks"] if d_ == 0]
        ok([t for t in tops if t != "Contents"] == titles and nums == list(range(nums[0], nums[-1] + 1)),
           f"{chap_label} (PDF bookmarks)", f"bookmarks differ: {tops[:6]}")
        starts = {}
        for d_, t, pg in p["bookmarks"]:
            if d_ == 0:
                starts.setdefault(pg, []).append(t)
        shared = [v for v in starts.values() if len(v) > 1]
        first_lines_ok = all(squeeze([p["page_text"][pg]]).startswith(squeeze([t]))
                             for d_, t, pg in p["bookmarks"] if d_ == 0)
        ok(not shared and first_lines_ok, "every act, chapter and back-matter section starts on a new page",
           f"sections sharing a page or not at the top: {shared[:3]}")
        offset = 1 if spec["layout"] == "reader" and (WORK / "cover.jpg").exists() else 0
        real = [pg + 1 for d_, t, pg in p["bookmarks"] if d_ == 0 and t != "Contents"]
        ok(p["links"] >= len(titles) and p["toc_nums"] == real,
           f"contents page: {len(titles)} linked entries, and every page number shown matches the page the section starts on",
           f"contents page numbers wrong: shown {p['toc_nums'][:6]}, real {real[:6]}")
        ok(not p["fonts_not_embedded"], f"all {p['fonts']} fonts embedded", f"not embedded: {p['fonts_not_embedded']}")
        want_img = n_img + (1 if spec["layout"] == "reader" and (WORK / "cover.jpg").exists() else 0)
        ok(p["images"] == want_img, (f"{n_img} pictures in place" if n_img else "no pictures inside the book") + (", cover on page 1" if want_img > n_img else ""),
           f"pictures: {p['images']} of {want_img}")
        ok(all(squeeze([l]) in b for l in MODEL["copyright_lines"]), "title page and copyright page present")
        if spec["layout"] == "print":
            ok(p["size_in"] == (6.0, 9.0), "trim 6 x 9 in, no bleed", f"page size {p['size_in']}")
            inner = float(spec["INNER"].rstrip("in"))
            ok(inner >= spec["kdp_min_inner_in"] and inner + 1e-9 >= 0.375,
               f"{p['pages']} pages; mirrored margins: inside {inner} in (KDP minimum for this page count "
               f"{spec['kdp_min_inner_in']} in), outside {spec['OUTER']}, top and bottom {spec['TOP']}")
            mid = p["page_text"][len(p["page_text"]) // 2: len(p["page_text"]) // 2 + 2]
            ok(any(norm(CFG["title"]) in norm(t) for t in mid), "running heads (book title left, chapter title right) and page numbers")
        else:
            ok(p["size_in"] == (8.5, 11.0), f"letter size, {p['pages']} pages", f"page size {p['size_in']}")
        text = p["full"]
    src_text = "\n".join(exp)
    for ch, label in BAD.items():
        n_out, n_src = text.count(ch), src_text.count(ch)
        if n_out != n_src:
            res["fail"].append(f"{label} {ch!r}: {n_out} in file, {n_src} in manuscript")
    if not any(ch in text for ch in BAD):
        res["pass"].append("no em dashes; quotes all straight, as in the manuscript")
    return res


def main():
    results = []
    for name, spec in SPECS.items():
        if spec["kind"] == "cover":
            continue
        if (OUT / name).exists():
            print("checking", name)
            results.append(check_file(name, spec))
    added = [s for s in MODEL["sections"] if s.get("added")]
    added_words = len(words(MODEL["copyright_lines"])) + sum(
        len(words([s["title"]] * 2 + [plain(b["runs"]) for b in s["blocks"]])) for s in added)
    src_words = len(words([l for l in expected_lines("full")])) - added_words
    out = ["# Checks: " + CFG["title"] + " " + CFG["version"], "",
           f"Source: `{Path(MODEL['source']).name}` ({src_words:,} words, {len(MODEL['sections'])} sections, "
           f"{MODEL['images']} pictures inside the book" +
           (f"; the manuscript's {MODEL['pictures_left_out']} pictures are left out on purpose"
            if MODEL.get("pictures_left_out") else "") + ").",
           "Words added by the build: the copyright page" +
           "".join(f" and the page \"{s['title']}\"" for s in added) + f" ({added_words} words, from book.json).", ""]
    failed = False
    for r in results:
        out.append(f"## {r['file']} ({r['size'] / 1e6:.1f} MB)")
        out += [f"- PASS: {x}" for x in r["pass"]]
        out += [f"- FAIL: {x}" for x in r["fail"]]
        out += [f"- note: {x}" for x in r["note"]]
        out.append("")
        failed |= bool(r["fail"])
    (OUT / "CHECKS.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
