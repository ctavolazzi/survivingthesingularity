# Continuation prompt: fixes from the Riemann and Praether chat (26 Nov)

Written 26 Nov 2026 at the end of the chat that logged edits 229 and 230, at CT's request ("put a continuation prompt
for all of this ... Make sure you also upload all of this to GitHub"). Paste the section below into the chat that picks
it up.

## Hand-off prompt (27 Nov, after edit 234; paste this into the chat that picks it up)

```
We're finishing my novel, Surviving the Singularity. Pick up where the Riemann and Praether chat left off.

1. Work on branch claude/singularity-publication-build-kparqk in both repos (ctavolazzi/survivingthesingularity and
   ctavolazzi/_workbench). Push every commit there, whatever branch this chat was given. No pull requests. Another
   chat may be logging on the same branch: fetch first, read the "Next edit" line in manuscript/novel/TODO.md before
   you number anything, fetch again before every commit, and merge, never force-push.
2. Read manuscript/novel/REFERENCE.md (start at section 1 and follow it), then the first section of
   manuscript/novel/CHECKPOINT-2026-11-26-riemann-praether.md, then CHECKPOINT-2026-11-27-eleventh.md, TODO.md and all
   of WRITING-INSTRUCTIONS.md. Then STATE.md and the top entry of sessions/LOG.md in _workbench.
3. Read both Docs fresh with the Docs connector (ids in REFERENCE.md, section 1) and run make_v6.py and verify.py. You
   should get all 234 check rows passing, 223 rows "accepted" in v8, edits 224 to 234 "not in the Doc", and nothing
   PARTIAL. If you get anything else, stop and tell me.
4. Don't change any Google Doc. Don't put the open list to me unless I ask for it.

The last thing logged was edit 234: Grace doesn't know about the arms until the table finds out in Chapter 34. One
question from it is waiting on me (whether the fight at the fire should name the hiding). The smell pass has not been
started; its own prompt is at the end of CHECKPOINT-2026-11-27-eleventh.md.

When you're done spinning up, tell me in one line that you're ready and that the next edit is 235.
```

## Close of this chat, 27 November (read this part first)

- **Last word from this chat (27 Nov, final turn).** The one branch for the book is
  `claude/singularity-publication-build-kparqk`, in both repos; every commit from this chat is on it (the session
  branch `claude/riemann-hypothesis-scene-li2h5n` holds nothing it lacks). This chat started a cell-by-cell check of
  the scene sheet against the book; its readers stopped on a usage limit and returned nothing. That check is
  **superseded** by the other chat's full read (commit f644636e, 30 cells fixed, the Epilogue's word count among them)
  and its thread tags (1d339a15). This chat's own sheet fixes (rows 52, 53, 59, 123, and "This Sunday" for the lien
  sale) are in both the Sheet and the repo copy. Where this section and newer notes disagree, the newer notes win.

The chat ran on after the prompt further down was written. Where its work stands now:

- **Edit 234, logged last (27 Nov), changes what the bullets below say about counts.** CT: "She can't know about the
  arms. It has to be a secret he's been keeping from her, or else the breakup doesn't work." Grace now believes the
  arms went at a lien sale, Lou goes to Praether's with Elijah, Chapter 18's opening is cut, and she finds out at the
  table in Chapter 34. It reverses his decision of 26 Nov in the plan, 10.5. The build now passes 234 rows (608
  replacements), 224 to 234 are not in the Doc, and **the next edit is 235**. One question is held for him: should the
  fight at the fire name the hiding. Record: `drafts/edit-234-grace-doesnt-know.md`.
- **The scene sheet** was brought up to edit 234 in four rows (52, 53, 59 and 123), in the repo copy and in the Google
  Sheet. Row 59 (the cut Chapter 18 scene) is kept and marked as cut, so the numbering holds.

- **Edits 229 and 230 are on `claude/singularity-publication-build-kparqk`**, merged on CT's word ("I think it should
  be merged into the current branch"). The eleventh chat was logging at the same time and renumbered its own edits to
  231 to 233 at the merge; 229 and 230 kept their numbers. The session branch
  `claude/riemann-hypothesis-scene-li2h5n` holds nothing the shared branch lacks.
