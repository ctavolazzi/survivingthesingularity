"""Regenerate five print-readable figures, retaining the book's vector palette.

Run from any directory: python3 docs/v0.10.0/figures.py
The food chart reads the committed USDA data used by the previous edition.
"""
from pathlib import Path
import csv
from html import escape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'static/book-images'
FONT = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace"
BG, PANEL, EDGE, INK, MUTED = '#020617', '#0f172a', '#334155', '#f1f5f9', '#94a3b8'
AMBER, BLUE, RED = '#f59e0b', '#3b82f6', '#ef4444'
W = 480


def text(x, y, value, size=12, color=MUTED, anchor='start', bold=False):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{600 if bold else 400}">{escape(value)}</text>\n'


def lines(x, y, values, size=12, color=MUTED, anchor='start', step=19, bold=False):
    return ''.join(text(x, y + i * step, v, size, color, anchor, bold) for i, v in enumerate(values))


def rect(x, y, w, h, stroke=EDGE, fill=PANEL):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n'


def path(d, color=AMBER, arrow=True, dash=''):
    mark = f' marker-end="url(#{dict([(AMBER,"amber"),(BLUE,"blue"),(RED,"red")])[color]})"' if arrow else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"{mark}{f" stroke-dasharray={chr(34)}{dash}{chr(34)}" if dash else ""}/>\n'


def frame(height, title, subtitle, body):
    defs = '<defs>' + ''.join(f'<marker id="{name}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0L10,5L0,10z" fill="{color}"/></marker>' for name, color in [('amber', AMBER), ('blue', BLUE), ('red', RED)]) + '</defs>\n'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" font-family="{FONT}" role="img" aria-label="{escape(title, quote=True)}">\n' + defs + rect(1, 1, W-2, height-2, EDGE, BG) + text(24, 34, title, 16, INK, bold=True) + f'<line x1="24" y1="46" x2="456" y2="46" stroke="{AMBER}" stroke-width="1.5"/>\n' + lines(24, 69, subtitle) + body + '</svg>\n'


def box(x, y, width, height, title, detail, color=AMBER):
    return rect(x, y, width, height, color) + lines(x + width/2, y+26, title, 14, INK, 'middle', 20, True) + lines(x + width/2, y+26+len(title)*20+7, detail, 12, MUTED, 'middle', 18)


def region():
    body = box(24, 115, 207, 110, ['FOOD PRODUCTION'], ['CSA farms, greenhouses,', 'grow towers'])
    body += box(249, 115, 207, 110, ['MATERIALS RECOVERY'], ['Recover scrap and', 'reusable materials'])
    body += path('M127 225 V252 H194 V270') + path('M353 225 V252 H286 V270')
    body += box(114, 276, 252, 90, ['DENSE CITY CORE'], ['High density,', 'low production'], BLUE)
    body += text(407, 266, 'SUPPLY IN', 12, AMBER, 'middle')
    body += path('M127 409 V389 H194 V372') + path('M353 409 V389 H286 V372')
    body += box(24, 415, 207, 112, ['ENERGY + WATER'], ['Solar, storage,', 'microgrids'])
    body += box(249, 415, 207, 112, ['NEIGHBORHOOD', 'FACTORIES'], ['Plasma tables,', 'printers, fab labs'])
    body += lines(24, 555, ['The ring builds capacity and local work.', 'If the trucks stop, the region still eats.', 'Resilience, not secession.'])
    return frame(610, 'THE REGION, NOT THE CITY LIMITS', ['A dense core cannot produce everything.', 'The productive region around it can.'], body)


def cooling():
    body = text(240, 112, 'INSIDE THE INSULATED SHELL', 13, MUTED, 'middle', True)
    body += box(42, 133, 177, 94, ['GPU BLOCK'], ['Heat at the silicon'], RED)
    body += box(261, 133, 177, 94, ['CPU BLOCK'], ['600–1000 W total*'], RED)
    body += path('M131 227 V241 H179 V259', RED) + path('M350 227 V241 H300 V259', RED)
    body += box(120, 265, 240, 81, ['12V BRUSHLESS PUMP'], ['PWM speed control'], RED)
    body += path('M360 302 H455 V434 H389', RED)
    body += text(444, 373, 'HOT OUT', 12, RED, 'end')
    body += f'<line x1="42" y1="361" x2="325" y2="361" stroke="{EDGE}" stroke-dasharray="5 5"/>\n'
    body += text(240, 390, 'OUTSIDE THE SHELL: FREE AIR', 13, BLUE, 'middle', True)
    body += box(100, 407, 280, 99, ['EXTERNAL RADIATOR'], ['Salvaged Honda Civic core*', '+ 12V high-static fans*'], BLUE)
    body += path('M100 456 H20 V174 H36', BLUE)
    body += path('M20 174 V123 H455 V174 H444', BLUE)
    body += text(44, 529, 'COOL RETURN TO THE CHIPS', 12, BLUE)
    body += lines(24, 555, ['Move heat outside, away from living space.', 'Heat per second = flow × Cp × ΔT', 'In winter, recover heat for the living space.', '*Illustrative components and combined load.', 'Schematic only; engineer a compatible system.'])
    return frame(650, 'THE SPLIT-LOOP THERMAL EXCHANGE', ['A conceptual coolant circuit.', 'Hot out, cool back.'], body)


