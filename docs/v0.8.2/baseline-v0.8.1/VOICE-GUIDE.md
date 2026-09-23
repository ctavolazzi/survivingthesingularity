# Voice Guide: Surviving the Singularity

Written 2026-07-26 against the shipped v0.7.1 prose, not against memory of it. Every
rule below is followed by a real line from the book, so you can hear the target rather
than infer it.

**This replaced `WRITING_CHECKLIST.md`**, which was blog-era guidance (emoji headers, a
30% humor quota, "Buckle up, buttercup" transitions) predating the v0.6.x
techno-optimist turn and the v0.7.1 wake-up-call turn. Following the old checklist
literally produced the wrong book. Retired and deleted 2026-07-26 on CT's sign-off.

---

## 1. The book runs three registers, on purpose

Most of the "voice is inconsistent" problem is not inconsistency. It is three legitimate
registers that have not been given clean borders. Learn which one you are in.

### A. The Argument (Introduction, Preface, Part I and II Foundations)

First person, direct address, confessional and confrontational at once. Short declarative
hammers between long argumentative runs. Contractions always. Profanity is allowed and
rare, always as emphasis, never as decoration.

> It's time. It's finally time.

> Get your goddamn hands on it. Use it yourself. Then you'll know.

> Not abolished. Optional. And optional is the whole ballgame.

> The technology is new every time. The stampede never is.

The move that defines this register: build a long paragraph of argument, then land it on
a short sentence that could be tattooed. "The plow doesn't pull itself." Do not explain
the hammer after you swing it.

### B. The Narrative (Chapter 0 and the chapter-opening scenes)

Third person, past tense, Elijah and the co-op. Literary, patient, physical. Concrete
nouns doing the argumentative work so nobody has to state the moral. This register is
the strongest writing in the book. Do not "improve" it toward the Argument voice.

> The bead snapped clean along its own centerline. Inside, the break was bright and
> crystalline and full of small round voids, like honeycomb cast in nickel.

> "See the sparkle," she said, not a question. "Cold lap. Porosity. It sat on top of the
> steel and never became the steel."

Rule: the scene never announces its lesson. If a narrative passage ends by explaining
what it meant, cut the explanation. The vise already said it.

### C. The Field Manual (Part III, chapters 10 through 18)

Imperative, numbered, specific. Real numbers, named tools, named failure modes. The
reader is holding a wrench, not a thesis.

> Own the dirt. Build the systems. Be the one who is prepared, rather than the one who
> is surprised.

> Don't be afraid of the local building department. They are not the police. They are
> bureaucrats who want to check off boxes.

Rule: every Field Manual section owes the reader a thing to do this week, a number, or a
named part. "Consider your energy needs" is not field manual. "Two steel boxes and
roughly $25,000" is.

---

## 2. The actual defect to hunt

The editorial docs call it "Foundations swing rant to academic." Here is what that looks
like in the wild. Chapter 13 opens its Autonomous Shell section like this:

> Let us talk about shelter.
>
> And no, I do not mean a standard suburban split-level home... That is not a home; it
> is a financial cage... you are not a citizen; you are a tenant in a high-security
> penal colony.

Two things are wrong, and only one of them is obvious.

**The stiffness.** "Let us talk about" and "I do not mean" are uncontracted formal
English. The book everywhere else says "It's time," "don't," "you're," "we aren't."
The register slips into lecture exactly when it most wants to sound urgent. Fix by
contracting and cutting the throat-clearing: the section can open on "Let's talk about
shelter" or, better, on the claim itself.

**The escalation.** "High-security penal colony" is the rant end of the swing. The book
at v0.7.1 aims anger at systems and at wounded ego, never at the reader, and it earns
its heat with specifics rather than volume. Compare the Introduction, which takes the
same swing but lands it on a person's motive rather than on a metaphor:

