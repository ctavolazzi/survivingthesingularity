"""Use captured layout to select raster samples from the final PDF bytes."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import subprocess
import unicodedata

from bs4 import BeautifulSoup
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'publication/output'
TARGET = HERE / 'pdf-proof'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s).lower())


def main():
    TARGET.mkdir(exist_ok=True)
    pdfs = {kind: OUT / f'Surviving-the-Singularity-{suffix}.pdf'
            for kind, suffix in [('interior', 'interior'), ('print', 'print-interior')]}
    records = {kind: {'path': str(path.relative_to(ROOT)), 'sha256': sha(path),
                     'pages': len(PdfReader(path).pages)} for kind, path in pdfs.items()}
    reader = PdfReader(pdfs['interior'])
    geometry_path = OUT / 'interior-layout.json'
    geometry = json.loads(geometry_path.read_text())
    assert len(geometry) == len(reader.pages)
    page_text = [norm(' '.join(box['text'] for box in page['boxes'])) for page in geometry]
    selected = {1, 4, len(reader.pages) - 1, len(reader.pages)}
    edits = [edit for name in ('opening', 'middle', 'ending')
             for edit in json.loads((HERE / f'{name}-review.json').read_text())['edits']]
    locations = []
    for edit in edits:
        html = subprocess.run(['pandoc', '--from=markdown', '--to=html'], input=edit['after'],
                              capture_output=True, text=True, check=True).stdout
        soup = BeautifulSoup(html, 'html.parser')
        found = set()
        for element in soup.find_all(['p', 'li', 'h1', 'h2', 'h3']):
            text = norm(element.get_text(' ', strip=True))
            if not text:
                continue
            # Endpoint excerpts locate the revised blocks, including blocks spanning pages.
            for excerpt in (text[:30], text[-30:]):
                hits = [index + 1 for index, body in enumerate(page_text) if excerpt in body]
                assert hits, ('Revised excerpt not found in final PDF', edit['file'], excerpt)
                found.update(hits)
        assert found, edit['file']
        selected.update(found)
        locations.append({'file': Path(edit['file']).name, 'reason': edit['reason'], 'pages': sorted(found)})
    layout = json.loads((OUT / 'interior-figure-layout.json').read_text())
    for page in layout['pages']:
        if any(figure['file'].startswith('v103-') for figure in page['figures']):
            selected.add(page['page'])
    for page in geometry:
        if not page['boxes'] and not page['images']:
            selected.update([page['page'] - 1, page['page'], page['page'] + 1])
    # The previous pass repaired Chapter 19's opening. Keep that transition in view.
    chapter = [page['page'] for page in geometry
               if any(box['tag'] == 'h1' and 'The Ladder' in box['text'] for box in page['boxes'])]
    if chapter:
        selected.update([chapter[0] - 1, chapter[0]])
    pages = sorted(p for p in selected if 1 <= p <= len(reader.pages))
    prepared = OUT / 'print-prepared.pdf'
    build = json.loads((OUT / 'build.json').read_text())
    preparation = build['outputs']['print-interior']['resource_pruning']
    # production.py produced this color-equivalent resource-pruned input for efficient rasterization.
    assert prepared.is_file() and len(PdfReader(prepared).pages) == len(reader.pages)
    assert preparation['input_sha256'] == records['interior']['sha256']
    assert preparation['prepared_sha256'] == sha(prepared)
    assert preparation['page_streams_unchanged'] and preparation['annotation_descriptors_unchanged']

    def render(kind):
        source = prepared if kind == 'interior' else pdfs[kind]
        page_list = pages + ([records[kind]['pages']] if kind == 'print' and records[kind]['pages'] > len(reader.pages) else [])
        pattern = TARGET / f'{kind}-%03d.png'
        subprocess.run(['gs', '-q', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m',
                        '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4', '-r150',
                        '-sPageList=' + ','.join(map(str, page_list)),
                        '-sOutputFile=' + str(pattern), str(source)], check=True)
        return [{'edition': kind, 'physical_page': page, 'path': str((TARGET / f'{kind}-{i:03d}.png').relative_to(ROOT)),
                 'sha256': sha(TARGET / f'{kind}-{i:03d}.png')}
                for i, page in enumerate(page_list, 1)]

    with ThreadPoolExecutor(max_workers=2) as pool:
        samples = [entry for group in pool.map(render, pdfs) for entry in group]
    for kind, path in pdfs.items():
        assert sha(path) == records[kind]['sha256'], 'PDF changed during rendering'
    report = {'version': '0.10.4', 'created_utc': datetime.now(timezone.utc).isoformat(),
              'pdfs': records, 'prepared_color_sha256': sha(prepared), 'resource_preparation': preparation,
              'selection_layout_sha256': sha(geometry_path),
              'dpi': 150, 'edits': locations, 'samples': samples,
              'limits': 'Raster samples of all revised blocks, eight retained recent figures and selected transitions. Full source/geometry proof is separate; visual judgment is recorded after inspection.'}
    p = TARGET / 'final-samples.json'
    p.write_text(json.dumps(report, indent=2) + '\n')
    assert json.loads(p.read_text()) == report
    print('Rendered', len(samples), 'samples covering', len(locations), 'editorial changes')


if __name__ == '__main__':
    main()
