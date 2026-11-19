"""Build the reading page (one HTML file) from the novel notes in manuscript/.

Usage: python3 build_page.py [output.html]
Needs the Python package "markdown" (pip install markdown). See README.md beside this file.
"""
import os, re, sys, html

import markdown

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
REPO = os.path.normpath(HERE + '../..') + '/'          # the manuscript/ folder
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE + 'singularity-cast-bible.html'
sys.path.insert(0, HERE)
PROFILES = open(REPO + 'NOVEL-CHARACTER-PROFILES-2026-11-18.md').read()
ARCS = open(REPO + 'NOVEL-CHARACTER-ARCS-2026-11-18.md').read()
AUDIT = open(REPO + 'NOVEL-CONSISTENCY-AUDIT-2026-11-18.md').read()
DRIVE = open(REPO + 'NOVEL-DRIVE-FINDINGS-2026-11-19.md').read()
SCENE = open(REPO + 'drafts/draft-elijah-crash-out-arc.md').read()
LATER = open(REPO + 'drafts/draft-later-chapters-36-37-39.md').read()
# Made by tools/consistency-pass/apply.py. It quotes the manuscript, so it is kept out of git.
_changes = REPO + 'drafts/_private/CHANGES.md'
CHANGES = open(_changes).read() if os.path.exists(_changes) else '# Changes\n\nNot built in this copy. Run tools/consistency-pass/apply.py first.\n'
BEATS = open(REPO + 'NOVEL-BEATS-2026-11-19.md').read()
STRUCT = open(REPO + 'NOVEL-STRUCTURE-2026-11-19.md').read()
MAPE = open(REPO + 'NOVEL-MAP-ELIJAH-2026-11-19.md').read()
MAPALL = open(REPO + 'NOVEL-MAP-EVERYONE-2026-11-19.md').read()
import map_svg
import bigmap


def md(text, prefix=None):
    text = re.sub(r'\n(?=(1\. |- ))', lambda m: '\n\n', re.sub(r'\n\n+', '\n\n', text)) if False else text
    out = markdown.markdown(text, extensions=['tables', 'sane_lists', 'toc'])
    out = out.replace('<table>', '<div class="tbl"><table>').replace('</table>', '</table></div>')
    if prefix:
        out = re.sub(r'id="', 'id="%s-' % prefix, out)
    else:
        out = re.sub(r' id="[^"]*"', '', out)
    return out


def md_block(text):
    """Markdown for one labelled block: make sure a list that follows a line of text is seen as a list."""
    lines = text.strip('\n').split('\n')
    fixed = []
    for i, ln in enumerate(lines):
        is_item = re.match(r'(\d+\. |- )', ln)
        if is_item and fixed and fixed[-1].strip() and not re.match(r'(\d+\. |- |\s)', fixed[-1]):
            fixed.append('')
        fixed.append(ln)
    return md('\n'.join(fixed))


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


LABEL = re.compile(r'^\*\*((?:Portrait[^*]*?)|Reads as|Voice|His plate|Her plate|Their plate|Its plate|Blank|Suggestions|Suggestion)\.\*\*[ \t]*')
KIND = {'Reads as': 'reads', 'Voice': 'voice', 'Blank': 'blank', 'Suggestions': 'sugg', 'Suggestion': 'sugg'}


def parse_entry(body):
    sections = []  # [label, kind, text]
    for block in re.split(r'\n\s*\n', body.strip('\n')):
        if not block.strip():
            continue
        m = LABEL.match(block)
        if m:
            label = m.group(1)
            if label.startswith('Portrait'):
                kind = 'portrait'
            elif label.endswith('plate'):
                kind = 'plate'
            else:
                kind = KIND[label]
            sections.append([label, kind, block[m.end():]])
        else:
            if not sections:
                sections.append(['', 'portrait', block])
            else:
                sections[-1][2] += '\n\n' + block
    return sections


