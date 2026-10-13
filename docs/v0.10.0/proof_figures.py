"""Build the five print derivatives and prove physical label size and geometry.

Loads the packaged font in Chrome, uses the existing collision-fit pipeline,
then measures both sources and derivatives at the 6x9 edition's 4.56in width.
Negative controls inject an overlapping duplicate and a 1px label in memory.
"""
from pathlib import Path
import base64
import importlib.util
import json
import sys
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from figures import FIGURES

spec = importlib.util.spec_from_file_location('print_figures', HERE.parent / 'v0.9.2/print_figures.py')
printer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(printer)
PROOF = HERE / 'figure-proof'
WIDTH = 4.56 * 96
font_css = ''
for face, weight in [('Regular',400),('SemiBold',600),('Bold',700)]:
    data = base64.b64encode((ROOT / f'publication/assets/fonts/JetBrainsMono-{face}.ttf').read_bytes()).decode()
    font_css += f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{data});font-weight:{weight};}}"

class FontPage:
    def __init__(self, page):
        self.page = page
    def set_content(self, content):
        self.page.set_content(content.replace('<svg ', '<style>'+font_css+'</style><svg ', 1))
        self.page.evaluate('() => document.fonts.ready')
    def evaluate(self, *args):
        return self.page.evaluate(*args)

METRICS = r'''() => {
    const svg=document.querySelector('svg'), vb=svg.viewBox.baseVal;
    const svgRect=svg.getBoundingClientRect();
    const texts=[...svg.querySelectorAll('text')];
    const sizes=texts.map(t=>({text:t.textContent,pt:parseFloat(getComputedStyle(t).fontSize)*svgRect.width/vb.width*72/96}));
    const outside=texts.filter(t=>{let b=t.getBBox();return b.x<vb.x-0.1||b.y<vb.y-0.1||b.x+b.width>vb.x+vb.width+0.1||b.y+b.height>vb.y+vb.height+0.1;}).map(t=>t.textContent);
    return {width_in:svgRect.width/96,height_in:svgRect.height/96,min_pt:Math.min(...sizes.map(s=>s.pt)),labels:texts.length,outside,smallest:sizes.sort((a,b)=>a.pt-b.pt).slice(0,3)};
}'''

def load(page, svg):
    svg = svg[svg.index('<svg '):]
    page.set_content('<!doctype html><body style="margin:0;background:white">'+svg.replace('<svg ', f'<svg width="{WIDTH}" ', 1))


def main():
    PROOF.mkdir(exist_ok=True)
    report = json.loads(printer.REPORT.read_text())
    records = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome')
        raw = browser.new_page(viewport={'width': 500, 'height': 1100}, device_scale_factor=2)
        page = FontPage(raw)
        # Prove that the inherited geometric instrument catches an actual overlap.
        load(page, (printer.IMAGES / 'ch09-region-ring.svg').read_text())
        raw.evaluate('''() => {const t=document.querySelector('svg text'); t.parentNode.appendChild(t.cloneNode(true));}''')
        overlap = page.evaluate(printer.AUDIT_JS)
        assert any('labels overlap' in result for result in overlap), 'Overlap negative control stayed green'
        # Prove that minimum physical size is measured, not inferred from pixels.
        load(page, (printer.IMAGES / 'ch09-region-ring.svg').read_text())
        raw.evaluate('''() => document.querySelector('svg text').setAttribute('font-size','1')''')
        assert page.evaluate(METRICS)['min_pt'] < 7, 'Size negative control stayed green'
        negative = {'overlap_detected': True, 'undersize_detected': True}
        for name in FIGURES:
            source = (printer.IMAGES / name).read_text()
            load(page, source)
            original_errors = page.evaluate(printer.AUDIT_JS)
            original_metrics = page.evaluate(METRICS)
            assert not original_errors, (name, 'source', original_errors)
            assert not original_metrics['outside'], (name, original_metrics)
            raw.locator('svg').screenshot(path=str(PROOF / name.replace('.svg','-screen.png')))
            fit = printer.fit(page, printer.recolor(source, name))
            assert not fit['new_collisions'], (name, fit['new_collisions'])
            printed = fit.pop('svg')
            destination = printer.OUT / name
            destination.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+printed+'\n')
            fit.pop('new_collisions')
            fit['source_sha256'] = printer.sha(printer.IMAGES / name)
            fit['print_sha256'] = printer.sha(destination)
            report['figures'][name] = fit
            load(page, printed)
            print_errors = page.evaluate(printer.AUDIT_JS)
            print_metrics = page.evaluate(METRICS)
            assert not print_errors, (name, 'print', print_errors)
            assert not print_metrics['outside'], (name, print_metrics)
            assert print_metrics['min_pt'] >= 7, (name, 'too small', print_metrics)
            assert print_metrics['height_in'] <= 7.0, (name, 'height limit', print_metrics)
            raw.locator('svg').screenshot(path=str(PROOF / name.replace('.svg','-print.png')))
            records[name] = {'source': original_metrics, 'print': print_metrics, 'source_collisions': original_errors, 'print_collisions': print_errors, 'source_sha256':fit['source_sha256'],'print_sha256':fit['print_sha256']}
            print(name, round(print_metrics['min_pt'],2), 'pt minimum,', round(print_metrics['height_in'],2), 'in high')
        browser.close()
    printer.REPORT.write_text(json.dumps(report, indent=2)+'\n')
    (PROOF / 'checks.json').write_text(json.dumps({'negative_controls':negative,'figures':records},indent=2)+'\n')

if __name__ == '__main__':
    main()
