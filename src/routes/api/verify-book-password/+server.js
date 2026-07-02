import { json } from '@sveltejs/kit';
import { peekRate, recordHit } from '$lib/server/rateLimit.js';
import { verifyBookPassword, BOOK_ACCESS_COOKIE } from '$lib/server/bookAccess.js';

// Per-IP: max 5 FAILED attempts per 10 minutes. Successful attempts don't
// count, so multiple legitimate buyers behind one shared IP (CGNAT, office,
// café) can't lock each other out; brute force is still capped.
const RATE_LIMIT = 5;
const RATE_WINDOW_MS = 10 * 60 * 1000;
const COOKIE_MAX_AGE = 60 * 60 * 24 * 365; // 1 year — one-time purchase, long-lived gate

/** @type {import('./$types').RequestHandler} */
export async function POST(event) {
  // 1. Origin check — reject cross-site POSTs (cheap CSRF mitigation).
  const origin = event.request.headers.get('origin');
  if (origin && origin !== event.url.origin) {
    return json({ error: 'Bad request.' }, { status: 403 });
  }

  // 2. Rate limit per client IP (failed attempts only — see note above).
  const ip = event.getClientAddress();
  const rateKey = `book-pw:${ip}`;
  const { allowed, retryAfterMs } = peekRate(rateKey, RATE_LIMIT, RATE_WINDOW_MS);
  if (!allowed) {
    return json(
      { error: 'Too many attempts. Try again later.' },
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

  const password = typeof body.password === 'string' ? body.password : '';
  if (!verifyBookPassword(password)) {
    recordHit(rateKey);
    return json({ error: 'Incorrect password.' }, { status: 401 });
  }

  event.cookies.set(BOOK_ACCESS_COOKIE, '1', {
    path: '/',
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: COOKIE_MAX_AGE,
  });

  return json({ ok: true }, { status: 200 });
}
