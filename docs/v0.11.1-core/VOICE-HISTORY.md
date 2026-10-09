# How your book got from April 2024 to v0.11.0

*A historian's report for CT. Quotes from v0.11.0 carry their block IDs and are verbatim. Quotes from earlier drafts are labeled by draft. "Your author voice" means the first-person narrator; Elijah and the narration around him are fiction.*

## The short version

Your April 2024 draft was a funny, scared, profane, 2,000-word pep talk that told the reader the game was lost and promised to teach survival. v0.11.0 is a 102,000-word argument that the game is rigged, not lost, and that the rules can be changed, starting with dinner. The thesis got better. The evidence got much better. The structure got heavier, and your voice now arrives in bursts, surrounded by a careful, hedging, slogan-making second voice that is not yours. The good news for the cut: your bursts are easy to find, and they are the strongest blocks in the book.

## The path, in seven steps

1. **April 2024, Drive.** Your intro and two chapters. Jokes, fear, profanity, "it's already over."
2. **May to August 2024, Drive (v.00, v.01, Workbook).** Your intro survives, then chatbot material takes over: the Miller family "Black Mirror Moments," a Roko's Basilisk epilogue, "Netflix and AI: A Love Story." Chatbot replies were left in the text, for example: "Got it, let's get this right. Here’s Chapter 8 with your style, raw and real:" (v.01). The earliest place I found the title "Welcome to the Weirdness" is an outline inside a chatbot-written "Book Review and Development Plan" pasted into v.00; the Workbook's contents page uses it too. AI drafting in your style is older than the repo.
3. **May to June 2026, Draft 5, "A Manual for the Cracks."** The darkest turn: shipping-container exits, "You are experiencing a **thermodynamic deficit**," "quietly allow yourself to be metabolically liquidated." It reads machine-drafted.
4. **July 2026, repo v0.0.1.** The Premortem renames "Sovereign" to "Autonomy." Your June 2026 "Page 1" Introduction is preserved verbatim, and it is pure you: "Maybe I am an asshole." Chapter 1 is a research report. The Conclusion: "Wake the fuck up." and "The singularity is here. Survive it if you can."
5. **September 2026, v0.8.0, the "food-first developmental edit."** The heaviest hedging in the record. Your first line was softened to "So the robots are coming for the jobs. Congratulations, apparently."
6. **September 23 to 24, v0.9.1 and v0.9.2.** Your rulings restore the first line, the horse and Einstein, and add "We don't have to live like this," money as optional, and Chapter 19.
7. **October 2026, v0.11.0.** Ownership, participation, solarpunk. Your dictated "Get involved" passage goes in, turned down.

## Your original voice

- **Comic catastrophe.** You opened on a joke about losing: nanobots, a brain in a jar, a sim in an alien game. "You're just a disembodied brain in a jar."
- **Profanity as punctuation.** "What the fuck is going on?" opens Chapter 1.
- **Confession.** "These are the questions that keep me up at night, and I suspect I'm not alone."
- **Teasing warmth that undercuts itself.** "Kidding. Mostly." "Go ahead and grab your favorite drink and your favorite tinfoil hat, and let's dive in."
- **Homemade images.** "What if the shovel dug its own hoe?" "Every person on this spinning rock gets their own Einstein."
- **Pop shorthand.** Frankenstein, the Golem, the Terminator, the Matrix. "If humanity could get its collective head out of its collective ass, we could be living in the Star Trek future or the Jetsons."
- **Wonder.** "So let's dig in, let's get uncomfortable, let’s get excited, because this is the single most exhilarating time to be alive in the history of humanity."
- **Speed.** You reached "What is the Singularity?" in about 1,500 words.

One honest caveat about the anchor itself: the April 2024 Chapter 1 also has "we'll delve deeper" and two uses of "brave new world," which read like 2024 chatbot prose. I can't tell from the record; you would know. The lines no model would have written are the jokes, the swearing, the hoe, and the jar.

## What survived

