# Surviving the Singularity: remediation and launch plan

## 1. Document control

| Field | Value |
|---|---|
| **Document ID** | STS-PLAN-0.0.1 |
| **Version** | 0.0.1 |
| **Created** | 2026-07-29 |
| **Status** | Active |
| **Owner** | Chris Tavolazzi |
| **Scope** | Live site remediation, offer architecture, demo MVP, launch sequencing |
| **Supersedes** | Nothing. First revision. |
| **Companion docs** | `design/01-design-doc.txt`, `design/02-design-doc.md`, `design/03-design-doc.html` |
| **Working copy** | `~/Code/active/sts-mvp` |
| **Live source** | `~/Code/active/sts-v0.7.3` (git worktree, branch `v0.7.3`) |
| **Production pin** | deployment `af13a3c9`, source `332fdfd`, branch `main` |
| **Evidence ledger** | `~/Code/active/STS-VERIFICATION-LEDGER.md` (append-only) |

---

## 2. How to use this document

### 2.1 Identifier scheme

Every item has a stable, greppable ID. IDs are never reused or renumbered.

| Prefix | Meaning | Example | Count |
|---|---|---|---:|
| `F-nn` | Finding. A defect measured on the live site or in the source. | `F-03` | 9 |
| `D-nn` | Decision required. Blocks work until answered by a human. | `D-01` | 4 |
| `WS-x` | Workstream. A grouping of tasks with a shared goal. | `WS-B` | 6 |
| `x-nn` | Task, prefixed by its workstream letter. | `B-04` | 45 |
| `R-nn` | Risk. | `R-02` | 6 |
| `V-nn` | Verification gate. Definition of done for a workstream. | `V-01` | 6 |

To find everything about one item: `grep -rn "B-04" PLAN.md`.

### 2.2 Status legend

| Token | Meaning |
|---|---|
<span class="st st-done">DONE</span> | Complete and verified. Evidence recorded in the task row. |
<span class="st st-prog">IN PROGRESS</span> | Started, not finished. |
<span class="st st-todo">TODO</span> | Ready to start. Nothing blocks it. |
<span class="st st-block">BLOCKED</span> | Cannot start. The blocker is named in the row. |
<span class="st st-dec">DECISION</span> | Waiting on a `D-nn` answer from Chris. |
<span class="st st-defer">DEFERRED</span> | Deliberately not now. The gate that releases it is named. |

### 2.3 Priority scheme

| Level | Meaning |
|---|---|
`P0` | Blocks taking money. Nothing downstream matters until these close. |
`P1` | Blocks launching honestly. Ship before any promotion. |
`P2` | Should ship with launch, not fatal if it slips a week. |
`P3` | Post-launch. |

### 2.4 The one rule this document enforces

> Any task that changes what the customer is promised must change
> `app/src/lib/offer.js` (demo) or its production equivalent, and never a
> component's inline prose. Offer language typed directly into a page is the
> defect class that produced `F-01`.

---

## 3. Executive summary

### 3.1 Situation

The live site converts, and the underlying book is in good shape: 23 of 23
precedents indexed, zero dangling cross references, 90,623 words, security
headers all live, database locked down. That work is real and none of this plan
disturbs it.

Three things are nonetheless true and blocking:

1. The site describes the same $5 purchase three different ways, and the legal
   layer describes a different transaction than the sales layer (`F-01`).
2. The store has never accepted a real dollar, and there is no live-mode webhook
   endpoint, so switching keys today would take payments and record none of them
   (`F-04`, `F-05`).
3. The homepage claims 29 documented cases where the project's own harness counts
   23 (`F-02`).

### 3.2 Critical path

```
D-01 (ratify the offer sentence)
  |
  +--> A-01..A-06  reconcile sales copy and /policies      P0
  |
  +--> C-01..C-04  fix and derive the counts               P1
  |
  v
B-01..B-07  checkout: fix the button, create the live
            webhook, flip keys, take one real dollar       P0
  |
  v
V-04  one real transaction verified end to end
  |
  v
WS-F  launch campaign (already designed, gated on V-04)
```

### 3.3 What is already built

The demo MVP exists, builds clean, and runs. See `WS-D`. It is the argument for
the offer architecture rendered as a working site, including a `/policies` page
that derives its refund clause from the same object the hero reads.

---

## 4. Findings register

Measured 2026-07-29 against production `af13a3c9` / source `332fdfd`. Each row
names the method, so each is re-runnable.

