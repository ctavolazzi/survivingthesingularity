/**
 * Server hooks.
 *
 * NO AUTH, AGAIN, AND THIS TIME BY RULING RATHER THAN BY DEFAULT
 *
 * Accounts, sessions and sign-in existed here between 2026-08-01 and
 * 2026-08-04, then CT killed them: "kill user profiles. Kill accounts. Kill
 * sign in." The identity model is the purchase email. Buyers are recognised
 * by the address they paid with (the transactions ledger the Stripe webhook
 * writes), and future editions reach them by email with whatever discount the
 * terms of that day set. No passwords, no sessions, no cookies to protect, no
 * OAuth surface, and a privacy policy a person can actually read.
 *
 * The rule the old auth was built around still stands and is now simpler to
 * see: there is no browser-side Supabase client and no key of any kind in the
 * bundle. Every table read goes through `$lib/server/supabaseAdmin.js` on the
 * service role. See README's "Database access" section.
 *
 * The auth implementation was removed at commit history around 2026-08-04; if
 * it is ever wanted again it is one revert away, but read the ruling above
 * before proposing that.
 */

export async function handle({ event, resolve }) {
  // Fix for "[object Object]" navigation errors (pre-existing safety net)
  if (event.url.pathname.includes('[object%20Object]') || event.url.pathname.includes('[object Object]')) {
    return new Response('Redirect', {
      status: 302,
      headers: { Location: '/' }
    });
  }

  const response = await resolve(event);

  // Security headers for SSR routes (Worker). CSP is handled by kit.csp in
  // svelte.config.js, which injects per-request nonces into SvelteKit's own
  // inline scripts and sets the CSP header automatically. Prerendered pages
  // get CSP from static/_headers (served by Cloudflare Pages CDN, no Worker).
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'SAMEORIGIN');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('Permissions-Policy', 'geolocation=(), microphone=(), camera=(), payment=()');
  response.headers.set('Cross-Origin-Opener-Policy', 'same-origin');
  response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');

  return response;
}
