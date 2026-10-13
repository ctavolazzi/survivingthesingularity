import test from 'node:test';
import assert from 'node:assert/strict';
import { loadSource, query } from './load-source.mjs';

const env = { STRIPE_SECRET_KEY: 'sk_test_local_regression', STRIPE_WEBHOOK_SECRET: 'whsec_local_regression' };
const json = (body, options) => new Response(JSON.stringify(body), { ...options, headers: { 'content-type': 'application/json' } });
const paid = { id: 'cs_test_paid', mode: 'payment', payment_status: 'paid', status: 'complete', customer_email: 'buyer@example.test', metadata: { product: 'early-access-bundle-v1', edition_type: 'standard' } };

async function fulfillmentHarness({ claim, send = async () => ({ ok: true }), outcomeError, preorderError,
  bundle = { ok: true, path: 'reviewed-bundle.zip', bucket: 'downloads' } } = {}) {
  const outcomes = [], sends = [];
  const database = {
    rpc: async () => claim ?? { data: { state: 'claimed', lease_token: 'lease-current' }, error: null },
    storage: { from: () => ({ createSignedUrl: async () => ({ data: { signedUrl: 'https://storage.example.test/download' } }) }) },
    from: (table) => query((calls) => {
      if (table === 'fulfilled_sessions') {
        outcomes.push(calls);
        return outcomeError ? { error: { message: 'db offline' } } : { data: [{ session_id: paid.id }] };
      }
      if (table === 'preorders') return { data: { copy_number: 1, discount_code: 'ABC123' }, error: preorderError };
      throw new Error(`Unexpected table ${table}`);
    }),
  };
  const mod = await loadSource('src/lib/server/fulfillment.js', {
    '$env/dynamic/private': { env }, '$lib/server/supabaseAdmin.js': { supabaseAdmin: database },
    '$lib/server/bundleRelease.js': { currentBundleRelease: () => bundle },
    '$lib/server/email.js': {
      sendDownloadEmail: async (payload) => { sends.push(payload); return send(payload); },
      sendAdminPreorderAlert: async () => ({ ok: true }),
    },
  });
  return { mod, outcomes, sends, database, fulfill: () => mod.fulfillPreorder({ sessionId: paid.id, email: 'Buyer@Example.test', editionType: 'standard' }) };
}

test('database claim errors are retryable, never already delivered', async () => {
  const h = await fulfillmentHarness({ claim: { error: { message: 'missing migration' } } });
  const result = await h.fulfill();
  assert.equal(result.state, 'retryable_failure');
  assert.equal(result.alreadyFulfilled, false);
  assert.equal(h.sends.length, 0);
});

test('in-flight and already-delivered claims remain different outcomes', async () => {
  for (const state of ['in_flight', 'already_delivered']) {
    const h = await fulfillmentHarness({ claim: { data: { state } } });
    const result = await h.fulfill();
    assert.equal(result.state, state);
    assert.equal(result.alreadyFulfilled, state === 'already_delivered');
    assert.equal(h.sends.length, 0);
  }
});

test('provider errors, skipped sends and undefined results never complete fulfillment', async () => {
  for (const response of [{ error: { message: 'provider unavailable' } }, { skipped: true }, undefined]) {
    const h = await fulfillmentHarness({ send: async () => response });
    const result = await h.fulfill();
    assert.equal(result.state, 'retryable_failure');
    assert.equal(result.delivered, false);
    assert.equal(h.outcomes[0].find(([key]) => key === 'update')[1].status, 'failed');
  }
});

test('outcome write is fenced by the acquired lease and provider key is stable', async () => {
  const h = await fulfillmentHarness();
  const result = await h.fulfill();
  assert.equal(result.state, 'accepted');
  assert.equal(h.sends[0].to, 'buyer@example.test');
  assert.equal(h.sends[0].idempotencyKey, `fulfillment/${paid.id}/download`);
  assert(h.outcomes[0].some(([op, key, value]) => op === 'eq' && key === 'lease_token' && value === 'lease-current'));
  assert(h.outcomes[0].some(([op, key, value]) => op === 'eq' && key === 'status' && value === 'claimed'));
});

