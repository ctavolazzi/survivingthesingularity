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
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What is material independence?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>Material independence is the ability to meet your basic survival needs — food, shelter, energy, and income — without depending on extractive corporate or financial systems. It means:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Owning land and shelter outright, bypassing the 30-year mortgage trap</li>
            <li>Growing a significant portion of your own food using open-source robotics like FarmBot</li>
            <li>Running your own AI tools locally instead of paying for cloud subscriptions</li>
            <li>Generating income through direct-to-consumer digital products rather than corporate employment</li>
          </ul>
          <p>As purchasing power erodes and AI transforms the labor market, material independence is becoming the primary survival strategy for those without inherited wealth.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What is a "shouse" and why does it matter?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>A shouse (shop-house) is a hybrid structure that prioritizes production space over living space. Instead of a traditional suburban home designed for consumption and leisure, the shouse model:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Puts the workshop first — your engine of production and income</li>
            <li>Keeps living quarters minimal and efficient (often under $8,000)</li>
            <li>Can be built on rural land using steel construction at $25-45 per square foot</li>
            <li>Drops monthly overhead to the bare minimum, buying back decades of your life</li>
          </ul>
          <p>The shouse is the physical foundation of the Millennial Builder framework — a way to escape the debt cycle and reclaim time for meaningful work.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">What tools do I need to get started?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>The Millennial Builder stack has both a digital and physical layer:</p>
          <ul class="list-disc pl-5 mt-2">
            <li><strong>Local AI:</strong> A machine with 32GB+ RAM and a high-VRAM GPU (RTX 3090/4090/5090) running Ollama or LM Studio</li>
            <li><strong>Food production:</strong> FarmBot Genesis or similar open-source CNC garden robots for automated growing</li>
            <li><strong>Workshop automation:</strong> Mobile ALOHA or similar bimanual robots for physical task assistance</li>
            <li><strong>Digital income:</strong> YouTube channel documenting your build process, plus direct-to-consumer solutions via platforms like Lemon Squeezy</li>
          </ul>
          <p>Start with what you have. The most important first step is documenting your journey — even a three-minute phone video has value.</p>
          <div class="mt-4 text-center">
            <a href="/blog" class="inline-block px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors">
              Read Our Guides
            </a>
          </div>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">Why is local AI sovereignty important?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>Running AI models locally on your own hardware ensures that your intelligence layer is as secure as your most sensitive data. Local AI sovereignty means:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Your research and proprietary data never leaves your machine — no cloud exposure</li>
            <li>No subscription fees or API costs eating into your margins</li>
            <li>No corporate alignment filters restricting what you can research or synthesize</li>
            <li>Full control over your tools, even if external services go down or change terms</li>
          </ul>
          <p>With hardware like the RTX 5090 (32GB VRAM) and open-weight models like Llama 4, running 70B-parameter models locally is now practical for individual builders.</p>
        </div>
      </AccordionItem>

      <AccordionItem>
        <span slot="header" class="text-lg font-semibold text-[var(--color-text-primary)]">Do I need to be technical to follow this path?</span>
        <div class="text-[var(--color-text-secondary)]">
          <p>No. The entire framework is built on the principle that if something took you more than an hour to learn, you can teach it to someone else. The path is designed to be learned by doing:</p>
          <ul class="list-disc pl-5 mt-2">
            <li>Start by documenting what you already know — everyone has at least one teachable skill</li>
            <li>Use AI tools to accelerate your learning curve on technical topics</li>
            <li>Follow open-source project documentation — FarmBot and Mobile ALOHA have step-by-step guides</li>
            <li>The community of builders shares blueprints, costs, and real results openly</li>
          </ul>
          <p>The goal is not to become a software engineer. It is to become competent enough with modern tools to secure your own resources independently.</p>
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