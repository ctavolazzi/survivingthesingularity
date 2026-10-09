# v0.9.2: critique of the work so far, and the build plan

Written 2026-09-23 on branch `book-v0.9.2`, from v0.9.1 at `0f322b7`.

CT's brief for v0.9.2: the best possible version, with art, formatting that is
easy to skim but fun to read, factual backing for every claim, historical
analogues and usable data, and whatever else the book is missing.

Every number below was measured on the v0.9.1 text. The claim counts come from
`sts.py factcheck`, filtered to the non-fiction parts of each chapter: Elijah's
scenes and Chapter 0 are left out, because a character's line is not a factual
claim.

---

## Part A. Critique: what I got wrong or left undone

### Errors (things the book currently says that are wrong or misleading)

1. **Chapter 2's modern Stage 2 example is missing its ending.** On 12 June 2026,
   Commerce (BIS) required a license for Anthropic's two top models, and the book
   says so. It leaves out that the controls were lifted on 30 June after two weeks
   of negotiation. The paragraph also has no citation, in the text or in Appendix B.
   I carried it through v0.9.0 and v0.9.1 without checking it. The full story is
   the stronger example: panic, then the adults step in (Stages 2 and 3), inside
   three weeks. Its companion claim, a Chinese open-weight MIT-licensed model "in
   the same news cycle," is also unverified.
2. **The Kropotkin epigraph (Ch. 9) marks an omission that isn't there.** The first
   ellipsis stands where the original has only a dash. It should read "…over the
   country, so as to bring the factory amidst the fields … is surely…".
3. **The v0.9.1 edition notes overstate how much of the restored text is CT's.**
   They say every addition is CT's wording. I wrote these sentences myself:
   - "What you've lost is the old deal: sell your days or don't eat."
   - "Here's how I first pictured it, years before I had the words."
   - "It's a funny picture. Now ask what happens to everyone who was paid to be
     the smart one in the room."
   - "I'll tell you where I stand, because you'll find out anyway."
   - Most of the Chapter 6 paragraph ("my evidence is sitting on a desk…").
   - The closing turn of the horse parable.

   The substance is CT's, but the sentences are mine, in CT's voice. That is the
   pattern my mistakes ledger warns about (M-16, M-17). They must be listed
   honestly so CT can keep or cut each one.
4. **The book now seems to contradict itself.** Chapter 6 says "we're already
   inside the Singularity," and the Introduction forecasts AGI for Thanksgiving
   2027. The two are consistent under the book's own definition (the Singularity
   is intelligence ceasing to be scarce, not AGI), but no sentence says so. A
   careful reader will call it a contradiction.
5. **Two factual claims I added in v0.9.1 have no source:** that useful models
   run on consumer hardware, and the thesis line's framing. The first is true and
   easy to cite. The second needs to read as CT's view, not as reported fact.

### Gaps (things the book should have and doesn't)

6. **Factual backing.** 238 factual claims in the non-fiction sections have no
   source link in their own paragraph: 80 attributions, 65 dated events, 6
   statistics and 87 causal claims. Appendix B covers many of them by topic, but
   a reader can't tell which source backs which sentence. Five have no source
   anywhere:
   - the Commerce order
   - Cortical Labs' neurons (Ch. 1)
   - the Waymo incidents (Ch. 7)
   - the 1970 Census home-price ratio (Ch. 6)
   - Sam Altman's "universal basic compute" (Ch. 1)

   The v0.9.0 fact-check was a spot check plus a gate that only catches errors
   already known. The Works Cited links haven't been network-checked since v0.9.0
   (running now).
7. **Data.** The whole book has 11 statistics in 86,478 words and no data charts.
   A book arguing about food, work, housing and energy never says how many people
   are food insecure, how much food is wasted, how exposed jobs are, or what data
   centers draw.
