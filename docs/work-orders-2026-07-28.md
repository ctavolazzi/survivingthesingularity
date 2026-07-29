# StS Work Orders — 2026-07-28

Generated from the Supabase + Stripe security audit. Every claim below was verified
against live production on 2026-07-28, not read from prior notes.

**Canonical working copy:** `~/Code/active/sts-v0.7.3` (branch `v0.7.3`, HEAD `5e9716e`)
**Live site:** https://survivingthesingularity.com
**Supabase project:** `skifaazhbxaddttbbfuo`
**CF Pages project:** `survivingthesingularity` (account `57c4a9e23c2d33763040f3020ce1dcda`)

Priority key: **P0** ship today · **P1** this week · **P2** before Stripe go-live · **P3** when convenient

---

## Status update, 2026-07-29

The per-work-order sections below are the original audit text and are left
unedited as the record of what was found. This block is the current state.

| ID | State | Note |
|----|-------|------|
| WO-01 | **Done** | sql/012 run against production. Needed a fix first: the default-privileges block raised `42501` on `supabase_admin` and, because everything runs in one transaction, took the whole lockdown down with it. Now caught per role. |
| WO-02 | **Done, proven** | `preorders` and `waitlist` went `400 23502` to `401 42501`; both control tables unchanged. Squat rejected. `preorder_counts` no longer readable. Counts unchanged at 8/5/12/0. Live signup POST still returns 201. |
| WO-03 | Open, needs you | The failing download URL has not been supplied yet. |
| WO-04 | **Done, verified** | Fallback to `fulfilled_sessions` implemented and tested in all four cases against live data, including the security case: a `cs_test_` string with no matching row does **not** mint a download. Recovered link served the real 48,776,826-byte zip. |
| WO-05 | **Closed, no action needed** | Project `cflncektpegrccomneqc` no longer exists. `dig` returns no A record and the connection fails, while `skifaazhbxaddttbbfuo` resolves and answers 401 from the same command. Supabase drops DNS on project deletion, so the leaked anon key authenticates against nothing. Checked by DNS rather than the dashboard search, which filters on project name and would not match a ref. |
| WO-06 | Downgraded to housekeeping | Old CF deployments still serve the bundle, but the key in it is now inert. No longer a security item. |
| WO-07 | **Do not do** | Was "skip, provided WO-05 lands". WO-05 landed by deletion, so rewriting public history to purge a dead credential buys nothing and risks both worktrees. |
| WO-08 | **Done, wider than specified** | Scope grew: `src/lib/supabase.js` was also a browser-capable client (`createBrowserClient`, exported but never called) and was the last consumer of `PUBLIC_SUPABASE_*`. Four files deleted, not three. The build now succeeds with no Supabase env set at all, so no publishable key is a build input. |
| WO-09 | Open, needs you | sql/011 (`email_deliveries`) still unrun; table still 404s. |
| WO-10 | Open, needs you | Blocked by WO-09. |
| WO-11 | **Done, verified** | Origin check now fails closed. Verified matrix: no Origin 403, forged Origin 403, correct Origin 201, no-Origin-but-same-origin-Referer 201, foreign Referer 403. **The durable rate limiter is still not fixed** and remains a decision for you, see below. |
| WO-12 | Open, needs you | Stripe still on test keys. WO-04 now unblocks it. |
| WO-13 | Awaiting go-ahead | Nothing committed yet. |

### Carried forward, not yet done

- **The rate limiter is still per-isolate.** `rateLimit.js` keeps counters in
  module scope, so on Cloudflare Pages an attacker distributing requests resets
  it without trying. The origin fix stops header-less scripted POSTs, which was
  the cheaper half. The durable half needs an infrastructure decision from you:
  Cloudflare WAF rate limiting (never reaches your isolate, no code change),
  Turnstile on the form (addresses automation directly), or KV/Durable Object
  counters (most code). Not chosen unilaterally because each adds a binding or a
  dashboard rule.
- **CSP still allows `connect-src https://*.supabase.co wss://*.supabase.co`**
  in `static/_headers`. That was for the browser client that no longer exists.
  It can probably be dropped, but only after confirming at runtime that nothing
  in the browser connects to Supabase, so it was left alone rather than changed
  blind.

