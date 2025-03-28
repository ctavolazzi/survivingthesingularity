<script>
  // Props for the Treasure Tavern ad component
  export let title = "Discover Unique Treasures";
  export let subtitle = "The Treasure Tavern";
  export let description = "Find rare collectibles, unique artifacts, and curated treasures from around the world. Each item has a story, each purchase is an adventure.";
  export let ctaText = "Explore the Tavern";
  export let ctaUrl = "https://treasuretavernhq.com/"; // Update with actual store URL
  export let imagePath = "/images/treasure-tavern-square.png"; // Changed to square image
  export let showBadge = true;
  export let badgeText = "New Arrivals";
  // New prop for bullet points
  export let bulletPoints = [];

  // Featured product props
  export let featuredProduct = null; // { title, price, image, url }
  export let showFeaturedProduct = false;

  // Compute if we should show the featured product
  $: canShowFeaturedProduct = showFeaturedProduct && featuredProduct;
  // Check if we have bullet points
  $: hasBulletPoints = bulletPoints && bulletPoints.length > 0;
</script>

<div class="treasure-tavern-ad">
  <div class="treasure-shimmer"></div>
  <div class="ad-content">
    <div class="ad-image-container">
      <img src={imagePath} alt="Treasure Tavern Store" class="ad-image" loading="lazy" />
      {#if showBadge}
        <div class="treasure-badge">{badgeText}</div>
      {/if}
    </div>
    <div class="ad-text">
      <div class="ad-header">
        <h3>{subtitle}</h3>
        <h2>{title}</h2>
      </div>
      <p class="ad-description">{description}</p>

      {#if hasBulletPoints}
        <ul class="feature-list">
          {#each bulletPoints as point}
            <li class="feature-item">
              <span class="feature-icon">✦</span>
              <span class="feature-text">{point}</span>
            </li>
          {/each}
        </ul>
      {/if}

      {#if canShowFeaturedProduct}
        <div class="featured-product">
          <div class="product-image-container">
            <img src={featuredProduct.image} alt={featuredProduct.title} class="product-image"  loading="lazy" />
            <div class="product-price">${featuredProduct.price}</div>
          </div>
          <div class="product-details">
            <h4 class="product-title">{featuredProduct.title}</h4>
            <a href={featuredProduct.url} class="product-link">View Item →</a>
          </div>
        </div>
      {/if}

      <div class="ad-footer">
        <a href={ctaUrl} class="cta-button">
          <span class="cta-text">{ctaText}</span>
          <span class="cta-icon">→</span>
        </a>
      </div>
    </div>
  </div>
  <div class="corner-decoration top-left"></div>
  <div class="corner-decoration top-right"></div>
  <div class="corner-decoration bottom-left"></div>
  <div class="corner-decoration bottom-right"></div>
</div>

<style>
  .treasure-tavern-ad {
    position: relative;
    margin: 2rem auto;
    max-width: 900px;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid rgba(193, 154, 73, 0.3);
    padding: 4px;
    box-sizing: border-box;
  }

  .treasure-shimmer {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ddb86b, transparent);
    animation: shimmer 3s infinite;
    z-index: 1;
  }

  @keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }

  .corner-decoration {
    position: absolute;
    width: 20px;
    height: 20px;
    border-color: #c19a49;
    z-index: 2;
  }

  .top-left {
    top: 8px;
    left: 8px;
    border-top: 2px solid;
    border-left: 2px solid;
    border-radius: 4px 0 0 0;
  }

  .top-right {
    top: 8px;
    right: 8px;
    border-top: 2px solid;
    border-right: 2px solid;
    border-radius: 0 4px 0 0;
  }

  .bottom-left {
    bottom: 8px;
    left: 8px;
    border-bottom: 2px solid;
    border-left: 2px solid;
    border-radius: 0 0 0 4px;
  }

  .bottom-right {
    bottom: 8px;
    right: 8px;
    border-bottom: 2px solid;
    border-right: 2px solid;
    border-radius: 0 0 4px 0;
  }

  .treasure-tavern-ad:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 0 0 20px rgba(193, 154, 73, 0.2);
  }

  .ad-content {
    display: flex;
    flex-direction: column;
    position: relative;
    z-index: 2;
    background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
    border-radius: 8px;
    overflow: hidden;
  }

  /* Desktop layout - larger screens */
  @media (min-width: 768px) {
    .ad-content {
      flex-direction: row;
      min-height: 350px; /* Set minimum height for desktop */
    }

    .ad-image-container {
      flex: 0 0 40%; /* Fixed width for image container on desktop */
      max-width: 40%;
    }

    .ad-text {
      flex: 0 0 60%; /* Fixed width for text container on desktop */
      max-width: 60%;
    }
  }

  /* Large desktop screens */
  @media (min-width: 1200px) {
    .treasure-tavern-ad {
      max-width: 1000px; /* Slightly wider on very large screens */
    }

    .ad-content {
      min-height: 380px;
    }

    h2 {
      font-size: 2.4rem;
    }

    .ad-description {
      font-size: 1.2rem;
    }
  }

  .ad-image-container {
    position: relative;
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1.5rem;
    background: radial-gradient(circle at center, rgba(193, 154, 73, 0.1), transparent 70%);
    overflow: hidden; /* Prevent image overflow */
  }

  .ad-image {
    max-width: 100%;
    height: auto;
    max-height: 300px; /* Limit image height */
    object-fit: contain; /* Maintain aspect ratio */
    filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.5));
    transition: transform 0.5s ease;
    border-radius: 8px;
    border: 2px solid rgba(193, 154, 73, 0.4);
    transform: rotate(-3deg);
  }

  @media (min-width: 768px) {
    .ad-image {
      max-height: none; /* Allow natural height on desktop */
      width: 90%; /* Slightly smaller than container for spacing */
    }
  }

  .treasure-tavern-ad:hover .ad-image {
    transform: rotate(0deg) scale(1.05);
  }

  .treasure-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: linear-gradient(135deg, #c7593b 0%, #e27b58 100%);
    color: white;
    font-size: 0.9rem;
    font-weight: bold;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    transform: rotate(5deg);
    box-shadow: 0 3px 6px rgba(199, 89, 59, 0.5);
    z-index: 3;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .ad-text {
    flex: 1.5;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    background: linear-gradient(rgba(0,0,0,0.2), transparent);
  }

  .ad-header {
    margin-bottom: 1.5rem;
  }

  h2 {
    margin: 0.3rem 0 0 0;
    font-size: 2.2rem;
    color: #f0f0f0;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    letter-spacing: 0.5px;
  }

  h3 {
    margin: 0;
    font-size: 1.2rem;
    color: #ddb86b;
    font-weight: normal;
    text-transform: uppercase;
    letter-spacing: 2px;
  }

  .ad-description {
    margin: 0 0 1.5rem 0;
    font-size: 1.15rem;
    color: #adb5bd;
    line-height: 1.7;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }

  .ad-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: auto;
  }

  .cta-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #c19a49 0%, #ddb86b 100%);
    color: #1a1a2e;
    font-weight: bold;
    padding: 0.9rem 2rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(193, 154, 73, 0.4);
    text-align: center;
    font-size: 1.1rem;
    position: relative;
    overflow: hidden;
    white-space: normal;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }

  .cta-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.7s ease;
  }

  .cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(193, 154, 73, 0.5);
    background: linear-gradient(135deg, #d4af61 0%, #e9ca83 100%);
  }

  .cta-button:hover::before {
    left: 100%;
  }

  .cta-text {
    margin-right: 8px;
  }

  .cta-icon {
    font-size: 1.3rem;
    transition: transform 0.3s ease;
  }

  .cta-button:hover .cta-icon {
    transform: translateX(4px);
  }

  /* Mobile optimization for CTA button */
  @media (max-width: 480px) {
    .cta-button {
      padding: 0.8rem 1.5rem;
      width: 80%;
      max-width: 250px;
      margin: 0 auto;
    }

    .ad-footer {
      margin-top: 1.5rem;
    }
  }

  /* Desktop optimization for CTA button */
  @media (min-width: 768px) {
    .cta-button {
      padding: 0.9rem 2.5rem;
      margin: 0; /* Remove centering on desktop */
    }

    .ad-footer {
      justify-content: flex-start; /* Align to left on desktop */
    }
  }

  .featured-product {
    margin: 0 0 1.5rem 0;
    padding: 1rem;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    border: 1px solid rgba(193, 154, 73, 0.3);
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.3s ease;
  }

  .featured-product:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    border-color: rgba(193, 154, 73, 0.5);
  }

  /* Desktop layout for featured product */
  @media (min-width: 768px) {
    .featured-product {
      max-width: 85%; /* Limit width on desktop */
      margin-bottom: 2rem;
    }
  }

  .product-image-container {
    position: relative;
    flex: 0 0 100px;
  }

  .product-image {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 6px;
    border: 2px solid rgba(193, 154, 73, 0.5);
    filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.3));
  }

  .product-price {
    position: absolute;
    bottom: -8px;
    right: -8px;
    background: linear-gradient(135deg, #c19a49 0%, #ddb86b 100%);
    color: #1a1a2e;
    font-weight: bold;
    padding: 0.3rem 0.6rem;
    border-radius: 6px;
    font-size: 0.95rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  }

  .product-details {
    flex: 1;
  }

  .product-title {
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    color: #f0f0f0;
    font-weight: bold;
  }

  .product-link {
    color: #ddb86b;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: bold;
    display: inline-flex;
    align-items: center;
    transition: all 0.2s ease;
  }

  .product-link:hover {
    color: #e9ca83;
    text-decoration: underline;
  }

  /* Responsive adjustments */
  @media (max-width: 767px) {
    .ad-image-container {
      min-height: 200px;
      padding: 1rem;
    }

    .ad-text {
      padding: 1.5rem;
    }

    h2 {
      font-size: 1.8rem;
    }

    .ad-description {
      font-size: 1rem;
      margin-bottom: 1.5rem;
    }

    .treasure-badge {
      font-size: 0.8rem;
      padding: 0.3rem 0.8rem;
    }

    .featured-product {
      flex-direction: column;
      align-items: flex-start;
      padding: 0.85rem;
    }

    .product-image-container {
      margin-bottom: 1rem;
    }
  }

  /* Small mobile screens */
  @media (max-width: 380px) {
    .ad-text {
      padding: 1.25rem;
    }

    h2 {
      font-size: 1.6rem;
    }

    h3 {
      font-size: 1rem;
    }

    .ad-description {
      font-size: 0.95rem;
    }

    .treasure-badge {
      font-size: 0.75rem;
      padding: 0.25rem 0.7rem;
      top: 5px;
      right: 5px;
    }
  }

  /* Tablet-specific adjustments */
  @media (min-width: 768px) and (max-width: 1023px) {
    .treasure-tavern-ad {
      max-width: 90%;
    }

    .ad-content {
      min-height: 320px;
    }

    .ad-image-container {
      flex: 0 0 45%;
      max-width: 45%;
    }

    .ad-text {
      flex: 0 0 55%;
      max-width: 55%;
      padding: 1.75rem;
    }

    h2 {
      font-size: 2rem;
    }
  }

  /* New styles for bullet points */
  .feature-list {
    list-style: none;
    padding: 0;
    margin: 0 0 1.5rem 0;
  }

  @media (min-width: 768px) {
    .feature-list {
      margin: 0 0 2rem 0;
      max-width: 90%; /* Limit width on desktop */
    }
  }

  .feature-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.75rem;
    transition: transform 0.2s ease;
  }

  .feature-item:hover {
    transform: translateX(3px);
  }

  .feature-icon {
    color: #ddb86b;
    font-size: 1rem;
    margin-right: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(193, 154, 73, 0.15);
    border-radius: 50%;
    width: 22px;
    height: 22px;
    flex-shrink: 0;
    box-shadow: 0 0 10px rgba(193, 154, 73, 0.2);
  }

  .feature-text {
    color: #e2e8f0;
    font-size: 0.95rem;
    line-height: 1.5;
  }

  /* Container responsive margins */
  @media (max-width: 767px) {
    .treasure-tavern-ad {
      margin: 1.5rem auto;
      max-width: 95%;
    }
  }

  @media (max-width: 480px) {
    .treasure-tavern-ad {
      margin: 1rem auto;
      max-width: 100%;
      border-radius: 10px;
    }
  }
</style>