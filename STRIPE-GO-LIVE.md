# Stripe Go-Live Checklist — Edition Prices

**Status: NOT LIVE YET.** Local/dev is intentionally still on the test-mode price.
Last updated: 2026-07-02.

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
   - `STRIPE_PRICE_ID_AUTHORS=price_1TogztCYoTMkQm81Nfv3uJ20`
   - Keep `STRIPE_PRICE_ID` set (fallback only; safe to point at the standard live price).
2. Remove the mock-mode branch in `stripe-checkout/+server.js` (marked with a
   "Remove the mock branch before launch" comment) so misconfigured env fails loudly
   instead of faking success.
3. Do a real end-to-end purchase of EACH edition in production:
   - Standard → confirm research-bundle email + preorder confirmation.
   - Author's → confirm copy number is assigned and appears in the confirmation +
     download emails ("copy #N of 100").
4. Confirm the success page fulfillment ([early-access/success/+page.server.js](src/routes/early-access/success/+page.server.js))
   reads `edition_type` from the live session metadata.
5. Leave local `.env` on the test price so dev never touches live checkout.

Do NOT change component code for the cutover — edition selection and linking are already
wired; the switch is environment-variable-only (plus removing the mock branch).