---

## Summary table

| ID | Title | Owner | Priority | Blocks |
|----|-------|-------|----------|--------|
| WO-01 | Close the anon INSERT grant (run sql/012) | You | P0 | WO-02 |
| WO-02 | Prove the hole is shut | Claude | P0 | — |
| WO-03 | Capture the failing download URL | You | P0 | WO-04 |
| WO-04 | Success page falls back to fulfilled_sessions | Claude | P1 | — |
| WO-05 | Rotate the leaked Supabase project | You | P0 | WO-06 |
| WO-06 | Delete CF deployments serving the leaked key | You | P1 | — |
| WO-07 | Decide on purging the key from public git history | You | P2 | — |
| WO-08 | Delete the orphan browser Supabase client | Claude | P1 | — |
| WO-09 | Run sql/011 (email_deliveries) | You | P1 | WO-10 |
| WO-10 | Configure the Resend webhook | You | P1 | — |
| WO-11 | Harden the waitlist origin check | Claude | P2 | — |
| WO-12 | Stripe go-live checklist | You | P2 | — |
| WO-13 | Commit the staged security work | Claude | P1 | — |

---

## WO-01 — Close the anon INSERT grant

**Owner:** You (no CLI path exists; this project exposes no SQL-exec RPC, verified)
**Priority:** P0
**Estimated time:** 3 minutes
**Blocks:** WO-02

### Why

The publishable key can INSERT into `public.waitlist` and `public.preorders`. Re-probed
2026-07-28:

```
POST /rest/v1/preorders  {}  -> 400 23502   (grant + RLS policy already cleared)
POST /rest/v1/waitlist   {}  -> 400 23502   (grant + RLS policy already cleared)
POST /rest/v1/fulfilled_sessions  {}  -> 401 42501   (control: correctly locked)
POST /rest/v1/discord_applications {} -> 401 42501   (control: correctly locked)
```

A `23502` is a NOT NULL rejection, which means the request already passed both the table
grant and the RLS policy. The controls prove the probe discriminates.

This is not a spam risk. It is a silent denial of fulfillment. `preorders` carries
`unique (email, edition_type)`. An attacker who plants `{email, edition_type}` for a
target address causes the genuine service-role fulfillment insert to fail with `409 23505`.
`fulfillment.js` reads that as `duplicate = true`, and `duplicate` is exactly what
suppresses the admin alert. A paid order then vanishes from the table that exists as
redundancy against Stripe going down, and nobody is notified.

### Preconditions

None. The migration is idempotent and safe to run more than once.

### Steps

1. Open the Supabase SQL Editor for project `skifaazhbxaddttbbfuo`.
2. Paste the entire contents of `sql/012_lockdown_public_grants.sql`.
3. Run it.
4. Run the verify query at the bottom of the file (it is below the `commit;`, so run it as
   a second statement if the editor does not run it automatically).

### Verification

The verify query must show `anon_grants = none` for **every** row. Any row showing
`INSERT`, `SELECT`, `UPDATE`, or `DELETE` means the revoke did not take.

Also expect a notice if sql/011 has not run yet:
`011_email_deliveries.sql has not run yet - skipping that table.` That is expected and
harmless. See WO-09.

### Safety analysis (why this will not break the site)

Checked rather than assumed, because revoking anon INSERT would break signup if any code
path fell back to the anon client:

- `src/routes/api/waitlist/+server.js:77` is `supabaseAdmin ?? createSupabaseServerClient(event)`.
  The anon fallback is reachable only when `supabaseAdmin` is null.
- `SUPABASE_URL` (plain_text) and `SUPABASE_SERVICE_KEY` (secret_text) are both present in
  CF Pages production.
- Live probe: `/unsubscribe?token=<well-formed nonexistent uuid>` returned the `not_found`
  branch, not the `error` branch. `supabaseAdmin` is therefore non-null in production and
  the fallback is unreachable.
- Every other write path uses `supabaseAdmin` directly: `fulfillment.js`,
  `api/discord-application`, `api/unsubscribe`, `api/checklist-email`, `unsubscribe/+page.server.js`.
