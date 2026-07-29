import { json } from '@sveltejs/kit';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { rateLimit } from '$lib/server/rateLimit.js';
import { sendWelcomeEmail } from '$lib/server/email.js';

const EMAIL_RE = /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/;
const MAX_EMAIL_LENGTH = 254; // RFC 5321

// Per-IP: max 5 signups per 10 minutes.
const RATE_LIMIT = 5;
const RATE_WINDOW_MS = 10 * 60 * 1000;

/** Origin of a Referer URL, or null if it is absent or unparseable. */
function refererOrigin(referer) {
  if (!referer) return null;
  try {
    return new URL(referer).origin;
  } catch {
    return null;
  }
}

/** @type {import('./$types').RequestHandler} */
export async function POST(event) {
  // 1. Origin check - reject cross-site POSTs (cheap CSRF mitigation).
  //
  // This now fails CLOSED. The previous condition was
  // `if (origin && origin !== event.url.origin)`, which skipped the check
  // entirely whenever the header was absent. Verified live on 2026-07-28: a
  // POST with a forged Origin was correctly refused with 403, while a POST
  // with no Origin header at all returned 201. Every non-browser client gets
  // to simply omit the header and walk through, which is the opposite of what
  // the check is for.
  //
  // Requiring it costs no real signup: browsers attach Origin to every POST,
  // same-origin included, and the only two callers are same-origin fetches
  // (NewsletterSignup.svelte, EmailGate.svelte). Referer is accepted as a
  // fallback for the rare privacy tool that strips one header but not the other.
  const origin = event.request.headers.get('origin');
  const expected = event.url.origin;
  const sameOrigin = origin
    ? origin === expected
    : refererOrigin(event.request.headers.get('referer')) === expected;

  if (!sameOrigin) {
    return json({ error: 'Bad request.' }, { status: 403 });
  }

  // 2. Rate limit per client IP.
  const ip = event.getClientAddress();
  const { allowed, retryAfterMs } = rateLimit(`waitlist:${ip}`, RATE_LIMIT, RATE_WINDOW_MS);
  if (!allowed) {
    return json(
      { error: 'Too many requests. Try again later.' },
      { status: 429, headers: { 'Retry-After': String(Math.ceil(retryAfterMs / 1000)) } }
    );
  }

  // 3. Content-type guard.
  const contentType = event.request.headers.get('content-type') ?? '';
  if (!contentType.includes('application/json')) {
    return json({ error: 'Bad request.' }, { status: 400 });
  }

  const body = await event.request.json().catch(() => null);
  if (!body || typeof body !== 'object') {
    return json({ error: 'Bad request.' }, { status: 400 });
  }

  // 4. Honeypot - bots fill this, humans don't. Silent success.
  if (body._hp) {
    return json({ ok: true }, { status: 201 });
  }

  const email = typeof body.email === 'string' ? body.email.trim().toLowerCase() : '';
  const source = typeof body.source === 'string' ? body.source.slice(0, 64).trim() : 'homepage';
  const newsletterConsent = body.newsletter_consent === true;
  const bookReleaseConsent = body.book_release_consent === true;

  if (!email) {
    return json({ error: 'Email is required.' }, { status: 400 });
  }
  if (email.length > MAX_EMAIL_LENGTH) {
    return json({ error: 'Email address is too long.' }, { status: 400 });
  }
  if (!EMAIL_RE.test(email)) {
    return json({ error: 'Enter a valid email address.' }, { status: 400 });
  }
  // No hard consent requirement: the email itself is the value exchange
  // (e.g. unlocking gated content is transactional). We record the consent
  // flags honestly - false/false simply means "captured, do not market".
  // The NewsletterSignup component still enforces an explicit choice in its
  // own UI by disabling submit until a box is checked.

  // Service role only. There is deliberately no anon fallback any more.
  //
  // There used to be one (`supabaseAdmin ?? createSupabaseServerClient(event)`)
  // for local dev without secrets. sql/012 revoked every anon grant on this
  // table on 2026-07-28, so that path can now only ever return 42501. Keeping
  // it would turn a missing service key into a confusing "permission denied"
  // deep in the insert instead of an obvious misconfiguration here, and it was
  // the last thing in the codebase importing a Supabase client that could be
  // constructed in a browser.
  //
  // This endpoint is now the only door into the table. That is the point:
  // anything reachable with the publishable key is reachable by anyone,
  // skipping the origin check, rate limit, honeypot and validation above.
  if (!supabaseAdmin) {
    console.error('[waitlist] SUPABASE_SERVICE_KEY is not configured; cannot record signup.');
    return json({ error: 'Signups are temporarily unavailable.' }, { status: 503 });
  }
  const supabase = supabaseAdmin;

  let { error } = await supabase
    .from('waitlist')
    .insert({ email, source, newsletter_consent: newsletterConsent, book_release_consent: bookReleaseConsent });

  // Graceful fallback: if the consent columns don't exist yet (migration not
  // run) or aren't in PostgREST's schema cache, capturing the email still
  // matters most - retry with the minimal row so the funnel never hard-fails.
  // 42703 = undefined column; PGRST204 = column not found in schema cache.
  if (error && (error.code === '42703' || error.code === 'PGRST204')) {
    console.warn('[waitlist] consent columns missing - run sql/001_waitlist.sql. Falling back to email-only insert.');
    ({ error } = await supabase.from('waitlist').insert({ email, source }));
  }

  if (error) {
    if (error.code === '23505') {
      return json({ error: 'already_subscribed' }, { status: 409 });
    }
    console.error('[waitlist insert]', error.message);
    return json({ error: 'Something went wrong. Try again.' }, { status: 500 });
  }

  // Fetch the generated unsubscribe token so we can include a real link in the
  // welcome email. Use the admin client since anon SELECT is blocked by RLS.
  let unsubscribeToken;
  if (supabaseAdmin) {
    const { data: tokenRow } = await supabaseAdmin
      .from('waitlist')
      .select('unsubscribe_token')
      .eq('email', email)
      .single();
    unsubscribeToken = tokenRow?.unsubscribe_token;
  }

  // Welcome/confirmation email. Out of the signup critical path: the DB insert is
  // the only thing the visitor waits on, so a slow/rate-limited Resend send during
  // a traffic spike never becomes signup latency. On serverless we hand the send to
  // waitUntil() so it survives after the response is returned (a bare promise can be
  // killed when the isolate freezes); locally it just runs in the background.
  const welcome = sendWelcomeEmail({ to: email, source, unsubscribeToken }).catch((e) =>
    console.error('[waitlist] welcome email threw:', e?.message ?? e)
  );
  if (event.platform?.context?.waitUntil) {
    event.platform.context.waitUntil(welcome);
  }

  return json({ ok: true }, { status: 201 });
}
