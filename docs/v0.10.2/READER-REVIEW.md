# v0.10.2 reader review

Reviewed the current reader routes, shared Markdown renderer, figure wrapper, scene controller, scene segmentation/catalog, and WebGL lifecycle. This pass found and repaired actual keyboard/focus defects and missing canonical content. It did not change the manuscript, artwork, catalogs, package dependencies, production Vite configuration, or v0.10.1 evidence.

## Before evidence

`reader-proof/before.json` and `before-divider.png` were captured on the new v0.10.2 server before the fixes:

- Opening and closing a 3D scene with Enter removed the focused button and left focus on `BODY`.
- ArrowRight on the scene's Explore button navigated from Chapter 9 to Part III.
- Opening the continuous reader's chapter drawer left focus outside it. Escape did not dismiss it.
- The continuous reader rendered Part II as a title alone: zero images and none of its canonical introduction. Its separate divider branch discarded every divider's Markdown body.
- Selecting a section left focus on `BODY` rather than the selected content.

The earlier v0.10.1 proofs checked keyboard activation and eventual Tab exit but not focus retention at the moment a control was replaced. Their continuous-reader checks covered scenes in chapters, not divider-content parity. These defects were outside those instruments' assertions.

## Changes

Only these production source files changed:

1. `src/lib/components/interactives/BookScene.svelte`: retain one toggle button across still/loading/3D states, expose the busy state with `aria-disabled`, prevent repeated activation during loading, restore focus when context loss removes a focused camera control, and ignore failed asynchronous work after disposal or cancellation.
2. `src/routes/book/[sectionId]/+page.svelte`: leave arrow keys to focused controls, interactive embeds, links, editable content, and modified keyboard shortcuts; retain ordinary chapter navigation from prose. Escape closes the chapter dropdown and returns focus to its trigger. A focused navigation bar remains visible while reading.
3. `src/routes/read/+page.svelte`: render full canonical divider Markdown; use a labeled native modal dialog for the chapter drawer; allow Escape, the Close button, and backdrop dismissal; restore trigger focus on cancellation and heading focus on section selection/start-over; give the icon-only mobile trigger an accessible name; respect reduced-motion preferences for programmatic scrolling.

The native dialog is deliberately opened after Svelte applies its visible-state class. An initial focused test caught opening it before that update, when browser focus selection encountered hidden contents. That ordering was corrected. The backdrop click handler has a narrowly documented Svelte 4 warning suppression because native Escape and the visible Close button supply keyboard dismissal; the browser tests exercise both.

The drawer permits browser-chrome focus as native dialogs do, while making background page controls inert. The proof therefore checks that a background button cannot receive focus and that Tab returns to the dialog, rather than treating a temporary `BODY` focus while the browser toolbar owns focus as an application escape.

## Proofs and results

All proof scripts and fresh evidence are under `docs/v0.10.2/reader-proof/`.

- `after.mjs` / `after.json`: scene open/close focus, context-loss focus recovery, arrow-key isolation, both chapter-navigation Escape flows, modal background isolation, restored selection focus, Part II and III full prose/artwork, and shared renderer alt/caption/link preservation. It iterates the live visual registry instead of asserting a frozen image count. The initial run covered **23 entries**, preserved in `after-initial-23.json`; the final integration rerun passes for **all 54 registered figures**, with no page errors.
- `browser-proof.mjs` / `browser-proof.json`: adapted from the previous bounded proof with new port and output paths. All three scenes pass real WebGL rendering, no eager Three.js download, no continuous animation loop, changed pixels after rotation, selected-description parity, native text tables, still restoration, deliberate context loss, deliberately unavailable WebGL, mobile target sizes, reduced motion, and continuous-reader enhancement. No page errors were captured.
- `navigation-proof.mjs` / `navigation-proof.json`: actual client-side Chapter 9 to Chapter 15 navigation disposes the old WebGL context and begins the next scene on its own still.
- `static-fallback-proof.mjs` / `static-fallback-proof.json`: server-rendered figures retain images, captions, and usable native details with JavaScript disabled. The pre-existing full-reader access gate still requires JavaScript; this proof does not claim otherwise.
- `mobile-reader.mjs` / `mobile-reader.json`: 390-pixel reader layout, named chapter trigger, modal focus, restored close focus, Part I's canonical body/artwork without horizontal overflow, and recorded `scrollTo` calls using `auto` under reduced motion.
- `release-mobile-figures.mjs` / `release-mobile-figures.json`: final 54-entry registry, actual chapter-drawer navigation to the introduction and Appendix D, and two revised figures at a 390-by-844 viewport. Both images load with registered dimensions, retain their canonical alt text and captions, and fit a 351-pixel column without figure or page horizontal overflow. Screenshots are `mobile-release-intro-nine-stages.png` and `mobile-release-appd-precedent-timeline.png`.
- `compile.json`: the three changed Svelte files compile without remaining warnings.

Before/after divider screenshots and mobile chapter-drawer screenshots were reviewed. The new divider image and prose fit the reading column. The scene proof also captures all three models in still, 3D, selected, and no-JavaScript states.

The final 390-pixel figure screenshots were visually inspected: labels and captions fit, and the late timeline retains distinct dots, solid spans and visibly dashed approximate spans. Console inspection recorded no page errors, console errors, failed requests or HTTP errors. Three Svelte development warnings report an unknown `params` prop on Layout/Page; the proof retains those messages and rejects any other warning. The early screenshot also retains the White Rabbit debug trigger over a corner of its caption. `src/routes/+layout.svelte` renders that trigger only inside `{#if dev}`; it is not part of the production reader.

One integration rerun was interrupted by live manuscript reloads that reset the development-only in-memory unlock. After the source was frozen, the unchanged `after.mjs` passed all checks and recorded 54 entries. The mobile drawer proof also passed after integration. No artwork, production source or registry was changed in this final reader pass.

## Reproduction and local server

Run from the repository root:

```sh
export DAILY_NOTE_AGENT=codex
node docs/v0.10.2/reader-proof/server.mjs
node docs/v0.10.2/reader-proof/after.mjs
node docs/v0.10.2/reader-proof/browser-proof.mjs
node docs/v0.10.2/reader-proof/navigation-proof.mjs
node docs/v0.10.2/reader-proof/static-fallback-proof.mjs
node docs/v0.10.2/reader-proof/mobile-reader.mjs
node docs/v0.10.2/reader-proof/release-mobile-figures.mjs
```

The new server is `http://127.0.0.1:5190`, PID 82271 at creation. It was left available for root's integration checks. Existing v0.10.1 server on 5189 was not touched.

This checkout uses a `node_modules` symlink into v0.10.1. Unmodified Vite denied the resolved SvelteKit client runtime, preventing hydration. The proof-only server extends the filesystem allowance to exactly `realpath(node_modules)` while retaining the existing configuration. This changes neither the production configuration nor the older checkout. The first failed server attempt, PID 81171 on 5190 only, was stopped before the corrected proof server started.

The proof scripts unlock the existing development-only in-memory book store. They do not submit credentials or modify the gate. Do not rerun `before.mjs` against the final code if the purpose is to retain the historical failure evidence.

## Sources and limits

The native behavior was checked against [MDN's dialog reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog), [showModal](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal), and [inert](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/inert). Those APIs support the focus and background-interaction design; observed browser behavior supplies the evidence for this implementation.

Checks used installed Chrome with Playwright on this machine. They are not a screen-reader user study, a complete WCAG audit, or coverage of every browser engine. No full publication build was run here. The final reader count is refreshed to 54; root owns publication builds and final artifact review.
