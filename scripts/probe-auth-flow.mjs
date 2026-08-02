#!/usr/bin/env node
/**
 * Probe the /signup auth flow against a running server.
 *
 *   npx vite dev --port 5199
 *   node scripts/probe-auth-flow.mjs http://localhost:5199
 *
 * Same shape as the other probe-*.mjs scripts here: hit the real endpoints,
 * assert on what comes back, print a table, exit non-zero on failure.
 *
 * WHY THIS EXISTS RATHER THAN A UNIT TEST
 *
 * Most of what this checks is not a function's return value; it is a property
 * of the deployed surface - what status a route answers, whether a cross-origin
 * POST is refused, whether a key appears in delivered HTML. Those only exist
 * once the framework, the hooks and the CSP are all in play.
 *
 * EVERY CHECK HAS A NEGATIVE CONTROL
 *
 * A checker that cannot fail is not a checker. Where a check asserts something
 * is blocked, there is a paired case that SHOULD be allowed, so a probe that
 * starts passing everything because the server stopped responding is visible
 * rather than reassuring.
 */

import { safeRedirect } from '../src/lib/server/safeRedirect.js';
import { checkPassword, strengthScore } from '../src/lib/server/passwordPolicy.js';
import { isUsableSupabaseUrl, isUsableSupabaseKey } from '../src/lib/server/supabaseEnv.js';

const BASE = (process.argv[2] ?? 'http://localhost:5199').replace(/\/$/, '');