test('accepted email with failed outcome persistence remains retryable', async () => {
  const h = await fulfillmentHarness({ outcomeError: true });
  assert.equal((await h.fulfill()).state, 'retryable_failure');
});

test('preorder persistence failure does not send a false confirmation', async () => {
  const h = await fulfillmentHarness({ preorderError: { code: '42501', message: 'permission denied' } });
  assert.equal((await h.fulfill()).state, 'retryable_failure');
  assert.equal(h.sends.length, 0);
});

test('unconfirmed bundle release never signs old storage or accepts fulfillment', async () => {
  const h = await fulfillmentHarness({ bundle: { ok: false, error: 'Bundle release not configured' } });
  h.database.storage.from = () => { throw new Error('Old archive must never be accessed'); };
  assert.equal(await h.mod.getBundleUrl(), null);
  assert.equal((await h.fulfill()).state, 'retryable_failure');
  assert.equal(h.sends.length, 0);
});

test('storage transport failures return unavailable access and retryable fulfillment', async () => {
  const h = await fulfillmentHarness();
  h.database.storage.from = () => ({ createSignedUrl: async () => { throw new Error('Network unavailable'); } });
  assert.equal(await h.mod.getBundleUrl(), null);
  assert.equal((await h.fulfill()).state, 'retryable_failure');
  assert.equal(h.sends.length, 0);
});

async function webhookHarness({ result = { state: 'accepted' }, disposition = { proceed: true }, ledger = { configured: true, ok: true }, throwFulfill = false, session = paid, fulfillment = null } = {}) {
  const counts = { processed: 0, failed: 0, fulfilled: 0, sent: 0 };
  class Stripe { constructor() { this.webhooks = { constructEventAsync: async () => ({ id: 'evt_test', type: 'checkout.session.completed', data: { object: session } }) }; } }
  const mod = await loadSource('src/routes/api/webhooks/stripe/+server.js', {
    '@sveltejs/kit': { json }, '$env/dynamic/private': { env }, stripe: { default: Stripe },
    '$lib/server/fulfillment.js': { fulfillPreorder: async () => { counts.sent++; if (throwFulfill) throw new Error('offline'); return fulfillment ? fulfillment() : result; } },
    '$lib/server/transactions.js': {
      recordCheckoutCompleted: async () => ledger, recordCheckoutExpired: async () => {},
      markTransactionFulfilled: async () => { counts.fulfilled++; return { ok: true }; },
    },
    '$lib/server/webhookEvents.js': {
      beginEvent: async () => disposition, markEventProcessed: async () => { counts.processed++; },
      markEventFailed: async () => { counts.failed++; },
    },
    '$lib/server/webhookFreshness.js': { checkFreshness: () => ({ ok: true }) },
  });
  const response = await mod.POST({ request: new Request('https://site.example.test/api/webhooks/stripe', { method: 'POST', headers: { 'stripe-signature': 'signed-by-mock' }, body: '{}' }) });
  return { response, counts };
}

test('webhook requests retry for failed or in-flight fulfillment, never marks processed', async () => {
  for (const state of ['retryable_failure', 'in_flight', undefined]) {
    const { response, counts } = await webhookHarness({ result: { state } });
    assert.equal(response.status, 500);
    assert.equal(counts.failed, 1);
    assert.equal(counts.processed, 0);
    assert.equal(counts.fulfilled, 0);
  }
});

test('webhook only acknowledges terminal fulfillment and repairs its financial flag', async () => {
  for (const state of ['accepted', 'already_delivered']) {
    const { response, counts } = await webhookHarness({ result: { state } });
    assert.equal(response.status, 200);
    assert.equal(counts.processed, 1);
    assert.equal(counts.fulfilled, 1);
  }
});

test('event replay in flight retries; processed duplicate is acknowledged', async () => {
  const pending = await webhookHarness({ disposition: { proceed: false, duplicate: false, reason: 'in-flight' } });
  assert.equal(pending.response.status, 500);
  assert.equal(pending.counts.sent, 0);
  const done = await webhookHarness({ disposition: { proceed: false, duplicate: true } });
  assert.equal(done.response.status, 200);
  assert.equal(done.counts.sent, 0);
});

