#!/usr/bin/env node
/**
 * Cloudflare production build gate. Uses injected build configuration, never .env.
 * Read-only GETs: existing service preflight, PostgREST OpenAPI, bucket and object.
 * Schema discovery cannot prove SQL function bodies/grants or actual fulfillment.
 */
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkLaunchReadiness } from './check-launch-readiness.mjs';
import manifest from '../src/lib/data/bundleManifest.js';

const PRODUCTION_ORIGIN = 'https://survivingthesingularity.com';
const MAX_SCHEMA_BYTES = 8 * 1024 * 1024;
const COLUMNS = {
  fulfilled_sessions: { lease_token: 'uuid', lease_expires_at: 'timestamp with time zone' },
  preorders: { payment_session_id: 'text' },
  checkout_transactions: { review_reason: 'text' },
  checkout_reservations: { email: 'text', edition_type: 'text', reservation_key: 'uuid', session_id: 'text', created_at: 'timestamp with time zone' }
};
const RPC_ARGUMENTS = {
  claim_fulfillment_session: { required: ['p_session_id', 'p_email'], optional: [] },
  reserve_checkout: { required: ['p_email', 'p_edition_type'], optional: ['p_expired_session'] },
  find_preorder: { required: ['p_email', 'p_edition_type'], optional: [] }
};
const REMAINING = [
  'OpenAPI presence does not prove migration 017 function semantics, grants, RLS or retained-receipt behavior.',
  'Build configuration must also be available to the deployed runtime; this gate cannot inspect runtime bindings.',
  'A real test-mode purchase, signed webhook, recovery and inbox delivery still require hosted validation.',
  'Resend webhook delivery and the production reconciliation monitor require their separate hosted checks.'
];

class GateError extends Error {}
const entry = (id, status, detail) => ({ id, status, detail });

async function responseFor(fetchImpl, url, headers, timeoutMs) {
  try {
    const response = await fetchImpl(url, { method: 'GET', headers, redirect: 'error', signal: AbortSignal.timeout(timeoutMs) });
    if (!response.ok) {
      await response.body?.cancel();
      throw new GateError(`Read-only hosted request returned HTTP ${response.status}.`);
    }
    return response;
  } catch (error) {
    if (error instanceof GateError) throw error;
    throw new GateError('Hosted request could not be verified (network, timeout or redirect failure).');
  }
}

// The request's abort signal remains attached while reading. Never buffer a ZIP.
async function readBounded(response, maximum, consume) {
  const length = response.headers.get('content-length');
  if (length !== null && (!/^\d+$/.test(length) || Number(length) > maximum)) {
    await response.body?.cancel();
    throw new GateError('Hosted response exceeded the permitted size.');
  }
  if (!response.body) throw new GateError('Hosted response had no readable body.');
  const reader = response.body.getReader();
  let bytes = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) return bytes;
      bytes += value.byteLength;
      if (bytes > maximum) throw new GateError('Hosted response exceeded the permitted size.');
      consume(value);
    }
  } catch (error) {
    try { await reader.cancel(); } catch { /* Preserve only a controlled error. */ }
    throw error instanceof GateError ? error : new GateError('Hosted response body could not be verified (read or timeout failure).');
  } finally { reader.releaseLock(); }
}

async function getJson(fetchImpl, url, headers, timeoutMs, maximum = MAX_SCHEMA_BYTES) {
  const response = await responseFor(fetchImpl, url, headers, timeoutMs);
  const chunks = [];
  await readBounded(response, maximum, chunk => chunks.push(Buffer.from(chunk)));
  try { return JSON.parse(Buffer.concat(chunks).toString('utf8')); }
  catch { throw new GateError('Hosted response was not valid JSON.'); }
}

function verifyMigrationShape(schema) {
  if (schema?.swagger !== '2.0') throw new GateError('The exposed database schema format could not be verified.');
  for (const [table, columns] of Object.entries(COLUMNS)) {
    const properties = schema.definitions?.[table]?.properties;
    if (!schema.paths?.[`/${table}`]?.get || !Object.entries(columns).every(([name, format]) =>
      properties?.[name]?.type === 'string' && properties[name].format === format)) {
      throw new GateError('Required migration 017 tables or column types are absent from the exposed schema.');
    }
  }
  // PostgREST OpenAPI v2 embeds RPC args in a body parameter, not requestBody.
  for (const [name, { required, optional }] of Object.entries(RPC_ARGUMENTS)) {
    const parameters = schema.paths?.[`/rpc/${name}`]?.post?.parameters;
    const bodies = Array.isArray(parameters) ? parameters.filter(parameter => parameter.in === 'body') : [];
    const body = bodies[0];
    const args = body?.schema;
    const names = [...required, ...optional];
    if (bodies.length !== 1 || body.required !== true || args?.type !== 'object'
        || !args.properties || Object.keys(args.properties).length !== names.length
        || !names.every(arg => args.properties[arg]?.type === 'string' && args.properties[arg]?.format === 'text')
        || !Array.isArray(args.required) || args.required.length !== required.length
        || !required.every(arg => args.required.includes(arg))) {
      throw new GateError('Required migration 017 RPC argument signatures could not be verified.');
    }
  }
}

