#!/usr/bin/env python3
"""Export the reviewed publication without copying unapproved or unused images.

Run --check to construct and validate the complete package in memory. Normal
execution writes a new package and ZIP. Existing edited files are never replaced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import sys
import zipfile
from importlib.metadata import version
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit, urlunsplit

from bs4 import BeautifulSoup


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "output"
PACKAGE = HERE / "package"
ZIP = OUT / "Surviving-the-Singularity-editable-publication.zip"
BOOK = ROOT / "src/lib/data/book"
AUDITS = ROOT / "docs/publication"
ASSETS = HERE / "assets"
IMAGES = ROOT / "static/book-images"
FONT_NOTICES = (
    "SourceSansPro-LICENSE.txt", "SourceSerif4-LICENSE.md",
    "FONT-COPYRIGHTS.txt", "SOURCES.md", "font-provenance.json",
)
CSS_URL = re.compile(r"url\(\s*(?P<quote>['\"]?)(?P<url>[^)'\"]+)(?P=quote)\s*\)", re.I)
CSS_IMPORT = re.compile(r"(@import\s+)(['\"])([^'\"]+)\2", re.I)


class PackageError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> bytes:
    if not path.is_file():
        raise PackageError(f"Required file is missing: {path}")
    return path.read_bytes()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


class Plan:
    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}
        self.origins: dict[str, str] = {}
        self.resources: dict[Path, str] = {}
        self.references: list[tuple[str, str]] = []
        self.omitted: list[str] = []
        ledger = json.loads(read(AUDITS / "asset-rights.json"))
        self.rights = {item["file"]: item for item in ledger["assets"]}
        self.retained: set[str] = set()

    def add(self, name: str, data: bytes, origin: str) -> None:
        parts = PurePosixPath(name)
        if parts.is_absolute() or ".." in parts.parts or "\\" in name:
            raise PackageError(f"Unsafe package destination: {name}")
        if name in self.files and self.files[name] != data:
            raise PackageError(f"Conflicting package destination: {name}")
        self.files[name] = data
        self.origins[name] = origin

    def copy(self, path: Path, name: str) -> None:
        resolved = path.resolve()
        if not resolved.is_relative_to(ROOT):
            raise PackageError(f"Refusing to copy a file outside this project: {path}")
        self.add(name, read(resolved), str(resolved.relative_to(ROOT)))

    def local_path(self, value: str, source: Path) -> Path | None:
        parsed = urlsplit(value.strip())
        if not value.strip() or value.startswith("#") or parsed.scheme == "data":
            return None
        if parsed.scheme not in ("", "file") or parsed.netloc not in ("", "localhost"):
            raise PackageError(f"Offline rendering cannot depend on {value!r} in {source.name}")
        if parsed.scheme == "file":
            return Path(unquote(parsed.path)).resolve()
        return (source.parent / unquote(parsed.path)).resolve()

    def resource(self, path: Path) -> str:
        path = path.resolve()
        if path in self.resources:
            return self.resources[path]
        if path == HERE / "book.css":
            name = "book.css"
        elif path.is_relative_to(ASSETS):
            if path.suffix.lower() not in (".svg", ".otf", ".ttf", ".woff", ".woff2", ".css"):
                raise PackageError(f"Unexpected publication resource type: {path}")
            name = "assets/" + path.relative_to(ASSETS).as_posix()
        elif path.parent == IMAGES:
            record = self.rights.get(path.name)
            if not record or record["status"] != "retain":
                raise PackageError(f"Excluded or unaudited image referenced by publication: {path.name}")
            name = "assets/images/" + path.name
            self.retained.add(path.name)
        else:
            raise PackageError(f"Resource outside the approved asset locations: {path}")
        data = read(path)
        if path.parent == IMAGES and self.rights[path.name]["sha256"] != digest(data):
            raise PackageError(f"Image changed after rights audit: {path.name}")
        self.resources[path] = name
        if path.suffix.lower() == ".css":
            data = self.css(data.decode(), path, name).encode()
        elif path.suffix.lower() == ".svg":
            # Current artwork is standalone geometry. Inspect linked resources
            # without serializing or otherwise changing the original artwork.
            svg = BeautifulSoup(data, "xml")
            for element in svg.find_all(True):
                for attr in ("href", "xlink:href", "src"):
                    if element.has_attr(attr):
                        value = element[attr]
                        revised = self.ref(value, path, name)
                        if revised != value:
                            raise PackageError(f"SVG contains a nonportable linked resource: {path}")
                if element.has_attr("style"):
                    if self.css(element["style"], path, name) != element["style"]:
                        raise PackageError(f"SVG contains a nonportable CSS resource: {path}")
            for style in svg.find_all("style"):
                if self.css(style.get_text(), path, name) != style.get_text():
                    raise PackageError(f"SVG contains a nonportable style resource: {path}")
        self.add(name, data, str(path.relative_to(ROOT)))
        return name

    def ref(self, value: str, source: Path, destination: str) -> str:
        path = self.local_path(value, source)
        if path is None:
            return value
        target = self.resource(path)
        self.references.append((destination, target))
        parsed = urlsplit(value)
        relative = posixpath.relpath(target, posixpath.dirname(destination) or ".")
        return urlunsplit(("", "", relative, parsed.query, parsed.fragment))

    def css(self, text: str, source: Path, destination: str) -> str:
        # Reject unsupported escaping instead of silently missing a font/image.
        if "\\" in text and ("url(" in text.lower() or "@import" in text.lower()):
            raise PackageError(f"Escaped CSS URLs require explicit review: {source}")
        def replace_url(match: re.Match) -> str:
            revised = self.ref(match["url"].strip(), source, destination)
            if revised == match["url"].strip():
                return match[0]
            return "url('" + revised + "')"
        matches = list(CSS_URL.finditer(text))
        if len(matches) != len(re.findall(r"url\s*\(", text, re.I)):
            raise PackageError(f"Unparsed CSS URL in {source}")
        text = CSS_URL.sub(replace_url, text)
        return CSS_IMPORT.sub(
            lambda m: m[1] + m[2] + self.ref(m[3], source, destination) + m[2], text
        )

    def html(self, source: Path, destination: str, diagnostic: bool = False) -> None:
        soup = BeautifulSoup(read(source), "html.parser")
        if soup.find("base"):
            raise PackageError(f"Unexpected HTML base URL: {source}")
        for element in list(soup.find_all(True)):
            if diagnostic and element.name == "img" and element.has_attr("src"):
                path = self.local_path(element["src"], source)
                record = self.rights.get(path.name) if path else None
                if record and record["status"] == "replace":
                    placeholder = soup.new_tag("span", attrs={"class": "omitted-source-image"})
                    placeholder.string = f"[Original image not bundled: {path.name}. See audits/RIGHTS-AUDIT.md.]"
                    element.replace_with(placeholder)
                    self.omitted.append(path.name)
                    continue
            if element.has_attr("srcset"):
                raise PackageError(f"Unexpected srcset needs explicit packaging support: {source}")
            for attr in ("src", "poster", "data", "xlink:href"):
                if element.has_attr(attr):
                    element[attr] = self.ref(element[attr], source, destination)
            if element.has_attr("href"):
                if element.name == "link" or element["href"].startswith("file:"):
                    element["href"] = self.ref(element["href"], source, destination)
            if element.has_attr("style"):
                element["style"] = self.css(element["style"], source, destination)
            if element.name == "style":
                element.string = self.css(element.get_text(), source, destination)
        result = str(soup)
        if "file://" in result:
            raise PackageError(f"Unconverted file URL in {destination}")
        self.add(destination, result.encode(), str(source.relative_to(ROOT)))

    def validate(self) -> None:
        for source, target in self.references:
            if target not in self.files:
                raise PackageError(f"Missing packaged resource: {source} -> {target}")
        for notice in FONT_NOTICES:
            if "assets/fonts/" + notice not in self.files:
                raise PackageError(f"Missing required font license/provenance: {notice}")
        for notice in FONT_NOTICES[:2]:
            if b"OPEN FONT LICENSE" not in self.files["assets/fonts/" + notice].upper():
                raise PackageError(f"Unexpected font license content: {notice}")
        provenance = json.loads(self.files["assets/fonts/font-provenance.json"])
        records = {item["file"]: item for item in provenance}
        for name, data in self.files.items():
            if name.startswith("assets/fonts/") and Path(name).suffix in (".otf", ".ttf", ".woff", ".woff2"):
                record = records.get(Path(name).name)
                if not record or record["sha256"] != digest(data):
                    raise PackageError(f"Font does not match provenance: {name}")
        for filename, record in self.rights.items():
            if record["status"] != "retain" and "assets/images/" + filename in self.files:
                raise PackageError(f"Excluded image entered the package: {filename}")


def make_plan() -> Plan:
    plan = Plan()
    baseline = json.loads(read(AUDITS / "baseline.json"))
    metadata = json.loads(read(BOOK / "book.json"))
    sections = [s["file"] for s in metadata["sections"]]
    if len(sections) != 30 or len(set(sections)) != 30 or set(sections) != set(baseline):
        raise PackageError("Expected the complete 30-section reviewed manuscript baseline")
    for filename in sections:
        if Path(filename).name != filename or not filename.endswith(".md"):
            raise PackageError(f"Unsafe manuscript filename: {filename}")
        if digest(read(BOOK / filename)) != baseline[filename]:
            raise PackageError(f"Manuscript changed after publication baseline: {filename}")
        plan.copy(BOOK / filename, "manuscript/" + filename)
    plan.copy(BOOK / "book.json", "manuscript/book.json")
    plan.add("manuscript/baseline-sha256.json", json_bytes({
        **baseline, "book.json": digest(read(BOOK / "book.json")),
    }), "Reviewed section baseline plus packaged manifest checksum")

    for filename in ("interior.html", "front-cover.html"):
        plan.html(OUT / filename, filename)
    included_in_publication = set(plan.retained)
    plan.html(OUT / "source-rendered.html", "source-rendered.html", diagnostic=True)
    if plan.retained != included_in_publication:
        raise PackageError("Diagnostic source HTML introduces images absent from the publication")
    for filename in FONT_NOTICES:
        plan.copy(ASSETS / "fonts" / filename, "assets/fonts/" + filename)

    # Retain provenance for included editable motifs, without bundling unused
    # illustrations, proof sheets, generator scratch files or excluded rasters.
    motif_manifest = json.loads(read(ASSETS / "motifs/manifest.json"))
    selected = []
    for item in motif_manifest["assets"]:
        if "assets/motifs/" + item["file"] in plan.files:
            item = dict(item)
            item.pop("monochrome", None)
            selected.append(item)
    motif_manifest["assets"] = selected
    motif_manifest["package_note"] = "Only referenced motifs are bundled. Cover artwork is assets/cover-art.svg."
    plan.add("assets/motifs/manifest.json", json_bytes(motif_manifest), "Filtered publication/assets/motifs/manifest.json")

    audit_names = []
    for path in sorted(AUDITS.iterdir()):
        if path.is_file() and not path.name.startswith(".") and path.suffix in (".md", ".json"):
            plan.copy(path, "audits/" + path.name)
            if path.suffix == ".md":
                audit_names.append(path.name)
    build = json.loads(read(OUT / "build.json"))
    if build["source_sha256"] != baseline or build["sections"] != 30:
        raise PackageError("Build record differs from the reviewed manuscript baseline")
    if set(build["included_images"]) != included_in_publication:
        raise PackageError("Publication images do not match build.json")
    pdf_names = set()
    for record in build["outputs"].values():
        path = Path(record["path"])
        if not path.is_absolute():
            path = OUT / path
        if path.resolve().parent != OUT or path.suffix != ".pdf":
            raise PackageError(f"Unexpected output in build record: {path}")
        if digest(read(path)) != record["sha256"]:
            raise PackageError(f"PDF differs from build record; finish rebuilding first: {path.name}")
        plan.copy(path, "pdfs/" + path.name)
        record["path"] = "pdfs/" + path.name
        pdf_names.add(path.name)
    for filename in ("Surviving-the-Singularity-print-interior.pdf", "Surviving-the-Singularity-interior-print.pdf"):
        path = OUT / filename
        if path.exists() and filename not in pdf_names:
            plan.copy(path, "pdfs/" + filename)
            pdf_names.add(filename)
    if "Surviving-the-Singularity-reading.pdf" not in pdf_names:
        raise PackageError("Final reading PDF is required")
    build["package_note"] = "PDF paths rewritten relative to this package; other build evidence preserved."
    plan.add("build.json", json_bytes(build), "publication/output/build.json with portable PDF paths")

    links = "\n".join(f"- [{name}](audits/{name})" for name in audit_names)
    pdf_links = "\n".join(f"- [{name}](pdfs/{name})" for name in sorted(pdf_names))
    weasy_version = version("weasyprint")
    readme = f"""# Surviving the Singularity: editable publication package

