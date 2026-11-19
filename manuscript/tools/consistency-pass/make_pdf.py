"""Make a reading PDF of the manuscript after the pass.

Usage: python3 make_pdf.py <drafts/_private folder> <out.html>
Then print the HTML to PDF with make_pdf.cjs. The PDF holds manuscript text: keep it out of git.
"""
import html
import json
import re
import sys

private, out = sys.argv[1].rstrip('/') + '/', sys.argv[2]
paras = json.load(open(private + 'book.json'))
a = next(i for i, p in enumerate(paras) if p[0] == "Author's Note")
b = next(i for i, p in enumerate(paras) if p[0].startswith('Next book:'))
head = re.compile(r"^(Author's Note|Act \w+: .*|Chapter \d+: .*|Meanwhile|Afterword: .*)$")


def inline(t):
    return html.escape(t, quote=False).replace('[[i]]', '<em>').replace('[[/i]]', '</em>')


rows, prev, skip_caption = [], '', False
for text, _ in paras[a:b]:
    bare = text.replace('[[i]]', '').replace('[[/i]]', '')
    if head.match(bare):
        if bare.startswith('Act '):
            rows.append('<section class="act"><h1>%s</h1></section>' % html.escape(bare))
        elif bare.startswith('Chapter '):
            num, title = bare.split(': ', 1)
            rows.append('<h2><span>%s</span>%s</h2>' % (html.escape(num), html.escape(title)))
        elif bare.startswith('Afterword'):
            rows.append('<h2><span>Afterword</span>%s</h2>' % html.escape(bare.split(': ', 1)[1]))
        else:
            rows.append('<h2>%s</h2>' % html.escape(bare))
        prev = 'head'
    elif bare == ' ' or not bare.strip():
        rows.append('<p class="brk">&#8226;</p>')
        prev = 'brk'
    elif bare.startswith('[Figure:'):
        skip_caption = True      # text only: no picture placeholders and no captions
    elif skip_caption:
        skip_caption = False
    elif re.match(r'^[A-Z][A-Za-z\' ]{2,60}$', bare) and prev != 'head' and len(bare) < 50 and bare in (
            'Listen to the words between the lines', "We don't have to live like this", 'Food first', 'Get involved'):
        rows.append('<h3>%s</h3>' % html.escape(bare))
        prev = 'head'
    else:
        cls = ' class="first"' if prev in ('head', 'brk') else ''
        rows.append('<p%s>%s</p>' % (cls, inline(text)))
        prev = 'p'

doc = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Surviving the Singularity</title><style>
@page { size: 6in 9in; margin: 0.8in 0.7in 0.85in; }
html { font-family: "Liberation Serif", "DejaVu Serif", Georgia, "Times New Roman", serif; font-size: 11pt; line-height: 1.42; color: #111; }
body { margin: 0; }
.title { height: 7.2in; display: flex; flex-direction: column; justify-content: center; text-align: center; page-break-after: always; }
.title h1 { font-size: 26pt; line-height: 1.15; margin: 0 0 14pt; letter-spacing: .02em; }
.title p { text-indent: 0; text-align: center; }
.title .sub { font-style: italic; font-size: 13pt; margin: 0 0 10pt; }
.title .genre { font-size: 10pt; letter-spacing: .14em; text-transform: uppercase; margin: 0 0 40pt; }
.title .by { font-size: 12pt; margin: 0 0 6pt; }
.title .ver { font-size: 9pt; color: #555; margin: 30pt 0 0; }
.act { page-break-before: always; page-break-after: always; height: 7in; display: flex; align-items: center; justify-content: center; }
.act h1 { font-size: 20pt; font-weight: normal; letter-spacing: .08em; text-transform: uppercase; margin: 0; text-align: center; }
h2 { page-break-before: always; font-size: 17pt; line-height: 1.2; font-weight: bold; text-align: center; margin: 1.1in 0 0.5in; }
.act + h2 { page-break-before: auto; }
h2 span { display: block; font-size: 10pt; font-weight: normal; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 8pt; color: #333; }
h3 { font-size: 12pt; margin: 18pt 0 6pt; page-break-after: avoid; }
p { margin: 0; text-indent: 1.4em; text-align: left; orphans: 2; widows: 2; }
p.first { text-indent: 0; }
p.brk { text-indent: 0; text-align: center; margin: 12pt 0; page-break-after: avoid; }
p.fig { text-indent: 0; font-size: 9pt; color: #555; text-align: center; margin: 12pt 0 2pt; page-break-after: avoid; }
p.cap { text-indent: 0; font-size: 9.5pt; font-style: italic; text-align: center; margin: 0 0 12pt; }
em { font-style: italic; }
</style></head><body>
<section class="title"><h1>SURVIVING THE SINGULARITY</h1><p class="genre">A Solarpunk Novel</p><p class="by">Christopher Tavolazzi</p><p class="ver">Revised manuscript, 19 November 2026</p></section>
''' + '\n'.join(rows) + '\n</body></html>\n'
open(out, 'w').write(doc)
print('paragraphs', len(rows))
