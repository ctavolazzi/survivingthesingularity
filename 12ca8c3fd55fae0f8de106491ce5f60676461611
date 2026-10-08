"""Ten native SVG revisions for v0.10.2, with matching screen/print geometry.

Run: python3 docs/v0.10.2/figures_opening.py --proof
Only owned images, their print variants, and this pass's reports are written.
No registry, manuscript, rights catalogue, or whole-book build is changed.
Charts read preserved USDA transcriptions; conceptual figures have no data scale.
"""
from pathlib import Path
from html import escape
import base64
import csv
import hashlib
import importlib.util
import json
import math
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
IMAGES = ROOT / 'static/book-images'
WIDTH = 480
PALETTES = {
    'screen': dict(ink='#f1f5f9', muted='#a6b4c8', amber='#f59e0b',
                   blue='#60a5fa', paper='#0f172a', rule='#526176', wash='#263548'),
    'print': dict(ink='#17251f', muted='#4b5b52', amber='#9a4f13',
                  blue='#315f78', paper='#ffffff', rule='#a2afa6', wash='#edf0ec'),
}


class Art:
    def __init__(self, mode, height, title, desc, title_size=20):
        self.p = PALETTES[mode]
        self.height, self.title, self.desc = height, title, desc
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 {height}" role="img" aria-labelledby="title desc" font-family="JetBrains Mono, monospace">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="desc">{escape(desc)}</desc>',
        ]
        self.rect(0, 0, 480, height, fill='paper', stroke='none')
        self.text(20, 32, title, title_size, 'ink', weight=600)
        self.line(20, 48, 460, 48, 'amber', 2)

    def text(self, x, y, value, size=14, color='muted', anchor='start', weight=400):
        assert size >= 14
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{self.p[color]}" text-anchor="{anchor}" font-weight="{weight}">{escape(value)}</text>')

    def lines(self, x, y, values, size=14, color='muted', step=21, **kw):
        for i, value in enumerate(values):
            self.text(x, y + i * step, value, size, color, **kw)

    def line(self, x, y, x2, y2, color='rule', width=1, dash=None):
        self.path(f'M{x} {y}L{x2} {y2}', color, width, dash=dash)

    def path(self, d, color='ink', width=2, fill='none', dash=None, attrs=''):
        self.parts.append(f'<path d="{d}" fill="{self.p.get(fill, fill)}" stroke="{self.p.get(color, color)}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="butt"'
                          + (f' stroke-dasharray="{dash}"' if dash else '') + f' {attrs}/>')

    def rect(self, x, y, width, height, fill='none', stroke='rule', sw=1):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{self.p.get(fill, fill)}" stroke="{self.p.get(stroke, stroke)}" stroke-width="{sw}"/>')

    def circle(self, x, y, r, color='ink', width=2, fill='paper'):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{self.p.get(fill, fill)}" stroke="{self.p[color]}" stroke-width="{width}"/>')

    def down(self, x, y, y2, color='amber'):
        self.line(x, y, x, y2, color, 2)
        self.path(f'M{x-5} {y2-7}L{x} {y2}L{x+5} {y2-7}', color, 2)

    def footer(self, y, lines):
        self.line(20, y - 20, 460, y - 20)
        self.lines(20, y, lines)

    def series(self, rows, field, X, Y, color, dash=None):
        d = ' '.join(('M' if i == 0 else 'L') + f'{X(int(row["year"])):.3f} {Y(float(row[field])):.3f}' for i, row in enumerate(rows))
        self.path(d, color, 2.5, dash=dash, attrs=f'data-series="{field}" data-count="{len(rows)}"')

    def finish(self):
        return '\n'.join(self.parts) + '\n</svg>\n'


def dataset(name):
    with (ROOT / 'docs/v0.9.2/data' / name).open() as f:
        return list(csv.DictReader(line for line in f if not line.startswith('#')))


