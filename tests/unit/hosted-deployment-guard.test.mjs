import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { hostedDeploymentGuard } from '../../scripts/vite-hosted-deployment-guard.mjs';

test('server build awaits verification and duplicate hooks share one result', async () => {
  let calls = 0;
  let release;
  const gate = hostedDeploymentGuard({ inspect: () => {
    calls++;
    return new Promise(resolve => { release = resolve; });
  } });
  assert.equal(gate.apply, 'build');
  gate.configResolved({ build: { ssr: true } });
  let finished = false;
  const first = gate.buildStart().then(() => { finished = true; });
  const second = gate.buildStart();
  await Promise.resolve();
  assert.equal(finished, false);
  assert.equal(calls, 1);
  release({ ok: true, skipped: true });
  await Promise.all([first, second]);
  assert.equal(finished, true);
});

test('nested client compilation never starts a second provider inspection', async () => {
  const gate = hostedDeploymentGuard({ inspect: () => { throw new Error('unexpected inspection'); } });
  gate.configResolved({ build: { ssr: false } });
  await gate.buildStart();
});

test('unverified hosted prerequisites reject the server build', async () => {
  const gate = hostedDeploymentGuard({ inspect: async () => ({ ok: false, checks: [] }) });
  gate.configResolved({ build: { ssr: true } });
  await assert.rejects(gate.buildStart(), /publication stopped/);
});

test('unexpected checker errors cannot expose their provider details through Vite', async () => {
  const secret = 'private-provider-value-sentinel';
  const gate = hostedDeploymentGuard({ inspect: async () => { throw new Error(secret); } });
  gate.configResolved({ build: { ssr: true } });
  await assert.rejects(gate.buildStart(), error => {
    assert.match(error.message, /publication stopped/);
    assert(!String(error.stack).includes(secret));
    assert.equal(error.cause, undefined);
    return true;
  });
});

test('the actual direct Vite build stops at the hosted gate without configured payment credentials', { timeout: 45_000 }, () => {
  const root = fileURLToPath(new URL('../../', import.meta.url));
  const vite = fileURLToPath(new URL('../../node_modules/vite/bin/vite.js', import.meta.url));
  const result = spawnSync(process.execPath, [vite, 'build'], {
    cwd: root,
    // An empty Stripe key makes preflight return before any provider request,
    // even if a developer has unrelated service credentials in their shell.
    env: { ...process.env, CF_PAGES: '1', CF_PAGES_BRANCH: 'main', STRIPE_SECRET_KEY: '' },
    encoding: 'utf8', timeout: 40_000
  });
  assert.equal(result.error, undefined);
  assert.notEqual(result.status, 0);
  // A parser/import failure must not masquerade as a working deployment guard.
  assert.match(result.stdout + result.stderr, /\[sts-hosted-deployment-guard\] Hosted deployment prerequisites are unverified; publication stopped/);
});
