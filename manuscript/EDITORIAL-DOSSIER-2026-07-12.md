# Editorial Dossier — Surviving the Singularity

**Pass:** Ruthless acquisitions-editor read of the full v5.4 manuscript (all 24 content files), 2026-07-12.
**Rule of engagement:** Diagnosis only. Nothing was fixed except one author-approved phrase
(`02-introduction.md:13` — "like I'd finally cracked" → "like I'd finally lost it", killing the
crackpot/cracked redundancy).
**Companion docs:** `EDITORIAL-QUEUE.md` (work tracking), `src/lib/data/book/ELIJAH-PROTOCOL.md` (design law).

---

## How to use this dossier

Work one chapter at a time, in book order. For each chapter: open the source file and its dossier
section side by side, read the chapter, then read the findings, and mark each finding
**accept / reject / modify** in the margin. Every finding cites `file:line` against the current
source in `src/lib/data/book/`. The systemic findings (S1–S9) apply everywhere; the chapter notes
only repeat them where a specific instance needs a line number.

Severity key:

- 🔴 **Structural** — would block publication; a reviewer or reader will hit it and lose trust.
- 🟠 **Chapter-level** — makes the chapter read unfinished or self-contradictory.
- 🟡 **Line-level** — polish; fix in a sweep.

---

## The verdict

If this landed on my desk as an acquisitions editor, here's the letter:

The premise is sellable and the spine is real: nine stages, a psychology of collapse, and a
build-your-way-out program is a genuinely distinct package in the AI-books shelf, which is
currently split between breathless boosterism and doom lit. Chapter 0 is the best thing in the
manuscript — a cold open that earns its dread through specificity — and the new narrative scenes
in Chapters 1–3 hold that standard. The manual chapters (13's container build, 11's Crucible,
17's toolbench) are the second-best thing: concrete, numerate, confident.

The problem is the middle. **This currently reads as three books stitched together** — a hot
first-person manifesto, a clinical third-person research synthesis, and a calm second-person
survival manual — and the stitching is visible on almost every seam: chapters that announce
themselves as "this final chapter" (Ch. 8), a six-step program that now runs in the order
1, 6, 2, 3, 4, 5 because the chapters were reshuffled around it, ten chapters that end by promising
a "next chapter" that no longer exists at that number, ~450 words that appear verbatim twice, and
a table of contents that currently contains the line "Ensure system packages are up to date."

None of this is fatal. All of it is mechanical. But it must be fixed before anyone outside this
repo reads the book, because each seam breaks the reader's trust in exactly the way this book
cannot afford — the author's authority *is* the product.

The deeper editorial question is voice, and the author has already diagnosed it: the original
register — "So the robots have taken over! Congratulations, you've lost." — was softened for
market, and the softening shows. The hot voice survives in patches (the Stage chapters, the
Chapter 5 opener, the Conclusion) and those patches are the best-written manifesto material in
the book. The softened material (Preface bullets, Ch. 6 "The Premise", Ch. 18 "Synthesis") reads
like a landing page or a grant abstract. **Recommendation: commit to the hot register for
Zones 1 and 3 manifesto material, keep the manual register for the builds, and let the narrative
scenes stay gritty — three voices by design, not by accident.** The market-softened fourth voice
should be eliminated entirely.

---

## Systemic findings (book-wide)

### S1 🔴 The broken cross-reference lattice

Zone 3 material was folded in from an older draft whose chapter numbering no longer exists.
Every internal "Chapter N" pointer and every end-of-chapter cliffhanger is wrong in the current
TOC. Complete inventory:

| Where | Says | Actually is / problem |
|---|---|---|
| `10-chapter8.md:124` | "community trust (Chapter 3)... microgrid (Chapter 5)... mesh node (Chapter 2)" | CLT = Ch. 12/15; microgrid = Ch. 17; mesh = Ch. 14/17 |
| `10-chapter8.md:150` | "ESP32 LoRa chip (Chapter 5), compost pile (Chapter 3)" | Ch. 17; Ch. 9/15 |
| `10-chapter8.md:155-159` | "Land Trust (Chapter 3)... Mesh (Chapter 2 & 5)... Microgrid (Chapter 1 & 5)" | all wrong |
| `10-chapter8.md:168` | "Faraday drawer (Chapter 5)" | Ch. 17 |
| `10-chapter8.md:278` | "server's cooling fluid (from Chapter 7)" | Ch. 11 |
| `10-chapter8.md:284` | "DC bus bar we built in Chapter 6" | never built as a numbered chapter; content in Ch. 17 |
| `10-chapter8.md:497` | "Chapter 10: The Autonomy Protocol (Mesh Networks, LoRa...)" | doesn't exist; content in Ch. 14/17 |
| `11-chapter9.md:278` | "server's cooling fluid (from Chapter 7)" | Ch. 11 |
| `11-chapter9.md:287` | "we transition from Acts I and II to Act III... Chapter 9: Hacking the Deed" | said *inside* Chapter 9, pointing at a different Chapter 9; CLT content is Ch. 15 |
| `12-chapter10.md:206` | "We start with Chapter 5: The Autonomous Shell ($25,000 Exit Strategy)" | that's Ch. 13 |
| `13-chapter11.md:284` | "DC bus bar we built in Chapter 6" | Ch. 17 |
| `13-chapter11.md:290` | "next chapter... Chapter 8: The Robot in the Soil" | that content is in Ch. 9 (behind us) |
| `14-chapter12.md:168-186` | Master checklist cites Chapters 3, 10, 7, 5, 6, 8 | all old numbering |
| `15-chapter13.md:280` | "next chapter... Chapter 6: DC-Native Solar and Recycled Storage" | no such chapter; content in Ch. 17 |
| `19-chapter17.md:27` | "In Chapter 2, we discussed the... Municipal Mesh Network" | that's Ch. 14 |
| `17-chapter15.md:150` | "thermodynamic limits we discussed in Chapter 1" | that's Ch. 5 |
| `17-chapter15.md:162` | "your Chapter 2 Redirection Protocol" | that's Ch. 14 |
| `22-appendix-a.md:39-41` | "Chapter 3" (CLT), "Chapter 5" (microgrids) | Ch. 12/15; Ch. 17 |
| `10-chapter8.md:12` | "Remember the Introduction? The part where I joked that you might just be a disembodied brain in a jar... neural link electrodes" | the electrodes joke is in the **Preface** (`01-preface.md:56`), and it was never a brain-in-a-jar joke — pointer broken twice |

Also the old book's **six-step program** is still embedded across the reshuffled chapters and now
runs out of order: Step One `07-chapter5.md:131`, Step Two `16-chapter14.md:143`, Step Three
`17-chapter15.md:158`, Step Four `18-chapter16.md:145`, Step Five `19-chapter17.md:182`, Step Six
`10-chapter8.md:165`. Reading order: **1, 6, 2, 3, 4, 5.** Either renumber to match the new book,
convert to unnumbered "Do this now" blocks, or restore them as an explicit numbered program in an
appendix roadmap.

**Decision needed:** fix pointers to current numbers, or strip all forward-promising chapter
handoffs (the "In the next chapter we will..." blocks are an old-serial artifact; the Elijah
architecture makes them redundant anyway).

### S2 🔴 The three-books problem (register whiplash)

Three registers coexist, per design — but a fourth, unplanned one (research-synthesis academic)
is sitting inside Zone 3 material that the Elijah protocol says should be manifesto voice:

- **Manifesto (hot, first person):** Intro, Ch. 2–4 stages, Ch. 5 opener, Ch. 12 finale, Ch. 18 opener, Conclusion. *The best of the book.*
- **Manual (calm, second person, numerate):** Ch. 5, 8 (protocols), 9, 11, 13, 14–17 builds. *Works.*
- **Narrative (third person, gritty):** Ch. 0–3 scenes. *Works.*
- **Research-synthesis (clinical, third person, hedged):** Ch. 1 Foundations (`03-chapter1.md:53-55`), Ch. 6 Premise + Economic Paradox (`08-chapter6.md:13-40`), Ch. 7 Jahoda/Keynes section (`09-chapter7.md:29-49`), Ch. 4 Kipping section (`06-chapter4.md:33-53`), Ch. 18 Synthesis (`20-chapter18.md:57-61`). *Reads like a different author — "empirical trajectories indicate," "necessitates the implementation of."*

The research content is valuable — it's the book's evidence base. The fix isn't deletion; it's
**translation into the author's voice** (the way Ch. 7's Waymo table already almost is), plus
manifesto-voice on-ramps and off-ramps around the dense material. Worst offender: Ch. 18's
"Synthesis and the New Social Contract" (`20-chapter18.md:57-61`), which reads like a grant
application placed two pages before "Wake the fuck up."

