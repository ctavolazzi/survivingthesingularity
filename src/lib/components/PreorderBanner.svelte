<script>
    import { fade, slide } from 'svelte/transition';
    import { onMount } from 'svelte';
    import StSBookImage from '$lib/images/Surviving-the-Singularity-Cover.png';
    import CtHeroImage from '$lib/images/ct_hero_image.png';
    import { darkMode } from '$lib/stores/darkMode';

    let isExpanded = false;
    let isLoading = false;
    let error = null;
    let showDropdown = false;

    function toggleExpand() {
        isExpanded = !isExpanded;
    }

    function toggleDropdown() {
        showDropdown = !showDropdown;
    }

    async function handlePreorder() {
        isLoading = true;
        error = null;

        try {
            const response = await fetch('/api/create-checkout-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const { url } = await response.json();
            window.location.href = url;
        } catch (err) {
            console.error('Preorder error:', err);
            error = 'An error occurred. Please try again.';
        } finally {
            isLoading = false;
        }
    }

    // Close dropdown when clicking outside
    onMount(() => {
        const handleClickOutside = (event) => {
            const dropdown = document.getElementById('learn-more-dropdown');
            const trigger = document.getElementById('learn-more-button');
            if (dropdown && !dropdown.contains(event.target) && trigger && !trigger.contains(event.target)) {
                showDropdown = false;
            }
        };
        window.addEventListener('click', handleClickOutside);
        return () => {
            window.removeEventListener('click', handleClickOutside);
        };
    });
</script>

<div class="banner" class:dark={$darkMode} in:fade="{{ duration: 500 }}">
    <div class="banner-content">
        <img src={StSBookImage} alt="Surviving the Singularity Book Cover" class="book-image" />
        <div class="banner-text">
            <h2>Surviving the Singularity: Workbook</h2>
            <p>Empowering you to empower yourself.</p>
            <div class="cta-container">
                <button
                    on:click={handlePreorder}
                    disabled={isLoading}
                    class="preorder-button"
                >
                    {#if isLoading}
                        <span class="loader"></span>
                    {:else}
                        PREORDER NOW
                    {/if}
                </button>
            </div>
        </div>
    </div>
    <button class="expand-button" on:click={toggleExpand}>
        {isExpanded ? 'Show Less' : 'View Book Details'}
        <span class="arrow" class:rotated={isExpanded}>▼</span>
    </button>

    {#if isExpanded}
        <div class="expanded-content" transition:slide="{{ duration: 300 }}">
            <!-- Book Preview Section -->
            <div class="learning-section">
                <h3 class="section-title">
                    <span class="title-highlight">What You'll Learn</span>
                </h3>
                <div class="learning-grid">
                    <div class="learning-item">
                        <div class="icon-wrapper">
                            <span class="icon">🎯</span>
                        </div>
                        <div class="content">
                            <h4>AI Strategy</h4>
                            <p>Practical strategies for adapting to AI changes in your career</p>
                        </div>
                    </div>

                    <div class="learning-item">
                        <div class="icon-wrapper">
                            <span class="icon">💡</span>
                        </div>
                        <div class="content">
                            <h4>Real Examples</h4>
                            <p>Case studies from professionals successfully using AI</p>
                        </div>
                    </div>

                    <div class="learning-item">
                        <div class="icon-wrapper">
                            <span class="icon">✏️</span>
                        </div>
                        <div class="content">
                            <h4>Hands-on Practice</h4>
                            <p>Interactive exercises to build your AI skills</p>
                        </div>
                    </div>

                    <div class="learning-item">
                        <div class="icon-wrapper">
                            <span class="icon">🚀</span>
                        </div>
                        <div class="content">
                            <h4>Future-Proof</h4>
                            <p>Expert insights on AI development and trends</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Social Proof -->
            <div class="author-section">
                <h2 class="author-title">The Author</h2>

                <div class="author-content">
                    <div class="author-image-container">
                        <img
                        src={CtHeroImage}
                        alt="Christopher Tavolazzi"
                        class="author-image"
                        />
                    </div>

                    <div class="author-text">
                        <p class="author-byline">
                            <span class="author-name">Christopher Tavolazzi</span>
                        </p>
                        <p class="author-description">
                            Software engineer and AI researcher making complex technology accessible.
                        </p>
                    </div>
                    <div class="credentials-list">
                        <a href="https://themultiverse.school" class="credential-item">
                            <span class="credential-icon">🎓</span>
                            <span class="credential-text">Professor at <span class="highlight-link">The Multiverse School</span></span>
                        </a>

                        <a href="https://solo.to/thecoffeejesus" class="credential-item">
                            <span class="credential-icon">🚀</span>
                            <span class="credential-text">Creator with <span class="highlight-link">100,000+ followers</span> across platforms</span>
                        </a>

                        <a href="https://thecoffeejesus.com" class="credential-item">
                            <span class="credential-icon">💻</span>
                            <span class="credential-text">Tech educator at <span class="highlight-link">thecoffeejesus.com</span></span>
                        </a>
                    </div>
                </div>
            </div>

            <!-- Call to Action -->
            <div class="preview-cta">
                <div class="launch-price">
                    <div class="price-info">
                        <span class="price-label">Limited time offer:</span>
                        <span class="price-amount">$9</span>
                    </div>
                    <p class="availability-note">Limited copies available at launch price</p>
                </div>
                <button
                    on:click={handlePreorder}
                    disabled={isLoading}
                    class="preorder-button"
                >
                    {#if isLoading}
                        <span class="loader"></span>
                    {:else}
                        PREORDER NOW & SAVE
                    {/if}
                </button>
            </div>
        </div>
    {/if}
</div>

<style>
    /* Base styles */
    .banner {
        --bg-color: #ffffff;
        --text-color: #1a1f2e;
        --border-color: #e5e7eb;
        --accent-color: #ff7708;
        --accent-hover: #ff8533;
        background-color: var(--bg-color);
        color: var(--text-color);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .banner.dark {
        --bg-color: #1a1f2e;
        --text-color: #ffffff;
        --border-color: rgba(255, 255, 255, 0.1);
        --accent-color: #ff9933;
        --accent-hover: #ffb366;
    }

    .banner-content {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .book-image {
        width: 160px;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease;
    }

    .book-image:hover {
        transform: scale(1.02);
    }

    .banner-text {
        flex-grow: 1;
    }

    .banner-text h2 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        line-height: 1.2;
    }

    .banner-text p {
        margin: 0 0 1rem 0;
        font-size: 1.15rem;
        line-height: 1.4;
        opacity: 0.9;
    }

    /* Button styles */
    .preorder-button {
        background: var(--accent-color);
        color: white;
        padding: 0.85rem 2rem;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 12px rgba(255, 119, 8, 0.2);
    }

    .preorder-button:hover {
        background: var(--accent-hover);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255, 119, 8, 0.3);
    }

    .preorder-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
        transform: none;
    }

    .expand-button {
        width: auto;
        margin: 1.25rem auto 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.6rem 1.25rem;
        background: rgba(255, 119, 8, 0.08);
        border: 1px solid rgba(255, 119, 8, 0.15);
        border-radius: 24px;
        color: var(--accent-color);
        cursor: pointer;
        font-size: 0.95rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .expand-button:hover {
        background: rgba(255, 119, 8, 0.12);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(255, 119, 8, 0.15);
    }

    .arrow {
        font-size: 0.85rem;
        transition: transform 0.3s ease;
        animation: subtle-bounce 2s infinite;
    }

    .arrow.rotated {
        transform: rotate(180deg);
        animation: none;
    }

    @keyframes subtle-bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(3px);
        }
    }

    /* Dark mode adjustments */
    .banner.dark .expand-button {
        background: rgba(255, 153, 51, 0.08);
        border-color: rgba(255, 153, 51, 0.15);
    }

    .banner.dark .expand-button:hover {
        background: rgba(255, 153, 51, 0.12);
        box-shadow: 0 2px 8px rgba(255, 153, 51, 0.15);
    }

    /* Expanded content */
    .expanded-content {
        margin-top: 0.75rem;
        padding-top: 0.75rem;
        border-top: 1px solid var(--border-color);
    }

    .learning-section {
        margin: 0.75rem 0;
    }

    .learning-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 0.75rem;
        padding: 0 0.25rem;
    }

    .learning-item {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.03);
        border-radius: 8px;
        transition: transform 0.3s ease;
    }

    .learning-item:hover {
        transform: translateY(-4px);
    }

    .icon-wrapper {
        background: linear-gradient(135deg, rgba(255, 138, 0, 0.2), rgba(255, 94, 3, 0.2));
        border-radius: 8px;
        padding: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .icon {
        font-size: 1.5rem;
    }

    .content h4 {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0 0 0.25rem 0;
        color: var(--text-color);
    }

    .content p {
        font-size: 0.95rem;
        line-height: 1.4;
        margin: 0;
        opacity: 0.9;
        color: var(--text-color);
    }

    /* Author section */
    .author-section {
        text-align: center;
        padding: 0.6rem 0;
    }

    .author-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.6rem;
    }

    .author-image-container {
        width: 140px;
        height: 140px;
        border-radius: 10px;
        overflow: hidden;
        margin: 0 auto;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }

    .author-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .author-text {
        margin: 0.4rem 0;
        text-align: center;
    }

    .author-name {
        color: var(--accent-color);
        font-weight: 600;
    }

    .credentials-list {
        gap: 0.4rem;
        margin-top: 0.2rem;
    }

    /* Price section */
    .preview-cta {
        margin-top: 1rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .launch-price {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        gap: 0.15rem;
        padding: 0.5rem 1rem;
        margin-bottom: 0.6rem;
        background: rgba(26, 31, 46, 0.7);
        border: 1px solid rgba(255, 153, 51, 0.3);
        border-radius: 16px;
        text-align: center;
        max-width: 380px;
    }

    .price-info {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
    }

    .price-label {
        font-size: 1.1rem;
        font-weight: 800;
        color: var(--accent-color);
    }

    .price-amount {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--accent-color);
    }

    .availability-note {
        color: var(--accent-color);
        font-size: 0.85rem;
        opacity: 0.9;
        margin-top: 0.25rem;
    }

    .preview-cta .preorder-button {
        min-width: 250px;
    }

    /* Light mode adjustments */
    .banner:not(.dark) .launch-price {
        background: rgba(0, 0, 0, 0.05);
        border-color: rgba(255, 119, 8, 0.2);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .banner {
            padding: 1rem;
        }

        .banner-content {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }

        .book-image {
            width: 150px;
        }

        .banner-text h2 {
            font-size: 1.6rem;
        }

        .banner-text p {
            font-size: 1.1rem;
        }

        .learning-grid {
            gap: 1rem;
        }

        .learning-item {
            padding: 0.75rem;
        }

        .author-image-container {
            width: 160px;
            height: 160px;
        }
    }

    @media (max-width: 480px) {
        .banner-text h2 {
            font-size: 1.4rem;
        }

        .book-image {
            width: 140px;
        }

        .learning-item {
            padding: 0.75rem;
        }
    }
</style>










