| ID | Severity | Finding | Method | Status |
|---|---|---|---|---|
| `F-01` | **P0** | The $5 offer is described three ways. Homepage and `/early-access` sell digital access plus a 50% launch coupon. `/policies` sells merchandise, offering refunds "prior to shipment" and citing the FTC Mail, Internet, or Telephone Order Merchandise Rule. `/terms` says the site is "informational only" and never mentions a sale. **It was worse than three: `/about`, `/checklist`, the navbar, the success page, and the confirmation email each carried a sixth, seventh, eighth, ninth and tenth wording.** | Read all four rendered surfaces plus source, then a lint sweep that found five more | <span class="st st-done">CLOSED</span> `WS-A` |
| `F-02` | **P1** | Homepage claims "The Precedent File: 29 documented cases". The book contains 23, `P-01` through `P-23`. Likely origin: the site has 29 pages. | `python3 scripts/sts.py verify` reports "all 23 present in the book and indexed in Appendix D" | <span class="st st-done">CLOSED</span> `C-01` |
| `F-03` | **P0** | Bottom buy button on `/early-access` binds `disabled` to `checkoutLoading` only, unlike the top button which also requires a valid email. Button looks clickable, does nothing, and renders its error message 4052px away in a 720px viewport. | Playwright, production, measured | <span class="st st-done">CLOSED</span> `B-01` `B-02` |
| `F-04` | **P0** | Store has never taken real money. 92 Stripe sessions with `livemode=true` count 0. 24 charges with 0 livemode paid charges. | Stripe API as authoritative ledger | <span class="st st-todo">TODO</span> `B-04` |
| `F-05` | **P0** | No live-mode webhook endpoint exists. `webhook_endpoints` count 1, `livemode=false`. Flipping to live keys without creating one loses every order silently. | Stripe API | <span class="st st-todo">TODO</span> `B-03` |
| `F-06` | P2 | 10 paid test sessions have no corresponding app row (23 complete/paid sessions vs 13 `fulfilled_sessions`). All test mode, no money lost, but the reconciliation gap is real. | Stripe to Supabase reconciliation | <span class="st st-todo">TODO</span> `B-06` |
| `F-07` | P2 | `preorder_counts` table exists in the schema and is referenced nowhere in `src/`. Plumbing without wiring. | `rg preorder_counts src/` returns nothing | <span class="st st-defer">DEFERRED</span> `F-03` gate |
| `F-08` | P2 | `/policies` says "As of May 2026, no firm shipping date has been set" while `V0.7.3-SCOPE.md` says the book ships September 2026 with the preorder campaign in August. Stale by two months. | Source comparison | <span class="st st-done">CLOSED</span> `A-05` |
| `F-09` | P3 | Local `RESEND_API_KEY` is dead, so email reconciliation against the Resend API is impossible from this machine. Production has its own key and `fulfilled_sessions` shows 13 rows all `status: delivered`, so prod delivery probably works, but "probably" is not adequate under a promise phrased "I will ensure". | Bogus-key and real-key controls both return identical 400 | <span class="st st-block">BLOCKED</span> needs a valid key |

---

## 5. Decisions

`D-01`, `D-02` and `D-03` were **RATIFIED by Chris on 2026-07-29** and are
recorded below as answers, not as proposals. The production offer module
`~/Code/active/sts-v0.7.3/src/lib/offer.js` is the executable copy of this
section; where prose here and that file disagree, the file is right and this
section is stale.

### 5.1 `D-01` What does five dollars actually buy? RATIFIED

**Answer, and it is not the recommended default that was on the table.** The 50%
discount survives, but it now attaches specifically to the **Print Edition**
rather than to the book in general. That is better than the proposed default,
because it keeps the incentive while pointing it at a real physical good
carrying its own separate price, instead of discounting a digital edition that
the offer now gives away.

Five dollars, once, buys:

| # | Item | Available |
|---:|---|---|
| 1 | All the digital content. Full stop. | immediately |
| 2 | Read the current pre-release version of the book on the site. | immediately |
| 3 | The Precedent File, 23 documented cases, every source. | immediately |
| 4 | A permanent spot on the early-access list, until they ask to come off. | immediately |
| 5 | Only substantial version updates get sent. No weekly noise to this list. | immediately |
| 6 | A place in line to buy the **Print Edition** at 50% off, as an early supporter. | future |
| 7 | **Grandfathering.** When the membership or subscription launches, preorder buyers never pay it. | future |

Item 7 is economically the most valuable thing in the list, so it is stated as a
headline benefit and rendered last in the offer table as the closer, not buried.

After the preorder window closes that exclusive price is gone, and new arrivals
who want updates buy a membership or subscription.

**Legal consequence, load-bearing:** the $5 SKU still ships nothing. It grants
digital access plus a discount right on a future purchase. So
`shipsPhysicalGoods` stays **false**, the FTC Mail, Internet, or Telephone Order
Merchandise Rule does not apply to it, and `/policies` must **not** carry a
shipment clause for it. The Print Edition is a separate SKU and gets its own
terms when it exists. Do not flip the flag to cover it.

### 5.2 `D-02` What is the bounded scope of "forever"? RATIFIED

Bounded on three axes, all three stated on the page rather than in terms:

1. **Cohort-limited.** It belongs to preorder buyers, and the window closes.
2. **Opt-out at any time by request.** One reply is enough.
3. **Substantial version updates only.** Not every small change.

That is a real long-term obligation, bounded on every axis, which is what made
it safe to sell.

### 5.3 `D-03` Does the Print Edition get sold, and at what price? RATIFIED

Yes, as **numbered Print Editions**, not a single release. A new Print Edition
ships only when enough has changed to warrant one, which Chris estimates at
every one to two years, tracking the tech industry's own release cadence. Print
is a separate product at a real price and is not bundled into the $5.

The term of art is **"Print Edition"**, capitalised. Not "printed copy", not
"physical edition", not "hardback".

### 5.3.1 The cadence conflict, resolved

The handoff flagged a contradiction: "printed versions available as editions,
updated monthly, and released every 1-2 years". Chris resolved it on 2026-07-29:

| Surface | Cadence |
|---|---|
| Research | Daily. |
| The site | New coverage as often as daily, depending on the news cycle and whether there is anything worth pushing that day. |
| Newsletter | Weekly. |
| The book itself, digital | Monthly. |
| **Print Edition** | A new one every year or two. |

The site line is deliberately hedged in the shipped copy. "Updated daily" flat
would be a promise that has to be kept on a slow news week, and house rule 5
forbids a false live-data claim. `cadence.site` in `offer.js` states the true
thing.

### 5.4 `D-05` Which of the five proposed additions to the offer get shipped? OPEN

**Status:** <span class="st st-dec">DECISION</span>. **Blocks:** nothing
currently in flight. `WS-A` shipped the seven ratified items only.

