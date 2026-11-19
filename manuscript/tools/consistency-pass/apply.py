"""Apply the consistency pass to a plain-text copy of the manuscript and report what changed.

Usage: python3 apply.py <manuscript-paragraphs.txt> <output-folder>

The input is the Doc's text, one paragraph per line (made from a read of the Google Doc). It is
not in this repo, because the repo is public. The outputs go to the folder you name, which should
be drafts/_private/ (ignored by git):

  corrected.txt   the whole manuscript after the pass, one paragraph per line
  CHANGES.md      every change, by chapter, with what was there and why
  ch13-15.md      chapters 13 to 15 as they read after the pass

Nothing here writes to the Doc.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
REPO = os.path.normpath(HERE + '../..') + '/'
sys.path.insert(0, HERE)
from ops import OPS, LEFT, I, E, DEL, NB  # noqa: E402

src, out = sys.argv[1], sys.argv[2].rstrip('/') + '/'
P = open(src).read().split('\n')
if P and P[-1] == '':
    P.pop()


def idx(pred, start=0):
    hits = [i for i in range(start, len(P)) if pred(P[i])]
    if not hits:
        raise SystemExit('anchor not found')
    return hits[0]


def starts(s):
    return lambda p: p.startswith(s)


def sub(paras, old, new):
    n = sum(p.count(old) for p in paras)
    if n != 1:
        raise SystemExit('builder: %d matches for %r' % (n, old))
    res = []
    for p in paras:
        if old in p:
            res.extend(p.replace(old, new).split('\n'))
        else:
            res.append(p)
    return [p for p in res if p != DEL]


# ---------- chapters 13 to 15: where the old pieces are ----------
h13 = idx(starts("Chapter 13: One O'Clock on Saturday"), 500)
b0 = idx(starts('On Friday afternoon the cab was too hot'), h13)
c_last = idx(starts('He ate a peanut butter sandwich'), b0)
h14 = idx(starts('Chapter 14: Hand Up'), c_last)
h15 = idx(starts('Chapter 15: Concerned'), h14)
act3 = idx(starts('Act Three: The Farm'), h15)


def block(first, last, lo, hi):
    a = idx(starts(first), lo)
    b = idx(starts(last), a)
    assert b < hi
    return P[a:b + 1]


old_A = P[h13 + 1:b0]
oldman_foodbank = P[b0:c_last]
E_scene = block('On the sixth day he drove into town', 'Elijah walked on to the truck.', h14, h15)
F_scene = block('At four in the morning he asked the machine again.', 'Then he logged out of everything', h15, act3)
email = block('It was from somebody named Grace.', 'How do we work together? I want to pay you.', h15, act3)
reply = block('Good. We already have a welder', 'P.S. Eat something first.', h15, act3)
H_scene = block('David showed up Tuesday morning', 'He put the hand truck back in his pickup.', h15, act3)

# Nate and Wes on Main Street, then the Bear Flag window
E_scene = sub(E_scene, 'On the sixth day he drove into town for her, for chicken feed and a prescription.',
              'On Wednesday he drove into town for a letter from her doctor. The trust wanted one.')
E_scene = sub(E_scene, 'Seventeen years of load-ins.', 'Eighteen years of load-ins.')
cut = [i for i, p in enumerate(E_scene) if p.startswith('He got the feed.')][0]
E_main = E_scene[:cut] + ['He got the letter. He walked back to the truck the other way, which took him past the Bear Flag.']
E_window = ["He looked in, because he couldn't not."] + E_scene[cut + 1:]

# David and the hand truck
H = H_scene
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
F = F_scene
F = sub(F, 'He was in his old bedroom, under the poster, with the laptop on his chest.',
        'He was lying across the seat with the laptop on his chest.')
F = sub(F, 'He lay there until the window went gray.', 'He lay there until the windshield went gray.')
F = sub(F, 'Then he logged out of everything and went to help Manny with the fence.', 'Then he logged out of everything.')

# ---------- the new prose, from the scene draft in this repo ----------
draft = open(REPO + 'drafts/draft-elijah-crash-out-arc.md').read()
draft = draft[draft.index('### Chapter 13: Two in the Afternoon'):draft.index('## What this changes later in the book')]
for old, new in [
    ('He got as far as a side street by a\npark downtown, pulled in under a sycamore, and turned the truck off.',
     'He got as far as a side street downtown and turned the truck off.'),
    ('for seventeen\nyears. *Take the band', 'for eighteen\nyears. *Take the band'),
    ('He smoked what was left of the bag at night so he could sleep, until it was gone.',
     'He made the bag last. One at night, so he could sleep.'),
    ('on a roof ten miles off that belonged to', 'on a roof down the hill that belonged to'),
    ("like a passenger who didn't care for conversation.",
     "like a passenger who didn't care for conversation. He had a manuscript in a bag and two phone numbers he hadn't called."),
]:
    assert draft.count(old) == 1, old
    draft = draft.replace(old, new)

placeholders = iter([
    E_main,                      # Main Street
    H,                           # the hand truck
    F,                           # Am I crazy?
    email,                       # Grace's email, unchanged
    oldman_foodbank,             # the old man and the food bank, in place
    [],                          # (food bank is inside the block above)
    reply,                       # Grace's reply, unchanged
])
chapters = {}
for chunk in re.split(r'^### ', draft, flags=re.M)[1:]:
    title, body = chunk.split('\n', 1)
    paras = []
    for para in re.split(r'\n\s*\n', body.strip()):
        text = ' '.join(ln.strip() for ln in para.split('\n')).strip()
        if not text:
            continue
        if text == '•':
            paras.append(NB)
        elif text.startswith('*['):
            paras.extend(next(placeholders))
        else:
            paras.append(re.sub(r'\*([^*]+)\*', lambda m: I + m.group(1) + E, text))
            if text.endswith('Somebody ought to tell you."'):
                paras.extend(E_window)
    chapters[title] = paras
assert next(placeholders, None) is None
titles = list(chapters)
assert titles == ['Chapter 13: Two in the Afternoon', 'Chapter 14: Rain', "Chapter 15: One O'Clock on Saturday"], titles

new_13_15 = []
for t in titles:
    new_13_15.append(t)
    new_13_15.extend(chapters[t])
before_13_15 = P[h13:act3]
P = P[:h13] + new_13_15 + P[act3:]
span = (h13, h13 + len(new_13_15))

# ---------- the single-spot changes ----------
report = {}
for ch, kind, find, repl, why in OPS:
    if kind == 'R':
        hits = [(i, m) for i, p in enumerate(P) for m in [re.search(find, p)] if m]
    else:
        hits = [(i, None) for i, p in enumerate(P) if find in p]
    if len(hits) != 1 or (kind == 'L' and P[hits[0][0]].count(find) != 1):
        raise SystemExit('chapter %s: %d paragraphs match %r' % (ch, len(hits), find))
    i, m = hits[0]
    was = m.group(0) if m else find
    P[i] = P[i].replace(was, repl)
    report.setdefault(ch, []).append((was, repl, why))
out_paras = []
for p in P:
    for q in p.split('\n'):
        if q != DEL and DEL not in q:
            out_paras.append(q)
        elif q != DEL:
            raise SystemExit('DEL inside a paragraph: ' + q[:60])
P = out_paras


def show(t):
    return t.replace(I, '*').replace(E, '*').replace(NB, '(scene break)')


def quote(t):
    return '\n>\n'.join('> ' + show(x) for x in t.split('\n') if x != DEL) or '> (cut)'


os.makedirs(out, exist_ok=True)
open(out + 'corrected.txt', 'w').write('\n'.join(P) + '\n')

n_ops = sum(len(v) for v in report.values())
md = ['# What the consistency pass changes', '',
      '*19 November 2026. Checked against your Doc as it stood this morning. Every change below was run against a copy of your text and lands in exactly one place.*',
      '', '**%d single-spot changes in %d chapters, and chapters 13 to 15 rebuilt around the stroke.**' % (n_ops, len(report)), '',
      '## Chapters 13, 14 and 15', '',
      'These three are rebuilt from the scene draft. Your scenes are kept and moved, not rewritten:', '',
      '- **Chapter 13, "Two in the Afternoon."** New: Manny\'s call, the hospital, "Barry," the kitchen, the barn, the two pages, his followers, the sale. Yours, moved here: Nate and Wes on Main Street, David through the window, David and the hand truck. In the hand truck scene David now says "Heard they close Friday," and the offer of shifts is unchanged.',
      '- **Chapter 14, "Rain."** New: the crash out under the madrones. The four days on his mother\'s couch are gone.',
      '- **Chapter 15, "One O\'Clock on Saturday."** New: five weeks in the truck in Santa Rosa, the pawned guitar, the Sundays in her room. Yours, moved here: "Am I crazy?", Grace\'s email and her reply, the old man, the food bank. Grace\'s email is word for word, including "I want to pay you."',
      '- **Cut, because the stroke comes first:** "Who\'s Grace?" "She married?" "I\'m asking." "Go be useful, baby. You\'re underfoot." And the 9:40 call from the next room.',
      '', 'The full text of the three chapters is at the bottom of this tab.', '',
      '## Every other change, by chapter', '']
for ch in sorted(report):
    md += ['### Chapter %d' % ch, '']
    for was, repl, why in report[ch]:
        md += ['**Was**', '', quote(was), '', '**Now**', '', quote(repl), '']
        if why:
            md += ['*' + why + '*', '']
md += ['## Left alone on purpose', '']
for name, why in LEFT:
    md += ['- **%s.** %s' % (name, why)]
md += ['', '## Chapters 13 to 15 as they read now', '']
for p in new_13_15:
    if p in titles:
        md += ['### ' + p, '']
    else:
        md += [show(p) if p != NB else '&middot;', '']
open(out + 'CHANGES.md', 'w').write('\n'.join(md) + '\n')
print('paragraphs before 13-15: %d, after: %d' % (len(before_13_15), len(new_13_15)))
print('single-spot changes: %d in %d chapters' % (n_ops, len(report)))
print('wrote', out + 'corrected.txt', len(P), 'paragraphs')