- **The fix list below, item by item:**
  - 1, 2 and 3 are done, in edit 233 (the eleventh chat's finishing pass): the secrecy is said once, at the barn;
    "Good. Keep it that way." is gone from Chapter 18; a scene break stands before the Riemann dinner.
  - 4, the lien sale: checked on the page on 27 Nov, nothing to fix. Lou covers what Elijah owes on the unit before
    the visit to Praether, so the sale is off, and "They'll be here on Wednesday" and "Elijah canceled the storage
    unit" hold.
  - 5, 6 and 7 are CT's taste calls. They are in `CHECKPOINT-2026-11-27-eleventh.md`, "Open with CT".
  - 8, 9 and 10 are still to do, on his word.
- **The prompt below is superseded.** The current one is the smell pass prompt at the end of
  `CHECKPOINT-2026-11-27-eleventh.md`. Don't paste the one below.
- **The smell pass prompt was run once already, inside this chat (27 Nov).** CT pasted it with "Roll up all the edits
  into GitHub and be sure to use the scene spreadsheet". Spin-up was clean on fresh reads of both Docs: make_v6.py
  passed all 233 rows (591 replacements); verify.py on v8 showed 223 accepted, 224 to 233 not in the Doc, nothing
  PARTIAL. The scene sheet's rows for his two places: 29 to 32 (the party, Chapters 9 and 10) and 47 to 49 (the truck,
  Chapters 14 and 15). He then asked a question about the story instead (below). **No smell line was shown or logged.
  The next edit is still 234.** The saved reads were in that session's scratchpad and are gone; read both Docs again.
- **A commit that broke the build went up and was fixed by the next one** (e9862f96, then b992f584). The cause and the
  rule are in `EDIT-LOGGING-PROCEDURE.md`, "Things that have gone wrong before".
- Lessons from his corrections in this chat are in `WRITING-INSTRUCTIONS.md`: section 15b, the people in section 12
  (Tyler, Marta, Curtis, Grace, Praether) and "Read the chat before you ask" in section 14.

### Not logged: one idea of Claude's, said to CT on 27 Nov, no answer yet

Grace's "promise me, no matter what happens, you will put humans first" (Ch 27, edit 229) never comes back; the word
"promise" between them appears again only for the journal post in Chapter 36. At the gate (Ch 36) Elijah's refusal to
bring the arms in over the table's no is arguably that promise kept, in a way she can't accept. One line there would
tie the two scenes. It is not an edit. The fight in Chapter 36 is his, and he has said he doesn't want to add. Write
nothing unless he asks for it.

### CT's words in this chat that are context, not for the page

- Why the scene exists: "I know I said already a bunch of times that I don't want to add anything new, and I really
  don't, but this is the one that will really make it click for anybody who's out of the loop."
- What it is for: "I feel like this is kind of a linchpin scene for what happens later with the ASI sort of like all of
  a sudden existing. And we may even not need to mention it again after this because it's like really clear where
  it's headed for anybody that gets it. But for people who don't get it, it might be a bit of a jump. But that's okay,
  because it'll feel like a jump in real life."
- Tyler: "now he suspects that this other person knows too. More than they're letting on. Which will not pay off. We
  don't need to make that necessarily pay off, but we could just like loosely connect it with following events".
- What is left to do: "I don't know what else we would even add. Like at this point, we just need to kind of like work
  through how to subtract things to make sure the story is nice and clean. Tight, easy, easily, you know, consumed for
  an average reader, for the layperson, which I think we've done a pretty good job of so far. But we're getting real
  close to doing a version bump and then producing something for me to read. So let's get ready for that next step."
- The arms: "The arms, stay there for a while ... However we resolved it before. I can't remember what we ended up
  deciding to do with them." The book: offered and refused in Chapter 34, let go in Chapter 36 ("I'm letting it go"), left in Praether's barn
  in Chapter 37 ("Nobody had ever bid on them. He left them where they were.").
- "But I think we've got most of the loose ends tied up now, right?" Answered: this thread, yes; the list of what is
  his is in the eleventh checkpoint, "Open with CT".

### "What's really at stake here in this story? Especially in the second half?" (CT, 27 Nov)

Claude's answer, from the scene sheet (rows 50 to 138) and the pages of Chapters 34 to 37. He has not replied to it.

- Under everything, who gets to choose. The machine that could take over keeps asking ("It asked"), and Elijah is
  tested on whether he will do the same with the people he loves.
