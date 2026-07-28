import { env } from '$env/dynamic/private';
import { Resend } from 'resend';
import { BOOK_ACCESS_PASSWORD } from '$lib/bookAccessCode.js';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';

// Dynamic env so a missing key never breaks the build. If RESEND_API_KEY is
// unset, every send becomes a logged no-op and signups still succeed.
const apiKey = env.RESEND_API_KEY;
const from = env.EMAIL_FROM || 'Surviving the Singularity <onboarding@resend.dev>';

const resend = apiKey ? new Resend(apiKey) : null;

/**
 * Send through Resend and record the attempt in email_deliveries.
 *
 * Every send used to do `const { error } = await resend.emails.send(...)`,
 * which threw away `data.id` - the one handle that lets a delivery outcome be
 * matched back to the send. A bounced confirmation and a delivered one left
 * the database in identical states, so "did this customer actually receive
 * their bundle link?" could only be answered from Resend's dashboard, which
 * is a third party with ~30 day retention. For a table whose whole job is
 * redundancy against Stripe, that is the wrong shape.
 *
 * The ledger write is deliberately best-effort and never throws: failing to
 * RECORD an email must not stop the email, and must not take down fulfillment.
 * A missing ledger row is a reporting gap; a thrown error here would be a lost
 * order.
 *
 * @param {{ type: string, to: string, sessionId?: string|null }} meta
 * @param {object} payload passed straight to resend.emails.send
 */
async function sendAndRecord(meta, payload) {
  const { data, error } = await resend.emails.send(payload);

  try {
    if (supabaseAdmin) {
      // supabase-js RETURNS errors, it does not throw them, so the catch below
      // would never fire on a failed insert. Read `error` explicitly or a
      // broken ledger stays completely silent - which is the exact failure
      // mode this table was built to eliminate.
      const { error: logErr } = await supabaseAdmin.from('email_deliveries').insert({
        message_id: data?.id ?? null,
        to_email: meta.to,
        email_type: meta.type,
        session_id: meta.sessionId ?? null,
        // 'sent' means Resend accepted it, NOT that it arrived. Only the
        // Resend webhook can move this to 'delivered' or 'bounced'.
        status: error ? 'failed' : 'sent',
        error: error ? String(error.message ?? error).slice(0, 500) : null
      });
      if (logErr) {
        console.error(
          `[email] delivery ledger write failed for ${meta.type} to ${meta.to}: ${logErr.message}` +
          (logErr.code === 'PGRST205' ? ' (run sql/011_email_deliveries.sql)' : '')
        );
      }
    }
  } catch (e) {
    console.error('[email] could not record delivery for', meta.type, e?.message ?? e);
  }

  return { data, error };
}

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
        'All 7 moves are unlocked on the site. Work through them at your own pace. ' +
        'Start with the three you have been avoiding. When you want the deeper strategy, ' +
        'the book is there too.',
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
    ? `${greeting} Your Author's Limited Edition preorder is confirmed. Copy #${copy_number} of 100 is reserved for you. ` +
      `Every copy is hand-bound, signed, and numbered by the author. No two are alike, so #${copy_number} is one of a kind. ` +
      `No payment is collected now. You'll hear from us before the book ships in August 2026.`
    : `${greeting} Your preorder is confirmed. You'll get first access when the book launches in August 2026, ` +
      `available here on the site and on Amazon in paperback and Kindle. No payment collected now. We'll reach out when it's ready.`;

  const cta = isAuthors
    ? { label: 'Read the draft now', url: 'https://survivingthesingularity.com/book' }
    : { label: 'Read the draft now', url: 'https://survivingthesingularity.com/book' };

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
  // Recorded too, and for a specific reason: a buyer name containing CRLF
  // makes Resend reject this subject, so the alert silently never sends while
  // the order records fine. Without a row here that failure is invisible.
  const { error } = await sendAndRecord(
    { type: 'admin_preorder_alert', to: 'admin@johnnyautoseed.com' },
    { from, to: 'admin@johnnyautoseed.com', subject, text: body }
  );
  if (error) console.error('[email] admin preorder alert failed:', error.message ?? error);
  return error ? { error } : { ok: true };
}

/**
 * Confirm a Discord membership application was received. Reviewed by hand,
 * not automatic, so the copy sets that expectation.
 *
 * @param {{ name: string, email: string }} args
 */
