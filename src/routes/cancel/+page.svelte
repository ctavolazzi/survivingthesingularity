<script>
  import { enhance } from '$app/forms';
  import { goto } from '$app/navigation';
  import Countdown from '$lib/components/Countdown.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import ContactForm from '$lib/components/ContactForm.svelte';
  import { onMount } from 'svelte';

  let cancellationSuccess = false;
  let error = '';
  let isLoading = false;

  const targetDate = new Date("2027-11-20T23:59:59").getTime();

  // Redirect to home page after a short delay
  onMount(() => {
    const timer = setTimeout(() => {
      goto('/');
    }, 0); // Immediate redirect

    return () => clearTimeout(timer);
  });

  const handleSubmit = () => {
    return async ({ result }) => {
      if (result.type === 'success') {
        cancellationSuccess = true;
      } else {
        error = 'An error occurred during cancellation. Please try again.';
      }
    };
  };

  async function handlePreorder() {
    isLoading = true;
    error = null;

    try {
      const response = await fetch('/api/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const { url } = await response.json();

      // Redirect to Stripe Checkout
      window.location.href = url;
    } catch (err) {
      console.error('Preorder error:', err);
      error = 'An error occurred. Please try again.';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="main-content">
  <Countdown {targetDate} />

  <div class="stylish-divider"></div>

  <h1>Redirecting to Home Page...</h1>

  <p class="centered-text">Please wait while we redirect you...</p>

  <div class="stylish-divider"></div>

  <Spacer height="1rem"/>
</div>

<style>
  .main-content {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    color: var(--color-text-primary);
    text-align: center;
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
  }

  .quote-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1rem 0;
    padding: 1rem;
  }

  .quote {
    font-style: italic;
    font-size: 1.8rem;
    text-align: center;
    margin: 0;
    line-height: 1.4;
    font-weight: 500;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  }

  .attribution {
    font-weight: bold;
    margin-top: 1rem;
    font-size: 1.2rem;
    color: var(--color-text-secondary);
  }

  .button-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .big-button {
    font-weight: 600;
    font-size: 1.2rem;
    border-radius: 6px;
    padding: 1rem 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }

  .cancel-button {
    background-color: var(--color-bg-secondary);
    color: var(--color-text-primary);
    border: 1px solid var(--color-border);
  }

  .preorder-button {
    background-color: #ff6600;
    color: white;
    border: none;
  }

  .big-button:hover {
    box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    transform: translateY(-3px);
  }

  .cancel-button:hover {
    background-color: var(--color-bg-hover);
  }

  .preorder-button:hover {
    background-color: #ff8533;
  }

  .stylish-divider {
    height: 2px;
    background-image: linear-gradient(to right, rgba(255, 102, 0, 0), rgba(255, 102, 0, 0.75), rgba(255, 102, 0, 0));
    margin: 2.5rem auto;
    max-width: 80%;
  }

  .benefits-container {
    background-color: var(--color-bg-secondary);
    border: 2px solid #ff6600;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1.5rem auto;
    max-width: 600px;
  }

  .benefits-container h2 {
    font-size: 1.4rem;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
  }

  .benefits-container ul {
    text-align: left;
    display: inline-block;
    margin: 0 auto;
  }

  .benefits-container li {
    color: var(--color-text-secondary);
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
  }

  .error {
    color: #ff3333;
    text-align: center;
    font-weight: bold;
  }

  .loader {
    display: inline-block;
    width: 24px;
    height: 24px;
    border: 3px solid #ffffff;
    border-radius: 50%;
    border-top-color: #ff6600;
    animation: spin 1s ease-in-out infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .urgency-message {
    background-color: #fff3e6;
    border: 2px solid #ff6600;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1.5rem auto;
    text-align: center;
    color: #ff6600;
    font-weight: bold;
    font-size: 1.2rem;
    max-width: 600px;
  }

  :global(.dark) .urgency-message {
    background-color: #4d2600;
    color: #ff9933;
  }

  .centered-text {
    text-align: center;
    font-size: 1.1rem;
    margin: 1rem 0;
  }

  @media (max-width: 768px) {
    .button-container {
      flex-direction: column;
    }

    .big-button {
      width: 100%;
    }
  }
</style>