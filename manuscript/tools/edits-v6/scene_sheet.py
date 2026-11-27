#!/usr/bin/env python3
"""Check the scene sheet against the built book, so the sheet cannot fall behind the edits.

    python3 manuscript/tools/edits-v6/scene_sheet.py check OUT/v6.txt manuscript/novel/scene-sheet.csv
    python3 manuscript/tools/edits-v6/scene_sheet.py scene OUT/v6.txt 52          print scene 52 as it is in the book
    python3 manuscript/tools/edits-v6/scene_sheet.py sheet GSHEET.json manuscript/novel/scene-sheet.csv
                                                    compare a saved read of the Google Sheet with the CSV, cell for cell

OUT/v6.txt is what make_v6.py writes: the book with every logged edit. GSHEET.json is the saved result of the Sheets
connector's get_values on the tab "Scenes".

`check` tests what a script can test. It does not read for meaning. It reports:
  1. Structure: the same sections in the same order, the same number of scenes in each.
  2. Words: each scene's count, and the total.
  3. Opens with: each scene's first words.
  4. On the page: a name in that column that the scene's text never uses.
  5. Numbers on the page: a number in that column that the scene's text does not hold.
  6. Threads: a thread that is not on the fixed list, and the longest silence of each thread.
  7. Questions: one that is closed and was never opened, and one that is opened and never closed.
It exits 1 if 1, 2 or 3 fail, because those mean the sheet is behind the book. 4 to 7 are lists to read.
"""
import csv
import json
import re
import sys

SECTION = re.compile(r"^(Chapter \d+: .*|Meanwhile|Pondwater|Epilogue)$")
STOP = ('About This Book', 'Afterword', 'Appendix', 'Thank You')
THREADS = [
    "The machine (AGI, the labs, the Architect, the bet)", "Elijah and Grace", "Elijah's book and notebooks",
    "Elijah and Ma", "David and the Bear Flag (Ray, the three careers)", "Lou",
    "The boxes and Rod Code (Tyler, the pledge, the network)", "The co-op's money (pay, the trust, the land, votes)",
    "Wes and the band", "The land buyer (Bidwell, the LLC, the parcels)", "Denny's channel", "Ruby and Porchlight",
    "The route and the county (Curtis, Rosa, Mrs. Delgado)", "The arms (Praether)", "The Ochoas", "Irene and Walt",
    "The rovers and Priya's soil", "Wren", "Marta's shoulder and the welder gap", "Grace and fire", "Devendra",
    "Frank and the tool library", "Melody", "Grace's family (Faith, her father)", "Elijah's father",
]
def scenes(path):
    """[(section heading, scene number in it, [paragraphs])] for the body of the book."""
    lines = open(path).read().split('\n')
    start = [i for i, l in enumerate(lines) if l == 'Act One: The Bar'][-1]     # the first one is the contents list
    out, head, buf, n, last_ch = [], None, [], 0, ''

    def flush():
        nonlocal buf, n
        if head and buf:
            n += 1
            out.append((head, n, buf))
        buf = []

    for l in lines[start:]:
        if l in STOP:
            break
        if SECTION.match(l):
            flush()
            if l.startswith('Chapter'):
                last_ch = l.split(':')[0]
            head, n = ('Meanwhile (after %s)' % last_ch if l == 'Meanwhile' else l), 0
        elif l.startswith('Act ') and len(l) < 40:
            flush()
            head = None
        elif not l.strip():
            flush()
        elif head:
            buf.append(l)
    flush()
    return out


def count(paras):
    return sum(len(p.split()) for p in paras)


def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', s.lower().replace('’', "'").replace("'", ''))


NUMWORDS = set('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen '
               'seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million '
               'billion trillion half dozen'.split())


def toks(s):
    """Lower-case words and numbers. "twenty-two" is two words, "2,011.46" is one."""
    s = s.lower().replace('\u2019', "'")
    return [w.strip(".,'") for w in re.findall(r"[a-z']+|\d[\d,.]*", s) if w.strip(".,'")]


def rows_of(path):
    """The sheet's rows, without rows kept only as a record of a cut scene (0 words, What happens starts CUT)."""
    return [r for r in csv.DictReader(open(path, newline=''))
            if not (r['Words'].strip() == '0' and r['What happens'].startswith('CUT'))]


