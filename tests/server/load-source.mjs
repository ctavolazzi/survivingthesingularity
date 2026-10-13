import { readFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { SourceTextModule, SyntheticModule, createContext } from 'node:vm';
import { webcrypto } from 'node:crypto';

// Evaluate actual server modules, with external IO replaced explicitly. This
// catches control-flow regressions without credentials, network or a dev server.
export async function loadSource(path, mocks = {}) {
  const context = createContext({
    URL, Request, Response, Headers, TextEncoder, TextDecoder, crypto: webcrypto,
    Date, console: { log() {}, warn() {}, error() {} }, setTimeout, clearTimeout,
    fetch() { throw new Error('External requests forbidden in server regressions'); },
  });
  const modules = new Map();
  const create = async (filename) => {
    if (modules.has(filename)) return modules.get(filename);
    const mod = new SourceTextModule(await readFile(filename, 'utf8'), { context, identifier: filename });
    modules.set(filename, mod);
    await mod.link(async (specifier, referring) => {
      if (Object.hasOwn(mocks, specifier)) {
        const values = mocks[specifier];
        return new SyntheticModule(Object.keys(values), function () {
          for (const [key, value] of Object.entries(values)) this.setExport(key, value);
        }, { context });
      }
      if (specifier.startsWith('.')) return create(resolve(dirname(referring.identifier), specifier));
      if (specifier.startsWith('$lib/')) return create(resolve('src/lib', specifier.slice(5)));
      throw new Error(`Unmocked dependency: ${specifier}`);
    });
    return mod;
  };
  const mod = await create(resolve(path));
  await mod.evaluate();
  return mod.namespace;
}

export function query(result, onCall = () => {}) {
  const calls = [];
  const chain = new Proxy({}, { get(_target, key) {
    if (key === 'then') return (resolve, reject) => Promise.resolve(typeof result === 'function' ? result(calls) : result).then(resolve, reject);
    return (...args) => { calls.push([key, ...args]); onCall(key, args); return chain; };
  } });
  return chain;
}
