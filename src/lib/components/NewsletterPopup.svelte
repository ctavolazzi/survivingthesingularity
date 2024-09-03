<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import { elasticOut, cubicOut } from 'svelte/easing';
  import { supabase } from '$lib/utils/supabaseClient';
  import { newsletterSubmitted } from '$lib/stores/newsletterSubmitted';

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

  $: isValid = email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  onMount(async () => {
    mounted = true;
    window.addEventListener('scroll', checkScroll);
    setTimeout(showPopup, delayMs);

    // Fetch subscriber count
    const { count, error } = await supabase
      .from('newsletter_subscribers')
      .select('*', { count: 'exact' });
    
    if (!error) {
      subscriberCount = count;
    }
  });

  function checkScroll() {
    const scrollPercentage = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight);
    if (scrollPercentage > scrollThreshold) {
      showPopup();
    }
  }

  function showPopup() {
    if (!$newsletterSubmitted) {
      isOpen = true;
      window.removeEventListener('scroll', checkScroll);
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
  <div class="newsletter-popup-container" transition:fade="{{ duration: 300 }}">
    <div class="newsletter-popup" 
         in:fly="{{ y: 100, duration: 800, easing: elasticOut }}" 
         out:scale="{{ duration: 300, start: 1, opacity: 0 }}">
      <button class="close-button" on:click={closePopup} aria-label="Close newsletter popup">×</button>
      <div class="popup-content">
        {#if isSuccess}
          <div class="success-message" in:scale="{{ duration: 300, easing: cubicOut }}">
            <h2>Thank You For Subscribing!</h2>
            <p>We appreciate your interest. You'll hear from us soon!</p>
          </div>
        {:else}
          <div id="mc_embed_signup">
            <form on:submit={handleSubmit} id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate">
              <div id="mc_embed_signup_scroll">
                <h2>Get The Survival Newsletter</h2>
                <p class="newsletter-description">Join {subscriberCount.toLocaleString()}+ forward-thinkers and receive our insights directly in your inbox.</p>
                <div class="mc-field-group">
                  <label for="mce-EMAIL">Email Address <span class="asterisk">*</span></label>
                  <div class="input-wrapper">
                    <input 
                      type="email" 
                      name="EMAIL" 
                      class="required email" 
                      id="mce-EMAIL" 
                      required 
                      placeholder="Your email address" 
                      bind:value={email}
                      on:input={validateEmail}
                    >
                    {#if isValid}
                      <span class="valid-email" in:scale="{{ duration: 200 }}">✓</span>
                    {/if}
                  </div>
                </div>
                {#if showOptIn}
                  <div id="mergeRow-gdpr" class="mergeRow gdpr-mergeRow content__gdprBlock mc-field-group" in:scale="{{ duration: 300, easing: cubicOut }}">
                    <div class="content__gdpr">
                      <label class="checkbox-container">
                        <input type="checkbox" id="gdpr_122232" name="gdpr[122232]" value="Y" class="gdpr" bind:checked={marketingOptIn}>
                        <span class="checkbox-custom"></span>
                        <span class="checkbox-text">I agree to receive the newsletter via email. You can unsubscribe at any time.</span>
                      </label>
                    </div>
                  </div>
                {/if}
                <div class="clear">
                  <button type="submit" name="subscribe" id="mc-embedded-subscribe" class="button" disabled={isLoading || !isValid}>
                    {#if isLoading}
                      <div class="spinner"></div>
                    {:else}
                      Prepare Me for the Singularity
                    {/if}
                  </button>
                </div>
                <p class="legal-text">You may opt out at any time. We will never sell your data without your consent.</p>
              </div>
            </form>
          </div>
        {/if}
        {#if message}
          <p class="message" in:scale="{{ duration: 300 }}">{message}</p>
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
    display: flex;
    justify-content: center;
    z-index: 1000;
  }

  .newsletter-popup {
    background: var(--color-bg-primary);
    color: var(--color-text-primary);
    width: 100%;
    max-width: 600px;
    position: relative;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    border-top: 3px solid black;
  }

  .popup-content {
    background-color: var(--color-bg-primary);
    margin: 0;
    padding: 1.5rem;
  }

  .close-button {
    position: absolute;
    top: 0.75rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--color-text-primary);
  }

  .success-message {
    text-align: center;
    padding: 2rem 0;
  }

  .message {
    text-align: center;
    margin-top: 1rem;
    color: var(--color-text-secondary);
  }

  .input-wrapper {
    position: relative;
  }

  .valid-email {
    color: var(--color-success);
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
  }

  .legal-text {
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin-top: 0.75rem;
    text-align: center;
    line-height: 1.4;
  }

  .spinner {
    border: 2px solid var(--color-bg-secondary);
    border-top: 2px solid var(--color-primary);
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Responsive styles */
  @media (max-width: 600px) {
    .newsletter-popup {
      width: 100%;
      max-width: none;
      border-radius: 0;
      margin: 0;
      padding: 0;
      border-top: 3px solid black;
    }

    .popup-content {
      padding: 1rem;
    }

    :global(#mc_embed_signup h2) {
      font-size: 1.3rem !important;
    }

    :global(#mc_embed_signup .newsletter-description) {
      font-size: 0.8rem !important;
    }

    :global(#mc_embed_signup .mc-field-group input) {
      padding: 0.6rem 0.8rem !important;
      font-size: 0.9rem !important;
    }

    :global(#mc_embed_signup .button) {
      padding: 0.8rem !important;
      font-size: 0.8rem !important;
      white-space: nowrap;
    }

    :global(#mc_embed_signup .checkbox-text) {
      font-size: 0.7rem !important;
    }
  }

  /* Override Mailchimp styles */
  :global(#mc_embed_signup) {
    background: transparent !important;
    font-family: 'Arial', sans-serif !important;
    width: 100% !important;
    color: var(--color-text-primary) !important;
  }

  :global(#mc_embed_signup form) {
    padding: 0 !important;
  }

  :global(#mc_embed_signup h2) {
    font-size: 1.8rem !important;
    margin-bottom: 0.5rem !important;
    text-align: center !important;
  }

  :global(#mc_embed_signup .newsletter-description) {
    font-size: 0.9rem !important;
    text-align: center !important;
    margin-bottom: 1rem !important;
    line-height: 1.4 !important;
  }

  :global(#mc_embed_signup .mc-field-group) {
    width: 100% !important;
    padding-bottom: 1% !important;
  }

  :global(#mc_embed_signup .mc-field-group input) {
    width: 100% !important;
    max-width: none !important;
    box-sizing: border-box !important;
    padding: 0.8rem 1rem !important;
    font-size: 1rem !important;
    border: 2px solid var(--color-border) !important;
    border-radius: 4px !important;
    background-color: var(--color-bg-secondary) !important;
    color: var(--color-text-primary) !important;
  }

  :global(#mc_embed_signup .checkbox-container) {
    display: flex !important;
    align-items: flex-start !important;
    position: relative !important;
    padding-left: 35px !important;
    margin-bottom: 12px !important;
    cursor: pointer !important;
    font-size: 14px !important;
    user-select: none !important;
  }

  :global(#mc_embed_signup .checkbox-container input) {
    position: absolute !important;
    opacity: 0 !important;
    cursor: pointer !important;
    height: 0 !important;
    width: 0 !important;
  }

  :global(#mc_embed_signup .checkbox-custom) {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    height: 25px !important;
    width: 25px !important;
    background-color: var(--color-bg-secondary) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: 4px !important;
  }

  :global(#mc_embed_signup .checkbox-container:hover input ~ .checkbox-custom) {
    background-color: var(--color-bg-hover) !important;
  }

  :global(#mc_embed_signup .checkbox-container input:checked ~ .checkbox-custom) {
    background-color: var(--color-primary) !important;
  }

  :global(#mc_embed_signup .checkbox-custom:after) {
    content: "" !important;
    position: absolute !important;
    display: none !important;
  }

  :global(#mc_embed_signup .checkbox-container input:checked ~ .checkbox-custom:after) {
    display: block !important;
  }

  :global(#mc_embed_signup .checkbox-container .checkbox-custom:after) {
    left: 9px !important;
    top: 5px !important;
    width: 5px !important;
    height: 10px !important;
    border: solid white !important;
    border-width: 0 3px 3px 0 !important;
    transform: rotate(45deg) !important;
  }

  :global(#mc_embed_signup .checkbox-text) {
    margin-left: 8px !important;
  }

  :global(#mc_embed_signup .button) {
    background: linear-gradient(135deg, #ff8f00, #ff6b00) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 1rem !important;
    font-size: 0.9rem !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    border-radius: 30px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    max-width: none !important;
    height: auto !important;
    margin: 1rem auto !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    box-shadow: 0 2px 10px rgba(255, 107, 0, 0.3) !important;
    text-align: center !important;
    line-height: 1 !important;
  }

  :global(#mc_embed_signup .button:hover) {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(255, 107, 0, 0.5) !important;
    background: linear-gradient(135deg, #ffa000, #ff7900) !important;
  }

  @media (max-width: 600px) {
    .newsletter-popup {
      padding: 1.5rem;
      border-radius: 0;
      max-width: 100%;
    }

    :global(#mc_embed_signup h2) {
      font-size: 1.5rem !important;
    }

    :global(#mc_embed_signup .newsletter-description) {
      font-size: 0.8rem !important;
    }

    :global(#mc_embed_signup .mc-field-group input) {
      padding: 0.7rem 0.9rem !important;
      font-size: 0.9rem !important;
    }

    :global(#mc_embed_signup .button) {
      padding: 0.8rem !important;
      font-size: 0.9rem !important;
    }

    :global(#mc_embed_signup .checkbox-text) {
      font-size: 0.75rem !important;
    }
  }
</style>