<script>
  import { fade, fly } from 'svelte/transition';
  import FAQ from '$lib/components/FAQ.svelte';
  import Countdown from '$lib/components/Countdown.svelte';
  import AIThreatMeter from '$lib/components/AIThreatMeter.svelte';
  import BookSample from '$lib/components/BookSample.svelte';
  import CommunityIntakePopupForm from '$lib/components/CommunityIntakePopupForm.svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import SkoolGroup from '$lib/components/SkoolGroup.svelte';

  const targetDate = new Date("2027-11-20T23:59:59").getTime();

  import { onMount } from 'svelte';

  let showContent = false;

  onMount(() => {
    showContent = true;
  });
</script>

<Spacer height="50px" />

<div class="about-container bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition-colors duration-300">
  <header class="mb-8">
    <h1 class="title text-4xl md:text-5xl font-bold mb-4" in:fly="{{ y: -20, duration: 500 }}">About Surviving the Singularity</h1>
    <p class="subtitle text-xl md:text-2xl text-gray-600 dark:text-gray-400" in:fly="{{ y: 20, duration: 500, delay: 200 }}">Navigate the AI Revolution Together</p>
  </header>

  <section class="book-info mb-12" in:fade="{{ duration: 500, delay: 800 }}">
    <h2 class="text-3xl font-bold mb-6">More Than Just a Book</h2>
    
    <div class="grid md:grid-cols-2 gap-8 items-start">
      <div>
        <p class="mb-4 text-lg">"Surviving the Singularity" is a revolutionary multi-format experience designed to guide you through the AI revolution:</p>
        <ul class="list-disc list-inside space-y-2 mb-6">
          <li><strong>Interactive Workbook:</strong> Engage with thought-provoking exercises and scenarios to deepen your understanding of AI's impact.</li>
          <li><strong>Personal AI Journal:</strong> Document your journey and insights as you navigate the rapidly evolving AI landscape.</li>
          <li><strong>Exclusive Digital Content:</strong> Access hidden rabbit holes of knowledge via QR codes, unlocking additional resources and cutting-edge information.</li>
          <li><strong>Self-Guided Research Tool:</strong> Embark on your own AI exploration with curated starting points and guided inquiry methods.</li>
          <li><strong>Future-Proofing Strategies:</strong> Develop practical skills and mindsets to thrive in an AI-driven world.</li>
        </ul>
        <BookSample />
    <div class="mt-8 bg-gray-100 dark:bg-gray-800 p-6 rounded-lg">
      <h3 class="text-2xl font-bold mb-4">Experience the Future of Learning</h3>
      <p class="mb-4">Our innovative QR code system allows you to:</p>
      <ul class="list-disc list-inside space-y-2">
        <li>Access exclusive online content updated in real-time</li>
        <li>Dive deep into AI topics with curated resources</li>
        <li>Participate in community discussions and expert Q&As</li>
        <li>Track your progress and unlock achievements</li>
      </ul>
    </div>

    <div class="mt-8 bg-gray-100 dark:bg-gray-800 p-6 rounded-lg">
      <h3 class="text-2xl font-bold mb-4">What Early Adopters Are Saying</h3>
      <div class="space-y-4">
        <blockquote class="italic">
          "This isn't just a book, it's a personal AI revolution in your hands. The interactive elements and QR codes make learning about AI an exciting journey of discovery."
          <footer class="text-right">- Emma Rodriguez, Tech Entrepreneur</footer>
        </blockquote>
        <blockquote class="italic">
          "The workbook and journal aspects helped me apply AI concepts to my own life and career in ways I never imagined. A truly transformative experience!"
          <footer class="text-right">- Dr. James Lee, Futurist</footer>
        </blockquote>
      </div>
    </div>
    
  </section>

  <!-- <SkoolGroup /> -->
  
  <FAQ />

  <section class="intro mb-8" in:fade="{{ duration: 500, delay: 400 }}">
    <p class="text-lg">Surviving the Singularity is a vibrant community of like-minded individuals navigating the AI revolution together. We're here to help each other stay informed, get ahead, and understand the transformative impact of AI on our world.</p>
  </section>

  <section class="community-info mb-8" in:fade="{{ duration: 500, delay: 600 }}">
    <h2 class="text-3xl font-bold mb-4">Join Our Supportive AI Community</h2>
    <p class="mb-4">Our community is a space where members:</p>
    <ul class="list-disc list-inside space-y-2">
      <li><strong>Share Insights:</strong> Post about the latest AI developments and their implications.</li>
      <li><strong>Collaborate:</strong> Help each other understand and contextualize new technologies.</li>
      <li><strong>Stay Ahead:</strong> Access curated content and discussions to remain at the forefront of AI advancements.</li>
      <li><strong>Support Growth:</strong> Encourage and assist one another in personal and professional development.</li>
      <li><strong>Navigate Change:</strong> Work together to adapt to the rapidly transforming AI landscape.</li>
    </ul>
    <CommunityIntakePopupForm />
  </section>

  <section class="newsletter mb-8" in:fade="{{ duration: 500, delay: 1000 }}">
    <h2 class="text-3xl font-bold mb-4">Stay Informed</h2>
    <p class="mb-4">Join our newsletter to receive regular updates on AI advancements and community insights.</p>
    <NewsletterSignup />
  </section>

  <p class="text-lg text-center">What's your risk tolerance?</p>
  <AIThreatMeter />


  <section class="countdown mb-8" in:fade="{{ duration: 500, delay: 1200 }}">
    <div class="bg-gray-100 dark:bg-gray-800 p-6 rounded-lg">
      <Countdown targetDate={targetDate} />
      <p class="mt-4 text-lg">The technological singularity is approaching rapidly. This countdown represents our estimated timeline to the mass production of human-level AI robots, but the exact moment is unpredictable. Will you be prepared?</p>
    </div>
  </section>

</div>

<style>
  .about-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }

  @media (max-width: 768px) {
    .about-container {
      padding: 1rem;
    }
  }
</style>