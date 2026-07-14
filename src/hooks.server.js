/**
 * Server hooks - no auth. The site is read-only and does not maintain
 * user sessions. Supabase remains available via `$lib/supabase.js` for
 * anonymous newsletter inserts only.
 */

export async function handle({ event, resolve }) {
  // Fix for "[object Object]" navigation errors (pre-existing safety net)
  if (event.url.pathname.includes('[object%20Object]') || event.url.pathname.includes('[object Object]')) {
    return new Response('Redirect', {
      status: 302,
      headers: { Location: '/' }
    });
  }

  // Stub: anything that still calls locals.safeGetSession() gets a null user.
  // Kept so old callers don't crash during the auth-removal transition.
  event.locals.safeGetSession = async () => ({ session: null, user: null });

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
