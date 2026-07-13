import { json } from '@sveltejs/kit';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { rateLimit } from '$lib/server/rateLimit.js';
import { sendAdminDiscordApplicationAlert, sendDiscordApplicationConfirmation } from '$lib/server/email.js';

const EMAIL_RE = /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/;
const RATE_LIMIT = 3;
const RATE_WINDOW_MS = 10 * 60 * 1000;

/** @type {import('./$types').RequestHandler} */
export async function POST(event) {
  // Origin check: cheap CSRF mitigation.
  const origin = event.request.headers.get('origin');
  if (origin && origin !== event.url.origin) {
    return json({ error: 'Bad request.' }, { status: 403 });
  }

  // Rate limit per client IP.
  const ip = event.getClientAddress();
  const { allowed, retryAfterMs } = rateLimit(`discord-app:${ip}`, RATE_LIMIT, RATE_WINDOW_MS);
  if (!allowed) {
    return json(
      { error: 'Too many requests. Try again later.' },
      { status: 429, headers: { 'Retry-After': String(Math.ceil(retryAfterMs / 1000)) } }
    );
  }

  const contentType = event.request.headers.get('content-type') ?? '';
  if (!contentType.includes('application/json')) {
    return json({ error: 'Bad request.' }, { status: 400 });
  }

  const body = await event.request.json().catch(() => null);
  if (!body || typeof body !== 'object') {
    return json({ error: 'Bad request.' }, { status: 400 });
  }

  // Honeypot: silent success so bots get no signal.
  if (body._hp) return json({ ok: true }, { status: 201 });

  const name   = typeof body.name  === 'string' ? body.name.trim().slice(0, 120)   : '';
  const email  = typeof body.email === 'string' ? body.email.trim().toLowerCase()  : '';
  const answer = typeof body.answer === 'string' ? body.answer.trim().slice(0, 2000) : '';

  if (!name)                 return json({ error: 'Name is required.' },             { status: 400 });
  if (!email)                return json({ error: 'Email is required.' },            { status: 400 });
  if (email.length > 254)    return json({ error: 'Email address is too long.' },    { status: 400 });
  if (!EMAIL_RE.test(email)) return json({ error: 'Enter a valid email address.' },   { status: 400 });
  if (!answer)                return json({ error: 'Tell us a bit about yourself.' }, { status: 400 });

  if (!supabaseAdmin) {
    return json({ error: 'Service unavailable.' }, { status: 503 });
  }

  const { error } = await supabaseAdmin
    .from('discord_applications')
    .insert({ name, email, answer });

  if (error) {
    console.error('[discord-application] insert error:', error.message);
    return json({ error: 'Something went wrong. Try again.' }, { status: 500 });
  }

  // Notifications: applicant confirmation + admin alert. Not gating the
  // response on these - a slow/rate-limited Resend send shouldn't hold up
  // the applicant's confirmation of a successful submission.
  const notify = Promise.all([
    sendDiscordApplicationConfirmation({ name, email }).catch((e) => console.error('[discord-application] confirmation threw:', e?.message ?? e)),
    sendAdminDiscordApplicationAlert({ name, email, answer }).catch((e) => console.error('[discord-application] admin alert threw:', e?.message ?? e)),
  ]);
  if (event.platform?.context?.waitUntil) {
    event.platform.context.waitUntil(notify);
  }

  return json({ ok: true }, { status: 201 });
}
