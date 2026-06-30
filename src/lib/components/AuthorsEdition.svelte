<script>
  import { onMount } from 'svelte';

  const AUTHORS_LIMIT = 100;

  let authorsClaimed = null; // null = loading
  let email = '';
  let name = '';
  let honeypot = '';
  let state = 'idle'; // idle | loading | success | duplicate | sold_out | error
  let errorMsg = '';
  let copyNumber = null;

  onMount(async () => {
    try {
      const res = await fetch('/api/preorder-count');
      if (res.ok) {
        const data = await res.json();
        authorsClaimed = data.authors ?? 0;
      } else {
        authorsClaimed = 0;
      }
    } catch {
      authorsClaimed = 0;
    }
  });

  $: remaining = authorsClaimed === null ? null : AUTHORS_LIMIT - authorsClaimed;
  $: soldOut = remaining !== null && remaining <= 0;

  async function submit(e) {
    e.preventDefault();
    if (state === 'loading' || soldOut) return;
    state = 'loading';
    errorMsg = '';

    try {
      const res = await fetch('/api/preorder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          name,
          edition_type: 'authors',
          _hp: honeypot,
        }),
      });

      const data = await res.json();

      if (res.status === 201) {
        state = 'success';
        copyNumber = data.copy_number;
        if (authorsClaimed !== null) authorsClaimed += 1;
      } else if (res.status === 409 && data.error === 'sold_out') {
        state = 'sold_out';
        authorsClaimed = AUTHORS_LIMIT;
      } else if (res.status === 409) {
        state = 'duplicate';
      } else {
        state = 'error';
        errorMsg = data.error || 'Something went wrong. Try again.';
      }
    } catch {
      state = 'error';
      errorMsg = 'Network error. Try again.';
    }
  }
</script>