def render_voice(text):
    flat = ' '.join(text.split())
    quotes = re.findall(r'"[^"]+"', flat)
    rest = re.sub(r'"[^"]+"', '', flat).strip()
    if quotes and not rest:
        return '<ul class="lines">' + ''.join('<li>%s</li>' % html.escape(q.strip('"')) for q in quotes) + '</ul>'
    return md_block(text)


def render_entry(name, part_title, body):
    eid = 'p-' + slug(name)
    out = ['<article class="person" id="%s">' % eid,
           '<p class="eyebrow">%s</p>' % html.escape(part_title),
           '<h2>%s</h2>' % html.escape(name)]
    for label, kind, text in parse_entry(body):
        out.append('<section class="blk %s">' % kind)
        if kind == 'sugg':
            out.append('<h3 class="lbl">%s <span class="mine">mine, for you to change</span></h3>' % html.escape(label))
        elif label:
            out.append('<h3 class="lbl">%s</h3>' % html.escape(label))
        out.append(render_voice(text) if kind == 'voice' else md_block(text))
        out.append('</section>')
    out.append('</article>')
    return eid, '\n'.join(out)


# ---- split the profiles file
part_iter = list(re.finditer(r'^# (Part (\d)\. (.+)|How to use this)\s*$', PROFILES, flags=re.M))
head = PROFILES[:part_iter[0].start()]
chunks = []
for i, m in enumerate(part_iter):
    end = part_iter[i + 1].start() if i + 1 < len(part_iter) else len(PROFILES)
    body = re.sub(r'\n---\s*$', '', PROFILES[m.end():end].strip()).strip()
    chunks.append((m.group(2), m.group(3) or 'How to use this', body))

method_at = head.index('## The method, taken from your old work')
method_md = head[method_at:].strip()
method_md = re.sub(r'\n---\s*$', '', method_md).strip()
legend_md = head[head.index('**How to read a profile**'):method_at]
legend_md = re.sub(r'\n---\s*$', '', legend_md.strip()).strip().replace('**How to read a profile**', '').strip()

people_html, index, count = [], [], 0
rhymes_md, howto_md = '', ''
for num, title, body in chunks:
    if num is None:
        howto_md = body
        continue
    if num == '6':
        rhymes_md = body
        continue
    entries = []
    subs = list(re.finditer(r'^## (.+)\s*$', body, flags=re.M))
    if not subs:
        entries.append((title[0].upper() + title[1:], body))
    else:
        for j, sm in enumerate(subs):
            e_end = subs[j + 1].start() if j + 1 < len(subs) else len(body)
            entries.append((sm.group(1).strip(), body[sm.end():e_end]))
    people_html.append('<div class="part"><p class="partno">Part %s</p><h2 class="parttitle">%s</h2></div>' % (num, html.escape(title)))
    group = []
    for name, ebody in entries:
        ebody = re.sub(r'\n---\s*$', '', ebody.strip())
        eid, h = render_entry(name, title, ebody)
        people_html.append(h)
        group.append((eid, name))
        count += 1
    index.append((title, group))

select = ['<select id="jump" aria-label="Jump to a person"><option value="">Jump to a person…</option>']
toc = ['<nav class="toc" aria-label="People">']
for title, group in index:
    select.append('<optgroup label="%s">' % html.escape(title))
    toc.append('<div class="tocgroup"><p class="lbl">%s</p><ul>' % html.escape(title))
    for eid, name in group:
        select.append('<option value="%s">%s</option>' % (eid, html.escape(name)))
        toc.append('<li><button type="button" class="tocbtn" data-jump="%s">%s</button></li>' % (eid, html.escape(name)))
    select.append('</optgroup>')
    toc.append('</ul></div>')
select.append('</select>')
toc.append('</nav>')


def strip_h1(text):
    return re.sub(r'\A# .*\n', '', text.lstrip())