def stages(mode):
    a = Art(mode, 640, 'NINE STAGES OF THE SINGULARITY',
            'Nine speculative stages grouped into AGI, ASI, and later imagined possibilities. The fourth stage, a new social contract, is emphasized as a choice. The diagram assigns no guaranteed arrival date; stages may overlap, stall, or fail to occur.')
    a.text(20, 78, 'A speculative map, not a timetable.')
    a.text(20, 111, 'THE ERA OF AGI · STAGES 1–5', 14, 'blue', weight=600)
    for top, bottom in [(150, 158), (184, 192), (218, 226), (252, 278)]:
        a.line(40, top, 40, bottom, 'rule', 2)
    rows = [(1, 142, ['The Cash Grab']), (2, 176, ['The Panic and the Plug']),
            (3, 210, ['The Adults Step In']),
            (4, 244, ['The New Social Contract', '& the End of Labor']),
            (5, 296, ['The Primate Backlash'])]
    for number, y, words in rows:
        color = 'amber' if number == 4 else 'ink'
        a.circle(40, y-5, 13, color, 2)
        a.text(40, y, str(number), 15, color, anchor='middle', weight=600)
        a.lines(68, y, words, 15, color, step=20, weight=600 if number == 4 else 400)
    a.text(20, 336, 'THE LEAP TO ASI · STAGES 6–7', 14, 'blue', weight=600)
    for number, y, words in [(6, 365, ['The ASI Exodus']),
                              (7, 399, ['Simulation, Transhumanism,', 'the Ultimate Cure'])]:
        a.text(40, y, str(number), 15, 'ink', anchor='middle')
        a.lines(68, y, words, 15, 'ink', step=20)
    a.text(20, 461, 'SPECULATIVE APEX · STAGES 8–9', 14, 'blue', weight=600)
    for number, y, label in [(8, 490, 'The Transition to USI'), (9, 524, 'The Apex Intelligence')]:
        a.text(40, y, str(number), 15, 'ink', anchor='middle')
        a.text(68, y, label, 15, 'ink')
    a.footer(578, ['Stages may overlap, stall or not occur.',
                   'Stage 4 is the choice this book argues for.',
                   'Later stages are imagined possibilities.'])
    return a


def eighteen_days(mode):
    a = Art(mode, 636, 'PANIC TO PAPERWORK',
            'Selected events in June and July 2026. On June 12 US export controls took effect and Anthropic suspended Fable 5 and Mythos 5 worldwide. June 26 approval allowed Mythos access for a set of US organizations. Export controls were lifted June 30. Fable access returned globally July 1 while Mythos access stayed limited. Event spacing is not proportional to elapsed time.')
    a.lines(20, 78, ['Eighteen days: June 12 to June 30, 2026.',
                     'Fable 5 and Mythos 5; different access.'])
    events = [
        (135, 'JUNE 12', ['US export controls take effect.', 'Anthropic suspends both models', 'for all users worldwide.']),
        (244, 'JUNE 26', ['Government approval permits Mythos', 'access for a set of US organizations.']),
        (336, 'JUNE 30', ['Export controls are lifted.', 'Anthropic outlines new safeguards', 'and government collaboration.']),
        (446, 'JULY 1', ['Fable access returns globally.', 'Mythos access remains limited', 'to approved organizations.']),
    ]
    a.line(40, 132, 40, 448, 'rule', 2)
    for index, (y, date, words) in enumerate(events):
        a.circle(40, y-5, 7, 'amber' if index == 0 else 'blue', 2,
                 fill='amber' if index == 0 else 'paper')
        a.text(67, y, date, 16, 'ink', weight=600)
        a.lines(67, y+25, words)
    a.footer(553, ['Selected events; spacing is not elapsed time.',
                   'Source: Anthropic, Redeploying Fable 5,',
                   'June 30, updated July 1, 2026.',
                   'Stage 2 / Stage 3 is the author’s reading.'])
    return a


def horses(mode):
    rows = dataset('horses-tractors-us-farms.csv')
    a = Art(mode, 650, 'THE HERD AND THE MACHINE',
            'Two line charts of US farm counts on January 1, 1910 through 1949. Horses and mules peaked at 26.723 million in 1918 and fell to 8.274 million in 1949. Tractors increased from 1,000 in 1910 to 3.5 million in 1949. The charts use different vertical scales. 1948 and 1949 data are preliminary in USDA Statistical Bulletin 83, table 14.')
    a.text(20, 78, 'On US farms, January 1, 1910–1949.')
    a.text(20, 105, 'HORSES AND MULES · MILLIONS', 15, 'ink', weight=600)
    a.text(20, 132, '1918 peak: 26.7 million', 14, 'amber')
    X = lambda year: 55 + (year-1910)/39*386
    def panel(field, top, bottom, maximum, ticks, color):
        Y = lambda v: bottom - v/1000/maximum*(bottom-top)
        for tick in ticks:
            y = Y(tick*1000)
            a.line(55, y, 441, y, 'rule', 0.8)
            a.text(44, y+5, str(tick), anchor='end')
        a.series(rows, field, X, Y, color)
        for year in [1910, 1930, 1949]:
            a.text(X(year), bottom+24, str(year), anchor='middle')
        return Y
    Y = panel('horses_and_mules_thousands', 151, 270, 30, [0, 10, 20, 30], 'amber')
    a.circle(X(1918), Y(26723), 3.5, 'amber', 1, fill='amber')
    a.circle(X(1949), Y(8274), 3.5, 'amber', 1, fill='amber')
    a.text(20, 324, '1949: 8.3 million, under a third of the peak.')
    a.line(20, 344, 460, 344)
    a.text(20, 371, 'TRACTORS · MILLIONS', 15, 'ink', weight=600)
    Y = panel('tractors_thousands', 396, 507, 4, [0, 1, 2, 3, 4], 'blue')
    a.circle(X(1949), Y(3500), 3.5, 'blue', 1, fill='blue')
    a.text(20, 558, '1910: 1,000 → 1949: 3.5 million', 14, 'blue')
    a.footer(601, ['Separate vertical scales; 1948–49 preliminary.',
                   'Source: USDA, Statistical Bulletin 83 (1949),',
                   'table 14, p. 45. All annual values plotted.'])
    return a