Chris asked for input on what else the $5 should carry. Five candidates were
proposed, chosen for near-zero marginal cost, real perceived value, and
deliverability by one person on a health-constrained runway. **None are
implemented**, because none are ratified, and shipping an unratified promise to
a paying customer is the exact defect class this plan exists to close.

| ID | Proposal | Cost to deliver |
|---|---|---|
| `D-05a` | **Name in the Print Edition.** An opt-in "Founding Readers" appendix listing preorder supporters by name in every Print Edition. | One page of layout. Needs a name field at checkout and a trivial opt-out. |
| `D-05b` | **First read.** Preorder buyers get each substantial update before the public post goes live. | Send ordering only. |
| `D-05c` | **Name the grandfathering as a benefit.** Already ratified as item 7; this was only about stating it loudly. | Done, shipped in `WS-A`. |
| `D-05d` | **Reader questions shape coverage.** Buyers can reply to any update and it gets read, with no promise it gets answered. | Attention only. The "read, not necessarily answered" phrasing is what keeps it sustainable. |
| `D-05e` | **Version-pinned archive.** Every version they were a supporter for stays downloadable. | Already technically possible: the downloads bucket is private and the signed-URL path exists. |

**Explicitly not proposed:** Discord, live calls, or office hours. One person
doing daily research cannot also staff a community, and a dead Discord is worse
than no Discord.

### 5.4 `D-04` Does the new site replace the current homepage, or ship alongside it?

**Blocks:** `D-05` sequencing of `WS-D` into production.

**Recommended default:** port the offer architecture (`offer.js`, derived stats,
the reconciled `/policies`) into the existing site first, as that is where the
P0 findings live. Treat the new homepage layout as a second, separable change.
Do not couple a legal fix to a redesign.

---

## 6. `WS-A` Offer reconciliation

**Goal:** one offer, stated identically on every surface including the legal
pages, traceable to a single source of truth.

**Verification gate:** `V-01`.

| ID | Pri | Task | Status | Blocked by | Done when |
|---|---|---|---|---|---|
| `A-01` | P0 | Create the production offer module at `src/lib/offer.js` in the live repo. | <span class="st st-done">DONE</span> | none | Frozen object, `refundClause()`, `offerBlurb()`, `cadence`. `npm run build` passes. Carries the 7 ratified items, the excluded Print Edition row, `foreverScope`, `windowClose`, `precedentCount`, `shipsPhysicalGoods:false`. |
| `A-02` | P0 | Render the `/early-access` hero, includes grid, and bottom CTA from the offer module. Delete the inline prose. | <span class="st st-done">DONE</span> | `A-01` | Rendered `/early-access` carries `offer.sentence` twice; the 4 hand-written cards are replaced by a 7-item `{#each offer.included}`. |
| `A-03` | P0 | Render the bounded "forever" scope on the page rather than buried in terms. | <span class="st st-done">DONE</span> | `D-02` | `.ea-scope` block on `/early-access` renders `foreverScope` + `windowClose`; `/policies` renders both again in its offer section. |
| `A-04` | P0 | Derive `/policies` refund language from `refundClause()`. Remove the shipment clause while `shipsPhysicalGoods` is false. | <span class="st st-done">DONE</span> | `A-01` | Rendered `/policies`: `prior to shipment` 0 hits, `Merchandise Rule` 0 hits, derived clause reads "Nothing is shipped, so no shipment date applies and no shipping policy is involved." |
| `A-05` | P1 | Fix the stale "As of May 2026, no firm shipping date" line. | <span class="st st-done">DONE</span> | none | `F-08` closed. 0 hits for `As of May 2026`. Replaced with a September 2026 target explicitly labelled a target, not a guarantee. |
| `A-06` | P1 | Add the explicit excluded row to the live site. | <span class="st st-done">DONE</span> | `D-03` | "Not included: the Print Edition itself." renders full-width at the same surface, padding, and type sizes as the included cards. Screenshot verified at 1280 and 390. |
| `A-07` | P1 | Update `/terms` so it acknowledges that a sale occurs on this site. | <span class="st st-done">DONE</span> | `A-01` | New section 2 "Purchases and digital access", sections 2-15 renumbered to 3-16, links to `/policies` and states it governs on conflict. |
| `A-09` | P0 | **Surfaces the plan missed.** The lint found `/about`, `/checklist`, `Navbar.svelte`, `/early-access/success`, and the confirmation email all carrying independent offer prose. | <span class="st st-done">DONE</span> | `A-01` | All five now derive. The email's promo-code block re-describes the 50% as attaching to the Print Edition and says plainly there is nothing to redeem against yet. |
| `A-08` | P2 | Add a build-time assertion that fails the build if offer language appears outside the offer module. | <span class="st st-done">DONE</span> `297543b` | `A-01` | `scripts/check-offer-drift.mjs`, wired into `prebuild`. Derives all 5 rules FROM `offer.js` at lint time so a price change retargets it instead of blinding it. Found **12** hardcoded surfaces, not the 6 a hand grep found, across 6 files including both homepage buy buttons and the receipt header. Verified before being trusted: 5/5 planted violations caught, 0/6 negative-control classes false-positived, `npm run build` exits 1 on a plant with `vite build` never reached. Offer copy byte-identical after the fixes. Ledger round 5. |

---

## 7. `WS-B` Checkout go-live

**Goal:** one real dollar moves from a real card and every downstream effect
fires. This is the only workstream that unblocks promotion.

**Verification gate:** `V-04`. **Order matters. Do not reorder `B-03` and `B-04`.**

