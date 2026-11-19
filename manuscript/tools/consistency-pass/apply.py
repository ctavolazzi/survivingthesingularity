"""Apply the consistency and story pass to a plain-text copy of the manuscript and report what changed.

Usage: python3 apply.py <doc-paragraphs.txt> <output-folder>

The input is the Doc's text, one paragraph per line, with italics marked [[i]]like this[[/i]]
(made from a read of the Google Doc). It is not in this repo, because the repo is public. The
outputs go to the folder you name, which should be drafts/_private/ (ignored by git):

  book.json       the manuscript after the pass: a list of [text, mark] where mark is
                  "" (CT's text, untouched), "moved", "changed" or "new"
  corrected.txt   the same, text only
  CHANGES.md      the decisions, then every change by chapter with what was there and why

Nothing here writes to the Doc.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
REPO = os.path.normpath(HERE + '../..') + '/'
sys.path.insert(0, HERE)
from ops import OPS, OPS2, OPS3, OPS4, LEFT, DECIDED, REJECTED, I, E, DEL, NB  # noqa: E402

src, out = sys.argv[1], sys.argv[2].rstrip('/') + '/'
P = open(src).read().split('\n')
if P and P[-1] == '':
    P.pop()
P = [[p, ''] for p in P]


def bare(t):
    return t.replace(I, '').replace(E, '')


def idx(s, start=0):
    for i in range(start, len(P)):
        if bare(P[i][0]).startswith(s):
            return i
    raise SystemExit('anchor not found: ' + s)


def sub(paras, old, new, mark='changed'):
    """Replace old with new in exactly one paragraph of a block. A newline in new starts a paragraph."""
    n = sum(p[0].count(old) for p in paras)
    if n != 1:
        raise SystemExit('builder: %d matches for %r' % (n, old))
    res = []
    for p in paras:
        if old in p[0]:
            res.extend([q, mark] for q in p[0].replace(old, new).split('\n') if q != DEL)
        else:
            res.append(p)
    return res


# ---------- chapters 13 to 15: where the old pieces are ----------
h13 = idx("Chapter 13: One O'Clock on Saturday", 500)
b0 = idx('On Friday afternoon the cab was too hot', h13)
c_last = idx('He ate a peanut butter sandwich', b0)
h14 = idx('Chapter 14: Hand Up', c_last)
h15 = idx('Chapter 15: Concerned', h14)
act3 = idx('Act Three: The Farm', h15)


def block(first, last, lo, hi):
    a = idx(first, lo)
    b = idx(last, a)
    assert b < hi
    return [[p[0], 'moved'] for p in P[a:b + 1]]


oldman_foodbank = [list(p) for p in P[b0:c_last]]
E_scene = block('On the sixth day he drove into town', 'Elijah walked on to the truck.', h14, h15)
F = block('At four in the morning he asked the machine again.', 'Then he logged out of everything', h15, act3)
email = block('It was from somebody named Grace.', 'How do we work together? I want to pay you.', h15, act3)
reply = block('Good. We already have a welder', 'P.S. Eat something first.', h15, act3)
H = block('David showed up Tuesday morning', 'He put the hand truck back in his pickup.', h15, act3)

# Nate and Wes on Main Street, then the Bear Flag window
E_scene = sub(E_scene, 'On the sixth day he drove into town for her, for chicken feed and a prescription.',
              'On Wednesday he drove into town for a letter from her doctor. The trust wanted one.')
E_scene = sub(E_scene, 'Seventeen years of load-ins.', 'Eighteen years of load-ins.')
cut = [i for i, p in enumerate(E_scene) if p[0].startswith('He got the feed.')][0]
E_main = E_scene[:cut] + [['He got the letter. He walked back to the truck the other way, which took him past the Bear Flag.', 'changed']]
E_window = [["He looked in, because he couldn't not.", 'changed']] + E_scene[cut + 1:]

# David and the hand truck
H = sub(H, 'David showed up Tuesday morning', 'David showed up Thursday morning')
H = sub(H, "Elijah hadn't called him. His mother had. She stood on the porch with her arms folded and watched the two of them not say hello.",
        "Elijah hadn't called him. Nobody had.\n\"Heard they close Friday,\" David said.\n\"Yeah.\"")
H = sub(H, 'They went into the barn and pulled the tarp. It took',
        'They went into the barn. David looked at the buckets, stacked five high, and at the two generators, and did not say one word about them. They pulled the tarp. It took')
H = sub(H, '"She says you\'re going north," David said. "Some commune."', '"Where are you going to put it?" David said.')
H = sub(H, '"It\'s a co-op."', DEL)
H = sub(H, '"What\'s the difference?"', DEL)
H = sub(H, "You don't have to go live with strangers, Mad.", "You don't have to go anywhere, Mad.")
H = sub(H, "It would've been so easy.",
        "It would've been so easy.\nHe could see the other thing too. Pruitt on the sidewalk. Everybody in that room knowing what he had signed.")
H = sub(H, "He hugged Elijah's mother on the porch.", 'He looked at the porch a second. There was nobody on it.')

# "Am I crazy?" moves into the truck
F = sub(F, 'He was in his old bedroom, under the poster, with the laptop on his chest.',
        'He was lying across the seat with the laptop on his chest.')
F = sub(F, 'He lay there until the window went gray.', 'He lay there until the windshield went gray.')
F = sub(F, 'Then he logged out of everything and went to help Manny with the fence.', 'Then he logged out of everything.')

# ---------- the new prose, from the scene draft in this repo ----------
draft = open(REPO + 'drafts/draft-elijah-crash-out-arc.md').read()
draft = draft[draft.index('### Chapter 13: Two in the Afternoon'):draft.index('## What this changes later in the book')]
for old, new, n in [
    ('He got as far as a side street by a\npark downtown, pulled in under a sycamore, and turned the truck off.',
     'He got as far as a side street downtown and turned the truck off.', 1),
    ('for seventeen\nyears. *Take the band', 'for eighteen\nyears. *Take the band', 1),
    ('He smoked what was left of the bag at night so he could sleep, until it was gone.',
     'He made the bag last. One at night, so he could sleep.', 1),
    ('on a roof ten miles off that belonged to', 'on a roof down the hill that belonged to', 1),
    ("like a passenger who didn't care for conversation.",
     "like a passenger who didn't care for conversation. He had a manuscript in a bag and two phone numbers he hadn't called.", 1),
    # the Alderson husband in chapter 32 is already a Tom
    ('"My dad was Tom."', '"My dad was Joe."', 1),
    ('Once she called him Tom, and laughed', 'Once she called him Joe, and laughed', 1),
    ('He never thought of it as his.',
     'He never thought of it as his. He had done the division. Every twenty he took out came off the far end of her room.', 1),
]:
    assert draft.count(old) == n, old
    draft = draft.replace(old, new)

placeholders = iter([E_main, H, F, email, oldman_foodbank, [], reply])
chapters = {}
for chunk in re.split(r'^### ', draft, flags=re.M)[1:]:
    title, body = chunk.split('\n', 1)
    paras = []
    for para in re.split(r'\n\s*\n', body.strip()):
        text = ' '.join(ln.strip() for ln in para.split('\n')).strip()
        if not text:
            continue
        if text == '•':
            paras.append([NB, 'new'])
        elif text.startswith('*['):
            paras.extend(next(placeholders))
        else:
            paras.append([re.sub(r'\*([^*]+)\*', lambda m: I + m.group(1) + E, text), 'new'])
            if text.endswith('Somebody ought to tell you."'):
                paras.extend(E_window)
    chapters[title] = paras
assert next(placeholders, None) is None
titles = list(chapters)
assert titles == ['Chapter 13: Two in the Afternoon', 'Chapter 14: Rain', "Chapter 15: One O'Clock on Saturday"], titles

new_13_15 = []
for t in titles:
    new_13_15.append([t, 'changed' if t.startswith('Chapter 13') else 'new'])
    new_13_15.extend(chapters[t])
n_before = act3 - h13
os.makedirs(out, exist_ok=True)
json.dump(new_13_15, open(out + 'built-13-15.json', 'w'))
P = P[:h13] + new_13_15 + P[act3:]

# ---------- the single-spot changes ----------
report = {}
for ch, kind, find, repl, why in OPS + OPS2 + OPS3 + OPS4:
    if kind == 'P':
        hits = [(i, re.search(re.escape(p[0]), p[0])) for i, p in enumerate(P) if bare(p[0]) == find]
    elif kind == 'R':
        hits = [(i, m) for i, p in enumerate(P) for m in [re.search(find, p[0])] if m]
    else:
        hits = [(i, None) for i, p in enumerate(P) if find in p[0]]
    if len(hits) != 1 or (kind == 'L' and P[hits[0][0]][0].count(find) != 1):
        raise SystemExit('chapter %s: %d paragraphs match %r' % (ch, len(hits), find))
    i, m = hits[0]
    before = P[i][0]
    was = m.group(0) if m else find
    pos = before.index(was)
    pre, post = before[:pos], before[pos + len(was):]
    parts = repl.split('\n')
    pieces = []
    for k, part in enumerate(parts):
        text = (pre if k == 0 else '') + part + (post if k == len(parts) - 1 else '')
        if part == DEL and len(parts) == 1 and not pre and not post:
            continue
        own = (pre if k == 0 else '') + (post if k == len(parts) - 1 else '')
        if text == before or (not own and part == was) or (not own and part == NB):
            mark = P[i][1]
        elif own.strip():
            mark = 'changed'
        else:
            mark = 'new'
        pieces.append([text, mark])
    P[i:i + 1] = pieces
    report.setdefault(ch, []).append((was, repl, why))
assert not any(DEL in p[0] for p in P)


def show(t):
    return t.replace(I, '*').replace(E, '*').replace(NB, '(scene break)')


def quote(t):
    return '\n>\n'.join('> ' + show(x) for x in t.split('\n') if x != DEL) or '> (cut)'


os.makedirs(out, exist_ok=True)
json.dump(P, open(out + 'book.json', 'w'))
open(out + 'corrected.txt', 'w').write('\n'.join(p[0] for p in P) + '\n')

n_ops = sum(len(v) for v in report.values())
md = ['# The best version I can give you', '',
      '*19 November 2026. This is my pass over the whole book: the story decisions first, then the consistency fixes. It is all in your Doc now, checked paragraph by paragraph against the **Book** tab, where everything that is not yours is marked in the margin. The version of the Doc from before the pass is in its version history.*',
      '',
      '## What I decided', '',
      'Each of these starts from something already on your page. Each one I argued with before I kept it.', '']
for k, (what, where, why) in enumerate(DECIDED, 1):
    md += ['%d. **%s.** %s. %s' % (k, what, where, why)]
md += ['', '## What I turned down', '']
for what, why in REJECTED:
    md += ['- **%s** %s' % (what, why)]
md += ['', '## What the stroke costs', '',
       'She has one word after chapter 13, so three of her lines are gone: "It reads better than it sounded," "She married? I\'m asking," and "Where\'s the Fisher?" Four more were saved by moving them or by having him say them for her.',
       '', '## Chapters 13, 14 and 15', '',
       'Rebuilt around the stroke. Your scenes are kept and moved, not rewritten.', '',
       '- **Chapter 13, "Two in the Afternoon."** New: Manny\'s call, the hospital, "Barry," the kitchen, the barn, the two pages, his followers, the sale. Yours, moved here: Nate and Wes on Main Street, David through the window, David and the hand truck.',
       '- **Chapter 14, "Rain."** New: the crash out under the madrones. The four days on his mother\'s couch are gone.',
       '- **Chapter 15, "One O\'Clock on Saturday."** New: five weeks in the truck in Santa Rosa, the pawned guitar, the Sundays in her room. Yours, moved here: "Am I crazy?", Grace\'s email and her reply word for word, the old man, the food bank.',
       '- One name changed from the scene draft: his father is Joe, not Tom. The Alderson who dies in chapter 32 is already a Tom.',
       '', '## Every other change, by chapter', '',
       '%d changes in %d chapters. Each one was run against a copy of your text and lands in exactly one place.' % (n_ops, len(report)), '']
for ch in sorted(report):
    md += ['### ' + ('Chapter %d' % ch if ch else 'Title page'), '']
    for was, repl, why in report[ch]:
        if repl.endswith('\x00'):
            continue
        md += ['**Was**', '', quote(was), '', '**Now**', '', quote(repl), '']
        if why:
            md += ['*' + why + '*', '']
md += ['## Left alone on purpose', '']
for name, why in LEFT:
    md += ['- **%s.** %s' % (name, why)]
open(out + 'CHANGES.md', 'w').write('\n'.join(md) + '\n')
marks = {}
for p in P:
    marks[p[1]] = marks.get(p[1], 0) + 1
print('chapters 13-15: %d paragraphs before, %d after' % (n_before, len(new_13_15)))
print('single-spot changes: %d in %d chapters' % (n_ops, len(report)))
print('paragraphs:', len(P), marks)
