import { json } from '@sveltejs/kit';
import { sendChecklistEmail } from '$lib/server/email.js';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';

// In-memory rate limit: ip -> [timestamp, ...]
// Resets on server restart - intentional; keeps it dependency-free.
const rateMap = new Map();

function checkRate(ip) {
  const now = Date.now();
  const windowMs = 60 * 60 * 1000; // 1 hour
  const max = 3;
  const hits = (rateMap.get(ip) ?? []).filter(t => now - t < windowMs);
  if (hits.length >= max) return false;
  rateMap.set(ip, [...hits, now]);
  return true;
}

// HTML entity-encode all user-supplied text. Never inject raw user strings
// into the email HTML template.
function sanitize(value, maxLen = 1000) {
  if (typeof value !== 'string') return '';
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .trim()
    .slice(0, maxLen);
}

function isValidEmail(str) {
  if (typeof str !== 'string') return false;
  const t = str.trim();
  return t.length >= 5 && t.length <= 254 && /^[^\s@]{1,64}@[^\s@]{1,255}\.[^\s@]{2,}$/.test(t);
}

// Known-good category keys from the checklist data
const VALID_CATS = new Set(['foundation', 'infrastructure', 'autonomy', 'network']);

export async function POST({ request, url, getClientAddress }) {
  // Origin check - reject cross-site POSTs.
  const origin = request.headers.get('origin');
  if (origin && origin !== url.origin) {
    return json({ error: 'Bad request.' }, { status: 403 });
  }

  // Content-type guard.
  const contentType = request.headers.get('content-type') ?? '';
  if (!contentType.includes('application/json')) {
    return json({ error: 'Bad request.' }, { status: 400 });
  }

  const ip = getClientAddress();

  if (!checkRate(ip)) {
    return json({ error: 'Too many requests. Try again in an hour.' }, { status: 429 });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid request.' }, { status: 400 });
  }

  const { email, honeypot, answers } = body ?? {};

  // Honeypot: silently succeed so bots think they won
  if (honeypot) return json({ ok: true });

  if (!isValidEmail(email)) {
    return json({ error: 'Please enter a valid email address.' }, { status: 400 });
  }

  if (!Array.isArray(answers) || answers.length === 0 || answers.length > 12) {
    return json({ error: 'Invalid data.' }, { status: 400 });
  }

  // Only send to addresses already on the waitlist - the checklist page can
  // only obtain an email through EmailGate, which inserts it there first. A
  // direct POST with a stranger's address (email-bombing that burns Resend
  // quota and sender reputation) gets the same silent fake-success as the
  // honeypot. Fails open on infra errors so a Supabase blip never blocks a
  // real visitor's delivery.
  if (supabaseAdmin) {
    const { data: row, error: lookupErr } = await supabaseAdmin
      .from('waitlist')
      .select('email')
      .eq('email', email.trim().toLowerCase())
      .maybeSingle();
    if (lookupErr) {
      console.warn('[checklist-email] waitlist lookup failed, failing open:', lookupErr.message);
    } else if (!row) {
      return json({ ok: true });
    }
  }

  const clean = answers.map(item => ({
    n:       sanitize(String(item?.n ?? ''), 10),
    title:   sanitize(String(item?.title ?? ''), 200),
    cat:     VALID_CATS.has(item?.cat) ? item.cat : 'foundation',
    body:    sanitize(String(item?.body ?? ''), 2000),
    action:  sanitize(String(item?.action ?? ''), 500),
    cost:    sanitize(String(item?.cost ?? ''), 50),
    effort:  sanitize(String(item?.effort ?? ''), 50),
    checked: item?.checked === true,
    notes:   sanitize(String(item?.notes ?? ''), 1000),
  }));

  const result = await sendChecklistEmail({ to: email.trim(), answers: clean });

  if (result?.error) {
    console.error('[checklist-email] send failed:', result.error);
    return json({ error: 'Failed to send. Please try again.' }, { status: 500 });
  }

  return json({ ok: true });
}
