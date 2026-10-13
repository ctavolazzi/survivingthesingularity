import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createServer } from 'node:http';
import { once } from 'node:events';
import { spawnSync } from 'node:child_process';
import { runHostedDeploymentGate } from './check-hosted-deployment.mjs';
import manifest from '../src/lib/data/bundleManifest.js';

const payload = Buffer.from('reviewed-private-bundle-fixture');
const expected = { ...manifest, bundle: { ...manifest.bundle, bytes: payload.length, sha256: createHash('sha256').update(payload).digest('hex') } };
const origin = 'https://survivingthesingularity.com';
const bucketPath = `/storage/v1/bucket/${expected.bundle.bucket}`;
const objectPath = `/storage/v1/object/${expected.bundle.bucket}/${expected.bundle.object}`;
const fixture = () => ({
  CF_PAGES: '1', CF_PAGES_BRANCH: 'main',
  STRIPE_SECRET_KEY: 'rk_live_0123456789abcdef', STRIPE_PRICE_ID_STANDARD: 'price_0123456789',
  STRIPE_WEBHOOK_SECRET: 'whsec_0123456789abcdef', RESEND_API_KEY: 're_0123456789abcdefghij',
  EMAIL_FROM: 'STS <books@survivingthesingularity.com>', RESEND_WEBHOOK_SECRET: `whsec_${Buffer.alloc(24, 7).toString('base64')}`,
  SUPABASE_URL: 'https://projectref.supabase.co', SUPABASE_SERVICE_KEY: 'sb_secret_0123456789abcdefghijkl',
  ADMIN_RECONCILE_TOKEN: '0123456789abcdef0123456789abcdef',
  DOWNLOAD_BUCKET: expected.bundle.bucket, DOWNLOAD_BUNDLE_PATH: expected.bundle.object,
  DOWNLOAD_BUNDLE_SHA256: expected.bundle.sha256, DOWNLOAD_BUNDLE_BOOK_VERSION: expected.book.version
});

function schemaFixture() {
  const columns = {
    fulfilled_sessions: { lease_token: 'uuid', lease_expires_at: 'timestamp with time zone' },
    preorders: { payment_session_id: 'text' }, checkout_transactions: { review_reason: 'text' },
    checkout_reservations: { email: 'text', edition_type: 'text', reservation_key: 'uuid', session_id: 'text', created_at: 'timestamp with time zone' }
  };
  const definitions = Object.fromEntries(Object.entries(columns).map(([table, fields]) => [table,
    { type: 'object', properties: Object.fromEntries(Object.entries(fields).map(([name, format]) => [name, { type: 'string', format }])) }]));
  const paths = Object.fromEntries(Object.keys(columns).map(table => [`/${table}`, { get: {} }]));
  for (const [name, required, optional = []] of [
    ['claim_fulfillment_session', ['p_session_id', 'p_email']],
    ['reserve_checkout', ['p_email', 'p_edition_type'], ['p_expired_session']],
    ['find_preorder', ['p_email', 'p_edition_type']]
  ]) {
    paths[`/rpc/${name}`] = { post: { parameters: [{ $ref: '#/parameters/preferParams' }, { in: 'body', name: 'args', required: true,
      schema: { type: 'object', properties: Object.fromEntries([...required, ...optional].map(arg => [arg, { type: 'string', format: 'text' }])), required } }] } };
  }
  return { swagger: '2.0', definitions, paths };
}

function serviceMock(overrides = {}) {
  const calls = [];
  return { calls, fetchImpl: async (input, options) => {
    const url = new URL(input);
    calls.push({ url, options });
    assert.equal(options.method, 'GET');
    assert.equal(options.redirect, 'error');
    assert.equal(options.body, undefined);
    assert(options.signal instanceof AbortSignal);
    assert(['https://api.stripe.com', 'https://api.resend.com', 'https://projectref.supabase.co'].includes(url.origin));
    const domain = { id: 'fixture-domain', name: 'survivingthesingularity.com', status: 'verified', capabilities: { sending: 'enabled' } };
    const defaults = {
      '/v1/prices/price_0123456789': { id: 'price_0123456789', active: true, type: 'one_time', currency: 'usd', unit_amount: 500, livemode: true, billing_scheme: 'per_unit' },
      '/v1/webhook_endpoints': { data: [{ id: 'fixture-webhook', url: `${origin}/api/webhooks/stripe`, status: 'enabled', livemode: true,
        enabled_events: ['checkout.session.completed', 'checkout.session.expired', 'checkout.session.async_payment_succeeded'] }], has_more: false },
      '/domains': { data: [domain], has_more: false }, '/domains/fixture-domain': domain,
      '/rest/v1/': schemaFixture(), [bucketPath]: { id: expected.bundle.bucket, name: expected.bundle.bucket, public: false },
      [objectPath]: () => new Response(payload)
    };
    assert(Object.hasOwn(defaults, url.pathname));
    const value = Object.hasOwn(overrides, url.pathname) ? overrides[url.pathname] : defaults[url.pathname];
    return typeof value === 'function' ? value(url, options) : Response.json(value);
  } };
}
const check = (report, id) => report.checks.find(item => item.id === id);
const run = (mock, env = fixture(), options = {}) => runHostedDeploymentGate({ env, expected, ...mock, ...options });

