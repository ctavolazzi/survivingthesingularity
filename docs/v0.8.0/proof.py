"""Structural and rendered proof checks; not a factual or literary certification."""
from pathlib import Path
import json
import re
import unicodedata
from pypdf import PdfReader
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'book-build/v0.8.0-source'
PROOF = ROOT / 'book-build/v0.8.0-proof'
PROOF.mkdir(exist_ok=True)
SOURCE = ROOT / 'src/lib/data/book'
meta = json.loads((SOURCE / 'book.json').read_text())
reader = PdfReader(ROOT / 'book-build/Surviving-the-Singularity-v0.8.0.pdf')
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
needles = ['grow our fucking food first', 'The line cook still eats',
           'Free to the person who needs it', 'The record that keeps the promise honest',
           'How the small thing becomes a larger promise', 'numerical calibration',
           'v0.8.0', 'Thanksgiving 2027']
for phrase in needles:
    assert normalize(phrase) in normalize(text), phrase
assert not re.search(r'\]\(sts:|\[\^[^\]]+\]', text), 'Unrendered markup'

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
          'source_images_present': len(images), 'text_outside_page': overflow,
          'negative_controls': ['missing-section detector', 'text-boundary detector'],
          'sample_pages': samples,
          'limits': 'Text and layout checks do not certify facts, quotation rights, or visual quality. Representative page images inspected separately.'}
(PROOF / 'checks.json').write_text(json.dumps(result, indent=2)+'\n')
(PROOF / 'extracted-text.txt').write_text(text)
print(json.dumps(result, indent=2))
