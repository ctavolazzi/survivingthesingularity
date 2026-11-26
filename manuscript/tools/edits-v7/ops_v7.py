"""v7 only: changes that go into v7 and not into v6 (CT, 26 Nov: "keep v7 as a totally new, totally separate thing").

Same format as edits-v6/ops.py. Two extra markers at the start of a new paragraph: "§H1 " makes it a heading,
"§C " centers it. The record of each change, with who wrote what, is manuscript/novel/V7-CHANGES.md.
"""
NOTE_START = "Appendix\nAuthor's Note\nFor years, I've been talking about this.\n"
NOTE_END = "Let's begin to imagine how."

DEDICATION = "For the people I love who looked me in the eye like I'd finally lost it."

THANKS = [
    "Thank you for your time. I know how much of it you gave me, and I don't take that lightly.",
    "You just spent a whole book with a man who saw it coming and still got most of it wrong. Take what you learned, about the world and about yourself, and do better than Elijah did. Ask before you fix. Listen longer than feels comfortable. Do one real thing before noon.",
    "And when it gets loud, believe in yourself. Most of what you need, you already have.",
]

OPS_V7 = [
    ("v7-1", "", "Recognize Your Power"),  # an empty find means: a centered first paragraph, before the title
    ("v7-2", "Contents\nAuthor's Note\n", "Contents\nDedication\n"),
    ("v7-3", None, None),  # filled in by make_v7.py: the whole Author's Note becomes the Dedication
    ("v7-4", "Thursday, November 25, 2027. Thanksgiving.",
     "Thursday, November 25, 2027. Thanksgiving.\n§H1 Thank You\n" + "\n".join(THANKS) + "\n§C Recognize Your Power"),
]