Manuscript v{metadata['version']}, publication design {build['design_version']}.
This is an editable production handoff and review copy. It is not an approval
for public sale or a substitute for the publisher's production and rights review.

## Edit and regenerate

Edit `interior.html`, `front-cover.html`, `book.css`, or the SVGs in `assets/`.
All rendering assets are included. The HTML has relative local resource URLs.
The bundled static fonts are Adobe Source Serif 4 and Source Sans Pro.
Keep their licenses, copyright notices and provenance with any redistribution.

From this directory, with WeasyPrint {weasy_version} and its system dependencies
installed, generate new PDFs under new names so the supplied proofs stay intact:

```sh
weasyprint --full-fonts interior.html regenerated-interior.pdf
weasyprint --full-fonts front-cover.html regenerated-front-cover.pdf
```

These commands regenerate the layout PDFs. They do not impose printer pages,
convert to a printer color profile, create a wraparound cover, or certify PDF/X.
The supplied reading PDF includes the cover and interior, with page labels.
Printer-specific conversion, stock, binding, bleed and spine dimensions remain
production decisions. See the companion production and review notes below.

The 30 Markdown sections and `book.json` in `manuscript/` are unchanged source
snapshots. `manuscript/baseline-sha256.json` records their checksums. Editing them
does not automatically update the included HTML. The original repository build
performs manuscript-to-layout transformations; this portable package provides
the fully editable final HTML and CSS independently of that repository.

