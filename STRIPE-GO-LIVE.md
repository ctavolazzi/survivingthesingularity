# Stripe Go-Live Checklist — Edition Prices

**Status: NOT LIVE YET.** Local/dev is intentionally still on the test-mode price.
Last updated: 2026-07-13.

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

## When it's time to go live

1. In the production host's environment (Vercel/Cloudflare/etc.), set:
   - `STRIPE_SECRET_KEY` → the **live-mode** key
   - `STRIPE_PRICE_ID_STANDARD=price_1To6muCYoTMkQm81rXG6QagG`
   - `STRIPE_PRICE_ID_AUTHORS=price_1TogztCYoTMkQm81Nfv3uJ20` (kept set even though
     the UI doesn't expose it yet — costs nothing, keeps the backend ready)
   - Keep `STRIPE_PRICE_ID` set (fallback only; safe to point at the standard live price).
2. Remove the mock-mode branch in `stripe-checkout/+server.js` (marked with a
   "Remove the mock branch before launch" comment) so misconfigured env fails loudly
   instead of faking success.
3. **Register the live webhook** (new step, 2026-07-13 — this did not exist before):
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

## Also needed before go-live (unrelated to Stripe, found in the 2026-07-13 pre-flight sweep)

- Run `sql/008_discord_applications.sql` in the Supabase SQL Editor. The
  `discord_applications` table doesn't exist on the live project yet, so the
  Discord application form on `/checklist` currently returns a clean "not wired up
  yet" message instead of crashing, but it still doesn't work until this runs.
