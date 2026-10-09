# Stripe Go-Live Checklist — Edition Prices

**Status: LIVE. The storefront is taking real money and fulfilling orders.**
Cutover completed 2026-08-01 evening. Local/dev remains on the test-mode price, which
is unchanged and intentional.
Last updated: 2026-08-01 (cutover verified end to end).

> **Do not trust a remembered status line in this file, including this one.** It said
> "NOT LIVE YET" for ten days after the cutover actually happened, then "LIVE AND
> TAKING REAL MONEY" after production had been rolled back, then "BACK ON TEST-MODE
> KEYS" for the first hours of taking live payments. Three wrong readings, all written
> in good faith. Verify with `python3 scripts/sts.py stripe --live`, which probes
> production directly. A `cs_live_` session id means real cards are being charged;
> `cs_test_` means they are not.

## Verified production state (2026-08-01, cutover night)

Verified against completed orders rather than a probe reading.

| Signal | Reading | Means |
|---|---|---|
| Checkout session id | `cs_live_…` | Real cards are being charged |
| Advertised vs charged | $5.00 vs $5.00 | No price drift |
| Signed webhook probe | **200** | Signature verification genuinely runs |
| `fulfilled_sessions` | `status=delivered`, `attempts=1`, `last_error=null` | The order completed, first try |
| `checkout_transactions` | `status=completed`, `fulfilled=true` | Paid AND received, recorded separately |
| Statement descriptor | `STS-SINGULARITY` | Recognisable on a bank statement |

Fulfillment ran in under four seconds from Stripe event to `delivered`, unattended,
on the first attempt. Order-level identifiers are deliberately not recorded here: this
file is in a public repository and Stripe object ids are customer-linked. Reconcile
against the Stripe dashboard instead.

### What this means

The two defects logged on 2026-07-26 — the $9-vs-$5 overcharge and the 503 webhook —
are both resolved, and the storefront is now live. The overcharge window was audited
directly against the Stripe API afterwards: the account has only ever carried three
live charges, all on cutover night, so **nobody was overcharged and there is nothing
to refund**.

**Whether that rollback was deliberate is unknown and was not verified.** Pulling live
keys would be a sound deliberate response to an 80% overcharge; an accidental revert of
the env vars would look identical from outside. Either way the consequence is the same
and it is the thing that matters: **the store currently collects nothing.** A real
customer reaches a test-mode Stripe page, and a real card is declined there. If the
rollback was accidental, note that it also silently un-fixed nothing — the $9 price may
still be waiting on the live price object.

So this is no longer a defect list. It is a **re-cutover**: the remaining work is to put
live keys back with the price verified at $5 *before* they go in, so the overcharge
cannot recur. See "Re-cutover checklist" below.

None of *this* is a code defect: `stripe-checkout/+server.js` resolves the price
correctly, and the mode/price faults have all been environment or dashboard
configuration. Do not "fix" those by editing application code.

**But do not generalize that.** This paragraph used to also assert "the webhook handler
is written correctly," and that sentence is why nobody read the handler for weeks while
it rejected every event Stripe sent. It was a code defect, in application code, and it
was the most expensive one in the project. See "Resolved 2026-07-28" below. A prior
claim that an area is clean is not evidence about that area.

### History: the $9 / $5 gap (live window 2026-07-13 → 2026-07-26)

**No longer reproducible** — production now charges $5, matching the site. Kept because
the cause was never identified from the dashboard, so it can recur the moment live keys
go back in. Read this before re-cutting over.

As observed while live: creating a real live checkout session against production and
rendering the returned Stripe page showed `$9.00` under the line item "Preorder
Surviving the Singularity". `$5` is what the site promises on `/`, `/about`,
`/early-access` (6 places), `/checklist`, the `/book` gate hint, the Navbar CTA, and the
`og:description` social meta.

**The intended price is $5** (confirmed by the author 2026-07-26). The site copy is
correct; Stripe is wrong. Two possible causes, distinguishable only from the dashboard:

