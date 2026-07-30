/**
 * B-08: the webhook event idempotency policy.
 *
 * No browser and no database. This exercises the pure decision function that
 * decides whether a repeat delivery of a Stripe event should run fulfillment,
 * which is where the only interesting bug in B-08 can live.
 *
 * WHY A PURE TEST IS THE RIGHT TEST HERE, AND WHAT IT DOES NOT COVER
 *
 * The database wiring in webhookEvents.js cannot be verified in this
 * environment: there is no .env and therefore no Supabase, so `supabaseAdmin` is
 * null and every query path no-ops. Rather than write a test that passes because
 * nothing ran, which is precisely the false-pass shape recorded twice in the
 * verification ledger, the load-bearing rule was extracted into a module with no
 * dependencies and is tested exhaustively here.
 *
 * What this proves: every state a prior event row can be in maps to the right
 * decision, including the one that matters.
 * What this does NOT prove: that the insert, the conflict code, or the outcome
 * update work against real Postgres. Those stay unverified until someone runs
 * sql/014 and replays a signed event at a deployment with credentials.
 */
import { test, expect } from '@playwright/test';
import {
  decideEventDisposition,
  STALE_EVENT_MS,
  PROCESSED,
  PROCESSING,
  FAILED
} from '../../src/lib/server/webhookEventPolicy.js';

const NOW = Date.parse('2026-07-29T12:00:00.000Z');
const iso = (msAgo) => new Date(NOW - msAgo).toISOString();

