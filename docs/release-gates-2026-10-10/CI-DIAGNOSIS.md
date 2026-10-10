# PR24 WebKit CI diagnosis

Reviewed October 10, 2026. Historical run: [37885118087](https://github.com/ctavolazzi/survivingthesingularity/actions/runs/37885118087), attempt 1, source `4377394471357ce5660a0cf62d2eeed3e13d8e77` on `release/v0.11.0`.

The account tests expect a sign-in surface that CT explicitly removed. The run provides no evidence of a WebKit installation failure or a Safari layout defect behind these failures.

## Retrieved evidence

Job metadata and job logs were retrieved with `gh api`, using `GODEBUG=http2client=0`. Check-run annotations were also retrieved. Later artifact downloads and repeat log requests hit connection resets or 35-second timeouts; no artifact ZIP was retained or inspected.

| Project | Job | Verified result |
|---|---|---|
| Desktop Safari / `webkit` | [113673276714](https://github.com/ctavolazzi/survivingthesingularity/actions/runs/37885118087/job/113673276714) | Job failed in the test step; the three sign-in assertions below failed. |
| iPhone 13 / `mobile-safari` | [113673276475](https://github.com/ctavolazzi/survivingthesingularity/actions/runs/37885118087/job/113673276475) | Job failed in the test step; the three sign-in assertions below failed. |
| iPad / `tablet` | [113673276734](https://github.com/ctavolazzi/survivingthesingularity/actions/runs/37885118087/job/113673276734) | Final log summary: **3 failed, 177 passed**. |

All three jobs successfully checked out source, installed dependencies, installed WebKit, and uploaded their reports. Final pass counts for the first two projects are not claimed here because they were not retained in the inspected output.

The failing tests, at their original line numbers in `tests/e2e/g-user-profiles.spec.js`, are:

1. Line 20: `Sign-in page loads and has form elements`.
2. Line 32: `Sign-in form validates email input`.
3. Line 82: `Sign-in page is accessible on mobile`.

Each navigates to `/signup?mode=signin`. The server logs show `404 GET /signup`; `input[type="email"]` is absent, and `toBeVisible()` fails after its 5-second assertion timeout. Retries repeat the same obsolete expectation.

All three check-run annotations state that `i-checkout-gate` was excluded because no `SUPABASE_URL` CI secret was configured. This run therefore does not verify the backend purchase and fulfillment path. Node action-runtime deprecation and an announced Ubuntu runner migration are warnings, not the observed cause of failure.

## Product contract and repair

`src/hooks.server.js:4` records CT's August 4 ruling: accounts, profiles and sign-in were removed. Buyer identity is the purchase email. `/signup`, `/profile` and `/auth/callback` are absent from the source tree. Reintroducing accounts to satisfy these assertions would reverse that ruling.

The repaired spec keeps its historical filename and checks the current behavior:

- Removed signup, sign-in query, profile and OAuth callback paths return exactly 404 and contain no account controls.
- Both preorder buttons require a valid purchase email and share the entered value.
- An existing buyer's mocked recovery response uses the purchase email, without a sign-in redirect or password field.
- The real preorder email input remains usable at 375 by 667. Input and button bounding boxes must fit inside the viewport; the original document-overflow constraint is also retained. Bounding boxes catch clipping hidden by `overflow-x: hidden`.
- Checklist progress and notes survive a reload. This replaces a nonasserting log of storage keys on a removed blueprint route.
- The actual free checklist email gate submits explicit consent choices, reveals four additional items, and remains unlocked after reload. This replaces an optional homepage form check that could pass when no form existed.

The spec now has nine tests: four removed-route cases and five current email/local-state cases. There are no skipped tests or conditional assertions that allow a missing form to pass. The shared local-only fixture blocks cross-origin browser requests and returns a synthetic 503 for unmocked browser `/api/` requests. Selected cases override it with synthetic checkout, waitlist and checklist-email responses. No real payment, message delivery or customer record is used. The local server has no Stripe, Supabase, Resend or SMTP credentials; browser interception alone cannot prevent server-side calls.

## Usability coverage and discovered product defect

`h-usability.spec.js` now requires both palette shortcuts, focus, search and empty results, Escape, keyboard navigation, the skip link, actual `.reveal.visible` behavior, the thank-you dialog and current internal links. It no longer treats a missing feature or a count greater than or equal to zero as proof of functionality. Removed blueprint, stack-table, calculator and dev-only panel checks are not claims of current product coverage. Internal link requests disable automatic redirects and validate each destination's origin and non-API path before following it.

The first Chromium run produced 16 passes and two failures. One was an ambiguous email selector in the new test, corrected by scoping it to the checklist gate. The other exposed a real defect: checklist defaults overwrote localStorage before `onMount` restored saved progress. `src/routes/checklist/+page.svelte` now waits until restoration completes before persisting. The original regression test failed at its post-reload checked-state assertion before this repair.

A subsequent 54-case run passed 52 cases and identified two Firefox test-environment issues. Readiness now allows 15 seconds for hydration rather than five. Firefox's first Tab focuses the scrollable body, reproduced independently with minimal HTML and the site's height/overflow CSS; its next Tab focuses the skip link, and Enter focuses main content. The test allows that one Firefox scroll-container stop and still requires both navigation assertions. No product CSS was changed for this behavior.

## Verification record

Five temporary test-only faults each produced exactly one expected Chromium failure, then the original spec bytes were restored:

| Injected fault | Assertion observed failing |
|---|---|
| `/signup` responds 200 | Exact 404 status |
| Buy button enabled for an invalid email | Disabled button |
| Buy button forced to 900px on a 375px viewport | Bounding-box right edge |
| Keyboard event prevented from reaching palette | Visible dialog |
| IntersectionObserver never reports an intersection | Required `visible` class after scrolling |

Raw counts and timestamps are retained in [negative-controls.json](negative-controls.json). These controls establish that those assertions can observe those defect classes. They do not establish backend fulfillment.

The three changed JavaScript files pass `node --check`. Offer drift, book-download and resolver-parity guards pass. The download guard explicitly reports an open cycle: v0.11.0 source with v0.7.5 public downloads. That result is not certification that a v0.11.0 download was published.

`npm run check` cannot finish because `svelte-check` is absent from both package manifests and the installed dependencies. This is an existing repository check-configuration gap, not a passing type check. Fresh dependency installation also timed out; local browser verification uses a private copy of an existing installation whose `package-lock.json` is byte-identical. No dependency versions or lockfiles were changed.

Final local result: **54 passed, zero failed, zero skipped, zero flaky**, with 18 cases each in Chromium, Firefox and mobile Chrome. See [local-validation.json](local-validation.json) for timestamps, command, project counts and exact changed-file hashes. All five negative controls preceded this final restored run.

This macOS host cannot run WebKit; Chromium and Firefox results cannot substitute for the three Linux WebKit projects. The Linux CI follow-up is pending at this commit. Backend checkout remains a separate gate; repository secret-name metadata currently contains no Supabase test configuration.
