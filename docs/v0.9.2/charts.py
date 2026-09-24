"""Generate the v0.9.2 data charts as SVG in the book's figure house style.

Every chart is drawn from a committed CSV in docs/v0.9.2/data/ (or from
Appendix D), so each number can be traced and each chart rebuilt:

    python3 docs/v0.9.2/charts.py

House style (matches the existing figures): dark card #020617, monospace,
uppercase letter-spaced title, #f59e0b brand rule. Data colors #d97706 and
#3b82f6 were validated with the dataviz skill's validator on the #020617
surface (dark mode): lightness band, chroma, CVD and normal-vision separation,
and contrast all pass. Every series is also named in text, so identity never
rests on color alone, which matters for the grayscale print interior.
"""
import csv
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'static' / 'book-images'

BG, CARD, EDGE = '#020617', '#0f172a', '#1e293b'
INK, MUTED, FAINT = '#f1f5f9', '#94a3b8', '#475569'
BRAND = '#f59e0b'
AMBER, BLUE = '#d97706', '#3b82f6'
FONT = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace"


def esc(s):
    return html.escape(str(s), quote=True)


def read_csv(name):
    rows = [r for r in csv.reader(l for l in open(HERE / 'data' / name) if not l.startswith('#'))]
    return rows[0], rows[1:]


def frame(w, h, title, subtitle, body, source):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}" role="img" aria-label="{esc(title.title())}">\n'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{BG}" stroke="{EDGE}" stroke-width="2"/>\n'
            f'<text x="40" y="46" font-size="19" letter-spacing="2" fill="{INK}">{esc(title)}</text>\n'
            f'<line x1="40" y1="60" x2="{min(40 + len(title) * 12.2, w - 40):.0f}" y2="60" stroke="{BRAND}" stroke-width="2"/>\n'
            f'<text x="40" y="82" font-size="12.5" fill="{MUTED}">{esc(subtitle)}</text>\n'
            f'{body}'
            f'<text x="40" y="{h-22}" font-size="10.5" fill="{MUTED}">{esc(source)}</text>\n'
            '</svg>\n')


def polyline(pts, color, width=2.5):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>\n'


def horses_tractors():
    _, rows = read_csv('horses-tractors-us-farms.csv')
    years = [int(r[0]) for r in rows]
    horses = [int(r[1]) / 1000 for r in rows]
    tractors = [int(r[2]) / 1000 for r in rows]
    W, H = 900, 620
    x0, x1 = 110, 840
    X = lambda y: x0 + (y - 1910) / (1949 - 1910) * (x1 - x0)
    body = ''
    panels = [('HORSES AND MULES ON FARMS', horses, AMBER, 132, 318, 30, [0, 10, 20, 30]),
              ('TRACTORS ON FARMS', tractors, BLUE, 368, 518, 4, [0, 1, 2, 3, 4])]
    for label, series, color, top, bottom, ymax, ticks in panels:
        Y = lambda v: bottom - v / ymax * (bottom - top)
        body += f'<text x="{x0}" y="{top-14}" font-size="12.5" font-weight="600" fill="{INK}">{label}, MILLIONS</text>\n'
        for t in ticks:
            body += f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x1}" y2="{Y(t):.1f}" stroke="{EDGE}" stroke-width="1"/>\n'
            body += f'<text x="{x0-12}" y="{Y(t)+4:.1f}" font-size="11" fill="{MUTED}" text-anchor="end">{t}</text>\n'
        pts = [(X(y), Y(v)) for y, v in zip(years, series)]
        area = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        body += f'<polygon points="{X(1910):.1f},{Y(0):.1f} {area} {X(1949):.1f},{Y(0):.1f}" fill="{color}" fill-opacity="0.16"/>\n'
        body += polyline(pts, color)
        if series is horses:
            px, py = X(1918), Y(26.723)
            body += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{color}" stroke="{BG}" stroke-width="2"/>\n'
            body += f'<text x="{px+10:.1f}" y="{py-10:.1f}" font-size="12" fill="{INK}">1918 peak: 26.7 million</text>\n'
            ex, ey = X(1949), Y(8.274)
            body += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5" fill="{color}" stroke="{BG}" stroke-width="2"/>\n'
            body += f'<text x="{ex-10:.1f}" y="{ey-14:.1f}" font-size="12" fill="{INK}" text-anchor="end">1949: 8.3 million, under a third</text>\n'
        else:
            ex, ey = X(1949), Y(3.5)
            body += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5" fill="{color}" stroke="{BG}" stroke-width="2"/>\n'
            body += f'<text x="{ex-10:.1f}" y="{ey-12:.1f}" font-size="12" fill="{INK}" text-anchor="end">1949: 3.5 million</text>\n'
            sx, sy = X(1910), Y(0.001)
            body += f'<text x="{sx+6:.1f}" y="{sy-10:.1f}" font-size="12" fill="{INK}">1910: about 1,000</text>\n'
    for y in range(1910, 1950, 5):
        body += f'<text x="{X(y):.1f}" y="540" font-size="11" fill="{MUTED}" text-anchor="middle">{y}</text>\n'
    body += f'<text x="{X(1945):.1f}" y="560" font-size="11" fill="{MUTED}" text-anchor="middle">(1948 and 1949 preliminary)</text>\n'
    return frame(W, H, 'THE HERD AND THE MACHINE', 'On American farms, 1910 to 1949. The horse didn\'t get worse. The ledger changed.',
                 body, 'Source: USDA, Farm Production Practices, Costs, and Returns, Statistical Bulletin 83 (1949), table 14.')


