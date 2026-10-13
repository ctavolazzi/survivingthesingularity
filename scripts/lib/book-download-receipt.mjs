import { createHash } from 'node:crypto';
import { readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { assetName, DOWNLOAD_FORMATS } from '../../src/lib/bookManifest.js';

export const DOWNLOAD_LIMIT = 25 * 1024 * 1024;
export const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');

/** Bind the actual downloadable bytes to a proved edition and canonical source. */
export function verifyDownloadReceipt({ root, directory, receipt, manifest, version }) {
  if (receipt.schema !== 1 || receipt.version !== version || !receipt.source_manifest_release_independent) {
    throw new Error(`Missing or unsupported download proof for v${version}; run python3 scripts/prepare-book-downloads.py`);
  }
  for (const ext of DOWNLOAD_FORMATS) {
    const expected = receipt.artifacts?.[ext];
    const name = assetName(version, ext);
    const path = join(directory, name);
    const bytes = statSync(path).size;
    if (expected?.name !== name || bytes !== expected.bytes || bytes >= DOWNLOAD_LIMIT || hash(readFileSync(path)) !== expected.sha256) {
      throw new Error(`${name} differs from its verified download proof or exceeds the Pages limit`);
    }
  }
  // An open editing cycle may differ from the last published edition. When the
  // labels match, edits to a chapter or its ordering require a fresh artifact.
  if (manifest.version === version) {
    const names = ['book.json', ...manifest.sections.map(section => section.file)];
    if (Object.keys(receipt.source_sha256 ?? {}).length !== names.length) throw new Error('Download proof omits source files');
    for (const name of names) {
      let data = readFileSync(join(root, 'src/lib/data/book', name));
      if (name === 'book.json') data = data.toString().replace(/"released":\s*"[^"]*"/, '"released": "<release>"');
      if (hash(data) !== receipt.source_sha256[name]) throw new Error(`Download proof is stale: ${name}`);
    }
    if (!receipt.input_sha256 || !Object.keys(receipt.input_sha256).length) throw new Error('Download proof omits artwork inputs');
    for (const [path, expected] of Object.entries(receipt.input_sha256)) {
      if (hash(readFileSync(join(root, path))) !== expected) throw new Error(`Download artwork/layout proof is stale: ${path}`);
    }
  }
}
