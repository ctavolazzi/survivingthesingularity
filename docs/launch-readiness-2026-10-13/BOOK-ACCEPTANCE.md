# Book and buyer acceptance, 13 October 2026

This review opened the actual public PDF and EPUB and the private research ZIP,
then checked them as reading products. It goes beyond archive hashes and the
website build. It does not establish live purchase or inbox delivery.

## Fixed during acceptance

- The shipped EPUB passed EPUBCheck but still let wide tables and enlarged
  headings extend beyond a phone-sized reading column. The CSS now wraps prose
  and contains wide tables in a horizontally scrollable area with readable
  column widths. An initial fixed-column approach was rejected after visual
  inspection because enlarged text broke words into narrow fragments.
- The ZIP previously offered its instructions only as Markdown, without clear
  phone extraction or ebook-import steps. It now includes a self-contained
  `START-HERE.html`, matching text instructions, working links to the included
  books, PDF/EPUB choices, Kindle delivery guidance, and access recovery steps.
- A repeatable EPUB reflow check now reads the actual distributed artifact in
  Chromium, Firefox or WebKit. EPUB-only regeneration preserves the reviewed
  PDF only when its master, source, artwork and layout receipts still match.

All 35 canonical sections are unchanged. Within the EPUB, every member except
the stylesheet and the metadata modification timestamp is byte-identical to
the previous candidate, including prose, captions, navigation and artwork.
The distributed PDF remains byte-identical.

## Checks and practical limits

| Check | Result |
| --- | --- |
| W3C EPUBCheck 5.4.0, actual distributed EPUB | No fatal errors, errors, warnings or informational findings |
| EPUB title, author, language, spine and contents | Present; all 35 sections linked in order |
| EPUB inline book images | All 110 have nonempty alternative text; no missing resources in the tested renders |
| Browser reflow | All 420 combinations pass: 35 chapters × 2 widths (320/768 px) × 2 text sizes (18/28 px), in Chromium, Firefox and WebKit; 71 contained-table pan checks pass |
| Old EPUB negative control | The same Chromium probe catches the original 13 overflow cases |
| PDF | 416 pages, selectable text and chapter bookmarks; source and link preservation guards retained |
| Research PDF | 16 pages; all 227 checked source blocks remain; deleted-paragraph control detects loss |
| Buyer guide | 12 archive-relative links resolve; four phone/desktop widths fit; no scripts, external assets or network requests |
| Research CSV | 396 data rows; all rows have 13 columns; no cells begin with formula-leading characters |
| Archive | CRC, exact manifest membership and per-file hashes checked; book copies match public downloads |

Accepted artifact hashes:

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| v0.11.0 book PDF | 3,248,621 | `71a07967791fbd35175e2154d8c258aec468e8f45e72952a207250d33d20862d` |
| v0.11.0 book EPUB | 21,751,704 | `f1d9bfae8df0a6879d1180e2a451d76040a739e3f7e688170f156beaeffe2cb6` |
| `research-bundle-book-v0.11.0.zip` (11 files) | 28,280,000 | `8b437b324b076809b6a024396d098d06fe4ffb8ca5a4518b871945659504f7c1` |

The EPUB probe tests normal browser layout, including actually panning contained
tables. Kindle and Apple Books pagination have not been tested. Some dedicated
readers handle wide tables differently; the buyer instructions explain
landscape orientation and the PDF alternative. Browser checks are not a claim
of native reading-app compatibility.

The PDFs lack tagged reading structure, and the main PDF lacks a document
language entry. The EPUB cover's SVG has no textual label, although inline book
images have alternative text. These artifacts have not received complete
assistive-technology certification. Do not advertise them as certified
accessible ebooks. The reflowable EPUB and online reader provide alternatives
to fixed PDF pages, but those alternatives also need reader-specific testing.

## The product a reader actually receives