export async function sendDiscordApplicationConfirmation({ name, email }) {
  if (!resend) return { skipped: true };
  const safeName = name ? escapeHtml(name.slice(0, 120)) : '';
  const greeting = safeName ? `Hi ${safeName},` : 'Hi,';
  const heading = 'Application received.';
  const body = `${greeting} Your application to join the Surviving the Singularity Discord is in. We review every application by hand, so it may take a few days. You'll hear from us either way.`;
  const cta = { label: 'Back to the checklist', url: 'https://survivingthesingularity.com/checklist' };
  const { error } = await resend.emails.send({
    from,
    to: email,
    subject: 'Your Discord application is in',
    html: renderHtml({ heading, body, cta }),
  });
  if (error) console.error('[email] discord application confirmation failed:', error.message ?? error);
  return error ? { error } : { ok: true };
}

/**
 * Notify the admin inbox when a Discord membership application lands.
 *
 * @param {{ name: string, email: string, answer: string }} args
 */
export async function sendAdminDiscordApplicationAlert({ name, email, answer }) {
  if (!resend) return { skipped: true };
  const subject = `[STS] Discord application: ${name}`;
  const body = `Name: ${name}\nEmail: ${email}\n\nAnswer:\n${answer}`;
  const { error } = await resend.emails.send({
    from,
    to: 'admin@johnnyautoseed.com',
    subject,
    text: body,
  });
  if (error) console.error('[email] admin discord application alert failed:', error.message ?? error);
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
    console.warn('[email] RESEND_API_KEY unset - skipping checklist email to', to);
    return { skipped: true };
  }

  const checkedCount = answers.filter(a => a.checked).length;
  const total = answers.length;

  const heading =
    checkedCount === total ? `You've completed all ${total} steps.` :
    checkedCount === 0     ? 'Your Singularity Readiness Checklist' :
                             `${checkedCount}/${total} steps checked. Keep going.`;

  const intro = checkedCount > 0
    ? `Here's your checklist with your notes. ${total - checkedCount} step${total - checkedCount !== 1 ? 's' : ''} still to do.`
    : 'Your full Singularity Readiness Checklist. Work through these at your own pace.';

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
 * Send the early-access confirmation email after payment. Links to the
 * branded success page (which mints a fresh signed download URL on every
 * visit) rather than a raw storage URL directly, so the link never goes
 * stale and the customer always lands on something in Surviving the
 * Singularity's own branding.
 *
 * @param {{ to: string, sessionId: string, discount_code?: string|null }} args
 */
