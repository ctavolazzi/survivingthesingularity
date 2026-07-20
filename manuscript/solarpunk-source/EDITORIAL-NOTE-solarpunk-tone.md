# Editorial note: the techno-optimist / solarpunk register

Prepared for CT, 2026-07-19, against book v0.5.2. This is a findings document, not
an edit. Everything below is a judgment call (voice/structure), so per the auditor
brief nothing in the book source was touched. It exists to let you rule before any
rewriting happens.

## 1. The four videos (transcripts saved alongside this file)

| # | Title / channel | What it actually is | Why it matters to us |
|---|---|---|---|
| 01 | *I 3D Printed a Photobioreactor* / SECTOR 07 | One engineer builds an open-source algae reactor to close the loop on a home aquaponic system: grow the algae, make the fish food, stop buying inputs. Bambu A1 printer, Raspberry Pi 5 + two Arduino Nanos, a hand-built pH-automation module, a Secchi-disk light sensor hack. | This is the book's whole thesis rendered as a person in a garage. Cheap tools, local AI-adjacent automation, a closed loop toward self-reliance. The framing device is literally a far-future archivist *reconstructing* our era's artifacts. |
| 02 | *Mad scientist's homestead is parking size* / Kirsten Dirksen | The "EasyGrow" guy: recirculating vertical hydroponic towers (patented quad-pots), self-built tri-helix wind turbines with axial-flux "pancake" alternators he winds himself, rural-internet antennas. His systems feed a stadium (Amalie Arena), lettuce stores in Nigeria, off-grid gardens in Argentina. | The counter-figure to the book's "lone household with a generator and a rifle." One man, a garage, a patent, feeding cities, and explicitly *not in it to get rich*: "I'm in business to grow food and help people grow food." Solarpunk that already exists. |
| 03 | *Build an Automated Hydroponic System* / Kyle Gabriel | Full DIY build using Mycodo (open-source), Raspberry Pi, PID + conditional controllers with user Python, a cultured biocontrol agent. The whole thing is a give-away schematic. | The "Tools of the Trade" chapter made concrete: the software is free, the parts are cheap, the knowledge is published. |
| 04 | *SANANBIO Uplift* / SANANBIO (1:34 promo) | Corporate fully-automated vertical farm: "reduces labor costs," "decreases human touch," "feed the world better." | The industrial mirror-image. Same technology, opposite spirit: it removes people. Useful only as contrast, to sharpen what the DIY builders are choosing instead. |

## 2. What solarpunk is, and why the book is missing it

