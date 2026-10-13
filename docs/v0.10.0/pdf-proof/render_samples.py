"""Render bounded final-PDF review samples without modifying publication PDFs."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / 'publication/output'
DPI = 140

# Interior physical pages; the reading edition prepends its cover.
INTERIOR = {
    1: 'title', 2: 'copyright', 3: 'contents-1', 4: 'contents-2',
    11: 'food-chart', 12: 'food-chart-following', 37: 'part-1',
    97: 'part-2', 98: 'cooperative-portraits',
    155: 'regional-production', 156: 'regional-production-following',
    165: 'part-3', 189: 'model-memory-equations', 190: 'heat-equations',
    191: 'cooling-loop', 192: 'cooling-following',
    266: 'mesh-node', 267: 'mesh-following',
    270: 'fabrication', 271: 'fabrication-following',
    304: 'conclusion-opening', 311: 'conclusion-bookend',
    312: 'conclusion-continuation', 313: 'conclusion-end',
    329: 'dense-bibliography', 333: 'epigraph-bibliography',
    335: 'bibliography-ending', 365: 'discussion-appendix',
    369: 'credits-opening', 370: 'credits-continued',
    371: 'credits-continued', 372: 'credits-ending',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(item):
    pdf, physical_page, name = item
    target = HERE / name
    subprocess.run([
        'gs', '-q', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m',
        '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4', f'-r{DPI}',
        f'-dFirstPage={physical_page}', f'-dLastPage={physical_page}',
        f'-sOutputFile={target}', str(pdf),
    ], check=True, stdout=subprocess.DEVNULL)
    return {'pdf': pdf.name, 'physical_page': physical_page,
            'render': target.name, 'sha256': digest(target)}


def main():
    pdf = OUT / 'Surviving-the-Singularity-reading.pdf'
    before = digest(pdf)
    tasks = [(pdf, 1, 'reading-001-cover.png')]
    tasks += [(pdf, p + 1, f'reading-{p+1:03d}-{label}.png')
              for p, label in INTERIOR.items()]
    with ThreadPoolExecutor(max_workers=3) as pool:
        samples = list(pool.map(render, tasks))
    assert digest(pdf) == before, 'PDF changed during review rendering'
    record = {
        'review_date': '2026-09-27', 'dpi': DPI,
        'source_pdf': str(pdf.relative_to(ROOT)), 'source_sha256': before,
        'interior_sha256': digest(OUT / 'Surviving-the-Singularity-interior.pdf'),
        'build_sha256': digest(OUT / 'build.json'),
        'page_number_note': 'Physical PDF pages; reading page = interior page + 1.',
        'samples': samples,
        'limits': 'Representative-page visual review; not a full-page, printer, accessibility, or rights certification.',
    }
    (HERE / 'reading-samples.json').write_text(json.dumps(record, indent=2) + '\n')
    print(f'{len(samples)} reading samples rendered; PDF hash remained {before}')


if __name__ == '__main__':
    main()
