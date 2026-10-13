import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { once } from 'node:events';
import { checkLaunchReadiness } from './check-launch-readiness.mjs';
import manifest from '../src/lib/data/bundleManifest.js';

const fixture = () => ({
  STRIPE_SECRET_KEY: 'sk_live_0123456789abcdef', STRIPE_PRICE_ID_STANDARD: 'price_0123456789',
  STRIPE_WEBHOOK_SECRET: 'whsec_0123456789abcdef', RESEND_API_KEY: 're_0123456789abcdefghij',
  EMAIL_FROM: 'STS <books@survivingthesingularity.com>', RESEND_WEBHOOK_SECRET: `whsec_${Buffer.alloc(24, 7).toString('base64')}`,
  SUPABASE_URL: 'https://projectref.supabase.co', SUPABASE_SERVICE_KEY: 'sb_secret_0123456789abcdefghijkl',
  ADMIN_RECONCILE_TOKEN: '0123456789abcdef0123456789abcdef',
  PUBLIC_ORIGIN: 'https://survivingthesingularity.com', PUBLIC_BASE_URL: 'https://survivingthesingularity.com',
  DOWNLOAD_BUCKET: manifest.bundle.bucket, DOWNLOAD_BUNDLE_PATH: manifest.bundle.object,
  DOWNLOAD_BUNDLE_SHA256: manifest.bundle.sha256, DOWNLOAD_BUNDLE_BOOK_VERSION: manifest.book.version
});
const check = (report, id) => report.checks.find(item => item.id === id);
const goodPrice = { id: 'price_0123456789', active: true, type: 'one_time', currency: 'usd', unit_amount: 500, livemode: true, billing_scheme: 'per_unit' };
const goodEndpoint = { id: 'we_fixture', url: 'https://survivingthesingularity.com/api/webhooks/stripe', status: 'enabled', livemode: true,
  enabled_events: ['checkout.session.completed', 'checkout.session.expired', 'checkout.session.async_payment_succeeded'] };
const goodDomain = { id: 'domain-fixture', name: 'survivingthesingularity.com', status: 'verified', capabilities: { sending: 'enabled' } };
const goodSchema = { paths: Object.fromEntries(['claim_fulfillment_session', 'reserve_checkout', 'find_preorder'].map(name => [`/rpc/${name}`, { post: {} }])) };
function serviceMock(overrides = {}) {
  const calls = [];
  return { calls, fetchImpl: async (input, options) => {
    const url = new URL(input);
    calls.push({ url, options });
    assert.equal(options.method, 'GET');
    assert.equal(options.redirect, 'error');
    assert.equal(options.body, undefined);
    assert(options.signal instanceof AbortSignal);
    const defaults = {
      '/v1/prices/price_0123456789': goodPrice,
      '/v1/webhook_endpoints': { data: [goodEndpoint], has_more: false },
      '/domains': { data: [goodDomain], has_more: false }, '/domains/domain-fixture': goodDomain,
      '/rest/v1/': goodSchema
    };
    assert(Object.hasOwn(defaults, url.pathname), `Unexpected request path ${url.pathname}`);
    const value = Object.hasOwn(overrides, url.pathname) ? overrides[url.pathname] : defaults[url.pathname];
    if (typeof value === 'function') return value(url, options);
    return Response.json(value);
  } };
}

test('default preflight is network-free and missing config never triggers service requests', async () => {
  let requests = 0;
  const fetchImpl = async () => { requests++; throw new Error('Network forbidden'); };
  const ready = await checkLaunchReadiness({ env: fixture(), fetchImpl });
  assert.equal(ready.ok, true);
  assert.equal(ready.mode, 'configuration-only');
  const missing = await checkLaunchReadiness({ env: {}, services: true, fetchImpl });
  assert.equal(missing.ok, false);
  assert.equal(check(missing, 'services').status, 'unverified');
  assert.equal(requests, 0);
});

