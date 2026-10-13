"""Render registered artwork from actual final PDFs without changing them.

Run after publication/build.py, publication/production.py and publication/proof.py.
The layout capture selects pages; image inspection remains a human review step.
"""
from concurrent.futures import ThreadPoolExecutor
from collections import Counter, defaultdict
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "publication/output"
PDFS = {
    "interior": "Surviving-the-Singularity-interior.pdf",
    "print": "Surviving-the-Singularity-print-interior.pdf",
    "reading": "Surviving-the-Singularity-reading.pdf",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", default="final", choices=("initial", "final"))
    parser.add_argument("--editions", default="interior,print")
    parser.add_argument("--non-cutouts", action="store_true")
    parser.add_argument("--prepared-color", action="store_true",
                        help="Render the verified resource-pruned color PDF")
    parser.add_argument("--dpi", default=140, type=int)
    args = parser.parse_args()
    editions = args.editions.split(",")
    if any(x not in PDFS for x in editions) or len(editions) != len(set(editions)):
        parser.error("editions must be interior, print and/or reading")
    assert args.dpi > 0, 'DPI must be positive'
    source = ROOT / 'src/lib/data/book'
    meta = json.loads((source / 'book.json').read_text())
    assert meta['version'] == HERE.parent.name.removeprefix('v'), 'Wrong edition sample directory'
    registry_path = source / 'visuals.json'
    registry = json.loads(registry_path.read_text())['images']
    references = Counter(name for section in meta['sections']
                         for name in re.findall(r'\]\(/book-images/([^\s)]+)\)', (source / section['file']).read_text()))
    expected = Counter({name: count for name, count in references.items() if name in registry})
    assert set(registry) == set(expected), 'Registry contains artwork absent from source'

    target_dir = HERE / args.stage
    target_dir.mkdir(parents=True, exist_ok=True)
    layout_file = OUT / "interior-figure-layout.json"
    layout_digest = digest(layout_file)
    layout = json.loads(layout_file.read_text())
    assert layout["html_sha256"] == digest(OUT / "interior.html"), "Stale layout capture"
    assert layout["registry_sha256"] == digest(registry_path), "Stale registry capture"
    captured = Counter(figure['file'] for page in layout['pages'] for figure in page['figures'])
    assert captured == expected, 'Layout must cover each registered source occurrence'
    source_records = {}
    render_inputs = {}
    for edition in editions:
        pdf = OUT / PDFS[edition]
        source_records[edition] = {
            "path": str(pdf.relative_to(ROOT)),
            "sha256": digest(pdf),
            "pages": len(PdfReader(pdf).pages),
        }
        render_inputs[edition] = pdf
    if args.prepared_color:
        assert "interior" in editions, "Prepared color applies to the interior edition"
        build = json.loads((OUT / "build.json").read_text())
        pruning = build["outputs"]["print-interior"]["resource_pruning"]
        prepared = OUT / "print-prepared.pdf"
        assert pruning["input_sha256"] == source_records["interior"]["sha256"]
        assert pruning["prepared_sha256"] == digest(prepared)
        assert pruning["page_streams_unchanged"] and pruning["annotation_descriptors_unchanged"]
        assert all(pruning["controls"].values())
        source_records["interior"]["rendering_source"] = {
            "path": str(prepared.relative_to(ROOT)),
            "sha256": digest(prepared),
            "page_streams_unchanged": True,
            "annotation_descriptors_unchanged": True,
        }
        render_inputs["interior"] = prepared

    tasks = []
    occurrence_counts = Counter()
    for page in layout["pages"]:
        for figure in page["figures"]:
            if args.non_cutouts and figure["file"].startswith("v101-cutout-"):
                continue
            label = Path(figure["file"]).stem.removeprefix("v101-")
            occurrence_counts[(page['page'], figure['file'])] += 1
            occurrence = occurrence_counts[(page['page'], figure['file'])]
            if occurrence > 1:
                label += f'-occurrence-{occurrence}'
            folios = [item["text"] for item in page["other_text"]
                      if re.fullmatch(r"\d+", item["text"].strip()) and item["rect"][1] > 790]
            for edition in editions:
                physical_page = page["page"] + (edition == "reading")
                assert physical_page <= source_records[edition]["pages"]
                tasks.append({
                    "edition": edition,
                    "physical_page": physical_page,
                    "printed_folio": folios[-1] if folios else None,
                    "figure": figure["file"],
                    "caption_fragments": [x["text"] for x in figure["caption_boxes"]],
                    "render": str((target_dir / f"{edition}-{physical_page:03d}-{label}.png").relative_to(HERE)),
                })

    def render_edition(edition):
        selection = [task for task in tasks if task["edition"] == edition]
        page_numbers = sorted({task["physical_page"] for task in selection})
        destinations = defaultdict(list)
        for task in selection:
            destinations[task['physical_page']].append(HERE / task['render'])
        page_list = ",".join(str(page) for page in page_numbers)
        subprocess.run([
            "gs", "-q", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m",
            "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", f"-r{args.dpi}",
            f"-sPageList={page_list}",
            f"-sOutputFile={target_dir / (edition + '-sample-%03d.png')}",
            str(render_inputs[edition]),
        ], check=True, stdout=subprocess.DEVNULL)
        for sequence, page_number in enumerate(page_numbers, 1):
            generated = target_dir / f"{edition}-sample-{sequence:03d}.png"
            targets = destinations[page_number]
            generated.replace(targets[0])
            # Several registered figures can share one PDF page. Retain a
            # complete capture under every manifest entry instead of losing
            # all but the last figure's destination in a dict overwrite.
            for target in targets[1:]:
                target.write_bytes(targets[0].read_bytes())
        return [{**task, "sha256": digest(HERE / task["render"])} for task in selection]

    with ThreadPoolExecutor(max_workers=2) as pool:
        samples = [sample for result in pool.map(render_edition, editions) for sample in result]
    assert digest(layout_file) == layout_digest, "Layout capture changed while rendering"
    for edition, record in source_records.items():
        assert digest(OUT / PDFS[edition]) == record["sha256"], f"{edition} PDF changed while rendering"
        if "rendering_source" in record:
            assert digest(render_inputs[edition]) == record["rendering_source"]["sha256"]

    record = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "version": meta['version'],
        "source_image_references": sum(references.values()),
        "registered_figures": len(registry),
        "registered_source_occurrences": sum(expected.values()),
        "stage": args.stage,
        "dpi": args.dpi,
        "renderer": subprocess.check_output(["gs", "--version"], text=True).strip(),
        "pdfs": source_records,
        "layout_sha256": layout_digest,
        "build_sha256": digest(OUT / "build.json"),
        "page_number_note": "Physical PDF pages; reading adds one cover page. Folios come from the interior layout capture.",
        "samples": samples,
        "limits": "Raster evidence only. The review report identifies visual findings; this script does not certify appearance or physical print quality.",
    }
    manifest = HERE / f"{args.stage}-samples.json"
    manifest.write_text(json.dumps(record, indent=2) + "\n")
    assert json.loads(manifest.read_text()) == record
    print(f"Rendered {len(samples)} samples at {args.dpi} dpi; source hashes stayed unchanged.")
    print(manifest.relative_to(ROOT))


if __name__ == "__main__":
    main()
