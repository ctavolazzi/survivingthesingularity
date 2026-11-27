# Plants and payoffs, 27 Nov 2026

The fifth story check CT asked for on 27 Nov: everything the book sets up, and where it pays off, or "never". Built
from the book with edits 1 to 245 by `python3 manuscript/tools/edits-v6/story_checks.py plants OUT/v6.txt manuscript/novel`.

| File | What it is |
|---|---|
| `plants-payoffs-2026-11-27.csv` | Every question the scene sheet's "Opens a question" column holds (130), with a verdict, the line that pays it, or for a "never" what was searched and how many lines it found |

In Drive: tab "Plants and payoffs" in the story checks workbook (`11zW0LizfKqEXEmFIrTQ5MpeuW7rLtg9C5mrqm1zjsf8`).

## How far to trust it

- **Counted by the script:** the list of questions (read straight from the scene sheet; a question with no verdict
  stops the run, so a new row in the sheet can't be skipped), where each payoff line is (found in the book), and for a
  "never", every line after the scene that matches the search words.
- **Claude's reading, from the whole read:** each verdict and which line pays it. The scene sheet's "Closes a question"
  column words its questions differently, so matching the two by script found only 9 of 126; every pairing here is read.
- Verdicts: **paid** (a later line answers it), **same scene** (answered where it is asked), **open on purpose** (the
  book ends on it: the vote, January, the song, who holds the plug, the watcher CT keeps unnamed), **after the book
  ends** (the dealer fight is set for December 2027), **never**.

## Counts

131 questions (edits 1 to 299): 100 paid, 15 in the same scene, 11 open on purpose, 1 after the book ends, 4 left open on CT's word. Until the seventeenth chat (27 Nov) those four read "never"; CT: "The four unanswered things are fine to be left unanswered ... Not essential to the story as far as I'm concerned." They are the four listed under Findings below.

## Findings (only two kinds: the page contradicts itself, or something is set up and never paid)

No contradictions found. Set up and never paid:

1. **"Agreed on what?"** (Ch 17 and 19): what Grace and Curtis agreed about Elijah. Searched "agreed", "agree", "knack",
   "marketing": 11 lines, none answers it. Same as finding 2 on the desires sheet; flagged for CT there.
2. **Why Lou asked Grace to write to Elijah** (Ch 26, the fence: "there's a reason why I asked you to reach out to
   him"). Searched "reach out", "write to him/you", "asked you to", "a reason why": the only hits are that line and Grace's
   "I wrote to you, Elijah" at the fire, which doesn't contradict it. The reason is never given. With Bidwell's "somebody
   near him ... close enough to eat with" and Lou as Bidwell's cousin (Appendix), a reader may take it as a shadow over
   Lou; CT's rule is that no edit clears anyone. Likely on purpose; flagged for CT only to confirm.
3. **Priya's forking trial, "run it again next year, properly"** (Ch 26). 2027 never reports it: her rows are "knee high"
   (Ch 33) and the pits go on, but the result of the second year is never given. Searched "fork", "broadfork", "trial",
   "run it again": 20 lines, none answers it (most are dinner forks). Smallest fix, Claude's wording and an invented
   result: in Ch 33, "Priya's rows were knee high." becomes "Priya's rows were knee high, the forked ones a hand taller
   than the rest." Flagged for CT: the result is his to choose.
4. **What Priya wrote on the back of the pledge** (Ch 27). Searched "back of the pledge", "shirt pocket", "the pledge": 5
   lines. The nearest is her line in Irene's kitchen (Ch 34): "I read the pledge again. It covers the field to the box."
   Smallest fix, Claude's wording, which pays it with what she says there: "I read the pledge again, and what I wrote on
   the back of it. It covers the field to the box."
