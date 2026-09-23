# Surviving the Singularity v0.9.0: edition notes

Assembled 2026-09-23 from every edition, per CT's brief: cross-reference them,
build the best book possible, restore the original cover. Method and constraints
are in [EDITORIAL-PLAN.md](EDITORIAL-PLAN.md). Branch `book-v0.9.0`, worktree
`active/sts-v0.9.0`. Nothing merged, pushed, deployed, or published.

## The result

| | v0.7.5.1 | v0.8.2 | **v0.9.0** |
|---|---:|---:|---:|
| Words (content files) | 93,702 | 58,360 | **84,483** |
| PDF pages (letter) | 293 | 175 | **254** |
| "doesn't establish/prove/guarantee" | 1 | 25 | **6** |
| "appropriate/qualified/assessed" | 3 | 28 | **8** |
| Contractions per 1k words | 12.4 | 16.4 | **23.7** |
| Author-ruled passages present (marker count) | 31 | 0 | **28** |
| Known factual errors from both reviews | ~25 | 0 | **0** (gated) |

PDF: `book-build/Surviving-the-Singularity-v0.9.0.pdf`, 254 pages, original
cover (`scripts/book-cover.png`) full-bleed on page 1. Build:
`python3 docs/v0.9.0/build.py`.

## What each edition contributed

- **v0.8.2 (base):** the food-first thesis, researched history in every
  precedent, the new scenes (Rosa, the delivery route, Devendra's layoff and
  arrival, Irene's written questions, the funding-through-June meeting), every
  factual correction, the discussion-brief Appendix A, British Restaurants, New
  Communities, Red Vienna.
- **v0.7.5.1 (voice and substance):** every author-ruled passage (ox and
  husbandry; "Not abolished. Optional."; the unprecedented machine and the
  precedented stampede; "the wise ones are learning how to solder"; the cyberdeck
  doctrine and Tiffany; The Proof Is Not Hypothetical; "fear wearing the costume
  of caution"; the Moral Mandate; the Adequate Level of Care), the original stage
  names, chapter titles for 7 and 13, the scenes' sensory lines, the
  seventeen-definitions lineage, the Letterhead and Egalitarian Pivot sections,
  the canned-music precedent, the cognitive firewall, deglobalization and the
  region ring, the storm on the ridge, the symptom index and blacklist, the
  cyberdeck appendix.
- **Food-first review (21 Sept):** governed what stayed out (below) and added the
  objections passage in Chapter 11, in the review's own wording.

## Kept out on purpose

From the food-first review: compost-tea recipe and causation, server-exposure
config and "skip patches" policy, structural dimensions and pier/beam
calculations, greywater plumbing, salvaged battery builds, deprivation as a
compliance tool, the municipal code as an operative template.

From the two error catalogues: the Napoleon troop superlative, "four thousand
acts", the Hitchcock quote, "doctors across Europe", 1915 horse peak, "forty
thousand pounds" and "eighty pounds", Universal Basic Computing, sub-millimeter
FarmBot, millions of joules per page, the 48-hour dopamine claim, the welded LAMB
statistic, Safe Street Rebels (plural), 365-degree cameras, the bad Mycodo URL
and port, 3 percent Haber-Bosch emissions, "decades" of lead-acid life, PETG from
bottles, Google's "synthetic neurons", the barter-can't-be-taxed line, Krugman and
Daily Mail quotes, "seventy-nine pages", the 72-hour starvation line, terminator
seeds, religious tax shields, and reader-directed lines ("Wake the fuck up",
"think about someone other than yourself", "you are failing", "capitalist
goblins"). A gate script fails the build on any of these; its negative control
was watched to fire.

## Checked for the first time in this edition

Danaylov's list (16 definitions + empty slot; Kelly's "five minutes" is
correct), the NYT 1903 editorial, NPS Victory Garden figures (18.5 million
gardeners, 40 percent of fresh vegetables, 1944), the Mycodo installer (old URL
404, documented URL 200), the Shumailov 2024 *Nature* paper, the Kipping 2020
paper, the USDA food-waste FAQ (moved URL), the 2026 Newsweek and TechCrunch
cyberdeck coverage, and every figure in The Proof Is Not Hypothetical against
the source transcripts. The Naval epigraph was checked and is not in his own
transcript, so it stays out.

## Decisions CT should confirm

1. **Chapter titles restored:** Chapter 7 "The Battle Lines: The Entitled vs.
   The Ready" (recast in the text as mindsets, not demographics), Chapter 13 "The
   Shouse Protocol", Appendix E "The Cyberdeck". Chapter 11 keeps the approved
   court title; Chapter 6 and the Conclusion keep v0.8.2's titles.
2. **Stage names** restored to match the book's own nine-stages figure.
3. **The Chapter 17 storm scene** is v0.7.5.1's climb, with Curtis added so
   nobody climbs alone. v0.8.2 had replaced it with a next-day visit.
4. **Chapter 15's trial** is now broadforking and cover crop, not compost tea,
   with the contaminated end staked off.
5. **Epigraphs:** restored four with honest attribution (Tsiolkovsky, Pasteur,
   Archimedes, Brand in its 1968 wording). Chapters 6, 8, 9, 13, 16, the
   Introduction and the Conclusion have none, because their earlier quotes could
   not be verified. New epigraphs are an author choice.
6. **Profanity:** five uses, all load-bearing ("asshole", "goddamn" twice,
   "fucking food first", "actual fucking labor").
7. **Figures edited:** two SVG labels changed to match corrected text
   (Chapter 10 "OUTRAGE / TRAGEDY" is now "A TRUE STORY"; Chapter 15 no longer
   promises "zero chemical fertilizers"), and the Chapter 8 lightning glyphs
   became zigzag arrows so WeasyPrint can render the figure.

## Verification

- `sts.py verify`: Clean (math, meta, refs, P-01..P-23).
- `sts.py id verify`: OK, 1,936 blocks. The committed index was regenerated with
  `sts.py id build`; the verify command checks a live index, so its pass alone
  did not cover the stored file.
- Gate script (`python3 docs/v0.9.0/gates.py .`): 0 failures
  on the manuscript, 13 on a deliberately broken copy.
- PDF: 30 sections, zero TeX or markdown in the extracted text, zero render
  errors; cover, title, contents, all equation pages, two diagram pages and the
  final page were rendered and inspected.
- New Works Cited URLs: 17 return 200; four refuse scripted requests and were
  confirmed another way.

## Not done

- **No complete fact-check.** Restored material was checked against both error
  catalogues and spot-checked; not every sentence was re-verified.
- **The 6x9 publication edition was not rebuilt.** `publication/` still typesets
  v0.8.2 with the replacement vector cover. Rebuilding it for v0.9.0 with the
  original cover is a separate job.
- **No website build or release.** `released` stays 0.7.5; README, RELEASES.md
  and the site's download links were not updated.
- **Image rights** are as inherited; the publication rights audit's caption
  corrections were not ported into source.
