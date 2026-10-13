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

`tests/e2e/launch-resilience.spec.js` now defines 13 cases:

1. Storage reads denied: navigation, checklist unlock and book reading remain usable.
2. Storage writes/removal fail: the same paths work without false persistence promises.
3. Invalid JSON recovers without falsely completed steps.
4. A stored null recovers safely.
5. A stored string recovers safely.
6. Numeric checklist fields do not become completed steps or notes.
7. String booleans, object notes and unknown keys recover safely.
8. JavaScript disabled: the sample is readable and checkout has a useful fallback.
9. A stalled checkout times out, preserves the email and permits a controlled retry.
10. A failed connection and an HTML gateway error leave checkout recoverable.
11. Five principal pages fit 320px with doubled root text and reduced motion.
12. A tagged social sample link survives navigation, back, forward and reload.
13. A delayed fragment-focus callback cannot overwrite a later history entry.

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