def food_insecurity():
    _, rows = read_csv('food-insecurity-us.csv')
    years = [int(r[0]) for r in rows]
    fi = [float(r[1]) for r in rows]
    vl = [float(r[2]) for r in rows]
    W, H = 900, 560
    x0, x1, top, bottom = 110, 840, 130, 450
    X = lambda y: x0 + (y - 2001) / (2024 - 2001) * (x1 - x0)
    Y = lambda v: bottom - v / 16 * (bottom - top)
    body = ''
    for t in (0, 4, 8, 12, 16):
        body += f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x1}" y2="{Y(t):.1f}" stroke="{EDGE}" stroke-width="1"/>\n'
        body += f'<text x="{x0-12}" y="{Y(t)+4:.1f}" font-size="11" fill="{MUTED}" text-anchor="end">{t}%</text>\n'
    # recession band: December 2007 to June 2009 (NBER), drawn over the 2008 and 2009 data years
    body += f'<rect x="{X(2007.5):.1f}" y="{top}" width="{X(2009.5)-X(2007.5):.1f}" height="{bottom-top}" fill="{FAINT}" fill-opacity="0.25"/>\n'
    body += f'<text x="{X(2008.5):.1f}" y="{bottom-10}" font-size="11" fill="{MUTED}" text-anchor="middle">RECESSION</text>\n'
    body += polyline([(X(y), Y(v)) for y, v in zip(years, fi)], AMBER)
    body += polyline([(X(y), Y(v)) for y, v in zip(years, vl)], BLUE)
    for y, v, c in ((2007, 11.1, AMBER), (2008, 14.6, AMBER), (2024, 13.7, AMBER), (2024, 5.4, BLUE)):
        body += f'<circle cx="{X(y):.1f}" cy="{Y(v):.1f}" r="5" fill="{c}" stroke="{BG}" stroke-width="2"/>\n'
    body += f'<text x="{X(2007)-8:.1f}" y="{Y(11.1)+20:.1f}" font-size="12" fill="{INK}" text-anchor="end">2007: 11.1%</text>\n'
    body += f'<text x="{X(2008)+10:.1f}" y="{Y(14.6)-12:.1f}" font-size="12" fill="{INK}">2008: 14.6%, in one year</text>\n'
    body += f'<text x="{X(2024)-10:.1f}" y="{Y(13.7)-14:.1f}" font-size="12" fill="{INK}" text-anchor="end">2024: 13.7%, 18.3 million households</text>\n'
    body += f'<text x="{X(2024)-10:.1f}" y="{Y(5.4)-14:.1f}" font-size="12" fill="{INK}" text-anchor="end">very low food security: 5.4%</text>\n'
    body += f'<text x="{X(2001)+4:.1f}" y="{Y(8.8):.1f}" font-size="12" fill="{MUTED}">food insecure, any time in the year</text>\n'
    body += f'<text x="{X(2003):.1f}" y="{Y(3.5)-14:.1f}" font-size="12" fill="{MUTED}">very low food security</text>\n'
    for y in range(2001, 2025, 3):
        body += f'<text x="{X(y):.1f}" y="{bottom+22}" font-size="11" fill="{MUTED}" text-anchor="middle">{y}</text>\n'
    body += f'<text x="{x0}" y="{top-18}" font-size="12.5" font-weight="600" fill="{INK}">SHARE OF US HOUSEHOLDS</text>\n'
    return frame(W, H, 'WHEN THE JOBS GO, DINNER GOES', 'Food insecurity jumped by a third in the year the recession took the jobs, and took a decade to fall back.',
                 body, 'Source: USDA Economic Research Service, food security trends, 2001 to 2024 (Current Population Survey supplement).')


