# How the work was done, 2026-11-19

Three things are written down here so a new session can do them again: what made Elijah's arc
stronger, how the ten readers were run, and how to write to the Google Doc without breaking it.

---

## 1. What made Elijah's arc stronger

CT said on the evening of 19 November that Elijah's arc "is really strong. A lot stronger than
it was when we started." These are the moves that did it, in the order they happened. Each one
is a thing to try on Grace, his mother and the others.

### Move 1. Find the behavior that is already on the page and has no cause

Elijah turns down Ruby's money, will not do the truck ads, works three weeks unpaid, says "I'm
not selling anything" in the video, and says "It's more than I'm worth up here" when he is
finally paid. The book showed all of that and never said why. CT asked one plain question: "If
he sells the farm, why didn't he keep some money for himself?" The honest answer was that the
text had no reason.

The fix was a cause, not a new behavior. CT supplied it: someone close who called him greedy.
That became Melody.

**To repeat it:** list what a character does more than twice. If the book never says why, that
is where their backstory goes. Do not invent a new trait. Explain the one that is there.

### Move 2. Run the cause to an end

A cause that appears once is a patch. Melody now has a beginning (what she said at their
father's funeral is why the farm is in a trust), a hint (he hears "Grub" when Ruby offers him
money), a scene (her call, which sets off the crash out), a consequence (he will not touch his
mother's money, and never cashes his pay), an echo (Patricia asks who paid for his year in the
city), and an end (he pays for the proofs of his book with the first cheque he lets himself
cash, hears "grub" as he does it, and does it anyway). He does not get over it. He acts anyway.

**To repeat it:** for each new piece of backstory, find the five or six places it would have
shown, and the place it stops running him.

### Move 3. Fill a blank with something the author already ruled

CT had ruled that "the farm people nurse him back." The book jumped from "Eat. Then I'll show
you where you sleep" to three weeks later. The blank became half a page: a cot, a plate twice a
day, a pump to fix, gloves left on a step, and nobody asking him anything.

**To repeat it:** look for time jumps and "a year later." Check each against his rulings.

### Move 4. Pay off what is planted, and plant what is paid

"You're just the lamp" was said in chapter 31 with the line "He would never remember it. She
would." Then nothing. It now fires inside the fight in chapter 36. In the other direction,
chapter 37 had Manny offering his back room "once, three years back," and no such scene
existed, so one was written in chapter 13.

**To repeat it:** run the plants-and-payoffs reader (section 2). Its three lists are the work
order: planted and never paid, paid without a plant, overused.

### Move 5. Put something of his at risk in the flat part

A reader mapped chapters 24 to 31 scene by scene and found that from the first fire to the day
his magnet is moved, nothing of Elijah's is at risk. Another reader noticed that after he
confesses the leak and confesses about Frank, he hides one thing. Those two findings were the
same fix: the hidden thing became a live wire (the deed), and Reuben finds it.

**To repeat it:** when a stretch goes flat, do not add an event. Look for something the
character is already hiding or already owes.

### Move 6. Let him be wrong

CT's criticism of the first attempts was that they were "a little predictable" and "a little
formulaic." What had gone wrong: every thread tied, everyone kind, Elijah always in the right,
stock props, and the text telling the reader what was coming. The repairs:

