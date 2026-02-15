import { redirect } from '@sveltejs/kit';

/**
 * Auth callback handler — processes the code from Supabase OAuth/magic link/signup confirmation.
 * Exchanges the code for a session and redirects to /profile.
 */
export async function GET(event) {
  const { url, locals } = event;
  const code = url.searchParams.get('code');
  const next = url.searchParams.get('next') ?? '/profile';

  if (code) {
    const { error } = await locals.supabase.auth.exchangeCodeForSession(code);
    if (!error) {
      throw redirect(303, next);
    }
  }

  // If something went wrong, redirect to login with error
  throw redirect(303, '/login');
}
