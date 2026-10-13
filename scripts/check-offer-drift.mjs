#!/usr/bin/env node
/**
 * OFFER DRIFT ASSERTION  (plan item A-08)
 *
 * Fails the build if offer FACTS are typed into a sales surface instead of
 * derived from src/lib/offer.js.
 *
 * WHY THIS EXISTS
 *
 * On 2026-07-29 the offer was consolidated into one module and nine surfaces
 * were pointed at it. That pass moved the offer SENTENCE. It did not move the
 * offer NUMBERS, and nobody noticed, because prose review does not catch a
 * numeral. A grep afterwards found the price still hand-typed in six places,
 * including both homepage buy buttons, the page's own meta description, and the
 * confirmation email a paying customer receives.
 *
 * The homepage was the sharpest case. Line 4 of src/routes/+page.svelte said
 * "No offer prose is typed into this file", one line 354 correctly rendered
 * {offer.price}, and five other lines in the same file hardcoded it anyway. A
 * comment is not an assertion. This file is the assertion.
 *
 * THE DESIGN DECISION THAT MATTERS
 *
 * Every pattern below is DERIVED FROM THE MODULE at lint time, never hardcoded
 * here. The price rule is built from `offer.price`, so changing the price to $7
 * retargets this lint at "$7" automatically. A lint with "$5" baked into it
 * would go quietly blind on exactly the commit where it was needed most, which
 * is the same failure shape as the checks in section 9 of the verification
 * ledger: a passing state indistinguishable from a dead one.
 *
 * WHAT IS IN SCOPE, AND WHY THE BOUNDARY IS THERE
 *
 * Sales surfaces only: routes, components, and the transactional email. Book
 * and blueprint prose in src/lib/data/ is editorial content that legitimately
 * discusses dollar figures ($100,000 robot arms, $500/month pilot programs) and
 * is not making an offer, so it is out of scope.
 *
 * The rule is FACTS, not phrasing. A number or a percentage is a claim that can
 * be checked against the product and can therefore be WRONG, so it must derive.
 * Legal pages are still free to paraphrase the offer in their own register,
 * which is why /terms restating the Print Edition carve-out in its own words
 * does not trip anything here.
 *
 * USAGE
 *
 *   node scripts/check-offer-drift.mjs          # exits 1 on any violation
 *   node scripts/check-offer-drift.mjs --list   # print scope and rules, exit 0
 *
 * Wired into `prebuild`, ahead of the image hook, so `npm run build` fails fast.
 */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join, relative } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OFFER_MODULE = 'src/lib/offer.js';

const { offer } = await import(pathToFileURL(join(ROOT, OFFER_MODULE)).href);

/**
 * Directories walked for .svelte and .js, plus individual files.
 *
 * src/lib/server/email.js is named explicitly rather than walking src/lib,
 * because src/lib also holds data/, archive/ and utils/, none of which are
 * sales surfaces. Naming the one file that is keeps the boundary deliberate: a
 * new sales surface has to be added here on purpose.
 */
const SCOPE_DIRS = ['src/routes', 'src/lib/components'];
const SCOPE_FILES = ['src/lib/server/email.js'];
const EXTENSIONS = ['.svelte', '.js'];

/**
 * Escapes a string for literal use inside a RegExp.
 */
function escapeRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * The price as a regex that matches the offer price and nothing longer.
 *
 * "$5" must match in "Preorder for $5" and in "for $5." at the end of a
 * sentence, but must NOT match inside "$500", "$5,000" or "$5.00". So: reject a
 * following digit, and reject a following separator that is itself followed by a
 * digit. Verified against the real homepage, which legitimately prints
 * $100,000, $1,000 and $432,500 in its argument copy.
 */
const priceRe = new RegExp(`${escapeRe(offer.price)}(?!\\d|[.,]\\d)`);

/**
 * The discount percentage rule requires the word "off".
 *
 * A bare percentage cannot be used: every unqualified "50%" in the component
 * tree is CSS (border-radius: 50%, translate(-50%, -50%), and a 50% keyframe
 * stop). Measured, not assumed. Requiring "off" is what makes this rule about
 * the offer rather than about stylesheets.
 */
const discountRe = /\b\d{1,3}\s*%\s*off\b/i;

/**
 * A COUNT RULE MUST NOT BE ABLE TO BUILD ITSELF OUT OF NOTHING.
 *
 * The rule below used to read `offer.precedentCount`. When that field was split
 * into two correctly-named ones, this line would have produced
 * `new RegExp('\\bundefined\\s+(documented|...)')`, which matches nothing, and
 * the lint would have printed "clean" while enforcing a dead rule.
 *
 * That is the exact failure this file's own header calls out: "a passing state
 * indistinguishable from a dead one". Exit 2 instead. A lint that cannot build
 * its rule has to fail loudly, not quietly succeed.
 */