PRECEDENTS_MODERN = [  # (id, name, start, end, approximate)
    ('P-01', 'The Reading Rage', 1770, 1830, True),
    ('P-07', 'The Horse and the Ledger', 1786, 1949, True),
    ('P-20', 'An Argument in Circulation', 1776, 1776, False),
    ('P-09', 'The Frame-Breakers', 1811, 1816, False),
    ('P-15', 'One Hundred Sixty Acres', 1862, 1862, False),
    ('P-04', 'The Red Flag', 1865, 1865, False),
    ('P-02', 'The Voice at the Fair', 1876, 1876, False),
    ('P-03', 'One Million Years, Give or Take', 1903, 1903, False),
    ('P-16', 'The House That Came by Mail', 1908, 1940, True),
    ('P-10', 'The Robot in the Orchestra Pit', 1929, 1948, False),
    ('P-11', 'Torches of Freedom', 1929, 1929, False),
    ('P-19', 'Organizing the Harvest', 1943, 1944, False),
    ('P-14', 'Quartz and the Assembly Line', 1962, 1983, False),
    ('P-21', 'Access to Tools', 1968, 1968, False),
    ('P-17', 'The Graveyard of the Unconvinced', 1975, 2013, False),
    ('P-23', 'The Day Care Stopped Costing Money', 1942, 1948, False),
    ('P-24', 'What the Forecast Missed', 1993, 1995, False),
    ('P-22', 'The Apocalypse That Ran On Time', 1999, 2004, False),
    ('P-18', 'The Mirror Twin', 2000, 2009, True),
]
PRECEDENTS_DEEP = [
    ('P-08', 'The Grain Trap', 'c. 9500 to 6000 BC'),
    ('P-12', 'The Networks Behind the Bronze', '14th to 12th c. BC'),
    ('P-05', 'The Court and the Fleet', '1405 to 1433'),
    ('P-13', 'The Abbot and the Press', '1492 to 1494'),
    ('P-06', 'The Great Demotion', '1543'),
]


