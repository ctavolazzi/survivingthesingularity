#!/usr/bin/env node
/**
 * PROBE THE STRIPE WEBHOOK WITH FORGED SIGNATURES
 *
 * Verifies the webhook handler end to end against a running dev server, without
 * Stripe and without a database. It computes real HMAC-SHA256 signatures itself,
 * so the handler's actual verification path runs rather than being bypassed.
 *
 * WHY THIS FILE IS IN THE REPO
 *
 * It was originally written in a scratch directory during the 2026-07-29 session
 * and would have died with it. It is the only cheap way to verify a change to the
 * webhook without a live Stripe endpoint, and it is what a future session needs to
 * confirm a fix for plan item B-09. Rebuilding it costs more than keeping it.
 *
 * SETUP, INCLUDING THE PART THAT IS EASY TO GET WRONG
 *
 * The handler refuses to run at all unless STRIPE_SECRET_KEY and
 * STRIPE_WEBHOOK_SECRET are both set, returning 503. So a temporary .env is
 * required, and both values may be fake because signature verification never
 * calls the Stripe API:
 *
 *   cat > .env <<'EOF'
 *   STRIPE_SECRET_KEY=sk_test_probe0000000000000000000000000
 *   STRIPE_WEBHOOK_SECRET=whsec_localprobe0000000000000000000000
 *   EOF
 *   npm run dev -- --port 5174
 *   node scripts/probe-stripe-webhook.mjs
 *   rm .env      # DELETE IT AFTERWARDS
 *
 * Port 5174, not 5173: a stale `python -m http.server` has been squatting 5173,
 * and playwright.config.js sets reuseExistingServer true, so anything pointed at
 * 5173 may silently talk to the squatter instead of the app.
 *
 * With no SUPABASE_* vars set, `supabaseAdmin` is null and every database path
 * no-ops. That is deliberate here: it proves the handler degrades open rather
 * than throwing when its bookkeeping tables are unreachable.
 *
 * WHAT A PASS MEANS AND WHAT IT DOES NOT
 *
 * Passing proves signature verification, the routing of each event type, the
 * response codes, and that the new event-bookkeeping layer does not throw. It
 * proves NOTHING about the database writes, because there is no database. Do not
 * read a clean run here as evidence that fulfillment works.
 *
 * The five negative controls are not optional decoration. A handler that returned
 * 200 to everything would pass all four positive checks, so without the controls
 * a clean run and a broken-open handler look identical.
 */
import { createHmac } from 'node:crypto';

const PORT = process.env.PROBE_PORT || '5174';
const SECRET =
  process.env.STRIPE_WEBHOOK_SECRET ||
  'whsec_localprobe0000000000000000000000';
const URL = `http://localhost:${PORT}/api/webhooks/stripe`;

/**
 * Stripe's signature scheme: HMAC-SHA256 over "<timestamp>.<raw body>", hex, in a
 * `t=...,v1=...` header. The raw body bytes matter: a JSON parse and re-stringify
 * would change key order and break the HMAC, which is why the handler reads the
 * request as text.
 */
function sign(payload, tsSeconds, secret = SECRET) {
  const sig = createHmac('sha256', secret)
    .update(`${tsSeconds}.${payload}`)
    .digest('hex');
  return `t=${tsSeconds},v1=${sig}`;
}

function evt(id, type, obj = {}) {
  return JSON.stringify({
    id,
    type,
    livemode: false,
    created: Math.floor(Date.now() / 1000),
    data: { object: { id: 'cs_test_probe_1', object: 'checkout_session', ...obj } }
  });
}

const now = () => Math.floor(Date.now() / 1000);
const results = [];

async function post(name, { payload, header, expect }) {
  const headers = { 'content-type': 'application/json' };
  if (header !== null) headers['stripe-signature'] = header;
  let res, body;
  try {
    res = await fetch(URL, { method: 'POST', headers, body: payload });
    body = await res.text();
  } catch (e) {
    console.log(`  ERROR ${name}: ${e.message}`);
    console.log(`        Is the dev server up on :${PORT}?`);
    results.push(false);
    return false;
  }
  const ok = res.status === expect;
  results.push(ok);
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}`);
  console.log(`        expected ${expect}, got ${res.status}  ${body.slice(0, 130)}`);
  return ok;
}

const paid = {
  payment_status: 'paid',
  customer_details: { email: 'probe@survivingthesingularity.com', name: 'Probe' },
  metadata: { edition_type: 'standard' },
  amount_total: 500,
  currency: 'usd'
};

const p1 = evt('evt_probe_paid_1', 'checkout.session.completed', paid);
const p2 = evt('evt_probe_unpaid_1', 'checkout.session.completed', { payment_status: 'unpaid' });
const p3 = evt('evt_probe_other_1', 'payment_intent.created', {});
const p4 = evt('evt_probe_expired_1', 'checkout.session.expired', {});

console.log(`probing ${URL}\n`);
console.log('--- POSITIVE: the handler is alive and processes valid signed events ---');
await post('valid signature, paid session -> 200', { payload: p1, header: sign(p1, now()), expect: 200 });
await post('valid signature, unpaid session -> 200', { payload: p2, header: sign(p2, now()), expect: 200 });
await post('valid signature, unhandled event type -> 200', { payload: p3, header: sign(p3, now()), expect: 200 });
await post('valid signature, expired session -> 200', { payload: p4, header: sign(p4, now()), expect: 200 });

console.log('\n--- NEGATIVE CONTROLS: these are what make the 200s above mean anything ---');
await post('no stripe-signature header -> 400', { payload: p1, header: null, expect: 400 });
await post('garbage signature -> 400', { payload: p1, header: 't=1,v1=deadbeef', expect: 400 });
await post('signature from the WRONG secret -> 400', { payload: p1, header: sign(p1, now(), 'whsec_wrongsecret000000000000000000000'), expect: 400 });
await post('valid signature for a DIFFERENT payload -> 400', { payload: p1, header: sign(p2, now()), expect: 400 });
await post('timestamp 600s in the PAST -> 400', { payload: p1, header: sign(p1, now() - 600), expect: 400 });

/**
 * B-09. Stripe's constructEvent enforces its tolerance on the PAST side only, so a
 * future-dated timestamp currently sails through. Measured at 200 on 2026-07-29.
 *
 * When B-09 is fixed, flip this expectation to 400. Until then a 200 here is the
 * bug reproducing, which is why it is labelled rather than counted as a pass.
 */
console.log('\n--- B-09: future-dated timestamp (200 = bug still present) ---');
const B09_EXPECT = Number(process.env.B09_EXPECT || 200);
await post(`timestamp 600s in the FUTURE -> ${B09_EXPECT}`, { payload: p1, header: sign(p1, now() + 600), expect: B09_EXPECT });
console.log(
  B09_EXPECT === 200
    ? '        200 means B-09 is unfixed, which was the state on 2026-07-29.\n' +
      '        After fixing it, re-run with B09_EXPECT=400.'
    : '        Expecting 400, so B-09 is being verified as fixed.'
);

console.log(`\n${results.filter(Boolean).length}/${results.length} assertions passed`);
process.exit(results.every(Boolean) ? 0 : 1);