export async function sendDownloadEmail({ to, sessionId, edition_type, copy_number, discount_code }) {
  if (!resend) {
    console.warn('[email] RESEND_API_KEY unset - skipping download email to', to);
    return { skipped: true };
  }

  const isAuthors = edition_type === 'authors';
  const subject = isAuthors
    ? `Your bundle is ready: Author's Edition copy #${copy_number}`
    : 'Your bundle is ready: preorder confirmed';
  const heading = isAuthors
    ? `Your download is ready. You're copy #${copy_number} of 100.`
    : "Your download is ready. You're on the list.";
  const confirmLine = isAuthors
    ? `Your Author's Limited Edition preorder is confirmed: copy #${copy_number} of 100 is reserved for you. Hand-bound, signed, and numbered by the author, and no two copies are alike. `
    : 'Your preorder is confirmed. ';
  // Describe the bundle by what is ACTUALLY in it. This line previously promised
  // "research PDFs, papers, images, and source documents" while the archive held
  // four .txt files totalling 3KB and no book at all. If the bundle's contents
  // change, change this sentence in the same commit.
  const body =
    `${confirmLine}Your spot in line is locked in at 50% off the finished book, and we will email you an exclusive link when it is ready. ` +
    'Your download is The Precedent File: 29 documented cases of people meeting a machine that changed everything, with every source listed so you can check the work. ' +
    'It also carries the complete current book in PDF and EPUB, the Municipal Autonomy Code, and the cover art.';
  // Links to the branded confirmation page, not the raw storage file directly.
  // The page mints a fresh signed download URL on every visit, so this link
  // works whenever the customer clicks it instead of expiring after 7 days.
  const pageUrl = `https://survivingthesingularity.com/early-access/success?session_id=${encodeURIComponent(sessionId)}`;
  // Shared Stripe promotion code that actually redeems the 50% off at the
  // future book checkout (allow_promotion_codes is already on in
  // stripe-checkout/+server.js). The personal code below is this specific
  // customer's proof of a genuine preorder, stored in Supabase
  // (sql/009_preorder_discount_code.sql) - not itself a Stripe object.
  const masterCode = env.MASTER_DISCOUNT_CODE || 'PREORDER50';

  // The personal code only exists once sql/009_preorder_discount_code.sql has
  // run; until then fulfillPreorder retries the insert without it and passes
  // null through. This used to render the words "Emailed separately", which
  // nothing in this codebase does - there is no follow-up send, so it was a
  // promise to the customer that could never be kept. Show the row only when
  // there is a real code. The master code is the one that actually redeems, so
  // a customer missing the personal code still has everything they need.
  const hasPersonalCode = Boolean(discount_code);
  const keepLine = hasPersonalCode
    ? "Keep both of these. You'll need them when the finished book launches."
    : "Keep this code. You'll need it when the finished book launches.";
  const personalCodeCell = hasPersonalCode
    ? `<td style="padding:8px 0;border-top:1px solid rgba(16,185,129,0.15);">
            <span style="font-size:12px;color:#64748b;display:block;">Your personal code</span>
            <strong style="font-size:18px;letter-spacing:0.08em;color:#f1f5f9;">${escapeHtml(discount_code)}</strong>
          </td>`
    : '';

  const html = `<!doctype html><html><body style="margin:0;background:#020617;font-family:Inter,system-ui,sans-serif;color:#e2e8f0;">
  <div style="max-width:520px;margin:0 auto;padding:40px 24px;">
    <p style="font-size:13px;letter-spacing:0.15em;text-transform:uppercase;color:#f59e0b;font-weight:700;margin:0 0 16px;">Surviving the Singularity</p>
    <h1 style="font-size:24px;color:#f1f5f9;margin:0 0 16px;">${heading}</h1>
    <p style="font-size:15px;line-height:1.7;color:#94a3b8;margin:0 0 28px;">${body}</p>
    <a href="${pageUrl}" style="display:inline-block;background:#f59e0b;color:#0f172a;font-weight:700;font-size:14px;text-decoration:none;padding:14px 24px;border-radius:8px;margin-bottom:24px;">Download The Precedent File</a>
    <div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2);border-radius:10px;padding:16px 20px;margin-bottom:16px;">
      <p style="font-size:13px;color:#6ee7b7;font-weight:700;margin:0 0 10px;text-transform:uppercase;letter-spacing:0.06em;">Your 50% off launch discount</p>
      <p style="font-size:13px;color:#94a3b8;margin:0 0 8px;line-height:1.6;">${keepLine}</p>
      <table role="presentation" style="width:100%;border-collapse:collapse;">
        <tr>
          ${personalCodeCell}
          <td style="padding:8px 0;border-top:1px solid rgba(16,185,129,0.15);">
            <span style="font-size:12px;color:#64748b;display:block;">Code to redeem at checkout</span>
            <strong style="font-size:18px;letter-spacing:0.08em;color:#f1f5f9;">${escapeHtml(masterCode)}</strong>
          </td>
        </tr>
      </table>
    </div>
    <div style="background:rgba(245,158,11,0.05);border:1px solid rgba(245,158,11,0.15);border-radius:10px;padding:16px 20px;margin-top:8px;">
      <p style="font-size:13px;color:#64748b;margin:0 0 10px;">Also included in your early access:</p>
      <p style="font-size:13px;color:#94a3b8;margin:0;line-height:1.7;">
        Full book: current draft <a href="https://survivingthesingularity.com/book" style="color:#f59e0b;">survivingthesingularity.com/book</a>
      </p>
      <p style="font-size:13px;color:#94a3b8;margin:10px 0 0;line-height:1.7;border-top:1px solid rgba(245,158,11,0.12);padding-top:10px;">Book page password: <strong style="color:#f1f5f9;letter-spacing:0.02em;">${escapeHtml(BOOK_ACCESS_PASSWORD)}</strong></p>
    </div>
    <p style="font-size:11px;color:#334155;margin:36px 0 0;">Order ref: ${sessionId.slice(0, 24)}... · survivingthesingularity.com · Reply to this email for support.</p>
  </div></body></html>`;

  // The one email a paying customer must receive. Recorded so a bounce is
  // visible in our own data rather than only in Resend's dashboard.
  const { data, error } = await sendAndRecord(
    { type: 'preorder_download', to, sessionId },
    { from, to, subject, html }
  );
  if (error) {
    console.error('[email] download email failed:', error.message ?? error);
    return { error };
  }
  return { ok: true, messageId: data?.id ?? null };
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
    console.warn('[email] RESEND_API_KEY unset - skipping welcome email to', to);
    return { skipped: true };
  }
  const baseUrl = env.PUBLIC_BASE_URL || 'https://survivingthesingularity.com';
  const unsubscribeUrl = unsubscribeToken
    ? `${baseUrl}/unsubscribe?token=${unsubscribeToken}`
    : null;
  const copy = buildWelcome(source);
  const { error } = await sendAndRecord(
    { type: 'welcome', to },
    { from, to, subject: copy.subject, html: renderHtml({ ...copy, unsubscribeUrl }) }
  );
  if (error) {
    console.error('[email] welcome send failed:', error.message ?? error);
    return { error };
  }
  return { ok: true };
}
