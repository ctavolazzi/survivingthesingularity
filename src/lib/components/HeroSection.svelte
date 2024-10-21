<script>
  import { goto } from '$app/navigation';
  import { darkMode } from '$lib/stores/darkMode';

  function handlePreorder() {
    goto('/preorder');
  }
</script>

<section class="hero-section" class:dark={$darkMode}>
  <h1>Surviving the Singularity</h1>
  <p class="tagline">Your guide to thriving in an AI-dominated world</p>

  <div class="content-box">
    <p class="welcome">Welcome to <strong>Surviving the Singularity</strong>, your comprehensive guide to navigating the rapidly evolving world of artificial intelligence and its impact on our future.</p>

    <p class="mission">This book will help you:</p>

    <ul class="benefits">
      <li>Stay informed about the latest AI developments</li>
      <li>Understand the risks and benefits of AI</li>
      <li>Adapt to an AI-dominated world</li>
      <li>Engage with ethical implications of rapid tech change</li>
      <li>Prepare your future for the Singularity</li>
    </ul>
  </div>

  <div class="cta-container">
    <button class="cta-button" on:click={handlePreorder}>Preorder the Full Book</button>
    <p class="cta-info">Available November 2024</p>
  </div>
</section>

<style>
  :root {
    --bg-primary: #f0f4f8;
    --bg-secondary: #ffffff;
    --text-primary: #2c3e50;
    --text-secondary: #34495e;
    --accent-primary: #3498db;
    --accent-secondary: #8e44ad;
    --shadow-color: rgba(0, 0, 0, 0.1);
    --checkmark-color: #27ae60;
  }

  .dark {
    --bg-primary: #1a202c;
    --bg-secondary: #2d3748;
    --text-primary: #e2e8f0;
    --text-secondary: #a0aec0;
    --accent-primary: #4299e1;
    --accent-secondary: #b794f4;
    --shadow-color: rgba(255, 255, 255, 0.1);
    --checkmark-color: #4299e1;
  }

  .hero-section {
    padding: 3rem 2rem;
    background-color: var(--bg-primary);
    border-radius: 16px;
    box-shadow: 0 8px 16px var(--shadow-color);
    max-width: 800px;
    margin: 2rem auto;
    transition: all 0.3s ease;
  }

  h1 {
    font-size: 3rem;
    color: var(--text-primary);
    margin-bottom: 1rem;
    text-align: center;
    font-weight: 700;
    letter-spacing: -0.5px;
  }

  .tagline {
    font-size: 1.4rem;
    color: var(--text-secondary);
    text-align: center;
    margin-bottom: 2.5rem;
    font-weight: 300;
  }

  .content-box {
    background-color: var(--bg-secondary);
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2.5rem;
    box-shadow: 0 4px 6px var(--shadow-color);
  }

  .welcome {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    line-height: 1.6;
    color: var(--text-primary);
  }

  .mission {
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }

  .benefits {
    list-style-type: none;
    padding-left: 0;
  }

  .benefits li {
    margin-bottom: 0.75rem;
    padding-left: 1.75rem;
    position: relative;
    color: var(--text-primary);
  }

  .benefits li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: var(--checkmark-color);
    font-weight: bold;
  }

  .cta-container {
    text-align: center;
  }

  .cta-button {
    display: inline-block;
    padding: 1rem 2rem;
    background-color: var(--accent-primary);
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(52, 152, 219, 0.3);
  }

  .cta-button:hover {
    background-color: var(--accent-primary);
    filter: brightness(90%);
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(52, 152, 219, 0.4);
  }

  .cta-info {
    margin-top: 1.25rem;
    font-size: 1.1rem;
    color: var(--accent-secondary);
    font-weight: bold;
  }

  @media (max-width: 768px) {
    .hero-section {
      padding: 2rem 1.5rem;
      margin: 1rem auto;
    }

    h1 {
      font-size: 2.5rem;
    }

    .tagline {
      font-size: 1.2rem;
    }

    .content-box {
      padding: 1.5rem;
    }
  }
</style>
