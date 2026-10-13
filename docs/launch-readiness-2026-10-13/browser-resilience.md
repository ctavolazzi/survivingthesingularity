# Browser resilience acceptance evidence

This second pass used the release candidate in `/workspace/sts-launch` and
simulated conditions a reader can encounter after opening a social post.
It found and corrected issues that the earlier ordinary browser flows did not
exercise. This is local evidence, not proof of a live purchase or inbox delivery.

## Findings and changes

- **Blocked browser storage broke the whole site.** Throwing `SecurityError`
  when accessing local/session storage changed successfully rendered pages into
  Svelte's `500 Internal Error` screen after hydration. The homepage, sample,
  offer, checklist and book gate all reproduced it. Shared reader preference
  stores now tolerate unavailable storage; state can continue in memory.
  Checklist signup also reveals the checklist after a successful response when
  saving the unlock flag fails. Its notes notice explicitly says when progress
  will be lost on reload, instead of claiming the notes were saved.
- **Malformed stored progress could mark unfinished steps complete.** A stored
  string such as `"false"` was coerced to true. Restoration now requires a real
  boolean, accepts only string notes, limits note length and ignores unknown
  keys. Invalid JSON, null, strings, numeric fields and an unexpected prototype
  key are covered separately.
- **A stalled request could leave checkout disabled indefinitely.** Checkout,
  checklist unlock and checklist email now have a 30-second deadline covering
  both headers and response body. Checkout restores its controls and tells the
  reader that the result is unconfirmed and to retry with the same email.
  This does not claim that a timed-out request failed to create a Stripe
  session. The server's existing reservation/idempotency flow remains the
  protection against duplicate checkout creation.
- **Small screens clipped useful content.** At a 320px viewport, checklist
  text and controls extended beyond the viewport (some text reached x=387px).
  With root text doubled, the sample container, home heading/action and an
  offer caption also overflowed. Explicit container sizing and wrapping now
  keep those surfaces within the viewport. Wide sample tables retain their
  own horizontal scrolling area.
- **Checkout without JavaScript had no explanation.** A visible `noscript`
  message now explains the requirement and links to the public sample and
  purchase support. The public sample itself remains readable without scripts.

## Checks added

`tests/e2e/launch-resilience.spec.js` now defines 23 cases:

- Twelve storage checks: four page-navigation checks, checklist unlock and book
  reading, each exercised with denied reads and separately with failed writes/removal.
- Five malformed-progress checks: invalid JSON, null, a string, numeric fields,
  and string booleans/object notes/unknown keys.
- JavaScript disabled: the sample is readable and checkout has a useful fallback.
- A stalled checkout times out, preserves the email and permits a controlled retry.
- A failed connection and an HTML gateway error leave checkout recoverable.
- Five principal pages fit 320px with doubled root text and reduced motion.
- A tagged social sample link survives navigation, back, forward and reload.
- A delayed fragment-focus callback cannot overwrite a later history entry.

The original 12 passed in Chromium against the source development server before
the coordinated production build. The combined release suite owns the final
built-site, cross-browser result; do not substitute this development result for it.

`tests/unit/request-json.test.mjs` adds three passing tests against a real local
HTTP server: no response headers, a response body that never completes, and
normal JSON versus an HTML gateway failure. The tests use a shorter configurable
deadline; the shipped request deadline is 30 seconds. The browser timeout check
advances browser time after observing the outgoing request.

The browser tests intercept writes and block external requests. They do not
buy, subscribe, send email or access production services. Root-font doubling is
an explicit text enlargement probe, not a claim to cover every browser zoom or
assistive technology configuration. Actual social-app webviews, screen readers,
live checkout, provider delivery and production performance still require their
own acceptance evidence.

Initial reproductions and local logs are retained in the execution workspace at
`/workspace/review/launch-second-pass/`; that directory is not part of the release.

## History race found during the combined built-site run

The first combined run exposed a WebKit mobile failure after rapidly returning
from the offer to a sample fragment and going forward again. Independent probes
reproduced it six times in 24 runs. The DOM displayed the offer while the actual
browser URL had reverted to the sample; it was not just a stale automation URL.

SvelteKit 2.70.3's `reset_focus` schedules a fragment-focus callback with
`setTimeout`. That callback calls `location.replace` and `history.replaceState`
using its original URL, even if the browser has already navigated forward.
The deferred callback therefore overwrote the newer history entry. Waiting in
the test would conceal a real navigation defect.