def capability(mode):
    a = Art(mode, 548, 'THE GAP IS WHERE WE DECIDE',
            'Four distinct questions: whether a machine can do a task, whether it is deployed, who controls it, and whether someone can access the result without money. A vertical rail links four different symbols; no answer guarantees the next.')
    a.text(20, 78, 'Four questions. Each needs its own answer.')
    # Open rail: capability is not an automatic conveyor to access.
    a.line(56, 114, 56, 423, 'rule', 2)
    for index, (name, lines) in enumerate([
        ('CAPABILITY', ['Can a machine', 'do the task?']),
        ('DEPLOYMENT', ['Is it working', 'somewhere real?']),
        ('OWNERSHIP', ['Who controls it', 'and sets the terms?']),
        ('ACCESS', ['Can a person get the result', 'without money?']),
    ]):
        y = 126+91*index
        a.circle(56, y+13, 22, 'amber' if index<3 else 'blue')
        if index == 0:
            a.path(f'M44 {y+13}H68M56 {y+1}V{y+25}', 'amber', 2)
            a.circle(56, y+13, 7, 'amber', 1)
        elif index == 1:
            a.path(f'M45 {y+14}L53 {y+22}L68 {y+5}', 'amber', 2.5)
        elif index == 2:
            a.circle(50, y+12, 5, 'amber', 1.5)
            a.path(f'M55 {y+12}H69V{y+19}M63 {y+12}V{y+17}', 'amber', 2)
        else:
            a.circle(56, y+13, 13, 'blue', 1)
        a.text(99, y, name, 16, 'ink', weight=600)
        a.lines(99, y+26, lines)
    a.footer(493, ['A productive farm can stand beside hunger.',
                   'The terms of access are a decision.'])
    return a


def extraction(mode):
    a = Art(mode, 542, 'WHEN ATTENTION GETS DIVERTED',
            'A conceptual sequence follows time for a chosen task, a switch to another item, unfinished work, and possible time spent reorienting. A side branch shows an alert drawing attention away. Some switches help; no brain chemistry or fixed time cost is claimed.')
    a.text(20, 78, 'A possible pattern to notice in your day.')
    a.line(59, 111, 59, 448, 'blue', 2)
    for i, (y, title, details) in enumerate([
        (125, 'THE TASK YOU CHOSE', ['Time and attention available.']),
        (228, 'A SWITCH TO SOMETHING ELSE', ['Some switches help; others interrupt.']),
        (334, 'WORK LEFT WAITING', ['Returning can require reorientation.']),
        (436, 'LESS TIME ON THE TASK', ['A possible cost, not a diagnosis.']),
    ]):
        a.circle(59, y-5, 8, 'amber' if i==1 else 'blue', 2)
        a.text(86, y, title, 15, 'ink', weight=600)
        a.lines(86, y+26, details)
    # An off-ramp in the rail, with its own readable annotation above it.
    a.path('M59 173H403V205', 'amber', 1.7)
    a.path('M398 198L403 205L408 198', 'amber', 1.7)
    a.text(87, 195, 'An alert or a feed pulls you away.', 14, 'amber')
    a.footer(507, ['Conceptual illustration, not brain chemistry.'])
    return a


def focus(mode):
    a = Art(mode, 457, 'INTERRUPTED WORK',
            'An illustrative attention curve rises, drops after three interruptions, and resumes unevenly. A dashed line is a sustained-focus reference. Neither line represents measured data or establishes a recovery time, causal effect size, or interruption threshold.')
    a.text(20, 78, 'Attention on task · illustrative, not data')
    a.text(272, 111, 'Interruptions', anchor='middle')
    # No numbers on either axis: this is a conceptual pattern, not a result.
    a.path('M58 145V326H449', 'rule', 1.5)
    a.path('M443 321L449 326L443 331', 'rule', 1.5)
    a.line(58, 168, 443, 168, 'blue', 1.5, '7 5')
    for x in [191, 286, 367]:
        a.line(x, 142, x, 315, 'rule', 1, '3 5')
        a.path(f'M{x+4} 121L{x-4} 130H{x+3}L{x-4} 139', 'ink', 1.7)
    a.path('M58 318C80 303 101 186 132 171L188 170L194 310C216 292 242 223 283 200L289 309C314 294 343 248 364 231L370 313C395 296 416 280 441 269', 'amber', 2.7)
    a.text(253, 355, 'Time · not to scale', anchor='middle')
    a.line(23, 385, 52, 385, 'blue', 1.5, '7 5')
    a.text(64, 390, 'Sustained focus reference')
    a.lines(20, 422, ['No fixed recovery time or threshold.',
                      'Returning to unfinished work varies.'])
    return a


