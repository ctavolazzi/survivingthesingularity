"""Four original practical illustrations with shared screen and print geometry.

Run once to write the assets and add their canonical image/caption blocks. The
inserts are idempotent and leave all pre-existing manuscript bytes unchanged.
Run with --proof to inspect embedded-font browser geometry at print width.
"""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
IMAGES = ROOT / 'static/book-images'
OUT = HERE / 'practical-art'
sys.path.insert(0, str(ROOT / 'docs/v0.10.1'))
from vignettes import Art, PALETTES


def reading_routes(mode):
    a = Art(mode, 376, 'THREE WAYS INTO THE BOOK',
            'Three reading routes. The short route links the Introduction, Chapter 19 and Appendix C. A wider view adds the Preface, Chapters 6 and 12, and the Conclusion. The full route reads every section in order, following Elijah through the chapters.')
    a.text(20, 77, 'Start with the route you need.', color='ink')
    a.text(20, 108, '01  THE SHORT ROUTE', 16, 'ink', weight=600)
    a.line(50, 131, 431, 131, 'amber', 2)
    for x, label in [(50, 'Intro'), (240, 'Ch. 19'), (431, 'App. C')]:
        a.circle(x, 131, 5, 'amber', 2, 'paper')
        a.text(x, 158, label, 14, 'ink', anchor='middle')
    a.text(20, 196, '02  WIDEN THE VIEW: ADD', 16, 'ink', weight=600)
    a.line(50, 219, 417, 219, 'blue', 2)
    for x, label in [(50, 'Preface'), (173, 'Ch. 6'), (295, 'Ch. 12'), (417, 'Conclusion')]:
        a.circle(x, 219, 5, 'blue', 2, 'paper')
        a.text(x, 246, label, 14, 'ink', anchor='middle')
    a.text(20, 285, '03  THE WHOLE THING', 16, 'ink', weight=600)
    a.path('M20 309H449M442 303L449 309L442 315', 'ink', 2)
    a.text(20, 340, "Read in order. Follow Elijah's story.", 14, 'ink')
    return a


def service_ledger(mode):
    a = Art(mode, 357, 'WHAT A CONTINUING SERVICE COSTS',
            'An open ledger names four costs behind a continuing service: equipment, maintenance, remaining labor and delivery. All four require dependable funding, even when the person eating pays nothing.')
    a.text(20, 77, 'Free at the door still needs funding.', color='ink')
    # One open ledger, four entries, a visible center fold. These are cost
    # categories from the source, not invented amounts or a budget estimate.
    a.path('M20 104Q128 92 240 107Q348 92 460 104V282Q348 268 240 286Q128 268 20 282Z', 'ink', 1.8, 'paper')
    a.path('M240 107V286', 'rule', 1)
    for x in (37, 260):
        for y in (160, 233, 253):
            a.line(x, y, x + 183, y, 'rule', .6)
    a.text(38, 136, 'Equipment', 16, 'ink', weight=600)
    a.text(38, 207, 'Maintenance', 16, 'ink', weight=600)
    a.text(260, 136, 'Remaining labor', 16, 'ink', weight=600)
    a.text(260, 207, 'Delivery', 16, 'ink', weight=600)
    # Small leaf-like bookkeeping ticks evoke a used working ledger.
    for x, y in [(201, 181), (201, 267), (423, 181), (423, 267)]:
        a.path(f'M{x-9} {y-10}L{x-3} {y-4}L{x+9} {y-18}', 'amber', 1.5)
    a.footer(327, ['Name who pays, and what keeps getting done.'])
    return a


def offline_check(mode):
    a = Art(mode, 381, 'PROVE YOUR OFFLINE COPY WORKS',
            'A phone beside four steps: save a reference you may copy, record its source and date, turn the network off, then open it and find a specific answer. The test proves retrieval, not the truth of every claim in the reference.')
    # A physical phone with an open reference page, not an app screenshot.
    a.path('M39 103Q39 93 49 93H117Q127 93 127 103V267Q127 277 117 277H49Q39 277 39 267Z', 'ink', 2, 'paper')
    a.path('M47 117H119V254H47Z', 'blue', 1.2)
    a.line(71, 105, 96, 105, 'ink', 2)
    a.circle(83, 266, 3, 'ink', 1)
    a.path('M60 137H105M60 149H105M60 161H93M60 186H105M60 198H105M60 210H97', 'rule', 1.4)
    a.path('M64 234L75 243L102 220', 'amber', 2.2)
    a.text(83, 309, 'Offline', 16, 'ink', anchor='middle')
    steps = [
        ('Save one reference.', 'Choose one you may copy.'),
        ('Record source + date.', 'Know which edition it is.'),
        ('Turn the network off.', 'Test the local copy.'),
        ('Open it. Find an answer.', 'Check you can retrieve it.'),
    ]
    for n, (heading, detail) in enumerate(steps, 1):
        y = 102 + (n - 1) * 66
        a.text(158, y, str(n), 20, 'amber', weight=600)
        a.text(183, y, heading, 14, 'ink', weight=600)
        a.text(183, y + 23, detail, 14)
    a.footer(358, ['Start with the device you already have.'])
    return a


