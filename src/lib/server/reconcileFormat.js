/**
 * Rendering and thresholds for the reconciliation report (plan item B-06).
 *
 * Split out of reconcile.js for one reason: reconcile.js imports supabaseAdmin,
 * which pulls in $env/dynamic/private, and a module carrying a SvelteKit alias
 * cannot be loaded by a plain test runner. This project has no vitest, so
 * anything that needs real test coverage has to live somewhere importable by
 * relative path. Same reasoning as webhookEventPolicy.js and adminToken.js.
 *
 * This file is worth testing rather than eyeballing because it produces the text
 * a human reads while deciding whether money is currently going missing. A
 * formatter bug here does not crash anything; it just quietly misstates the
 * amount, which is the kind of defect that survives review.
 *
 * Tested in tests/e2e/l-reconcile-format.spec.js.
 */

/**
 * Minutes a paid session may go unfulfilled before it counts as a problem.
 *
 * Not arbitrary. The success page and the webhook routinely land within seconds
 * of each other, and Stripe spaces its retries minutes apart, so a tighter
 * window would fire on healthy traffic mid-retry. An alert that cries wolf gets
 * filtered into a folder nobody reads, at which point the real one is missed
 * too, so the threshold is set where a firing genuinely means something.
 *
 * The SQL view in sql/014 carries the same 15 minute floor. This constant is
 * the one used for anything stricter the caller asks for.
 */
export const DEFAULT_GRACE_MINUTES = 15;

/**
 * Render the report as plain text for an alert email or a terminal.
 *
 * Leads with the amount of money involved, because that is the number that
 * decides whether this gets looked at now or after lunch.
 *
 * @param {{ ok: boolean, configured: boolean, rows: object[], count: number, error?: string, graceMinutes: number }} report
 */
export function formatReconciliationReport(report) {
  if (!report.configured) {
    return `RECONCILIATION COULD NOT RUN: ${report.error}\n\nThis is not an all-clear. Nothing was checked.`;
  }
  if (!report.ok) {
    return `RECONCILIATION FAILED: ${report.error}\n\nThis is not an all-clear. Nothing was checked.`;
  }
  if (report.count === 0) {
    return `No unreconciled paid sessions older than ${report.graceMinutes} minutes. Checked and clear.`;
  }

  const totalMinor = report.rows.reduce((sum, r) => sum + (r.amount_total ?? 0), 0);
  const currency = (report.rows.find((r) => r.currency)?.currency ?? 'usd').toUpperCase();
  const lines = report.rows.map((r) => {
    const amount = r.amount_total != null ? `${(r.amount_total / 100).toFixed(2)}` : 'unknown';
    const state = r.never_claimed
      ? 'NEVER CLAIMED (webhook likely never arrived)'
      : `claimed but ${r.fulfillment_status ?? 'unknown'}`;
    // Every interpolation below is guarded, including the ones that "cannot" be
    // null because the view declares them non-null. A test with a deliberately
    // sparse row caught `paid undefined min ago` here, which would have gone out
    // in a real alert: the reader would have seen the word undefined next to a
    // dollar amount and had no idea whether the age or the money was the
    // unreliable part. A formatter that is fed a surprising row should degrade to
    // saying less, never to saying nonsense.
    const age = Number.isFinite(r.minutes_outstanding)
      ? `paid ${r.minutes_outstanding} min ago`
      : 'age unknown';
    return [
      `  ${r.session_id ?? '(no session id on record)'}`,
      `    ${age}, ${amount} ${currency}`,
      `    ${r.email ?? 'no email on record'}  (${r.edition_type ?? 'unknown edition'})`,
      `    ${state}`,
      r.fulfillment_error ? `    last error: ${r.fulfillment_error}` : null,
      r.webhook_event_id
        ? `    webhook event ${r.webhook_event_id} (${r.webhook_status ?? 'status unknown'})`
        : '    no webhook event recorded for this session',
    ]
      .filter(Boolean)
      .join('\n');
  });

  return [
    `${report.count} PAID SESSION(S) NOT FULFILLED, totalling ${(totalMinor / 100).toFixed(2)} ${currency}.`,
    `Older than ${report.graceMinutes} minutes, so this is not a race in progress.`,
    '',
    ...lines,
    '',
    'Each of these is someone who paid and did not receive what they paid for.',
    'Fix by replaying the Stripe event, or by fulfilling by hand and recording it.',
  ].join('\n');
}
