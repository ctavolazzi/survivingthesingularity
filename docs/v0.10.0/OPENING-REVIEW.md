# Opening manuscript review: v0.10.0

Reviewed on September 27, 2026, against the v0.9.2 canonical manuscript at
`3d29215`. This pass read all sixteen assigned files in full, approximately
43,016 words including Markdown and URLs before editing. It addressed concrete
accuracy, continuity, and reader-guidance defects while preserving the approved
food-first argument, the Thanksgiving 2027 forecast and its test, the three
registers, the Precedent Ledger, and the Elijah arc.

The governing references were `CLAUDE.md`, the root and canonical-source
READMEs, `VOICE-GUIDE.md`, `ELIJAH-PROTOCOL.md`, and the v0.9.2 plan and edition
notes. Earlier evidence reviews and chapter reviews informed the pass; earlier
recommendations did not override later author decisions. No new first-person
mission or motive was supplied.

## Coverage and decisions

All manuscript paths below are relative to `src/lib/data/book/`. Line numbers
refer to the source at the end of this review.

| File | Review outcome |
| --- | --- |
| `02-introduction.md` | Retained the approved position and practical sequence. Corrected the ox analogy at lines 35-43: animal traction requires training, feeding, guidance, and care. Removed the claim that autonomous work happened only twice in history. Kept “The second ox” as a metaphor and updated its caption. |
| `01-preface.md` | Preserved the invitation and author register. At line 21, narrowed the claim about weapons ending all life to devastation of civilization. |
| `31-how-to-use.md` | Replaced unsupported reading-time promises with route names. The baseline short route totaled about 8,505 source words, not a credible twenty-minute promise. “Condensed version” replaces a format-dependent one-page claim. The glossary covers key terms, and the year sequence refers specifically to Ledger practices. |
| `00-chapter0.md` | Preserved the demonstration and layoff scene. At line 48, separated parallel Transformer training from sequential generation. |
| `03-chapter1.md` | Retained the definitions, forecast, falsification test, and comparison table. Corrected the same Transformer mechanism at line 141. Checked the original paper's table against the retained base/big sizes and translation scores. |
| `04-chapter2.md` | Preserved stages as scenarios. At lines 91-93, distinguished the Fable safeguard report and global July 1 return from limited Mythos access. At line 101, separated a lost internet connection from electrical failure: a mesh link cannot power medical equipment. Added the FDA's outage-planning reference. |
| `05-chapter3.md` | Read in full; no change needed. Speculation, the implementation gap, and the right to refuse treatment remain explicit. |
| `06-chapter4.md` | Retained the speculative register. At lines 93-95, made equal weighting and priors explicit in the simulation model. Kipping's result is conditional, not an observed probability that our world is simulated. |
| `07-chapter5.md` | Corrected the second-law explanation at line 61 and an electric-pump example. Updated data-center electricity estimates to the IEA's 2026 report: approximately 485 TWh in 2025 and a forecast of 950 TWh in 2030. Corrected human “cell walls” to tissue. Removed the stove alt text's cast-iron claim because the scene identifies a plate-steel Fisher stove. |
| `08-chapter6.md` | Clarified the housing table's different measures: 1970 median value versus 2024 median sale price. Clarified that the USDA's 7.3 million children in food-insecure households category is not equivalent to every child eating less. Preserved the root agent's original-motif image replacement. |
| `09-chapter7.md` | Preserved the historical and political argument. At lines 166 and 237, distinguished Sousa's band's recording career from Sousa personally conducting studio sessions. |
| `10-chapter8.md` | Corrected unsupported neurological mechanisms, the fixed mental-energy allowance, and the universal twenty-minute recovery claim. Explained what the interruption studies measured. Kept Shannon's equation while separating information uncertainty from compulsion and fatigue. Qualified the proposed routines, cooperative savings, mesh resilience, and Dunbar estimate. Updated all four associated SVG/caption pairs. |
| `11-chapter9.md` | Preserved the gardening, nitrogen, and regional-production limits. Corrected a sentence-capitalization error and linked the Mycodo installer's current official requirements at line 141. |
| `part1-divider.md` | Read in full; consistent with the opening chapters, no change. |
| `part2-divider.md` | Corrected Denny's portrait alt text at line 7 from network engineer to former logistics worker, matching the narrative and character protocol. |
| `part3-divider.md` | Read in full; consistent with the current narrative arc and the manual's purpose, no change. |

The main continuity check concerned who has which practical expertise, what the
co-op has actually built, and whether food access remains unconditional. The
manuscript's repeated food-first commitment is deliberate argument structure,
not an accidental refrain to remove. No narrative scene was expanded and no
new event was introduced.

