# Layout polish for v0.10.3

The previous edition's type, margins and revised diagram label sizes are retained. This pass improves page transitions and heading hierarchy by moving three complete image/caption pairs and adjusting the publication builder. No manuscript prose, image alt text or caption wording was rewritten.

## Observed problems and changes

Page numbers below identify the v0.10.2 interior PDF. Add one for the reading PDF, which includes the cover. The printed Arabic folio is four less than the interior page number.

| Before | Change |
| --- | --- |
| Interior 318 had only the running head and folio; 319 had only the Chapter 19 title; the story began on 321. | Moved the existing ladder diagram and its caption immediately before Rung 1, after the plan introduction. The opening now proceeds through the quote and chapter summary into the story. |
| Interior 170 held only “The greenhouse brain” and its 34-word introduction. The figure filled 171; the component and operating explanation resumed on 172. | Moved the greenhouse diagram after the complete controller explanation, just before “A worked example.” The sensor, actuator, installation, PID and manual-control prose now stays in sequence. |
| Interior 373 held Appendix D's title and short introduction, followed by a full-page timeline. | Moved the unchanged timeline after the ledger table. The appendix begins with its operating procedure, then the index, then the visual timeline. |
| Interior 24 repeated “How to Use This Book” as both eyebrow and title. | The builder emits the chapter eyebrow only when the source heading contains a separate label before a colon. Chapter, part and appendix labels remain. |
| Interior 407 held only the final 41-word narrative-art provenance paragraph. | Reduced the margin between individual credits from 0.14 to 0.10 inches, retaining font sizes. The two closing provenance paragraphs form a group that stays on one page. |

The title-only opening and preceding blank were one layout failure: moving the oversized opening figure removed both in the isolated reproduction. Removing the chapter's float-clearing pseudo-element did not fix them, so that rule was preserved.

The greenhouse figure was initially tried immediately after the Sensors/Actuators list. That improved the stub but still left a short page. Placing it after the full explanation removed an additional page without reducing diagram labels or changing the instructional sequence.

## Evidence and limits

Eight before images were copied into [layout-proof](layout-proof/) from rasterizations of the previous edition's actual prepared PDF. They show the duplicate heading, empty page, title-only opening, delayed story, greenhouse stub, appendix entry and credits tail.

[prove_layout_polish.py](prove_layout_polish.py) renders bounded fragments of the previous edition's final HTML with the changes applied. It does not build the complete book or include the new narrative plates. Its [receipt](layout-proof/fragment-checks.json) records hashes, text/image preservation and these outcomes:

- Chapter 18 plus Chapter 19: 34 pages to 32. The observed blank and title-only pages disappear. The new Chapter 19 opening includes 259 words and the start of the story.
- Chapter 9: 21 pages to 20. The greenhouse opening page grows from 34 to 264 words, including the operating explanation.
- Appendix D: nine pages to eight. Its first page now includes the operating procedure.
- The same prior credit entries: six pages to five. The final page includes the closing provenance group and 280 words, rather than a 41-word final leaf.
- The actual builder heading block retains numbered labels and produces only one unnumbered title.

The prior defects are observed failing controls. Before/after fragment checks also require identical text and image inventories. Exact source moves, whole-file hashes at movement time and unchanged paragraph-multiset checks are recorded in [layout-source-moves.json](layout-source-moves.json). Later narrative-plate additions legitimately change the corresponding whole-file hashes.

The four resulting sample PDF pages were rasterized and visually reviewed: Chapter 19 opening, greenhouse explanation, Appendix D opening and final credit page. All retain readable type and show the intended reading flow.

Full assembled pagination, new figure captions, internal navigation and text recovery still require the normal edition build and final PDF/EPUB review. Fragment page counts are evidence of these isolated fixes, not a promise about the final book's length. The new image-generation credits must be added by integration; inherited PixelLab attribution must not be applied to new plates from another provider.
