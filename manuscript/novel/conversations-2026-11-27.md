# The conversation map, layer one, 27 Nov 2026

CT, 27 Nov: "Map the conversations, who has them ... who it's between, how it influences the story, how it develops
the characters, what type of senses are activated in the conversation." Agreed in two layers. This is layer one: what
a script can count. Built from the book with edits 1 to 236 by
`python3 manuscript/tools/edits-v6/story_checks.py conversations OUT/v6.txt manuscript/novel`.

| File | What it is |
|---|---|
| `conversations-2026-11-27.csv` | One row per scene (137): words, how much is talk, lines of talk, who speaks and how many lines, and counts of sound, touch, smell and taste words |
| `conversation-pairs-2026-11-27.csv` | Each pair of people: lines traded, scenes, first and last chapter, every chapter |
| `conversation-lines-2026-11-27.csv` | Each person's lines of talk, chapter by chapter |

In Drive: the Google Sheet "Surviving the Singularity: story checks, conversations (edits 1 to 236)"; id
`1frR-rdgqZ_d7Dq70T0gG-0uhlc7siyZHEzlNP81lhxg`, three tabs.

## How far to trust it

The book has 1,937 lines of talk. 700 have the speaker's name beside them. 1,040 more were placed by rule: "she said"
goes to the last woman named, an unnamed "he" goes to Elijah (the book sits on his shoulder), and an untagged line
between two people goes to the other one. 197 (10%) were not placed. **So the counts by person and by pair are rough.**
The rule gives Elijah too many lines and other men too few: Lou in the radish scene (Ch 17) and Curtis under the
hood (Ch 37) lose lines to him. "The old man" in Chapter 17 is Praether, not the man on the curb. What is solid:
which scenes are mostly talk, how many voices a scene holds, and the sense words.

## What it shows (solid)

- **The senses.** Across the book: 551 sound words, 370 touch words, 17 smell words, 14 taste words. 122 of 137 scenes
  have no smell word and 126 have no taste word. Sound and touch are everywhere. This is the measure behind CT's
  smell pass and the taste pass to come.
- **The most talk:** the walk to the beds and the tomato dinner (Ch 33, 71% and 66% in quotes), Priya and Grace the
  night before the county meeting (Ch 30), Irene's kitchen (Ch 34), the ride with Gus (Ch 11).
- **The most voices in one scene:** the October meeting (Ch 34) and Thanksgiving 2027 (Ch 38), fourteen each; the
  tomato dinner, twelve.
- **Ten scenes have no talk at all,** nearly all of them Elijah alone in Acts One and Two.

## Leads for layer two (rough counts, to be checked by reading)

- **Grace and Lou.** By Claude's reading as well as the count, they have very few direct exchanges: the introduction
  (Ch 16), the radishes (Ch 17), a line at the tomato dinner (Ch 33), "Did you know?" (Ch 34). CT's note for edit 234
  says she "wants a father figure so bad, she doesn't want to lose Lou." The page shows almost none of that bond before
  it is tested.
- Pairs at the co-op the script finds trading no lines: Marta and Wren, Reuben and Wren, Denny and Patricia. Pairs with
  one or two: Curtis and Tyler, Grace and Wren, Lou and Reuben. Each needs a look on the page before it is called a gap.
- Who goes quiet late: Priya has no lines counted in Chapters 35 to 37 or 39.

## Layer two (for a fresh session)

For each conversation that matters: who wants what, what changes between the two people, what it sets up or pays off
(cross-checked with `knowledge-sheet-2026-11-27.md`), and which sense carries it. It has to be read, from a fresh read
of the book, starting from the leads above and the pair sheet. It should add only what the scene sheet's "What
happens" and "What turns" columns do not already say.
