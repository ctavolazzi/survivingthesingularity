import { env } from '$env/dynamic/private';
import { Resend } from 'resend';
import { BOOK_ACCESS_PASSWORD } from '$lib/bookAccessCode.js';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
// The confirmation email is a sales surface like any other, and it is the one a
// customer keeps. It derives its offer claims from the same object the pages do.
import { offer, offerItemLabel } from '$lib/offer.js';
// The itemised file table is a MEASUREMENT of the archive, not a description of
// it. A static import, so it bundles into the Worker with no filesystem read.
// Regenerated only by scripts/build_bonus.py, and `sts.py bundle verify` is what
// proves it still matches the zip customers actually receive.
import bundleManifest from '$lib/data/bundleManifest.js';

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
 * Stripe reports most currencies in minor units (cents), but not all of them.
 * Dividing by 100 unconditionally would print a 500 yen charge as 5.00 yen.
 * This is the full Stripe zero-decimal set as of 2026-08.
 */
const ZERO_DECIMAL = new Set([
  'bif', 'clp', 'djf', 'gnf', 'jpy', 'kmf', 'krw', 'mga',
  'pyg', 'rwf', 'ugx', 'vnd', 'vuv', 'xaf', 'xof', 'xpf',
]);

/**
 * What the customer was ACTUALLY charged, formatted, or null.
 *
 * DELIBERATELY NOT DERIVED FROM offer.priceCents, and this is the one place in
 * this codebase where deriving from the offer object would be wrong. Checkout
 * runs with allow_promotion_codes, so the advertised price and the charged
 * amount legitimately differ, and a receipt that states the list price to
 * someone who used a code is a false financial record.
 *
 * Returns null rather than a guess when Stripe gave us nothing. The caller then
 * omits the row: a receipt with no amount line is incomplete, a receipt with an
 * invented amount is wrong.
 */
function formatMoney(amountMinor, currency) {
  if (!Number.isFinite(amountMinor) || !currency) return null;
  const code = String(currency).toLowerCase();
  const major = ZERO_DECIMAL.has(code) ? amountMinor : amountMinor / 100;
  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: code.toUpperCase(),
    }).format(major);
  } catch {
    // Unknown currency code, or an Intl build without it. Still better than
    // dropping the amount entirely, since the number itself is the fact.
    return `${major.toFixed(ZERO_DECIMAL.has(code) ? 0 : 2)} ${code.toUpperCase()}`;
  }
}