<div class="ae-wrap">

  <!-- AUTHOR'S EDITION CARD -->
  <div class="ae-card">
    <div class="ae-card-inner">

      <!-- LEFT: details -->
      <div class="ae-left">
        <div class="ae-badge">
          <svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
            <path d="M8 1l1.88 3.82L14 5.64l-3 2.93.71 4.12L8 10.77l-3.71 1.92L5 8.57 2 5.64l4.12-.82L8 1z"/>
          </svg>
          Author's Edition
        </div>

        <h2 class="ae-title">Hand-bound. Signed. Numbered.</h2>
        <p class="ae-subtitle">Limited to 100 copies worldwide.</p>

        <ul class="ae-features">
          <li>
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 8l4 4 8-8"/></svg>
            Hand-bound by the author
          </li>
          <li>
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 8l4 4 8-8"/></svg>
            Signed and individually numbered (#1 through #100)
          </li>
          <li>
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 8l4 4 8-8"/></svg>
            Exclusive content not available anywhere else
          </li>
          <li>
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 8l4 4 8-8"/></svg>
            Ships August 2026 directly from the author
          </li>
        </ul>

        <!-- Availability meter -->
        <div class="ae-meter-wrap" aria-live="polite">
          {#if authorsClaimed === null}
            <div class="ae-meter-loading">Checking availability...</div>
          {:else if soldOut}
            <div class="ae-meter-soldout">Sold out. All 100 copies claimed.</div>
          {:else}
            <div class="ae-meter-label">
              <span class="ae-meter-num">{remaining}</span> of {AUTHORS_LIMIT} remaining
            </div>
            <div class="ae-meter-bar" role="progressbar" aria-valuenow={authorsClaimed} aria-valuemin="0" aria-valuemax={AUTHORS_LIMIT}>
              <div class="ae-meter-fill" style="width: {(authorsClaimed / AUTHORS_LIMIT) * 100}%"></div>
            </div>
          {/if}
        </div>
      </div>

      <!-- RIGHT: form -->
      <div class="ae-right">

        {#if state === 'success'}
          <div class="ae-success" role="status">
            <div class="ae-success-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
            </div>
            <h3 class="ae-success-title">
              {#if copyNumber}Copy #{copyNumber} reserved.{:else}You're in.{/if}
            </h3>
            <p class="ae-success-body">
              We have your spot. You'll get a confirmation and payment details by email before the August 2026 launch. Thank you for supporting the project.
            </p>
          </div>

        {:else if state === 'sold_out'}
          <div class="ae-success ae-success--soldout" role="status">
            <p class="ae-success-title">All 100 copies are claimed.</p>
            <p class="ae-success-body">
              The Author's Edition is sold out. The regular edition launches on Amazon and this site in August 2026.
            </p>
          </div>

        {:else if state === 'duplicate'}
          <div class="ae-success ae-success--dup" role="status">
            <p class="ae-success-title">Already reserved.</p>
            <p class="ae-success-body">We already have your preorder. You'll hear from us before launch.</p>
          </div>

        {:else}
          <div class="ae-form-head">
            <p class="ae-form-label">Reserve your copy</p>
            <p class="ae-form-note">
              Payment is collected at launch. Reserving your spot costs nothing now.
            </p>
          </div>

          <form class="ae-form" on:submit={submit} novalidate>
            <!-- Honeypot -->
            <input
              type="text"
              name="website"
              bind:value={honeypot}
              tabindex="-1"
              autocomplete="off"
              aria-hidden="true"
              style="display:none"
            />

            <div class="ae-field">
              <label for="ae-name" class="ae-field-label">Your name</label>
              <input
                id="ae-name"
                type="text"
                class="ae-input"
                placeholder="Jane Smith"
                bind:value={name}
                autocomplete="name"
                required
                disabled={state === 'loading' || soldOut}
              />
            </div>

            <div class="ae-field">
              <label for="ae-email" class="ae-field-label">Email address</label>
              <input
                id="ae-email"
                type="email"
                class="ae-input"
                placeholder="you@example.com"
                bind:value={email}
                autocomplete="email"
                required
                disabled={state === 'loading' || soldOut}
              />
            </div>

            {#if state === 'error'}
              <p class="ae-error" role="alert">{errorMsg}</p>
            {/if}

            <button
              type="submit"
              class="ae-submit"
              disabled={state === 'loading' || soldOut || !email || !name}
              aria-busy={state === 'loading'}
            >
              {#if state === 'loading'}
                Reserving...
              {:else if soldOut}
                Sold Out
              {:else}
                Reserve My Copy
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              {/if}
            </button>

            <p class="ae-fine-print">
              No payment now. We'll email you before August 2026 with pricing and shipping details.
            </p>
          </form>
        {/if}

      </div>
    </div>
  </div>

  <!-- REGULAR EDITION NOTE -->
  <div class="ae-regular">
    <div class="ae-regular-inner">
      <div class="ae-regular-text">
        <strong>Regular edition:</strong> Available August 2026 on <span class="ae-highlight">Amazon</span> and directly on this site. Digital and print.
      </div>
      <a href="/checklist" class="ae-regular-link">Get notified at launch →</a>
    </div>
  </div>

</div>

<style>
  .ae-wrap {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  /* ── MAIN CARD ── */
  .ae-card {
    background: #0a0f23;
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-top: 2px solid rgba(245, 158, 11, 0.5);
    border-radius: 18px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 0 60px rgba(245, 158, 11, 0.08), 0 24px 48px rgba(0,0,0,0.4);
  }

  .ae-card-inner {
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
    padding: 2rem 1.5rem;
  }

  @media (min-width: 768px) {
    .ae-card-inner {
      flex-direction: row;
      align-items: flex-start;
      padding: 2.5rem;
      gap: 3rem;
    }
  }

  /* ── LEFT ── */
  .ae-left {
    flex: 1;
    min-width: 0;
  }

  .ae-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.75rem;
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #f59e0b;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
  }

  .ae-title {
    font-size: clamp(1.4rem, 4vw, 2rem);
    font-weight: 800;
    color: #fef3c7;
    margin: 0 0 0.35rem;
    letter-spacing: -0.025em;
    line-height: 1.15;
  }

  .ae-subtitle {
    font-size: 1rem;
    color: #f59e0b;
    font-weight: 600;
    margin: 0 0 1.5rem;
  }

  .ae-features {
    list-style: none;
    padding: 0;
    margin: 0 0 1.75rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }

  .ae-features li {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    font-size: 0.92rem;
    color: #e2e8f0;
    line-height: 1.4;
  }

  .ae-features svg {
    width: 14px;
    height: 14px;
    color: #f59e0b;
    flex-shrink: 0;
  }

  /* ── AVAILABILITY METER ── */
  .ae-meter-wrap { margin-top: 0.25rem; }

  .ae-meter-loading {
    font-size: 0.82rem;
    color: #64748b;
    font-style: italic;
  }

  .ae-meter-soldout {
    font-size: 0.88rem;
    font-weight: 700;
    color: #ef4444;
  }

  .ae-meter-label {
    font-size: 0.82rem;
    color: #94a3b8;
    margin-bottom: 0.5rem;
  }

  .ae-meter-num {
    font-weight: 800;
    color: #f59e0b;
    font-size: 1rem;
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
  }

  .ae-meter-bar {
    height: 6px;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.06);
    overflow: hidden;
  }

  .ae-meter-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #f59e0b, #fbbf24);
    transition: width 0.6s ease;
  }

  /* ── RIGHT: FORM ── */
  .ae-right {
    width: 100%;
    flex-shrink: 0;
  }

  @media (min-width: 768px) {
    .ae-right { width: 300px; }
  }

  .ae-form-head {
    margin-bottom: 1.25rem;
  }

  .ae-form-label {
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: rgba(245, 158, 11, 0.7);
    margin: 0 0 0.35rem;
    font-family: var(--font-primary, 'Inter', sans-serif);
  }

  .ae-form-note {
    font-size: 0.82rem;
    color: #64748b;
    line-height: 1.5;
    margin: 0;
  }

  .ae-form {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .ae-field {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .ae-field-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 0.01em;
  }

  .ae-input {
    width: 100%;
    padding: 0.65rem 0.85rem;
    background: rgba(2, 6, 23, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 8px;
    color: #f1f5f9;
    font-size: 0.9rem;
    transition: border-color 0.15s ease;
    box-sizing: border-box;
    font-family: inherit;
  }

  .ae-input::placeholder { color: #475569; }

  .ae-input:focus {
    outline: none;
    border-color: rgba(245, 158, 11, 0.6);
  }

  .ae-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .ae-error {
    font-size: 0.82rem;
    color: #f87171;
    margin: 0;
  }

  .ae-submit {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    width: 100%;
    padding: 0.85rem 1.25rem;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 800;
    font-size: 0.92rem;
    border: none;
    border-radius: 999px;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.35);
    transition: filter 0.2s ease, transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.2s ease;
    letter-spacing: 0.01em;
    font-family: inherit;
  }

  .ae-submit:hover:not(:disabled) {
    filter: brightness(1.08);
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(245, 158, 11, 0.45);
  }
  .ae-submit:active:not(:disabled) { transform: scale(0.97); }

  .ae-submit:disabled {
    opacity: 0.45;
    cursor: not-allowed;
    transform: none;
  }

  .ae-fine-print {
    font-size: 0.75rem;
    color: #475569;
    line-height: 1.5;
    margin: 0;
    text-align: center;
  }

  /* ── SUCCESS / STATUS STATES ── */
  .ae-success {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 1.5rem;
    background: rgba(16, 185, 129, 0.06);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 12px;
  }

  .ae-success--soldout {
    background: rgba(239, 68, 68, 0.06);
    border-color: rgba(239, 68, 68, 0.2);
  }

  .ae-success--dup {
    background: rgba(245, 158, 11, 0.06);
    border-color: rgba(245, 158, 11, 0.2);
  }

  .ae-success-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(16, 185, 129, 0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #10b981;
    margin-bottom: 0.25rem;
  }

  .ae-success-icon svg { width: 18px; height: 18px; }

  .ae-success-title {
    font-size: 1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
  }

  .ae-success-body {
    font-size: 0.87rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
  }

  /* ── REGULAR EDITION NOTE ── */
  .ae-regular {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 12px;
    padding: 1rem 1.25rem;
  }

  .ae-regular-inner {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  @media (min-width: 540px) {
    .ae-regular-inner {
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
    }
  }

  .ae-regular-text {
    font-size: 0.88rem;
    color: #64748b;
    line-height: 1.5;
  }

  .ae-highlight {
    color: #94a3b8;
    font-weight: 600;
  }

  .ae-regular-link {
    font-size: 0.82rem;
    font-weight: 600;
    color: #f59e0b;
    text-decoration: none;
    white-space: nowrap;
    flex-shrink: 0;
    transition: color 0.15s ease;
  }

  .ae-regular-link:hover { color: #fbbf24; }
</style>
