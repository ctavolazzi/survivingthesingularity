# Site audit tools

Six scripts that measure what a built copy of the site actually serves and
draws. They exist to answer one question honestly: did a change alter anything
it was not meant to?

They run against a served build, never against source. Build twice (the tree
before your change and the tree after), serve both, and point the tools at each.

```bash
# before: an untouched checkout        after: your working tree
npm run build && npm run preview -- --port 4411 --strictPort --host 127.0.0.1
npm run build && npm run preview -- --port 4412 --strictPort --host 127.0.0.1
```

A preview server started from a checkout with no `.env` cannot reach Supabase,
Stripe or Resend, so nothing these tools do can send mail or write a row.

## The tools

| Script | Reads | Reports |
|---|---|---|
| `crawl_site.py BASE OUT.json [start paths]` | served HTML only | status, title, description, canonical, headings, images, every link; then resolves each internal link and `#anchor` |
| `audit_browser.mjs BASE OUT_DIR LABEL` | real Chrome, 1280 and 390 wide | console errors, failed requests, horizontal overflow, layout shift |
| `audit_a11y.mjs BASE OUT.json --scroll` | real Chrome | form fields and buttons with no accessible name, text contrast, which elements shift |
| `audit_extra.mjs BASE OUT_DIR LABEL` | Chrome and plain fetch | blog dates in two time zones, what shows with JavaScript off, meta tag counts per page (set `PAGES="/ /blog ..."`) |
| `audit_tiles.mjs BASE OUT_DIR LABEL` | real Chrome | viewport-sized screenshots at each scroll stop, for before and after picture comparison |
| `probe_geometry.mjs OUT.json` | both builds | every element's box to 0.01px and the computed styles that decide its look, before against after |

`crawl_site.py` only follows links. Pages nothing links to (`/read`,
`/workshop`, `/exclusive-friends-only`, `/unsubscribe`, `/early-access/success`)
must be passed as start paths, or the second crawl will appear to have lost them.

## Prove each one can fail first

A clean result from a tool that cannot go red is not evidence. Three of them
plant a known defect when asked, and the planted defect must show up in the
output before a clean run counts:

```bash
CRAWL_CONTROL=1 python3 crawl_site.py BASE out.json   # a missing page and a dead anchor
node audit_browser.mjs BASE DIR LABEL --control        # a console error and a 3000px-wide element
node audit_a11y.mjs BASE out.json --control            # an unlabeled input, an empty button, grey on grey
node probe_geometry.mjs out.json --control             # one element 3px narrower in the after page
```

## Traps, each one found by getting it wrong

1. **`fullPage` screenshots are blind below the fold here.** `html` and `body`
   both set `overflow-y: auto`, so the page scrolls an inner box. A full-page
   capture paints the first 800px and blank background below. Two blank halves
   compare as identical. Compare `audit_tiles.mjs` output instead.
2. **`window.scrollTo` moves nothing**, for the same reason. Scroll with real
   wheel events (`page.mouse.wheel`) and read the position back.
3. **`scrollWidth` cannot detect overflow.** The site sets `overflow-x: hidden`,
   which pins `scrollWidth` to the viewport. Measure element boxes.
4. **Reveal-on-scroll text measures as contrast 1:1** until it has been scrolled
   into view, because it sits at opacity 0. Pass `--scroll`.
5. **Web fonts land at a different moment on every load.** There are 74 font
   faces. A capture taken before they have all arrived shows small text a pixel
   off, and identical text measuring different widths. Wait for
   `document.fonts.ready` and load every face before measuring.
6. **Remote images change page height from run to run.** Block requests to
   other hosts in both builds when comparing pictures, so the comparison is
   about markup and CSS.
7. **Layout shift numbers are bimodal.** Run each build twice. `/devlog` scored
   0 and 0.153 on two runs of the same build.
8. **A count is not a match.** `grep -c cloudflareinsights` returned 1 on the
   live home page. The match was the Content-Security-Policy allow-list, not an
   analytics tag. Read the matched text.
9. **A background build can report exit 0 after failing**, when another command
   follows it. Print the real status into the log:
   `npm run build 2>&1; echo "BUILD_EXIT=$?"`.
10. **A fresh checkout's build rewrites two tracked files**,
    `static/images/optimized/manifest.json` and `.build-cache.json`. Nothing in
    `src/` reads them. Restore them before reviewing your diff.

## What these do not check

Whether the words are true, whether the legal pages match the product, and
whether a page looks good. Those need a person reading the rendered page.
