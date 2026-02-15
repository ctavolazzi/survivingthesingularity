/** @type {import('./$types').LayoutServerLoad} */
export async function load({ locals }) {
  // Safely get session — returns null if no Supabase or no auth
  try {
    const { session, user } = await locals.safeGetSession();
    return {
      session,
      user,
    };
  } catch {
    // Supabase not configured yet — return null session
    return {
      session: null,
      user: null,
    };
  }
}
