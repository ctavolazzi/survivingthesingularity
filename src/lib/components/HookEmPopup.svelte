<script>
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { elasticOut, backOut, quintOut } from 'svelte/easing';
  import { supabase } from '$lib/utils/supabaseClient';
  import { createEventDispatcher } from 'svelte';

  export let isOpen = false;

  const dispatch = createEventDispatcher();

  let name = '';
  let email = '';
  let address = '';
  let city = '';
  let state = '';
  let zipCode = '';
  let country = '';
  let age = '';
  let occupation = '';
  let interests = '';
  let isLoading = false;
  let message = '';
  let isSuccess = false;
  let isSubmitted = false;
  let errorCode = '';

  let currentStep = 1;
  const totalSteps = 3;

  let slideDirection = 1; // 1 for forward, -1 for backward

  function nextStep() {
    if (currentStep < totalSteps) {
      slideDirection = 1;
      currentStep++;
    }
  }

  function prevStep() {
    if (currentStep > 1) {
      slideDirection = -1;
      currentStep--;
    }
  }

  function goToStep(step) {
    if (step >= 1 && step <= totalSteps) {
      slideDirection = step > currentStep ? 1 : -1;
      currentStep = step;
    }
  }

  function goToHomePage() {
    window.location.href = '/'; // Adjust this if your home page URL is different
  }

  async function handleSubmit(event) {
    event.preventDefault();
    isLoading = true;
    isSubmitted = true;
    message = '';
    errorCode = '';

    try {
      const { error } = await supabase
        .from('hooked_leads')
        .insert([{
          name,
          email,
          address,
          city,
          state,
          zip_code: zipCode,
          country,
          age: age ? parseInt(age) : null,
          occupation,
          interests: interests.split(',').map(i => i.trim())
        }]);

      if (error) throw error;

      isSuccess = true;
      message = 'Thank you for joining the Singularity Survival Club!';
    } catch (error) {
      console.error('Submission error:', error);
      isSuccess = false;
      errorCode = error.code;
      if (error.code === '23505') {
        message = 'This email address is already registered. Please use a different email or contact support if you believe this is an error.';
      } else {
        message = 'Error submitting your information. Please try again.';
      }
    } finally {
      isLoading = false;
    }
  }

  function resetForm() {
    name = '';
    email = '';
    address = '';
    city = '';
    state = '';
    zipCode = '';
    country = '';
    age = '';
    occupation = '';
    interests = '';
    message = '';
    isSuccess = false;
    isSubmitted = false;
    errorCode = '';
    currentStep = 1;
  }

  function closePopup() {
    isOpen = false;
    resetForm();
    dispatch('close');
  }
</script>

