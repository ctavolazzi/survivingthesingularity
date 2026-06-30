import { env } from '$env/dynamic/private';
import { Resend } from 'resend';

// Dynamic env so a missing key never breaks the build. If RESEND_API_KEY is
// unset, every send becomes a logged no-op and signups still succeed.
const apiKey = env.RESEND_API_KEY;
const from = env.EMAIL_FROM || 'Surviving the Singularity <onboarding@resend.dev>';

const resend = apiKey ? new Resend(apiKey) : null;

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

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
        'All 12 moves are unlocked on the site. Work through them at your own pace. ' +
        'Start with the three you have been avoiding. When you want the deeper strategy, ' +
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
    cta: { label: 'Read the Book', url: 'https://survivingthesingularity.com/book' },
  };
}

function renderHtml({ heading, body, cta, unsubscribeUrl }) {
  const footerUnsubscribe = unsubscribeUrl
    ? `<a href="${unsubscribeUrl}" style="color:#475569;text-decoration:underline;">Unsubscribe</a>`
    : 'Reply to unsubscribe';
  return `<!doctype html><html><body style="margin:0;background:#020617;font-family:Inter,system-ui,sans-serif;color:#e2e8f0;">
  <div style="max-width:520px;margin:0 auto;padding:40px 24px;">
    <p style="font-size:13px;letter-spacing:0.15em;text-transform:uppercase;color:#f59e0b;font-weight:700;margin:0 0 16px;">Surviving the Singularity</p>
    <h1 style="font-size:24px;color:#f1f5f9;margin:0 0 16px;">${heading}</h1>
    <p style="font-size:15px;line-height:1.7;color:#94a3b8;margin:0 0 28px;">${body}</p>
    <a href="${cta.url}" style="display:inline-block;background:#f59e0b;color:#0f172a;font-weight:700;font-size:14px;text-decoration:none;padding:12px 22px;border-radius:8px;">${cta.label}</a>
    <p style="font-size:12px;color:#475569;margin:36px 0 0;">You received this because you signed up at survivingthesingularity.com. ${footerUnsubscribe}.</p>
  </div></body></html>`;
}

/**
 * Confirm a preorder to the customer.
 * Non-blocking: caller should not await in a way that blocks the response.
 *
 * @param {{ name: string, email: string, edition_type: string, copy_number?: number|null }} args
 */
export async function sendPreorderConfirmation({ name, email, edition_type, copy_number }) {
  if (!resend) return { skipped: true };
  const isAuthors = edition_type === 'authors';
  const safeName = name ? escapeHtml(name.slice(0, 120)) : '';
  const greeting = safeName ? `Hi ${safeName},` : 'Hi,';

  const heading = isAuthors
    ? `You're copy #${copy_number} of 100.`
    : "You're on the preorder list.";

  const body = isAuthors
    ? `${greeting} Your Author's Edition preorder is confirmed. Copy #${copy_number} of 100 is reserved for you. ` +
      `Each Author's Edition is hand-bound and signed. No payment is collected now. You'll hear from us before the book ships in August 2026.`
    : `${greeting} Your preorder is confirmed. You'll get first access when the book launches in August 2026, ` +
      `available here on the site and on Amazon. No payment collected now. We'll reach out when it's ready.`;

  const cta = isAuthors
    ? { label: 'See the launch plan', url: 'https://survivingthesingularity.com/launch' }
    : { label: 'Learn more', url: 'https://survivingthesingularity.com/launch' };

  const subject = isAuthors
    ? `Author's Edition confirmed: copy #${copy_number}`
    : 'Preorder confirmed: Surviving the Singularity';

  const { error } = await resend.emails.send({
    from,
    to: email,
    subject,
    html: renderHtml({ heading, body, cta }),
  });
  if (error) console.error('[email] preorder confirmation failed:', error.message ?? error);
  return error ? { error } : { ok: true };
}

/**
 * Notify the admin inbox when a preorder lands.
 * Non-blocking: caller should not await in a way that blocks the response.
 *
 * @param {{ name: string, email: string, edition_type: string, copy_number?: number|null }} args
 */
export async function sendAdminPreorderAlert({ name, email, edition_type, copy_number }) {
  if (!resend) return { skipped: true };
  const isAuthors = edition_type === 'authors';
  const subject = isAuthors
    ? `[STS] Author's Edition preorder #${copy_number}: ${name}`
    : `[STS] Regular edition preorder: ${name}`;
  const body = `Name: ${name}\nEmail: ${email}\nEdition: ${edition_type}${isAuthors && copy_number ? `\nCopy: #${copy_number} / 100` : ''}`;
  const { error } = await resend.emails.send({
    from,
    to: 'admin@johnnyautoseed.com',
    subject,
    text: body,
  });
  if (error) console.error('[email] admin preorder alert failed:', error.message ?? error);
  return error ? { error } : { ok: true };
}

