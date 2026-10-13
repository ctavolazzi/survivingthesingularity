"""Browser proof at actual 4.56-inch print width, including red controls."""
from pathlib import Path
import base64
import importlib.util
import json
from playwright.sync_api import sync_playwright
from vignettes import ROOT, HERE, IMAGES, BUILDERS, PALETTES

METRICS = r'''() => {
 const svg=document.querySelector('svg'), frame=svg.getBoundingClientRect();
 const ts=[...svg.querySelectorAll('text')];
 const boxes=ts.map(t=>({text:t.textContent, ...JSON.parse(JSON.stringify(t.getBoundingClientRect().toJSON()))}));
 const overlaps=[];
 for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
  const a=boxes[i],b=boxes[j];
  if(a.left<b.right && b.left<a.right && a.top<b.bottom && b.top<a.bottom)overlaps.push([a.text,b.text]);
 }
 return {labels:ts.length,min_pt:Math.min(...ts.map(t=>parseFloat(getComputedStyle(t).fontSize)*frame.width/svg.viewBox.baseVal.width*.75)),
   width_in:frame.width/96,height_in:frame.height/96,overlaps,
   outside:boxes.filter(b=>b.left<frame.left || b.right>frame.right || b.top<frame.top || b.bottom>frame.bottom).map(b=>b.text)};
}'''


def proof():
 out=HERE/'visual-proof';out.mkdir(exist_ok=True)
 spec=importlib.util.spec_from_file_location('legacy_geometry',ROOT/'docs/v0.9.2/print_figures.py')
 geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
 font=base64.b64encode((ROOT/'publication/assets/fonts/JetBrainsMono-Regular.ttf').read_bytes()).decode()
 style=f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{font})}} body{{margin:0}}svg{{display:block;width:4.56in;height:auto}}"
 checks={};controls={}
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome');page=browser.new_page(viewport={'width':600,'height':700},device_scale_factor=1)
  def load(svg,mode='print'):
   page.set_content(f'<style>{style}body{{background:{"#020617" if mode=="screen" else "#fff"}}}</style>'+svg)
   page.evaluate('document.fonts.ready')
  sample=BUILDERS['access-gate']('print').finish();load(sample)
  page.evaluate("document.querySelector('text').setAttribute('font-size','4')")
  assert page.evaluate(METRICS)['min_pt']<8;controls['undersized_label']=True
  load(sample);page.evaluate("const ts=document.querySelectorAll('text');ts[1].setAttribute('x',ts[0].getAttribute('x'));ts[1].setAttribute('y',ts[0].getAttribute('y'))")
  assert page.evaluate(METRICS)['overlaps'];controls['overlapping_labels']=True
  load(sample);page.evaluate("document.querySelector('text').setAttribute('x','470')")
  assert page.evaluate(METRICS)['outside'];controls['out_of_frame']=True
  load(sample);page.evaluate("""const t=document.querySelector('text'),b=t.getBBox(),l=document.createElementNS('http://www.w3.org/2000/svg','path');l.setAttribute('d',`M${b.x} ${b.y+b.height/2}h${b.width}`);l.setAttribute('stroke','red');t.parentNode.append(l);""")
  assert any('crosses' in x for x in page.evaluate(geometry.AUDIT_JS));controls['path_through_label']=True
  for key in BUILDERS:
   checks[key]={}
   for mode in PALETTES:
    name='v101-visual-'+key+'.svg';load((IMAGES/('print' if mode=='print' else '')/name).read_text(),mode)
    measure=page.evaluate(METRICS);measure['path_errors']=page.evaluate(geometry.AUDIT_JS)
    assert measure['min_pt']>=8 and not measure['overlaps'] and not measure['outside'],(key,mode,measure)
    assert not measure['path_errors'],(key,mode,measure['path_errors'])
    page.locator('svg').screenshot(path=str(out/f'{key}-{mode}.png'))
    checks[key][mode]=measure
  browser.close()
 report={'figures':checks,'negative_controls':controls,'limits':'Browser geometry and screen screenshots at 4.56-inch width, including label intersections with sampled paths. This cannot certify physical printer contrast, SVG font substitution in every reader, or full-book pagination.'}
 (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'figures':len(checks),'minimum_pt':min(r['print']['min_pt'] for r in checks.values()),'negative_controls':controls}))


if __name__=='__main__':proof()