test('local builds skip without network; partial, malformed and preview Cloudflare contexts fail closed', async () => {
  const fetchImpl = () => { throw new Error('Network must not be reached'); };
  const local = await runHostedDeploymentGate({ env: {}, fetchImpl });
  assert.equal(local.ok, true);
  assert.equal(local.skipped, true);
  for (const env of [{ CF_PAGES: '1' }, { CF_PAGES_BRANCH: 'main' }, { CF_PAGES: '' }, { CF_PAGES: 'true', CF_PAGES_BRANCH: 'main' },
    { CF_PAGES: '0', CF_PAGES_BRANCH: 'main' }, { CF_PAGES: '1', CF_PAGES_BRANCH: 'preview' }]) {
    const result = await runHostedDeploymentGate({ env, fetchImpl });
    assert.equal(result.ok, false);
    assert.equal(result.skipped, false);
  }
});

test('production gate defaults only the public origin and verifies live services, private storage and exact streamed bytes', async () => {
  const env = fixture();
  const mock = serviceMock();
  const report = await run(mock, env);
  assert.equal(report.ok, true);
  assert.equal(report.skipped, false);
  assert.equal(mock.calls.length, 8);
  assert.equal(env.PUBLIC_ORIGIN, undefined);
  for (const id of ['migration-017-schema', 'private-bundle-bucket', 'remote-bundle-bytes']) assert.equal(check(report, id).status, 'pass');
  assert(report.remaining.some(message => message.includes('semantics')));
  assert(report.remaining.some(message => message.includes('inbox')));
  for (const { url, options } of mock.calls.filter(call => call.url.origin.endsWith('.supabase.co'))) {
    assert.equal(options.headers.apikey, env.SUPABASE_SERVICE_KEY);
    assert.equal(options.headers.Authorization, undefined);
    assert.equal(url.search, '');
  }
  const output = JSON.stringify(report);
  for (const key of ['STRIPE_SECRET_KEY', 'RESEND_API_KEY', 'EMAIL_FROM', 'SUPABASE_SERVICE_KEY', 'ADMIN_RECONCILE_TOKEN']) assert(!output.includes(env[key]));
  assert(!output.includes('fixture-domain'));
  assert(!output.includes('fixture-webhook'));
});

test('wrong origin, test keys, placeholders and missing config stop all requests', async () => {
  for (const changes of [{ PUBLIC_ORIGIN: 'https://wrong.pages.dev' }, { PUBLIC_ORIGIN: '' }, { STRIPE_SECRET_KEY: 'rk_test_0123456789abcdef' },
    { SUPABASE_SERVICE_KEY: 'sb_secret_your_placeholder_key' }, { EMAIL_FROM: 'onboarding@resend.dev' }, { STRIPE_WEBHOOK_SECRET: '' },
    { PUBLIC_BASE_URL: 'https://preview.pages.dev' }]) {
    const mock = serviceMock();
    assert.equal((await run(mock, { ...fixture(), ...changes })).ok, false);
    assert.equal(mock.calls.length, 0);
  }
});

test('a service failure cannot be mistaken for a hosted pass or initiate storage verification', async () => {
  const mock = serviceMock({ '/domains': () => new Response('private-provider-detail', { status: 403 }) });
  const report = await run(mock);
  assert.equal(report.ok, false);
  assert.equal(check(report, 'resend-domain-service').status, 'unverified');
  assert.equal(mock.calls.some(({ url }) => url.pathname.startsWith('/storage/')), false);
  assert(!JSON.stringify(report).includes('private-provider-detail'));
});

test('legacy service-role JWT remains authenticated for the schema and storage GETs', async () => {
  const key = `${Buffer.from('{}').toString('base64url')}.${Buffer.from('{"role":"service_role"}').toString('base64url')}.signature`;
  const mock = serviceMock();
  assert.equal((await run(mock, { ...fixture(), SUPABASE_SERVICE_KEY: key })).ok, true);
  for (const { url, options } of mock.calls) if (url.origin.endsWith('.supabase.co')) assert.equal(options.headers.Authorization, `Bearer ${key}`);
});

test('public, missing-privacy and wrong-identity buckets fail without downloading the object', async () => {
  for (const value of [{ id: expected.bundle.bucket, name: expected.bundle.bucket, public: true },
    { id: expected.bundle.bucket, name: expected.bundle.bucket }, { id: 'another', name: expected.bundle.bucket, public: false },
    { id: expected.bundle.bucket, name: 'another', public: false }, null]) {
    const mock = serviceMock({ [bucketPath]: value });
    const report = await run(mock);
    assert.equal(report.ok, false);
    assert.equal(check(report, 'private-bundle-bucket').status, 'unverified');
    assert.equal(mock.calls.some(({ url }) => url.pathname === objectPath), false);
  }
});