def firewall(mode):
    a = Art(mode, 585, 'THE COGNITIVE FIREWALL',
            'A suggested routine moves from incoming messages, through scheduled checks and paper notes, to a chosen task. A clock, ledger and workbench distinguish steps. Twice-daily checks are an example schedule rather than an experimentally measured optimum.')
    a.text(20, 78, 'A routine you can try, observe and adjust.')
    for y, title, details in [
        (128, 'INCOMING', ['Messages, feeds and alerts.']),
        (239, 'SCHEDULE CHECKS', ['Try two timed windows each day.', 'Adjust to the work and people involved.']),
        (353, 'MAKE NOTES', ['Put useful findings in a paper ledger.', 'Keep what the chosen task needs.']),
        (465, 'DO THE WORK', ['Welds, beds, charters:', 'return to a task you chose.']),
    ]:
        a.text(112, y, title, 16, 'ink', weight=600)
        a.lines(112, y+26, details)
    # Pictograms replace four identical boxes.
    for x, y, w in [(27, 110, 42), (43, 122, 42), (31, 135, 42)]:
        a.rect(x, y, w, 22, fill='paper', stroke='rule')
        a.line(x+7, y+8, x+w-7, y+8, 'rule')
    a.circle(57, 247, 24, 'amber', 2)
    a.path('M57 229V247L71 256', 'amber', 2)
    for angle in range(0, 360, 90):
        t=math.radians(angle)
        a.line(57+19*math.cos(t), 247+19*math.sin(t), 57+22*math.cos(t), 247+22*math.sin(t), 'rule')
    a.path('M29 328H83V384H29Z', 'blue', 2)
    a.line(39, 328, 39, 384, 'blue')
    for y in [342, 353, 364, 375]:
        a.line(46, y, 75, y, 'rule')
    a.path('M28 473H85M35 473V496M79 473V496M42 466V454H70V466', 'amber', 2)
    for top, bottom in [(167, 202), (282, 314), (395, 432)]:
        a.down(57, top, bottom, 'rule')
    a.footer(548, ['You run the queries; they do not run you.'])
    return a


def architectures(mode):
    a = Art(mode, 607, 'TWO WAYS TO TAKE IN INFORMATION',
            'Two illustrative routines contrast responding to each alert with chosen check times. Broken task segments show interruptions; two message-check windows surround a protected task period. No quantitative time scale, neurological measurement, or guaranteed cognitive benefit is implied.')
    a.text(20, 78, 'Routines, not measurements of your brain.')
    a.text(20, 117, 'RESPOND TO EACH ALERT', 16, 'ink', weight=600)
    a.text(20, 145, 'Work pauses when another item arrives.')
    for x in [97, 210, 330]:
        a.rect(x-13, 167, 26, 16, fill='paper', stroke='rule')
        a.path(f'M{x-10} 170L{x} 177L{x+10} 170', 'rule', 1)
        a.down(x, 188, 214, 'amber')
    for x, w in [(31, 51), (113, 81), (229, 85), (348, 100)]:
        a.rect(x, 227, w, 18, fill='wash', stroke='amber', sw=1.5)
    a.text(20, 277, 'Task interrupted; returning takes attention.')
    a.line(20, 307, 460, 307)
    a.text(20, 344, 'CHOOSE WHEN TO CHECK', 16, 'ink', weight=600)
    a.text(20, 372, 'Batch messages; keep notes you can use.')
    a.rect(31, 398, 86, 59, fill='wash', stroke='rule')
    a.rect(360, 398, 87, 59, fill='wash', stroke='rule')
    a.text(74, 433, 'Check', anchor='middle')
    a.text(404, 433, 'Check', anchor='middle')
    a.rect(129, 408, 219, 39, fill='paper', stroke='blue', sw=2)
    a.text(238, 433, 'Chosen task', 15, 'ink', anchor='middle')
    a.text(20, 489, 'A schedule can protect time for that task.')
    a.footer(540, ['Some interruptions are useful or urgent.',
                   'Try a routine; check whether it helps.',
                   'No guaranteed cognitive effect is implied.'])
    return a


