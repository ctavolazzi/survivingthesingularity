# Website and reader review: v0.11.0

Final `npm run build` passed. Public download release remains v0.7.5; the open manuscript is v0.11.0. No deployment or release was performed.

Playwright tested the built website through Vite preview on localhost port 5193 at 390px and 1280px. All eight viewport checks passed: the changed landing section and the new sections in Chapter 6, Conclusion, and Chapter 19. Their rendered text matches canonical source after chapter-pointer expansion. Prose stays within horizontal bounds, opening paragraphs fit the viewport, and body text is at least 16px. No browser page errors occurred. Source hashes were read back after the run and still match the proof inputs.

The real password gate rejected an invalid password and accepted the configured book password. No access code was printed or included in screenshots. Browser DOM mutations made missing revised text and horizontal overflow fail the checks before restoration. Visual inspection confirmed legible mobile and desktop captures, with consent accepted and section headings placed below existing fixed navigation.

Early proof runs exposed a raw-pointer expectation mismatch and development-server hydration timing. The final run uses the shared pointer resolver and the completed production build. Those earlier instrument failures are superseded by the successful built-preview run; no product source changes were needed.

Proof records:

- [Build result](website-build.json) and [full build log](website-build.log).
- [Browser checks](website-review.json), [reproducible browser script](website-review.mjs), and [local preview script](server.mjs).
- Landing screenshots: `landing-{390,1280}-{revision,actions,full}.png`.
- Reader screenshots: `{chapter6,conclusion,chapter19}-{390,1280}-addition.png`.

Build warnings concern existing Svelte unused selectors and accessibility notices, an outdated Browserslist database, existing Markdown import and chunk-size notices, local email postal configuration, and the released PDF's remaining static-hosting size headroom. They did not fail the build.

The image build hook generated 62 untracked optimized derivatives from unchanged image sources. They remain at their current paths and are excluded from the intended editorial change. Their complete list is in [build-byproducts.txt](build-byproducts.txt). The two tracked generated metadata files, `static/images/optimized/.build-cache.json` and `manifest.json`, were restored byte-for-byte to `book-v0.10.4` after the final build. A future build can regenerate those incidental entries. No derivative files were deleted or moved.