- `getBundleUrl()` signs storage URLs with the service role, which bypasses grants and RLS
  entirely. Downloads are unaffected.

### Rollback

If something unexpected breaks, restore the previous state with:

```sql
grant insert on public.waitlist  to anon;
grant insert on public.preorders to anon;
create policy "anon_insert_waitlist"  on public.waitlist  for insert to anon with check (true);
create policy "anon_insert_preorders" on public.preorders for insert to anon with check (true);
```

Do this only as an emergency measure. It reopens the vulnerability.

---

## WO-02 — Prove the hole is shut

**Owner:** Claude
**Priority:** P0
**Estimated time:** 2 minutes
**Blocked by:** WO-01

### Why

A migration that ran without error is not proof the grant is gone. The only proof is the
same probe that found the hole, returning a different answer.

### Steps

Re-run the probe matrix with the publishable key against all four tables, including the two
known-locked controls.

### Verification

Pass criteria, all four required:

| Table | Before | Required after |
|-------|--------|----------------|
| `preorders` | 400 `23502` | **401 `42501`** |
| `waitlist` | 400 `23502` | **401 `42501`** |
| `fulfilled_sessions` | 401 `42501` | 401 `42501` (unchanged control) |
| `discord_applications` | 401 `42501` | 401 `42501` (unchanged control) |

Then confirm the denial-of-fulfillment squat specifically fails: attempt to plant a
`{email, edition_type}` row and confirm it is rejected rather than accepted.

Finally, re-count all tables via the service role and confirm the totals are unchanged from
the audit baseline (`waitlist 8`, `preorders 5`, `fulfilled_sessions 12`,
`discord_applications 0`), so no probe row is left behind.

### Note on method

Always run the known-negative control in the same pass. Earlier in this audit an HTTP 204 on
anon PATCH/DELETE was briefly misread as "anon can update and delete". PostgREST returns 204
for a zero-row write regardless of authorization, and a control run against known-locked
tables returned 204 as well. The control is what makes a positive result meaningful.

---

## WO-03 — Capture the failing download URL

**Owner:** You
**Priority:** P0
**Estimated time:** 1 minute
**Blocks:** WO-04

### Why

Your report was that the asset pack download says it could not confirm your purchase. I
could not reproduce it. Every recorded purchase currently works:

- All 12 rows in `fulfilled_sessions` produce a signed URL on the live success page, `error: null`
- The signed URL serves the real file: HTTP 200, 48,776,826 bytes, `application/zip`

The wording you described does not exist in the codebase. The closest real string is
**"Could not verify your payment. Contact us for help."** at
`src/routes/early-access/success/+page.server.js:54`, which fires only when
`stripe.checkout.sessions.retrieve()` throws.

I reproduced that error by corrupting the `session_id`, which is the most likely cause:

| URL variant | Result |
|---|---|
| Intact 66-char `session_id` (control) | ok, download minted |
| Truncated to 48 chars | "Could not verify your payment" |
| Trailing `.` appended | "Could not verify your payment" |
| Trailing `%3E` appended | "Could not verify your payment" |

### Steps

1. Open the download email.
2. Right-click the "Download The Precedent File" button and choose Copy Link Address.
3. Paste the full URL here.
4. Also paste the exact on-screen wording you saw, word for word.

### Verification

The URL should look like:

```
https://survivingthesingularity.com/early-access/success?session_id=cs_test_b1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Count the characters after `session_id=`. It must be **66**. If it is shorter, or has
trailing punctuation, that is the entire bug and it lives in whatever rewrote the link
(email client, forwarding, a link tracker), not in the site.

If the URL is intact and 66 characters and it still fails, the cause is different and I will
need the timestamp of the attempt so I can correlate against Stripe.

---

## WO-04 — Success page falls back to fulfilled_sessions

**Owner:** Claude
**Priority:** P1
**Estimated time:** 30 minutes including a live test
**Blocked by:** WO-03 (not strictly; worth doing regardless of what WO-03 finds)

### Why

The success page is completely dependent on a live Stripe API call and has no fallback.
Your database already knows the purchase is real, and the bundle is a static file behind a
service-role signed URL that does not involve Stripe at all. Despite that, any Stripe
hiccup hard-fails a paying customer:

- a network blip or Stripe rate limit
- a rotated `STRIPE_SECRET_KEY`
- the test-to-live mode switch invalidating old session ids (see WO-12)
- one mangled character in the URL

The customer is then shown "Contact us for help" with no contact link, no retry, and no
recovery path. For a product whose whole fulfillment guarantee is redundancy against Stripe
going down, the customer-facing page having zero redundancy against Stripe going down is
the wrong shape.

### Steps

1. In `src/routes/early-access/success/+page.server.js`, in the `catch` around
   `stripe.checkout.sessions.retrieve()`, before returning the error: look up `sessionId`
   in `fulfilled_sessions` via `supabaseAdmin`.
2. If a row exists, that session was already verified as paid and fulfilled by either the
   success page or the Stripe webhook. Mint the bundle URL and return the success shape,
   with a flag noting Stripe was unreachable so the page can stay honest.
3. Do the same for the `payment_status !== 'paid'` branch only if a `fulfilled_sessions` row
   exists, since that row is written only after a confirmed payment.
4. If no row exists, keep the current error, but add a real support path: a mailto link and
   a short "email us your order ref" instruction using `sessionId.slice(0, 24)`.

### Verification

Live test, all four cases:

1. Intact valid `session_id` still works (no regression)
2. Valid `session_id` with a deliberately broken Stripe key still serves the download via
   the fallback
3. A `session_id` not present in `fulfilled_sessions` still shows the error, and the error
   now carries a working support link
4. A random `cs_test_` string that was never a real session still shows the error

### Design constraint

The fallback must key on `fulfilled_sessions`, never on the `session_id` string shape alone.
`fulfilled_sessions` rows are written only by the service role after Stripe confirmed
payment, which is what makes them trustworthy. Trusting a `cs_`-prefixed string by itself
would let anyone mint a download by guessing a URL.

---

## WO-05 — Rotate the leaked Supabase project

**Owner:** You
**Priority:** P0
**Estimated time:** 5 minutes
**Blocks:** WO-06

### Why

A working anon JWT for an older, different Supabase project is public. Verified live on
2026-07-28:

```
GET https://362ecb98.survivingthesingularity.pages.dev/_app/immutable/chunks/supabaseClient.CK6rhp95.js
-> HTTP 200, contains project ref cflncektpegrccomneqc and a live JWT (exp 2034)
```

It is public in two independent places:

1. The **public** GitHub repo history, commits `846dad0` and `c42f9b9`
2. Permanent Cloudflare Pages deployment hash URLs, which are served today

Good news, verified by enumerating every JWT in git history: **no `service_role` key was
ever committed.** The only JWT found carries `role: anon`.

The exposure severity depends entirely on one thing I could not check: whether project
`cflncektpegrccomneqc` still exists and still holds data. An anon key against a project with
permissive RLS is a live data breach. Against a deleted project it is inert.

### Steps

1. Log into the Supabase dashboard and check whether project `cflncektpegrccomneqc` still
   exists.
2. If it does not exist, this work order is complete. Note it and move to WO-06.
3. If it does exist:
   a. Check whether it holds any real data.
   b. If it is dead weight, **delete the project.** This is the cleanest fix and makes the
      leaked key permanently inert.
   c. If it is still in use, rotate its anon key immediately (Settings, API, then roll the
      key), and audit its RLS policies for every table before assuming the old key was
      harmless.

### Verification

After deletion or rotation, confirm the leaked key no longer authenticates:

```
POST https://cflncektpegrccomneqc.supabase.co/rest/v1/<any_table>
with the leaked key -> must return 401
```

I can run this probe for you once you confirm you own that project. I declined to hit it
unprompted because from outside it is indistinguishable from probing a third party's
database.

### Note

Rotation is the real fix. WO-06 and WO-07 reduce the exposure surface but neither can
un-publish a credential that has already been public in a public repository. Assume it is
archived by third parties.

---

## WO-06 — Delete CF deployments serving the leaked key

**Owner:** You
**Priority:** P1
**Estimated time:** 10 minutes
**Blocked by:** WO-05 (do the rotation first; this is cleanup, not the fix)

### Why

Cloudflare Pages keeps every historical deployment at a permanent hash subdomain forever.
Those URLs are not linked from anywhere, but they are public, they are indexed, and they
serve the old bundle containing the leaked key. Deleting the deployments removes one of the
two live copies.

### Steps

1. List deployments:
   ```
   npx wrangler pages deployment list --project-name survivingthesingularity
   ```
2. Identify deployments predating the Supabase project migration. `362ecb98` is a confirmed
   offender.
3. Delete each offending deployment through the Cloudflare dashboard (Workers and Pages,
   then the project, then Deployments, then the per-deployment delete action). Keep the
   current production deployment and at least one recent known-good rollback target.

### Verification

```
curl -s -o /dev/null -w "%{http_code}\n" \
  https://362ecb98.survivingthesingularity.pages.dev/_app/immutable/chunks/supabaseClient.CK6rhp95.js
