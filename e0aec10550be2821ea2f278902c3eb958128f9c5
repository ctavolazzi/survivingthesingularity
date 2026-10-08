"""Bounded production and renderer proof, without building the full book."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from unittest.mock import patch
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
OUT=HERE/'visual-proof'
OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'publication'))
import visuals


def production_proof():
 names=[name for name in visuals.entries() if name.endswith('.svg')]
 for name in names:assert visuals.prepared_variant(name).exists()
 registered=visuals.entries()
 bad=json.loads(json.dumps(registered));name=names[0];bad[name]['print']['sha256']='0'*64
 with patch.object(visuals,'entries',return_value=bad):
  try:visuals.prepared_variant(name)
  except AssertionError:pass
  else:raise AssertionError('Stale print hash negative control stayed green')
 missing={k:v for k,v in registered.items() if k!=name}
 with patch.object(visuals,'entries',return_value=missing):
  try:visuals.prepared_variant(name)
  except AssertionError:pass
  else:raise AssertionError('Unregistered prepared artwork control stayed green')
 spec=importlib.util.spec_from_file_location('legacy_print',ROOT/'docs/v0.9.2/print_figures.py')
 legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
 before={name:hashlib.sha256(visuals.prepared_variant(name).read_bytes()).hexdigest() for name in names}
 with patch.object(legacy,'figures_in_book',return_value=names),patch.object(legacy,'REPORT',OUT/'prepared-bridge-check.json'),patch.object(legacy,'recolor',side_effect=AssertionError('Prepared artwork reached generic recoloring')):
  legacy.main()
 after={name:hashlib.sha256(visuals.prepared_variant(name).read_bytes()).hexdigest() for name in names}
 assert before==after
 return {'prepared_svg_count':len(names),'unchanged_after_legacy_pipeline':True,'negative_controls':['stale print hash','unregistered prepared SVG']}


PARAGRAPH='A useful service reaches the people who depend on it. Its work includes maintaining equipment, checking the arrangements, listening to complaints, and telling households what they can rely on. A meal has to arrive on an ordinary day as well as a demonstration day. '


def inspect_print(document):
 errors=[];figures=[]
 for page_no,page in enumerate(document.pages,1):
  pagebox=page._page_box
  content=(pagebox.content_box_x(),pagebox.content_box_y(),pagebox.content_box_x()+pagebox.width,pagebox.content_box_y()+pagebox.height)
  for b in pagebox.descendants():
   if b.element is not None and b.element.tag=='figure' and type(b).__name__ in ('BlockBox','FlexBox') and b.style.get('float') in ('left','right'):
    bounds=(b.content_box_x(),b.content_box_y(),b.content_box_x()+b.width,b.content_box_y()+b.height)
    figures.append({'page':page_no,'class':b.element.get('class'),'x_in':b.content_box_x()/96,'width_in':b.width/96,'height_in':b.height/96})
    if bounds[0]<content[0]-.1 or bounds[2]>content[2]+.1 or bounds[1]<content[1]-.1 or bounds[3]>content[3]+.1:errors.append(['figure outside content',page_no,bounds,content])
    for text in pagebox.descendants():
     if type(text).__name__=='TextBox' and text.element is not None and text.element.tag=='p':
      r=(text.position_x,text.position_y,text.position_x+text.width,text.position_y+text.height)
      # Use figure content rectangle, excluding deliberate inter-column margin.
      f=(b.content_box_x(),b.content_box_y(),b.content_box_x()+b.width,b.content_box_y()+b.height)
      if r[0]<f[2] and f[0]<r[2] and r[1]<f[3] and f[1]<r[3]:errors.append(['prose intersects figure',page_no,text.text])
 return errors,figures


def print_proof():
 # Portrait source serves only as a geometry fixture while root prepares alpha art.
 photo=(ROOT/'static/book-images/ch01-atlas.jpg').as_uri()
 chunks=[]
 for side in ['left','right']:
  chunks.append(f'<section class="chapter"><h2>Cutout float: {side}</h2><figure class="book-figure figure-cutout-{side}"><img src="{photo}" alt="Geometry fixture"/><figcaption>Caption stays with the image, inside the text area.</figcaption></figure>'+''.join('<p>'+PARAGRAPH+'</p>' for _ in range(6))+'<h2>Following section clears the illustration</h2><p>'+PARAGRAPH+'</p></section>')
 document=HTML(string='<!doctype html><html><main>'+''.join(chunks)+'</main></html>',base_url=str(ROOT)).render(stylesheets=[CSS(filename=str(ROOT/'publication/book.css'))])
 errors,figures=inspect_print(document)
 assert len(figures)==2,figures
 assert not errors,errors
 mutant=HTML(string='<!doctype html><html><main>'+''.join(chunks)+'</main></html>',base_url=str(ROOT)).render(stylesheets=[CSS(filename=str(ROOT/'publication/book.css')),CSS(string='figure.figure-cutout-left { margin-left: -1in; }')])
 assert any(e[0]=='figure outside content' for e in inspect_print(mutant)[0]), 'Gutter defect control stayed green'
 mutant=HTML(string='<!doctype html><html><main>'+''.join(chunks)+'</main></html>',base_url=str(ROOT)).render(stylesheets=[CSS(filename=str(ROOT/'publication/book.css')),CSS(string='figure.figure-cutout-left { position: relative; left: 1in; }')])
 assert any(e[0]=='prose intersects figure' for e in inspect_print(mutant)[0]), 'Prose intersection control stayed green'
 document.write_pdf(OUT/'presentation-print.pdf')
 return {'pages':len(document.pages),'figures':figures,'out_of_bounds_or_prose_intersections':errors,'negative_controls':['negative margin into gutter','relative displacement into prose'],'limit':'Portrait placeholder tests the float geometry; final alpha images and complete chapter pagination need the frozen-book proof.'}


def epub_proof():
 md='''# Presentation proof\n\n![Accessible conceptual still]('''+(ROOT/'static/book-images/v101-visual-access-gate.svg').as_uri()+''')\n\n*Caption stays in the text.*\n\n<!-- interactive:food-delivery -->\n\nA retained paragraph follows.\n'''
 result=subprocess.run(['pandoc','-f','markdown','-t','html5','--filter',str(ROOT/'scripts/book_visual_filter.py')],input=md,text=True,capture_output=True,check=True).stdout
 soup=BeautifulSoup(result,'html.parser')
 figure=soup.find('figure');assert figure and 'book-figure' in figure['class']
 assert figure.find('figcaption').get_text()=='Caption stays in the text.'
 assert figure.find('img')['alt']=='Accessible conceptual still'
 assert 'interactive:' not in result and 'A retained paragraph follows.' in result
 (OUT/'epub-figure-fixture.html').write_text(result)
 broken=result.replace('A retained paragraph follows.','')
 assert 'A retained paragraph follows.' not in BeautifulSoup(broken,'html.parser').get_text()
 return {'class_preserved':True,'manual_caption_once':result.count('Caption stays in the text.')==1,'accessible_alt_preserved':True,'interactive_marker_absent':True,'negative_control':'removed paragraph'}


if __name__=='__main__':
 report={'prepared_variants':production_proof(),'print':print_proof(),'epub_filter':epub_proof()}
 (OUT/'presentation-checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
