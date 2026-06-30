import { json } from '@sveltejs/kit';
import { createSupabaseServerClient } from '$lib/supabase.js';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { rateLimit } from '$lib/server/rateLimit.js';
import { sendWelcomeEmail } from '$lib/server/email.js';

const EMAIL_RE = /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/;
const MAX_EMAIL_LENGTH = 254; // RFC 5321

// Per-IP: max 5 signups per 10 minutes.
const RATE_LIMIT = 5;
const RATE_WINDOW_MS = 10 * 60 * 1000;

/** @type {import('./$types').RequestHandler} */
export async function POST(event) {
  // 1. Origin check — reject cross-site POSTs (cheap CSRF mitigation).
  const origin = event.request.headers.get('origin');
  if (origin && origin !== event.url.origin) {
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

  // 4. Honeypot — bots fill this, humans don't. Silent success.
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
  // flags honestly — false/false simply means "captured, do not market".
  // The NewsletterSignup component still enforces an explicit choice in its
  // own UI by disabling submit until a box is checked.

  const supabase = createSupabaseServerClient(event);

  let { error } = await supabase
    .from('waitlist')
    .insert({ email, source, newsletter_consent: newsletterConsent, book_release_consent: bookReleaseConsent });

  // Graceful fallback: if the consent columns don't exist yet (migration not
  // run) or aren't in PostgREST's schema cache, capturing the email still
  // matters most — retry with the minimal row so the funnel never hard-fails.
  // 42703 = undefined column; PGRST204 = column not found in schema cache.
  if (error && (error.code === '42703' || error.code === 'PGRST204')) {
    console.warn('[waitlist] consent columns missing — run sql/001_waitlist.sql. Falling back to email-only insert.');
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
