<script>
  import { darkMode } from '$lib/stores/darkMode';
  import { fade } from 'svelte/transition';
  import { goto } from '$app/navigation';

  let name = '';
  let email = '';
  let subject = '';
  let message = '';
  let isLoading = false;
  let isSubmitted = false;
  let isSuccess = false;
  let errorMessage = '';

  const exploreOptions = [
    { title: 'Explore Our Blog', path: '/blog' },
    { title: 'Read a Book Sample', path: '/sample' },
    { title: 'Download the Free Guide', path: '/download' },
    { title: 'Join Our Newsletter', path: '/newsletter' }
  ];

  async function handleSubmit(event) {
    event.preventDefault();
    if (isLoading) return;

    isLoading = true;
    errorMessage = '';

    try {
      // Using the specific Formspree endpoint
      const response = await fetch('https://formspree.io/f/xgvawenl', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name,
          email,
          subject: subject || 'Contact Form Submission',
          message,
          _gotcha: '' // This is the honeypot field
        })
      });

      if (!response.ok) {
        const result = await response.json();
        throw new Error(result.error || 'Failed to submit form');
      }

      isSuccess = true;
    } catch (error) {
      console.error('Submission error:', error);
      isSuccess = false;
      errorMessage = error.message || 'An unexpected error occurred. Please try again later.';
    } finally {
      isLoading = false;
      isSubmitted = true;
    }
  }

  function handleExplore(path) {
    goto(path);
  }

  // Format the subject line
  $: formattedSubject = subject ? `Contact Form: ${subject}` : 'Contact Form Submission';

  // Format the body with name and email
  $: formattedBody = `Name: ${name}
Email: ${email}

Message:
${message}`;
</script>

<div class="contact-form" class:dark={$darkMode}>
  <div class="form-content">
    {#if !isSubmitted}
      <form on:submit={handleSubmit} id="contact-form" name="contact-form" class="validate">
        <h2>Contact Us</h2>
        <div class="form-group">
          <label for="name">Name <span class="asterisk">*</span></label>
          <input type="text" name="name" class="required" id="name" required bind:value={name} />
        </div>
        <div class="form-group">
          <label for="email">Email Address <span class="asterisk">*</span></label>
          <input type="email" name="email" class="required email" id="email" required bind:value={email} />
        </div>
        <div class="form-group">
          <label for="subject">Subject</label>
          <input type="text" name="subject" id="subject" bind:value={subject} />
        </div>
        <div class="form-group">
          <label for="message">Message <span class="asterisk">*</span></label>
          <textarea name="message" class="required" id="message" required bind:value={message}></textarea>
        </div>
        <!-- Honeypot field to prevent spam -->
        <div style="display:none">
          <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" />
        </div>
        <div class="form-group">
          <button type="submit" class="button" disabled={isLoading}>
            {isLoading ? 'Sending...' : 'Send Message'}
          </button>
        </div>
      </form>
    {:else}
      <div class="response-message" transition:fade>
        {#if isSuccess}
          <h2>Thank You!</h2>
          <p>Your message has been sent successfully. We'll get back to you soon!</p>
        {:else}
          <h2>Oops!</h2>
          <p>There was an error submitting your message. {errorMessage}</p>
          <button class="button retry-button" on:click={() => isSubmitted = false}>Try Again</button>
        {/if}
        <h3>While you wait, why not explore more?</h3>
        <div class="explore-options">
          {#each exploreOptions as option}
            <button class="button explore-button" on:click={() => handleExplore(option.path)}>
              {option.title}
            </button>
          {/each}
        </div>
      </div>
    {/if}
    <p class="disclaimer">We respect your privacy and will never share your information.</p>
  </div>
</div>

<style>
  .contact-form {
    --bg-color: transparent;
    --text-color: #2c3e50;
    --input-bg: #ffffff;
    --input-border: #e2e8f0;
    --button-bg: linear-gradient(135deg, #f97316, #f59e0b);
    --button-text: #ffffff;
    --button-hover: linear-gradient(135deg, #ea580c, #d97706);
    --disclaimer-color: #6c757d;

    width: 100%;
    margin: 0 auto;
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: all 0.3s ease;
    height: auto;
    display: flex;
    flex-direction: column;
  }

  :global(.dark) .contact-form {
    --bg-color: transparent;
    --text-color: #e5e7eb;
    --input-bg: rgba(55, 65, 81, 0.8);
    --input-border: #4b5563;
    --button-bg: linear-gradient(135deg, #f97316, #f59e0b);
    --button-text: #ffffff;
    --button-hover: linear-gradient(135deg, #ea580c, #d97706);
    --disclaimer-color: #9ca3af;
  }

  .form-content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
  }

  form, .response-message {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
    color: var(--text-color);
    font-weight: 700;
  }

  h3 {
    font-size: 1.2rem;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
    color: var(--text-color);
  }

  .form-group {
    margin-bottom: 1.25rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--text-color);
    font-size: 0.9rem;
  }

  .asterisk {
    color: #f97316;
  }

  input[type="text"],
  input[type="email"],
  textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--input-border);
    border-radius: 0.5rem;
    background-color: var(--input-bg);
    color: var(--text-color);
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  }

  input[type="text"]:focus,
  input[type="email"]:focus,
  textarea:focus {
    outline: none;
    border-color: #f97316;
    box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.2);
  }

  textarea {
    height: 120px;
    resize: vertical;
  }

  .button {
    display: inline-block;
    width: 100%;
    padding: 0.75rem 1rem;
    background: var(--button-bg);
    color: var(--button-text);
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .button:hover {
    background: var(--button-hover);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
  }

  .button:active {
    transform: translateY(0);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .response-message {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
  }

  .response-message p {
    margin-top: 1rem;
    margin-bottom: 1rem;
    font-size: 1.1rem;
    line-height: 1.6;
  }

  .explore-options {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-top: 1rem;
    width: 100%;
    justify-items: center;
  }

  .explore-button {
    width: 100%;
    max-width: 180px;
    font-size: 0.9rem;
  }

  .disclaimer {
    font-size: 0.8rem;
    text-align: center;
    color: var(--disclaimer-color);
    padding-top: 1rem; /* Added padding */
    margin-top: auto; /* Push to the bottom */
    margin-bottom: 0;
  }

  @media (max-width: 768px) {
    .contact-form {
      padding: 1rem;
      margin: 1rem auto;
      height: auto; /* Change fixed height to auto */
      min-height: auto; /* Remove minimum height on mobile */
    }

    .explore-options {
      grid-template-columns: 1fr;
    }

    .explore-button {
      max-width: 200px;
    }
  }

  .hidden {
    display: none;
  }

  .retry-button {
    margin-top: 1rem;
    max-width: 200px;
  }
</style>