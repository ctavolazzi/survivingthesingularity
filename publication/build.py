"""Reproducible publication layout of unchanged v0.8.2 manuscript.

Run from any directory: python3 publication/build.py
The source manuscript and previous editions are never overwritten.
"""
from pathlib import Path
import hashlib
import html
import json
import re
import subprocess
import sys
from bs4 import BeautifulSoup
from weasyprint import HTML
from pypdf import PdfReader, PdfWriter
from pypdf.constants import PageLabelStyle
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / 'src/lib/data/book'
OUT = HERE / 'output'
OUT.mkdir(parents=True, exist_ok=True)
META = json.loads((SOURCE / 'book.json').read_text())
BASELINE = json.loads((ROOT / 'docs/publication/baseline.json').read_text())
RIGHTS = json.loads((ROOT/'docs/publication/asset-rights.json').read_text())
assert RIGHTS['status'] == 'complete_with_documented_limits', 'Complete the image-rights audit before publication build'
RIGHTS_BY_FILE = {a['file']:a for a in RIGHTS['assets']}
for filename, expected in BASELINE.items():
    assert hashlib.sha256((SOURCE / filename).read_bytes()).hexdigest() == expected, filename

MOTIFS = {
    'part-1': 'event-horizon', 'part-2': 'shared-table', 'part-3': 'grain-and-gripper',
    'chapter0': 'open-gate', 'chapter5': 'centrifugal-governor',
    'chapter7': 'shared-table', 'chapter9': 'water-pump',
    'chapter10': 'pamphlet-and-thread', 'chapter12': 'seed-and-root',
    'chapter13': 'roof-and-joint', 'chapter15': 'soil-profile',
    'chapter16': 'pamphlet-and-thread', 'chapter17': 'repair-tools',
    'chapter18': 'continuity-route', 'conclusion': 'grain-and-gripper',
}
RIGHTS_REPLACEMENTS = {
    'ch06-edmond-de-belamy.png': 'repair-tools',
    'ch10-nyse.jpg': 'pamphlet-and-thread',
    'ch12-farmbot.jpg': 'seed-and-root',
    'ch12-farmbot-watering.jpg': 'soil-profile',
}

def motif(name):
    matches = list((HERE / 'assets/motifs').glob('*-' + name + '.svg'))
    if not matches:
        return ''
    path = matches[0]
    return f'<figure class="motif" aria-hidden="true"><img src="{path.as_uri()}" alt="" /></figure>'

def make(tag, attrs=None, text=None):
    soup = BeautifulSoup('', 'html.parser')
    node = soup.new_tag(tag, attrs=attrs or {})
    if text is not None:
        node.string = text
    return node

def diagram(title, items, note):
    cells = [f'<div class="diagram-item"><span class="diagram-number">{i+1:02}</span><b>{html.escape(a)}</b><br/>{html.escape(b)}</div>' for i, (a,b) in enumerate(items)]
    rows = ''.join('<div class="diagram-row">'+''.join(cells[i:i+2])+'</div>' for i in range(0,len(cells),2))
    return BeautifulSoup(f'<aside class="diagram"><div class="eyebrow">{title}</div>{rows}<p class="diagram-note">{note}</p></aside>', 'html.parser')

