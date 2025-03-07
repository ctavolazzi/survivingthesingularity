<script>
  /**
   * A reusable section component for newsletters
   * This component provides consistent styling for newsletter sections
   */

  // Section title (required)
  export let title = "";

  // Section type affects styling (optional)
  // Options: "default", "featured", "news", "resources", "community", "tip"
  export let type = "default";

  // Whether the section should have a border (optional)
  export let bordered = false;

  // Additional custom class (optional)
  export let className = "";

  // Generate classes based on props
  $: sectionClasses = `newsletter-section ${type}-section ${bordered ? 'bordered' : ''} ${className}`;
</script>

<section class={sectionClasses}>
  <h2>{title}</h2>
  <div class="section-content">
    <slot></slot>
  </div>
</section>

<style>
  .newsletter-section {
    margin: 2rem 0;
    padding: 0.5rem 0;
    width: 100%;
  }

  .bordered {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
  }

  :global(.dark) .bordered {
    border-color: #374151;
  }

  h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #1f2937;
  }

  :global(.dark) h2 {
    color: #f3f4f6;
  }

  .section-content {
    line-height: 1.6;
  }

  /* Special styling for different section types */
  .featured-section h2 {
    font-size: 1.75rem;
    color: #2563eb;
  }

  :global(.dark) .featured-section h2 {
    color: #60a5fa;
  }

  .news-section {
    background-color: #f9fafb;
    padding: 1.5rem;
    border-radius: 8px;
  }

  :global(.dark) .news-section {
    background-color: #111827;
  }

  .tip-section {
    background-color: #f0f9ff;
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid #3b82f6;
  }

  :global(.dark) .tip-section {
    background-color: #082f49;
    border-left-color: #60a5fa;
  }

  /* Responsive styling */
  @media (max-width: 768px) {
    .newsletter-section {
      margin: 1.5rem 0;
    }

    h2 {
      font-size: 1.35rem;
    }

    .featured-section h2 {
      font-size: 1.5rem;
    }
  }

  @media (max-width: 480px) {
    .newsletter-section {
      margin: 1rem 0;
    }

    .bordered, .news-section, .tip-section {
      padding: 1rem;
    }

    h2 {
      font-size: 1.25rem;
      margin-bottom: 0.75rem;
    }
  }
</style>