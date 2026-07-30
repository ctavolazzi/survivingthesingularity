import { defineConfig, devices } from '@playwright/test';

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
    baseURL: 'http://localhost:5174',
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
  ],

  webServer: {
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
