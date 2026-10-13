#!/usr/bin/env node
// Exercise the actual Pages Worker with GET/HEAD requests only. This proves
// server imports, canonical chapter loading and static routing; it does not
// prove an unlocked browser reader or external payment/email integration.
import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { once } from 'node:events';
import { cp, mkdtemp, mkdir, readFile, readdir, rm, symlink, writeFile } from 'node:fs/promises';
import { createServer } from 'node:net';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { setTimeout as delay } from 'node:timers/promises';
import { expandRefs, assetName, releasedVersion } from '../src/lib/bookManifest.js';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const book = JSON.parse(await readFile(join(root, 'src/lib/data/book/book.json'), 'utf8'));
const config = JSON.parse(await readFile(join(root, 'wrangler.jsonc'), 'utf8'));
const output = join(root, config.pages_build_output_dir);
const routes = JSON.parse(await readFile(join(output, '_routes.json'), 'utf8'));
const matches = (rule, path) => rule.endsWith('*') ? path.startsWith(rule.slice(0, -1)) : path === rule;
const excluded = (path) => routes.exclude.some((rule) => matches(rule, path));
assert(routes.include.length + routes.exclude.length <= 100, 'Pages route rules exceed the limit');
for (const path of ['/book', ...book.sections.map((s) => `/book/${s.id}`), '/early-access', '/api/stripe-checkout', '/api/webhooks/stripe']) {
  assert(routes.include.some((rule) => matches(rule, path)) && !excluded(path), `${path} must reach the Worker`);
}
async function assertStaticCoverage(directory, prefix = '') {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const path = `${prefix}/${entry.name}`;
    if (entry.isDirectory()) await assertStaticCoverage(join(directory, entry.name), path);
    else assert(excluded(path), `Static asset is missing from Pages exclusions: ${path}`);
  }
}
await assertStaticCoverage(join(root, 'static'));
const redirects = (await readFile(join(root, '_redirects'), 'utf8'))
  .split('\n').map((line) => line.trim()).filter((line) => line && !line.startsWith('#'))
  .map((line) => line.split(/\s+/));
for (const [source] of redirects) {
  assert(excluded(source), `Redirect must bypass the Worker: ${source}`);
}

