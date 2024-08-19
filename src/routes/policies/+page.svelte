<script>
  import Spacer from '$lib/components/Spacer.svelte';
  import { onMount } from 'svelte';

  let navbarHeight = 0;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
  });
</script>

<div class="outer-container" style="padding-top: {navbarHeight}px">
  <Spacer height="1rem">
    <span class="spacer-text">Our Policies</span>
  </Spacer>

  <div class="content-container">
    <h1 class="text-3xl font-bold mb-6 text-center">Our Policies</h1>

    <section id="privacy-policy" class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">Privacy Policy</h2>
      <p class="mb-2">Your privacy is important to us. This privacy statement explains the personal data we process, how we process it, and for what purposes.</p>
      <p class="mb-2">We collect information to provide better services to all our users. We collect information in the following ways: information you give us, information we get from your use of our services, and information from third parties.</p>
      <p class="mb-2">We use the information we collect from all our services to provide, maintain, protect, and improve them, to develop new ones, and to protect our users. We also use this information to offer you tailored content.</p>
      <p class="mb-2">We will never sell or share your data without your permission. By submitting information through our site, you grant us a license to use your information in our normal business actions, including market research and product development. We will never personally identify you without your consent, and we will only use your data in adherance with applicable laws.</p>
      <p class="mb-2">We may share aggregated, non-personally identifiable information publicly and with our partners. For example, we may share information publicly to show trends about the general use of our services.</p>
      <p class="mb-2">If you have any questions about this Privacy Policy, please contact us.</p>
    </section>

    <section id="terms-of-service" class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">Terms of Service</h2>
      <p class="mb-2">By accessing or using our services, you agree to be bound by these terms. If you disagree with any part of the terms, you may not access the service.</p>
      <p class="mb-2">Our services are diverse, so sometimes additional terms or product requirements may apply. Additional terms will be available with the relevant services, and those additional terms become part of your agreement with us if you use those services.</p>
      <p class="mb-2">We may modify these terms or any additional terms that apply to a service to reflect changes to the law or changes to our services. You should look at the terms regularly. Changes will not apply retroactively and will become effective no sooner than fourteen days after they are posted.</p>
      <p class="mb-2">We grant you a personal, non-transferable, non-exclusive, limited license to use our services. This license is for the sole purpose of enabling you to use and enjoy the benefit of the services as provided by us, in the manner permitted by these terms.</p>
      <p class="mb-2">You may use the content on our site for personal or commercial purposes, including creating derivative works, provided that you do not replicate the exact content of the book "Surviving the Singularity" or any of its derivative works produced by Christopher Tavolazzi or AIECO without permission. You are free to use the book content to make derivative works or for any lawful purpose, but you must obtain permission before using the exact contents of the book or its derivative works produced by Christopher Tavolazzi and/or AIECO.</p>
      <p class="mb-2">You may not copy, modify, distribute, sell, or lease any part of our services or included software, nor may you reverse engineer or attempt to extract the source code of that software, unless laws prohibit those restrictions or you have our written permission.</p>
      <p class="mb-2">Using our services does not give you ownership of any intellectual property rights in our services or the content you access. You may not use content from our services unless you obtain permission from its owner or are otherwise permitted by law.</p>
      <p class="mb-2">If you have any questions about these Terms of Service, please contact us.</p>
    </section>

    <section id="cookie-policy" class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">Cookie Policy</h2>
      <p class="mb-2">We use cookies to personalize content and ads, to provide social media features, and to analyze our traffic. We also share information about your use of our site with our social media, advertising, and analytics partners.</p>
      <p class="mb-2">Cookies are small text files that can be used by websites to make a user's experience more efficient. The law states that we can store cookies on your device if they are strictly necessary for the operation of this site. For all other types of cookies, we need your permission.</p>
      <p class="mb-2">This site uses different types of cookies. Some cookies are placed by third-party services that appear on our pages. You can at any time change or withdraw your consent from the Cookie Declaration on our website.</p>
      <p class="mb-2">We use cookies for the following purposes:</p>
      <ul class="list-disc list-inside mb-2">
        <li>Necessary: These cookies are essential for the website to function properly.</li>
        <li>Preferences: These cookies allow the website to remember choices you make to give you better functionality and personal features.</li>
        <li>Statistics: These cookies help us understand how visitors interact with our website by collecting and reporting information anonymously.</li>
        <li>Marketing: These cookies are used to track visitors across websites to display ads that are relevant and engaging for the individual user.</li>
      </ul>
      <p class="mb-2">If you have any questions about this Cookie Policy, please contact us.</p>
    </section>
  </div>
</div>

<style>
  .outer-container {
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
    min-height: 100vh;
  }

  .content-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .spacer-text {
    font-size: 1.5rem;
    font-weight: bold;
    background-color: var(--color-bg-secondary);
    color: var(--color-text-secondary);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  h1 {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 2rem;
    color: var(--color-text-accent);
    text-align: center;
  }

  h2 {
    font-size: 1.8rem;
    font-weight: semibold;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: var(--color-text-accent);
  }

  p {
    margin-bottom: 1rem;
    line-height: 1.6;
  }

  ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 1rem;
  }

  li {
    margin-bottom: 0.5rem;
  }

  section {
    margin-bottom: 3rem;
    padding: 1.5rem;
    background-color: var(--color-bg-secondary);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 2rem;
    }

    h2 {
      font-size: 1.5rem;
    }

    .content-container {
      padding: 1rem;
    }
  }
</style>