Solarpunk (per the movement's manifesto and common definition): "solar" = renewable
energy plus an optimistic future that rejects doomerism; "punk" = DIY, decentralized,
post-scarcity-minded counterculture. Core tenets that map cleanly onto this book:

- Decentralization of energy and food (communities running their own grids and gardens
  instead of depending on distant corporations). This is the Neighborhood Factory and
  the Shouse Protocol already.
- Handcraft and local making *alongside* high technology. This is "learning to solder."
- Sustainability accessible to everyone, not a luxury good.
- Beauty and joy as intrinsic to the project, not decoration.

That last one is the gap. Right now the book's emotional palette is: machine God,
collapse, stampede, cyber war, shredded social contract, the psychology of panic. It
is a *survival* book and it earns its darkness. But there is almost no register in
which building the new thing is a **joy** rather than a fallback from catastrophe. The
SECTOR 07 and EasyGrow builders are having the time of their lives. Dirksen calls it a
hobby he refuses to let become a job. That felt-sense of delight is the techno-optimism
you asked for, and it is exactly what makes readers lean in instead of brace.

The book already has the intellectual optimism ("you don't have to take anyone's wealth
to end the terror; use the robots to grow food"). What it lacks is the *shown, joyful*
version. Marta's shop is close, but it's framed as grim competence under threat, not as
something a reader would envy.

## 3. Where to fold it in (proposal, pending your ruling)

Strongest, lowest-risk placements:

1. **Chapter 15 (Reclaiming Soil) or Chapter 17 (Tools of the Trade): a real builder
   vignette.** A short, sourced sidebar or opener on the photobioreactor build: a guy
   who wanted his aquaponic loop to stop needing store-bought fish food, so he printed
   a lab instrument on a $400 machine. It is the "create over consume" protocol with a
   face. SECTOR 07's honesty ("the design remains incomplete... not recommended for
   direct replication") is a feature: it models the iterate-in-public ethic without
   overclaiming, which fits the book's credibility standard.

2. **Chapter 11 (Neighborhood Factory) or Chapter 9: EasyGrow as the anti-bunker.**
   Dirksen is the living rebuttal to Ch. 7's "readiness that ends at your property line
   has a shelf life measured in weeks." He built the tech *to give away*, feeds a
   stadium off it, and turned down the scale-and-extract path on purpose. Use him where
   the book argues cooperation beats fortification.

3. **A named counter-image: DIY loop vs. SANANBIO.** Same vertical-farming technology,
   two spirits. SANANBIO's own words ("decreases of human touch," "reduces labor costs")
   are the enclosure the book warns about; the DIY builders are the pivot. One clean
   paragraph contrasting them would do real work in Part II.

4. **Tone-level, everywhere: add a "builder's delight" beat.** Not a new chapter, a
   recurring note. When the book describes the new economy, let at least some of it read
   like the algae guy at 3 a.m. happy, not just like Elijah at 3 a.m. doom-scrolling.
   That is the single biggest lever on the "intrigued, not punished" feeling.

None of this requires softening the confrontational spine. It adds a second color.

## 4. Tone audit: where the book currently punishes the reader

The important distinction, and I think it's the one you're circling: the book is
abrasive in two very different directions, and only one of them costs you readers.

**Abrasive at external targets (keep it, it's the voice):**
- Ch. 8 bullet: "Your phone is not a tool. It is a harvesting machine, and the crop is
  your executive function." Sharp, true, aimed at the system. Keep.
- The Precedent Ledger's forager/hand-scribe/stage-play riff on AI-slop egos. Aimed at
  a posture, not the reader. Keep.
- Marta calling Elijah "college." In-scene, earned. Keep.

**Abrasive at the reader (this is what makes people defensive):**

| Loc | Passage | Problem |
|---|---|---|
| 02-introduction.md:24 | "If you're still skimming headlines and parroting the popular opinion you saw on a Reddit thread, you're not looking at the data. You're looking at the noise." | Opens by telling the reader they're a parrot. A reader who *was* skimming now feels caught and defensive on page one, before any trust is built. The instruction "get your goddamn hands on it" is great; the insult in front of it undercuts it. |
| 02-introduction.md:28 | "stop looking for a safe space and start looking at the reality" | "Safe space" is a culture-war tripwire that sorts readers into camps and costs you half of them for no argumentative gain. The point (stop seeking comfort, look at reality) survives without the loaded phrase. |
| 06-chapter4.md:60 | "you have to look back and laugh at the sheer, pathetic absurdity of the people in Stage 2... The executives banging their fists..." | Invites the reader to sneer. Contempt is the emotion that reads as condescension even when it's aimed elsewhere, because the reader recognizes themselves in "the people." |
| 06-chapter4.md:62 | "That is the scale of human arrogance. We thought we could put a leash on infinity." | "We" briefly includes the reader in the mocked group. A small reframe (awe at the scale rather than contempt for the leash-holders) keeps the grandeur, drops the sneer. |

The pattern: confrontation *with* the reader ("here is the hard thing, come look at it
with me") intrigues; confrontation *at* the reader ("you've been a fool") punishes. The
four flagged spots are the at-the-reader kind. The fix in each case is small: keep the
demand, remove the verdict on the reader's character. I did not make these edits; they
touch voice, so they're yours to rule on.

If you want, I can draft the four reworded passages plus one builder vignette (SECTOR 07)
as a diff for you to approve, and only then run the version ritual.

---

## 5. Refined thesis (CT ruling, 2026-07-19) and drafted prose

CT's direction, in his words, distilled to what the book has to *do*:

- The same facts read two ways: "it's so over" vs "we're so back." The tools don't
  pick which comes true; people do. Defeatism is the thing the book confronts.
- The confrontation is aimed at the **"AI slop" crowd and the doomers**, not the anxious
  reader. Under the AI-slop complaint is wounded status ("I was special for knowing how
  to do this"). The moral hit is selfishness: *think about someone other than yourself.*
- The reader we are recruiting is the young person who does not want to trade their whole
  day for permission slips: asking to use the bathroom, a boss denying time off for
  shareholder value. They want tangible return on their time. These tools are the first
  chance ever to offload survival-work to a machine that does not need line-by-line
  programming.
- Core analogy: **animal husbandry / the ox.** You do not program the ox. You point it at
  the field and it walks and the field gets tilled. AI is the second time in history that
  labor can be delegated to something that runs on its own.
- The argument to make explicit: capitalism *persists.* This is not the end of the world
  and not even the end of capitalism. "It is easier to imagine the end of the world than
  the end of capitalism" (Fisher/Jameson) is precisely the reflex to break. What ends is
  capitalism being **mandatory for survival.** Not abolished. Optional. Optional is the
  whole ballgame.
- Success metric: a reader closes the book thinking *I can do that for the people I love.*

### Draft A: the ox passage (proposed home: Introduction, or Ch. 6 "Done Deal")

> Here is the thing the panic keeps you from seeing. For the entire history of our
> species, staying alive has been work you did yourself or paid someone else to do. Every
> tool we ever built still needed a human holding it. The plow does not pull itself.
>
> Then, once, we found an exception. We domesticated the animal. We put an ox in front of
> the plow and something happened that had never happened before: the work got done
> without a human doing it. You do not program an ox. You do not write it a line of
> instruction for every furrow. You point it at the field and it walks, and the field gets
> tilled, and you go spend that hour of your one life on something else. Husbandry was the
> first time labor could be handed to something that ran on its own.
>
> This is the second time. That is what the machine actually is, under all the doom. Not a
> god arriving to end us. An animal we just learned to domesticate, one that happens to
> think. For the first time since the ox, the work of keeping yourself alive can be given
> to something that does not need you standing over it.
>
> Which is why "it's all over" and "we're so back" are the same facts read by two
> different kinds of people. The tools do not decide which one comes true. People do. Tell
> someone the machine can do most jobs now and watch them leap straight to the apocalypse,
> skipping clean over the far likelier outcome, which is not the end of the world and not
> even the end of capitalism. Capitalism is going to be fine. The markets will still be
> here. What ends is the part where you *have* to sell your day to a corporation to be
> allowed to eat. For the first time, that becomes optional. Not abolished. Optional. And
> optional is the whole ballgame.

### Draft B: sharpen the AI-slop confrontation (Introduction, replacing the softer
close of the Precedent Ledger's slop riff, keeping the solder pull quote)

> Strip the aesthetics off the "AI slop" complaint and look at what is underneath it: *I
> was special for knowing how to do this, and now I am not.* That is the whole objection.
> It is a person looking at a tool that could feed someone, teach someone, get a scared
> kid out of a job that treats a bathroom break as a privilege, and deciding that the
> important thing, the thing worth posting about, is their own wounded status. Think about
> someone other than yourself for once. The wise ones already are.
>
> > **The wise ones are learning how to solder.**

### Draft C: intro:24, keep the demand, drop the verdict on the reader

> The loudest voices in the room are working from a headline and a Reddit thread they
> skimmed once. That is noise, and noise is cheap. I am not asking you to trust me over
> them. I am asking you to go around all of us. Stop listening to the men in lab coats who
> have a vested interest in keeping you afraid, and stop listening to me while you are at
> it. Get your goddamn hands on it. Use it yourself. Then you will know.

### Draft D: intro:28, drop the culture-war tripwire

> ...and the first thing you need to do is stop waiting for someone to promise you it will
> be fine and start looking at the reality of what is coming.

### Draft E: the builders as proof of "we're so back" (Ch. 15 or 17 opener)

Short, sourced vignette on SECTOR 07's photobioreactor and/or Dirksen's EasyGrow, framed
not as survivalism but as the rising tide already visible: ordinary people, cheap tools,
building the exit and giving away the schematics. This is the evidence for the optimism
the rest of the book asserts. Full draft to follow once the register above is approved.

### Lower priority / author's call

- 06-chapter4.md:60-62 ("pathetic absurdity," "human arrogance") aims contempt at
  executives and politicians, not the reader. It is more on-brand than the intro spots.
  Recommend a light touch (trade sneer for tragic-hubris awe) only if you want it; not
  load-bearing for the "don't punish the reader" goal.