def networks(mode):
    a = Art(mode, 616, 'TRUST NETWORK TOPOLOGIES',
            'A star graph loses its hub and the spokes connected to it. A mesh with a failed central node retains a route around the outside. Failure is shown with crosses, affected links with dashes, and surviving links with solid strokes, so the distinction does not depend on color. Actual resilience requires a working path and maintained relationships.')
    a.text(20, 83, 'ONE HUB', 16, 'ink', weight=600)
    leaves = [(143, 126), (240, 116), (337, 126), (143, 231), (337, 231)]
    for x,y in leaves:
        a.line(240, 184, x, y, 'rule', 1.6, '4 5')
    for x,y in leaves:
        a.circle(x, y, 10, 'rule', 1.8)
    a.circle(240, 184, 23, 'amber', 2)
    a.path('M227 171L253 197M253 171L227 197', 'amber', 3)
    a.text(20, 278, 'Lose this hub and its links stop working.')
    a.line(20, 302, 460, 302)
    a.text(20, 334, 'ALTERNATE PATHS', 16, 'ink', weight=600)
    pts=[(143, 376), (337, 376), (372, 439), (314, 501), (165, 501), (107, 439)]
    for i,(x,y) in enumerate(pts):
        x2,y2=pts[(i+1)%len(pts)]
        a.line(x, y, x2, y2, 'blue', 2.6)
        a.line(x, y, 240, 437, 'rule', 1.3, '4 5')
    for x,y in pts:
        a.circle(x, y, 10, 'blue', 2)
    a.circle(240, 437, 21, 'amber', 2)
    a.path('M228 425L252 449M252 425L228 449', 'amber', 3)
    a.lines(20, 550, ['A mesh can reroute if a usable path remains.',
                      'People maintain the circle and its links.',
                      'Cross: failed node. Dashes: affected links.'])
    return a


def food(mode):
    rows = dataset('food-insecurity-us.csv')
    a = Art(mode, 646, 'FOOD INSECURITY, 2001–2024',
            'Annual shares of US households: food insecurity rose from 11.1 percent in 2007 to 14.6 percent in 2008. In 2024 it was 13.7 percent and very low food security was 5.4 percent. The solid series includes the dashed very-low-food-security series; they must not be added. The shaded 2007 to 2009 period highlights the recession-era change, without assigning causality or exact recession-month boundaries.')
    a.text(20, 78, 'Share of US households · annual estimates')
    a.line(24, 105, 50, 105, 'amber', 2.5)
    a.text(62, 110, 'Food insecure during the year')
    a.line(24, 133, 50, 133, 'blue', 2.5, '5 4')
    a.text(62, 138, 'Very low food security (a subset)')
    a.text(20, 168, 'Shaded: 2007–2009 period')
    X = lambda year: 62+(year-2001)/23*379
    Y = lambda value: 407-value/16*214
    a.rect(X(2007), 193, X(2009)-X(2007), 214, fill='wash', stroke='none')
    for tick in [0, 4, 8, 12, 16]:
        y=Y(tick)
        a.line(62, y, 441, y, 'rule', .8)
        a.text(51, y+5, f'{tick}%', anchor='end')
    a.series(rows, 'food_insecure_pct', X, Y, 'amber')
    a.series(rows, 'very_low_food_security_pct', X, Y, 'blue', '5 4')
    for year in [2001, 2007, 2013, 2019, 2024]:
        a.text(X(year), 434, str(year), anchor='middle')
    a.lines(20, 474, ['2007: 11.1% food insecure',
                      '2008: 14.6%, about one-third higher',
                      '2024: 13.7%, 18.3 million households',
                      '2024: 5.4% with very low food security'], color='ink', step=23)
    a.footer(588, ['Source: USDA Economic Research Service,',
                   'food-security trends, 2001–2024.',
                   'Current Population Survey supplement.'])
    return a


BUILDERS = {
    'intro-nine-stages.svg': stages,
    'ch02-eighteen-days.svg': eighteen_days,
    'ch05-horses-tractors.svg': horses,
    'ch06-capability-access.svg': capability,
    'ch08-cognitive-extraction.svg': extraction,
    'ch08-focus-recovery.svg': focus,
    'ch08-firewall-pipeline.svg': firewall,
    'ch08-info-architectures.svg': architectures,
    'ch08-star-vs-mesh.svg': networks,
    'intro-food-insecurity.svg': food,
}

