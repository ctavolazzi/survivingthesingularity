# Payment reliability rollout

This release changes the payment contract: a verified payment gets immediate on-site access, while email fulfillment remains retryable until the provider accepts the message and the outcome is durably recorded. Provider acceptance is not inbox delivery; the Resend delivery webhook remains the delivery/bounce evidence.

## Database first

Apply `sql/017_payment_reliability.sql` before deploying this code, using a reviewed database change. It depends on the existing preorder/discount, fulfillment, transaction and webhook tables from migrations 003–014. It does **not** require account migrations 015 or 016 and does not restore accounts.

Migration 017 adds two lease fields, a preorder payment-session reference, a transaction review reason, and a checkout-reservation table. Three service-role-only functions acquire a fulfillment lease, acquire/reuse a checkout reservation, and find an existing buyer with exact case-insensitive comparison. It also disables the old fulfilled-session purge, preserving receipt recovery and idempotency records. Revisit retention explicitly before enabling any replacement purge.

The migration reopens previously processed events when the local ledger says a paid session remains unfulfilled. This enables an operator's Stripe event replay; updating a database row does not make Stripe send an already-acknowledged event again.

Use the corrected 013 included in this release if replaying prerequisites. Earlier copies unconditionally backfilled unfinished claims as delivered every time the migration ran. The corrected backfill runs only when the status column is first introduced. Always run 017 last; its retained-record behavior replaces 013's old purge definition.

The disposable PostgreSQL 17.11 integration suite passed all eight groups: prerequisite migration replay, RPC grants, concurrent claims/reservations, stale-worker fencing, exact ownership lookup, and retained receipt records. Run `python3 tests/server/payment-sql.integration.py` to reproduce it with Docker. This executes PL/pgSQL; it does not establish the hosted project's existing grants, PostgREST configuration or migration state.

## Environment and deployment checks

The paid flow requires working Stripe keys/webhook secret and edition-specific price IDs, Supabase service-role access, the reviewed bundle in Supabase Storage, and a Resend key with a verified sender. `DOWNLOAD_BUCKET`, `DOWNLOAD_BUNDLE_PATH`, `DOWNLOAD_BUNDLE_SHA256` and `DOWNLOAD_BUNDLE_BOOK_VERSION` must match the active bundle manifest. Use `publication/PRIVATE-BUNDLE.md` to upload without overwriting and verify the remote bytes before configuring checkout. New hosted checkouts allow synchronous card payments only. Historical asynchronous sessions with terminal payment failures need operator review before releasing their reservation; pending payments must remain blocked against a second charge. Both the webhook and success page verify this product and edition metadata before granting a new entitlement. The new code fails closed when the required storage or ledger cannot be used. No missing-key or synthetic waitlist/mock branch can mint a production download. Development mocks also avoid real storage.

After deploying a preview with **test-mode credentials**, perform a Stripe test checkout with a test card and a verified test mailbox. Confirm the signed webhook, financial row, lease outcome, provider message ID, email content, receipt recovery, book code and bundle all correspond to that same session. Use a fresh test email for a new purchase: TEST_REPEAT_PURCHASE_EMAIL no longer deletes existing order rows. Repeat with two tabs to check that they share the same open checkout. Test provider and database failures, then retry the same signed event. Finally verify a production-mode invalid signature is rejected and production test branches cannot grant access. Do not describe local mocks as this service integration test.

## Recovery and monitoring

The included `.github/workflows/payment-reconciliation.yml` calls the protected `/api/admin/reconcile` endpoint hourly after this release reaches the default branch. Set its `ADMIN_RECONCILE_TOKEN` secret to match hosting and enable failure notifications in GitHub. Verify a successful manual run and monitor for missing scheduled runs. You can also call the endpoint on another monitored schedule with `Authorization: Bearer <ADMIN_RECONCILE_TOKEN>`. Configure the token and scheduling secret in the hosting/CI secret stores, never in source. Treat a non-2xx response, `ok:false`, a missing scheduled run, or a nonzero `count` as needing attention. `?alert=1` additionally attempts an admin email; a failed email must not be the monitor's only signal.

The report combines the local unfinished-payment backlog, duplicate-payment review flags, and a Stripe comparison for the preceding **seven days of checkout creation**, excluding the configured grace window. It scans at most 1,000 Stripe sessions and 100 rows per local backlog query; hitting a cap reports an incomplete check rather than an all-clear. Older payments and delayed methods paid long after checkout creation need a separate historical Stripe export comparison. Existing purchases lacking this product's metadata are not included in the external scan.

For a verified paid, undelivered order, replay its authentic `checkout.session.completed` or `checkout.session.async_payment_succeeded` event through Stripe's dashboard/CLI, then verify the ledger, fulfillment state and provider message. If an old event remains marked processed while delivery is unresolved, inspect the records and reset that event to failed before replay; do not manufacture a payment or mark an unverified order delivered. A missing customer email requires a human support resolution.

A `possible_duplicate_payment` flag means inspect both Stripe charges and refund the extra payment if warranted. The flag is conservative for pre-migration orders without a session reference. Clear `checkout_transactions.review_reason` only after recording the reviewed outcome in the operational support record. Automatic refunds are not implemented.

A checkout reservation with no attached session and age over 23 hours is intentionally blocked: the application cannot safely infer whether a previous Stripe create request succeeded after Stripe's 24-hour idempotency retention expires. An operator must find the corresponding Stripe session and attach it, or confirm no payable/paid session remains before clearing the reservation. Ordinary open sessions are reused, and confirmed expired sessions rotate automatically.

Fulfillment leases last two minutes and use a fencing token on outcome writes. Automatic emails use a stable session/purpose Resend idempotency key; Resend retains it for 24 hours. A prolonged ambiguous send or a template change during retry can require operator review. This is bounded duplicate suppression, not an exactly-once inbox-delivery claim.

## Local regression evidence

Run:

```sh
node --experimental-vm-modules tests/server/payment-reliability.test.mjs
```

The suite evaluates actual server source with explicit database, Stripe, and Resend doubles; network requests are forbidden. It covers failure and in-flight outcomes, webhook retry status, production mock rejection, verified access recovery, provider idempotency options, concurrent checkout reservation use, and Stripe/local reconciliation. Live provider behavior, SQL locks/grants, migrations and actual mail delivery are separate release checks above.