def precedent_timeline():
    order = sorted(PRECEDENTS_MODERN, key=lambda p: (p[2], p[3]))
    W = 900
    row = 23
    top = 150
    H = top + len(order) * row + 60 + 40 + len(PRECEDENTS_DEEP) * row + 70
    lx, x0, x1 = 40, 380, 850
    X = lambda y: x0 + (y - 1750) / (2025 - 1750) * (x1 - x0)
    body = f'<text x="{lx}" y="{top-30}" font-size="12.5" font-weight="600" fill="{INK}">1750 TO TODAY</text>\n'
    for y in (1750, 1800, 1850, 1900, 1950, 2000, 2025):
        body += f'<line x1="{X(y):.1f}" y1="{top-14}" x2="{X(y):.1f}" y2="{top + len(order)*row - 6}" stroke="{EDGE}" stroke-width="1"/>\n'
        body += f'<text x="{X(y):.1f}" y="{top-20}" font-size="11" fill="{MUTED}" text-anchor="middle">{y}</text>\n'
    for i, (pid, name, a, b, approx) in enumerate(order):
        cy = top + i * row + 6
        body += f'<text x="{lx}" y="{cy+4}" font-size="11.5" fill="{MUTED}">{pid}</text>\n'
        body += f'<text x="{lx+46}" y="{cy+4}" font-size="11.5" fill="{INK}">{esc(name)}</text>\n'
        if b - a >= 2:
            dash = ' stroke-dasharray="5 4"' if approx else ''
            body += f'<line x1="{X(a):.1f}" y1="{cy}" x2="{X(b):.1f}" y2="{cy}" stroke="{AMBER}" stroke-width="6" stroke-linecap="round"{dash}/>\n'
        else:
            body += f'<circle cx="{X(a):.1f}" cy="{cy}" r="5" fill="{AMBER}" stroke="{BG}" stroke-width="2"/>\n'
    ly = top + len(order) * row + 20
    body += f'<line x1="{x0}" y1="{ly}" x2="{x0+30}" y2="{ly}" stroke="{AMBER}" stroke-width="6" stroke-linecap="round" stroke-dasharray="5 4"/>\n'
    body += f'<text x="{x0+40}" y="{ly+4}" font-size="11" fill="{MUTED}">dashed: an approximate span, from the chapter\'s documents</text>\n'
    dy = ly + 50
    body += f'<text x="{lx}" y="{dy}" font-size="12.5" font-weight="600" fill="{INK}">DEEP HISTORY</text>\n'
    for i, (pid, name, when) in enumerate(PRECEDENTS_DEEP):
        cy = dy + 24 + i * row
        body += f'<text x="{lx}" y="{cy}" font-size="11.5" fill="{MUTED}">{pid}</text>\n'
        body += f'<text x="{lx+46}" y="{cy}" font-size="11.5" fill="{INK}">{esc(name)}</text>\n'
        body += f'<text x="{x0}" y="{cy}" font-size="11.5" fill="{AMBER}">{esc(when)}</text>\n'
    return frame(W, H, 'THE LEDGER ON ONE PAGE', 'Twenty-four times people watched a new capability arrive, or a new rule, and reprice their world.',
                 body, 'Dates from Appendix D; sources for every entry in Appendix B.')


RUNGS = [  # (number, rung, proof it's possible)
    (1, 'Count what\'s wasted and who\'s hungry', 'California SB 1383 recovery targets'),
    (2, 'Feed everyone who asks', 'France, 2016: no destroying edible food'),
    (3, 'Make the meal a public service', 'California universal school meals, 2022'),
    (4, 'Take the ground off the market', 'community land trusts, 99-year leases'),
    (5, 'Own the machines together', 'rural electric co-ops, from 1936'),
    (6, 'Stop letting a score decide who survives', 'NYC right to counsel, 2017'),
    (7, 'Widen the floor', 'NHS, 1948; Universal Basic Services'),
    (8, 'Put it on the scoreboard, in public', 'holds the ladder together'),
    (9, 'Keep the market above the floor', 'money stays; it becomes optional'),
]
BANDS = [(1, 3, 'FEED PEOPLE NOW'), (4, 6, 'CHANGE WHO OWNS AND DECIDES'), (7, 9, 'WIDEN THE FLOOR')]


