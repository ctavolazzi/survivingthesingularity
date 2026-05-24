/** @type {import('./$types').LayoutServerLoad} */
export async function load() {
  // No auth on this site. Returning stub user/session so layout components
  // that destructure data.user don't blow up during the transition.
  return { session: null, user: null };
}