def year_index(mode):
    a = Art(mode, 398, 'YOUR FIRST YEAR, AT A GLANCE',
            'A two-page index of the twelve monthly themes: get your bearings, know your numbers, know your work, learn the tools, plant something, find your people, count the food, own something, tell it, find ground, go on the record, and look back then forward. Move months to fit your life and season.')
    a.text(20, 77, 'Move a month to fit your season or life.', color='ink')
    a.path('M20 100H230V357H20ZM250 100H460V357H250Z', 'rule', 1, 'paper')
    a.line(20, 105, 230, 105, 'amber', 3)
    a.line(250, 105, 460, 105, 'blue', 3)
    months = [
        ('Get your bearings',), ('Know your numbers',), ('Know your work',),
        ('Learn the tools',), ('Plant something',), ('Find your people',),
        ('Count the food',), ('Own something',), ('Tell it',),
        ('Find ground',), ('Go on the record',), ('Look back,', 'then forward'),
    ]
    for i, labels in enumerate(months):
        column, row = divmod(i, 6)
        x, y = 31 + column * 230, 131 + row * 40
        a.text(x, y, f'{i+1:02}', 17, 'amber' if column == 0 else 'blue')
        for j, label in enumerate(labels):
            a.text(x + 39, y - (4 if len(labels) > 1 else 0) + 21 * j, label, 14, 'ink')
        if row < 5:
            a.line(x + 39, y + 13, x + 183, y + 13, 'rule', .6)
    a.text(20, 382, 'Choose a scale you can sustain.', color='ink')
    return a


