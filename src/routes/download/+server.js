import crypto from 'crypto';
import { SECRET_STRIPE_KEY_TEST, SECRET_STRIPE_KEY_LIVE } from '$env/static/private';
import path from 'path';
import fs from 'fs';

export async function GET({ url }) {
  const token = url.searchParams.get('token');
  const sessionId = getSessionIdFromToken(token);

  if (!sessionId) {
    return {
      status: 400,
      body: { error: 'Invalid or expired token' }
    };
  }

  // Path to the file
  const filePath = path.resolve('path/to/Surviving_the_Singularity.pdf');

  if (!fs.existsSync(filePath)) {
    return {
      status: 404,
      body: { error: 'File not found' }
    };
  }

  return {
    status: 200,
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': `attachment; filename="Surviving_the_Singularity.pdf"`
    },
    body: fs.createReadStream(filePath)
  };
}

// Helper function to get the sessionId from the token
function getSessionIdFromToken(token) {
  const sessions = {}; // Retrieve stored sessions or use a database
  for (const sessionId in sessions) {
    const validToken = crypto.createHash('sha256').update(sessionId + SECRET_STRIPE_KEY_TEST).digest('hex');
    if (token === validToken) {
      return sessionId;
    }
  }
  return null;
}