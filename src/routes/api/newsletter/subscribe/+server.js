import { json } from '@sveltejs/kit';
import { supabase } from '$lib/server/supabaseAdmin';

export async function POST({ request, getClientAddress }) {
  try {
    const { email, marketingOptIn } = await request.json();
    const clientIp = getClientAddress();
    const userAgent = request.headers.get('user-agent') || '';
    const referrer = request.headers.get('referer') || '';

    // Server-side validation
    if (!email || !/^\S+@\S+\.\S+$/.test(email)) {
      return json({ success: false, error: 'Invalid email format' }, { status: 400 });
    }

    const { error } = await supabase
      .from('sts_newsletter_subscribers')
      .insert([{
        email: email.trim(),
        marketing_opt_in: marketingOptIn,
        source: 'website',
        ip_address: clientIp,
        user_agent: userAgent,
        referrer: referrer
      }]);

    if (error) {
      if (error.code === '23505') {
        return json({ success: false, error: 'This email is already subscribed' }, { status: 409 });
      }
      console.error('Database error:', error);
      throw error;
    }

    // Successfully subscribed
    return json({
      success: true,
      message: 'Thank you for subscribing to the Surviving the Singularity newsletter!'
    });
  } catch (error) {
    console.error('Newsletter subscription error:', error);
    return json({
      success: false,
      error: 'Server error processing subscription. Please try again later.'
    }, { status: 500 });
  }
}