RECOMMENDATIONS = {
    'intro-nine-stages.svg': ('A01, L01', 'Removed a guaranteed 2027 ASI leap and claims about outgrowing physics. Retained all nine named stages and emphasized Stage 4 as a proposal.',
        'A speculative map of nine stages, grouped into AGI, ASI, and later imagined possibilities. Stage 4, a new social contract, is emphasized as a choice. Stages may overlap, stall, or fail to occur.',
        'A speculative map, not a timetable. The fourth stage is the choice this book argues for; later stages are imagined possibilities.'),
    'ch02-eighteen-days.svg': ('L01; access scope', 'Replaced the crowded horizontal timeline with dated vertical milestones. July 1 global restoration applies to Fable, while Mythos remains limited. June 26 approval is specific to Mythos access. Removed the side quotation about another model; it remains in prose. Stage labels are explicitly the author’s interpretation.',
        'Four dated events: June 12 export controls and worldwide suspension of Fable 5 and Mythos 5; June 26 approval for Mythos access by a set of US organizations; June 30 lifting of export controls; July 1 global return of Fable, with Mythos still limited to approved organizations. Spacing is not proportional to elapsed time.',
        'Eighteen days from the June 12 export controls to their lifting on June 30. Access to the two models still differed. Selected events from Anthropic’s June 30 account, updated July 1; Stage 2 and Stage 3 are the author’s interpretation.'),
    'ch05-horses-tractors.svg': ('L01', 'Replotted every preserved annual observation in two narrow panels, with explicit units and separate vertical scales. Added January 1 reference date; retained preliminary-data qualification.',
        'Two line charts show horses and mules on US farms peaking at 26.7 million in 1918 and falling to 8.3 million in 1949, while tractors rise from 1,000 in 1910 to 3.5 million in 1949. The vertical scales differ; all annual values are plotted.',
        'US farm counts on January 1, 1910–1949. Separate vertical scales; 1948 and 1949 figures were preliminary. Source: USDA Statistical Bulletin 83 (1949), table 14, p. 45.'),
    'ch06-capability-access.svg': ('L01', 'Recomposed four questions vertically using distinct symbols. Ownership refers to terms, including price, and access explicitly refers to the result.',
        'Four questions ask whether a machine can do a task, whether it is deployed, who sets its terms, and whether someone can receive the result without money. A rail connects distinct symbols without promising automatic progress.',
        'Capability, deployment, ownership and access are separate questions. A productive farm can stand beside hunger.'),
    'ch08-cognitive-extraction.svg': ('L01', 'Recomposed an existing qualified conceptual sequence with an attention off-ramp. Preserved possible rather than guaranteed costs and the boundary against brain-chemistry claims.',
        'A rail follows time for a chosen task, switching away, unfinished work, and a possible loss of task time. An off-ramp marks an alert or feed. Some switches help; returning can require reorientation.',
        'A possible pattern to notice in your own day. Conceptual illustration, not a diagnosis or a model of brain chemistry.'),
    'ch08-focus-recovery.svg': ('L01', 'Recomposed the qualitative chart at print width. Kept a dashed reference, varied returns after interruptions, and explicit absence of measured values or fixed recovery times.',
        'An illustrative attention curve rises, drops after three interruptions, and resumes unevenly. A dashed sustained-focus reference and unnumbered axes make this a conceptual sketch, not measured data.',
        'One possible pattern of interrupted work. The drawing gives no fixed recovery time, interruption threshold, or measured effect size.'),
    'ch08-firewall-pipeline.svg': ('L01', 'Replaced four tiny horizontal boxes with a vertical icon-led routine. Scheduled checks are a trial to adjust rather than a measured optimum; retained paper notes and chosen physical work.',
        'Messages, a clock, a paper ledger and a workbench show a suggested routine: receive information, schedule checks, make useful notes, and return to chosen work.',
        'A routine to try, observe and adjust. Two timed windows each day are an example schedule, not a measured optimum.'),
    'ch08-info-architectures.svg': ('A02, L01', 'Removed guaranteed anxiety, memory, executive-function and surplus-energy outcomes. Contrasted observable checking routines and protected task time; acknowledged useful or urgent interruptions.',
        'Two unscaled task strips compare responding to each incoming alert with choosing message-check times. The first task is fragmented; two check windows surround a chosen task in the second. No cognitive benefit is guaranteed.',
        'Routines, not measurements of your brain. Some interruptions are useful or urgent. Try a schedule and check whether it helps.'),
    'ch08-star-vs-mesh.svg': ('L01; hub-label collision', 'Stacked star and mesh graphs; removed the hub label previously crossed by a failure mark. Showed the same central-node failure in both examples and encoded affected versus surviving links with dash patterns as well as color.',
        'A star loses its crossed-out hub and its dashed links. A mesh with a crossed-out central node retains a solid route around the outside. Rerouting requires a usable path and maintained relationships.',
        'A mesh can reroute only if a usable path remains. Crosses mark failed nodes; dashed links are affected by that failure. People still maintain the circle and its connections.'),
    'intro-food-insecurity.svg': ('A14; label floor', 'Replaced the causal jobs-to-dinner headline with the observed series title. Preserved every USDA observation and the 2024 callouts. Explicitly identified very low food security as a subset, not an additive series. Shading marks the 2007–2009 period, not exact recession months.',
        'Annual US household food insecurity, 2001–2024, shown as a solid line, with its very-low-food-security subset dashed. Food insecurity rises from 11.1% in 2007 to 14.6% in 2008; in 2024 the two rates are 13.7% and 5.4%. Shading marks the 2007–2009 period.',
        'Food insecurity rose sharply in 2008. These household survey estimates show a historical pattern, not a causal test of job loss. Very low food security is included within food insecurity. USDA Economic Research Service, 2001–2024.'),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_chart_data():
    """Coordinate arithmetic is checked against every preserved CSV observation."""
    report = {}
    for name, csv_name, fields in [
        ('ch05-horses-tractors.svg', 'horses-tractors-us-farms.csv', ['horses_and_mules_thousands', 'tractors_thousands']),
        ('intro-food-insecurity.svg', 'food-insecurity-us.csv', ['food_insecure_pct', 'very_low_food_security_pct']),
    ]:
        rows = dataset(csv_name)
        svg = ET.fromstring((IMAGES/name).read_text())
        series = {el.attrib['data-series']: el for el in svg.iter() if 'data-series' in el.attrib}
        assert set(series) == set(fields)
        import re
        def validate_points(points, field):
            assert len(points)==len(rows)
            for (x,y), row in zip(points, rows):
                if name.startswith('ch05'):
                    year=1910+(x-55)/386*39
                    if field.startswith('horses'):
                        value=(270-y)/119*30000
                    else:
                        value=(507-y)/111*4000
                    value_tolerance=.13  # at most half a 0.001-unit path-coordinate rounding step
                else:
                    year=2001+(x-62)/379*23
                    value=(407-y)/214*16
                    value_tolerance=.00004
                assert abs(year-int(row['year']))<.00006, (name, field, year, row)
                assert abs(value-float(row[field]))<=value_tolerance, (name, field, value, row)
        controls={}
        for field in fields:
            assert int(series[field].attrib['data-count']) == len(rows)
            points=[tuple(map(float, point)) for point in re.findall(r'[ML]([\d.]+) ([\d.]+)', series[field].attrib['d'])]
            bad_points=[(points[0][0], points[0][1]+5), *points[1:]]
            try:
                validate_points(bad_points, field)
            except AssertionError:
                controls[field]=True
            else:
                raise AssertionError('A deliberately displaced data point escaped detection')
            validate_points(points, field)
        report[name] = {'csv': 'docs/v0.9.2/data/'+csv_name, 'sha256': sha(ROOT/'docs/v0.9.2/data'/csv_name),
                        'observations_per_series': len(rows), 'fields': fields,
                        'negative_control_displaced_first_point_detected':controls,
                        'method': 'Every plotted path coordinate is read back, transformed back into its year and data value, and compared with the corresponding CSV row within coordinate-rounding tolerance. No smoothing or omitted years.'}
    return report


METRICS = r'''() => {
 const svg=document.querySelector('svg'), frame=svg.getBoundingClientRect();
 const ts=[...svg.querySelectorAll('text')];
 const boxes=ts.map(t=>({text:t.textContent,...t.getBoundingClientRect().toJSON()}));
 const overlaps=[];
 for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
  const a=boxes[i],b=boxes[j];
  if(a.left<b.right && b.left<a.right && a.top<b.bottom && b.top<a.bottom)overlaps.push([a.text,b.text]);
 }
 return {labels:ts.length,min_pt:Math.min(...ts.map(t=>parseFloat(getComputedStyle(t).fontSize)*frame.width/svg.viewBox.baseVal.width*.75)),
   min_svg_font:Math.min(...ts.map(t=>parseFloat(getComputedStyle(t).fontSize))),
   width_in:frame.width/96,height_in:frame.height/96,overlaps,
   outside:boxes.filter(b=>b.left<frame.left || b.right>frame.right || b.top<frame.top || b.bottom>frame.bottom).map(b=>b.text)};
}'''


def proof():
    from playwright.sync_api import sync_playwright
    out=HERE/'art-opening-proof'
    out.mkdir(exist_ok=True)
    spec=importlib.util.spec_from_file_location('legacy_geometry',ROOT/'docs/v0.9.2/print_figures.py')
    geometry=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geometry)
    font=base64.b64encode((ROOT/'publication/assets/fonts/JetBrainsMono-Regular.ttf').read_bytes()).decode()
    style=f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{font})}}body{{margin:0}}svg{{display:block;width:4.56in;height:auto}}"
    checks, controls = {}, {}
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='chrome')
        page=browser.new_page(viewport={'width':520,'height':720},device_scale_factor=1)
        def load(svg, mode='print'):
            page.set_content(f'<style>{style}body{{background:{PALETTES[mode]["paper"]}}}</style>'+svg)
            page.evaluate('document.fonts.ready')
        sample=capability('print').finish()
        load(sample)
        page.evaluate("document.querySelector('text').setAttribute('font-size','4')")
        bad=page.evaluate(METRICS)
        assert bad['min_pt']<8
        controls['undersized_label']={'detected':True,'min_pt':bad['min_pt']}
        page.locator('svg').screenshot(path=str(out/'negative-control-undersized.png'))
        load(sample)
        page.evaluate("const ts=document.querySelectorAll('text');ts[1].setAttribute('x',ts[0].getAttribute('x'));ts[1].setAttribute('y',ts[0].getAttribute('y'))")
        bad=page.evaluate(METRICS)
        assert bad['overlaps']
        controls['overlapping_labels']={'detected':True,'pairs':bad['overlaps']}
        load(sample)
        page.evaluate("document.querySelector('text').setAttribute('x','470')")
        bad=page.evaluate(METRICS)
        assert bad['outside']
        controls['out_of_frame']={'detected':True,'labels':bad['outside']}
        load(sample)
        page.evaluate("const t=document.querySelector('text'),b=t.getBBox(),l=document.createElementNS('http://www.w3.org/2000/svg','path');l.setAttribute('d',`M${b.x} ${b.y+b.height/2}h${b.width}`);l.setAttribute('stroke','red');t.parentNode.append(l)")
        errors=page.evaluate(geometry.AUDIT_JS)
        assert any('crosses' in x for x in errors)
        controls['path_through_label']={'detected':True,'errors':errors}
        for name in BUILDERS:
            checks[name]={}
            for mode in PALETTES:
                path=IMAGES/('print' if mode=='print' else '')/name
                load(path.read_text(),mode)
                measure=page.evaluate(METRICS)
                measure['path_errors']=page.evaluate(geometry.AUDIT_JS)
                measure['file_sha256']=sha(path)
                page.locator('svg').screenshot(path=str(out/f'{Path(name).stem}-{mode}.png'))
                checks[name][mode]=measure
        browser.close()
    report={'figures':checks,'negative_controls':controls,
            'limits':'Browser bounds and sampled path intersections at 4.56-inch width, using the publication font. Screenshots are browser renders, not a whole-book PDF proof or a guarantee of physical printer contrast.'}
    target=out/'checks.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    assert json.loads(target.read_text())==report
    failures={n:{m:r for m,r in modes.items() if r['min_svg_font']<14 or r['min_pt']<8 or r['overlaps'] or r['outside'] or r['path_errors']} for n,modes in checks.items()}
    failures={n:r for n,r in failures.items() if r}
    if failures:
        print(json.dumps(failures,indent=2))
        raise SystemExit('Opening art proof has failures; inspect checks.json.')
    print(json.dumps({'figures':len(checks),'variants':sum(map(len,checks.values())),
                      'min_print_pt':min(r['print']['min_pt'] for r in checks.values()),
                      'negative_controls':{k:v['detected'] for k,v in controls.items()}}))