The latest available Kit 2 release remained 2.70.3 during this check. The related
[upstream discussion](https://github.com/sveltejs/kit/issues/16982) concerns
replacing this focus workaround; moving to Kit 3 would require a broader upgrade.
A narrow Vite transform in `scripts/vite-hash-focus-guard.mjs` instead returns
from the deferred callback if the browser URL no longer matches its target.
The existing focus behavior runs normally for the active target.

The transform applies only to the resolved Kit client runtime, requires the
reviewed function and callback shape, and fails the build if that shape changes
or the transform fails to reach a browser build. A dependency upgrade must review
and remove or update the workaround. It does not edit installed dependency files.

Five unit checks execute the actual installed function before and after the
transform, reproduce the original overwrite, preserve the active-target behavior,
and check the transform's file and source guards. All five passed. A deterministic
browser regression holds only that focus callback, navigates forward, then
releases it. It failed against the original production build at the final URL
assertion, establishing a negative control. After the coordinated rebuild, all
20 targeted checks passed across Chromium desktop/mobile, Firefox desktop and
WebKit desktop/mobile: original back/forward navigation, forced stale callback,
keyboard skip focus and unlocked reading/chapter navigation. The original URL
assertions remain unchanged. Full-suite results are tracked in PR #31's checks.

## CI follow-up: wait for completed navigation before reloading

Build-guard run 38341859024 passed the history URL assertions but WebKit mobile
reported an access-control error for the offer's same-origin `__data.json`
request. Instrumented repeats showed a different cause from the focus race above:
`goForward` returned after the history URL changed, while SvelteKit's offer data
request had only just started. Reloading 5–12ms later cancelled that request;
WebKit reported its cancellation as an access-control page error during document
teardown. The next document rendered normally.

The test now waits for the offer email field to appear and the existing navigation
loading bar to disappear before reloading. It retains every URL assertion and the
empty page-error assertion. There are no added sleeps, retries or ignored errors.
The original sequence reproduced 13 failures and 13 cancelled data requests in
24 WebKit mobile runs. The synchronized sequence passed 20 consecutive runs with
zero cancelled data requests; every forward data request completed before reload.
The social-history and deterministic stale-focus tests also passed all ten checks
across the five launch browser profiles.

The request-event negative control and comparison are retained as
`reload-probe-results.json`, `reload-synchronized-results.json` and
`reload-comparison.json` in `/workspace/review/launch-second-pass/`.

## CI follow-up: isolate storage checks under the development server

The broader WebKit workflow exhausted its 30-second budget during the two original
storage tests, which each combined six page loads and several independent user
journeys. Its development server and four workers compounded cold compilation
costs. Retried runs also sometimes clicked SSR menu controls before hydration.

Each storage mode now has separate page-navigation, checklist-unlock and reading
cases. Before exercising storage fallbacks, each waits for the existing SSR splash
node to be removed by `onMount`, proving that the client has mounted. The checks
retain the original usability, truthful-persistence and empty page-error assertions;
menu checks also confirm that Escape closes the menu. No timeout was increased.

All 12 decomposed cases passed the actual legacy development-server configuration
with four workers, zero retries and its unchanged 30-second per-test timeout.
The corresponding 24 checks also passed against the built site in WebKit desktop
and mobile. Logs are `storage-decomposed-dev.log` and
`storage-decomposed-built.log` in the same evidence directory. These are targeted
results; the coordinated release suite owns the final integrated result.

## Slow JavaScript: preserve input before hydration

Delaying the client scripts exposed a real visitor issue: Svelte's initially
empty `bind:value` erased an email or book password typed into the server-rendered
page before hydration. The checkout regression failed against the old built site
in both Chromium and WebKit. Separate negative controls reproduced the same
problem in book access and checklist signup.

The purchase page now adopts existing field values on mount, synchronizes both
email fields on input/change, and reads the submitting field before validation.
Both purchase buttons and Enter are covered. Independent review caught and fixed
the case where a populated field could be erased because the visitor had focused
the other, still-empty field. The two fields continue to work as a synchronized
pair; the test verifies actual submitted addresses, not just enabled buttons.

BookGate and EmailGate similarly preserve existing DOM values and read them again
on submission. Checklist signup preserves the visitor's explicit consent choice
and the anti-bot field. Optional updates still start unchecked. Restoring saved
checklist access still performs no new signup or email request.

The final checkout change passed 42 targeted development-server checks across
Chromium, Firefox and WebKit without retries, including the existing checkout-gate
suite. Five additional book/checklist regression cases passed in Chromium and
mobile WebKit; six focused checklist runs also passed after adding an assertion
for consent changed without a DOM event. Browser writes are intercepted locally.
After the combined production rebuild, all 105 targeted hydration, storage and
history checks passed across the five browser/device profiles without retries.
That run is recorded in `browser-hydration-final.log`. The full launch suite now
defines 245 checks; the final committed-suite results belong to PR #31's checks.

Evidence is retained in `/workspace/review/launch-second-pass/` as
`checkout-hydration-results.json`, `hydration-browser-before.log`,
`hydration-paired-browser-dev-after.log`, `input-hydration-before.log`,
`input-hydration-email-before.log`, `input-hydration-after.log` and
`input-hydration-consent-final.log`.