This book combines a speculative argument about AI, a fictional narrative,
historical comparisons and a community action guide. Its strongest practical
entry is the Introduction, Chapter 19 and Appendix C, followed by one action
from Appendix G. Appendix A asks concrete questions about a food baseline:
need, resources, access, maintenance, workers, authority and evidence.

A first-time reader should hear that framing before a sales pitch. Someone
seeking an AGI engineering textbook, an investment recommendation, or a complete
household self-sufficiency manual would be buying a different product. The
current reading guide helps readers choose a route instead of requiring a
416-page commitment before finding an actionable idea.

The language is deliberately forceful and sometimes profane. That can connect
with readers frustrated by abstract AI commentary, but an expert or critic may
reject the tone before reaching its qualifications. Social promotion should
make the perspective visible and invite readers into the free sample. It
should describe the 2027 forecast as the author's forecast, the nine stages as
a speculative map, and the action sections as proposals to test locally.

The companion contains 31 cases, 28 with listed sources. A listed source is
not equivalent to independent verification; three unsourced cases remain
identified in the manifest and the introduction explains that limit. The
robotics CSV is a research lead, not a verified or endorsed supplier directory.

## Fresh source spot-checks

The following checks concern specific sample claims, not a complete fact-check
of the inherited book or every bonus case:

- [CDFA Food Recovery](https://www.cdfa.ca.gov/is/foodrecovery/) states that US
  food waste is estimated at 30–40% of the food supply and Californians discard
  5–6 million tons annually. Those figures match the introduction's attribution.
- [Oxfam's 19 January 2026 release](https://www.oxfam.org/en/press-releases/billionaire-wealth-jumps-three-times-faster-2025-highest-peak-ever-sparking)
  states billionaire wealth of $18.3 trillion, an 81% increase since 2020,
  billionaires being 4,000 times more likely to hold political office, and one
  in four people not regularly having enough to eat. The introduction attributes
  those figures to Oxfam. This checks the attribution; it does not independently
  reproduce Oxfam's underlying calculations.
- The cited UN food page returned HTTP 403 to this session. Its wording was
  not freshly independently verified here; a blocked fetch is not evidence
  that the claim is false.

## Specific editorial decisions still open

The repository already documents a cover provenance exception and unresolved
external-use assessments for modern epigraphs. The current edition retains
them. See [the quotation and cover inventory](../publication/QUOTATIONS-v0.10.0.md)
and [the earlier rights audit](../publication/RIGHTS-AUDIT.md).

The concrete passages include the Vinge quotation in `03-chapter1.md:8`, the
Good quotation in `04-chapter2.md:8`, and the Mitchell quotation in
`14-chapter12.md:8`. The existing inventory counts 21, 30 and 23 words
respectively. No permission correspondence or completed applicable-use
assessment was found in the reviewed repository. That does not establish
infringement or exclude fair use. The [US Copyright Office guidance](https://www.copyright.gov/fair-use/more-info.html)
states that there is no automatically safe word count and that fair use is
case-specific. Technical acceptance must not be described as clearance of
those publication decisions.

The public PDF correctly distinguishes original text from quoted material and
third-party images on its copyright page. No source prose, quotations or cover
art were silently removed to manufacture a clean review.

## Repeatable checks

```sh
node scripts/check-epub-reflow.mjs
EPUB_REFLOW_BROWSER=firefox node scripts/check-epub-reflow.mjs
EPUB_REFLOW_BROWSER=webkit node scripts/check-epub-reflow.mjs
java -jar /path/to/epubcheck.jar static/downloads/Surviving-the-Singularity-v0.11.0.epub
node scripts/deploy-book-bundle.mjs --local
```

The publication pipeline and private-storage instructions remain in
[publication/README.md](../../publication/README.md) and
[PRIVATE-BUNDLE.md](../../publication/PRIVATE-BUNDLE.md). Raw local proof logs
and inspected screenshots are retained under `/workspace/review/book-acceptance/`.