1. ~~The live Standard price object `price_1To6muCYoTMkQm81rXG6QagG` was created at $9.~~
   **Ruled out 2026-07-26.** The live dashboard shows that price at **$5.00 USD**
   one-time, default price on product `prod_UniDSzyaLPPGZY` ("Surviving the
   Singularity: Pre-Order the First Edition", Active), created 6/30/26 6:53 PM. It is
   live-mode data: price ids are mode-scoped, so a live id returns no result when
   searched in test mode.

   A price's **`unit_amount` is not updatable** in the Stripe API — you cannot edit
   $9 into $5 — and this object has no `currency_options` entries that could carry a
   second amount. So it was never $9.

   Its log does show two `POST /v1/prices/{id}` calls after creation (7/2/26 9:34 AM and
   **7/26/26 7:38 PM**). Those can only have touched mutable fields — `active`,
   `nickname`, `metadata`, `tax_behavior`, `lookup_key` — never the amount. Worth
   knowing that the 7/26 one lands about 90 minutes before production was observed back
   on test keys; if that edit was not deliberate, find out what made it.
2. ✅ **This is the cause.** Production was pointing at some *other* live price object
   that is $9. The $5 price was correct the whole time; the environment was aimed at
   the wrong one.

   **Prime suspect: the Author's Edition price** `price_1TogztCYoTMkQm81Nfv3uJ20` on
   `prod_UoJdPeLmMWnpsL`. It is the other live price this project owns, it is a
   higher-tier product, and `STRIPE_PRICE_ID` — the shared fallback that a missing
   `STRIPE_PRICE_ID_STANDARD` silently drops through to — is exactly the kind of
   variable that ends up pointing at it. **Check that price's unit amount first.** If it
   reads $9, the whole incident is explained and no unknown price object is loose in the
   catalog.

### The silent fallback that makes cause 2 possible

[src/routes/api/stripe-checkout/+server.js](src/routes/api/stripe-checkout/+server.js)
resolves the price as:

```js
standard: env.STRIPE_PRICE_ID_STANDARD || PRICE_ID,   // PRICE_ID = env.STRIPE_PRICE_ID
```

If `STRIPE_PRICE_ID_STANDARD` is unset — or misspelled, or dropped during an env edit —
checkout does not fail. It silently falls through to `STRIPE_PRICE_ID` and charges
whatever that points at, with no error anywhere. That is a plausible mechanism for an
$9 charge against a $5 catalog, and it will still be there at the next cutover.

**Before re-cutover, decide what `STRIPE_PRICE_ID` should hold.** Either point it at the
same $5 price so the fallback is harmless, or remove it and make a missing
`STRIPE_PRICE_ID_STANDARD` fail loudly in production the way the mock branch already
does. A fallback that quietly charges a different amount than the site advertises is
worse than a 503.

**Still to find:** the $9 price object itself. It is presumably still live and still
selectable. Locate it via Payments (below) — open any $9 charge and read which price it
used — then archive it.

**To fix:** open the Stripe dashboard in **live mode** and read the unit amount on
`price_1To6muCYoTMkQm81rXG6QagG`.

- If it reads **$9** → Stripe prices are immutable, so create a **new** live price at
  $5.00 USD one-time on product `prod_UniDSzyaLPPGZY`, then set
  `STRIPE_PRICE_ID_STANDARD` in the production environment to the new id and redeploy.
  Archive the $9 price so it can't be selected again.
- If it reads **$5** → the price object is fine and production's
  `STRIPE_PRICE_ID_STANDARD` (or the `STRIPE_PRICE_ID` fallback it silently drops
  through to) is pointing somewhere else. Correct the env var and redeploy.

Afterwards, re-run `python3 scripts/sts.py stripe --live`; it compares the amount
actually charged against the amount the site advertises and exits non-zero if they
disagree.

**Also check whether anyone was overcharged.** Stripe Dashboard → Payments, live mode,
filtered to since the cutover. Any successful $9 payment is a customer owed a $4 refund
and an apology.

### Resolved 2026-07-28: the webhook had never verified a single event

**Corrected.** This section used to say a 400 on an unsigned POST "proves both
`STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` are set and signature verification is
running." The first half was true. The second half was wrong, and it was wrong for
weeks across three audits.

The endpoint was rejecting **every** event, including correctly signed ones. From the
Cloudflare runtime's own log:

```text
[webhook] signature verification failed: CryptoProvider cannot be used in a
synchronous context. Use `await constructEventAsync(...)` instead of `constructEvent(...)`
```

Production runs on the Cloudflare Workers runtime, so the bundler resolves Stripe's
`workerd` export condition and the SDK's crypto provider is SubtleCrypto, which is
async-only. The synchronous `constructEvent` threw before it ever compared a signature.
The secret was never the problem; every secret failed identically. Consequence: the
webhook never fulfilled an order. All fulfillment to date came from the success page, so
any customer who closed the tab, or paid with a delayed method, was charged and never
fulfilled. Impact was zero only because production is on test keys.

Fixed in `aea146e` (`await constructEventAsync`, plus a catch that separates
"verification could not run" from "signature rejected"), cherry-picked to main as
`dcc7809` and deployed 2026-07-28.

**Verified in production, not inferred.** A correctly signed benign event
(`payment_intent.created`, deliberately a type the handler does not act on, so a valid
signature cannot fulfil anything) returns `200 {"received":true}`, and the request logs
no error line at all. That also settles a second question: the `whsec_…` in `.env`
**matches** the one in Cloudflare, which a 400 alone could never have told us.

> **The lesson worth keeping.** A 400 is what a *correctly configured* webhook returns
> to an unsigned POST, and also what a webhook whose verifier cannot run returns to
> *everything*. Those two look identical from outside. `sts stripe --live` printed
> "HTTP 400 <- OK: configured" and every audit believed it. The check now sends a
> signed event and requires a 200 before it will say VERIFIED; a rejection is an error
> and an unprovable state is a warning, never a clean bill of health. When a check says
> something is fine, ask what observation would look identical if it were broken.

What is proven above is proven for **test mode only**, and the reason is the next
paragraph.

> ⚠️ **This does not carry over to live mode.** Stripe signing secrets are per-endpoint
> *and* per-mode. Production is on test keys, so the `whsec_…` currently set is almost
> certainly the **test-mode** endpoint's. Re-cutting over to live keys without also
> swapping in the **live** endpoint's signing secret puts the webhook straight back into
> silent failure — except worse than a 503: every real Stripe delivery would fail
> signature verification with a 400, and Stripe would retry and then give up. Treat
> "webhook secret is set" as mode-specific, never as done.

**Launch scope:** going live with the Standard Edition only. The Author's Edition
toggle was removed from the UI in the single-offer cut (2026-07-12); the price ID
and Stripe backend support for it still exist and work, there's just no button
that calls it right now.

## Current state

- Checkout ([src/routes/api/stripe-checkout/+server.js](src/routes/api/stripe-checkout/+server.js))
  selects a price per edition via `STRIPE_PRICE_ID_STANDARD` / `STRIPE_PRICE_ID_AUTHORS`,
  falling back to the shared `STRIPE_PRICE_ID` when unset.
- The UI (early-access page edition toggle + `?edition=authors` deep link from /book and
  /launch) already lets users pick either edition; `edition_type` flows into Stripe
  session metadata and drives copy numbering + edition-specific emails.
- Local `.env` points BOTH edition vars at the test-mode price
  (`price_1To6noCYoTMkQm81oN2Zcgsp`) because `STRIPE_SECRET_KEY` there is a
  test-mode restricted key. Both flows verified working against test mode on 2026-07-02.

## Live products (created in the Stripe dashboard, live mode)

| Edition | Product | Price ID |
|---|---|---|
| Standard ("Singularity Pre-Order Standard Edition") | `prod_UniDSzyaLPPGZY` | `price_1To6muCYoTMkQm81rXG6QagG` |
| Author's ("Singularity Pre-Order Author's Edition") | `prod_UoJdPeLmMWnpsL` | `price_1TogztCYoTMkQm81Nfv3uJ20` |

These are also kept as commented lines in `.env`.

## Re-cutover checklist

Production is on **test** keys (verified 2026-07-26). Work these in order. Do not skip
step 0 — it is the step whose absence caused the overcharge.

- [ ] **0. Verify the live price reads $5 BEFORE any key goes in.** Stripe dashboard,
      **live mode**, open `price_1To6muCYoTMkQm81rXG6QagG`. If it is not $5.00 USD
      one-time, create a new live price at $5.00 on product `prod_UniDSzyaLPPGZY`,
      archive the wrong one, and use the new id below. Prices are immutable — you cannot
      edit $9 into $5.
- [~] **1. Audit the previous live window for overcharges.** Stripe → Payments, live
      mode, 2026-07-13 → 2026-07-26. Every successful $9 payment is a customer owed a $4
      refund and an apology.
      - **Strong evidence the answer is zero.** The 2026-07-26 Supabase backup
        (`~/Backups/sts-supabase/2026-07-26/tables/`) shows all **9**
        `fulfilled_sessions` rows carrying `cs_test_` session ids — not one `cs_live_`,
        across the entire history. `preorders` holds 3 rows: two `test@example.com`
        dummies from 06-27, and one self-test from the author's own address on 07-14,
        also via a test session. No real customer appears to have ever completed a
        purchase.
      - **Do not close this on that evidence alone.** The backup was taken 13:10 on
        07-26, so it cannot see a payment made later that day. Worse,
        `fulfilled_sessions` only records orders that were *fulfilled*, and for part of
        the live window the webhook was returning 503 — precisely the condition under
        which a paid order leaves no row. Absence of rows is weakest exactly where it
        matters most. The Stripe Payments dashboard is the only authoritative source.
        Check it, then mark this `[x]` with the number.
- [ ] **2. Set the live env vars** in Cloudflare (see step 1 of the procedure below),
      and in the same change flip `EXPECTED_MODE` from `test` to `live` in
      [.github/workflows/stripe-guard.yml](.github/workflows/stripe-guard.yml). That
      workflow probes production daily and fails whenever the real mode stops matching
      the declared one — it is what would have caught both the silent cutover and the
      silent rollback. Leaving it on `test` after going live means it alarms every day
      for the wrong reason; leaving it on `live` after a rollback is exactly the alarm
      you want.
- [ ] **3. Register the LIVE webhook endpoint** and set its own `whsec_…` — the
      test-mode secret currently in place will not verify live traffic. See the warning
      under "Resolved 2026-07-28: the webhook had never verified a single event".
      After swapping the secret, re-prove it the same way that section describes:
      `sts stripe --live` must print VERIFIED, not merely HTTP 400.
- [x] **4. Supabase migrations: verified applied 2026-08-01.** Every migration in
      `sql/` has been run on the live project *except* `014_webhook_events.sql`. This
      was checked directly against `information_schema`, not inferred:
      `checkout_transactions` (`013`) exists **and** carries all four durability
      columns (`status`, `completed_at`, `last_error`, `attempts`), and `002`, `008`,
      `009`, `010`, `011` are all present.
      - **The list this step used to carry was stale.** It read `002`, `008`, `009`,
        `010` "as of 2026-07-28", and had been wrong long enough to send a session
        hunting four problems that did not exist while saying nothing about `013` and
        `014`, the two that could actually have hurt. If you edit this step again,
        re-verify against the database rather than copying the previous list forward.
      - **`014` is the only real gap, and it does not block go-live.** Verified in
        code, not assumed from the comment: `beginEvent` returns `proceed: true` on any
        non-`23505` insert error (`webhookEvents.js:72`) and on a throw (`:121`), so a
        missing `webhook_events` table degrades open and never stalls a paid order.
        Duplicate protection also survives at the session layer, where `claimSession`
        checks `fulfilled_sessions`. What is lost is the audit trail and the
        unfinished-events queue, which is operational visibility rather than
        customer-facing correctness. Run it soon; do not delay a cutover for it.
- [ ] **5. Create `PREORDER50` in live mode** — it exists only in test mode.
- [ ] **6. Re-probe:** `python3 scripts/sts.py stripe --live` must report `mode live`,
      webhook configured, and no price drift.
- [ ] **7. One real purchase with a real card**, then confirm every downstream effect
      (steps 4–5 of the procedure below).

## Cutover procedure

Reference detail for the checklist above. Step 2 (mock gating) is a permanent code
property and stays done. Every other step must be redone for the re-cutover, because
production was rolled back to test keys.

1. ⬜ In the production host's environment (**Cloudflare** — confirmed from response
   headers; adapter-auto resolves to the Cloudflare adapter), set:
   - `STRIPE_SECRET_KEY` → the **live-mode** key
   - `STRIPE_PRICE_ID_STANDARD=price_1To6muCYoTMkQm81rXG6QagG`
   - `STRIPE_PRICE_ID_AUTHORS=price_1TogztCYoTMkQm81Nfv3uJ20` — **currently not set in
     production** (confirmed via `wrangler pages secret list`). It used to not matter,
     because the endpoint fell back to the shared `STRIPE_PRICE_ID`; that fallback is
     now dev-only, so the `authors` path returns 503 until this is set. That is
     deliberate: the fallback meant an Author's Edition sale billed the *standard*
     price, and `edition_type` is accepted from any caller regardless of what the UI
     exposes. Set it if you want the edition sellable; leave it unset to keep the
     path closed.
   - Keep `STRIPE_PRICE_ID` set (fallback only; safe to point at the standard live price).
