"""Build eight new editorial graphics and prove screen/print geometry.

Only chart-data.json supplies plotted values. Source and light variants use
the same geometry. Run from any directory; requires Playwright and Chrome.
"""
from pathlib import Path
import base64
import copy
from decimal import Decimal
from html import escape
import hashlib
import importlib.util
import json
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
IMAGES = ROOT / 'static/book-images'
PROOF = HERE / 'chart-proof'
DATA = json.loads((HERE / 'chart-data.json').read_text())
WIDTH = 480
DISPLAY_WIDTH = 4.56 * 96
SPEC = importlib.util.spec_from_file_location('chart_geometry', ROOT/'docs/v0.9.2/print_figures.py')
GEOMETRY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEOMETRY)
PALETTES = {
    'screen': {'bg':'#020617','ink':'#f1f5f9','muted':'#94a3b8','rule':'#334155','amber':'#f59e0b','blue':'#3b82f6'},
    'print': {'bg':'#ffffff','ink':'#0f172a','muted':'#334155','rule':'#cbd5e1','amber':'#b45309','blue':'#1d4ed8'},
}


class Figure:
    def __init__(self, chart, mode, height, title, subtitle):
        self.chart, self.colors, self.height = chart, PALETTES[mode], height
        slug = chart['id']
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" font-family="\'JetBrains Mono\',monospace" role="img" aria-labelledby="{slug}-title {slug}-desc">',
                      f'<title id="{slug}-title">{escape(title)}</title>',
                      f'<desc id="{slug}-desc">{escape(subtitle)}. {escape(" ".join(chart["limits"]))}</desc>',
                      f'<defs><pattern id="hatch-{slug}" patternUnits="userSpaceOnUse" width="8" height="8"><path d="M-2 2L2 -2M0 8L8 0M6 10L10 6" stroke="{self.colors["blue"]}" stroke-width="1"/></pattern></defs>']
        self.rect(0, 0, WIDTH, height, 'bg')
        self.text(24, 34, title, 19, 'ink', weight=600)
        self.line(24, 48, 456, 48, 'amber', 1.5)
        self.text(24, 73, subtitle)

    def text(self, x, y, value, size=13.5, color='muted', anchor='start', weight=400):
        self.parts.append(f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{self.colors[color]}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(value))}</text>')

    def lines(self, x, y, values, **kwargs):
        for i, value in enumerate(values):
            self.text(x, y+21*i, value, **kwargs)

    def line(self, x1, y1, x2, y2, color='rule', width=1, dash=None):
        self.parts.append(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{self.colors[color]}" stroke-width="{width:g}"{f" stroke-dasharray={chr(34)}{dash}{chr(34)}" if dash else ""}/>')

    def rect(self, x, y, width, height, color, stroke=None, hatch=False):
        fill = f'url(#hatch-{self.chart["id"]})' if hatch else self.colors[color]
        self.parts.append(f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" fill="{fill}"{f" stroke={chr(34)}{self.colors[stroke]}{chr(34)} stroke-width={chr(34)}2{chr(34)}" if stroke else ""}/>')

    def circle(self, x, y, r=4, color='amber', hollow=False):
        self.parts.append(f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{self.colors["bg" if hollow else color]}" stroke="{self.colors[color]}" stroke-width="2"/>')

    def footer(self, y, lines):
        self.line(24, y-16, 456, y-16)
        self.lines(24, y+7, lines)

    def finish(self):
        return '\n'.join(self.parts) + '\n</svg>\n'


def waste(c, mode):
    f = Figure(c, mode, 674, 'WHERE WASTED FOOD GOES', 'US retail, food service, households · 2019')
    f.text(24, 110, f'{c["reported_total_tons"]/1e6:.1f} million tons', 24, 'ink', weight=600)
    rows = sorted(c['rows'], key=lambda r: -r['percent'])
    for i, row in enumerate(rows):
        y = 148 + i*46
        color = 'amber' if row['label'] == 'Landfill' else 'blue'
        f.text(24, y, row['label'], color='ink')
        f.text(456, y, f'{row["percent"]:.2f}%', color=color, anchor='end', weight=600)
        f.rect(24, y+9, 432, 10, 'rule')
        f.rect(24, y+9, row['percent']/60*432, 10, color)
    f.line(24, 554, 456, 554)
    for tick in [0, 20, 40, 60]:
        x = 24+tick/60*432
        f.line(x, 551, x, 558)
        f.text(x, 580, f'{tick}%', anchor='start' if tick == 0 else 'end' if tick == 60 else 'middle')
    f.footer(606, ['EPA estimates; 2019 Wasted Food Report,', 'Table 5. Includes inedible parts.', 'Donation is net of food banks’ unusable share.'])
    return f


def land(c, mode):
    f = Figure(c, mode, 564, 'WHAT AN ACRE COSTS', 'Average US farm real estate value')
    f.text(24, 106, 'Nominal dollars per acre', color='ink')
    left, right, top, bottom = 72, 444, 142, 405
    X = lambda year: left+(year-2012)/14*(right-left)
    Y = lambda value: bottom-value/5000*(bottom-top)
    for tick in range(0, 5001, 1000):
        f.line(left, Y(tick), right, Y(tick))
        f.text(left-12, Y(tick)+5, f'{tick:,}', anchor='end')
    points = ' '.join(f'{X(r["year"]):.3f},{Y(r["value"]):.3f}' for r in c['rows'])
    f.parts.append(f'<polyline points="{points}" fill="none" stroke="{f.colors["amber"]}" stroke-width="3"/>')
    for row in c['rows']:
        f.circle(X(row['year']), Y(row['value']), 3)
    for year in [2012, 2016, 2020, 2026]:
        f.line(X(year), bottom, X(year), bottom+6)
        f.text(X(year), bottom+29, str(year), anchor='middle')
    first, last = c['rows'][0], c['rows'][-1]
    f.line(X(first['year'])+1, Y(first['value'])+6, X(first['year'])+8, Y(first['value'])+29, 'muted')
    f.text(X(first['year'])+8, Y(first['value'])+50, f'${first["value"]:,}', color='amber', weight=600)
    f.text(X(last['year'])-4, Y(last['value'])-14, f'${last["value"]:,}', color='amber', anchor='end', weight=600)
    f.footer(473, ['Survey estimates include land and buildings.', 'National averages, not local asking prices.', 'Source: USDA NASS, Land Values 2026, p. 5.'])
    return f


def access(c, mode):
    f = Figure(c, mode, 504, 'INCOME AND FOOD ACCESS', 'Share of US households food insecure · 2024')
    f.line(25, 105, 51, 105, 'muted', 2, '3 3')
    f.text(64, 110, f'National rate: {c["national_percent"]:.1f}%')
    X = lambda value: 50+value/45*394
    for i, row in enumerate(c['rows']):
        title_y = 160+i*118
        dot_y = title_y+40
        f.text(24, title_y, row['label'], color='ink')
        f.line(X(0), dot_y, X(45), dot_y)
        f.line(X(0), dot_y, X(row['percent']), dot_y, 'amber', 3)
        f.line(X(c['national_percent']), dot_y-13, X(c['national_percent']), dot_y+13, 'muted', 2, '3 3')
        f.circle(X(row['percent']), dot_y, 6)
        f.text(X(row['percent']), dot_y+30, f'{row["percent"]:.1f}%', color='amber', anchor='middle', weight=600)
    for tick in [0, 10, 20, 30, 40]:
        f.line(X(tick), 368, X(tick), 374)
        f.text(X(tick), 397, f'{tick}%', anchor='middle')
    f.footer(436, ['Selected income groups; survey estimates.', 'Association does not establish causation.', 'Source: USDA ERS, ERR-358, Table 2.'])
    return f


def power(c, mode):
    f = Figure(c, mode, 562, 'THE MACHINE’S APPETITE', 'Worldwide data-centre electricity demand')
    f.text(24, 110, 'Terawatt-hours per year', color='ink')
    top, bottom = 147, 403
    Y = lambda value: bottom-value/1000*(bottom-top)
    for tick in [0, 250, 500, 750, 1000]:
        spans = [(85, 448)]
        for row, center in zip(c['rows'], [170, 352]):
            if Y(row['value'])-42 < Y(tick) < Y(row['value'])-8:
                spans = [(a, min(b, center-34)) for a,b in spans if a < center-34] + [(max(a, center+34), b) for a,b in spans if b > center+34]
        for a,b in spans:
            if b > a:
                f.line(a, Y(tick), b, Y(tick))
        f.text(73, Y(tick)+5, str(tick), anchor='end')
    for row, x in zip(c['rows'], [120, 302]):
        forecast = row['type'] == 'forecast'
        f.rect(x, Y(row['value']), 100, bottom-Y(row['value']), 'amber', 'blue' if forecast else None, forecast)
        f.text(x+50, Y(row['value'])-15, str(row['value']), 23, 'blue' if forecast else 'amber', 'middle', 600)
        f.text(x+50, 433, str(row['year']), 18, 'ink', 'middle', 600)
        f.text(x+50, 458, 'Projection' if forecast else 'Estimate', anchor='middle')
    f.footer(499, ['All data centres, not AI alone.', '2030 is a forecast, not a meter reading.', 'Source: IEA, Key Questions on Energy and AI, 2026.'])
    return f


def forecasts(c, mode):
    f = Figure(c, mode, 554, 'FORECASTS MOVED CLOSER', 'Two surveys; aggregate 50% forecast dates')
    f.circle(32, 104, 6, 'muted', True)
    f.text(48, 109, '2022 survey')
    f.circle(263, 104, 6)
    f.text(279, 109, '2023 survey')
    X = lambda year: 72+(year-2020)/160*368
    for index, row in enumerate(c['rows']):
        y = 211+145*index
        f.text(24, y-57, row['label'], color='ink', weight=600)
        f.text(24, y-34, f'{row["shift_years"]} years earlier')
        f.line(72, y, 440, y)
        f.line(X(row['survey_2023']), y, X(row['survey_2022']), y, 'amber', 3)
        f.circle(X(row['survey_2022']), y, 6, 'muted', True)
        f.circle(X(row['survey_2023']), y, 6)
        f.text(X(row['survey_2023']), y-13, str(row['survey_2023']), color='amber', anchor='middle', weight=600)
        f.text(X(row['survey_2022']), y+28, str(row['survey_2022']), anchor='middle')
    for year in [2020, 2060, 2100, 2140, 2180]:
        f.line(X(year), 415, X(year), 422)
        f.text(X(year), 445, str(year), anchor='middle')
    f.footer(483, ['Respondent forecasts, not arrival dates.', 'The two milestones measure different things.', 'Source: Grace et al., arXiv:2401.02843.'])
    return f


def ammonia(c, mode):
    f = Figure(c, mode, 592, 'THE ENERGY IN AMMONIA', 'Gigajoules per tonne, net basis')
    f.text(24, 106, 'IEA 2021 assessment', color='ink')
    top, bottom = 142, 402
    Y = lambda value: bottom-value/45*(bottom-top)
    for tick in [0, 15, 30, 45]:
        # Leave real gaps around direct labels, not lines painted underneath.
        spans = [(67, 450)]
        for row, center in zip(c['rows'], [120, 257, 394]):
            if Y(row['value'])-42 < Y(tick) < Y(row['value'])-8:
                spans = [(a, min(b, center-32)) for a,b in spans if a < center-32] + [(max(a, center+32), b) for a,b in spans if b > center+32]
        for a,b in spans:
            if b > a:
                f.line(a, Y(tick), b, Y(tick))
        f.text(55, Y(tick)+5, str(tick), anchor='end')
    labels = [['Global', 'average'], ['Natural gas', 'best available'], ['Coal', 'best available']]
    for row, center, words in zip(c['rows'], [120, 257, 394], labels):
        benchmark = row['type'] == 'benchmark'
        f.rect(center-35, Y(row['value']), 70, bottom-Y(row['value']), 'amber', 'blue' if benchmark else None, benchmark)
        f.text(center, Y(row['value'])-14, str(row['value']), 24, 'blue' if benchmark else 'amber', 'middle', 600)
        f.lines(center, 432, words, anchor='middle')
    f.line(27, 481, 50, 481, 'amber', 4)
    f.text(63, 486, 'Average estimate')
    f.rect(267, 473, 21, 15, 'bg', 'blue', True)
    f.text(300, 486, 'Benchmarks')
    f.footer(525, ['Best available is not universal deployment.', 'These are industrial production figures.', 'Source: IEA, Ammonia Technology Roadmap.'])
    return f


def memory(c, mode):
    f = Figure(c, mode, 570, 'HOW MUCH MEMORY FOR WEIGHTS?', 'Derived arithmetic · decimal gigabytes')
    columns = [180, 283, 386]
    for bits, x in zip([4, 8, 16], columns):
        f.text(x, 128, f'{bits}-bit', 17, 'ink', 'middle', 600)
    f.line(24, 147, 456, 147)
    for p, y in [(8, 206), (70, 338)]:
        f.text(25, y-8, f'{p}B', 23, 'ink', weight=600)
        f.text(25, y+18, 'parameters')
        for bits, x in zip([4, 8, 16], columns):
            value = next(r['gb'] for r in c['rows'] if r['parameters_billion'] == p and r['bits'] == bits)
            f.text(x, y+6, str(value), 29, 'amber', 'middle', 600)
            f.text(x, y+33, 'GB', anchor='middle')
        f.line(24, y+61, 456, y+61)
    f.text(24, 439, 'GB = billions of parameters × bits / 8', color='ink')
    f.footer(474, ['Weights only. Runtime needs more.', 'Cache, context, buffers, quantization metadata,', 'and simultaneous users add to the requirement.', 'Source: Chapter 11; llama.cpp documentation.'])
    return f


def meals(c, mode):
    f = Figure(c, mode, 676, 'WHEN A MEAL FAILS', 'Illustrative premortem worksheet')
    for index, row in enumerate(c['rows']):
        y = 130+82*index
        if index < len(c['rows'])-1:
            f.line(39, y+12, 39, y+60, 'rule', 2)
        f.circle(39, y-5, 16, 'amber', True)
        f.text(39, y, str(index+1), 15, 'amber', 'middle', 600)
        f.text(72, y, row['question'], 14.5, 'ink', weight=600)
        f.text(72, y+25, row['detail'])
    f.footer(615, ['Test the handoff before making the promise.', 'Keep personal details out of the public board.', 'Source: Chapter 18, failed-meal record.'])
    return f


BUILDERS = {'waste-pathways':waste,'land-values':land,'income-food-access':access,
            'data-centre-demand':power,'forecast-shift':forecasts,'ammonia-energy':ammonia,
            'weights-memory':memory,'meal-response':meals}


def validate_data(data):
    charts = {c['id']: c for c in data['charts']}
    assert set(charts) == set(BUILDERS) and len(data['charts']) == 8
    waste_data = charts['waste-pathways']
    assert sum(Decimal(str(r['percent'])) for r in waste_data['rows']) == Decimal('100.00')
    assert abs(sum(r['tons'] for r in waste_data['rows'])-waste_data['reported_total_tons']) <= 1
    for row in waste_data['rows']:
        computed = row['tons']/waste_data['reported_total_tons']*100
        assert abs(computed-row['percent']) <= 0.0051
    assert [r['year'] for r in charts['land-values']['rows']] == list(range(2012, 2027))
    assert charts['land-values']['rows'][0]['value'] == 2520 and charts['land-values']['rows'][-1]['value'] == 4500
    assert [r['type'] for r in charts['data-centre-demand']['rows']] == ['estimate','forecast']
    for row in charts['forecast-shift']['rows']:
        assert row['survey_2022']-row['survey_2023'] == row['shift_years']
    for row in charts['weights-memory']['rows']:
        assert row['parameters_billion']*row['bits']/8 == row['gb']
    assert len(charts['meal-response']['rows']) == 6
    return {'figures':8,'data_charts':6,'derived_graphics':1,'illustrative_workflows':1,
            'waste_percentage_sum':100,'waste_source_row_rounding_difference_tons':sum(r['tons'] for r in waste_data['rows'])-waste_data['reported_total_tons']}


METRICS = r'''() => {
 const svg=document.querySelector('svg'), s=svg.getBoundingClientRect();
 const labels=[...svg.querySelectorAll('text')].map(t=>{const b=t.getBoundingClientRect();return {text:t.textContent,x:b.x,y:b.y,w:b.width,h:b.height,pt:parseFloat(getComputedStyle(t).fontSize)*s.width/svg.viewBox.baseVal.width*72/96};});
 const overlaps=[];
 for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++){
  const a=labels[i],b=labels[j];
  if(a.x<b.x+b.w-0.1&&b.x<a.x+a.w-0.1&&a.y<b.y+b.h-0.1&&b.y<a.y+a.h-0.1)overlaps.push([a.text,b.text]);
 }
 const outside=labels.filter(b=>b.x<s.x-0.1||b.y<s.y-0.1||b.x+b.w>s.right+0.1||b.y+b.h>s.bottom+0.1).map(b=>b.text);
 return {width_in:s.width/96,height_in:s.height/96,min_pt:Math.min(...labels.map(b=>b.pt)),labels:labels.length,overlaps,outside};
}'''


def main():
    validation = validate_data(DATA)
    negative = {}
    for fault in ['percentage','forecast_type']:
        broken = copy.deepcopy(DATA)
        if fault == 'percentage':
            broken['charts'][0]['rows'][0]['percent'] += 1
        else:
            next(c for c in broken['charts'] if c['id']=='data-centre-demand')['rows'][1]['type'] = 'estimate'
        try:
            validate_data(broken)
        except AssertionError:
            negative[fault] = True
        else:
            raise AssertionError('Data negative control stayed green: '+fault)
    PROOF.mkdir(parents=True, exist_ok=True)
    records = {}
    css = ''
    for face, weight in [('Regular',400),('SemiBold',600)]:
        encoded = base64.b64encode((ROOT/f'publication/assets/fonts/JetBrainsMono-{face}.ttf').read_bytes()).decode()
        css += f"@font-face{{font-family:'JetBrains Mono';font-weight:{weight};src:url(data:font/ttf;base64,{encoded});}}"
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome')
        page = browser.new_page(viewport={'width':500,'height':760},device_scale_factor=2)
        def load(svg):
            page.set_content('<!doctype html><style>'+css+'</style><body style="margin:0;background:white">'+svg.replace('<svg ',f'<svg width="{DISPLAY_WIDTH}" ',1))
            page.evaluate('() => document.fonts.ready')
        control = waste(DATA['charts'][0], 'print').finish()
        load(control)
        page.evaluate("() => {const t=document.querySelector('svg text');t.parentNode.appendChild(t.cloneNode(true));}")
        assert page.evaluate(METRICS)['overlaps'], 'Overlap negative control stayed green'
        negative['label_overlap'] = True
        load(control)
        page.evaluate("() => document.querySelector('svg text').setAttribute('font-size','1')")
        assert page.evaluate(METRICS)['min_pt'] < 8, 'Size negative control stayed green'
        negative['undersized_label'] = True
        load(control)
        page.evaluate("""() => {
          const t=document.querySelector('svg text'),b=t.getBBox();
          const line=document.createElementNS('http://www.w3.org/2000/svg','line');
          line.setAttribute('x1',b.x);line.setAttribute('x2',b.x+b.width);
          line.setAttribute('y1',b.y+b.height/2);line.setAttribute('y2',b.y+b.height/2);
          line.setAttribute('stroke','red');t.parentNode.appendChild(line);
        }""")
        assert any('crosses' in issue for issue in page.evaluate(GEOMETRY.AUDIT_JS)), 'Path-crossing negative control stayed green'
        negative['path_through_label'] = True
        for chart in DATA['charts']:
            records[chart['id']] = {}
            for mode in PALETTES:
                svg = BUILDERS[chart['id']](chart, mode).finish()
                ET.fromstring(svg)
                load(svg)
                metrics = page.evaluate(METRICS)
                metrics['path_and_box_errors'] = page.evaluate(GEOMETRY.AUDIT_JS)
                assert not metrics['overlaps'] and not metrics['outside'], (chart['id'], mode, metrics)
                assert not metrics['path_and_box_errors'], (chart['id'], mode, metrics)
                assert metrics['min_pt'] >= 8 and metrics['height_in'] <= 7, (chart['id'], mode, metrics)
                filename = 'v101-chart-'+chart['id']+'.svg'
                destination = IMAGES / ('print' if mode=='print' else '') / filename
                destination.write_text(svg)
                assert destination.read_text() == svg
                page.locator('body > svg').screenshot(path=str(PROOF/f'{chart["id"]}-{mode}.png'))
                records[chart['id']][mode] = {'path':str(destination.relative_to(ROOT)),'sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'geometry':metrics}
            print(chart['id'], records[chart['id']]['print']['geometry'], flush=True)
        browser.close()
    report = {'data_validation':validation,'negative_controls':negative,'figures':records,
              'limits':'Digital text geometry at 4.56-inch width and source arithmetic checks, not physical printer acceptance, independent replication of the source surveys, or a forecast accuracy test.'}
    (PROOF/'checks.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    main()
