#!/usr/bin/env python3
"""Build and prove compact public downloads without changing master artwork.

Run before `npm run book:publish`. Requirements are in publication/README.md.
The full-size publication master and EPUB remain in their existing locations;
only the copies under book-build/downloads are optimized for web distribution.
"""
from pathlib import Path
from io import BytesIO
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unicodedata
import zipfile

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/lib/data/book'
BUILD = ROOT / 'book-build'
OUT = BUILD / 'downloads'
LIMIT = 25 * 1024 * 1024


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def publication_inputs(meta, print_variant):
    """Bind source artwork as well as prose; an art-only edit is a new build."""
    paths = {ROOT / 'scripts/book-cover.png', ROOT / 'scripts/epub.css',
             SOURCE / 'visuals.json', ROOT / 'publication/book.css'}
    paths.update(path for path in (ROOT / 'publication/assets').rglob('*') if path.is_file())
    for section in meta['sections']:
        for name in re.findall(r'\]\(/book-images/([^)\s]+)', (SOURCE / section['file']).read_text()):
            paths.add(ROOT / 'static/book-images' / name)
            if name.endswith('.svg'):
                paths.add(print_variant(name))
    return {str(path.relative_to(ROOT)): digest(path) for path in sorted(paths)}


def run(*args):
    subprocess.run(list(map(str, args)), cwd=ROOT, check=True)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def optimize_epub(source, target):
    """Recompress photographic rasters; preserve vector art and transparency."""
    with zipfile.ZipFile(source) as archive:
        assert archive.testzip() is None
        entries = archive.infolist()
        original = {entry.filename: archive.read(entry) for entry in entries}
    output = dict(original)
    renames, image_records = {}, []
    for name, data in original.items():
        if not name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        with Image.open(BytesIO(data)) as image:
            before = image.size
            # Small PNG diagrams stay lossless. Alpha remains alpha.
            alpha = image.mode in ('RGBA', 'LA') or 'transparency' in image.info
            photo = name.lower().endswith(('.jpg', '.jpeg')) or (not alpha and len(data) > 250_000)
            if not photo:
                continue
            image = image.convert('RGB')
            image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=85, optimize=True, progressive=False)
            if len(buffer.getvalue()) >= len(data):
                continue
            new_name = str(Path(name).with_suffix('.jpg'))
            assert new_name == name or new_name not in original, 'Image filename collision'
            output.pop(name)
            output[new_name] = buffer.getvalue()
            if new_name != name:
                renames[Path(name).name] = Path(new_name).name
            image_records.append({'input': name, 'output': new_name, 'input_pixels': before,
                                  'output_pixels': image.size, 'input_sha256': hashlib.sha256(data).hexdigest(),
                                  'output_sha256': hashlib.sha256(buffer.getvalue()).hexdigest()})
    for name, data in original.items():
        if not name.endswith(('.xhtml', '.html', '.opf', '.ncx', '.css', '.svg')):
            continue
        text = data.decode()
        for before, after in renames.items():
            # Pandoc gives embedded images unique basenames. The substitution
            # changes resource names only, never prose or alternative text.
            text = re.sub(r'(?<=[/"\'])' + re.escape(before) + r'(?=["\'\)])', after, text)
            if name.endswith('.opf'):
                text = re.sub(r'(<item\b[^>]*href="[^"]*/' + re.escape(after) + r'"[^>]*media-type=")image/png', r'\1image/jpeg', text)
        output[name] = text.encode()
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        # EPUB requires this exact, first, uncompressed entry.
        archive.writestr('mimetype', output.pop('mimetype'), compress_type=zipfile.ZIP_STORED)
        for name, data in output.items():
            archive.writestr(name, data)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        final = {name: archive.read(name) for name in archive.namelist()}
    return image_records, original, final, renames


def prove_epub(master_proof, original, final, images, renames):
    """Preserve every prose/navigation/vector byte, allowing resource renames."""
    transformed = {record['input'] for record in images}
    for name, before in original.items():
        if name in transformed:
            continue
        after = final[name]
        if name.endswith(('.xhtml', '.html', '.opf', '.ncx', '.css', '.svg')):
            # Reverse only the recorded resource-reference changes.
            text = after.decode()
            for old, new in renames.items():
                if name.endswith('.opf'):
                    text = re.sub(r'(<item\b[^>]*href="[^"]*/' + re.escape(new) + r'"[^>]*media-type=")image/jpeg', r'\1image/png', text)
                text = re.sub(r'(?<=[/"\'])' + re.escape(new) + r'(?=["\'\)])', old, text)
            after = text.encode()
        assert before == after, f'Non-raster content changed: {name}'
    assert not master_proof.check_resources(final), 'Broken optimized EPUB resource'
    for record in images:
        with Image.open(BytesIO(final[record['output']])) as image:
            assert image.format == 'JPEG'
            image.verify()


