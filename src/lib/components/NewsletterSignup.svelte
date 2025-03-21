<script>
    import { darkMode } from '$lib/stores/darkMode';
    import Button from '$lib/components/ui/Button.svelte';
    import Input from '$lib/components/ui/Input.svelte';
    import Checkbox from '$lib/components/ui/Checkbox.svelte';
    import { fade, fly } from 'svelte/transition';
    import { elasticOut } from 'svelte/easing';

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

  <div class="newsletter-signup" class:dark={$darkMode}>
    {#if isSuccess}
      <div class="success-message" in:fly={{ y: 20, duration: 500, easing: elasticOut }}>
        <div class="checkmark-circle">
          <div class="checkmark"></div>
        </div>
        <h2 class="success-title">Welcome Aboard! 🚀</h2>
        <p class="success-text">{message}</p>
        <p class="success-subtext">
          Get ready for insights that will help you thrive in the age of AI.
        </p>
      </div>
    {:else}
      <form on:submit={handleSubmit} id="newsletter-subscribe-form" name="newsletter-subscribe-form">
        <div class="form-header">
          <h2>Join Our Newsletter</h2>
          <p class="subtitle">
            Stay ahead of AI developments with curated insights and practical strategies.
          </p>
        </div>

        <div class="form-content">
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

          <div class="checkbox-wrapper">
            <Checkbox
              id="marketing_opt_in"
              label="Send me updates about surviving the AI revolution"
              checked={marketingOptIn}
              on:change={e => marketingOptIn = e.detail.checked}
            />
          </div>

          <div class="button-wrapper">
            <Button
              type="submit"
              variant="primary"
              fullWidth={true}
              loading={isLoading}
              disabled={isLoading}
            >
              {isLoading ? 'Joining...' : 'Join Newsletter'}
            </Button>
          </div>

          {#if message && !isSuccess}
            <p class="error-message" in:fade={{ duration: 200 }}>
              {message}
            </p>
          {/if}

          <p class="privacy-notice">
            We value your privacy. Unsubscribe anytime with one click.
          </p>
        </div>
      </form>
    {/if}
  </div>

  <style>
    .newsletter-signup {
      --gradient-start: rgba(59, 130, 246, 0.1);
      --gradient-end: rgba(147, 51, 234, 0.1);
      --border-color: rgba(59, 130, 246, 0.2);
      --text-primary: #1a1a1a;
      --text-secondary: #4a5568;
      --success-color: #4ade80;
      --error-color: #ef4444;

      width: 100%;
      max-width: min(500px, 100% - 2rem);
      margin: 2rem auto;
      padding: 2rem;
      background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
      border: 1px solid var(--border-color);
      border-radius: 16px;
      box-shadow:
        0 4px 6px -1px rgba(0, 0, 0, 0.1),
        0 2px 4px -1px rgba(0, 0, 0, 0.06),
        inset 0 2px 4px rgba(255, 255, 255, 0.1);
      transition: all 0.3s ease;
    }

    .newsletter-signup:hover {
      box-shadow:
        0 10px 15px -3px rgba(0, 0, 0, 0.1),
        0 4px 6px -2px rgba(0, 0, 0, 0.05),
        inset 0 2px 4px rgba(255, 255, 255, 0.1);
      transform: translateY(-2px);
    }

    :global(.dark) .newsletter-signup {
      --gradient-start: rgba(59, 130, 246, 0.05);
      --gradient-end: rgba(147, 51, 234, 0.05);
      --border-color: rgba(59, 130, 246, 0.1);
      --text-primary: #e5e7eb;
      --text-secondary: #9ca3af;
    }

    .form-header {
      text-align: center;
      margin-bottom: 2rem;
    }

    h2 {
      font-size: 1.75rem;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 0.75rem;
      letter-spacing: -0.025em;
    }

    .subtitle {
      color: var(--text-secondary);
      font-size: 1rem;
      line-height: 1.5;
      max-width: 90%;
      margin: 0 auto;
    }

    .form-content {
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .checkbox-wrapper {
      margin-top: -0.5rem;
    }

    .button-wrapper {
      margin-top: 0.5rem;
    }

    .privacy-notice {
      text-align: center;
      font-size: 0.875rem;
      color: var(--text-secondary);
      margin-top: 1rem;
    }

    .success-message {
      text-align: center;
      padding: 2rem 1rem;
    }

    .success-title {
      color: var(--text-primary);
      font-size: 1.5rem;
      font-weight: 700;
      margin: 1rem 0;
    }

    .success-text {
      color: var(--text-primary);
      font-size: 1.125rem;
      margin-bottom: 1rem;
    }

    .success-subtext {
      color: var(--text-secondary);
      font-size: 0.875rem;
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

    .error-message {
      text-align: center;
      color: var(--error-color);
      font-size: 0.875rem;
      font-weight: 500;
      padding: 0.5rem;
      border-radius: 6px;
      background: rgba(239, 68, 68, 0.1);
    }

    @keyframes pulse {
      0% {
        box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.4);
      }
      70% {
        box-shadow: 0 0 0 10px rgba(74, 222, 128, 0);
      }
      100% {
        box-shadow: 0 0 0 0 rgba(74, 222, 128, 0);
      }
    }

    @keyframes checkmark {
      0% {
        height: 0;
        width: 0;
        opacity: 1;
      }
      20% {
        height: 0;
        width: 100%;
        opacity: 1;
      }
      40% {
        height: 100%;
        width: 100%;
        opacity: 1;
      }
    }

    @media (max-width: 768px) {
      .newsletter-signup {
        margin: 1.5rem auto;
        padding: 1.5rem;
      }

      h2 {
        font-size: 1.5rem;
      }

      .subtitle {
        font-size: 0.875rem;
      }
    }

    @media (max-width: 480px) {
      .newsletter-signup {
        margin: 1rem auto;
        padding: 1.25rem;
      }

      .form-header {
        margin-bottom: 1.5rem;
      }

      h2 {
        font-size: 1.25rem;
      }

      .form-content {
        gap: 1rem;
      }
    }
  </style>