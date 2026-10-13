"""Browser proof for four corrected resource diagrams at print width."""
import base64
import importlib.util
import json
from playwright.sync_api import sync_playwright
from figures_core import ROOT, HERE, BUILDERS, PALETTES

spec=importlib.util.spec_from_file_location('legacy_geometry',ROOT/'docs/v0.9.2/print_figures.py')
geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
spec=importlib.util.spec_from_file_location('vignette_metrics',ROOT/'docs/v0.10.1/prove_vignettes.py')
metrics=importlib.util.module_from_spec(spec);spec.loader.exec_module(metrics)
OUT=HERE/'art-core-proof';OUT.mkdir(exist_ok=True)
font=base64.b64encode((ROOT/'publication/assets/fonts/JetBrainsMono-Regular.ttf').read_bytes()).decode()
style=f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{font})}} body{{margin:0}}svg{{display:block;width:4.56in;height:auto}}"
records={};controls={}
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome');page=browser.new_page(viewport={'width':500,'height':700})
    def load(svg,mode='print'):
        page.set_content(f'<style>{style}body{{background:{"#020617" if mode=="screen" else "white"}}}</style>'+svg)
        page.evaluate('document.fonts.ready')
    sample=next(iter(BUILDERS.values()))('print').finish()
    load(sample);page.evaluate("document.querySelector('text').setAttribute('font-size','4')")
    assert page.evaluate(metrics.METRICS)['min_pt']<8;controls['small_label']=True
    load(sample);page.evaluate("document.querySelector('text').setAttribute('x','470')")
    assert page.evaluate(metrics.METRICS)['outside'];controls['outside_label']=True
    load(sample);page.evaluate("const t=document.querySelectorAll('text');t[1].setAttribute('x',t[0].getAttribute('x'));t[1].setAttribute('y',t[0].getAttribute('y'))")
    assert page.evaluate(metrics.METRICS)['overlaps'];controls['label_overlap']=True
    load(sample);page.evaluate("const t=document.querySelector('text'),b=t.getBBox(),l=document.createElementNS('http://www.w3.org/2000/svg','path');l.setAttribute('d',`M${b.x} ${b.y+b.height/2}h${b.width}`);l.setAttribute('stroke','red');t.parentNode.append(l)")
    assert any('crosses' in e for e in page.evaluate(geometry.AUDIT_JS));controls['path_through_label']=True
    for name in BUILDERS:
        records[name]={}
        for mode in PALETTES:
            load((ROOT/'static/book-images'/('print' if mode=='print' else '')/name).read_text(),mode)
            result=page.evaluate(metrics.METRICS);result['paths']=page.evaluate(geometry.AUDIT_JS)
            records[name][mode]=result
            page.locator('svg').screenshot(path=str(OUT/f'{name[:-4]}-{mode}.png'))
    browser.close()
report={'figures':records,'negative_controls':controls,'limits':'Actual-width browser geometry and screenshot evidence; final PDF page placement requires separate proof.'}
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
errors={n:{m:r for m,r in modes.items() if r['min_pt']<8 or r['outside'] or r['overlaps'] or r['paths']} for n,modes in records.items()}
errors={n:r for n,r in errors.items() if r}
print(json.dumps(errors or {'figures':len(records),'controls':controls}));assert not errors
