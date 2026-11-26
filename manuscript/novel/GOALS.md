# Goals: what "done" means for the novel

Written 26 Nov 2026, eighth logging chat, at CT's request: "Make a to-do list, make a detailed goals list, make a
reference guide for doing this, policies, procedures ... Finish the fight. It's time to be done."

The three files that run the endgame:
- `GOALS.md` (this file): what done looks like, and how each goal is checked.
- `TODO.md`: the ordered list of what is left, with the next step at the top.
- `REFERENCE.md`: how the work is done (reading order, policies, procedures, tools, pitfalls).

The book is done when CT says it is. Everything below serves that.

## 1. The story

The book's job, in CT's words (`PLAN-CHAPTERS-20-TO-36.md`, section 2): "this is why we can't blindly trust the
machines. We need to double check everything ... for the critical stuff that cannot fail, we need to do it ourselves to
the best of our ability. I mean, of course we need to use the tools." And the last page: "if you touch any heart,
please be sure to start with your own. Recognize your power."

| Goal | How it is checked |
|---|---|
| The middle has stakes. Every chapter from 20 to 36 costs somebody something that stays lost, and the next chapter opens on it. CT: "We need setbacks. We need problems." | The chain of cause in the plan, section 10.1, holds link by link in the text |
| It reads as a story, not "a series of events" (CT at Chapter 20) | Each chapter in 27 to 36 does what section 11 of the plan says, and CT's chapter questions (`WRITING-INSTRUCTIONS.md`, section 3) get a yes |
| Every person has an arc: a flaw, what is in the way, and a change | The beats in the plan, section 10.2, are on the page for Elijah, Grace, Lou, Marta, Denny, Tyler, Curtis, Priya, Wren, Reuben, Patricia and the Ochoas |
| Elijah and Grace are a will-they-won't-they that earns the fire | The quarrels in 10.3 are on the page, in order, and every line the fire throws has its setup (the table at the end of 10.3) |
| The ending stands as CT loves it | Chapters 37 to the Epilogue change only by the lines in section 13 of the plan, each with CT's yes |
| Nothing confuses a first-time reader | No open item in section 12.3 of the plan; a final readers' pass finds no continuity error |

## 2. The writing

| Goal | How it is checked |
|---|---|
| It sounds like CT | Every new passage passes the checklist in `WRITING-INSTRUCTIONS.md`, section 13, before it is logged |
| His words are his | CT's words go in word for word and are marked in each chapter's file in `drafts/` |
| Length is not the measure (CT, 26 Nov: "I don't care how long it gets I want it to be good"). The row below is kept for the record only |
| ~~The book does not get longer~~ | Chapters 27 to 36 total 22,590 words now (`story_report.py`, edits 1 to 205; an earlier 24,084 counted line numbers). They finish at or under that. Each chapter's target is in the plan, section 11 |
| Every invented fact is flagged | Each chapter report lists what Claude invented; CT changes what he wants |

## 3. The record

| Goal | How it is checked |
|---|---|
| Every change is logged in GitHub and can be rebuilt | `EDITS.md` entry, check row, ops rows and a `drafts/` file for each edit; make_v6.py passes every row |
| The Docs are untouched until CT clears them | verify.py on a fresh read of the v8 Doc shows every logged edit "accepted" (v8 was made from all 223, on CT's word, 26 Nov) and "not in the Doc" for everything newer |
| A new chat can pick up cold | `REFERENCE.md` and `TODO.md` are current at the end of every session, with "Where things stand" in `EDIT-LOGGING-PROCEDURE.md` |

## 4. The finished book

| Goal | How it is checked |
|---|---|
| One current copy | A new Google Doc made from make_v6.py's .docx (on CT's go), named for what it is, marked CURRENT in the bridge map. Its structure and gate: `NEXT-BUILD.md`; `build_gate.py` says READY |
| The front and back are right | Title page first; Dedication; Thank You and "Recognize Your Power" last; the cover credit on the copyright page (CT: "cover credit : me, the author, sketches and Midjourney", inside, where other books have it); an ISBN CT buys |
| The files he sells | The large print PDF on request, then the release build (PDF and EPUB) with every check in `publication/novel/output/CHECKS.md` passing |
| CT says it's done | CT's word |