- What is on the table in Acts Three and Four: people eating (a hundred and forty boxes, money gone in December, and
  Grace makes it one woman, Mrs. Delgado with her insulin in the door of the fridge); the harvest ("Forty bodies for
  nine days. We have twenty-two", then the Ochoas leave and it is twenty; Patricia buys more than half of what Lou
  grows); Elijah's place ("Maybe you should go home" against "This is my home, he thought"); Grace; and being right
  ("Were you right?", from a woman whose own job hangs on the answer).
- The stake itself is the arms. He has the machine that would bring in the harvest and feed Mrs. Delgado, the table
  says no, and he keeps to the no. Grace wanted them brought in anyway ("Once they're packing boxes, nobody sends them
  back."; "You only respect a no when it costs you nothing."). His answer is "This is the gate" ("My house, my choice.
  You couldn't have made him."). That is the book's question about the machine, asked of a man, and it costs him Grace
  and the farm.
- Weaker places, from `STORY-REPORT-2026-11-26.md` (written before edits 224 to 233, so check each on the page first):
  some losses are paid back inside the chapter that charges them; Elijah never stands in front of the Ochoas; the
  third time he fails to go south costs nothing.

### Sources for the facts in edit 229 (web search, 26 and 27 Nov; search summaries only, the articles could not be opened)

- The proof: https://www.scientificamerican.com/article/anthropic-mathematician-claims-to-prove-riemann-hypothesis-most-famous-problem-in-all-of-math/
  and https://www.science.org/content/article/ai-may-have-solved-math-s-greatest-mystery-can-humans-understand-answer
  and https://www.smithsonianmag.com/innovation/ai-cracked-the-riemann-hypothesis-the-most-famous-unsolved-math-problem-the-proof-is-17-million-lines-long-180989939/
  and https://www.forbes.com/sites/jonmarkman/2026/11/24/riemann-hypothesis-proof-built-with-claude-passes-lean-verification/
- The problem itself: https://en.wikipedia.org/wiki/Riemann_hypothesis
- Navier-Stokes, September 2026: https://www.npr.org/2026/09/22/nx-s1-5968588/openai-navier-stokes-problem-mathematicians-learn-little
- Perelman and the million: https://physicstoday.aip.org/news/mathematician-turns-down-1-million-prize-for-proving-the-poincare-conjecture
- GTA 6, out 19 Nov 2026: https://www.aljazeera.com/news/2026/11/19/grand-theft-auto-vi-launches-to-rave-reviews-after-13-year-wait

As reported then: announced 20 Nov 2026, checked by computer and certified the next day, not yet read through by
mathematicians, and the prize still unclaimed. Curtis's "solved" is ahead of the mathematicians; that is in character.

## The prompt written on 26 November (superseded; kept for the record)

---

You're picking up the novel *Surviving the Singularity*. Work in `ctavolazzi/survivingthesingularity` and
`ctavolazzi/_workbench`, both on the branch `claude/singularity-publication-build-kparqk`. Fetch it fresh first.

**Another chat is logging new edits from CT on that same branch right now.** Before you number anything, read the "Next
edit" line in `manuscript/novel/TODO.md` on the freshest fetch. Pull again before every commit, so the two chats don't
take the same edit number or overwrite each other's rows in `ops.py` and `checks.py`.

**Read first:**
- `manuscript/novel/REFERENCE.md`, section 1
- `WRITING-INSTRUCTIONS.md`, all of it
- `EDIT-LOGGING-PROCEDURE.md`
- Edits 229 and 230 in `EDITS.md`, with their records in `manuscript/novel/drafts/edit-229-riemann.md` and
  `edit-230-praether-and-lou.md`

**Then build the book:**
1. Read the v5 Doc fresh: "StS v5 draft (Nov 23)", `1TyvxCS0y_FPXGllFo3vaO2AqyoCBrS-VWX9Aslmp0hA`.
2. Run `make_v6.py` on it. Every row must pass.
3. Work from its `v6.txt`.

**What the last chat did (all logged in GitHub only, not in any Doc):**
- **Edit 229, Chapter 27.**
  - At the Friday dinner before Thanksgiving 2026, Curtis announces the Riemann hypothesis is solved. Marta is shaken:
    "It means AI is better than humanity at math," "And it always will."
  - Tyler says "who cares" and brings up GTA 6, Elijah says "one giant leap closer to RSI," and Elijah starts to
    suspect Tyler knows more.
  - Then Grace makes Elijah promise to put humans first.
  - It fits the real dates: the proof was announced 20 Nov 2026 and GTA 6 came out 19 Nov.
- **Edit 230, Chapters 17 and 18.**
  - Grace and Elijah make the deal with Praether before the arms come: his terms, the ordnance, the
    military-industrial complex, "Skylinks and Starnets," and "You messing with me, son?" answered with the lizard
    people, then he laughs.
  - His first line has "a rattle in his voice like a can of paint being turned over," and the VA letter goes into the
    mailbox.
  - The arms arrive on time, and Lou helps put them in the barn and gives the ace in the hole talk: "They're your
    people too now. Don't forget that."
  - The arms stay in the barn to the end.
- **Status:** all 230 check rows pass, and `verify.py` on the v8 Doc shows 223 accepted and 224 to 230 not in the Doc.

**Fixes to make.** Items 1 to 4 are continuity problems: for each, show CT one line and log it on his word. Items 5 and
6 are his taste calls, so just ask.

**Done, 27 Nov, in the other chat's edit 233** (the finishing pass, `drafts/finishing-2026-11-27.md`), on CT's word there
("finish everything ... deleting, buffing out the hard spots"): item 1 (Grace's Chapter 17 line cut, Lou's loan now a
gift; Chapter 18's "Good. Keep it that way." cut), item 2 with it, and item 3 (a scene break between the two Fridays).
Item 4: with Lou paying the unit, the lien sale no longer happens, so nothing is in the way; left as it is. Items 5 to 7
are still his. Edit 228's held Rosa scenes and the "stay for free" talk are placed as edits 231 and 232. The next edit
is 234.

1. **Lou's secrecy is said three times in a row.** Grace in Chapter 17 ("keep it between the three of us"), Lou at the
   barn (same words), and the Chapter 18 opening ("Good. Keep it that way."). Cut the Chapter 18 instance, and probably
   Grace's "three of us."
2. **"Good. Keep it that way."** already appears earlier in the book (Chapter 9; first written here as "about Chapter 5"), so fix 1 also clears
   this repeat.
3. **Chapter 27 has two Friday dinners with no break between them.** The Riemann dinner runs straight on from the
   post-midterms dinner about two weeks earlier. It needs a scene break or a time line.
4. **Lien sale.** Chapter 17 says it is "at the end of the week." The new deal has the arms arriving "on Wednesday" and
   never says they beat the sale. Check the days or add one line.
5. **"Wingnut"** appears three times: Priya's "Wingnuts," "I speak wingnut" (Ch 17), and "Curtis was a wingnut" (Ch 27).
6. **"Taken aback"** appears twice (Ch 16, and the Grace scene in Ch 27). CT said with Praether that the book has had it
   enough. The Ch 27 one is his own dictation.
7. **Praether's "I'll check them myself" and the ordnance threat never pay off.** CT said loose is fine. Leave it unless
   he says otherwise.

**Before the version bump CT wants to read:**

8. Put edits 224 onward in. Ask CT which way first: as suggestions in the v8 Doc ("StS v8 draft (Nov 26)",
   `1nSA0h5SlWtlVVPUYdq5AEt5BPjKuew5tKJjw3lWfVk8`), or as a new Doc from `make_v6.py`'s .docx. Then add it to the
   bridge map and make a new large print PDF for him.
9. The 19 empty paragraphs in the v8 Doc where the pictures were.
10. Fold in the findings of CT's separate contradiction sweep, when he hands them over.

**Still held for CT:**
- Edit 226: "under 6 months" or "under a year"
- Grace's winter away, which isn't written
- Edit 228's Rosa scenes and the "stay for free" talk
- "Creator Fund" or "creator fund"
- The gas cap (Ch 25)
- "Marta had heard it as a murder" (Ch 39)
- The Instagram synopsis
- The ISBN and the release build
- The merge to `main`, only when he says

**Rules:** CT's words go in word for word, and you mark what Claude worded and every fact Claude invents. Nothing goes
into a Google Doc until he clears it. No em dashes. At the end of the session, update `STATE.md` and `sessions/LOG.md`
in `_workbench`.
