import { getWaitlistCount } from '$lib/server/supabaseAdmin.js';

// Only surface a signup count once it's genuinely impressive. Below this it
// reads as "nobody signed up" and hurts conversion, so we hide it entirely.
const SOCIAL_PROOF_THRESHOLD = 100;

export async function load() {
  const count = await getWaitlistCount();
  return {
    items: [],
    // Display-ready: a number to show, or null to hide the proof entirely.
    signupCount: typeof count === 'number' && count >= SOCIAL_PROOF_THRESHOLD ? count : null,
  };
}
