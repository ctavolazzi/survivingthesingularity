# Email Funnel — Implementation Notes

This site implements the reusable **email-capture funnel** pattern. The full,
generalized recipe (with rationale, gotchas, security checklist, and stack
adaptation) lives as a local Claude skill:

    ~/.claude/skills/email-funnel/        (SKILL.md + playbook.md)

## What's wired here

| Piece | File |
|-------|------|
| DB table + RLS migration | [sql/001_waitlist.sql](../sql/001_waitlist.sql) |
| Capture endpoint (security gauntlet + insert + email) | [src/routes/api/waitlist/+server.js](../src/routes/api/waitlist/+server.js) |
| Rate limiter (in-memory sliding window) | [src/lib/server/rateLimit.js](../src/lib/server/rateLimit.js) |
| Transactional welcome email (Resend, graceful) | [src/lib/server/email.js](../src/lib/server/email.js) |
| Privileged count + cache (social proof) | [src/lib/server/supabaseAdmin.js](../src/lib/server/supabaseAdmin.js) |
| Threshold-gated social proof (hidden below 100) | [src/routes/+page.server.js](../src/routes/+page.server.js) |
| Opt-in signup component | [src/lib/components/NewsletterSignup.svelte](../src/lib/components/NewsletterSignup.svelte) |
| Sticky scroll bar (lead-magnet driver) | [src/lib/components/StickyCaptureBar.svelte](../src/lib/components/StickyCaptureBar.svelte) |
| Soft content gate | [src/lib/components/EmailGate.svelte](../src/lib/components/EmailGate.svelte) |
| Lead magnet page | [src/routes/checklist/+page.svelte](../src/routes/checklist/+page.svelte) |

## Capture surfaces (all → one `waitlist` table, `source`-tagged)

- Hero inline form (`source=hero`)
- Sticky scroll bar → drives `/checklist` lead magnet
- Book/launch banner (`source=book-banner`)
- Footer CTA
- `/checklist` EmailGate (`source=checklist`)

## Operational notes

- **Migration must be run** in the Supabase SQL editor (`sql/001_waitlist.sql`).
  Until then the endpoint falls back to email-only inserts (consent flags lost).
- **Welcome email** needs `RESEND_API_KEY` + a verified sending domain
  (`EMAIL_FROM`) in prod env. Without the key, signups still succeed; the email
  is a logged no-op.
- **Social proof** is dormant until the count clears `SOCIAL_PROOF_THRESHOLD`
  (100) in `+page.server.js`.
- Stripe pre-order is the planned extension of this same table — see
  [PREORDER-ROADMAP.md](PREORDER-ROADMAP.md).
