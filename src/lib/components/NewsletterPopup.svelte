<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import { elasticOut, cubicOut } from 'svelte/easing';
  import { supabase } from '$lib/utils/supabaseClient';
  import { newsletterSubmitted } from '$lib/stores/newsletterSubmitted';
  import { darkMode } from '$lib/stores/darkMode';

  export let delayMs = 5000;
  export let scrollThreshold = 0.5;

  let isOpen = false;
  let mounted = false;
  let email = '';
  let marketingOptIn = false;
  let message = '';
  let isLoading = false;
  let isSuccess = false;
  let showOptIn = false;
  let subscriberCount = 0;
  let scrollProgress = 0;

  $: isValid = email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  onMount(async () => {
    mounted = true;
    window.addEventListener('scroll', handleScroll);
    setTimeout(showPopup, delayMs);

    // Fetch subscriber count
    const { count, error } = await supabase
      .from('newsletter_subscribers')
      .select('*', { count: 'exact' });

    if (!error) {
      subscriberCount = count;
    }
  });

  function handleScroll() {
    const scrollPercentage = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight);
    scrollProgress = Math.min(scrollPercentage * 100, 100);

    if (scrollPercentage > scrollThreshold) {
      showPopup();
    }
  }

  function showPopup() {
    if (!$newsletterSubmitted) {
      isOpen = true;
      window.removeEventListener('scroll', handleScroll);
    }
  }

  function validateEmail() {
    if (isValid && !showOptIn) {
      setTimeout(() => {
        showOptIn = true;
      }, 300);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (isLoading || !isValid) return;

    isLoading = true;
    message = '';

    try {
      const { error } = await supabase
        .from('newsletter_subscribers')
        .insert([{
          email: email.trim(),
          marketing_opt_in: marketingOptIn
        }]);

      if (error) throw error;

      isSuccess = true;
      message = 'Thank you for subscribing!';
      email = '';
      marketingOptIn = false;
      subscriberCount++;

      setTimeout(() => closePopup(), 3000);
    } catch (error) {
      console.error('Subscription error:', error);
      message = error.code === '23505'
        ? 'This email is already subscribed.'
        : 'Error subscribing. Please try again.';
    } finally {
      isLoading = false;
    }
  }

  function closePopup() {
    isOpen = false;
    email = '';
    marketingOptIn = false;
    message = '';
    isLoading = false;
    isSuccess = false;
    showOptIn = false;
    newsletterSubmitted.setSubmitted();
  }
</script>

{#if mounted && isOpen && !$newsletterSubmitted}
  <div class="newsletter-popup-container" class:dark={$darkMode} transition:fade={{ duration: 300 }}>
    <div class="newsletter-popup"
         in:fly="{{ y: 100, duration: 800, easing: elasticOut }}"
         out:scale="{{ duration: 300, start: 1, opacity: 0 }}">
      <button class="close-button" on:click={closePopup} aria-label="Close newsletter popup">×</button>

      <!-- Progress Bar -->
      <div class="progress-bar">
        <div class="progress-fill" style="width: {scrollProgress}%"></div>
      </div>

      <div class="popup-content">
        {#if isSuccess}
          <div class="success-message" in:scale="{{ duration: 300, easing: cubicOut }}">
            <div class="checkmark-circle">
              <div class="checkmark"></div>
            </div>
            <h2>Welcome to the Community! 🚀</h2>
            <p class="success-text">You're now part of a growing movement preparing for the AI revolution.</p>
          </div>
        {:else}
          <div id="mc_embed_signup">
            <form on:submit={handleSubmit} id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate">
              <div class="form-header">
                <h2>Join {subscriberCount.toLocaleString()}+ Forward-Thinkers</h2>
                <p class="subtitle">Get weekly insights on thriving in the age of AI</p>
              </div>

              <div class="form-content">
                <div class="input-group">
                  <label for="mce-EMAIL">Email Address <span class="required">*</span></label>
                  <div class="input-wrapper">
                    <input
                      type="email"
                      name="EMAIL"
                      class="required email"
                      id="mce-EMAIL"
                      required
                      placeholder="your@email.com"
                      bind:value={email}
                      on:input={validateEmail}
                    >
                    {#if isValid}
                      <span class="valid-indicator" in:scale="{{ duration: 200 }}">✓</span>
                    {/if}
                  </div>
                </div>

                {#if showOptIn}
                  <div class="opt-in-group" in:scale="{{ duration: 300, easing: cubicOut }}">
                    <label class="checkbox-container">
                      <input type="checkbox" id="gdpr_122232" name="gdpr[122232]" value="Y" bind:checked={marketingOptIn}>
                      <span class="checkbox-custom"></span>
                      <span class="checkbox-text">Send me AI survival strategies and insights</span>
                    </label>
                  </div>
                {/if}

                <button type="submit" class="submit-button" disabled={isLoading || !isValid}>
                  {#if isLoading}
                    <div class="spinner"></div>
                  {:else}
                    Join the Movement
                  {/if}
                </button>

                {#if message}
                  <p class="message" class:error={!isSuccess} in:scale="{{ duration: 300 }}">{message}</p>
                {/if}

                <p class="privacy-notice">
                  Your privacy matters. Unsubscribe instantly at any time.
                </p>
              </div>
            </form>
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .newsletter-popup-container {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    display: flex;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
  }

  .newsletter-popup {
    --gradient-start: rgba(59, 130, 246, 0.1);
    --gradient-end: rgba(147, 51, 234, 0.1);
    --border-color: rgba(59, 130, 246, 0.2);
    --text-primary: #1a1a1a;
    --text-secondary: #4a5568;
    --success-color: #4ade80;
    --error-color: #ef4444;

    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    border: 1px solid var(--border-color);
    border-radius: 16px;
    width: 100%;
    max-width: 500px;
    position: relative;
    box-shadow:
      0 -4px 6px -1px rgba(0, 0, 0, 0.1),
      0 -2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  :global(.dark) .newsletter-popup {
    --gradient-start: rgba(59, 130, 246, 0.05);
    --gradient-end: rgba(147, 51, 234, 0.05);
    --border-color: rgba(59, 130, 246, 0.1);
    --text-primary: #e5e7eb;
    --text-secondary: #9ca3af;
  }

  .progress-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 16px 16px 0 0;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #9333ea);
    transition: width 0.3s ease;
  }

  .close-button {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    color: var(--text-secondary);
    cursor: pointer;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(0, 0, 0, 0.1);
    transform: scale(1.1);
  }

  .popup-content {
    padding: 2rem;
  }

  .form-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
    letter-spacing: -0.025em;
  }

  .subtitle {
    color: var(--text-secondary);
    font-size: 1rem;
  }

  .form-content {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .input-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
  }

  .input-wrapper {
    position: relative;
  }

  input[type="email"] {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-primary);
    font-size: 1rem;
    transition: all 0.2s ease;
  }

  input[type="email"]:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    outline: none;
  }

  .valid-indicator {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--success-color);
    font-size: 1.25rem;
  }

  .opt-in-group {
    margin-top: -0.5rem;
  }

  .checkbox-container {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    cursor: pointer;
  }

  .checkbox-custom {
    width: 20px;
    height: 20px;
    border: 2px solid var(--border-color);
    border-radius: 4px;
    position: relative;
    transition: all 0.2s ease;
  }

  input[type="checkbox"] {
    position: absolute;
    opacity: 0;
    cursor: pointer;
  }

  input[type="checkbox"]:checked ~ .checkbox-custom {
    background: #3b82f6;
    border-color: #3b82f6;
  }

  input[type="checkbox"]:checked ~ .checkbox-custom:after {
    content: '';
    position: absolute;
    left: 6px;
    top: 2px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }

  .checkbox-text {
    font-size: 0.875rem;
    color: var(--text-secondary);
    line-height: 1.4;
  }

  .submit-button {
    background: linear-gradient(135deg, #3b82f6, #9333ea);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.875rem;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
  }

  .submit-button:not(:disabled):hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  }

  .submit-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 0.8s linear infinite;
  }

  .message {
    text-align: center;
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 0.875rem;
  }

  .message.error {
    color: var(--error-color);
    background: rgba(239, 68, 68, 0.1);
  }

  .privacy-notice {
    text-align: center;
    font-size: 0.75rem;
    color: var(--text-secondary);
  }

  .success-message {
    text-align: center;
    padding: 2rem 1rem;
  }

  .checkmark-circle {
    width: 60px;
    height: 60px;
    position: relative;
    display: inline-block;
    vertical-align: top;
    margin-bottom: 1rem;
    background: rgba(74, 222, 128, 0.1);
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  .checkmark {
    border-radius: 5px;
    height: 50%;
    width: 25%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -60%) rotate(45deg);
    transform-origin: center;
  }

  .checkmark:after {
    content: '';
    display: block;
    width: 100%;
    height: 100%;
    border: solid var(--success-color);
    border-width: 0 2px 2px 0;
    animation: checkmark 0.3s ease-in-out forwards;
  }

  .success-text {
    color: var(--text-primary);
    font-size: 1.125rem;
    margin-top: 1rem;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(74, 222, 128, 0); }
    100% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }
  }

  @keyframes checkmark {
    0% { height: 0; width: 0; opacity: 1; }
    20% { height: 0; width: 100%; opacity: 1; }
    40% { height: 100%; width: 100%; opacity: 1; }
  }

  @media (max-width: 768px) {
    .newsletter-popup-container {
      padding: 0.75rem;
    }

    .popup-content {
      padding: 1.5rem;
    }

    h2 {
      font-size: 1.25rem;
    }

    .subtitle {
      font-size: 0.875rem;
    }
  }

  @media (max-width: 480px) {
    .newsletter-popup-container {
      padding: 0.5rem;
    }

    .popup-content {
      padding: 1.25rem;
    }

    .form-content {
      gap: 1rem;
    }

    .submit-button {
      font-size: 0.875rem;
      padding: 0.75rem;
    }
  }
</style>