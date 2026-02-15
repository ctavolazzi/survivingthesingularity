/**
 * Supabase Client Factory — SSR-compatible
 * Uses @supabase/ssr for proper cookie-based auth in SvelteKit
 */
import { createBrowserClient, createServerClient, isBrowser } from '@supabase/ssr';
import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';

/**
 * Create a Supabase client for the browser.
 * Automatically manages auth tokens via cookies.
 */
export function createSupabaseBrowserClient() {
  return createBrowserClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY);
}

/**
 * Create a Supabase client for the server (hooks, +page.server.js, +server.js).
 * Reads/writes auth cookies via the event object.
 */
export function createSupabaseServerClient(event) {
  return createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
    cookies: {
      getAll() {
        return event.cookies.getAll();
      },
      setAll(cookiesToSet) {
        cookiesToSet.forEach(({ name, value, options }) =>
          event.cookies.set(name, value, {
            ...options,
            path: '/',
            httpOnly: true,
            secure: true,
            sameSite: 'lax',
          })
        );
      },
    },
  });
}
