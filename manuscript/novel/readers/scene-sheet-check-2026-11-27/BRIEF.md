# Brief: check the scene sheet against the page

You are a research checker for a novelist's editor. You retrieve facts. Read-only: do not edit any existing
file, do not use the web, do not touch git. Write only your one report file.

## The files
- The book: `/tmp/claude-0/-home-user/0213088c-16d1-53c9-b974-eea47de9d5ac/scratchpad/OUT/v6.txt`
  One paragraph per line. `*...*` marks italics. A blank line is a scene break. Read it with the Read tool
  using offset and limit; cite line numbers.
- The scene sheet: `/tmp/claude-0/-home-user/0213088c-16d1-53c9-b974-eea47de9d5ac/scratchpad/sheet.txt`
  One block per scene ("=== ROW n"), with the book line range for that scene, then the cells.

## The novel in six lines
Surviving the Singularity. Elijah Madrone, a self-taught data man in a Sonoma County town, shows three
realtors an AI tool at his friend David's bar (late 2022) and it costs them their work. He goes to San
Francisco, loses his footing, his mother has a stroke, the farm is sold, he lives in his truck, and in March
2025 he arrives at a farm co-op outside Ardell (Grace, Marta, Lou, Priya, Curtis, Irene, Denny, Tyler, Rosa
and others). Acts Three and Four are the co-op, 2025 to late 2027. "Meanwhile" sections follow Aaron Bidwell,
a land buyer. The last chapters are Thanksgiving 2027 and an Epilogue.

## Your job
For every row in your range, read the whole scene on the page (the row's line range), then check each cell
of that row against the page:

- **When** and **When (basis)**: does the page support the date? List every time marker in the scene (a
  weekday, a month, a year, a season, a holiday, "three weeks later", an age) and say if the cell misses or
  contradicts one. Also flag a When that cannot sit between the rows before and after it.
- **Where**.
- **Whose scene** (whose point of view).
- **On the page**: everyone present or speaking in the scene, including by phone or message. Flag anyone
  listed who is not in the scene, and anyone in the scene who is not listed.
- **What happens**: is every statement true of this scene? Is anything important in the scene left out?
- **What turns**: does the scene support it?
- **Threads**: only names from the fixed list below. Flag a listed thread with no trace in the scene, and a
  thread plainly in the scene that is not listed.
- **Opens a question** and **Closes a question**: is that question really raised, or answered, in this scene?
- **Numbers on the page**: every item listed must be in the scene, exactly as quoted. Also flag any number,
  date, count, sum of money, age or duration in the scene that the cell leaves out and that a later scene
  would have to agree with (skip throwaway ones).

Label each finding one of: WRONG (the cell contradicts the page), STALE (the cell describes something that
is no longer in this scene), MISSING (the page has something the cell should list), DEBATABLE. Quote the
page exactly and briefly, with the line number. Do not report cells that are right. Do not suggest changes
to the book's text.

One recent change to know about: the last edit (number 234) changed Chapters 17, 18, 34, 35 and 36 so that
Grace does NOT know Elijah kept his robot arms (they are stored at Richard Praether's barn) until the co-op
table finds out in Chapter 34. A cell that has Grace knowing earlier may be stale. Check it on the page; do
not assume.

After the rows, add two short lists:
1. **Contradictions inside the book** that you noticed in your range (dates, ages, counts, money, who knows
   what, where someone is), with both line numbers.
2. **Rows that disagree with each other** inside the sheet (a When that runs backwards, a question closed
   that was never opened in your range, a person in two places).

## The fixed thread list
The machine (AGI, the labs, the Architect, the bet); Elijah and Grace; Elijah's book and notebooks; Elijah
and Ma; David and the Bear Flag (Ray, the three careers); Lou; The boxes and Rod Code (Tyler, the pledge,
the network); The co-op's money (pay, the trust, the land, votes); Wes and the band; The land buyer
(Bidwell, the LLC, the parcels); Denny's channel; Ruby and Porchlight; The route and the county (Curtis,
Rosa, Mrs. Delgado); The arms (Praether); The Ochoas; Irene and Walt; The rovers and Priya's soil; Wren;
Marta's shoulder and the welder gap; Grace and fire; Devendra; Frank and the tool library; Melody; Grace's
family (Faith, her father); Elijah's father

## What to hand back
Write the full findings to your report file, row by row (skip rows with nothing wrong, but end with a line
listing the row numbers you found clean). Check every quote by reading the line before you write it down.
Then reply with at most 250 words: how many rows you checked, how many findings of each label, and the
five most important.
