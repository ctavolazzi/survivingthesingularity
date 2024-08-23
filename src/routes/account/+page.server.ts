import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals: { supabase, safeGetSession } }) => {
  const { session } = await safeGetSession();
  if (!session) {
    throw redirect(303, '/');
  }

  const { data: profile } = await supabase
    .from('users')
    .select(`first_name, last_name, website, avatar_url`)
    .eq('id', session.user.id)
    .single();

  return { session, profile };
};

export const actions: Actions = {
  update: async ({ request, locals: { supabase, safeGetSession } }) => {
    const formData = await request.formData();
    const fullName = formData.get('fullName') as string;
    const username = formData.get('username') as string;
    const website = formData.get('website') as string;
    const avatarUrl = formData.get('avatarUrl') as string;
    const bio = formData.get('bio') as string;
    const location = formData.get('location') as string;
    const twitter = formData.get('twitter') as string;
    const github = formData.get('github') as string;

    const { session } = await safeGetSession();

    const { error } = await supabase.from('profiles').upsert({
      id: session?.user.id,
      full_name: fullName,
      username,
      website,
      avatar_url: avatarUrl,
      bio,
      location,
      social_links: { twitter, github },
      updated_at: new Date(),
    });

    if (error) {
      return fail(500, {
        fullName,
        username,
        website,
        avatarUrl,
        bio,
        location,
        twitter,
        github,
      });
    }

    return {
      fullName,
      username,
      website,
      avatarUrl,
      bio,
      location,
      twitter,
      github,
    };
  },
  signout: async ({ locals: { supabase } }) => {
    await supabase.auth.signOut();
    throw redirect(303, '/');
  },
};