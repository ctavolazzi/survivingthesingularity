"""Exercise final figure markers and real Weasy boxes without a whole-book build."""
from pathlib import Path
import json
import subprocess
import sys
from bs4 import BeautifulSoup
from weasyprint import HTML,CSS

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'publication'))
sys.path.insert(0,str(ROOT/'docs/v0.9.2'))
from figure_layout import capture,check,specifications,negative_controls
from print_figures import print_variant
from visuals import apply_figure_class,entries

OUT=Path(__file__).parent/'visual-proof';registry=entries();sections=[]
meta=json.loads((ROOT/'src/lib/data/book/book.json').read_text())
for section in meta['sections']:
 raw=(ROOT/'src/lib/data/book'/section['file']).read_text()
 html=subprocess.run(['pandoc','-f','markdown','-t','html5'],input=raw,text=True,capture_output=True,check=True).stdout
 soup=BeautifulSoup(html,'html.parser')
 for figure in soup.find_all('figure'):
  image=figure.find('img');name=Path(image['src']).name if image else None
  if name not in registry:continue
  caption=figure.find_next_sibling()
  if figure.find('figcaption'):figure.find('figcaption').decompose()
  assert caption and caption.name=='p' and caption.find('em') and len(caption.get_text())<650,name
  caption.name='figcaption';figure.append(caption.extract())
  image['src']=(print_variant(name) if name.endswith('.svg') else ROOT/'static/book-images'/name).as_uri()
  apply_figure_class(figure,name)
  sections.append('<section class="chapter">'+str(figure)+'<p>A service needs people who can maintain it, clear agreements, and a way to ask for help. This surrounding prose checks the actual image and caption footprint.</p>'*4+'</section>')
path=OUT/'all-figures-fixture.html';path.write_text('<html><head><meta charset="utf-8"/></head><body><main>'+''.join(sections)+'</main></body></html>')
doc=HTML(filename=path).render(stylesheets=[CSS(filename=ROOT/'publication/book.css')])
record=capture(doc,path,ROOT/'src/lib/data/book/visuals.json')
errors,measurements=check(record,specifications(BeautifulSoup(path.read_text(),'html.parser'),registry),registry)
(OUT/'all-figures-layout.json').write_text(json.dumps(record,indent=2)+'\n')
report={'figures':len(measurements),'pages':len(doc.pages),'errors':errors,'negative_controls':negative_controls(),'measurements':measurements,'limit':'All 23 final images and canonical captions with adjacent prose; not final full-book pagination.'}
(OUT/'all-figures-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='measurements'},indent=2))
assert not errors,errors
assert len(measurements)==23
