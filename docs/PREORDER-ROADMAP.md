# Pre-Order & Payments Roadmap

Status: PLANNED — not yet implemented.
Current: Email waitlist only (`/api/waitlist` → Supabase `waitlist` table).

---

## Phase 1 (done): Email waitlist

- Capture email + source in Supabase `waitlist` table
- No payment, no auth required
- Notify list on book release via email service (TBD: Resend, Postmark, etc.)

---

## Phase 2 (next): Stripe pre-order

### What we need

| Item | Detail |
|------|--------|
| Stripe account | Under the LLC (not personal) |
| Product | "Surviving the Singularity — Book" |
| Price | One-time, TBD amount |
| `STRIPE_SECRET_KEY` | Server-only, never public |
| `STRIPE_PRICE_ID` | The price object ID from Stripe dashboard |
| `PUBLIC_BASE_URL` | For redirect URLs after checkout |

### New routes to build

```
/preorder                → Marketing page with Stripe Checkout button
/api/checkout            → POST: create Stripe Checkout Session, return URL
/preorder/success        → Thank-you page (Stripe redirects here after payment)
/preorder/cancel         → Cancelled page (Stripe redirects here on back)
/api/webhooks/stripe     → POST: handle Stripe events (payment_intent.succeeded, etc.)
```

### Fulfillment flow

1. User clicks "Pre-order" on `/preorder`
2. POST `/api/checkout` → creates Stripe Checkout Session
3. User completes payment on Stripe-hosted page
4. Stripe redirects to `/preorder/success?session_id=...`
5. Stripe webhook fires `checkout.session.completed`
6. `/api/webhooks/stripe` verifies signature, inserts order into `orders` table
7. Send confirmation email (Resend or Postmark)

### Supabase tables needed

```sql
-- orders: one row per completed purchase
create table public.orders (
  id uuid default gen_random_uuid() primary key,
  stripe_session_id text not null unique,
  stripe_payment_intent text,
  email text not null,
  amount_cents integer not null,
  currency text not null default 'usd',
  status text not null default 'pending', -- pending | paid | refunded
  created_at timestamptz default now() not null
);
-- RLS: no anon access; service role only via webhook handler
```

### Security notes

- Webhook endpoint MUST verify `stripe-signature` header before trusting payload
- `STRIPE_SECRET_KEY` and webhook signing secret are server-only env vars
- Never put Stripe secret key in any `PUBLIC_` env var

---

## Phase 3 (future): User accounts + purchase history

- Supabase Auth (email magic link)
- Link orders to user accounts (`orders.user_id` FK)
- `/profile` page showing purchase history and book download link

See CLAUDE.md for the full auth route plan.