8. **Skimmability.** 18 of 22 chapters open with "In this chapter" bullets, and
   that is the only navigation aid. There are no end-of-chapter takeaways, no data
   boxes, no glossary, no reading paths, no timeline and no discussion guide. The
   24 practice sections are spread through the book, with no one place that turns
   them into a plan.
9. **Art.** Part I is thin: Chapters 2, 3 and 4 have one image each (the chapter
   opener). So are Chapters 6, 12 and 16, and Appendices A to D have none. None of
   the art shows data.
10. **Formats.** There has been no EPUB since v0.7.x. The site still releases
    v0.7.5 (out of scope unless CT asks).
11. **Print readiness.** Menlo is embedded for diagram labels; its license needs
    checking or swapping for JetBrains Mono (OFL). The cover master is about 228
    dpi at 6x9. Four images with unclear rights still show on the website. No
    physical proof has been made.

### What held up

The voice restorations, the seven epigraphs (except the Kropotkin punctuation),
the caption corrections, the 6x9 pipeline and its proof are sound. The report's
history is supported by the primary sources committed under `docs/history/`.

---

## Part B. The plan

Seven waves, each committed and pushed when its acceptance check passes. Nothing
is claimed done until its check has been seen to fail on a planted defect and
pass on the real text (the rule from M-04 and M-21).

### Wave 0. The claim ledger (the backbone)

Build `docs/v0.9.2/claims.json`: one row per non-fiction factual claim, with its
block id, the source URL, the exact supporting passage as fetched, a verdict
(verified / corrected / softened to the author's view / cut), and the date
checked. Generate it from `sts.py factcheck` and fill it by hand.

Also: finish the Works Cited link check and repair dead links through archive.org.
Add every error fixed in v0.9.2 to the gate script so it can't come back.

**Accept when:** every row has a verdict, no factual claim is left without a
source or a clear "my view" or "illustrative" label, and the gate fires on a
planted copy of each fixed error.

### Wave 1. Fix the known errors

1. Chapter 2: verify the Commerce order against primary or legal-analysis sources
   and add the 30 June lifting, with citations. Check the open-weight model claim
   and cut it if unverified.
2. Chapter 9: correct the Kropotkin ellipsis.
3. One sentence reconciling "already inside the Singularity" with "AGI by
   Thanksgiving 2027", using the book's own definition.
4. Cite local models on consumer hardware. Mark the thesis line as CT's view.
5. Rewrite the v0.9.1 attribution record: list every sentence I wrote in CT's
   voice, carried forward into the v0.9.2 notes.

### Wave 2. Back every claim, chapter by chapter

In reading order, Introduction to Appendix E:
- **Statistics and dated events:** fetch the primary source, confirm the number or
  date, and add an inline citation in the book's style (a markdown link after the
  sentence). If the source disagrees, the text changes, not the source.
- **Attributions and quotes:** confirm the wording against the original or a
  facsimile citation. A quote that can't be confirmed becomes a paraphrase marked
  as such, or is cut.
