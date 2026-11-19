#!/usr/bin/env python3
"""Version control for the book. Run from anywhere inside the repository.

  book.py status                 where the current book is, how big, and how every branch stands
  book.py verify READ.json       is the Google Doc the same as the copy in the repository?
  book.py pull READ.json [WHY]   write the Doc into the repository as a new version, and log it
  book.py changes [REV]          what changed in the manuscript since REV (default: the last commit)
  book.py cast                   rebuild every character's folder from the notes and the manuscript
  book.py catchup                bring every character branch with nothing waiting up to the book

READ.json is a saved result of the Docs connector's read_doc on CT's Doc, "FINAL StS Manuscript".
This script never calls the connector and never writes to the Doc. It does not commit or push,
except `catchup`, which only moves branches that hold no work of their own.

manuscript/novel/README.md says how these fit together.
"""
import datetime
import difflib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
MS = os.path.normpath(HERE + '..') + '/'                 # manuscript/
NOVEL = MS + 'novel/'
BOOK = NOVEL + 'FINAL-StS-Manuscript.md'
LOG = NOVEL + 'CHANGES.md'
CAST = NOVEL + 'characters/'
REL = 'manuscript/novel/FINAL-StS-Manuscript.md'
NB = ' '
BREAK = '<p align="center">&middot;</p>'
HASH = {'HEADING_1': '# ', 'HEADING_2': '## ', 'HEADING_3': '### ', 'HEADING_4': '#### '}
PART = re.compile(r"^# (Author's Note|Act \w+: .*|Chapter \d+: .*|Meanwhile|Afterword: .*)$")


def git(*args, check=True):
    r = subprocess.run(['git', '-C', MS] + list(args), capture_output=True, text=True)
    if check and r.returncode:
        sys.exit('git %s failed: %s' % (' '.join(args), r.stderr.strip()))
    return r.stdout.strip()


def version():
    return open(NOVEL + 'VERSION').read().strip()


# ---- the Doc as Markdown

def styled(runs):
    """One paragraph's runs as Markdown. Italic is *..*, bold is **..**, and the marks hug the words."""
    chars = []
    for content, it, bo in runs:
        chars.extend((ch, it, bo) for ch in content)
    while chars and chars[-1][0] == '\n':
        chars.pop()
    out, i, n = [], 0, len(chars)
    while i < n:
        ch, it, bo = chars[i]
        if not ch.strip() or not (it or bo):
            out.append(ch)
            i += 1
            continue
        j = i
        while j < n and (not chars[j][0].strip() or chars[j][1:] == (it, bo)):
            j += 1
        while not chars[j - 1][0].strip():
            j -= 1
        mark = ('**' if bo else '') + ('*' if it else '')
        out.append(mark + ''.join(c[0] for c in chars[i:j]) + mark[::-1])
        i = j
    return ''.join(out)


def markdown(path):
    """The whole Doc as Markdown, one line for each paragraph. Returns (text, revision id)."""
    d = json.load(open(path))
    d = d.get('content', d)
    blocks, was_item = [], False
    for el in d['tabs'][0]['documentTab']['body']['content']:
        p = el.get('paragraph')
        if not p:
            continue
        runs = [(e['textRun']['content'], bool(e['textRun'].get('textStyle', {}).get('italic')),
                 bool(e['textRun'].get('textStyle', {}).get('bold'))) for e in p['elements'] if e.get('textRun')]
        plain = ''.join(r[0] for r in runs).rstrip('\n')
        style = p['paragraphStyle'].get('namedStyleType')
        item = bool(p.get('bullet'))
        if plain == NB or not plain.strip():
            line = BREAK                                              # a scene break
        elif style in HASH:
            line = HASH[style] + plain
        else:
            line = re.sub(r'^(\d+)([.)]) ', r'\1\\\2 ', styled(runs))   # "1. The Cash Grab" is a sentence, not a list
            if item:
                line = '- ' + line
        blocks.append(('\n' if item and was_item else '\n\n') + line)
        was_item = item
    return ''.join(blocks).lstrip('\n') + '\n', d.get('revisionId', '')


def paragraphs(text):
    """The manuscript as a list of paragraphs. Paragraph N here is paragraph N of the Doc."""
    return [ln for ln in text.split('\n') if ln]


def words(paras):
    return sum(len(re.sub(r'^(#+ |- )', '', p).split()) for p in paras if p != BREAK)


def novel_span(paras):
    a = next(i for i, p in enumerate(paras) if p == "# Author's Note")
    b = next((i for i, p in enumerate(paras) if p.startswith('# Next book:')), len(paras))
    return a, b