test('webhook refuses missing financial storage before customer email is sent', async () => {
  const { response, counts } = await webhookHarness({ ledger: { ok: true, configured: false } });
  assert.equal(response.status, 500);
  assert.equal(counts.sent, 0);
});

async function successHarness({ dev = false, secret = env.STRIPE_SECRET_KEY, verified = paid, database = null } = {}) {
  const calls = { stripe: 0, bundle: 0, fulfill: 0 };
  class Stripe { constructor() { this.checkout = { sessions: { retrieve: async () => { calls.stripe++; return verified; } } }; } }
  const mod = await loadSource('src/routes/early-access/success/+page.server.js', {
    '@sveltejs/kit': { redirect: (status, location) => ({ status, location }) },
    '$app/environment': { dev }, '$env/dynamic/private': { env: { STRIPE_SECRET_KEY: secret } }, stripe: { default: Stripe },
    '$lib/bookAccessCode.js': { BOOK_ACCESS_PASSWORD: 'shared-reading-code' },
    '$lib/server/supabaseAdmin.js': { supabaseAdmin: database },
    '$lib/server/fulfillment.js': {
      getBundleUrl: async () => { calls.bundle++; return 'https://storage.example.test/download'; },
      fulfillPreorder: async () => { calls.fulfill++; return { state: 'retryable_failure' }; },
    },
    '$lib/server/transactions.js': {
      recordCheckoutCompleted: async () => ({ ok: true, configured: true }), markTransactionFulfilled: async () => ({ ok: true }),
    },
  });
  return { calls, load: (id) => mod.load({ url: new URL(`https://site.example.test/early-access/success?session_id=${id}`) }) };
}

test('production mock/waitlist IDs cannot mint storage URLs or claim payment', async () => {
  for (const id of ['waitlist', 'mock_session', 'mock_probe', '']) {
    const h = await successHarness();
    await assert.rejects(h.load(id), (error) => error.status === 302);
    assert.equal(h.calls.bundle, 0);
    assert.equal(h.calls.stripe, 0);
  }
});

test('missing Stripe credentials fail closed without an independent paid record', async () => {
  const h = await successHarness({ secret: '' });
  assert.equal((await h.load('cs_test_unverified')).ok, false);
  assert.equal(h.calls.bundle, 0);
});

test('development mock never uses real download storage', async () => {
  const h = await successHarness({ dev: true, secret: '' });
  const result = await h.load('mock_session');
  assert.equal(result.mock, true);
  assert.equal(result.bundleUrl, null);
  assert.equal(h.calls.bundle, 0);
});

test('verified customer keeps download and book access when email fulfillment fails', async () => {
  const h = await successHarness();
  const result = await h.load(paid.id);
  assert.equal(result.ok, true);
  assert.equal(result.emailStatus, 'retryable_failure');
  assert.equal(result.bookAccessPassword, 'shared-reading-code');
  assert.equal(h.calls.fulfill, 1);
});

test('permanent paid ledger recovers access without claiming email delivery', async () => {
  const h = await successHarness({ secret: '', database: { from: () => query({ data: { session_id: paid.id, email: paid.customer_email } }) } });
  const result = await h.load(paid.id);
  assert.equal(result.ok, true);
  assert.equal(result.recovered, true);
  assert.equal(result.emailStatus, 'unknown');
});

test('concurrent checkout requests share a provider idempotency key', async () => {
  const keys = [], attachments = [];
  const database = {
    rpc: async () => ({ data: { reservation_key: 'reservation-1', created_at: new Date().toISOString() } }),
    from: () => query({ data: [{ session_id: 'cs_shared' }] }, (op, args) => { if (op === 'update') attachments.push(args[0]); }),
  };
  const stripe = { checkout: { sessions: { create: async (_params, options) => { keys.push(options.idempotencyKey); return { id: 'cs_shared', url: 'https://checkout.example.test/shared' }; } } } };
  const { getOrCreateCheckout } = await loadSource('src/lib/server/checkoutReservations.js', { '$lib/server/supabaseAdmin.js': { supabaseAdmin: database } });
  const args = { stripe, email: 'buyer@example.test', editionType: 'standard', params: { customer_email: 'buyer@example.test' } };
  const sessions = await Promise.all([getOrCreateCheckout(args), getOrCreateCheckout(args)]);
  assert.deepEqual(keys, ['checkout/reservation-1', 'checkout/reservation-1']);
  assert.equal(sessions[0].id, sessions[1].id);
  assert.equal(attachments.length, 2);
});