function requireCount(name, value) {
  if (!Number.isInteger(value) || value <= 0) {
    console.error(
      `check-offer-drift: offer.${name} is ${JSON.stringify(value)}, ` +
        'so no rule can be built from it. Refusing to report a pass with a dead rule.'
    );
    process.exit(2);
  }
  return value;
}

/**
 * A count followed by the nouns it is ever counted in.
 *
 * Two rules, not one, because there are two counts describing two different
 * artifacts: the book's 23-precedent ledger, and the bonus file's measured case
 * count. Conflating them is the bug that put a wrong number on four live
 * surfaces including the confirmation email, so each gets its own guard and its
 * own fix hint naming the right field.
 */
function countRe(value) {
  return new RegExp(`\\b${value}\\s+(documented|cases?|precedents?|entries)\\b`, 'i');
}

/**
 * Shipment language, live only while the SKU ships nothing.
 *
 * Tied to the flag rather than stated flatly, so that if a future physical SKU
 * legitimately flips offer.shipsPhysicalGoods to true, this rule retires itself
 * instead of blocking the build with a stale objection.
 */
const shipmentRe = /prior to shipment|Merchandise Rule/i;

const RULES = [
  {
    id: 'price',
    active: true,
    re: priceRe,
    what: `the offer price ${offer.price} typed by hand`,
    fix: `render {offer.price} from $lib/offer instead`
  },
  {
    id: 'price-words',
    active: Boolean(offer.priceWords),
    re: new RegExp(`\\b${escapeRe(offer.priceWords ?? '')}\\b`, 'i'),
    what: `the price spelled out as "${offer.priceWords}"`,
    fix: 'render {offer.priceWords} from $lib/offer instead'
  },
  {
    id: 'discount',
    active: true,
    re: discountRe,
    what: 'a discount percentage typed by hand',
    fix: "use offerItemLabel('print-discount') from $lib/offer instead"
  },
  {
    id: 'ledger-precedent-count',
    active: true,
    re: countRe(requireCount('ledgerPrecedentCount', offer.ledgerPrecedentCount)),
    what: `the book's ledger count ${offer.ledgerPrecedentCount} typed by hand`,
    fix: 'render {offer.ledgerPrecedentCount} from $lib/offer instead'
  },
  {
    id: 'precedent-file-case-count',
    active: true,
    re: countRe(requireCount('precedentFileCaseCount', offer.precedentFileCaseCount)),
    what: `the Precedent File case count ${offer.precedentFileCaseCount} typed by hand`,
    fix: 'render {offer.precedentFileCaseCount} from $lib/offer instead'
  },
  {
    id: 'shipment',
    active: offer.shipsPhysicalGoods === false,
    re: shipmentRe,
    what: 'shipment or FTC merchandise language on a SKU that ships nothing',
    fix: 'derive the refund paragraph from refundClause() in $lib/offer'
  }
].filter((rule) => rule.active);

/**
 * Comment text is exempt.
 *
 * A comment cannot mislead a customer, and the history of WHY the offer changed
 * is worth keeping written down next to the code it explains. email.js carries a
 * note recording that the discount used to be 50% off the finished book; that
 * note is the opposite of drift and should not have to be deleted to satisfy a
 * lint.
 *
 * THIS WAS A LINT BUG, CAUGHT BY TESTING THE LINT. The first version of this
 * file checked whether a line STARTED with a comment marker. That passed the
 * obvious cases and then false-positived on early-access/+page.svelte:293, a
 * continuation line inside a multi-line HTML comment which begins with the word
 * "Saying" and is not a comment marker at all. A per-line test cannot see a
 * comment that opened on a previous line, so the state has to be carried.
 *
 * `stripBlockComments` removes <!-- ... --> and slash-star regions while
 * carrying state across lines. Note what it does NOT do: strip from `//` to end
 * of line anywhere it appears. Doing that would eat the remainder of every line
 * holding an "https://" URL, and this codebase has offer copy sitting on the
 * same line as links. Line comments are handled by the narrower start-of-line
 * test instead, so a trailing comment after real code still trips the rules.
 * That direction of error is the safe one.
 */
