# Edits 235 and 236: the smell of the truck (Ch 15) and the smell of the party (Ch 9)

27 November 2026, the smell chat (twelfth). Source: CT's two places for smell, 26 Nov (`WRITING-INSTRUCTIONS.md`,
section 7a), placed and shown to him on 27 Nov, corrected once, and logged on his "Yes, log them". Logged only; not in
the v8 Doc. The pass that found the places is `manuscript/novel/smell-table-2026-11-27.md`.

**CT's words are in bold.** Everything else is Claude's.

## CT's words, as he gave them (26 Nov)

"the Smell of a car you've been living in. The way you stop noticing it after a while but everyone else sure does,
right away."

"the SMELL of a high-dollar party. The faint back notes of cleaning supplies. The perfume, how it acts like a
lightning rod for knuckleheads and more or less behaves like a slime mold, expanding out in every direction, but how
it is utterly decimated by the ferocity of the air from the kitchen."

His correction to the truck line (27 Nov): "The delivery bag which had held on to just about every order he'd ever
carried." With it: "We can't be too absolute in situations that don't actually seem feasible for absolution.
Remember, only a Sith deals in absolutes." (The lesson is in `WRITING-INSTRUCTIONS.md`, 15c.)

## 235, Chapter 15: the five months in the truck

Book now:

> He showered at the Y for five dollars, and when five dollars got to be a lot he stopped. He was on the last hole of
> his belt by Christmas.

Change to:

> He showered at the Y for five dollars, and when five dollars got to be a lot he stopped. By then the cab had **the
> smell of a car you've been living in**: smoke, a wet jacket, and **the delivery bag, which had held on to just about
> every order he'd ever carried. You stop noticing it after a while, but everyone else sure does, right away.** He was
> on the last hole of his belt by Christmas.

Corrected in place the same day (Claude's own review, on CT's "Finalize changes"; the edit is not in the Doc). As first
logged it read: "The cab had a smell by then: weed, a wet jacket, and the delivery bag, which had held on to just about
every order he'd ever carried. A car you've been living in gets like that. You stop noticing it ..." Two faults:
it dropped "the smell of" from his phrase and added a filler ("gets like that"), and it said "weed" three sentences
after "The bag of weed had to last." Now his phrase is whole, the filler is gone, and "weed" is "smoke". CT approved
the first wording and has not seen this one.

## 236, Chapter 9: the house on the hill

Book now (the dining room):

> ...Elijah knew four of the faces from slides. The rest just looked like people who owned things.
> There was one empty chair, near the head, with a full place setting in front of it.

Change to (a new paragraph between them):

> ...Elijah knew four of the faces from slides. The rest just looked like people who owned things.
> Under the candles and the wine were **the faint back notes of cleaning supplies.** Over all of it was **the perfume.
> It acted like a lightning rod for knuckleheads and more or less behaved like a slime mold, expanding out in every
> direction.** Two men had found reasons to stand behind the same woman's chair.
> There was one empty chair, near the head, with a full place setting in front of it.

Book now (the back hall):

> Four caterers in black came out through it as they got there, empty-handed, and stood along the hall wall with
> their phones, like people sent out of their own room.

Change to:

> Four caterers in black came out through it as they got there, empty-handed, and stood along the hall wall with
> their phones, like people sent out of their own room. The door swung behind them, and the kitchen air came out into
> the hall, hot, with fish and butter in it. The perfume had come down the hall with Elijah and Ruby. It was **utterly
> decimated by the ferocity of the air from the kitchen.**

## What Claude changed in his words

- "acts" and "behaves" are "acted" and "behaved", for the book's past tense.
- His "how it acts ... but how it is" became separate sentences around the scene.
- After he saw the draft: "The perfume had come down the hall with them" became "with Elijah and Ruby", because the
  sentence before it is about the caterers (clarity; not shown to him before logging).

## Facts Claude invented (his to change)

- What the cab smells of: smoke, a wet jacket, the delivery bag (the nightly smoke and the delivery runs are on the
  page).
- The two men behind the same woman's chair.
- Fish and butter in the kitchen air. Fish fits "Meanwhile" after Chapter 10: Bidwell "left the dinner before the
  fish".

## What it touches in other chapters

- Ch 8: his line at the coffee urn ("He could smell her perfume, and it was nice, and he felt a rush.") now sets up the
  perfume in Chapter 9. Not changed.
- Ch 17: Grace cleans out the cab and tosses "A delivery bag". Not changed; it now pays off the bag.
- Ch 15: the people who get close to him after the line (the pawn man, Ma, the old man on the curb, the food bank
  woman) are unchanged. None of them mentions the smell; the line lets the reader supply it.

## Checks

- Every new phrase searched in the built book first: "slime", "lightning rod", "knucklehead", "cleaning supplies",
  "decimated", "ferocity", "held on to", "a car you've" were not in it. "followed them" was (Ch 30), so the draft
  says "had come down the hall with".
- `openers.py`: no new runs in Chapters 9 or 15. No dashes.
- `make_v6.py`: all 236 check rows pass (611 replacements). `verify.py` on the v8 read: 223 accepted, 224 to 236 not
  in the Doc, nothing PARTIAL.
- Words: 148 in, none out. 103,647 words in the chapters (`story_report.py`), from 103,499.
