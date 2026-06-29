import { json } from '@sveltejs/kit';
import { withSupabase } from '@supabase/server';
import { SUPABASE_URL, SUPABASE_SECRET_KEY, SUPABASE_PUBLISHABLE_KEY } from '$env/static/private';
import { rateLimit } from '$lib/server/rateLimit.js';
import { sendAdminPreorderAlert, sendPreorderConfirmation } from '$lib/server/email.js';

const EMAIL_RE = /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/;
const AUTHORS_LIMIT = 100;
const RATE_LIMIT = 3;
const RATE_WINDOW_MS = 10 * 60 * 1000;

// Pass Supabase env explicitly: Vite doesn't inject private vars into process.env.
const supabaseEnv = {
  url: SUPABASE_URL,
  secretKeys:      { default: SUPABASE_SECRET_KEY },
  publishableKeys: { default: SUPABASE_PUBLISHABLE_KEY },
};

const preorderHandler = withSupabase({ auth: 'none', env: supabaseEnv }, async (req, ctx) => {
  const contentType = req.headers.get('content-type') ?? '';
  if (!contentType.includes('application/json')) {
    return Response.json({ error: 'Bad request.' }, { status: 400 });
  }

  const body = await req.json().catch(() => null);
  if (!body || typeof body !== 'object') {
    return Response.json({ error: 'Bad request.' }, { status: 400 });
  }

  // Honeypot: silent success so bots get no signal.
  if (body._hp) return Response.json({ ok: true }, { status: 201 });

  const email       = typeof body.email        === 'string' ? body.email.trim().toLowerCase()  : '';
  const name        = typeof body.name         === 'string' ? body.name.trim().slice(0, 120)   : '';
  const editionType = body.edition_type === 'authors' ? 'authors' : 'regular';

  if (!email)                return Response.json({ error: 'Email is required.' },            { status: 400 });
  if (email.length > 254)    return Response.json({ error: 'Email address is too long.' },    { status: 400 });
  if (!EMAIL_RE.test(email)) return Response.json({ error: 'Enter a valid email address.' },  { status: 400 });

  // Check author's edition capacity before inserting.
  if (editionType === 'authors') {
    const { data: counts, error: countErr } = await ctx.supabaseAdmin
      .from('preorder_counts')
      .select('claimed')
      .eq('edition_type', 'authors')
      .maybeSingle();

    if (countErr) {
      console.error('[preorder count]', countErr.message);
      return Response.json({ error: 'Something went wrong. Try again.' }, { status: 500 });
    }

    if ((counts?.claimed ?? 0) >= AUTHORS_LIMIT) {
      return Response.json({ error: 'sold_out' }, { status: 409 });
    }
  }

  const { data, error } = await ctx.supabaseAdmin
    .from('preorders')
    .insert({ email, name, edition_type: editionType, source: 'launch-page' })
    .select('copy_number')
    .single();

  if (error) {
    if (error.code === '23505')               return Response.json({ error: 'already_preordered' }, { status: 409 });
    if (error.message?.includes('SOLD_OUT'))  return Response.json({ error: 'sold_out' },            { status: 409 });
    console.error('[preorder insert]', error.message);
    return Response.json({ error: 'Something went wrong. Try again.' }, { status: 500 });
  }

  // Non-blocking notifications.
  const notifyArgs = { name, email, edition_type: editionType, copy_number: data?.copy_number ?? null };
  sendAdminPreorderAlert(notifyArgs)
    .catch((e) => console.error('[preorder] admin alert threw:', e?.message ?? e));
  sendPreorderConfirmation(notifyArgs)
    .catch((e) => console.error('[preorder] confirmation threw:', e?.message ?? e));

  return Response.json({ ok: true, copy_number: data?.copy_number ?? null }, { status: 201 });
});

/** @type {import('./$types').RequestHandler} */
export async function POST(event) {
  // Origin check: cheap CSRF mitigation.
  const origin = event.request.headers.get('origin');
  if (origin && origin !== event.url.origin) {
    return json({ error: 'Bad request.' }, { status: 403 });
  }

  // Rate limit per client IP (SvelteKit event has getClientAddress; the handler doesn't).
  const ip = event.getClientAddress();
  const { allowed, retryAfterMs } = rateLimit(`preorder:${ip}`, RATE_LIMIT, RATE_WINDOW_MS);
  if (!allowed) {
    return json(
      { error: 'Too many requests. Try again later.' },
      { status: 429, headers: { 'Retry-After': String(Math.ceil(retryAfterMs / 1000)) } }
    );
  }

  return preorderHandler(event.request);
}
