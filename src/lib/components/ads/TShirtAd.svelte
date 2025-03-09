<script>
  // Props for the ad component
  export let title = "Surviving The Singularity T-Shirt";
  export let description = "Show the world you're prepared for what's coming. Limited edition, high-quality cotton blend t-shirt featuring our iconic 'Surviving The Singularity' design.";
  export let price = "$29.99";
  export let ctaText = "Get Yours Now";
  export let imagePath = "/images/singularity-tshirt-ad.webp";
</script>

<div class="tshirt-ad-container">
  <div class="ad-content">
    <div class="ad-image-container">
      <img src={imagePath} alt="Surviving The Singularity T-Shirt" class="ad-image"  loading="lazy" \/\>
      <div class="limited-badge">Limited Edition</div>
    </div>
    <div class="ad-text">
      <h3>{title}</h3>
      <p class="ad-description">{description}</p>
      <div class="ad-footer">
        <span class="price">{price}</span>
        <a href="#" class="cta-button">{ctaText}</a>
      </div>
    </div>
  </div>
</div>

<style>
  .tshirt-ad-container {
    margin: 2rem auto;
    max-width: 800px;
    background: var(--color-bg-secondary, #f8f9fa);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .tshirt-ad-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  .ad-content {
    display: flex;
    flex-direction: column;

    @media (min-width: 768px) {
      flex-direction: row;
    }
  }

  .ad-image-container {
    position: relative;
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
  }

  .ad-image {
    max-width: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 8px;
  }

  .limited-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: #ff3e00;
    color: white;
    font-size: 0.8rem;
    font-weight: bold;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    transform: rotate(5deg);
    box-shadow: 0 2px 4px rgba(255, 62, 0, 0.3);
    z-index: 2;
  }

  .ad-text {
    flex: 1;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
  }

  h3 {
    margin: 0 0 0.75rem 0;
    font-size: 1.5rem;
    color: var(--color-text-primary, #212529);
  }

  .ad-description {
    margin: 0 0 1.5rem 0;
    font-size: 1rem;
    color: var(--color-text-secondary, #6c757d);
    flex-grow: 1;
    line-height: 1.6;
  }

  .ad-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
  }

  .price {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--color-text-primary, #212529);
  }

  .cta-button {
    display: inline-block;
    background: linear-gradient(135deg, #ff3e00 0%, #ff8700 100%);
    color: white;
    font-weight: bold;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    text-decoration: none;
    transition: all 0.2s ease;
    box-shadow: 0 4px 8px rgba(255, 62, 0, 0.25);
  }

  .cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(255, 62, 0, 0.35);
  }

  /* Dark mode support */
  :global(.dark) .tshirt-ad-container {
    background: var(--color-bg-secondary-dark, #2a2d31);
  }

  :global(.dark) h3 {
    color: var(--color-text-primary-dark, #f8f9fa);
  }

  :global(.dark) .ad-description {
    color: var(--color-text-secondary-dark, #adb5bd);
  }

  :global(.dark) .price {
    color: var(--color-text-primary-dark, #f8f9fa);
  }
</style>