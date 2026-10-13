# Launch candidate: 13 October 2026

The release code and current book downloads are prepared. **Do not merge to production until the deployment steps below are completed.** This workspace has GitHub access, but no configured Supabase, Stripe, Resend or Cloudflare deployment credentials. No production migration, upload, purchase, email or deployment was performed.

The deeper social-launch review is recorded in the [audience, evidence and social launch brief](audience-evidence-and-social-launch.md), [browser resilience findings](browser-resilience.md), [social/accessibility review](social-and-accessibility.md), and [book acceptance report](BOOK-ACCEPTANCE.md). The audience brief includes a detailed customer hypothesis, current primary research, competing books, critic responses and unsent social copy. Announce the actual $5 digital early-access draft; print is a separate future product. Use the [read-only operations preflight](operations-preflight.md) before completing the deployment evidence below.

## Integrated release

This branch starts from `release/v0.11.0` at `4377394471357ce5660a0cf62d2eeed3e13d8e77`, incorporates the site changes from PRs #28 and #30 and the isolated checklist/test fixes from #29, and applies the readiness repairs. It retains the v0.11 manuscript rather than the alternative v0.11.1 cut. All 35 canonical prose sections are unchanged by this repair; only the download release stamp changes.

Changes include:

- Explicit retryable fulfillment states, atomic database leases and fencing, stable provider idempotency keys, concurrent checkout reuse, duplicate-payment review flags, and a Stripe/local reconciliation monitor.
- Private bundle downloads require verified payment; development mocks cannot sign real downloads. Missing or mismatched bundle configuration disables paid checkout and signing. The checked-in manuscript and public book downloads remain public; the browser reader gate is not a secure paywall.
- Corrected Goldman Sachs, Mercer and AGI-survey claims with primary links; personal-forecast labeling; consistent digital/print/refund terms and accurate privacy disclosures.
- A public `/sample` introduction and reading guide; value proposition before the homepage forecast/video; coherent access-code labels and recovery.
- Keyboard focus containment and restoration, named checklist controls, optional unchecked marketing consent, accurate delivery feedback, and current reader navigation checks.
- Current PDF/EPUB, removal of outdated downloads and unsafe legal-advice PDF, one sitemap owner, removal of broken video recommendations, and fail-closed consent/email responses.
- Installable Svelte checks, focused regression/SQL/browser CI, compatible dependency updates, a scoped cookie patch, updated math renderer, and removal of five unused dependencies.
- A Worker-compatible HTML sanitizer replaces DOM-dependent rendering that crashed chapter pages on Cloudflare. The hosting adapter and Wrangler are pinned; local Worker checks cover all canonical chapters, assets and redirects. The final purchase prompt stays visible even if a browser animation stalls.
- Browser storage denial no longer crashes hydration. Checklist progress reports when persistence fails, and a 30-second request deadline restores checkout controls while explaining that the outcome is unconfirmed and retries should use the same email.
- Checkout, book access and checklist signup retain input entered before JavaScript loads. Both purchase fields stay synchronized, including autofill and Enter submission; each button submits its own current field value. Checklist consent and the anti-bot field also retain their actual values through hydration.
- A reproduced SvelteKit fragment-focus race no longer rewrites a newer checkout history entry with the previous sample URL. A scoped build transform guards that deferred callback; source-shape changes fail the build and require review. Normal fragment focus is preserved, with an actual-runtime negative control and deterministic browser regression.
- Crawler-visible social metadata is consolidated, the sample has a share card, and purchase/evidence cards state the current offer and review scope. A real HTTP guard checks all sitemap pages and served preview images without JavaScript.
- Narrow EPUB tables and long text now wrap. The private archive includes a script-free HTML getting-started guide with desktop, phone, PDF, EPUB, Kindle and purchase-recovery instructions. Canonical prose and the reviewed PDF bytes are unchanged.
- Purchase-page and two biological-computing blog comparisons now distinguish forecasts, proposals and measurements. New purchases fail closed when the sender, email-link origin or Stripe signing-secret configuration is knowingly unusable; existing paid-buyer recovery remains available. Preview receipts and unsubscribe links now use the intended public origin.

## Local evidence

