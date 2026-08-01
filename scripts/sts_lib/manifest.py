"""book.json: the one place it is read, and the rules derived from it.

WHY THIS MODULE EXISTS

`json.loads((BOOK_DIR / "book.json").read_text(...))` appeared eight times
inside sts.py, and one of those first re-derived the book directory that was
already a module constant. Eight readers of one file is eight places to update
when the manifest shape moves, and eight chances for one of them to disagree
about what counts as a section.

The split is deliberate: LOADING is here, and so are the pure RULES that turn a
manifest into a name, a label or an ordered file list. Everything that needs a
manifest asks this module for it.

THE OTHER HALF OF THIS RULE SET

src/lib/bookManifest.js carries the same LABEL rule in JavaScript, because the
website cannot call Python at build time and the alternative - emitting a
generated JSON for the site to consume - adds an artifact that can go stale,
which is the class of bug this whole effort exists to remove. Two
implementations of that one rule is the honest floor, not an accident.

They are held together by scripts/check-resolver-parity.mjs, which runs both
over the real manifest and every cross-reference in the book and fails the
build if a single label disagrees. Keep the two files in step by changing them
together; the parity check is what catches you when you forget.

Only the label rule is duplicated. The download filename rule lives ONLY in
bookManifest.js, because only JavaScript callers ever name a shipped artifact -
two route components, the download guard and the publish script. Mirroring it
here for symmetry would create a second definition with no caller, which is a
liability pretending to be consistency.

NOT CACHED, ON PURPOSE

book.json is a few kilobytes and a CLI run is short, so re-reading costs
nothing worth measuring. `sts.py refs stress` writes a mutated manifest into a
temp tree and re-reads it to prove the checks fire, which a path-keyed cache
would quietly defeat by handing back the pre-mutation copy.
"""

import json


def load_manifest(book_dir) -> dict:
    """The parsed book.json. The one read of the file in the Python half."""
    return json.loads((book_dir / "book.json").read_text(encoding="utf-8"))


def section_label(title: str) -> str:
    """'Chapter 1: The Event Horizon' -> 'Chapter 1'.

    book.json titles are '<short name>: <descriptive tail>'. The short name is
    what prose actually says ("as we saw in Chapter 1"), so that is what a
    generated label expands to. Titles with no colon are used whole.
    """
    return title.split(":", 1)[0].strip() if ":" in title else title.strip()


def section_files(manifest: dict, exclude=()) -> list:
    """Section files in running order.

    `exclude` drops sections a given consumer cannot use. The EPUB build skips
    the print-style index, which is generated for the PDF and meaningless in a
    reflowable format; it is passed as data rather than grepped out of this
    list downstream, so that renaming the file cannot silently stop excluding
    it.
    """
    return [s["file"] for s in manifest["sections"] if s["file"] not in exclude]