```

Must return `404`. It currently returns `200`.

Then spot-check two or three other old deployment hashes from the list the same way.

### Caution

Do not delete the live production deployment. Confirm which one is production in the
dashboard before deleting anything.

---

## WO-07 — Decide on purging the key from public git history

**Owner:** You (decision), Claude (execution if you choose to)
**Priority:** P2
**Estimated time:** 45 minutes plus coordination cost

### Why

The leaked anon JWT is in the history of a **public** GitHub repo at commits `846dad0` and
`c42f9b9`. Purging it requires rewriting history with BFG or `git filter-repo` and a force
push.

### The honest tradeoff

**Purging does not undo the leak.** The key has been publicly cloneable. GitHub retains
unreferenced objects, forks keep their own copies, and third-party mirrors and code search
indexes may have cached it. Treat the credential as permanently compromised regardless.

**Therefore: WO-05 is the fix. WO-07 is hygiene.** If the project is deleted or the key is
rotated, a dead credential sitting in history is a cosmetic issue, not a security one.

**Costs of purging:** every commit SHA after the rewrite point changes. Both of your
worktrees (`sts-v0.7.3` and `survivingthesingularity`, currently on divergent branches) need
re-cloning or careful rebasing. Any open PR, any external clone, and any pinned SHA breaks.
Given you already have two divergent worktrees and a history of parallel sessions stashing
work, this carries real risk of losing uncommitted work.

### Recommendation

**Skip it,** provided WO-05 lands. Rotate or delete the old project, delete the old
deployments, and leave history alone. Revisit only if you later find the old project held
sensitive data under permissive RLS.

### Steps, if you choose to proceed anyway

1. Confirm both worktrees are fully committed and pushed. Verify with `git status` in each.
2. Take a full backup clone: `git clone --mirror` to a safe location.
3. Run `git filter-repo` with a replacement expression targeting the JWT string.
4. Force push all branches and tags.
5. Re-clone both working copies from scratch. Do not attempt to rebase existing ones.
6. Ask GitHub Support to garbage-collect unreferenced objects, since a force push alone does
   not remove them from the public API.

---

## WO-08 — Delete the orphan browser Supabase client

**Owner:** Claude
**Priority:** P1
**Estimated time:** 15 minutes

### Why

`src/lib/utils/supabaseClient.js` builds a browser Supabase client from
`PUBLIC_SUPABASE_ANON_KEY`. It is currently harmless only by accident: the two modules that
import it, `src/lib/stores/researchLinksStore.js` and `src/lib/stores/tacticLibrary.js`, are
themselves orphans that no route imports. Verified: the key is absent from the live bundle
today.

That is not a safe resting state. It is one `import` away from shipping the publishable key
to every browser. Combined with WO-01 being open, that would turn the denial-of-fulfillment
attack from theoretical into remotely exploitable by anyone who views source.

This is not hypothetical. The already-leaked file is literally named
`supabaseClient.CK6rhp95.js`. This exact pattern is how the first leak happened.

It also matters because the Supabase onboarding boilerplate actively recommends this
pattern. Following that guide would recreate the vulnerability.

### Steps

1. Confirm the orphan status still holds (nothing outside the stores imports them, and no
   route imports the stores).
2. Delete all three files:
   - `src/lib/utils/supabaseClient.js`
   - `src/lib/stores/researchLinksStore.js`
   - `src/lib/stores/tacticLibrary.js`
3. Note that these stores query tables named `tactics` and `research_links`, neither of
   which exists in this database, so they were already non-functional.
4. Add a short note to `README.md` recording that this project is server-side only through
   the service role and does not use a browser Supabase client, so the next person does not
   reintroduce one.

### Verification

1. `npm run build` succeeds
2. Grep the built output for `sb_publishable_` and for `eyJhbGciOi`, expecting no matches
3. After deploy, re-check the live bundle chunks the same way

### Standing rule this establishes

Do not create `src/lib/supabaseClient.js` or any browser-side Supabase client in this
project. All database access goes through server endpoints using the service role. If a
future feature genuinely needs public read access, add a server endpoint for it rather than
shipping a key.

---

## WO-09 — Run sql/011 (email_deliveries)

**Owner:** You
**Priority:** P1
**Estimated time:** 2 minutes
**Blocks:** WO-10

### Why

`public.email_deliveries` does not exist. Confirmed: the table 404s with `PGRST205`.

Nothing currently records email outcomes. A bounced download confirmation and a delivered
one leave the database in an identical state, so "did this customer actually receive their
bundle link?" cannot be answered from your own data. The only record is Resend's dashboard,
which is a third party with roughly 30 day retention.

For a store whose fulfillment guarantee depends on an email arriving, that is the wrong
shape.

Two code paths already write to this table and are currently failing silently:
`src/lib/server/email.js:41` and `src/routes/api/webhooks/resend/+server.js:162`.

### Steps

1. Open the Supabase SQL Editor for `skifaazhbxaddttbbfuo`.
2. Paste and run the full contents of `sql/011_email_deliveries.sql`.
3. If you have already run WO-01, also re-run just the `email_deliveries` guard block from
   `sql/012` so the new table gets locked down too. The simplest correct move is to re-run
   all of `sql/012`, which is idempotent.

### Verification

```
GET /rest/v1/email_deliveries  with the service role key  -> 200 (empty array)
GET /rest/v1/email_deliveries  with the publishable key   -> 401 42501
```

The second is the one that matters. sql/011 enables RLS on the table, and sql/012 revokes
the grants. If the publishable key can read it, run sql/012 again.

### Order note

sql/012 is written to run before or after sql/011 in either order. If you run 012 first it
emits a notice and skips the table, which is why re-running 012 after 011 is the correct
finishing move.

---

## WO-10 — Configure the Resend webhook

**Owner:** You
**Priority:** P1
**Estimated time:** 10 minutes
**Blocked by:** WO-09

### Why

The endpoint is live but refuses everything because no secret is configured. Verified:

```
POST https://survivingthesingularity.com/api/webhooks/resend  {}  -> 503
```

Source: `src/routes/api/webhooks/resend/+server.js:78` logs
`RESEND_WEBHOOK_SECRET not set; rejecting.` and returns 503.

The verification code itself was audited and is correct: SubtleCrypto HMAC, constant-time
comparison, a 5 minute replay window, and rank-ordered status updates that cannot downgrade
a delivered email back to sent. It is simply unproven end to end because it has never
received a real event.

### Steps

1. In the Resend dashboard, create a webhook endpoint:
   - URL: `https://survivingthesingularity.com/api/webhooks/resend`
   - Events: `email.sent`, `email.delivered`, `email.bounced`, `email.complained`,
     `email.delivery_delayed`