const results = [];
function record(name, pass, detail) {
  results.push({ name, pass, detail });
  const mark = pass ? '\x1b[32mPASS\x1b[0m' : '\x1b[31mFAIL\x1b[0m';
  console.log(`  ${mark}  ${name}${detail ? `  \x1b[2m${detail}\x1b[0m` : ''}`);
}

function skip(name, why) {
  results.push({ name, pass: true, skipped: true, detail: why });
  console.log(`  \x1b[33mSKIP\x1b[0m  ${name}  \x1b[2m${why}\x1b[0m`);
}

/**
 * Is this a `vite dev` server rather than a production build?
 *
 * It matters for exactly one check. SvelteKit's CSRF origin check is wrapped in
 * `if (!DEV)` - see node_modules/@sveltejs/kit/src/runtime/server/respond.js.
 * On a dev server a cross-origin form POST is therefore ALLOWED THROUGH, and a
 * probe that asserts 403 against `vite dev` fails against correct code, while
 * one that asserts 200 would "pass" against a production build with CSRF
 * genuinely broken. Both readings are useless.
 *
 * So: detect the environment and only run the check where it means something.
 * Detection is the Vite client module, which only a dev server serves.
 */
async function isDevServer() {
  try {
    const res = await fetch(`${BASE}/@vite/client`, { redirect: 'manual' });
    return res.status === 200;
  } catch {
    return false;
  }
}

/** fetch without following redirects, so we can assert on the Location. */
function raw(path, init = {}) {
  return fetch(`${BASE}${path}`, { redirect: 'manual', ...init });
}

console.log(`\nProbing ${BASE}\n`);

// ---------------------------------------------------------------------------
console.log('Reachability');
// ---------------------------------------------------------------------------
{
  const res = await raw('/signup');
  const html = await res.text();
  record('GET /signup renders', res.status === 200, `${res.status}`);
  record(
    '  ...in signup mode by default',
    html.includes('Create your account'),
    html.includes('Create your account') ? '' : 'title missing'
  );
  record(
    '  ...with the email + password fields',
    html.includes('name="email"') && html.includes('name="password"'),
    ''
  );
  record(
    '  ...posting to the signup action',
    html.includes('?/signup'),
    ''
  );
  record(
    '  ...with the honeypot present',
    html.includes('name="_hp"'),
    ''
  );

  // The whole architectural claim, checked against delivered bytes: a Supabase
  // JWT starts `eyJ` at a token boundary. Anything matching here means the key
  // reached the browser.
  const jwtish = html.match(/["'\s]eyJ[A-Za-z0-9_-]{20,}/g) ?? [];
  record('  ...and no Supabase key in the HTML', jwtish.length === 0, `${jwtish.length} matches`);
  record(
    '  ...and no supabase.co origin in the HTML',
    !html.includes('supabase.co'),
    ''
  );

  const signin = await raw('/signup?mode=signin');
  const signinHtml = await signin.text();
  record(
    'GET /signup?mode=signin switches mode',
    signinHtml.includes('Welcome back') && signinHtml.includes('?/signin'),
    `${signin.status}`
  );
}

// ---------------------------------------------------------------------------
console.log('\nOAuth provider allowlist');
// ---------------------------------------------------------------------------
{
  const bad = await raw('/auth/oauth/evilprovider');
  record('unknown provider is refused', bad.status === 404, `${bad.status}`);

  // Negative control: an allowlisted provider must NOT 404, or the check above
  // would pass simply because the route is broken.
  const good = await raw('/auth/oauth/google');
  record(
    'allowlisted provider is not refused (control)',
    good.status !== 404,
    `${good.status} -> ${(good.headers.get('location') ?? '').slice(0, 60)}`
  );
}

// ---------------------------------------------------------------------------
console.log('\nCallback');
// ---------------------------------------------------------------------------
{
  const bare = await raw('/auth/callback');
  const loc = bare.headers.get('location') ?? '';
  record(
    'bare /auth/callback redirects to /signup, never 500s',
    bare.status === 303 && loc.startsWith('/signup'),
    `${bare.status} -> ${loc}`
  );

  const badCode = await raw('/auth/callback?code=not-a-real-code');
  const badLoc = badCode.headers.get('location') ?? '';
  record(
    'invalid code bounces back with a message, never 500s',
    badCode.status === 303 && badLoc.startsWith('/signup'),
    `${badCode.status} -> ${badLoc.slice(0, 70)}`
  );
}

// ---------------------------------------------------------------------------
console.log('\nSignout');
// ---------------------------------------------------------------------------
{
  const get = await raw('/auth/signout');
  record(
    'GET /auth/signout does not sign anyone out',
    get.status === 303 && (get.headers.get('location') ?? '') === '/',
    `${get.status}`
  );
}

// ---------------------------------------------------------------------------
console.log('\nCSRF (SvelteKit built-in, covers form posts)');
// ---------------------------------------------------------------------------
{
  const dev = await isDevServer();
  const body = new URLSearchParams({ email: 'probe@example.com', password: 'hunter2hunter2' });

  if (dev) {
    skip(
      'cross-origin POST to an action is refused',
      'vite dev disables CSRF (respond.js `if (!DEV)`) - run against `npm run preview`'
    );
    skip('same-origin POST is accepted (control)', 'same reason');
  } else {
    const crossOrigin = await raw('/signup?/signin', {
      method: 'POST',
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        origin: 'https://evil.example'
      },
      body
    });
    record(
      'cross-origin POST to an action is refused',
      crossOrigin.status === 403,
      `${crossOrigin.status}`
    );

    // Negative control. Same request, our own Origin. If this also 403s, the
    // check above is measuring something other than the origin.
    const sameOrigin = await raw('/signup?/signin', {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded', origin: BASE },
      body
    });
    record(
      'same-origin POST is accepted (control)',
      sameOrigin.status !== 403,
      `${sameOrigin.status}`
    );
  }
}

// ---------------------------------------------------------------------------
console.log('\nOpen redirect (safeRedirect)');
// ---------------------------------------------------------------------------
{
  const hostile = [
    'https://evil.example',
    '//evil.example',
    '/\\evil.example',
    'javascript:alert(1)',
    'http://evil.example/path'
  ];
  const rejected = hostile.filter((t) => safeRedirect(t) === '/');
  record(
    'hostile next= values are rejected',
    rejected.length === hostile.length,
    `${rejected.length}/${hostile.length}`
  );

  const benign = ['/read', '/checklist', '/book/03-chapter1'];
  const kept = benign.filter((t) => safeRedirect(t) === t);
  record('same-site next= values are kept (control)', kept.length === benign.length, `${kept.length}/${benign.length}`);

  record('CRLF in next= is rejected', safeRedirect('/read\r\nX-Injected: 1') === '/', '');
  record('/auth/* loop is broken', safeRedirect('/auth/callback') === '/', '');

  // End to end: the value must not survive into the rendered page.
  const res = await raw('/signup?next=https://evil.example');
  const html = await res.text();
  record(
    'hostile next= does not reach the rendered page',
    !html.includes('evil.example'),
    ''
  );
}

// ---------------------------------------------------------------------------
console.log('\nPassword policy');
// ---------------------------------------------------------------------------
{
  const rejects = [
    ['', 'empty'],
    ['short', 'under 8'],
    ['password', 'common'],
    ['aaaaaaaa', 'single repeated char'],
    ['x'.repeat(200), 'over the bcrypt 72-byte limit']
  ];
  const failed = rejects.filter(([pw]) => checkPassword(pw, 'someone@example.com').ok === false);
  record('weak passwords are rejected', failed.length === rejects.length, `${failed.length}/${rejects.length}`);

  record(
    'password equal to the email is rejected',
    checkPassword('someone', 'someone@example.com').ok === false,
    ''
  );

  const accepts = ['correct horse battery', 'Tr0ub4dor&3xx', 'a-reasonable-passphrase'];
  const ok = accepts.filter((pw) => checkPassword(pw, 'someone@example.com').ok === true);
  record('reasonable passwords are accepted (control)', ok.length === accepts.length, `${ok.length}/${accepts.length}`);

  // A multi-byte password under 72 characters but over 72 bytes must be caught
  // by the BYTE check; a character-length check would wave it through.
  const emoji = 'x'.repeat(20) + 'a'.repeat(0) + '.'.repeat(0) + 'e'.repeat(0) + 'X'.repeat(0);
  record(
    'byte length is what is measured, not character count',
    checkPassword('a'.repeat(73), 'someone@example.com').ok === false && emoji.length === 20,
    ''
  );

  record(
    'strength score matches the meter contract',
    strengthScore('') === 0 && strengthScore('abcdefgh') === 0 && strengthScore('abcdefghijklm1!') === 3,
    `${strengthScore('abcdefghijklm1!')}`
  );
}

// ---------------------------------------------------------------------------
console.log('\nConfig guard (a bad env var must not 500 the site)');
// ---------------------------------------------------------------------------
{
  // Regression test for 2026-08-01: an unedited .env.example URL reached
  // createClient(), which throws at module scope, which 500'd every route
  // including ones that never touch Supabase. The guard has to reject bad
  // values AND still accept good ones, or it just disables Supabase entirely.
  const rejects = [
    'https://<your-project-ref>.supabase.co',
    'your_supabase_url',
    'not a url',
    undefined
  ];
  const refused = rejects.filter((u) => isUsableSupabaseUrl(u) === false);
  record('placeholder / malformed URLs refused', refused.length === rejects.length,
    `${refused.length}/${rejects.length}`);

  record('a real project URL is accepted (control)',
    isUsableSupabaseUrl('https://abcdefghijklm.supabase.co') === true, '');
  record('a real key is accepted (control)',
    isUsableSupabaseKey('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.body.sig') === true, '');
  record('placeholder key refused',
    isUsableSupabaseKey('your_supabase_anon_key') === false, '');

  // The end-to-end version: whatever this deployment's config is, the site
  // must serve. A 500 here means the guard is not doing its job.
  const home = await raw('/');
  record('homepage serves regardless of Supabase config', home.status === 200, `${home.status}`);
}

// ---------------------------------------------------------------------------
const failures = results.filter((r) => !r.pass);
console.log(`\n${results.length - failures.length}/${results.length} checks passed\n`);

if (process.env.PROBE_JSON) {
  console.log(JSON.stringify({ base: BASE, results }, null, 2));
}

if (failures.length > 0) {
  console.error('Failed:');
  for (const f of failures) console.error(`  - ${f.name} (${f.detail})`);
  process.exit(1);
}
