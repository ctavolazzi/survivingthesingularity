---
type: research
date: 2026-09-21
parent: "[[Daily Notes/2026-09-21]]"
hub: "[[Hubs/2026-09-21_hub]]"
status: brief-for-codex
tags:
  - research
  - sts-book
  - editorial-brief
---

# Floor-raising argument: research brief for formalization

**Author of the source argument:** CT. **Status:** raw, unedited, captured verbatim below.
**Task owner:** Codex. **Target:** Surviving the Singularity, following the v0.8.0 food-first edit.

---

## 1. Source text, verbatim

Reproduced exactly as CT wrote it, including one transcription slip resolved in section 7.
Do not silently correct this block. It is the source of record.

> What all these people fail to address is that very few people care about protecting social order.
>
> People care about feeling safe. They care about having food and shelter.
>
> HOW that happens, currently, is completely dependent on money.
>
> We pay poor people to do the work we either can't or don't want to do.
>
> Your clothes were made by Simeon working for less than $3 a day. Your food was grown by immigrants working all day out in the sun.
>
> The modern world exists on the broken backs of exploited brown people, and all these alarmists worry about is losing their jobs...and becoming like the masses.
>
> I've seen absolutely NO ONE talking about how the pace of tech promises to increase the floor level of quality for ALL HUMANS if we steer this right.
>
> Sure, oppression will obviously come first. The jabs will leverage this against their enemies. Always have.
>
> But why happens afterwards?
>
> Humans have ALWAYS followed a repetitive pattern of technological development:
>
> 1. first it didn't exist
> 2. a power imbalance forms
> 3. privileged people leverage that imbalance
> 4. regular people start to notice they are being exploited
> 5. someone invents something new
> 6. the establishment tries to purchase the innovation, either to leverage or suppress it
> 7. more people make the same discovery over time
> 8. the technology is violently resisted
> 9. years later, when the next generation is born into a world where the technology has always existed since before they were born, it becomes commonplace and taken utterly for granted
>
> This is called the hype cycle.
>
> First, it's impossible
> Then, it's a miracle
> Later, it's just a part of everyday life
> Finally, it fucking sucks and always has
>
> This is just how it goes for us humans.
>
> AI might be different...but for now, it is still very much a part of the same overall human technological development process.

---

## 2. The argument decomposed

Formalize these as distinct claims. Each one has a different evidentiary burden, and merging them is how the piece becomes attackable.

| # | Claim | Type |
|---|---|---|
| C1 | People do not value social order as such. They value safety, food, shelter. Social order is instrumental. | Empirical, testable |
| C2 | Access to safety, food and shelter is currently mediated almost entirely through money. | Empirical, largely uncontested |
| C3 | That mediation is sustained by low-paid labor performing work wealthier people cannot or will not do. | Empirical, sourceable |
| C4 | That labor is disproportionately non-white and often migrant. | Empirical, sourceable |
| C5 | Mainstream AI alarm concerns white-collar job loss, that is, the fear of joining the exploited class rather than the fact of that class existing. | Interpretive, needs discourse evidence |
| C6 | Almost no one discusses AI raising the floor for all humans. | Falsifiable, probably overstated, see section 5 |
| C7 | Oppression arrives first. Incumbents weaponize new capability against opponents. | Historical, well supported |
| C8 | Technology follows a repeating nine-stage pattern. | Model claim, needs literature placement |
| C9 | AI currently sits inside that pattern rather than outside it. | Argued conclusion |

---

## 3. Task

Produce a formal, researched, well rounded version of this argument suitable for the book. Work in `active/sts-v0.8.0` on branch `book-v0.8.0`, consistent with the food-first edit already there.

Deliver in this order:

1. **Research memo first.** Before any prose, produce `docs/v0.8.0/FLOOR-ARGUMENT-RESEARCH.md`: every claim above, the evidence found for and against it, with citations and exact locators. Mark each claim supported, narrowed, or unsupported.
2. **Then a position on placement.** Where the argument belongs. Options include a new section, an expansion of the introduction, or distribution across the existing practical chapters. Recommend one, and say what it costs.
3. **Then prose,** only once 1 and 2 are settled and CT has seen them.

Do not skip to prose. The v0.8.0 critique already established that unsupported prescription is the book's main historical failure mode, and this argument is the most prescription-adjacent material yet proposed for it.

---

## 4. Boundaries

These are not stylistic preferences. Each one has cost real rework on this project before.

- **Do not write in CT's voice from priors.** Read the existing manuscript in `src/lib/data/book/` first. That is the voice corpus. The v0.8.0 chapters are the most current reference.
- **Do not soften the moral claim into neutrality.** The argument is that the current arrangement is built on exploitation and that the alarm discourse is self-interested. Making it defensible means narrowing the evidence, not blunting the point.
- **Do not invent motive, positioning, or mission language CT did not write.** If a bridging sentence requires asserting something CT has not said, stop and ask instead.
- **Do not add a universal policy blueprint.** The same failure was corrected in v0.8.0 findings 5 and 11. Bounded examples and open questions only.
- **Do not name or characterize real living individuals** beyond what a cited source states.
- **Keep the nine stages as CT's model.** Place it against the literature, note where it agrees and diverges, but do not replace it with someone else's framework and present that as CT's.

---

## 5. Claims that need narrowing before they can be published