test('open checkout is reused and completed checkout never creates another charge', async () => {
  for (const status of ['open', 'complete']) {
    let created = 0;
    const database = { rpc: async () => ({ data: { reservation_key: 'key', session_id: 'cs_existing', created_at: new Date().toISOString() } }) };
    const { getOrCreateCheckout } = await loadSource('src/lib/server/checkoutReservations.js', { '$lib/server/supabaseAdmin.js': { supabaseAdmin: database } });
    const stripe = { checkout: { sessions: { retrieve: async () => ({ id: 'cs_existing', status }), create: async () => { created++; } } } };
    const result = await getOrCreateCheckout({ stripe, email: 'buyer@example.test', editionType: 'standard', params: {} });
    assert.equal(created, 0);
    assert.equal(status === 'open' ? result.id : result.pendingPayment, status === 'open' ? 'cs_existing' : true);
  }
});

test('ambiguous checkout older than provider idempotency retention fails closed', async () => {
  const database = { rpc: async () => ({ data: { reservation_key: 'old', created_at: '2020-01-01T00:00:00Z' } }) };
  const { getOrCreateCheckout } = await loadSource('src/lib/server/checkoutReservations.js', { '$lib/server/supabaseAdmin.js': { supabaseAdmin: database } });
  await assert.rejects(getOrCreateCheckout({ stripe: {}, email: 'buyer@example.test', editionType: 'standard', params: {} }), /reconciliation/);
});

test('real email module passes automatic fulfillment idempotency to Resend, not manual resends', async () => {
  const requests = [];
  class Resend { constructor() { this.emails = { send: async (payload, options) => { requests.push({ payload, options }); return { data: { id: 'email_mock' } }; } }; } }
  const { sendDownloadEmail } = await loadSource('src/lib/server/email.js', {
    '$env/dynamic/private': { env: { RESEND_API_KEY: 'mock-api-key', EMAIL_POSTAL_ADDRESS: 'Regression fixture' } },
    '$env/dynamic/public': { env: {} },
    resend: { Resend }, '$lib/server/supabaseAdmin.js': { supabaseAdmin: null },
    '$lib/bookAccessCode.js': { BOOK_ACCESS_PASSWORD: 'test-reading-code' },
  });
  const args = { to: 'buyer@example.test', sessionId: paid.id, edition_type: 'standard', copy_number: null, discount_code: 'EXAMPLE' };
  assert.equal((await sendDownloadEmail({ ...args, idempotencyKey: 'fulfillment/cs_test/download' })).ok, true);
  assert.equal(requests[0].options.idempotencyKey, 'fulfillment/cs_test/download');
  assert(requests[0].payload.text.includes('https://survivingthesingularity.com/early-access/success'));
  await sendDownloadEmail(args);
  assert.equal(requests[1].options, undefined);
});

test('missing provider acceptance ID is an email failure even without an explicit error', async () => {
  class Resend { constructor() { this.emails = { send: async () => ({ data: null, error: null }) }; } }
  const { sendDownloadEmail } = await loadSource('src/lib/server/email.js', {
    '$env/dynamic/private': { env: { RESEND_API_KEY: 'mock-api-key' } },
    '$env/dynamic/public': { env: {} },
    resend: { Resend }, '$lib/server/supabaseAdmin.js': { supabaseAdmin: null },
    '$lib/bookAccessCode.js': { BOOK_ACCESS_PASSWORD: 'test-reading-code' },
  });
  const result = await sendDownloadEmail({ to: 'buyer@example.test', sessionId: paid.id, edition_type: 'standard' });
  assert.equal(result.ok, undefined);
  assert.match(result.error.message, /acceptance ID/);
});