sections = []
transformations = []
included_images = []
visible_baseline = []
for index, section in enumerate(META['sections']):
    sid = section['id']
    rendered = subprocess.run([sys.executable, str(ROOT/'scripts/sts.py'), 'refs','render', section['file']], capture_output=True, text=True, check=True).stdout
    rendered = rendered.replace('](/book-images/', '](' + (ROOT/'static/book-images').as_uri() + '/')
    rendered = re.sub(r'^(> \*.*\*)\n(?=> )', r'\1  \n', rendered, flags=re.M)
    rendered = re.sub(r'\[\^([^\]]+)\]', lambda m: f'[^{index}-{m[1]}]', rendered)
    raw = subprocess.run(['pandoc','--from=markdown','--to=html5'], input=rendered, text=True, capture_output=True, check=True).stdout
    visible_baseline.append(f'<section data-source="{section["file"]}">{raw}</section>')
    soup = BeautifulSoup(raw, 'html.parser')
    original_h1 = soup.find('h1')
    full_title = original_h1.get_text(' ', strip=True)
    label, _, title = full_title.partition(':')
    title = title.strip() or full_title
    # Case is display typography only; the manifest supplies the canonical title.
    canonical = section['title'].partition(':')[2].strip()
    if canonical:
        title = canonical
    original_h1.clear(); original_h1.string = title
    running = make('div', {'class':'running-label'}, section['title'].split(':')[0].upper())
    original_h1.insert_before(running)
    opening = make('header', {'class':'chapter-opening'})
    original_h1.wrap(opening)
    original_h1.insert_before(make('div', {'class':'chapter-label'}, label.title()))
    for fig in soup.find_all('figure'):
        img = fig.find('img')
        if not img:
            continue
        filename = Path(img['src']).name
        next_p = fig.find_next_sibling()
        # Existing manual captions are the publication captions. Pandoc's alt
        # text remains on the image, not duplicated below it.
        old_caption = fig.find('figcaption')
        if old_caption:
            old_caption.decompose()
        if next_p and next_p.name == 'p' and next_p.find('em') and len(next_p.get_text()) < 650:
            next_p.name = 'figcaption'
            fig.append(next_p.extract())
        if filename in RIGHTS_REPLACEMENTS:
            caption=fig.find('figcaption')
            caption_text=caption.get_text() if caption else ''
            transformations.append({'section':sid,'original':filename,'omitted_caption':caption_text,'replacement':RIGHTS_REPLACEMENTS[filename],'action':'Replace image and its credit caption with original motif; commercial reproduction basis unclear or conflicting. Source unchanged. See RIGHTS-AUDIT.md.'})
            fig.replace_with(BeautifulSoup(motif(RIGHTS_REPLACEMENTS[filename]), 'html.parser'))
            continue
        if sid.startswith('part-'):
            cap = fig.find('figcaption')
            fig.replace_with(BeautifulSoup(motif(MOTIFS[sid]), 'html.parser'))
            transformations.append({'section':sid,'original':filename,'omitted_caption':cap.get_text() if cap else '','action':'Replace generated divider with original vector motif; retain all divider prose. The image caption goes with the image.'})
        else:
            audit = RIGHTS_BY_FILE.get(filename)
            assert audit and audit['status'] == 'retain', ('Uncleared image',filename)
            caption = fig.find('figcaption')
            if caption and audit['kind'] == 'third_party' and audit.get('caption_policy') != 'keep':
                # Pandoc wraps long captions, so normalize whitespace before
                # finding the credit. Since v0.9.1 the source captions carry the
                # audited identifications themselves (ch02 Thinktank, ch14 Haifa).
                old = ' '.join(caption.get_text().split())
                description = old.split(' (',1)[0]
                new = f'{description} ({audit["artist"]}, {audit["license"]}, via Wikimedia Commons)'
                if ' '.join(new.split()) != ' '.join(old.split()):
                    caption.clear(); caption.string = new
                    transformations.append({'section':sid,'original':filename,'original_caption':old,'replacement_caption':new,'action':'Correct caption identification or required attribution from audited image source.'})
            fig['class'] = ['opener-image' if len(included_images) == 0 or not fig.find_previous_sibling('p') else 'scene-image']
            # The first image follows the chapter opening in every source section.
            if fig.find_previous_sibling() and fig.find_previous_sibling().name in ('header','div'):
                fig['class'] = ['opener-image']
            included_images.append(filename)
    for p in soup.find_all('p'):
        if p.get_text(strip=True) == 'In this chapter:':
            ul = p.find_next_sibling()
            if ul and ul.name == 'ul':
                box = make('div', {'class':'summary'})
                p.wrap(box); box.append(ul.extract())
    for h in soup.find_all('h2'):
        text = h.get_text(' ',strip=True)
        if text == 'The Foundations':
            h['class'] = ['foundation']
        if text.startswith('Precedent '):
            h['class'] = ['precedent-heading']
    for p in list(soup.find_all('p')):
        if p.get_text(' ',strip=True).startswith('The mechanism.'):
            group = make('div', {'class':'end-group'})
            p.wrap(group)
            while True:
                following = group.find_next_sibling()
                if not following or following.name not in ('p','ol','ul'):
                    break
                group.append(following.extract())
    if sid.startswith('appendix-'):
        paragraphs = soup.find_all('p',recursive=False)
        if len(paragraphs)>1 and paragraphs[-2].find_next_sibling() is paragraphs[-1]:
            group=make('div',{'class':'closing-pair'})
            paragraphs[-2].wrap(group); group.append(paragraphs[-1].extract())
    if sid == 'appendix-d':
        for colgroup in soup.find_all('colgroup'):
            colgroup.decompose()
    # Place sparse motifs at the turn from story to analysis; do not inflate
    # every opening or interrupt evidence/reference apparatus.
    if sid in MOTIFS and not sid.startswith('part-'):
        target = soup.find('h2', class_='foundation')
        if target:
            target.insert_before(BeautifulSoup(motif(MOTIFS[sid]), 'html.parser'))
        elif sid == 'conclusion':
            last = soup.find_all('h2')[-1]
            last.insert_before(BeautifulSoup(motif(MOTIFS[sid]), 'html.parser'))
    if sid == 'chapter1':
        target = next((p for p in soup.find_all('p') if p.get_text().startswith('Those four questions are the spine')), None)
        if target:
            target.insert_after(diagram('Four distinct questions', [('Capability','What can the system do?'),('Improvement','Can it help make a better successor?'),('Deployment','Can it do useful work in ordinary conditions?'),('Access','Who actually receives the result?')], 'An answer to one question does not settle the others.'))
    if sid == 'appendix-a':
        target = soup.find('h2')
        target.insert_before(diagram('From a capability to a meal', [('Produce','Enough suitable food.'),('Prepare','Food the person can use.'),('Deliver','Access the person can reach.'),('Sustain','People, repairs and dependable funding.')], 'A schematic of the proposal. Each part needs people, resources and accountable decisions.'))
    # A section already ends with a page transition. A trailing ornament must
    # never create a page of its own, so suppress purely decorative end rules.
    while soup.find_all(recursive=False) and soup.find_all(recursive=False)[-1].name == 'hr':
        soup.find_all(recursive=False)[-1].decompose()
    classes = ['chapter']
    if sid.startswith('part-'):
        classes = ['part']
    if sid.startswith('appendix-'):
        classes += ['appendix']
    if sid == 'appendix-b':
        classes += ['bibliography']
    sections.append(f'<section id="sec-{sid}" class="{" ".join(classes)}">{soup}</section>')

