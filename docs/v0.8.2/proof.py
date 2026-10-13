"""Structural and rendered proof checks; not a factual or literary certification."""
from pathlib import Path
import json
import re
import unicodedata
from html.parser import HTMLParser
from pypdf import PdfReader
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'book-build/v0.8.2-source'
PROOF = ROOT / 'book-build/v0.8.2-proof'
PROOF.mkdir(exist_ok=True)
SOURCE = ROOT / 'src/lib/data/book'
meta = json.loads((SOURCE / 'book.json').read_text())
reader = PdfReader(ROOT / 'book-build/Surviving-the-Singularity-v0.8.2.pdf')
pages = [p.extract_text() for p in reader.pages]
text = '\n'.join(pages)

def normalize(s):
    return re.sub(r'[^a-z0-9]+', '', unicodedata.normalize('NFKD', s).lower())

def missing_sections(contents):
    body = normalize(contents)
    return [s['id'] for s in meta['sections']
            if normalize((SOURCE / s['file']).read_text().splitlines()[0].lstrip('# ')) not in body]

assert missing_sections('deliberately empty manuscript'), 'Negative control failed'
missing = missing_sections('\n'.join(pages[3:]))  # Exclude cover, title, and contents.
assert not missing, missing
needles = ['What if it all goes right?', 'Doesn’t change your dinner', 'Dinner’s dinner',
           'beyond June', 'funded through June', 'Some could close', 'v0.8.2',
           'AlphaFold', 'numerical calibration']
for phrase in needles:
    assert normalize(phrase) in normalize(text), phrase
assert not re.search(r'\]\(sts:|\[\^[^\]]+\]', text), 'Unrendered markup'

class TextBlocks(HTMLParser):
    """Collect visible prose, headings, list items and cells from the built HTML."""
    def __init__(self):
        super().__init__()
        self.stack = []
        self.active = []
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag in {'img', 'br', 'hr', 'meta', 'link', 'input', 'wbr'}:
            return
        self.stack.append(tag)
        if tag in {'p', 'li', 'th', 'td', 'h1', 'h2', 'h3', 'h4'} and not any(
                t in self.stack for t in {'nav', 'figcaption', 'head', 'script', 'style'}):
            self.active.append([len(self.stack), []])

    def handle_data(self, data):
        for _, pieces in self.active:
            pieces.append(data)

    def handle_endtag(self, tag):
        if not self.stack or tag not in self.stack:
            return
        depth = len(self.stack) - self.stack[::-1].index(tag)
        remaining = []
        for d, pieces in self.active:
            if d >= depth:
                value = normalize(''.join(pieces))
                if len(value) > 20:
                    self.blocks.append(value)
            else:
                remaining.append([d, pieces])
        self.active = remaining
        self.stack = self.stack[:depth-1]

blocks = TextBlocks()
blocks.feed((WORK / 'book.html').read_text())
clean_text = re.sub(r'Surviving the Singularity\s*·\s*v0\.8\.2\s+\d+', '', text)
normalized_pdf = normalize(clean_text)
missing_blocks = [v[:140] for v in blocks.blocks if v not in normalized_pdf]
assert not missing_blocks, {'missing_text_blocks': missing_blocks}
probe = next(v for v in blocks.blocks if 'rosacheckedthecontainers' in v)
assert probe not in normalized_pdf.replace(probe, ''), 'Missing-paragraph negative control failed'

def outside(rect, width, height):
    x, y, w, h = rect
    return x < -1 or y < -1 or x+w > width+1 or y+h > height+1

assert outside((-5, 40, 30, 20), 816, 1056), 'Negative control failed'
assert not outside((60, 40, 30, 20), 816, 1056)
document = HTML(filename=str(WORK / 'book.html')).render()
assert len(document.pages) == len(pages)
overflow = []
for n, page in enumerate(document.pages, 1):
    for box in page._page_box.descendants():
        if type(box).__name__ != 'TextBox':
            continue
        rect = (box.position_x, box.position_y, box.width, box.height)
        if outside(rect, page.width, page.height):
            overflow.append({'page': n, 'text': box.text, 'rect': rect})
assert not overflow, overflow
images = re.findall(r'!\[[^\]]*\]\(/book-images/([^\)]+)\)',
                    '\n'.join((SOURCE / s['file']).read_text() for s in meta['sections']))
assert all((ROOT / 'static/book-images' / p).exists() for p in images)
samples = {phrase: next(i+1 for i,p in enumerate(pages) if normalize(phrase) in normalize(p))
           for phrase in needles}
result = {'pages': len(pages), 'sections_present': len(meta['sections']),
          'html_text_blocks_present_in_pdf': len(blocks.blocks),
          'source_images_present': len(images), 'text_outside_page': overflow,
          'negative_controls': ['missing-section detector', 'missing-paragraph detector', 'text-boundary detector'],
          'sample_pages': samples,
          'limits': 'Text and layout checks do not certify facts, quotation rights, or visual quality. Representative page images inspected separately.'}
(PROOF / 'checks.json').write_text(json.dumps(result, indent=2)+'\n')
(PROOF / 'extracted-text.txt').write_text(text)
print(json.dumps(result, indent=2))
