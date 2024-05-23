// src/lib/userStore.js
import { writable } from 'svelte/store';
import { supabase } from '$lib/supabaseClient';

export const user = writable(null);

export async function fetchUser() {
  const { data, error } = await supabase.auth.getUser();
  if (error) {
    console.error('Error fetching user:', error);
    user.set(null);
  } else {
    const { id, email } = data.user;

    // Fetch additional profile data
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('username, full_name, bio, avatar_url')
      .eq('id', id)
      .single();

    if (profileError) {
      console.error('Error fetching profile:', profileError);
      user.set({ id, email });
    } else {
      user.set({ id, email, ...profile });
    }
  }
}