| ID | Pri | Task | Status | Blocked by | Done when |
|---|---|---|---|---|---|
| `B-01` | P0 | Fix the bottom buy button binding on `/early-access` so `disabled` also requires `emailOk`, matching the hero button. | <span class="st st-done">DONE</span> | none | Playwright, 1280x720 and 390x844: bottom button `disabled=true` before a valid email, `false` after, and it agrees with the hero button in both states. The bottom CTA now carries its own email field bound to the same value, so a customer who scrolls straight to it can actually buy. See 7.1 |
| `B-02` | P0 | Move the checkout error message so it renders adjacent to the button that produced it, not 4052px away. | <span class="st st-done">DONE</span> | `B-01` | Measured **gap = 16px**, down from 4052px, at both 1280x720 and 390x844, with the endpoint intercepted so a real error state actually rendered. Button and error confirmed on screen together. |
| `B-03` | P0 | **Create the live-mode Stripe webhook endpoint** pointing at `/api/webhooks/stripe`. | <span class="st st-todo">TODO</span> | none | Stripe API shows `webhook_endpoints` with a `livemode=true` row. `F-05` closed. |
| `B-04` | P0 | Set the live-mode signing secret and switch `STRIPE_SECRET_KEY` to the live key in Cloudflare Pages secrets. | <span class="st st-block">BLOCKED</span> | `B-03` | `wrangler pages secret list` shows the live key. Checkout probe reports `mode live`. |
| `B-05` | P0 | Add the missing `STRIPE_PRICE_ID_AUTHORS` secret. Code reads it, the secret inventory does not contain it. | <span class="st st-todo">TODO</span> | none | `wrangler pages secret list` includes it. |
| `B-06` | P1 | Close the reconciliation gap behind `F-06`: 10 paid sessions with no app row. Add an alert when a paid session has no `fulfilled_sessions` row within N minutes. | <span class="st st-prog">CODE DONE, NOT CLOSABLE</span> `36c0edb` | none | **Acceptance criterion NOT met.** Built: `unreconciled_paid_sessions` view in sql/014, `reconcile.js`, `reconcileFormat.js` (14 tests), `sendAdminReconciliationAlert`, and `GET /api/admin/reconcile` behind a bearer token proven to fail SHUT (10/10 live probes). **Two gaps:** (1) nothing calls it, Pages has no cron, and an on-demand check nobody demands is not an alarm; (2) sql/014 has never run, so the view is unverified against real Postgres. The deliberately-dropped-webhook test needs a database. |
| `B-07` | P0 | **Take one real dollar from one real card.** Confirm charge, `fulfilled_sessions` row, transactional email, and working download link. | <span class="st st-block">BLOCKED</span> | `B-04` | All four effects observed and recorded in the verification ledger. `V-04` passes. |
| `B-08` | P1 | Add webhook event-id idempotency so identical signed bytes replayed twice are recorded once. | <span class="st st-prog">CODE DONE, NOT CLOSABLE</span> `36c0edb` | none | **The naive reading of this task was a trap and is documented in `webhookEventPolicy.js`: Stripe REUSES the event id on retries**, so dedup on "seen before" would strand a paid order whose first attempt failed, reintroducing the exact bug sql/013 removed. Only a terminal `processed` earns a skip. 14 tests plus a mutation test prove the retry path is not skipped. Handler wired at all 9 exit paths and probed live: 4 signed events to 200, 5 negative controls to 400. **Gap:** sql/014 never executed, so the insert, the 23505 conflict path and the outcome update are unverified against real Postgres. |
| `B-09` | P2 | Reject future-dated webhook timestamps. Stripe's `constructEvent` enforces tolerance on the past side only; `t+600s` currently returns 200. | <span class="st st-todo">TODO</span> | none | `t+600s` returns 400. **REPRODUCED 2026-07-29 with a forged signature against the live handler**, so this is measured rather than inferred: `t+600s` returns 200, `t-600s` returns 400. The harness that proves it is the same signature-forging probe used for `B-08`, so the fix is cheap to verify when someone takes it. |
| `B-10` | P2 | Shorten the 7 day signed download URL TTL, or accept it explicitly in writing. | <span class="st st-todo">TODO</span> | none | TTL decision recorded in `/policies`. Unblocked: `D-01` is ratified. |

### 7.1 A passing check that proved nothing, caught by its own control

Worth recording, because it is the same shape as the 9.4 clipping defect and it
nearly produced a false PASS on a `P0` fix.

The first run of the `B-01` measurement filled the email field 600ms after
`load` and asserted the buttons. It reported:

```
PASS  hero button disabled before a valid email :: disabled=true
PASS  bottom button disabled before a valid email :: disabled=true
FAIL  bottom button enabled after a valid email  :: disabled=true
FAIL  hero field mirrors the bottom field        :: hero=""
```

The two PASS lines are worthless. The page had not hydrated, and **the
server-rendered markup already ships both buttons disabled**, so "disabled=true
before a valid email" is exactly what a completely dead page returns. Had the
run stopped after the two gate assertions, as a narrower test would have, it
would have reported the fix verified while measuring a page Svelte was not yet
listening to. The only reason the flaw surfaced is that a later assertion in the
same run required the page to actually *react*, and that one failed.

Fixed by adding an explicit hydration gate: type into the hero field, wait for
the framework to enable the hero button, and only then begin asserting. If the
gate never fires, the run records `PAGE HYDRATED = FAIL` and voids the rest
rather than reporting a green suite.

**The rule:** a check whose passing state is indistinguishable from the
unhydrated, unloaded, or unreachable state is not a check. Every UI assertion
needs a control that can only pass if the thing under test is alive. This is the
same lesson as the Cloudflare 1010 bot-block in the verification ledger, where
every origin probe "passed" because the app never saw the request.

---

## 8. `WS-C` Data accuracy and derivation

