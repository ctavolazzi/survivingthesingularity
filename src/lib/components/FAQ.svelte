<script>
  import { Accordion, AccordionItem } from 'flowbite-svelte';

  // Handle class properly - In Svelte, we use class directly
  let cssClass = "";
  export { cssClass as class };
</script>

<div class="content-container {cssClass}">
    <div class="faq-header">Frequently Asked Questions</div>
    <Accordion class="content-box">
      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What is the Singularity?</span>
        <p class="text-[var(--color-text-secondary)]">
          The Technological Singularity refers to a hypothetical future point when artificial intelligence surpasses human intelligence, potentially leading to rapid and unpredictable technological growth. This concept is central to our book, as we explore its implications and how to navigate this transformative period.
        </p>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">How can I think about preparing for these changes?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>Navigating the AI revolution involves considering several approaches:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Staying informed about AI developments and their potential impacts</li>
            <li>Developing frameworks for thinking about the relationship between humans and AI</li>
            <li>Exploring ethical considerations surrounding emerging technologies</li>
            <li>Considering how AI might affect different aspects of society and personal life</li>
          </ul>
          <p>The book explores these topics as they continue to evolve.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">Is there something I can read now to help me understand what's going on?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>"Surviving the Singularity" is examining a range of crucial topics, including:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>The potential impact of AI on various industries and social structures</li>
            <li>Approaches for adapting to rapid technological changes</li>
            <li>Ethical considerations in AI development and implementation</li>
            <li>The evolving relationship between humans and technology</li>
            <li>Tools for processing complex technological shifts</li>
          </ul>
          <p>The free sample provides initial thoughts on these topics as they continue to be developed.</p>
          <div class="mt-4 text-center">
            <a href="/book" class="inline-block px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors">
              Read a Sample
            </a>
          </div>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">Is "Surviving the Singularity" suitable for non-technical readers?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>Absolutely! "Surviving the Singularity" is being written for a broad audience, including:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>People from all backgrounds interested in understanding technological change</li>
            <li>Anyone trying to make sense of how AI might affect society</li>
            <li>Those feeling overwhelmed by the pace of technological advancement</li>
            <li>People curious about developing clearer thinking about the future</li>
          </ul>
          <p>The book approaches complex concepts in an accessible manner, making it valuable for both technical and non-technical readers.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What's this I hear about a Skool community? Is it any good?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>"Surviving the Singularity" connects with the Skool community's focus on learning and adaptation:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>It explores AI's potential impacts, complementing Skool's tech-focused discussions</li>
            <li>The book's frameworks for thinking about change resonate with Skool's emphasis on development</li>
            <li>It encourages critical thinking about future scenarios, supporting the kind of forward-thinking mindset valued in the Skool community</li>
            <li>The evolving content can spark meaningful discussions among those interested in AI and future technologies</li>
          </ul>
          <p>The Skool community provides a space for readers to discuss these topics as the book develops.</p>
        </div>
      </AccordionItem>
    </Accordion>
</div>

<style>
  .faq-header {
    font-size: clamp(1.5rem, 3.5vw, 1.75rem);
    font-weight: bold;
    color: var(--color-text-primary);
    text-align: center;
    margin: 2rem 0 1rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Very small screen adjustment */
  @media (max-width: 350px) {
    .faq-header {
      font-size: clamp(1.35rem, 3vw, 1.5rem);
    }
  }
</style>