**C6 is the weak link.** "Absolutely NO ONE" is falsifiable and there are visible counterexamples. Test it honestly. Acemoglu and Johnson, `Power and Progress` (2023), argues almost exactly this thesis: that technological gains flow to whoever holds power, and that direction is a choice rather than a law. Related: Brynjolfsson and McAfee `The Second Machine Age`, Benanav `Automation and the Future of Work`, the basic income literature (Van Parijs, Standing, Widerquist), Altman `Moore's Law for Everything`.

If those hold up, the honest restatement is that floor-raising is absent from the mainstream *alarm* discourse and underweighted relative to displacement fear, not that nobody has said it. That version is stronger, because it is true and because it puts CT in identified company rather than alone.

**C8 is mislabeled.** What CT describes is not the hype cycle. The Gartner Hype Cycle is five phases about expectation, not power. CT's nine stages are much closer to Carlota Perez, `Technological Revolutions and Financial Capital` (2002), specifically the installation period, turning point, and deployment period, and to Rogers, `Diffusion of Innovations` (1962) for stage 9. Either correct the label or keep it knowingly with a footnote. Do not publish the misattribution silently.

**C3 and C4 need real anchors, not the illustrative figure.** "Less than $3 a day" needs a country, sector and year, or it should become a cited range. Verify against ILO Global Wage Report, Clean Clothes Campaign living wage research, Fair Wear Foundation country studies, and the Anker living wage methodology. For US agriculture: USDA National Agricultural Workers Survey for demographics, status and wages. The sourced figures may be more severe than the estimate, which would strengthen the passage.

**C1 needs a framework, not Maslow.** Maslow's hierarchy is weakly evidenced and easy to attack. Sen `Development as Freedom` and Nussbaum's central capabilities carry the same point with far better standing.

---

## 6. Counter-arguments to engage, not avoid

A version that does not survive these is not finished.

- **The Engels pause.** Real wages stagnated for roughly five decades into British industrialization while productivity climbed. This is the strongest available evidence for CT's "oppression will obviously come first," and also the strongest evidence that the floor does not rise on its own.
- **Gains required organizing and policy.** Historically the floor rose where labor organized and states legislated. That is a condition on "if we steer this right," and it names who does the steering.
- **Luddite scholarship supports CT, correctly read.** Luddites were not opposed to machines. They opposed machinery deployed to bypass labor standards. See Binfield `Writings of the Luddites`, Hobsbawm `The Machine Breakers`, Randall `Before the Luddites`. Stage 8 gets more accurate and more sympathetic with this correction.
- **A real floor-raising case exists.** The Green Revolution raised caloric floors at large scale, with contested distributional and ecological costs. It is the closest historical analogue to the claim being made and should be treated as evidence, including its failures.
- **Jevons and induced demand.** Efficiency gains often expand consumption rather than free capacity. Relevant to any claim that abundance follows capability.

---

## 7. Resolved and open questions for CT

### RESOLVED 2026-09-21: "the jabs" means "the haves"

CT confirmed the word is "haves," as in haves and have nots. The sentence reads:

> The haves will leverage this against their enemies. Always have.

This is no longer blocked. Three things follow.

1. **Keep the echo.** "The haves ... Always have." lands as deliberate wordplay. Preserve it
   rather than smoothing it out in the formal version. If a rewrite loses it, say so and show
   CT both options.
2. **The term now has a clean scholarly bridge.** Haves and have nots maps onto the
   distributional literature directly, which is where C1 wants to go anyway via Sen and
   Nussbaum. Use the bridge; do not replace CT's plain words with jargon in the prose itself.
3. **It sharpens C7, it does not soften it.** The claim is that incumbents weaponize new
   capability against opponents. Name which incumbents the evidence actually supports rather
   than leaving "the haves" to do unexamined work in a researched passage.

### RESOLVED 2026-10-08: Simeon is illustrative or composite

CT answered on 2026-10-08: Simeon is illustrative or composite, not a real named worker. CT
chose that combined answer and did not say which of the two, so do not narrow it further.

What follows from the rule already stated below: no consent or identity verification is
needed, and if the name is ever used in the book it must be labeled as an illustration. A
wage figure attached to him still needs an earnings source. As of v0.11.0 the name appears
nowhere in the book; chapter 7 makes the point with an unnamed garment worker and a cited
report. Whether Simeon returns is an open, optional choice for CT.

Not yet updated: the copies of `FLOOR-ARGUMENT-RESEARCH.md` and `FLOOR-ARGUMENT-PLACEMENT.md`
inside the STS edition folders still list this as open.

The original question, kept for the record:

The source reads: "Your clothes were made by Simeon working for less than $3 a day."

Establish with CT whether Simeon is a real named worker, a composite, or illustrative.
This changes what is publishable. A real person needs consent and verification. A composite
or illustration needs labeling as such, in line with the v0.8.0 rule that illustrative
quantities are labeled. Do not resolve this by guessing, and do not quietly drop the name to
avoid the question. Ask CT.

### Minor, correctable without asking

"But why happens afterwards?" is an obvious typo for "what happens afterwards?" Correct it in
the formal version. The verbatim block in section 1 stays as written.

## 8. Standing rules

- No commit, no merge, no publication, no site deploy. Same as v0.8.0.
- Original manuscript files stay intact. Work additively.
- Log artifacts to today's daily note with wikilinks as they land.
- Structural checks are not fact checks. Anything asserted here needs a source, not a green harness.

---

## Related

- [[Daily Notes/2026-09-21]]
- [[Hubs/2026-09-21_hub]]
- `active/sts-v0.8.0/docs/v0.8.0/CRITIQUE.md`
- `active/sts-v0.8.0/docs/v0.8.0/EDITION-NOTES.md`
