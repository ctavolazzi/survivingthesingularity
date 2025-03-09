<script>
  import NewsletterSection from '../NewsletterSection.svelte';
</script>

<!-- This is a template for creating newsletter editions using the modular component approach -->
<!-- When creating a new newsletter, copy this file and customize the content -->

<div class="newsletter">
  <!-- Header Section -->
  <header class="newsletter-header">
    <h1>[Newsletter Title]</h1>
    <p class="intro">
      Welcome to edition #XXX of the Surviving the Singularity newsletter.
    </p>
  </header>

  <!-- Introduction Section -->
  <NewsletterSection title="Introduction" type="default">
    <p>
      A brief introduction to this week's newsletter and the main themes covered.
    </p>
  </NewsletterSection>

  <!-- Main Topic Section -->
  <NewsletterSection title="Main Topic: [Topic Title]" type="featured">
    <p>
      Your main content goes here. This is where you write about the primary focus of this newsletter edition.
    </p>

    <h3>[Main Topic Subheading]</h3>
    <p>Continue your main topic content here.</p>

    <!-- Example of how to add an image -->
    <!--
    <figure class="image-container">
      <img src="/path/to/image.jpg" alt="Description of image"  loading="lazy" \/>
      <figcaption>Image caption goes here</figcaption>
    </figure>
    -->

    <!-- Example of how to add a quote -->
    <!--
    <blockquote>
      <p>"This is an important quote that emphasizes your point."</p>
      <cite>— Source Name</cite>
    </blockquote>
    -->
  </NewsletterSection>

  <!-- News Section -->
  <NewsletterSection title="This Week in AI" type="news">
    <ul class="news-list">
      <li>
        <strong>[News Item 1]:</strong> Description or commentary about this news item
      </li>
      <li>
        <strong>[News Item 2]:</strong> Description or commentary about this news item
      </li>
      <li>
        <strong>[News Item 3]:</strong> Description or commentary about this news item
      </li>
    </ul>
  </NewsletterSection>

  <!-- Resources Section -->
  <NewsletterSection title="Resources & Tools" type="resources">
    <div class="resource">
      <h3>[Resource Name 1]</h3>
      <p>Brief description of this resource and why it's valuable.</p>
      <a href="#" class="resource-link">Check it out →</a>
    </div>

    <div class="resource">
      <h3>[Resource Name 2]</h3>
      <p>Brief description of this resource and why it's valuable.</p>
      <a href="#" class="resource-link">Check it out →</a>
    </div>
  </NewsletterSection>

  <!-- Community Section (Optional) -->
  <NewsletterSection title="Community Spotlight" type="community">
    <p>
      Highlight community members, questions, or discussions here.
    </p>
  </NewsletterSection>

  <!-- Practical Tip Section -->
  <NewsletterSection title="Practical Tip" type="tip">
    <p>
      A concise, practical tip related to AI, technology, or surviving the singularity.
    </p>
  </NewsletterSection>

  <!-- Footer Section -->
  <footer class="newsletter-footer">
    <hr />
    <p>
      That's all for this edition! Let me know what you think by replying to this email.
    </p>
    <p class="signature">
      Stay curious,<br />
      [Your Name]
    </p>
  </footer>
</div>

<style>
  .newsletter {
    max-width: 100%;
    margin: 0 auto;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  .newsletter-header {
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
  }

  .intro {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }

  h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 1.5rem 0 0.75rem 0;
  }

  p {
    margin: 0 0 1rem 0;
    line-height: 1.6;
  }

  /* News list styling */
  .news-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }

  .news-list li {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
    position: relative;
  }

  .news-list li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #3b82f6;
  }

  /* Resources styling */
  .resource {
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
  }

  .resource:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }

  .resource-link {
    display: inline-block;
    color: #3b82f6;
    font-weight: 500;
    text-decoration: none;
    margin-top: 0.5rem;
  }

  .resource-link:hover {
    text-decoration: underline;
  }

  /* Image container */
  .image-container {
    margin: 1.5rem 0;
    width: 100%;
  }

  .image-container img {
    max-width: 100%;
    height: auto;
    border-radius: 0.5rem;
  }

  figcaption {
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: #6b7280;
    text-align: center;
  }

  /* Quote styling */
  blockquote {
    margin: 1.5rem 0;
    padding: 1rem 1.5rem;
    border-left: 4px solid #3b82f6;
    background-color: #f9fafb;
    font-style: italic;
  }

  blockquote p {
    margin-bottom: 0.5rem;
  }

  blockquote cite {
    font-size: 0.875rem;
    font-style: normal;
    color: #6b7280;
  }

  /* Footer styling */
  .newsletter-footer {
    margin-top: 3rem;
  }

  hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 2rem 0;
  }

  .signature {
    margin-top: 1rem;
    font-style: italic;
  }

  /* Dark mode adjustments are handled by the parent components */
</style>
