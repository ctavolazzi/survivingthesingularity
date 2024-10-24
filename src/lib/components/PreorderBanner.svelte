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
                <!-- <p class="preorder-info">Limited copies at launch price!</p> -->
            </div>
        </div>
    </div>
    <button class="expand-button" on:click={toggleExpand}>
        {isExpanded ? 'Show Less' : 'Preview Book Contents'} 
        <span class="arrow" class:rotated={isExpanded}>▼</span>
    </button>

    {#if isExpanded}
        <div class="expanded-content" transition:slide="{{ duration: 300 }}">
            <p class="author-tagline">Empowering you to empower yourself.</p>
            
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
                <h2 class="author-title">About the Author</h2>
                
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
                            Written by <span class="author-name">Christopher Tavolazzi</span>,
                        </p>
                        <p class="author-description">
                            a software engineer and AI researcher making complex technology accessible.
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
    .banner {
        /* Light mode defaults */
        --bg-color: #ffffff;
        --text-color: #1a1f2e;
        --border-color: #e5e7eb;
        background-color: var(--bg-color);
        color: var(--text-color);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* Dark mode overrides */
    .banner.dark {
        --bg-color: #1a1f2e;
        --text-color: #ffffff;
        --border-color: rgba(255, 255, 255, 0.1);
    }

    .banner-content {
        display: flex;
        align-items: center;
        gap: 2.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .book-image {
        width: 140px;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    .banner-text {
        flex-grow: 1;
    }

    .banner-text h2 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: var(--text-color);
    }

    .banner-text p {
        font-size: 1.2rem;
        margin: 0 0 1rem 0;
        opacity: 0.9;
    }

    .cta-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .preorder-info {
        font-size: 0.9rem;
        color: #ff6b6b;
        font-weight: 600;
    }

    .expand-button {
        background: rgba(255, 153, 51, 0.1);
        border: 1px solid rgba(255, 153, 51, 0.2);
        color: #ff9933;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.4rem 0.8rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin: 0.75rem auto 0;
        transition: all 0.3s ease;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
    }

    .expand-button::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255, 153, 51, 0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }

    .expand-button:hover {
        color: #ffb366;
        text-shadow: 0 0 8px rgba(255, 153, 51, 0.3);
    }

    .expand-button:hover::after {
        transform: translateX(100%);
    }

    .arrow {
        font-size: 0.7rem;
        transition: transform 0.3s ease;
        opacity: 0.9;
    }

    .arrow.rotated {
        transform: rotate(180deg);
    }

    .expand-button:hover .arrow {
        transform: translateY(2px);
    }

    .expand-button:hover .arrow.rotated {
        transform: translateY(-2px) rotate(180deg);
    }

    .expanded-content {
        margin-top: 0.75rem; /* Reduced spacing */
        padding-top: 0.75rem; /* Reduced spacing */
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .preorder-button {
        width: 100%;
        background: linear-gradient(135deg, #ff8a00, #ff5e03);
        border: none;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.9rem 2rem;
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 94, 3, 0.2);
    }

    .preorder-button:hover {
        background: linear-gradient(135deg, #ff5e03, #ff8a00);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 94, 3, 0.3);
    }

    .preorder-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .loader {
        display: inline-block;
        width: 22px;
        height: 22px;
        border: 4px solid #ffffff;
        border-radius: 50%;
        border-top: 4px solid transparent;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @media (max-width: 768px) {
        .banner-content {
            flex-direction: column;
            text-align: center;
            gap: 1.5rem;
        }

        .cta-container {
            align-items: center;
        }

        .book-image {
            width: 180px;
        }

        .banner-text h2 {
            font-size: 1.8rem;
        }

        .banner-text p {
            font-size: 1.1rem;
        }
    }

    .learning-section {
        padding-top: 0.5rem; /* Reduced top padding */
    }

    .section-title {
        font-size: 2rem;
        text-align: center;
        margin: 0 0 1.25rem 0;
        position: relative;
        display: inline-block;
        width: 100%;
    }

    .title-highlight {
        background: linear-gradient(120deg, #ff9933 0%, #ff5e03 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: 0.5px;
        position: relative;
        display: inline-block;
        transition: transform 0.3s ease;
    }

    .title-highlight::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff9933, transparent);
        transform: scaleX(0.8);
        opacity: 0.7;
    }

    .learning-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem; /* Reduced gap */
        padding: 0 0.5rem; /* Reduced padding */
    }

    .learning-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem; /* Reduced padding */
        background: rgba(0, 0, 0, 0.03);
        border-radius: 8px; /* Slightly reduced border radius */
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .learning-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }

    .icon-wrapper {
        background: linear-gradient(135deg, rgba(255, 138, 0, 0.2), rgba(255, 94, 3, 0.2));
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .icon {
        font-size: 1.5rem;
    }

    .content {
        flex: 1;
    }

    .content h4 {
        color: var(--text-color);
        font-size: 1.2rem;
        margin: 0 0 0.25rem 0; /* Reduced margin bottom */
        font-weight: 600;
    }

    .content p {
        color: var(--text-color);
        opacity: 0.8;
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.4; /* Slightly reduced line height */
    }

    @media (max-width: 768px) {
        .learning-section {
            padding: 0.75rem 0; /* Even smaller padding on mobile */
        }

        .learning-grid {
            gap: 0.75rem; /* Reduced gap on mobile */
        }

        .section-title {
            font-size: 1.75rem;
            margin-bottom: 1rem;
        }

        .learning-item {
            padding: 0.5rem 0.75rem; /* Reduced padding further on mobile */
        }
    }

    .author-section {
        text-align: center;
        padding: 1rem 0.75rem;
    }

    .author-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: var(--text-color);
    }

    .author-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.25rem;
    }

    .author-image-container {
        width: 200px;
        height: 200px;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }

    .author-image-container:hover {
        transform: scale(1.02);
    }

    .author-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 16px;
    }

    .author-bio {
        font-size: 1.2rem;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
    }

    .author-name {
        color: #ff7708;
        font-weight: 700;
        font-size: 1.3rem;
        text-decoration: none;
        transition: color 0.3s ease;
    }

    .author-name:hover {
        color: #ffb366;
        text-decoration: underline;
    }

    .author-description {
        display: block;
        margin-top: 0.5rem;
        color: #4a5568;
    }

    .credentials-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        width: 100%;
        max-width: 600px;
    }

    .credential-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.6rem 1rem;
        background: rgba(0, 0, 0, 0.03);
        border-radius: 8px;
        text-decoration: none;
        color: inherit;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        text-align: left;
    }

    .credential-item::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            120deg,
            transparent,
            rgba(255, 153, 51, 0.1),
            transparent
        );
        transform: translateX(-100%);
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .credential-item:hover {
        transform: translateX(8px);
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .credential-item:hover::after {
        transform: translateX(100%);
    }

    .credential-icon {
        flex-shrink: 0;
        font-size: 1.3rem;
        transition: transform 0.3s ease;
    }

    .credential-item:hover .credential-icon {
        transform: scale(1.2);
    }

    .highlight-link {
        color: #ff9933;
        transition: color 0.3s ease;
    }

    .credential-item:hover .highlight-link {
        color: #ffb366;
    }

    @media (max-width: 768px) {
        .author-section {
            padding: 0.75rem 0.5rem;
        }

        .author-image-container {
            width: 180px;
            height: 180px;
        }

        .author-bio {
            font-size: 1.1rem;
            padding: 0 0.5rem;
        }

        .credential-item:hover {
            transform: translateY(-4px);
        }
    }

    .launch-price-container {
        margin-top: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
    }

    .launch-price-banner {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.8rem 1.2rem;
        background: rgba(40, 30, 25, 0.6);
        border-radius: 8px;
        width: fit-content;
    }

    .price-icon {
        font-size: 1.3rem;
    }

    .price-text {
        font-weight: 600;
        color: #ff9933;
        font-size: 1.1rem;
    }

    @media (max-width: 768px) {
        .author-section {
            padding: 0.75rem 0.5rem; /* Even smaller padding on mobile */
            margin: 0.75rem auto; /* Smaller margin on mobile */
        }

        .author-title {
            margin-bottom: 0.75rem;
        }
    }

    @media (max-width: 480px) {
        .author-title {
            font-size: 1.75rem;
        }

        .author-intro {
            font-size: 1.1rem;
        }

        .credential-item {
            font-size: 1rem;
            padding: 0.8rem;
        }
    }

    .launch-price {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.7rem 1.2rem 1.2rem 1.2rem;
        background: linear-gradient(
            to bottom,
            rgba(255, 255, 255, 0),
            rgba(0, 0, 0, 0.05) 80%,
            rgba(0, 0, 0, 0.08)
        );
        margin: 0.5rem auto 0 auto;
        max-width: 300px;
        text-align: center;
    }

    .launch-price span {
        font-size: 1rem;
        font-weight: 500;
        background: linear-gradient(135deg, #ffa533, #ff5e03);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.3px;
    }

    @media (max-width: 768px) {
        .launch-price {
            padding: 0.6rem 1rem 1rem 1rem;
            margin: 0.5rem auto 0 auto;
        }
        
        .launch-price span {
            font-size: 0.95rem;
        }
    }

    .fire-icon {
        font-size: 1.4rem;
        animation: flicker 1.5s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        50% {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(255, 94, 3, 0.15);
        }
    }

    @keyframes flicker {
        0%, 100% {
            opacity: 1;
            transform: rotate(-5deg) scale(1);
        }
        50% {
            opacity: 0.8;
            transform: rotate(5deg) scale(1.1);
        }
    }

    .launch-price span:not(.fire-icon) {
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        background: linear-gradient(135deg, #ffa533, #ff5e03);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(255, 153, 51, 0.2);
    }

    @media (max-width: 768px) {
        .launch-price {
            padding: 0.6rem 1rem;
            margin: 0.75rem auto;
        }
        
        .fire-icon {
            font-size: 1.2rem;
        }
        
        .launch-price span:not(.fire-icon) {
            font-size: 1rem;
        }
    }

    /* If there's a container wrapping all these elements */
    .author-container {
        padding: 0.75rem; /* Reduced outer padding */
    }

    .author-text {
        text-align: center;
        margin: 0.5rem 0;
    }

    .author-tagline {
        font-size: 2rem;
        background: linear-gradient(135deg, #ffa533 0%, #ff5e03 50%, #ffc107 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1.5rem auto 3rem auto;
        font-weight: 800;
        font-style: italic;
        text-align: center;
        letter-spacing: 1.5px;
        position: relative;
        padding: 1.5rem 0;
        text-shadow: 0 2px 20px rgba(255, 153, 51, 0.3);
        max-width: 800px;
        animation: float 6s ease-in-out infinite;
        transform-style: preserve-3d;
        perspective: 1000px;
    }

    .author-tagline::before {
        content: '✨';
        position: absolute;
        left: 50%;
        top: -12px;
        transform: translateX(-50%);
        font-size: 1.4rem;
        opacity: 0.9;
        animation: sparkleFloat 3s ease-in-out infinite;
        filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.8));
    }

    .author-tagline::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 280px;
        height: 4px;
        background: linear-gradient(90deg, 
            transparent,
            rgba(255, 153, 51, 0.2),
            rgba(255, 153, 51, 0.8), 
            #ff9933,
            rgba(255, 153, 51, 0.8),
            rgba(255, 153, 51, 0.2),
            transparent
        );
        box-shadow: 
            0 2px 12px rgba(255, 153, 51, 0.4),
            0 4px 24px rgba(255, 94, 3, 0.2);
        animation: shineAndPulse 4s ease-in-out infinite;
        border-radius: 2px;
    }

    @keyframes float {
        0%, 100% {
            transform: translateY(0) rotateX(5deg);
            letter-spacing: 1.5px;
        }
        50% {
            transform: translateY(-8px) rotateX(5deg);
            letter-spacing: 2px;
        }
    }

    @keyframes sparkleFloat {
        0%, 100% {
            transform: translate(-50%, 0) rotate(0deg) scale(1);
            opacity: 0.9;
        }
        50% {
            transform: translate(-50%, -5px) rotate(180deg) scale(1.3);
            opacity: 1;
        }
    }

    @keyframes shineAndPulse {
        0%, 100% {
            width: 240px;
            opacity: 0.8;
            filter: blur(0px);
            transform: translateX(-50%) scaleX(0.9);
        }
        50% {
            width: 280px;
            opacity: 1;
            filter: blur(0.5px);
            transform: translateX(-50%) scaleX(1);
        }
    }

    /* Add a pseudo-element for the glow effect */
    .author-tagline::before {
        content: attr(data-text);
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        filter: blur(8px);
        opacity: 0.3;
        animation: glowPulse 4s ease-in-out infinite;
        z-index: -1;
    }

    @keyframes glowPulse {
        0%, 100% {
            filter: blur(8px);
            opacity: 0.3;
        }
        50% {
            filter: blur(12px);
            opacity: 0.5;
        }
    }

    @media (max-width: 768px) {
        .author-tagline {
            font-size: 1.5rem;
            margin: 1rem auto 2.5rem auto;
            letter-spacing: 1px;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotateX(3deg);
                letter-spacing: 1px;
            }
            50% {
                transform: translateY(-5px) rotateX(3deg);
                letter-spacing: 1.5px;
            }
        }
    }

    .preview-cta {
        margin-top: 2rem;
        text-align: center;
    }

    .launch-price {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.25rem;
        padding: 0.5rem 1.25rem;
        border-radius: 20px;
        background: rgba(255, 119, 8, 0.08);
        border: 1px solid rgba(255, 119, 8, 0.15);
    }

    .price-label {
        font-size: 0.95rem;
        font-weight: 500;
        color: #4a5568;
        letter-spacing: 0.02em;
    }

    .price-amount {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ff7708;
        letter-spacing: 0.02em;
    }

    /* Dark mode adjustments */
    .banner.dark .launch-price {
        background: rgba(255, 153, 51, 0.1);
        border-color: rgba(255, 153, 51, 0.2);
    }

    .banner.dark .price-label {
        color: #e2e8f0;
    }

    .banner.dark .price-amount {
        color: #ff9933;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .preview-cta {
            margin-top: 1.5rem;
        }
        
        .launch-price {
            padding: 0.4rem 1rem;
        }

        .price-label {
            font-size: 0.9rem;
        }

        .price-amount {
            font-size: 1rem;
        }
    }

    /* Author styles */
    .author-byline {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #e2e8f0;
    }

    .author-name {
        color: #ff9933;
        font-weight: 600;
    }

    .author-description {
        color: #cbd5e0;
    }

    /* Launch price styles */
    .launch-price {
        margin-bottom: 1.25rem;
        text-align: center;
    }

    .price-info {
        margin-bottom: 0.5rem;
    }

    .price-label {
        font-size: 0.95rem;
        font-weight: 500;
        color: #4a5568;
    }

    .price-amount {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ff7708;
        margin-left: 0.5rem;
    }

    .availability-note {
        font-size: 0.85rem;
        color: #ff7708;
        font-weight: 500;
        opacity: 0.9;
    }

    /* Dark mode adjustments */
    .banner.dark .author-byline {
        color: #e2e8f0;
    }

    .banner.dark .author-description {
        color: #cbd5e0;
    }

    .banner.dark .price-label {
        color: #e2e8f0;
    }

    .banner.dark .price-amount,
    .banner.dark .availability-note {
        color: #ff9933;
    }

    .launch-price {
        background: rgba(26, 31, 46, 0.7);
        border: 1px solid rgba(255, 153, 51, 0.3);
        border-radius: 24px;
        padding: 0.75rem 1.5rem;
        margin-bottom: 1rem;
        display: inline-flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .price-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .price-label {
        color: #ff9933;
        font-size: 0.95rem;
        font-weight: 500;
    }

    .price-amount {
        color: #ff9933;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .availability-note {
        color: #ff9933;
        opacity: 0.8;
        font-size: 0.85rem;
    }

    /* Light mode adjustments */
    .banner:not(.dark) .launch-price {
        background: rgba(0, 0, 0, 0.05);
        border-color: rgba(255, 119, 8, 0.2);
    }

    .banner:not(.dark) .price-label,
    .banner:not(.dark) .price-amount,
    .banner:not(.dark) .availability-note {
        color: #ff7708;
    }

    .author-text {
        text-align: center;
        margin: 1rem 0;
    }

    .author-byline {
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
        color: #1a1f2e;  /* Dark text for light mode */
    }

    .author-name {
        color: #ff7708;  /* Warm orange that works in both modes */
        font-weight: 600;
    }

    .author-description {
        font-size: 1rem;
        line-height: 1.5;
        color: #4a5568;  /* Medium gray for light mode */
    }

    /* Dark mode overrides */
    .banner.dark .author-byline {
        color: #e2e8f0;
    }

    .banner.dark .author-description {
        color: #cbd5e0;
    }

    .banner.dark .author-name {
        color: #ff9933;  /* Slightly lighter orange for dark mode */
    }
</style>










































