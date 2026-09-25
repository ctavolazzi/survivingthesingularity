"""Generate print variants of the book's dark SVG figures.

The website keeps the dark originals. The letter and 6x9 builds use these:
light paper palette, frame removed, viewBox cropped to the content, and
labels enlarged as far as each figure allows without a new collision.

Enlargement is measured, not guessed. Each figure is loaded in Chrome,
every label gets a target scale, and any label that comes closer to another
label than before (or than 2 units), loses its margin inside a box (keeping
up to 6 units), runs into a box it was clear of, covers more of any line,
arrow or curve than it did, or leaves the frame, is stepped back toward its
original size until nothing new collides. Stacked lines of one label share a
scale, and no label ends larger than one that started larger.

    python3 docs/v0.9.2/print_figures.py            # write static/book-images/print/
    python3 docs/v0.9.2/print_figures.py --check    # also run the negative control
    python3 docs/v0.9.2/print_figures.py --audit    # list defects in the originals
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / 'src/lib/data/book'
IMAGES = ROOT / 'static/book-images'
OUT = IMAGES / 'print'
REPORT = ROOT / 'docs/v0.9.2/print-figures.json'
SVG_NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)

TARGET = 1.4      # label scale tried first
CAP = 22          # no label is enlarged past this; titles are big enough already
PAD = 12          # user units of margin kept around the content

# Dark screen palette to light print palette. Shapes and text map separately:
# a light ink on a dark card becomes a dark ink on paper, and an accent used
# for text is darkened further than the same accent used for a line.
SHAPE = {
    '#020617': '#ffffff', '#0f172a': '#f1f5f9', '#1e293b': '#cbd5e1',
    '#334155': '#94a3b8', '#475569': '#64748b', '#64748b': '#475569',
    '#94a3b8': '#64748b', '#f1f5f9': '#0f172a', '#f59e0b': '#d97706',
    '#d97706': '#d97706', '#3b82f6': '#2563eb', '#c2410c': '#c2410c',
    '#ef4444': '#dc2626', '#f87171': '#dc2626', '#22c55e': '#16a34a',
    '#78350f': '#78350f', '#1a1005': '#fef3c7', '#1a1206': '#fef3c7',
    '#1a0a08': '#fee2e2', '#7f1d1d': '#dc2626',
}
TEXT = {
    '#020617': '#020617', '#0f172a': '#0f172a', '#1e293b': '#1e293b',
    '#f1f5f9': '#0f172a', '#94a3b8': '#334155', '#64748b': '#475569',
    '#475569': '#475569', '#334155': '#334155', '#f59e0b': '#b45309',
    '#d97706': '#b45309', '#3b82f6': '#1d4ed8', '#c2410c': '#c2410c',
    '#ef4444': '#b91c1c', '#f87171': '#b91c1c', '#22c55e': '#15803d',
}
COLOR_ATTRS = ('fill', 'stroke', 'stop-color')
TEXTY = {'text', 'tspan'}
SHAPES = {'rect', 'circle', 'ellipse', 'line', 'path', 'polygon', 'polyline', 'use', 'image'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def print_variant(name):
    """The print copy of a figure, for the print builds. Refuses a stale copy:
    the source and the print file must both match what the last run recorded."""
    report = json.loads(REPORT.read_text())['figures']
    record = report.get(name)
    if record is None:
        raise SystemExit(f'No print copy of {name}; run docs/v0.9.2/print_figures.py')
    if record['source_sha256'] != sha(IMAGES / name) or record['print_sha256'] != sha(OUT / name):
        raise SystemExit(f'Print copy of {name} is stale; run docs/v0.9.2/print_figures.py')
    return OUT / name


def local(tag):
    return tag.rsplit('}', 1)[-1]


def figures_in_book():
    names = set()
    for md in sorted(BOOK.glob('[0-9][0-9]-*.md')):
        names.update(re.findall(r'\]\(/book-images/([^)\s]+\.svg)\)', md.read_text()))
    return sorted(names)


def remap(value, table, where):
    key = value.strip().lower()
    if key in ('none', 'currentcolor') or key.startswith('url('):
        return value
    if key not in table:
        raise SystemExit(f'Unmapped color {value!r} in {where}')
    return table[key]


def recolor(svg_text, name):
    root = ET.fromstring(svg_text)
    parents = {c: p for p in root.iter() for c in p}

    def has(el, kinds):
        return any(local(d.tag) in kinds for d in el.iter() if d is not el)

    for el in root.iter():
        tag = local(el.tag)
        for attr in COLOR_ATTRS:
            if attr not in el.attrib:
                continue
            value = el.attrib[attr]
            if tag in TEXTY:
                el.attrib[attr] = remap(value, TEXT, name)
            elif tag == 'g' and attr == 'fill' and has(el, TEXTY):
                # A group fill reaches both its labels and its shapes. Push the
                # text reading down onto labels that don't set their own fill.
                for d in el.iter():
                    if local(d.tag) == 'text' and 'fill' not in d.attrib and not any(
                            'fill' in a.attrib for a in ancestors(d, parents, stop=el)):
                        d.attrib['fill'] = remap(value, TEXT, name)
                el.attrib[attr] = remap(value, SHAPE, name)
            else:
                el.attrib[attr] = remap(value, SHAPE, name)
    return ET.tostring(root, encoding='unicode')


def ancestors(el, parents, stop):
    out = []
    p = parents.get(el)
    while p is not None and p is not stop:
        out.append(p)
        p = parents.get(p)
    return out


# Runs in the page. Returns the finished SVG and what it did.
FIT_JS = r"""
([TARGET, CAP, PAD, FORCE]) => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const frame = {x: vb.x, y: vb.y, w: vb.width, h: vb.height};
  // Remove the dark card the figure sits on; paper is the card now.
  for (const r of svg.querySelectorAll(':scope > rect')) {
    const b = r.getBBox();
    if (b.x <= frame.x + 2 && b.y <= frame.y + 2 && b.width >= frame.w - 4 && b.height >= frame.h - 4) { r.remove(); break; }
  }
  const rootInv = svg.getScreenCTM().inverse();
  const toRoot = el => rootInv.multiply(el.getScreenCTM());
  const box = el => {
    const b = el.getBBox(), m = toRoot(el);
    const pts = [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y]) => {
      const p = new DOMPoint(x, y).matrixTransform(m); return [p.x, p.y]; });
    const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
    return {x0: Math.min(...xs), y0: Math.min(...ys), x1: Math.max(...xs), y1: Math.max(...ys)};
  };
  const live = el => !el.closest('defs, marker, pattern, clipPath, mask');
  const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && live(t));
  const boxes = [...svg.querySelectorAll('rect, circle, ellipse')].filter(live).map(box);
  // Every stroke and outline, sampled as points in root coordinates.
  const marks = [];
  for (const g of svg.querySelectorAll('line, path, polyline, polygon, circle, ellipse, rect')) {
    if (!live(g) || !g.getTotalLength) continue;
    const cs = getComputedStyle(g);
    if (cs.stroke === 'none' && g.tagName !== 'circle') continue;
    const m = toRoot(g), L = g.getTotalLength(), pts = [];
    for (let d = 0; d <= L; d += 2.5) { const q = g.getPointAtLength(d).matrixTransform(m); pts.push([q.x, q.y]); }
    marks.push(pts);
  }
  const base = texts.map(t => parseFloat(getComputedStyle(t).fontSize));
  const baseLS = texts.map(t => { const v = getComputedStyle(t).letterSpacing; return v === 'normal' ? 0 : parseFloat(v); });
  const apply = s => texts.forEach((t, i) => {
    const size = Math.max(base[i], Math.min(base[i] * s[i], Math.max(base[i], CAP)));
    t.setAttribute('font-size', +size.toFixed(2));
    if (baseLS[i]) t.setAttribute('letter-spacing', +(baseLS[i] * size / base[i]).toFixed(2));
  });
  const sizeNow = i => parseFloat(texts[i].getAttribute('font-size'));
  // The line box has room above the capitals; trim it to where ink can be.
  const ink = b => { const h = b.y1 - b.y0; return {x0: b.x0, x1: b.x1, y0: b.y0 + 0.15*h, y1: b.y1 - 0.03*h}; };
  const gap = (a, b) => Math.max(b.x0 - a.x1, a.x0 - b.x1, b.y0 - a.y1, a.y0 - b.y1);
  const clearance = (a, b) => Math.min(a.x0 - b.x0, b.x1 - a.x1, a.y0 - b.y0, b.y1 - a.y1);
  const touches = (a, b) => a.x0 < b.x1 && b.x0 < a.x1 && a.y0 < b.y1 && b.y0 < a.y1;
  const covered = (b, pts) => { let n = 0; for (const [x, y] of pts) if (x > b.x0 - 1.5 && x < b.x1 + 1.5 && y > b.y0 - 1.5 && y < b.y1 + 1.5) n++; return n; };
  const snapshot = () => {
    const tb = texts.map(t => ink(box(t)));
    return {
      tb,
      tt: tb.map((a, i) => tb.map((b, j) => j > i ? gap(a, b) : null)),
      tr: tb.map(a => boxes.map(r => touches(a, r) ? clearance(a, r) : null)),
      tm: tb.map(a => marks.map(pts => covered(a, pts))),
    };
  };
  apply(texts.map(() => 1));
  const B = snapshot();
  const violations = () => {
    const S = snapshot(), v = [];
    S.tb.forEach((b, i) => {
      if (b.x0 < frame.x + 4 || b.x1 > frame.x + frame.w - 4 || b.y0 < frame.y + 4 || b.y1 > frame.y + frame.h - 4) v.push(['out', i]);
      for (let j = i + 1; j < S.tb.length; j++) {
        // Labels side by side on one line need a word space; stacked lines need 2 units.
        const a = S.tb[j], sameLine = b.y0 < a.y1 && a.y0 < b.y1;
        const need = sameLine ? 0.8 * Math.max(sizeNow(i), sizeNow(j)) : 2;
        if (S.tt[i][j] < Math.min(B.tt[i][j], need) - 0.1) v.push(['tt', i, j]);
      }
      S.tr[i].forEach((c, k) => {
        const c0 = B.tr[i][k];
        if (c === null) return;                                   // not touching this box now
        if (c0 === null) { v.push(['tr', i]); return; }           // grew into a box it was clear of
        if (c < Math.min(c0, 6) - 0.25) v.push(['tr', i]);        // lost its margin inside a box
      });
      S.tm[i].forEach((n, k) => { if (n > B.tm[i][k]) v.push(['tm', i]); });
    });
    return v;
  };
  let s = texts.map(() => TARGET), left = [];
  for (let iter = 0; iter < 60; iter++) {
    apply(s);
    left = violations();
    if (!left.length) break;
    const idx = new Set(left.flatMap(([, a, b]) => b === undefined ? [a] : [a, b]));
    let moved = false;
    for (const i of idx) if (s[i] > 1) { s[i] = Math.max(1, +(s[i] - 0.05).toFixed(2)); moved = true; }
    if (!moved) break;
  }
  // Lines of one label (same x, anchor and size, stacked) share the smallest scale.
  const key = t => [t.getAttribute('x'), getComputedStyle(t).textAnchor].join('|');
  for (let i = 0; i < texts.length; i++) for (let j = 0; j < texts.length; j++) {
    if (i === j || key(texts[i]) !== key(texts[j]) || base[i] !== base[j]) continue;
    const dy = Math.abs(parseFloat(texts[i].getAttribute('y')) - parseFloat(texts[j].getAttribute('y')));
    if (dy > 0 && dy <= 2.4 * base[i]) s[i] = s[j] = Math.min(s[i], s[j]);
  }
  // Keep the hierarchy: nothing ends larger than a label that started larger.
  const size = i => Math.max(base[i], Math.min(base[i] * s[i], Math.max(base[i], CAP)));
  for (let pass = 0; pass < 3; pass++) for (let i = 0; i < texts.length; i++) for (let j = 0; j < texts.length; j++)
    if (base[i] < base[j] && size(i) > size(j)) s[i] = size(j) / base[i];
  if (FORCE) s = texts.map(() => FORCE);
  apply(s);
  const after = violations();
  const c = svg.getBBox();
  svg.setAttribute('viewBox', [c.x - PAD, c.y - PAD, c.width + 2*PAD, c.height + 2*PAD].map(n => +n.toFixed(1)).join(' '));
  svg.removeAttribute('width'); svg.removeAttribute('height');
  const sizes = texts.map((t, i) => size(i));
  return {svg: new XMLSerializer().serializeToString(svg), new_collisions: after.map(x => x.join(':')),
          labels: texts.length, marks: marks.length,
          min_base: Math.min(...base), min_final: +Math.min(...sizes).toFixed(2),
          median_scale: +[...sizes.map((z, i) => z / base[i])].sort((a,b)=>a-b)[Math.floor(sizes.length/2)].toFixed(2),
          frame_width: frame.w, crop_width: +(c.width + 2*PAD).toFixed(1)};
}
"""


# Drawn this way on purpose, so the audit doesn't report them.
ALLOWED = {
    ('ch08-star-vs-mesh.svg', 'a line crosses: "HUB"'): 'the hub is struck through: it dies',
    ('intro-food-insecurity.svg', 'label reaches its box edge: "RECESSION"'): 'names the shaded band it sits in',
    ('ch17-lora-node.svg', 'a line crosses: "5W SOLAR PV PANEL"'): 'set on a halo over the panel grid',
    ('ch17-lora-node.svg', 'a line crosses: "paperback-sized, roof of the case"'): 'set on a halo over the panel grid',
}

# Lists what is already wrong in an original figure, by label text.
AUDIT_JS = r"""
() => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const frame = {x: vb.x, y: vb.y, w: vb.width, h: vb.height};
  const rootInv = svg.getScreenCTM().inverse();
  const toRoot = el => rootInv.multiply(el.getScreenCTM());
  const box = el => {
    const b = el.getBBox(), m = toRoot(el);
    const pts = [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y]) => {
      const p = new DOMPoint(x, y).matrixTransform(m); return [p.x, p.y]; });
    const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
    return {x0: Math.min(...xs), y0: Math.min(...ys), x1: Math.max(...xs), y1: Math.max(...ys)};
  };
  const live = el => !el.closest('defs, marker, pattern, clipPath, mask');
  const bg = [...svg.querySelectorAll(':scope > rect')].find(r => { const b = r.getBBox();
    return b.x <= frame.x + 2 && b.y <= frame.y + 2 && b.width >= frame.w - 4 && b.height >= frame.h - 4; });
  const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && live(t));
  const ink = b => { const h = b.y1 - b.y0; return {x0: b.x0, x1: b.x1, y0: b.y0 + 0.15*h, y1: b.y1 - 0.03*h}; };
  const tb = texts.map(t => ink(box(t)));
  const name = i => texts[i].textContent.trim().slice(0, 40);
  const out = [];
  for (let i = 0; i < tb.length; i++) for (let j = i + 1; j < tb.length; j++) {
    const a = tb[i], b = tb[j];
    if (a.x0 < b.x1 - 1 && b.x0 < a.x1 - 1 && a.y0 < b.y1 - 1 && b.y0 < a.y1 - 1) out.push(`labels overlap: "${name(i)}" / "${name(j)}"`);
  }
  for (const r of svg.querySelectorAll('rect, circle, ellipse')) {
    if (r === bg || !live(r)) continue;
    const b = box(r);
    tb.forEach((a, i) => {
      const cx = (a.x0 + a.x1) / 2, cy = (a.y0 + a.y1) / 2;
      const centred = cx > b.x0 && cx < b.x1 && cy > b.y0 && cy < b.y1;
      if (centred && (a.x0 < b.x0 + 2 || a.x1 > b.x1 - 2)) out.push(`label reaches its box edge: "${name(i)}"`);
    });
  }
  for (const g of svg.querySelectorAll('line, path, polyline, polygon')) {
    if (!live(g) || getComputedStyle(g).stroke === 'none') continue;
    const m = toRoot(g), L = g.getTotalLength();
    const hitBy = new Set();
    for (let d = 0; d <= L; d += 2) { const q = g.getPointAtLength(d).matrixTransform(m);
      tb.forEach((a, i) => { if (q.x > a.x0 && q.x < a.x1 && q.y > a.y0 && q.y < a.y1) hitBy.add(i); }); }
    for (const i of hitBy) out.push(`a ${g.tagName} crosses: "${name(i)}"`);
  }
  return [...new Set(out)];
}
"""


def fit(page, svg_text, force=0):
    page.set_content('<!doctype html><html><body style="margin:0;background:#fff">'
                     + svg_text.replace('<svg ', '<svg width="900" ', 1) + '</body></html>')
    return page.evaluate(FIT_JS, [TARGET, CAP, PAD, force])


def main():
    from playwright.sync_api import sync_playwright
    check = '--check' in sys.argv
    names = figures_in_book()
    if '--audit' in sys.argv:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel='chrome')
            page = browser.new_page(viewport={'width': 1000, 'height': 1000})
            total = 0
            for name in names:
                page.set_content('<!doctype html><body style="margin:0">'
                                 + (IMAGES / name).read_text().replace('<svg ', '<svg width="900" ', 1))
                found = [f for f in page.evaluate(AUDIT_JS) if (name, f) not in ALLOWED]
                total += len(found)
                for line in found:
                    print(f'{name}: {line}')
            browser.close()
        print(f'{total} problems in {len(names)} original figures ({len(ALLOWED)} intentional, allowed)')
        sys.exit(1 if total else 0)
    OUT.mkdir(exist_ok=True)
    report = {'target_scale': TARGET, 'cap_px': CAP, 'figures': {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome')
        page = browser.new_page(viewport={'width': 1000, 'height': 1000})
        if check:
            # Negative control: force every label to 1.8x in a dense figure;
            # the collision measure has to see it.
            src = recolor((IMAGES / 'ch09-cnc-bed.svg').read_text(), 'control')
            forced = fit(page, src, force=1.8)
            assert forced['new_collisions'], 'Negative control failed: forced enlargement reported clean'
            print(f"negative control: {len(forced['new_collisions'])} collisions detected at forced 1.8x")
        for name in names:
            src = recolor((IMAGES / name).read_text(), name)
            result = fit(page, src)
            if result['new_collisions']:
                raise SystemExit(f'{name}: fitting left new collisions {result["new_collisions"]}')
            svg = result.pop('svg')
            (OUT / name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + '\n')
            result.pop('new_collisions')
            result['source_sha256'] = sha(IMAGES / name)
            result['print_sha256'] = sha(OUT / name)
            report['figures'][name] = result
            print(f"{name:34} labels {result['labels']:3}  min {result['min_base']:5.1f} -> {result['min_final']:5.1f}px"
                  f"  median x{result['median_scale']:.2f}  width {result['frame_width']:.0f} -> {result['crop_width']:.0f}")
        browser.close()
    report['count'] = len(report['figures'])
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print(f"wrote {report['count']} print figures to {OUT.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