### S3 🟠 The softened voice (the "you've lost" problem)

The author's original register was deliberately blunted for market appeal; the blunt spots read
as generic. Ground zero: `01-preface.md:10` — "So the robots have taken over. Congratulations!
The Singularity is upon us." The original construction ("Congratulations, you've lost.") had a
verdict in it; the current line is a greeting card. Other sanded-flat patches:

- `01-preface.md:12-14` — "Sure, popular media tells us... but that's not the only way it can go" / "This is about so much more than just the fear." Hedge, then filler.
- `01-preface.md:16` — the bolded "neat trick" paragraph ("your entire reality is a construct of your focus") is self-help register; Ch. 5 (`07-chapter5.md:12`) openly mocks exactly this kind of talk ("align your chakras... highly aesthetic ice crystals"). The book makes fun of its own preface.
- `08-chapter6.md:11-17` — "The Premise" headers-and-bold format; landing-page cadence.
- `20-chapter18.md:63-77` — "The Empowerment Architecture... The curriculum is modular, actionable, and technical." Strategy-deck language.

**Decision needed:** restore the verdict energy in the Preface/Intro ("you've lost" or equivalent),
and set a rule: no sentence in a manifesto zone that could survive unedited on a corporate site.

### S4 🔴 Duplication inventory (the fold's double-vision)

Verified duplicates, worst first:

1. **~450 words verbatim, twice.** "The Economic Paradox: Zero Marginal Cost and Post-Scarcity"
   (incl. the FALC treatment) appears identically at `03-chapter1.md:109-116` and
   `08-chapter6.md:32-40`. Sentence-for-sentence. One must go; Ch. 6 is the natural owner
   (Ch. 1 should tease, not deliver).
2. **The Redirection Protocol legal text, twice.** `16-chapter14.md:86-93` vs
   `22-appendix-a.md:80+` — near-verbatim ("community limits" vs "city limits"). Ch. 14 should
   summarize and point at Appendix A, which exists for exactly this.
3. **Chapter 8 teaches itself twice.** No-Notifications (`10-chapter8.md:70-75` vs `294-303`),
   dopamine reset / batch-processing (`76-80, 126-150` vs `304-311`), semantic hygiene
   (`82-124` vs `271-293`). Two folds of the same old chapter both survived the merge.
4. **Slop-ocalypse / Model Collapse / Algorithmic Judo, twice.** Full treatment in Ch. 10
   (`12-chapter10.md:41-200`, with math) and again in Ch. 16 (`18-chapter16.md:22-87`, without).
   Decide the owner: suggest Ch. 10 owns model collapse + judo as *doctrine*, Ch. 16 owns
   *distribution infrastructure* (metadata, IPFS, sneakernet — its unique content, `93-133`) and
   references back.
5. **The Shouse, introduced twice.** Ch. 12 defines it in full (`14-chapter12.md:37-69`), then
   Ch. 13 introduces it as new ("you build a 'Shouse' (Shop-House)", `15-chapter13.md:11`).
   Ch. 13's own build section then re-describes the architecture. Order the reveal.
6. **Soil biology, twice.** Rhizobium/soil-food-web/compost-tea: `11-chapter9.md:93-101, 207-273`
   vs `17-chapter15.md:89-145`. Suggest Ch. 15 owns the *why* (soil doctrine), Ch. 9 owns the
   *build* (bioreactor specs) — currently both do both.
7. **Mesh networks, three times.** Doctrine in Ch. 14 (`16-chapter14.md:96-141`), hardware in
   Ch. 17 (`19-chapter17.md:26-67`), plus Ch. 8's Relational Autonomy topology section
   (`10-chapter8.md:413-443`). Tolerable if each keeps its lane; currently they overlap ~40%.
