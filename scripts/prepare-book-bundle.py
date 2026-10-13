#!/usr/bin/env python3
"""Prepare a versioned paid ZIP locally; do not change the live site manifest.

Run after npm run book:release. The result still requires editorial review,
storage upload, remote hash verification and coordinated deployment.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from pypdf import PdfReader

import build_bonus as builder
from sts_lib import bonus

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prove_bonus_text(stage):
    rendered = subprocess.run(['pandoc', str(stage / 'The-Precedent-File.md'), '-t', 'html5'],
                              capture_output=True, text=True, check=True).stdout
    document = BeautifulSoup(rendered, 'html.parser')
    normalize = lambda text: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', text).lower())
    blocks = [node.get_text('', strip=False) for node in document.select('p, li, th, td, h1, h2, h3, h4')]
    blocks = [block for block in blocks if len(normalize(block)) >= 15]
    # Plain PDF operator order preserves whole table cells; a spatial layout
    # extraction interleaves adjacent columns across wrapped lines.
    extracted = '\n'.join(page.extract_text() for page in PdfReader(stage / 'The-Precedent-File.pdf').pages)
    # Drop generated folios only; keep dates and numbers within source text.
    text = normalize(re.sub(r'^\s*\d+\s*$', '', extracted, flags=re.MULTILINE))
    missing = [block for block in blocks if normalize(block) not in text]
    if missing:
        raise RuntimeError(f'Bonus PDF omitted {len(missing)} source blocks: {missing[:3]}')
    probe = next(normalize(block) for block in blocks if len(normalize(block)) > 100)
    assert probe not in text.replace(probe, ''), 'Deleted paragraph control failed'
    return {'source_blocks_checked': len(blocks), 'missing_blocks': [], 'deleted_paragraph_control': True}


def prove_reader_instructions(stage):
    """Check the browser guide as delivered, including all archive-relative links."""
    source = (stage / 'START-HERE.html').read_text(encoding='utf8')
    page = BeautifulSoup(source, 'html.parser')
    assert page.html.get('lang') == 'en', 'Reading guide must declare its language'
    assert page.find('meta', attrs={'name': 'viewport'}), 'Missing phone viewport'
    assert page.main and len(page.find_all('h1')) == 1, 'Missing reading-guide structure'
    assert not page.find_all(['script', 'iframe', 'object', 'embed', 'form', 'link']), 'Reading guide has active or external assets'
    assert not re.search(r'@import|url\s*\(', str(page.style), re.I), 'Reading guide CSS requires another resource'
    for tag in page.find_all():
        assert not any(key.lower().startswith('on') for key in tag.attrs), 'Reading guide has an event handler'
        assert not tag.get('src'), 'Reading guide must be self-contained'
    local_links = []
    for link in page.find_all('a', href=True):
        url = urlsplit(link['href'])
        assert url.scheme in ('', 'https', 'mailto'), f'Unexpected reading-guide link scheme: {url.scheme}'
        if url.scheme:
            continue
        target = (stage / unquote(url.path)).resolve()
        assert target.is_relative_to(stage.resolve()) and target.is_file(), f'Broken or escaping archive link: {url.path}'
        local_links.append(url.path)
    for required in ['book/Surviving-the-Singularity.pdf', 'book/Surviving-the-Singularity.epub', 'The-Precedent-File.pdf']:
        assert required in local_links, f'Missing reading choice: {required}'
    assert '{{' not in page.get_text(), 'Unfilled reader instruction token'
    return {'local_file_links_checked': len(local_links), 'broken_links': [], 'self_contained_script_free': True}


def main():
    subprocess.run(['node', 'scripts/check-book-downloads.mjs'], cwd=ROOT, check=True)
    source = json.loads((ROOT / 'src/lib/data/book/book.json').read_text())
    assert source['version'] == source['released'], 'Publish the current corrected book first'
    site_manifest = ROOT / 'src/lib/data/bundleManifest.js'
    existing_site = digest(site_manifest)
    output = ROOT / 'book-build' / ('bundle-v' + source['version'])
    output.mkdir(parents=True, exist_ok=True)
    builder.DIST = output
    builder.STAGE = output / 'The-Precedent-File'
    builder.SITE_MANIFEST = output / 'bundleManifest.js'
    sys.argv = ['build_bonus.py']  # Never forward --upload to the shared builder.
    assert builder.main() == 0, 'Bundle build failed'
    text_proof = prove_bonus_text(builder.STAGE)
    reader_proof = prove_reader_instructions(builder.STAGE)
    manifest_path = output / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    name = 'research-bundle-book-v' + source['version'] + '.zip'
    (output / 'research-bundle-v1.zip').replace(output / name)
    manifest['bundle']['object'] = name
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    builder._write_site_manifest(manifest)
    # Reuse the independent archive/input verifier against the isolated files.
    bonus.SITE_MANIFEST_REL = str(builder.SITE_MANIFEST.relative_to(ROOT))
    bonus.DIST_MANIFEST_REL = str(manifest_path.relative_to(ROOT))
    bonus.ZIP_REL = str((output / name).relative_to(ROOT))
    findings, _ = bonus.verify_local(ROOT)
    assert not findings, findings
    assert digest(site_manifest) == existing_site, 'Live site manifest changed during preparation'
    record = {'status': 'prepared locally; not uploaded or activated', 'version': source['version'],
              'object': name, 'bytes': (output / name).stat().st_size, 'sha256': digest(output / name),
              'archive_and_inputs_verified': True, 'live_manifest_unchanged': True,
              'bonus_pdf_text_proof': text_proof,
              'reader_instructions_proof': reader_proof,
              'required_before_release': ['Review the inherited research cases; packaging proof is not independent historical fact-checking.',
                                          'Upload the versioned object and verify its downloaded bytes against this hash.',
                                          'Coordinate the site manifest and storage configuration with that verified object.']}
    (output / 'preparation.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
