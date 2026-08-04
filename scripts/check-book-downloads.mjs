#!/usr/bin/env node
/**
 * BOOK DOWNLOAD ASSERTION
 *
 * Fails the build if the book files the site LINKS TO are not the book files
 * the site SHIPS, or if they cannot survive a Cloudflare Pages deploy.
 *
 * WHY THIS EXISTS
 *
 * On 2026-08-01 the PDF download on /exclusive-friends-only was found 404ing
 * in production. Nothing was broken in the sense of a bug. Two surfaces build
 * the download URL by deriving it from book.json:
 *
 *     const pdfHref = `/downloads/Surviving-the-Singularity-v${book.version}.pdf`;
 *
 * book.json said 0.7.4. static/downloads/ held 0.7.2. The link was generated
 * correctly, pointed at a file that had never been shipped, and returned 404
 * to every friend who was handed the password.
 *
 * The gap was documented and still missed. src/lib/data/book/README.md says
 * the "static/downloads/ swap happen[s] once, at version close" - a manual
 * step in prose, which is the same as no step at all on the one release where
 * it matters. The href is derived; the file was hand-placed; nothing asserted
 * that the two agreed. This file is that assertion.
 *
 * THE SECOND FAILURE THIS CATCHES
 *
 * A Cloudflare Pages site asset has a hard 25 MiB ceiling
 * (developers.cloudflare.com/pages/platform/limits/#file-size). v0.7.4 is
 * 22.34 MiB. There is under 3 MiB of headroom, and the book gains images
 * every version. When it crosses the line, the DEPLOY fails, not the build -
 * which surfaces far from the change that caused it and long after it merged.
 * WARN_AT_FRACTION below turns that cliff into a runway.
 *
 * When the warning fires, the fix is not to compress the book. It is to move
 * the file to an R2 public bucket on a subdomain: R2 charges nothing for
 * egress at any volume, so the hosting cost of the book does not change.
 *
 * THE DESIGN DECISION THAT MATTERS
 *
 * Nothing here hardcodes a version. The expected filenames are built from
 * book.json at lint time, so bumping the book to 0.7.5 retargets this check
 * automatically. A check with "0.7.4" baked into it would go quietly green on
 * exactly the release where it was needed, which is the failure it exists to
 * prevent.
 *
 * It also GENERATES static/_redirects, for the same reason: a redirect target
 * typed by hand is one more copy of the version to forget.
 */

import { readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

// The filename rule is shared with the two route components that build the
// href and with scripts/publish-book-downloads.mjs, which places the files.
// Asserting a name this script spells itself would only prove it agrees with
// itself - the 404 this check exists to prevent was four copies of one string.
import { assetName, DOWNLOAD_FORMATS, releasedVersion } from '../src/lib/bookManifest.js';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const BOOK_JSON = 'src/lib/data/book/book.json';
const DOWNLOADS = 'static/downloads';
const REDIRECTS = 'static/_redirects';

/** Cloudflare Pages hard limit for a single site asset. Not negotiable. */
const PAGES_MAX_BYTES = 25 * 1024 * 1024;

/** Warn once an artifact is this close to the ceiling, so the cliff is visible early. */
const WARN_AT_FRACTION = 0.85;

/**
 * Versions that were live at some point and may still be in somebody's text
 * message or preorder email. They get redirected to the current file rather
 * than 404ing. Append at version close; never remove.
 */
const RETIRED_VERSIONS = ['0.7.2', '0.7.3'];

const FORMATS = DOWNLOAD_FORMATS;

const mib = (bytes) => (bytes / 1024 / 1024).toFixed(2);

// ── Read the single source of truth ──────────────────────────────────────────

let manifest;
try {
  manifest = JSON.parse(readFileSync(join(ROOT, BOOK_JSON), 'utf8'));
} catch (err) {
  console.error(`\ncheck-book-downloads: cannot read ${BOOK_JSON}: ${err.message}\n`);
  process.exit(1);
}

if (!manifest.version) {
  console.error(`\ncheck-book-downloads: ${BOOK_JSON} has no "version".\n`);
  process.exit(1);
}

/**
 * TWO VERSIONS, TWO JOBS - see releasedVersion() in src/lib/bookManifest.js.
 *
 * Everything a reader touches derives from `released`, the newest PUBLISHED
 * build. `version` is the open working label and runs ahead of `released` for
 * the whole editing cycle. This check used to derive from `version`, which
 * made it fail on every mid-cycle push by construction: weeks of failure
 * emails that all meant "the cycle is open", burying the one that would have
 * meant "readers are getting 404s". An alarm that is expected to be red is
 * not an alarm (2026-08-04, CT). Now green means the released files exist and
 * every derived link resolves, in ANY cycle state; red means a reader-facing
 * problem, full stop.
 */
const version = releasedVersion(manifest);
const sourceAhead = manifest.version !== version;

// ── Assert the linked files exist and can be deployed ────────────────────────

const errors = [];
const warnings = [];
const shipped = [];

for (const ext of FORMATS) {
  const name = assetName(version, ext);
  const abs = join(ROOT, DOWNLOADS, name);
  const href = `/downloads/${name}`;

  if (!existsSync(abs)) {
    errors.push({
      what: `${DOWNLOADS}/${name} does not exist`,
      why: `/exclusive-friends-only and /book both link ${href}, derived from ${BOOK_JSON} released ${version}. That link will 404.`,
      // Not a cp line to retype. Retyping a version into a shell is the manual
      // step that produced the 404 documented at the top of this file.
      fix: `npm run book:publish`
    });
    continue;
  }

  const bytes = statSync(abs).size;
  shipped.push({ name, bytes });

  if (bytes > PAGES_MAX_BYTES) {
    errors.push({
      what: `${DOWNLOADS}/${name} is ${mib(bytes)} MiB, over the ${mib(PAGES_MAX_BYTES)} MiB Cloudflare Pages asset limit`,
      why: 'The build would pass and the DEPLOY would fail. Pages rejects the asset, and the download 404s in production.',
      fix: 'Move the book to an R2 public bucket on a subdomain (R2 has no egress charges), and point the href at it.'
    });
  } else if (bytes > PAGES_MAX_BYTES * WARN_AT_FRACTION) {
    warnings.push(
      `${name} is ${mib(bytes)} MiB, ${mib(PAGES_MAX_BYTES - bytes)} MiB under the ${mib(PAGES_MAX_BYTES)} MiB Pages ceiling. ` +
        'Plan the R2 move before the next illustrated version.'
    );
  }
}

if (errors.length) {
  console.error(`\ncheck-book-downloads: ${errors.length} problem(s). book.json releases v${version}` +
    (sourceAhead ? ` (source at v${manifest.version})` : '') + `.\n`);
  for (const e of errors) {
    console.error(`  ${e.what}`);
    console.error(`    why: ${e.why}`);
    console.error(`    fix: ${e.fix}\n`);
  }
  console.error(`See the header of ${relative(ROOT, fileURLToPath(import.meta.url))} for why this is enforced.\n`);
  process.exit(1);
}

// ── Generate the redirects, so no version is ever typed by hand ───────────────

const lines = [
  '# GENERATED by scripts/check-book-downloads.mjs at prebuild. Do not edit.',
  '# Every target is derived from the "released" version in',
  '# src/lib/data/book/book.json, so links cannot drift from the files that ship.',
  '',
  '# Stable aliases. These paths never change, so a link shared today keeps',
  '# working after the next version bump. Prefer them when sending the book.'
];

for (const ext of FORMATS) {
  lines.push(`/downloads/Surviving-the-Singularity.${ext}  /downloads/${assetName(version, ext)}  302`);
}

lines.push('', '# Retired versions land on the current file instead of 404ing.');

for (const old of RETIRED_VERSIONS) {
  if (old === version) continue;
  for (const ext of FORMATS) {
    lines.push(`/downloads/${assetName(old, ext)}  /downloads/${assetName(version, ext)}  302`);
  }
}

lines.push('');
writeFileSync(join(ROOT, REDIRECTS), lines.join('\n'), 'utf8');

// ── Report ───────────────────────────────────────────────────────────────────

for (const w of warnings) console.warn(`check-book-downloads: WARNING - ${w}`);

if (sourceAhead) {
  console.log(
    `check-book-downloads: open cycle. Source is at v${manifest.version}; readers ` +
      `ship v${version} until the next \`npm run book:release\` stamps a new release.`
  );
}

console.log(
  `check-book-downloads: clean. v${version} shipping ` +
    shipped.map((s) => `${s.name.split('.').pop().toUpperCase()} ${mib(s.bytes)} MiB`).join(', ') +
    `; ${REDIRECTS} regenerated.`
);
process.exit(0);
