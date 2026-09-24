"""Publication preflight: preservation, rendered text, geometry and PDF resources.

Run after build.py. These checks do not replace inspection of rendered pages.
"""
from pathlib import Path
import hashlib
import json
import re
import unicodedata
from bs4 import BeautifulSoup
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE/'output'
PROOF = OUT/'proof'
PROOF.mkdir(exist_ok=True)

def normalize(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD',s).lower())

def cleaned_page(s):
    lines = s.splitlines()
    if lines and re.fullmatch(r'\d+|[ivx]+',lines[-1].strip()):
        lines=lines[:-1]
    # pypdf emits outside list markers at the end of the page's content
    # stream. These are generated counters, not manuscript paragraph text.
    return '\n'.join(line for line in lines if not re.fullmatch(r'(?:SURVIVING THE SINGULARITY|INTRODUCTION|PREFACE|CHAPTER \d+|CONCLUSION|APPENDIX [A-E]|ILLUSTRATION CREDITS|[1-9][0-9]?\.)',line.strip()))

def outside(rect,w,h):
    x,y,bw,bh=rect
    return x < -0.5 or y < -0.5 or x+bw > w+0.5 or y+bh > h+0.5

def split_present(b, normalized, window=6000, pieces=4):
    """True when every character of b appears in order, in at most `pieces`
    runs of 12+ characters within `window` characters. A figure placed across a
    page break makes pypdf emit its SVG labels mid-paragraph; the paragraph is
    intact but interrupted. Text cut from the middle still fails: every
    character has to be matched."""
    pos, start = 0, None
    while b:
        lo, hi, best = 0, len(b), -1
        end = None if start is None else pos + window
        while lo < hi:
            mid = (lo + hi + 1) // 2
            j = normalized.find(b[:mid], pos, end)
            if j >= 0: lo, best = mid, j
            else: hi = mid - 1
        if lo < min(12, len(b)): return False
        if start is None: start = best
        pos, b, pieces = best + lo, b[lo:], pieces - 1
        if pieces < 0: return False
    return True

def missing_blocks(blocks, normalized):
    return [b for b in blocks if normalize(b) not in normalized and not split_present(normalize(b), normalized)]

baseline=json.loads((ROOT/'docs/publication/baseline.json').read_text())
source=ROOT/'src/lib/data/book'
unchanged={name:hashlib.sha256((source/name).read_bytes()).hexdigest()==digest for name,digest in baseline.items()}
assert all(unchanged.values()), unchanged
reader=PdfReader(OUT/'Surviving-the-Singularity-interior.pdf')
pages=[p.extract_text() for p in reader.pages]
text='\n'.join(cleaned_page(p) for p in pages)
normalized=normalize(text)
reference=BeautifulSoup((OUT/'source-rendered.html').read_text(),'html.parser')
blocks=[]
exceptions=[]
transformations=json.loads((OUT/'build.json').read_text())['image_transformations']
omitted={normalize(t['omitted_caption']) for t in transformations if t.get('omitted_caption')}
omitted.update(normalize(t['original_caption']) for t in transformations if t.get('original_caption'))
for figure in reference.find_all('figure'):
    cap=figure.find('figcaption')
    if cap: cap.decompose() # Alt descriptions were not visible in the baseline.
for node in reference.select('p, li, th, td, h2, h3, h4'):
    value=node.get_text('',strip=False)
    if len(normalize(value))<15: continue
    if normalize(value) in omitted:
        exceptions.append(value)
        continue
    blocks.append(value)
blocks.extend(t['replacement_caption'] for t in transformations if t.get('replacement_caption'))
missing=missing_blocks(blocks,normalized)
layout=json.loads((OUT/'interior-layout.json').read_text())
overflow=[]
for p in layout:
    for b in p['boxes']:
        if outside(b['rect'],p['width'],p['height']):
            overflow.append({'page':p['page'],**b})
fonts={}
for page in reader.pages:
    for ref in page['/Resources'].get('/Font',{}).get_object().values():
        font=ref.get_object(); name=str(font.get('/BaseFont'))
        descendants=font.get('/DescendantFonts')
        if descendants: font=descendants[0].get_object()
        desc=font.get('/FontDescriptor',{}).get_object()
        fonts[name]=any(key in desc for key in ('/FontFile','/FontFile2','/FontFile3'))
html_doc=BeautifulSoup((OUT/'interior.html').read_text(),'html.parser')
ids={n['id'] for n in html_doc.select('[id]')}
broken_links=[a['href'] for a in html_doc.select('a[href^="#"]') if a['href'][1:] not in ids]
missing_assets=[img['src'] for img in html_doc.select('img[src]') if img['src'].startswith('file:') and not Path(img['src'].removeprefix('file://')).exists()]
sizes={tuple(round(float(x),3) for x in page.mediabox[2:]) for page in reader.pages}
source_sections=json.loads((source/'book.json').read_text())['sections']
sections_present=[s['id'] for s in source_sections if html_doc.find(id='sec-'+s['id'])]
assert missing_blocks(['This intentionally absent publication proof sentence.'],normalized)
probe=next(b for b in blocks if 'rosacheckedthecontainers' in normalize(b))
assert missing_blocks([probe],normalized.replace(normalize(probe),''))
cut=normalize(probe); assert missing_blocks([probe],normalized.replace(cut,cut[:len(cut)//3]+cut[2*len(cut)//3:]))
assert outside((-5,40,30,20),576,864)
assert '#intentionally-missing' not in ids
report={
    'pages':len(pages),'page_size_points':[list(s) for s in sizes],
    'source_sections_unchanged':sum(unchanged.values()),
    'sections_present':len(sections_present),'source_text_blocks_checked':len(blocks),
    'missing_text_blocks':missing,'documented_caption_exceptions':exceptions,
    'text_outside_page':overflow,'fonts_embedded':fonts,'broken_internal_links':broken_links,
    'missing_assets':missing_assets,'negative_controls':['absent text','removed known paragraph','middle third cut from a paragraph','outside-page rectangle','absent destination'],
    'limits':'Does not establish legal clearance, vendor acceptance, factual accuracy or visual quality. Contact sheets and full-size samples are reviewed separately.'
}
(PROOF/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
(PROOF/'extracted-text.txt').write_text('\n\n'.join(pages))
print(json.dumps({k:(v[:4] if k=='missing_text_blocks' else v) for k,v in report.items()},indent=2))
assert not missing, f'{len(missing)} source text blocks not recovered from PDF'
assert not overflow, overflow
assert not broken_links, broken_links
assert not missing_assets, missing_assets
assert all(fonts.values()), fonts
assert sizes=={(432.0,648.0)}, sizes
assert len(sections_present)==len(source_sections), (len(sections_present), len(source_sections))
assert 'The Uncompromising Truth' in pages[4], 'Front matter must occupy exactly four pages before numbering restarts'
