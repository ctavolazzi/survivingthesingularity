"""Cross-reference rules: pointers in, text out.

WHAT A REF IS, AND WHY

A cross-reference in the manuscript is written as a POINTER, not a number:

    [](sts:chapter1)             -> "Chapter 1"    (label generated)
    [](sts:sts.chapter1.b0003)   -> "Chapter 1"    (block-precise pointer)
    [the limits](sts:chapter1)   -> "the limits"   (author's words, checked)

An empty label is generated from book.json, so renumbering a chapter rewrites
every sentence that points at it instead of leaving prose that is quietly
wrong. A non-empty label is the author's phrasing and is left alone - but the
pointer is still resolved, so deleting the target fails the build instead of
leaving a sentence that references nothing.

WHY EXPANSION, NOT HYPERLINKS

Three consumers read the raw .md: `sts.py compile`, scripts/build-epub.sh
(pandoc, straight off the book directory), and the website
(src/lib/bookContent.js, via Vite ?raw). No single href is correct in all three
- the site needs /book/<section>, print needs an internal anchor, and anchors
in the source are exactly what the id subsystem exists to avoid. So a ref
expands to TEXT, identically everywhere. The edge table is target-agnostic, so
emitting real hrefs later is a change of one function, not a redesign.

WHY THESE FUNCTIONS TAKE book_dir

_ref_edges used to read the module-level BOOK_DIR in sts.py. That single hidden
dependency is why `refs stress` had to declare `global BOOK_DIR` and rebind it
to a temp directory to test the resolver against a throwaway copy of the book -
a test faking its environment by mutating a global belonging to the module
under test, which breaks the moment anything runs concurrently and makes the
functions impossible to lift out of sts.py at all.

Passing the directory in is the whole fix. These are now pure functions of
(index, book_dir), the stress test hands them a temp tree like any other
caller, and nothing rebinds anything.

The label rule itself lives in sts_lib.manifest, shared with the parity check.
"""

import re

from sts_lib.manifest import section_label

# [label](sts:target) -- target is a section id or a full sts.<sec>.b<NNNN> id.
SREF_RE = re.compile(r"\[([^\]\n]*)\]\(sts:([A-Za-z0-9._-]+)\)")


def ref_targets(index: dict) -> dict:
    """{ref target -> {...}} for every addressable thing a ref may point at.

    Two granularities, both legal:
      * section id   ('chapter1')           -- stable across editing, use in prose
      * block id     ('sts.chapter1.b0003') -- precise, but blocks churn
    """
    out = {}
    for sec in index["sections"]:
        out[sec["id"]] = {"kind": "section", "section": sec["id"],
                          "title": sec["title"], "file": sec["file"],
                          "label": section_label(sec["title"])}
        for blk in sec["blocks"]:
            out[blk["id"]] = {"kind": "block", "section": sec["id"],
                              "title": sec["title"], "file": sec["file"],
                              "label": section_label(sec["title"]),
                              "block": blk["id"], "lines": blk["lines"]}
    return out


def ref_edges(index: dict, book_dir) -> list:
    """Every sts: reference in the manuscript, as (source -> target) edges.

    The shared substrate: `refs --to` reads it backwards to answer "what breaks
    if I cut this", and the expanders read it forwards to render.
    """
    targets = ref_targets(index)
    edges = []
    for sec in index["sections"]:
        # line -> owning block id, so an edge knows which block it lives in.
        owner = {}
        for blk in sec["blocks"]:
            a, z = blk["lines"]
            for ln in range(a, z + 1):
                owner[ln] = blk["id"]
        text = (book_dir / sec["file"]).read_text(encoding="utf-8")
        for lineno, line in enumerate(text.split("\n"), 1):
            for m in SREF_RE.finditer(line):
                label, target = m.group(1), m.group(2)
                edges.append({
                    "from_section": sec["id"], "from_block": owner.get(lineno),
                    "file": sec["file"], "line": lineno,
                    "label": label, "to": target,
                    "resolved": target in targets,
                    "to_section": targets.get(target, {}).get("section"),
                    "generated": not label.strip(),
                    "raw": m.group(0)})
    return edges


def expand_refs(text: str, targets: dict, where: str = "") -> str:
    """Replace every sts: ref in `text` with its rendered form.

    Raises KeyError on a dangling target -- a broken cross-reference must stop a
    build, not ship. The website deliberately does the opposite and drops the
    marker (see src/lib/bookManifest.js), because by then this check has already
    had its chance and rendering "](sts:" at a reader is strictly worse.
    """
    def sub(m):
        label, target = m.group(1), m.group(2)
        t = targets.get(target)
        if t is None:
            raise KeyError(f"{where}: unresolvable reference sts:{target} "
                           f"in {m.group(0)!r}")
        return label if label.strip() else t["label"]
    return SREF_RE.sub(sub, text)
