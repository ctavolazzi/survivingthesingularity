# Surviving the Singularity v0.9.2: edition notes

Built 2026-09-23 and 24 on branch `book-v0.9.2` (worktree `active/sts-v0.9.2`),
from v0.9.1. The brief, from CT: the best possible version, with art,
formatting that's easy to skim and fun to read, factual backing for every
claim, historical analogues and usable data, plus whatever else was missing.
Mid-build, CT added a ruling that became this edition's center: the book must
say plainly that **we don't have to live like this**, that money should be
optional, and it must propose a literal step-by-step plan.

After the first build CT asked for recommendations on content, language and
design, then said "Do it." That revision pass is section 7. The plan and the
critique that preceded the work are in [PLAN.md](PLAN.md).
Every citation and correction made through `cite.py` is logged, one per line,
in [claims-ledger.jsonl](claims-ledger.jsonl) (75 entries).

## What changed from v0.9.1

| | v0.9.1 | v0.9.2 |
|---|---:|---:|
| Words (manuscript index) | 86,478 | 97,840 |
| Sections | 30 | 35 |
| Inline source links in the text | 236 | 353 |
| Images | 73 | 79 |
| Data charts | 0 | 3 |
| "By the numbers" boxes | 0 | 4 |
| Precedents | 23 | 24 |
| Diagrams with a light print version | 0 | 32 |

### 1. CT's ruling: "We don't have to live like this"