toc = '<section class="front toc"><h1>Contents</h1>'
for s in META['sections']:
    if s['id'] == 'part-3':
        toc += '</section><section class="front toc"><h1>Contents</h1>'
    cls = 'toc-row toc-part' if s['id'].startswith('part-') else 'toc-row'
    toc += f'<a class="{cls}" href="#sec-{s["id"]}">{html.escape(s["title"])}</a>'
toc += '<a class="toc-row" href="#image-credits">Illustration credits &amp; design notes</a></section>'

credits_data = json.loads((ROOT/'static/book-images/credits.json').read_text())
credits = '<section class="chapter credits" id="image-credits"><div class="running-label">ILLUSTRATION CREDITS</div><h1>Illustration credits<br/>&amp; design notes</h1>'
credits += '<p>The cover is the book\'s original cover illustration. Original botanical and mechanical line drawings were created with Codex for an earlier design as editable SVG artwork. The three part-divider illustrations and four photographs or artworks whose commercial reproduction basis was unclear have been replaced with those drawings. Explanatory diagrams were drawn for this book as SVG. Image captions follow the audited sources.</p>'
credits += '<p>Typeset in Source Serif 4 and Source Sans Pro, designed by Frank Grießhammer and Paul D. Hunt respectively, published by Adobe under the SIL Open Font License 1.1.</p>'
license_urls = {'CC BY 4.0':'https://creativecommons.org/licenses/by/4.0/','CC BY 2.0':'https://creativecommons.org/licenses/by/2.0/','CC BY-SA 4.0':'https://creativecommons.org/licenses/by-sa/4.0/','CC BY-SA 3.0':'https://creativecommons.org/licenses/by-sa/3.0/','CC BY-SA 2.0':'https://creativecommons.org/licenses/by-sa/2.0/','CC0':'https://creativecommons.org/publicdomain/zero/1.0/'}
for item in credits_data:
    if item['file'] not in included_images:
        continue
    audit = RIGHTS_BY_FILE[item['file']]
    license_url = audit['license_url']
    title = item['source_title'].removeprefix('File:')
    source_url=audit['source_url']
    credits += f'<div class="credit"><p><b>{html.escape(title)}</b><br/>{html.escape(audit["artist"])}. {html.escape(audit["license"])}. {html.escape(audit["modification_note"])}</p><p class="credit-url"><a href="{html.escape(source_url)}">{html.escape(source_url.removeprefix("https://"))}</a><br/><a href="{html.escape(license_url)}">{html.escape(license_url.removeprefix("https://"))}</a></p></div>'
credits += '<p>Image adaptations retain the relevant image licenses. Those licenses do not extend to the manuscript text.</p><p>'+str(sum(1 for f in included_images if RIGHTS_BY_FILE.get(f,{}).get('kind')=='generated' and f.endswith('.png')))+' narrative plates were created with PixelLab and assembled for an earlier edition. These generated illustrations depict fictional scenes and are not photographs or evidence of actual deployments. The companion asset register records generation identifiers, component files and provider terms.</p></section>'