- Your first line, word for word: "So the robots have taken over. Congratulations! You've lost." (sts.preface.b0039, your author voice). But the Introduction now runs before the Preface in `book.json`, so the line lands about 3,800 words in, not on page one.
- "Right now, doesn't it seem like everything is getting a lot weirder, a lot faster?" (sts.preface.b0053) and the hundred years that are "pretty much the same" (sts.preface.b0043).
- The horse parable, grown from a 2024 one-liner and the Workbook's "wild mustangs" into "But nobody owns a Mustang." (sts.preface.b0072).
- The Einstein image, now flagged as yours: "Here's how I first pictured it, years before I had the words." (sts.chapter1.b0173).
- The shovel, with the typo fixed: "The shovel never dug its own hole." (sts.introduction.b0138).
- The deep breath: "So take a deep breath. And let's get to work." (sts.preface.b0057).
- "Needs met." In 2024, "the way you get your needs met is changing." Now: "What the fuck is the point of having a society at all if it doesn't meet the needs of the people who live in it?" (sts.introduction.b0148).
- Your 2024 loneliness, handed to Elijah: "*Am I crazy? Is nobody else seeing this?*" (sts.chapter0.b0019, narration of Elijah's thought).

## What was lost

- **The comic opening.** The jar and the alien sim are gone; the simulation idea became a sourced trilemma in Chapter 4. A joke became a literature review.
- **The frightened narrator.** No "What the fuck is going on?", no "keep me up at night." The 2026 narrator is vindicated and angry, never scared. Your fear now belongs to Elijah.
- **Pop on-ramps for newcomers.** Frankenstein and the Jetsons gave a total beginner a handhold. Turing, Ulam and I. J. Good are better history and a steeper climb.
- **Teasing warmth.** The voice guide retired "Buckle up, buttercup" as blog-era. It was yours first; the chatbot drafts overused it, and the line went out with the pastiche.
- **Wonder.** In v0.11.0 the "most incredible thing I have ever seen in my life" is Elijah's (sts.chapter0.b0041), and that enthusiasm costs three people their jobs. The book turned your 2024 excitement into its hero's original sin. That is powerful, but the author voice is almost never thrilled anymore.
- **Your sharpest 2024 political line:** "Unfortunately, in those stories there is always a period where Capitalism fights to the last breath and takes a lot of people with it."
- **June 2026 lines** that fell out of your Page 1: "I've lost relationships over this." "Maybe I am an asshole." "If that sends a shiver down your spine, good. It should."
- **Speed.** Front matter is now 9,320 words before Chapter 1 begins.

## What was gained

- **A first commitment you can test.** Food first is a design brief, not a mood: "If these things are going to take all our jobs, why not make them grow our fucking food first?" (sts.introduction.b0050).
- **Receipts for the anger.** The UN on food supply, California's sheriff lockout (sts.introduction.b0162), Oxfam. The 2024 draft asserted; v0.11.0 proves.
- **Errors fixed.** v0.0.1 called the Transformer "the literal automation of thought processing" and said it gave the model "the ability to process its own structure." v0.11.0 gets it right: "Parallel training and sequential generation are different jobs." (sts.chapter1.b0147).
- **A forecast you can be graded on,** with your joke intact: "Why that day? Because." (sts.chapter1.b0111).
- **Elijah.** The 2024 Millers were chatbot filler. Elijah dramatizes your fear and isolation better than your exposition did, and the "Congratulations" bookend closes the loop your first line opened.
- **The Precedent Ledger.** Real history instead of movie references. P-03, the Wright brothers' wind tunnel, is excellent.
- **Respect for the scared reader:** "A comparison with a dead person doesn't pay a living person's electric bill." (sts.introduction.b0087).
- **Agency.** 2024: "There is nothing you can do as an individual to stop it or change its course." 2026: "Take fucking action." (sts.chapter19.b0105).

## How the thesis moved

In 2024 your thesis was surrender plus survival: "Before you resign yourself to your new overlords, pause for a moment, breathe, and know it’s already over." But the seed of v0.11.0 was already there, as an aside you put in the reader's mouth and then agreed with: "Sure,” you might say, “and we could create a utopia right now with our existing resources if we could get our shit together." Two years later that aside became the spine: "We don't have to live like this." (sts.introduction.b0127).

The middle years wandered. The 2024 chatbot drafts were a generic tour of jobs, health and dating, and were even friendly to billionaires. Draft 5 was a bunker manual. July 2026 still ended on "Survive it if you can." The food seed shows up in v0.0.1's Chapter 6: "We simply need to use robots to grow the food and build the houses."

v0.11.0 reconciles the two theses in one block, your answer in Chapter 6: "So is it a done deal? My answer, for the record, is yes." and then "what happens next, isn't done at all." (sts.chapter6.b0113). The titles moved with it: Chapter 6 went from "The Singularity Is a Done Deal" to "Is the Singularity a Done Deal?", and the Conclusion from "The 2027 Tipping Point" to "What If It All Goes Right?" Two inversions are worth seeing. In 2024 the reader had lost; now "What you've lost is the old deal" (sts.preface.b0069). In 2024 the machines wake up; now the reader does: "So wake up. All the way up." (sts.conclusion.b0079). You even gave your old thesis to Elijah, "I think it's already over," (sts.chapter1.b0010), so the book could argue with it.

## Where AI-era drafting shifted the voice

These patterns are not yours, or not at this density. None is fatal alone; together they are why the book reads as two authors.

1. **Your heat, turned down on entry.** You dictated "Take fucking ACTION." and "DO. SOMETHING." The book prints "Take fucking action." (sts.chapter19.b0105), then four paragraphs of meeting procedure. Your "Write a fucking book." became "Write a book." (sts.chapter19.b0104).
2. **The raw line plus a compliance sentence.** "actual fucking labor" (sts.chapter12.b0136) is followed at once by "With their agreement, help close one gap." (sts.chapter12.b0137).
3. **Paraphrase inside your own passages.** Your July Tiffany draft had a robot that "can fold your underwear." Now: "She's teaching herself the pieces of the kind of machine that might someday fold your laundry and grab you a beer" (sts.chapter5.b0150).
4. **The "isn't X. It's Y." pivot,** about thirty times. You used it in 2024 too; the problem is the count. "That question isn't a complaint. It's a design brief." (sts.introduction.b0110); "Autonomy isn't an idea. It's calluses." (sts.chapter17.b0169); "True autonomy isn't individual. It's relational." (sts.chapter8.b0272).
5. **The "X, not Y" disclaimer bolted onto facts:** "That's one insider's argument, not a measurement." (sts.chapter1.b0155); "It's a lab result, not a product." (sts.chapter1.b0152).
6. **Stacked pre-emptive negations:** "Not flawlessly. Not without arguments, broken machines, bad decisions, or people who try to keep the best parts for themselves." (sts.introduction.b0095).
7. **Policy-memo abstraction,** worst in the Conclusion: "Ask about time returned, danger avoided, access secured, and power over the service." (sts.conclusion.b0100); "We can insist that commitments be funded and decisions challengeable." (sts.conclusion.b0102).
8. **The slogan machine:** "Hope gets useful when we give it a job." (sts.conclusion.b0134); "A speech starts a conversation; the follow-up keeps the request alive." (sts.chapter19.b0108).
9. **Announced honesty and stage directions:** "Now the honest part." (sts.chapter3.b0088); "Sit with that." (sts.preface.b0064); "The Ledger closes with a receipt. Frame it." (sts.conclusion.b0120).
10. **"Quietly,"** in more than 20 blocks, including the book's own definition: "every institution quietly built on its scarcity" (sts.chapter1.b0138).
11. **Scenes that explain themselves,** which your own voice guide forbids: "There was no forecast in it this time. Just relief at the ordinary, unfinished work waiting for him at home." (sts.conclusion.b0085, narration).
12. **Template fatigue.** Twenty-four identical mechanism, rule and practice blocks, and near-duplicate journaling chores: "Start a timeline file." (sts.chapter1.b0126), "Keep a demonstration log." (sts.chapter0.b0096), "Start your own receipts file today." (sts.conclusion.b0080). They are the 2024 Workbook's journal prompts, reborn.

To be fair: the second voice also wrote some of the book's best lines, and some of what it softened needed softening. Your v0.6.0 ox claim, that husbandry was labor "handed to something that ran on its own," was wrong, and the fix is right.

## Blocks closest to you (protect these in the cut)

- **Preface:** sts.preface.b0039, b0040, b0041, b0043, b0053, b0054, b0046, b0071, b0072, b0073, b0057.
- **Introduction:** sts.introduction.b0081, b0082, b0083, b0086 (your Page 1); b0136 (your two worries); b0050; b0094; b0124, b0125, b0138 (your v0.5.1 material); b0127, b0147, b0148, b0149 (your September ruling); b0109 and b0118 (renting your survival).
- **Chapters:** sts.chapter1.b0111 and b0173; sts.chapter6.b0113; sts.chapter5.b0148 to b0153 (Tiffany); sts.chapter12.b0134 to b0136 and b0161; sts.chapter13.b0164 ("What the fuck is a shouse?").
- **Chapter 19:** sts.chapter19.b0096, b0097, b0098, b0100, b0105. "I'm so fucking pissed off about this. Not at you. At the arrangement." (b0096) is the rawest author voice in the book.
- **Conclusion:** sts.conclusion.b0078 and b0079. These come from source documents you supplied in July 2026, and they sound like you.

## Bottom line

The book changed for the better in what it argues and how it proves it, and for the worse in how it sounds. Your 2024 voice survives as an outline (the first line, the horse, Einstein, the shovel), and your 2026 voice survives as loud, sourced, angry bursts. Between them sits a careful second voice that hedges, summarizes and coins slogans. Keep your bursts and the Elijah spine, cut the second voice hardest, and v0.12 will have room for the scared, funny guy from April 2024.


---

## Verification notes (added when this report was filed)

- **The anchor text is real and dated.** `original-first-draft-2024-04-11.md` in this folder is copied verbatim from your Google Drive doc "Surviving the Singularity - First Draft" (created 2024-04-11, last edited 2024-04-23). It is the earliest time-stamped version found. A Drive search for 2023 material turned up code and game lore, not the book.
- **The chatbot replies in v.01 check out.** Drive's full-text search for "with your style, raw and real" returns "Surviving the Singularity - First Draft -v.01" (created 2024-07-31).
- **Not read:** two February 2026 Drive drafts, "StS Draft 2.5" and "StS Draft 3". They sit between the 2024 drafts and the June 2026 Draft 5 and are worth a look if you want the full path.
- **Your voice in the cut.** The report names 48 blocks as closest to you. The core cut kept 39 of them and cut 9. These are your call in v0.12:

| Block | Words | Why the cutter dropped it | Opens with |
|---|---:|---|---|
| `sts.introduction.b0094` | 137 | Said to duplicate b0147's "optional" line | "Which is why \"it's all over\" and \"we're so back\" are the same facts read by two different kinds of people. The tools don't decide which one comes true. People do." |
| `sts.introduction.b0124` | 167 | Sneers at the artists Chapter 0 grieves for | "Go into any comment section and you'll find the chorus: AI slop this, AI slop that." |
| `sts.introduction.b0125` | 9 | Pull quote for the cut riff | "The wise ones are learning how to solder." |
| `sts.introduction.b0136` | 31 | Promises two worries the section never develops | "And I'm not worried about the machines. I'm worried about two very specific things..." |
| `sts.chapter19.b0097` | 68 | Repeats Introduction b0162 and b0149 | "Greed is a sickness, and too many of the decisions that shape our lives serve private property first..." |
| `sts.chapter5.b0150` | 105 | Scolds Grandpa; its setup was cut | "So: Grandpa. I'm sorry Tiffany wasn't around when they put a man on the moon." |
| `sts.chapter1.b0148` | 52 | Parameter counts and benchmarks | "The foundational model was small by today's standards..." |
| `sts.preface.b0054` | 6 | Filler between two kept lines | "And that's why you're reading this." |
| `sts.chapter1.b0134` | 10 | Caption that gives away Devendra's arc | "Devendra. Senior and calm. Wrong about the thing that mattered." |

The one to look at first is `b0094`: "The tools don't decide which one comes true. People do." is one of the lines that best states your moral.