def conversion_ladder():
    W, row, top = 900, 52, 112
    H = top + len(RUNGS) * row + 70
    body = ''
    y_of = lambda n: top + (len(RUNGS) - n) * row  # rung 1 at the bottom
    for a, b, label in BANDS:
        y0, y1 = y_of(b), y_of(a) + row - 8
        body += f'<rect x="40" y="{y0}" width="6" height="{y1-y0}" rx="3" fill="{BRAND}"/>\n'
        body += f'<text x="58" y="{(y0+y1)/2+4:.0f}" font-size="11" letter-spacing="1" fill="{MUTED}">{label}</text>\n'
    for n, rung, proof in RUNGS:
        y = y_of(n)
        held = n >= 8
        stroke = BLUE if held else AMBER
        body += f'<rect x="300" y="{y}" width="560" height="{row-12}" rx="8" fill="{CARD}" stroke="{stroke}" stroke-width="2"/>\n'
        body += f'<text x="322" y="{y+26}" font-size="16" font-weight="600" fill="{INK}">{n}</text>\n'
        body += f'<text x="352" y="{y+17}" font-size="13" font-weight="600" fill="{INK}">{esc(rung)}</text>\n'
        body += f'<text x="352" y="{y+33}" font-size="11" fill="{MUTED}">{esc(proof)}</text>\n'
    ly = top + len(RUNGS) * row + 8
    body += f'<rect x="300" y="{ly}" width="18" height="12" rx="3" fill="{CARD}" stroke="{AMBER}" stroke-width="2"/>\n'
    body += f'<text x="326" y="{ly+11}" font-size="11" fill="{MUTED}">already done somewhere</text>\n'
    body += f'<rect x="520" y="{ly}" width="18" height="12" rx="3" fill="{CARD}" stroke="{BLUE}" stroke-width="2"/>\n'
    body += f'<text x="546" y="{ly+11}" font-size="11" fill="{MUTED}">how you hold it together</text>\n'
    return frame(W, H, 'THE LADDER', 'Nine rungs, from the bottom up. Start with food. Climb as far as your town can hold.',
                 body, 'Chapter 19. Sources for every rung in the chapter and in Appendix B.')


def eighteen_days():
    """Chapter 2: the June 2026 export-control episode. Only dates verified in
    sources get a position; the open-weight release is a note ('within days')."""
    import datetime as dt
    W, H = 900, 520
    x0, x1 = 80, 840
    d0, d1 = dt.date(2026, 6, 10), dt.date(2026, 7, 3)
    X = lambda d: x0 + (d - d0).days / (d1 - d0).days * (x1 - x0)
    axis_y = 250
    body = ''
    # stage bands
    body += f'<rect x="{X(dt.date(2026,6,12)):.1f}" y="120" width="{X(dt.date(2026,6,26))-X(dt.date(2026,6,12)):.1f}" height="16" rx="4" fill="{AMBER}" fill-opacity="0.85"/>\n'
    body += f'<text x="{X(dt.date(2026,6,12))+8:.1f}" y="132" font-size="11" fill="{BG}" font-weight="600">STAGE 2: THE PANIC AND THE PLUG</text>\n'
    body += f'<rect x="{X(dt.date(2026,6,26)):.1f}" y="120" width="{X(dt.date(2026,7,1))-X(dt.date(2026,6,26)):.1f}" height="16" rx="4" fill="{BLUE}" fill-opacity="0.9"/>\n'
    body += f'<text x="{X(dt.date(2026,6,26))+6:.1f}" y="132" font-size="11" fill="{INK}" font-weight="600">STAGE 3</text>\n'
    body += f'<line x1="{x0}" y1="{axis_y}" x2="{x1}" y2="{axis_y}" stroke="{FAINT}" stroke-width="2"/>\n'
    for d in (dt.date(2026,6,15), dt.date(2026,6,22), dt.date(2026,6,29)):
        body += f'<text x="{X(d):.1f}" y="{axis_y+22}" font-size="10.5" fill="{MUTED}" text-anchor="middle">{d.strftime("%b %-d")}</text>\n'
    events = [
        (dt.date(2026,6,12), 'up', 'JUNE 12', ['Commerce requires a license', 'for two frontier models;', 'the lab switches them off', 'worldwide']),
        (dt.date(2026,6,26), 'down', 'JUNE 26', ['Trusted partners exempted', 'for critical infrastructure']),
        (dt.date(2026,6,30), 'up', 'JUNE 30', ['Controls lifted, on', 'conditions: detect risks,', 'report misuse, set standards']),
        (dt.date(2026,7,1), 'down2', 'JULY 1', ['Access begins returning']),
    ]
    for d, side, label, lines in events:
        x = X(d)
        body += f'<circle cx="{x:.1f}" cy="{axis_y}" r="7" fill="{AMBER if d < dt.date(2026,6,26) else BLUE}" stroke="{BG}" stroke-width="2"/>\n'
        if side == 'up':
            ty = 158
            body += f'<line x1="{x:.1f}" y1="{ty+len(lines)*15+4}" x2="{x:.1f}" y2="{axis_y-9}" stroke="{FAINT}" stroke-width="1"/>\n'
        else:
            ty = axis_y + (44 if side == 'down' else 104)
            body += f'<line x1="{x:.1f}" y1="{axis_y+9}" x2="{x:.1f}" y2="{ty-12}" stroke="{FAINT}" stroke-width="1"/>\n'
        anchor = 'end' if x > 590 else 'start'
        tx = x - 6 if anchor == 'end' else x + 6
        body += f'<text x="{tx:.1f}" y="{ty}" font-size="12" font-weight="600" fill="{INK}" text-anchor="{anchor}">{label}</text>\n'
        for i, ln in enumerate(lines):
            body += f'<text x="{tx:.1f}" y="{ty+16+i*15}" font-size="11.5" fill="{MUTED}" text-anchor="{anchor}">{esc(ln)}</text>\n'
    body += f'<text x="{x0}" y="{H-70}" font-size="11.5" fill="{MUTED}">Within days of the order, a Chinese lab published an open-weight model under an MIT license:</text>\n'
    body += f'<text x="{x0}" y="{H-54}" font-size="11.5" fill="{MUTED}">"no regional limits, technical access without borders."</text>\n'
    return frame(W, H, 'PANIC TO PAPERWORK IN EIGHTEEN DAYS', 'June 12 to June 30, 2026: Stage 2 and Stage 3 of this chapter, run at speed.',
                 body, 'Sources: Mayer Brown (June 30, 2026); Al Jazeera (July 1, 2026); Z.ai GLM-5.2 model card. Details in the chapter.')


