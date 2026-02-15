/** @type {import('./$types').PageServerLoad} */
export async function load({ locals }) {
  try {
    const { session, user } = await locals.safeGetSession();
    return { user: user || null };
  } catch {
    return { user: null };
  }
}
