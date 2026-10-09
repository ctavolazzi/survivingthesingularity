# Account signup — design study

Design only. No routing, no Supabase wiring, no API. This folder answers one
question: what should signing up for an account on survivingthesingularity.com
look like, at any screen size.

## Files

| File | What it is |
| --- | --- |
| `signup.html` | The design itself. Standalone, opens in a browser, no build step. Every state is reachable from the demo bar along the bottom. |
| `wireframes.html` | The design board: annotated mobile / desktop / tablet wireframes, the breakpoint rationale, and the same `signup.html` rendered live in iframes at seven device sizes. |
| `verify_responsive.py` | Measures the design at 12 viewports and fails loudly on horizontal overflow, escaping boxes, undersized tap targets, or missing critical elements. |
| `shots/` | Screenshots at all 12 viewports, written by `--shots`. |
| `verify_results.json` | Raw measurements from the last run. |

```bash
open design/signup/wireframes.html          # start here
open design/signup/signup.html              # the live design

python3 design/signup/verify_responsive.py           # measure
python3 design/signup/verify_responsive.py --shots   # measure + screenshot
```

## Design language

Tokens are lifted from `src/routes/+page.svelte`, which is the current homepage,
**not** from `src/lib/styles/theme.css`. The two disagree: `theme.css` is the older
brutalist layer (`--radius-*: 0`, hard offset shadows) while the homepage has moved
to Outfit, `--r-card: 20px`, and the ambient orb field. This surface matches the
homepage, since that is what a visitor sees immediately before arriving here.

Amber `#f59e0b` carries exactly one primary action per screen. Blue and green are
reserved for state, never for chrome.

## The responsive model

Four mechanisms, in order of authority:

1. **Fluid by default.** Every size is `clamp()`-based, so the layout is continuous
   between breakpoints instead of stepping at them. `--gutter`, `--stack` and
   `--card-pad` are the only sizing decisions; everything composes from those.
2. **Container queries drive the card.** The card is its own containment context,
   so its internals key off the width of *its pane*, not the viewport. The
   federated buttons pair at a card width of 380px and the padding tightens under
   320px. That means the card stays correct if it is ever reused in a modal or a
   narrower shell.
3. **Media queries do one job:** the page-level composition switch. Three
   thresholds, each placed by widening the window until something actually broke.
4. **Height is a dimension too.** Two height thresholds compress the vertical
   rhythm and, below 560px tall, collapse the value rail to its headline.

### Thresholds

| Threshold | What changes | Why there |
| --- | --- | --- |
| base, < 560px | Single column, **card first**, rail below. Federated buttons stacked. Wordmark reduced to the glyph. | Floor is 280px: folded phones and narrow browser side panels. |
| 560px | Benefits go 2-up. Full wordmark appears. | Below this a 2-up benefit grid produces four-word lines. |
| 900px | Rail centers and the page composes as one narrative column. | The rail can hold a 60-character measure at full width here, but there is still not enough room for two panes. |
| 900px **and** ≥1000px tall | Rail moves *above* the card. | Gated on height. See "what measurement changed" below. |
| 1140px | Two panes: rail at 1.05fr, card pinned to 420–480px. Benefits return to 1-up. | First width where the card can hold 480px and the rail still clears 500px. |
| 1600px | Growth stops, gap opens to 120px. | Nothing on an ultrawide should be 1600px of input field. |
| ≤760px tall | Vertical rhythm, card padding and headline compress against `vh`. | An 800×600 window, a square viewport and a laptop with a browser toolbar all fail the same way. |
| ≤560px tall | Rail collapses to its headline; benefits, proof line and footer hide. | Landscape phone. The rail stops being persuasion and becomes an obstacle. |

### Two decisions worth defending

**The card comes before the rail on mobile.** Someone arriving on a phone from a
checkout link has already decided. Making them scroll past four benefit bullets to
reach an email field taxes a user who is already converted. The rail is still
there, underneath, for whoever needs convincing.

**Tablet does not get the two-pane split.** 768px is the reflex breakpoint and it is
the wrong one here. Split an 834px tablet and each pane gets roughly 380px: the rail
copy sets at about 30 characters per line and the card drops back to stacked
federated buttons anyway. Both panes lose. So the split waits until 1140px, and
between 900 and 1139 the page composes as one centered column instead.

## What measurement changed

The layout was drawn first and measured second, and the measurement moved it. Real
findings from `verify_responsive.py`, all now fixed:

- **The rail-above-card order cost the fold on short wide screens.** On a 900×900
  square the submit button landed 269px below the fold; on a 1112×834 iPad landscape,
  412px below. Both dropped the user onto an argument they did not ask to re-read.
  Promoting the rail is now gated on `min-height: 1000px`, so short and square
  viewports keep the form first, exactly like mobile. Both now pass.
- **Four controls were under the 44px WCAG 2.5.5 target**: the wordmark link (22px),
  both segmented tabs (40px), and the password reveal toggle (38px). All raised.
- **The consent checkbox measured 20px**, but it is wrapped in a `<label>`, so the
  label box is the real target. The probe was corrected to measure the label, and
  the label was given an explicit 44px floor.
- **280px wrapped "Create account" onto two lines** inside the tab. A container
  query shortens it to "Create" below a 320px card width.
- **The desktop two-pane split opened a void between the panes.** A `1.05fr` rail
  column measures about 790px at 1440, while the rail copy is capped at 560px to
  hold its measure. The leftover ~230px sat as dead space between the rail and the
  card, and the composition read as two unrelated halves. Both columns are now
  sized to their content (`minmax(0, 560px)` and `minmax(420px, 480px)`) and the
  pair is centered as a unit, so the gap is the only thing between them.

## Known and accepted

Three viewports still need a scroll to reach the submit button: 320×568, 500×500,
and 844×390. A full signup form (mode switch, two federated buttons, two fields,
consent, submit) does not fit in 500px of height without removing something the
user needs. Scrolling is the right answer there, so the height rules make the form
start at the very top of the viewport rather than pretending to fit. This is
measured and deliberate, not an oversight: see `verify_results.json`.

## Verification

`verify_responsive.py` is stdlib-only and checks 12 viewports for horizontal
overflow, elements escaping the viewport, tap targets under 44px, missing or
zero-box critical elements, and whether the primary action clears the fold.

Two macOS specifics are worth knowing before touching it:

- **`--window-size` clamps to roughly 500px.** Screenshotting at 280px silently
  renders at 500px and reports no overflow when there is plenty. Every width below
  500 must be measured inside an iframe instead, which is what the probe does.
- **Chrome does not exit** after `--dump-dom` or `--screenshot` in this setup, and
  `--dump-dom` serialises at the load event anyway, which is before an async chain
  of iframe loads finishes. So the probe posts its measurements back to the local
  Python server and the browser is killed once they arrive.

The checker has been negative-controlled: injecting a 1400px-wide element makes it
report `overflow-x 1136px` at 280px and fail every viewport. A green run means the
check ran, not that it was skipped.

## Open questions for whoever builds this

These are build decisions, not design ones, and they are deliberately unresolved:

- Confirm which OAuth providers are actually enabled in Supabase before shipping
  both buttons.
- Magic link and password are both drawn. Pick one as primary, or ship both.
- The site currently has no `/login` or `/auth` route (they were removed in a past
  redesign), so routing is a fresh decision.
- The consent checkbox wording needs a legal read against the existing policies page.
