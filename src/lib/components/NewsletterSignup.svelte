<script>
    import { darkMode } from '$lib/stores/darkMode';
    import Button from '$lib/components/ui/Button.svelte';
    import Input from '$lib/components/ui/Input.svelte';
    import Checkbox from '$lib/components/ui/Checkbox.svelte';

    let email = '';
    let marketingOptIn = false;
    let isLoading = false;
    let message = '';
    let emailError = '';

    async function handleSubmit(event) {
      event.preventDefault();
      if (isLoading) return;

      isLoading = true;
      message = '';
      emailError = '';

      try {
        const response = await fetch('/api/newsletter/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: email.trim(),
            marketingOptIn
          })
        });

        const result = await response.json();

        if (!response.ok) {
          if (response.status === 400) {
            emailError = result.error;
            throw new Error(result.error);
          } else if (response.status === 409) {
            throw new Error(result.error);
          } else {
            throw new Error('Server error. Please try again later.');
          }
        }

        message = 'Thank you for subscribing!';
        email = '';
        marketingOptIn = false;
      } catch (error) {
        console.error('Subscription error:', error);
        message = error.message || 'Error subscribing. Please try again.';
      } finally {
        isLoading = false;
      }
    }

    function handleEmailInput(event) {
      email = event.detail.target.value;
      emailError = '';
    }
  </script>

  <div class="newsletter-signup rounded-lg shadow-md p-6 bg-white dark:bg-gray-800" class:dark={$darkMode}>
    <form on:submit={handleSubmit} id="newsletter-subscribe-form" name="newsletter-subscribe-form">
      <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Subscribe to our newsletter</h2>

      <Input
        type="email"
        id="newsletter-email"
        name="email"
        label="Email Address"
        required={true}
        value={email}
        error={emailError}
        on:input={handleEmailInput}
        placeholder="your@email.com"
        disabled={isLoading}
      />

      <Checkbox
        id="marketing_opt_in"
        label="I agree to receive marketing emails"
        checked={marketingOptIn}
        on:change={e => marketingOptIn = e.detail.checked}
      />

      <div class="mt-4">
        <Button
          type="submit"
          variant="primary"
          fullWidth={true}
          loading={isLoading}
          disabled={isLoading}
        >
          {isLoading ? 'Subscribing...' : 'Subscribe'}
        </Button>
      </div>

      {#if message}
        <p class="mt-3 text-center font-medium {message.includes('Error') ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'}">
          {message}
        </p>
      {/if}

      <p class="text-xs text-center mt-4 text-gray-500 dark:text-gray-400">
        We respect your privacy. Unsubscribe at any time.
      </p>
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