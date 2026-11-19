# Continuation prompt: Surviving the Singularity, the novel, 2026-11-19

Read this at the start of a fresh session. It says where the novel work stands, where every
piece is, what CT has decided, what is still his to decide, and how he wants to be worked with.

## Update, 19 November, later the same day

Read this before the rest. It is newer.

- CT asked for one thing, in his words: "create a structure and a scaffolding onto which I can
  paint." Find and fix the inconsistencies, improve the story structure, test the characters
  against their motivations, argue with the result, and present the best version. He then edits
  for style. He does not want to be asked what he wants at each step, and he does not want
  guesses presented as questions.
- That pass exists. `tools/consistency-pass/` holds it: `ops.py` (105 single-spot changes, the
  story decisions and what was turned down) and `apply.py` (rebuilds chapters 13 to 15 and
  applies everything to a copy of the Doc's text).
- The reading page has two new tabs. **Book** is the whole manuscript after the pass, with a
  bar in the margin beside anything that is not his. **Changes** is the decisions and every
  change. The Later tab is gone, its content is in the pass.
- **The pass is in the Google Doc.** CT said "write it to the Doc" on 19 November. It was
  written with `tools/consistency-pass/doc_sync.py` and checked: the Doc matches `book.json`
  paragraph for paragraph, text and italics. The Doc as it was before the pass is in its version
  history. Later story changes go in `OPS2` in `ops.py` and are sent the same way (`STAGE=2`).
- His sister is Melody (his name for her). She is his father's daughter from before, in Miami.
  Her call the night after the sale sets off the crash out. Her lines in that call are his
  dictation.
- Ten Sonnet readers went through the whole book on 19 November (CT asked for subagents on
  Sonnet 5.5, fetching information for the main session to judge). Their reports are in
  `drafts/_private/readers/` in a live session and are not in git. What was acted on is `OPS3`
  in `ops.py`: about thirty plain slips, and one story change, "the deed" (Reuben finds that the
  farm Elijah sold went to the co-op's enemy; chapters 23, 25, 29, 31). Not acted on, because
  they are CT's: the letter Elijah signs half read in chapter 8, the leaked journal's three
  crawlers, the welder for the gap, and why he says no to Gus.
- The work now is the story structure. He asks a plain question about the story ("why didn't he
  keep some money?"), the answer shows a weak joint, and it gets fixed in the Doc. Do not hand
  him lists of fixes. Tell him the story.
- To rebuild: read the Doc with the Docs connector, turn it into one paragraph per line with
  italics marked `[[i]]...[[/i]]`, run `apply.py`, then build the page. The working copies go in
  `drafts/_private/`, which git ignores.
- `drafts/draft-later-chapters-36-37-39.md` is superseded by the pass in three places: the lamp
  line is now inside the fire, David says seven months, and Elijah sleeps at Manny's.

## The job

CT is finishing his novel, "Surviving the Singularity." The protagonist is Elijah Madrone. The
book is chapters 0 to 39 in four acts, plus an afterword.

His schedule, from his own manuscript Doc:

| Date | What |
|---|---|
| Sunday 22 November | New writing done |
| 23 and 24 November | Read-through |
| 25 November | Build |
| Thursday 26 November 2026 | Publish |

## Where everything is

**Branch.** All of this work is on `claude/elijah-van-farm-arc-ur5d5p`. It is pushed and not
merged. Merging to `main` deploys the live site, so do not merge without CT saying so. No pull
request is open. CT does not want pull requests opened or watched unless he asks.

First step in a new session:

```bash
git fetch origin claude/elijah-van-farm-arc-ur5d5p
git log --oneline -12 FETCH_HEAD
```

Then bring that work onto whatever branch the new session is told to use.

**The manuscript itself is not in this repo.** This repository is public. The live text is CT's
Google Doc, "FINAL StS Manuscript." Its story text is the same as the PDF he attached on 18
November. The top of the Doc holds his TO DO, his Story plan, his story direction and final
conflict "in your words," and his character pages. Nothing in the Doc has been edited by
Claude. Read it through the Google Drive connector, read-only, and do not write to it unless he
says to. The chat prompt CT pastes has the Doc's id.

**The notes, all in `manuscript/`:**

| File | What it is |
|---|---|
| `drafts/draft-elijah-crash-out-arc.md` | The scene draft, fifth version. New prose for chapters 13, 14 and 15: his mother's stroke, the barn, the choice, his followers turning on him, the sale, the crash out, five weeks in the truck, the road north. Also what each later chapter must change, and a list of everything Claude invented. |
| `NOVEL-BEATS-2026-11-19.md` | Starts with "Decided, 19 November": CT's rulings and the lines that go with them. Below that, the seventeen original beats, each marked if replaced or cut. |
| `NOVEL-MAP-EVERYONE-2026-11-19.md` | The big map in words: 25 people, each with what they want, try, are stopped by, do about it, end as, and whether they get it. |
| `NOVEL-MAP-ELIJAH-2026-11-19.md` | Elijah's map in words: seven attempts and where he ends. |
| `NOVEL-STRUCTURE-2026-11-19.md` | Rising and falling action by chapter, obstacles, doors, choices, core motivations, five small fixes. |
| `NOVEL-DRIVE-FINDINGS-2026-11-19.md` | What a read-only search of his Drive found: his plan, his schedule, where Claude's work conflicted with his decisions, thirteen proposed Want, Flaw and Arc pages, new material by where it goes, and what was not searched. |
| `NOVEL-CHARACTER-PROFILES-2026-11-18.md` | Profiles of the whole cast, written in the show-don't-tell manner of his older story "The Golden Plates." |
| `NOVEL-CHARACTER-ARCS-2026-11-18.md` | Each arc: finished, missing steps, stopped, or flat and needing one beat. |
| `NOVEL-CONSISTENCY-AUDIT-2026-11-18.md` | 27 line fixes, a short list of decisions, and what was checked and found fine. |
| `tools/reading-page/` | The scripts that turn the files above into the reading page. Its `README.md` says how to build, check and publish. |

**The reading page.** A private page on claude.ai titled "Singularity Cast Bible." CT reads the
work there, mostly on a phone. Tabs: People, Map, Drive, Scene, Beats, Shape, Rhymes, Arcs,
Fixes, Method. It is built from the Markdown above, so change the Markdown and rebuild. To
update the same page from a new session, read it with the Artifact tool first, then publish to
its URL. The chat prompt has the URL.

## How CT wants to be worked with

His own instructions load on their own in a new session. These are the ones this work kept
running into:

- Answer first, in a line or two. Then stop.
- Do exactly what he asks. Use his words. Never fill a gap with an assumption. If something is
  missing, ask one short question.
- "Let's figure out" and "think about" mean plan with him. "Do it" means do it.
- No em dashes or en dashes, anywhere.
- He reads on a phone. Long output in chat does not work. Put it on the reading page and point
  to the tab.
- What he says in the chat beats any file, including this one. The latest thing he said wins.
- Think for yourself and critique your own idea before showing it. On 19 November he said the
  gap-fills were "a little predictable" and "a little formulaic." What went wrong, so it is not
  repeated: every thread got tied, everyone was kind, Elijah was always in the right, the props
  were stock, and the text told the reader what was coming.
- He agreed the book does not need twists. In his words it is "a story of character
  development" and of "the solarpunk farm."

## What CT has decided

Latest first. The exact words are quoted in the scene draft and at the top of the beats file.

**19 November, after the pushback**

- The barn full of supplies stays, but his mother did not believe him. She was humoring him,
  and she was slipping.
- She has a massive stroke. She ate a little tub of Ben and Jerry's every day and was not
  healthy.
- After the stroke she has one word: "Barry." Elijah does not know who Barry is. He was her
  first love.
- At the fire, Elijah strikes first without knowing it. He is only pointing something out.
  Grace defends herself from an attack that is not happening. They talk past each other. It
  stays in the subtext.
- Grace says: "And now you're taking out your mother trauma on me!" She growls and shakes her
  hands up by her chin. Elijah is speechless. His heart sinks. The woman he trusted most, and
  in one instant the trust is shattered.
- Ray, David's father, was the one sitting with her.
- The guitar is gone for good.
- He asks his followers for help and is mocked. Hate in the comments, hateful messages from old
  friends, and at the same time incredible offers. It overwhelms him and he steps away. He
  makes many videos about what is happening to him, and it escalates past what he can hold.
- The voicemail, "Tom," the milk and the glasses may have a place. They are still in the draft.
- His mother is nice, kind, funny, sweet and charming, and also a perfectionist and a
  catastrophizer.
- **What the book is about:** "Surviving the singularity involves surviving yourself." It is
  not about getting ahead of the technology, and not about control or self-discipline, which
  are traps Elijah may be tempted by. It is about feeling your body and your feelings, being
  present, and accepting that you were never in control. "You don't control when you get
  hungry. You don't control when you have to pee."

**19 November, earlier**

- No mother's couch. She does not die. She goes into a care facility, and Elijah makes an
  impossible choice: he sells the house to pay for her care.
- She had been forgetting things and was still very sweet. She was behind on the mortgage and
  told nobody. "We're not even sure if she knew it herself."
- He has no siblings and no next of kin. His father died ten years ago.

**18 November**

- The crash out in his vehicle: "I hate this" three times, "I wish I was never born," yelling
  at God, then no answer, only rain. He cries himself to sleep.
- A time jump of weeks, not months. Gig work, job applications, the money and food running
  out, the food bank, the homeless man.
- A friend invites him to the farm. He is not rescued. He has nothing to lose and spends his
  last dollars on gas. The farm people nurse him back.

**From his own plan in the Doc**

- The enemy is Aaron Bidwell, who never really meets them and pulls strings without the others
  ever knowing.
- Four factions: Naturalists, Accelerationists, We'll-Sees, Salt of the Earth.
- The novel ends on Thanksgiving 2027.
- The core conflict is the right to choose for yourself.
- Elijah goes from prophet to a man who can sit at a bar.
- Grace's speech at the fire ("Millions of people die every single day") is his own dictation.
  Do not rewrite it.

## What Claude invented and CT has not confirmed

Two lists hold all of it:

- "What I invented, for you to check," at the end of the scene draft.
- "What I filled in, for you to check," in the Decided section of the beats file.

The larger ones: that what Elijah points out at the fire is the gate; that David reveals Barry
in chapter 39, with Barry's last name, school and car; everything inside the barn; which old
friends write to him; that it was a clot; that he keeps none of the sale money; the trust that
lets him sign.

## What is open

1. **Nothing is in the Google Doc.** CT has not said whether Claude should write into the Doc
   or hand him finished text to paste. Asked, not answered.
2. **Later chapters have to change to match the stroke.** Chapters 18, 22, 23, 24, 31, 32, 36,
   37 and 39. The table is in the scene draft under "What this changes later in the book."
3. **Short pieces not written yet:** how Grace and Elijah become a couple; "You're the lamp"
   coming back; Grace asking out loud for the truck; the three weeks after he arrives; a line
   in each of chapters 7 to 10 of him filming as he goes; the ice cream once, early.
4. **The 27 line fixes** in the audit. None applied.
5. **Thirteen proposed Want, Flaw and Arc pages** in the Drive findings. No ruling yet.
6. **Beat 5** in the beats file, the two other ways to pay for her room. Keep it or let the
   followers scene do that work alone.
7. **Not searched:** the Doc's version history before 16 November; eighteen suggestions in an
   older version of the Doc; about ten personal documents and one audio file; Gmail; Notion.
8. **His dictations.** He said he has dictated material for years. It was not found in Drive.
   Asked where it lives, not answered.

## Mistakes already corrected

So they are not made again:

- Proposed that Bidwell be named to the co-op. Withdrawn. His plan says they never know.
- Proposed rewriting Grace's speech at the fire. Withdrawn. It is his dictation.
- The man with the arms in chapter 34 is Gus.
- Marta's shaking cup in chapter 29 is deliberate.
- Elijah is thirty-six. The co-op is three hours north.
- Denny's silence at the arms meeting is not a hole. Turning the glass is his speech.

## Privacy

- **This repository is public.** That is why the manuscript text is not in it.
- His personal journal material was found in Drive and kept out of every file here. If he asks
  for it, give it to him in chat only.
- One Drive document covers a subject he said he does not want to tell in this book. It was
  left alone.
- His social media export holds other people's private messages. It was left alone. Open it
  only if he says to.
- Drive is read-only. Never create, edit, move, share or delete there.
- His email address and personal details never go into requests to outside services.

## What comes next

Wait for CT to say. If he does not, the nearest work is item 2 above: rewriting the later
chapters so they match the stroke, starting with 36, 37 and 39, where his rulings land hardest.
