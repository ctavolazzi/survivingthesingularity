# Editorial art and presentation review

Six new conceptual vignettes are complete, with twelve source/print SVGs and deterministic generator `vignettes.py`. Their geometry is identical in both palettes. The screen artwork sits directly on the dark reading surface. Print/EPUB artwork has a white SVG ground so dark-mode ebook settings cannot make its lettering disappear.

All six canonical placements were inserted after unique, freshly read paragraph anchors. Exact image blocks, captions, and their purpose are recorded in `VISUAL-PLACEMENTS.md`. The source text outside those insertions was preserved.

| Illustration | Chapter | Print size at content width | Smallest label |
| --- | --- | --- | --- |
| Access gate | 6 | 4.56 × 3.21 in | 9.576 pt |
| Attention ribbon | 8 | 4.56 × 3.34 in | 9.576 pt |
| Operating stack | 11 | 4.56 × 3.77 in | 9.576 pt |
| Local copies | 2 | 4.56 × 3.55 in | 9.576 pt |
| Shared land | 12 | 4.56 × 3.79 in | 9.576 pt |
| Continuity calendar | 18 | 4.56 × 3.65 in | 9.576 pt |

These are explanatory illustrations. They contain no invented measurements, forecast probabilities, hardware specifications, legal forms, or service guarantees. The calendar uses the fictional scene's explicit boundary, funding through June, without adding a year or a delivery schedule.

## Shared layout

`src/lib/data/book/visuals.json` is the presentation registry. Its finite layouts are `diagram`, `cutout-left`, `cutout-right`, and `inset`. Registered ordinary Markdown images receive semantic figures and their immediately following italic captions. Unregistered and inline images retain their existing Markdown behavior. Legacy intrinsic image dimensions remain available, and each new asset can supply its own pixel dimensions.

`src/lib/styles/book-figures.css` overrides the older image panels in both web readers. Cutouts float at 32 percent of the text width on screens at least 760 pixels wide, then stack on narrower screens. Illustrations have no border, rounding, shadow, or opaque CSS panel. The PDF uses contained 1.42-inch left/right floats with 0.18-inch space beside prose. Headings, lists, tables, and other major blocks clear floats. There are no negative gutter offsets. EPUB figures always stack, use prepared light SVGs, and retain normal images and captions without requiring JavaScript.

The six raster cutouts are reserved in the registry. Their final files, dimensions, rights, and full chapter placement proof are owned by the main production task. The bounded layout proof uses the existing portrait photograph when the final Atlas cutout is unavailable; that is a geometry fixture, not a claim to have reviewed the final alpha edge.

## Prepared artwork protection

`publication/visuals.py` validates registered source and print SHA-256 values and bounds the print path to `static/book-images/print`. `docs/v0.9.2/print_figures.py` now recognizes prepared figures before any recoloring/fitting, preserving their distinct designs. An unregistered `v101-*.svg` fails instead of silently falling through to the old generic fitter. All seventeen new SVG pairs are registered: six concepts, eight charts, and three scene stills.

The final edition builder is `docs/v0.10.1/build.py`. It uses the existing frozen-source assertions, the same prepared light SVG resolver as print, and `scripts/book_visual_filter.py` for EPUB figure classes/manual captions. Invisible scene comments are removed from EPUB output while ordinary stills and all prose remain. `docs/v0.10.1/check_epub.py` retains resource/anchor/text checks and adds packaged-art hash coverage, accessible stills, marker absence, and stacking CSS checks.

## Proof and negative controls

Commands run:

```sh
python3 docs/v0.10.1/vignettes.py --proof
python3 docs/v0.10.1/prove_presentation.py
python3 docs/v0.10.1/prove_reader_art.py
python3 -m py_compile publication/visuals.py scripts/book_visual_filter.py docs/v0.10.1/build.py docs/v0.10.1/check_epub.py
node --check src/lib/utils/bookMarkdown.js
```

Browser SVG proof used actual Chrome text geometry, the publication JetBrains Mono font, and a 4.56-inch rendered width. All twelve files had zero label overlaps, out-of-frame labels, or sampled stroke crossings. Screenshots of all six illustrations were visually inspected at their actual width. Deliberately reduced type, overlapping text, an off-frame label, and a path through a label all failed the relevant checks. Results and screenshots: `visual-proof/checks.json` and `visual-proof/*-print.png` / `*-screen.png`.

