import { json } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';

const WEBHOOK_SECRET = env.RESEND_WEBHOOK_SECRET;

// Svix (which Resend uses) rejects anything older than 5 minutes. Matching
// that here stops a captured request being replayed back at us later.
const TOLERANCE_SECONDS = 5 * 60;

/**
 * Which outcome is allowed to overwrite which.
 *
 * Webhook deliveries are not ordered. Without a rule, a straggling 'sent'
 * event arriving after 'delivered' would quietly downgrade the record and the
 * customer would look unfulfilled. Higher rank wins; equal or lower is
 * ignored.
 *
 * bounced/complained outrank the success states on purpose: those are the two
 * that mean a human needs to intervene, and burying one under a stale
 * 'delivered' is the failure this whole table exists to prevent.
 */
const RANK = {
  failed: 0,
  sent: 1,
  delivery_delayed: 2,
  delivered: 3,
  opened: 4,
  clicked: 5,
  bounced: 6,
  complained: 7
};

/** Constant-time compare so a signature cannot be recovered by timing. */
function safeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

/**
 * Verify a Svix signature.
 *
 * Deliberately async and built on SubtleCrypto. This runs on the Cloudflare
 * Workers runtime, where SubtleCrypto is the only crypto provider and it is
 * async-only - the exact condition that made the Stripe webhook reject every
 * event it ever received while looking correctly configured from outside.
 * There is no synchronous path here to get wrong.
 */
async function verifySvixSignature({ secret, id, timestamp, header, body }) {
  const b64 = secret.startsWith('whsec_') ? secret.slice(6) : secret;
  const keyBytes = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
  const key = await crypto.subtle.importKey(
    'raw', keyBytes, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const mac = await crypto.subtle.sign(
    'HMAC', key, new TextEncoder().encode(`${id}.${timestamp}.${body}`)
  );
  const expected = btoa(String.fromCharCode(...new Uint8Array(mac)));

  // Header is space-separated "v<version>,<base64sig>" pairs; Svix sends more
  // than one during a secret rotation, and any match is valid.
  return header
    .split(' ')
    .map((part) => part.split(',')[1])
    .filter(Boolean)
    .some((sig) => safeEqual(sig, expected));
}

/**
 * Resend delivery events. This is what turns "we sent it" into "they got it".
 *
 * @type {import('./$types').RequestHandler}
 */
export async function POST({ request }) {
  if (!WEBHOOK_SECRET) {
    console.error('[resend-webhook] RESEND_WEBHOOK_SECRET not set; rejecting.');
    return json({ error: 'Not configured' }, { status: 503 });
  }

  const id = request.headers.get('svix-id');
  const timestamp = request.headers.get('svix-timestamp');
  const signature = request.headers.get('svix-signature');
  if (!id || !timestamp || !signature) {
    return json({ error: 'Missing signature headers' }, { status: 400 });
  }

  const age = Math.abs(Math.floor(Date.now() / 1000) - Number(timestamp));
  if (!Number.isFinite(age) || age > TOLERANCE_SECONDS) {
    return json({ error: 'Timestamp outside tolerance' }, { status: 400 });
  }

  // Exact raw bytes: a JSON.parse -> stringify round trip would change
  // whitespace and key order and break the HMAC.
  const rawBody = await request.text();

  let ok;
  try {
    ok = await verifySvixSignature({
      secret: WEBHOOK_SECRET, id, timestamp, header: signature, body: rawBody
    });
  } catch (err) {
    // Split from "signature did not match" on purpose. Collapsing a config
    // fault into a generic rejection is what hid the Stripe bug for weeks.
    console.error(
      `[resend-webhook] verification could not run (likely misconfiguration): ` +
      `${err?.constructor?.name}: ${err?.message}`
    );
    return json({ error: 'Invalid signature' }, { status: 400 });
  }
  if (!ok) {
    console.error('[resend-webhook] signature rejected');
    return json({ error: 'Invalid signature' }, { status: 400 });
  }

  let event;
  try {
    event = JSON.parse(rawBody);
  } catch {
    return json({ error: 'Bad payload' }, { status: 400 });
  }

  // 'email.delivered' -> 'delivered'
  const status = String(event?.type ?? '').replace(/^email\./, '');
  const messageId = event?.data?.email_id;
  if (!(status in RANK) || !messageId) {
    // Unknown event types are acknowledged, not retried. Resend adds new ones
    // over time and a 400 here would make it retry forever.
    return json({ received: true, ignored: true });
  }

  if (!supabaseAdmin) {
    console.error('[resend-webhook] supabaseAdmin unavailable; cannot record', status);
    return json({ error: 'Storage unavailable' }, { status: 503 });
  }

  const eventAt = event?.created_at ? new Date(event.created_at).toISOString() : new Date().toISOString();
  const lower = Object.keys(RANK).filter((s) => RANK[s] < RANK[status]);

  try {
    const { data: updated, error } = await supabaseAdmin
      .from('email_deliveries')
      .update({ status, last_event_at: eventAt })
      .eq('message_id', messageId)
      .in('status', lower)
      .select('id');

    if (error) throw new Error(error.message);

    if (!updated?.length) {
      // Either the row is already at an equal-or-higher rank (nothing to do),
      // or we have never seen this message id - which happens for anything
      // sent before this table existed. Record it rather than drop it.
      const { data: existing } = await supabaseAdmin
        .from('email_deliveries')
        .select('id')
        .eq('message_id', messageId)
        .maybeSingle();

      if (!existing) {
        await supabaseAdmin.from('email_deliveries').insert({
          message_id: messageId,
          to_email: Array.isArray(event?.data?.to) ? event.data.to[0] : (event?.data?.to ?? 'unknown'),
          email_type: 'unknown',
          status,
          last_event_at: eventAt
        });
      }
    }
  } catch (err) {
    // 500 so Svix retries with backoff rather than losing the outcome.
    console.error('[resend-webhook] could not record event:', err?.message ?? err);
    return json({ error: 'Record failed' }, { status: 500 });
  }

  return json({ received: true });
}
