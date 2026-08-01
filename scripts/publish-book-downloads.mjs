#!/usr/bin/env node
/**
 * BOOK DOWNLOAD PUBLISH
 *
 * Copies the built book out of book-build/ into static/downloads/, deriving
 * every filename from book.json.
 *
 * WHY THIS EXISTS
 *
 * This step used to be a person. src/lib/data/book/README.md described the
 * "static/downloads/ swap" as something that "happen[s] once, at version
 * close", and scripts/check-book-downloads.mjs ended its failure message with a
 * cp line for a human to retype:
 *
 *     fix: cp book-build/Surviving-the-Singularity-v0.7.4.pdf static/downloads/
 *
 * A correct instruction is still a manual step, and on 2026-08-01 the manual
 * step did not happen: book.json said 0.7.4, static/downloads/ held 0.7.2, and
 * the derived link 404'd for every friend who had been handed the password.
 * Retyping a version into a shell is exactly the operation that check exists to
 * prove nobody has to do.
 *
 * WHAT IT DELIBERATELY DOES NOT DO
 *
 * This does not run at prebuild. A copy that fires on every build would ship
 * whatever artifact happened to be sitting in book-build/, which is worse than
 * a missing file because it is a wrong file that passes. Publishing stays an
 * explicit gesture at version close - the person still decides WHEN, they just
 * no longer type WHAT. `npm run check:downloads` fails the build until it is
 * done, so a forgotten publish surfaces as a red build rather than a 404.
 *
 * It also does not judge the artifact. Size limits, Cloudflare's asset ceiling
 * and redirect generation belong to check-book-downloads.mjs. This script
 * places files; that one asserts them. Running both is `npm run book:release`.
 *
 * Usage:
 *   npm run book:publish          copy the current version into static/downloads/
 *   npm run book:publish -- --dry show what would be copied, touch nothing
 */

import { readFileSync, writeFileSync, existsSync, statSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import { assetName, DOWNLOAD_FORMATS } from '../src/lib/bookManifest.js';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const BOOK_JSON = 'src/lib/data/book/book.json';
const BUILD = 'book-build';
const DOWNLOADS = 'static/downloads';

const dryRun = process.argv.includes('--dry');
const mib = (bytes) => (bytes / 1024 / 1024).toFixed(2);
const digest = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');

// ── Read the single source of truth ──────────────────────────────────────────

let version;
try {
  version = JSON.parse(readFileSync(join(ROOT, BOOK_JSON), 'utf8')).version;
} catch (err) {
  console.error(`\npublish-book-downloads: cannot read ${BOOK_JSON}: ${err.message}\n`);
  process.exit(1);
}

if (!version) {
  console.error(`\npublish-book-downloads: ${BOOK_JSON} has no "version". Every download path is derived from it.\n`);
  process.exit(1);
}

// ── Resolve what should ship ─────────────────────────────────────────────────

const missing = [];
const planned = [];

for (const ext of DOWNLOAD_FORMATS) {
  const name = assetName(version, ext);
  const from = join(ROOT, BUILD, name);
  const to = join(ROOT, DOWNLOADS, name);

  if (!existsSync(from)) {
    missing.push({ name, from: `${BUILD}/${name}` });
    continue;
  }

  // Byte-identical means already published. Comparing content rather than
  // mtime keeps this idempotent across a rebuild that produced the same file.
  const unchanged = existsSync(to) && digest(from) === digest(to);
  planned.push({ name, from, to, bytes: statSync(from).size, unchanged });
}

if (missing.length) {
  console.error(`\npublish-book-downloads: ${missing.length} artifact(s) for v${version} were never built.\n`);
  for (const m of missing) console.error(`  ${m.from} does not exist`);
  console.error(`\n  fix: scripts/build-epub.sh v${version}\n`);
  process.exit(1);
}

// ── Place them ───────────────────────────────────────────────────────────────

if (!dryRun) mkdirSync(join(ROOT, DOWNLOADS), { recursive: true });

let copied = 0;
for (const p of planned) {
  if (p.unchanged) {
    console.log(`publish-book-downloads: ${p.name} already published, unchanged (${mib(p.bytes)} MiB)`);
    continue;
  }
  if (dryRun) {
    console.log(`publish-book-downloads: WOULD copy ${p.name} (${mib(p.bytes)} MiB) -> ${DOWNLOADS}/`);
    continue;
  }
  writeFileSync(p.to, readFileSync(p.from));
  copied += 1;
  console.log(`publish-book-downloads: published ${p.name} (${mib(p.bytes)} MiB)`);
}

if (dryRun) {
  console.log(`publish-book-downloads: dry run, nothing written. v${version}.`);
  process.exit(0);
}

console.log(
  `publish-book-downloads: v${version} in ${DOWNLOADS}/ ` +
    `(${copied} copied, ${planned.length - copied} already current). ` +
    `Run \`npm run check:downloads\` to assert what ships.`
);
process.exit(0);