`source-rendered.html` is a diagnostic rendering of the original manuscript,
not the publication interior. Its {len(plan.omitted)} excluded image elements have
been replaced with explicit placeholders. Original surrounding captions remain
as source evidence. No excluded raster artwork is bundled. Publication image
substitutions and caption corrections are recorded in `build.json` and the audits.
The original cover was also replaced in this design.

## Supplied PDFs

{pdf_links}

## Publisher production and review notes

{links}

`audits/asset-rights.json` records authors, sources, license URLs, modifications
and unresolved limitations. Image licenses apply to the relevant images, not
the manuscript. The epigraph review in the rights audit identifies remaining
publication decisions. Generated narrative plates are fictional illustrations;
their provenance does not establish exclusive copyright in every output.

## Package verification

`package-manifest.json` records every bundled file's SHA-256, size and source,
except the manifest itself. `build.json` preserves PDF hashes and source hashes;
its PDF paths are portable. External citation and license links require network
access, but page rendering does not. Font and artwork provenance may retain
historical source-location text; those locations are not rendering dependencies.
Only explicitly selected publication files are included. No credentials,
environment files, repository history, excluded images or proof-sheet clutter
are copied.
"""
    plan.add("README.md", readme.encode(), "Generated portable production handoff")
    plan.validate()
    plan.add("package-manifest.json", json_bytes({
        "schema": "sts-editable-publication-package/v1",
        "manuscript_version": metadata["version"],
        "weasyprint_version": weasy_version,
        "diagnostic_image_placeholders": plan.omitted,
        "files": [{"path": name, "sha256": digest(data), "bytes": len(data),
                   "origin": plan.origins[name]} for name, data in sorted(plan.files.items())],
    }), "Generated checksums; excludes this manifest itself")
    return plan


def export(plan: Plan) -> None:
    if ZIP.exists():
        raise PackageError(f"Archive already exists; preserve it before a new export: {ZIP}")
    if PACKAGE.exists():
        if PACKAGE.is_symlink():
            raise PackageError("Package directory must not be a symbolic link")
        for path in PACKAGE.rglob("*"):
            if path.is_symlink():
                raise PackageError(f"Unexpected symbolic link in package: {path}")
            if path.is_file():
                name = path.relative_to(PACKAGE).as_posix()
                if name not in plan.files or read(path) != plan.files[name]:
                    raise PackageError(f"Existing package contains an edited or stale file; preserve it first: {name}")
    for name, data in sorted(plan.files.items()):
        path = PACKAGE / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            with path.open("xb") as handle:
                handle.write(data)
        if read(path) != data:
            raise PackageError(f"Package readback differs: {name}")
    with zipfile.ZipFile(ZIP, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(plan.files.items()):
            archive.writestr("Surviving-the-Singularity-editable-publication/" + name, data)
    with zipfile.ZipFile(ZIP) as archive:
        bad = archive.testzip()
        if bad:
            raise PackageError(f"ZIP verification failed: {bad}")
        for name, data in plan.files.items():
            if archive.read("Surviving-the-Singularity-editable-publication/" + name) != data:
                raise PackageError(f"ZIP readback differs: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate entirely in memory; do not write package or ZIP")
    args = parser.parse_args()
    os.environ["DAILY_NOTE_AGENT"] = "codex"
    try:
        plan = make_plan()
        size = sum(map(len, plan.files.values()))
        print(f"Validated {len(plan.files)} files, {size / 1024 / 1024:.1f} MiB, {len(plan.retained)} retained source images.")
        if args.check:
            print("Check only: package directory and ZIP were not written.")
        else:
            export(plan)
            print(f"Editable package: {PACKAGE}\nArchive: {ZIP}")
    except (PackageError, KeyError, ValueError, OSError) as error:
        print(f"Package failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
