#!/usr/bin/env node
/** Verify the reviewed private ZIP. Only --upload may create a storage object. */
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createClient } from '@supabase/supabase-js';
import manifest from '../src/lib/data/bundleManifest.js';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const sha256 = data => createHash('sha256').update(data).digest('hex');

export function verifyLocalBundle(root, expected) {
  const { bundle, book } = expected;
  if (!/^research-bundle-book-v\d+\.\d+\.\d+\.zip$/.test(bundle.object)) throw new Error('Expected a versioned book bundle object');
  const directory = join(root, 'book-build', `bundle-v${book.version}`);
  const prepared = JSON.parse(readFileSync(join(directory, 'manifest.json'), 'utf8'));
  if (JSON.stringify(prepared) !== JSON.stringify(expected)) throw new Error('Prepared and active bundle manifests differ');
  const payload = readFileSync(join(directory, bundle.object));
  if (payload.length !== bundle.bytes || sha256(payload) !== bundle.sha256) throw new Error('Local ZIP differs from the reviewed manifest');
  const current = JSON.parse(readFileSync(join(root, 'src/lib/data/book/book.json'), 'utf8'));
  if (current.version !== book.version || current.released !== book.version) throw new Error('Bundle contains an obsolete book edition');
  for (const input of Object.values(expected.inputs)) {
    if (sha256(readFileSync(join(root, input.path))) !== input.sha256) throw new Error(`Bundle source changed: ${input.path}`);
  }
  for (const ext of ['pdf', 'epub']) {
    const file = expected.files.find(file => file.path === `The-Precedent-File/book/Surviving-the-Singularity.${ext}`);
    if (!file || file.sha256 !== sha256(readFileSync(join(root, 'static/downloads', `Surviving-the-Singularity-v${book.version}.${ext}`)))) {
      throw new Error(`Private ${ext} differs from the proved public book`);
    }
  }
  return payload;
}

const isMissing = error => String(error?.statusCode ?? error?.status) === '404'
  || (String(error?.statusCode ?? error?.status) === '400' && /^object not found\.?$/i.test(error?.message ?? ''));

async function matches(data, expected) {
  const bytes = Buffer.from(await data.arrayBuffer());
  return bytes.length === expected.bytes && sha256(bytes) === expected.sha256;
}

/** No overwrite path: a changed artifact needs a new reviewed version. */
export async function verifyOrUploadBundle(storage, expected, payload, { upload = false } = {}) {
  const { bundle } = expected;
  if (payload.length !== bundle.bytes || sha256(payload) !== bundle.sha256) throw new Error('Unverified upload payload');
  const bucket = storage.from(bundle.bucket);
  const existing = await bucket.download(bundle.object);
  if (!existing.error) {
    if (!await matches(existing.data, bundle)) throw new Error('Existing versioned storage object has different bytes; refusing to overwrite');
    return { uploaded: false, verified: true };
  }
  if (!isMissing(existing.error)) throw new Error(`Storage verification failed: ${existing.error.message}`);
  if (!upload) throw new Error('Reviewed storage object is absent; use --upload only when ready to create it');
  const result = await bucket.upload(bundle.object, payload, { contentType: 'application/zip', upsert: false });
  // Read back even after an ambiguous upload response. A concurrent identical
  // upload is safe; a different existing object is never overwritten.
  const fetched = await bucket.download(bundle.object);
  if (fetched.error || !await matches(fetched.data, bundle)) {
    throw new Error(result.error ? `Upload not verified: ${result.error.message}` : 'Uploaded object failed remote hash verification');
  }
  return { uploaded: !result.error, verified: true };
}

async function main() {
  const args = new Set(process.argv.slice(2));
  if ([...args].some(arg => !['--upload', '--local'].includes(arg)) || (args.has('--upload') && args.has('--local'))) {
    throw new Error('Usage: node scripts/deploy-book-bundle.mjs [--local | --upload]');
  }
  const payload = verifyLocalBundle(ROOT, manifest);
  console.log(`Local bundle verified: ${manifest.bundle.object}, ${payload.length} bytes, SHA256 ${manifest.bundle.sha256}`);
  if (args.has('--local')) return;
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_KEY || process.env.SUPABASE_SECRET_KEY;
  if (!url || !key) throw new Error('Set SUPABASE_URL and SUPABASE_SERVICE_KEY (or SUPABASE_SECRET_KEY) in this process environment; no credentials are written to disk');
  const client = createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } });
  const result = await verifyOrUploadBundle(client.storage, manifest, payload, { upload: args.has('--upload') });
  console.log(`Remote bundle ${result.uploaded ? 'created and ' : ''}verified. Configure the deployment with:`);
  console.log(`DOWNLOAD_BUCKET=${manifest.bundle.bucket}\nDOWNLOAD_BUNDLE_PATH=${manifest.bundle.object}\nDOWNLOAD_BUNDLE_SHA256=${manifest.bundle.sha256}\nDOWNLOAD_BUNDLE_BOOK_VERSION=${manifest.book.version}`);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
