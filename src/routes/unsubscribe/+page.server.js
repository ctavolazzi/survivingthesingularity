import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {
  const token = url.searchParams.get('token') ?? '';
  const uuidRe = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

  if (!token || !uuidRe.test(token)) {
    return { status: 'invalid' };
  }

  if (!supabaseAdmin) {
    return { status: 'error' };
  }

  const { data, error } = await supabaseAdmin
    .from('waitlist')
    .select('email, unsubscribed_at')
    .eq('unsubscribe_token', token)
    .single();

  if (error || !data) {
    return { status: 'not_found' };
  }

  if (data.unsubscribed_at) {
    return { status: 'already_done', email: data.email };
  }

  return { status: 'pending', email: data.email, token };
}
