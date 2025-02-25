import { json } from '@sveltejs/kit';
import { supabase } from '$lib/server/supabaseAdmin';

export async function POST({ request }) {
  try {
    const { email, marketingOptIn } = await request.json();

    // Server-side validation
    if (!email || !/^\S+@\S+\.\S+$/.test(email)) {
      return json({ success: false, error: 'Invalid email format' }, { status: 400 });
    }

    const { error } = await supabase
      .from('newsletter_subscribers')
      .insert([{
        email: email.trim(),
        marketing_opt_in: marketingOptIn
      }]);

    if (error) {
      if (error.code === '23505') {
        return json({ success: false, error: 'This email is already subscribed' }, { status: 409 });
      }
      console.error('Database error:', error);
      throw error;
    }

    return json({ success: true });
  } catch (error) {
    console.error('Newsletter subscription error:', error);
    return json({ success: false, error: 'Server error processing subscription' }, { status: 500 });
  }
}