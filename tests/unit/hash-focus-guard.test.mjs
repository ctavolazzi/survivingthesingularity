import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { parse } from 'acorn';
import { guardHashFocus, hashFocusGuard, kitClientPath } from '../../scripts/vite-hash-focus-guard.mjs';

const source = readFileSync(kitClientPath, 'utf8');
const patched = guardHashFocus(source);
function extractedFunction(code) {
  const node = parse(code, { ecmaVersion: 'latest', sourceType: 'module' }).body.find(node => node.type === 'FunctionDeclaration' && node.id.name === 'reset_focus');
  assert(node, 'Installed runtime must contain the function being tested.');
  return code.slice(node.start, node.end);
}
function focusHarness(code) {
  const callbacks = [], writes = [];
  const original = 'https://survivingthesingularity.com/sample?utm_source=instagram#how-to-use';
  const location = { href: original, replace(url) { this.href = String(url); writes.push({ kind: 'location', url: this.href }); } };
  const history = { state: { navigation: 'sample' }, replaceState(state, _title, url) { this.state = state; location.href = String(url); writes.push({ kind: 'history', url: location.href }); } };
  const sandbox = {
    URL, location, history, resetting_focus: false,
    document: { querySelector: () => null, getElementById: () => ({}) },
    getSelection: () => null,
    get_id: url => url.hash.slice(1), scroll_state: () => ({ x: 0, y: 100 }),
    scrollTo() {}, setTimeout: callback => callbacks.push(callback)
  };
  vm.createContext(sandbox);
  vm.runInContext(extractedFunction(code) + '\nthis.focusForTest = reset_focus;', sandbox);
  sandbox.focusForTest(new URL(original));
  assert.equal(callbacks.length, 1);
  return { location, history, writes, flush: () => callbacks.shift()(), original };
}

test('the installed unguarded callback reproduces the observed stale-history overwrite', () => {
  const runtime = focusHarness(source);
  runtime.location.href = 'https://survivingthesingularity.com/early-access';
  runtime.history.state = { navigation: 'offer' };
  runtime.flush();
  assert.equal(runtime.location.href, runtime.original);
  assert.equal(runtime.writes.length, 2);
});

test('the guarded installed callback leaves a newer navigation and its history untouched', () => {
  const runtime = focusHarness(patched);
  runtime.location.href = 'https://survivingthesingularity.com/early-access';
  const newer = runtime.history.state = { navigation: 'offer' };
  runtime.flush();
  assert.equal(runtime.location.href, 'https://survivingthesingularity.com/early-access');
  assert.equal(runtime.history.state, newer);
  assert.deepEqual(runtime.writes, []);
});

test('the active fragment navigation keeps the original focus behavior', () => {
  const runtime = focusHarness(patched);
  const state = runtime.history.state;
  runtime.flush();
  assert.equal(runtime.location.href, runtime.original);
  assert.equal(runtime.history.state, state);
  assert.equal(runtime.writes.length, 2);
});

test('unknown, duplicated or already-patched runtime shapes fail closed', () => {
  assert.throws(() => guardHashFocus('export const updated = true;'), /implementation changed/);
  assert.throws(() => guardHashFocus(source + '\n' + extractedFunction(source)), /implementation changed/);
  assert.throws(() => guardHashFocus(patched), /implementation changed/);
});

test('Vite applies the guard only to the resolved Kit client and requires it in client builds', () => {
  const plugin = hashFocusGuard();
  plugin.configResolved({ command: 'build', build: { ssr: false } });
  plugin.buildStart();
  assert.equal(plugin.transform(source, '/app/src/runtime/client/client.js'), null);
  assert.throws(() => plugin.generateBundle(), /did not reach/);
  assert.equal(plugin.transform(source, kitClientPath + '?v=fixture').code, patched);
  plugin.generateBundle();
  plugin.configResolved({ command: 'build', build: { ssr: true } });
  plugin.buildStart();
  plugin.generateBundle();
});
