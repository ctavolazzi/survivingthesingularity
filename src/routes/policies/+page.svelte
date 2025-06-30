<script>
  import { onMount } from 'svelte';

  let navbarHeight = 0;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
  });
</script>

<div class="outer-container">
  <div class="content-container">
    <h1 class="text-3xl font-bold text-center">Our Policies</h1>

    <section id="privacy-policy" class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">Privacy Policy</h2>
      <p class="mb-2"><strong>Last Updated: December 19, 2024</strong></p>
      <p class="mb-2">Your privacy is important to us. This privacy statement explains our approach to personal data and privacy.</p>
      <p class="mb-2">We do not actively collect personal information from our users. Our website is designed to be informational and educational, allowing you to browse and read content without providing any personal data.</p>

              <p class="mb-2">Should you choose to interact with any future features that might collect data, we will never sell or share your data without your permission. We will never personally identify you without your consent, and we will only use your data in adherence with applicable laws.</p>
      <p class="mb-2">We may share aggregated, non-personally identifiable information publicly and with our partners. For example, we may share information publicly to show trends about the general use of our services.</p>

      <h3 class="text-xl font-semibold mt-4 mb-2">Data Retention</h3>
      <p class="mb-2">We retain minimal personal information and only for as long as necessary to fulfill legitimate purposes. Any data collected is handled in accordance with applicable privacy laws and regulations.</p>

      <h3 class="text-xl font-semibold mt-4 mb-2">Your Rights</h3>
      <p class="mb-2">Depending on your location, you may have rights regarding your personal data, including:</p>
      <ul class="list-disc list-inside mb-2">
        <li>The right to access and receive a copy of your personal data</li>
        <li>The right to rectify or update your personal data</li>
        <li>The right to erase your personal data</li>
        <li>The right to restrict processing of your personal data</li>
        <li>The right to object to processing of your personal data</li>
        <li>The right to data portability</li>
        <li>The right to withdraw consent</li>
      </ul>
      <p class="mb-2">To exercise these rights, please contact us directly.</p>

      <h3 class="text-xl font-semibold mt-4 mb-2">Data Security</h3>
      <p class="mb-2">We implement appropriate technical and organizational measures to protect your personal data against unauthorized or unlawful processing, accidental loss, destruction, or damage.</p>

      <h3 class="text-xl font-semibold mt-4 mb-2">Changes to This Policy</h3>
      <p class="mb-2">We may update this Privacy Policy from time to time to reflect changes in our practices or for other operational, legal, or regulatory reasons. When we make material changes to this Privacy Policy, we will notify you by posting the updated policy on this page with a "Last Updated" date.</p>

      <h3 class="text-xl font-semibold mt-4 mb-2">Questions</h3>
      <p class="mb-2">If you have any questions about this Privacy Policy or our data practices, you may reach out to us via email.</p>
    </section>

    <section id="cookie-policy" class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">Cookie Policy</h2>
      <p class="mb-2"><strong>Last Updated: December 19, 2024</strong></p>
      <p class="mb-2">As of December 19, 2024, we do not collect or use cookies on this website. Our site is designed to be simple and straightforward, without the need for tracking technologies that collect personal information. We prioritize your privacy and aim to provide valuable content without unnecessary data collection.</p>
      <p class="mb-2">We have no plans to collect cookies in the near future. If this policy changes, we will update this page and provide clear notification to all site visitors before implementing any cookie-based technologies.</p>
      <p class="mb-2">We use minimal third-party services and prioritize privacy-focused solutions. Any third-party services we use are carefully selected to align with our privacy-first approach.</p>

      <h3 class="text-xl font-semibold mt-4 mb-2">Third-Party Services</h3>
      <ul class="list-disc list-inside mb-2">
        <li><strong>Supabase</strong> - Used for database services and user authentication. Data stored in Supabase is subject to their <a href="https://supabase.com/privacy" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">privacy policy</a>.</li>
      </ul>

      <p class="mb-2">Any third-party services we use may collect data according to their own privacy policies, which may change over time. We recommend reviewing the privacy policies of these services for the most up-to-date information about how they handle your data.</p>
      <p class="mb-2">This policy is designed to be transparent and straightforward. If you have specific concerns about legal compliance, we recommend consulting with a legal professional familiar with privacy laws in your jurisdiction.</p>
    </section>

    <section id="usage-guidelines" class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">Usage Guidelines</h2>
      <p class="mb-2">Our usage guidelines are designed to ensure a positive experience for all users. By using our website, you agree to adhere to these guidelines:</p>
      <ul class="list-disc list-inside mb-2">
        <li>Comply with all applicable laws and regulations.</li>
        <li>Respect the rights and dignity of others.</li>
        <li>Use the site responsibly and for its intended educational and informational purpose.</li>
        <li>Protect your personal information and respect the privacy of others.</li>
        <li>Adhere to intellectual property laws and respect copyrights.</li>
        <li>Use the content for personal, non-commercial purposes unless otherwise specified.</li>
      </ul>
      <p class="mb-2">We reserve the right to take appropriate action for any behavior that violates these guidelines.</p>
      <p class="mb-2">These guidelines may be updated periodically. Users are encouraged to review them regularly to ensure compliance.</p>
    </section>

    <section id="disclaimers" class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">Disclaimers</h2>
      <p class="mb-2"><strong>General Disclaimer:</strong> The content on this website represents educated guesses, personal opinions, and commentary about artificial intelligence, technology, and potential future developments. Nothing presented on this site that is unconfirmed by official sources should be considered certain or guaranteed.</p>

      <p class="mb-2"><strong>Technological Progression is Not Guaranteed:</strong> While we discuss potential future scenarios and developments, no one can predict the future with certainty. All discussions about future events should be understood as speculation and possibility, not certainty.</p>

      <p class="mb-2"><strong>Not Professional Advice:</strong> The information provided on this website is for general informational and educational purposes only. It is not intended to be and should not be taken as financial, legal, investment, medical, or other professional advice.</p>

      <p class="mb-2"><strong>Do Your Own Research:</strong> We strongly encourage visitors to conduct their own research, exercise critical thinking, and consult qualified professionals before making any decisions based on information found on this site.</p>

      <p class="mb-2"><strong>No Liability:</strong> By using this site, you are agreeing that you understand that anything unconfirmed by official sources is speculation and should be treated as such. We will not be held liable for any losses, damages, or other negative outcomes that may result from using or relying upon the information presented on this website.</p>

      <p class="mb-2"><strong>Accuracy of Information:</strong> While we strive to provide accurate and up-to-date information, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability of the information contained on this website.</p>

      <p class="mb-2"><strong>External Links:</strong> This website may contain links to external websites that are not provided or maintained by us. We do not guarantee the accuracy, relevance, timeliness, or completeness of any information on these external websites.</p>

      <p class="mb-2">By using this website, you acknowledge and agree that you understand these disclaimers and will not hold us responsible for any decisions you make based on any information provided on this website.</p>
    </section>

    <section id="legal-notice" class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">Legal Notice</h2>
      <p class="mb-2"><strong>Last Updated: December 19, 2024</strong></p>
      <p class="mb-2">While we've made our best effort to comply with relevant privacy laws and regulations, the policies on this page are not legal advice. These policies are provided for transparency and to inform you about our practices.</p>
      <p class="mb-2">This website is owned and operated by Surviving the Singularity. If you have any questions about these policies or our practices, you may reach out to us via email.</p>
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