function formatBytes(bytes) {
  if (!Number.isFinite(bytes)) return '';
  if (bytes >= 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  if (bytes >= 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${bytes} B`;
}

/**
 * Stripe hands out unix SECONDS. Rendered in UTC and labelled as such, because
 * a date with no zone on a financial record is ambiguous by exactly the amount
 * that matters at a month boundary.
 */
function formatOrderDate(unixSeconds) {
  if (!Number.isFinite(unixSeconds)) return null;
  try {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC',
    }).format(new Date(unixSeconds * 1000)) + ' UTC';
  } catch {
    return null;
  }
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

/**
 * Postal address for the email footer.
 *
 * The federal CAN-SPAM Act requires a valid physical postal address, a street
 * address or a registered PO box, in commercial email. Verified 2026-07-29: no
 * address of any kind appeared anywhere in this file, so every commercial send
 * was missing it.
 *
 * DELIBERATELY UNSET AND DELIBERATELY NOT INVENTED. Nobody should guess a
 * business address into a legal notice, and shipping a plausible-looking
 * placeholder would be worse than shipping nothing: it reads as compliance while
 * being false. So the mechanism is wired and the value is one environment
 * variable away.
 *
 * Set EMAIL_POSTAL_ADDRESS in Cloudflare Pages, for example
 * "Christopher Tavolazzi, PO Box 1234, Chico, CA 95926", before running any
 * newsletter or promotional send. The transactional receipt is on a different
 * footing, since CAN-SPAM treats transactional or relationship messages
 * differently from commercial ones, but there is no downside to it appearing
 * there too.
 */
const postalAddress = env.EMAIL_POSTAL_ADDRESS || null;
if (!postalAddress) {
  console.warn(
    '[email] EMAIL_POSTAL_ADDRESS is unset, so the CAN-SPAM postal address is ' +
      'omitted from email footers. Set it before any commercial or newsletter send.'
  );
}

/**
 * The legal footer, in ONE place.
 *
 * Extracted because sendDownloadEmail builds its own HTML rather than going
 * through renderHtml, and so shipped without any postal address at all. That
 * made the CAN-SPAM line absent from the single email every paying customer
 * receives, which is the worst possible file to omit it from. A shared helper
 * means the next hand-rolled email cannot quietly drop it either.
 *
 * `reason` states why this person is receiving mail, which has to be true of
 * the specific send: a purchase receipt did not arrive because someone "signed
 * up", and saying so on a transactional message is both wrong and confusing.
 */
function footerHtml({ unsubscribeUrl = null, reason = 'you signed up at survivingthesingularity.com' } = {}) {
  const unsub = unsubscribeUrl
    ? `<a href="${unsubscribeUrl}" style="color:#475569;text-decoration:underline;">Unsubscribe</a>`
    : 'Reply to unsubscribe';
  // Rendered only when a real address is configured. An empty line is better
  // than a fabricated one.
  const postal = postalAddress
    ? `<p style="font-size:12px;color:#475569;margin:8px 0 0;">${escapeHtml(postalAddress)}</p>`
    : '';
  return `<p style="font-size:12px;color:#475569;margin:36px 0 0;">You received this because ${reason}. ${unsub}.</p>
    ${postal}`;
}

function renderHtml({ heading, body, cta, unsubscribeUrl }) {
  return `<!doctype html><html><body style="margin:0;background:#020617;font-family:Inter,system-ui,sans-serif;color:#e2e8f0;">
  <div style="max-width:520px;margin:0 auto;padding:40px 24px;">
    <p style="font-size:13px;letter-spacing:0.15em;text-transform:uppercase;color:#f59e0b;font-weight:700;margin:0 0 16px;">Surviving the Singularity</p>
    <h1 style="font-size:24px;color:#f1f5f9;margin:0 0 16px;">${heading}</h1>
    <p style="font-size:15px;line-height:1.7;color:#94a3b8;margin:0 0 28px;">${body}</p>
    <a href="${cta.url}" style="display:inline-block;background:#f59e0b;color:#0f172a;font-weight:700;font-size:14px;text-decoration:none;padding:12px 22px;border-radius:8px;">${cta.label}</a>
    ${footerHtml({ unsubscribeUrl })}
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

  // Recorded: this is the customer's own copy of the order. The admin alert
  // below was already in the ledger while this was not, which had it backwards
  // - a bounced admin alert costs us an inbox notification, a bounced customer
  // confirmation costs the customer any record that the order exists.
  const { error } = await sendAndRecord(
    { type: 'preorder_confirmation', to: email },
    { from, to: email, subject, html: renderHtml({ heading, body, cta }) }
  );
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
  const { error } = await sendAndRecord(
    { type: 'discord_application_confirmation', to: email },
    { from, to: email, subject: 'Your Discord application is in', html: renderHtml({ heading, body, cta }) }
  );
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
  // Same reasoning as the preorder alert: an applicant name containing CRLF
  // makes Resend reject this subject, so the alert silently never sends while
  // the application records fine. Without a row here that failure is invisible.
  const { error } = await sendAndRecord(
    { type: 'admin_discord_application_alert', to: 'admin@johnnyautoseed.com' },
    { from, to: 'admin@johnnyautoseed.com', subject, text: body }
  );
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

  const { error } = await sendAndRecord(
    { type: 'checklist', to },
    { from, to, subject, html }
  );
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
export async function sendDownloadEmail({
  to, sessionId, edition_type, copy_number, discount_code,
  amountTotal = null, currency = null, paymentIntent = null, orderedAt = null,
}) {
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
    `${confirmLine}Every digital thing this project makes is now yours, including the finished edition when it lands, at no additional cost. ` +
    'When the membership launches later, you never pay it. ' +
    `Your download is The Precedent File: ${offer.precedentFileCaseCount} documented cases of people meeting a machine that changed everything, ` +
    `${offer.precedentFileSourcedCount} of them with their sources listed inline so you can check the work. ` +
    'It carries the sources index, the cover art, and the Robotics Company Index alongside it. ' +
    // The book files ride along for convenience and are NOT what the five
    // dollars bought: they are free to anyone at /downloads, and this sentence
    // says so rather than letting the list imply otherwise. The itemised table
    // below marks them from bundleManifest role: "convenience-copy", so this
    // cannot drift back into a selling point without the manifest changing too.
    'It also carries the full book in PDF and EPUB and the Municipal Autonomy Code, which are free to download by anyone and are in here so you do not have to go and get them.';
  // Links to the branded confirmation page, not the raw storage file directly.
  // The page mints a fresh signed download URL on every visit, so this link
  // works whenever the customer clicks it instead of expiring after 7 days.
  const pageUrl = `https://survivingthesingularity.com/early-access/success?session_id=${encodeURIComponent(sessionId)}`;
  // Shared Stripe promotion code (allow_promotion_codes is already on in
  // stripe-checkout/+server.js). The personal code below is this specific
  // customer's proof of a genuine preorder, stored in Supabase
  // (sql/009_preorder_discount_code.sql) - not itself a Stripe object.
  //
  // 2026-07-29: what this code buys CHANGED. It used to be 50% off the finished
  // book, which no longer means anything now that the digital edition is
  // included in the $5. Per the ratified offer it attaches to the Print
  // Edition, a separate product at its own price that does not exist yet. The
  // copy below says exactly that rather than implying the code is redeemable
  // today, because it is not: there is nothing to redeem it against until the
  // first Print Edition goes on sale.
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
    ? 'Keep both of these. The Print Edition is a separate product and it is not ready yet, so there is nothing to redeem against today. When the first one goes on sale, these are what get you half off it.'
    : 'Keep this code. The Print Edition is a separate product and it is not ready yet, so there is nothing to redeem against today. When the first one goes on sale, this is what gets you half off it.';
  const personalCodeCell = hasPersonalCode
    ? `<td style="padding:8px 0;border-top:1px solid rgba(16,185,129,0.15);">
            <span style="font-size:12px;color:#64748b;display:block;">Your personal code</span>
            <strong style="font-size:18px;letter-spacing:0.08em;color:#f1f5f9;">${escapeHtml(discount_code)}</strong>
          </td>`
    : '';

  // ── ORDER RECEIPT ─────────────────────────────────────────────────────────
  // Each row is OMITTED when its fact is missing rather than filled with a
  // plausible value. A receipt is a financial record: a missing line is a gap
  // the customer can ask about, an invented line is a misstatement they cannot
  // detect. The amount in particular never falls back to the list price, since
  // promotion codes make the charged amount legitimately different.
  const amountPaid = formatMoney(amountTotal, currency);
  const orderDate = formatOrderDate(orderedAt);
  const receiptRows = [
    ['Order reference', sessionId],
    orderDate ? ['Order date', orderDate] : null,
    amountPaid ? ['Amount paid', amountPaid] : null,
    paymentIntent ? ['Payment reference', paymentIntent] : null,
  ]
    .filter(Boolean)
    .map(
      ([k, v]) => `<tr>
          <td style="padding:6px 12px 6px 0;font-size:12px;color:#64748b;white-space:nowrap;vertical-align:top;">${k}</td>
          <td style="padding:6px 0;font-size:12px;color:#e2e8f0;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;word-break:break-all;">${escapeHtml(v)}</td>
        </tr>`
    )
    .join('');

  // ── WHAT IS IN THE ARCHIVE ────────────────────────────────────────────────
  // Generated from bundleManifest, which scripts/build_bonus.py writes from the
  // same staged file list it zips. So this table cannot describe a file the
  // archive does not contain, and `sts.py bundle verify` fails if it drifts.
  // The convenience copies are tagged as free rather than listed flat, so the
  // list cannot read as though five dollars unlocked the book.
  const fileRows = bundleManifest.files
    .map((f) => {
      // Keyed on `role`, which is the semantic field, with `also_free_at`
      // supplying the location. The comment above the body copy promises this
      // marking, so it reads the field that promise names.
      const freeTag = f.role === 'convenience-copy' && f.also_free_at
        ? `<span style="display:inline-block;font-size:10px;color:#6ee7b7;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);border-radius:4px;padding:1px 6px;margin-left:6px;white-space:nowrap;">free at ${escapeHtml(f.also_free_at.replace(/\/[^/]*$/, '') || '/downloads')}</span>`
        : '';
      return `<tr>
          <td style="padding:7px 12px 7px 0;font-size:12px;color:#e2e8f0;line-height:1.5;border-top:1px solid rgba(148,163,184,0.12);">${escapeHtml(f.label)}${freeTag}</td>
          <td style="padding:7px 0;font-size:11px;color:#64748b;text-align:right;white-space:nowrap;vertical-align:top;border-top:1px solid rgba(148,163,184,0.12);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;">${escapeHtml(f.format.toUpperCase())} · ${formatBytes(f.bytes)}</td>
        </tr>`;
    })
    .join('');

  const html = `<!doctype html><html><body style="margin:0;background:#020617;font-family:Inter,system-ui,sans-serif;color:#e2e8f0;">
  <div style="max-width:520px;margin:0 auto;padding:40px 24px;">
    <p style="font-size:13px;letter-spacing:0.15em;text-transform:uppercase;color:#f59e0b;font-weight:700;margin:0 0 16px;">Surviving the Singularity</p>
    <h1 style="font-size:24px;color:#f1f5f9;margin:0 0 16px;">${heading}</h1>
    <p style="font-size:15px;line-height:1.7;color:#94a3b8;margin:0 0 28px;">${body}</p>
    <a href="${pageUrl}" style="display:inline-block;background:#f59e0b;color:#0f172a;font-weight:700;font-size:14px;text-decoration:none;padding:14px 24px;border-radius:8px;margin-bottom:24px;">Download The Precedent File</a>
    <div style="background:rgba(148,163,184,0.04);border:1px solid rgba(148,163,184,0.15);border-radius:10px;padding:16px 20px;margin-bottom:16px;">
      <p style="font-size:12px;color:#64748b;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;">In your archive</p>
      <p style="font-size:12px;color:#64748b;margin:0 0 6px;">${bundleManifest.bundle.entries} files, ${formatBytes(bundleManifest.bundle.bytes)} zipped.</p>
      <table role="presentation" style="width:100%;border-collapse:collapse;">${fileRows}</table>
    </div>
    <div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2);border-radius:10px;padding:16px 20px;margin-bottom:16px;">
      <p style="font-size:13px;color:#6ee7b7;font-weight:700;margin:0 0 10px;text-transform:uppercase;letter-spacing:0.06em;">Your ${offerItemLabel('print-discount')}</p>
      <p style="font-size:13px;color:#94a3b8;margin:0 0 8px;line-height:1.6;">${keepLine}</p>
      <table role="presentation" style="width:100%;border-collapse:collapse;">
        <tr>
          ${personalCodeCell}
          <td style="padding:8px 0;border-top:1px solid rgba(16,185,129,0.15);">
            <span style="font-size:12px;color:#64748b;display:block;">Code to redeem when the Print Edition is on sale</span>
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
    <div style="border-top:1px solid rgba(148,163,184,0.15);margin-top:32px;padding-top:20px;">
      <p style="font-size:12px;color:#64748b;margin:0 0 10px;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;">Order receipt</p>
      <table role="presentation" style="width:100%;border-collapse:collapse;">${receiptRows}</table>
      <p style="font-size:11px;color:#334155;margin:14px 0 0;">Keep this for your records. Reply to this email for support.</p>
    </div>
    ${footerHtml({ reason: 'you bought early access at survivingthesingularity.com' })}
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
/**
 * Alert the admin inbox that paid sessions were never fulfilled (plan item B-06).
 *
 * Plain text, not HTML, and deliberately so: this one is read in a hurry on a
 * phone, and every line of it is an action item rather than a nicety.
 *
 * The subject carries the COUNT, because the whole value of this alert is being
 * able to tell "one order needs a nudge" from "the pipeline is down" without
 * opening it.
 *
 * @param {{ count: number, body: string }} args
 */
export async function sendAdminReconciliationAlert({ count, body }) {
  if (!resend) return { skipped: true };
  const subject = `[STS] ${count} paid session${count === 1 ? '' : 's'} not fulfilled`;
  const { error } = await sendAndRecord(
    { type: 'admin_reconciliation_alert', to: 'admin@johnnyautoseed.com' },
    { from, to: 'admin@johnnyautoseed.com', subject, text: body }
  );
  if (error) console.error('[email] reconciliation alert failed:', error.message ?? error);
  return error ? { error } : { ok: true };
}

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