test('production config rejects test keys and unsafe origins; explicit test mode accepts a preview', async () => {
  const env = { ...fixture(), STRIPE_SECRET_KEY: 'sk_test_0123456789abcdef', PUBLIC_ORIGIN: 'https://candidate.project.pages.dev', PUBLIC_BASE_URL: 'https://candidate.project.pages.dev' };
  assert.equal((await checkLaunchReadiness({ env })).ok, false);
  assert.equal((await checkLaunchReadiness({ env, mode: 'test' })).ok, true);
  for (const unsafe of ['http://projectref.supabase.co', 'https://user:secret@projectref.supabase.co', 'https://127.0.0.1', 'https://[::1]',
    'https://projectref.supabase.co/rest/v1', 'https://projectref.supabase.co?secret=fixture', 'https://localhost', 'https://api.example.com']) {
    const mock = serviceMock();
    const report = await checkLaunchReadiness({ env: { ...fixture(), SUPABASE_URL: unsafe }, services: true, ...mock });
    assert.equal(check(report, 'supabase-url').status, 'fail');
    assert.equal(mock.calls.length, 0);
  }
});

test('configuration rejects missing/mismatched delivery, bundle, monitor and email-link values', async () => {
  for (const [key, value, id] of [
    ['RESEND_API_KEY', 'your_resend_api_key', 'purchase-email'], ['EMAIL_FROM', 'onboarding@resend.dev', 'purchase-email'],
    ['STRIPE_WEBHOOK_SECRET', 'whsec_your_secret', 'stripe-webhook-secret'], ['RESEND_WEBHOOK_SECRET', 'whsec_bad', 'resend-webhook-secret'],
    ['SUPABASE_SERVICE_KEY', 'sb_publishable_0123456789abcdefghijkl', 'supabase-service-key'],
    ['DOWNLOAD_BUNDLE_SHA256', 'old-digest', 'reviewed-bundle'], ['ADMIN_RECONCILE_TOKEN', 'too-short', 'reconciliation-token'],
    ['PUBLIC_BASE_URL', 'https://wrong-site.pages.dev', 'email-link-origin']
  ]) {
    const report = await checkLaunchReadiness({ env: { ...fixture(), [key]: value } });
    assert.equal(check(report, id).status, 'fail');
  }
});

test('service verification makes only authenticated GETs to fixed provider origins and supplied Supabase origin', async () => {
  const mock = serviceMock();
  const report = await checkLaunchReadiness({ env: fixture(), services: true, ...mock });
  assert.equal(report.ok, true);
  assert.equal(mock.calls.length, 5);
  for (const { url, options } of mock.calls) {
    assert(['https://api.stripe.com', 'https://api.resend.com', 'https://projectref.supabase.co'].includes(url.origin));
    if (url.origin === 'https://api.stripe.com') assert.equal(options.headers.Authorization, `Bearer ${fixture().STRIPE_SECRET_KEY}`);
    if (url.origin === 'https://api.resend.com') assert.equal(options.headers.Authorization, `Bearer ${fixture().RESEND_API_KEY}`);
    if (url.origin === 'https://projectref.supabase.co') {
      assert.equal(options.headers.apikey, fixture().SUPABASE_SERVICE_KEY);
      assert.equal(options.headers.Authorization, undefined);
      assert.equal(options.headers.Accept, 'application/openapi+json');
    }
  }
});

test('explicit test-mode service verification checks the supplied preview endpoint and test-mode price', async () => {
  const origin = 'https://candidate.project.pages.dev';
  const env = { ...fixture(), STRIPE_SECRET_KEY: 'sk_test_0123456789abcdef', PUBLIC_ORIGIN: origin, PUBLIC_BASE_URL: origin };
  const mock = serviceMock({ '/v1/prices/price_0123456789': { ...goodPrice, livemode: false },
    '/v1/webhook_endpoints': { data: [{ ...goodEndpoint, livemode: false, url: `${origin}/api/webhooks/stripe` }], has_more: false } });
  assert.equal((await checkLaunchReadiness({ env, mode: 'test', services: true, ...mock })).ok, true);
});

test('restricted Stripe keys support live and test inspection while preserving price and endpoint mode checks', async () => {
  for (const mode of ['live', 'test']) {
    const live = mode === 'live';
    const env = { ...fixture(), STRIPE_SECRET_KEY: `rk_${mode}_0123456789abcdef` };
    const responses = { '/v1/prices/price_0123456789': { ...goodPrice, livemode: live },
      '/v1/webhook_endpoints': { data: [{ ...goodEndpoint, livemode: live }], has_more: false } };
    const mock = serviceMock(responses);
    assert.equal((await checkLaunchReadiness({ env, mode, services: true, ...mock })).ok, true);
    assert.equal(mock.calls[0].options.headers.Authorization, `Bearer ${env.STRIPE_SECRET_KEY}`);
    const mismatch = serviceMock({ ...responses, '/v1/prices/price_0123456789': { ...goodPrice, livemode: !live },
      '/v1/webhook_endpoints': { data: [{ ...goodEndpoint, livemode: !live }], has_more: false } });
    const report = await checkLaunchReadiness({ env, mode, services: true, ...mismatch });
    assert.equal(check(report, 'stripe-price-service').status, 'unverified');
    assert.equal(check(report, 'stripe-webhook-service').status, 'unverified');
    assert.equal((await checkLaunchReadiness({ env, mode: live ? 'test' : 'live' })).ok, false);
  }
});