def parts(paras):
    """For each paragraph, the part of the book it sits in."""
    a, b = novel_span(paras)
    out, here, last_ch = [], 'Planning notes at the top of the Doc', ''
    for i, p in enumerate(paras):
        if i >= b:
            here = 'Notes after the Afterword'
        elif i >= a and PART.match(p):
            here = p[2:]
            if here.startswith('Chapter'):
                last_ch = here.split(':')[0]
            elif here == 'Meanwhile':
                here = 'Meanwhile (after %s)' % last_ch if last_ch else 'Meanwhile'
        out.append(here)
    return out


def measure(paras):
    a, b = novel_span(paras)
    return len(paras), words(paras), b - a, words(paras[a:b])


def by_part(old, new):
    """What changed between two lists of paragraphs, counted by part of the book."""
    where_old, where_new = parts(old), parts(new)
    tally, order = {}, []

    def bump(part, key, n):
        if part not in tally:
            tally[part] = {'added': 0, 'removed': 0, 'changed': 0}
            order.append(part)
        tally[part][key] += n

    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        both = min(i2 - i1, j2 - j1)
        for k in range(both):
            bump(where_new[j1 + k], 'changed', 1)
        for k in range(i1 + both, i2):
            bump(where_old[k], 'removed', 1)
        for k in range(j1 + both, j2):
            bump(where_new[k], 'added', 1)
    return [(part, tally[part]) for part in order]


def say_changes(rows):
    if not rows:
        return ['Nothing changed.']
    out = []
    for part, t in rows:
        bits = ['%d %s' % (t[k], k) for k in ('changed', 'added', 'removed') if t[k]]
        out.append('%s: %s' % (part, ', '.join(bits)))
    return out


# ---- commands

def cmd_verify(read):
    text, rev = markdown(read)
    here = open(BOOK).read()
    if text == here:
        n, w, nn, nw = measure(paragraphs(here))
        print('THE DOC AND THE REPOSITORY MATCH. %d paragraphs, %d words.' % (n, w))
        return 0
    print('THE DOC HAS CHANGED since the copy in the repository was made.')
    for line in say_changes(by_part(paragraphs(here), paragraphs(text))):
        print('  ' + line)
    print('Run `book.py pull` to make a new version.')
    return 1


def cmd_pull(read, why):
    text, rev = markdown(read)
    old = open(BOOK).read() if os.path.exists(BOOK) else ''
    if text == old:
        print('Nothing to pull. The Doc and the repository match.')
        return 0
    rows = by_part(paragraphs(old), paragraphs(text))
    open(BOOK, 'w').write(text)
    n, w, nn, nw = measure(paragraphs(text))
    now = datetime.datetime.now(datetime.timezone.utc)
    entry = ['### %s, %s UTC. %s' % (now.strftime('%Y-%m-%d'), now.strftime('%H:%M'), why or 'Pulled from the Doc'), '',
             '- **Changed by:** CT, in the Doc.' if not why else '- **Why:** %s' % why,
             '- **What changed, by part of the book:**']
    entry += ['  - ' + line for line in say_changes(rows)]
    entry += ['- **Measured:** %d paragraphs and %d words in the whole Doc. The novel itself is %d paragraphs and %d words.' % (n, w, nn, nw),
              '- **Doc revision:** `%s`' % rev[:23], '', '']
    log = open(LOG).read()
    mark = '## Versions\n\n'
    at = log.index(mark) + len(mark)
    open(LOG, 'w').write(log[:at] + '\n'.join(entry) + log[at:])
    print('\n'.join(entry))
    print('Wrote the manuscript and a new entry in CHANGES.md. Read the entry, fix the wording, then commit')
    print('those two files together, alone, on the version branch: book/' + version())
    return 0


def cmd_changes(rev):
    old = git('show', '%s:%s' % (rev, REL))
    new = open(BOOK).read()
    print('Since %s:' % rev)
    for line in say_changes(by_part(paragraphs(old), paragraphs(new))):
        print('  ' + line)
    print('For the words themselves: git diff --word-diff %s -- %s' % (rev, REL))
    return 0


def refs(prefix):
    out = git('for-each-ref', '--format=%(refname:short)', 'refs/remotes/origin/' + prefix)
    return [r for r in out.split('\n') if r]


