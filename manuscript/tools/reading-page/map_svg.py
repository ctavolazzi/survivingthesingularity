"""Draw one character's map as a tall, narrow flowchart (reads top to bottom, snakes left-right)."""
import re, html, textwrap

W = 420
XL, XR, CW = 10, 218, 192
LH = 15            # body line height
WRAP = 29          # characters per body line


def esc(s):
    return html.escape(s, quote=False)


def parse(md_text):
    want = re.search(r'\*\*He wants:\*\*\s*(.+)', md_text).group(1).strip()
    fear = re.search(r'\*\*He is afraid of:\*\*\s*(.+)', md_text).group(1).strip()
    rows = []
    for line in md_text.splitlines():
        if not line.startswith('|') or line.startswith('|---') or line.startswith('| When'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 7:
            rows.append(dict(zip(['when', 'tries', 'stops', 'so', 'leaves', 'gets', 'then'], cells)))
    m = re.search(r'\*\*Where he ends, ([^:]+):\*\*\s*(.+)', md_text, flags=re.S)
    end_when, end_text = m.group(1).strip(), ' '.join(m.group(2).split())
    return want, fear, rows, end_when, end_text


def box_h(text, wrap=WRAP):
    return 12 + 12 + 6 + len(textwrap.wrap(text, wrap)) * LH + 6


def box(out, x, y, w, h, cls, head, text, right_head=None, wrap=WRAP, marker=None):
    out.append('<rect class="%s" x="%s" y="%s" width="%s" height="%s" rx="6"/>' % (cls, x, y, w, h))
    out.append('<text class="m-h" x="%s" y="%s">%s</text>' % (x + 10, y + 19, esc(head)))
    if right_head:
        rx = x + w - 10
        if marker:
            mx = rx - len(right_head) * 6.3 - 9
            out.append('<circle class="m-mk m-mk-%s" cx="%s" cy="%s" r="3.6"/>' % (marker, round(mx, 1), y + 15.5))
        out.append('<text class="m-h m-hr" x="%s" y="%s" text-anchor="end">%s</text>' % (rx, y + 19, esc(right_head)))
    ty = y + 12 + 12 + 6 + 11
    for i, ln in enumerate(textwrap.wrap(text, wrap)):
        out.append('<text class="m-t" x="%s" y="%s">%s</text>' % (x + 10, ty + i * LH, esc(ln)))


def arrow(out, x1, y1, x2, y2):
    """Axis-aligned arrow with a small head at (x2, y2)."""
    out.append('<line class="m-arrow" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (x1, y1, x2, y2))
    s = 4.5
    if x1 == x2:
        d = 1 if y2 > y1 else -1
        pts = [(x2, y2), (x2 - s, y2 - d * s * 1.6), (x2 + s, y2 - d * s * 1.6)]
    else:
        d = 1 if x2 > x1 else -1
        pts = [(x2, y2), (x2 - d * s * 1.6, y2 - s), (x2 - d * s * 1.6, y2 + s)]
    out.append('<polygon class="m-head" points="%s"/>' % ' '.join('%s,%s' % (round(a, 1), round(b, 1)) for a, b in pts))


def draw(md_text, name, svg_id):
    want, fear, rows, end_when, end_text = parse(md_text)
    out = []
    y = 8
    h0 = max(box_h(want), box_h(fear))
    box(out, XL, y, CW, h0, 'm-box m-want', 'HE WANTS', want)
    box(out, XR, y, CW, h0, 'm-box', 'HE IS AFRAID OF', fear)
    y += h0
    prev_bottom = y
    tag = {'Yes': ('GETS IT', 'yes'), 'Half': ('HALF', 'half'), 'No': ("DOESN'T", 'no')}
    then_label = None
    for r in rows:
        ya = prev_bottom + 46
        cx = XL + CW / 2
        arrow(out, cx, prev_bottom, cx, ya - 2)
        if then_label:
            out.append('<text class="m-then" x="%s" y="%s">%s</text>' % (cx + 12, prev_bottom + 27, esc(then_label)))
        when = re.sub(r'^Act \w+, ', '', r['when']).upper()
        ha = max(box_h(r['tries']), box_h(r['stops']))
        box(out, XL, ya, CW, ha, 'm-box', 'HE TRIES', r['tries'], right_head=when)
        box(out, XR, ya, CW, ha, 'm-box m-stop', 'WHAT STOPS HIM', r['stops'])
        arrow(out, XL + CW, ya + ha / 2, XR - 2, ya + ha / 2)
        yb = ya + ha + 26
        hb = max(box_h(r['leaves']), box_h(r['so']))
        arrow(out, XR + CW / 2, ya + ha, XR + CW / 2, yb - 2)
        t, mk = tag[r['gets']]
        box(out, XR, yb, CW, hb, 'm-box', 'SO HE', r['so'])
        box(out, XL, yb, CW, hb, 'm-box m-res m-res-' + mk, 'IT LEAVES HIM', r['leaves'], right_head=t, marker=mk)
        arrow(out, XR, yb + hb / 2, XL + CW + 2, yb + hb / 2)
        prev_bottom = yb + hb
        then_label = r['then']
    ye = prev_bottom + 46
    cx = XL + CW / 2
    arrow(out, cx, prev_bottom, cx, ye - 2)
    out.append('<text class="m-then" x="%s" y="%s">%s</text>' % (cx + 12, prev_bottom + 27, esc(then_label)))
    he = box_h(end_text, 62)
    box(out, XL, ye, W - 2 * XL, he, 'm-end', 'WHERE HE ENDS', end_text, right_head=end_when.upper(), wrap=62)
    H = ye + he + 8
    label = ("%s's map, read top to bottom. He wants to be believed. Seven times he goes after it; "
             "each time something stops him, he answers it, and it leaves him somewhere. He gets it once fully, "
             "once by half, and ends without needing it." % name)
    svg = ('<svg id="%s" viewBox="0 0 %d %d" role="img" aria-label="%s">' % (svg_id, W, H, html.escape(label))
           + ''.join(out) + '</svg>')
    return svg
