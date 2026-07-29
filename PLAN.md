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
| `F-01` | **P0** | The $5 offer is described three ways. Homepage and `/early-access` sell digital access plus a 50% launch coupon. `/policies` sells merchandise, offering refunds "prior to shipment" and citing the FTC Mail, Internet, or Telephone Order Merchandise Rule. `/terms` says the site is "informational only" and never mentions a sale. | Read all four rendered surfaces plus source | <span class="st st-dec">DECISION</span> `D-01` |
| `F-02` | **P1** | Homepage claims "The Precedent File: 29 documented cases". The book contains 23, `P-01` through `P-23`. Likely origin: the site has 29 pages. | `python3 scripts/sts.py verify` reports "all 23 present in the book and indexed in Appendix D" | <span class="st st-todo">TODO</span> `C-01` |
| `F-03` | **P0** | Bottom buy button on `/early-access` binds `disabled` to `checkoutLoading` only, unlike the top button which also requires a valid email. Button looks clickable, does nothing, and renders its error message 4052px away in a 720px viewport. | Playwright, production, measured | <span class="st st-todo">TODO</span> `B-01` |
| `F-04` | **P0** | Store has never taken real money. 92 Stripe sessions with `livemode=true` count 0. 24 charges with 0 livemode paid charges. | Stripe API as authoritative ledger | <span class="st st-todo">TODO</span> `B-04` |
| `F-05` | **P0** | No live-mode webhook endpoint exists. `webhook_endpoints` count 1, `livemode=false`. Flipping to live keys without creating one loses every order silently. | Stripe API | <span class="st st-todo">TODO</span> `B-03` |
| `F-06` | P2 | 10 paid test sessions have no corresponding app row (23 complete/paid sessions vs 13 `fulfilled_sessions`). All test mode, no money lost, but the reconciliation gap is real. | Stripe to Supabase reconciliation | <span class="st st-todo">TODO</span> `B-06` |
| `F-07` | P2 | `preorder_counts` table exists in the schema and is referenced nowhere in `src/`. Plumbing without wiring. | `rg preorder_counts src/` returns nothing | <span class="st st-defer">DEFERRED</span> `F-03` gate |
| `F-08` | P2 | `/policies` says "As of May 2026, no firm shipping date has been set" while `V0.7.3-SCOPE.md` says the book ships September 2026 with the preorder campaign in August. Stale by two months. | Source comparison | <span class="st st-todo">TODO</span> `A-05` |
| `F-09` | P3 | Local `RESEND_API_KEY` is dead, so email reconciliation against the Resend API is impossible from this machine. Production has its own key and `fulfilled_sessions` shows 13 rows all `status: delivered`, so prod delivery probably works, but "probably" is not adequate under a promise phrased "I will ensure". | Bogus-key and real-key controls both return identical 400 | <span class="st st-block">BLOCKED</span> needs a valid key |

---

## 5. Decisions required

These block work. Each has a recommended default and the cost of each
alternative. Nothing in `WS-A` can start until `D-01` is answered.

### 5.1 `D-01` What does five dollars actually buy?

**Blocks:** `A-01` through `A-06`, `V-01`. Transitively blocks `WS-F`.

**Recommended default:**

> Five dollars, once. You get the book as it is being written, The Precedent
> File, and every update forever. When the finished book ships, the digital
> edition is yours at no additional cost.

**Why:** it matches what is actually delivered today, it replaces the 50% coupon
(the weakest thing to be holding a month before launch) with the hook Chris
identified himself, and it says nothing about a physical copy, which keeps the
FTC Merchandise Rule out of scope and keeps print and postage out of a five
dollar price.

**Alternatives:**

| Option | Upside | Cost |
|---|---|---|
| A. Keep the 50% coupon | Lowest change cost | Keeps the weak promise. Leaves `/policies` shipment language wrong. |
| B. Include a physical copy | Strongest emotional offer | Needs a real price ($29 to $39), a fulfilment path, and full Merchandise Rule compliance. Not a five dollar product. |

### 5.2 `D-02` What is the bounded scope of "forever"?

**Blocks:** `A-03`.

