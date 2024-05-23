// src/routes/api/profiles.js
import { supabase } from '$lib/supabaseClient';

export async function get() {
  const { data, error } = await supabase
    .from('profiles')
    .select(`
      id,
      username,
      full_name,
      bio,
      avatar_url
    `);

  if (error) {
    console.error('Error fetching profiles:', error);
    return {
      status: 500,
      body: { error: 'Failed to fetch profiles' }
    };
  }

  return {
    status: 200,
    body: { profiles: data }
  };
}