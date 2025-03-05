import { json } from '@sveltejs/kit';

export async function POST({ request, fetch }) {
  try {
    // Parse the request body
    const formData = await request.json();

    // Validate required fields
    if (!formData.email || !formData.message) {
      return json({ success: false, error: 'Missing required fields' }, { status: 400 });
    }

    // Add the honeypot field if not present
    if (!formData._gotcha) {
      formData._gotcha = '';
    }

    // Forward the submission to Formspree
    const response = await fetch('https://formspree.io/f/xgvawenl', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(formData)
    });

    const responseData = await response.json();

    if (!response.ok) {
      throw new Error(responseData.error || 'Failed to submit form');
    }

    return json({
      success: true,
      message: 'Your message has been received. We will get back to you soon.'
    });
  } catch (error) {
    console.error('Server error:', error);
    return json({
      success: false,
      error: 'Failed to send message. Please try again later.'
    }, { status: 500 });
  }
}