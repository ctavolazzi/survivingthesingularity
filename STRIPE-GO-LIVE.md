# Stripe Go-Live Checklist — Edition Prices

**Status: LIVE AND TAKING REAL MONEY.** Production has been on live-mode keys since
some point between 2026-07-13 and 2026-07-16. Local/dev is still correctly on the
test-mode price — that part is unchanged and intentional.
Last updated: 2026-07-26.

> **Do not trust a remembered status line in this file.** It said "NOT LIVE YET" for
> ten days after the cutover actually happened, which is how the pricing defect below
> went unnoticed. Verify with `python3 scripts/sts.py stripe --live`, which probes
> production directly. A `cs_live_` session id means real cards are being charged.

## 🔴 Open defects in production (found 2026-07-26)

| # | Defect | Impact | Fix lives in |
|---|---|---|---|
| 1 | Live checkout charges **$9.00**; every page advertises **$5** | Customers are billed 80% over the advertised price | Stripe dashboard / prod env |
| 2 | `/api/webhooks/stripe` returns **503** | Paid orders are silently lost when the browser doesn't reach the success page | Prod env (`STRIPE_WEBHOOK_SECRET`) |

Neither is a code defect. `stripe-checkout/+server.js` resolves the price correctly and
the webhook handler is written correctly; both faults are in environment/dashboard
configuration. Do not "fix" them by editing application code.

### Defect 1 — the $9 / $5 gap

Confirmed by creating a real live checkout session against production and rendering the
returned Stripe page: it shows `$9.00` under the line item "Preorder Surviving the
Singularity". `$5` is what the site promises on `/`, `/about`, `/early-access` (6
places), `/checklist`, the `/book` gate hint, the Navbar CTA, and the `og:description`
social meta.

**The intended price is $5** (confirmed by the author 2026-07-26). The site copy is
correct; Stripe is wrong. Two possible causes, distinguishable only from the dashboard:

1. The live Standard price object `price_1To6muCYoTMkQm81rXG6QagG` was created at $9.
2. Production's `STRIPE_PRICE_ID_STANDARD` points at some other live price that is $9.

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

### Defect 2 — the missing webhook secret

`POST /api/webhooks/stripe` on production returns 503. In
[src/routes/api/webhooks/stripe/+server.js](src/routes/api/webhooks/stripe/+server.js)
that status is returned from exactly one branch — `if (!stripe || !WEBHOOK_SECRET)`.
Checkout works, so `STRIPE_SECRET_KEY` is set; the missing variable is
`STRIPE_WEBHOOK_SECRET`. Follow step 3 of the cutover procedure below to register the
live endpoint and set the secret. A correctly configured endpoint answers an unsigned
POST with **400** (missing signature), not 503.

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

## Cutover procedure

Steps 1 and 2 are **done** — production is live and the mock branch is correctly gated.
Step 3 is **not done** (defect 2 above). Steps 4–6 remain unverified.

1. ✅ In the production host's environment (Vercel/Cloudflare/etc.), set:
   - `STRIPE_SECRET_KEY` → the **live-mode** key
   - `STRIPE_PRICE_ID_STANDARD=price_1To6muCYoTMkQm81rXG6QagG`
   - `STRIPE_PRICE_ID_AUTHORS=price_1TogztCYoTMkQm81Nfv3uJ20` (kept set even though
     the UI doesn't expose it yet — costs nothing, keeps the backend ready)
   - Keep `STRIPE_PRICE_ID` set (fallback only; safe to point at the standard live price).
2. ✅ Make the mock-mode branch in `stripe-checkout/+server.js` unreachable in
   production. Resolved by **gating rather than removing**: the branch still exists but
   is wrapped in `if (!dev)` so production returns a 503 instead of faking a successful
   checkout. `sts.py stripe` asserts this on every run.
3. ❌ **Register the live webhook** — NOT DONE. This is defect 2 above; production
   currently 503s here.
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

## Still outstanding while live (found in the 2026-07-13 pre-flight sweep, unverified since)

These were "before go-live" items. Go-live happened without them, so they are now
running gaps on a live storefront rather than pre-launch chores. None has been verified
against the live project — checking requires Supabase and live-Stripe dashboard access.

- Run `sql/008_discord_applications.sql` in the Supabase SQL Editor. The
  `discord_applications` table doesn't exist on the live project yet, so the
  Discord application form on `/checklist` currently returns a clean "not wired up
  yet" message instead of crashing, but it still doesn't work until this runs.
- Run `sql/009_preorder_discount_code.sql` in the Supabase SQL Editor. Preorders
  work fine without it (the insert falls back gracefully), but each customer's
  personal discount code won't be generated or shown in their email until it runs.
- **Create the live-mode 50%-off promotion code.** `PREORDER50` currently only
  exists in Stripe **test** mode (created via the API on 2026-07-13: a
  `percent_off: 50, duration: once` coupon wrapped in a promotion code with that
  exact string). Live mode is a separate Stripe environment - repeat the same two
  API calls (or do it by hand in the dashboard: Product catalog → Coupons → new
  50% once coupon → Promotion codes → code `PREORDER50`) once live keys are in
  place. `MASTER_DISCOUNT_CODE` in `.env` can be overridden if you want a
  different string in live mode.
