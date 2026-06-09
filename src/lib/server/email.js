import { env } from '$env/dynamic/private';
import { Resend } from 'resend';

// Dynamic env so a missing key never breaks the build. If RESEND_API_KEY is
// unset, every send becomes a logged no-op and signups still succeed.
const apiKey = env.RESEND_API_KEY;
const from = env.EMAIL_FROM || 'Surviving the Singularity <onboarding@resend.dev>';

const resend = apiKey ? new Resend(apiKey) : null;

/**
 * Source-aware welcome copy. The checklist is delivered on-site (the email is
 * a confirmation + nudge back), so its copy differs from the book waitlist.
 */
function buildWelcome(source) {
  if (source === 'checklist') {
    return {
      subject: 'Your Readiness Checklist is unlocked',
      heading: "You're in. The full checklist is open.",
      body:
        'All 12 moves are unlocked on the site. Work through them at your own pace — ' +
        'start with the three you have been avoiding. When you want the deeper strategy, ' +
        'the full Blueprint is there too.',
      cta: { label: 'Open the checklist', url: 'https://survivingthesingularity.com/checklist' },
    };
  }
  return {
    subject: "You're on the list",
    heading: "You're on the list.",
    body:
      "You'll be the first to know when the book launches, plus the field notes published " +
      'along the way. No spam, no noise. Unsubscribe anytime.',
    cta: { label: 'Read the Blueprint', url: 'https://survivingthesingularity.com/blueprint' },
  };
}

function renderHtml({ heading, body, cta }) {
  return `<!doctype html><html><body style="margin:0;background:#020617;font-family:Inter,system-ui,sans-serif;color:#e2e8f0;">
  <div style="max-width:520px;margin:0 auto;padding:40px 24px;">
    <p style="font-size:13px;letter-spacing:0.15em;text-transform:uppercase;color:#f59e0b;font-weight:700;margin:0 0 16px;">Surviving the Singularity</p>
    <h1 style="font-size:24px;color:#f1f5f9;margin:0 0 16px;">${heading}</h1>
    <p style="font-size:15px;line-height:1.7;color:#94a3b8;margin:0 0 28px;">${body}</p>
    <a href="${cta.url}" style="display:inline-block;background:#f59e0b;color:#0f172a;font-weight:700;font-size:14px;text-decoration:none;padding:12px 22px;border-radius:8px;">${cta.label}</a>
    <p style="font-size:12px;color:#475569;margin:36px 0 0;">You received this because you signed up at survivingthesingularity.com. Reply to unsubscribe.</p>
  </div></body></html>`;
}

/**
 * Fire a welcome/confirmation email. Safe to call unconditionally:
 * - no API key  -> logs a warning, returns { skipped: true }
 * - send errors -> caught by caller; must never block signup.
 *
 * @param {{ to: string, source?: string }} args
 */
export async function sendWelcomeEmail({ to, source = 'homepage' }) {
  if (!resend) {
    console.warn('[email] RESEND_API_KEY unset — skipping welcome email to', to);
    return { skipped: true };
  }
  const copy = buildWelcome(source);
  const { error } = await resend.emails.send({
    from,
    to,
    subject: copy.subject,
    html: renderHtml(copy),
  });
  if (error) {
    console.error('[email] welcome send failed:', error.message ?? error);
    return { error };
  }
  return { ok: true };
}