## Primary evidence used for corrections

These sources were inspected for the specific corrections, not treated as
blanket support for every adjacent claim. New bibliography entries were passed
to the root agent for Appendix B integration.

| Source | Use |
| --- | --- |
| [FAO, Draught animal power and implements](https://www.fao.org/family-farming/detail/en/c/1619223/) | Animal traction's training, care, and human labor requirements. |
| [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762), especially sections 1 and 3 and Table 2 | Training parallelism, autoregressive decoding, and retained benchmark data. |
| [Anthropic, Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5), June 30, updated July 1, 2026 | Model-access chronology and the distinction between Fable and Mythos. The company's characterization of its safeguards remains attributed. |
| [FDA, Medical Devices and Natural Disasters](https://www.fda.gov/medical-devices/emergency-situations-medical-devices/fda-offers-tips-about-medical-devices-and-natural-disasters) | Planning for interruption of power to medical equipment with the relevant providers. |
| [Kipping, A Bayesian Approach to the Simulation Argument](https://arxiv.org/abs/2008.12254) | Conditional model result. The author preprint was available; direct retrieval of the existing MDPI link failed. |
| [OpenStax, Statements of the Second Law of Thermodynamics](https://openstax.org/books/university-physics-volume-2/pages/4-4-statements-of-the-second-law-of-thermodynamics) | Heat-engine limitation applies to operation in a complete cycle. |
| [IEA, Key Questions on Energy and AI, executive summary](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) | Updated 2025 electricity estimate and 2030 forecast, kept distinct. |
| [USDA ERS, Key Statistics and Graphics](https://www.ers.usda.gov/topics/food-nutrition-assistance/food-security-in-the-us/key-statistics-graphics) | Meaning of the 2024 household and child food-insecurity categories. |
| [Library of Congress, Good Times Are Here: New to the National Jukebox](https://blogs.loc.gov/now-see-hear/2022/10/good-times-are-here-new-to-the-national-jukebox/) | Sousa's band frequently recorded under other conductors; Sousa rarely entered the studio. |
| [Raichle and Gusnard, Appraising the Brain's Energy Budget](https://pmc.ncbi.nlm.nih.gov/articles/124895/) | Ongoing brain activity consumes substantial energy; the rough twenty-percent figure is not an allowance of decisions. Direct retrieval encountered a challenge page; indexed primary-source text supplied the relevant passage. |
| [Mark, Gonzalez, and Harris, No Task Left Behind?](https://www.ics.uci.edu/~gmark/CHI2005.pdf) | Observed elapsed return time included other work; it did not measure neurological recovery. |
| [Mark, Gudith, and Klocke, The Cost of Interrupted Work](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) | Faster completion with higher reported stress, frustration, effort, and time pressure in that experiment. |
| [Mycodo official installation instructions](https://github.com/kizniche/Mycodo#install-mycodo) | The printed command matches the project's documented installer; current platform requirements remain linked rather than assumed timeless. |

## Figure verification and boundaries

Edited canonical SVGs:

- `static/book-images/ch08-cognitive-extraction.svg`: observable diversion of time replaces unsupported prefrontal depletion, dopamine, and suggestibility mechanisms.
- `static/book-images/ch08-focus-recovery.svg`: conceptual curve, unmeasured axes, no fixed recovery duration or interruptions-per-hour threshold.
- `static/book-images/ch08-firewall-pipeline.svg`: proposed routine, no measured entropy or agency effect.
- `static/book-images/ch08-star-vs-mesh.svg`: alternate working paths are a condition for rerouting; Dunbar's estimate is not a hard group-size rule.

Parsed the SVGs and ran the repository's browser-based collision detector. A
negative control deliberately placed a label over the focus-chart title; the
detector reported the overlap. An initial real-label collision in that chart
was corrected. Final source checks had no unexpected collisions. The topology
figure retains the detector's pre-existing allowed crossing of “HUB” by the
intentional failure X. All four source renderings were visually inspected.
Review screenshots are in `book-build/v0.10.0-opening-review/`.

`git diff --check` passed after the source edits. Source SVG checks do not prove
physical print legibility. The root agent owns regenerated print derivatives,
art-catalog synchronization, final layout proofing, cross-book references, and
the release gates. Source readiness was reported after the fourth SVG changed.

This was an editorial and targeted evidence pass, not an independent audit of
every historical assertion or quotation. Existing source reviews remain part
of the evidence record. No installer was executed, no greenhouse hardware was
tested, and no medical, electrical, structural, or legal design was certified.
The original narrative register and speculative premises remain deliberate.