2. Copy the signing secret Resend generates (`whsec_...`).
3. Add it to Cloudflare Pages production as a **secret**, not plain text:
   ```
   npx wrangler pages secret put RESEND_WEBHOOK_SECRET --project-name survivingthesingularity
   ```
4. Redeploy, since Pages env changes do not apply to existing deployments.

### Verification

1. `POST /api/webhooks/resend` with an empty body must now return **400** (bad signature),
   not 503. That single status change proves the secret is loaded.
2. Send yourself a real transactional email through the site.
3. Confirm a row appears in `email_deliveries` with status `sent`, then updates to
   `delivered` within a minute or two.
4. Use Resend's "send test event" if available and confirm it is accepted.

### Related cleanup while you are in the Pages settings

`RESEND_API_KEY` is currently stored as **plain_text** in CF Pages production. It should be
`secret_text`. Fix it in the same pass:

```
npx wrangler pages secret put RESEND_API_KEY --project-name survivingthesingularity
```

Then delete the plain-text variable of the same name so there is exactly one definition.
Rotate the key afterward, since a plain-text value was readable by anyone with dashboard
access.

---

## WO-11 — Harden the waitlist origin check

**Owner:** Claude
**Priority:** P2
**Estimated time:** 20 minutes

### Why

Two weaknesses compound in `src/routes/api/waitlist/+server.js`.