test('missing migration columns, wrong types and inaccessible table shapes cannot pass schema verification', async () => {
  for (const change of [schema => delete schema.definitions.fulfilled_sessions.properties.lease_token,
    schema => { schema.definitions.fulfilled_sessions.properties.lease_expires_at.format = 'date-time'; },
    schema => delete schema.definitions.preorders.properties.payment_session_id,
    schema => delete schema.definitions.checkout_transactions.properties.review_reason,
    schema => delete schema.paths['/checkout_reservations'], schema => { schema.swagger = '3.0'; }]) {
    const schema = schemaFixture();
    change(schema);
    const report = await run(serviceMock({ '/rest/v1/': schema }));
    assert.equal(report.ok, false);
    assert.equal(check(report, 'migration-017-schema').status, 'unverified');
  }
});

test('RPC signatures require all exact text args with the expired-session default remaining optional', async () => {
  for (const change of [body => delete body.schema.properties.p_expired_session,
    body => body.schema.required.push('p_expired_session'), body => { body.schema.properties.p_email.format = 'uuid'; },
    body => { body.schema.properties.unexpected = { type: 'string', format: 'text' }; },
    body => { body.required = false; }]) {
    const schema = schemaFixture();
    change(schema.paths['/rpc/reserve_checkout'].post.parameters[1]);
    const report = await run(serviceMock({ '/rest/v1/': schema }));
    assert.equal(check(report, 'migration-017-schema').status, 'unverified');
    assert.equal(report.ok, false);
  }
  for (const name of ['claim_fulfillment_session', 'find_preorder']) {
    const schema = schemaFixture();
    schema.paths[`/rpc/${name}`].post.parameters[1].schema.required.pop();
    assert.equal(check(await run(serviceMock({ '/rest/v1/': schema })), 'migration-017-schema').status, 'unverified');
  }
});

test('truncated or changed object bytes fail even with an otherwise correct manifest', async () => {
  for (const bytes of [payload.subarray(1), Buffer.alloc(payload.length, 97)]) {
    const report = await run(serviceMock({ [objectPath]: () => new Response(bytes) }));
    assert.equal(report.ok, false);
    assert.equal(check(report, 'remote-bundle-bytes').status, 'unverified');
  }
});

test('oversized content-length and oversized streaming bodies are cancelled at the release bound', async () => {
  for (const declared of [false, true]) {
    let cancelled = false;
    const body = new ReadableStream({ start(controller) { controller.enqueue(Buffer.alloc(payload.length + 1)); }, cancel() { cancelled = true; } });
    const headers = declared ? { 'content-length': String(payload.length + 1) } : {};
    const report = await run(serviceMock({ [objectPath]: () => new Response(body, { headers }) }));
    assert.equal(report.ok, false);
    assert.equal(cancelled, true);
    assert.equal(check(report, 'remote-bundle-bytes').detail, 'Hosted response exceeded the permitted size.');
  }
});

test('hosted failures redact provider bodies, exceptions, customer data and identifiers', async () => {
  const sentinel = 'private-buyer@unsafe.test secret-service-value object-sensitive-id';
  for (const pathname of [bucketPath, objectPath]) {
    for (const failure of [() => new Response(sentinel, { status: 404 }), () => { throw new Error(sentinel); },
      () => new Response(sentinel, { status: 200 })]) {
      const report = await run(serviceMock({ [pathname]: failure }));
      assert.equal(report.ok, false);
      assert(!JSON.stringify(report).includes(sentinel));
    }
  }
});

test('native fetch rejects redirects and aborts stalled object bodies without disclosing redirect targets', { timeout: 5_000 }, async () => {
  for (const scenario of ['redirect', 'stalled-body']) {
    let requests = 0;
    const server = createServer((request, response) => {
      requests++;
      assert.equal(request.method, 'GET');
      if (scenario === 'redirect') response.writeHead(302, { Location: 'https://secret-sentinel.invalid/private' }).end();
      else { response.writeHead(200); response.write(payload.subarray(0, 1)); }
    });
    server.listen(0, '127.0.0.1');
    await once(server, 'listening');
    try {
      const mock = serviceMock({ [objectPath]: (_url, options) => fetch(`http://127.0.0.1:${server.address().port}/fixture`, options) });
      const report = await run(mock, fixture(), { objectTimeoutMs: 150 });
      assert.equal(report.ok, false);
      assert.equal(check(report, 'remote-bundle-bytes').status, 'unverified');
      assert.equal(requests, 1);
      assert(!JSON.stringify(report).includes('secret-sentinel'));
    } finally {
      server.closeAllConnections();
      await new Promise(resolve => server.close(resolve));
    }
  }
});

test('CLI skips local builds but exits nonzero for an incomplete production configuration', () => {
  const script = new URL('./check-hosted-deployment.mjs', import.meta.url);
  const local = spawnSync(process.execPath, [script.pathname], { env: {}, encoding: 'utf8' });
  assert.equal(local.status, 0);
  assert.equal(JSON.parse(local.stdout).skipped, true);
  const hosted = spawnSync(process.execPath, [script.pathname], { env: { CF_PAGES: '1', CF_PAGES_BRANCH: 'main' }, encoding: 'utf8' });
  assert.equal(hosted.status, 1);
  assert.equal(JSON.parse(hosted.stdout).ok, false);
});
