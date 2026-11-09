# Operations record: 24 and 25 October 2026

What one Claude Code cloud session changed or found in this site's production setup, with the
evidence. Written 2026-11-09 at the owner's request, from the session's record. The business side
of the same session (offers, posts, videos, schedule) is in `ctavolazzi/_workbench`,
`sessions/2026-10-24-book-orders-and-launch-plan/SESSION_LOG.md`.

| Field | Value |
|---|---|
| Session | Claude Code cloud session `session_01JdN6Rtt8Qc7Du2bhBkpa77` |
| Commits in this repo | `df34e3f6` (merged to `main`, deployed), `e62bed18` (draft PR #35, closed without merging 2026-11-09, reverted on its branch) |
| Production systems changed | Supabase project `StS-redux`: migrations 014 and 017 applied 2026-10-25 with the owner's approval |
| Not changed | Cloudflare settings, Stripe, storage objects. The session had no access to change them |

## 1. Production database: migrations 014 and 017 applied (2026-10-25)

**Found:** production `StS-redux` had never received `014` (the Stripe event ledger) or `017`
(payment reliability). The current code calls into both: checkout reserves through
`reserve_checkout`, fulfillment claims each paid session through `claim_fulfillment_session`,
lookups use `find_preorder`, and the webhook and the reconciliation monitor read and write
`webhook_events` and `unreconciled_paid_sessions`. Without them, those calls return errors, and
the event history `docs/payment-reliability-rollout.md` relies on was not being kept.

**Applied** with the Supabase connector's migration tool, owner approval given in the session:

| Applied as | Contents |
|---|---|
| `014_webhook_events` | `webhook_events` table, its indexes and row-level security; the `unreconciled_paid_sessions` view |
| `017_payment_reliability` | lease columns, `payment_session_id`, `review_reason`; `claim_fulfillment_session`; `checkout_reservations` and `reserve_checkout`; `find_preorder`; `delete_old_fulfilled_sessions` as a no-op; one index |

The files' own `begin`/`commit` lines and trailing verification selects were left out, because
the tool wraps each migration in its own transaction. **Checked after:** row counts in the existing
tables were the same before and after; the new objects are service-role only; the
`unreconciled_paid_sessions` view returned 0 rows.

**Not applied:** `015` and `016`. They serve the admin activation-codes route, not the order path.

**Not done:** a real paid order traced end to end through the event ledger, the claim, the email
and the download.

## 2. FogSift Prompt Pack gift file (`df34e3f6`, deployed 2026-10-25)

The pack is the owner's thank-you gift for $5 preorder buyers. It is served from
`static/gifts/` under an unguessable file name, with no link to it anywhere on the site, and this
block in `_headers`:

```
# Gifts sent by email to existing buyers (the FogSift Prompt Pack). Unlinked,
# unguessable file names, and kept out of search results.
/gifts/*
  X-Robots-Tag: noindex, nofollow
```

The link was tested locally before merging, and one test email carrying it went only to
`info@survivingthesingularity.com`. No buyer emails were sent by the session.

The deploy guard failed once on this commit with "Address already in use" in
`scripts/check-cloudflare-runtime.mjs` (a port collision). The same commit had passed
on its branch run, and a re-run passed.

## 3. The paid download zip is not in storage (found 2026-10-25)

**Found:** the active `src/lib/data/bundleManifest.js` names
`research-bundle-book-v0.11.0.zip` (28,280,000 bytes, SHA-256 `8b437b324b07...`). The
`downloads` bucket held only `research-bundle-v1.zip` (June 2026) and backups. The reviewed zip
lives in the git-ignored `book-build/`, so it existed only on the machine that built it.

**Effect:** `src/lib/server/bundleRelease.js` refuses checkout unless `DOWNLOAD_BUCKET`,
`DOWNLOAD_BUNDLE_PATH`, `DOWNLOAD_BUNDLE_SHA256` and `DOWNLOAD_BUNDLE_BOOK_VERSION` match the
manifest. So, depending on those Cloudflare settings (a session cannot read them), checkout
either answers "Checkout is temporarily unavailable" or takes payment and cannot sign a download.

**Tried:** rebuilding the zip in the cloud workspace.

1. Installed the PDF engine: `apt-get install --no-install-recommends texlive-xetex
   texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended lmodern`, plus
   `poppler-utils` for page images. Pandoc 3.1.3, `bs4` and `pypdf` were already present.
2. `python3 scripts/prepare-book-bundle.py` passed. Every input hash matched. Only
   `The-Precedent-File.pdf` had new bytes (89,308 to 91,271, from a different XeLaTeX build). Its
   text proof passed (227 source blocks, none missing), and pages 1 and 7 were checked by eye. New
   zip: 28,281,967 bytes, SHA-256 `545e6d1412ce2437800c4c2661a0addc26071116cc5337a3c9ec0ddfa295e4b9`.
   `build_bonus.py` already notes that the zip is not byte-reproducible, so a new hash was
   expected.
3. With the manifest pointed at it: `node scripts/deploy-book-bundle.mjs --local` verified;
   `node --test scripts/deploy-book-bundle.test.mjs` 5/5; `npm run check` 0 errors;
   `npm run test:release`, `npm run build` and `npm run test:cloudflare` passed.
   `npm run test:launch-browser` did not run: all 250 tests failed to launch, because the pinned
   Playwright wanted `chromium_headless_shell-1208` and the container had a different build.
4. Pushed as `e62bed18`, opened as draft PR #35, and sent the zip to the owner.

**Outcome:** the owner chose not to use a rebuilt bundle (2026-11-09) and closed PR #35 without
merging. `e62bed18` is reverted on `claude/recent-commits-recap-ts0xcd`, so `main` and the active
manifest are unchanged. As of the session, the reviewed file was still not in storage; this record
does not re-check it.

## 4. Recurring alert emails (diagnosed 2026-10-25)

- **Payment reconciliation** (scheduled workflow) failed every hour because the GitHub secret
  `ADMIN_RECONCILE_TOKEN` was empty. It needs the same value as the hosting setting of that name.
  Not set by the session (no access).

## 5. Email sending health (measured 2026-10-25, Resend connector)

`survivingthesingularity.com` is verified for sending. The last 30 days showed 502 bounces and 2
complaints. Because of that, the planned release announcement was limited to recent opt-ins and
buyers (about 18 addresses) rather than the older list.

## Notes for the next cloud session

- PDF builds need the TeX packages in section 3 installed first; they are not in the base image.
- The browser suite needs the exact browser build the pinned Playwright expects.
- The deploy guard's port race can fail a good commit once; a pass on the same commit settles it.
