# Surviving the Singularity: design document for the new site

**Version 0.0.1** · Written 2026-07-29 · Status: **Proposal**

> Nothing in this document is built into the live site. It describes a demo MVP
> that exists to make a set of decisions visible and arguable before any of them
> touch production.

Every number below was measured on 2026-07-29 against the working copy at
`~/Code/active/sts-v0.7.3` and against production deployment `af13a3c9`
(source `332fdfd`). Numbers that could not be verified are marked
`UNVERIFIED` rather than estimated.

**Contents**

1. [Why this document exists](#why-this-document-exists)
2. [Measured state of the current site](#measured-state)
3. [The one decision this asks for](#the-one-decision)
4. [Positioning](#positioning)
5. [The Explore component](#the-explore-component)
6. [Page structure](#page-structure)
7. [Visual direction](#visual-direction)
8. [Technical shape of the MVP](#technical-shape)
9. [What shipping this requires](#what-shipping-requires)

---

<a id="why-this-document-exists"></a>
## 0. Why this document exists

The live site sells well. It also currently says three different things about
what a customer is buying, claims a number it cannot support, and routes every
one of those sales into a payment processor that has never accepted a real
dollar.

None of those are marketing problems. They are all one problem: **the offer is
described in prose, separately, on every surface that mentions it, and prose
drifts.**

The new site fixes that structurally. There is one offer object. It is defined
once. Every surface that describes the offer, including the refund policy, reads
from it. A number that appears on the sales page is derived from the artifact it
describes, not typed by hand.

That is the entire architectural thesis. Everything else here is presentation.

---

<a id="measured-state"></a>
## 1. Measured state of the current site

### 1.1 Three descriptions of one purchase

| Surface | What it says | What it implies |
|---|---|---|
| Homepage hero + close | "The book draft. The Precedent File. The readiness checklist. One payment, everything now, plus 50% off the finished book at launch." | $5 is access plus a discount coupon. No merchandise. |
| `/early-access` (checkout) | "$5 today. The Precedent File in your inbox now. When the book launches, I'll email you an exclusive link at 50% off." | Same. Consistent with the homepage. |
| `/policies` (refunds) | "Preorder customers may request a full refund at any time **prior to shipment**," citing the U.S. FTC Mail, Internet, or Telephone Order Merchandise Rule. | $5 is money taken for goods that will be shipped. Triggers a 30 day ship-or-refund obligation. |
| `/terms` | The site is "informational only." Never mentions a sale. | No transaction exists. |

These cannot all be true. The sales layer sells access. The legal layer sells
merchandise. Three price tiers and a countdown deadline would make that gap
considerably more expensive than it is today.

### 1.2 The number that does not survive checking

The homepage says:

> The Precedent File: **29 documented cases**, with every source

The book contains **23** precedents, `P-01` through `P-23`. Not an estimate.
The project's own harness confirms it:

```console
$ python3 scripts/sts.py verify
  precedents  P-01..P-23 ledger integrity
    OK     all 23 present in the book and indexed in Appendix D
```

The claim overstates by six, on the one asset whose entire pitch is that you can
check the work. A reader who checks the work finds the count wrong before they
find anything else.

> **Likely origin:** the site has 29 *pages*. That collision is exactly what
> hardcoding produces and derivation prevents.

### 1.3 The checkout

From the verification ledger, round 3, 2026-07-29, Stripe API as authoritative:

```
92 sessions,  livemode=true count:       0
24 charges,   livemode paid charges:     0
webhook_endpoints count 1, livemode=false
```

The store has **never taken real money**. There is **no live-mode webhook
endpoint**, so switching to live keys without creating one first would accept
payments and record none of them.

Separately, a confirmed conversion defect: the bottom buy button on
`/early-access` binds `disabled` to `checkoutLoading` only, while the top button
also requires a valid email. The bottom button looks clickable, does nothing,
and renders its error message **4052px away in a 720px viewport**.

### 1.4 The audience, actually

| Table | Rows |
|---|---:|
| `waitlist` | 9 |
| `preorders` | 6 *(all test mode)* |
| `fulfilled_sessions` | 13 |
| `discord_applications` | 0 |

This is the number that should govern the launch design. A scarcity counter
reading "6 of 500 claimed" is not urgency. It is negative social proof rendered
in a box with a border around it.

The schema has a `preorder_counts` table. It is referenced nowhere in `src/`.
The plumbing exists, the wiring does not, and until the numerator is worth
showing it should stay that way.

### 1.5 What is already good and must not regress

Measured, not assumed:

- 23 of 23 precedents present and indexed. Zero dangling cross references, zero
  math drift, zero metadata drift.
- 186 sources in Works Cited, 1 dead.
- 90,623 words, 30 sections.
- Security headers all live: HSTS, CSP `default-src 'self'`, COOP, nosniff, XFO,
  Referrer-Policy, Permissions-Policy.
- Anon database access denied on all six tables, verified with a live-key
  positive control.
- The download bucket is genuinely private. Anon signing of a real object path
  returns 404.
- No em dashes on the homepage. No banned vocabulary. **The site holds the voice
  rules better than most copy written for it.**

This is a re-architecture of the offer surface, not a rewrite of the book or the
security posture.

---

<a id="the-one-decision"></a>
## 2. The one decision this document asks for

Everything downstream depends on a single sentence, and only Chris can ratify
it. The MVP ships with a recommended default so the consequences are visible,
and the default is changeable in one file.

### Recommended default

> **Five dollars, once. You get the book as it is being written, The Precedent
> File, and every update forever. When the finished book ships, the digital
> edition is yours at no additional cost.**

**Why this one.** It matches what is actually delivered today. It removes the
discount coupon, which is the weakest possible thing to be holding a month
before launch, and replaces it with the thing Chris identified as the real hook:
buy once, receive updates forever.

It deliberately says nothing about a physical copy. The moment the offer
promises shipped merchandise, the FTC Merchandise Rule applies, a 30 day clock
starts, and a five dollar price has to absorb print and postage. Physical stays
a separate, later, correctly priced product.

It makes `/policies` correct instead of contradictory: no shipment, no shipment
clause.

### The two alternatives, stated honestly

| Option | Upside | Cost |
|---|---|---|
| **A.** Keep the 50% coupon | Lowest change cost | Keeps the weak promise. Leaves `/policies` shipment language wrong. |
| **B.** Include a physical copy | Strongest emotional offer | Needs a real price ($29 to $39), a fulfilment path, full Merchandise Rule compliance. Not a five dollar product. |

### Open question before selling "forever"

"Every update forever" is an unbounded obligation. Before it is sold it needs a
written scope: **what counts as an update, in what form it arrives, and what
happens if the project stops.** One paragraph. It protects the buyer and it
protects Chris.

The MVP renders that paragraph as a real, visible part of the offer rather than
hiding it in terms. An honest boundary sells better than an unbounded promise
nobody believes.

---

<a id="positioning"></a>
## 3. Positioning

### 3.1 The shift

| | |
|---|---|
| **From** | Here is a book about the singularity, buy it. |
| **To** | Here is a standing position on what is happening, it keeps updating, and five dollars puts you inside it permanently. |

The book is the artifact. **The updates are the product.** The current site leads
with the artifact and mentions the updates in a bullet. The new site inverts
that.

### 3.2 What the site must not sound like

- Not a prepper guide. Not secession. Not bunkers.
- Emergency resilience, community scale, deglobalized.
- Hyper-local, neighborhood-based, cooperative.
- Avoid "independent" as an identity.
- The thesis is empowerment and a new social contract, not survivalism.
- The seminal line: *if a robot grows my food and builds my house, why am I
  renting survival?*
- No em dashes anywhere. No banned vocabulary.

### 3.3 Proof strategy: derived, not asserted

Every headline number is computed from an artifact at build time and carries the
artifact it came from.

| Stat | Derived from |
|---|---|
| 23 precedents | count of `## Precedent P-NN` headings in book source |
| 90,623 words | harness word count |
| 186 sources | Works Cited index |
| 30 sections | manuscript index |

If the book gains a precedent, the site says 24 without anyone editing the site.
**If a number cannot be derived, it does not go on the page.** This is the direct
structural answer to [1.2](#measured-state).

### 3.4 Social proof, honestly

With 9 people on the waitlist, the site does not display a count of people. It
displays a **count of work**. Work is the thing there is a lot of.

No seat counters. No "318 of 500 remaining." No countdown to a deadline that is
not real. When the audience is large enough that a number helps,
`preorder_counts` is already there.

---

<a id="the-explore-component"></a>
## 4. The Explore component

### 4.1 What it is

A secondary call to action beside the primary buy button in the hero. Its job is
to serve the visitor who will not spend five dollars on a page they have read
for eleven seconds, and who wants to see the goods first.

**Name: `EXPLORE THE PRECEDENT FILE`**

Chosen over "the vault," "the playbook," and "the living archive" for one
reason: The Precedent File is a real thing that exists, has a real count, and
can be verified by the person clicking. The other three are names for a thing
that would have to be built first.

### 4.2 What it does

Smooth scrolls to an in-page section. It does not navigate away and it does not
open a modal. The visitor keeps their scroll position and their momentum.

### 4.3 What they land on

A tabbed reader showing three **real** precedents in full, pulled from the book
source. Not summaries. The actual opening passage and the actual sources.

| ID | Title | Why this one |
|---|---|---|
| `P-07` | The Horse's Last Ledger (1783 to 1960) | Labor displacement that completed |
| `P-09` | The Frame-Breakers (England, 1811 to 1816) | Organized resistance that failed |
| `P-19` | Twenty Million Gardens (United States, 1943 to 1944) | Distributed food response that worked at national scale in under two years |

Below the three open tabs, the remaining twenty are listed by title and date,
greyed, with a single line: **"Twenty more, every one sourced."** That is the
unlock. The visitor can see the exact shape of what they do not have.

### 4.4 Why this beats a blurred paragraph

A blur says "there is more text." A list of twenty real titles with real dates
says "there is more work, and it is specific, and none of it is filler." The
second is a stronger argument and it is also simply true.

---

<a id="page-structure"></a>
## 5. Page structure

The MVP builds the homepage only. Other routes are stubs so the nav resolves.
Deliberate: the homepage carries the offer, and the offer is what is being
decided.

| # | Section | Contents |
|---|---|---|
| **S1** | Header | Wordmark, four nav items, one persistent buy button that appears after the hero scrolls past |
| **S2** | Hero | Eyebrow (derived), headline, offer sentence verbatim from the offer object, dual CTA, four derived proof numbers |
| **S3** | The Precedent File | Target of the explore button. Tabbed reader, three real precedents, twenty listed. See [§4](#the-explore-component) |
| **S4** | What five dollars buys | One table from the offer object: four included rows, **one explicitly excluded row**, and the "forever" scope paragraph |
| **S5** | The update engine | How updates reach you. Stated cadence, stated limit, visible unsubscribe link **in the section that asks for the email** |
| **S6** | The book | Three parts, real titles, real descriptions, current word count |
| **S7** | Close | Offer sentence again, buy button again, nothing else. No countdown, no counter, no scarcity |
| **S8** | Footer | Johnny Autoseed LLC, policy links, the four legal routes |

The excluded row in S4 is the trust move. Nobody else does it.

---

<a id="visual-direction"></a>
## 6. Visual direction

Inherit the existing dark technical aesthetic. **This is not a rebrand.**

| Axis | Direction |
|---|---|
| Surface | Near black, layered by elevation not by border alone |
| Text | High contrast, generous measure, never below 16px |
| Accent | The existing amber, used for exactly one thing per screen: the thing you should click |
| Type | One serif for headlines, one system stack for interface, one mono for derived numbers and IDs |
| Motion | Entrance only, short, fully disabled under `prefers-reduced-motion` |
| Grid | Single column on mobile, twelve column above 900px |
| Density | The current site is dense and that is correct for this audience. Keep it. Add air only around the offer, the one place a reader stops |

**Explicitly rejected:** glassmorphism, gradient text, animated gradient borders,
hero video, and any element whose purpose is to look expensive rather than to be
read.

---

<a id="technical-shape"></a>
## 7. Technical shape of the MVP

### 7.1 The offer object

`src/lib/offer.js` exports one frozen object: price, offer sentence, included
list, excluded list, forever-scope paragraph.

The hero reads from it. The offer table reads from it. The close reads from it.
The policies stub reads from it. Changing the offer is a one file change and
every surface moves together, which is the entire point of [§0](#why-this-document-exists).

### 7.2 Derived stats

`src/lib/stats.js` exports numbers **with their provenance attached**. Each stat
carries a source string saying where it came from. In the MVP these are literals
with provenance recorded; in production they are computed at build time by
`scripts/sts.py`, which already produces every one of them.

The provenance field is not decoration. It is what makes [1.2](#measured-state)
impossible to repeat.

### 7.3 Stack

SvelteKit 2, Svelte 5, Vite. No CSS framework, no component library, no external
font, no analytics. Plain CSS with custom properties, because the whole file is
under 900 lines and a framework would be more code than the site.

### 7.4 Explicitly out of scope

- **No payment integration.** The buy button is inert and says so. Wiring a demo
  to a live Stripe key is how test charges end up in a real ledger.
- **No email capture that writes anywhere.** The field validates and reports what
  *would* happen. Collecting real addresses into a demo with no privacy policy is
  a real problem, not a small one.
- No database, no auth, no book reader, no blog, no signals feed.

---

<a id="what-shipping-requires"></a>
## 8. What shipping this actually requires

In order. Steps 1 through 4 are blocking and none of them is a design task.

1. **Ratify the offer sentence** in [§2](#the-one-decision).
2. **Rewrite `/policies`** to match it. Remove the shipment clause if the offer
   has no shipment.
3. **Fix the 29 to 23**, or better, derive it.
4. **Fix the bottom buy button** disabled binding.
5. **Create the live-mode Stripe webhook endpoint, then switch to live keys.**
   That order, or every order is lost.
6. **Take one real dollar from one real card** and confirm every downstream
   effect fires: charge, row, email, download link.
7. Then build audience.
8. Then, when a counter would read a number worth reading, wire
   `preorder_counts`.

> The campaign is step 7. It has been designed. It is not the bottleneck and it
> never was.