subtitle = html.escape(META['subtitle']).replace(' and the Future','<br/>and the Future')
front = f'''<section class="front title-page"><div class="chapter-label">Christopher Tavolazzi</div><h1>Surviving<br/>the Singularity</h1><p class="subtitle">{subtitle}</p>{motif('grain-and-gripper')}<p class="edition">ILLUSTRATED EDITION</p></section>
<section class="front copyright"><p>Surviving the Singularity<br/>{html.escape(META['author'])}</p><p>Copyright © 2026 Christopher Tavolazzi.<br/>All rights reserved in original text. Quoted material and third-party images remain subject to their respective rights. Image licenses are identified in the illustration credits.</p><p>Manuscript v{META['version']} · Publication design 01<br/>September 2026</p><p>Elijah Madrone and the cooperative are fiction. The story and its imagined deployments are distinguished from historical evidence and sourced claims in the manuscript.</p></section>'''

(HERE/'assets').mkdir(exist_ok=True)
(HERE/'assets/ornament.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 30"><g fill="none" stroke="#66764e" stroke-width="1.5"><path d="M4 15h27m38 0h27M40 15l10-7 10 7-10 7z"/><circle cx="50" cy="15" r="2"/></g></svg>')
cover_motif = HERE/'assets/motifs/cover-harvest.svg'
if not cover_motif.exists():
    cover_motif = HERE/'assets/motifs/01-grain-and-gripper.svg'
if cover_motif.exists():
    art = cover_motif.read_text().replace('#202c28','#eee8d1').replace('#66764e','#bcc995')
    (HERE/'assets/cover-art.svg').write_text(art)
cover = f'''<section class="cover original-cover"><img class="cover-original" src="{(ROOT/'scripts/book-cover.png').as_uri()}" alt="Surviving the Singularity by Christopher Tavolazzi: a moss-covered robot resting in a meadow of flowers"/></section>'''

def document(body):
    return f'<!DOCTYPE html><html lang="en-US"><head><meta charset="utf-8"/><title>Surviving the Singularity</title><meta name="author" content="Christopher Tavolazzi"/><link rel="stylesheet" href="{(HERE/"book.css").as_uri()}"/></head><body>{body}</body></html>'

interior = front + toc + '<main>' + ''.join(sections) + credits + '</main>'
records = {'manuscript_version':META['version'],'design_version':'01','sections':len(sections),'source_sha256':BASELINE,'image_transformations':transformations,'included_images':included_images,'outputs':{}}
for kind, body in [('interior',interior), ('front-cover',cover)]:
    html_path = OUT / f'{kind}.html'
    html_path.write_text(document(body))
    pdf_path = OUT / f'Surviving-the-Singularity-{kind}.pdf'
    doc = HTML(filename=html_path).render()
    doc.write_pdf(pdf_path, full_fonts=True)
    layout = []
    for n, page in enumerate(doc.pages, 1):
        boxes = []
        images = []
        for b in page._page_box.descendants():
            if type(b).__name__ == 'TextBox' and b.text.strip():
                boxes.append({'text':b.text,'rect':[b.position_x,b.position_y,b.width,b.height],'tag':b.element_tag})
            if 'ReplacedBox' in type(b).__name__ and b.element is not None:
                src=b.element.get('src','')
                if src.startswith('file:') and not src.endswith('.svg'):
                    with Image.open(src.removeprefix('file://')) as im:
                        images.append({'file':Path(src).name,'pixels':list(im.size),'display_inches':[b.width/96,b.height/96],'ppi':min(im.width/(b.width/96),im.height/(b.height/96))})
        layout.append({'page':n,'width':page.width,'height':page.height,'boxes':boxes,'images':images})
    (OUT/f'{kind}-layout.json').write_text(json.dumps(layout))
    records['outputs'][kind]={'path':str(pdf_path),'pages':len(doc.pages),'sha256':hashlib.sha256(pdf_path.read_bytes()).hexdigest()}
    print(f'{kind}: {len(doc.pages)} pages', flush=True)
(OUT/'source-rendered.html').write_text(''.join(visible_baseline))
writer = PdfWriter(clone_from=OUT/'Surviving-the-Singularity-interior.pdf')
writer.insert_page(PdfReader(OUT/'Surviving-the-Singularity-front-cover.pdf').pages[0],0)
writer.set_page_label(0,0,prefix='Cover')
writer.set_page_label(1,4,style=PageLabelStyle.LOWERCASE_ROMAN,start=1)
writer.set_page_label(5,len(writer.pages)-1,style=PageLabelStyle.DECIMAL,start=1)
writer.add_metadata({'/Title':META['title'],'/Author':META['author'],'/Subject':f'Publication design edition of manuscript v{META["version"]}'})
reading = OUT/'Surviving-the-Singularity-reading.pdf'
writer.write(reading)
records['outputs']['reading']={'path':str(reading),'pages':len(writer.pages),'sha256':hashlib.sha256(reading.read_bytes()).hexdigest()}
print(f'reading: {len(writer.pages)} pages', flush=True)
(OUT/'build.json').write_text(json.dumps(records,indent=2)+'\n')
print('Manuscript hashes unchanged. Build record:', OUT/'build.json')