export async function runHostedDeploymentGate({ env = process.env, fetchImpl = globalThis.fetch,
  expected = manifest, timeoutMs = 10_000, objectTimeoutMs = 60_000 } = {}) {
  const checks = [];
  const report = (skipped = false) => ({ ok: checks.every(check => check.status === 'pass'), skipped, checks, remaining: skipped ? [] : REMAINING });
  if (!Object.hasOwn(env, 'CF_PAGES') && !Object.hasOwn(env, 'CF_PAGES_BRANCH')) {
    checks.push(entry('hosting-context', 'pass', 'Hosted gate skipped outside Cloudflare Pages.'));
    return report(true);
  }
  if (env.CF_PAGES !== '1' || env.CF_PAGES_BRANCH !== 'main') {
    checks.push(entry('hosting-context', 'fail', 'Hosted gate requires Cloudflare Pages main; other or incomplete hosting contexts have no approved deployment policy.'));
    return report();
  }
  checks.push(entry('hosting-context', 'pass', 'Cloudflare Pages production branch confirmed.'));
  const effectiveEnv = { ...env, PUBLIC_ORIGIN: env.PUBLIC_ORIGIN ?? PRODUCTION_ORIGIN };
  if (![PRODUCTION_ORIGIN, `${PRODUCTION_ORIGIN}/`].includes(effectiveEnv.PUBLIC_ORIGIN)) {
    checks.push(entry('production-origin', 'fail', 'The production build must use the canonical public origin.'));
    return report();
  }
  const inspect = async (id, action) => {
    try { checks.push(entry(id, 'pass', await action())); }
    catch (error) { checks.push(entry(id, 'unverified', error instanceof GateError ? error.message : 'Hosted prerequisite could not be verified.')); }
  };
  // This validator prevents requests until all configured values are plausible.
  try {
    const launch = await checkLaunchReadiness({ env: effectiveEnv, services: true, mode: 'live', fetchImpl, expected, timeoutMs });
    checks.push(...launch.checks);
    if (!launch.ok) return report();
  } catch {
    checks.push(entry('service-preflight', 'unverified', 'Read-only service preflight could not complete.'));
    return report();
  }
  const origin = new URL(effectiveEnv.SUPABASE_URL).origin;
  const headers = { apikey: effectiveEnv.SUPABASE_SERVICE_KEY };
  if (!effectiveEnv.SUPABASE_SERVICE_KEY.startsWith('sb_secret_')) headers.Authorization = `Bearer ${effectiveEnv.SUPABASE_SERVICE_KEY}`;
  await inspect('migration-017-schema', async () => {
    const schema = await getJson(fetchImpl, `${origin}/rest/v1/`, { ...headers, Accept: 'application/openapi+json' }, timeoutMs);
    verifyMigrationShape(schema);
    return 'Required migration columns and RPC argument shapes are exposed; semantics and grants are not certified.';
  });
  const bucket = expected.bundle.bucket;
  await inspect('private-bundle-bucket', async () => {
    const metadata = await getJson(fetchImpl, `${origin}/storage/v1/bucket/${encodeURIComponent(bucket)}`, headers, timeoutMs, 64 * 1024);
    if (metadata?.id !== bucket || metadata.name !== bucket || metadata.public !== false) {
      throw new GateError('The reviewed download bucket was not verified as private with the expected identity.');
    }
    return 'The reviewed download bucket is private.';
  });
  // A private metadata check must pass before retrieving the book object.
  if (checks.at(-1).status === 'pass') {
    await inspect('remote-bundle-bytes', async () => {
      const { bytes, sha256, object } = expected.bundle;
      if (!Number.isSafeInteger(bytes) || bytes < 1 || !/^[a-f0-9]{64}$/.test(sha256)
          || typeof object !== 'string' || object.split('/').some(part => !part || part === '.' || part === '..')) {
        throw new GateError('The reviewed bundle manifest cannot safely bound verification.');
      }
      const path = object.split('/').map(encodeURIComponent).join('/');
      const response = await responseFor(fetchImpl, `${origin}/storage/v1/object/${encodeURIComponent(bucket)}/${path}`, headers, objectTimeoutMs);
      const hash = createHash('sha256');
      const actualBytes = await readBounded(response, bytes, chunk => hash.update(chunk));
      if (actualBytes !== bytes || hash.digest('hex') !== sha256) throw new GateError('Stored bundle size or SHA-256 does not match the reviewed release.');
      return 'Private stored ZIP bytes and SHA-256 match the reviewed release.';
    });
  }
  return report();
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  runHostedDeploymentGate().then(report => {
    console.log(JSON.stringify(report, null, 2));
    process.exitCode = report.ok ? 0 : 1;
  }).catch(() => { console.error('Hosted deployment prerequisites could not be verified.'); process.exitCode = 1; });
}
