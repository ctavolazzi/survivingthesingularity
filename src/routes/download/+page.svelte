<script>
  import { onMount, onDestroy } from 'svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import StSFreeGuideImage from '$lib/images/StSFreeGuide.png';
  import { downloadStats } from '$lib/stores/downloadStats';
  import SKoolGroup from '$lib/components/SKoolGroup.svelte';
  import { fade, fly, scale, slide } from 'svelte/transition';
  import { tweened } from 'svelte/motion';
  import { cubicOut, elasticOut } from 'svelte/easing';
  import { spring } from 'svelte/motion';

  let isDownloading = false;
  let buttonText = "Get Your FREE Checklist (Limited Time Offer)";
  let remainingTime = 600; // 10 minutes in seconds
  let showTestimonials = false;
  let spotsRemaining = 100;
  let currentBenefitIndex = 0;
  let showPopup = false;
  let email = '';
  let showSocialProof = false;
  let currentUserCount = 0;
  let targetUserCount = 10000;
  let showFloatingCTA = false;

  const progress = tweened(100, {
    duration: 400,
    easing: cubicOut
  });

  const popupSpring = spring({ y: -100, opacity: 0 }, {
    stiffness: 0.1,
    damping: 0.25
  });

  const userCountTween = tweened(0, {
    duration: 3000,
    easing: cubicOut
  });

  const benefits = [
    "Stay ahead of AI advancements",
    "Future-proof your career",
    "Understand emerging technologies",
    "Network with industry experts",
    "Access exclusive resources"
  ];

  function onInterval(callback, milliseconds) {
    const interval = setInterval(callback, milliseconds);
    onDestroy(() => {
      clearInterval(interval);
    });
  }

  function updateSpotsRemaining() {
    spotsRemaining = Math.max(0, spotsRemaining - Math.floor(Math.random() * 3));
    progress.set(spotsRemaining);
  }

  function showExitIntentPopup(event) {
    if (event.clientY <= 0 && !showPopup) {
      showPopup = true;
      popupSpring.set({ y: 0, opacity: 1 });
    }
  }

  function closePopup() {
    showPopup = false;
    popupSpring.set({ y: -100, opacity: 0 });
  }

  function handleEmailSubmit() {
    // Implement email submission logic here
    console.log('Email submitted:', email);
    closePopup();
  }

  function handleScroll() {
    if (window.scrollY > 300) {
      showFloatingCTA = true;
    } else {
      showFloatingCTA = false;
    }
  }

  onMount(() => {
    const interval = setInterval(() => {
      downloadStats.incrementDownloads();
      if (remainingTime > 0) {
        remainingTime--;
      } else {
        clearInterval(interval);
      }
    }, 1000);

    setTimeout(() => {
      showTestimonials = true;
    }, 3000);

    onInterval(() => {
      currentBenefitIndex = (currentBenefitIndex + 1) % benefits.length;
    }, 3000);

    const spotInterval = setInterval(updateSpotsRemaining, 10000);

    document.addEventListener('mouseleave', showExitIntentPopup);
    window.addEventListener('scroll', handleScroll);

    setTimeout(() => {
      showSocialProof = true;
      userCountTween.set(targetUserCount);
    }, 5000);

    return () => {
      clearInterval(interval);
      clearInterval(spotInterval);
      document.removeEventListener('mouseleave', showExitIntentPopup);
      window.removeEventListener('scroll', handleScroll);
    };
  });

  $: minutes = Math.floor(remainingTime / 60);
  $: seconds = remainingTime % 60;
  $: progressPercentage = $progress;
  $: urgencyMessage = spotsRemaining <= 10 ? "Only a few spots left!" : 
                      spotsRemaining <= 50 ? "Spots are filling up fast!" : 
                      "Join now while spots are available!";
  $: formattedUserCount = Math.floor($userCountTween).toLocaleString();

  async function downloadSamplePDF() {
    isDownloading = true;
    const pdfUrl = '/Singularity-checklist.pdf';
    const link = document.createElement('a');
    link.href = pdfUrl;
    link.download = 'Singularity-checklist.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate download time
    isDownloading = false;
  }

  function handleJoinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }

  function handleReadSample() {
    window.location.href = 'https://survivingthesingularity.com/sample';
  }