2. ✅ Make the mock-mode branch in `stripe-checkout/+server.js` unreachable in
   production. Resolved by **gating rather than removing**: the branch still exists but
   is wrapped in `if (!dev)` so production returns a 503 instead of faking a successful
   checkout. `sts.py stripe` asserts this on every run.
3. ⬜ **Register the live webhook.** A secret is set today, but for test mode — see the
   warning above. This must be redone against the live-mode endpoint.
   - Stripe Dashboard → Developers → Webhooks → Add endpoint →
     `https://survivingthesingularity.com/api/webhooks/stripe`
   - Events: `checkout.session.completed` and `checkout.session.async_payment_succeeded`
   - Copy the signing secret Stripe gives you (`whsec_...`) into the production
     environment as `STRIPE_WEBHOOK_SECRET`. The value in local `.env` right now is a
     self-generated placeholder for local testing only — it will not verify real
     Stripe traffic and must be replaced with the real one.
   - Without this step, the site still works for the common case (customer's browser
     reaches the success page), but a dropped connection or closed tab right after
     paying will silently lose the order. See `src/lib/server/fulfillment.js` and
     `src/routes/api/webhooks/stripe/+server.js`.
4. Do a real end-to-end purchase in production with the Standard Edition:
   confirm the download+confirmation email and the admin alert
   (`admin@johnnyautoseed.com`) both arrive, and confirm a `preorders` row exists.
