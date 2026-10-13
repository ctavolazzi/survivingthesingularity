import { spawnSync } from 'node:child_process';

const suites = [
  ['--experimental-vm-modules', 'tests/server/payment-reliability.test.mjs'],
  ['tests/unit/signup-delivery.test.mjs'],
  ['tests/unit/sitemap.test.mjs'],
  ['tests/unit/bundle-release.test.mjs'],
  ['tests/unit/book-math.test.mjs'],
  ['tests/unit/sanitize-html.test.mjs'],
  ['tests/unit/request-json.test.mjs'],
  ['tests/unit/hash-focus-guard.test.mjs'],
  ['scripts/check-launch-readiness.test.mjs'],
  ['scripts/book-downloads.test.mjs'],
  ['scripts/deploy-book-bundle.test.mjs']
];
for (const args of suites) {
  const result = spawnSync(process.execPath, args, { stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status || 1);
}
