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

  // Security headers - applied to every response. Strict by default; loosen if
  // you add new third-party embeds (YouTube, Vimeo, etc.) by extending the
  // relevant CSP directive below.
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'SAMEORIGIN');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('Permissions-Policy', 'geolocation=(), microphone=(), camera=(), payment=()');

  // Content Security Policy - covers Supabase (newsletter), self-hosted assets.
  // Allowlist additions: add domains to the matching directive (script-src, frame-src, etc.).
  const csp = [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline'",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com data:",
    "img-src 'self' data: blob:",
    "media-src 'self'",
    "connect-src 'self' https://*.supabase.co wss://*.supabase.co",
    "frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'self'"
  ].join('; ');
  response.headers.set('Content-Security-Policy', csp);

  return response;
}