const CAT_COLORS = {
  foundation:     '#f59e0b',
  infrastructure: '#3b82f6',
  autonomy:       '#10b981',
  network:        '#a78bfa',
};
const CAT_LABELS = {
  foundation:     'Foundation',
  infrastructure: 'Infrastructure',
  autonomy:       'Autonomy',
  network:        'Network',
};

/**
 * Send the user their completed checklist + any notes they added.
 * All `answers` must already be sanitized by the caller (API route).
 *
 * @param {{ to: string, answers: Array<{n,title,cat,body,action,cost,effort,checked,notes}> }} args
 */
export async function sendChecklistEmail({ to, answers }) {
  if (!resend) {
    console.warn('[email] RESEND_API_KEY unset — skipping checklist email to', to);
    return { skipped: true };
  }

  const checkedCount = answers.filter(a => a.checked).length;
  const total = answers.length;

  const heading =
    checkedCount === total ? `You've completed all ${total} steps.` :
    checkedCount === 0     ? 'Your Singularity Readiness Checklist' :
                             `${checkedCount}/${total} steps checked — keep going.`;

  const intro = checkedCount > 0
    ? `Here's your checklist with your notes. ${total - checkedCount} step${total - checkedCount !== 1 ? 's' : ''} still to do.`
    : 'Your full Singularity Readiness Checklist — work through these at your own pace.';

  const itemsHtml = answers.map(item => {
    const color = CAT_COLORS[item.cat] ?? '#f59e0b';
    const label = CAT_LABELS[item.cat] ?? item.cat;

    const checkBox = item.checked
      ? `<span style="display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;background:#f59e0b;border-radius:50%;flex-shrink:0;">
           <svg width="10" height="8" viewBox="0 0 10 8" fill="none" xmlns="http://www.w3.org/2000/svg">
             <path d="M1 4l2.5 2.5L9 1" stroke="#0a0a0a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
           </svg>
         </span>`
      : `<span style="display:inline-block;width:20px;height:20px;border-radius:50%;border:1.5px solid #334155;flex-shrink:0;"></span>`;

    const notesBlock = item.notes
      ? `<div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:6px;padding:10px 14px;margin-top:10px;">
           <p style="font-family:monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:#f59e0b;margin:0 0 5px;">Your notes</p>
           <p style="font-size:13px;color:#e2e8f0;line-height:1.65;margin:0;white-space:pre-wrap;">${item.notes}</p>
         </div>`
      : '';

    const titleStyle = item.checked
      ? 'font-size:14px;font-weight:700;color:#64748b;line-height:1.3;text-decoration:line-through;'
      : 'font-size:14px;font-weight:700;color:#f1f5f9;line-height:1.3;';

    return `
<div style="margin:10px 0;padding:16px;background:#0f172a;border-left:3px solid ${color};border-radius:8px;">
  <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;">
    ${checkBox}
    <div style="flex:1;min-width:0;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;flex-wrap:wrap;">
        <span style="font-family:monospace;font-size:11px;font-weight:700;color:${color};">${item.n}</span>
        <span style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:${color};background:rgba(255,255,255,0.06);padding:2px 7px;border-radius:4px;">${label}</span>
        <span style="font-family:monospace;font-size:10px;color:#475569;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);padding:2px 6px;border-radius:4px;">${item.cost}</span>
      </div>
      <p style="${titleStyle}">${item.title}</p>
    </div>
  </div>
  <p style="font-size:13px;color:#94a3b8;line-height:1.65;margin:0 0 10px;">${item.body}</p>
  <div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.12);border-radius:6px;padding:10px 14px;">
    <p style="font-family:monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:#f59e0b;margin:0 0 4px;">First action</p>
    <p style="font-size:13px;color:#e2e8f0;line-height:1.5;margin:0;">${item.action}</p>
  </div>
  ${notesBlock}
</div>`;
  }).join('\n');

  const subject = checkedCount > 0
    ? `Your checklist: ${checkedCount}/${total} steps`
    : 'Your Singularity Readiness Checklist';

  const html = `<!doctype html><html><body style="margin:0;background:#020617;font-family:Inter,system-ui,sans-serif;color:#e2e8f0;">
<div style="max-width:600px;margin:0 auto;padding:40px 24px;">
  <p style="font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:#f59e0b;font-weight:700;margin:0 0 20px;">Surviving the Singularity</p>
  <h1 style="font-size:22px;color:#f1f5f9;margin:0 0 10px;line-height:1.3;">${heading}</h1>
  <p style="font-size:14px;line-height:1.7;color:#94a3b8;margin:0 0 28px;">${intro}</p>
  ${itemsHtml}
  <div style="margin:32px 0;padding:20px 24px;background:rgba(245,158,11,0.05);border:1px solid rgba(245,158,11,0.2);border-radius:12px;">
    <p style="font-size:13px;color:#94a3b8;margin:0 0 14px;line-height:1.5;">Want the full strategy behind each step? The book expands every area of this checklist.</p>
    <a href="https://survivingthesingularity.com/book" style="display:inline-block;background:#f59e0b;color:#0f172a;font-weight:700;font-size:13px;text-decoration:none;padding:11px 20px;border-radius:8px;">Read the Book →</a>
  </div>
  <p style="font-size:11px;color:#334155;margin:32px 0 0;">You requested this at survivingthesingularity.com. Reply to unsubscribe.</p>
</div>
</body></html>`;

  const { error } = await resend.emails.send({ from, to, subject, html });
  if (error) {
    console.error('[email] checklist send failed:', error.message ?? error);
    return { error };
  }
  return { ok: true };
}