test('public email origin keeps receipt, reading and unsubscribe links in the configured preview', async () => {
  const requests = [];
  class Resend { constructor() { this.emails = { send: async (payload) => { requests.push(payload); return { data: { id: 'email_mock' } }; } }; } }
  const { sendDownloadEmail, sendWelcomeEmail } = await loadSource('src/lib/server/email.js', {
    '$env/dynamic/private': { env: { RESEND_API_KEY: 'mock-api-key' } },
    '$env/dynamic/public': { env: { PUBLIC_BASE_URL: 'https://candidate.project.pages.dev/' } },
    resend: { Resend }, '$lib/server/supabaseAdmin.js': { supabaseAdmin: null },
    '$lib/bookAccessCode.js': { BOOK_ACCESS_PASSWORD: 'test-reading-code' },
  });
  await sendDownloadEmail({ to: 'buyer@example.test', sessionId: 'cs_test_preview', edition_type: 'standard' });
  await sendWelcomeEmail({ to: 'buyer@example.test', unsubscribeToken: 'a&b' });
  assert(requests[0].text.includes('https://candidate.project.pages.dev/early-access/success?session_id=cs_test_preview'));
  assert(requests[0].html.includes('href="https://candidate.project.pages.dev/book"'));
  assert(requests[1].text.includes('https://candidate.project.pages.dev/unsubscribe?token=a%26b'));
  assert(requests[1].html.includes('href="https://candidate.project.pages.dev/book"'));
});

test('unsafe configured email origins never send a customer link', async () => {
  for (const base of ['http://sender.com', 'https://name:password@sender.com', 'https://sender.com/wrong-path', 'not a URL']) {
    let sends = 0;
    class Resend { constructor() { this.emails = { send: async () => { sends++; return { data: { id: 'email_mock' } }; } }; } }
    const { sendDownloadEmail } = await loadSource('src/lib/server/email.js', {
      '$env/dynamic/private': { env: { RESEND_API_KEY: 'mock-api-key' } },
      '$env/dynamic/public': { env: { PUBLIC_BASE_URL: base } },
      resend: { Resend }, '$lib/server/supabaseAdmin.js': { supabaseAdmin: null },
      '$lib/bookAccessCode.js': { BOOK_ACCESS_PASSWORD: 'test-reading-code' },
    });
    await assert.rejects(sendDownloadEmail({ to: 'buyer@example.test', sessionId: paid.id, edition_type: 'standard' }), /HTTPS site origin/);
    assert.equal(sends, 0);
  }
});

const configuredPurchaseEmail = { RESEND_API_KEY: 're_0123456789abcdefghij', EMAIL_FROM: 'STS <books@survivingthesingularity.com>' };

async function checkoutHarness({ dev = false, credentials = true, checked = true, bundleReady = true,
  emailConfig = configuredPurchaseEmail, publicEmailConfig = {}, checkoutEnv = {}, alreadyOwned = false } = {}) {
  const calls = { lookup: 0, checkout: 0, bundle: 0, resend: 0 };
  class Stripe {}
  const mod = await loadSource('src/routes/api/stripe-checkout/+server.js', {
    '@sveltejs/kit': { json }, '$app/environment': { dev },
    '$env/dynamic/private': { env: credentials ? { ...env, STRIPE_PRICE_ID_STANDARD: 'price_fixture', ...emailConfig, ...checkoutEnv } : {} },
    '$env/dynamic/public': { env: publicEmailConfig },
    stripe: { default: Stripe },
    '$lib/server/sameOrigin.js': { isSameOrigin: () => true },
    '$lib/server/rateLimit.js': { rateLimit: () => ({ allowed: true }) },
    '$lib/server/checkoutReservations.js': { getOrCreateCheckout: async () => {
      calls.checkout++;
      return { id: 'cs_test_new', url: 'https://checkout.example.test/new' };
    } },
    '$lib/server/bundleRelease.js': { currentBundleRelease: () => {
      calls.bundle++;
      return { ok: bundleReady, error: 'Bundle not configured' };
    } },
    '$lib/server/transactions.js': { recordCheckoutInitiated: async () => {} },
    '$lib/server/preorderLookup.js': {
      findExistingPreorder: async () => { calls.lookup++; return { found: alreadyOwned, checked, preorder: { copy_number: 7 } }; },
      resendPreorderDownload: async () => { calls.resend++; return { resent: false, reason: 'email_unavailable' }; },
    },
  });
  const response = await mod.POST({
    request: new Request('https://site.example.test/api/stripe-checkout', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: 'buyer@example.test', edition_type: 'standard' }),
    }),
    url: new URL('https://site.example.test/api/stripe-checkout'), getClientAddress: () => '127.0.0.1',
  });
  return { response, calls };
}

