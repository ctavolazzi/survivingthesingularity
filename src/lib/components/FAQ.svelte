<script>
  import { Accordion, AccordionItem } from 'flowbite-svelte';
</script>

<div class="content-container">
    <div class="faq-header">Frequently Asked Questions</div>
    <Accordion class="content-box">
      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What is the Singularity?</span>
        <p class="text-[var(--color-text-secondary)]">
          The Singularity is that mind-bending point where AI surpasses human intelligence. Imagine your smartphone suddenly deciding it's smarter than you - and being right. It's when our tech takes the wheel and starts driving us into uncharted territory. Whether that's a utopia or a "rise of the machines" scenario is anyone's guess. Buckle up!
        </p>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">When is the Singularity expected to occur?</span>
        <p class="text-[var(--color-text-secondary)]">
          Here's the thing about the Singularity - it's not a single "boom" moment, but more like a rollercoaster that's already left the station and is picking up speed. Check out our timeline below for our best educated guess on when things will really start to feel like they're taking off. But remember, we're already on this ride. Each day, technology gets more sophisticated, cheaper, and easier to access. The pace of change is accelerating, and before you know it, we'll be in a world that makes today look like the Stone Age. So when is the Singularity? In many ways, it's already begun.
        </p>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What are the potential impacts of the Singularity?</span>
        <p class="text-[var(--color-text-secondary)]">
          As our timeline shows, the impacts of the Singularity will be far-reaching and mind-boggling:
          <ul class="list-disc pl-5 mt-2">
            <li>Medicine: We might cure death before we cure the common cold. Immortality, anyone?</li>
            <li>Economy: When AI can do any job, what happens to human work? Universal Basic Income or universal poverty?</li>
            <li>Education: Forget studying - just download knowledge directly to your brain. Hope you like pop-up ads in your dreams.</li>
            <li>Ethics: When machines can think and feel, do they deserve rights? And who gets to decide?</li>
          </ul>
          Each advancement on our timeline isn't just a cool new gadget - it's a step towards a fundamentally different world. The Singularity isn't just a tech revolution - it's a redefinition of what it means to be human.
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">How can one prepare for the Singularity?</span>
        <p class="text-[var(--color-text-secondary)]">
          Preparing for the Singularity is like trying to pack for a trip where the destination keeps changing. But don't panic - here's your survival kit:
          <ul class="list-disc pl-5 mt-2">
            <li>Stay informed: Keep an eye on our timeline. Today's sci-fi is tomorrow's reality.</li>
            <li>Embrace adaptability: The only constant will be change, so get comfortable with being uncomfortable.</li>
            <li>Develop a growth mindset: Learning won't stop when you leave school. In fact, it'll be more important than ever.</li>
            <li>Engage in the conversation: The future's coming whether we like it or not. Might as well have a say in shaping it.</li>
          </ul>
          Remember, surviving the Singularity isn't just about keeping up with the latest tech - it's about staying human in a world that's evolving faster than we can comprehend. Keep an eye on our timeline, but more importantly, keep an eye on what makes us human.
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