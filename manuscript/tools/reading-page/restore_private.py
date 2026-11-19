"""Rebuild the private files the reading page needs, in a new session where they are gone.

Usage: python3 restore_private.py PUBLISHED.html CORRECTED.txt

PUBLISHED.html is the reading page as the Artifact tool saves it when it reads the artifact.
CORRECTED.txt is the Doc as `tools/consistency-pass/doc_sync.py dump` writes it.

It writes, under drafts/_private/ (which git ignores):
  book.json            every paragraph of the Doc as it is now, with the margin mark the
                       published Book tab gives it (new, changed, moved, or none)
  CHANGES.html         the Changes tab, as published
  readers/NN-name.html one file for each report on the Readers tab, as published

build_page.py reads book.json as it stands. It does not yet read CHANGES.html or the .html
reports: that is the next change to make there. Reports written in a new session go beside
them as NN-name.md.
It prints every paragraph where the Doc and the published Book tab disagree. Those are edits
made to the Doc since the page was last built.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
PRIV = os.path.normpath(HERE + '../../drafts/_private') + '/'
NB = ' '


def section(page, name):
    a = page.index('<section id="view-%s"' % name)
    b = page.index('</section>', a)
    return page[a:b]


def plain(fragment):
    return html.unescape(re.sub(r'<[^>]+>', '', fragment))


def main(published, corrected):
    page = open(published).read()
    paras = open(corrected).read().split('\n')
    if paras and paras[-1] == '':
        paras.pop()

    # ---- the Book tab: one row per paragraph, in order
    book = section(page, 'book')
    book = book[book.index('<div class="booktext">'):]
    rows = re.findall(r'<(h2|h3|p)((?: [a-z-]+="[^"]*")*)>(.*?)</\1>', book, flags=re.S)
    bare = lambda t: t.replace('[[i]]', '').replace('[[/i]]', '')
    a = next(i for i, p in enumerate(paras) if bare(p) == "Author's Note")
    b = next(i for i, p in enumerate(paras) if bare(p).startswith('Next book:'))
    out = [[p, ''] for p in paras]
    differ = []
    if len(rows) != b - a:
        print('Book tab has %d rows, the Doc has %d paragraphs in the same stretch.' % (len(rows), b - a))
    for k, (tag, attrs, inner) in enumerate(rows[:b - a]):
        text = paras[a + k]
        m = re.search(r'mk-(new|changed|moved)', attrs)
        mark = m.group(1) if m else ''
        is_break = 'class="brk"' in attrs
        same = (is_break and (bare(text) == NB or not bare(text).strip())) or plain(inner) == bare(text)
        if same:
            out[a + k][1] = mark
        else:
            differ.append((a + k + 1, plain(inner)[:70], bare(text)[:70]))
    json.dump(out, open(PRIV + 'book.json', 'w'), ensure_ascii=False)
    marked = sum(1 for _, mk in out if mk)
    print('book.json: %d paragraphs, %d carry a mark' % (len(out), marked))
    for line, was, now in differ:
        print('  differs at line %d\n    page: %s\n    doc:  %s' % (line, was, now))

    # ---- the Changes tab
    changes = section(page, 'changes')
    changes = changes[changes.index('</h1>') + 5:].strip()
    open(PRIV + 'CHANGES.html', 'w').write(changes)
    print('CHANGES.html: %d bytes' % len(changes))

    # ---- the Readers tab
    os.makedirs(PRIV + 'readers', exist_ok=True)
    readers = section(page, 'readers')
    reps = re.findall(r'<details class="rep"><summary>(\d+)\. (.*?)</summary><div class="prose repbody">(.*?)</div></details>',
                      readers, flags=re.S)
    for num, title, body in reps:
        slug = re.sub(r'[^a-z0-9]+', '-', html.unescape(title).lower()).strip('-')[:40].strip('-')
        name = '%02d-%s.html' % (int(num), slug)
        open(PRIV + 'readers/' + name, 'w').write('<!-- %s -->\n%s\n' % (html.unescape(title), body))
    print('readers: %d reports' % len(reps))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
