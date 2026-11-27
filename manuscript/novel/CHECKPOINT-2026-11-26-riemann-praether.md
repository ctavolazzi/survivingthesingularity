# Continuation prompt: fixes from the Riemann and Praether chat (26 Nov)

Written 26 Nov 2026 at the end of the chat that logged edits 229 and 230, at CT's request ("put a continuation prompt
for all of this ... Make sure you also upload all of this to GitHub"). Paste the section below into the chat that picks
it up.

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

1. **Lou's secrecy is said three times in a row.** Grace in Chapter 17 ("keep it between the three of us"), Lou at the
   barn (same words), and the Chapter 18 opening ("Good. Keep it that way."). Cut the Chapter 18 instance, and probably
   Grace's "three of us."
2. **"Good. Keep it that way."** already appears near the start of the book (about Chapter 5), so fix 1 also clears
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
