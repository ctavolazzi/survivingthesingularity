#!/usr/bin/env node
/**
 * PROBE THE CONFIRMATION EMAIL
 *
 * sendDownloadEmail is the ONE email every paying customer receives, and it is
 * the hardest thing in this codebase to look at: it lives behind Resend, behind
 * a Stripe webhook, behind a paid checkout. So it historically got changed by
 * reading it, which is how it ended up promising "research PDFs, papers, images
 * and source documents" over an archive of four text files, how it described a
 * 31-case file as having 23, and how it shipped with no CAN-SPAM postal address
 * at all while the helper that renders one sat unused in the same file.
 *
 * This renders the real function, with the real offer object and the real
 * bundle manifest, and asserts on the HTML that comes out. Resend is stubbed at
 * the module boundary so nothing is sent and no API key is needed.
 *
 *   node scripts/probe-download-email.mjs
 *   node scripts/probe-download-email.mjs --write   # also dump the HTML to view
 *
 * EVERY ASSERTION HERE HAS A NEGATIVE CONTROL. A check that has never been
 * watched failing is not evidence, and this repo has already paid for that
 * lesson twice: a webhook that answered 400 to everything read as "configured",
 * and a lint whose rule silently became `undefined` reported clean.
 *
 * THE ONE THAT MATTERS MOST is the promotion-code case. Checkout runs with
 * allow_promotion_codes, so the charged amount and the advertised price
 * legitimately differ. A receipt built from offer.priceCents would state the
 * list price to someone who paid half of it, which is a false financial record
 * that no page-level drift lint would ever catch. So the probe pays 250 cents
 * against a 500 cent offer and asserts the receipt says the former and never
 * the latter.
 */
import * as esbuild from 'esbuild';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const WRITE = process.argv.includes('--write');

let failures = 0;
let checks = 0;
function ok(label, cond, detail = '') {
  checks++;
  if (cond) {
    console.log(`  PASS  ${label}`);
  } else {
    failures++;
    console.log(`  FAIL  ${label}${detail ? `\n          ${detail}` : ''}`);
  }
}

/**
 * Stub the three module boundaries that need a running platform, and let
 * everything else resolve to the real source. offer.js, bookAccessCode.js and
 * bundleManifest.js are deliberately NOT stubbed: the whole point is to assert
 * against the real numbers those files carry.
 */
