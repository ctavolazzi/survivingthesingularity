# Who knows what, and when: the knowledge sheet, 27 Nov 2026

CT, 27 Nov: "having key bits of information logged in a spreadsheet, and then having flags indicating which characters
know them at what time would really help us."

Built from the book with edits 1 to 236 by `manuscript/tools/edits-v6/knowledge.py`. The only thing written by hand is
the list of facts and, for each person, the exact line where the page shows them knowing it. The script finds every
line in the built book and reads the chapter off the page: 35 facts, 113 lines, all found.

| File | What it is |
|---|---|
| `knowledge-sheet-2026-11-27.csv` | One row per fact, one column per person: the chapter they learn it, and whether they know, suspect or have it wrong |
| `knowledge-flags-2026-11-27.csv` | The flags: K (knows), S (suspects or half knows), F (believes something false) for each person at the end of each of seven phases |
| `knowledge-evidence-2026-11-27.csv` | One row per line of evidence, with its line number in `v6.txt` |

In Drive the three are tabs of one Google Sheet; its id is in `EDIT-LOGGING-PROCEDURE.md`, "Where things stand".

## How to read it

- A fact is something at least one person in the book does not know or gets wrong. Things everyone knows are not in it.
- **An empty cell means the page never shows that person knowing. It does not mean they never find out.**
- "With the table" means it was said in front of the co-op and that person was there. Denny is left out of April 2027
  (he was in Spokane).
- "From Ch N, off the page (told Ch M)" means the book tells us in Ch M that they had known since Ch N.
- Phases: The Bar (Ch 0 to 5), The City (6 to 15), Farm 2025 (16 to 25), Farm 2026 (26 to 28), Early 2027 (29 to 33),
  Fall 2027 (34 to 36), The end (37 on).

## How to use it before logging an edit

Find the facts the new lines touch. Check that nobody says or does something that needs a fact they don't have yet,
and that a secret someone is about to learn is still a secret to them on the page. When a line is added or moved,
add or change its row in `FACTS` in `knowledge.py` and run it again; a quote that is no longer in the book stops the
run.

    python3 manuscript/tools/edits-v6/knowledge.py OUT/v6.txt manuscript/novel --date YYYY-MM-DD

## What Grace knows when she finds out about the arms (Ch 34), and at the fire (Ch 36)

Knows: he once had two arms (her own message, Ch 15). Believes: they went at a lien sale (his lie, Ch 17). Then, at the
table: they are in Praether's barn, they have been there since his first weeks, and Lou told him to keep it from her.
Also knows by then: he sold his mother's farm (Ch 24) and to whom (Ch 33); the coffee can of order slips (Ch 32);
that he has never cashed his pay checks (Ch 32); what he said during the tea, which he does not remember (Ch 31).
Suspects with him that the machine is already here (Ch 32).

Does not know, on the page: that he tried to sell the arms and nobody bid (A5); that Ruby offered him a million dollars
and he said no (A6); that the farm money is in an account with his name on it and he takes none (A7).

## Found while building it (CT's to rule on; nothing was changed)

1. **"Why did you pretend to be poor?"** CT described Grace's anger this way on 27 Nov. Neither the table scene nor
   the fire has her say it. If she does, the page gives her grounds and a blind spot: she does not know he tried to
   sell them (A5), and she does know he has refused his pay for a year (A8), which cuts against "pretending".
   The fire (Ch 36) never mentions the hiding at all; that question has been held since edit 234.
2. **Tyler sent him to Praether's** for "a couple of big crates" (Ch 17), and Ch 19 reminds the reader. At the table in
   Ch 34 he hears "Praether's pole barn" and shows nothing. Not an error. A look or a half line is available.
3. **"Agreed on what?"** (D7). Curtis says the table agreed on Elijah's "knack for marketing" (Ch 17); Elijah wonders
   again in Ch 19; the page never answers it.
4. **"They've been there since my first week"** (Ch 34). The arms arrive in his second week (already in the scene
   sheet audit).
5. **Marta never hears that the three are fine.** Ch 39: "He would have to tell Marta." The book ends before he does.
   Probably on purpose.
6. **His age.** Grace says "You're almost forty" in Ch 25, and nothing on the page says how she knows it. This is the
   open place for the birthday plan (Grace finds out his birthday passed in his first year).
7. **The watcher (G2).** The sheet names nobody, and no row clears anybody. Keep it that way.
8. **Lou and Bidwell (G4).** Only Bidwell and the reader know. The page never shows Lou knowing who his mother's
   family was.