test('credential-free development checkout works without touching database, bundle or Stripe', async () => {
  const { response, calls } = await checkoutHarness({ dev: true, credentials: false, checked: false, bundleReady: false });
  assert.equal(response.status, 200);
  assert.match((await response.json()).url, /session_id=mock_session$/);
  assert.deepEqual(calls, { lookup: 0, checkout: 0, bundle: 0, resend: 0 });
});

test('production checkout fails closed for missing credentials, duplicate check or reviewed bundle', async () => {
  for (const options of [{ credentials: false }, { checked: false }, { bundleReady: false }]) {
    const { response, calls } = await checkoutHarness(options);
    assert.equal(response.status, 503);
    assert.equal(calls.checkout, 0);
    assert.equal((await response.json()).url, undefined);
  }
});

test('configured checkout reaches the durable reservation after bundle, email and ownership checks', async () => {
  const { response, calls } = await checkoutHarness();
  assert.equal(response.status, 200);
  assert.deepEqual(calls, { lookup: 1, checkout: 1, bundle: 1, resend: 0 });
});

test('new purchases cannot create Stripe sessions with missing or placeholder delivery credentials', async () => {
  for (const key of [undefined, '', 'placeholder', 'your_resend_api_key', 're_placeholder123', 're_xxxxxxxxxxxxxxxx', 'not-a-resend-key']) {
    const { response, calls } = await checkoutHarness({ emailConfig: { ...configuredPurchaseEmail, RESEND_API_KEY: key } });
    assert.equal(response.status, 503, `Key fixture: ${key}`);
    assert.equal(calls.checkout, 0);
    assert.equal((await response.json()).url, undefined);
  }
});

test('new checkout requires a configured Stripe webhook secret even if every other prerequisite is present', async () => {
  for (const secret of [undefined, '', 'placeholder', 'whsec_your_stripe_webhook_secret', 'whsec_placeholder123', 'not-a-signing-secret']) {
    const { response, calls } = await checkoutHarness({ checkoutEnv: { STRIPE_WEBHOOK_SECRET: secret } });
    assert.equal(response.status, 503);
    assert.equal(calls.checkout, 0);
    assert.equal((await response.json()).url, undefined);
  }
});

test('new purchases require a valid production sender before creating a Stripe session', async () => {
  for (const from of [undefined, '', 'nobody', 'Surviving the Singularity <onboarding@resend.dev>', 'onboarding@sub.resend.dev',
    'STS <hello@yourdomain.com>', 'books@example.com', 'books@local.test', 'books@sender.example', 'books@-broken.com', '.books@sender.com',
    'STS <books@sender.com>\r\nBcc: someone@else.com', 'books@sender.com\r\n', 'books@sender.com,second@sender.com']) {
    const { response, calls } = await checkoutHarness({ emailConfig: { ...configuredPurchaseEmail, EMAIL_FROM: from } });
    assert.equal(response.status, 503, `Sender fixture: ${from}`);
    assert.equal(calls.checkout, 0);
    assert.equal((await response.json()).url, undefined);
  }
});

test('existing paid buyer recovery remains available with no delivery or payment configuration', async () => {
  for (const options of [{ emailConfig: {} }, { credentials: false }, { publicEmailConfig: { PUBLIC_BASE_URL: 'broken' } },
    { checkoutEnv: { STRIPE_WEBHOOK_SECRET: undefined } }]) {
    const { response, calls } = await checkoutHarness({ ...options, alreadyOwned: true, bundleReady: false });
    assert.equal(response.status, 200);
    const body = await response.json();
    assert.equal(body.already_owned, true);
    assert.equal(body.resent, false);
    assert.equal(body.reason, 'email_unavailable');
    assert.equal(body.copy_number, 7);
    assert.deepEqual(calls, { lookup: 1, checkout: 0, bundle: 0, resend: 1 });
  }
});

