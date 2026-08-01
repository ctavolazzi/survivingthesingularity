#!/usr/bin/env node
/**
 * CROSS-RUNTIME RESOLVER PARITY
 *
 * Fails the build if the Python resolver and the JavaScript resolver disagree
 * about what a cross-reference says.
 *
 * WHY TWO RESOLVERS EXIST AT ALL
 *
 * `[](sts:chapter1)` renders as "Chapter 1", generated from book.json, so that
 * renumbering a chapter rewrites every sentence pointing at it instead of
 * leaving prose that is quietly wrong. Something has to turn a pointer into
 * words, and there are two places that must do it:
 *
 *   - scripts/sts.py, for `compile`, `refs render` and the EPUB/PDF builds
 *   - src/lib/bookManifest.js, for the website
 *
 * The site cannot call Python at build time. The obvious dodge - have Python
 * emit a generated JSON that the site imports - trades two implementations for
 * one implementation plus one artifact that can go stale, which is the exact
 * class of bug the whole single-source effort exists to remove. So two
 * implementations is the honest floor.
 *
 * What is NOT acceptable is two implementations that nobody compares. This
 * script is the comparison: it asks sts.py for every label it generates, runs
 * the JavaScript rules over the same manifest, and diffs them.
 *
 * THE ASYMMETRY IS DELIBERATE, AND CHECKED IN ONE DIRECTION ONLY
 *
 * sts.py resolves against the manuscript index, so it sees SECTIONS and
 * BLOCKS, and can reject `sts.chapter1.b0003` when block b0003 no longer
 * exists. bookManifest.js only ever sees book.json, so it resolves that
 * pointer to its section. That makes Python strictly stronger, which is fine:
 * the EPUB build raises and the release stops before a reader sees anything.
 *
 * So the directions are not symmetric:
 *   - both resolve, labels differ   -> FAIL. A real disagreement.
 *   - Python resolves, JS does not  -> FAIL. The site would silently drop a
 *                                      marker the book build accepted.
 *   - JS resolves, Python does not  -> NOTE. Python is being stricter, by
 *                                      design, and its build already fails.
 */

import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import { shortLabel, labelFor } from '../src/lib/bookManifest.js';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const BOOK_JSON = 'src/lib/data/book/book.json';

// ── Ask each side ────────────────────────────────────────────────────────────

let manifest;
try {
  manifest = JSON.parse(readFileSync(join(ROOT, BOOK_JSON), 'utf8'));
} catch (err) {
  console.error(`\ncheck-resolver-parity: cannot read ${BOOK_JSON}: ${err.message}\n`);
  process.exit(1);
}

let python;
try {
  python = JSON.parse(
    execFileSync('python3', [join(ROOT, 'scripts/sts.py'), 'refs', 'labels'], {
      cwd: ROOT,
      encoding: 'utf8',
      maxBuffer: 32 * 1024 * 1024
    })
  );
} catch (err) {
  console.error(`\ncheck-resolver-parity: \`sts.py refs labels\` failed.\n`);
  console.error(`  ${err.stderr?.toString().trim() || err.message}\n`);
  console.error('  The Python resolver is the canonical one. If it cannot run,');
  console.error('  this check cannot certify the website agrees with it.\n');
  process.exit(1);
}

// ── Compare ──────────────────────────────────────────────────────────────────

const failures = [];
const notes = [];

// 1. The shared half: every section title must shorten identically.
for (const s of python.sections) {
  const js = shortLabel(s.title);
  if (js !== s.label) {
    failures.push({
      what: `section "${s.id}" shortens differently`,
      py: s.label,
      js,
      why: 'sts.py generates the label the EPUB and PDF ship; bookManifest.js generates the one the website renders. Same pointer, two different words.'
    });
  }
}

// 2. Every pointer the manuscript actually contains.
for (const [target, pyLabel] of Object.entries(python.targets)) {
  const jsLabel = labelFor(manifest, target);

  if (pyLabel !== null && jsLabel !== null && pyLabel !== jsLabel) {
    failures.push({
      what: `sts:${target} resolves to different text`,
      py: pyLabel,
      js: jsLabel,
      why: 'A reader of the book and a reader of the site would see two different cross-references pointing at the same place.'
    });
  } else if (pyLabel !== null && jsLabel === null) {
    failures.push({
      what: `sts:${target} resolves in sts.py but not on the website`,
      py: pyLabel,
      js: '(dropped)',
      why: 'bookManifest.js drops a marker it cannot resolve rather than render "](sts:" at a reader. The book would print the reference and the site would print nothing.'
    });
  } else if (pyLabel === null && jsLabel !== null) {
    notes.push(
      `sts:${target} -> website says "${jsLabel}", sts.py rejects it. ` +
        'Expected: sts.py checks block ids against the manuscript index and is deliberately stricter. The EPUB build fails on this before it can ship.'
    );
  }
}

// ── Report ───────────────────────────────────────────────────────────────────

for (const n of notes) console.warn(`check-resolver-parity: NOTE - ${n}`);

if (failures.length) {
  console.error(
    `\ncheck-resolver-parity: ${failures.length} disagreement(s) between ` +
      `scripts/sts.py and src/lib/bookManifest.js.\n`
  );
  for (const f of failures) {
    console.error(`  ${f.what}`);
    console.error(`    sts.py:          ${f.py}`);
    console.error(`    bookManifest.js: ${f.js}`);
    console.error(`    why: ${f.why}\n`);
  }
  console.error('  Fix: change both rule sets together. They are two implementations');
  console.error('  of one rule because the site cannot call Python at build time;');
  console.error('  this check is what stops that from meaning two behaviours.\n');
  process.exit(1);
}

console.log(
  `check-resolver-parity: clean. ${python.sections.length} sections and ` +
    `${Object.keys(python.targets).length} pointer(s) resolve identically in ` +
    `sts.py and bookManifest.js (book v${python.version}).`
);
process.exit(0);
