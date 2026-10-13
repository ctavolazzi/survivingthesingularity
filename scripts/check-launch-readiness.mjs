#!/usr/bin/env node
/**
 * Read-only deployment checks; no .env loading or network without --services.
 * Service contracts: docs.stripe.com/api/webhook_endpoints/list,
 * resend.com/docs/api-reference/pagination, resend.com/docs/api-reference/domains/get-domain,
 * supabase.com/docs/guides/getting-started/api-keys.
 */
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { isIP } from 'node:net';
import { validatePurchaseEmailConfig, validateEmailLinkOrigin } from '../src/lib/emailConfig.js';
import { isConfiguredStripeWebhookSecret } from '../src/lib/stripeConfig.js';
import { validateBundleRelease } from '../src/lib/bundleRelease.js';
import manifest from '../src/lib/data/bundleManifest.js';

const PLACEHOLDER = /placeholder|your[_-]|replace[_-]?|changeme|example|dummy|<|>/i;
const EVENTS = ['checkout.session.completed', 'checkout.session.expired', 'checkout.session.async_payment_succeeded'];
const RPCS = ['claim_fulfillment_session', 'reserve_checkout', 'find_preorder'];
const MAX_PAGES = 5;

function configured(value, pattern = /\S{16,}/) {
  return typeof value === 'string' && pattern.test(value) && !PLACEHOLDER.test(value) && !/[\r\n]/.test(value);
}

function publicHttpsOrigin(value) {
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash
        || url.pathname !== '/' || url.port || isIP(url.hostname) || url.hostname.startsWith('[')
        || !url.hostname.includes('.') || /\.(localhost|local|test|invalid|example)$/.test(url.hostname)
        || /(^|\.)(example\.(com|net|org)|localhost)$/.test(url.hostname)
        || PLACEHOLDER.test(url.hostname)) return null;
    return url.origin;
  } catch { return null; }
}

function serviceKey(value) {
  if (!configured(value)) return false;
  if (/^sb_secret_[A-Za-z0-9_-]{16,}$/.test(value)) return true;
  try {
    const parts = value.split('.');
    return parts.length === 3 && JSON.parse(Buffer.from(parts[1], 'base64url').toString()).role === 'service_role';
  } catch { return false; }
}

export function checkLaunchConfig(env = {}, expected = manifest, { mode = 'live' } = {}) {
  const checks = [];
  const add = (id, ok, detail) => checks.push({ id, status: ok ? 'pass' : 'fail', detail });
  const email = validatePurchaseEmailConfig(env);
  const bundle = validateBundleRelease(env, expected);
  add('stripe-key', ['live', 'test'].includes(mode) && configured(env.STRIPE_SECRET_KEY, /^(sk|rk)_(live|test)_[A-Za-z0-9]{8,}$/)
    && env.STRIPE_SECRET_KEY.split('_')[1] === mode, `STRIPE_SECRET_KEY must be a standard or restricted key configured for the requested ${mode === 'test' ? 'test' : 'live'} mode.`);
  add('stripe-price', configured(env.STRIPE_PRICE_ID_STANDARD, /^price_[A-Za-z0-9]{4,}$/), 'STRIPE_PRICE_ID_STANDARD must identify the advertised standard edition.');
  add('stripe-webhook-secret', isConfiguredStripeWebhookSecret(env.STRIPE_WEBHOOK_SECRET), 'STRIPE_WEBHOOK_SECRET must be configured for the selected endpoint and mode.');
  add('purchase-email', email.ok, email.ok ? 'Purchase email configuration is present; provider verification is separate.' : email.error);
  const resendSecret = env.RESEND_WEBHOOK_SECRET;
  const base64 = typeof resendSecret === 'string' ? resendSecret.replace(/^whsec_/, '') : '';
  add('resend-webhook-secret', configured(resendSecret, /^whsec_[A-Za-z0-9+/]+={0,2}$/) && Buffer.from(base64, 'base64').length >= 16,
    'RESEND_WEBHOOK_SECRET must contain a configured Svix signing secret.');
  add('supabase-url', Boolean(publicHttpsOrigin(env.SUPABASE_URL)), 'SUPABASE_URL must be the HTTPS project origin, without a path or credentials.');
  add('supabase-service-key', serviceKey(env.SUPABASE_SERVICE_KEY), 'SUPABASE_SERVICE_KEY must be a secret key or a JWT declaring service_role; local inspection does not authenticate it.');
  add('reviewed-bundle', bundle.ok, bundle.ok ? 'Bundle configuration matches the reviewed manifest; remote bytes require separate verification.' : bundle.error);
  add('reconciliation-token', configured(env.ADMIN_RECONCILE_TOKEN, /^\S{32,}$/), 'ADMIN_RECONCILE_TOKEN must be a non-placeholder token of at least 32 characters.');
  add('public-origin', Boolean(publicHttpsOrigin(env.PUBLIC_ORIGIN)), 'PUBLIC_ORIGIN must be the production HTTPS origin used for webhook matching.');
  const emailOrigin = validateEmailLinkOrigin(env);
  const baseOrigin = emailOrigin.ok ? publicHttpsOrigin(emailOrigin.origin) : null;
  add('email-link-origin', Boolean(baseOrigin) && baseOrigin === publicHttpsOrigin(env.PUBLIC_ORIGIN),
    'PUBLIC_BASE_URL (or its production default) must match PUBLIC_ORIGIN so welcome links target the intended site.');
  return checks;
}