def main():
    baseline_path=HERE/'art-opening-baseline.json'
    if not baseline_path.exists():
        baseline={name:{'source_sha256':sha(IMAGES/name),'print_sha256':sha(IMAGES/'print'/name),
                        'source_viewBox':ET.fromstring((IMAGES/name).read_text()).attrib['viewBox']} for name in BUILDERS}
        baseline_path.write_text(json.dumps(baseline,indent=2)+'\n')
    baseline=json.loads(baseline_path.read_text())
    report={'generator':'docs/v0.10.2/figures_opening.py','figures':{},'source_limits':{
        'charts':'Preserved USDA CSV transcriptions and their source metadata. No new dataset retrieval or numerical revision in this pass.',
        'timeline':'Anthropic is the primary source for its suspensions/restorations and account of approvals; this is not independent verification of government motives or safety efficacy.',
        'concepts':'Authored conceptual diagrams grounded in the revised chapters. No invented measurements or guaranteed outcomes.'},
        'sources':[{'url':'https://www.anthropic.com/news/redeploying-fable-5','checked':'2026-09-28','use':'June 12 suspension, June 26 limited approval, June 30 lifting and July 1 Fable restoration; Mythos access remains limited.'},
                   {'path':'docs/v0.9.2/data/horses-tractors-us-farms.csv','use':'All 40 annual observations in both series, in thousands; labels convert to millions.'},
                   {'path':'docs/v0.9.2/data/food-insecurity-us.csv','use':'All 24 annual household rates in both series.'}]}
    for name,builder in BUILDERS.items():
        for mode in PALETTES:
            art=builder(mode)
            target=IMAGES/('print' if mode=='print' else '')/name
            content=art.finish()
            ET.fromstring(content)
            target.write_text(content)
            assert target.read_text()==content
        audit,semantic,alt,caption=RECOMMENDATIONS[name]
        report['figures'][name]={'audit_items':audit,'semantic_changes':semantic,'composition':'480-unit print-first reflow with labels at least 14 units and identical geometry in both palettes.',
            'dimensions':[480,art.height],'minimum_font_svg_units':14,
            'before':baseline[name],'after':{'source_sha256':sha(IMAGES/name),'print_sha256':sha(IMAGES/'print'/name)},
            'print_file':'print/'+name,'recommended_alt':alt,'recommended_caption':caption,
            'provenance':'Native vector redraw by Codex; derived from the existing authored diagram and revised canonical prose. No generated raster or external artwork.'}
    report['data_preservation']=verify_chart_data()
    target=HERE/'art-opening-changes.json'
    target.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    assert json.loads(target.read_text())==report
    if '--proof' in sys.argv:
        proof()
    else:
        print('Wrote 10 screen SVGs, 10 print SVGs and change metadata. Run --proof for browser checks.')


if __name__ == '__main__':
    main()
