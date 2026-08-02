import { defineConfig, devices, webkit } from '@playwright/test';
import { existsSync } from 'node:fs';

/* WEBKIT CANNOT BE INSTALLED ON THIS MACHINE, AND THAT IS NOT FIXABLE HERE.
   `npx playwright install webkit` exits with "Playwright does not support
   webkit on mac12". This host is macOS 12.7.6 and cannot be upgraded, so the
   binary will never appear no matter how many times anyone runs the install.

   Left unhandled, the three WebKit projects do NOT skip. They FAIL, once per
   test, with a launch error. Measured 2026-08-01: that turned a 94-failure run
   into a 398-failure run. The 304 phantom failures buried the real ones, and
   because the run was piped through `tail`, the visible summary line read
   "634 passed" while the exit code came from `tail` rather than Playwright.
   Two separate signals both said green on a 39% failure rate.

   So detect the binary and drop those projects when it is absent. On CI
   (ubuntu-latest) the executable exists, so all six projects run there and
   that is where genuine Safari-engine coverage now comes from. A local run is
   explicitly NOT full coverage, and says so on stderr rather than pretending. */
const webkitAvailable = (() => {
  try {
    return existsSync(webkit.executablePath());
  } catch {
    return false;
  }
})();

const WEBKIT_PROJECTS = new Set(['webkit', 'mobile-safari', 'tablet']);

if (!webkitAvailable) {
  console.warn(
    '\x1b[33m[playwright] WebKit is unavailable on this OS. Skipping: ' +
      [...WEBKIT_PROJECTS].join(', ') +
      '. These run in CI. This run is not full browser coverage.\x1b[0m'
  );
}

/* Point the run at a server this process did not start. The reason this exists
   is the WebKit gap above: the documented workaround is to run the Linux
   Playwright image in Docker against a dev server on the macOS host, and from
   inside that container `localhost` is the container, not the host. Set
   PLAYWRIGHT_BASE_URL=http://host.docker.internal:5174 and the run targets the
   host instead.

   When it is set, `webServer` is disabled entirely. Leaving it enabled would
   have the container try to boot its own vite against a bind-mounted
   node_modules full of darwin binaries, which fails in a way that looks like a
   test failure rather than a setup problem. */
const EXTERNAL_BASE_URL = process.env.PLAYWRIGHT_BASE_URL || '';
const BASE_URL = EXTERNAL_BASE_URL || 'http://localhost:5174';

if (EXTERNAL_BASE_URL) {
  console.warn(
    `\x1b[36m[playwright] Using external server ${EXTERNAL_BASE_URL}. ` +
      'Not starting one. Make sure it is already running.\x1b[0m'
  );
}

export default defineConfig({
  testDir: './tests/e2e',
  outputDir: './tests/results',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: './tests/reports/html' }],
    ['json', { outputFile: './tests/reports/results.json' }],
    ['list']
  ],
  use: {
    /* PORT 5174, NOT 5173, AND THIS IS NOT COSMETIC.
       A stale `python -m http.server` has been squatting 5173 on this machine
       (PID 6731, still up on 2026-07-29). Combined with reuseExistingServer
       below, Playwright adopted the squatter instead of starting the app, so
       every relative goto() resolved to a 404 and EVERY page-based test failed
       on `waiting for locator(...)`. Measured that day: i-checkout-gate, the
       whole B-01/B-02 regression suite, was 8 of 8 failing for this reason and
       had been silently providing zero coverage. Against 5174 the same specs
       return 3 passed / 6 failed, where the 6 need Stripe and Supabase env that
       this machine does not have. */
    baseURL: BASE_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    // Desktop browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    // Mobile devices
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 13'] },
    },

    // Tablet
    {
      name: 'tablet',
      use: { ...devices['iPad (gen 7)'] },
    },
  ].filter((p) => webkitAvailable || !WEBKIT_PROJECTS.has(p.name)),

  webServer: EXTERNAL_BASE_URL ? undefined : {
    /* Must pass the port explicitly. Without it vite picks 5173, finds the
       squatter, and silently increments to some other port that baseURL above
       is not pointing at. */
    command: 'npm run dev -- --port 5174',
    url: 'http://localhost:5174',
    /* Kept true so a dev server you already have on 5174 is reused rather than
       fought over. That is safe here in a way it was not on 5173, because 5174
       is not occupied by a foreign process. */
    reuseExistingServer: true,
    timeout: 30000,
  },
});