| Gate | Result |
| --- | --- |
| Dependency install | Clean locked install completed; lockfile updated for the new checker and security fixes |
| `npm run check` | 0 errors; 314 legacy unused-style/compatibility warnings, no Svelte accessibility warnings |
| `npm run test:release` | 89 tests passed, including 37 payment source tests, 15 read-only preflight tests, eight sanitizer regressions and five actual-runtime history-guard checks; external service calls mocked, request deadlines also tested against real localhost HTTP fixtures |
| Disposable PostgreSQL 17.11 | 8 integration groups passed; real migrations, permission denials, concurrent claims/reservations, fencing and replay |
| Production build | Explicit Cloudflare Pages output passed with offer, artifact and reference-resolution guards |
| `npm run test:cloudflare` | 79 local Worker HTTP checks passed, covering all 35 canonical chapter loads, public sample, assets and redirects; 96 routing rules, no dropped exclusions; no Node compatibility flag; crawler guard also passed all 25 canonical pages and eight served PNG previews |
| Sanitizer review | 102 adversarial Chromium checks passed, including malformed markup, unsafe URLs, CSS, SVG and MathML payloads |
| Launch browser flows | Required CI covers Chromium desktop/mobile, Firefox desktop and WebKit desktop/mobile. Targeted history/focus/reading checks pass across all five profiles; delayed-script checkout checks also exercise both purchase fields. See [PR #31 checks](https://github.com/ctavolazzi/survivingthesingularity/pull/31/checks) for the final committed-suite result and [browser findings](browser-resilience.md) for reproduced failures and fixes |
| Existing regression suites | 87 source-policy tests and 18 checkout-gate browser cases passed; checkout mocks now run in WebKit CI without service secrets |
| Sitemap | All 25 listed paths return 200 locally |
| Visual checks | 10 page/viewport combinations: no uncaught page errors or horizontal overflow; primary mobile/desktop screenshots inspected |
| Automated accessibility | 12 settled mobile/desktop axe scans plus one built-site open-menu scan: no reported violations or page errors; manual/incomplete checks remain documented |
| Book proof | PDF 3.10 MiB / 416 pages, unchanged; EPUB 20.74 MiB passes EPUBCheck 5.4.0 with zero findings and all 420 browser layout combinations across three engines; canonical prose/artwork preserved |
| Private bundle | 11 files, 28,280,000 bytes; current books match public artifact hashes; local verification and storage-operation regressions pass |
| Deployment preflight | New configuration/read-only service checker verified with fault injection; actual workspace configuration fails because service credentials are absent. No live provider outcome inferred |

The browser suite intercepts all writes and blocks third-party requests. It tests the built site, not a real payment or inbox. Local WebKit used workspace-installed system libraries because system package installation was unavailable; the browser itself ran normally. The Worker guard runs the actual Pages output locally with isolated configuration and no service credentials. It checks gated chapter HTML and complete canonical server-data payloads; browser tests separately exercise unlocked reading. These checks do not establish Core Web Vitals, screen-reader certification, hosted database state or a live Cloudflare deployment.

## Deployment sequence

1. Apply and verify `sql/017_payment_reliability.sql` against the intended hosted database, after its prerequisites. Follow [the payment rollout](../payment-reliability-rollout.md). Keep a database backup and rollback plan for that environment. The migration is additive, but this code depends on its RPCs.
2. Upload the reviewed private artifact and verify the downloaded bytes using [the bundle instructions](../../publication/PRIVATE-BUNDLE.md). The prepared ZIP is at `book-build/bundle-v0.11.0/research-bundle-book-v0.11.0.zip`. It is intentionally not committed as a public download.
3. Configure hosting from the verified artifact manifest:

   ```text
   DOWNLOAD_BUCKET=downloads
   DOWNLOAD_BUNDLE_PATH=research-bundle-book-v0.11.0.zip
   DOWNLOAD_BUNDLE_BOOK_VERSION=0.11.0
   DOWNLOAD_BUNDLE_SHA256=8b437b324b076809b6a024396d098d06fe4ffb8ca5a4518b871945659504f7c1
   ```

4. Configure a preview with test-mode Stripe, an **isolated Supabase project/database and private storage**, and a verified test mailbox. Apply the prerequisites and migration 017 there and verify its reviewed bundle too. Never point this rehearsal or failure injection at the production database: ownership and reservations are keyed by email and edition, without a Stripe-mode partition. Verify checkout, authentic signed webhook, ledger, email provider ID, inbox, book code, private ZIP contents and return-link recovery. Repeat with a provider failure and two concurrent checkout tabs. Use fresh test addresses; no code deletes old purchases to enable retesting.
5. Rehearse the monitor against that preview by running `scripts/check-payment-reconciliation.mjs` with `RECONCILE_ORIGIN` set to the preview origin and its preview-only `ADMIN_RECONCILE_TOKEN`. Separately configure the same strong production token in production hosting and the GitHub monitor secret, and enable failure notifications. The new workflow cannot be manually dispatched until it exists on the default branch. The monitor scans seven days of Stripe checkout creation plus the local backlog; it is not a complete historical financial audit.
6. Review the rendered candidate and merge only after the preview and configuration checks pass. Once the workflow exists on the default branch, verify its manual production run and subsequent hourly schedule. Confirm the deployed commit, current downloads/redirects, production signature rejection, correct price/mode and reconciliation on the actual domain before the purchase announcement. Switching code alone does not apply SQL or upload private storage.

The connected GitHub integration denied repository-secret metadata access (403), and the managed environment reports no service credentials. Credential values should be configured in the service/CI secret stores, never pasted into this repository or a PR.

The existing [quotation and cover inventory](../publication/QUOTATIONS-v0.10.0.md) still records unresolved provenance for the retained cover and external-publication decisions for modern epigraphs, notably Vinge, Good and Mitchell. This review found no permission correspondence and does not determine whether a particular use is lawful. Resolve those recorded publication decisions before describing the book as cleared for external release. The PDFs are untagged; the reflowable EPUB is an alternative format, not a claim of screen-reader certification.

## Remaining dependency risk

The final full dependency audit still reports 22 findings (9 high, 13 moderate). High findings are in the legacy build/tooling chains; no visitor-controlled path to those high-severity conditions was identified. Svelte 4 retains moderate advisories requiring a framework upgrade. The application does not expose the identified untrusted dynamic-tag, attribute-spread or contenteditable-binding flows, but this is not a vulnerability clearance. Do not expose the development server publicly or build untrusted source with privileged secrets. A planned Svelte/Vite/Tailwind/toolchain upgrade remains maintenance work; blanket `audit fix --force` would introduce breaking framework changes.
