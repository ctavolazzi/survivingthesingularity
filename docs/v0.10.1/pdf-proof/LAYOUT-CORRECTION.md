# Cutout pagination correction

The first whole-book proof rejected the tools cutout because its image was
on interior page 277 and its caption continued on page 278. The continued
float also retained the previous page's horizontal position across mirrored
margins. Five other cutout captions had glyph boxes extending slightly below
their figure bounds. The failed measurement is retained in
[first-build-checks.json](first-build-checks.json), with the captured boxes in
[first-build-figure-layout.json](first-build-figure-layout.json).

`publication/book.css` now gives cutout floats a vertical flex layout so the
image and credit move together. Caption line height increased from 1.25 to
1.5. Text, captions, image widths and source artwork remain unchanged. The
print fixture's inspector now recognizes both block and flex float boxes.

The correction was first exercised against the complete Chapter 17 layout.
The final complete-book capture then placed all 23 additions on individual
pages with complete captions, inside the content area and without intersecting
prose. Tools and its credit now occupy interior page 278 together. Interior
length changed from 392 to 393 pages; the reading copy adds its cover.

The figure checker also rejected eight deliberate defects: gutter intrusion,
prose collision, caption overflow, missing caption text, missing figure,
undersized artwork, a caption on a second page, and a missing HTML marker.
The updated two-float fixture rejected deliberate gutter and prose collisions.
Evidence is in `publication/output/interior-figure-layout.json`,
`docs/v0.10.1/visual-proof/all-figures-checks.json`, and
`docs/v0.10.1/visual-proof/presentation-checks.json`.

These are geometry measurements. Final rendered-page inspection, PDF text and
resource validation, and EPUB verification have separate reports.
