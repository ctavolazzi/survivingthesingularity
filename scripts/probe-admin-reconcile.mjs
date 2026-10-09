#!/usr/bin/env node
/**
 * PROBE THE ADMIN RECONCILIATION ENDPOINT
 *
 * Verifies the auth boundary in front of /api/admin/reconcile against a running
 * dev server. That endpoint returns customer email addresses joined to payment
 * references, so its guard is worth probing over real HTTP rather than trusting
 * the unit tests on adminToken.js alone.
 *
 * Kept in the repo because it was written in a scratch directory on 2026-07-29
 * and would otherwise have been lost. Re-run it after any change to the endpoint,
 * the token guard, or the reconciliation query.
 *
 * RUN IT IN BOTH CONFIGURATIONS. ONE ALONE PROVES HALF THE THING.
 *
 *   # Phase 1: no token configured. Must serve NOTHING to anyone.
 *   npm run dev -- --port 5174
 *   node scripts/probe-admin-reconcile.mjs
 *
 *   # Phase 2: token configured. Only the exact token gets in.
 *   echo "ADMIN_RECONCILE_TOKEN=probe$(printf 'k%.0s' {1..40})" >> .env
 *   # restart the dev server so it picks the var up, then:
 *   PROBE_TOKEN="probe$(printf 'k%.0s' {1..40})" node scripts/probe-admin-reconcile.mjs
 *   rm .env
 *
 * The token must be at least 32 characters or the guard refuses to operate at all
 * and answers 503, by design: see MIN_TOKEN_LENGTH in src/lib/server/adminToken.js.
 *
 * WHAT THE CORRECT-TOKEN CASE ASSERTS, AND WHY IT EXPECTS 503
 *
 * With no SUPABASE_* vars the reconciliation check CANNOT RUN. The required
 * behaviour is 503 with `ok:false` and `count:null` plus an explicit
 * not-an-all-clear note. It must never answer 200 with `count:0`, because a
 * monitor that cannot run and a monitor that found nothing are the same shape on
 * the wire, and conflating them is how a broken alarm reads as silence.
 *
 * Once sql/014 has been applied and SUPABASE_* is configured, the correct-token
 * case flips to 200. Set EXPECT_DB=1 to assert that instead.
 */
const PORT = process.env.PROBE_PORT || '5174';
const URL = `http://localhost:${PORT}/api/admin/reconcile`;
const TOKEN = process.env.PROBE_TOKEN || '';
const EXPECT_DB = process.env.EXPECT_DB === '1';

const results = [];

async function probe(name, { header, expect, expectBody }) {
  const headers = {};
  if (header) headers.authorization = header;
  let res, body;
  try {
    res = await fetch(URL, { headers });
    body = await res.text();
  } catch (e) {
    console.log(`  ERROR ${name}: ${e.message}`);
    console.log(`        Is the dev server up on :${PORT}?`);
    results.push(false);
    return false;
  }
  const ok = res.status === expect && (expectBody ? body.includes(expectBody) : true);
  results.push(ok);
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}`);
  console.log(`        want ${expect}${expectBody ? ` + "${expectBody}"` : ''}, got ${res.status}  ${body.slice(0, 120)}`);
  return ok;
}

console.log(`probing ${URL}`);

if (!TOKEN) {
  console.log('\n--- PHASE 1: no PROBE_TOKEN given, so asserting the UNSET-token contract ---');
  console.log('    (if the server DOES have a token set, these will fail: that is the point)\n');
  await probe('no header -> 503 Not configured', { header: null, expect: 503, expectBody: 'Not configured' });
  await probe('a 40-char bearer token -> 503 Not configured', { header: `Bearer ${'z'.repeat(40)}`, expect: 503, expectBody: 'Not configured' });
  await probe('empty bearer -> 503 Not configured', { header: 'Bearer ', expect: 503, expectBody: 'Not configured' });
  console.log('\n    An unset secret authorising nobody is the single most important');
  console.log('    behaviour here. It is the classic route to a world-readable admin endpoint.');
} else {
  console.log(`\n--- PHASE 2: token supplied (${TOKEN.length} chars), asserting only it gets in ---\n`);
  await probe('no header -> 401', { header: null, expect: 401, expectBody: 'Unauthorized' });
  await probe('wrong token -> 401', { header: `Bearer ${'z'.repeat(TOKEN.length)}`, expect: 401, expectBody: 'Unauthorized' });
  await probe('correct token minus its last char -> 401', { header: `Bearer ${TOKEN.slice(0, -1)}`, expect: 401, expectBody: 'Unauthorized' });
  await probe('correct token plus a char -> 401', { header: `Bearer ${TOKEN}x`, expect: 401, expectBody: 'Unauthorized' });
  await probe('wrong scheme -> 401', { header: `Basic ${TOKEN}`, expect: 401, expectBody: 'Unauthorized' });

  if (EXPECT_DB) {
    await probe('correct token, database present -> 200', { header: `Bearer ${TOKEN}`, expect: 200, expectBody: '"ok":true' });
    console.log('\n    A count of 0 here is a genuine all-clear ONLY because ok is true.');
  } else {
    await probe('correct token, no database -> 503 ok:false', { header: `Bearer ${TOKEN}`, expect: 503, expectBody: '"ok":false' });
    await probe('correct token, must NOT claim count 0', { header: `Bearer ${TOKEN}`, expect: 503, expectBody: '"count":null' });
    await probe('correct token, carries the not-an-all-clear note', { header: `Bearer ${TOKEN}`, expect: 503, expectBody: 'not an all-clear' });
    console.log('\n    These three are the anti-false-pass contract: a check that could not');
    console.log('    run must not be reportable as a clean result. Set EXPECT_DB=1 once');
    console.log('    sql/014 is applied and SUPABASE_* is configured.');
  }
}

console.log(`\n${results.filter(Boolean).length}/${results.length} assertions passed`);
process.exit(results.every(Boolean) ? 0 : 1);
