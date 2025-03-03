import { json } from '@sveltejs/kit';
import { supabase } from '$lib/utils/supabaseClient';

export async function POST({ request, locals }) {
  return new Response(
    JSON.stringify({
      success: false,
      message: "This feature is no longer available. The data warehouse has moved to a curated model with administrator-only submissions."
    }),
    {
      status: 403,
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );
}

// Original code commented out for reference
/*
export async function POST({ request, locals }) {
  const { supabase } = locals;
  const data = await request.json();

  try {
    const { error } = await supabase
      .from('research_links')
      .insert([data]);

    if (error) {
      console.error('Error inserting link:', error);
      return new Response(JSON.stringify({ success: false, error: error.message }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json'
        }
      });
    }

    return new Response(JSON.stringify({ success: true }), {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (err) {
    console.error('Server error:', err);
    return new Response(JSON.stringify({ success: false, error: 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
}
*/