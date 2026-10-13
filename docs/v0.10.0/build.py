"""Build the final EPUB and 6 x 9 reading/print PDFs from the frozen source."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/lib/data/book'
META = json.loads((SOURCE / 'book.json').read_text())
VERSION = 'v' + META['version']
OUT = ROOT / 'book-build'
WORK = OUT / (VERSION + '-source')


def run(*args):
    subprocess.run(list(map(str, args)), cwd=ROOT, check=True)


def main():
    frozen = json.loads((ROOT / 'docs/publication/baseline.json').read_text())
    for name, digest in frozen.items():
        assert hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() == digest, name
    WORK.mkdir(parents=True, exist_ok=True)
    sections = []
    for index, section in enumerate(META['sections']):
        text = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/sts.py'), 'refs', 'render', section['file']],
            check=True, capture_output=True, text=True,
        ).stdout
        text = text.replace('](/book-images/', '](' + (ROOT / 'static/book-images').as_uri() + '/')
        text = re.sub(r'\[\^([^\]]+)\]', lambda m: f'[^{index}-{m[1]}]', text)
        text = re.sub(r'^(> \*.*\*)\n(?=> )', r'\1  \n', text, flags=re.MULTILINE)
        sections.append(text)
    manuscript = WORK / 'manuscript.md'
    manuscript.write_text('\n\n'.join(sections))
    metadata = {key: META[key] for key in ('title', 'subtitle', 'author')}
    metadata.update({'lang': 'en-US', 'date': META['lastUpdated'],
                     'identifier': f'urn:sts:edition:{VERSION}',
                     'rights': 'Copyright 2026 Christopher Tavolazzi. All rights reserved.',
                     'description': f'{META["subtitle"]}. Edition {VERSION}.'})
    (WORK / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    epub = OUT / f'Surviving-the-Singularity-{VERSION}.epub'
    run('pandoc', manuscript, '--metadata-file', WORK / 'metadata.json',
        '--toc', '--toc-depth=1', '--split-level=1',
        '--epub-cover-image', ROOT / 'scripts/book-cover.png',
        '--css', ROOT / 'scripts/epub.css', '-o', epub)
    run(sys.executable, ROOT / 'publication/build.py')
    run(sys.executable, ROOT / 'publication/production.py')
    run(sys.executable, ROOT / 'scripts/sts.py', 'compile', '--force', '--out',
        ROOT / 'manuscript' / f'Surviving-the-Singularity-{VERSION}.md')
    print('Built', VERSION, 'from', len(sections), 'canonical sections.', flush=True)


if __name__ == '__main__':
    main()
