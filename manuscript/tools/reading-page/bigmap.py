"""Draw the big map of everyone: Elijah's spine down the left, each other person hung off it."""
import re, html, textwrap

W = 420
RAIL = 16
EX, EW = 6, 408            # Elijah boxes
CX, CW = 36, 378           # cards
LH = 14
TX = 92                    # row text offset inside a card
WRAP = 44
EWRAP = 62
TAG = {'Yes': ('GETS IT', 'yes'), 'Half': ('HALF', 'half'), 'No': ("DOESN'T", 'no'),
       'Open': ('OPEN', 'open'), 'None': ('', None), 'Ends': ('WHERE HE ENDS', None)}
ROWS = [('Wants', 'WANTS'), ('Tries', 'TRIES'), ('Stopped by', 'STOPPED BY'), ('So', 'SO'), ('Ends', 'ENDS')]
WHO = ['Elijah', 'machine']


def esc(s):
    return html.escape(s, quote=False)


def parse(md_text):
    items = []
    cur = None
    for line in md_text.splitlines():
        m = re.match(r'^## Elijah \| (.+) \| (\w+)\s*$', line)
        if m:
            cur = {'kind': 'elijah', 'when': m.group(1), 'gets': m.group(2), 'text': ''}
            items.append(cur)
            continue
        m = re.match(r'^### (.+) \| (.+) \| (\w+)\s*$', line)
        if m:
            cur = {'kind': 'card', 'name': m.group(1), 'when': m.group(2), 'gets': m.group(3), 'f': {}}
            items.append(cur)
            continue
        if cur is None:
            continue
        if cur['kind'] == 'elijah':
            if line.strip() and not line.startswith('#'):
                cur['text'] = (cur['text'] + ' ' + line.strip()).strip()
        else:
            m = re.match(r'^- ([A-Za-z ]+): (.+)$', line)
            if m:
                cur['f'][m.group(1)] = m.group(2).strip()
    return items


def marker(out, xr, y, gets):
    """Right-aligned outcome: dot plus label, ending at xr. y is the text baseline."""
    label, mk = TAG[gets]
    if not label:
        return
    out.append('<text class="m-h m-hr" x="%s" y="%s" text-anchor="end">%s</text>' % (xr, y, esc(label)))
    if mk:
        mx = xr - len(label) * 6.3 - 9
        out.append('<circle class="m-mk m-mk-%s" cx="%s" cy="%s" r="3.6"/>' % (mk, round(mx, 1), y - 3.5))


def bold_who(line):
    s = esc(line)
    for w in WHO:
        s = re.sub(r'\b%s\b' % w, '<tspan class="bm-who">%s</tspan>' % w, s)
    return s


def draw(md_text, svg_id):
    items = parse(md_text)
    out = []
    y = 6
    rail_from = None
    for it in items:
        if it['kind'] == 'elijah':
            lines = textwrap.wrap(it['text'], EWRAP)
            h = 26 + len(lines) * 15 + 9
            if rail_from is not None:
                out.append('<line class="bm-rail" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (RAIL, rail_from, RAIL, y))
            out.append('<rect class="bm-e" x="%s" y="%s" width="%s" height="%s" rx="6"/>' % (EX, y, EW, h))
            out.append('<text class="m-h bm-eh" x="%s" y="%s">ELIJAH · %s</text>'
                       % (EX + 12, y + 18, esc(re.sub(r'^Act \w+, ', '', it['when']).upper())))
            marker(out, EX + EW - 12, y + 18, it['gets'])
            for i, ln in enumerate(lines):
                out.append('<text class="m-t" x="%s" y="%s">%s</text>' % (EX + 12, y + 37 + i * 15, esc(ln)))
            y += h
            rail_from = y
            y += 14
            continue
        # a card
        f = it['f']
        tag_lines = textwrap.wrap(f.get('To Elijah', ''), 54)
        rows = [(lab, textwrap.wrap(f[key], WRAP)) for key, lab in ROWS if f.get(key)]
        h = 26 + len(tag_lines) * LH + 8 + sum(len(ls) * LH + 7 for _, ls in rows) + 3
        out.append('<rect class="m-box" x="%s" y="%s" width="%s" height="%s" rx="6"/>' % (CX, y, CW, h))
        # connector from the spine
        out.append('<line class="bm-link" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (RAIL, y + 14, CX, y + 14))
        out.append('<circle class="bm-node" cx="%s" cy="%s" r="2.6"/>' % (RAIL, y + 14))
        out.append('<text x="%s" y="%s"><tspan class="bm-name">%s</tspan><tspan class="m-h" dx="9">%s</tspan></text>'
                   % (CX + 10, y + 18, esc(it['name']), esc(it['when'].upper())))
        marker(out, CX + CW - 10, y + 18, it['gets'])
        ty = y + 26 + 9
        for i, ln in enumerate(tag_lines):
            out.append('<text class="m-then" x="%s" y="%s">%s</text>' % (CX + 10, ty + i * LH, esc(ln)))
        ry = y + 26 + len(tag_lines) * LH + 8
        fx = CX + TX - 9
        first = True
        for lab, ls in rows:
            rh = len(ls) * LH
            if not first:
                # small arrow down the flow, into this row
                out.append('<line class="m-arrow" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (fx, ry - 7 - 6, fx, ry + 3))
                out.append('<polygon class="m-head" points="%s,%s %s,%s %s,%s"/>'
                           % (fx, ry + 7, fx - 3.2, ry + 1.5, fx + 3.2, ry + 1.5))
            first = False
            if lab == 'STOPPED BY':
                out.append('<rect class="bm-wall" x="%s" y="%s" width="3" height="%s"/>' % (CX + 1, ry - 2, rh + 3))
            out.append('<text class="m-h" x="%s" y="%s">%s</text>' % (CX + 10, ry + 10, lab))
            for i, ln in enumerate(ls):
                body = bold_who(ln) if lab == 'STOPPED BY' else esc(ln)
                out.append('<text class="bm-t" x="%s" y="%s">%s</text>' % (CX + TX, ry + 10.5 + i * LH, body))
            ry += rh + 7
        y += h + 10
    H = y - 4
    n = sum(1 for it in items if it['kind'] == 'card')
    label = ("The big map of everyone. Elijah's eight stages run down the left. %d other people hang off the stage "
             "where they come into his story, each with what they want, what they try, what stops them, what they do "
             "about it, where they end, and whether they get it." % n)
    return ('<svg id="%s" viewBox="0 0 %d %d" role="img" aria-label="%s">' % (svg_id, W, H, html.escape(label))
            + ''.join(out) + '</svg>'), n
