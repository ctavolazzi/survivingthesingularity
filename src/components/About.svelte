<script>
    let email = '';
    let subscribed = false;
  
    function handleSubscribe() {
      // Here, you would typically send the email to your newsletter service provider
      // For this example, we'll just display a success message
      subscribed = true;
      email = '';
    }
  </script>
  
  <div class="container">
    <div class="content">
      <h1 class="title">What is this all about?</h1>
      <p class="description">
        Once considered a theoretical concept confined to the realms of science fiction and fringe discussions, the technological singularity has now become an increasingly plausible reality. The singularity—a future period during which the pace of technological change will be so rapid, its impact so deep, that human life will be irreversibly transformed—is no longer a mere hypothetical scenario.
      </p>
      <p class="description">
        With advancements in fields like artificial intelligence, biotechnology, and quantum computing, we are rapidly approaching a pivotal moment in human history. Unless we collectively take drastic measures to avert potential catastrophes, the singularity may be inevitable. This project aims to explore and discuss the implications of such a future, providing insights, discussions, and resources to help us navigate this impending era.
      </p>
      <p class="description">
        Whether it's through understanding artificial intelligence, biotechnology, or other facets of technological advancement, "Surviving the Singularity" seeks to equip individuals with the knowledge and tools necessary to thrive in an increasingly complex world. By fostering a deeper understanding of the challenges and opportunities ahead, we can work together to shape a future that maximizes the benefits of technological progress while mitigating potential risks.
      </p>
  
      <div class="additional-content">
        <div class="section">
          <h2 class="section-title">Our Mission</h2>
          <p class="section-description">
            Our mission is to foster a deeper understanding of the technological singularity and its potential impact on humanity. We strive to create a community of forward-thinkers, researchers, and innovators who can work together to navigate the challenges and opportunities that lie ahead.
          </p>
        </div>
  
        <div class="section">
          <h2 class="section-title">Stay Updated</h2>
          <p class="section-description">
            Subscribe to our newsletter to receive regular updates, insights, and exclusive content related to the technological singularity.
          </p>
          <div class="newsletter-form">
            <input
              type="email"
              placeholder="Enter your email"
              bind:value={email}
              class="newsletter-input"
            />
            <button
              on:click={handleSubscribe}
              class="newsletter-button"
              disabled={subscribed}>
              {subscribed ? 'Subscribed!' : 'Subscribe'}
            </button>
          </div>
          {#if subscribed}
            <p class="success-message">Thank you for subscribing!</p>
          {/if}
        </div>
      </div>
    </div>
  </div>
  
  <style>
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
      color: #333;
    }
  
    .content {
      text-align: left;
    }
  
    .title {
      font-size: 3rem;
      margin-bottom: 2rem;
    }
  
    .description {
      font-size: 1.2rem;
      line-height: 1.6;
      margin-bottom: 2rem;
    }
  
    .additional-content {
      margin-top: 3rem;
      text-align: left;
    }
  
    .section {
      margin-bottom: 2rem;
    }
  
    .section-title {
      font-size: 2rem;
      margin-bottom: 1rem;
    }
  
    .section-description {
      font-size: 1.1rem;
      line-height: 1.6;
      margin-bottom: 1rem;
    }
  
    .newsletter-form {
      display: flex;
      justify-content: center;
      margin-bottom: 1rem;
    }
  
    .newsletter-input {
      padding: 0.5rem;
      border: 1px solid #333;
      border-radius: 4px;
      margin-right: 0.5rem;
    }
  
    .newsletter-button {
      padding: 0.5rem 1rem;
      background-color: #333;
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
  
    .newsletter-button:hover {
      background-color: #555;
    }
  
    .newsletter-button:disabled {
      background-color: #999;
      cursor: not-allowed;
    }
  
    .success-message {
      color: #333;
    }
  </style>