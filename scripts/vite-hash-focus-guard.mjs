import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';

const require = createRequire(import.meta.url);
export const kitClientPath = join(dirname(require.resolve('@sveltejs/kit/package.json')), 'src/runtime/client/client.js');
const normalize = path => path.replaceAll('\\', '/').split('?')[0];
const target = normalize(kitClientPath);

const functionStart = 'function reset_focus(url, scroll = true) {';
const callbackStart = [
  '\t\t\tsetTimeout(() => {',
  '\t\t\t\tconst history_state = history.state;',
  '',
  '\t\t\t\tresetting_focus = true;',
  '\t\t\t\tlocation.replace(new URL(`#${id}`, location.href));'
].join('\n');
const guardedCallback = callbackStart.replace(
  'setTimeout(() => {\n',
  'setTimeout(() => {\n\t\t\t\tif (location.href !== url.href) return;\n'
);

/**
 * Kit 2.70.3 defers fragment focus, then rewrites history using the old URL.
 * A quick forward navigation can finish before that callback runs. Refuse to
 * let a superseded callback change the new entry. Remove after an upstream
 * compatible fix; a changed upstream implementation requires explicit review.
 */
export function guardHashFocus(source) {
  const start = source.indexOf(functionStart);
  const callback = source.indexOf(callbackStart);
  const nextFunction = source.indexOf('\nfunction ', start + functionStart.length);
  if (start < 0 || source.indexOf(functionStart, start + 1) !== -1
      || callback <= start || source.indexOf(callbackStart, callback + 1) !== -1
      || (nextFunction !== -1 && callback >= nextFunction)) {
    throw new Error('SvelteKit fragment-focus implementation changed. Review and remove or update the stale-history guard before building.');
  }
  return source.replace(callbackStart, guardedCallback);
}

export function hashFocusGuard() {
  let requireClientTransform = false;
  let transformed = false;
  return {
    name: 'sts-stale-hash-focus-guard',
    enforce: 'pre',
    configResolved(config) {
      requireClientTransform = config.command === 'build' && !config.build.ssr;
    },
    buildStart() {
      transformed = false;
      // Fail even when an upgraded dependency stops importing this module.
      guardHashFocus(readFileSync(kitClientPath, 'utf8'));
    },
    transform(source, id) {
      if (normalize(id) !== target) return null;
      transformed = true;
      return { code: guardHashFocus(source), map: null };
    },
    generateBundle() {
      if (requireClientTransform && !transformed) {
        throw new Error('SvelteKit fragment-focus guard did not reach the browser bundle. Review the client runtime path before building.');
      }
    }
  };
}