5. Confirm the success page fulfillment ([early-access/success/+page.server.js](src/routes/early-access/success/+page.server.js))
   reads `edition_type` from the live session metadata.
6. Leave local `.env` on the test price so dev never touches live checkout.

Do NOT change component code for the cutover — edition selection and linking are already
wired; the switch is environment-variable-only (plus removing the mock branch and
registering the webhook above).

## Still outstanding (found in the 2026-07-13 pre-flight sweep, unverified since)

**Updated 2026-08-01: most of this section is no longer outstanding.** The live schema
was queried directly against `information_schema` on that date. Every Supabase item
below has been run except `sql/014_webhook_events.sql`. What genuinely remains is the
live-Stripe work, which still needs dashboard access.

The original framing is kept below rather than deleted, because the gap between what
this section claimed and what the database actually contained is the useful part: it
went unchecked from 2026-07-13 to 2026-08-01, and in that time it was wrong in both
directions.

- **DONE (verified 2026-08-01).** `sql/008_discord_applications.sql` has been run:
  `discord_applications` exists on the live project, so the Discord application form on
  `/checklist` is wired up rather than returning its "not wired up yet" message.
  **Note (2026-07-26):** this file was referenced by this doc, by `SITEMAP.md`, and by
  `009`'s own header, but had never actually been written: it was absent from the
  working tree *and* from all of git history. It now exists.
  **Correction (2026-08-01):** this note previously claimed migrations `001`, `003`,
  `004`, `006`, `007` were still missing from `sql/`. They are all present. `sql/` now
  holds a complete `001` through `014`, so the directory can rebuild a Supabase project
  from scratch, and the live schema is no longer the only source of truth
  for those.
- **DONE (verified 2026-08-01).** `sql/009_preorder_discount_code.sql` has been run:
  `preorders.discount_code` exists, so each customer's personal discount code is
  generated and shown in their email. The graceful fallback in `fulfillment.js` that
  retries the insert without the column is now belt-and-braces rather than load-bearing.
- **Still outstanding: `sql/014_webhook_events.sql`.** The only migration not yet run.
  Non-blocking for go-live (see step 4 of the re-cutover checklist for the verification),
  but it is what gives you the event audit trail and the unfinished-events queue.
- **Create the live-mode 50%-off promotion code.** `PREORDER50` currently only
  exists in Stripe **test** mode (created via the API on 2026-07-13: a
  `percent_off: 50, duration: once` coupon wrapped in a promotion code with that
  exact string). Live mode is a separate Stripe environment - repeat the same two
  API calls (or do it by hand in the dashboard: Product catalog → Coupons → new
  50% once coupon → Promotion codes → code `PREORDER50`) once live keys are in
  place. `MASTER_DISCOUNT_CODE` in `.env` can be overridden if you want a
  different string in live mode.
