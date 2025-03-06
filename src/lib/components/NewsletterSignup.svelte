<script>
    import { darkMode } from '$lib/stores/darkMode';
    import Button from '$lib/components/ui/Button.svelte';
    import Input from '$lib/components/ui/Input.svelte';
    import Checkbox from '$lib/components/ui/Checkbox.svelte';
    import { fade } from 'svelte/transition';

    let email = '';
    let marketingOptIn = true; // Default to checked for better conversion
    let isLoading = false;
    let message = '';
    let emailError = '';
    let isSuccess = false;

    async function handleSubmit(event) {
      event.preventDefault();
      if (isLoading) return;

      isLoading = true;
      message = '';
      emailError = '';
      isSuccess = false;

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
            throw new Error(result.error || 'Server error. Please try again later.');
          }
        }

        // Success!
        isSuccess = true;
        message = result.message || 'Thank you for subscribing to the Surviving the Singularity newsletter!';
        email = '';
        marketingOptIn = true;
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
    {#if isSuccess}
      <div class="success-message" in:fade={{ duration: 300 }}>
        <div class="checkmark-circle">
          <div class="checkmark"></div>
        </div>
        <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Subscription Successful!</h2>
        <p class="text-center text-green-600 dark:text-green-400 mb-4">{message}</p>
        <p class="text-sm text-center text-gray-600 dark:text-gray-400">
          We've added your email to our list. You'll be the first to know about new content and updates.
        </p>
      </div>
    {:else}
      <form on:submit={handleSubmit} id="newsletter-subscribe-form" name="newsletter-subscribe-form">
        <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Subscribe to our newsletter</h2>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
          Stay updated with the latest insights on AI, technology, and the future of humanity.
        </p>

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
          label="I agree to receive marketing emails about Surviving the Singularity"
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

        {#if message && !isSuccess}
          <p class="mt-3 text-center font-medium text-red-600 dark:text-red-400">
            {message}
          </p>
        {/if}

        <p class="text-xs text-center mt-4 text-gray-500 dark:text-gray-400">
          We respect your privacy. Unsubscribe at any time.
        </p>
      </form>
    {/if}
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

      width: 100%;
      max-width: min(500px, 100% - 2rem);
      margin: 2rem auto;
      padding: min(2rem, 5vw);
      background-color: var(--bg-color);
      color: var(--text-color);
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
      box-sizing: border-box;
    }

    /* Ensure form elements stay within bounds */
    .newsletter-signup form {
      width: 100%;
      max-width: 100%;
    }

    .newsletter-signup input,
    .newsletter-signup button {
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
    }

    /* Ensure text content wraps properly */
    .newsletter-signup h2,
    .newsletter-signup p {
      max-width: 100%;
      overflow-wrap: break-word;
      word-wrap: break-word;
      word-break: break-word;
      hyphens: auto;
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

    .success-message {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 1rem;
    }

    .checkmark-circle {
      width: 60px;
      height: 60px;
      position: relative;
      display: inline-block;
      vertical-align: top;
      margin-bottom: 1rem;
    }

    .checkmark-circle .checkmark {
      border-radius: 5px;
    }

    .checkmark-circle .checkmark:after {
      content: '';
      display: block;
      width: 25px;
      height: 50px;
      border: solid #4ade80;
      border-width: 0 4px 4px 0;
      transform: rotate(45deg);
      position: absolute;
      top: 0;
      left: 18px;
    }

    @media (max-width: 768px) {
      .newsletter-signup {
        margin: 1rem auto;
        padding: min(1.5rem, 4vw);
      }
    }

    @media (max-width: 480px) {
      .newsletter-signup {
        margin: 0.5rem auto;
        padding: min(1rem, 3vw);
      }
    }
  </style>