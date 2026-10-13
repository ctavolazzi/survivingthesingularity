# Launch candidate: 13 October 2026

The release code and current book downloads are prepared. **Do not merge to production until the deployment steps below are completed.** This workspace has GitHub access, but no configured Supabase, Stripe, Resend or Cloudflare deployment credentials. No production migration, upload, purchase, email or deployment was performed.

## Integrated release

This branch starts from `release/v0.11.0` at `4377394471357ce5660a0cf62d2eeed3e13d8e77`, incorporates the site changes from PRs #28 and #30 and the isolated checklist/test fixes from #29, and applies the readiness repairs. It retains the v0.11 manuscript rather than the alternative v0.11.1 cut. All 35 canonical prose sections are unchanged by this repair; only the download release stamp changes.

Changes include:

- Explicit retryable fulfillment states, atomic database leases and fencing, stable provider idempotency keys, concurrent checkout reuse, duplicate-payment review flags, and a Stripe/local reconciliation monitor.
- Verified production purchase access; development mocks cannot sign real downloads. Missing or mismatched bundle configuration disables paid checkout and signing.
- Corrected Goldman Sachs, Mercer and AGI-survey claims with primary links; personal-forecast labeling; consistent digital/print/refund terms and accurate privacy disclosures.
- A public `/sample` introduction and reading guide; value proposition before the homepage forecast/video; coherent access-code labels and recovery.
- Keyboard focus containment and restoration, named checklist controls, optional unchecked marketing consent, accurate delivery feedback, and current reader navigation checks.
- Current PDF/EPUB, removal of outdated downloads and unsafe legal-advice PDF, one sitemap owner, removal of broken video recommendations, and fail-closed consent/email responses.
- Installable Svelte checks, focused regression/SQL/browser CI, compatible dependency updates, a scoped cookie patch, updated math renderer, and removal of five unused dependencies.
- A Worker-compatible HTML sanitizer replaces DOM-dependent rendering that crashed chapter pages on Cloudflare. The hosting adapter and Wrangler are pinned; local Worker checks cover all canonical chapters, assets and redirects. The final purchase prompt stays visible even if a browser animation stalls.

## Local evidence

| Gate | Result |
| --- | --- |
| Dependency install | Clean locked install completed; lockfile updated for the new checker and security fixes |
| `npm run check` | 0 errors; 314 legacy unused-style/compatibility warnings, no Svelte accessibility warnings |
| `npm run test:release` | 59 tests passed, including 30 payment source tests and eight sanitizer regressions; all service calls mocked |
| Disposable PostgreSQL 17.11 | 8 integration groups passed; real migrations, permission denials, concurrent claims/reservations, fencing and replay |
| Production build | Explicit Cloudflare Pages output passed with offer, artifact and reference-resolution guards |
| `npm run test:cloudflare` | 79 local Worker HTTP checks passed, covering all 35 canonical chapter loads, public sample, assets and redirects; 96 routing rules, no dropped exclusions; no Node compatibility flag |
| Sanitizer review | 102 adversarial Chromium checks passed, including malformed markup, unsafe URLs, CSS, SVG and MathML payloads |
| Launch browser flows | 55 passed across Chromium desktop/mobile, Firefox desktop, WebKit desktop/mobile: 45 standard launch cases plus 10 final-CTA animation/failure cases |
| Existing regression suites | 87 source-policy tests and 18 checkout-gate browser cases passed; checkout mocks now run in WebKit CI without service secrets |
| Sitemap | All 25 listed paths return 200 locally |
| Visual checks | 10 page/viewport combinations: no uncaught page errors or horizontal overflow; primary mobile/desktop screenshots inspected |
| Book proof | PDF 3.10 MiB / 416 pages; EPUB 20.74 MiB; all expected text blocks, artwork inputs and PDF links checked |
| Private bundle | 10 files, 28,272,621 bytes; current books match public artifact hashes; local verification and five storage-operation regressions pass |

The browser suite intercepts all writes and blocks third-party requests. It tests the built site, not a real payment or inbox. Local WebKit used workspace-installed system libraries because system package installation was unavailable; the browser itself ran normally. The Worker guard runs the actual Pages output locally with isolated configuration and no service credentials. It checks gated chapter HTML and complete canonical server-data payloads; browser tests separately exercise unlocked reading. These checks do not establish Core Web Vitals, screen-reader certification, hosted database state or a live Cloudflare deployment.

## Deployment sequence

1. Apply and verify `sql/017_payment_reliability.sql` against the intended hosted database, after its prerequisites. Follow [the payment rollout](../payment-reliability-rollout.md). Keep a database backup and rollback plan for that environment. The migration is additive, but this code depends on its RPCs.
2. Upload the reviewed private artifact and verify the downloaded bytes using [the bundle instructions](../../publication/PRIVATE-BUNDLE.md). The prepared ZIP is at `book-build/bundle-v0.11.0/research-bundle-book-v0.11.0.zip`. It is intentionally not committed as a public download.
3. Configure hosting from the verified artifact manifest:

   ```text
   DOWNLOAD_BUCKET=downloads
   DOWNLOAD_BUNDLE_PATH=research-bundle-book-v0.11.0.zip
   DOWNLOAD_BUNDLE_BOOK_VERSION=0.11.0
   DOWNLOAD_BUNDLE_SHA256=8864d224a25328ca5f5fa8e02c91df80d38cd9a408aefe6126a65edb1068d99b
   ```

4. Configure a preview with test-mode Stripe and a verified test mailbox. Verify checkout, authentic signed webhook, ledger, email provider ID, inbox, book code, private ZIP contents and return-link recovery. Repeat with a provider failure and two concurrent checkout tabs. Use fresh test addresses; no code deletes old purchases to enable retesting.
5. Configure the same strong `ADMIN_RECONCILE_TOKEN` in hosting and the GitHub monitor secret. Run the monitor manually, verify its result, and enable failure notifications. It scans seven days of Stripe checkout creation plus the local backlog; it is not a complete historical financial audit.
6. Review the rendered candidate and merge only after those checks pass. Confirm the deployed commit, current downloads/redirects, production signature rejection, correct price/mode and reconciliation on the actual domain. Switching code alone does not apply SQL or upload private storage.

The connected GitHub integration denied repository-secret metadata access (403), and the managed environment reports no service credentials. Credential values should be configured in the service/CI secret stores, never pasted into this repository or a PR.

## Remaining dependency risk

The final full dependency audit still reports 22 findings (9 high, 13 moderate). High findings are in the legacy build/tooling chains; no visitor-controlled path to those high-severity conditions was identified. Svelte 4 retains moderate advisories requiring a framework upgrade. The application does not expose the identified untrusted dynamic-tag, attribute-spread or contenteditable-binding flows, but this is not a vulnerability clearance. Do not expose the development server publicly or build untrusted source with privileged secrets. A planned Svelte/Vite/Tailwind/toolchain upgrade remains maintenance work; blanket `audit fix --force` would introduce breaking framework changes.