// Provider errors can contain credentials, addresses and customer records.
// Only controlled messages and HTTP status codes may leave these helpers.
class CheckError extends Error {
  constructor(message) { super(message); this.name = 'CheckError'; }
}

async function getJson(fetchImpl, url, headers, timeoutMs) {
  let response;
  try {
    response = await fetchImpl(url, { method: 'GET', headers, redirect: 'error', signal: AbortSignal.timeout(timeoutMs) });
  } catch { throw new CheckError('Request could not be verified (network, timeout or redirect failure).'); }
  if (!response.ok) {
    if (response.status === 403 && new URL(url).origin === 'https://api.resend.com') {
      throw new CheckError('Domain verification unavailable to this restricted Resend key (HTTP 403); verify in the dashboard without broadening the production key.');
    }
    if (response.status === 403 && new URL(url).origin === 'https://api.stripe.com') {
      throw new CheckError('Stripe inspection unavailable to this key (HTTP 403); verify in the dashboard without broadening the production key.');
    }
    throw new CheckError(`Read-only provider request returned HTTP ${response.status}.`);
  }
  try { return await response.json(); }
  catch { throw new CheckError('Provider returned an unreadable JSON response.'); }
}

async function listAll(fetchImpl, base, headers, cursorName, timeoutMs) {
  const rows = [], cursors = new Set();
  let cursor;
  for (let page = 0; page < MAX_PAGES; page++) {
    const url = new URL(base);
    url.searchParams.set('limit', '100');
    if (cursor) url.searchParams.set(cursorName, cursor);
    const result = await getJson(fetchImpl, url.href, headers, timeoutMs);
    if (!Array.isArray(result.data) || typeof result.has_more !== 'boolean') throw new CheckError('Provider list pagination could not be verified.');
    rows.push(...result.data);
    if (!result.has_more) return rows;
    cursor = result.data.at(-1)?.id;
    if (typeof cursor !== 'string' || !cursor || cursors.has(cursor)) throw new CheckError('Provider pagination cursor did not advance.');
    cursors.add(cursor);
  }
  throw new CheckError('Provider pagination exceeded the bounded scan; verification is incomplete.');
}

