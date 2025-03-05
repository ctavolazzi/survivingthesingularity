import { json } from '@sveltejs/kit';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

export async function POST({ request }) {
  try {
    // Parse the request body
    const { name, email, subject, message } = await request.json();

    // Validate required fields
    if (!name || !email || !message) {
      return json({ success: false, error: 'Missing required fields' }, { status: 400 });
    }

    // Format the email subject and body
    const emailSubject = subject ? `[Contact Form] ${subject}` : '[Contact Form] New message from website';
    const emailBody = `
From: ${name} <${email}>
Subject: ${subject || 'N/A'}

Message:
${message}
    `;

    // Send email using the mail command
    // This works because we confirmed the mail command works from the terminal
    await execPromise(`echo "${emailBody}" | mail -s "${emailSubject}" info@survivingthesingularity.com`);

    return json({ success: true });
  } catch (error) {
    console.error('Server error:', error);
    return json({ success: false, error: 'Failed to send message. Please try again later.' }, { status: 500 });
  }
}