SPECS = [
    dict(file='v103-reading-routes.svg', builder=reading_routes,
         source_file='31-how-to-use.md', anchor='## Start from where you\'re standing',
         alt='Three reading routes: Introduction, Chapter 19 and Appendix C; add Preface, Chapters 6 and 12, and Conclusion for a wider view; or read every section in order.',
         caption="Three ways in. The short route gives you the argument and plan; the full route follows Elijah through the chapters."),
    dict(file='v103-service-ledger.svg', builder=service_ledger,
         source_file='24-appendix-c.md', anchor='After food, the order is land care, cleanup, shelter, then everything further out. A priority is where you start, not a waiting list for people in urgent need.',
         alt='An open ledger with four continuing service costs: equipment, maintenance, remaining labor and delivery. No prices or budget estimates are shown.',
         caption='Free to the person eating still leaves a working ledger: equipment, maintenance, remaining labor, and delivery need dependable funding.'),
    dict(file='v103-offline-check.svg', builder=offline_check,
         source_file='26-appendix-e.md', anchor='**Tier 1, the Communicator.**', prefix=True,
         alt='A phone and an offline retrieval test: save a reference you may copy, record source and date, turn the network off, then open the copy and find an answer.',
         caption='Tier 0 ends with a test: can you open the reference and find what you need with the network off? Record the source and date so you know which copy you have.'),
    dict(file='v103-first-year-index.svg', builder=year_index,
         source_file='29-appendix-g.md', anchor='## Month 1: Get your bearings',
         alt='Twelve monthly themes arranged as a two-page year index, from getting your bearings and knowing your numbers to going on the record and looking back, then forward.',
         caption='A year of practice, at a scale you can sustain. Shift the months to fit your season and your life; the actions and precedent references follow below.'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate():
    OUT.mkdir(exist_ok=True)
    records = []
    for spec in SPECS:
        record = {k: spec[k] for k in ('file', 'source_file', 'alt', 'caption')}
        record.update(kind='conceptual', layout='diagram', pixels=[480, spec['builder']('print').height],
                      generator='docs/v0.10.3/figures_practical.py',
                      provenance='Original native SVG illustration drawn in code for v0.10.3 from the adjacent canonical text. No external visual reference or new numerical dataset.')
        for mode in PALETTES:
            path = IMAGES / ('print' if mode == 'print' else '') / spec['file']
            content = spec['builder'](mode).finish()
            path.write_text(content)
            assert path.read_text() == content
            record[mode + '_sha256'] = sha(path)
        record['print_file'] = 'print/' + spec['file']
        source = ROOT / 'src/lib/data/book' / spec['source_file']
        before = source.read_text()
        insertion = f"![{spec['alt']}](/book-images/{spec['file']})\n\n*{spec['caption']}*\n\n"
        if f'/book-images/{spec["file"]}' not in before:
            assert before.count(spec['anchor']) == 1
            after = before.replace(spec['anchor'], insertion + spec['anchor'], 1)
            assert after.replace(insertion, '', 1) == before
            source.write_text(after)
            assert source.read_text() == after
        else:
            assert insertion in before
        record['canonical_sha256'] = sha(source)
        record['insertion'] = insertion
        records.append(record)
    destination = OUT / 'integration.json'
    destination.write_text(json.dumps(records, indent=2) + '\n')
    assert json.loads(destination.read_text()) == records
    return records


METRICS = r'''() => {
 const svg=document.querySelector('svg'), frame=svg.getBoundingClientRect();
 const texts=[...svg.querySelectorAll('text')];
 const boxes=texts.map(t=>({text:t.textContent,...t.getBoundingClientRect().toJSON()}));
 const overlaps=[];
 for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
  const a=boxes[i],b=boxes[j];
  if(a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom)overlaps.push([a.text,b.text]);
 }
 return {labels:texts.length,min_pt:Math.min(...texts.map(t=>parseFloat(getComputedStyle(t).fontSize)*frame.width/svg.viewBox.baseVal.width*.75)),
  width_in:frame.width/96,height_in:frame.height/96,overlaps,
  outside:boxes.filter(b=>b.left<frame.left||b.right>frame.right||b.top<frame.top||b.bottom>frame.bottom).map(b=>b.text)};
}'''


def geometry(svg):
    root = ET.fromstring(svg)
    records = []
    for element in root:
        tag = element.tag.rsplit('}', 1)[-1]
        if tag == 'rect' and element.get('width') == '480':
            continue
        records.append((tag, {k: v for k, v in element.attrib.items() if k not in ('fill', 'stroke')}, element.text))
    return root.get('viewBox'), records


def proof():
    from playwright.sync_api import sync_playwright
    helper_spec = importlib.util.spec_from_file_location('legacy_geometry', ROOT / 'docs/v0.9.2/print_figures.py')
    helper = importlib.util.module_from_spec(helper_spec)
    helper_spec.loader.exec_module(helper)
    font = base64.b64encode((ROOT / 'publication/assets/fonts/JetBrainsMono-Regular.ttf').read_bytes()).decode()
    style = f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{font})}}body{{margin:0}}svg{{display:block;width:4.56in;height:auto}}"
    checks, controls = {}, {}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome')
        page = browser.new_page(viewport={'width': 600, 'height': 500}, device_scale_factor=2)

        def load(svg, mode='print'):
            page.set_content(f'<style>{style}body{{background:{"#0f172a" if mode == "screen" else "#fff"}}}</style>' + svg)
            page.evaluate('document.fonts.ready')

        def measure():
            result = page.evaluate(METRICS)
            result['path_errors'] = page.evaluate(helper.AUDIT_JS)
            result['pass'] = result['min_pt'] >= 9.5 and not any(result[k] for k in ('outside', 'overlaps', 'path_errors'))
            return result

        sample = reading_routes('print').finish()
        mutations = {
            'undersized_label': "document.querySelector('text').setAttribute('font-size','4')",
            'overlapping_labels': "const t=document.querySelectorAll('text');t[1].setAttribute('x',t[0].getAttribute('x'));t[1].setAttribute('y',t[0].getAttribute('y'))",
            'out_of_frame': "document.querySelector('text').setAttribute('x','470')",
            'path_through_label': "const t=document.querySelector('text'),b=t.getBBox(),l=document.createElementNS('http://www.w3.org/2000/svg','path');l.setAttribute('d',`M${b.x} ${b.y+b.height/2}h${b.width}`);l.setAttribute('stroke','red');t.parentNode.append(l)",
        }
        for key, mutation in mutations.items():
            load(sample)
            page.evaluate(mutation)
            controls[key] = measure()
            assert not controls[key]['pass'], key
            expected_failure = {
                'undersized_label': controls[key]['min_pt'] < 9.5,
                'overlapping_labels': bool(controls[key]['overlaps']),
                'out_of_frame': bool(controls[key]['outside']),
                'path_through_label': any('crosses' in error for error in controls[key]['path_errors']),
            }[key]
            assert expected_failure, ('Control failed for the wrong reason', key)
        for spec in SPECS:
            name = spec['file']
            checks[name] = {}
            for mode in PALETTES:
                path = IMAGES / ('print' if mode == 'print' else '') / name
                load(path.read_text(), mode)
                checks[name][mode] = measure()
                page.locator('svg').screenshot(path=str(OUT / f'{Path(name).stem}-{mode}.png'))
            checks[name]['identical_geometry'] = geometry((IMAGES / name).read_text()) == geometry((IMAGES / 'print' / name).read_text())
        browser.close()
    report = dict(figures=checks, negative_controls=controls,
                  scope='Embedded-font Chromium geometry and screenshots at 4.56 inches. Text boundaries, text overlap, sampled path intersections, screen/print geometry equality. Does not certify publication pagination or physical print output.')
    output = OUT / 'checks.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    assert json.loads(output.read_text()) == report
    failures = [(name, mode, result) for name, modes in checks.items() for mode, result in modes.items() if isinstance(result, dict) and not result['pass']]
    assert not failures, failures
    assert all(modes['identical_geometry'] for modes in checks.values())
    print(json.dumps({'figures': len(checks), 'variants': len(checks) * 2, 'minimum_pt': min(modes['print']['min_pt'] for modes in checks.values()), 'negative_controls': len(controls)}))


if __name__ == '__main__':
    generate()
    if '--proof' in sys.argv:
        proof()