**Goal:** no number on a sales page that a reader can disprove.

**Verification gate:** `V-02`.

| ID | Pri | Task | Status | Blocked by | Done when |
|---|---|---|---|---|---|
| `C-01` | P1 | Fix the "29 documented cases" claim to 23. | <span class="st st-done">DONE</span> | none | Not a one-word fix in the end: the claim appeared on the homepage, `/early-access`, `/early-access/success`, **and inside the confirmation email**, so a customer who bought could be told 29 after the site said 23. All four now render `offer.precedentCount`. Rendered output: `29 documented` 0 hits, `23 documented` 3 hits. `F-02` closed. |
| `C-02` | P1 | Add a prebuild step that emits `src/lib/stats.generated.json` from `scripts/sts.py`: precedent count, word count, source count, section count. | <span class="st st-todo">TODO</span> | `C-01` | Adding a 24th precedent to the book makes the site say 24 with no site edit. |
| `C-03` | P1 | Port the provenance pattern: every rendered stat carries the artifact it came from, rendered on the page in mono. | <span class="st st-todo">TODO</span> | `C-02` | Each stat displays a source string. |
| `C-04` | P2 | Add a build assertion that fails if any four-or-fewer-digit integer appears in sales copy without coming from the stats module. | <span class="st st-todo">TODO</span> | `C-02` | Test exists and fails on a planted hardcoded number. |
| `C-05` | P2 | Resolve the 1 dead link of 186 in Works Cited. | <span class="st st-todo">TODO</span> | none | `sts.py verify --links` reports 0 dead. |

---

## 9. `WS-D` Demo MVP

**Goal:** make the offer architecture arguable by rendering it as a working
site before it touches production.

**Verification gate:** `V-03`. **Location:** `~/Code/active/sts-mvp`.

### 9.1 Pipeline stages

| ID | Stage | Artifact | Status | Evidence |
|---|---|---|---|---|
| `D-S1` | Plain text design doc | `design/01-design-doc.txt` | <span class="st st-done">DONE</span> | 8 sections, every number measured or marked unverified |
| `D-S2` | Markdown conversion | `design/02-design-doc.md` | <span class="st st-done">DONE</span> | Tables, anchors, fences, cross-links |
| `D-S3` | HTML conversion | `design/03-design-doc.html` | <span class="st st-done">DONE</span> | pandoc 3.6.4, `--standalone --embed-resources`, CSS fully inlined, verified no external `href` |
| `D-S4` | Wireframe | `design/04-wireframe.html` | <span class="st st-done">DONE</span> | 8 labeled sections `S1` to `S8`, intent and rule annotations, screenshot verified |
| `D-S5` | Vanilla mockup | `design/05-mockup/` | <span class="st st-done">DONE</span> | Real book prose, no `!important`, screenshot verified at 1440x3400 |
| `D-S6` | SvelteKit MVP | `app/` | <span class="st st-done">DONE</span> | Builds clean, dev server on `:5180`, both routes HTTP 200 |
| `D-S7` | `/mvp-spinup` skill | `~/.claude/skills/mvp-spinup/` | <span class="st st-done">DONE</span> | Skill, slash command, 3 scripts, 4 references. Registered and listed. See `WS-E` |

### 9.2 Build tasks

| ID | Pri | Task | Status | Blocked by | Done when |
|---|---|---|---|---|---|
| `D-01t` | P1 | Offer module with frozen object and `refundClause()` derivation. | <span class="st st-done">DONE</span> | none | `app/src/lib/offer.js`, 4 included, 1 excluded, `shipsPhysicalGoods` flag |
| `D-02t` | P1 | Stats module with provenance per number. | <span class="st st-done">DONE</span> | none | `app/src/lib/stats.js`, 4 stats each carrying `source` and `measuredOn` |
| `D-03t` | P1 | Precedent data: 3 open cases from real book prose, 20 listed, total derived. | <span class="st st-done">DONE</span> | none | `app/src/lib/precedents.js`, `total = open.length + rest.length` |
| `D-04t` | P1 | Eight sections as Svelte 5 components with scoped styles. | <span class="st st-done">DONE</span> | none | Header, Hero, PrecedentFile, OfferTable, UpdateEngine, BookParts, Close, SiteFooter |
| `D-05t` | P1 | `/policies` route deriving every clause from the offer object. | <span class="st st-done">DONE</span> | none | Renders "Nothing is shipped, so no shipment date applies." with zero hand-written refund prose |
| `D-06t` | P1 | Accessible tablist: `aria-selected`, roving tabindex, arrow-key navigation. | <span class="st st-done">DONE</span> | none | `PrecedentFile.svelte` |
| `D-07t` | P1 | Inert buy button and email field that state what they are. | <span class="st st-done">DONE</span> | none | Toast on buy, validate-and-report on email, nothing persisted |
| `D-08t` | P1 | Headless screenshot helper encoding the two macOS gotchas. | <span class="st st-done">DONE</span> | none | `scripts/shot.sh`, refuses widths under 500px |
| `D-09t` | P2 | Narrow-viewport screenshot helper. Shipped as `scripts/shot-narrow.mjs`, driving Playwright rather than the iframe trick: a `file://` harness wrapping an `http://localhost` page is cross-origin, so it cannot read `scrollWidth`, and an overflow check that cannot read the document is not a check. | <span class="st st-done">DONE</span> | none | Sets an exact viewport with no clamp, measures overflow inside the page, and names the widest offending element |
| `D-10t` | P2 | Verify at 390px and 768px. | <span class="st st-done">DONE</span> | `D-09t` | Both PASS for overflow. Visual review at 390px found a real clipping defect the measurement could not see. See 9.4 |
| `D-11t` | P2 | Accessibility pass: contrast ratios, focus order, reduced-motion behavior. | <span class="st st-todo">TODO</span> | none | Contrast measured, keyboard walk-through recorded |
| `D-12t` | P3 | Wire `stats.generated.json` in the demo to prove the derivation end to end. | <span class="st st-todo">TODO</span> | `C-02` | Editing the book changes the demo's numbers |