arcs_html = md(strip_h1(ARCS), 'arcs')
audit_html = md(strip_h1(AUDIT), 'fixes')
drive_html = md(strip_h1(DRIVE), 'drive')
scene_html = md(strip_h1(SCENE), 'scene')
later_html = md(strip_h1(LATER), 'later')
changes_html = md(strip_h1(CHANGES), 'changes')
beats_html = md(strip_h1(BEATS), 'beats')
shape_html = md(strip_h1(STRUCT), 'shape')
map_fig = ('<figure class="mapfig">' + map_svg.draw(MAPE, 'Elijah', 'map-elijah')
           + '<figcaption>Read down. Each pair of rows is one attempt: what he tries, what stops him, what he does about it, and where it leaves him. The heavy box is the wall. The dot says whether he got what he wanted.</figcaption></figure>')
map_text_html = md(strip_h1(MAPE), 'map')
big_svg, big_n = bigmap.draw(MAPALL, 'map-all')
big_fig = ('<figure class="mapfig">' + big_svg
           + '<figcaption>Elijah runs down the left, one amber box for each thing he tries. Everyone else hangs off the point where they come into his story. The line in italics is what they are to him. The heavy bar is what stops them. The mark at the top right says whether they get what they want.</figcaption></figure>')
print('big map people', big_n)

# ---- the rising-and-falling chart, drawn from the table in the structure file
import json
rows = []
for m in re.finditer(r'^\| (\d+) \| ([^|]+) \| ([^|]+) \| ([^|]*)\|\s*$', STRUCT, flags=re.M):
    v = m.group(4).strip()
    rows.append({'c': int(m.group(1)), 't': m.group(2).strip(), 'n': m.group(3).strip(),
                 'v': (int(v) if v else None)})
assert len(rows) == 40, len(rows)
W, H, L, R, T, B = 480, 300, 30, 10, 30, 28
PW, PH = W - L - R, H - T - B
def X(i): return round(L + i * PW / 39, 1)
def Y(v): return round(T + (5 - v) * PH / 10, 1)
KEYS = [(9, '"Correct."'), (14, 'The crash out'), (24, 'First fire'), (31, 'The dark night'),
        (33, 'Believed, and loved'), (36, 'The fire'), (39, 'The bar')]
svg = ['<svg viewBox="0 0 %d %d" role="img" aria-labelledby="shape-title shape-desc" id="shape-svg">' % (W, H),
       '<title id="shape-title">How things stand for Elijah, chapter by chapter</title>',
       '<desc id="shape-desc">A line from chapter 0 to chapter 39 on a scale from minus five to plus five. It falls to minus five at chapters 13 and 14, climbs to plus three at chapter 24, falls to minus four at chapter 31, peaks at plus three at chapter 33, falls to minus four at chapter 36 and ends at plus two.</desc>']
for a, b, name in [(0, 5, 'ONE'), (6, 15, 'TWO'), (16, 31, 'THREE'), (32, 39, 'FOUR')]:
    svg.append('<text class="c-act" x="%s" y="14" text-anchor="middle">%s</text>' % (round((X(a) + X(b)) / 2, 1), name))
for bx in (5.5, 15.5, 31.5):
    svg.append('<line class="c-div" x1="%s" x2="%s" y1="20" y2="%s"/>' % (X(bx), X(bx), T + PH))
for v in (5, -5):
    svg.append('<line class="c-grid" x1="%s" x2="%s" y1="%s" y2="%s"/>' % (L, L + PW, Y(v), Y(v)))
svg.append('<line class="c-zero" x1="%s" x2="%s" y1="%s" y2="%s"/>' % (L, L + PW, Y(0), Y(0)))
for v, lab in ((5, '+5'), (0, '0'), (-5, '-5')):
    svg.append('<text class="c-ax" x="%s" y="%s" text-anchor="end">%s</text>' % (L - 6, Y(v) + 4, lab))