def cmd_status():
    v = version()
    paras = paragraphs(open(BOOK).read())
    n, w, nn, nw = measure(paras)
    last = next((ln[4:] for ln in open(LOG).read().split('\n') if ln.startswith('### ')), '')
    print('The book:        %s' % REL)
    print('Version:         %s, on the branch book/%s' % (v, v))
    print('Size:            %d paragraphs, %d words. The novel itself: %d paragraphs, %d words.' % (n, w, nn, nw))
    print('Last version:    %s' % last)
    print('You are on:      %s%s' % (git('rev-parse', '--abbrev-ref', 'HEAD'),
                                   '' if not git('status', '--porcelain') else '  (with changes not yet committed)'))
    git('fetch', '-q', 'origin', check=False)
    base = 'origin/book/' + v
    if base not in refs('book/'):
        print('The branch book/%s is not on GitHub yet.' % v)
        return 0
    print('\nHow each branch stands against book/%s:' % v)
    for r in ['origin/main'] + refs('character/') + [x for x in refs('claude/')]:
        if git('rev-parse', '-q', '--verify', r, check=False) == '':
            continue
        ahead = int(git('rev-list', '--count', '%s..%s' % (base, r)))
        behind = int(git('rev-list', '--count', '%s..%s' % (r, base)))
        if not ahead and not behind:
            note = 'even with the book'
        elif not ahead:
            note = 'behind by %d, nothing waiting' % behind
        else:
            note = '%d waiting%s' % (ahead, ', and behind by %d' % behind if behind else '')
        print('  %-44s %s' % (r.replace('origin/', ''), note))
    return 0


def cmd_catchup():
    v = version()
    git('fetch', '-q', 'origin')
    base = 'origin/book/' + v
    moved = []
    for r in refs('character/'):
        ahead = int(git('rev-list', '--count', '%s..%s' % (base, r)))
        behind = int(git('rev-list', '--count', '%s..%s' % (r, base)))
        if not ahead and behind:
            moved.append('%s:refs/heads/%s' % (git('rev-parse', base), r.replace('origin/', '')))
    if moved:
        git('push', '-q', 'origin', *moved)
    print('Brought %d character branches up to book/%s. Branches with work waiting were left alone.' % (len(moved), v))
    return 0


# ---- the cast

def sections(text, level):
    """{heading: body} for headings of one level. A body runs to the next heading of that level or higher."""
    out, name, buf = {}, None, []
    for ln in text.split('\n'):
        m = re.match(r'^(#{1,6}) (.*)$', ln)
        if m and len(m.group(1)) <= level:
            if name is not None:
                out.setdefault(name, []).append('\n'.join(buf).strip())
            name, buf = (m.group(2).strip() if len(m.group(1)) == level else None), []
        elif name is not None:
            buf.append(ln)
    if name is not None:
        out.setdefault(name, []).append('\n'.join(buf).strip())
    return out


def bold_paragraphs(text):
    """{name: paragraph} for paragraphs that open with **Name.**"""
    out = {}
    for block in re.split(r'\n\s*\n', text):
        m = re.match(r'^\*\*([^*]+?)\.\*\*', block.strip())
        if m:
            out[m.group(1)] = block.strip()
    return out


