"""Validate the shipped EPUB against freshly rendered, frozen canonical source.

The negative controls mutate in-memory copies, never the source or EPUB.
This is a scoped structural/content check, not EPUBCheck certification.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import posixpath
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/lib/data/book'
META = json.loads((SOURCE / 'book.json').read_text())
EPUB = ROOT / 'book-build' / f'Surviving-the-Singularity-v{META["version"]}.epub'
sys.path.insert(0, str(ROOT / 'docs/v0.9.2'))
from print_figures import print_variant


def sha(data):
    return hashlib.sha256(data).hexdigest()


def norm(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text)).replace('\u00ad', '')


def resolve(name, ref):
    url = urlsplit(ref)
    return posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path))) if url.path else name


def check_resources(files):
    errors = []
    parsed = {name: BeautifulSoup(data, 'xml') for name, data in files.items()
              if name.endswith(('.xhtml', '.html', '.opf', '.ncx', '.svg'))}
    for name, doc in parsed.items():
        for node in doc.select('[href], [src], [xlink\\:href]'):
            for attribute in ('href', 'src', 'xlink:href'):
                ref = node.get(attribute)
                if not ref:
                    continue
                url = urlsplit(ref)
                if url.scheme or url.netloc:
                    continue
                target = resolve(name, ref)
                if target not in files:
                    errors.append(f'{name}: missing {ref}')
                elif url.fragment and target in parsed and not parsed[target].find(id=unquote(url.fragment)):
                    errors.append(f'{name}: missing anchor {ref}')
    for name, data in files.items():
        if name.endswith('.css'):
            for ref in re.findall(r'url\([\s\'"]*([^\)\'"\s]+)', data.decode()):
                if not urlsplit(ref).scheme and resolve(name, ref) not in files:
                    errors.append(f'{name}: missing CSS resource {ref}')
    return errors


def missing_blocks(blocks, text):
    normalized = norm(text)
    return [block for block in blocks if norm(block) not in normalized]


def rendered_source():
    """Render independently from source rather than trust a stale build diagnostic."""
    sections = []
    for index, section in enumerate(META['sections']):
        rendered = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/sts.py'), 'refs', 'render', section['file']],
            capture_output=True, text=True, check=True,
        ).stdout
        rendered = re.sub(r'^(> \*.*\*)\n(?=> )', r'\1  \n', rendered, flags=re.M)
        rendered = re.sub(r'\[\^([^\]]+)\]', lambda m: f'[^{index}-{m[1]}]', rendered)
        raw = subprocess.run(['pandoc', '--from=markdown', '--to=html5'],
                             input=rendered, capture_output=True, text=True, check=True).stdout
        doc = BeautifulSoup(raw, 'html.parser')
        # Pandoc's generated alt-text captions are not narrative prose.
        for caption in doc.select('figure figcaption'):
            caption.decompose()
        blocks = [node.get_text('', strip=False) for node in doc.select('p, li, th, td, h1, h2, h3, h4')]
        sections.append({'file': section['file'], 'heading': doc.h1.get_text(),
                         'blocks': [block for block in blocks if len(norm(block)) >= 15]})
    return sections


def source_artwork(visuals):
    """Keep every canonical placement, including deliberately uncaptioned dividers."""
    expected = []
    for section in META['sections']:
        text = (SOURCE / section['file']).read_text()
        assets = []
        placements = list(re.finditer(r'!\[[^\]]*\]\(/book-images/([^)\s]+)\)', text))
        references = re.findall(r'\]\(/book-images/([^)\s]+)\)', text)
        assert [match[1] for match in placements] == references, (
            'Canonical artwork reference was not parsed as an image', section['file'],
        )
        for match in placements:
            name = match[1]
            following = text[match.end():].lstrip('\n').split('\n\n', 1)[0].strip()
            manual_caption = bool(re.fullmatch(r'\*[^\n]+\*', following))
            registered = name in visuals
            # Source part dividers intentionally have no manual caption. Do not
            # turn their alternative text into a required invented caption.
            divider = re.fullmatch(r'part[123]-divider\.md', section['file']) is not None
            assert not registered or manual_caption or divider, (
                'Registered artwork lacks a source caption outside a part divider',
                section['file'], name,
            )
            path = print_variant(name) if name.endswith('.svg') else ROOT / 'static/book-images' / name
            assets.append({'file': name, 'section': section['file'], 'sha256': sha(path.read_bytes()),
                           'registered': registered, 'caption_required': manual_caption})
        expected.append(assets)
    referenced = {asset['file'] for assets in expected for asset in assets}
    assert set(visuals) <= referenced, ('Unreferenced registry artwork', sorted(set(visuals) - referenced))
    return expected


def check_art(files, chapters, expected):
    errors = []
    records = []
    for chapter, assets in zip(chapters, expected):
        doc = BeautifulSoup(files[chapter], 'xml')
        images = doc.find_all('img')
        actual = Counter(sha(files[resolve(chapter, image['src'])]) for image in images
                         if resolve(chapter, image['src']) in files)
        wanted = Counter(asset['sha256'] for asset in assets)
        if actual != wanted:
            errors.append(f'{chapter}: displayed artwork differs from canonical section')
        for image in images:
            if not image.get('alt', '').strip():
                errors.append(f'{chapter}: missing image alternative text')
        for asset in assets:
            matching = [image for image in images if resolve(chapter, image['src']) in files
                        and sha(files[resolve(chapter, image['src'])]) == asset['sha256']]
            if asset['registered']:
                for image in matching:
                    figure = image.find_parent('figure')
                    classes = figure.get('class', []) if figure else []
                    classes = classes.split() if isinstance(classes, str) else classes
                    if not figure or 'book-figure' not in classes:
                        errors.append(f'{chapter}: missing registered figure for {asset["file"]}')
                    caption = figure.find('figcaption') if figure else None
                    if asset['caption_required'] and (not caption or not caption.get_text(strip=True)):
                        errors.append(f'{chapter}: missing source-required caption for {asset["file"]}')
            records.append({**asset, 'chapter': chapter,
                            'embedded': [resolve(chapter, image['src']) for image in matching]})
    return errors, records


def main():
    frozen = json.loads((ROOT / 'docs/publication/baseline.json').read_text())
    expected_source = {'book.json', *(section['file'] for section in META['sections'])}
    assert set(frozen) == expected_source, 'Frozen baseline does not cover manifest and all sections'
    source_hashes = {name: sha((SOURCE / name).read_bytes()) for name in frozen}
    assert source_hashes == frozen, 'Canonical source changed after publication freeze'
    with zipfile.ZipFile(EPUB) as archive:
        assert archive.testzip() is None, 'ZIP CRC failure'
        entries = archive.infolist()
        assert len({entry.filename for entry in entries}) == len(entries), 'Duplicate ZIP member'
        assert entries[0].filename == 'mimetype' and entries[0].compress_type == zipfile.ZIP_STORED
        files = {name: archive.read(name) for name in archive.namelist()}
    assert files['mimetype'] == b'application/epub+zip'
    xml_count = 0
    for name, data in files.items():
        if name.endswith(('.xml', '.xhtml', '.opf', '.ncx', '.svg')):
            ET.fromstring(data)
            xml_count += 1
    container = BeautifulSoup(files['META-INF/container.xml'], 'xml')
    opf = container.find('rootfile')['full-path']
    package = BeautifulSoup(files[opf], 'xml')
    assert package.find('dc:identifier').get_text() == f'urn:sts:edition:v{META["version"]}'
    assert package.find('dc:title').get_text() == META['title']
    assert package.find('dc:creator').get_text() == META['author']
    assert package.find('dc:language').get_text() == 'en-US'
    manifest = {item['id']: resolve(opf, item['href']) for item in package.find_all('item')}
    assert len(manifest) == len(package.find_all('item')), 'Duplicate manifest id'
    assert all(path in files for path in manifest.values()), 'Manifest resource absent'
    spine = [manifest[item['idref']] for item in package.find_all('itemref')]
    nav_item = next(item for item in package.find_all('item') if 'nav' in item.get('properties', '').split())
    nav_path = manifest[nav_item['id']]
    nav = BeautifulSoup(files[nav_path], 'xml').find('nav', {'epub:type': 'toc'})
    links = nav.find_all('a')
    chapters = [resolve(nav_path, link['href']) for link in links]
    assert len(chapters) == len(set(chapters)) == len(META['sections']), 'TOC must link every section once'
    assert chapters == [path for path in spine if path in chapters], 'TOC order differs from spine'
    assert set(spine) - set(chapters) == {nav_path, manifest['cover_xhtml'], manifest['title_page_xhtml']}
    assert not any(name.endswith(('.js', '.mjs')) for name in files), 'JavaScript packaged in static EPUB'
    for name, data in files.items():
        if name.endswith(('.xhtml', '.svg')):
            document = BeautifulSoup(data, 'xml')
            assert not document.find('script'), ('Script in EPUB', name)
            assert not re.search(r'<!--\s*(?:book-scene|interactive:)|\[\[interactive:|data-scene-marker', data.decode()), ('Scene marker leaked', name)
    reference = rendered_source()
    missing = []
    for section, chapter in zip(reference, chapters):
        document = BeautifulSoup(files[chapter], 'xml')
        assert norm(document.h1.get_text()) == norm(section['heading']), ('Section order/heading changed', section['file'])
        missing.extend({'section': section['file'], 'text': block}
                       for block in missing_blocks(section['blocks'], document.get_text()))
    registry_bytes = (SOURCE / 'visuals.json').read_bytes()
    visuals = json.loads(registry_bytes)['images']
    expected = source_artwork(visuals)
    art_errors, art_records = check_art(files, chapters, expected)
    errors = check_resources(files)
    css = '\n'.join(data.decode() for name, data in files.items() if name.endswith('.css'))
    assert 'figure.book-figure { float: none' in css, 'Missing EPUB stacked-art rule'

    # Break observed content, then run the same checks used for the real EPUB.
    image_chapter = next(chapter for chapter in chapters if BeautifulSoup(files[chapter], 'xml').find('img'))
    image_doc = BeautifulSoup(files[image_chapter], 'xml')
    target = resolve(image_chapter, image_doc.img['src'])
    mutant = {name: data for name, data in files.items() if name != target}
    assert check_resources(mutant), 'Deleted embedded image control stayed green'
    image_doc.img.decompose()
    mutant = {**files, image_chapter: str(image_doc).encode()}
    assert check_art(mutant, chapters, expected)[0], 'Unreferenced artwork control stayed green'
    caption_record = next(record for record in art_records if record['registered'] and record['caption_required'])
    caption_doc = BeautifulSoup(files[caption_record['chapter']], 'xml')
    caption_image = next(image for image in caption_doc.find_all('img')
                         if resolve(caption_record['chapter'], image['src']) in caption_record['embedded'])
    caption_image.find_parent('figure').find('figcaption').decompose()
    mutant = {**files, caption_record['chapter']: str(caption_doc).encode()}
    assert any('missing source-required caption' in error for error in check_art(mutant, chapters, expected)[0]), 'Deleted required caption control stayed green'
    chapter_doc = BeautifulSoup(files[chapters[0]], 'xml')
    baseline_missing = missing_blocks(reference[0]['blocks'], chapter_doc.get_text())
    paragraph = next(node for node in chapter_doc.find_all('p') if len(norm(node.get_text())) > 100)
    paragraph.decompose()
    assert len(missing_blocks(reference[0]['blocks'], chapter_doc.get_text())) > len(baseline_missing), 'Deleted paragraph control stayed green'
    mutant = {**files, 'EPUB/styles/probe.css': b'body { background: url(missing-image.png); }'}
    assert check_resources(mutant), 'Missing CSS resource control stayed green'
    mutant = {**files, 'EPUB/text/probe.xhtml': b'<html xmlns="http://www.w3.org/1999/xhtml"><body><a href="ch001.xhtml#missing-anchor">Probe</a></body></html>'}
    assert check_resources(mutant), 'Broken anchor control stayed green'
    report = {
        'version': META['version'], 'spine_documents': len(spine), 'source_sections': len(reference),
        'epub_sha256': sha(EPUB.read_bytes()), 'epub_bytes': EPUB.stat().st_size,
        'source_sha256': source_hashes, 'source_hashes_verified': True,
        'registry_sha256': sha(registry_bytes), 'registry_entries': len(visuals),
        'source_reference': 'Fresh Pandoc render of canonical sections with resolved cross-references',
        'source_blocks_checked': sum(len(section['blocks']) for section in reference),
        'missing_blocks': missing, 'resource_errors': errors, 'art_errors': art_errors,
        'source_art_assets_checked': len(art_records),
        'distinct_source_art_assets_checked': len({asset['file'] for asset in art_records}),
        'registered_art_assets_checked': sum(asset['registered'] for asset in art_records),
        'registered_art_figures': sum(asset['registered'] for asset in art_records),
        'registered_captioned_figures': sum(asset['registered'] and asset['caption_required'] for asset in art_records),
        'registered_uncaptioned_figures': sum(asset['registered'] and not asset['caption_required'] for asset in art_records),
        'artwork': art_records, 'art_stacking_css': True, 'scene_markers_absent': True,
        'static_no_javascript': True, 'metadata_checked': True,
        'navigation_sections_checked': len(chapters), 'xml_documents_checked': xml_count,
        'zip_integrity': True, 'uncompressed_first_mimetype': True,
        'negative_controls': ['deleted embedded image', 'deleted displayed image with bytes retained',
                              'deleted required caption', 'deleted real paragraph',
                              'missing CSS resource', 'broken internal anchor'],
        'limits': 'Structural and text proof; not EPUBCheck certification or a physical-device test.',
    }
    (HERE / 'epub-checks.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('source_sha256', 'artwork')}, indent=2))
    assert not errors, errors
    assert not art_errors, art_errors
    assert not missing, f'{len(missing)} missing EPUB source blocks'


if __name__ == '__main__':
    main()