{#if isOpen}
  <div class="popup-overlay" transition:fade="{{ duration: 300 }}" on:click|self={closePopup}>
    <div class="popup"
         in:fly="{{ y: 100, duration: 800, easing: backOut }}"
         out:fade="{{ duration: 300 }}">
      <button class="close-button" on:click={closePopup} aria-label="Close popup">×</button>
      <div class="popup-content">
        {#if isSubmitted}
          {#if isLoading}
            <div class="loading-message">
              <h2>Submitting...</h2>
              <div class="spinner"></div>
            </div>
          {:else if isSuccess}
            <div class="success-message" in:fade="{{ duration: 300 }}">
              <h2>Welcome to the Singularity Survival Club!</h2>
              <p>Thank you for joining us on this exciting journey into the future. Here's what you can expect:</p>
              <ul>
                <li><span class="icon">📧</span> A welcome email within the next 24 hours with important information</li>
                <li><span class="icon">📊</span> Weekly newsletters with cutting-edge insights and survival tips</li>
                <li><span class="icon">🎟️</span> Exclusive access to our member-only webinars and events</li>
              </ul>
              <h3>Next steps:</h3>
              <ol>
                <li><span class="icon">✉️</span> Check your email (including spam folder) for our welcome message</li>
                <li><span class="icon">🌐</span> Follow us on social media for daily updates and discussions</li>
                <li><span class="icon">🔍</span> Start exploring our online resources to prepare for the future</li>
              </ol>
              <p class="motto">Remember, the future is what we make it. Together, we'll be ready for anything!</p>
              <button class="home-button" on:click={goToHomePage}>Explore Our Website</button>
            </div>
          {:else}
            <div class="error-message" in:fade="{{ duration: 300 }}">
              <h2>Submission Error</h2>
              <p>{message}</p>
              <p>Error code: {errorCode}</p>
            </div>
          {/if}
        {:else}
          <div class="step-indicator">
            {#each Array(totalSteps) as _, i}
              <button
                class="step-dot"
                class:active={currentStep === i + 1}
                on:click={() => goToStep(i + 1)}
                aria-label="Go to step {i + 1}"
              ></button>
            {/each}
          </div>

          {#key currentStep}
            <div
              class="step"
              in:fly="{{ x: 100 * slideDirection, duration: 300, easing: quintOut }}"
              out:fly="{{ x: -100 * slideDirection, duration: 300, easing: quintOut }}"
            >
              {#if currentStep === 1}
                <div class="step" in:fade>
                  <h2>Join the Singularity Survival Club</h2>
                  <p class="subtitle">Prepare for tomorrow, today.</p>
                  <div class="feature-list">
                    <div class="feature" transition:scale>
                      <span class="icon">🧠</span>
                      <h3>Cutting-edge Insights</h3>
                      <p>Access to the latest AI developments and their potential impacts.</p>
                    </div>
                    <div class="feature" transition:scale>
                      <span class="icon">🛡️</span>
                      <h3>Survival Strategies</h3>
                      <p>Learn how to adapt and thrive in a rapidly changing world.</p>
                    </div>
                    <div class="feature" transition:scale>
                      <span class="icon">🌐</span>
                      <h3>Global Community</h3>
                      <p>Connect with like-minded individuals from around the world.</p>
                    </div>
                  </div>
                  <div class="button-group">
                    <button class="next-button" on:click={nextStep}>Continue</button>
                  </div>
                </div>
              {:else if currentStep === 2}
                <h2>What You'll Receive</h2>
                <ul class="benefits-list">
                  {#each ['Weekly newsletters with exclusive content', 'Invitations to members-only webinars and events', 'Access to our private online community', 'Early access to AI-related tools and resources', 'Personalized survival readiness assessments'] as benefit}
                    <li transition:slide|local="{{ duration: 200, easing: quintOut }}">{benefit}</li>
                  {/each}
                </ul>
                <div class="button-group with-back">
                  <button class="prev-button" on:click={prevStep}>Back</button>
                  <button class="next-button" on:click={nextStep}>Join Now</button>
                </div>
              {:else}
                <div class="step" in:fade>
                  <h2>Complete Your Enrollment</h2>
                  <p class="subtitle">Join us in shaping the future.</p>
                  <form on:submit={handleSubmit}>
                    <div class="form-grid">
                      <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" id="name" bind:value={name} required>
                      </div>
                      <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" bind:value={email} required>
                      </div>
                      <div class="form-group">
                        <label for="address">Address</label>
                        <input type="text" id="address" bind:value={address}>
                      </div>
                      <div class="form-group">
                        <label for="city">City</label>
                        <input type="text" id="city" bind:value={city}>
                      </div>
                      <div class="form-group">
                        <label for="state">State</label>
                        <input type="text" id="state" bind:value={state}>
                      </div>
                      <div class="form-group">
                        <label for="zipCode">Zip Code</label>
                        <input type="text" id="zipCode" bind:value={zipCode}>
                      </div>
                      <div class="form-group">
                        <label for="country">Country</label>
                        <input type="text" id="country" bind:value={country}>
                      </div>
                      <div class="form-group">
                        <label for="age">Age</label>
                        <input type="number" id="age" bind:value={age}>
                      </div>
                      <div class="form-group">
                        <label for="occupation">Occupation</label>
                        <input type="text" id="occupation" bind:value={occupation}>
                      </div>
                      <div class="form-group">
                        <label for="interests">Interests (comma-separated)</label>
                        <input type="text" id="interests" bind:value={interests}>
                      </div>
                    </div>

                    <div class="button-container">
                      <button type="button" class="prev-button" on:click={prevStep}>
                        <span class="arrow">←</span> Back
                      </button>
                      <button class="next-button">
                        ENLIST NOW <span class="arrow">→</span>
                      </button>
                    </div>
                    <p class="disclaimer">By enlisting, you agree to receive communications about our community and singularity-related topics. We respect your privacy and will never share your information.</p>
                  </form>
                </div>
              {/if}
            </div>
          {/key}
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.75);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    backdrop-filter: blur(8px);
  }

  .popup {
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    padding: 3rem;
    position: relative;
    transition: background-color 0.3s ease;
  }

  .close-button {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: var(--color-text-primary, #2d3748);
    transition: color 0.3s ease, transform 0.3s ease;
  }

  .close-button:hover {
    color: var(--color-primary, #ff7708);
    transform: rotate(90deg);
  }

  h2 {
    font-family: 'Orbitron', sans-serif;
    color: var(--color-primary, #ff7708);
    margin-bottom: 0.5rem;
    text-align: center;
    font-size: 2.2rem;
    text-transform: uppercase;
    letter-spacing: 2px;
  }

  .subtitle {
    text-align: center;
    color: var(--color-text-secondary, #4a5568);
    margin-bottom: 2rem;
    font-size: 1.1rem;
  }

  .form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
  }

  label {
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: var(--color-text-secondary, #4a5568);
  }

  input {
    padding: 0.75rem;
    border: 2px solid var(--color-border, #e2e8f0);
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background-color: var(--color-bg-secondary, #f7fafc);
    color: var(--color-text-primary, #2d3748);
  }

  input[type="number"] {
    -moz-appearance: textfield;
  }

  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  input:focus {
    outline: none;
    border-color: var(--color-primary, #ff7708);
    box-shadow: 0 0 0 3px rgba(255, 119, 8, 0.2);
  }

  button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(255, 119, 8, 0.3);
  }

  .loading-message,
  .success-message,
  .error-message {
    text-align: center;
    padding: 2rem;
  }

  .loading-message h2,
  .success-message h2,
  .error-message h2 {
    margin-bottom: 1rem;
  }

  .error-message {
    color: #e53e3e;
  }

  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .success-message {
    text-align: left;
    padding: 2rem;
    background: rgba(26, 32, 44, 0.8);
    border-radius: 12px;
    box-shadow: 0 0 40px 20px rgba(26, 32, 44, 0.8);
    position: relative;
    overflow: hidden;
  }

  .success-message::before {
    content: '';
    position: absolute;
    top: -10px;
    left: -10px;
    right: -10px;
    bottom: -10px;
    background: inherit;
    filter: blur(10px);
    z-index: -1;
  }

  .success-message h2 {
    font-family: 'Orbitron', sans-serif;
    color: #ff7708;
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 2rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 0 2px 4px rgba(255, 119, 8, 0.3);
  }

  .success-message h3 {
    font-family: 'Orbitron', sans-serif;
    color: #ff9933;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .success-message p {
    margin-bottom: 1rem;
    line-height: 1.6;
    color: #e2e8f0;
  }

  .success-message ul, .success-message ol {
    margin-left: 0;
    margin-bottom: 1rem;
    list-style-type: none;
  }

  .success-message li {
    margin-bottom: 1rem;
    line-height: 1.4;
    color: #e2e8f0;
    display: flex;
    align-items: center;
  }

  .success-message .icon {
    margin-right: 0.5rem;
    font-size: 1.2em;
  }

  .success-message .motto {
    font-style: italic;
    text-align: center;
    color: #ff9933;
    font-weight: bold;
    margin-top: 1.5rem;
    font-size: 1.1rem;
  }

  .home-button {
    display: block;
    width: 100%;
    padding: 1rem;
    margin-top: 2rem;
    font-size: 1.2rem;
    font-weight: bold;
    text-align: center;
    color: #1a202c;
    background: linear-gradient(135deg, #ff9933, #ff7708);
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 6px rgba(255, 119, 8, 0.2);
  }

  .home-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(255, 119, 8, 0.3);
  }

  .home-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(255, 119, 8, 0.2);
  }

  @media (max-width: 640px) {
    .popup {
      padding: 2rem 1rem;
    }

    h2 {
      font-size: 1.5rem;
    }

    input {
      font-size: 1rem;
    }

    .success-message h2 {
      font-size: 1.5rem;
    }
  }

  :global(.dark) .popup {
    background: #2d3748;
  }

  :global(.dark) .close-button {
    color: #e2e8f0;
  }

  :global(.dark) h2 {
    color: #f7fafc;
  }

  :global(.dark) p {
    color: #e2e8f0;
  }

  :global(.dark) input {
    border-color: #4a5568;
    background-color: #2d3748;
    color: #f7fafc;
  }

  :global(.dark) input:focus {
    border-color: #ff9933;
  }

  :global(.dark) .success-message h2 {
    color: #ff9933;
  }

  :global(.dark) .success-message h3 {
    color: #f7fafc;
  }

  .step-indicator {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
  }

  .step-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: var(--color-border, #e2e8f0);
    margin: 0 5px;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    padding: 0;
  }

  .step-dot.active {
    background-color: var(--color-primary, #ff7708);
    transform: scale(1.2);
  }

  .step-dot:hover {
    background-color: var(--color-primary-light, #ff9933);
  }

  .feature-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .feature {
    text-align: center;
    padding: 1.5rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    transition: all 0.3s ease;
  }

  .feature:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }

  .feature .icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }

  .feature h3 {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
    color: var(--color-primary, #ff7708);
  }

  .benefits-list {
    list-style-type: none;
    padding: 0;
    margin-bottom: 2rem;
  }

  .benefits-list li {
    padding: 0.75rem 0;
    position: relative;
    padding-left: 2.5rem;
    font-size: 1.1rem;
    color: var(--color-text-primary, #2d3748);
  }

  .benefits-list li::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: var(--color-primary, #ff7708);
    font-weight: bold;
    font-size: 1.2rem;
  }

  .button-group {
    display: flex;
    justify-content: flex-end;
    margin-top: 1rem;
  }

  .button-group.with-back {
    justify-content: space-between;
  }

  .next-button, .prev-button {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: opacity 0.3s ease;
  }

  .next-button {
    background: linear-gradient(135deg, #ff9933, #ff7708);
    color: white;
  }

  .prev-button {
    background: none !important;
    color: #000000 !important; /* Dark text for light mode */
    padding: 0.75rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
  }

  .prev-button:hover {
    background-color: rgba(0, 0, 0, 0.1) !important; /* Slight background on hover */
  }

  :global(.dark) .prev-button {
    color: #ffffff !important; /* White text for dark mode */
  }

  :global(.dark) .prev-button:hover {
    background-color: rgba(255, 255, 255, 0.1) !important; /* Slight background on hover in dark mode */
  }

  .arrow {
    display: inline-block;
    margin: 0 0.5rem;
  }

  /* Ensure text is vertically centered */
  .prev-button span, .next-button span {
    display: flex;
    align-items: center;
    height: 100%;
  }

  @media (max-width: 480px) {
    .button-group {
      flex-direction: column;
      align-items: stretch;
    }

    .prev-button, .next-button {
      max-width: 100%;
      margin-bottom: 1rem;
    }
  }

  .disclaimer {
    font-size: 0.75rem;
    color: #718096;
    margin-top: 1rem;
    text-align: center;
  }

  :global(.dark) .feature {
    background-color: rgba(255, 255, 255, 0.05);
  }

  .button-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2rem;
    gap: 1rem;
  }

  .prev-button, .next-button {
    width: 100%;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow for better readability */
    font-weight: 600; /* Slightly bolder text for better visibility */
  }

  :global(.dark) .prev-button, :global(.dark) .next-button {
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.1); /* Subtle text shadow for dark mode */
  }

  .prev-button {
    background-color: transparent;
    color: #ffffff;
    border: 2px solid #ffffff;
    flex: 1;
  }

  .next-button {
    background-color: #ff7708;
    color: white;
    border: none;
    flex: 2;
  }

  .arrow {
    display: inline-block;
    margin: 0 0.5rem;
  }

  .next-button {
    background-color: #ff7708;
    color: white;
    border: none;
    transition: box-shadow 0.3s ease;
  }

  .next-button:hover {
    box-shadow: 0 0 15px #ff7708, 0 0 30px #ff7708;
  }

  .arrow {
    display: inline-block;
    margin: 0 0.5rem;
  }
</style>