def cmd_cast():
    people = json.load(open(CAST + 'cast.json'))
    read = lambda f: open(MS + f).read() if os.path.exists(MS + f) else ''
    book = open(BOOK).read()
    paras = paragraphs(book)
    where = parts(paras)
    pages = book[book.index('# Character pages'):book.index("# Author's Note")]
    src = [
        ("CT's own character page, at the top of the Doc", 'novel/FINAL-StS-Manuscript.md', sections(pages, 3), None),
        ('The next pass: substrate, 19 November', 'NOVEL-SUBSTRATE-2026-11-19.md',
         {**{k: v for k, v in sections(read('NOVEL-SUBSTRATE-2026-11-19.md'), 2).items()},
          **{k: [v] for k, v in bold_paragraphs(read('NOVEL-SUBSTRATE-2026-11-19.md')).items()}}, None),
        ('The map of everyone, 19 November', 'NOVEL-MAP-EVERYONE-2026-11-19.md', None, 'map'),
        ('What the Drive holds, 19 November', 'NOVEL-DRIVE-FINDINGS-2026-11-19.md',
         sections(read('NOVEL-DRIVE-FINDINGS-2026-11-19.md'), 3), None),
        ('Character arcs, first pass, 18 November', 'NOVEL-CHARACTER-ARCS-2026-11-18.md',
         sections(read('NOVEL-CHARACTER-ARCS-2026-11-18.md'), 3), None),
        ('Character profiles, first pass, 18 November', 'NOVEL-CHARACTER-PROFILES-2026-11-18.md',
         sections(read('NOVEL-CHARACTER-PROFILES-2026-11-18.md'), 2), None),
    ]
    themap = read('NOVEL-MAP-EVERYONE-2026-11-19.md')
    map2, map3 = sections(themap, 2), sections(themap, 3)
    said = sections(read('novel/dictation-2026-11-19-morning.md'), 2)
    today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    index = ['| Folder | Who | First seen | Last seen | Paragraphs that name them |', '|---|---|---|---|---|']
    for p in people:
        slug, name, keys = p['slug'], p['name'], set(p.get('keys', []) + [p['name']])
        os.makedirs(CAST + slug, exist_ok=True)
        # where they are in the book
        hits, first, last, total = {}, '', '', 0
        if p.get('find'):
            rx = re.compile(p['find'])
            for i, para in enumerate(paras):
                if rx.search(para) and not para.startswith('#'):
                    hits.setdefault(where[i], []).append(i + 1)
            story = [k for k in hits if not k.startswith(('Planning', 'Notes after'))]
            total = sum(len(hits[k]) for k in story)
            first, last = (story[0], story[-1]) if story else ('', '')
        rows = ['# %s: where they are in the book' % name, '',
                'Built by `manuscript/tools/book.py cast` on %s. It is rebuilt each time, so do not edit it.' % today, '',
                'A paragraph is counted when it matches `%s`. Paragraph N is paragraph N of the Doc and line N of' % p.get('find', ''),
                'what `doc_sync.py dump` prints, which is the number the readers cite. The count is of paragraphs',
                'that name them. It misses scenes where they are present and not named.', '',
                '| Part of the book | Paragraphs | Which |', '|---|---|---|']
        for part, nums in hits.items():
            rows.append('| %s | %d | %s |' % (part, len(nums), ', '.join(str(x) for x in nums)))
        open(CAST + slug + '/appearances.md', 'w').write('\n'.join(rows) + '\n')
        # what has been gathered
        out = ['# %s: what has been gathered' % name, '',
               'Built by `manuscript/tools/book.py cast` on %s. It is rebuilt each time, so do not edit it.' % today,
               'Each piece says which file it came from. Change the file, then run `cast` again.', '',
               'The pieces dated 18 November and the map were written before the pass of 19 November. They can',
               'describe the book as it was.', '']
        for n in p.get('dictation', []):
            for head, bodies in said.items():
                if head.startswith('%d.' % n):
                    out += ['## CT, the morning of 19 November: %s' % head.split('. ', 1)[1], '',
                            'From `novel/dictation-2026-11-19-morning.md`. His words, as sent.', '', bodies[0], '']
        for title, fname, table, kind in src:
            got = []
            if kind == 'map':
                for head, bodies in list(map3.items()) + list(map2.items()):
                    if head.split(' | ')[0].strip() in keys:
                        got += ['**%s**\n\n%s' % (head, b.split('\n### ')[0].strip()) for b in bodies]
            else:
                for k in keys:
                    got += table.get(k, [])
            if got:
                out += ['## %s' % title, '', 'From `%s`.' % fname, ''] + ['\n\n'.join(got), '']
        open(CAST + slug + '/gathered.md', 'w').write('\n'.join(out).rstrip('\n') + '\n')
        reports = sorted(os.listdir(CAST + slug + '/readers')) if os.path.isdir(CAST + slug + '/readers') else []
        if not os.path.exists(CAST + slug + '/README.md'):
            open(CAST + slug + '/README.md', 'w').write('\n'.join([
                '# %s' % name, '', p.get('note', ''), '',
                '| File | What it is |', '|---|---|',
                '| `gathered.md` | Everything the notes say about them, each piece with its source. Rebuilt by code. |',
                '| `appearances.md` | Where they are in the book, by chapter and paragraph. Rebuilt by code. |']
                + (['| `readers/` | Readers\' reports about them: %d. |' % len(reports)] if reports else [])
                + ['', 'Their branch is `character/%s`. Work on them waits there until CT says go.' % slug, '']))
        index.append('| [`%s/`](%s/) | %s | %s | %s | %s |' % (slug, slug, name, first, last, total or ''))
    head = open(CAST + 'README.md').read().split('<!-- cast -->')[0] if os.path.exists(CAST + 'README.md') else '# The cast\n\n'
    open(CAST + 'README.md', 'w').write(head + '<!-- cast -->\n\n' + '\n'.join(index) + '\n')
    print('Rebuilt %d character folders in manuscript/novel/characters/' % len(people))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == 'status':
        sys.exit(cmd_status())
    if a[0] == 'verify' and len(a) == 2:
        sys.exit(cmd_verify(a[1]))
    if a[0] == 'pull' and len(a) >= 2:
        sys.exit(cmd_pull(a[1], ' '.join(a[2:])))
    if a[0] == 'changes':
        sys.exit(cmd_changes(a[1] if len(a) > 1 else 'HEAD'))
    if a[0] == 'cast':
        sys.exit(cmd_cast())
    if a[0] == 'catchup':
        sys.exit(cmd_catchup())
    sys.exit(__doc__)
