# Private bundle deployment

The reviewed candidate is `book-build/bundle-v0.11.0/research-bundle-book-v0.11.0.zip`.
It contains the current book, the corrected research introduction and instructions,
and the research/cover extras. The obsolete municipal ordinance is omitted.
Open `The-Precedent-File/START-HERE.html` after extracting the ZIP for the
browser-friendly, offline reading guide. It explains extraction on phones and
computers, PDF versus EPUB, importing into a reader, Kindle delivery, and access
recovery. The same instructions remain available as plain-text Markdown.
Its exact contents and hash are in the active `src/lib/data/bundleManifest.js`.
The storage object has **not** been uploaded or remotely verified in this workspace.

## Prepare and verify locally

After preparing the public book downloads as described in [README.md](README.md):

```sh
python3 scripts/prepare-book-bundle.py
node --test scripts/deploy-book-bundle.test.mjs
node scripts/deploy-book-bundle.mjs --local
```

Preparation writes a candidate `bundleManifest.js` beside the ZIP and leaves the
active site manifest alone. Review the candidate, then copy that generated file
to `src/lib/data/bundleManifest.js` before the local deployment verification.
The launch branch already contains the manifest for the prepared candidate.
Rebuilding may change ZIP/PDF timestamps and hashes even when prose is unchanged;
use the exact reviewed ZIP, or review and commit its new manifest before uploading.
The builder copies the proved public book PDF and EPUB byte for byte. It does
not rebuild those books. Preparation checks the research PDF's source blocks
and every archive-relative link in the self-contained HTML instructions.

## Reading acceptance

The actual v0.11.0 public EPUB passed W3C EPUBCheck 5.4.0 with no errors,
warnings or informational findings on 2026-10-13. Its 35-section navigation,
language, title and author metadata are present, and all 110 inline book images
have nonempty alternative text. This is EPUB format validation, not a guarantee
about every reading app or a complete accessibility certification. The SVG
cover has no textual label and the PDFs are not tagged; prefer the reflowable
EPUB or online reader when fixed PDF pages are difficult to use. Device-specific
reading and assistive-technology acceptance remain separate checks.

Wide reference tables keep readable columns within a horizontally scrollable
container on narrow screens. Chromium checks verify that the tables pan without
making the entire chapter overflow. Paginated Kindle/Apple Books behavior has
not been verified; it must not be inferred from Chromium. The included guide
explains landscape orientation and the PDF alternative for readers whose apps
handle wide tables differently.

Do not mistake technical acceptance for rights clearance. The current source
retains the cover provenance exception and modern epigraph questions documented
in [the quotation and cover inventory](../docs/publication/QUOTATIONS-v0.10.0.md).

## Upload and verify the immutable object

Supply `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` (or `SUPABASE_SECRET_KEY`) through
the process environment. Keep credentials out of source files, commands saved
to the repository, and deployment receipts.

```sh
# Read-only verification; never creates or replaces a storage object.
node scripts/deploy-book-bundle.mjs

# Explicitly create the absent versioned object, then download and hash it.
node scripts/deploy-book-bundle.mjs --upload
```

The uploader uses `upsert: false`. An identical object is a successful no-op.
An existing object with different bytes is an error; it is never overwritten.
Storage/API errors are not treated as proof that an object is absent.

After remote verification, configure the site deployment with the four nonsecret
values printed by the script: `DOWNLOAD_BUCKET`, `DOWNLOAD_BUNDLE_PATH`,
`DOWNLOAD_BUNDLE_SHA256`, and `DOWNLOAD_BUNDLE_BOOK_VERSION`. They must match the
active manifest. Checkout and signed download creation remain unavailable until
the runtime configuration matches. Keep the old storage object for existing
signed URLs; new fulfillment must use the reviewed versioned object.

The older `sts.py bundle upload` command targets the legacy in-place workflow.
Use this versioned deployment script for the launch candidate. Complete an actual
paid checkout, receipt and signed download check after deployment configuration;
an authenticated storage read alone does not prove that customer journey.