test.describe('B-08 event disposition', () => {
  test('a never-before-seen event is processed', () => {
    const d = decideEventDisposition(null, NOW);
    expect(d.proceed).toBe(true);
    expect(d.duplicate).toBe(false);
    expect(d.reason).toBe('first-delivery');
  });

  test('undefined is treated the same as null, not as a row', () => {
    expect(decideEventDisposition(undefined, NOW).proceed).toBe(true);
  });

  /**
   * The acceptance condition from the plan: a genuine replay of completed work
   * is recognised and not redone.
   */
  test('an already-processed event is a duplicate and is skipped', () => {
    const d = decideEventDisposition(
      { status: PROCESSED, received_at: iso(1000) },
      NOW
    );
    expect(d.proceed).toBe(false);
    expect(d.duplicate).toBe(true);
    expect(d.reason).toBe('already-processed');
  });

  test('a processed event stays skipped no matter how old it is', () => {
    const ancient = decideEventDisposition(
      { status: PROCESSED, received_at: iso(365 * 24 * 60 * 60 * 1000) },
      NOW
    );
    expect(ancient.proceed).toBe(false);
    expect(ancient.duplicate).toBe(true);
  });

  /**
   * THE HAZARD. This is the assertion the whole file exists for.
   *
   * Stripe reuses the same event id when it retries. A naive dedup on event id
   * would return proceed=false here, the handler would answer 200, and a paid
   * order whose first attempt failed would never be fulfilled while the events
   * table claimed it was handled. Same failure shape as the pre-013
   * fulfilled_sessions tombstone: a row meaning "began" being read as "done".
   */
  test('a retry after a FAILED attempt is allowed through, not skipped', () => {
    const d = decideEventDisposition(
      { status: FAILED, received_at: iso(30 * 1000), attempts: 1 },
      NOW
    );
    expect(d.proceed).toBe(true);
    expect(d.reason).toBe('retry-after-failure');
    // Not a duplicate: nothing was ever delivered for this event.
    expect(d.duplicate).toBe(false);
  });

  test('a failed attempt is retryable immediately, with no cool-off', () => {
    // Deliberate: Stripe already spaces retries minutes apart. Adding our own
    // delay on top would only widen the window in which a paid order sits
    // undelivered.
    const d = decideEventDisposition({ status: FAILED, received_at: iso(0) }, NOW);
    expect(d.proceed).toBe(true);
  });

  test('an in-flight attempt is left alone and is NOT reported a duplicate', () => {
    const d = decideEventDisposition(
      { status: PROCESSING, received_at: iso(5 * 1000) },
      NOW
    );
    expect(d.proceed).toBe(false);
    expect(d.reason).toBe('in-flight');
    // Load-bearing distinction: standing down because someone else is working
    // is not the same as standing down because the work is done. Conflating
    // them would report success for an order still in limbo.
    expect(d.duplicate).toBe(false);
  });

  test('a stale in-flight attempt is repaired, not abandoned', () => {
    const d = decideEventDisposition(
      { status: PROCESSING, received_at: iso(STALE_EVENT_MS + 1000) },
      NOW
    );
    expect(d.proceed).toBe(true);
    expect(d.reason).toBe('stale-repair');
    expect(d.duplicate).toBe(false);
  });

  test('the stale boundary is exclusive on the in-flight side', () => {
    const justInside = decideEventDisposition(
      { status: PROCESSING, received_at: iso(STALE_EVENT_MS - 1) },
      NOW
    );
    const justOutside = decideEventDisposition(
      { status: PROCESSING, received_at: iso(STALE_EVENT_MS) },
      NOW
    );
    expect(justInside.proceed).toBe(false);
    expect(justOutside.proceed).toBe(true);
  });

  test('a row with an unparseable timestamp proceeds rather than standing down', () => {
    for (const received_at of ['', 'not-a-date', null, undefined]) {
      const d = decideEventDisposition({ status: PROCESSING, received_at }, NOW);
      expect(d.proceed, `received_at=${JSON.stringify(received_at)}`).toBe(true);
      expect(d.reason).toBe('unknown-age-proceeding');
    }
  });

  test('an unrecognised status is treated as in-flight, not as processed', () => {
    // Forward compatibility: a status this build does not know about must never
    // be mistaken for terminal success, because that is the one branch that
    // skips real work.
    const d = decideEventDisposition(
      { status: 'some-future-state', received_at: iso(5 * 1000) },
      NOW
    );
    expect(d.duplicate).toBe(false);
    expect(d.proceed).toBe(false);

    const old = decideEventDisposition(
      { status: 'some-future-state', received_at: iso(STALE_EVENT_MS + 1) },
      NOW
    );
    expect(old.proceed).toBe(true);
  });

  test('a missing status is not read as processed', () => {
    const d = decideEventDisposition({ received_at: iso(1000) }, NOW);
    expect(d.duplicate).toBe(false);
  });

  /**
   * The invariant that keeps this layer subordinate to claimSession: exactly one
   * reachable state skips work while claiming the work is done. If a future edit
   * adds a second, that edit needs to justify itself against this test.
   */
  test('only one state in the whole space reports duplicate', () => {
    const states = [PROCESSED, PROCESSING, FAILED, 'weird', undefined];
    const ages = [0, 1000, STALE_EVENT_MS - 1, STALE_EVENT_MS, STALE_EVENT_MS * 10];

    const duplicates = [];
    for (const status of states) {
      for (const age of ages) {
        const d = decideEventDisposition({ status, received_at: iso(age) }, NOW);
        if (d.duplicate) duplicates.push(`${status}@${age}`);
      }
    }

    expect(duplicates.every((s) => s.startsWith(`${PROCESSED}@`))).toBe(true);
    expect(duplicates.length).toBe(ages.length);
  });

  test('every state in the space yields a well-formed disposition', () => {
    const states = [PROCESSED, PROCESSING, FAILED, 'weird', undefined, null];
    for (const status of states) {
      const d = decideEventDisposition({ status, received_at: iso(1000) }, NOW);
      expect(typeof d.proceed, `status=${status}`).toBe('boolean');
      expect(typeof d.duplicate).toBe('boolean');
      expect(d.reason.length).toBeGreaterThan(0);
    }
  });
});
