# Grayscale production resource preparation

The 372-page color PDF declared the same 565 image/form XObjects on every
page, including plain text pages. Ghostscript's original whole-book
conversion took approximately 22 minutes. The new preparation step removes
unused names from each page's resource dictionary while retaining every
referenced object, every nested resource scope, and the color master.

## Measured effect

| Probe | Original resources | Prepared resources |
| --- | ---: | ---: |
| Page 1, text | 5.52s | 0.18s |
| Page 6, text | 5.29s | 0.20s |
| Page 25, photograph | 6.73s | 1.07s |
| Page 151, SVG | not separately timed | 0.22s |

These are single-page Ghostscript conversions using the production settings,
not an estimate of the final whole-book time. Each prepared output was
confirmed to contain its requested page. Disabling duplicate-image detection
alone did not materially improve the original text-page times.

The guarded preparation completed in 40.37 seconds. It narrowed 210,180
page-level XObject references to 565, removing 209,615 unused references.
All 529 nested resource scopes were unchanged. The final build records its
own preparation counts and conversion time under `resource_pruning` and
`conversion_seconds` in `publication/output/build.json`.

## Implementation

`publication/prune_pdf_resources.py` clones the PDF into a separate
`print-prepared.pdf`. For each page it parses the content stream's `Do`
operators and retains only those named XObjects in a fresh, shallow resource
dictionary. It preserves original indirect references, font resources,
image streams and nested scopes. Forms, tiling patterns and Type3 fonts with
missing or unknown resource scopes are rejected. Unknown XObject types are
also rejected.

Before conversion, the written prepared PDF must preserve every page's
content-stream bytes and every annotation descriptor. Each called XObject
must still exist as an indirect reference after serialization. The original
color PDF's hash must remain unchanged. Ghostscript then uses the existing
grayscale, font-embedding and no-downsampling settings. The conversion now
also uses `PDFSTOPONERROR` and must retain the exact source page count before
any intentional blank final verso is added.

## Verification

On the diagnostic 372-page source:

- All page-content streams were byte-identical before and after preparation.
- Extracted text matched on every page.
- Every annotation rectangle and destination descriptor matched.
- Ghostscript rasterizations of pages 1, 6, 25, 151 and 251 were pixel-identical.
- The production helper's own output rendered page 151 correctly in 0.21s.
- Controls retained a referenced object, removed an unused name, and rejected
  a missing referenced object, a dereferenced direct stream, and an inherited
  resource scope.

The controls went red during development when content-stream truthiness
incorrectly classified a nonempty stream as absent. The implementation now
uses explicit `is not None` checks. A separate diagnostic also showed why an
exit code alone is insufficient: a malformed direct-stream PDF could make
Ghostscript skip pages while returning zero. Indirect-reference validation,
`PDFSTOPONERROR` and page-count preservation guard that failure.

Measured results and hashes are in
[`print-production-checks.json`](print-production-checks.json). Diagnostic
PDFs and rasters remain in `publication/output/diagnostic-*`.

## Limits

This preparation is deliberately conservative and tailored to the current
WeasyPrint resource structure. It refuses unfamiliar inherited scopes rather
than guessing which names can be removed. It uses pypdf's cloned object table
for the nested-scope audit; rerun its controls after dependency upgrades.

Ghostscript reconstructs PDF content during conversion, so preparation
parity does not establish final grayscale parity. The complete final output
still must pass `publication/check_pdf_resources.py`, including fonts,
annotations, text, grayscale streams, rendered samples, and optional blank
verso checks. See [Ghostscript's high-level device documentation](https://ghostscript.readthedocs.io/en/latest/VectorDevices.html).