function stubPlugin(envValues) {
  return {
    name: 'probe-stubs',
    setup(build) {
      build.onResolve({ filter: /^\$env\// }, () => ({ path: 'probe-env', namespace: 'stub' }));
      build.onResolve({ filter: /^resend$/ }, () => ({ path: 'probe-resend', namespace: 'stub' }));
      build.onResolve({ filter: /supabaseAdmin\.js$/ }, () => ({ path: 'probe-supabase', namespace: 'stub' }));
      build.onResolve({ filter: /^\$lib\// }, (a) => ({ path: join(ROOT, 'src', 'lib', a.path.slice('$lib/'.length)) }));
      build.onLoad({ filter: /.*/, namespace: 'stub' }, (a) => {
        if (a.path === 'probe-env') {
          return { contents: `export const env = ${JSON.stringify(envValues)};`, loader: 'js' };
        }
        if (a.path === 'probe-resend') {
          return {
            contents: `export class Resend {
              constructor() {
                this.emails = { send: async (payload) => {
                  globalThis.__PROBE_SENT__.push(payload);
                  return { data: { id: 'probe_msg' }, error: null };
                } };
              }
            }`,
            loader: 'js',
          };
        }
        return { contents: 'export const supabaseAdmin = null;', loader: 'js' };
      });
    },
  };
}

/**
 * Bundle and import email.js fresh for a given env. Fresh because
 * `postalAddress` is captured at module load, so the configured and unconfigured
 * footer states are only separable across two separate module instances.
 */
async function loadEmailModule(envValues, tag) {
  const out = await esbuild.build({
    entryPoints: [join(ROOT, 'src', 'lib', 'server', 'email.js')],
    bundle: true,
    format: 'esm',
    platform: 'node',
    write: false,
    logLevel: 'silent',
    plugins: [stubPlugin(envValues)],
  });
  const dir = mkdtempSync(join(tmpdir(), 'sts-email-probe-'));
  const file = join(dir, `email-${tag}.mjs`);
  writeFileSync(file, out.outputFiles[0].text);
  return import(pathToFileURL(file).href);
}

const BASE_ENV = {
  RESEND_API_KEY: 'probe_key',
  EMAIL_FROM: 'Surviving the Singularity <hello@survivingthesingularity.com>',
  MASTER_DISCOUNT_CODE: 'PREORDER50',
};

async function render(mod, args) {
  globalThis.__PROBE_SENT__ = [];
  await mod.sendDownloadEmail(args);
  if (globalThis.__PROBE_SENT__.length !== 1) {
    throw new Error(`expected exactly 1 send, got ${globalThis.__PROBE_SENT__.length}`);
  }
  return globalThis.__PROBE_SENT__[0];
}

const SESSION = 'cs_test_a1ProbeSessionIdentifierThatIsRealisticallyLong0123456789';

const [manifest, offerMod] = await Promise.all([
  import(pathToFileURL(join(ROOT, 'src/lib/data/bundleManifest.js')).href),
  import(pathToFileURL(join(ROOT, 'src/lib/offer.js')).href),
]);
const bundle = manifest.default;
const offer = offerMod.offer;

console.log('\nprobe-download-email');
console.log(`  manifest: ${bundle.bundle.entries} entries, ${bundle.bundle.bytes.toLocaleString()} bytes`);
console.log(`  offer:    priceCents=${offer.priceCents}\n`);

// ── 1. THE PAID CASE, WITH A PROMOTION CODE APPLIED ────────────────────────
console.log('1. receipt reflects what was CHARGED, not what is advertised');
const paidMod = await loadEmailModule({ ...BASE_ENV, EMAIL_POSTAL_ADDRESS: 'Johnny Autoseed LLC, PO Box 1234, Chico, CA 95926' }, 'paid');
const paid = await render(paidMod, {
  to: 'buyer@example.com',
  sessionId: SESSION,
  edition_type: 'standard',
  copy_number: null,
  discount_code: 'ABC123',
  // Half the list price: exactly the allow_promotion_codes case.
  amountTotal: 250,
  currency: 'usd',
  paymentIntent: 'pi_3ProbePaymentIntent0001',
  orderedAt: 1785000000,
});
const html = paid.html;

ok('charged amount $2.50 appears', html.includes('$2.50'));
ok(
  'advertised price is NOT stated as the amount paid',
  !/Amount paid[\s\S]{0,200}\$5\.00/.test(html),
  'a receipt built from offer.priceCents would say $5.00 here'
);
ok('payment reference appears', html.includes('pi_3ProbePaymentIntent0001'));
ok('full order reference appears', html.includes(SESSION));
ok('order date is rendered in UTC', /2026[\s\S]{0,40}UTC/.test(html));
ok('receipt block is labelled', /Order receipt/i.test(html));

// ── 2. THE ITEMISED FILE TABLE ─────────────────────────────────────────────
console.log('\n2. the file table is a measurement of the archive');
const missing = bundle.files.filter((f) => !html.includes(f.label));
ok(`all ${bundle.files.length} manifest labels are itemised`, missing.length === 0,
  missing.length ? `missing: ${missing.map((f) => f.label).join(', ')}` : '');
ok('entry count is rendered from the manifest', html.includes(String(bundle.bundle.entries)));
const conv = bundle.files.filter((f) => f.role === 'convenience-copy');
ok(`all ${conv.length} convenience copies are tagged free`,
  conv.every((f) => {
    const i = html.indexOf(f.label);
    return i !== -1 && html.slice(i, i + 400).includes('free at');
  }),
  'the book files must not read as something the five dollars unlocked');
ok('primary files are NOT tagged free',
  bundle.files.filter((f) => f.role === 'primary').every((f) => {
    const i = html.indexOf(f.label);
    return i !== -1 && !html.slice(i, i + 200).includes('free at');
  }));

// ── 3. THE CAN-SPAM POSTAL FOOTER ──────────────────────────────────────────
console.log('\n3. postal address, the gap that made this probe worth writing');
ok('postal address renders when configured', html.includes('PO Box 1234'));

const noPostalMod = await loadEmailModule({ ...BASE_ENV }, 'nopostal');
const noPostal = await render(noPostalMod, {
  to: 'buyer@example.com', sessionId: SESSION, edition_type: 'standard',
  copy_number: null, discount_code: null,
  amountTotal: 500, currency: 'usd', paymentIntent: 'pi_x', orderedAt: 1785000000,
});
ok('NEGATIVE CONTROL: no address is invented when unset',
  !noPostal.html.includes('PO Box') && !/\b\d{5}(-\d{4})?\b/.test(noPostal.html.split('You received this because')[1] ?? ''),
  'an invented placeholder reads as compliance while being false');
ok('the receiving reason is still stated when unset',
  noPostal.html.includes('You received this because'));

// ── 4. MISSING FACTS ARE OMITTED, NEVER GUESSED ────────────────────────────
console.log('\n4. an absent fact produces an absent row, not a plausible one');
const bareMod = await loadEmailModule({ ...BASE_ENV }, 'bare');
const bare = await render(bareMod, {
  to: 'buyer@example.com', sessionId: SESSION, edition_type: 'standard',
  copy_number: null, discount_code: null,
  // Everything Stripe would normally supply is absent: a manual replay.
  amountTotal: null, currency: null, paymentIntent: null, orderedAt: null,
});
ok('no Amount paid row when Stripe gave no amount', !/Amount paid/.test(bare.html));
ok('no Payment reference row when there is no intent', !/Payment reference/.test(bare.html));
ok('no Order date row when there is no timestamp', !/Order date/.test(bare.html));
ok('the order reference still renders', bare.html.includes(SESSION));
ok('NEGATIVE CONTROL: the paid render DID have those rows',
  /Amount paid/.test(html) && /Payment reference/.test(html) && /Order date/.test(html),
  'if this fails the absence checks above prove nothing');

// ── 5. HOUSE RULES AND ESCAPING ────────────────────────────────────────────
console.log('\n5. house rules and injection');
ok('no em dashes anywhere in the rendered email', !html.includes('—'));
const evilMod = await loadEmailModule({ ...BASE_ENV }, 'evil');
const evil = await render(evilMod, {
  to: 'buyer@example.com',
  sessionId: 'cs_test_<script>alert(1)</script>',
  edition_type: 'standard', copy_number: null,
  discount_code: '<img src=x onerror=alert(2)>',
  amountTotal: 500, currency: 'usd',
  paymentIntent: 'pi_"onmouseover="alert(3)', orderedAt: 1785000000,
});
ok('session id is escaped in the receipt', !evil.html.includes('<script>alert(1)</script>'));
ok('discount code is escaped', !evil.html.includes('<img src=x onerror'));
ok('payment reference is escaped', !evil.html.includes('pi_"onmouseover="'));

// ── 6. ZERO-DECIMAL CURRENCY ───────────────────────────────────────────────
console.log('\n6. zero-decimal currency is not divided by 100');
const jpyMod = await loadEmailModule({ ...BASE_ENV }, 'jpy');
const jpy = await render(jpyMod, {
  to: 'buyer@example.com', sessionId: SESSION, edition_type: 'standard',
  copy_number: null, discount_code: null,
  amountTotal: 500, currency: 'jpy', paymentIntent: 'pi_y', orderedAt: 1785000000,
});
ok('500 JPY renders as 500, not 5', /¥500|JPY\s*500|500\s*JPY/.test(jpy.html),
  'dividing by 100 would print a 500 yen charge as 5 yen');

if (WRITE) {
  // A temp dir, deliberately: this worktree is shared with other sessions and
  // a probe should not drop artifacts into anyone's tree, or into git status.
  const out = join(mkdtempSync(join(tmpdir(), 'sts-email-html-')), 'download-email.html');
  writeFileSync(out, html);
  console.log(`\n  wrote ${out}\n  open it with:  open "${out}"`);
}

console.log(`\n${failures ? 'FAILED' : 'OK'}: ${checks - failures}/${checks} checks passed.\n`);
process.exit(failures ? 1 : 0);
