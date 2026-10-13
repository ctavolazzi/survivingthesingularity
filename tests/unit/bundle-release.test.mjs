import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateBundleRelease } from '../../src/lib/bundleRelease.js';

const manifest = { bundle: { object: 'current.zip', sha256: 'reviewed-hash', bucket: 'downloads' }, book: { version: '0.11.0' } };
const configured = { DOWNLOAD_BUNDLE_PATH: 'current.zip', DOWNLOAD_BUNDLE_SHA256: 'reviewed-hash', DOWNLOAD_BUNDLE_BOOK_VERSION: '0.11.0' };
test('only the reviewed version, path and checksum can enable delivery', () => {
  assert.equal(validateBundleRelease(configured, manifest).ok, true);
  for (const field of Object.keys(configured)) {
    assert.equal(validateBundleRelease({ ...configured, [field]: 'old' }, manifest).ok, false, field);
    assert.equal(validateBundleRelease({ ...configured, [field]: undefined }, manifest).ok, false, field);
  }
  assert.equal(validateBundleRelease({}, manifest).ok, false);
  assert.equal(validateBundleRelease(configured, {}).ok, false);
  assert.equal(validateBundleRelease({ ...configured, DOWNLOAD_BUCKET: 'unverified' }, manifest).ok, false);
});