8. **Stage-handoff stutters (stitching artifacts):** `04-chapter2.md:29` ("And that is exactly
   when the greed of Stage 1 turns into the sheer, unbridled terror of Stage 2.") vs `:35`
   ("That is when the greed of Stage 1 metastasizes into the sheer, unbridled terror of
   Stage 2.") — same sentence twice, six lines apart. Same pattern `:51` vs `:57` (adults step
   into the room), `:73` vs `:77` (dust settles). Ch. 2's Stage 5 close (`:115`) then Ch. 3
   re-derives the exodus decision at length.
9. **"Wake the fuck up," twice** — `20-chapter18.md:21` and `21-conclusion.md:13`, roughly six
   pages apart. It's a payload phrase; it detonates once.
10. **Reddit as the strawman, twice** — `02-introduction.md:21`, `21-conclusion.md:11`.

### S5 🟠 Substack scannability vs. depth

The author's own diagnosis is correct. The scannable architecture (short paragraphs, bold
headers, bullets, rhetorical question → answer) is right for the manual zones and the Zone 1
briefings — and fatal in the argument zones, where the book *asserts* instead of *argues*.
The tell: whenever a claim meets resistance, the text reaches for volume ("Bullshit. Absolute
bullshit.") instead of evidence or a scene. Specific depth deficits a hostile reviewer will find:

- **Stage 3's "adults"** (`04-chapter2.md:53-71`): the book's most load-bearing optimistic claim —
  who are they, how do they coordinate, why do they win? — is answered with "They deploy mesh
  networks." Three sentences of mechanism for the hinge of the entire nine-stage arc. (The Elijah
  weave's co-op *is* the answer at street level; the Foundations text needs the macro version.)
- **"The Preservation Solution"** (`08-chapter6.md:28`): "we simply need to use robots to grow the
  food and build the houses" — the word "simply" is doing the work of three chapters.
- **"Survival by Decree"** (`11-chapter9.md:15`): decreed *by whom*? Appendix A is the actual
  mechanism and isn't cited here — a missed self-rescue.
- **The Egalitarian Pivot**: promised on the site, absent from the book (known gap; belongs in
  Ch. 6/7).
- **Invented equations dressed as physics** 🟠: `10-chapter8.md:219` (t_recovery = τ·e^(λ·f) with
  an undefined "cognitive fragmentation constant"), `:204` (E_cognitive budget),
  `14-chapter12.md:103` (E-net = yield − demand in symbols). These sit next to *real* math
  (Ch. 13's beam calcs, Ch. 11's VRAM math, Ch. 10's model-collapse formalism) and cheapen it by
  association. Either flag them as illustrative models in a sentence, or cut the notation and say
  it in prose. A reviewer who catches one fake equation stops believing the real ones.

### S6 🟡 Crutch-word dependency (counts across book source)

"highly" ×52 · "thermodynamic(s)" ×49 · "completely" ×34 · "massive" ×30 · "autonomy" ×31 ·
"independent" ×37 (often as a find-replace scar — see S7) · "slop" ×22 · "corporate state /
corporate-state" ×19 · "in the cracks" ×14 · "primate" ×13 · "fundamentally" ×10 · "absolutely" ×6 ·
"lizard brain" ×3 (Intro, Ch. 2, Conclusion — enough that the Conclusion's use reads as a rerun).
"Thermodynamic" is a signature word and can keep a high count, but at 49 it's seasoning applied
with a shovel — especially "thermodynamic foresight" (`10-chapter8.md:345`, `15-chapter13.md:238`)
and "thermodynamic pod" (`07-chapter5.md:136`). "Highly" is pure filler in ~40 of its 52 uses.

### S7 🟠 Find-replace scars and grammar damage

A previous terminology sweep (sovereign → autonomous/independent) left visible scars:

- "a Autonomous Shell" / "a autonomous environment" / "a Independent Mesh Network" /
  "a elevated... node" — 5+ instances: `10-chapter8.md:343, 157`, `13-chapter11.md:237, 283`,
  `19-chapter17.md:67`. The article never got fixed.
- "an autonomous, autonomous node" — `14-chapter12.md:164` (doubled word).
- "SEMI-AUTOMATON CSA" — `14-chapter12.md:78` diagram title (automaton ≠ autonomous).
- "we are not passivists" — `12-chapter10.md:138` (malapropism for *pacifists*).
- "you will go absolute, raving mad" — `15-chapter13.md:55` ("absolutely").
- "we will layout Chapter 6" — `15-chapter13.md:280` ("lay out").
- "late twenty-first century" — `19-chapter17.md:12`; context is present-day satire, should be
  *early*.
- "The Doctor Analogy" — `15-chapter13.md:14` heading contains no doctor; mislabeled.

### S8 🔴 Formatting damage (will show in the printed book)

- **TOC pollution (verified in the built v5.4 EPUB):** the Mycodo install commands in
  `11-chapter9.md:151-159` escaped their code fence; "# Ensure system packages are up to date"
  and "# Download and run the Mycodo installation script" render as chapter-level headings and
  **currently appear in the book's table of contents.**
- **Chopped ASCII diagrams:** stray triple-backtick fences slice diagrams into fragments with
  orphaned arrows between them — `07-chapter5.md:90-129` (closed-loop cycle),
  `10-chapter8.md:25-55, 87-115`, `16-chapter14.md:25-55, 103-124`, `17-chapter15.md:29-61,
  98-135`, `18-chapter16.md:25-42, 63-78, 109-126`, `19-chapter17.md:76-112`,
  `22-appendix-a.md:44-60`. Every one renders broken.
- **Epigraph collisions:** no blank line between attribution and first paragraph in
  `01-preface.md:9-10`, `07-chapter5.md:9-10`, `10-chapter8.md:9-10`, `16-chapter14.md:9-10`,
  `17-chapter15.md:9-10`, `18-chapter16.md:9-10`, `19-chapter17.md:9-10` — the opening line glues
  itself to the quote in rendered output.
- **Doubled quote marks** in the Hemingway epigraph, `16-chapter14.md:8` ("“How did you...").
- **Double-bold artifact** `01-preface.md:52` (`****How to prepare...****`).
- **Stray em-dash sign-offs** ending Ch. 5, 8, 9, 10, 11, 14, 15, 16, 17 (`—` alone on a line) —
  a blog-serial artifact; the book needs chapter endings, not post signatures.
- **Raw LaTeX leakage:** `03-chapter1.md:73` (`y = x + \\text{MHA}(...)`) and escaped `\\~`/`\\>`
  in the Ch. 1 tables; headerless tables at `03-chapter1.md:62-69, 97-105` (`| | | |` first row).
- **Appendix B is a wall:** all 104 sources in a single unbroken paragraph
  (`23-appendix-b.md:3`). Unusable as a reference section; needs a numbered list, one source per
  line.

### S9 🔴 The timeline contradiction (when is the reader standing?)

The book cannot decide whether the collapse **is coming** or **already happened**, and the two
framings currently interleave:

- **Pre-2027 framing** (Intro, Ch. 1–4, 18, Conclusion): "the clock is ticking toward 2027";
  "we are already well into [Stage 1]."
- **Post-collapse framing** (the folded manual chapters): "Now that those supply chains have
  collapsed" (`07-chapter5.md:31`); "When the Singularity hit, the corporate-state algorithms..."
  (`16-chapter14.md:62`); "a staggering statistic from the twilight of the old world"
  (`16-chapter14.md:76`); "In the late twenty-first century, your refrigerator..."
  (`19-chapter17.md:12`); Appendix A's "modeled directly on the historic self-preservation codes
  deployed during the early days of the Singularity" (`22-appendix-a.md:12`).

Related internal contradiction: `07-chapter5.md:24` advises making yourself "thermodynamically
expensive to hunt" by drones — but Ch. 2/3's core thesis is that the machine *doesn't hunt
humans*, it leaves ("Why the hell would it fight us? Eradicating humanity is inefficient,"
`04-chapter2.md:111`). Pick one: either the manual chapters are written *from* the post-2027
world as a device (which is actually a strong conceit — the manual Elijah writes), or everything
is present-tense preparation. **This is the single biggest author decision in the dossier**,
because the Elijah weave makes the device available for free: Zone 3 could be framed as the
manual-in-progress, written as things fall.

Also in this family: legal posture whiplash in Ch. 13 — the manifesto section says work *with*
the building department ("They are not the police... get the official stamp,"
`15-chapter13.md:14`) while the build section engineers *around* inspection ("If the local
municipality sees you... their building inspectors will descend upon you like locusts,"
`15-chapter13.md:65`). Both postures are defensible; holding both without acknowledgment isn't.

---

## Chapter-by-chapter findings

### Preface — "Welcome to the Weirdness" (`01-preface.md`, 769 words)

**Verdict:** The most market-softened pages in the book; currently the weakest opening possible
for this voice. 🟠

- 🟠 `:10` — the amputated punchline (see S3). This is page one; the verdict belongs here.
- 🟠 `:16` — self-help register clash ("reality is a construct of your focus"); contradicted in
  spirit by `07-chapter5.md:12`. Cut or rewrite as cognitive-firewall preview in the book's voice.
- 🟡 `:12` — "Sure, popular media tells us we'll be fending off hordes of Terminator bots" +
  trailing space typo; `:14` "This is about so much more than just the fear" is filler between
  two better sentences.
- 🟡 `:22` — the hundred-year joke lands but the sentence is a 60-word pileup; needs one breath
  ("...threaten to eradicate all life on earth to... well. It's pretty much the same, isn't it?").
- 🟡 `:26` — "First / Second / Third" list asserts the book's whole thesis in 40 words before the
  book has earned it; consider making these the promised *findings* rather than givens.
- 🟡 `:44-52` — chapter list bullets reference "the next few chapters" but describe the whole
  book; `:52` double-bold artifact; `:46-51` the parenthetical jokes are the voice — keep those.
- 🟡 `:56` — "Adjust your neural link electrodes" is the phrase Ch. 8 mis-remembers as the
  Introduction's brain-in-a-jar joke (S1); if the Preface keeps it, fix Ch. 8's pointer; if the
  Preface loses it, Ch. 8's opener needs a new anchor.
- Keep: "You are an active participant, even if your participation is currently limited to trying
  not to starve" (`:54`) — best line on the page.

### Introduction — "The Uncompromising Truth" (`02-introduction.md`, 592 words)

**Verdict:** This is the tone benchmark for the manifesto register. Mostly keep. 🟡

- ✅ `:13` — crackpot/cracked redundancy fixed this session (author-approved).
- 🟡 `:15` — "I needed an appeal to authority" opens a thought it never finishes: *which*
  authority? The industry figures now conceding AGI? Name it or cut the setup.
- 🟡 `:17` — "This is the ultimate idea creator" — floating antecedent (the machine? the moment?).
- 🟡 `:19` — "People used it to build entire game worlds in a single prompt. I used it to secure
  my own infrastructure and rebuild the way I interface with the world" — the one spot where a
  *specific* example would prove the authority claim; currently vague exactly where it must not be.
- 🟡 `:23` — "It's not five years away. It's not ten." followed by 2027: from a 2026 vantage the
  rhetorical ladder undersells the actual claim. "It is eighteen months away" hits harder than
  both sentences.
- 🟡 `:25` — "it's already happened in the past tense" — redundant ("already happened" + "in the
  past tense"); pick one.
- Keep: "It's time. It's finally time." · the asshole paragraph (`:13`) · "Be afraid of the people
  who think they can control it" (`:27`).

### Chapter 0 — "The Demonstration" (`00-chapter0.md`, ~3,400 words)

**Verdict:** The crown jewel. Do not touch the architecture. 🟡 only.

- 🟡 `:120` — **age continuity error:** "forty years of social training will run the body" — by
  the established timeline (grew up on farm, gig-economy twenties, taught himself DS in 2020, two
  years into Claypot at the Chat Horizon launch) Elijah is early thirties. "Thirty years" or "a
  lifetime."
- 🟡 `:64` — the "polite about it" paragraph is a ~120-word single sentence; it *almost* earns its
  length; consider one full stop after "day trading."
- 🟡 `:16` — "It took about thirty years and the end of the world as he understood it before the
  lesson came back around" — quietly confirms the ~30s age; keep consistent with the `:120` fix.
- Keep, specifically: the napkin ("I just want people to see what's coming" → "He thought he was
  handing them a telescope"), "the vertigo of watching the impossible get a Jira ticket," "it
  wasn't a client, it was the tide," "Congratulations on the — yeah. Congratulations."

### Chapter 1 — "The Event Horizon" (`03-chapter1.md`, ~3,100 words)

**Verdict:** Scene excellent; Foundations is where the register whiplash begins. 🟠

- 🟠 `:53-55` — first appearance of research-synthesis voice ("empirical trajectories across
  machine learning... indicate that the event horizon has already been crossed"). Two paragraphs
  after a scene that *dramatized* exactly this, the clinical restatement reads like a deposition.
  Translate into first person or trim to an on-ramp.
- 🔴 `:109-116` — the Economic Paradox / FALC block that also lives verbatim in Ch. 6 (S4-1).
  Recommend: cut here, keep a two-sentence tease pointing at Part II.
- 🟠 `:62-69, 97-105` — headerless tables render with an empty first row; `:65` escaped `\\~` and
  `\\>` artifacts; `:73` raw LaTeX will print as source code in the EPUB (S8).
- 🟡 `:77` — "without a human touching a joystick" also appears at `02-introduction.md:15`
  ("without a human ever touching a joystick") — same image twice in 20 pages.
- Keep: the whole Zone 2 scene; "There was only the power bill, and the people who could afford
  it" (`:42`).

### Chapter 2 — "The Era of AGI, Stages 1–5" (`04-chapter2.md`, ~3,400 words)

**Verdict:** The manifesto engine of the book — and the stitch-stutter capital. 🟠

- 🟠 Stage-handoff stutters (S4-8): `:29` vs `:35`; `:51` vs `:57`; `:73` vs `:77`. Each pair says
  the same sentence twice because chapter breaks used to live between them. Kill one of each.
- 🔴 Stage 3 depth gap (S5): "the adults" get no mechanism. This stage carries the book's
  optimism; it's currently the thinnest argued section in Part I.
- 🟡 `:81-83` — "The robots will just do stuff... it will download itself into a physical body,
  look at the world, and just go out and do shit" — "just do stuff/do shit" twice in three lines;
  the second one should escalate, not repeat.
- 🟡 `:87-91` — the free-butler passage ("Look me in the face. Look me dead in the eyeballs...")
  is the hot voice working; keep — but "Bullshit. Absolute bullshit." + "for one second" is
  assertion stacked on assertion; one more concrete image (who lies, and why) would make it argue.
- 🟡 `:101` — Waymo evidence here duplicates Ch. 7's documented version (`09-chapter7.md:53-62`);
  fine as preview if Ch. 7 is cited.
- Keep: "They looked at the closest thing we've ever had to magic, and their first instinct was to
  figure out how to put a coin slot on it" (`:17`) · "You cannot ban mathematics" (`:47`) · "We
  are just something it outgrew" (Ch. 3 carries the twin of this — coordinate them).

### Chapter 3 — "The Leap to ASI" (`05-chapter3.md`, ~2,000 words)

**Verdict:** Scene new (this session); Foundations mostly sound; one weak patch. 🟡

- 🟡 `:49` (Stage 7) — the intuition/meat-avatar aside ("your gut feeling... might just be your
  *true* self, sitting somewhere outside the game") is unsupported woo sitting directly before
  Ch. 4's careful Bayesian treatment of the same hypothesis; the contrast damages it. Cut or
  reframe as a deliberate provocation.
- 🟡 `:23` — "It is the ultimate insult to human arrogance: we aren't even worth destroying. We
  are just something it outgrew." Excellent — but it pre-spends Ch. 4's Stage 8 opening beat
  (machine stops paying attention). Sequence check.
- 🟡 `:39` — "tosses us the cure the same way you might toss a bone to a stray dog" — the Zone 1
  bullet now uses the same image; vary one.

### Chapter 4 — "Universal and Multiverse Apex" (`06-chapter4.md`, 855 words — thinnest remaining)

**Verdict:** Register-whiplash exemplar; also the shortest chapter. 🟠

- 🟠 The cut from "We thought we could put a leash on infinity" (`:19`) to "advanced Bayesian
  statistical analyses, such as those conducted by astronomer David Kipping" (`:43`) is the
  hardest tonal jump in the book. The Kipping material is good; it needs a manifesto on-ramp
  (two sentences of "here's why you should care about the math") and an off-ramp back to the
  reader.
- 🟡 `:27` — "we literally lack the biological hardware" — one of the three "literally"s; fine
  here, but see S6.
- 🟡 Planned Elijah scene (overreach modeling the cosmic scale) will double the chapter; the
  Foundations text should then lose its own repeated "scale" throat-clearing (`:13-15` says
  "scales out / galactic scale / optimizing the universe" three ways).
- Keep: "That is the scale of human arrogance. We thought we could put a leash on infinity."

### Chapter 5 — "The Thermodynamics of Survival" (`07-chapter5.md`, ~1,400 words)

**Verdict:** Best manual-register opener in the book; two doctrine bugs. 🟠

- 🔴 `:31` — post-collapse tense slip (S9): "Now that those supply chains have collapsed or been
  locked behind corporate firewalls, you are on your own."
- 🟠 `:24` — the drone-hunting ROI aside contradicts the book's own no-war thesis
  (`04-chapter2.md:111`). Either delete, or explicitly mark it as the *corporate-state* threat
  model (human-owned machines, not the ASI) — which is actually the book's position elsewhere.
- 🟠 `:90-129` — chopped closed-loop diagram (S8).
- 🟡 `:55` — "brain generating existential dread" as a metabolic line item: keep, it's the voice.
- 🟡 `:140` — "It's time to stop leaking energy to a machine that doesn't love you" — strong
  close, then a stray "—" sign-off under it (S8).
- Keep: the chakra/ice-crystals opener (`:12`), "metabolic liquidation" (first use — later reuses
  dilute it), the efficiency table.

### Chapter 6 — "The Singularity Is a Done Deal" (`08-chapter6.md`, ~1,050 words)

**Verdict:** Currently a scaffold: an abstract, a duplicate, and two good fragments. The
Egalitarian Pivot belongs here. 🔴

- 🔴 `:32-40` — verbatim duplicate of Ch. 1's Economic Paradox block (S4-1). If Ch. 6 keeps it,
  it must be *rewritten into the hot register*, not pasted.
- 🟠 `:13-17` — "The Premise" re-argues Ch. 1's event-horizon claim in bold-header landing-page
  format, including a near-verbatim reprise of the "fence this moment behind a digital moat"
  sentence (`03-chapter1.md:55`).
- 🟠 `:28` — "The Preservation Solution" (S5): "we simply need to use robots to grow the food and
  build the houses" — this *is* the Egalitarian Pivot in embryo; it deserves the section the
  homepage promises, with the mechanism (who buys the robots, who owns them, what happens to the
  first town that does it).
- 🟡 `:46` — "The Invisible Hand Made Visible" is a great coinage buried mid-paragraph in
  quotation marks; it's a section header trying to escape.
- 🟡 `:48` — "'Number Go Up' over human survival" — keep.
- Note: planned Elijah scene (quits Claypot, walks into Marta's shop, pitches the co-op like a
  startup, gets shut down) will carry this chapter; the Foundations here need the most rebuild of
  any chapter to deserve their scene.

### Chapter 7 — "The Battle Lines" (`09-chapter7.md`, ~1,650 words)

**Verdict:** Strong evidence, risky frame, no connective tissue. 🟠

- 🟠 `:13-17` — the Entitled/Ready table's demographic claims ("Primarily low-empathy
  individuals") are unfalsifiable psychographics presented as taxonomy — the single most
  review-vulnerable passage in the book. The *behavioral* split (resist vs. receive) is
  defensible; the *characterological* one invites the "phrenology of class" take-down. Reframe
  rows as incentives, not natures.
- 🟠 The chapter is three blocks (table / capitalism bullets / Jahoda-Keynes-scarcity research)
  with no authorial thread between them; the research is clinical register (S2) but close to
  translating well — the Jahoda table is already the book's method at its best.
- 🟡 `:53-62` — Waymo/Luddite section is good and should be the *canonical* home of that evidence
  (Ch. 2 previews it).
- 🟡 Planned Denny scene (naive "reskilling" comment taken apart) is the missing connective
  tissue; the Luddite allegory weapon is already staged in the ledger.
- Keep: "The modern 'rage against the robots' follows this exact historical lineage" paragraph
  (`:62`); the Jahoda latent-functions table.

### Chapter 8 — "The Psychology of the Collapse" (`10-chapter8.md`, ~4,850 words — 2.4× median)

**Verdict:** The most damaged chapter in the book: an old *final* chapter and two other folds all
pasted whole. Needs surgery, not sanding. 🔴

- 🔴 `:18` — "In this **final** chapter" — it's Chapter 8 of 18.
- 🔴 `:165-176` — "Step Six: Reboot Your Operating System" + "The book is written. The systems are
  designed." — a book *ending* living mid-book, complete with valediction ("Let's get to work.").
- 🔴 `:12` — broken opening callback (S1): the brain-in-a-jar joke it "remembers" from the
  Introduction doesn't exist there or anywhere.
- 🔴 Duplicate protocol teaching (S4-3): the same three protocols appear twice each in two
  registers. Suggested cut line: keep the *second* fold ("Cognitive Firewalls and Semantic
  Hygiene," `:182-335`) which is stronger and quantified, fold the first pass (`:10-176`) down to
  its unique material (the extraction-engine framing, `:14-16`, and the master-key thesis,
  `:152-163`).
- 🟠 `:219, 204` — invented-equation risk (S5): t_recovery and E_cognitive notation.
- 🟠 `:341-497` — the Relational Autonomy fold is *good* but arguably mis-shelved: it's commons
  doctrine (game theory, Dunbar, mesh topology) inside a psychology chapter, overlapping Ch. 12's
  CSA and Ch. 15's pooling. Candidate: it becomes the Foundations of Ch. 6 or 9 (where the co-op
  enters the narrative), letting Ch. 8 be purely the mind chapter.
- 🟠 `:335, 497` — two different "in the next chapter" promises, both wrong (S1), six hundred
  words apart, each ending in an em-dash sign-off.
- 🟡 `:14` — "Your jar is your smartphone" — keep; it's the chapter's true opening.
- Keep: "They do not need to physically cage your body if they can completely rent out your
  prefrontal cortex for a fraction of a cent per impression" (`:16`) · "Reclaiming your focus is
  not a personal self-care option; it is a hostile, political act" (`:163`) · the Tit-for-Tat and
  Dunbar sections (wherever they land).

### Chapter 9 — "Deglobalization and the Neighborhood Factory" (`11-chapter9.md`, ~2,700 words)

**Verdict:** Identity crisis: policy manifesto + energy-market case study + full greenhouse build
manual, under one title. 🔴

- 🔴 `:151-159` — **the TOC bug (verified):** Mycodo install commands escaped their code fence;
  two bash comments render as h1 and appear in the book's table of contents. Highest-priority
  mechanical fix in the dossier.
- 🔴 `:287-289` — "we transition from Acts I and II to Act III... Chapter 9: Hacking the Deed"
  (S1) — spoken from inside Chapter 9.
- 🟠 `:15` — "Survival by Decree... guaranteed by decree" (S5): no mechanism; Appendix A *is* the
  mechanism and goes uncited.
- 🟠 `:16` — "Johnny Autoseed: This is the practical execution of this vision" — introduced as if
  the reader knows it; one grounding sentence needed (what it is, whose it is).
- 🟠 Soil/build overlap with Ch. 15 (S4-6): this chapter should own the *hardware* (Mycodo, CNC
  bed, ACT reactor specs); the soil-doctrine paragraphs (`:93-101`) belong to Ch. 15.
- 🟡 `:141-145, 266-270` — list items wrapped in stray code fences (S8).
- 🟡 `:47` — "you are eating petroleum" — keep; the strongest three words in the chapter.
- 🟡 Planned Marta/Reuben scene (elegant unbuildable spec, reworked for the real world) is the
  natural carrier for the chapter's thesis; the "guild returns" allegory is staged in the ledger.

### Chapter 10 — "The 'Create Over Consume' Protocol" (`12-chapter10.md`, ~2,200 words)

**Verdict:** Title promises doctrine; chapter delivers a 3-step civic starter plus a full essay
that Ch. 16 repeats. 🔴

- 🔴 S4-4 — decide ownership of Slop-ocalypse/Model Collapse/Algorithmic Judo between Ch. 10 and
  Ch. 16 (recommendation in S4).
- 🟠 `:169-176` — Rule 1 teaches manufacturing outrage two chapters after Ch. 8 teaches detoxing
  from it. The tension is resolvable in one line ("we are not adding to the slop; we are wrapping
  the antidote in its skin") — currently unacknowledged.
- 🟠 `:206` — ends promising "Chapter 5: The Autonomous Shell" (S1).
- 🟡 `:138` — "passivists" → pacifists (S7).
- 🟡 `:11` — "The line between someone who survives this period and someone who is a casualty is
  simple: Create more than you consume." — the actual thesis; deserves to be the chapter's spine
  rather than paragraph two of eleven.
- 🟡 `:37` — the intergenerational garage exchange is quietly one of the most practical ideas in
  the book; currently a bullet. Consider expansion (or let the Denny scene dramatize it).
- Keep: "It is a copy of a copy of a copy, run through a fax machine, photocopied, and scanned
  back in" (`:105`) · "You are using their silicon to build our stone" (`:200`).

### Chapter 11 — "Using the Tech to Your Advantage" (`13-chapter11.md`, ~2,200 words)

**Verdict:** The Crucible build is the best pure-manual section in the book; the two manifesto
stubs above it are vestigial. 🟠

- 🟠 `:11-19` — the two numbered sections (Skill Acquisition, Geographic/Legal Literacy) are
  outline notes wearing a chapter's clothes: five sentences each, no examples. Either grow them
  (the "argue with the machine" idea deserves a worked example) or fold into Zone 1 bullets.
- 🟠 `:284, 290` — old chapter refs (S1).
- 🟡 `:237` — "a Autonomous Shell" (S7); `:283` "a autonomous environment."
- 🟡 `:61-88` — VRAM math is sound and reads well; model names (Llama-3, Mistral-8x22B, RTX 3090,
  P40) will date the book fastest of anything in it — consider a one-line hedge ("models and
  cards will have new names by the time you read this; the math won't").
- 🟡 `:156` — docker-compose `version: '3.8'` key is obsolete in Compose v2 (cosmetic; flagged
  only because the book's authority is technical).
- 🟡 `:283` — "No-Updates Policy... security patches, which are frequently used to push remote
  telemetry" — defensible in an air-gapped context but will be quoted out of context by hostile
  reviewers; consider one qualifying clause (air-gapped systems only).
- Keep: "we compute on copper and silicon we own, under a roof we built, powered by solar
  electrons we harvested" (`:29`) · the split-loop cooling design.

### Chapter 12 — "The Land Strategy" (`14-chapter12.md`, ~2,300 words)

**Verdict:** Contains the book's emotional proof-of-concept (the grandmother) and its most
redundant back half. 🟠

- 🟠 `:160-194` — the Master Checklist recapitulates the whole book with old chapter numbers
  (S1); as-is it's a broken index. Either update and move to Ch. 18/appendix (it *is* the
  roadmap), or cut — Ch. 18 already does this job.
- 🟠 Shouse definition precedes Ch. 13's introduction of the Shouse (S4-5).
- 🟡 `:78` — "SEMI-AUTOMATON CSA" (S7); `:164` "autonomous, autonomous node" (S7).
- 🟡 `:103-112` — E-net equation is prose in costume (S5).
- 🟡 `:204-226` — "The Recapping Truth: Right Fucking Now" — the hot register done *right*
  (it's earned by the grandmother scenario above it); but it is a chapter-ending crescendo
  followed by six more chapters — check placement in the read-through.
- Keep: the entire grandmother scenario (`:23-35`) — "Is she just supposed to sit there, run out
  of money, and die in a fire trap because her personal ledger doesn't balance?" · "We are
  conducting systemic maintenance of our human perimeter" (`:152`) · "her existence was validated
  and secured by the thermodynamic surplus of her local community" (`:158`).

### Chapter 13 — "The Shouse Protocol" (`15-chapter13.md`, ~2,800 words)

**Verdict:** The best manual chapter, nearly print-ready; three posture/consistency bugs. 🟠

- 🟠 Legal-posture whiplash (S9): `:14` (befriend the building dept) vs `:65` (design to evade
  inspectors). Needs one bridging sentence establishing the doctrine (e.g., permits where the
  code serves you, low profile where it's captured) — or the Reuben scene carries it.
- 🟠 `:280` — ends promising nonexistent "Chapter 6" (S1).
- 🟡 `:27-31` — "$25,000 exit strategy" never reconciles with Ch. 12's land-plus-ten-years-of-taxes
  math; one sentence ("materials only; land is Chapter 12's problem") closes the hole.
- 🟡 `:55` — "go absolute, raving mad" (S7); `:14` "The Doctor Analogy" heading (S7).
- 🟡 `:9` — Buckminster Fuller epigraph is "attributed" — the one epigraph without a source; fine,
  but the book leans on citation authority elsewhere; consider swapping for a sourced quote.
- Keep: everything from `:51` down — the pier math, the surgical cut, the wet-room. "It feels
  less like a sanctuary and more like a highly aesthetic, industrial coffin" (`:57`) is the manual
  voice at its best.

### Chapter 14 — "The Collapse of the Long Tail" (`16-chapter14.md`, ~1,450 words)

**Verdict:** Good systems essay wearing the wrong tense and carrying a duplicate statute. 🟠

- 🔴 `:62, 76` — the strongest post-collapse tense violations in the book (S9): "When the
  Singularity hit..." / "twilight of the old world."
- 🔴 `:86-93` — Redirection Protocol legal text duplicates Appendix A (S4-2).
- 🟠 `:96-141` — Municipal Mesh section overlaps Ch. 17 hardware and Ch. 8 topology (S4-7); this
  chapter's unique contribution is the *logistics* frame (JIT trap, short loop) — let it keep
  that and point sideways for the radios.
- 🟡 `:8` — doubled quote marks in the Hemingway epigraph (S8); `:143` "Step Two" orphan (S1).
- 🟡 `:16` — "a high-wire act performed by a drunk unicyclist during an earthquake" — keep.
- 🟡 Planned Denny scene (the local business that dies; Elijah could have warned them) is the
  guilt-echo of Ch. 0 and will give this chapter the human floor it lacks.
- Keep: "In the cracks, there is no such thing as waste. There is only misplaced energy" (`:80`) ·
  "you are always exactly 72 hours away from starvation" (`:64`).

### Chapter 15 — "The Power of Reclaiming Soil" (`17-chapter15.md`, ~1,550 words)

**Verdict:** Solid doctrine chapter; needs deduplication against Ch. 9/12 and a legal flag. 🟠

- 🟠 S4-6 — owns soil *doctrine*; hand the reactor/build specifics back to Ch. 9.
- 🟠 `:87` — "Religious or Educational Trust Shields... complete exemption from local property
  taxes" — the most legally exposed paragraph in the book; needs either a jurisdictional hedge or
  publisher legal review. (Related: the book has no legal disclaimer in front/back matter; the
  site has one. Add one.)
- 🟡 `:150, 162` — old chapter refs (S1); `:158` "Step Three" orphan.
- 🟡 `:29-61, 98-135` — chopped diagrams (S8).
- Keep: "you cannot eat code" (`:16`) · "you are bringing a knife to a laser fight" (`:25`) ·
  "a tenant farmer with extra steps" (`:94`) · "The ground is the only thing they aren't making
  any more of" (`:167`).

### Chapter 16 — "Digital Leverage and Media Autonomy" (`18-chapter16.md`, ~1,470 words)

**Verdict:** Duplicate of Ch. 10 for its first half; genuinely unique and good in its second. 🔴

- 🔴 `:22-87` — S4-4 duplication (Slop-ocalypse, Model Collapse, Judo re-explained).
- 🟡 `:93-133` — metadata sanitization / IPFS / sneakernet is this chapter's real estate; keep and
  expand (the sneakernet cycle diagram is chopped, S8).
- 🟡 `:145` — "Step Four" orphan (S1); `:14` "we were the crop" — keep.
- 🟡 `:143` — "A community that stops telling its own stories will eventually believe the stories
  told about them by the machine" — quietly the thesis of the whole media part; deserves
  prominence.
- Planned scene here is the co-op's earned win (media cell scales while they sleep) — the one
  chapter whose ledger row has no friction; fine, but the Foundations then must carry the caution
  themselves (currently they do).

### Chapter 17 — "Tools of the Trade" (`19-chapter17.md`, ~1,700 words)

**Verdict:** Strong workbench chapter; small factual and reference bugs. 🟡

- 🟠 `:27` — "In Chapter 2, we discussed..." (S1).
- 🟡 `:12` — "late twenty-first century" → early (S7).
- 🟡 `:67` — "a elevated 100-milliwatt LoRa node can easily transmit messages over thirty miles"
  — grammar (S7), and "easily... thirty miles" needs the line-of-sight qualifier it half-has;
  real-world Meshtastic users will call this optimistic. Say "with clear line of sight from a
  ridge" and it's defensible.
- 🟡 `:76-112` — inverter-trap diagram chopped (S8); `:182` "Step Five" orphan.
- Keep: "If you cannot understand how it works, fix it with basic hand tools, and run it without
  an internet connection, it is not a tool — it is an electronic leash" (`:22`) · the Faraday
  trash can (`:178`).

### Chapter 18 — "The Roadmap and the Premortem Pivot" (`20-chapter18.md`, ~1,250 words)

**Verdict:** Opens as the best hot chapter in Part III; ends as a grant abstract. 🟠

- 🟠 `:57-61` — "Synthesis and the New Social Contract" is the densest clinical prose in the book
  (S2), two pages after "Wake the fuck up" (`:21`). Rewrite in the author's voice or cut — the
  ALC section already says it better.
- 🟠 `:63-77` — "The Empowerment Architecture" is strategy-deck register ("The curriculum is
  modular, actionable, and technical"); its two audiences (under-25s, institutional stakeholders)
  are a genuinely good framing trapped in bullet-speak.
- 🟡 `:35` — "the 'orbs' everyone keeps talking about" — a 2025-2026 news wink that will be
  incomprehensible in three years; either explain in a clause or cut.
- 🟡 `:45` — "I have coined a term for this baseline metric" — announcing the coinage deflates it;
  just coin it.
- 🟡 `:59` — "Abundance Quotient" appears here for the first time, capitalized, undefined (known
  gap from the editorial queue).
- 🟡 `:13` — the premortem list is the chapter's engine — the planned full-co-op premortem scene
  can dramatize exactly this list; keep them in sync.
- Keep: the Five Black Swans (`:27-35`) — best structural device in Part III · "GDP is a ghost
  metric designed to keep you on the hamster wheel" (`:47`) · "Wake the fuck up" (here, not in the
  Conclusion — see S4-9).

### Conclusion — "The 2027 Tipping Point" (`21-conclusion.md`, 359 words)

**Verdict:** A pamphlet ending a 45,000-word book. 🔴 thinness (known; expansion planned).

- 🔴 Length: the book spends 3,400 words arriving (Ch. 0) and 359 leaving. The planned Elijah
  loop-close (finishes the manuscript, back to the Bear Flag) is the right fix; the Conclusion
  also needs the reader's send-off — the "first 48 hours" directive the whole book has been
  promising.
- 🟠 `:13` — "Wake the fuck up" duplicate (S4-9); `:11` "scrolling through Reddit" duplicate of
  the Intro's Reddit beat; "your lizard brain is probably screaming" — third lizard-brain, and
  the *same reader-address move* Ch. 18 opened with eight pages earlier ("your brain is probably
  looking for an exit strategy") — pick one.
- 🟡 `:19` — "There is no pausing it. There is no pulling the plug. There is no going back" —
  good triple; note Ch. 2's Stage 2 already used "pull the plug" as the establishment's move —
  here it flips meaning (nobody can), which works if intentional; make sure it reads as an echo,
  not a contradiction.
- Keep: "The choice is ours: keep arguing over the scraps of a dying system, or build the
  machinery of our own freedom" · "The singularity is here. Survive it if you can." — the closer
  line is right; everything before it needs to earn it harder.

### Appendices

- **A — Municipal Autonomy Code** (`22-appendix-a.md`): the book's most original artifact; keep.
  🟠 old chapter refs `:39-41` (S1); chopped matrix diagram `:44-60` (S8); "modeled directly on
  the historic self-preservation codes deployed during the early days of the Singularity" (`:12`)
  is the post-collapse frame again (S9) — if the frame-device is adopted book-wide this line is
  perfect; if not, it dangles. Needs the same legal-review flag as Ch. 15.
- **B — Works Cited** (`23-appendix-b.md`): 🟠 all 104 sources in one unbroken paragraph (`:3`);
  reformat as a numbered list or it's decorative.
- **C — Executive Reference Guide** (`24-appendix-c.md`): useful; 🟡 its internal "PART I/II/III"
  labels (stage groupings) collide with the book's actual Part I/II/III (which are different
  divisions) — rename to "The Nine Stages: 1–5 / 6–7 / 8–9" and the confusion dies.

---

## Priority order (what I'd fix first, as your editor)

1. **S8/S1 mechanical sweep** — TOC pollution (Ch. 9 bash comments), chopped diagrams, epigraph
   spacing, grammar scars, and every chapter-number pointer. Zero judgment calls, pure trust
   repair. One focused session.
2. **S4 deduplication** — the verbatim econ block (Ch. 1 vs 6), Ch. 8's double-taught protocols,
   Ch. 10 vs 16 ownership, Ch. 14 vs Appendix A. Each is a decision + a deletion.
3. **S9 timeline ruling** — the author decides where the reader stands (recommend: Zone 3 as the
   manual Elijah writes as it happens; it converts every tense bug into a feature).
4. **S3 voice restoration** — Preface/Intro first (they're the sample chapters any agent or
   reader sees), then Ch. 6 and Ch. 18's synthesis sections.
5. **S5 depth work** — Stage 3 mechanism, the Preservation Solution → Egalitarian Pivot section,
   Conclusion expansion. This overlaps the planned Elijah weave and voice pass.
6. **Elijah weave continues** (Ch. 4–18 + Conclusion) — already planned and ledgered; the weave
   resolves several dossier items for free (Ch. 6's scaffold, Ch. 14's human floor, the
   Conclusion's loop-close).

---

*Dossier compiled from a full read of `src/lib/data/book/` at commit `9a6474b` (plus the
approved introduction phrase fix). Nothing else has been changed.*
