<script>
    import { darkMode } from '$lib/stores/darkMode';
    import { supabase } from '$lib/utils/supabaseClient';
  
    let email = '';
    let marketingOptIn = false;
    let isLoading = false;
    let message = '';
  
    async function handleSubmit(event) {
      event.preventDefault();
      if (isLoading) return;
  
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
  
        message = 'Thank you for subscribing!';
        email = '';
        marketingOptIn = false;
      } catch (error) {
        console.error('Subscription error:', error);
        message = error.code === '23505' 
          ? 'This email is already subscribed.' 
          : 'Error subscribing. Please try again.';
      } finally {
        isLoading = false;
      }
    }
  </script>
  
  <div class="newsletter-signup" class:dark={$darkMode}>
    <form on:submit={handleSubmit} id="newsletter-subscribe-form" name="newsletter-subscribe-form" class="validate">
      <h2>Subscribe to our newsletter</h2>
      <div class="form-group">
        <label for="email">Email Address <span class="asterisk">*</span></label>
        <input type="email" name="email" class="required email" id="email" required bind:value={email} />
      </div>
      <div class="form-group">
        <label for="marketing_opt_in" class="checkbox-label">
          <input type="checkbox" id="marketing_opt_in" name="marketing_opt_in" class="checkbox" bind:checked={marketingOptIn}>
          <span>I agree to receive marketing emails</span>
        </label>
      </div>
      <div class="form-group">
        <button type="submit" class="button" disabled={isLoading}>
          {isLoading ? 'Subscribing...' : 'Subscribe'}
        </button>
      </div>
      {#if message}
        <p class="message">{message}</p>
      {/if}
      <p class="disclaimer">We respect your privacy. Unsubscribe at any time.</p>
    </form>
  </div>
  
  <style>
    .newsletter-signup {
      --bg-color: #ffffff;
      --text-color: #2c3e50;
      --input-bg: #f8f9fa;
      --input-border: #ced4da;
      --button-bg: #2c3e50;
      --button-text: #ffffff;
      --button-hover: #34495e;
      --disclaimer-color: #6c757d;
  
      max-width: 500px;
      margin: 2rem auto;
      padding: 2rem;
      background-color: var(--bg-color);
      color: var(--text-color);
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
    }
  
    :global(.dark) .newsletter-signup {
      --bg-color: #1f2937;
      --text-color: #e5e7eb;
      --input-bg: #374151;
      --input-border: #4b5563;
      --button-bg: #e5e7eb;
      --button-text: #1f2937;
      --button-hover: #d1d5db;
      --disclaimer-color: #9ca3af;
    }
  
    h2 {
      font-size: 1.5rem;
      margin-bottom: 1rem;
      text-align: center;
      color: var(--text-color);
    }
  
    .form-group {
      margin-bottom: 1rem;
    }
  
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 600;
      color: var(--text-color);
    }
  
    input[type="email"] {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid var(--input-border);
      border-radius: 4px;
      background-color: var(--input-bg);
      color: var(--text-color);
    }
  
    .checkbox-label {
      display: flex;
      align-items: center;
      cursor: pointer;
    }
  
    .checkbox {
      margin-right: 0.5rem;
    }
  
    .button {
      display: inline-block;
      width: 100%;
      padding: 0.75rem 1rem;
      background-color: var(--button-bg);
      color: var(--button-text);
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      font-size: 1rem;
      font-weight: 600;
    }
  
    .button:hover {
      background-color: var(--button-hover);
    }
  
    .button:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }
  
    .message {
      text-align: center;
      margin-top: 1rem;
      font-weight: bold;
      color: var(--text-color);
    }
  
    .disclaimer {
      font-size: 0.8rem;
      text-align: center;
      margin-top: 1rem;
      color: var(--disclaimer-color);
    }
  
    @media (max-width: 768px) {
      .newsletter-signup {
        padding: 1rem;
        margin: 1rem auto;
      }
    }
  </style>