- **Introduction, new section.** CT's own sentences from the 24 September
  message, with every factual claim sourced: the UN (enough food for
  everyone), CDFA (30 to 40 percent wasted), CFPB (credit and risk scores in
  rental decisions), Zuboff, NLIHC/PNAS (3.6 million eviction filings a
  year), California Courts (the sheriff's lockout), Oxfam 2017 and 2026, and
  the USDA food-insecurity chart. It replaces the v0.9.1 paragraph I had
  written in CT's voice from the Thesis.
- **Chapter 19, "The Ladder: How Money Becomes Optional" (new).** The conversion
  plan: nine rungs, from counting wasted food to keeping the market above the
  floor. Rungs 1 to 7 each cite a place that already did it (SB 1383, France
  2016, California universal school meals, land trusts, rural electric
  co-ops, NYC right to counsel, the NHS and Universal Basic Services). It also
  covers honest obstacles and actions by role, and has a ladder figure.
- **P-23 (new): the NHS, 1942 to 1948.** The Conclusion's precedent becomes
  P-24, so serials still run in reading order. `sts.py` and the gates now
  expect 24.

**Where the book says something different from CT's message, and why:**

- "The state of CA says we throw away half the food": California's agencies
  say 30 to 40 percent (CDFA) and 5 to 6 million tons a year. The book uses
  the state's real numbers, so a skeptic can't dismiss the rest.
- "8 ultra wealthy guys want to control everyone else": intent can't be
  sourced. The book states what can be: eight men owned as much as half the
  world (Oxfam 2017), billionaires are 4,000 times more likely to hold office
  (Oxfam 2026), and "the people at the top of that pile have every reason to
  keep the rules exactly as they are."
- "A man with a gun": rendered in California's own court language (the
  sheriff's notice and lockout), with the national eviction count.
- Profanity: the Introduction keeps one of CT's lines ("What the fuck is the
  point of having a society at all..."), and the facts carry the rest of the
  anger there. The revision pass added CT's own words in Chapters 13 and 19
  (section 7), from his 24 September message and the StS-Redux draft. Two
  older curses can't be traced to CT: "why not make them grow our fucking
  food first?" (Introduction, first seen in the v0.8.0 edit) and "actual
  fucking labor" (Chapter 12, first seen in v0.9.0). Neither appears in any
  of CT's drafts in `docs/history/`. They're listed below with the other
  sentences written in his voice.

### 2. Factual backing (Wave 2)

- 238 factual claims in the non-fiction sections had no source link in their
  own paragraph. Each was reviewed by hand. The real factual claims got inline
  citations from sources opened this session; the rest were confirmed as
  opinion, fiction, labeled illustration, or practice steps.
- **Errors found and fixed while checking:**
  - The June 2026 export-control story was missing its ending (lifted
    June 30), carried an unverified "same day" and an unsupported quote.
  - Thornton wrote about a calculator; he didn't review one.
  - Cortical Labs' neurons were human *or* mouse, not a mixed dish; the
    "sliver of the power" claim had no support.
  - The energy-efficiency table didn't match any source.
  - The Kropotkin epigraph marked an omission that wasn't there.
  - "Tens of thousands" of theater musicians was about 22,000.
  - The farmland paragraph asserted buyers' motives.
  - One Appendix B entry was circular ("as cited in the chapter").
  - Two citations had landed mid-sentence, reversing a sentence's meaning.
- Checked against primary text, not memory: the 1930 AFM ad's "2,000,000"
  (archive.org OCR), USDA SB-83 table 14 (page image), Census 1970 home values
  and household income, RIAA's 2016 streaming majority, the York executions.

### 3. Data you can use (Wave 3)

- Charts: food insecurity 2001 to 2024 (USDA ERS), horses and mules against
  tractors 1910 to 1949 (USDA SB-83), the Ledger on one page. All three are
  generated by `docs/v0.9.2/charts.py` from committed CSVs, with a color pair
  validated on the dark surface.
- Boxes: energy (Ch. 5), work, home and dinner (Ch. 6), land (Ch. 12), food
  (Ch. 14). One HTML wrapper, tested in pandoc and the site's marked.

### 4. Easier to skim (Wave 4)

- "In this chapter" for the Introduction and Conclusion.
- Reading paths (twenty minutes, an evening, the whole book) and a
  start-here table by reader.

### 5. What was missing (Wave 5)

- Appendix F, Glossary (50 terms, each pointing to its chapter).
- Appendix G, Your First Year: all 72 practices sequenced into twelve months.
- Appendix H, Talk About It: discussion questions and twelve further
  readings, nine free online.
- Appendix C: the plan in nine lines and seven objections answered.
- EPUB, rebuilt for the first time since v0.7.x.

### 6. Art (Wave 6)

New: `ch02-eighteen-days.svg` and `ch06-capability-access.svg`, plus the three
charts and the Chapter 19 ladder. All are rendered in headless Chrome and
inspected, and all are registered in the rights audit. No PixelLab plates
were made, to save CT's credits. Section 7 covers the print versions and the
fixes to older diagrams.

### 7. Revision pass (24 September, after the first build)

Six waves, each committed on its own. Decisions that were CT's to make are
marked **(CT's call, made reversibly)**; each is a small edit to undo.

- **Subtitle: "We Don't Have to Live Like This"** (CT's line). The site
  description and the cover modal carry it too; `sts.py verify` caught the
  drift and now reports one subtitle. **(CT's call, made reversibly)**
- **Chapter 19 renamed "The Ladder: How Money Becomes Optional"**, so the
  subtitle phrase isn't used three times. **(CT's call, made reversibly)**
- **How to Use This Book** (new page after the Preface): reading paths and a
  start-here table, moved out of the Introduction.
- **Chapter 3 gets a signpost, not a merge with Chapter 4:** it's the most
  speculative stretch, and practical readers can skip to Chapter 5 without
  losing anything later chapters depend on. **(CT's call, made reversibly)**
- **Introduction and Preface keep their order.** **(CT's call, made reversibly)**
- **Chapter 1:** a paragraph for readers after November 25, 2027.
- **Chapter 18's middle in plain speech.** Bureaucratic vocabulary fell from
  8.2 to 2.4 per 1,000 words and contractions rose from 21 to 31 per 1,000
  (CT's own range is 24 to 47). The section is 24 percent shorter with every
  point kept.
- **Chapter 19's scene** (864 words, per ELIJAH-PROTOCOL): the public meeting
  Chapter 18 set up. Irene uses her father-in-law's 1939 electric co-op
  against "we can't afford it," which is Rung 5 used as a weapon rather than
  a lecture. It's a partial win: funded through December, with a permanent
  line sent to study.
- **Chapter 19, "Why I wrote this chapter":** CT in the first person, built
  only from his own 24 September lines not already used in the
  Introduction, including two of his curses. The anger is aimed at the
  arrangement, "not at you." CT's February 2026 mission line from the Redux
  is also in the chapter.
- **Chapter 13:** the shouse in CT's own words from StS-Redux ("What the
  fuck is a shouse?"). **Chapter 12:** CT's June 2026 thesis note frames
  Chapters 12 and 19. Twenty-six contractions in the argument sections of
  Chapters 9, 12, 13, 15, 17 and the Conclusion.
- **Left out of the Redux on purpose:** the "imaginary line" land passage
  (it contradicts the lawful plan), "clout for consent", and the medical
  disclosure, which stays out unless CT decides otherwise.
- **Primary sources replace Wikipedia** for Sony v. Universal (the Supreme
  Court opinion at Cornell LII) and Borders (Slate, July 2011). The Stoll
  citation stays on Wikipedia: his 2010 comment no longer appears on Boing
  Boing's served page, and nothing is cited for text that can't be seen.
- **Figures for print.** In the 6x9 grayscale edition the dark diagrams
  printed as solid black blocks. Their labels came out at about 4 point,
  because figures were capped at 2.05 to 2.65 inches tall.
  `print_figures.py` now makes a paper-palette copy of all 32 diagrams. It
  maps text and shapes separately, removes the dark card and crops to the
  content. It enlarges labels up to 1.4x only where Chrome measures no new
  collision with another label, a box edge, a line or the frame; a forced
  enlargement is its negative control. The 6x9 gives diagrams the full text
  width, and the letter PDF allows them 19 cm. The website keeps the dark
  originals. Both builds refuse a print copy whose source changed after it
  was made.
- **Older diagrams fixed at the source.** An audit of the originals found 31
  defects in 16 figures: labels spilling past their boxes, labels sitting on
  arrows and curves, and labels overlapping. All are fixed, so the website
  improves too. The audit now reports zero, with four intentional cases
  allowed and explained. Reinjected defects are caught. The Chapter 19
  ladder's held rungs are dashed as well as blue, so its legend works
  without color.
- **Diagram font: JetBrains Mono** (SIL OFL 1.1, release 2.304, with
  license and provenance in `publication/assets/fonts/`). The diagrams
  already named it first, and print had been falling back to Apple's Menlo.
  The two glyphs JetBrains Mono lacks were removed: the lightning marks in
  Chapter 8 are now drawn, and Chapter 11's formula line reads "heat per
  second = flow × Cp × ΔT". WeasyPrint's SVG renderer can't place combining
  dots, so Q̇ and ṁ printed with dotted-circle placeholders. They still
  appear in the body text, which shapes them correctly.
- **Build tooling:** `proof.py` and `package.py` read the section count
  instead of assuming 30. The EPUB review PDF has its own filename.
  `fonts_check.py` lists fonts inside SVG XObjects, which the old scan
  couldn't see; that's how the Menlo fallback was found.

## Sentences I wrote in CT's voice (for CT to keep or cut)

Carried forward from v0.9.1:
- "What you've lost is the old deal: sell your days or don't eat."
- "Here's how I first pictured it, years before I had the words."
- "It's a funny picture. Now ask what happens to everyone who was paid to be
  the smart one in the room."
- Most of the Chapter 6 "already inside" paragraph, and the closing turn of
  the horse parable.
- Introduction: "If these things are going to take all our jobs, why not
  make them grow our fucking food first?" (arrived with the v0.8.0 edit; not in CT's
  drafts).
- Chapter 12: "share not only food and tools but labor, actual fucking
  labor, with the people who need it most" (written for v0.9.0).

New in v0.9.2:
- Chapter 6: the sentence separating "already inside the Singularity" from
  the 2027 AGI date.
- The Introduction's "In this chapter" bullets, reading paths and start-here
  table.
- All of Chapter 19 except the facts and Bevan's words. It's in the book's
  field-manual register, built on CT's ruling, but the wording is mine.
- Chapter 19's Elijah scene (fiction, in the book's narrative voice) and the
  plain-speech rewrite of Chapter 18's middle.
- The joins in Chapter 19's "Why I wrote this chapter": the sentences are
  CT's, but the order and the one-line transitions are mine.
- The connective lines in the "We don't have to live like this" section:
  "That's what it means when survival costs money," "Greed isn't a law of
  physics. It's a set of choices, written down and enforced," "That's the
  whole book. Everything else is how."

## Verification

Final run, 24 September, after the revision pass. Each step was logged to
its own file with its own exit code, never through a pipe.

- `sts.py verify`: Clean, all 24 precedents present and indexed. `sts.py id
  verify`: 2,212 blocks across 35 sections, 97,840 words.
- Gates (`docs/v0.9.2/gates.py`): 0 failures. The negative control fired on
  every newly catalogued error.
- Figures: `print_figures.py --audit` reports 0 problems in the 32 original
  diagrams, with 4 intentional cases allowed. Three old defects put back
  into memory copies were all caught. `--check` forced labels to 1.8x and
  saw collisions. The builds refused a deliberately stale print copy.
- Letter PDF: 287 pages, original cover. It embeds JetBrains Mono for the
  diagrams and system Georgia and Helvetica for the text; this is the
  author-review copy. One bold arrow on page 124 falls back to Times New
  Roman Bold because Georgia Bold lacks the glyph.
- 6x9: the build passed its manuscript-hash and rights asserts against the
  refreshed 35-section baseline. The proof found all 2,459 text blocks in
  the 363-page interior across all 35 sections, with no overflow, broken
  links or missing assets. `fonts_check.py`, which went red on the previous
  build's Menlo, finds only BookSans, BookSerif and JetBrains Mono. Pages
  90 and 185 were rendered in grayscale and inspected: the diagrams now
  print on white at the full text width.
- Grayscale print interior: 364 pages, blank final verso added, no
  Ghostscript warnings. Ghostscript relabels the six CFF-based book faces
  as "Anonymous" on conversion. The face count (6 plus 2 JetBrains Mono)
  matches the color interior, and the text extracts normally.
- EPUB: 38 XHTML files, zip integrity OK. It keeps the dark diagrams, as the
  website does.

## Not done

- No physical print proof; the cover master is still about 228 dpi at 6x9.
- Some diagram labels couldn't grow without a collision and stay at their
  original size (10 to 11 user units, about 4 point in the 6x9). Per-figure
  numbers are in `print-figures.json`. Five figures have a label that
  stayed at 11 units or less: the Chapter 9 region ring, the Chapter 11
  cooling loop, the Chapter 17 fab lab and mesh node, and the
  Introduction's food-insecurity chart. Larger type there means redrawing
  those figures.
- The four unclear-rights images still show on the website.
- Site release, README and download links untouched; `released` stays 0.7.5.
- The speculative stages (Chapters 3 and 4) are argument by design and carry
  few sources; the chapters label them as scenario and speculation.
