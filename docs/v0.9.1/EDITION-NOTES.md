# Surviving the Singularity v0.9.1: edition notes

Built 2026-09-23 on branch `book-v0.9.1` (worktree `active/sts-v0.9.1`), from
v0.9.0. The brief: use every earlier version and the version-history report to
make the next edition, and make the editorial calls instead of handing them
back. Nothing merged, deployed or published; `released` stays 0.7.5.

The version-history report behind these choices is the doc "How the Book
Changed". Its primary sources are committed under `docs/history/google-docs/`.

## What changed from v0.9.0

| | v0.9.0 | v0.9.1 |
|---|---:|---:|
| Words (manuscript index) | 84,483 | 86,478 |
| Letter PDF pages | 254 | 256 |
| Chapters without an epigraph | 7 | 0 |
| Third-party captions matching the rights audit | 12 of 18 | 18 of 18 |
| 6x9 print edition | v0.8.2, vector cover | v0.9.1, original cover |

### 1. CT's own words, restored

Every addition is CT's wording from a dated source, lightly fitted to its new
place. Nothing here is invented positioning; where a line is new connective
tissue, it is listed so CT can cut it.

- **Preface opener.** "So the robots have taken over. Congratulations! You've
  lost." (First Draft, 11 Apr 2024; kept through v0.7.5.1, softened to
  "Congratulations, apparently" in v0.8.x.) The next line adapts CT's June 2026
  back-cover turn: what you've lost is the old deal, and losing it is the opening.
- **Preface: the horse parable** (Author's Foreword, May 2024): the flying-car
  horses, "They just want hay," "nobody owns a Mustang." *New connective text:*
  the closing paragraph turns it toward food first ("We can figure out how to get
  everybody their hay").
- **Introduction** (Thesis, 16 Jun 2026): "This one is intellectual. We have
  automated thought itself," and CT's two worries: missing the window, and what
  bad actors and sociopaths will do with it. Also "The shovel never dug its own
  hole" (First Draft).
- **Introduction, money.** CT's view that we must move away from money as a
  system of control, stated as CT's, beside the book's paid-for food baseline.
  The tension is named rather than resolved.
- **Chapter 1: Einstein as everyone's tech support** (First Draft), placed under
  the working definition, where it illustrates intelligence stopping being scarce.
- **Chapter 6** answers its own title in CT's voice: yes, already inside it; the
  evidence is useful models on consumer hardware; what happens next isn't done.

Considered and left out:
- "Capitalism fights to the last breath and takes a lot of people with it. We are
  entering that period now." Reads as defeatist against the v0.6.0 ruling
  ("confront defeatism, not the reader").
- The medical disclosure in StS-Redux. Personal; only CT should put it in.
- The Millers family and the 2024 joke chapter titles. Elijah replaced the first;
  the second belongs to a different book.
- Johnny Autoseed. Cut by CT in v0.7.1.

### 2. Seven epigraphs, each checked word for word

| Section | Epigraph | Checked against |
|---|---|---|
| Introduction | Upton Sinclair, *I, Candidate for Governor* (1935) | Quote Investigator facsimile citation |
| Ch. 6 | Arthur C. Clarke, *Profiles of the Future* (1962) | Quote Investigator |
| Ch. 8 | Charles Mackay, *Memoirs of Extraordinary Popular Delusions*, Preface | Gutenberg 24518 (1852 edition) |
| Ch. 9 | Peter Kropotkin, *Fields, Factories and Workshops* (1913), ch. VII | Gutenberg 64353 |
| Ch. 13 | Henry David Thoreau, *Walden* (1854), "Economy" | Gutenberg 205 |
| Ch. 16 | A. J. Liebling, *The New Yorker*, 14 May 1960 | Quote Investigator |
| Conclusion | Oscar Wilde, *The Soul of Man under Socialism* (1891) | Gutenberg 1017 |

Appendix B's epigraph section lists each source.

### 3. Image rights and captions

- Six captions now carry the audited credits: the Hubble Ultra-Deep Field is CC
  BY 4.0 with its full credit (it said "Public domain"), the solar-barn
  photographer is Reinhold Möller, and two photos are correctly identified
  (Thinktank's Jaguar exhibit; a bar in a Haifa mall).
- The rights audit now covers the 38 images v0.9.0 restored.
- Four third-party images with an unclear commercial basis (Edmond de Belamy,
  the NYSE floor, two FarmBot photos) stay in the web source. The print edition
  swaps them for line drawings. **CT decides** whether the web keeps them.

### 4. The 6x9 print edition

`publication/` now typesets v0.9.1 with the original cover full bleed. Outputs
(not committed) are in `publication/output/`. The cover master is 1410 x 2056
pixels, about 228 dpi at 6 x 9 inches, and slightly wider than 6:9. The crop is anchored left, so
the title lettering keeps its margin and about 3 percent of the tree on the right is trimmed. A printer
may ask for a larger master. The reading edition is 318 pages (cover plus 317).

## Verification

- `sts.py verify`: Clean. `sts.py id build` then `id verify`: 1,954 blocks.
- Gates: the two known *Northanger Abbey* "Chapter 25" false positives only. The
  negative control (injected "manifesto", "Wake the fuck up", the Napoleon
  superlative, Universal Basic Computing) fired on all four.
- Letter PDF (rebuilt after the SVG fix): 256 pages, 0 TeX or markdown leaks, every new passage found in the
  extracted text, and ten pages rendered and inspected (cover, Introduction,
  Preface, five epigraph pages).
- 6x9: `publication/build.py` passed its manuscript-hash and image-rights asserts;
  `publication/proof.py` recovered all 2,104 source text blocks from the 317-page
  interior, across 30 sections, with no text outside the page, no broken links and
  no missing assets. The only exceptions are five captions whose images the print
  edition replaces with line drawings. Its negative controls include a new one:
  cut the middle third of a paragraph and the proof must report it missing.
- Found and fixed while proofing: (1) the audited credit printed twice under three
  photos, because pandoc wraps captions and the credit swap missed the wrapped
  ones; the rendered interior now has no duplicated credit. (2) The first
  full-font build crashed on a subscript p in `ch11-cooling-loop.svg`; every used
  SVG was rendered alone to find it. (3) Paragraphs interrupted by a diagram at a
  page break read as missing; the proof now recovers them, and the new negative
  control keeps it honest. (4) Ghostscript's grayscale pass reported that Songti SC
  "cannot be embedded because of licensing restrictions" and dropped a glyph. A
  per-text-run font scan traced it to U+2223 (from \mid in two formulas) and traced
  two more system fallbacks to the Ch. 9 nitrogenase equation. The formulas now use
  | and <sup>/<sub>. The rebuilt interior has 0 text runs outside the book fonts
  and Menlo, and the grayscale pass prints no warnings.
- The rendered cover was inspected after the crop was anchored left.

## Not done

- No complete fact-check of restored material beyond the gates and spot checks.
- The four unclear-rights images remain in the web source (above).
- Site release, README, RELEASES.md and download links untouched.
- Printer readiness: the only fonts embedded are the book's own (Source Serif 4 and
  Source Sans, OFL) and Menlo for diagram labels, the same as v0.8.2. Check Menlo's
  embedding terms with the printer, or swap the diagrams to JetBrains Mono (OFL).
  No physical proof has been made.