</script>

<svelte:window on:mouseleave={showExitIntentPopup} />

<div class="main-content">
  <div class="content-container">
    <div class="card bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Download Singularity Checklist</h1>
      <p class="intro text-xl text-gray-700 dark:text-gray-300 mb-6">Prepare for the future with our comprehensive guide.</p>
      <img src={StSFreeGuideImage} alt="Surviving the Singularity Free Guide" class="w-full mb-4 rounded-lg shadow-md">
      <p class="text-xl font-bold text-red-600 dark:text-red-400 mb-4">
        Limited Time Offer: {minutes}:{seconds < 10 ? '0' : ''}{seconds} remaining!
      </p>
      <button on:click={downloadSamplePDF} 
        class="big-button gradient-button text-white w-full" 
        class:downloading={isDownloading} 
        disabled={isDownloading}>
        {isDownloading ? 'Downloading...' : buttonText}
        <span class="button-icon">{isDownloading ? '⟳' : '↓'}</span>
      </button>
      {#if $downloadStats}
        <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">
          <span class="font-semibold">{$downloadStats.totalDownloads.toLocaleString()}</span> total downloads
          {#if $downloadStats.recentDownloads > 0}
            • <span class="text-green-600 dark:text-green-400 font-semibold">{$downloadStats.recentDownloads} new</span> in the last 5 seconds
          {/if}
        </p>
      {/if}
      
      <div class="description text-gray-700 dark:text-gray-300 mb-8">
        <br>
        <p class="mb-4">Our Singularity Checklist is a carefully curated PDF resource designed to help you:</p>
        <div class="bullet-points-container">
          <ul>
            <li>Understand key concepts related to technological singularity</li>
            <li>Identify potential challenges and opportunities in a rapidly changing world</li>
            <li>Develop strategies to adapt and thrive in the face of exponential technological growth</li>
          </ul>
        </div>
        <p>Download now and take the first step towards future-proofing your life and career.</p>
      </div>
      <div class="button-container">
        <button class="big-button" on:click={handleReadSample}>
          Read a Sample
        </button>
        <button class="big-button" on:click={handleJoinSkool}>
          Join the Skool Community
        </button>
      </div>
    </div>

    {#if showTestimonials}
      <div class="testimonials" transition:fade={{ duration: 500 }}>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">What Our Community Says</h2>
        <div class="testimonial-grid">
          <div class="testimonial">
            <p>"This checklist changed my perspective on AI. Invaluable resource!"</p>
            <span>- Sarah K., Tech Entrepreneur</span>
          </div>
          <div class="testimonial">
            <p>"I feel more prepared for the future after going through this guide."</p>
            <span>- Mark R., Data Scientist</span>
          </div>
          <div class="testimonial">
            <p>"The Skool community is a goldmine of insights and support."</p>
            <span>- Emily L., Futurist</span>
          </div>
        </div>
      </div>
    {/if}

    <div class="benefits-section mt-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Why Join Our Community?</h2>
      <div class="benefit-container h-12">
        {#key currentBenefitIndex}
          <p class="text-xl text-gray-700 dark:text-gray-300" in:fly="{{ y: 20, duration: 300 }}" out:fly="{{ y: -20, duration: 300 }}">
            {benefits[currentBenefitIndex]}
          </p>
        {/key}
      </div>
    </div>

    <div class="faq-section mt-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Frequently Asked Questions</h2>
      <div class="faq-grid">
        <div class="faq-item">
          <h3 class="font-bold">What is the Singularity Checklist?</h3>
          <p>Our Singularity Checklist is a comprehensive guide to help you prepare for the technological singularity and its potential impacts on society and your personal life.</p>
        </div>
        <div class="faq-item">
          <h3 class="font-bold">How often is the content updated?</h3>
          <p>We regularly update our resources to keep up with the latest developments in AI and emerging technologies. Join our community for real-time updates and discussions.</p>
        </div>
        <div class="faq-item">
          <h3 class="font-bold">Is the Skool community right for me?</h3>
          <p>If you're interested in AI, future technologies, and personal growth, our community is perfect for you. We welcome members from all backgrounds and experience levels.</p>
        </div>
      </div>
    </div>

    <div class="guarantee-section mt-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Our Guarantee</h2>
      <p class="text-lg text-gray-700 dark:text-gray-300 mb-4">
        We're confident you'll find immense value in our Singularity Checklist and community. If you're not satisfied within 30 days, we'll refund your Skool membership - no questions asked.
      </p>
    </div>

    <div class="skool-section mt-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Join Our Thriving Community</h2>
      <p class="text-lg text-gray-700 dark:text-gray-300 mb-4">
        Connect with like-minded individuals, share insights, and stay ahead of the curve in our Skool community.
      </p>
      <SKoolGroup />
      <button class="big-button mt-4 w-full" on:click={handleJoinSkool}>
        Join Skool Now - Limited Spots Available!
      </button>
    </div>

    <div class="urgency-section mt-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Limited Availability</h2>
      <p class="text-lg text-gray-700 dark:text-gray-300 mb-4">
        {urgencyMessage}
      </p>
      <div class="progress-bar">
        <div class="progress-fill" style="width: {progressPercentage}%"></div>
      </div>
      <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">
        {spotsRemaining} spots remaining
      </p>
    </div>

    <div class="social-proof-section mt-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Trusted By Industry Leaders</h2>
      <div class="logo-grid">
        <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" alt="Google" class="company-logo">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/1024px-Microsoft_logo.svg.png" alt="Microsoft" class="company-logo">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/1200px-Apple_logo_black.svg.png" alt="Apple" class="company-logo">      
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1024px-Amazon_logo.svg.png" alt="Amazon" class="company-logo">        
      </div>
    </div>

    <div class="video-section mt-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">See What You'll Get</h2>
      <div class="video-container">
        <iframe
          width="560"
          height="315"
          src="https://www.youtube.com/embed/NKENM_J-rEg?si=nj2_umZmi0o-rd0x"
          title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerpolicy="strict-origin-when-cross-origin"
          allowfullscreen
        ></iframe>
      </div>
    </div>

    <div class="comparison-section mt-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Why Choose Our Community?</h2>
      <div class="comparison-table">
        <div class="comparison-header">
          <div class="comparison-cell"></div>
          <div class="comparison-cell">Our Community</div>
          <div class="comparison-cell">Others</div>
        </div>
        <div class="comparison-row">
          <div class="comparison-cell">Expert-led discussions</div>
          <div class="comparison-cell">✅</div>
          <div class="comparison-cell">❌</div>
        </div>
        <div class="comparison-row">
          <div class="comparison-cell">Exclusive resources</div>
          <div class="comparison-cell">✅</div>
          <div class="comparison-cell">❌</div>
        </div>
        <div class="comparison-row">
          <div class="comparison-cell">Regular updates</div>
          <div class="comparison-cell">✅</div>
          <div class="comparison-cell">❌</div>
        </div>
        <div class="comparison-row">
          <div class="comparison-cell">Networking opportunities</div>
          <div class="comparison-cell">✅</div>
          <div class="comparison-cell">❌</div>
        </div>
      </div>
    </div>

    <div class="final-cta-section mt-8">
      <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Ready to Secure Your Future?</h2>
      <p class="text-xl text-gray-700 dark:text-gray-300 mb-6">
        Join our community today and get instant access to the Singularity Checklist, expert insights, and a network of forward-thinking individuals.
      </p>
      <div class="cta-buttons">
        <button on:click={downloadSamplePDF} 
          class="big-button gradient-button text-white">
          Download Checklist
        </button>
        <button on:click={handleJoinSkool} 
          class="big-button bg-blue-500 hover:bg-blue-600 dark:bg-blue-700 dark:hover:bg-blue-800 text-white">
          Join Skool Community
        </button>
      </div>
    </div>
  </div>
</div>

<style>
  .main-content {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding-top: 1rem;
    padding: 2rem;
  }

  .content-container {
    max-width: 800px;
    text-align: center;
    margin-top: 0.5rem;
  }

  h1 {
    font-size: 2rem;
    margin-top: 0;
    margin-bottom: 1rem;
  }

  .intro {
    font-size: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .description p,
  li {
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  .bullet-points-container {
    width: 80%;
    margin: 0 auto;
  }

  ul {
    list-style-type: none;
    padding-left: 0;
    margin-bottom: 1rem;
    text-align: left;
  }

  li {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.5rem;
    font-weight: bold;
    text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.2);
  }

  li::before {
    content: "•";
    margin-right: 0.5em;
    flex-shrink: 0;
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
    border-radius: 6px;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .gradient-button {
    background: linear-gradient(135deg, #ff8a00, #ff5100);
    border: none;
    color: white;
  }

  .gradient-button:hover {
    background: linear-gradient(135deg, #ff9500, #ff6200);
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    transform: translateY(-2px);
  }

  :global(.dark) .gradient-button {
    background: linear-gradient(135deg, #ff7600, #ff4500);
  }

  :global(.dark) .gradient-button:hover {
    background: linear-gradient(135deg, #ff8500, #ff5500);
  }

  .button-icon {
    margin-left: 8px;
    font-size: 1.2rem;
  }

  .downloading .button-icon {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    100% { transform: rotate(360deg); }
  }

  .big-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .testimonials {
    margin-top: 2rem;
  }

  .testimonial-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }

  .testimonial {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  :global(.dark) .testimonial {
    background-color: #2c3e50;
  }

  .testimonial p {
    font-style: italic;
    margin-bottom: 0.5rem;
  }

  .testimonial span {
    font-weight: bold;
    font-size: 0.9rem;
  }

  .benefits-section, .faq-section, .guarantee-section, .skool-section, .urgency-section, .social-proof-section, .final-cta-section {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-top: 2rem;
  }

  :global(.dark) .benefits-section,
  :global(.dark) .faq-section,
  :global(.dark) .guarantee-section,
  :global(.dark) .skool-section,
  :global(.dark) .urgency-section,
  :global(.dark) .social-proof-section,
  :global(.dark) .final-cta-section {
    background-color: #2c3e50;
  }

  .benefit-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .faq-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }

  .faq-item {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  :global(.dark) .faq-item {
    background-color: #34495e;
  }

  .faq-item h3 {
    margin-bottom: 0.5rem;
  }

  .progress-bar {
    width: 100%;
    height: 20px;
    background-color: #e2e8f0;
    border-radius: 10px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background-color: #48bb78;
    transition: width 0.4s ease-out;
  }

  .logo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 1rem;
    align-items: center;
    justify-items: center;
  }

  .company-logo {
    max-width: 100px;
    max-height: 50px;
    object-fit: contain;
  }

  .cta-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
  }

  @media (max-width: 640px) {
    .cta-buttons {
      flex-direction: column;
    }
  }

  .video-container {
    position: relative;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
    height: 0;
    overflow: hidden;
  }

  .video-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .comparison-table {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 1px;
    background-color: #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
  }

  .comparison-header, .comparison-row {
    display: contents;
  }

  .comparison-cell {
    background-color: #ffffff;
    padding: 1rem;
    text-align: center;
  }

  :global(.dark) .comparison-cell {
    background-color: #2c3e50;
  }

  .comparison-header .comparison-cell {
    font-weight: bold;
    background-color: #f1f5f9;
  }

  :global(.dark) .comparison-header .comparison-cell {
    background-color: #1e293b;
  }
</style>