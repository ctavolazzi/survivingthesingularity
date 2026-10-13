"""Seven native SVG revisions with identical screen and print geometry.

Run this file to reproduce only these fourteen assets and their handoff JSON.
No registry, manuscript or publication build is modified. The preserved 0.10.1
edition supplies baseline hashes, not artwork embedded in the new figures.
"""
from pathlib import Path
from html import escape
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
IMAGES = ROOT / 'static/book-images'
BASELINE = ROOT.parent / 'sts-v0.10.1/static/book-images'
spec = importlib.util.spec_from_file_location('v101_art', ROOT / 'docs/v0.10.1/vignettes.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
Art = base.Art
PALETTES = base.PALETTES


def box(a, x, y, w, h, color='rule'):
    a.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{a.p["paper"]}" stroke="{a.p[color]}" stroke-width="1.5"/>')


def arrow(a, x, y, x2, y2, color='ink'):
    a.line(x, y, x2, y2, color, 1.6)
    if x == x2:
        d = 1 if y2 > y else -1
        a.path(f'M{x2-4} {y2-6*d}L{x2} {y2}L{x2+4} {y2-6*d}', color, 1.6)
    else:
        d = 1 if x2 > x else -1
        a.path(f'M{x2-6*d} {y2-4}L{x2} {y2}L{x2-6*d} {y2+4}', color, 1.6)


def supply(mode):
    a = Art(mode, 588, 'SHORTEN THE SUPPLY LINE', 'Two schematic routes lead to households. One passes through distant suppliers, factories and freight; another uses imported parts in nearby workshops and returns goods for repair. People, energy and imports sustain both routes. Neither distance nor this drawing proves fair treatment.')
    a.text(120, 88, 'LONGER ROUTE', color='ink', anchor='middle')
    a.text(350, 88, 'NEARBY WORK', color='ink', anchor='middle')
    a.text(240, 114, 'A comparison of dependencies, not distances.', anchor='middle')
    left = [('Raw inputs', 'Distant suppliers'), ('Factory + freight', 'Warehouses'), ('Regional delivery', 'Households')]
    right = [('Imported parts', 'Tools + materials'), ('Nearby workshops', 'Growers + repair'), ('Households', 'Use + return')]
    for x, rows, color in [(20, left, 'muted'), (250, right, 'amber')]:
        for i, (top, bottom) in enumerate(rows):
            y = 140 + i * 110
            box(a, x, y, 200, 68, color)
            a.text(x + 100, y + 27, top, color='ink', anchor='middle')
            a.text(x + 100, y + 49, bottom, anchor='middle')
            if i < 2:
                arrow(a, x + 100, y + 75, x + 100, y + 104, color)
    a.path('M450 404H466V284H454', 'blue', 1.6)
    a.path('M460 280L454 284L460 288', 'blue', 1.6)
    a.text(350, 456, 'Repair and reuse', color='blue', anchor='middle')
    a.footer(511, ['Imports remain in both routes.', 'People, energy and upkeep sustain the work.', 'Distance alone cannot establish fairness.'])
    return a


def region(mode):
    a = Art(mode, 624, 'BUILD REGIONAL CAPACITY', 'A town exchanges goods and services with nearby farms, materials recovery, power and water services, and workshops. This is a capacity-building objective. Coverage depends on stores, seasonal production, water, power, logistics and remaining imports, which must be measured.')
    a.text(20, 79, 'A regional objective, not a closed economy.')
    nodes = [(20, 116, 'FOOD', 'Farms + kitchens'), (252, 116, 'MATERIALS', 'Recovery + stores'), (20, 398, 'POWER + WATER', 'Supply + upkeep'), (252, 398, 'WORKSHOPS', 'Tools + repairs')]
    for x, y, title, line in nodes:
        box(a, x, y, 208, 76)
        a.text(x + 104, y + 28, title, color='ink', anchor='middle')
        a.text(x + 104, y + 53, line, anchor='middle')
    # Exchange paths occupy the four corners, away from the import label.
    a.path('M124 192V221H205V247M356 192V221H275V247M205 329V368H124V398M275 329V368H356V398', 'amber', 2)
    box(a, 129, 252, 222, 74, 'amber')
    a.text(240, 281, 'TOWN + HOUSEHOLDS', color='ink', anchor='middle')
    a.text(240, 305, 'People do the work', anchor='middle')
    a.text(20, 509, 'Still connected to outside suppliers.', color='blue')
    a.footer(548, ['Measure stores and seasonal production.', 'Water, power and delivery limit coverage.', 'Ask: what can we supply, and for how long?'])
    return a


def plant(a, x, y):
    a.path(f'M{x} {y+12}V{y-7}M{x} {y+2}Q{x-19} {y+1} {x-14} {y-10}Q{x-1} {y-11} {x} {y+2}M{x} {y-4}Q{x+3} {y-19} {x+17} {y-13}Q{x+16} {y-1} {x} {y-4}', 'blue', 1.5)


def cnc(mode):
    a = Art(mode, 610, 'TOOLS OVER A GROWING BED', 'Top-view concept of a growing bed with horizontal X travel, a gantry with Y travel across it, and a Z tool moving toward a plant. Generic tools seed, water or weed. Reduced walking space does not remove human inspection, maintenance and harvest, and this is not a model-specific build plan.')
    a.text(20, 77, 'A generic gantry concept, viewed from above.')
    a.text(240, 107, 'X travel', color='amber', anchor='middle')
    arrow(a, 74, 124, 408, 124, 'amber')
    box(a, 52, 148, 356, 202)
    for y in [154, 344]:
        a.line(45, y, 415, y, 'ink', 3)
    for x, y in [(101, 203), (166, 203), (330, 203), (101, 301), (166, 301), (330, 301)]:
        plant(a, x, y)
    # A narrow gantry spans the bed; the carriage carries a tool downward.
    a.path('M232 144V353M258 144V353', 'amber', 3)
    box(a, 222, 231, 46, 31, 'amber')
    a.circle(245, 247, 7, 'ink', 1.5)
    a.path('M241 243L249 251M249 243L241 251', 'ink', 1.4)
    a.line(274, 247, 282, 247, 'rule')
    a.text(290, 252, 'Z', color='ink')
    arrow(a, 434, 162, 434, 333, 'amber')
    a.text(446, 252, 'Y', color='amber')
    a.text(20, 390, 'X: move the gantry along the bed.', color='ink')
    a.text(20, 412, 'Y: move the carriage across the gantry.')
    a.text(20, 434, 'Z: crossed circle = down into the bed.')
    a.footer(482, ['Model-specific tools seed, water or weed.', 'A gantry can reduce walking space in a bed.', 'People still inspect, maintain and harvest.', 'Concept only; no machine version is implied.'])
    return a


def greenhouse(mode):
    a = Art(mode, 650, 'THE GREENHOUSE CONTROL BUS', 'A component map connects an SHT31-D air temperature and humidity sensor and a STEMMA capacitive moisture sensor to a Raspberry Pi running Mycodo over I2C. Growers configure and test setpoints, run-time and water limits, and irrigation fail-off behavior. Matched low-voltage drivers operate valves, fans and lights, with manual shutoffs. It is not a wiring diagram or an unattended safety guarantee.')
    a.text(20, 76, 'Component map, not a wiring diagram.')
    for x, title, line1, line2 in [(20, 'SHT31-D', 'Air temperature', '+ humidity'), (252, 'STEMMA 4026', 'Capacitive', 'moisture reading')]:
        box(a, x, 96, 208, 92)
        a.text(x + 104, 122, title, color='ink', anchor='middle')
        a.text(x + 104, 147, line1, anchor='middle')
        a.text(x + 104, 169, line2, anchor='middle')
    a.path('M124 188V210H356V188M240 210V228', 'blue', 1.6)
    a.path('M236 220L240 228L244 220', 'blue', 1.6)
    a.text(270, 228, 'I2C', color='blue')
    box(a, 104, 236, 272, 68, 'amber')
    a.text(240, 263, 'Raspberry Pi + Mycodo', color='ink', anchor='middle')
    a.text(240, 287, 'Read, decide, actuate', anchor='middle')
    arrow(a, 240, 309, 240, 329, 'amber')
    box(a, 20, 337, 440, 117, 'amber')
    a.text(38, 361, 'GROWER: CONFIGURE AND TEST', color='ink')
    a.text(38, 385, 'Setpoints + run-time and water limits')
    a.text(38, 409, 'Bad/missing moisture data: water OFF')
    a.text(38, 433, 'Keep a manual shutoff accessible')
    arrow(a, 240, 461, 240, 483, 'amber')
    box(a, 20, 491, 440, 65)
    a.text(240, 516, 'Matched drivers / relays', color='ink', anchor='middle')
    a.text(240, 540, 'Low-voltage valve, fan and light circuits', anchor='middle')
    a.footer(600, ['Check readings against conditions in the bed.', 'Verify water stops on faults and lost power.'])
    return a


def collapse(mode):
    a = Art(mode, 614, 'WHEN A MODEL EATS ITS OUTPUT', 'Three schematic distributions illustrate one possible failure during repeated training on generated samples. Rare cases can be lost and a later distribution can narrow or drift. The curves are illustrative, not measured data, a universal result or a timetable; real data, sampling and training choices matter.')
    a.text(20, 78, 'One possible lineage under repeated sampling.')
    curves = [
        ('M30 196C45 192 49 178 59 164S84 118 104 117S135 132 147 164S166 191 178 196', 'Starting examples', 'A range of cases', 'can be represented.'),
        ('M30 336C68 336 69 329 77 310S88 257 104 257S122 289 129 309S144 336 178 336', 'Generated samples', 'Rare cases can be', 'lost in resampling.'),
        ('M30 476H94C114 476 116 399 126 397S138 476 146 476H178', 'Possible collapse', 'Variety can shrink;', 'errors can drift.'),
    ]
    for i, (curve, title, line1, line2) in enumerate(curves):
        y = 113 + i * 140
        a.line(26, y + 87, 182, y + 87, 'rule', 1)
        a.path(curve, 'amber' if i else 'blue', 2.5)
        a.text(210, y + 28, title, color='ink')
        a.text(210, y + 53, line1)
        a.text(210, y + 76, line2)
        if i < 2:
            arrow(a, 104, y + 104, 104, y + 130, 'muted')
    a.footer(538, ['Schematic curves, not a generation timetable.', 'Real data, sampling and training all matter.', 'Shumailov et al., Nature (2024).'])
    return a


def story(mode):
    a = Art(mode, 599, 'USEFUL WORK, HUMAN STORY', 'Four illustrated stages connect documented useful work to a truthful human story, possible platform distribution and continued service to readers. A useful story may reach people, but no post is guaranteed an audience. Respect consent and preserve the actual instructions beyond the feed.')
    a.text(20, 78, 'A publishing sequence, not an audience formula.')
    rows = [(112, '1. DOCUMENT THE WORK', 'Parts, steps, errors and repairs.'), (213, '2. TELL THE TRUE STORY', 'Show the people with their consent.'), (314, '3. OFFER IT TO THE FEED', 'Distribution may bring new readers.'), (415, '4. KEEP THE WORK USABLE', 'Answer, correct, archive and repeat.')]
    for i, (y, title, line) in enumerate(rows):
        a.text(112, y + 19, title, color='ink')
        a.text(112, y + 46, line)
        if i < 3:
            arrow(a, 54, y + 65, 54, y + 87, 'rule')
    # Instructions, a person, distribution branches and a durable archive.
    a.path('M29 107H74V166H29ZM38 120H65M38 132H65M38 144H58', 'blue', 1.8)
    a.circle(54, 219, 13, 'amber', 1.8)
    a.path('M28 264Q27 239 54 239Q80 239 80 264Z', 'amber', 1.8)
    a.circle(54, 326, 7, 'blue', 1.8)
    for x in [29, 54, 79]:
        a.line(54, 333, x, 352, 'blue', 1.4)
        a.circle(x, 360, 6, 'blue', 1.8)
    a.path('M28 426H80V465H28ZM26 418H82V429H26ZM44 439H64', 'amber', 1.8)
    a.footer(533, ['No post is guaranteed reach or income.', 'Keep usable instructions beyond the feed.'])
    return a


def cooling(mode):
    a = Art(mode, 642, 'MOVE THE HEAT OUTSIDE', 'A conceptual coolant loop transfers heat from CPU and GPU water blocks through a pump to an outdoor radiator with airflow, then returns cooler coolant. Heat rate equals coolant mass flow times specific heat times temperature change. Components are illustrative; compatibility, heat load and actual flow require design and verification.')
    a.text(20, 78, 'Conceptual loop; not a component specification.')
    a.text(240, 112, 'INSIDE THE INSULATED SHELL', color='ink', anchor='middle')
    box(a, 100, 133, 280, 67, 'amber')
    a.text(240, 160, 'CPU + GPU water blocks', color='ink', anchor='middle')
    a.text(240, 184, 'Heat enters the coolant', anchor='middle')
    arrow(a, 240, 205, 240, 228, 'amber')
    box(a, 140, 237, 200, 62, 'amber')
    a.text(240, 263, 'CIRCULATING PUMP', color='ink', anchor='middle')
    a.text(240, 286, 'Verified flow', anchor='middle')
    a.path('M340 269H443V412H383', 'amber', 2)
    a.path('M391 408L383 412L391 416', 'amber', 1.6)
    a.text(430, 328, 'HOT OUT', color='amber', anchor='end')
    a.line(66, 342, 335, 342, 'rule', 1, '5 5')
    a.text(240, 365, 'OUTSIDE AIR', color='ink', anchor='middle')
    box(a, 100, 382, 280, 78, 'blue')
    a.text(240, 411, 'RADIATOR + AIRFLOW', color='ink', anchor='middle')
    a.text(240, 438, 'Heat leaves the coolant', anchor='middle')
    a.path('M100 424H38V168H95', 'blue', 2)
    a.path('M87 164L95 168L87 172', 'blue', 1.6)
    a.text(38, 490, 'COOL RETURN TO THE CHIPS', color='blue')
    a.footer(536, ['Heat rate = mass flow × Cp × ΔT', 'W = (kg/s) × [J/(kg·°C)] × °C', 'Match materials, coolant, pump and radiator.', 'Illustrative loop; verify load and heat removal.'])
    return a


BUILDERS = {
    'ch09-hyperlocal-vs-global.svg': supply,
    'ch09-region-ring.svg': region,
    'ch09-cnc-bed.svg': cnc,
    'ch09-greenhouse-bus.svg': greenhouse,
    'ch10-model-collapse.svg': collapse,
    'ch10-algorithm-unlock.svg': story,
    'ch11-cooling-loop.svg': cooling,
}

DETAILS = {
    'ch09-hyperlocal-vs-global.svg': {
        'changes': ['A03: removed universal exploitation and self-sufficiency claims', 'Made imported tools, materials, human work and upkeep visible', 'Stacked two schematic routes with a repair return'],
        'alt': 'Two schematic supply routes reach households: distant suppliers through factory and freight, or imported parts through nearby workshops and growers, with a repair return. Both rely on people, energy and imports.',
        'caption': 'Shorter supply lines can make repair and coordination more local. Imported parts, materials, energy and human work remain; distance alone does not establish fair treatment.',
    },
    'ch09-region-ring.svg': {
        'changes': ['A04: replaced complete regional self-sufficiency and guaranteed outage coverage', 'Coverage now depends on measured stores, seasonal output, water, power and delivery'],
        'alt': 'A town and households connect to nearby farms and kitchens, materials recovery and stores, power and water services, and workshops. Regional coverage is a capacity-building objective that must be measured, with outside suppliers still needed.',
        'caption': 'Build regional capacity, then measure what it covers. Stores, seasonal production, water, power, delivery and remaining imports determine how many people can be supplied and for how long.',
    },
    'ch09-cnc-bed.svg': {
        'changes': ['A06: generic model-dependent tooling replaces unpinned OpenCV rotary-weeder claim', 'Reduced walking space replaces zero wasted bed; inspection, upkeep and harvest stay human'],
        'sources': ['https://farm.bot/pages/tools', 'https://farm.bot/'],
        'alt': 'Top view of a gantry over a growing bed, with X travel along the bed, Y travel across the gantry and Z motion lowering the tool toward a plant. Generic tooling can seed, water or weed; people still inspect, maintain and harvest.',
        'caption': 'A gantry can reduce walking space in a bed. Tooling and behavior depend on the machine and software version; this concept is not a build plan or a promise to automate the entire crop.',
    },
    'ch09-greenhouse-bus.svg': {
        'changes': ['A05: STEMMA 4026 identified as capacitive moisture sensor, not a dedicated soil-temperature probe', 'Explicit grower setpoints, run-time and water limits, tested irrigation fail-off and manual shutoff', 'Component map retains I2C sensing and matched low-voltage actuation without wiring or unattended guarantees'],
        'sources': ['https://www.adafruit.com/product/4026'],
        'alt': 'SHT31-D air temperature and humidity and STEMMA capacitive moisture sensors connect over I2C to a Raspberry Pi running Mycodo. Growers configure and test setpoints, run-time and water limits, irrigation fail-off behavior and manual shutoffs; matched drivers operate low-voltage valve, fan and light circuits.',
        'caption': 'The greenhouse bus is a component map. Use moisture readings checked against the bed, configure run-time and water limits, verify that water stops on faults and power loss, and retain a manual shutoff.',
    },
    'ch10-model-collapse.svg': {
        'changes': ['Replaced fixed generation stages with a conditional training lineage', 'Illustrative curves explicitly identify possible loss of rare cases and drift, not universal inevitable failure'],
        'sources': ['https://www.nature.com/articles/s41586-024-07566-y'],
        'alt': 'Three schematic distributions show one possible result of repeatedly training on generated samples: rare cases can be lost, variety can narrow and errors can drift. The curves are illustrative, without measured axes or a generation timetable.',
        'caption': 'One possible failure in recursive training on generated samples. This schematic is not a universal outcome or a timetable; real data, sampling and training choices affect the result. Based on Shumailov et al., Nature (2024).',
    },
    'ch10-algorithm-unlock.svg': {
        'changes': ['Recomposed wide funnel as four illustrated stages', 'Kept human truth, consent, corrections and durable instructions visible', 'Distribution is possible, with no audience or income guarantee'],
        'alt': 'Four illustrated stages connect documenting useful work, telling a true story with consent, offering it to a feed and keeping instructions usable through answers, corrections and archives. Distribution may bring readers but is not guaranteed.',
        'caption': 'Document useful work, tell the true story with consent, and keep the instructions available. A platform may bring readers; a post is not guaranteed reach or income.',
    },
    'ch11-cooling-loop.svg': {
        'changes': ['A11: heat equation specifies mass flow in kg/s and explicit units', 'Kept conceptual loop and compatibility boundary while removing unverified combined load and salvaged-component recipe', 'Larger labels and simplified serial flow retain named hot and cool paths'],
        'alt': 'A conceptual coolant loop carries heat from CPU and GPU water blocks through a pump to an outdoor radiator with airflow and returns cooler coolant. Heat rate equals mass flow times specific heat times temperature change; materials, pump, coolant and radiator must be compatible.',
        'caption': 'Move heat out through a compatible, verified coolant loop. Heat rate uses mass flow in kilograms per second: Q̇ = ṁ Cp ΔT. This diagram specifies neither components nor cooling capacity.',
    },
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    changes = []
    for name, builder in BUILDERS.items():
        art = builder('screen')
        screen, printed = IMAGES / name, IMAGES / 'print' / name
        screen.write_text(art.finish())
        printed.write_text(builder('print').finish())
        # Read back every write; final metadata records bytes on disk.
        assert screen.read_text() == art.finish()
        assert printed.read_text() == builder('print').finish()
        detail = DETAILS[name]
        changes.append({
            'file': name,
            'generator': 'docs/v0.10.2/figures_middle.py',
            'kind': 'conceptual',
            'pixels': [480, art.height],
            'provenance': 'Original native SVG revision by Codex for v0.10.2. Semantics aligned with the reviewed chapter; no new measured dataset. Screen and print use identical geometry with palette-only differences.',
            'screen_sha256': digest(screen),
            'print_sha256': digest(printed),
            'baseline_screen_sha256': digest(BASELINE / name),
            'baseline_print_sha256': digest(BASELINE / 'print' / name),
            'recommended_alt': detail['alt'],
            'recommended_caption': detail['caption'],
            'changes': detail['changes'],
            'primary_sources': detail.get('sources', []),
            'source_review_date': '2026-09-28',
        })
    output = HERE / 'art-middle-changes.json'
    output.write_text(json.dumps(changes, indent=2, ensure_ascii=False) + '\n')
    assert json.loads(output.read_text()) == changes
    print(json.dumps({'figures': len(changes), 'variants': len(changes) * 2, 'metadata': str(output.relative_to(ROOT))}))


if __name__ == '__main__':
    main()
