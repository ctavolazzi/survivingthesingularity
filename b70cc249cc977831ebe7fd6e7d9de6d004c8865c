"""Verify fresh local proofs and make versioned, immutable delivery copies.

Creates no package, commit, public download or deployment. Include an already
prepared editable ZIP only with --include-package. Visual judgment is recorded
separately and is never inferred from automated checks.
"""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import zipfile

from pypdf import PdfReader
from check_source_preservation import asset_matches

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'publication/output'
SOURCE = ROOT / 'src/lib/data/book'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def validate_pdf_samples(report, version):
    """Bind the sample receipt to current PDFs, geometry, source, and PNGs."""
    assert report['version'] == version, 'Wrong PDF sample edition'
    assert report['source_preservation_sha256'] == digest(HERE / 'source-preservation.json'), 'Stale PDF sample source proof'
    assert report['geometry_sha256'] == digest(OUT / 'interior-layout.json'), 'Stale PDF sample geometry'
    paths = {'interior': OUT / 'Surviving-the-Singularity-interior.pdf',
             'print': OUT / 'Surviving-the-Singularity-print-interior.pdf'}
    assert set(report['pdfs']) == set(paths), 'Missing sampled PDF edition'
    for kind, path in paths.items():
        record = report['pdfs'][kind]
        assert record['path'] == str(path.relative_to(ROOT)), 'Unexpected sampled PDF path'
        assert record['sha256'] == digest(path), 'Stale sampled PDF: ' + kind
        assert record['pages'] == len(PdfReader(path).pages), 'Stale sampled PDF page count: ' + kind
    seen, files = set(), set()
    for sample in report['samples']:
        kind, page = sample['edition'], sample['physical_page']
        assert kind in paths and isinstance(page, int) and 1 <= page <= report['pdfs'][kind]['pages'], 'Invalid raster sample page'
        key = (kind, page)
        assert key not in seen, 'Duplicate raster sample page'
        seen.add(key)
        path = ROOT / sample['path']
        assert path.parent == HERE / 'pdf-proof' and path.suffix == '.png', 'Unexpected raster sample path'
        assert path not in files, 'Reused raster sample file'
        files.add(path)
        assert sample['sha256'] == digest(path), 'Stale raster sample: ' + sample['path']
    assert {kind for kind, _ in seen} == set(paths), 'Missing raster sample edition'
    assert report['new_blocks'], 'Missing PDF addition sample coverage'
    for block in report['new_blocks']:
        assert block['pages'], 'New text block has no raster sample page'
        for kind in paths:
            assert all((kind, page) in seen for page in block['pages']), 'New text block lacks a raster sample: ' + block['file']