function stripBlockComments(line, state) {
  let out = '';
  let i = 0;

  while (i < line.length) {
    if (state.inHtml) {
      const end = line.indexOf('-->', i);
      if (end === -1) return out;
      state.inHtml = false;
      i = end + 3;
      continue;
    }
    if (state.inJs) {
      const end = line.indexOf('*/', i);
      if (end === -1) return out;
      state.inJs = false;
      i = end + 2;
      continue;
    }

    const html = line.indexOf('<!--', i);
    const js = line.indexOf('/*', i);

    let next = -1;
    let kind = null;
    if (html !== -1 && (js === -1 || html < js)) {
      next = html;
      kind = 'html';
    } else if (js !== -1) {
      next = js;
      kind = 'js';
    }

    if (next === -1) return out + line.slice(i);

    out += line.slice(i, next);
    if (kind === 'html') {
      state.inHtml = true;
      i = next + 4;
    } else {
      state.inJs = true;
      i = next + 2;
    }
  }

  return out;
}

function isLineComment(line) {
  const t = line.trim();
  return t.startsWith('//') || t.startsWith('*');
}

/**
 * Explicit, justified exemptions. Empty on purpose.
 *
 * Anything added here needs a comment saying why the surface cannot derive from
 * the module. "It was easier" is not a reason; a growing allowlist means this
 * lint is being managed rather than obeyed.
 */
const ALLOW = [
  // { file: 'src/routes/example/+page.svelte', line: 42, rule: 'price', why: '...' }
];

function isAllowed(file, line, ruleId) {
  return ALLOW.some(
    (a) => a.file === file && a.line === line && a.rule === ruleId
  );
}

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (entry === 'node_modules' || entry.startsWith('.')) continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) walk(full, out);
    else if (EXTENSIONS.some((e) => entry.endsWith(e))) out.push(full);
  }
  return out;
}

function collectFiles() {
  const files = [];
  for (const dir of SCOPE_DIRS) {
    try {
      walk(join(ROOT, dir), files);
    } catch {
      // A scoped directory that does not exist is a scope bug, not a pass.
      console.error(`check-offer-drift: scope directory missing: ${dir}`);
      process.exit(2);
    }
  }
  for (const f of SCOPE_FILES) files.push(join(ROOT, f));
  return files
    .map((f) => relative(ROOT, f))
    .filter((f) => f !== OFFER_MODULE)
    .sort();
}

const files = collectFiles();

if (process.argv.includes('--list')) {
  console.log(`scope: ${files.length} files`);
  for (const r of RULES) console.log(`rule ${r.id.padEnd(15)} ${r.re}`);
  process.exit(0);
}

/**
 * A lint that reports zero violations because it read zero files is the exact
 * false-pass shape this project has already been bitten by twice. Refuse to
 * pass on an empty or implausibly small scope rather than report a clean run.
 */
if (files.length < 20) {
  console.error(
    `check-offer-drift: scope collapsed to ${files.length} files, expected 20+. ` +
      'Refusing to report a pass on a scope this small.'
  );
  process.exit(2);
}

const violations = [];

for (const file of files) {
  let text;
  try {
    text = readFileSync(join(ROOT, file), 'utf8');
  } catch {
    continue;
  }
  const lines = text.split('\n');
  const commentState = { inHtml: false, inJs: false };

  lines.forEach((line, i) => {
    // Always advance the block-comment state, even for lines we skip, or a
    // comment that opens on a skipped line never gets seen as opening.
    const code = stripBlockComments(line, commentState);
    if (isLineComment(line)) return;

    for (const rule of RULES) {
      const m = rule.re.exec(code);
      if (!m) continue;
      if (isAllowed(file, i + 1, rule.id)) continue;
      violations.push({
        file,
        line: i + 1,
        rule: rule.id,
        what: rule.what,
        fix: rule.fix,
        excerpt: line.trim().slice(0, 110)
      });
    }
  });
}

if (violations.length === 0) {
  console.log(
    `check-offer-drift: clean. ${files.length} sales surfaces scanned, ` +
      `${RULES.length} rules derived from ${OFFER_MODULE}.`
  );
  process.exit(0);
}

console.error(
  `\ncheck-offer-drift: ${violations.length} violation(s). ` +
    `Offer facts must come from ${OFFER_MODULE}, not from page prose.\n`
);

for (const v of violations) {
  console.error(`  ${v.file}:${v.line}  [${v.rule}]`);
  console.error(`    found: ${v.what}`);
  console.error(`    ${v.excerpt}`);
  console.error(`    fix:   ${v.fix}\n`);
}

console.error(
  `${violations.length} violation(s). See the header of ${OFFER_MODULE} for why ` +
    'this is enforced.\n'
);
process.exit(1);