**The origin check fails open.** Line 18 reads `if (origin && origin !== event.url.origin)`.
A request with no `Origin` header at all skips the check entirely. Verified live: a POST
with a forged Origin returns 403, and a POST with no Origin header returns 201.

**The rate limiter is close to useless in production.** `rateLimit.js` keeps counters in
module scope, which on Cloudflare Pages means per-isolate. Isolates are created and
destroyed constantly and there are many concurrently, so an attacker distributing requests
naturally resets the counter without trying.

Together the endpoint is floodable, and every insert fires a Resend welcome email. The cost
is not database rows. It is your Resend quota and your sender reputation, which is much
harder to repair than a table.

### Steps

1. Decide the policy for a missing `Origin` header. Rejecting outright is the correct
   default for a browser-only endpoint, but confirm no legitimate client omits it.
2. Change the check to require a valid same-origin `Origin`, or accept a matching `Referer`
   as a fallback before rejecting.
3. Replace or back the in-memory rate limiter with durable shared state. Options in
   preference order:
   - Cloudflare KV or a Durable Object keyed by IP
   - Cloudflare WAF rate limiting rules at the edge, which never reach your isolate
   - Cloudflare Turnstile on the signup form, which addresses the automation directly
4. Independently cap the outbound email side, so a flood cannot become a Resend bill even if
   the rate limiter is bypassed.

### Verification

1. POST with no `Origin` header must be rejected
2. POST with a forged `Origin` must still return 403
3. A normal signup from the site must still succeed (no regression)
4. Exceed the limit from one IP, then confirm the limit persists across repeated attempts
   over several minutes rather than resetting

### Note

Fix this after WO-01. WO-01 is what stops a direct-to-PostgREST write that skips this
endpoint's checks entirely. Hardening the endpoint while the database accepts anonymous
inserts around it would be securing the door and leaving the window open.

---

## WO-12 — Stripe go-live checklist

**Owner:** You
**Priority:** P2
**Estimated time:** 45 minutes

### Why

Production is on **TEST** keys. Re-verified 2026-07-28: all 12 sessions in
`fulfilled_sessions` are `cs_test_`. The store currently collects no money.

An earlier memory claiming the store went live on 2026-07-16 was wrong and has been
corrected. Verify live rather than trusting any status line, including this one.

Also currently failing by design: Author's Edition checkout returns 503 because
`STRIPE_PRICE_ID_AUTHORS` is unset in production. That is an intended safe failure, not a
bug, but it must be resolved before selling that edition.

### Steps

1. Complete Stripe account activation, including business details and a payout bank account.
2. Create **live-mode** products and prices. Test-mode price ids do not exist in live mode.
3. Update these CF Pages production secrets with their live values:
   - `STRIPE_SECRET_KEY` (`sk_live_...`)
   - `STRIPE_PRICE_ID`
   - `STRIPE_PRICE_ID_STANDARD`
   - `STRIPE_PRICE_ID_AUTHORS` if selling that edition, otherwise leave unset so it keeps
     failing safely
4. Update `STRIPE_PUBLIC_KEY` to the live publishable key.
5. **Register a separate live-mode webhook endpoint.** This is the step most easily missed.
   The test-mode signing secret does not carry over. Create the live endpoint at
   `https://survivingthesingularity.com/api/webhooks/stripe`, then set its own new
   `whsec_...` as `STRIPE_WEBHOOK_SECRET`.