Prepared-print proof passed all seventeen figures through the old pipeline while replacing its recoloring operation with an immediate failure. Every print file remained byte-identical. A bad print hash and a missing registry record both failed. Results: `visual-proof/prepared-bridge-check.json` and `presentation-checks.json`.

The PDF float fixture produced four pages, with a 1.42-inch figure on each of two pages and zero figure bounds violations or prose/figure intersections. A negative margin deliberately moved a figure into the gutter; another mutant moved it into the text. Both defects were detected. The first gutter control exposed a mistake in the instrument: a margin-box measurement concealed negative margins. The measurement now checks the actual content rectangle. The valid fixture was then rerun and its 96 dpi first-page raster inspected. Artifacts: `presentation-print.pdf`, `presentation-print-page-1.png`.

The actual Vite-served shared Markdown utility and stylesheet were exercised at desktop width and 390-pixel mobile width. Desktop floated the figure; mobile stacked it. Both had zero overflow or prose/image intersections and computed zero border/radius/shadow with a transparent background. A displaced figure triggered the gutter check. A hostile image handler was removed, and an italic-starting prose paragraph did not get consumed as a caption. Existing 1280 × 1920 image dimensions survived rendering. Results and screenshots: `reader-checks.json`, `reader-desktop.png`, `reader-mobile.png`.

The Pandoc EPUB filter fixture retained image alt text and the manual caption exactly once, assigned registered classes, retained the following paragraph, and removed the interactive comment. A removed-paragraph control failed coverage. Artifact: `epub-figure-fixture.html`.

## Limits

These checks establish vector label geometry, bounded layout behavior, preservation of prepared designs, and EPUB filter behavior. They do not certify physical print contrast or every EPUB device's font substitution. The complete EPUB audit and whole-book page/figure review require the frozen final manuscript and final cutout files. No full-book build was run during this task. Rights and release packaging remain with the main production task.

## Final asset and whole-book instrument follow-up, September 28

All six final alpha PNGs are now present with intrinsic dimensions in the common registry. `prove_figure_capture.py` exercises all twenty-three final new assets and their exact canonical captions in a bounded WeasyPrint document. All twenty-three passed: each image and complete caption occupies one page, lies within its containing figure and page content area, and avoids adjacent prose. Diagram widths are 4.56 inches; cutout widths are 1.42 inches. The fixture occupies 32 pages because it also contains repeated adjacent prose. It is not the final book pagination. Results: `visual-proof/all-figures-checks.json`; captured boxes: `all-figures-layout.json`.

The first run detected mojibake in captions from the test fixture's missing UTF-8 declaration. The fixture now declares UTF-8, matching the existing full publication template, and all exact-caption checks pass. The check did not normalize away the incorrect characters.

`publication/figure_layout.py` now captures the actual WeasyPrint box tree during the production build. Each registered figure receives a `data-book-visual` marker. `publication/build.py` saves `publication/output/interior-figure-layout.json`, including figure, image, caption and adjacent text rectangles, the page's actual content rectangle, and hashes of the final HTML and registry. `publication/proof.py` rejects a stale capture and checks every registered asset against its final HTML marker and caption. Edition 0.10.1 explicitly requires twenty-three registry entries.

Eight deliberate layout mutations are rejected: gutter intrusion, prose placed over a figure, a caption outside its container, missing caption text, a missing figure, an undersized image, a caption moved to another page, and a missing final HTML marker. The reusable instrument is ready for the final whole-book render; this follow-up does not claim that an unrendered final PDF passed.

`prove_cutout_chapters.py` checks the actual `/book` and `/read` routes for Introduction and Chapters 3, 5, 9, 11, and 17 at 1280 and 390 pixels. This uses final PNGs, full canonical chapters, and the real shared Markdown renderer. It checks decoded image dimensions, caption and alt presence, float/stack behavior, content bounds, transparent styling, and collisions with the actual text ranges. A real figure moved into the gutter must fail and is then restored. Screenshots and machine-readable results are saved under `visual-proof/cutout-chapters/`.

The route review found a mobile overflow in the continuous reader's Chapter 9 PID equation. The chapter reader already contained long display math; the continuous reader did not. Shared CSS now gives the continuous reader's display equations their own horizontal scrolling area. This leaves the surrounding chapter and cutout inside the viewport while retaining the complete equation. All twenty-four final cutout route/viewport cases then passed, with zero browser errors, image/prose intersections, or root overflow. No canonical Markdown was changed in this follow-up.