"Every update forever" is an unbounded obligation being sold to strangers by a
person on a health-constrained runway. It needs one written paragraph: what
counts as an update, in what form it arrives, and what happens if the project
stops.

**Recommended default:** the `foreverScope` string already written into
`app/src/lib/offer.js`, which promises revisions and corrections by email and on
the site for as long as the book is maintained, and guarantees that if the
project stops, everything already delivered stays yours and readable.

### 5.3 `D-03` Does the physical book get sold at all, and at what price?

**Blocks:** `A-06`, and any promotion that mentions print.

**Recommended default:** yes, later, as a separate product at $29 to $39, listed
as "not ready" until it is. Not bundled into the $5.

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
| `A-01` | P0 | Create the production offer module at `src/lib/offer.js` in the live repo, ported from `app/src/lib/offer.js`. | <span class="st st-dec">DECISION</span> | `D-01` | File exists, exports a frozen object, `npm run build` passes. |
| `A-02` | P0 | Rewrite the `/early-access` hero and bottom copy to render from `offer.sentence`. Delete the inline prose. | <span class="st st-dec">DECISION</span> | `A-01` | `rg '50% off' src/routes/early-access/` returns nothing, or returns only offer-object-derived output. |
| `A-03` | P0 | Add the bounded "forever" scope paragraph to the offer section, rendered on the page rather than buried in terms. | <span class="st st-dec">DECISION</span> | `D-02` | Paragraph visible on `/early-access` and `/policies`. |
| `A-04` | P0 | Rewrite `/policies` refund language to derive from `refundClause()`. Remove the shipment clause while `shipsPhysicalGoods` is false. | <span class="st st-dec">DECISION</span> | `A-01` | `/policies` contains no "prior to shipment" string and no FTC Merchandise Rule citation while the offer ships nothing. |
| `A-05` | P1 | Fix the stale "As of May 2026, no firm shipping date" line. Replace with a derived date or remove it. | <span class="st st-todo">TODO</span> | none | `F-08` closed. Rendered page agrees with `V0.7.3-SCOPE.md`. |
| `A-06` | P1 | Add the explicit "not included: a printed copy" row to the offer table on the live site. | <span class="st st-dec">DECISION</span> | `D-03` | Excluded row renders at the same size and weight as the included rows. |
| `A-07` | P1 | Update `/terms` so it acknowledges that a sale occurs on this site. | <span class="st st-todo">TODO</span> | `A-01` | `/terms` references the purchase and links to `/policies`. |
| `A-08` | P2 | Add a build-time assertion that fails the build if offer language appears outside the offer module. | <span class="st st-todo">TODO</span> | `A-01` | A test that greps components for `$5`/`50% off` and fails. |

---

## 7. `WS-B` Checkout go-live

**Goal:** one real dollar moves from a real card and every downstream effect
fires. This is the only workstream that unblocks promotion.

**Verification gate:** `V-04`. **Order matters. Do not reorder `B-03` and `B-04`.**

