import { json } from '@sveltejs/kit';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { rateLimit } from '$lib/server/rateLimit.js';

/** @type {import('./$types').RequestHandler} */
export async function POST(event) {
  const origin = event.request.headers.get('origin');
  if (origin && origin !== event.url.origin) {
    return json({ error: 'Bad request.' }, { status: 403 });
  }

  const contentType = event.request.headers.get('content-type') ?? '';
  if (!contentType.includes('application/json')) {
    return json({ error: 'Bad request.' }, { status: 400 });
  }

  const ip = event.getClientAddress();
  const { allowed } = rateLimit(`unsubscribe:${ip}`, 5, 60_000);
  if (!allowed) {
    return json({ error: 'Too many requests.' }, { status: 429 });
  }

  const body = await event.request.json().catch(() => null);
  if (!body || typeof body.token !== 'string') {
    return json({ error: 'Bad request.' }, { status: 400 });
  }

  // Honeypot: bots fill this, humans don't.
  if (body._hp) return json({ ok: true }, { status: 200 });

  const token = body.token.trim();
  // Basic UUID format check before hitting the DB.
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(token)) {
    return json({ error: 'Invalid token.' }, { status: 400 });
  }

  if (!supabaseAdmin) {
    console.error('[unsubscribe] supabaseAdmin unavailable — check SUPABASE_SERVICE_KEY');
    return json({ error: 'Service unavailable.' }, { status: 503 });
  }

  const { data, error } = await supabaseAdmin
    .from('waitlist')
    .update({ unsubscribed_at: new Date().toISOString() })
    .eq('unsubscribe_token', token)
    .is('unsubscribed_at', null)
    .select('email')
    .single();

  if (error) {
    // PGRST116 = no rows matched (already unsubscribed or bad token)
    if (error.code === 'PGRST116') {
      return json({ error: 'already_unsubscribed' }, { status: 409 });
    }
    console.error('[unsubscribe]', error.message);
    return json({ error: 'Something went wrong. Try again.' }, { status: 500 });
  }

  return json({ ok: true, email: data.email }, { status: 200 });
}
