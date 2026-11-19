"""Helpers for putting the pass into the Google Doc, once CT has said to write it there.

  dump   READ.json OUT.txt          paragraphs, one per line, italics as [[i]]..[[/i]]
  emit   READ.json PRIVATE OUTDIR   the replaceAllText batches still needed, checked by simulation
  fixup  READ.json PRIVATE OUT.json the one batch of styles and deletes that follows the text
  verify READ.json PRIVATE          compare the Doc with book.json, paragraph by paragraph

READ.json is a saved result of the Docs connector's read_doc. PRIVATE is drafts/_private/.
The batches are JSON for the connector's update_doc. This script never calls the connector.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, HERE)
I, E, DEL, NB = '[[i]]', '[[/i]]', '[[DEL]]', ' '
OLD14, ACT3 = 'Chapter 14: Hand Up', 'Act Three: The Farm'


def u16(s):
    return len(s.encode('utf-16-le')) // 2


def load(path):
    d = json.load(open(path))
    d = d.get('content', d)
    body = d['tabs'][0]['documentTab']['body']['content']
    paras = []
    for el in body:
        p = el.get('paragraph')
        if not p:
            continue
        runs = []
        for e in p['elements']:
            tr = e.get('textRun')
            if tr:
                runs.append((e['startIndex'], tr['content'], bool(tr.get('textStyle', {}).get('italic'))))
        text = ''.join(r[1] for r in runs).rstrip('\n')
        paras.append({'start': el['startIndex'], 'end': el['endIndex'], 'runs': runs, 'text': text,
                      'style': p['paragraphStyle'].get('namedStyleType')})
    return d['revisionId'], paras


def mask(p):
    """One bool per character of the paragraph text: is it italic in the Doc?"""
    m = []
    for _, content, it in p['runs']:
        m.extend([it] * len(content))
    return m[:len(p['text'])]


def marked(text, m):
    """Text with [[i]] markers from an italic mask. Whitespace at the edges of a span stays outside."""
    out, i, n = [], 0, len(text)
    while i < n:
        if m[i] and text[i].strip():
            j = i
            while j < n and (m[j] or not text[j].strip()):
                j += 1
            while not text[j - 1].strip() or not m[j - 1]:
                j -= 1
            out.append(I + text[i:j] + E)
            i = j
        else:
            out.append(text[i])
            i += 1
    return ''.join(out)


def unmark(t):
    """(plain text, italic mask) from text carrying [[i]] markers."""
    plain, m, on = [], [], False
    for part in re.split(r'(\[\[i\]\]|\[\[/i\]\])', t):
        if part == I:
            on = True
        elif part == E:
            on = False
        else:
            plain.append(part)
            m.extend([on and bool(ch.strip()) for ch in part])
    return ''.join(plain), m


def bare(t):
    return t.replace(I, '').replace(E, '')


def sim(paras, req):
    """What one replaceAllText does to a list of plain paragraphs. Returns (new list, paragraphs hit)."""
    r = req['replaceAllText']
    find, repl = r['containsText']['text'], r['replaceText']
    rx = re.compile(find if r['containsText'].get('searchByRegex') else re.escape(find))
    out, hit = [], 0
    for p in paras:
        if rx.search(p):
            hit += 1
            out.extend(rx.sub(lambda m: repl, p).split('\n'))
        else:
            out.append(p)
    return out, hit


def req(find, repl, regex=False):
    c = {'text': find, 'matchCase': True}
    if regex:
        c['searchByRegex'] = True
    return {'replaceAllText': {'containsText': c, 'replaceText': repl}}


def planned(private):
    from ops import OPS, OPS2
    if os.environ.get('STAGE') == '2':
        return [req(find, repl, kind == 'R') for ch, kind, find, repl, why in OPS2]
    built = [p[0] for p in json.load(open(private + 'built-13-15.json'))]
    steps = [
        req("Chapter 13: One O'Clock on Saturday", 'Chapter 13: Two in the Afternoon'),
        req('He got as far as a side street by a park downtown, pulled in under a sycamore, and turned the truck off.',
            'He got as far as a side street downtown and turned the truck off.'),
        req('He was there a week.', DEL),
        req(r"He could not have told you why\. He didn't have the gas.*", built[3], True),
        req(r'He smoked what was left of the bag\. He lay across the seat.*', DEL, True),
    ]
    a = built.index('Those were dark days.')
    assert built[4].startswith('On Sunday at 9:40 the phone rang on the dash')
    chunk, size = [], 0
    for t in built[5:a]:
        if size + len(t) > 6500 and chunk:
            steps.append(req('Those were dark days.', '\n'.join(chunk) + '\nThose were dark days.'))
            chunk, size = [], 0
        chunk.append(t)
        size += len(t) + 1
    steps.append(req('Those were dark days.', '\n'.join(chunk) + '\nThose were dark days.'))
    b = next(i for i, t in enumerate(built) if t.startswith('He ate a peanut butter sandwich'))
    steps.append(req(' Then he drove to the gas station on the corner, put all twenty dollars in the tank, and went north.',
                     '\n' + '\n'.join(built[b + 1:])))
    for ch, kind, find, repl, why in OPS:
        steps.append(req(find, repl.rstrip('\x00'), kind == 'R'))
    return steps


def target(private):
    return [p[0] for p in json.load(open(private + 'book.json'))]


def strip_old(paras):
    """Drop [[DEL]] paragraphs and the old chapters 14 and 15, which the fixup batch deletes."""
    out, skip = [], False
    for p in paras:
        if p == OLD14:
            skip = True
        elif p == ACT3:
            skip = False
        if not skip and p != DEL:
            out.append(p)
    return out


cmd = sys.argv[1]
rev, doc = load(sys.argv[2])

if cmd == 'dump':
    open(sys.argv[3], 'w').write('\n'.join(marked(p['text'], mask(p)) for p in doc) + '\n')
    print(rev, len(doc))

elif cmd == 'emit':
    private, outdir = sys.argv[3].rstrip('/') + '/', sys.argv[4].rstrip('/') + '/'
    os.makedirs(outdir, exist_ok=True)
    cur = [p['text'] for p in doc]
    want = [bare(t) for t in target(private)]
    todo = []
    for r in planned(private):
        nxt, hit = sim(cur, r)
        f, rp = r['replaceAllText']['containsText']['text'], r['replaceAllText']['replaceText']
        if hit == 1 and not r['replaceAllText']['containsText'].get('searchByRegex') and f in rp:
            rest = rp.replace(f, '', 1).strip('\n')
            if len(rest) > 10 and rest in '\n'.join(cur):
                continue      # the anchor is still there, and so is what was added to it
        if hit == 1:
            todo.append(r)
            cur = nxt
        elif hit == 0:
            pass          # already applied
        else:
            raise SystemExit('%d paragraphs match %r' % (hit, r['replaceAllText']['containsText']['text']))
    got = [bare(t) for t in strip_old(cur)]
    if got != want:
        for k, (x, y) in enumerate(zip(got, want)):
            if x != y:
                print('first difference at paragraph', k, '\n DOC :', x[:160], '\n BOOK:', y[:160])
                break
        raise SystemExit('simulation does not reach the book: %d vs %d paragraphs' % (len(got), len(want)))
    batches, cur_b, size = [], [], 0
    for r in todo:
        n = len(json.dumps(r, ensure_ascii=False))
        if cur_b and size + n > 7800:
            batches.append(cur_b)
            cur_b, size = [], 0
        cur_b.append(r)
        size += n
    if cur_b:
        batches.append(cur_b)
    for old in os.listdir(outdir):
        os.remove(outdir + old)
    for k, b in enumerate(batches, 1):
        open(outdir + '%02d.json' % k, 'w').write('[\n' + ',\n'.join(json.dumps(r, ensure_ascii=False) for r in b) + '\n]\n')
    print('simulation reaches the book. %d requests still to send, in %d batches' % (len(todo), len(batches)))
    print([sum(len(json.dumps(r, ensure_ascii=False)) for r in b) for b in batches])

elif cmd in ('fixup', 'verify'):
    private = sys.argv[3].rstrip('/') + '/'
    book = target(private)
    keep, dels, skip, old_start, old_end = [], [], False, None, None
    for p in doc:
        if p['text'] == OLD14 and p['style'] == 'HEADING_1':
            skip, old_start = True, p['start']
        elif p['text'] == ACT3:
            if skip:
                old_end = p['start']
            skip = False
        if skip:
            continue
        if p['text'] == DEL:
            dels.append((p['start'], p['end']))
        else:
            keep.append(p)
    if len(keep) != len(book):
        print('paragraph count: Doc %d, book %d' % (len(keep), len(book)))
    bad = 0
    styles, heads = [], []
    for p, want in zip(keep, book):
        w_plain, w_mask = unmark(want)
        # the Doc paragraph may still carry typed markers; they are not content
        d_plain, typed = unmark(p['text'])
        if d_plain != w_plain:
            bad += 1
            if bad <= 8:
                k = next((i for i, (x, y) in enumerate(zip(d_plain, w_plain)) if x != y), min(len(d_plain), len(w_plain)))
                print('TEXT differs at', p['start'], '\n DOC :', d_plain[max(0, k - 50):k + 70], '\n BOOK:', w_plain[max(0, k - 50):k + 70])
            continue
        # actual italic per content character, and its Doc index
        raw, m_raw = p['text'], mask(p)
        pos, act, k = [], [], 0
        off = p['start']
        while k < len(raw):
            if raw.startswith(I, k):
                off += u16(I); k += len(I); continue
            if raw.startswith(E, k):
                off += u16(E); k += len(E); continue
            pos.append(off); act.append(m_raw[k] and bool(raw[k].strip()))
            off += u16(raw[k]); k += 1
        assert len(act) == len(w_mask), (p['start'], len(act), len(w_mask))
        k = 0
        while k < len(act):
            if raw_ws := (not w_plain[k].strip()):
                k += 1; continue
            if act[k] != w_mask[k]:
                j = k
                while j < len(act) and (act[j] != w_mask[j] or not w_plain[j].strip()) and (w_mask[j] == w_mask[k] or not w_plain[j].strip()):
                    j += 1
                while not w_plain[j - 1].strip():
                    j -= 1
                styles.append((pos[k], pos[j - 1] + u16(w_plain[j - 1]), w_mask[k]))
                k = j
            else:
                k += 1
        is_head = re.match(r"^(Chapter \d+: |Act \w+: )", w_plain) and p['style'] != 'HEADING_1'
        if is_head and w_plain in ('Chapter 14: Rain', "Chapter 15: One O'Clock on Saturday"):
            heads.append((p['start'], p['end']))
    typed_left = sum(p['text'].count(I) for p in doc)
    print('text differences: %d, italic ranges to set: %d, [[DEL]] paragraphs: %d, old chapters 14-15 present: %s, headings to style: %d, typed markers: %d'
          % (bad, len(styles), len(dels), old_start is not None, len(heads), typed_left))
    if cmd == 'fixup':
        if bad:
            raise SystemExit('fix the text first')
        reqs = []
        for a, b, it in styles:
            reqs.append({'updateTextStyle': {'range': {'startIndex': a, 'endIndex': b}, 'textStyle': {'italic': it}, 'fields': 'italic'}})
        for a, b in heads:
            reqs.append({'updateParagraphStyle': {'range': {'startIndex': a, 'endIndex': b}, 'paragraphStyle': {'namedStyleType': 'HEADING_1'}, 'fields': 'namedStyleType'}})
        ranges = list(dels)
        if old_start is not None:
            ranges.append((old_start, old_end))
        for a, b in sorted(ranges, reverse=True):
            reqs.append({'deleteContentRange': {'range': {'startIndex': a, 'endIndex': b}}})
        if typed_left:
            reqs.append(req(I, ''))
            reqs.append(req(E, ''))
        open(sys.argv[4], 'w').write('[\n' + ',\n'.join(json.dumps(r, ensure_ascii=False) for r in reqs) + '\n]\n')
        print('revision', rev)
        print(len(reqs), 'requests,', os.path.getsize(sys.argv[4]), 'bytes')
    else:
        ok = not bad and not styles and not dels and old_start is None and not heads and not typed_left and len(keep) == len(book)
        print('THE DOC MATCHES THE BOOK' if ok else 'not yet')
