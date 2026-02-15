/**
 * Server hooks — handles Supabase auth session management.
 * Gracefully degrades if Supabase is not configured (no .env credentials).
 */

let supabaseConfigured = false;

try {
  // Try to import env vars at module level to check if they exist
  const { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } = await import('$env/static/public');
  supabaseConfigured = !!(PUBLIC_SUPABASE_URL && PUBLIC_SUPABASE_ANON_KEY
    && PUBLIC_SUPABASE_URL !== 'your_supabase_url'
    && PUBLIC_SUPABASE_ANON_KEY !== 'your_supabase_anon_key');
} catch {
  supabaseConfigured = false;
}

export async function handle({ event, resolve }) {
  // Fix for "[object Object]" navigation errors
  if (event.url.pathname.includes('[object%20Object]') || event.url.pathname.includes('[object Object]')) {
    return new Response('Redirect', {
      status: 302,
      headers: { Location: '/' }
    });
  }

  if (supabaseConfigured) {
    try {
      const { createSupabaseServerClient } = await import('$lib/supabase.js');
      event.locals.supabase = createSupabaseServerClient(event);

      event.locals.safeGetSession = async () => {
        const {
          data: { session },
        } = await event.locals.supabase.auth.getSession();

        if (!session) {
          return { session: null, user: null };
        }

        const {
          data: { user },
          error,
        } = await event.locals.supabase.auth.getUser();

        if (error) {
          return { session: null, user: null };
        }

        return { session, user };
      };
    } catch {
      // Supabase init failed — continue without auth
      event.locals.safeGetSession = async () => ({ session: null, user: null });
    }
  } else {
    // No Supabase configured — provide stub
    event.locals.safeGetSession = async () => ({ session: null, user: null });
  }

  return resolve(event, {
    filterSerializedResponseHeaders(name) {
      return name === 'content-range' || name === 'x-supabase-api-version';
    },
  });
}