### 9.3 How to run it

```bash
cd ~/Code/active/sts-mvp/app
npm run dev          # http://localhost:5180
```

To see the architectural thesis in one edit: open `app/src/lib/offer.js`, flip
`shipsPhysicalGoods` to `true`, and watch the shipment clause appear on
`/policies` and the excluded row change on the homepage, together.

### 9.4 A defect the automated check could not see

Worth recording because it is the general case, not a one-off.

At 390px the overflow measurement returned PASS: `scrollWidth` equalled
`clientWidth`, no horizontal page scroll. The precedent list was nonetheless
broken. Each row's date is `white-space: nowrap` and pushed right with
`margin-left: auto`, so at narrow widths it ran past the row's content box and
was **clipped** by the container's `overflow: hidden`, which exists only to make
the rounded corners work. Clipped content does not extend the document, so it
never trips a `scrollWidth` check. "New York," and "Eastern Mediterranean, c."
were simply cut in half, and every measurement said the page was fine.

Fixed by giving the date its own line below the title under 700px.

The rule this produces, now written into the skill: **the measurement and the eye
catch different bugs.** An automated check finds what it was told to look for.
Run it, then look at the screenshot anyway.

---

## 10. `WS-E` `/mvp-spinup` tooling

**Goal:** turn this pipeline into a repeatable skill so the next project gets the
same seven-stage treatment without rebuilding the scaffolding.

**Verification gate:** `V-05`.

| ID | Pri | Task | Status | Blocked by | Done when |
|---|---|---|---|---|---|
| `E-01` | P2 | Write `~/.claude/skills/mvp-spinup/SKILL.md` with the seven-stage procedure and its trigger conditions. | <span class="st st-done">DONE</span> | none | Skill registered and listed. Stage table matches section 9.1 |
| `E-02` | P2 | Write the slash command wrapper at `~/.claude/commands/mvp-spinup.md`. | <span class="st st-done">DONE</span> | `E-01` | `/mvp-spinup` present with `argument-hint`, defers to the skill rather than restating it |
| `E-03` | P2 | Bundle the screenshot scripts as skill assets. | <span class="st st-done">DONE</span> | `D-09t` | `scripts/shot.sh`, `scripts/shot-narrow.mjs`, `scripts/houserules.sh` |
| `E-04` | P2 | Bundle the stylesheets and the plan shell as reusable templates. | <span class="st st-done">DONE</span> | `E-01` | `references/doc.css`, `plan.css`, `plan-body.html`, `plan-template.md` |
| `E-05` | P2 | Encode the house rules as a lint step. | <span class="st st-done">DONE</span> | `E-01` | `houserules.sh` clean on this repo, and a planted canary trips em dash, `!important`, and banned vocabulary at once. Two of its own bugs found and fixed by that control. See 10.2 |
| `E-06` | P3 | Document the ground-truth-first rule: measure the existing system before designing its replacement. | <span class="st st-done">DONE</span> | `E-01` | Stage 0 is the skill's prime directive, with the three findings it produced named as the argument |
| `E-07` | P3 | Run `/mvp-spinup` against a second, unrelated project to prove it generalizes. | <span class="st st-todo">TODO</span> | `E-01` | `V-05` passes |

### 10.2 Two bugs the lint's own positive control caught

`houserules.sh` was wrong twice before it was right, and both failures argue for
always running a lint against planted violations rather than only against a
codebase you expect to be clean.

1. **A flag reached `grep` through the pattern parameter.** The helper took the
   pattern as `$1`, so calling it as `scan -i '<regex>'` made `-i` the search
   string. `grep -e "-i"` matched `align-items`, `margin-inline`, `z-index`,
   `tab-id`, and `aria-invalid`, producing roughly 80 false positives that
   looked like a catastrophic style failure. Case sensitivity is now fixed
   inside the helper and cannot be passed in.
2. **A code rule was applied to prose.** The `!important` check flagged four
   lines of this plan document that describe the rule forbidding `!important`.
   Documentation is not a violation. CSS and JS rules now scan code files only,
   while the em dash rule still scans everything, because prose is exactly where
   em dashes go wrong.

Both were found by planting a file containing an em dash, an `!important`, and a
banned word, and checking that all three tripped. Neither would have been found
by running the lint on a clean repository, which is the failure mode of every
check that has only ever passed.

### 10.3 The seven stages the skill encodes

| Stage | Input | Output | Why this step is not skippable |
|---|---|---|---|
| 0 | The live system | Measured baseline | A design built on a described system inherits the description's errors. This is how `F-01` and `F-02` were found. |
| 1 | Baseline | Plain text doc | No formatting to hide behind. Weak arguments are visible in plain text. |
| 2 | Plain text | Markdown | Structure: tables, anchors, cross-references. |
| 3 | Markdown | Standalone HTML | Real converter, resources embedded, shareable as one file. |
| 4 | HTML | Wireframe | Structure without aesthetics, so layout arguments happen before visual ones. |
| 5 | Wireframe | Vanilla mockup | Real content, real CSS, no framework, so the design is judged and not the tooling. |
| 6 | Mockup | Framework MVP | Componentized, data-driven, running on localhost. |

---

## 11. `WS-F` Launch campaign

