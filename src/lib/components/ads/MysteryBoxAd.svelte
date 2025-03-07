<script>
  // Props for the Mystery Box ad component
  export let title = "Mood Booster Mystery Box";
  export let subtitle = "Monthly Surprises";
  export let description = "Discover curated indie treasures delivered to your door each month. Experience the joy of surprise with handpicked items to boost your mood.";
  export let price = "24.99";
  export let frequency = "month";
  export let ctaText = "Subscribe Now";
  export let ctaUrl = "https://treasuretavernhq.myshopify.com/products/%F0%9F%91%89-mood-booster-mystery-box-classic-monthly-surprises-indie-finds";
  export let imagePath = "/images/treasure-tavern-square.png";
  export let showBadge = true;
  export let badgeText = "Most Popular";
  export let itemCount = "5-7 items";
</script>

<a href={ctaUrl} class="ad-wrapper" target="_blank" rel="noopener noreferrer">
  <div class="mystery-box-ad">
    <div class="ad-content">
      <div class="ad-left">
        <div class="mystery-image-container">
          <img src={imagePath} alt="Mood Booster Mystery Box" class="mystery-image" />
          {#if showBadge}
            <div class="mystery-badge">{badgeText}</div>
          {/if}
          <div class="mystery-icon">?</div>
        </div>

        <div class="price-tag">
          <span class="price-value">${price}</span>
          <span class="price-frequency">/{frequency}</span>
        </div>
      </div>

      <div class="ad-right">
        <div class="ad-header">
          <div class="subtitle-container">
            <h3>{subtitle}</h3>
            <div class="item-count">{itemCount}</div>
          </div>
          <h2>{title}</h2>
        </div>

        <p class="ad-description">{description}</p>

        <div class="features">
          <div class="feature">
            <div class="feature-icon">🎁</div>
            <div class="feature-text">Curated Surprises</div>
          </div>
          <div class="feature">
            <div class="feature-icon">🚚</div>
            <div class="feature-text">Free Shipping</div>
          </div>
          <div class="feature">
            <div class="feature-icon">💫</div>
            <div class="feature-text">Indie Finds</div>
          </div>
        </div>

        <div class="ad-footer">
          <div class="cta-button">
            <span class="cta-text">{ctaText}</span>
            <span class="box-icon">📦</span>
          </div>
        </div>
      </div>
    </div>

    <div class="corner top-left"></div>
    <div class="corner top-right"></div>
    <div class="corner bottom-left"></div>
    <div class="corner bottom-right"></div>
  </div>
</a>

<style>
  .ad-wrapper {
    display: block;
    text-decoration: none;
    width: fit-content;
    margin: 2rem auto;
    max-width: 900px;
  }

  .mystery-box-ad {
    position: relative;
    max-width: 900px;
    background: linear-gradient(135deg, #2b0968 0%, #318bbb 100%);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    aspect-ratio: 2 / 1;
    margin: 0; /* Remove margin as it's now on the parent */
  }

  .corner {
    position: absolute;
    width: 30px;
    height: 30px;
    border-color: rgba(255, 255, 255, 0.5);
    z-index: 5;
    pointer-events: none;
  }

  .top-left {
    top: 15px;
    left: 15px;
    border-top: 3px solid;
    border-left: 3px solid;
    border-radius: 8px 0 0 0;
  }

  .top-right {
    top: 15px;
    right: 15px;
    border-top: 3px solid;
    border-right: 3px solid;
    border-radius: 0 8px 0 0;
  }

  .bottom-left {
    bottom: 15px;
    left: 15px;
    border-bottom: 3px solid;
    border-left: 3px solid;
    border-radius: 0 0 0 8px;
  }

  .bottom-right {
    bottom: 15px;
    right: 15px;
    border-bottom: 3px solid;
    border-right: 3px solid;
    border-radius: 0 0 8px 0;
  }

  .mystery-box-ad:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 0 0 20px rgba(49, 167, 187, 0.3);
  }

  .ad-content {
    display: flex;
    position: relative;
    z-index: 2;
    border-radius: 12px;
    overflow: hidden;
    height: 100%;

    @media (max-width: 768px) {
      flex-direction: column;
    }
  }

  .ad-left {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1.5rem;
    position: relative;
    background: linear-gradient(135deg, #2b0968 0%, #274584 100%);
  }

  .mystery-image-container {
    position: relative;
    width: 180px;
    height: 180px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.5rem;
    border-radius: 10px;
    overflow: hidden;
  }

  .mystery-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
    filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.4));
    transition: transform 0.5s ease;
    z-index: 1;
  }

  .mystery-box-ad:hover .mystery-image {
    transform: scale(1.05);
  }

  .mystery-badge {
    position: absolute;
    top: 0;
    left: -5px;
    background: linear-gradient(135deg, #ff6b6b 0%, #ffc048 100%);
    color: white;
    font-size: 0.85rem;
    font-weight: bold;
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    transform: rotate(-3deg);
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
    z-index: 3;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .mystery-icon {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 70px;
    height: 70px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(5px);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 3rem;
    font-weight: bold;
    color: rgba(255, 255, 255, 0.9);
    border: 3px solid rgba(255, 255, 255, 0.4);
    z-index: 2;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  .price-tag {
    display: inline-flex;
    align-items: baseline;
    background: linear-gradient(135deg, #a8f0d3 0%, #41c1ea 100%);
    padding: 0.5rem 1.2rem;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
    color: #1a1a1a;
    transform: rotate(-2deg);
    margin-top: 1rem;
    font-weight: bold;
    z-index: 4;
  }

  .price-value {
    font-size: 1.8rem;
    font-weight: bold;
  }

  .price-frequency {
    font-size: 1rem;
    margin-left: 2px;
  }

  .ad-right {
    flex: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, #2e75bb 0%, #31a7bb 100%);
  }

  .ad-header {
    margin-bottom: 1rem;
  }

  .subtitle-container {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 500;
  }

  .item-count {
    margin-left: 1rem;
    background: rgba(255, 255, 255, 0.15);
    color: #ffffff;
    font-size: 0.8rem;
    padding: 0.25rem 1rem;
    border-radius: 50px;
    letter-spacing: 1px;
    backdrop-filter: blur(4px);
  }

  h2 {
    margin: 0;
    font-size: 2.4rem;
    color: #ffffff;
    font-weight: bold;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    letter-spacing: 0.5px;
    line-height: 1.1;
  }

  .ad-description {
    margin: 0 0 1.5rem 0;
    font-size: 1.15rem;
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.6;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }

  .features {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .feature {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.15);
    padding: 0.5rem 1rem;
    border-radius: 50px;
    flex: 1;
    backdrop-filter: blur(4px);
  }

  .feature-icon {
    font-size: 1.2rem;
    margin-right: 0.5rem;
  }

  .feature-text {
    font-size: 0.9rem;
    color: white;
    font-weight: 500;
  }

  .ad-footer {
    margin-top: auto;
    display: flex;
  }

  .cta-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(90deg, #ff6b6b 0%, #ffb84d 100%);
    color: white;
    font-weight: bold;
    padding: 1rem 2rem;
    border-radius: 50px;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    text-align: center;
    font-size: 1.1rem;
    position: relative;
    overflow: hidden;
  }

  .cta-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.7s ease;
  }

  .cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5);
    background: linear-gradient(135deg, #ff5252 0%, #ffb300 100%);
  }

  .cta-button:hover::before {
    left: 100%;
  }

  .cta-text {
    margin-right: 0.75rem;
  }

  .box-icon {
    font-size: 1.3rem;
    transition: transform 0.3s ease;
  }

  .cta-button:hover .box-icon {
    transform: translateY(-4px);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .ad-left {
      padding: 1.5rem 1rem;
    }

    .mystery-image-container {
      width: 160px;
      height: 160px;
      margin-bottom: 1rem;
    }

    .ad-right {
      padding: 1.5rem;
    }

    h2 {
      font-size: 2rem;
    }

    .ad-description {
      font-size: 1rem;
      margin-bottom: 1.2rem;
    }

    .features {
      flex-wrap: wrap;
    }

    .feature {
      min-width: 140px;
    }

    .mystery-box-ad {
      aspect-ratio: auto;
    }
  }

  @media (max-width: 480px) {
    .corner {
      width: 20px;
      height: 20px;
    }

    .top-left, .top-right, .bottom-left, .bottom-right {
      border-width: 2px;
    }

    .mystery-image-container {
      width: 140px;
      height: 140px;
    }

    .mystery-icon {
      width: 50px;
      height: 50px;
      font-size: 2rem;
    }

    .price-tag {
      padding: 0.4rem 0.8rem;
    }

    .price-value {
      font-size: 1.5rem;
    }

    h3 {
      font-size: 1rem;
    }

    .item-count {
      font-size: 0.7rem;
      padding: 0.2rem 0.6rem;
    }

    h2 {
      font-size: 1.7rem;
    }

    .features {
      flex-direction: column;
      gap: 0.6rem;
    }

    .cta-button {
      width: 100%;
      padding: 0.8rem 1.5rem;
    }
  }
</style>