- He strikes first at the fire and does not know it (CT's ruling).
- He does not own up about the deed.
- His name is in the visitors' book at his mother's care home only "a few times a year."
- Melody is not forgiven. Her number stays blocked.
- He never says "I love you" out loud.

**To repeat it:** for each character, write down what they do that is plainly wrong and that
the book does not excuse. If there is nothing, that is the gap.

### Move 7. Count what it costs

The stroke took seven of his mother's lines. Four were saved by moving them to before the
stroke or by having Elijah say them for her ("It looks like somewhere, Ma"). Three are gone.
CT was told which three. Every large change has a cost like this and he should hear it plainly.

### Move 8. Critique before showing, and say what was turned down

Three ideas from earlier notes were rejected after thinking them through, and the reasons are
recorded (`REJECTED` in `tools/consistency-pass/ops.py`). The clearest: the notes proposed that
Grace ask Elijah out loud to bring the robot arms. On reflection her not asking is who she is.
She wants the truck to just arrive, the way she later wants the machine to "just do it."

---

## 2. The ten readers

CT asked for subagents on Sonnet 5.5 "going and retrieving information for you to process."
Ten were run in parallel in the background, each with one narrow job, each told to bring back
facts and not fixes. The main session then checked every claim against the text before acting.
About a third of what they flagged was not an error.

### What each one needs in its brief

Every reader starts cold and knows nothing. Each brief had the same opening:

- You are a research reader for a novelist's editor. Retrieve facts. Read-only: do not edit
  anything, do not use the web, do not touch git, write only your one report file.
- Where the text is, and its shape: one paragraph per line, cite line numbers, `[[i]]..[[/i]]`
  marks italics, a line holding only a non-breaking space is a scene break, lines 1 to 500 are
  the author's planning notes and are partly out of date.
- The start line of every chapter.
- The novel in six lines, so they can find their feet.
- For the continuity readers: what was recently rewritten, because that is where old text and
  new text disagree.
- Keep "what the text says" strictly apart from "my read." Quote exactly and keep quotes short.
- Write the full findings to a named file. Reply with at most 300 words, most important first.

### The ten jobs

| # | Reader | What it brings back |
|---|---|---|
| 1 | Beat sheet for a stretch of chapters | For every scene: who wants what, what is in the way, what has changed by the end, what the hero stands to lose, any clock, the last line. Then the scenes where nothing is risked. |
| 2 | One character, chapter by chapter | What they want, every yes and no, every pitch, every real question asked, every mistake and whether it repeats, every lesson and whether it sticks, every time money comes up, how each chapter ends for them. Then lessons taught more than once and decisions the text leaves unexplained. |
| 3 | A dossier on one character | Every line spoken, every gesture, everything about their past, what they know and when, every statement of what they believe in order with which way it leans, every stage of a relationship, what they ask for and what they want and do not ask for. Then contradictions, absences, and what others say about them. |
| 4 | Numbers, dates and durations | Ledgers for the timeline, ages, counts, money, distances, deadlines, and "first time" and "never" claims. One list of contradictions. |
| 5 to 7 | Continuity, one third of the book each | People facts, family, objects and where they are, where people live and how they move, who knows what, weather and season, repeated text, leftovers from an older version. |
| 8 | Supporting cast against the author's own character pages | The plan, the page, what they want, whether they change, plan against page, where they go missing, their last line, and what the book raises about them and never answers. |
| 9 | Plants and payoffs | Every recurring object, phrase, gesture and promise with every occurrence. Three lists: planted and never paid, paid without a plant, overused. |
| 10 | A cold read | Told not to read the planning notes. Logs every "wait, why?", "wait, who?", "I don't believe it," "that again," where attention drifted and where they could not stop. Marks each why as answered later or never answered. No fixes. |

Reader 3 was run for Grace only. **It should be run again for his mother, David, Marta and
Melody** as part of the next pass. Reader 2 was run for Elijah only.

Reader 10 is the closest thing to CT's own way of working. Its never-answered whys are the
same kind of question he asks.

### How to give them the text

The readers read a local file, not the Doc.

1. Read the Doc with the Docs connector's `read_doc`. The result is too large to show and is
   saved to a file.
2. `python3 tools/consistency-pass/doc_sync.py dump <saved-read.json> drafts/_private/corrected.txt`
   writes it one paragraph per line with italics marked.
3. Get the chapter start lines with `grep -n "^Chapter [0-9]*:" corrected.txt`.
4. Launch the readers together, in the background, with `model: sonnet`.

`drafts/_private/` is ignored by git. The text must not be committed. The reports quote the
book heavily, so they are kept out of git too and published only to the private reading page.

---

## 3. Writing to the Google Doc

Only when CT has said to, in so many words.

The Doc is about 3,400 paragraphs in one tab. Everything below was learned by doing it.

### What works

- `replaceAllText` needs no positions and cannot land in the wrong place. Use it for nearly
  everything.
- A newline in `replaceText` makes a real new paragraph.
- `searchByRegex: true` works. `.*` stays inside one paragraph. `^...$` anchors to a whole
  paragraph, which is how one paragraph is replaced when the same words also appear inside a
  longer one.
- The replacement takes the style of the first character it replaces. Text typed into a plain
  paragraph comes out plain.
- A scene break is a paragraph holding one non-breaking space. Write it as ` `.

### What to watch

- **A find must match exactly one paragraph in the whole Doc.** The planning notes at the top
  quote lines from the book, so a sentence can be in two places. `doc_sync.py emit` simulates
  every request against the Doc's current text and refuses if a find hits twice.
- **Order matters** when one change creates text another change looks for. `ops.py` sorts one
  pair for this reason.
- **Italics cannot be typed.** New text carries `[[i]]..[[/i]]` markers. After the text is in,
  `doc_sync.py fixup` reads the Doc again and writes one batch that sets the italics, deletes
  any paragraph marked `[[DEL]]`, styles new chapter headings, and strips the markers. That
  batch uses positions, so it is sent with `writeControl.requiredRevisionId` from the same read.
- **Paragraphs cannot be deleted by find and replace.** Replace the paragraph with `[[DEL]]`
  and let the fixup batch delete it.
- **Moving a scene means deleting it and typing it again.** Chapters 13 to 15 were rebuilt that
  way. The retyped scenes were checked against his original text afterwards.

### The loop

1. Add the change to `ops.py` as a new stage. Each entry is the chapter, the kind (`L` literal,
   `R` regular expression, `P` whole paragraph), the text to find, the replacement, and why.
2. `apply.py` runs every stage against the saved copy of the original Doc text and writes
   `book.json`: the book as it should be, with each paragraph marked untouched, changed, new
   or moved.
3. `STAGE=n doc_sync.py emit` checks the stage against the Doc as it is now and writes the
   requests in batches.
4. Send each batch with the connector's `update_doc`. The requests have to be typed into the
   call, so keep batches under about 8,000 characters.
5. Read the Doc again. Run `doc_sync.py fixup` and send that batch if there is one.
6. Read the Doc again. `doc_sync.py verify` must print `THE DOC MATCHES THE BOOK`. It compares
   every paragraph, words and italics.
7. Rebuild the reading page and publish it, so the Book tab is what is in the Doc.

### Starting again in a new session

`apply.py` needs the Doc's text from before the pass, and that copy is gone. Two ways forward:

- **Simplest.** Treat the Doc as it is now as the new starting point. Dump it, save that as the
  baseline, start a fresh list of changes, and mark only the new session's work in the Book
  tab. The record of the 19 November changes stays in `ops.py` and on the Changes tab.
- **If the old marks are wanted.** The published reading page still holds the Book tab with
  every 19 November mark. Read the artifact and take the marks from its HTML.

Either way, read the Doc first and trust it over any file. He edits it by hand.