| ID | Pri | Task | Status | Blocked by | Done when |
|---|---|---|---|---|---|
| `B-01` | P0 | Fix the bottom buy button binding on `/early-access` line 351 so `disabled` also requires `emailOk`, matching line 162. | <span class="st st-todo">TODO</span> | none | Playwright asserts bottom button `disabled=true` before a valid email and `false` after. `F-03` closed. |
| `B-02` | P0 | Move the checkout error message so it renders adjacent to the button that produced it, not 4052px away. | <span class="st st-todo">TODO</span> | `B-01` | Measured distance from button to error under 400px at a 720px viewport. |
| `B-03` | P0 | **Create the live-mode Stripe webhook endpoint** pointing at `/api/webhooks/stripe`. | <span class="st st-todo">TODO</span> | none | Stripe API shows `webhook_endpoints` with a `livemode=true` row. `F-05` closed. |
| `B-04` | P0 | Set the live-mode signing secret and switch `STRIPE_SECRET_KEY` to the live key in Cloudflare Pages secrets. | <span class="st st-block">BLOCKED</span> | `B-03` | `wrangler pages secret list` shows the live key. Checkout probe reports `mode live`. |
| `B-05` | P0 | Add the missing `STRIPE_PRICE_ID_AUTHORS` secret. Code reads it, the secret inventory does not contain it. | <span class="st st-todo">TODO</span> | none | `wrangler pages secret list` includes it. |
| `B-06` | P1 | Close the reconciliation gap behind `F-06`: 10 paid sessions with no app row. Add an alert when a paid session has no `fulfilled_sessions` row within N minutes. | <span class="st st-todo">TODO</span> | none | A deliberately dropped webhook produces an admin alert. |
| `B-07` | P0 | **Take one real dollar from one real card.** Confirm charge, `fulfilled_sessions` row, transactional email, and working download link. | <span class="st st-block">BLOCKED</span> | `B-04` | All four effects observed and recorded in the verification ledger. `V-04` passes. |
| `B-08` | P1 | Add webhook event-id idempotency so identical signed bytes replayed twice are recorded once. | <span class="st st-todo">TODO</span> | none | Replay of identical signed payload produces one row, not two. |
| `B-09` | P2 | Reject future-dated webhook timestamps. Stripe's `constructEvent` enforces tolerance on the past side only; `t+600s` currently returns 200. | <span class="st st-todo">TODO</span> | none | `t+600s` returns 400. |
| `B-10` | P2 | Shorten the 7 day signed download URL TTL, or accept it explicitly in writing. | <span class="st st-todo">TODO</span> | `D-01` | TTL decision recorded in `/policies`. |

---

## 8. `WS-C` Data accuracy and derivation

**Goal:** no number on a sales page that a reader can disprove.

**Verification gate:** `V-02`.

| ID | Pri | Task | Status | Blocked by | Done when |
|---|---|---|---|---|---|
| `C-01` | P1 | Fix the "29 documented cases" claim to 23. Immediate one-word fix. | <span class="st st-todo">TODO</span> | none | `rg '29 documented' src/` returns nothing. `F-02` closed. |
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
| `F-01t` | P2 | Rewrite all campaign copy against the ratified offer sentence. Existing drafts assume a physical book and lifetime portal access that the offer does not contain. | <span class="st st-block">BLOCKED</span> | `D-01` | No campaign asset promises anything absent from `offer.js` |
| `F-02t` | P2 | Build audience before scarcity. Current state: waitlist 9, preorders 6 (all test mode). | <span class="st st-block">BLOCKED</span> | `V-04` | Waitlist above a threshold Chris sets |
| `F-03t` | P3 | Only once the numerator is worth showing, wire `preorder_counts` to a visible counter. Label it with an as-of date unless it genuinely queries on request. | <span class="st st-defer">DEFERRED</span> | `F-02t` | Counter reads a number that helps rather than harms |
| `F-04t` | P2 | Publish one full precedent as a free public post to demonstrate depth. | <span class="st st-todo">TODO</span> | `D-01` | Post live, links to a working checkout |

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
| `V-01` | Offer consistency | The offer sentence is byte-identical on the homepage, the checkout page, and `/policies`, and all three trace to one module. No surface contains offer prose that is not derived. | Fetch all three rendered pages, diff the extracted sentence |
| `V-02` | Numeric honesty | Every number in sales copy is derivable from an artifact, and adding a 24th precedent changes the site with no site edit. | Add a test precedent, rebuild, confirm the count moved, revert |
| `V-03` | Demo integrity | Build clean, both routes 200, derived count reads 23, `/policies` contains no shipment clause while `shipsPhysicalGoods` is false. | <span class="st st-done">DONE</span> 2026-07-29. See 13.1 |
| `V-04` | **Money moves** | One real card is charged, and the charge, the app row, the email, and the download link are all observed. | Live transaction, recorded in the verification ledger |
| `V-05` | Skill works | `/mvp-spinup` runs stages 0 through 6 on a project that is not this one. | Run it against a second project |
| `V-06` | No regression | The 23 precedents, 186 sources, security headers, and anon lockdown all still verify after every change. | `python3 scripts/sts.py verify` plus `sts.py schema` |

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