def pdf_sample_negative_controls(report, version):
    """Reject altered copies of the real receipt through the production gate."""
    validate_pdf_samples(report, version)
    controls = []
    mutations = {
        'stale sample source proof rejected': lambda item: item.update(source_preservation_sha256='0' * 64),
        'stale sample geometry rejected': lambda item: item.update(geometry_sha256='0' * 64),
        'stale interior PDF sample hash rejected': lambda item: item['pdfs']['interior'].update(sha256='0' * 64),
        'stale print PDF sample hash rejected': lambda item: item['pdfs']['print'].update(sha256='0' * 64),
        'stale raster sample hash rejected': lambda item: item['samples'][0].update(sha256='0' * 64),
        'missing print raster coverage rejected': lambda item: item.update(samples=[sample for sample in item['samples'] if sample['edition'] != 'print']),
        'missing addition coverage rejected': lambda item: item.update(new_blocks=[]),
    }
    for label, mutate in mutations.items():
        damaged = copy.deepcopy(report)
        mutate(damaged)
        try:
            validate_pdf_samples(damaged, version)
        except AssertionError:
            controls.append(label)
        else:
            raise AssertionError('Negative control unexpectedly passed: ' + label)
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-package', action='store_true')
    args = parser.parse_args()
    meta = read(SOURCE / 'book.json')
    version = meta['version']
    assert version == '0.11.0', 'Wrong edition'
    preservation = read(HERE / 'source-preservation.json')
    assert not preservation['errors'] and preservation['version'] == version
    assert preservation['index_sha256'] == digest(SOURCE / 'manuscript-index.json'), 'Stable-ID sidecar changed since source proof'
    frozen = read(ROOT / 'docs/publication/baseline.json')
    assert frozen == preservation['current_source_sha256']
    for name, expected in frozen.items():
        assert digest(SOURCE / name) == expected, 'Source changed after proofs: ' + name
    assert preservation['asset_files_checked'] == len(preservation['assets']) > 0, 'Missing retained artwork proof'
    for asset in preservation['assets']:
        path = ROOT / asset['file']
        assert asset['unchanged'] and path.is_file() and asset_matches(path.read_bytes(), asset['git_blob']), 'Artwork changed after source proof: ' + asset['file']
    pdf = read(HERE / 'pdf-checks.json')
    assert pdf['status'] == 'pass' and pdf['source_sha256'] == frozen
    for record in pdf['outputs'].values():
        path = Path(record['path'])
        assert digest(path if path.is_absolute() else OUT / path) == record['sha256'], 'Stale PDF proof'
    assert pdf['proof_sha256'] == digest(OUT / 'proof/checks.json')
    assert pdf['source_rendered_sha256'] == digest(OUT / 'source-rendered.html')
    assert pdf['geometry_sha256'] == digest(OUT / 'interior-layout.json')
    samples = read(HERE / 'pdf-proof/final-samples.json')
    sample_controls = pdf_sample_negative_controls(samples, version)
    resources = read(ROOT / 'docs/publication/PDF-RESOURCE-CHECKS.json')
    assert resources['overall_pass'] and all(resources['negative_controls'].values())
    for record in resources['files'].values():
        assert digest(Path(record['path'])) == record['sha256'], 'Stale PDF resources'
    epub = ROOT / 'book-build' / f'Surviving-the-Singularity-v{version}.epub'
    structural = read(HERE / 'epub-checks.json')
    layout = read(HERE / 'epub-proof/checks.json')
    additions = read(HERE / 'epub-proof/additions.json')
    assert structural['source_sha256'] == frozen and structural['version'] == version
    assert digest(epub) == structural['epub_sha256'] == layout['epub_sha256'] == additions['epub_sha256']
    assert not any(structural[key] for key in ('missing_blocks', 'resource_errors', 'art_errors'))
    assert not layout['layout_errors'] and not layout['missing_requests']
    assert additions['status'] == 'pass' and not additions['missing_requests']
    build = read(OUT / 'build.json')
    deliveries = []
    for kind, suffix in [('reading', ''), ('print-interior', '-print-interior'), ('front-cover', '-front-cover')]:
        source = OUT / f'Surviving-the-Singularity-{kind}.pdf'
        assert digest(source) == build['outputs'][kind]['sha256']
        target = ROOT / 'book-build' / f'Surviving-the-Singularity-v{version}{suffix}.pdf'
        if target.exists():
            assert digest(target) == digest(source), 'Refusing to replace changed delivery: ' + str(target)
        else:
            shutil.copyfile(source, target)
        assert digest(target) == digest(source)
        deliveries.append({'kind': kind, 'path': str(target.relative_to(ROOT)), 'bytes': target.stat().st_size,
                           'sha256': digest(target), 'pages': len(PdfReader(target).pages)})
    artifacts = [('epub', epub), ('markdown', ROOT / 'manuscript' / f'Surviving-the-Singularity-v{version}.md')]
    if args.include_package:
        package = OUT / f'Surviving-the-Singularity-v{version}-editable-publication.zip'
        with zipfile.ZipFile(package) as archive:
            assert archive.testzip() is None
            prefix = 'Surviving-the-Singularity-editable-publication/manuscript/'
            for name, expected in frozen.items():
                assert hashlib.sha256(archive.read(prefix + name)).hexdigest() == expected, 'Packaged source changed: ' + name
        artifacts.append(('editable_package', package))
    for kind, path in artifacts:
        deliveries.append({'kind': kind, 'path': str(path.relative_to(ROOT)),
                           'bytes': path.stat().st_size, 'sha256': digest(path)})
    receipts = ['source-preservation.json', 'pdf-checks.json', 'epub-checks.json',
                'epub-proof/checks.json', 'epub-proof/additions.json', 'pdf-proof/final-samples.json']
    report = {'version': version, 'prepared_utc': datetime.now(timezone.utc).isoformat(),
              'baseline_ref': preservation['baseline_ref'], 'baseline_commit': preservation['baseline_commit'],
              'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'source_uncommitted': True, 'status': 'Local digital artifacts prepared and automated proofs passed',
              'public_release': meta['released'], 'sections': len(meta['sections']),
              'images': sum(section['image_references'] for section in preservation['sections']),
              'registered_figures': structural['registry_entries'], 'added_graphics': 0,
              'changed_sections': sum(section['before_sha256'] != section['after_sha256'] for section in preservation['sections']),
              'stable_ids': preservation['stable_ids'], 'source_files_sha256': frozen,
              'index_sha256': digest(SOURCE / 'manuscript-index.json'), 'outputs': deliveries,
              'proof_receipts': {name: digest(HERE / name) for name in receipts},
              'finalizer_negative_controls': sample_controls,
              'publication_resource_proof_sha256': digest(ROOT / 'docs/publication/PDF-RESOURCE-CHECKS.json'),
              'visual_review': 'Record human/agent image inspection separately; automation does not establish visual quality.',
              'limits': 'Local source and digital rendering checks. No commit, deploy or public-release change. Does not recertify inherited claims or rights, dedicated-reader pagination, vendor acceptance or physical printing.'}
    target = HERE / 'deliverables.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    assert read(target) == report
    print(json.dumps({'version': version, 'outputs': deliveries}, indent=2))


if __name__ == '__main__':
    main()
