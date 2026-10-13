"""Locate every new text block in final PDF layout and raster those pages."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import subprocess
import unicodedata

from pypdf import PdfReader
from _additions import additions

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'publication/output'
TARGET = HERE / 'pdf-proof'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', value).lower())


def main():
    source_report, changes = additions()
    TARGET.mkdir(exist_ok=True)
    pdfs = {'interior': OUT / 'Surviving-the-Singularity-interior.pdf',
            'print': OUT / 'Surviving-the-Singularity-print-interior.pdf'}
    files = {kind: {'path': str(path.relative_to(ROOT)), 'sha256': digest(path),
                    'pages': len(PdfReader(path).pages)} for kind, path in pdfs.items()}
    geometry_path = OUT / 'interior-layout.json'
    geometry = json.loads(geometry_path.read_text())
    assert len(geometry) == files['interior']['pages']
    page_text = [normalize(' '.join(box['text'] for box in page['boxes'])) for page in geometry]
    selected = {1, 4, files['interior']['pages']}
    records = []
    for change in changes:
        found = set()
        for node in change['nodes']:
            text = normalize(node['text'])
            if not text:
                continue
            for excerpt in (text[:36], text[-36:]):
                pages = [index + 1 for index, value in enumerate(page_text) if excerpt in value]
                assert pages, ('New text endpoint absent from PDF layout', change['file'], excerpt)
                found.update(pages)
        assert found, ('New block not located', change)
        selected.update(found)
        records.append({'file': change['file'], 'block': change['block'], 'pages': sorted(found)})
    # The Rosa hearing and continuing closing scene must remain visible.
    for index, text in enumerate(page_text):
        if 'theladder' in text or 'backtobearflag' in text:
            selected.update({index, index + 1, index + 2})
    pages = sorted(page for page in selected if 1 <= page <= files['interior']['pages'])
    build = json.loads((OUT / 'build.json').read_text())
    preparation = build['outputs']['print-interior']['resource_pruning']
    prepared = OUT / 'print-prepared.pdf'
    assert digest(prepared) == preparation['prepared_sha256']
    assert files['interior']['sha256'] == preparation['input_sha256']
    assert preparation['page_streams_unchanged'] and preparation['annotation_descriptors_unchanged']

    def render(kind):
        source = prepared if kind == 'interior' else pdfs[kind]
        page_list = list(pages)
        if kind == 'print' and files[kind]['pages'] > files['interior']['pages']:
            page_list.append(files[kind]['pages'])
        subprocess.run(['gs', '-q', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m',
                        '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4', '-r150',
                        '-sPageList=' + ','.join(map(str, page_list)),
                        '-sOutputFile=' + str(TARGET / (kind + '-%03d.png')), str(source)], check=True)
        return [{'edition': kind, 'physical_page': page,
                 'path': str((TARGET / f'{kind}-{index:03d}.png').relative_to(ROOT)),
                 'sha256': digest(TARGET / f'{kind}-{index:03d}.png')}
                for index, page in enumerate(page_list, 1)]

    with ThreadPoolExecutor(max_workers=2) as pool:
        samples = [record for group in pool.map(render, pdfs) for record in group]
    assert all(digest(pdfs[kind]) == item['sha256'] for kind, item in files.items()), 'PDF changed during rasterization'
    report = {'version': source_report['version'], 'created_utc': datetime.now(timezone.utc).isoformat(),
              'pdfs': files, 'source_preservation_sha256': digest(HERE / 'source-preservation.json'),
              'geometry_sha256': digest(geometry_path), 'dpi': 150, 'new_blocks': records, 'samples': samples,
              'limits': 'Endpoint text selects raster samples; publication/proof.py separately checks complete PDF text. Screenshots require visual inspection and do not certify physical printing.'}
    path = TARGET / 'final-samples.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    assert json.loads(path.read_text()) == report
    print(json.dumps({'version': report['version'], 'new_blocks': len(records),
                      'selected_pages': len(pages), 'raster_samples': len(samples)}))


if __name__ == '__main__':
    main()