export async function checkLaunchReadiness({ env = process.env, services = false, mode = 'live', fetchImpl = globalThis.fetch,
  expected = manifest, timeoutMs = 10_000 } = {}) {
  const checks = checkLaunchConfig(env, expected, { mode });
  if (services && checks.every(check => check.status === 'pass')) {
    const inspect = async (id, action) => {
      try { checks.push({ id, status: 'pass', detail: await action() }); }
      catch (error) { checks.push({ id, status: 'unverified', detail: error instanceof CheckError ? error.message : 'Provider response could not be verified.' }); }
    };
    const stripeHeaders = { Authorization: `Bearer ${env.STRIPE_SECRET_KEY}`, 'Stripe-Version': '2024-06-20' };
    const resendHeaders = { Authorization: `Bearer ${env.RESEND_API_KEY}` };
    const live = mode === 'live';
    await inspect('stripe-price-service', async () => {
      const price = await getJson(fetchImpl, `https://api.stripe.com/v1/prices/${encodeURIComponent(env.STRIPE_PRICE_ID_STANDARD)}`, stripeHeaders, timeoutMs);
      if (price.id !== env.STRIPE_PRICE_ID_STANDARD || price.active !== true || price.type !== 'one_time'
          || price.currency !== 'usd' || price.unit_amount !== 500 || price.livemode !== live
          || price.billing_scheme !== 'per_unit' || price.custom_unit_amount != null || price.transform_quantity != null) {
        throw new CheckError('Standard price must be active, one-time, USD 5.00 per unit, without quantity/custom-price transformations, in the key mode.');
      }
      return `Standard price verified for ${live ? 'live' : 'test'} mode: USD 5.00 one-time.`;
    });
    await inspect('stripe-webhook-service', async () => {
      const endpoints = await listAll(fetchImpl, 'https://api.stripe.com/v1/webhook_endpoints', stripeHeaders, 'starting_after', timeoutMs);
      const target = `${publicHttpsOrigin(env.PUBLIC_ORIGIN)}/api/webhooks/stripe`;
      const endpoint = endpoints.find(item => item.url === target && item.status === 'enabled' && item.livemode === live
        && Array.isArray(item.enabled_events) && (item.enabled_events.includes('*') || EVENTS.every(event => item.enabled_events.includes(event))));
      if (!endpoint) throw new CheckError('No enabled webhook matches the production origin, key mode and completed/expired/async-success events.');
      return 'Expected Stripe endpoint and subscribed events found; its signing secret still requires a signed-event test.';
    });
    await inspect('resend-domain-service', async () => {
      const domains = await listAll(fetchImpl, 'https://api.resend.com/domains', resendHeaders, 'after', timeoutMs);
      const senderDomain = validatePurchaseEmailConfig(env).senderDomain;
      const matched = domains.find(domain => domain.name?.toLowerCase() === senderDomain);
      if (!matched || typeof matched.id !== 'string') throw new CheckError('The configured sender domain was not found in Resend.');
      const domain = await getJson(fetchImpl, `https://api.resend.com/domains/${encodeURIComponent(matched.id)}`, resendHeaders, timeoutMs);
      if (domain.name?.toLowerCase() !== senderDomain || domain.status !== 'verified' || domain.capabilities?.sending !== 'enabled') {
        throw new CheckError('Sender verification with sending enabled was not established; partial verification requires sending-record or dashboard evidence.');
      }
      return 'Sender domain verified with sending enabled; this does not prove inbox delivery or webhook setup.';
    });
    await inspect('supabase-schema-service', async () => {
      const key = env.SUPABASE_SERVICE_KEY;
      const headers = { apikey: key, Accept: 'application/openapi+json' };
      if (!key.startsWith('sb_secret_')) headers.Authorization = `Bearer ${key}`;
      const schema = await getJson(fetchImpl, `${publicHttpsOrigin(env.SUPABASE_URL)}/rest/v1/`, headers, timeoutMs);
      if (!RPCS.every(name => schema.paths?.[`/rpc/${name}`]?.post)) {
        throw new CheckError('Expected fulfillment, reservation and ownership RPCs are absent from the exposed schema.');
      }
      return 'Required RPC paths are exposed. Schema presence does not prove migration semantics, permissions or concurrency behavior.';
    });
  } else if (services) {
    checks.push({ id: 'services', status: 'unverified', detail: 'Service requests skipped because local configuration checks failed.' });
  }
  return {
    ok: checks.every(check => check.status === 'pass'), mode: services ? 'read-only-services' : 'configuration-only', stripeMode: mode, checks,
    remaining: [
      'Compare these process values with actual hosting configuration; local success does not inspect Cloudflare secrets.',
      'Verify private storage bytes separately with node scripts/deploy-book-bundle.mjs (default read-only).',
      'Apply and validate migration 017, then complete a test-mode purchase, signed webhooks, recovery and inbox delivery.',
      'Confirm Resend delivery-event webhook setup and matching signing secret; this script does not send webhooks.',
      'Enable the reconciliation monitor with the same token in hosting and CI; this script does not inspect CI secrets.'
    ]
  };
}

async function main() {
  const args = process.argv.slice(2);
  if (args.some(arg => !['--services', '--mode=test', '--mode=live'].includes(arg))
      || args.filter(arg => arg.startsWith('--mode=')).length > 1 || args.filter(arg => arg === '--services').length > 1) {
    throw new CheckError('Usage: node scripts/check-launch-readiness.mjs [--services] [--mode=live|test]');
  }
  const report = await checkLaunchReadiness({ services: args.includes('--services'), mode: args.includes('--mode=test') ? 'test' : 'live' });
  console.log(JSON.stringify(report, null, 2));
  process.exitCode = report.ok ? 0 : 1;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => { console.error(error instanceof CheckError ? error.message : 'Launch preflight could not complete.'); process.exitCode = 1; });
}
