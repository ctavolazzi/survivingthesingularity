#!/usr/bin/env node
/**
 * REGRESSION PROBE: THE MALFORMED-TIMESTAMP BYPASS
 *
 * B-09 was fixed in 6899e43 and was still bypassable. This probe is the thing
 * that caught it, and it is in the repo because the pure-logic spec CANNOT
 * catch this class on its own: the bug lives in the seam between stripe-node's
 * parser and ours, so only an end-to-end request through the real handler
 * exercises it. A stripe-node upgrade could reintroduce it and every unit test
 * would stay green.
 *
 * THE BUG, as measured before the fix: `t=abc` and `t=` both returned 200 with
 * a signature the handler accepted.
 *
 * THE MECHANISM, read out of node_modules/stripe/cjs/Webhooks.js:
 *
 *   parseHeader        `accum.timestamp = parseInt(kv[1], 10)`, no validity
 *                      check, defaulting to -1 when `t` is absent.
 *   makeHMACContent    signs the PARSED value back:
 *                      `${details.timestamp}.${payload}`
 *   validateComputed   `timestampAge = now - details.timestamp;`
 *                      `if (tolerance > 0 && timestampAge > tolerance) throw`
 *
 * So `t=abc` parses to NaN, an attacker signs over the literal string
 * "NaN.{body}", and the tolerance test becomes `NaN > 300`, which is false.
 * Stripe's past-side check does not fire, and the old freshness guard degraded
 * open on anything it could not parse, so neither did ours. The payload had no
 * time bound in either direction, which is exactly the unbounded-validity
 * window B-09 exists to close.
 *
 * THE FIX is the split between ABSENT and MALFORMED in webhookFreshness.js.
 * Absent degrades open (a Stripe-side format change worth surviving); present
 * but unparseable fails shut (a chosen input Stripe cannot produce with a valid
 * signature).
 *
 * SETUP, same as probe-stripe-webhook.mjs. Both values may be fake, because
 * signature verification never calls the Stripe API:
 *
 *   cat > .env <<'EOF'
 *   STRIPE_SECRET_KEY=sk_test_probe0000000000000000000000000
 *   STRIPE_WEBHOOK_SECRET=whsec_localprobe0000000000000000000000
 *   EOF
 *   npm run dev -- --port 5174
 *   node scripts/probe-webhook-timestamp-bypass.mjs
 *   rm .env      # DELETE IT AFTERWARDS
 *
 * THE CONTROLS ARE NOT DECORATION. Without them a handler that 400s everything
 * would "pass" this probe while being completely broken, which is the exact
 * false-pass family this project has now caught six times. Control 1 in
 * particular is the one that matters most: it proves a WELL-FORMED request is
 * still accepted, so the fix did not close the bypass by breaking the money
 * path. If control 1 ever goes red, stop and revert.
 */
import { createHmac } from 'node:crypto';

const URL = process.env.PROBE_URL || 'http://localhost:5174/api/webhooks/stripe';
const SECRET = process.env.STRIPE_WEBHOOK_SECRET || 'whsec_localprobe0000000000000000000000';
const now = () => Math.floor(Date.now() / 1000);

const body = JSON.stringify({
  id: 'evt_bypass_probe',
  type: 'checkout.session.completed',
  livemode: false,
  // Deliberately unpaid: this probe is about the signature and timestamp layer,
  // and an unpaid session exercises it without touching the ledger or fulfillment.
  data: { object: { id: 'cs_bypass_probe', payment_status: 'unpaid' } }
});

// Signs over an ARBITRARY prefix, because the attack turns on stripe rebuilding
// the signed string from its own parseInt result rather than from the raw header.
const hmac = (prefix) => createHmac('sha256', SECRET).update(`${prefix}.${body}`).digest('hex');

const results = [];

async function send(label, header, expect, why) {
  const res = await fetch(URL, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'stripe-signature': header },
    body
  });
  const text = (await res.text()).slice(0, 70);
  const pass = res.status === expect;
  results.push(pass);
  console.log(`  ${pass ? 'PASS' : 'FAIL'}  ${label}`);
  console.log(`        expected ${expect}, got ${res.status}  ${text}`);
  console.log(`        ${why}`);
  return res.status;
}

console.log(`probing ${URL}\n`);
console.log('--- CONTROLS: without these a 400-everything handler would look clean ---');
await send(
  'well-formed current timestamp -> 200',
  `t=${now()},v1=${hmac(now())}`,
  200,
  'THE CRITICAL CONTROL. Proves the fix did not close the bypass by breaking checkout.'
);
await send(
  'well-formed t+600 -> 400',
  `t=${now() + 600},v1=${hmac(now() + 600)}`,
  400,
  'The original B-09 case. Should read "Timestamp out of tolerance".'
);
await send(
  'no t= at all -> 400',
  `v1=${hmac(-1)}`,
  400,
  'Stripe defaults timestamp to -1 and its own tolerance rejects that as ancient.'
);

console.log('\n--- THE BYPASS: non-numeric t, signed over the literal "NaN" ---');
await send(
  't=abc -> 400',
  `t=abc,v1=${hmac(NaN)}`,
  400,
  'Returned 200 before the fix, defeating this guard AND stripe tolerance at once.'
);
await send(
  't= (empty) -> 400',
  `t=,v1=${hmac(NaN)}`,
  400,
  'parseInt("") is also NaN, so the empty value is the same attack.'
);
await send(
  't=123abc -> 400',
  `t=123abc,v1=${hmac(123)}`,
  400,
  'stripe parseInt yields 123 (ancient) so stripe rejects it first. Our parser also refuses it.'
);

console.log(`\n${results.filter(Boolean).length}/${results.length} assertions passed`);
process.exit(results.every(Boolean) ? 0 : 1);
