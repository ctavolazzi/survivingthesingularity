/**
 * ADMIN: paid sessions that were never fulfilled. Plan item B-06.
 *
 * GET  /api/admin/reconcile              report as JSON
 * GET  /api/admin/reconcile?format=text  report as plain text, for a terminal
 * GET  /api/admin/reconcile?alert=1      also email the admin inbox, if any found
 * GET  /api/admin/reconcile?grace=30     override the grace window, in minutes
 *
 * Requires `Authorization: Bearer <ADMIN_RECONCILE_TOKEN>`.
 *
 * THIS ENDPOINT FAILS SHUT, WHICH IS THE OPPOSITE OF THE WEBHOOK BOOKKEEPING.
 *
 * webhookEvents.js degrades OPEN on purpose: a missing table must not block a
 * paid order, because losing a log line costs a report while losing an order
 * costs a customer. This endpoint inverts that. It serves customer email
 * addresses joined to payment references, so with no token configured it serves
 * nothing at all. See adminToken.js.
 *
 * IT DOES NOT SCHEDULE ITSELF, AND THAT IS THE REMAINING GAP.
 *
 * The failure B-06 detects is a webhook that never arrived, which means none of
 * our code ran and nothing inside the app can notice. Detection has to be
 * out-of-band. Cloudflare Pages has no cron trigger, so something external has
 * to call this on a schedule. Until that caller exists this is an on-demand
 * report, and an on-demand report that nobody demands is not an alarm. Do not
 * record B-06 as closed on the strength of this file alone.
 */
import { json, text } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import { authorizeAdmin } from '$lib/server/adminToken.js';
import {
  findUnreconciled,
  formatReconciliationReport,
  DEFAULT_GRACE_MINUTES,
} from '$lib/server/reconcile.js';
import { sendAdminReconciliationAlert } from '$lib/server/email.js';

/**
 * Messages are intentionally vague about which check failed for a caller who is
 * not authorised, and specific for one who is. Telling an unauthenticated
 * stranger the difference between "wrong token" and "no token configured" hands
 * them a probe for free.
 */
const DENIED = {
  'not-configured': 'Not configured',
  'token-too-short': 'Not configured',
  'missing-token': 'Unauthorized',
  'bad-token': 'Unauthorized',
};

/** @type {import('./$types').RequestHandler} */
export async function GET({ request, url }) {
  const auth = authorizeAdmin(
    request.headers.get('authorization'),
    env.ADMIN_RECONCILE_TOKEN
  );

  if (!auth.ok) {
    // Logged server-side with the real reason, so an operator can tell a
    // misconfiguration from a bad call without that difference going on the wire.
    console.warn(`[reconcile] denied: ${auth.reason}`);
    return json({ error: DENIED[auth.reason] ?? 'Unauthorized' }, { status: auth.status });
  }

  const graceParam = Number.parseInt(url.searchParams.get('grace') ?? '', 10);
  const graceMinutes = Number.isFinite(graceParam) && graceParam >= 0
    ? graceParam
    : DEFAULT_GRACE_MINUTES;

  const report = await findUnreconciled({ graceMinutes });
  const body = formatReconciliationReport(report);

  // Only send when the check actually RAN and actually found something. Alerting
  // on a failed check would train the reader to ignore this mail, and staying
  // silent on a failed check would read as an all-clear, so the failure is
  // carried in the response instead where the caller has to look at it.
  let alerted = false;
  if (url.searchParams.get('alert') === '1' && report.ok && report.count > 0) {
    const sent = await sendAdminReconciliationAlert({ count: report.count, body });
    alerted = Boolean(sent?.ok);
  }

  if (url.searchParams.get('format') === 'text') {
    return text(`${body}\n`, {
      status: report.ok ? 200 : 503,
      headers: { 'cache-control': 'no-store' },
    });
  }

  return json(
    {
      // `ok:false` means the check could not run. A caller must not read that as
      // "nothing found", which is why count is omitted rather than zeroed when
      // the check failed.
      ok: report.ok,
      configured: report.configured,
      error: report.error ?? null,
      graceMinutes: report.graceMinutes,
      count: report.ok ? report.count : null,
      alerted,
      sessions: report.rows,
      note: report.ok
        ? undefined
        : 'This is not an all-clear. The reconciliation check did not run.',
    },
    { status: report.ok ? 200 : 503, headers: { 'cache-control': 'no-store' } }
  );
}