test('restricted Stripe read permissions can leave service checks unverified without exposing provider details', async () => {
  const env = { ...fixture(), STRIPE_SECRET_KEY: 'rk_live_0123456789abcdef' };
  const forbidden = () => new Response('private-provider-detail-sentinel', { status: 403 });
  const mock = serviceMock({ '/v1/prices/price_0123456789': forbidden, '/v1/webhook_endpoints': forbidden });
  const report = await checkLaunchReadiness({ env, services: true, ...mock });
  assert.equal(report.ok, false);
  for (const id of ['stripe-price-service', 'stripe-webhook-service']) {
    assert.equal(check(report, id).status, 'unverified');
    assert(check(report, id).detail.includes('without broadening the production key'));
  }
  assert(!JSON.stringify(report).includes('private-provider-detail-sentinel'));
  assert(!JSON.stringify(report).includes(env.STRIPE_SECRET_KEY));
});

test('legacy service-role JWT auth uses apikey and Bearer while anon JWTs cannot initiate requests', async () => {
  const jwt = role => `${Buffer.from('{}').toString('base64url')}.${Buffer.from(JSON.stringify({ role })).toString('base64url')}.signature`;
  const mock = serviceMock();
  const key = jwt('service_role');
  assert.equal((await checkLaunchReadiness({ env: { ...fixture(), SUPABASE_SERVICE_KEY: key }, services: true, ...mock })).ok, true);
  assert.equal(mock.calls.at(-1).options.headers.Authorization, `Bearer ${key}`);
  assert.equal((await checkLaunchReadiness({ env: { ...fixture(), SUPABASE_SERVICE_KEY: jwt('anon') } })).ok, false);
});

test('wrong, recurring, inactive, transformed or test-mode Stripe prices do not pass a live launch', async () => {
  for (const change of [{ unit_amount: 900 }, { currency: 'eur' }, { active: false }, { type: 'recurring' }, { livemode: false },
    { id: 'price_wrong' }, { custom_unit_amount: {} }, { transform_quantity: { divide_by: 10 } }, { billing_scheme: 'tiered' }]) {
    const mock = serviceMock({ '/v1/prices/price_0123456789': { ...goodPrice, ...change } });
    const report = await checkLaunchReadiness({ env: fixture(), services: true, ...mock });
    assert.equal(check(report, 'stripe-price-service').status, 'unverified');
    assert.equal(report.ok, false);
  }
});

test('webhook validation follows bounded pagination and requires endpoint, mode and all handled events', async () => {
  for (const change of [{ status: 'disabled' }, { livemode: false }, { url: 'https://wrong.pages.dev/api/webhooks/stripe' },
    { enabled_events: ['checkout.session.completed'] }]) {
    const mock = serviceMock({ '/v1/webhook_endpoints': { data: [{ ...goodEndpoint, ...change }], has_more: false } });
    const report = await checkLaunchReadiness({ env: fixture(), services: true, ...mock });
    assert.equal(check(report, 'stripe-webhook-service').status, 'unverified');
  }
  const mock = serviceMock({ '/v1/webhook_endpoints': url => Response.json(url.searchParams.has('starting_after')
    ? { data: [{ ...goodEndpoint, enabled_events: ['*'] }], has_more: false }
    : { data: [{ id: 'we_other', url: 'https://elsewhere.pages.dev' }], has_more: true }) });
  assert.equal((await checkLaunchReadiness({ env: fixture(), services: true, ...mock })).ok, true);
  assert.equal(mock.calls.find(({ url }) => url.searchParams.has('starting_after')).url.searchParams.get('starting_after'), 'we_other');
});

