/**
 * Is this Supabase configuration usable? One answer, shared by both clients.
 *
 * WHY THIS EXISTS
 *
 * supabaseAdmin.js already intended to degrade rather than crash - its header
 * says "a missing key never breaks builds; the client is simply null and
 * callers degrade gracefully". It checked that the values were present and that
 * the key was not the literal string 'placeholder'. It did not check that the
 * URL was a URL.
 *
 * That gap is not theoretical. Observed 2026-08-01 with a .env containing the
 * unedited example values:
 *
 *   SUPABASE_URL=https://<your-project-ref>.supabase.co
 *
 *   GET /          -> 500
 *   GET /policies  -> 500
 *   GET /signup    -> 500
 *   Error: Invalid supabaseUrl: Provided URL is malformed.
 *
 * createClient() throws on a malformed URL, at module scope. Every route that
 * transitively imports the module dies with it, including pages that never
 * touch Supabase, because hooks.server.js runs on every request. One typo in a
 * Cloudflare environment variable takes the whole site down, and the failure
 * mode is a blank 500 rather than anything that names the cause.
 *
 * The fix is to make the existing intent true: validate before constructing,
 * and let a bad value produce a null client - which every caller in this
 * codebase already handles, because they all had to handle the unset case.
 *
 * Kept in its own module rather than duplicated into both clients for the same
 * reason as sameOrigin.js and validEmail.js: the copies are the bug.
 */

/**
 * Values people leave behind when they copy .env.example without editing it.
 * `<` catches the angle-bracket style the runbook hands out; the rest are the
 * conventional stand-ins.
 */
function looksLikePlaceholder(value) {
  const v = value.toLowerCase();
  return (
    v.includes('<') ||
    v.includes('your_') ||
    v.includes('your-') ||
    v.startsWith('placeholder')
  );
}

/**
 * @param {string|undefined} url
 * @returns {boolean} true when this could actually be a Supabase project URL
 */
export function isUsableSupabaseUrl(url) {
  if (!url || looksLikePlaceholder(url)) return false;
  try {
    const parsed = new URL(url);
    // createClient accepts anything URL-shaped, but a non-http(s) scheme here
    // means the value is wrong in a way worth refusing rather than dialling.
    return parsed.protocol === 'https:' || parsed.protocol === 'http:';
  } catch {
    return false;
  }
}

/**
 * @param {string|undefined} key
 * @returns {boolean}
 */
export function isUsableSupabaseKey(key) {
  return Boolean(key) && !looksLikePlaceholder(key);
}

/**
 * Both halves, plus a one-line reason when the answer is no.
 *
 * The reason is logged rather than thrown. A misconfigured deployment should
 * say what is wrong in the server log and keep serving the pages that do not
 * need a database, which is nearly all of them.
 *
 * @param {string|undefined} url
 * @param {string|undefined} key
 * @param {string} label which client is asking, for the log line
 * @returns {boolean}
 */
export function supabaseConfigured(url, key, label) {
  if (!url && !key) return false; // Unset is the normal local state. Silent.

  if (!isUsableSupabaseUrl(url)) {
    console.error(
      `[${label}] SUPABASE_URL is missing or malformed; running without it. ` +
        `Expected https://<ref>.supabase.co - check the value is not still the .env.example placeholder.`
    );
    return false;
  }
  if (!isUsableSupabaseKey(key)) {
    console.error(`[${label}] key is missing or still a placeholder; running without it.`);
    return false;
  }
  return true;
}