test('new checkout refuses a malformed email-link origin before creating a Stripe session', async () => {
  for (const origin of ['http://localhost:5173', 'broken', 'https://user:password@sender.com', 'https://sender.com/path']) {
    const { response, calls } = await checkoutHarness({ publicEmailConfig: { PUBLIC_BASE_URL: origin } });
    assert.equal(response.status, 503);
    assert.equal(calls.checkout, 0);
  }
  const preview = await checkoutHarness({ publicEmailConfig: { PUBLIC_BASE_URL: 'https://candidate.project.pages.dev' } });
  assert.equal(preview.response.status, 200);
  assert.equal(preview.calls.checkout, 1);
});

async function reconciliationHarness({ sessions = [paid], local = [], stripeError = false, hasMore = false, review = [] } = {}) {
  class Stripe { constructor() { this.checkout = { sessions: { list: async () => {
    if (stripeError) throw new Error('Stripe unavailable');
    return { data: sessions.map((s) => ({ ...s, created: Math.floor(Date.now() / 1000) - 3600 })), has_more: hasMore };
  } } }; } }
  const database = { from: (table) => query((calls) => {
    if (table === 'unreconciled_paid_sessions') return { data: [] };
    if (calls.some(([op]) => op === 'not')) return { data: review };
    return { data: local };
  }) };
  return await loadSource('src/lib/server/reconcile.js', {
    '$env/dynamic/private': { env }, stripe: { default: Stripe }, '$lib/server/supabaseAdmin.js': { supabaseAdmin: database },
  });
}

test('reconciliation discovers a Stripe-paid session absent from the local ledger', async () => {
  const { findUnreconciled } = await reconciliationHarness();
  const report = await findUnreconciled();
  assert.equal(report.ok, true);
  assert.equal(report.count, 1);
  assert.equal(report.rows[0].source, 'stripe');
  assert.equal(report.stripeLookbackDays, 7);
});

test('reconciliation reports Stripe failure or truncated scan as incomplete', async () => {
  for (const options of [{ stripeError: true }, { hasMore: true }]) {
    const { findUnreconciled } = await reconciliationHarness(options);
    assert.equal((await findUnreconciled()).ok, false);
  }
});

test('reconciliation avoids fulfilled orders but keeps duplicate-charge review flags', async () => {
  const { findUnreconciled } = await reconciliationHarness({
    local: [{ session_id: paid.id, status: 'completed', fulfilled: true }],
    review: [{ session_id: 'cs_duplicate', review_reason: 'possible_duplicate_payment', created_at: new Date().toISOString() }],
  });
  const report = await findUnreconciled();
  assert.equal(report.count, 1);
  assert.equal(report.rows[0].session_id, 'cs_duplicate');
});


test('a paid session for another Stripe product grants no bundle or preorder', async () => {
  const other = { ...paid, metadata: { product: 'unrelated-product', edition_type: 'standard' } };
  const h = await successHarness({ verified: other });
  assert.equal((await h.load(other.id)).ok, false);
  assert.equal(h.calls.bundle, 0);
  assert.equal(h.calls.fulfill, 0);
  const hook = await webhookHarness({ session: other });
  assert.equal(hook.response.status, 200);
  assert.equal(hook.counts.sent, 0);
  assert.equal(hook.counts.fulfilled, 0);
});


test('return-page/webhook race keeps failure retryable and sends only after lease acquisition', async () => {
  let releaseSend, notifySend;
  const sending = new Promise((resolve) => { notifySend = resolve; });
  const provider = new Promise((resolve) => { releaseSend = resolve; });
  const h = await fulfillmentHarness({ send: async () => { notifySend(); return provider; } });
  let acquired = false;
  h.database.rpc = async () => {
    if (acquired) return { data: { state: 'in_flight' } };
    acquired = true;
    return { data: { state: 'claimed', lease_token: 'lease-current' } };
  };
  const returningCustomer = h.fulfill();
  await sending;
  const racingWebhook = await webhookHarness({ fulfillment: h.fulfill });
  assert.equal(racingWebhook.response.status, 500);
  assert.equal(racingWebhook.counts.processed, 0);
  assert.equal(h.sends.length, 1);
  releaseSend({ error: { message: 'provider rejected' } });
  assert.equal((await returningCustomer).state, 'retryable_failure');
  assert.equal(h.outcomes[0].find(([op]) => op === 'update')[1].status, 'failed');
});
