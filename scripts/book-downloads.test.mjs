import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { verifyDownloadReceipt, hash } from './lib/book-download-receipt.mjs';

test('download proof rejects changed bytes and stale source, allows the release stamp', () => {
  const root = mkdtempSync(join(tmpdir(), 'sts-download-proof-'));
  const directory = join(root, 'downloads');
  const source = join(root, 'src/lib/data/book');
  mkdirSync(directory); mkdirSync(source, { recursive: true });
  try {
    const manifest = { version: '0.11.0', released: '0.7.5', sections: [{ file: 'chapter.md' }] };
    const raw = JSON.stringify(manifest);
    writeFileSync(join(source, 'book.json'), raw);
    writeFileSync(join(source, 'chapter.md'), 'Current, corrected chapter.');
    writeFileSync(join(root, 'art.svg'), '<svg/>');
    const receipt = {
      schema: 1, version: manifest.version, source_manifest_release_independent: true,
      source_sha256: { 'book.json': hash(raw.replace(/"released":\s*"[^"]*"/, '"released": "<release>"')),
        'chapter.md': hash('Current, corrected chapter.') }, input_sha256: { 'art.svg': hash('<svg/>') }, artifacts: {}
    };
    for (const ext of ['pdf', 'epub']) {
      const name = `Surviving-the-Singularity-v${manifest.version}.${ext}`;
      const bytes = Buffer.from(`proved ${ext}`);
      writeFileSync(join(directory, name), bytes);
      receipt.artifacts[ext] = { name, bytes: bytes.length, sha256: hash(bytes) };
    }
    const check = () => verifyDownloadReceipt({ root, directory, receipt, manifest, version: manifest.version });
    assert.doesNotThrow(check);
    manifest.released = manifest.version;
    writeFileSync(join(source, 'book.json'), JSON.stringify(manifest));
    assert.doesNotThrow(check);
    writeFileSync(join(source, 'chapter.md'), 'An unbuilt chapter edit.');
    assert.throws(check, /stale: chapter.md/);
    assert.doesNotThrow(() => verifyDownloadReceipt({ root, directory, receipt,
      manifest: { ...manifest, version: '0.12.0' }, version: '0.11.0' }));
    writeFileSync(join(source, 'chapter.md'), 'Current, corrected chapter.');
    writeFileSync(join(root, 'art.svg'), '<svg>new art</svg>');
    assert.throws(check, /artwork\/layout proof is stale/);
    writeFileSync(join(root, 'art.svg'), '<svg/>');
    writeFileSync(join(directory, receipt.artifacts.pdf.name), 'wrong pdf!');
    assert.throws(check, /differs from its verified download proof/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