/**
 * Send the early-access research bundle download link after payment.
 * `downloadUrl` is a time-limited signed URL from Supabase Storage (or a
 * static URL in mock mode). The link is valid for 7 days.
 *
 * @param {{ to: string, downloadUrl: string, sessionId: string }} args
 */
export async function sendDownloadEmail({ to, downloadUrl, sessionId }) {
  if (!resend) {
    console.warn('[email] RESEND_API_KEY unset — skipping download email to', to);
    return { skipped: true };
  }

  const subject = 'Your research bundle is ready';
  const heading = 'Your download is ready.';
  const body =
    'Thank you for supporting Surviving the Singularity. ' +
    'The research bundle includes the PDFs, papers, images, and source documents behind the book. ' +
    'The link below is valid for 7 days. After that, reply to this email and we will send a fresh one.';
  const cta = { label: 'Download your bundle', url: downloadUrl };

  const html = `<!doctype html><html><body style="margin:0;background:#020617;font-family:Inter,system-ui,sans-serif;color:#e2e8f0;">
  <div style="max-width:520px;margin:0 auto;padding:40px 24px;">
    <p style="font-size:13px;letter-spacing:0.15em;text-transform:uppercase;color:#f59e0b;font-weight:700;margin:0 0 16px;">Surviving the Singularity</p>
    <h1 style="font-size:24px;color:#f1f5f9;margin:0 0 16px;">${heading}</h1>
    <p style="font-size:15px;line-height:1.7;color:#94a3b8;margin:0 0 28px;">${body}</p>
    <a href="${downloadUrl}" style="display:inline-block;background:#f59e0b;color:#0f172a;font-weight:700;font-size:14px;text-decoration:none;padding:14px 24px;border-radius:8px;margin-bottom:24px;">Download your bundle</a>
    <div style="background:rgba(245,158,11,0.05);border:1px solid rgba(245,158,11,0.15);border-radius:10px;padding:16px 20px;margin-top:8px;">
      <p style="font-size:13px;color:#64748b;margin:0 0 10px;">Also included in your early access:</p>
      <p style="font-size:13px;color:#94a3b8;margin:0;line-height:1.7;">
        The book: <a href="https://survivingthesingularity.com/book" style="color:#f59e0b;">survivingthesingularity.com/book</a><br>
        Readiness checklist: <a href="https://survivingthesingularity.com/checklist" style="color:#f59e0b;">survivingthesingularity.com/checklist</a><br>
        Research signals: <a href="https://survivingthesingularity.com/signals" style="color:#f59e0b;">survivingthesingularity.com/signals</a>
      </p>
    </div>
    <p style="font-size:11px;color:#334155;margin:36px 0 0;">Order ref: ${sessionId.slice(0, 24)}... · survivingthesingularity.com · Reply to this email for support.</p>
  </div></body></html>`;

  const { error } = await resend.emails.send({ from, to, subject, html });
  if (error) {
    console.error('[email] download email failed:', error.message ?? error);
    return { error };
  }
  return { ok: true };
}

/**
 * Fire a welcome/confirmation email. Safe to call unconditionally:
 * - no API key  -> logs a warning, returns { skipped: true }
 * - send errors -> caught by caller; must never block signup.
 *
 * @param {{ to: string, source?: string, unsubscribeToken?: string }} args
 */
export async function sendWelcomeEmail({ to, source = 'homepage', unsubscribeToken }) {
  if (!resend) {
    console.warn('[email] RESEND_API_KEY unset — skipping welcome email to', to);
    return { skipped: true };
  }
  const baseUrl = env.PUBLIC_BASE_URL || 'https://survivingthesingularity.com';
  const unsubscribeUrl = unsubscribeToken
    ? `${baseUrl}/unsubscribe?token=${unsubscribeToken}`
    : null;
  const copy = buildWelcome(source);
  const { error } = await resend.emails.send({
    from,
    to,
    subject: copy.subject,
    html: renderHtml({ ...copy, unsubscribeUrl }),
  });
  if (error) {
    console.error('[email] welcome send failed:', error.message ?? error);
    return { error };
  }
  return { ok: true };
}