> Strip the aesthetics off the "AI slop" complaint and look at what's underneath it:
> *I was special for knowing how to do this, and now I'm not.*

That is the calibrated version of the same energy. Diagnosis beats denunciation.

**When you find a swing, ask which of the three registers the passage should be in, then
commit to it.** Most swings are a Field Manual section that drifted into Argument, or an
Argument section that got embarrassed and retreated into academic.

---

## 3. Mechanics, non-negotiable

| Rule | Why |
|---|---|
| **No em dashes anywhere** | Swept at v0.5.0. Use a period, colon, comma, or parenthesis. |
| **Never the word "manifesto"** | Removed at v0.6.2. Only survivor is Bastani's real citation subtitle in Appendix B. |
| **Contractions on** | The uncontracted voice is the academic drift. "It's," "don't," "you're," "we aren't." |
| **Hyper-local, not decentralized** | "Decentralized" only for genuinely decentralized tech (mesh, LoRa, IPFS, distributed energy). Never as the goal. |
| **"Independent" is not an identity** | Moved to hyper-local, neighborhood, community-based at v0.7.1. Load-bearing uses stayed. |
| **Second person for the reader** | The book talks to one person, not to an audience. |
| **Profanity: sparing, load-bearing** | It appears a handful of times in 85,000 words. That is the budget. Each one should be doing work. |
| **Italics for the reframe, not for volume** | `*produce* survival instead of *renting* it` earns it. Italicized shouting does not. |
| **Pull quote syntax** | A standalone `> **Sentence.**` line. Renders bold on site and EPUB, centered amber in DELUXE, folded into prose in PLAIN. |

---

## 4. Humor

The one durable idea from the old checklist: **humor serves the point and punches up.**
Everything else in that file (quotas, stock transitions, stock closers) is retired.

There is no humor quota. The book is funny where the material is absurd and dead serious
where it is not. The Introduction's list of people refusing agriculture, the printing
press, and stage plays is the model: the joke IS the argument, compressed. A joke you
could delete without weakening the point is decoration, and decoration is what "AI slop"
actually means.

Never joke at the reader. The v0.6.x pass specifically redirected two reader-punishing
lines off the reader, and the "coward's way out" line in Chapter 18 became "fear wearing
the costume of caution." That is the standard.

---

## 5. Chapter shape

Every section from Preface through Conclusion carries these, in this order:

1. **Header image** with an italic caption line and, for photos, the license credit.
2. **Epigraph**, a real sourced quotation. Attribution on its own line.
3. **In this chapter** bullets, in Part III. Each bullet is a claim with teeth, not a topic.
4. **Narrative scene**, where the chapter has one.
5. **Foundations / body**, in the register that chapter belongs to.
6. **The Precedent block**, P-01 through P-23, in Greene register: story, then mechanism,
   then rule, then **the practice**, which is three concrete actions sized for one week.

The Precedent block is the chapter's closing move. Check that yours does not duplicate a
neighbor's closing line or its rule. Full index and operating manual are in Appendix D,
with the ID table and sources in `manuscript/HISTORY-CASEBOOK.md`.

---

## 6. The test

Read your passage out loud. Then ask:

1. **Which register is this, and did I stay in it?** If you cannot name it, that is the
   defect.
2. **Did I contract?** Uncontracted prose in an Argument or Field Manual passage is almost
   always drift.
3. **Is my anger aimed at a system, an incentive, or an ego, rather than at the reader?**
4. **Did I explain a scene that already worked?** Cut the explanation.
5. **Can the reader do something on Monday?** Mandatory in Part III, still owed elsewhere
   as a "so what."
6. **Would an acquisitions editor reading cold believe the numbers?** Every date, name,
   quote, and figure verified, or softened, or cut.

---

## 7. What this guide is not

It is not a license to rewrite the book toward one flat voice. The three registers are
the book's texture and the narrative scenes are its best asset. The job is clean borders
and calibrated heat, not homogenization.
