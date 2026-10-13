/**
 * The reconciliation report text (plan item B-06).
 *
 * This is the text a human reads while deciding whether money is currently going
 * missing, so the assertions are about whether it can MISLEAD, not about whether
 * it renders.
 *
 * The first block is the important one. A monitor that cannot run must never
 * produce output that reads like an all-clear. That failure mode has already bitten
 * this project twice, in a different costume each time, and it is recorded in
 * section 9 of the verification ledger.
 */
import { test, expect } from '@playwright/test';
import {
  formatReconciliationReport,
  DEFAULT_GRACE_MINUTES
} from '../../src/lib/server/reconcileFormat.js';

const row = (over = {}) => ({
  session_id: 'cs_test_abc',
  email: 'buyer@example.com',
  edition_type: 'standard',
  amount_total: 500,
  currency: 'usd',
  minutes_outstanding: 42,
  fulfillment_status: null,
  fulfillment_error: null,
  never_claimed: true,
  webhook_event_id: null,
  webhook_status: null,
  ...over
});

test.describe('a check that could not run must not read as an all-clear', () => {
  test('unconfigured says so and explicitly denies being an all-clear', () => {
    const out = formatReconciliationReport({
      ok: false, configured: false, rows: [], count: 0,
      error: 'Supabase not configured', graceMinutes: 15
    });
    expect(out).toContain('COULD NOT RUN');
    expect(out).toContain('not an all-clear');
    // Must not contain the reassuring phrasing used for a genuine clean result.
    expect(out).not.toContain('Checked and clear');
    expect(out).not.toContain('No unreconciled');
  });

  test('a failed query says so and denies being an all-clear', () => {
    const out = formatReconciliationReport({
      ok: false, configured: true, rows: [], count: 0,
      error: 'relation does not exist', graceMinutes: 15
    });
    expect(out).toContain('FAILED');
    expect(out).toContain('not an all-clear');
    expect(out).not.toContain('Checked and clear');
  });

  test('a genuinely clean result is the ONLY output that reassures', () => {
    const out = formatReconciliationReport({
      ok: true, configured: true, rows: [], count: 0, graceMinutes: 15
    });
    expect(out).toContain('No unreconciled');
    expect(out).toContain('Checked and clear');
    expect(out).not.toContain('not an all-clear');
  });

  test('clean output names the window it checked, so a short window cannot hide behind it', () => {
    const out = formatReconciliationReport({
      ok: true, configured: true, rows: [], count: 0, graceMinutes: 90
    });
    expect(out).toContain('90 minutes');
  });
});

test.describe('money is stated correctly', () => {
  test('a single session converts minor units to a readable amount', () => {
    const out = formatReconciliationReport({
      ok: true, configured: true, rows: [row()], count: 1, graceMinutes: 15
    });
    expect(out).toContain('1 PAID SESSION(S) NOT FULFILLED');
    expect(out).toContain('5.00 USD');
    expect(out).toContain('cs_test_abc');
    expect(out).toContain('buyer@example.com');
  });

  test('amounts are summed across sessions, not counted', () => {
    const out = formatReconciliationReport({
      ok: true,
      configured: true,
      rows: [row(), row({ session_id: 'cs_2', amount_total: 2500 }), row({ session_id: 'cs_3', amount_total: 1000 })],
      count: 3,
      graceMinutes: 15
    });
    // 500 + 2500 + 1000 = 4000 minor units = 40.00
    expect(out).toContain('totalling 40.00 USD');
    expect(out).toContain('3 PAID SESSION(S)');
  });

  test('a null amount does not poison the total with NaN', () => {
    const out = formatReconciliationReport({
      ok: true,
      configured: true,
      rows: [row({ amount_total: null }), row({ session_id: 'cs_2', amount_total: 500 })],
      count: 2,
      graceMinutes: 15
    });
    expect(out).not.toContain('NaN');
    expect(out).toContain('totalling 5.00 USD');
    expect(out).toContain('unknown');
  });

  test('currency comes from the data, not hardcoded, and survives a null first row', () => {
    const out = formatReconciliationReport({
      ok: true,
      configured: true,
      rows: [row({ currency: null }), row({ session_id: 'cs_2', currency: 'gbp' })],
      count: 2,
      graceMinutes: 15
    });
    expect(out).toContain('GBP');
    expect(out).not.toContain('USD');
  });
});

test.describe('each row says what actually went wrong', () => {
  test('never_claimed is called out as a probably-missing webhook', () => {
    const out = formatReconciliationReport({
      ok: true, configured: true, rows: [row({ never_claimed: true })], count: 1, graceMinutes: 15
    });
    expect(out).toContain('NEVER CLAIMED');
    expect(out).toContain('webhook likely never arrived');
    expect(out).toContain('no webhook event recorded for this session');
  });

  test('a claimed-but-failed row reports its status and error', () => {
    const out = formatReconciliationReport({
      ok: true,
      configured: true,
      rows: [row({
        never_claimed: false,
        fulfillment_status: 'failed',
        fulfillment_error: 'RESEND_API_KEY unset; no email sent',
        webhook_event_id: 'evt_123',
        webhook_status: 'processed'
      })],
      count: 1,
      graceMinutes: 15
    });
    expect(out).toContain('claimed but failed');
    expect(out).toContain('RESEND_API_KEY unset');
    expect(out).toContain('evt_123');
    expect(out).toContain('processed');
    expect(out).not.toContain('NEVER CLAIMED');
  });

  test('a missing email is stated rather than rendered as undefined', () => {
    const out = formatReconciliationReport({
      ok: true, configured: true, rows: [row({ email: null })], count: 1, graceMinutes: 15
    });
    expect(out).toContain('no email on record');
    expect(out).not.toContain('undefined');
    expect(out).not.toContain('null');
  });

  test('every row appears, not just the first', () => {
    const rows = Array.from({ length: 7 }, (_, i) => row({ session_id: `cs_${i}` }));
    const out = formatReconciliationReport({ ok: true, configured: true, rows, count: 7, graceMinutes: 15 });
    for (let i = 0; i < 7; i++) expect(out, `cs_${i}`).toContain(`cs_${i}`);
  });

  test('the report never renders the literal word undefined for any row shape', () => {
    const out = formatReconciliationReport({
      ok: true, configured: true, rows: [{ session_id: 'cs_bare' }], count: 1, graceMinutes: 15
    });
    expect(out).not.toContain('undefined');
  });
});

test('the default grace window is a sane non-zero value', () => {
  expect(DEFAULT_GRACE_MINUTES).toBeGreaterThan(0);
  expect(DEFAULT_GRACE_MINUTES).toBeGreaterThanOrEqual(15);
});