// Copy only build output into a fresh tree: Wrangler must never discover this
// checkout's .env/.dev.vars or the developer's authentication configuration.
const scratch = await mkdtemp(join(tmpdir(), 'sts-cloudflare-smoke-'));
let child;
let logs = '';
let probes = 0;
try {
  const kit = join(scratch, '.svelte-kit');
  await mkdir(kit);
  for (const directory of ['cloudflare', 'cloudflare-tmp', 'output/server']) {
    await cp(join(root, '.svelte-kit', directory), join(kit, directory), { recursive: true });
  }
  // The unbundled adapter output resolves third-party modules during Wrangler's
  // local build. A dependency-only link does not expose project dotenv files.
  await symlink(join(root, 'node_modules'), join(scratch, 'node_modules'), 'dir');
  await writeFile(join(scratch, 'package.json'), '{"type":"module"}\n');
  await writeFile(join(scratch, 'wrangler.jsonc'), JSON.stringify(config));
  const socket = createServer();
  socket.listen(0, '127.0.0.1');
  await once(socket, 'listening');
  const port = socket.address().port;
  await new Promise((resolve, reject) => socket.close((error) => error ? reject(error) : resolve()));

  const env = {};
  for (const key of ['PATH', 'SystemRoot', 'TMPDIR', 'TMP', 'TEMP', 'NODE_EXTRA_CA_CERTS', 'SSL_CERT_FILE', 'SSL_CERT_DIR', 'HTTPS_PROXY', 'HTTP_PROXY', 'ALL_PROXY', 'NO_PROXY', 'https_proxy', 'http_proxy', 'all_proxy', 'no_proxy']) {
    if (process.env[key]) env[key] = process.env[key];
  }
  Object.assign(env, {
    XDG_CONFIG_HOME: join(scratch, 'config'),
    WRANGLER_SEND_METRICS: 'false',
    CLOUDFLARE_LOAD_DEV_VARS_FROM_DOT_ENV: 'false',
    CI: 'true'
  });
  // `pages dev` runs workerd locally. No remote flags, credentials, application
  // environment, resource bindings, or mutating HTTP requests are supplied.
  child = spawn(process.execPath, [
    join(root, 'node_modules/wrangler/bin/wrangler.js'), 'pages', 'dev',
    join(kit, 'cloudflare'), '--ip', '127.0.0.1', '--port', String(port),
    '--inspector-port', '0', '--persist-to', join(scratch, 'state'),
    '--show-interactive-dev-session=false'
  ], { cwd: scratch, env, stdio: ['ignore', 'pipe', 'pipe'], detached: process.platform !== 'win32' });
  child.stdout.on('data', (chunk) => { logs = (logs + chunk).slice(-20000); });
  child.stderr.on('data', (chunk) => { logs = (logs + chunk).slice(-20000); });
  let spawnError;
  child.on('error', (error) => { spawnError = error; });
  const origin = `http://127.0.0.1:${port}`;
  const deadline = Date.now() + 60000;
  while (true) {
    if (spawnError) throw spawnError;
    assert(child.exitCode === null, `Wrangler exited before becoming ready (${child.exitCode})`);
    try {
      const response = await fetch(`${origin}/robots.txt`, { signal: AbortSignal.timeout(2000) });
      if (response.ok) break;
    } catch { /* startup is asynchronous */ }
    assert(Date.now() < deadline, 'Timed out waiting for local Pages Worker');
    await delay(200);
  }
  async function get(path, { status = 200, method = 'GET' } = {}) {
    const response = await fetch(`${origin}${path}`, { method, redirect: 'manual', signal: AbortSignal.timeout(15000) });
    assert.equal(response.status, status, `${method} ${path}`);
    probes += 1;
    return response;
  }
  const escapeHtml = (text) => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
  for (const section of book.sections) {
    const path = `/book/${section.id}`;
    const html = await (await get(path)).text();
    assert(html.includes(`<title>${escapeHtml(section.title)} | Surviving the Singularity</title>`), `${path}: correct SSR metadata`);
    assert(html.includes('Book access password'), `${path}: SSR reader gate`);
    assert(html.includes('content="noindex"'), `${path}: private-reader indexing policy`);
    const data = await (await get(`${path}/__data.json`)).json();
    const canonical = expandRefs(book, await readFile(join(root, 'src/lib/data/book', section.file), 'utf8'));
    assert(data.nodes?.some((node) => Array.isArray(node?.data) && node.data.includes(canonical)), `${path}: complete canonical markdown in server load`);
  }
  for (const [path, marker] of [
    ['/book', 'Read the Book | Surviving the Singularity'],
    ['/read', 'Book access password'],
    ['/sample', 'Start with the book.'],
    ['/early-access', 'Get the bundle now.']
  ]) {
    const html = await (await get(path)).text();
    assert(html.includes(marker), `${path}: expected rendered page content`);
    if (path === '/sample') {
      assert(html.includes('The Uncompromising Truth') && html.includes('How to Use This Book'), 'Public sample renders both excerpts');
      assert(html.includes('Upton Sinclair'), 'Public sample includes rendered canonical prose');
    }
  }
  const sitemap = await (await get('/sitemap.xml')).text();
  assert.equal(sitemap, await readFile(join(root, 'static/sitemap.xml'), 'utf8'), 'Published sitemap matches the authoritative file');
  await get('/fonts/inter-v20-latin.woff2', { method: 'HEAD' });
  const pdf = `/downloads/${assetName(releasedVersion(book), 'pdf')}`;
  const pdfResponse = await get(pdf, { method: 'HEAD' });
  assert(pdfResponse.headers.get('content-type')?.includes('application/pdf'), 'Current PDF has the correct MIME type');
  const alias = await get('/downloads/Surviving-the-Singularity.pdf', { method: 'HEAD', status: 302 });
  assert.equal(new URL(alias.headers.get('location'), origin).pathname, pdf, 'Stable PDF alias reaches current release');
  await get('/book/not-a-canonical-section', { status: 404 });
  const previews = spawnSync('python3', [join(root, 'scripts/check-social-previews.py'), '--origin', origin], {
    cwd: scratch, env, stdio: 'inherit'
  });
  if (previews.error) throw previews.error;
  assert.equal(previews.status, 0, 'Crawler-visible metadata and image checks must pass');
  console.log(`Cloudflare Pages runtime: ${probes} local GET/HEAD checks passed; ${book.sections.length} canonical chapter loads; ${routes.include.length + routes.exclude.length} route rules.`);
  console.log('Scope: Worker HTTP/SSR, chapter data, static sample/assets and redirects. Browser unlock and external services are separate release checks.');
} catch (error) {
  console.error(logs);
  throw error;
} finally {
  if (child?.pid && child.exitCode === null) {
    const stopped = once(child, 'exit').catch(() => {});
    try {
      if (process.platform === 'win32') child.kill('SIGTERM');
      else process.kill(-child.pid, 'SIGTERM');
    } catch { /* process already exited */ }
    await Promise.race([stopped, delay(3000)]);
    if (child.exitCode === null && child.signalCode === null) {
      try {
        if (process.platform === 'win32') child.kill('SIGKILL');
        else process.kill(-child.pid, 'SIGKILL');
      } catch { /* process already exited */ }
      await stopped;
    }
  }
  await rm(scratch, { recursive: true, force: true });
}
