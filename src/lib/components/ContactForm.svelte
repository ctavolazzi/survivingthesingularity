<script>
  import { darkMode } from '$lib/stores/darkMode';
  import { supabase } from '$lib/utils/supabaseClient';
  import { fade } from 'svelte/transition';
  import { goto } from '$app/navigation';

  let name = '';
  let email = '';
  let subject = '';
  let message = '';
  let isLoading = false;
  let isSubmitted = false;
  let isSuccess = false;

  const exploreOptions = [
    { title: 'Explore Our Blog', path: '/blog' },
    { title: 'Read a Book Sample', path: '/sample' },
    { title: 'Download the Free Guide', path: '/download' }
  ];

  async function handleSubmit(event) {
    event.preventDefault();
    if (isLoading) return;

    isLoading = true;

    try {
      const { error } = await supabase
        .from('contact_requests')
        .insert([{ name, email, subject, message }]);

      if (error) throw error;

      isSuccess = true;
    } catch (error) {
      console.error('Submission error:', error);
      isSuccess = false;
    } finally {
      isLoading = false;
      isSubmitted = true;
    }
  }

  function handleExplore(path) {
    goto(path);
  }
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
          <p>There was an error submitting your message. Please try again later or contact us directly.</p>
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
  </div>
  <p class="disclaimer">We respect your privacy and will never share your information.</p>
</div>

<style>
  .contact-form {
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
    height: 600px; /* Fixed height */
    display: flex;
    flex-direction: column;
  }

  :global(.dark) .contact-form {
    --bg-color: #1f2937;
    --text-color: #e5e7eb;
    --input-bg: #374151;
    --input-border: #4b5563;
    --button-bg: #e5e7eb;
    --button-text: #1f2937;
    --button-hover: #d1d5db;
    --disclaimer-color: #9ca3af;
  }

  .form-content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
    color: var(--text-color);
  }

  h3 {
    font-size: 1.2rem;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
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

  input[type="text"],
  input[type="email"],
  textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid var(--input-border);
    border-radius: 4px;
    background-color: var(--input-bg);
    color: var(--text-color);
  }

  textarea {
    height: 100px;
    resize: vertical;
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
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
  }

  .explore-button {
    max-width: 150px;
    font-size: 0.9rem;
  }

  .disclaimer {
    font-size: 0.8rem;
    text-align: center;
    margin-top: 1rem;
    color: var(--disclaimer-color);
  }

  @media (max-width: 768px) {
    .contact-form {
      padding: 1rem;
      margin: 1rem auto;
      height: 550px; /* Slightly reduced height for mobile */
    }

    .explore-options {
      grid-template-columns: 1fr;
    }

    .explore-button {
      max-width: 200px;
    }
  }
</style>