def check(book, sheet):
    sc, rows = scenes(book), rows_of(sheet)
    bad = 0
    print('The book has %d scenes and %d words in them. The sheet has %d rows and %d words.' % (
        len(sc), sum(count(p) for _, _, p in sc), len(rows), sum(int(r['Words']) for r in rows)))

    print('\n1. Structure')
    a = [(h, n) for h, n, _ in sc]
    b = [(r['Chapter'], int(r['Scene'])) for r in rows]
    if a == b:
        print('   The same sections, in the same order, with the same scenes.')
    else:
        bad += 1
        for x in a:
            if x not in b:
                print('   In the book, not on the sheet: %s, scene %d' % x)
        for x in b:
            if x not in a:
                print('   On the sheet, not in the book: %s, scene %d' % x)
    if a != b:
        print('\nThe rest is skipped until the structure matches.')
        return 1
    pairs = list(zip(rows, sc))

    print('\n2. Words')
    off = [(r['#'], r['Chapter'], int(r['Words']), count(p)) for r, (_, _, p) in pairs if int(r['Words']) != count(p)]
    for num, ch, was, now in off:
        print('   Scene %s (%s): the sheet says %d, the book has %d' % (num, ch.split(':')[0], was, now))
    print('   %d of %d differ.' % (len(off), len(pairs)))
    bad += bool(off)

    print('\n3. Opens with')
    n = 0
    for r, (_, _, p) in pairs:
        want = norm(r['Opens with'].rstrip('. ').rstrip('…'))[:60]
        if not norm(p[0]).startswith(want):
            n += 1
            print('   Scene %s: sheet "%s" | book "%s"' % (r['#'], r['Opens with'][:70], p[0][:70]))
    print('   %d of %d differ.' % (n, len(pairs)))
    bad += bool(n)

    print('\n4. On the page: names the scene never uses')
    skip = {'elijah', 'the', 'and', 'in', 'on', 'by', 'of', 'a', 'his', 'her', 'flashback', 'phone', 'text', 'voice',
            'voicemail', 'email', 'screen', 'video', 'narrator', 'only', 'mentioned', 'crowd', 'others', 'unnamed'}
    for r, (_, _, p) in pairs:
        text = norm(' '.join(p))
        miss = []
        for name in re.split(r'[,;()]| and ', r['On the page']):
            words = [w for w in norm(name).split() if w not in skip and len(w) > 2]
            if words and not any(w in text for w in words):
                miss.append(name.strip())
        if miss:
            print('   Scene %s (%s): %s' % (r['#'], r['Chapter'].split(':')[0], '; '.join(miss)))

    print('\n5. Numbers on the page: a number the text of the scene does not hold')
    for r, (_, _, p) in pairs:
        have = set(toks(' '.join(p)))
        miss = []
        for item in r['Numbers on the page'].split(';'):
            nums = [w for w in toks(item) if w in NUMWORDS or w[0].isdigit()]
            if any(w not in have for w in nums):
                miss.append('%s [%s]' % (re.sub(r'\s+', ' ', item.strip()), ', '.join(w for w in nums if w not in have)))
        if miss:
            print('   Scene %s (%s): %s' % (r['#'], r['Chapter'].split(':')[0], ' | '.join(miss)))

    print('\n6. Threads')
    seen = {}
    for i, r in enumerate(rows):
        for t in [x.strip() for x in r['Threads'].split(';')]:
            if not t:
                print('   Scene %s has an empty thread.' % r['#'])
            elif t not in THREADS:
                print('   Scene %s: "%s" is not on the list.' % (r['#'], t))
            else:
                seen.setdefault(t, []).append(i + 1)
    print('   %-58s %6s %6s %6s  %s' % ('Thread', 'scenes', 'first', 'last', 'longest silence'))
    for t in THREADS:
        s = seen.get(t, [])
        gap, at = max(((b - a - 1, a) for a, b in zip(s, s[1:])), default=(0, 0))
        print('   %-58s %6d %6s %6s  %d scenes, after scene %d' % (t, len(s), s[0] if s else '', s[-1] if s else '', gap, at))

    print('\n7. Questions')
    opened, closed = {}, {}
    for r in rows:
        for q in re.findall(r'[^;?]*\?', r['Opens a question']):
            opened.setdefault(norm(q), (q.strip(), r['#']))
        for q in re.findall(r'[^;?]*\?', r['Closes a question']):
            closed.setdefault(norm(q), (q.strip(), r['#']))
    print('   %d opened, %d closed.' % (len(opened), len(closed)))
    print('   Closed and never opened in these words:')
    for k, (q, num) in closed.items():
        if k not in opened:
            print('     scene %s: %s' % (num, q))
    print('   Opened and never closed in these words:')
    for k, (q, num) in opened.items():
        if k not in closed:
            print('     scene %s: %s' % (num, q))
    return 1 if bad else 0


def compare(gsheet, sheet):
    g = json.load(open(gsheet))
    g = g.get('values', g)
    c = list(csv.reader(open(sheet, newline='')))
    n = 0
    for i in range(max(len(g), len(c))):
        gr, cr = (g[i] if i < len(g) else []), (c[i] if i < len(c) else [])
        for j in range(len(c[0])):
            x, y = (gr[j] if j < len(gr) else ''), (cr[j] if j < len(cr) else '')
            if str(x) != y:
                n += 1
                print('Row %d (scene %s), %s\n   Sheet: %s\n   CSV:   %s' % (i + 1, cr[0] if cr else '?', c[0][j], str(x)[:300], y[:300]))
    print('%d cells differ. Google Sheet: %d rows. CSV: %d rows.' % (n, len(g), len(c)))
    return 1 if n else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == 'check':
        sys.exit(check(a[1], a[2]))
    if len(a) == 3 and a[0] == 'scene':
        h, n, p = scenes(a[1])[int(a[2]) - 1]
        print('%s, scene %d, %d words\n' % (h, n, count(p)))
        print('\n'.join(p))
        sys.exit(0)
    if len(a) == 3 and a[0] == 'sheet':
        sys.exit(compare(a[1], a[2]))
    sys.exit(__doc__)
