<!--
  /signup - account creation and sign-in.

  Ported from design/signup/signup.html. The markup and every style rule are
  the design study's, unchanged apart from the wiring described below; the demo
  scaffold at the bottom of that file (which it labels "strips out on build")
  is gone.

  WHAT CHANGED FROM THE MOCKUP, AND WHY

  1. The mode switch is two LINKS, not two buttons.
     The study toggled `mode` in JavaScript. Links to ?mode=signin mean the
     switch works with JS disabled, the two modes are separately addressable
     and linkable, and the back button behaves. An auth page is the worst place
     to require JS: failing here means someone cannot get into their account.

  2. The OAuth buttons are LINKS, not form submits.
     Not cosmetic. svelte.config.js sets `form-action: 'self'`, which browsers
     enforce across the redirect chain a form submission starts - so posting a
     form that redirects to accounts.google.com is blocked by our own CSP. A
     link is a top-level navigation and is not governed by it. The full
     reasoning is in src/routes/auth/oauth/[provider]/+server.js.

  3. The "sent" view is driven by the server's response, not a setTimeout.

  4. The strength meter is unchanged and still advisory. It shares its scoring
     with $lib/server/passwordPolicy.js, which is what actually decides.
-->
<script>
  import { enhance } from '$app/forms';
  import { page } from '$app/stores';

  export let data;
  export let form;

  // Mode comes from the URL so it survives a reload and works without JS.
  $: mode = $page.url.searchParams.get('mode') === 'signin' ? 'signin' : 'signup';
  $: isSignup = mode === 'signup';

  // The server echoes the address back on failure so a rejected submit does
  // not wipe what was typed.
  $: email = form?.email ?? '';

  // Errors arrive either from a failed action or as ?error= on a redirect back
  // from /auth/callback.
  $: errorMessage = form?.message ?? $page.url.searchParams.get('error') ?? '';
  $: errorField = form?.field ?? null;

  $: pending = Boolean(form?.pending);
  $: sentAddress = form?.email ?? '';

  $: next = data.next ?? '/';
  $: nextQuery = next && next !== '/' ? `?next=${encodeURIComponent(next)}` : '';

  let password = '';
  let revealed = false;
  let submitting = false;
  // Kept in component state so a rejected submit does not clear it. Retyping a
  // twelve-character code because the password was too short is the kind of
  // small insult that makes people give up on a form.
  let activationCode = '';

  // Identical to strengthScore() in $lib/server/passwordPolicy.js. Kept in step
  // deliberately: a meter that says "Strong" about something the server
  // rejects is worse than no meter.
  const LEVELS = [
    { label: 'Weak',   tip: 'Add a few more characters', color: '#ef4444', fill: 1 },
    { label: 'Fair',   tip: 'Mix in a number or symbol',  color: '#f59e0b', fill: 2 },
    { label: 'Good',   tip: 'Nearly there',               color: '#3b82f6', fill: 3 },
    { label: 'Strong', tip: 'That will hold up',          color: '#10b981', fill: 4 }
  ];

  function score(v) {
    let s = 0;
    if (v.length >= 8) s++;
    if (v.length >= 14) s++;
    if (/[0-9]/.test(v) && /[a-zA-Z]/.test(v)) s++;
    if (/[^a-zA-Z0-9]/.test(v)) s++;
    return Math.max(0, Math.min(3, s - 1));
  }

  $: level = LEVELS[score(password)];
  $: showStrength = isSignup && password.length > 0;

  // Progressive enhancement only: adds the spinner. With JS off the browser
  // posts the form and the server redirects, which is the same outcome.
  const handle = () => {
    submitting = true;
    return async ({ update }) => {
      await update({ reset: false });
      submitting = false;
    };
  };
</script>

<svelte:head>
  <title>{isSignup ? 'Create your account' : 'Sign in'} · Surviving the Singularity</title>
  <meta
    name="description"
    content="One account for the book, the checklist and the signal feed. Free, no card required."
  />
  <!-- An auth page has nothing to offer a search index and should not be a
       landing page in results. -->
  <meta name="robots" content="noindex, nofollow" />
</svelte:head>

<div class="ambient" aria-hidden="true">
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <div class="grid-veil"></div>
</div>