6. Redeploy.

### Verification

Verify live, never from code review. Run one real transaction with a real card:

1. Complete a purchase and confirm the session id begins `cs_live_`
2. Confirm a `fulfilled_sessions` row is written
3. Confirm a `preorders` row is written
4. Confirm the customer download email arrives
5. Confirm the admin alert email arrives
6. Confirm the download link serves the real zip
7. Confirm the Stripe webhook shows a 200 in the Stripe dashboard, not 400 or 503
8. Confirm the payment appears in your Stripe balance
9. Refund the test purchase

### Known live-mode consequence

Existing customers holding download links with `cs_test_` session ids will hit "Could not
verify your payment" once the live key is active, because a live key cannot retrieve a test
session. **WO-04 fixes exactly this**, since those sessions still exist in
`fulfilled_sessions`. Ship WO-04 before going live, or those 12 links break permanently.

---

## WO-13 — Commit the staged security work

**Owner:** Claude
**Priority:** P1
**Estimated time:** 5 minutes
**Requires:** your explicit go-ahead

### Why

The audit produced real files that are staged but uncommitted. Per house rules, uncommitted
work in a repo with parallel sessions is at risk of being stashed or lost, and nothing gets
committed without you asking.

### Currently staged

- `sql/012_lockdown_public_grants.sql` (new)
- `sql/001_waitlist.sql`, `sql/003_preorders.sql`, `sql/004_fulfilled_sessions.sql`,
  `sql/006_preorders_standard_edition.sql`, `sql/007_authors_edition_no_cap.sql` — these were
  **untracked on every branch**, meaning the schema was not rebuildable from the repo. That
  is arguably the most important thing this audit fixed.
- `.env.example` — documents `STRIPE_WEBHOOK_SECRET` and `RESEND_WEBHOOK_SECRET`, notes the
  plain_text issue, removes the dead `BOOK_ACCESS_PASSWORD` entry, and drops an em dash

### Explicitly NOT to be committed

The working tree also contains unrelated unstaged changes that are not part of this audit and
must be left alone:

- `src/lib/data/book/11-chapter9.md`, `12-chapter10.md`, `13-chapter11.md`, `15-chapter13.md`
- `src/lib/data/book/manuscript-index.json`
- `static/images/optimized/*` (cover images and new ch07 assets)
- `.empirica_reflex_logs/`
- `docs/next-steps-2026-07-27.html`

### Steps

1. Confirm `git status` still shows the same staged set and nothing extra.
2. Commit only the staged paths, naming them explicitly rather than using `git add -A`.
3. Do not push unless you ask.

### Suggested commit message

```
Lock down public grants and recover untracked schema migrations

sql/012 drops the anon insert policies on waitlist and preorders, revokes
table grants on all five tables plus preorder_counts, sets security_invoker
on that view, and revokes default privileges so future tables are not
auto-granted to anon.

Probed against production: the publishable key could insert into waitlist
and preorders (400 23502, past both grant and policy), while locked control
tables returned 401 42501. The exploit is a silent denial of fulfillment via
the unique(email, edition_type) constraint, which fulfillment.js reads as a
duplicate and which suppresses the admin alert.

Also adds sql/001, 003, 004, 006 and 007, which were untracked on every
branch, so the schema is rebuildable from the repo for the first time.

Updates .env.example to document STRIPE_WEBHOOK_SECRET and
RESEND_WEBHOOK_SECRET and to drop the dead BOOK_ACCESS_PASSWORD entry.
```

### Verification

`git show --stat HEAD` lists exactly the seven intended files and nothing from the book or
image sets.

---

## Recommended execution order

**Today (P0):** WO-01, then WO-02. WO-03 in parallel, it costs you one minute. WO-05.

**This week (P1):** WO-04 (needed before go-live regardless), WO-08, WO-09, WO-10, WO-06, WO-13.

**Before Stripe go-live (P2):** WO-11, WO-12, and a decision on WO-07.

The two fastest unblocks are WO-01 (one paste into the SQL Editor) and WO-03 (one
right-click). Those close the open security finding and the download bug in the same pass.