def compact_pdf(source, target):
    sys.path.insert(0, str(ROOT / 'publication'))
    from prune_pdf_resources import prepare
    from check_pdf_resources import annotations
    prepared = OUT / 'reading-prepared.pdf'
    preparation = prepare(source, prepared)
    run('gs', '-q', '-dBATCH', '-dNOPAUSE', '-dPDFSTOPONERROR', '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.7', '-dAutoRotatePages=/None', '-dEmbedAllFonts=true',
        '-dSubsetFonts=true', '-dDetectDuplicateImages=true', '-dCompressFonts=true',
        '-dDownsampleColorImages=true', '-dColorImageResolution=160',
        '-dColorImageDownsampleType=/Bicubic', '-dDownsampleGrayImages=true',
        '-dGrayImageResolution=160', '-dGrayImageDownsampleType=/Bicubic',
        '-dDownsampleMonoImages=false', '-dAutoFilterColorImages=false',
        '-dColorImageFilter=/DCTEncode', '-dJPEGQ=85', f'-sOutputFile={target}', prepared)
    before, after = PdfReader(source), PdfReader(target)
    assert len(before.pages) == len(after.pages), 'PDF page count changed'
    normalize = lambda text: re.sub(r'\s+', '', unicodedata.normalize('NFKC', text))
    text = []
    for path in (source, target):
        text.append(subprocess.run(['pdftotext', '-layout', str(path), '-'], check=True,
                                   capture_output=True, text=True).stdout.split('\f'))
    differences = [i + 1 for i, pair in enumerate(zip(*text)) if normalize(pair[0]) != normalize(pair[1])]
    assert len(text[0]) == len(text[1]) and not differences, f'PDF text changed on pages {differences}'
    for index, (left, right) in enumerate(zip(before.pages, after.pages), 1):
        assert list(left.mediabox) == list(right.mediabox), f'Page dimensions changed: {index}'
        # Link annotations must survive conversion, including internal TOC links.
        links = lambda page: [item.get_object() for item in page.get('/Annots', [])
                              if item.get_object().get('/Subtype') == '/Link']
        a, b = links(left), links(right)
        assert len(a) == len(b), f'PDF link count changed: {index}'
        def uris(annotations):
            result = []
            for annotation in annotations:
                action = annotation.get('/A', {})
                if hasattr(action, 'get_object'):
                    action = action.get_object()
                if action.get('/S') == '/URI':
                    result.append(str(action.get('/URI')))
            return sorted(result)
        assert uris(a) == uris(b), f'PDF external link changed: {index}'
    original_links, compact_links = annotations(before), annotations(after)
    assert not original_links['unresolved'] and not compact_links['unresolved'], 'Unresolved PDF link target'
    assert original_links['targets'] == compact_links['targets'], 'PDF internal/external destinations changed'
    return {'pages': len(after.pages), 'page_text_unchanged': True, 'link_counts_and_external_uris_preserved': True,
            'internal_destinations_resolve': True, 'link_targets_unchanged': True,
            'resource_preparation': preparation}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--existing-masters', action='store_true', help='Reprove existing masters before optimizing them')
    args = parser.parse_args()
    meta = json.loads((SOURCE / 'book.json').read_text())
    version = meta['version']
    baseline = json.loads((ROOT / 'docs/publication/baseline.json').read_text())
    hashes = {name: digest(SOURCE / name) for name in ['book.json', *(s['file'] for s in meta['sections'])]}
    assert hashes == baseline, 'Review source changes before updating the publication freeze'
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.existing_masters:
        run(sys.executable, ROOT / 'docs' / f'v{version}' / 'build.py')
    build = json.loads((ROOT / 'publication/output/build.json').read_text())
    assert build['source_sha256'] == hashes, 'Publication master is stale'
    run(sys.executable, ROOT / 'publication/proof.py')
    proof = module(ROOT / 'docs/v0.10.4/check_epub.py', 'epub_proof')
    proof.HERE = OUT
    proof.main()  # Fresh source, all blocks, images, metadata, spine and controls.
    epub_source = BUILD / f'Surviving-the-Singularity-v{version}.epub'
    pdf_source = ROOT / 'publication/output/Surviving-the-Singularity-reading.pdf'
    assert digest(pdf_source) == build['outputs']['reading']['sha256'], 'Reading master hash differs from build'
    epub_target, pdf_target = (OUT / f'Surviving-the-Singularity-v{version}.{ext}' for ext in ('epub', 'pdf'))
    images, original, final, renames = optimize_epub(epub_source, epub_target)
    prove_epub(proof, original, final, images, renames)
    pdf_proof = compact_pdf(pdf_source, pdf_target)
    artifacts = {}
    for ext, path in [('pdf', pdf_target), ('epub', epub_target)]:
        assert path.stat().st_size < LIMIT, f'{path.name} exceeds Pages 25 MiB limit'
        artifacts[ext] = {'name': path.name, 'bytes': path.stat().st_size, 'sha256': digest(path)}
    # `released` is distribution state, not manuscript content. Publishing stamps
    # it after this build, so bind the manifest's other exact bytes independently.
    hashes['book.json'] = hashlib.sha256(re.sub(r'"released":\s*"[^"]*"', '"released": "<release>"',
                                              (SOURCE / 'book.json').read_text()).encode()).hexdigest()
    receipt = {'schema': 1, 'version': version, 'source_manifest_release_independent': True,
               'source_sha256': hashes, 'input_sha256': publication_inputs(meta, proof.print_variant),
               'artifacts': artifacts,
               'masters': {'pdf': digest(pdf_source), 'epub': digest(epub_source)},
               'pdf_proof': pdf_proof, 'epub_images': images, 'epub_other_content_unchanged': True,
               'epub_source_proof': json.loads((OUT / 'epub-checks.json').read_text()),
               'limits': 'Digital distribution copies. No print proof or physical e-reader certification. Does not update private storage bundles.'}
    (OUT / 'book-downloads.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'version': version, 'artifacts': artifacts}, indent=2))


if __name__ == '__main__':
    main()