def capability_to_access():
    """Chapter 6: capability, deployment, ownership and access are different events."""
    W, H = 900, 400
    steps = [('CAPABILITY', 'Can a machine', 'do the task?'), ('DEPLOYMENT', 'Is it working', 'somewhere real?'),
             ('OWNERSHIP', 'Who controls it', 'and sets the price?'), ('ACCESS', 'Can a person get it', 'without money?')]
    bw, gap, y = 170, 26, 150
    x0 = (W - (4 * bw + 3 * gap)) / 2
    body = ''
    for i, (t, a, b) in enumerate(steps):
        x = x0 + i * (bw + gap)
        stroke = BLUE if i == 3 else AMBER
        body += f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="96" rx="10" fill="{CARD}" stroke="{stroke}" stroke-width="2"/>\n'
        body += f'<text x="{x+bw/2:.1f}" y="{y+30}" font-size="13.5" font-weight="600" fill="{INK}" text-anchor="middle">{t}</text>\n'
        body += f'<text x="{x+bw/2:.1f}" y="{y+56}" font-size="11.5" fill="{MUTED}" text-anchor="middle">{esc(a)}</text>\n'
        body += f'<text x="{x+bw/2:.1f}" y="{y+72}" font-size="11.5" fill="{MUTED}" text-anchor="middle">{esc(b)}</text>\n'
        if i < 3:
            gx = x + bw + gap / 2
            body += f'<text x="{gx:.1f}" y="{y+54}" font-size="20" fill="{BRAND}" text-anchor="middle">&#8250;</text>\n'
    body += f'<text x="{W/2:.0f}" y="{y+140}" font-size="13" fill="{INK}" text-anchor="middle">A tool can get better while its price goes up. A town can hold a productive farm</text>\n'
    body += f'<text x="{W/2:.0f}" y="{y+160}" font-size="13" fill="{INK}" text-anchor="middle">and people who can\'t afford its food. The gaps between these boxes are the part we get to decide.</text>\n'
    return frame(W, H, 'THE GAP IS WHERE WE DECIDE', 'Four different events, often confused for one.', body, 'Chapter 6.')


if __name__ == '__main__':
    for name, fn in (('ch05-horses-tractors.svg', horses_tractors),
                     ('intro-food-insecurity.svg', food_insecurity),
                     ('appd-precedent-timeline.svg', precedent_timeline),
                     ('ch19-conversion-ladder.svg', conversion_ladder),
                     ('ch02-eighteen-days.svg', eighteen_days),
                     ('ch06-capability-access.svg', capability_to_access)):
        (OUT / name).write_text(fn())
        print('wrote', OUT / name)
