import { withSupabase } from '@supabase/server';
import { SUPABASE_URL, SUPABASE_SECRET_KEY, SUPABASE_PUBLISHABLE_KEY } from '$env/static/private';

const supabaseEnv = {
  url: SUPABASE_URL,
  secretKeys:      { default: SUPABASE_SECRET_KEY },
  publishableKeys: { default: SUPABASE_PUBLISHABLE_KEY },
};

const countHandler = withSupabase({ auth: 'none', env: supabaseEnv }, async (_req, ctx) => {
  const { data, error } = await ctx.supabaseAdmin
    .from('preorder_counts')
    .select('edition_type, claimed');

  if (error) {
    console.error('[preorder-count]', error.message);
    return Response.json({ authors: 0, regular: 0 });
  }

  const result = { authors: 0, regular: 0 };
  for (const row of data ?? []) {
    if (row.edition_type === 'authors') result.authors = Number(row.claimed);
    if (row.edition_type === 'regular')  result.regular  = Number(row.claimed);
  }

  return new Response(JSON.stringify(result), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=30, stale-while-revalidate=60',
    },
  });
});

/** @type {import('./$types').RequestHandler} */
export async function GET(event) {
  return countHandler(event.request);
}