- **Causal claims:** attach evidence, or rephrase as argument ("I think," "the
  pattern suggests"). The author may argue; the book may not pass an argument off
  as a finding.
- The five claims with no source anywhere come first.

**Accept when:** the Wave 0 ledger is fully resolved and a re-run of the filter
counts 0 unresolved claims.

### Wave 3. Data you can use

About 12 verified "By the numbers" boxes, one per Foundations section where the
argument rests on a quantity, 3 to 5 figures each, every figure linked.
Candidates, each to be verified before use:
- Ch. 6: job exposure to generative AI (ILO 2025)
- Intro and Ch. 11: US food insecurity (USDA ERS, latest year)
- Ch. 14: food loss and waste (USDA and ReFED)
- Ch. 6: home price to income, 1970 against today (Census)
- Ch. 5: data-center electricity (IEA)
- Ch. 12: farmland value and land-trust data
- Ch. 15: topsoil loss
- Ch. 1: model and compute costs over time (Epoch AI or Stanford AI Index)

Five or six data charts drawn as SVG in the book's house style, with sources
printed under each:
- horses and mules against tractors on US farms (P-07, USDA census)
- the home-price to income ratio
- food insecurity over time
- data-center electricity
- the price of a unit of AI capability over time
- the 23 precedents on one timeline

### Wave 4. Easy to skim, fun to read

Components, tested in both renderers (pandoc for the PDFs, marked plus DOMPurify
for the site) before rollout:
- **"In this chapter"** on every chapter. Four are missing it.
- **"By the numbers"** boxes (Wave 3).
- **"If you remember one thing"**: a single closing line per chapter, CT's
  strongest existing line where one exists, not new copy.
- **Print styling** for these components, with pull quotes held to about two per
  chapter.
- **"How to read this book"** in the front matter, with reading paths: 20 minutes
  (Preface, Intro, Appendix C), an evening (plus one chapter per part), and the
  whole book; plus entry points by reader (worker, parent, organizer, builder).

### Wave 5. What the book is missing (my additions)

- **Appendix F, Glossary.** About 60 terms, each pointing to the chapter that
  defines it: AGI, ASI, open weights, Adequate Level of Care, shouse, land trust,
  CSA, mesh, LoRa, cyberdeck and so on.
- **Appendix G, Your First Year.** The 24 weekly practices plus the chapter
  exercises, sequenced into a 12-month plan with a checkbox per step. This is the
  most usable page the book can have.
- **Appendix H, Timeline.** 1811 (the Luddites) to Thanksgiving 2027: every
  precedent, every dated AI milestone the book uses, and the nine stages marked
  on it.
- **Appendix I, Talk About It.** Discussion questions per part, for book clubs,
  co-ops and classrooms.
- **Further reading.** 12 to 15 annotated books drawn from Appendix B.
- **Objections, answered.** Appendix C gains a short FAQ built from Chapter 11's
  objections passage and the September objections memo.
- **EPUB**, rebuilt and validated.
- **Alt-text audit** of all figures, for accessibility.

Deliberately not planned: a back-of-book page index. The PDF pipeline can't make
a reliable one, and the glossary's chapter pointers do the job.

### Wave 6. Art

- New SVG figures in the existing house style for Part I (a stage close-up each
  for Chapters 2, 3 and 4), Chapter 6 (the gap between capability and access),
  Chapter 12 (the land-trust structure), Chapter 16 (how a record travels), and
  the new appendices (the timeline and the first-year calendar).
- Pixel-art plates via PixelLab only for scenes that lack one, kept to a handful,
  because they spend CT's credits.
- Every new image goes into the rights audit and the art catalog, with alt text.

### Wave 7. Build, proof, deliver

1. Run `sts.py verify`, `id build`, the gates (with the new negative controls)
   and the link check.
2. Build the letter PDF, the 6x9 reading edition, the grayscale print interior
   and the EPUB.
3. Run the publication proof (all text blocks recovered), the font scan (0
   fallback runs) and the visual proof: a contact sheet of every chapter opener,
   every new component and every new chart.
4. Write the edition notes, add a v0.9.2 section to the report, and push.

### Order and checkpoints

Waves 0 → 1 → 2 are sequential; they are the backbone and the riskiest work.
Waves 3, 4 and 6 build on verified facts, so they come after Wave 2. Wave 5 can
run alongside Wave 3. I commit per wave and per chapter inside Wave 2.

### Decisions I will make without asking

Component syntax, which datasets to use, chart designs, glossary terms, the
first-year sequence, and whether a claim is cited, softened or cut. All of them
are recorded in the ledger and the notes, so CT can reverse any one.

### Needs CT

- PixelLab credits: about 6 to 10 plates. Say if that's too many.
- Which of the sentences I wrote in CT's voice (item 3) stay.
- The four unclear-rights images on the website.