**Status:** <span class="st st-defer">DEFERRED</span>. **Gate:** `V-04` must pass.

The campaign has already been designed across earlier sessions: Substack as the
primary vehicle, YouTube as visual proof, short-form as top of funnel, phased
across teaser, announcement, and deep dive. That design is not the bottleneck
and executing it before `V-04` would drive traffic at a checkout that collects
nothing.

| ID | Pri | Task | Status | Blocked by | Done when |
|---|---|---|---|---|---|
| `F-01t` | P2 | Rewrite all campaign copy against the ratified offer sentence. Existing drafts assume a physical book and lifetime portal access that the offer does not contain. | <span class="st st-todo">TODO</span> | none | No campaign asset promises anything absent from `offer.js`. Unblocked: `D-01` is ratified, and `src/lib/offer.js` is now the thing to write against. |
| `F-02t` | P2 | Build audience before scarcity. Current state: waitlist 9, preorders 6 (all test mode). | <span class="st st-block">BLOCKED</span> | `V-04` | Waitlist above a threshold Chris sets |
| `F-03t` | P3 | Only once the numerator is worth showing, wire `preorder_counts` to a visible counter. Label it with an as-of date unless it genuinely queries on request. | <span class="st st-defer">DEFERRED</span> | `F-02t` | Counter reads a number that helps rather than harms |
| `F-04t` | P2 | Publish one full precedent as a free public post to demonstrate depth. | <span class="st st-todo">TODO</span> | none | Post live, links to a working checkout. Unblocked by `D-01`, but still gated behind `V-04` in practice: do not point traffic at a checkout that has never taken a real dollar. |

### 11.1 Explicitly not doing

- No seat counters or countdown timers while the waitlist holds 9 people. A
  counter reading "6 of 500 claimed" is negative social proof.
- No three-tier cohort ladder. Three price points and three deadline windows is
  demand-conversion machinery, and the actual constraint is demand.
- No promotion of a physical copy until `D-03` is answered and fulfilment exists.

---

## 12. Dependency map

```
D-01 ratify offer sentence
 |
 +-- A-01 offer module ---+-- A-02 sales copy
 |                        +-- A-04 /policies
 |                        +-- A-07 /terms
 |                        +-- A-08 build assertion
 |
 +-- A-06 excluded row  (also needs D-03)
 +-- F-01t campaign copy rewrite

D-02 forever scope --------- A-03 scope paragraph

B-01 button binding ------- B-02 error placement
B-03 live webhook --------- B-04 live keys ------- B-07 one real dollar --> V-04
                                                                            |
C-01 fix 29 to 23 -------- C-02 derive stats ---+-- C-03 provenance         |
                                               +-- C-04 assertion          |
                                               +-- D-12t demo wiring       |
                                                                           v
D-09t shot-narrow -------- D-10t narrow verify                          WS-F launch

E-01 SKILL.md ------------+-- E-02 slash command
                          +-- E-04 templates
                          +-- E-05 house-rule lint
                          +-- E-06 stage 0 doc
D-09t --------------------+-- E-03 bundle scripts
```

---

## 13. Verification gates

A workstream is not done because its tasks are checked off. It is done when its
gate passes, with evidence written to the ledger.

| ID | Gate | Passes when | Method |
|---|---|---|---|
| `V-01` | Offer consistency | The offer sentence is byte-identical on the homepage, the checkout page, and `/policies`, and all three trace to one module. No surface contains offer prose that is not derived. | <span class="st st-done">PASSED</span> 2026-07-29. See 13.2 |
| `V-02` | Numeric honesty | Every number in sales copy is derivable from an artifact, and adding a 24th precedent changes the site with no site edit. | Add a test precedent, rebuild, confirm the count moved, revert |
| `V-03` | Demo integrity | Build clean, both routes 200, derived count reads 23, `/policies` contains no shipment clause while `shipsPhysicalGoods` is false. | <span class="st st-done">DONE</span> 2026-07-29. See 13.1 |
| `V-04` | **Money moves** | One real card is charged, and the charge, the app row, the email, and the download link are all observed. | Live transaction, recorded in the verification ledger |
| `V-05` | Skill works | `/mvp-spinup` runs stages 0 through 6 on a project that is not this one. | Run it against a second project |
| `V-06` | No regression | The 23 precedents, 186 sources, security headers, and anon lockdown all still verify after every change. | `python3 scripts/sts.py verify` plus `sts.py schema` |

### 13.2 `V-01` evidence, recorded 2026-07-29

Measured against the live source at `~/Code/active/sts-v0.7.3`, dev server on
`:5174`, all assertions read from **rendered HTML** rather than from source.
Port 5173 was skipped: the stale `python -m http.server` (PID 6731) recorded in
the verification ledger still holds it, and `reuseExistingServer:true` would have
silently adopted it.

| Check | Result | Evidence |
|---|---|---|
| Build | PASS | `vite build` clean, no errors |
| `/`, `/early-access`, `/policies`, `/terms`, `/about`, `/checklist` | PASS | all HTTP 200 |
| Offer sentence on homepage | PASS | "Five dollars, once" x1 |
| Offer sentence on `/early-access` | PASS | "Five dollars, once" x2 (hero and close) |
| Offer sentence on `/policies` | PASS | "Five dollars, once" x1 |
| No shipment clause while `shipsPhysicalGoods` is false | PASS | `prior to shipment` 0, `Merchandise Rule` 0 in rendered `/policies` |
| Refund clause is derived | PASS | "Nothing is shipped, so no shipment date applies and no shipping policy is involved." |
| Stale ship date gone | PASS | `As of May 2026` 0 hits |
| `/terms` acknowledges the sale | PASS | "This Site sells something" renders in new section 2 |
| Precedent count | PASS | `29 documented` 0 hits across all six pages, `23 documented` 3 hits |
| Book version surfaced on a sales page | PASS | "Draft v0.7.4, in progress" and "You get v0.7.4, updated 2026-07-27", both derived from `book.json` |
| House rules | PASS | em dashes, `!important`, banned vocabulary, version scheme, false live-data claims: all clean across 8 changed files |
| Horizontal overflow | PASS | 1280x900 and 390x844: `scrollWidth == clientWidth` |
| Visual review at 390 and 1280 | PASS | Screenshots inspected, not just measured. Excluded row confirmed rendering at the same weight as included rows |