for i in (0, 5, 10, 15, 20, 25, 30, 35, 39):
    svg.append('<text class="c-ax" x="%s" y="%s" text-anchor="middle">%d</text>' % (X(i), H - 8, i))
pts = [(X(r['c']), Y(r['v'])) for r in rows if r['v'] is not None and r['c'] <= 37]
svg.append('<polyline class="c-line" points="%s"/>' % ' '.join('%s,%s' % p for p in pts))
svg.append('<line class="c-gap" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (X(37), Y(rows[37]['v']), X(39), Y(rows[39]['v'])))
svg.append('<line id="shape-hair" class="c-hair" x1="0" x2="0" y1="%s" y2="%s" visibility="hidden"/>' % (T, T + PH))
for n, (c, lab) in enumerate(KEYS, 1):
    v = rows[c]['v']
    dy = -9 if v > 0 else 17
    dx = 0
    if v <= -5:
        dx, dy = -12, -5
    svg.append('<circle class="c-dot" cx="%s" cy="%s" r="5"/>' % (X(c), Y(v)))
    svg.append('<text class="c-key" x="%s" y="%s" text-anchor="middle">%d</text>' % (X(c) + dx, Y(v) + dy, n))
svg.append('<circle id="shape-cur" class="c-cur" cx="0" cy="0" r="5" visibility="hidden"/>')
svg.append('<rect id="shape-hit" x="%s" y="%s" width="%s" height="%s" fill="transparent"/>' % (L - 6, T - 6, PW + 12, PH + 12))
svg.append('</svg>')
keys_html = '<ol class="keys">' + ''.join('<li><span class="kch">Ch %d</span> %s</li>' % (c, html.escape(lab)) for c, lab in KEYS) + '</ol>'
chart_html = ('<figure class="chart" id="shape-chart" tabindex="0" aria-label="Chart. Use the left and right arrow keys to move between chapters.">'
              + ''.join(svg) + '<div class="tip" id="shape-tip" hidden></div>'
              + '<figcaption>How things stand for Elijah at the end of each chapter. Plus five is as good as it gets, minus five is the floor. Chapter 38 is dashed because he is not in it. My read, not a measurement.</figcaption>'
              + keys_html + '</figure>'
              + '<script type="application/json" id="shape-data">' + json.dumps({'rows': rows, 'L': L, 'PW': PW, 'T': T, 'PH': PH, 'W': W}).replace('</', '<\\/') + '</script>')
rhymes_html = md(rhymes_md)
method_html = md(method_md.replace('## The method, taken from your old work', '')) + '<h2>How to use this</h2>' + md(howto_md)
legend_html = md(legend_md)

CSS = open(HERE + 'page.css').read()
JS = open(HERE + 'page.js').read()

page = f'''<title>Singularity Cast Bible</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
{CSS}
</style>

<header class="bar">
  <div class="barin">
    <nav class="tabs" aria-label="Sections">
      <a id="tab-changes" href="#changes">Changes</a>
      <a id="tab-people" href="#people">People</a>
      <a id="tab-map" href="#map">Map</a>
      <a id="tab-drive" href="#drive">Drive</a>
      <a id="tab-scene" href="#scene">Scene</a>
      <a id="tab-later" href="#later">Later</a>
      <a id="tab-beats" href="#beats">Beats</a>
      <a id="tab-shape" href="#shape">Shape</a>
      <a id="tab-rhymes" href="#rhymes">Rhymes</a>
      <a id="tab-arcs" href="#arcs">Arcs</a>
      <a id="tab-fixes" href="#fixes">Fixes</a>
      <a id="tab-method" href="#method">Method</a>
    </nav>
    <div id="jumpwrap">{''.join(select)}</div>
  </div>
</header>

<main class="wrap">

<section id="view-people" class="view">
  <div class="intro">
    <p class="eyebrow">Surviving the Singularity · final rough draft, chapters 0 to 39</p>
    <h1>The cast</h1>
    <p class="lede">{count} profiles, built from your own lines. Serif text is the manuscript. Everything else is commentary. First pass, 18 November 2026.</p>
    <div class="legend">{legend_html}</div>
    {''.join(toc)}
  </div>
  {''.join(people_html)}
</section>

<section id="view-map" class="view prose">
  <p class="eyebrow">19 November 2026 · your rulings counted in</p>
  <h1>The map</h1>
  <p>Two drawings. The first is everyone, on one map. The second is Elijah on his own, in full.</p>
  <p class="mapjump"><button type="button" data-scroll="map-all-h">Everyone</button><button type="button" data-scroll="map-elijah-h">Elijah, in full</button></p>
  <h2 id="map-all-h">Everyone</h2>
  <p><strong>What it shows.</strong> Read the marks down the right side. The four who try to buy it, own it, steer it or force it do not get it. Ruby buys. Bidwell owns. Elijah, in Act Three, steers. Grace ends by wanting it done for people. That is your theme, and it is already in the cast.</p>
  {big_fig}
  <h2 id="map-elijah-h">Elijah, in full</h2>
  {map_fig}
  <h2>Elijah's map in words</h2>
  {map_text_html}
</section>

<section id="view-drive" class="view prose">
  <p class="eyebrow">Search of 19 November 2026</p>
  <h1>What the Drive holds</h1>
  {drive_html}
</section>

<section id="view-scene" class="view prose">
  <p class="eyebrow">Draft, fourth version, 19 November 2026</p>
  <h1>His mother's stroke, the choice, the crash out and the road to the farm</h1>
  {scene_html}
</section>

<section id="view-changes" class="view prose">
  <p class="eyebrow">Consistency pass, 19 November 2026. Not in your Doc yet.</p>
  <h1>What the consistency pass changes</h1>
  {changes_html}
</section>

<section id="view-later" class="view prose">
  <p class="eyebrow">Draft, first version, 19 November 2026</p>
  <h1>Chapters 36, 37 and 39 after the stroke</h1>
  {later_html}
</section>

<section id="view-beats" class="view prose">
  <p class="eyebrow">19 November 2026</p>
  <h1>Beats like the choice</h1>
  {beats_html}
</section>

<section id="view-shape" class="view prose">
  <p class="eyebrow">19 November 2026</p>
  <h1>The shape of the story</h1>
  {chart_html}
  {shape_html}
</section>

<section id="view-rhymes" class="view prose">
  <p class="eyebrow">Already on the page</p>
  <h1>What already rhymes</h1>
  {rhymes_html}
</section>

<section id="view-arcs" class="view prose">
  <p class="eyebrow">First pass</p>
  <h1>Character arcs</h1>
  {arcs_html}
</section>

<section id="view-fixes" class="view prose">
  <p class="eyebrow">Consistency audit</p>
  <h1>The fix list</h1>
  {audit_html}
</section>

<section id="view-method" class="view prose">
  <p class="eyebrow">From The Golden Plates</p>
  <h1>The method, taken from your old work</h1>
  {method_html}
</section>

<footer class="foot">
  <p>The same text lives in the book repo, in <code>manuscript/</code>: <code>NOVEL-CHARACTER-PROFILES</code>, <code>NOVEL-CHARACTER-ARCS</code>, <code>NOVEL-CONSISTENCY-AUDIT</code>, <code>NOVEL-DRIVE-FINDINGS</code>, <code>NOVEL-BEATS</code>, <code>NOVEL-STRUCTURE</code>, <code>NOVEL-MAP-ELIJAH</code>, <code>drafts/draft-elijah-crash-out-arc.md</code> and <code>drafts/draft-later-chapters-36-37-39.md</code>. Nothing here has gone into the manuscript.</p>
</footer>

</main>

<script>
{JS}
</script>
'''
open(OUT, 'w').write(page)
print('wrote', OUT)
print('profiles', count, 'bytes', len(page))
for title, group in index:
    print(' ', title, len(group))
