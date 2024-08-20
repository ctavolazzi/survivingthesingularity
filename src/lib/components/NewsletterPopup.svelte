<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import { elasticOut } from 'svelte/easing';

  export let delayMs = 1000;

  let isOpen = false;
  let mounted = false;

  onMount(() => {
    mounted = true;
    const timer = setTimeout(() => {
      isOpen = true;
    }, delayMs);

    return () => clearTimeout(timer);
  });

  function closePopup() {
    isOpen = false;
  }
</script>

{#if mounted && isOpen}
  <div class="newsletter-popup-container" transition:fade="{{ duration: 300 }}">
    <div class="newsletter-popup" 
         in:fly="{{ y: 100, duration: 800, easing: elasticOut }}" 
         out:scale="{{ duration: 300, start: 1, opacity: 0 }}">
      <button class="close-button" on:click={closePopup} aria-label="Close newsletter popup">×</button>
      <div id="mc_embed_signup">
        <form action="https://irg-listings.us19.list-manage.com/subscribe/post?u=79a060ac083c62360805246c1&amp;id=fe966f6f0e&amp;v_id=4556&amp;f_id=0003bce4f0" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
          <div id="mc_embed_signup_scroll">
            <h2 class="text-[var(--color-text-primary)]">Get Our Exclusive Newsletter</h2>
            <p class="newsletter-description text-[var(--color-text-secondary)]">Join other forward-thinkers and receive our insights directly in your email inbox.</p>
            <div class="mc-field-group">
              <label for="mce-EMAIL" class="text-[var(--color-text-primary)]">Email Address <span class="asterisk">*</span></label>
              <input type="email" name="EMAIL" class="required email" id="mce-EMAIL" required placeholder="Your email address">
            </div>
            <div id="mergeRow-gdpr" class="mergeRow gdpr-mergeRow content__gdprBlock mc-field-group">
              <div class="content__gdpr">
                <label class="checkbox-container text-[var(--color-text-secondary)]" for="gdpr122232">
                  <input type="checkbox" id="gdpr_122232" name="gdpr[122232]" class="gdpr" value="Y" required>
                  <span class="checkmark"></span>
                  <span class="checkbox-text">I agree to receive the newsletter via email. You can unsubscribe at any time.</span>
                </label>
              </div>
            </div>
            <div id="mce-responses" class="clear">
              <div class="response" id="mce-error-response" style="display: none;"></div>
              <div class="response" id="mce-success-response" style="display: none;"></div>
            </div>
            <div aria-hidden="true" style="position: absolute; left: -5000px;">
              <input type="text" name="b_79a060ac083c62360805246c1_fe966f6f0e" tabindex="-1" value="">
            </div>
            <div class="clear">
              <input type="submit" name="subscribe" id="mc-embedded-subscribe" class="button" value="SUBSCRIBE TO NEWSLETTER">
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
{/if}

<style>
  .newsletter-popup-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: auto;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: flex-end;
    z-index: 1000;
  }

  .newsletter-popup {
    background: linear-gradient(135deg, #ffffff, #f0f0f0);
    padding: 2rem;
    border-radius: 12px 12px 0 0;
    width: 100%;
    max-width: 600px;
    position: relative;
  }

  :global(.dark) .newsletter-popup {
    background: linear-gradient(135deg, #2c3e50, #34495e);
  }

  .close-button {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
    color: var(--color-text-primary);
    transition: transform 0.2s ease;
  }

  .close-button:hover {
    transform: scale(1.1);
  }

  /* Override Mailchimp styles */
  :global(#mc_embed_signup) {
    background: transparent !important;
    font-family: 'Arial', sans-serif !important;
    width: 100% !important;
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
    border: 2px solid var(--color-text-secondary) !important;
    border-radius: 4px !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: var(--color-text-primary) !important;
  }

  :global(#mc_embed_signup .checkbox-container) {
    display: flex !important;
    align-items: flex-start !important;
    position: relative !important;
    padding-left: 28px !important;
    margin-bottom: 0.5rem !important;
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

  :global(#mc_embed_signup .checkmark) {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    height: 20px !important;
    width: 20px !important;
    background-color: #eee !important;
    border-radius: 4px !important;
  }

  :global(.dark) :global(#mc_embed_signup .checkmark) {
    background-color: #4a5568 !important;
  }

  :global(#mc_embed_signup .checkbox-container:hover input ~ .checkmark) {
    background-color: #ccc !important;
  }

  :global(.dark) :global(#mc_embed_signup .checkbox-container:hover input ~ .checkmark) {
    background-color: #718096 !important;
  }

  :global(#mc_embed_signup .checkbox-container input:checked ~ .checkmark) {
    background-color: #FF4E50 !important;
  }

  :global(#mc_embed_signup .checkmark:after) {
    content: "" !important;
    position: absolute !important;
    display: none !important;
  }

  :global(#mc_embed_signup .checkbox-container input:checked ~ .checkmark:after) {
    display: block !important;
  }

  :global(#mc_embed_signup .checkbox-container .checkmark:after) {
    left: 6px !important;
    top: 2px !important;
    width: 5px !important;
    height: 10px !important;
    border: solid white !important;
    border-width: 0 3px 3px 0 !important;
    transform: rotate(45deg) !important;
  }

  :global(#mc_embed_signup .checkbox-text) {
    line-height: 1.3 !important;
    font-size: 0.85rem !important;
  }

  :global(#mc_embed_signup .button) {
    background: linear-gradient(45deg, #FF4E50, #F9D423) !important;
    color: white !important;
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
    box-shadow: 0 2px 10px rgba(255, 78, 80, 0.2) !important;
    text-align: center !important;
    line-height: 1 !important;
  }

  :global(#mc_embed_signup .button:hover) {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(255, 78, 80, 0.3) !important;
  }

  @media (max-width: 600px) {
    .newsletter-popup {
      padding: 1.5rem;
      border-radius: 12px 12px 0 0;
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