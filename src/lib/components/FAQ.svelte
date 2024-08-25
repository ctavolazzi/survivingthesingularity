<script>
  import { Accordion, AccordionItem } from 'flowbite-svelte';
</script>

<div class="content-container">
    <div class="faq-header">Frequently Asked Questions</div>
    <Accordion class="content-box">
      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What is this website about?</span>
        <p class="text-[var(--color-text-secondary)]">
          This website explores the potential future of technology and its impact on society. We provide information, timelines, and discussions about emerging technologies and their possible effects on various aspects of our lives.
        </p>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What is the Singularity?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>The Singularity refers to a hypothetical future point in time when artificial intelligence surpasses human intelligence, potentially leading to rapid and unpredictable technological growth. Key aspects include:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Exponential advancement in AI capabilities</li>
            <li>Potential for AI to improve itself, leading to recursive self-improvement</li>
            <li>Profound changes in society, economy, and human existence</li>
            <li>Debates about its likelihood, timeline, and implications</li>
          </ul>
          <p>The concept raises important questions about the future of humanity and our relationship with technology.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">How might my life be affected by near-future technology?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>Future technologies could potentially impact many areas of our lives, including:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Healthcare and medicine</li>
            <li>Work and the economy</li>
            <li>Education and learning</li>
            <li>Communication and social interactions</li>
            <li>Transportation and energy</li>
            <li>Environmental sustainability</li>
          </ul>
          <p>Our timeline and articles explore these topics in more detail.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">How can I stay informed about technological developments?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>To stay informed about technological developments:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Regularly check our timeline and articles for updates</li>
            <li>Follow reputable science and technology news sources</li>
            <li>Attend technology conferences or webinars</li>
            <li>Engage in discussions with others interested in these topics</li>
            <li>Consider taking online courses in relevant fields</li>
          </ul>
          <p>Remember, the goal is to develop a broad understanding of trends and potential impacts rather than focusing on every technical detail.</p>
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