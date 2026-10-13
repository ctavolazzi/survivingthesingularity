"""Build the author-review PDF from the manifest, retaining all intermediates."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from print_figures import print_variant  # noqa: E402
SOURCE = ROOT / 'src/lib/data/book'
META = json.loads((SOURCE / 'book.json').read_text())
OUT = ROOT / 'book-build'
WORK = OUT / 'v0.9.2-source'
WORK.mkdir(parents=True, exist_ok=True)
sections = []
for i, section in enumerate(META['sections']):
    result = subprocess.run(
        ['python3', str(ROOT / 'scripts/sts.py'), 'refs', 'render', section['file']],
        check=True, capture_output=True, text=True,
    )
    # Diagrams print from their light-palette copies; photos and plates are unchanged.
    text = re.sub(r'\]\(/book-images/([^)\s]+\.svg)', lambda m: '](' + print_variant(m[1]).as_uri(), result.stdout)
    text = text.replace('](/book-images/', '](' + (ROOT / 'static/book-images').as_uri() + '/')
    text = re.sub(r'^(> \*.*\*)\n(?=> )', r'\1  \n', text, flags=re.MULTILINE)
    text = re.sub(r'\[\^([^\]]+)\]', lambda m: f'[^{i}-{m[1]}]', text)
    sections.append(text)
manuscript = WORK / 'manuscript.md'
manuscript.write_text('\n\n'.join(sections))
metadata = {k: META[k] for k in ('title', 'subtitle', 'author')}
metadata.update({'lang': 'en-US', 'date': 'v0.9.2 | What if it all goes right? | September 24, 2026',
                 'rights': 'Copyright 2026 Christopher Tavolazzi. All rights reserved.'})
(WORK / 'metadata.json').write_text(json.dumps(metadata, indent=2))
css = (ROOT / 'scripts/book-print.css').read_text().replace('BOOK_VERSION', 'v0.9.2')
css = css.replace('height: 100vh;', 'height: 279.4mm;')
# Diagrams name JetBrains Mono first; supply it rather than fall back to Menlo.
FONTS = (ROOT / 'publication/assets/fonts').as_uri()
css = ''.join(f"@font-face {{ font-family: 'JetBrains Mono'; src: url('{FONTS}/JetBrainsMono-{face}.ttf');{weight} }}\n"
              for face, weight in (('Regular', ''), ('SemiBold', ' font-weight: 600;'), ('Bold', ' font-weight: 700;'))) + css
css += '''
/* Edition-specific proof improvements. */
body { margin: 0; }
#cover-page { margin: 0; width: 100%; height: 279.4mm; }
#cover-page img { width: 215.9mm; height: 279.4mm; }
header#title-block-header { page-break-after: always; padding-top: 3cm; }
header .date { margin-top: 2cm; color: #92400e; }
nav#TOC { font-family: Helvetica, Arial, sans-serif; font-size: 10pt; }
nav#TOC ul { list-style: none; padding-left: 0; }
nav#TOC li { margin-bottom: 0.25em; }
nav#TOC a::after { content: leader('.') target-counter(attr(href), page); }
h1, h2, h3 { break-after: avoid; }
p { orphans: 3; widows: 3; }
a { color: #3c5572; overflow-wrap: anywhere; }
table { table-layout: fixed; }
td, th { overflow-wrap: anywhere; }
figure img { max-height: 12cm; }
figure img[src$='.svg'] { max-height: 19cm; }
figcaption { display: none; }
tr { break-inside: avoid; }
'''
(WORK / 'book-print.css').write_text(css)
cover = '<div id="cover-page"><img src="' + (ROOT / 'scripts/book-cover.png').as_uri() + '" alt="Surviving the Singularity cover" /></div>'
(WORK / 'cover.html').write_text(cover)
html = WORK / 'book.html'
subprocess.run(['pandoc', str(manuscript), '--standalone', '--toc', '--toc-depth=1',
                '--metadata-file', str(WORK / 'metadata.json'),
                '--include-before-body', str(WORK / 'cover.html'),
                '--css', str(WORK / 'book-print.css'), '-o', str(html)], check=True)
pdf = OUT / 'Surviving-the-Singularity-v0.9.2.pdf'
subprocess.run(['weasyprint', str(html), str(pdf)], check=True)
record = {'version': META['version'], 'sections': len(sections),
          'source_sha256': {s['file']: hashlib.sha256((SOURCE / s['file']).read_bytes()).hexdigest() for s in META['sections']},
          'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(), 'pdf_bytes': pdf.stat().st_size}
(WORK / 'build.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'pdf': str(pdf), 'bytes': pdf.stat().st_size, 'sections': len(sections)}, indent=2))