def fab():
    body = box(24, 104, 432, 78, ['RECYCLED RAW MATERIALS'], ['Scrap steel · PETG · salvage'], BLUE)
    body += path('M240 182 V211', BLUE)
    body += text(240, 236, 'OPEN-SOURCE MACHINE CORES', 14, AMBER, 'middle', True)
    rows = [
        (253, ['3D PRINTER'], ['RepRap; prints some', 'of its own parts'], ['SEALS · GEARS', 'VALVES'], ['Replacement parts']),
        (367, ['CNC PLASMA', '/ ROUTER'], ['Match power supply', 'to machine load'], ['STRUCTURAL', 'STEEL'], ['Mounts, brackets,', 'frames']),
        (481, ['OPEN-SOURCE', 'TRACTOR'], ['BCS-type / GVCS', 'pattern'], ['TILLAGE', 'HAULING'], ['Field power,', 'PTO energy']),
    ]
    for y, title, detail, out, note in rows:
        body += box(24, y, 213, 111, title, detail)
        body += path(f'M237 {y+54} H265')
        body += box(273, y, 183, 111, out, note, EDGE)
    body += lines(24, 618, ['Fabricate the replacement instead of waiting.', 'Pattern library: Global Village Construction', 'Set, fifty machines for a small civilization.'])
    return frame(674, 'THE DECENTRALIZED FAB LAB', ['Local materials, shared machine designs,', 'useful parts and field power.'], body)


def mesh():
    body = rect(24, 110, 320, 420, MUTED)
    body += lines(184, 135, ['WATERPROOF PELICAN', '/ AMMO BOX'], 12, MUTED, 'middle')
    body += box(44, 168, 280, 79, ['5W SOLAR PV PANEL*'], ['Paperback-sized,', 'mounted on the case'], BLUE)
    body += path('M184 247 V274', BLUE)
    body += text(203, 267, 'Matched charger*')
    body += box(44, 281, 280, 75, ['PROTECTED BATTERY PACK*'], ['Matched cells and protection'])
    body += path('M184 356 V386', BLUE)
    body += box(44, 393, 280, 114, ['ESP32 / HELTEC', 'LORA BOARD*'], ['Meshtastic firmware;', 'idle draw varies by setup'])
    body += path('M324 451 H372 V278', AMBER, False)
    body += f'<circle cx="372" cy="270" r="5" fill="{AMBER}"/>\n'
    body += path('M357 257 Q372 239 387 257', AMBER, False)
    body += path('M348 248 Q372 221 396 248', AMBER, False)
    body += lines(397, 187, ['TUNED,', 'ELEVATED', 'ANTENNA'], 12, MUTED, 'middle')
    body += path('M390 270 H449', AMBER, True, '5 5')
    body += lines(384, 309, ['TO NEXT', 'NODE'], 12, AMBER)
    body += lines(24, 557, ['*Illustrative hardware. Use protected cells', 'and a charger matched to the battery pack.', 'Match 915 / 868 MHz hardware, firmware', 'and regional settings to local radio rules.', 'Reach depends on terrain and line of sight.', 'Solar runtime depends on weather and load.'])
    return frame(676, 'AN INDEPENDENT MESH NODE', ['The power path and radio link.', 'A component map, not assembly instructions.'], body)


def food_insecurity():
    with (ROOT / 'docs/v0.9.2/data/food-insecurity-us.csv').open() as source:
        data = list(csv.reader(line for line in source if not line.startswith('#')))
    rows = data[1:]
    years = [int(r[0]) for r in rows]
    fi = [float(r[1]) for r in rows]
    low = [float(r[2]) for r in rows]
    x0, x1, top, bottom = 62, 448, 215, 433
    X = lambda year: x0 + (year-2001)/23*(x1-x0)
    Y = lambda value: bottom - value/16*(bottom-top)
    body = text(24, 115, 'SHARE OF US HOUSEHOLDS', 13, INK, bold=True)
    body += path('M26 140 H55', AMBER, False) + text(66, 144, 'Food insecure at some time in the year')
    body += path('M26 164 H55', BLUE, False, '5 4') + text(66, 168, 'Very low food security')
    body += text(24, 194, 'SHADED: 2007–2009 RECESSION', 12)
    for tick in (0,4,8,12,16):
        y = Y(tick)
        body += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#1e293b" stroke-width="1"/>\n'
        body += text(x0-10, round(y+4,1), f'{tick}%', 12, MUTED, 'end')
    body += f'<rect x="{X(2007.5):.1f}" y="{top}" width="{X(2009.5)-X(2007.5):.1f}" height="{bottom-top}" fill="#475569" fill-opacity="0.25"/>\n'
    for values, color, dash in [(fi, AMBER, ''),(low, BLUE, '5 4')]:
        points = ' '.join(f'{X(y):.2f},{Y(v):.2f}' for y,v in zip(years,values))
        body += f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.5" stroke-dasharray="{dash or "none"}"/>\n'
    for year in [2001,2007,2013,2019,2024]:
        body += text(round(X(year),1), 458, str(year), 12, MUTED, 'middle')
    body += lines(24, 491, ['2007: 11.1% food insecure', '2008: 14.6%, a third higher in one year', '2024: 13.7%, 18.3 million households', '2024: 5.4% had very low food security'], 12, INK, step=23)
    body += lines(24, 591, ['Source: USDA Economic Research Service,', 'food security trends, 2001–2024.', 'Current Population Survey supplement.'])
    return frame(646, 'WHEN THE JOBS GO, DINNER GOES', ['Food insecurity rose sharply in the recession', 'and took a decade to return to earlier levels.'], body)


FIGURES = {
    'ch09-region-ring.svg': region,
    'ch11-cooling-loop.svg': cooling,
    'ch17-fab-lab.svg': fab,
    'ch17-lora-node.svg': mesh,
    'intro-food-insecurity.svg': food_insecurity,
}

if __name__ == '__main__':
    for name, generate in FIGURES.items():
        path_out = OUT / name
        path_out.write_text(generate())
        print(path_out.relative_to(ROOT))