<div class="page">
  <header class="masthead">
    <a class="wordmark" href="/">
      <span class="mark" aria-hidden="true">SS</span>
      <span class="full">Surviving the Singularity</span>
      <span class="sr-only">Surviving the Singularity home</span>
    </a>
    <p class="masthead-alt">
      {#if isSignup}
        Already have an account? <a href="/signup?mode=signin{nextQuery ? '&' + nextQuery.slice(1) : ''}">Sign in</a>
      {:else}
        Need an account? <a href="/signup{nextQuery}">Create one</a>
      {/if}
    </p>
  </header>

  <main class="main">
    <!-- ============ VALUE RAIL ============ -->
    <section class="rail">
      <p class="rail-eyebrow">Free account</p>
      <h1>Keep your place in <em>the transition</em>.</h1>
      <p class="rail-lede">
        The book, the checklist and the signal feed all remember where you left
        off. One account, every device, nothing to re-find.
      </p>

      <ul class="benefits">
        <li class="benefit">
          <span class="benefit-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          </span>
          <div>
            <p class="benefit-title">Read in the browser</p>
            <p class="benefit-body">Your progress follows you from phone to desk and back.</p>
          </div>
        </li>
        <li class="benefit">
          <span class="benefit-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          </span>
          <div>
            <p class="benefit-title">A checklist that saves</p>
            <p class="benefit-body">Tick items off as you build. It stays ticked.</p>
          </div>
        </li>
        <li class="benefit">
          <span class="benefit-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1.5"/></svg>
          </span>
          <div>
            <p class="benefit-title">Signals, filtered</p>
            <p class="benefit-body">The research sweep narrowed to the threads you follow.</p>
          </div>
        </li>
        <li class="benefit">
          <span class="benefit-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="M3.27 6.96 12 12.01l8.73-5.05"/><path d="M12 22.08V12"/></svg>
          </span>
          <div>
            <p class="benefit-title">Your library</p>
            <p class="benefit-body">Anything you preorder lands here the moment it ships.</p>
          </div>
        </li>
      </ul>

      <div class="rail-proof">
        <span class="proof-stat"><span class="proof-dot" aria-hidden="true"></span> Free forever</span>
        <span class="proof-stat">No card required</span>
      </div>
    </section>

    <!-- ============ FORM CARD ============ -->
    <div class="card-slot">
      <div class="card">
        {#if pending}
          <!-- SUCCESS VIEW -->
          <div class="sent">
            <div class="sent-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="m22 6-10 7L2 6"/></svg>
            </div>
            <h2>Check your email</h2>
            <p>
              We sent a sign-in link to <strong>{sentAddress}</strong>. Click it and
              your account is live.
            </p>
            <p class="sent-note">
              Nothing after a minute or two? Check spam, and confirm the address
              above is spelled correctly.
            </p>
            <div class="sent-actions">
              <form method="POST" action="?/resend" use:enhance>
                <input type="hidden" name="email" value={sentAddress} />
                <input type="hidden" name="next" value={next} />
                <button class="ghost-btn" type="submit">
                  {form?.resent ? 'Link sent again' : 'Resend the link'}
                </button>
              </form>
              <a class="ghost-btn" href="/signup{nextQuery}">Use a different email</a>
            </div>
          </div>
        {:else}
          <!-- FORM VIEW -->
          <div class="card-head">
            <h2 class="card-title">{isSignup ? 'Create your account' : 'Welcome back'}</h2>
            <p class="card-sub">
              {isSignup ? 'Takes about twenty seconds.' : 'Pick up where you left off.'}
            </p>
          </div>

          <div class="segmented" role="tablist" aria-label="Account mode">
            <a
              class="seg-btn"
              role="tab"
              aria-selected={isSignup}
              href="/signup{nextQuery}"
            >
              <span class="seg-long">Create account</span><span class="seg-short">Create</span>
            </a>
            <a
              class="seg-btn"
              role="tab"
              aria-selected={!isSignup}
              href="/signup?mode=signin{nextQuery ? '&' + nextQuery.slice(1) : ''}"
            >
              Sign in
            </a>
          </div>

          {#if errorMessage}
            <p class="form-alert" role="alert">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
              <span>{errorMessage}</span>
            </p>
          {/if}

          {#if !data.authConfigured}
            <p class="form-alert" role="alert">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
              <span>Accounts are not configured on this deployment yet.</span>
            </p>
          {/if}

          <div class="oauth">
            {#if data.providers.includes('google')}
              <a class="oauth-btn" href="/auth/oauth/google{nextQuery}" data-sveltekit-reload>
                <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.76h3.57c2.08-1.92 3.27-4.74 3.27-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.76c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.84 14.11a6.6 6.6 0 0 1 0-4.22V7.05H2.18a11 11 0 0 0 0 9.9l3.66-2.84z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1a11 11 0 0 0-9.82 6.05l3.66 2.84c.87-2.6 3.3-4.51 6.16-4.51z"/></svg>
                <span class="label-long">Continue with Google</span>
                <span class="label-short">Google</span>
              </a>
            {/if}
            {#if data.providers.includes('github')}
              <a class="oauth-btn" href="/auth/oauth/github{nextQuery}" data-sveltekit-reload>
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.9 1.2 1.9 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3z"/></svg>
                <span class="label-long">Continue with GitHub</span>
                <span class="label-short">GitHub</span>
              </a>
            {/if}
          </div>

          <div class="divider"><span>or</span></div>

          <form
            method="POST"
            action={isSignup ? '?/signup' : '?/signin'}
            use:enhance={handle}
            novalidate
          >
            <input type="hidden" name="next" value={next} />

            <!-- Honeypot. Hidden from people, filled by bots. Matches the
                 pattern in /api/waitlist, which answers success to a filled
                 trap so the bot learns nothing. -->
            <div class="trap" aria-hidden="true">
              <label for="company">Company</label>
              <input id="company" name="_hp" type="text" tabindex="-1" autocomplete="off" />
            </div>

            <div class="field" class:is-error={errorField === 'email'}>
              <div class="field-label">
                <label for="email">Email</label>
              </div>
              <div class="input-wrap">
                <input
                  class="input"
                  id="email"
                  name="email"
                  type="email"
                  inputmode="email"
                  autocomplete="email"
                  placeholder="you@example.com"
                  value={email}
                  required
                />
              </div>
            </div>

            <div class="field" class:is-error={errorField === 'password'}>
              <div class="field-label">
                <label for="password">Password</label>
                {#if isSignup}
                  <span class="field-hint">{data.passwordHint}</span>
                {/if}
              </div>
              <div class="input-wrap has-toggle">
                <!-- svelte-ignore a11y-autocomplete-valid -->
                <input
                  class="input"
                  id="password"
                  name="password"
                  type={revealed ? 'text' : 'password'}
                  autocomplete={isSignup ? 'new-password' : 'current-password'}
                  placeholder={isSignup ? 'Pick something you will remember' : 'Your password'}
                  aria-describedby="strength-meta"
                  value={password}
                  on:input={(e) => (password = e.currentTarget.value)}
                  required
                />
                <button
                  class="toggle-reveal"
                  type="button"
                  aria-label={revealed ? 'Hide password' : 'Show password'}
                  aria-pressed={revealed}
                  on:click={() => (revealed = !revealed)}
                >
                  {#if revealed}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><path d="M1 1l22 22"/></svg>
                  {:else}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  {/if}
                </button>
              </div>

              {#if showStrength}
                <div class="strength">
                  <div class="strength-track" aria-hidden="true">
                    {#each [0, 1, 2, 3] as i}
                      <span
                        class="strength-seg"
                        style:background={i < level.fill ? level.color : 'var(--surface-2)'}
                      ></span>
                    {/each}
                  </div>
                  <div class="strength-meta" id="strength-meta" aria-live="polite">
                    <span class="strength-label" style:color={level.color}>{level.label}</span>
                    <span>{level.tip}</span>
                  </div>
                </div>
              {/if}
            </div>

            {#if isSignup}
              <div class="field" class:is-error={errorField === 'activation_code'}>
                <div class="field-label">
                  <label for="activation_code">Activation code</label>
                  <span class="field-hint">Optional</span>
                </div>
                <input
                  class="input code-input"
                  id="activation_code"
                  name="activation_code"
                  type="text"
                  inputmode="latin"
                  autocomplete="off"
                  autocapitalize="characters"
                  spellcheck="false"
                  maxlength="20"
                  placeholder="XXXX-XXXX-XXXX"
                  aria-describedby="activation-help"
                  value={activationCode}
                  on:input={(e) => (activationCode = e.currentTarget.value)}
                />
                <p class="field-help" id="activation-help">
                  Got a code from a review copy or a giveaway? Enter it here. The
                  server folds case, dashes and spaces, so type it however it was
                  written.
                </p>
              </div>

              <label class="consent" class:is-error={errorField === 'consent'}>
                <input type="checkbox" name="consent" required />
                <span class="consent-text">
                  I agree to the <a href="/terms">Terms</a> and the
                  <a href="/policies">Privacy Policy</a>.
                </span>
              </label>
            {/if}

            <button class="submit" type="submit" disabled={submitting}>
              {#if submitting}
                <span class="spinner" aria-hidden="true"></span>
                <span>{isSignup ? 'Creating your account' : 'Signing you in'}</span>
              {:else}
                <span>{isSignup ? 'Create account' : 'Sign in'}</span>
                <span class="arrow" aria-hidden="true">&rarr;</span>
              {/if}
            </button>

            <!-- Same form, different action. formaction means the magic-link
                 path reuses the email already typed instead of asking again. -->
            <p class="card-foot">
              Prefer no password?
              <button class="linklike" type="submit" formaction="?/magiclink">
                Email me a sign-in link
              </button>
            </p>
          </form>
        {/if}
      </div>
    </div>
  </main>

  <footer class="footer">
    <a href="/terms">Terms</a>
    <a href="/policies">Privacy</a>
    <a href="/accessibility">Accessibility</a>
    <span>Surviving the Singularity</span>
  </footer>
</div>

<style>
/* ============================================================
   SURVIVING THE SINGULARITY - ACCOUNT SIGNUP
   Design study. Tokens lifted from src/routes/+page.svelte so
   this surface reads as the same product as the homepage.

   Responsive strategy, in order of authority:
     1. Fluid by default. Every size is clamp()-based, so the
        layout is continuous between breakpoints, not stepped.
     2. Container queries drive the card internals. The card
        adapts to the width of ITS pane, not the viewport, so it
        is correct at 380px in a phone and at 380px inside a
        narrow desktop pane.
     3. Media queries do one job only: the page-level switch from
        stacked to two-pane. Three thresholds, no more.
     4. Height is a dimension too. Short and square viewports get
        compressed vertical rhythm so the primary action stays
        reachable without scrolling.
   ============================================================ */

.page *, .page *::before, .page *::after { box-sizing: border-box; min-width: 0; }

:global(:root) {
  /* Palette: matches src/routes/+page.svelte */
  --bg:            #020617;
  --bg-raised:     #060d1f;
  --surface:       #0f172a;
  --surface-2:     #1e293b;
  --border:        rgba(255,255,255,0.05);
  --border-mid:    rgba(255,255,255,0.09);
  --border-strong: rgba(255,255,255,0.14);
  --amber:         #f59e0b;
  --amber-light:   #fbbf24;
  --amber-dim:     rgba(245,158,11,0.12);
  --blue:          #3b82f6;
  --green:         #10b981;
  --red:           #ef4444;
  --text-1:        #f8fafc;
  --text-2:        #cbd5e1;
  --text-3:        #64748b;
  --text-4:        #334155;

  --font:      'Outfit', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;

  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

  --r-card:  20px;
  --r-field: 12px;
  --r-pill:  999px;

  /* Fluid primitives. These are the only sizing decisions;
     everything else composes from them. */
  --gutter:   clamp(16px, 5vw, 56px);
  --stack:    clamp(14px, 2.6vw, 22px);   /* vertical rhythm inside the card */
  --card-pad: clamp(20px, 5.2vw, 40px);

  /* Minimum comfortable tap target. Never goes below this,
     at any viewport, on any control. */
  --tap: 48px;
}

:global(html) {
  -webkit-text-size-adjust: 100%;
  scroll-behavior: smooth;
}

:global(body) {
  margin: 0;
  min-height: 100vh;
  min-height: 100dvh;
  background: var(--bg);
  color: var(--text-1);
  font-family: var(--font);
  font-size: clamp(15px, 1.1vw + 12px, 17px);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;   /* belt; the layout never needs it */
}

/* ---------- Ambient field (same idiom as the homepage) ---------- */
.ambient { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.orb { position: absolute; border-radius: 50%; filter: blur(100px); }
.orb-1 {
  width: min(620px, 90vw); height: min(620px, 90vw);
  background: radial-gradient(circle, rgba(245,158,11,0.13) 0%, transparent 70%);
  top: -18%; right: -12%;
  animation: drift 14s ease-in-out infinite alternate;
}
.orb-2 {
  width: min(440px, 70vw); height: min(440px, 70vw);
  background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
  bottom: -10%; left: -10%;
  animation: drift 18s ease-in-out infinite alternate-reverse;
}
@keyframes drift {
  from { transform: translate(0,0) scale(1); }
  to   { transform: translate(30px, 20px) scale(1.08); }
}
.grid-veil {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
  background-size: 64px 64px;
  mask-image: radial-gradient(ellipse 90% 70% at 50% 0%, #000 20%, transparent 75%);
  -webkit-mask-image: radial-gradient(ellipse 90% 70% at 50% 0%, #000 20%, transparent 75%);
}

/* ============================================================
   PAGE SHELL
   Mobile default: one column, form first, rail underneath.
   ============================================================ */
.page {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  min-height: 100dvh;
  display: grid;
  grid-template-rows: auto 1fr auto;
  padding-left: max(var(--gutter), env(safe-area-inset-left));
  padding-right: max(var(--gutter), env(safe-area-inset-right));
  padding-bottom: max(var(--gutter), env(safe-area-inset-bottom));
}

/* ---------- Masthead ---------- */
.masthead {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: clamp(14px, 3vw, 26px) 0;
  flex-wrap: wrap;
}
.wordmark {
  display: inline-flex;
  align-items: center;
  min-height: 44px;   /* WCAG 2.5.5: it is a link, so it is a target */
  gap: 9px;
  text-decoration: none;
  color: var(--text-1);
  font-family: var(--font-mono);
  font-size: clamp(0.6rem, 1.5vw, 0.72rem);
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  white-space: nowrap;
}
.wordmark .mark {
  width: 22px; height: 22px; flex: none;
  border: 1.5px solid var(--amber);
  border-radius: 6px;
  display: grid; place-items: center;
  color: var(--amber);
  font-size: 0.66rem;
  letter-spacing: 0;
}
.wordmark .full { display: none; }
.masthead-alt {
  font-size: clamp(0.78rem, 1.9vw, 0.86rem);
  color: var(--text-3);
  white-space: nowrap;
}
.masthead-alt a {
  color: var(--text-2);
  text-decoration: none;
  font-weight: 600;
  border-bottom: 1px solid var(--border-strong);
  padding-bottom: 1px;
  transition: color .18s ease, border-color .18s ease;
}
.masthead-alt a:hover { color: var(--amber); border-color: var(--amber); }

/* ---------- Main region ---------- */
.main {
  display: grid;
  grid-template-columns: 1fr;
  gap: clamp(28px, 6vw, 48px);
  align-content: center;
  justify-items: center;
  width: 100%;
  max-width: 1360px;
  margin-inline: auto;
  padding-block: clamp(8px, 3vw, 40px);
}

/* ---------- The value rail ---------- */
.rail {
  width: 100%;
  max-width: 520px;
  order: 2;             /* mobile: form first, rail after */
}
.rail-eyebrow {
  font-family: var(--font-mono);
  font-size: 0.66rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--amber);
  margin: 0 0 12px;
  display: flex; align-items: center; gap: 9px;
}
.rail-eyebrow::after {
  content: ""; height: 1px; flex: 1;
  background: linear-gradient(90deg, var(--amber-dim), transparent);
}
.rail h1 {
  margin: 0 0 14px;
  font-size: clamp(1.65rem, 4.4vw, 3rem);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.025em;
}
.rail h1 em {
  font-style: normal;
  color: var(--amber);
}
.rail-lede {
  margin: 0 0 clamp(22px, 4vw, 34px);
  color: var(--text-2);
  font-size: clamp(0.95rem, 1.9vw, 1.08rem);
  line-height: 1.6;
  max-width: 46ch;
}

.benefits {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: clamp(12px, 2.4vw, 18px);
}
.benefit {
  display: grid;
  grid-template-columns: 30px 1fr;
  gap: 14px;
  align-items: start;
}
.benefit-icon {
  width: 30px; height: 30px;
  border-radius: 9px;
  display: grid; place-items: center;
  background: var(--amber-dim);
  border: 1px solid rgba(245,158,11,0.22);
  color: var(--amber);
}
.benefit-icon svg { width: 15px; height: 15px; display: block; }
.benefit-title {
  margin: 0 0 2px;
  font-size: clamp(0.9rem, 1.8vw, 0.98rem);
  font-weight: 600;
  color: var(--text-1);
  line-height: 1.35;
}
.benefit-body {
  margin: 0;
  font-size: clamp(0.82rem, 1.6vw, 0.9rem);
  color: var(--text-3);
  line-height: 1.55;
}

.rail-proof {
  margin-top: clamp(24px, 4vw, 36px);
  padding-top: clamp(18px, 3vw, 24px);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}
.proof-stat {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-3);
  display: inline-flex; align-items: center; gap: 7px;
}
.proof-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 0 3px rgba(16,185,129,0.14);
}

/* ============================================================
   THE CARD
   A container-query context. Everything inside sizes against
   the card, never the viewport, so the same component is
   correct in a phone and in a narrow desktop pane.
   ============================================================ */
.card-slot {
  width: 100%;
  max-width: 480px;
  order: 1;
  container-type: inline-size;
  container-name: card;
}

.card {
  position: relative;
  background: linear-gradient(180deg, rgba(15,23,42,0.92) 0%, rgba(6,13,31,0.92) 100%);
  border: 1px solid var(--border-mid);
  border-radius: var(--r-card);
  padding: var(--card-pad);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow:
    0 1px 0 rgba(255,255,255,0.04) inset,
    0 24px 60px -20px rgba(0,0,0,0.75);
}
/* Amber hairline along the top edge: the one ornament. */
.card::before {
  content: "";
  position: absolute; top: -1px; left: 12%; right: 12%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(245,158,11,0.55), transparent);
}

.card-head { margin-bottom: var(--stack); }
.card-title {
  margin: 0 0 5px;
  font-size: clamp(1.15rem, 4.6cqi, 1.45rem);
  font-weight: 700;
  letter-spacing: -0.015em;
  line-height: 1.2;
}
.card-sub {
  margin: 0;
  font-size: clamp(0.82rem, 3.2cqi, 0.9rem);
  color: var(--text-3);
  line-height: 1.5;
}

/* ---------- Mode switch (Create / Sign in) ---------- */
.segmented {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  padding: 4px;
  background: rgba(2,6,23,0.6);
  border: 1px solid var(--border);
  border-radius: var(--r-pill);
  margin-bottom: var(--stack);
}
.seg-btn {
  appearance: none;
  border: 0;
  background: transparent;
  color: var(--text-3);
  font-family: var(--font);
  font-size: clamp(0.82rem, 3.2cqi, 0.9rem);
  font-weight: 600;
  padding: 10px 8px;
  min-height: 44px;
  border-radius: var(--r-pill);
  cursor: pointer;
  transition: color .18s ease, background .18s ease;
}
.seg-btn[aria-selected="true"] {
  background: var(--surface-2);
  color: var(--text-1);
  box-shadow: 0 1px 0 rgba(255,255,255,0.06) inset;
}
.seg-btn:hover:not([aria-selected="true"]) { color: var(--text-2); }
.seg-short { display: none; }

/* ---------- Federated buttons ---------- */
.oauth {
  display: grid;
  grid-template-columns: 1fr;   /* stacked by default */
  gap: 10px;
  margin-bottom: var(--stack);
}
.oauth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: var(--tap);
  padding: 0 16px;
  background: var(--surface-2);
  border: 1px solid var(--border-strong);
  border-radius: var(--r-field);
  color: var(--text-1);
  font-family: var(--font);
  font-size: clamp(0.85rem, 3.3cqi, 0.94rem);
  font-weight: 600;
  cursor: pointer;
  transition: background .18s ease, border-color .18s ease, transform .18s var(--ease-spring);
}
.oauth-btn:hover { background: #263449; border-color: rgba(255,255,255,0.2); }
.oauth-btn:active { transform: scale(0.985); }
.oauth-btn svg { width: 17px; height: 17px; flex: none; }
.oauth-btn .label-long  { display: inline; }
.oauth-btn .label-short { display: none; }

/* ---------- Divider ---------- */
.divider {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: var(--stack);
  color: var(--text-4);
  font-family: var(--font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.divider::before, .divider::after {
  content: ""; height: 1px; flex: 1; background: var(--border-mid);
}

/* ---------- Fields ---------- */
.field { margin-bottom: var(--stack); }
.field-label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 7px;
}
.field-label label {
  font-size: clamp(0.78rem, 3cqi, 0.85rem);
  font-weight: 600;
  color: var(--text-2);
}
.field-hint {
  font-size: clamp(0.72rem, 2.8cqi, 0.79rem);
  color: var(--text-3);
}
.field-hint a { color: var(--amber); text-decoration: none; font-weight: 600; }
.field-hint a:hover { text-decoration: underline; }

.field-help {
  margin: 6px 0 0;
  font-size: clamp(0.72rem, 2.8cqi, 0.79rem);
  line-height: 1.5;
  color: var(--text-3);
}

/* Codes are read off a card and typed one character at a time, so they get the
   mono face the rest of this site uses for numbers and labels. The letter
   spacing is what stops XXXX-XXXX-XXXX reading as one long word. `uppercase` is
   presentational only - the server normalizes independently, so a paste of
   lowercase text still works if CSS never loads. */
.code-input {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.code-input::placeholder {
  letter-spacing: 0.12em;
  text-transform: none;
}

.input-wrap { position: relative; display: flex; }
.input {
  width: 100%;
  min-height: var(--tap);
  padding: 0 14px;
  background: rgba(2,6,23,0.72);
  border: 1px solid var(--border-strong);
  border-radius: var(--r-field);
  color: var(--text-1);
  font-family: var(--font);
  /* 16px floor: anything smaller makes iOS Safari zoom on focus. */
  font-size: max(16px, clamp(0.9rem, 3.4cqi, 0.96rem));
  transition: border-color .18s ease, box-shadow .18s ease, background .18s ease;
}
.input::placeholder { color: var(--text-4); }
.input:hover { border-color: rgba(255,255,255,0.2); }
.input:focus {
  outline: none;
  background: rgba(2,6,23,0.9);
  border-color: var(--amber);
  box-shadow: 0 0 0 3px rgba(245,158,11,0.16);
}
.has-toggle .input { padding-right: 52px; }

.toggle-reveal {
  position: absolute;
  right: 3px; top: 50%; transform: translateY(-50%);
  width: 44px; height: 44px;
  display: grid; place-items: center;
  background: transparent;
  border: 0;
  border-radius: 9px;
  color: var(--text-3);
  cursor: pointer;
  transition: color .18s ease, background .18s ease;
}
.toggle-reveal:hover { color: var(--text-1); background: rgba(255,255,255,0.05); }
.toggle-reveal svg { width: 17px; height: 17px; display: block; }

/* Error state */
.field.is-error .input {
  border-color: var(--red);
  box-shadow: 0 0 0 3px rgba(239,68,68,0.14);
}
.field-error {
  display: none;
  align-items: flex-start;
  gap: 7px;
  margin-top: 7px;
  color: #fca5a5;
  font-size: clamp(0.74rem, 2.9cqi, 0.81rem);
  line-height: 1.45;
}
.field.is-error .field-error { display: flex; }
.field-error svg { width: 14px; height: 14px; flex: none; margin-top: 2px; }

/* ---------- Password strength ---------- */
.strength { margin-top: 10px; }
.strength-track {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 4px;
  margin-bottom: 6px;
}
.strength-seg {
  height: 3px;
  border-radius: 2px;
  background: var(--surface-2);
  transition: background .3s var(--ease-out);
}
.strength-meta {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
  font-size: clamp(0.72rem, 2.8cqi, 0.78rem);
  color: var(--text-3);
  line-height: 1.4;
}
.strength-label { font-family: var(--font-mono); letter-spacing: 0.06em; text-transform: uppercase; font-size: 0.68rem; }

/* ---------- Consent ---------- */
.consent {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 11px;
  align-items: center;
  min-height: 44px;   /* the label is the tap target, not the 20px box */
  margin-bottom: var(--stack);
  cursor: pointer;
}
.consent input {
  appearance: none;
  width: 20px; height: 20px;
  margin: 1px 0 0;
  flex: none;
  background: rgba(2,6,23,0.72);
  border: 1px solid var(--border-strong);
  border-radius: 6px;
  cursor: pointer;
  display: grid; place-items: center;
  transition: background .16s ease, border-color .16s ease;
}
.consent input:checked { background: var(--amber); border-color: var(--amber); }
.consent input:checked::after {
  content: "";
  width: 5px; height: 9px;
  border: solid #0b0f1a;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg) translate(-1px, -1px);
}
.consent input:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(245,158,11,0.3);
}
.consent-text {
  font-size: clamp(0.78rem, 3cqi, 0.85rem);
  color: var(--text-3);
  line-height: 1.5;
}
.consent-text a { color: var(--text-2); text-decoration: underline; text-underline-offset: 2px; }
.consent-text a:hover { color: var(--amber); }

/* ---------- Primary action ---------- */
.submit {
  position: relative;
  width: 100%;
  min-height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  padding: 0 20px;
  background: linear-gradient(135deg, var(--amber) 0%, var(--amber-light) 100%);
  border: 0;
  border-radius: var(--r-field);
  color: #0b0f1a;
  font-family: var(--font);
  font-size: clamp(0.92rem, 3.5cqi, 1rem);
  font-weight: 700;
  letter-spacing: -0.005em;
  cursor: pointer;
  overflow: hidden;
  transition: filter .18s ease, transform .18s var(--ease-spring), box-shadow .18s ease;
  box-shadow: 0 6px 22px -8px rgba(245,158,11,0.55);
}
.submit:hover:not(:disabled) {
  filter: brightness(1.07);
  transform: translateY(-1px);
  box-shadow: 0 10px 28px -8px rgba(245,158,11,0.6);
}
.submit:active:not(:disabled) { transform: scale(0.99); }
.submit:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }
.submit .arrow { transition: transform .2s ease; }
.submit:hover:not(:disabled) .arrow { transform: translateX(3px); }

.spinner {
  width: 17px; height: 17px;
  border: 2px solid rgba(11,15,26,0.28);
  border-top-color: #0b0f1a;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.card-foot {
  margin-top: var(--stack);
  padding-top: var(--stack);
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: clamp(0.78rem, 3cqi, 0.85rem);
  color: var(--text-3);
}
.card-foot a { color: var(--amber); text-decoration: none; font-weight: 600; }
.card-foot a:hover { text-decoration: underline; }

/* ---------- Success panel ---------- */
.sent { text-align: center; padding: clamp(6px, 2vw, 14px) 0; }
.sent-icon {
  width: 62px; height: 62px;
  margin: 0 auto clamp(16px, 3vw, 22px);
  border-radius: 18px;
  display: grid; place-items: center;
  background: rgba(16,185,129,0.1);
  border: 1px solid rgba(16,185,129,0.28);
  color: var(--green);
}
.sent-icon svg { width: 27px; height: 27px; }
.sent h2 {
  margin: 0 0 9px;
  font-size: clamp(1.15rem, 4.6cqi, 1.4rem);
  font-weight: 700;
}
.sent p {
  margin: 0 auto clamp(18px, 3.4vw, 26px);
  max-width: 34ch;
  color: var(--text-3);
  font-size: clamp(0.85rem, 3.3cqi, 0.92rem);
  line-height: 1.6;
}
.sent p strong { color: var(--text-1); font-weight: 600; word-break: break-word; }
.sent-actions { display: grid; gap: 10px; }
.ghost-btn {
  min-height: var(--tap);
  display: flex; align-items: center; justify-content: center;
  background: transparent;
  border: 1px solid var(--border-strong);
  border-radius: var(--r-field);
  color: var(--text-2);
  font-family: var(--font);
  font-size: clamp(0.85rem, 3.3cqi, 0.92rem);
  font-weight: 600;
  cursor: pointer;
  transition: border-color .18s ease, color .18s ease, background .18s ease;
}
.ghost-btn:hover { border-color: var(--amber); color: var(--amber); background: rgba(245,158,11,0.06); }

/* ---------- Footer ---------- */
.footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(10px, 3vw, 22px);
  flex-wrap: wrap;
  padding: clamp(16px, 3vw, 24px) 0 0;
  font-size: clamp(0.72rem, 1.8vw, 0.79rem);
  color: var(--text-4);
  text-align: center;
}
.footer a { color: var(--text-3); text-decoration: none; }
.footer a:hover { color: var(--text-2); text-decoration: underline; }

/* Visually hidden but available to screen readers */
.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}

/* Universal focus ring for keyboard users */
:focus-visible {
  outline: 2px solid var(--amber);
  outline-offset: 2px;
}

/* ============================================================
   CONTAINER QUERIES - the card responds to its own pane
   ============================================================ */

/* Once the card itself has room, the federated buttons pair up
   and shorten their labels. This fires from the card width, so
   it is right in a wide phone AND wrong-proof in a narrow pane. */
@container card (min-width: 380px) {
  .oauth { grid-template-columns: 1fr 1fr; }
  .oauth-btn .label-long  { display: none; }
  .oauth-btn .label-short { display: inline; }
}

/* Very narrow containers (folded phones, 280px browsers, tiny
   embeds): pull the padding in and drop the ornament budget. */
@container card (max-width: 320px) {
  .card { padding: 18px 15px; border-radius: 16px; }
  .segmented { margin-bottom: 14px; }
  /* "Create account" wraps to two lines in the tab at this width. */
  .seg-long  { display: none; }
  .seg-short { display: inline; }
}

/* ============================================================
   MEDIA QUERIES - three thresholds, page composition only
   ============================================================ */

/* 1. 560px: comfortable phone / small square. The masthead can
      afford the full wordmark, and the benefits list can pair. */
@media (min-width: 560px) {
  .wordmark .full { display: inline; }
  .benefits { grid-template-columns: 1fr 1fr; gap: 18px 22px; }
  .rail { max-width: 640px; }
}

/* 2. 900px: tablet. The rail moves above the card and centers,
      composing as one narrative column rather than two panes.
      Deliberately NOT the two-pane split yet: at 900px a split
      would give the form about 420px and the rail about 420px,
      and the rail copy would set at 30 characters per line. */
@media (min-width: 900px) {
  .main {
    justify-items: center;
    gap: clamp(34px, 4.5vw, 52px);
  }
  .rail { text-align: center; max-width: 680px; }
  .rail-eyebrow { justify-content: center; }
  .rail-eyebrow::after { display: none; }
  .rail-eyebrow::before {
    content: ""; height: 1px; width: 34px;
    background: linear-gradient(90deg, transparent, var(--amber-dim));
  }
  .rail-lede { margin-inline: auto; }
  .benefits { text-align: left; }
  .rail-proof { justify-content: center; }
  .card-slot { max-width: 520px; }
}

/* 2b. The rail only earns the position ABOVE the card when there is real
      vertical room for it. Measured: on a 900x900 square the rail-first order
      pushed the submit button 269px below the fold, and on a 1112x834 iPad
      landscape 412px below it. Both land the user on an argument they did not
      ask to re-read. So promoting the rail is gated on height, and short or
      square viewports keep the form first, exactly like mobile. */
@media (min-width: 900px) and (min-height: 1000px) {
  .rail { order: 1; }
  .card-slot { order: 2; }
}

/* 3. 1140px: desktop. Now there is genuinely enough width for two
      panes: the rail gets ~1.05fr and the card a fixed 480px, so
      the rail keeps a 45-65 character measure and the form never
      stretches into an uncomfortably wide input row. */
@media (min-width: 1140px) {
  .main {
    /* Both columns are sized to their content rather than to a fraction of the
       viewport, and the pair is centered as a unit. A 1.05fr rail column reads
       as ~790px at 1440 while the rail copy is capped at 560px for measure, so
       the leftover ~230px opened a void between the panes and the composition
       fell apart into two unrelated halves. */
    grid-template-columns: minmax(0, 560px) minmax(420px, 480px);
    justify-content: center;
    gap: clamp(48px, 6vw, 96px);
    align-items: center;
    justify-items: stretch;
    padding-block: clamp(24px, 4vw, 56px);
  }
  .rail { order: 1; text-align: left; max-width: 560px; justify-self: start; }
  .rail-eyebrow { justify-content: flex-start; }
  .rail-eyebrow::before { display: none; }
  .rail-eyebrow::after { display: block; }
  .rail-lede { margin-inline: 0; }
  .benefits { grid-template-columns: 1fr; gap: 20px; }
  .rail-proof { justify-content: flex-start; }
  .card-slot { order: 2; justify-self: end; max-width: 480px; }
}

/* Very wide: stop growing, start breathing. */
@media (min-width: 1600px) {
  .main { max-width: 1480px; gap: 120px; grid-template-columns: minmax(0, 620px) 480px; }
  .rail { max-width: 620px; }
  .rail h1 { font-size: 3.15rem; }
}

/* ============================================================
   HEIGHT IS A DIMENSION TOO
   Square and short viewports: compress the vertical rhythm so
   the primary action stays reachable. This is what keeps an
   800x600 window, a landscape phone, and a 500x500 square from
   burying the submit button below the fold.
   ============================================================ */
@media (max-height: 760px) {
  :global(:root) { --stack: clamp(11px, 1.9vh, 16px); --card-pad: clamp(18px, 3.4vh, 28px); }
  .rail h1 { font-size: clamp(1.5rem, 3.4vh, 2.2rem); }
  .rail-lede { font-size: 0.94rem; }
  .submit { min-height: 50px; }
  .main { padding-block: 8px; }
  .masthead { padding: 8px 0; }
}

/* Landscape phones and short square windows: the rail is a
   luxury, the form is the job. Collapse the rail to its headline
   and hide the benefits rather than making the user scroll past
   them to reach the field they came for. */
@media (max-height: 560px) and (max-width: 1139px) {
  .benefits, .rail-proof, .rail-lede { display: none; }
  .rail { text-align: center; }
  .main { gap: 16px; }
  .rail h1 { font-size: clamp(1.3rem, 4.2vh, 1.7rem); margin-bottom: 0; }
  .footer { display: none; }
}

/* ---------- Motion preferences ---------- */
@media (prefers-reduced-motion: reduce) {
  .page *, .page *::before, .page *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
}

/* ---------- Forced colors / high contrast ---------- */
@media (forced-colors: active) {
  .card, .input, .oauth-btn, .ghost-btn { border: 1px solid CanvasText; }
  .submit { border: 1px solid CanvasText; }
}

/* ---------- Added by the port (see the comment at the top of the file) ---------- */

/* Honeypot. Off-screen rather than display:none - some bots skip hidden
   fields, and a field they can see is a field they fill. */
.trap {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

/* Server-rendered error banner. The mockup only had per-field errors; the
   server also returns whole-form failures (rate limited, unavailable, a bad
   link bounced back from /auth/callback). */
.form-alert {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  margin: 0 0 var(--stack);
  padding: 11px 13px;
  border: 1px solid rgba(239, 68, 68, 0.28);
  border-radius: var(--r-field);
  background: rgba(239, 68, 68, 0.08);
  color: #fca5a5;
  font-size: 0.85rem;
  line-height: 1.45;
}
.form-alert svg {
  width: 16px;
  height: 16px;
  flex: none;
  margin-top: 1px;
}

/* The mode switch and the OAuth buttons are anchors now, not <button>s.
   These restore the button geometry an anchor does not inherit. */
.seg-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}
.oauth-btn {
  text-decoration: none;
}
a.ghost-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

/* "Email me a sign-in link" is a submit button (it posts the email already
   typed, to a different action) but has to read as the link the design shows. */
.linklike {
  appearance: none;
  border: 0;
  background: none;
  padding: 0;
  font: inherit;
  color: var(--amber);
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
}
.linklike:hover {
  text-decoration: underline;
}
.linklike:focus-visible {
  outline: 2px solid var(--amber);
  outline-offset: 3px;
  border-radius: 3px;
}

.sent-note {
  color: var(--text-3);
  font-size: 0.82rem;
  margin-top: -4px;
}

.consent.is-error .consent-text {
  color: #fca5a5;
}
</style>