**Not claimed:** this is the dev server, not production. Nothing here says the
deployed site is fixed, only that the source is. Production still runs `332fdfd`.

### 13.1 `V-03` evidence, recorded 2026-07-29

| Check | Result | Evidence |
|---|---|---|
| Build | PASS | `vite build` completed in 4.01s, no errors |
| `/` | PASS | HTTP 200 |
| `/policies` | PASS | HTTP 200 |
| Derived precedent count | PASS | Rendered HTML contains "23 times, people met", never "29 documented" |
| No stray 29 | PASS | The only `29` in the output is inside the dates 1929 |
| Offer sentence on both surfaces | PASS | "Five dollars, once" appears 3 times on `/`, 1 time on `/policies` |
| Refund clause derived | PASS | "Nothing is shipped, so no shipment date applies." |
| No `!important` | PASS | Zero occurrences outside comments explaining its absence |
| No em dashes | PASS | Zero occurrences in `design/05-mockup/` and `app/src/` |

---

## 14. Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| `R-01` | Live keys flipped before `B-03`, so real orders arrive with no webhook to record them. | Medium | **Severe.** Silent revenue loss and unfulfilled customers. | `B-03` before `B-04`, stated twice in this document. `B-04` marked BLOCKED until `B-03` closes. |
| `R-02` | "Forever" is sold without a bounded scope and becomes an unpayable obligation. | Medium | High | `D-02` blocks `A-03`. Scope paragraph renders on the page, not in terms. |
| `R-03` | A customer checks the precedent count, finds 29 against 23, and stops trusting the sourcing. | Low per visitor, certain in aggregate | High | `C-01` is a one-word fix available today. `C-02` makes recurrence impossible. |
| `R-04` | Campaign runs before checkout works, spending scarce attention on a page that collects nothing. | Medium | High | `WS-F` gated on `V-04`. |
| `R-05` | The offer fix gets bundled with the homepage redesign and neither ships. | Medium | Medium | `D-04` recommends decoupling. `WS-A` touches copy and one module, not layout. |
| `R-06` | Concurrent sessions in the shared checkout clobber work, as happened 2026-07-26. | Medium | Medium | Work in the `v0.7.3` worktree. Do not `git checkout` another branch there. Commit per coherent wave. |

---

## 15. Appendices

### 15.1 File inventory, this working copy

```
~/Code/active/sts-mvp/
  PLAN.md                       this document
  PLAN.html                     rendered, pandoc
  design/
    01-design-doc.txt           stage 1
    02-design-doc.md            stage 2
    03-design-doc.html          stage 3, self-contained
    doc.css                     stylesheet for stage 3
    04-wireframe.html           stage 4
    05-mockup/
      index.html                stage 5
      styles.css
      app.js
  app/                          stage 6, SvelteKit
    src/lib/offer.js            THE offer object
    src/lib/stats.js            derived numbers with provenance
    src/lib/precedents.js       3 open cases, 20 listed, total derived
    src/lib/toast.svelte.js
    src/lib/components/         8 section components plus BuyButton, Toast
    src/routes/+layout.svelte
    src/routes/+page.svelte
    src/routes/policies/+page.svelte
  scripts/
    shot.sh                     headless screenshot, refuses sub-500px
```

### 15.2 Commands used to establish the baseline

```bash
# precedent count, authoritative
cd ~/Code/active/sts-v0.7.3 && python3 scripts/sts.py verify

# word count, page count, stripe mode
python3 scripts/sts.py status

# schema and migration state
python3 scripts/sts.py schema

# live route check
python3 scripts/sts.py live

# the offer, as three surfaces describe it
rg -n -i 'lifetime|forever|physical|50% off' src/routes/+page.svelte \
  src/routes/early-access/+page.svelte src/routes/policies/+page.svelte
```

### 15.3 Measured baselines, 2026-07-29

| Metric | Value | Source |
|---|---:|---|
| Words | 90,623 | `sts.py status` |
| Sections | 30 | manuscript index |
| Precedents | 23 | `sts.py verify`, `P-01` to `P-23` |
| Sources in Works Cited | 186 | link check, 1 dead |
| Site pages | 29 | `sts.py status` |
| Waitlist rows | 9 | Supabase |
| Preorder rows | 6 | Supabase, all test mode |
| Fulfilled sessions | 13 | Supabase |
| Stripe live-mode paid charges | 0 | Stripe API |
| Stripe live-mode webhook endpoints | 0 | Stripe API |

### 15.4 House rules this plan is written under

- No em dashes, in any copy, content, comment, or prose.
- No `!important`. Win CSS conflicts with specificity and source order.
- No banned vocabulary. Use "call to action" or "the close".
- Versions start at 0.0.1.
- Commit per coherent wave, never batch to the end.
- Verify UI headless before claiming it works. Never `--disable-gpu`.
  `--window-size` clamps to 500px on this macOS, so narrow viewports need an
  iframe.
- Never claim a payment pipeline works from code review. Run a real transaction.
- No false "live" or "real-time" labels on static or build-time data.
