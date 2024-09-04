<script>
  import { goto } from '$app/navigation';
  import SkoolGroup from '$lib/components/SkoolGroup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import StSWelcome from '$lib/images/sts-welcome.png';
  import ContactForm from '$lib/components/ContactForm.svelte';

  function goHome() {
    goto('/');
  }
</script>

<div class="main-content">
  <div class="content-container">
    <h1 class="quote">Congratulations!</h1>
    <p class="attribution">Your purchase was successful.</p>
    
    <img src={StSWelcome} alt="Welcome to Surviving the Singularity" class="congrats-image" />
    
    <p class="status">Thank you for your preorder of your very own copy of Surviving the Singularity!</p>
    
    <div class="stylish-divider"></div>
    
    <div class="skool-signup">
      <h2 class="quote text-2xl font-bold">Next Steps: Email Confirmation & Join Our Community</h2>
      <div class="skool-text-container">
        <p class="attribution">Now that you've got your book on the way, you're ready to dive deep into the community.</p>
        <p class="attribution highlight">If you entered your email, you should receive an email from us shortly with a link to confirm your email address.</p>
        <p class="attribution">Just wait for the email to hit your inbox, and you'll be all set.</p>
        <h3 class="text-4xl font-bold">Wait, don't go yet!</h3>
        <p class="attribution highlight-bright">By purchasing the book, you're now eligible to join the Surviving the Singularity community for FREE</p>
        <p class="attribution highlight">You should receive an email shortly with a link to join the community with exclusive LIFETIME FREE ACCESS</p>
        <p class="attribution">For any questions, please reach out to us through the contact form below.</p>
      </div>
      <ContactForm />
      <div class="skool-group-container">
        <SkoolGroup />
      </div>
    </div>
    
    <div class="stylish-divider"></div>
    
    <div class="button-container">
      <button class="big-button" on:click={goHome}>Return to Home</button>
    </div>
  </div>
</div>

<Spacer height="1rem"/>

<style>
  .main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: Arial, sans-serif;
    padding: 20px;
    text-align: center;
  }

  .content-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    width: 100%;
  }

  h1.quote {
    font-style: italic;
    font-size: 2.5rem;
    color: var(--color-text-primary);
    line-height: 1.4;
    font-weight: 500;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 10px;
  }

  .attribution {
    font-weight: bold;
    font-size: 1.2rem;
    color: var(--color-text-secondary);
  }

  .congrats-image {
    max-width: 100%;
    height: auto;
    margin: 20px 0;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #e5e7eb;
  }

  .status {
    font-weight: bold;
    margin-bottom: 20px;
    font-size: 1.1rem;
  }

  .skool-signup {
    background-color: var(--color-bg-secondary);
    border-radius: 10px;
    padding: 30px 15px;  /* Adjusted padding */
    margin: 30px 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .skool-text-container {
    margin: 20px 0;
    max-width: 100%;  /* Ensure text doesn't overflow */
    overflow-wrap: break-word;  /* Allow long words to break */
  }

  .skool-signup h2.quote {
    margin-bottom: 20px;
  }

  .skool-signup .attribution {
    margin-bottom: 15px;
    line-height: 1.5;
  }

  .skool-group-container {
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 2rem 0;
    margin-top: 30px;
  }

  .button-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 1rem 0;
  }

  .big-button {
    flex: 1;
    font-weight: 600;
    font-size: 1.1rem;
    background-color: #ffffff;
    border: 1px solid #2c3e50;
    border-radius: 6px;
    color: #2c3e50;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .big-button:hover {
    background-color: #f8f9fa;
    border-color: #34495e;
    color: #34495e;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transform: translateY(-2px);
  }

  .stylish-divider {
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
    margin: 2rem auto;
    max-width: 80%;
  }

  /* Dark mode styles */
  :global(.dark) h1.quote,
  :global(.dark) h2.quote {
    color: #e5e7eb;
  }

  :global(.dark) .attribution {
    color: #9ca3af;
  }

  :global(.dark) .big-button {
    background-color: #2c3e50;
    color: #ffffff;
    border-color: #34495e;
  }

  :global(.dark) .big-button:hover {
    background-color: #34495e;
    border-color: #4a6785;
    color: #ffffff;
  }

  :global(.dark) .stylish-divider {
    background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
  }

  :global(.dark) .skool-signup {
    background-color: #2c3e50;
  }

  /* Responsive styles */
  @media (max-width: 768px) {
    .button-container {
      flex-direction: column;
    }

    .big-button {
      width: 100%;
    }

    .content-container {
      padding: 0 0.5rem;
    }

    .skool-signup {
      padding: 20px 10px;
    }

    .attribution, .attribution.highlight, .attribution.highlight-bright {
      font-size: 1rem;
      padding: 0.5rem 0.25rem;
    }
  }

  .attribution.highlight {
    color: #ff6b6b;
    font-weight: bold;
    background-color: rgba(255, 107, 107, 0.1);
    padding: 0.5rem;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* For dark mode */
  :global(.dark) .attribution.highlight {
    color: #ffa07a;
    background-color: rgba(255, 160, 122, 0.2);
    box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
  }
  
  .attribution.highlight-bright {
    color: #ffffff;
    font-weight: bold;
    background-color: #ff4757;
    padding: 0.75rem;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(255, 71, 87, 0.6);
    border: 2px solid #ff6b6b;
    margin: 1rem 0;
    transform: translateY(-2px);
    transition: all 0.3s ease;
  }

  .attribution.highlight-bright:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 16px rgba(255, 71, 87, 0.7);
  }

  /* For dark mode */
  :global(.dark) .attribution.highlight-bright {
    color: #ff4757;
    background-color: #ffffff;
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
    border: 2px solid #ff4757;
  }

  :global(.dark) .attribution.highlight-bright:hover {
    box-shadow: 0 6px 16px rgba(255, 255, 255, 0.4);
  }
</style>