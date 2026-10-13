# Cast plate proof: v0.10.0

The new `static/book-images/coop-cast.svg` replaces the baked caption layer
with editable vector text. Its light counterpart is
`static/book-images/print/coop-cast.svg`. The prior `coop-cast.png` is preserved.
Regenerate both and their proofs with `python3 docs/v0.10.0/cast_plate.py`.

The four existing character PNGs are embedded unchanged. Decoding each SVG's
image data reproduced the corresponding source PNG byte for byte. Nested SVG
viewports omit only transparent outer margins, with padding around every
nontransparent pixel. No bitmap was retouched or generated. JetBrains Mono
Regular and SemiBold are embedded from the repository's existing font files;
their license and provenance remain in `publication/assets/fonts/`.

Roles follow the canonical art catalog: Elijah is a former tech worker
learning to build; Marta is a fabricator running the co-op shop; Priya is a
soil scientist; Denny is a former logistics worker and co-op media operator.
The outdated network-engineer label is absent.

Chrome measured both variants at the publication's 4.56-inch figure width.
The actual rendered dimensions were approximately 4.560 by 5.586 inches.
The thirteen text labels have a minimum measured size of **9.23 pt**, above
the required 8 pt. No text boxes overlapped or left the SVG frame.

Both negative controls failed as intended before the final measurements:
an injected duplicate label caused an overlap, and a label reduced to 1 SVG
unit fell below the physical size requirement. Neither control touched a
source file. Both screen and print screenshots were visually inspected.
The figures and all four portraits are complete and their labels are clear.

`checks.json` records source hashes, byte-preservation checks, physical sizes,
and geometric results. The two PNGs in this directory are browser screenshots
of the completed vector layouts. XML parsing and code readback also passed.
This is a digital proof, not a physical printer proof or external rights
clearance. Root owns canonical references, catalog and audit updates, final
PDF layout, and print-variant integration.
