/**
 * ADMIN: mint, list and revoke activation codes.
 *
 *   POST   /api/admin/activation-codes   mint a batch, returns the plaintext
 *   GET    /api/admin/activation-codes   list metadata (never the codes)
 *   PATCH  /api/admin/activation-codes   revoke one by id
 *
 * Requires `Authorization: Bearer <ADMIN_ACTIVATION_TOKEN>`.
 *
 * WHY A SEPARATE TOKEN FROM /api/admin/reconcile
 *
 * ADMIN_RECONCILE_TOKEN authorises reading the customer list. This endpoint
 * MINTS CREDENTIALS - a caller who can POST here can manufacture themselves
 * unlimited access to the paid book, and to anything accounts unlock later.
 * Those are different capabilities and they belong to different secrets, so
 * handing the reporting token to whatever runs a reconciliation cron does not
 * also hand over the ability to print keys. Both go through authorizeAdmin(),
 * which fails shut on an unset or under-length secret; see its header.
 *
 * THE RESPONSE TO A MINT IS THE ONLY COPY OF THOSE CODES.
 *
 * The database stores SHA-256 digests, so nothing here or anywhere else can
 * recover a code after this response is discarded. That is the property that
 * makes a leaked database dump useless, and the reason the response is marked
 * no-store: a mint response sitting in a proxy cache is a list of live keys.
 * Lose the response and the remedy is to revoke those rows and mint again.
 */
import { json } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import { authorizeAdmin } from '$lib/server/adminToken.js';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { mintActivationCodes } from '$lib/server/activationCodes.js';

export const prerender = false;

/**
 * Vague for a caller who is not authorised, specific for one who is. Telling an
 * unauthenticated stranger the difference between "wrong token" and "no token
 * configured" hands them a probe for free. Copied in shape from
 * /api/admin/reconcile deliberately - one house style for admin refusals.
 */
const DENIED = {
  'not-configured': 'Not configured',
  'token-too-short': 'Not configured',
  'missing-token': 'Unauthorized',
  'bad-token': 'Unauthorized',
};

/** Shared guard. Returns a Response to send, or null to proceed. */
function guard(request, route) {
  const auth = authorizeAdmin(request.headers.get('authorization'), env.ADMIN_ACTIVATION_TOKEN);
  if (!auth.ok) {
    // Real reason server-side, so an operator can tell a misconfiguration from
    // a bad call without that difference going on the wire.
    console.warn(`[activation-codes:${route}] denied: ${auth.reason}`);
    return json({ error: DENIED[auth.reason] ?? 'Unauthorized' }, { status: auth.status });
  }
  if (!supabaseAdmin) {
    return json({ error: 'Database is not configured.' }, { status: 503 });
  }
  return null;
}

/** Never cache a response that carries live credentials. */
const NO_STORE = { 'Cache-Control': 'no-store, no-cache, must-revalidate, private' };

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
  const denied = guard(request, 'mint');
  if (denied) return denied;

  const body = await request.json().catch(() => null);
  if (!body || typeof body !== 'object') {
    return json({ error: 'Expected a JSON object.' }, { status: 400 });
  }

  const count = body.count ?? 1;
  const maxUses = body.max_uses ?? body.maxUses ?? 1;
  const label = typeof body.label === 'string' ? body.label : '';
  const createdBy = typeof body.created_by === 'string' ? body.created_by : 'admin-api';

  // Expiry. Parsed and re-serialised rather than passed through, so a typo
  // becomes a 400 here instead of a Postgres error - or worse, a null that
  // silently mints codes that never expire.
  let expiresAt = null;
  const rawExpiry = body.expires_at ?? body.expiresAt ?? null;
  if (rawExpiry !== null && rawExpiry !== undefined) {
    const parsed = new Date(rawExpiry);
    if (Number.isNaN(parsed.getTime())) {
      return json({ error: 'expires_at is not a valid date.' }, { status: 400 });
    }
    if (parsed.getTime() <= Date.now()) {
      return json({ error: 'expires_at is already in the past.' }, { status: 400 });
    }
    expiresAt = parsed.toISOString();
  }

  const result = await mintActivationCodes({ count, label, maxUses, expiresAt, createdBy });
  if (!result.ok) {
    // `codes` may be partially populated when a batch fails midway. Returning
    // them is not optional: those rows exist in the database, and withholding
    // the only copy of their plaintext would strand live credentials nobody can
    // use and nobody knows to revoke.
    return json(
      { error: result.error, partial: result.codes ?? [] },
      { status: 400, headers: NO_STORE }
    );
  }

  return json(
    {
      ok: true,
      count: result.codes.length,
      max_uses: maxUses,
      expires_at: expiresAt,
      label,
      codes: result.codes,
      warning:
        'This is the only time these codes are readable. They are stored as ' +
        'SHA-256 digests and cannot be recovered. Save them now.',
    },
    { status: 201, headers: NO_STORE }
  );
}

/**
 * List codes. Metadata only - `code_hash` is never selected.
 *
 * Withholding the digest is not theatre. It is the input to an offline
 * dictionary attack, and while 60 bits makes that hopeless today, an endpoint
 * that hands out digests is one weak-code-format change away from being the
 * whole vulnerability. There is no operational reason to see it.
 */
export async function GET({ request, url }) {
  const denied = guard(request, 'list');
  if (denied) return denied;

  const limit = Math.min(Number.parseInt(url.searchParams.get('limit') ?? '100', 10) || 100, 500);

  const { data, error } = await supabaseAdmin
    .from('activation_codes')
    .select('id, label, max_uses, uses, expires_at, revoked_at, created_at, created_by')
    .order('created_at', { ascending: false })
    .limit(limit);

  if (error) {
    console.error('[activation-codes:list]', error.message);
    return json({ error: 'Could not list codes.' }, { status: 500 });
  }

  const now = Date.now();
  return json({
    ok: true,
    count: data.length,
    codes: data.map((c) => ({
      ...c,
      // Computed here so a human reading the list does not have to cross-check
      // three columns and a clock to answer "does this one still work?".
      status: c.revoked_at
        ? 'revoked'
        : c.expires_at && new Date(c.expires_at).getTime() <= now
          ? 'expired'
          : c.uses >= c.max_uses
            ? 'exhausted'
            : 'active',
      remaining: Math.max(0, c.max_uses - c.uses),
    })),
  });
}

/**
 * Revoke a code by id. The kill switch that does not care about counters.
 *
 * Revocation is by `id`, not by the code itself, because the plaintext is gone
 * and the digest is not exposed by GET. Take the id from the listing.
 *
 * Idempotent: revoking an already-revoked code leaves the original timestamp,
 * which is the one that matters if the revocation is ever questioned.
 */
export async function PATCH({ request }) {
  const denied = guard(request, 'revoke');
  if (denied) return denied;

  const body = await request.json().catch(() => null);
  const id = body?.id;
  if (typeof id !== 'string' || id.length === 0) {
    return json({ error: 'Expected { "id": "<uuid>" }.' }, { status: 400 });
  }

  const { data, error } = await supabaseAdmin
    .from('activation_codes')
    .update({ revoked_at: new Date().toISOString() })
    .eq('id', id)
    .is('revoked_at', null)
    .select('id, label, revoked_at')
    .maybeSingle();

  if (error) {
    console.error('[activation-codes:revoke]', error.message);
    return json({ error: 'Could not revoke.' }, { status: 500 });
  }

  // No row came back: either the id does not exist, or it was already revoked.
  // Both are reported as success, because the caller's intent - "this code must
  // not work" - is satisfied either way.
  return json({ ok: true, revoked: data ?? null, already: data === null });
}
