/**
 * Activation codes: the half that talks to Postgres.
 *
 * The pure half - generation, normalization, hashing, error copy - lives in
 * activationCodeCrypto.js and is imported here. This file adds the database
 * round trips and nothing else.
 *
 * WHERE THE ATOMICITY LIVES, AND WHY IT IS NOT IN THIS FILE
 *
 * `redeemActivationCode()` is a thin wrapper over the `redeem_activation_code`
 * SQL function from sql/015. That is deliberate. The obvious JavaScript version
 * - read the row, check `uses < max_uses`, write it back - is a check-then-act
 * race with a real exploit: two requests carrying a code's last use both read
 * `uses = 0`, both conclude they may proceed, and the code is spent twice. This
 * deploys to Cloudflare Workers, where those two requests are not even in the
 * same isolate, so no mutex in this process could fix it. The row lock inside
 * Postgres is the only place the check and the write become indivisible.
 *
 * Keep the rules in SQL. Keep this file dumb.
 */
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import {
  generateActivationCode,
  normalizeActivationCode,
  hashActivationCode,
} from '$lib/server/activationCodeCrypto.js';

/**
 * Is this code currently worth emailing a sign-in link about?
 *
 * Does NOT spend the code. Nothing is burned until the far side of the magic
 * link, once the address has been proven - see the activation_intents note in
 * sql/015 for why that ordering is the whole point rather than a nicety.
 *
 * @param {unknown} rawInput whatever the user typed
 * @returns {Promise<{ ok: boolean, reason: string, codeId?: string }>}
 */
export async function inspectActivationCode(rawInput) {
  const canonical = normalizeActivationCode(rawInput);
  // Rejected without a query. A malformed code is not a database question.
  if (!canonical) return { ok: false, reason: 'not_found' };

  if (!supabaseAdmin) {
    console.error('[activationCodes] SUPABASE_SERVICE_KEY is not configured; cannot inspect codes.');
    return { ok: false, reason: 'unavailable' };
  }

  const codeHash = await hashActivationCode(canonical);
  const { data, error } = await supabaseAdmin.rpc('inspect_activation_code', {
    p_code_hash: codeHash,
  });

  if (error) {
    console.error('[activationCodes] inspect failed:', error.message);
    return { ok: false, reason: 'unavailable' };
  }
  return { ok: data?.ok === true, reason: data?.reason ?? 'not_found', codeId: data?.code_id };
}

/**
 * Spend a code, atomically.
 *
 * Every guard - expiry, revocation, the use ceiling, the already-redeemed
 * shortcut - lives inside the SQL function under a row lock. This wrapper adds
 * error handling and nothing else, on purpose.
 *
 * @param {{ codeId: string, userId: string|null, email: string }} args
 * @returns {Promise<{ ok: boolean, reason: string, remaining?: number }>}
 */
export async function redeemActivationCode({ codeId, userId, email }) {
  if (!supabaseAdmin) {
    console.error('[activationCodes] SUPABASE_SERVICE_KEY is not configured; cannot redeem.');
    return { ok: false, reason: 'unavailable' };
  }

  const { data, error } = await supabaseAdmin.rpc('redeem_activation_code', {
    p_code_id: codeId,
    p_user_id: userId,
    p_email: email,
  });

  if (error) {
    console.error('[activationCodes] redeem failed:', error.message);
    return { ok: false, reason: 'unavailable' };
  }
  return { ok: data?.ok === true, reason: data?.reason ?? 'not_found', remaining: data?.remaining };
}

/**
 * Record which code a pending sign-in is carrying, keyed by the address that
 * has yet to prove itself.
 *
 * Stores `code_id`, never the code. No plaintext crosses the magic-link round
 * trip: not in this table, not in the link, not in the email. Upsert so that
 * asking for a second link replaces the first intent instead of colliding.
 *
 * @param {{ email: string, codeId: string }} args
 * @returns {Promise<boolean>} whether the intent was recorded
 */
export async function recordActivationIntent({ email, codeId }) {
  if (!supabaseAdmin) return false;
  const { error } = await supabaseAdmin
    .from('activation_intents')
    .upsert(
      {
        email: email.toLowerCase(),
        code_id: codeId,
        created_at: new Date().toISOString(),
        expires_at: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
      },
      { onConflict: 'email' }
    );
  if (error) {
    console.error('[activationCodes] could not record activation intent:', error.message);
    return false;
  }
  return true;
}

/**
 * The pending intent for a now-proven address, if it has not expired.
 *
 * Expiry is checked here rather than left to a cleanup job, because nothing
 * schedules cleanup jobs on this deployment - preorderLookup.js already carries
 * the scar of assuming a purge function runs when nothing calls it. An expired
 * row simply does not count.
 *
 * @param {string} email
 * @returns {Promise<{ codeId: string }|null>}
 */
export async function takeActivationIntent(email) {
  if (!supabaseAdmin) return null;
  const lower = email.toLowerCase();

  const { data, error } = await supabaseAdmin
    .from('activation_intents')
    .select('code_id, expires_at')
    .eq('email', lower)
    .maybeSingle();

  if (error) {
    console.error('[activationCodes] intent lookup failed:', error.message);
    return null;
  }
  if (!data) return null;

  if (new Date(data.expires_at).getTime() <= Date.now()) {
    await clearActivationIntent(lower);
    return null;
  }
  return { codeId: data.code_id };
}

