"""Browser geometry proof for seven revised diagrams and preserved baselines.

Screen is shown at 480 CSS pixels; print is shown at the actual 4.56-inch
placement width. This is a bounded figure proof, not a book render.
"""
from pathlib import Path
import base64
import importlib.util
import json
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
from figures_middle import ROOT, HERE, IMAGES, BASELINE, BUILDERS, PALETTES

METRICS = r'''() => {
 const svg=document.querySelector('svg'), frame=svg.getBoundingClientRect();
 const ts=[...svg.querySelectorAll('text')];
 const boxes=ts.map(t=>({text:t.textContent, ...t.getBoundingClientRect().toJSON()}));
 const overlaps=[];
 for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
  const a=boxes[i],b=boxes[j];
  if(a.left<b.right && b.left<a.right && a.top<b.bottom && b.top<a.bottom)overlaps.push([a.text,b.text]);
 }
 return {labels:ts.length,
   min_source_px:Math.min(...ts.map(t=>parseFloat(getComputedStyle(t).fontSize))),
   min_rendered_pt:Math.min(...ts.map(t=>parseFloat(getComputedStyle(t).fontSize)*frame.width/svg.viewBox.baseVal.width*.75)),
   width_css_px:frame.width,height_css_px:frame.height,overlaps,
   outside:boxes.filter(b=>b.left<frame.left || b.right>frame.right || b.top<frame.top || b.bottom>frame.bottom).map(b=>b.text), boxes};
}'''


def geometry(svg):
    """Compare layout separately from palette and print's white background."""
    root = ET.fromstring(svg)
    records = []
    for i, el in enumerate(root):
        tag = el.tag.rsplit('}', 1)[-1]
        if tag == 'rect' and el.get('width') == '480' and el.get('height') == root.get('viewBox').split()[-1]:
            continue
        records.append((tag, {k: v for k, v in el.attrib.items() if k not in ['fill', 'stroke']}, el.text))
    return root.get('viewBox'), records


def proof():
    out = HERE / 'middle-figure-proof'
    out.mkdir(exist_ok=True)
    spec = importlib.util.spec_from_file_location('legacy_geometry', ROOT / 'docs/v0.9.2/print_figures.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    font = base64.b64encode((ROOT / 'publication/assets/fonts/JetBrainsMono-Regular.ttf').read_bytes()).decode()
    font_style = f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{font})}}"
    checks, baseline, controls = {}, {}, {}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome')
        page = browser.new_page(viewport={'width': 520, 'height': 720}, device_scale_factor=1)

        def load(svg, mode='print'):
            width = '480px' if mode == 'screen' else '4.56in'
            background = '#0f172a' if mode == 'screen' else '#fff'
            page.set_content(f'<style>{font_style}body{{margin:0;background:{background}}}svg{{display:block;width:{width};height:auto}}</style>' + svg)
            page.evaluate('document.fonts.ready')

        def measure():
            result = page.evaluate(METRICS)
            result['path_errors'] = page.evaluate(helper.AUDIT_JS)
            result['pass'] = result['min_source_px'] >= 14 and result['min_rendered_pt'] >= 8 and not result['outside'] and not result['overlaps'] and not result['path_errors']
            return result

        sample = BUILDERS['ch09-hyperlocal-vs-global.svg']('print').finish()
        mutations = {
            'undersized_label': "document.querySelector('text').setAttribute('font-size','4')",
            'overlapping_labels': "const t=document.querySelectorAll('text');t[1].setAttribute('x',t[0].getAttribute('x'));t[1].setAttribute('y',t[0].getAttribute('y'))",
            'out_of_frame': "document.querySelector('text').setAttribute('x','470')",
            'path_through_label': "const t=document.querySelector('text'),b=t.getBBox(),l=document.createElementNS('http://www.w3.org/2000/svg','path');l.setAttribute('d',`M${b.x} ${b.y+b.height/2}h${b.width}`);l.setAttribute('stroke','red');t.parentNode.append(l)",
        }
        for key, mutation in mutations.items():
            load(sample)
            page.evaluate(mutation)
            result = measure()
            controls[key] = result
            page.locator('svg').screenshot(path=str(out / f'negative-{key}.png'))
            assert not result['pass'], ('Negative control unexpectedly passed', key)
            expected_failure = {
                'undersized_label': result['min_source_px'] < 14,
                'overlapping_labels': bool(result['overlaps']),
                'out_of_frame': bool(result['outside']),
                'path_through_label': any('crosses' in error for error in result['path_errors']),
            }[key]
            assert expected_failure, ('Control failed for the wrong reason', key)

        for name in BUILDERS:
            checks[name], baseline[name] = {}, {}
            for mode in PALETTES:
                subdir = 'print' if mode == 'print' else ''
                load((BASELINE / subdir / name).read_text(), mode)
                baseline[name][mode] = measure()
                load((IMAGES / subdir / name).read_text(), mode)
                checks[name][mode] = measure()
                page.locator('svg').screenshot(path=str(out / f'{Path(name).stem}-{mode}.png'))
            checks[name]['identical_geometry'] = geometry((IMAGES / name).read_text()) == geometry((IMAGES / 'print' / name).read_text())
        browser.close()
    report = {
        'screen_width_css_px': 480,
        'print_width_inches': 4.56,
        'font': 'Embedded publication/assets/fonts/JetBrainsMono-Regular.ttf',
        'negative_controls': controls,
        'baseline': baseline,
        'figures': checks,
        'limits': 'Chromium screenshots, label bounds and overlaps, sampled path intersections and screen/print layout comparison. Does not certify physical printer contrast, all reader font substitution, electronics safety, measured model distributions or full-book pagination.',
    }
    report_path = out / 'checks.json'
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    assert json.loads(report_path.read_text()) == report
    failures = [(name, mode, result) for name, modes in checks.items() for mode, result in modes.items() if isinstance(result, dict) and not result['pass']]
    assert not failures, [(name, mode, {k: v for k, v in result.items() if k not in ['boxes']}) for name, mode, result in failures]
    assert all(row['identical_geometry'] for row in checks.values())
    print(json.dumps({'figures': len(checks), 'variants': 2 * len(checks), 'minimum_print_pt': min(row['print']['min_rendered_pt'] for row in checks.values()), 'negative_controls': len(controls), 'passed': True}))


if __name__ == '__main__':
    proof()
