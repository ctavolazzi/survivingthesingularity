// Update the preorder bundle on Supabase: back up current zip, add the book
// draft PDF into it, re-upload in place, and upload a standalone PDF.
import { createClient } from '@supabase/supabase-js';
import { readFileSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';

const env = Object.fromEntries(
  readFileSync('/Users/ctavolazzi/Code/active/survivingthesingularity/.env', 'utf8')
    .split('\n')
    .filter(l => l.includes('=') && !l.trim().startsWith('#'))
    .map(l => [l.slice(0, l.indexOf('=')).trim(), l.slice(l.indexOf('=') + 1).trim()])
);

const BUCKET = env.DOWNLOAD_BUCKET || 'downloads';
const BUNDLE_PATH = env.DOWNLOAD_BUNDLE_PATH || 'research-bundle-v1.zip';
const PDF_LOCAL = '/Users/ctavolazzi/Code/active/survivingthesingularity/manuscript/Surviving-the-Singularity-Book-Draft-v0.2.pdf';
const PDF_NAME = 'Surviving-the-Singularity-Book-Draft-v0.2.pdf';
const WORK = process.env.WORKDIR;
const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');

const supabase = createClient(env.SUPABASE_URL, env.SUPABASE_SERVICE_KEY, {
  auth: { persistSession: false, autoRefreshToken: false },
});

// 1. List bucket to confirm bundle exists
const { data: listing, error: listErr } = await supabase.storage.from(BUCKET).list('', { limit: 100 });
if (listErr) throw new Error('list failed: ' + listErr.message);
console.log('bucket contents:', listing.map(f => `${f.name} (${f.metadata?.size ?? '?'} bytes)`).join(', '));

const exists = listing.some(f => f.name === BUNDLE_PATH);
if (!exists) throw new Error(`bundle ${BUNDLE_PATH} not found in bucket ${BUCKET} — aborting`);

// 2. Download current bundle
const { data: blob, error: dlErr } = await supabase.storage.from(BUCKET).download(BUNDLE_PATH);
if (dlErr) throw new Error('download failed: ' + dlErr.message);
const buf = Buffer.from(await blob.arrayBuffer());
writeFileSync(`${WORK}/bundle-current.zip`, buf);
console.log(`downloaded ${BUNDLE_PATH}: ${buf.length} bytes`);
console.log(execSync(`unzip -l "${WORK}/bundle-current.zip"`).toString());

// 3. Upload a timestamped backup of the untouched original
const backupName = BUNDLE_PATH.replace(/\.zip$/, `-backup-${today}.zip`);
const up1 = await supabase.storage.from(BUCKET).upload(backupName, buf, {
  contentType: 'application/zip', upsert: true,
});
if (up1.error) throw new Error('backup upload failed: ' + up1.error.message);
console.log('backup uploaded as', backupName);

// 4. Add the PDF into the zip
execSync(`cp "${PDF_LOCAL}" "${WORK}/${PDF_NAME}" && cd "${WORK}" && zip -j bundle-current.zip "${PDF_NAME}"`);
console.log(execSync(`unzip -l "${WORK}/bundle-current.zip"`).toString());

// 5. Re-upload bundle in place (same path → existing env config keeps working)
const newBuf = readFileSync(`${WORK}/bundle-current.zip`);
const up2 = await supabase.storage.from(BUCKET).upload(BUNDLE_PATH, newBuf, {
  contentType: 'application/zip', upsert: true,
});
if (up2.error) throw new Error('bundle re-upload failed: ' + up2.error.message);
console.log(`re-uploaded ${BUNDLE_PATH}: ${newBuf.length} bytes`);

// 6. Standalone PDF for direct linking
const pdfBuf = readFileSync(PDF_LOCAL);
const up3 = await supabase.storage.from(BUCKET).upload(PDF_NAME, pdfBuf, {
  contentType: 'application/pdf', upsert: true,
});
if (up3.error) throw new Error('pdf upload failed: ' + up3.error.message);
console.log(`standalone PDF uploaded: ${PDF_NAME} (${pdfBuf.length} bytes)`);

// 7. Verify with a signed URL
const { data: signed, error: sErr } = await supabase.storage.from(BUCKET).createSignedUrl(BUNDLE_PATH, 300);
if (sErr) throw new Error('signed url failed: ' + sErr.message);
console.log('verified signed URL OK');
