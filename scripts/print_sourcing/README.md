# print_sourcing

Turns a hyperlinked manuscript (markdown) into print-friendly sourcing.

    python3 scripts/print_sourcing/print_sourcing.py IN.md OUT.md --mode print --label-until "Chapter 2" --report REPORT.md

- Body citations `Claim. [Name](url)` become `(Source: Name)` up to the `--label-until` chapter, then `(Name)`.
- Back-to-back citations merge: `(Source: A; B)`. Already hand-converted `(Source: [Name](url))` is recognised, not double-wrapped.
- Image credits, in-sentence links and "Free at ..." links keep their words and lose the link (print).
- Appendix B keeps titles and prints the full URL at the end of each entry; body URLs missing from Appendix B go to
  "Additional sources cited in the text"; image-credit URLs go to "Image credits".
- `--mode ebook` keeps every link inside the same wording.
- Self-checks: every link accounted for; nothing outside an edit changes; zero links left in print mode.

Test: `cd scripts/print_sourcing && python3 test_print_sourcing.py` (includes a control that must fail).
