<script>
  import { Accordion, AccordionItem } from 'flowbite-svelte';
</script>

<div class="content-container">
    <div class="faq-header">Frequently Asked Questions</div>
    <Accordion class="content-box">
      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What is the Singularity?</span>
        <p class="text-[var(--color-text-secondary)]">
          The Technological Singularity refers to a hypothetical future point when artificial intelligence surpasses human intelligence, potentially leading to rapid and unpredictable technological growth. This concept is central to our book, as we explore its implications and how to prepare for this transformative event.
        </p>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">How can I best prepare for my future?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>Preparing for the AI revolution involves several strategies:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Stay informed about AI developments and their potential impacts</li>
            <li>Develop adaptable skills that complement AI capabilities</li>
            <li>Understand the ethical considerations surrounding AI</li>
            <li>Explore ways to leverage AI in your personal and professional life</li>
          </ul>
          <p>Our book provides in-depth guidance on these topics and more.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">Is there something I can read now to help me understand what's going on?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>"Surviving the Singularity" covers a range of crucial topics, including:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>The potential impact of AI on various industries and job markets</li>
            <li>Strategies for thriving in an AI-driven world</li>
            <li>Ethical considerations in AI development and implementation</li>
            <li>The future of human-AI collaboration</li>
            <li>Preparing for rapid technological changes</li>
          </ul>
          <p>The free sample provides a glimpse into these topics, enticing readers to explore further.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">Is "Surviving the Singularity" suitable for non-technical readers?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>Absolutely! "Surviving the Singularity" is written for a broad audience, including:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Professionals from various fields interested in future-proofing their careers</li>
            <li>Students preparing for a rapidly changing job market</li>
            <li>Entrepreneurs looking to leverage AI in their businesses</li>
            <li>Anyone curious about the future of technology and its impact on society</li>
          </ul>
          <p>The book explains complex concepts in an accessible manner, making it valuable for both technical and non-technical readers.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What's this I hear about a Skool community? Is it any good?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>"Surviving the Singularity" aligns perfectly with the Skool community's focus on continuous learning and adaptation:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>It provides a foundation for understanding AI's impact, complementing Skool's tech-focused courses</li>
            <li>The book's strategies for personal and professional growth resonate with Skool's emphasis on skill development</li>
            <li>It encourages critical thinking about future scenarios, fostering the kind of forward-thinking mindset valued in the Skool community</li>
            <li>The content can spark meaningful discussions and collaborations among Skool members interested in AI and future technologies</li>
          </ul>
          <p>By reading this book, Skool community members can gain valuable insights that enhance their learning journey and prepare them for the challenges and opportunities of an AI-driven future.</p>
        </div>
      </AccordionItem>
    </Accordion>
</div>

<style>
  .faq-header {
    font-size: 1.75rem;
    font-weight: bold;
    color: var(--color-text-primary);
    text-align: center;
    margin: 2rem 0 1rem;
  }
</style>