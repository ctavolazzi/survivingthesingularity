import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { verifyOrUploadBundle } from './deploy-book-bundle.mjs';

const payload = Buffer.from('reviewed private artifact');
const expected = { bundle: { object: 'research-bundle-book-v0.11.0.zip', bucket: 'downloads',
  bytes: payload.length, sha256: createHash('sha256').update(payload).digest('hex') } };
function storage(initial, { corruptUpload = false } = {}) {
  let object = initial, writes = 0;
  return { get writes() { return writes; }, from() { return {
    async download() { return object ? { data: new Blob([object]), error: null } : { error: { statusCode: '404', message: 'Object not found' } }; },
    async upload(path, body, options) {
      assert.equal(path, expected.bundle.object); assert.equal(options.upsert, false);
      writes++; object = corruptUpload ? Buffer.from('wrong') : body; return { error: null };
    }
  }; } };
}
test('default verify never uploads a missing private artifact', async () => {
  const fake = storage(null);
  await assert.rejects(verifyOrUploadBundle(fake, expected, payload), /object is absent/);
  assert.equal(fake.writes, 0);
});
test('upload creates once, verifies bytes, and repeats without another write', async () => {
  const fake = storage(null);
  assert.deepEqual(await verifyOrUploadBundle(fake, expected, payload, { upload: true }), { uploaded: true, verified: true });
  assert.deepEqual(await verifyOrUploadBundle(fake, expected, payload, { upload: true }), { uploaded: false, verified: true });
  assert.equal(fake.writes, 1);
});
test('existing different bytes are never overwritten', async () => {
  const fake = storage(Buffer.from('older artifact'));
  await assert.rejects(verifyOrUploadBundle(fake, expected, payload, { upload: true }), /refusing to overwrite/);
  assert.equal(fake.writes, 0);
});
test('a successful storage response with wrong bytes fails verification', async () => {
  const fake = storage(null, { corruptUpload: true });
  await assert.rejects(verifyOrUploadBundle(fake, expected, payload, { upload: true }), /remote hash verification/);
});
test('storage access errors are not treated as a missing object', async () => {
  let writes = 0;
  const fake = { from() { return {
    async download() { return { error: { statusCode: '403', message: 'Access denied' } }; },
    async upload() { writes++; return { error: null }; }
  }; } };
  await assert.rejects(verifyOrUploadBundle(fake, expected, payload, { upload: true }), /Storage verification failed/);
  assert.equal(writes, 0);
});
