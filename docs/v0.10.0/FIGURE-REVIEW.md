# v0.10.0 figure review

Reviewed 2026-09-27 against the five unresolved print-label problems named in
`docs/v0.9.2/EDITION-NOTES.md`. All five are redrawn as editable SVGs with the
existing navy, amber and blue palette. Dark website originals and light print
variants are both retained.

## Result at the book's actual content width

The 6 x 9 page has 0.80in and 0.64in horizontal margins: **4.56in of content**.
Measurements below use Chrome with the repository's packaged JetBrains Mono
font loaded explicitly, then convert SVG font units into physical points.
Screenshots use that same 4.56in viewport width, captured at 2x device density.

| Figure | Previous minimum at 4.56in | New print minimum | New height |
| --- | ---: | ---: | ---: |
| `ch09-region-ring.svg` | 4.22pt | 9.94pt | 6.10in |
| `ch11-cooling-loop.svg` | 3.78pt | 10.28pt | 6.43in |
| `ch17-fab-lab.svg` | 4.20pt | 10.37pt | 6.73in |
| `ch17-lora-node.svg` | 4.52pt | 9.50pt | 6.69in |
| `intro-food-insecurity.svg` | 4.19pt | 10.89pt | 6.26in |

Previous sizes are calculated from the prior edition's recorded minimum font
size and cropped width. New sizes are measured from the current rendered SVG.
Every dark source also has at least 8.21pt text at this width before the print
fitter enlarges anything. The acceptance threshold is 7pt.

Machine measurements, hashes and the negative-control results are in
[`figure-proof/checks.json`](figure-proof/checks.json). Each figure has a
`-screen.png` and `-print.png` proof in the same directory. All five print
proofs were inspected visually. Cooling and mesh were inspected again after
their final routing and spacing changes.

## What changed

- Region: four production sectors feed the city from above and below. Each
  sector now has room for wrapped labels. The unsourced materials-wide
  claim "capture the 40% we waste" is replaced with "recover scrap and
  reusable materials".
- Cooling: vertical hierarchy separates the insulated shell from outside
  air. The cool return explicitly reaches both processor blocks. Hardware
  choices and the 600 to 1000 watt combined load are labeled illustrative.
  The heat equation remains visible in full-size type.
- Fab lab: stacked machine-to-output rows replace three narrow columns.
  RepRap prints "some of its own parts". The broad "low-power, DC-bus
  friendly" claim is replaced with matching power supply to machine load.
- Mesh: an explicit power path and radio link replace labels laid over
  decorative panel lines. Idle power, runtime and reach are no longer
  unconditional promises. Hardware, firmware and regional radio settings
  must match. The drawing now names a matched charger and a protected battery
  pack; it no longer routes a plain 5V regulator into salvaged laptop cells.
- Food chart: original USDA data are unchanged. A separate legend and data
  summary replace annotations fighting the plotted lines. The second series
  is dashed so grayscale readers can identify it without color. Source text
  is full-size. The recession annotation is outside the narrow shaded band.

The charger correction follows the distinction between regulated output and
managed battery charging documented by [Texas Instruments](https://www.ti.com/product/BQ25157).
Regional radio settings are checked against [Meshtastic's LoRa configuration](https://meshtastic.org/docs/configuration/radio/lora/).
Both primary pages were opened during this review. These references explain
the corrections; they do not specify or certify this conceptual assembly.

## Verification and regeneration

```bash
python3 docs/v0.10.0/figures.py
python3 docs/v0.10.0/proof_figures.py
```

The first command regenerates all five dark SVGs. The second uses the existing
`docs/v0.9.2/print_figures.py` palette and measured fitting algorithm to create
five light derivatives. It updates only those five entries in the print hash
ledger, preserving other figures. The historical `charts.py` food-chart
function delegates to the new generator; this was checked against the actual
source file so an older chart command cannot silently restore the small type.

Both sources and derivatives have zero measured label overlaps, text outside
the frame, box-edge violations, or lines crossing text. Each derivative fits
the 7in diagram height limit. The proof script first inserts a duplicate label
in memory and requires the collision audit to detect it, then reduces one
label to 1px and requires the physical-size check to detect it. Both negative
controls passed. During development the same audit caught a supply arrow
crossing its label; the first fab layout also failed the 7in height gate.
Both were corrected before the final green run.

## Limits

This is a digital geometry and visual proof, not a physical print proof.
The final publication layout places all five at exactly 4.56in width;
`final-figure-layout.json` records their actual pages and dimensions.
Caption placement is included in the final PDF visual review. No claim
is made that these conceptual equipment diagrams are complete engineering
plans. Existing manuscript sources remain the authority for the accompanying
technical discussion. The rest of the book's figures were not redrawn by this
pass.