test('truncated, repeated-cursor and malformed provider lists remain unverified', async () => {
  for (const result of [() => ({ data: [{ id: 'same' }], has_more: true }), () => ({ data: [], has_more: true }),
    () => ({ data: [goodEndpoint] }), page => ({ data: [{ ...goodEndpoint, id: `page-${page}` }], has_more: true })]) {
    let pages = 0;
    const mock = serviceMock({ '/v1/webhook_endpoints': () => Response.json(result(++pages)) });
    const report = await checkLaunchReadiness({ env: fixture(), services: true, ...mock });
    assert.equal(check(report, 'stripe-webhook-service').status, 'unverified');
    assert(pages <= 5);
  }
});

test('Resend requires verified sending and correctly paginates domains', async () => {
  for (const change of [{ status: 'pending' }, { status: 'partially_verified' }, { capabilities: { sending: 'disabled' } }]) {
    const mock = serviceMock({ '/domains/domain-fixture': { ...goodDomain, ...change } });
    const report = await checkLaunchReadiness({ env: fixture(), services: true, ...mock });
    assert.equal(check(report, 'resend-domain-service').status, 'unverified');
  }
  const mock = serviceMock({ '/domains': url => Response.json(url.searchParams.has('after')
    ? { data: [goodDomain], has_more: false } : { data: [{ id: 'other-domain', name: 'elsewhere.com' }], has_more: true }) });
  assert.equal((await checkLaunchReadiness({ env: fixture(), services: true, ...mock })).ok, true);
  assert.equal(mock.calls.find(({ url }) => url.searchParams.has('after')).url.searchParams.get('after'), 'other-domain');
});

test('schema discovery cannot pass with missing RPCs or claim migration semantics', async () => {
  const mock = serviceMock({ '/rest/v1/': { paths: {} } });
  const report = await checkLaunchReadiness({ env: fixture(), services: true, ...mock });
  assert.equal(check(report, 'supabase-schema-service').status, 'unverified');
  assert(report.remaining.some(item => item.includes('migration 017')));
});

test('restricted Resend permission, redirects, timeouts and provider failures disclose no secrets or customer content', async () => {
  const secret = 'private-customer@unsafe.test raw-provider-secret-value';
  for (const failure of [() => new Response(secret, { status: 403 }), () => new Response(secret, { status: 500 }),
    () => { throw new Error(`redirect to ${secret}`); }, () => { throw new DOMException(secret, 'TimeoutError'); },
    () => new Response(secret, { status: 200 })]) {
    const mock = serviceMock({ '/domains': failure });
    const report = await checkLaunchReadiness({ env: fixture(), services: true, ...mock });
    assert.equal(check(report, 'resend-domain-service').status, 'unverified');
    const output = JSON.stringify(report);
    assert(!output.includes(secret));
    for (const key of ['STRIPE_SECRET_KEY', 'STRIPE_WEBHOOK_SECRET', 'RESEND_API_KEY', 'RESEND_WEBHOOK_SECRET', 'SUPABASE_SERVICE_KEY', 'ADMIN_RECONCILE_TOKEN', 'EMAIL_FROM']) {
      assert(!output.includes(fixture()[key]));
    }
    if (output.includes('403')) assert(output.includes('without broadening the production key'));
  }
});

test('native fetch rejects redirects and aborts a stalled JSON body without leaking response details', { timeout: 5_000 }, async () => {
  for (const scenario of ['redirect', 'stalled-body']) {
    let requests = 0;
    const server = createServer((request, response) => {
      requests++;
      assert.equal(request.method, 'GET');
      if (scenario === 'redirect') response.writeHead(302, { Location: 'https://secret-sentinel.invalid/private' }).end();
      else { response.writeHead(200, { 'content-type': 'application/json' }); response.write('{'); }
    });
    server.listen(0, '127.0.0.1');
    await once(server, 'listening');
    try {
      const mock = serviceMock({ '/domains': (_url, options) => fetch(`http://127.0.0.1:${server.address().port}/fixture`, options) });
      const report = await checkLaunchReadiness({ env: fixture(), services: true, timeoutMs: 150, ...mock });
      assert.equal(check(report, 'resend-domain-service').status, 'unverified');
      assert.equal(requests, 1);
      assert(!JSON.stringify(report).includes('secret-sentinel'));
    } finally {
      server.closeAllConnections();
      await new Promise(resolve => server.close(resolve));
    }
  }
});