/** Drop a consumed or expired intent. Best effort; never throws. */
export async function clearActivationIntent(email) {
  if (!supabaseAdmin) return;
  const { error } = await supabaseAdmin
    .from('activation_intents')
    .delete()
    .eq('email', email.toLowerCase());
  if (error) console.error('[activationCodes] could not clear intent:', error.message);
}

/**
 * Burn the code a now-proven address was carrying, if it was carrying one.
 *
 * Called from /auth/callback, which is the first moment control of the address
 * is established - by clicking the emailed link, or by a provider asserting it.
 * Everything before that point is a claim, and burning a single-use code on a
 * claim is how a stranger destroys a code before its recipient ever sees it.
 *
 * Ordering matters and is not arbitrary: this must run AFTER the callback's
 * ensureProfile(), because it updates the profile row rather than creating one.
 * ensureProfile writes `access_source: 'signup'` with `ignoreDuplicates`, so it
 * never overwrites a row that already says 'activation_code'.
 *
 * Never throws. A redemption failure must not cost someone the sign-in they
 * just completed - they are already authenticated by the time this runs, and
 * the code is still there to try again from the account page.
 *
 * @param {{ userId: string, email: string }} args
 * @returns {Promise<{ redeemed: boolean, reason?: string }>}
 */
export async function redeemPendingActivation({ userId, email }) {
  try {
    const intent = await takeActivationIntent(email);
    if (!intent) return { redeemed: false };

    const result = await redeemActivationCode({ codeId: intent.codeId, userId, email });

    // Only a genuine failure keeps the intent alive for a retry. 'exhausted',
    // 'revoked' and 'expired' are final answers, so the intent is cleared -
    // leaving it would re-attempt a dead code on every subsequent sign-in.
    if (!result.ok && result.reason === 'unavailable') {
      return { redeemed: false, reason: result.reason };
    }

    await clearActivationIntent(email);
    if (!result.ok) return { redeemed: false, reason: result.reason };

    await markProfileActivated(userId);
    return { redeemed: true };
  } catch (e) {
    console.error('[activationCodes] pending redemption threw:', e?.message ?? e);
    return { redeemed: false, reason: 'unavailable' };
  }
}

/**
 * Record that this account came in through a code rather than a purchase.
 *
 * Deliberately does NOT overwrite 'purchase'. Someone who bought the book and
 * also redeemed a comp code is a purchaser; downgrading that would misreport
 * what they are owed. sql/016 widened the constraint to allow 'signup', which
 * is the value this replaces.
 *
 * @param {string} userId
 */
async function markProfileActivated(userId) {
  if (!supabaseAdmin) return;
  const { error } = await supabaseAdmin
    .from('profiles')
    .update({ access_source: 'activation_code', updated_at: new Date().toISOString() })
    .eq('id', userId)
    .neq('access_source', 'purchase');
  if (error) console.error('[activationCodes] could not mark profile activated:', error.message);
}

/**
 * Mint a batch. Returns the plaintext codes, which is the only time they exist.
 *
 * The caller MUST show or store what comes back. There is no recovery path: the
 * database holds digests, and re-deriving a code from one is precisely what
 * SHA-256 is for. Losing the response means revoking those rows and minting
 * again.
 *
 * Collisions are handled rather than assumed away. At 60 bits the birthday bound
 * puts the first expected collision somewhere around a billion codes, so the
 * unique index on `code_hash` should never fire - but "should never" is what the
 * retry is for, and a bare 23505 would otherwise surface as an opaque insert
 * failure with no hint of its cause.
 *
 * @param {{ count?: number, label?: string, maxUses?: number,
 *           expiresAt?: string|null, createdBy?: string }} args
 * @returns {Promise<{ ok: boolean, codes?: string[], error?: string }>}
 */
export async function mintActivationCodes({
  count = 1,
  label = '',
  maxUses = 1,
  expiresAt = null,
  createdBy = '',
} = {}) {
  if (!supabaseAdmin) {
    return { ok: false, error: 'SUPABASE_SERVICE_KEY is not configured.' };
  }
  if (!Number.isInteger(count) || count < 1 || count > 500) {
    return { ok: false, error: 'count must be an integer between 1 and 500.' };
  }
  if (!Number.isInteger(maxUses) || maxUses < 1) {
    return { ok: false, error: 'maxUses must be an integer of at least 1.' };
  }

  const issued = [];
  for (let i = 0; i < count; i++) {
    let inserted = false;

    for (let attempt = 0; attempt < 3 && !inserted; attempt++) {
      const display = generateActivationCode();
      const canonical = normalizeActivationCode(display);
      const codeHash = await hashActivationCode(canonical);

      const { error } = await supabaseAdmin.from('activation_codes').insert({
        code_hash: codeHash,
        label: String(label).slice(0, 200),
        max_uses: maxUses,
        expires_at: expiresAt,
        created_by: String(createdBy).slice(0, 200),
      });

      if (!error) {
        issued.push(display);
        inserted = true;
      } else if (error.code === '23505') {
        console.warn('[activationCodes] code_hash collision, regenerating.');
      } else {
        console.error('[activationCodes] mint insert failed:', error.message);
        return { ok: false, error: error.message, codes: issued };
      }
    }

    if (!inserted) {
      return { ok: false, error: 'Could not generate a unique code after 3 attempts.', codes: issued };
    }
  }

  return { ok: true, codes: issued };
}
