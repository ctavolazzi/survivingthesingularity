<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import { browser } from '$app/environment';
  import bookCoverImage from '$lib/images/Surviving-the-Singularity-Cover.png';

  // Props
  export let title = "Prepare for the Future";
  export let description = "Discover the strategies and insights you need to navigate the approaching technological singularity.";
  export let buttonText = "Get the Book";
  export let buttonLink = "/book";
  export let imageSrc = bookCoverImage; // Use the imported image

  let visible = false;
  let shareMenuOpen = false;
  let copySuccess = false;
  let bookCalloutElement;
  let shareButtonElement;
  let shareMenuElement;
  let isProcessingClick = false;
  let lastClickTime = 0;

  // Enhanced Share functionality with debouncing
  function shareBook(event) {
    // Prevent multiple rapid clicks
    const now = Date.now();
    if (now - lastClickTime < 500 || isProcessingClick) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    isProcessingClick = true;
    lastClickTime = now;

    // Use setTimeout to ensure UI doesn't freeze
    setTimeout(() => {
      try {
        if (navigator && navigator.share) {
          // Use the Web Share API for devices that support it
          navigator.share({
            title: 'Surviving the Singularity',
            text: 'Check out this book about navigating the technological singularity!',
            url: window.location.origin + buttonLink,
          })
          .catch(() => {
            // Fallback to our custom menu if sharing fails
            shareMenuOpen = true;
          })
          .finally(() => {
            isProcessingClick = false;
          });
        } else {
          // Fallback for browsers that don't support navigator.share
          shareMenuOpen = !shareMenuOpen;
          isProcessingClick = false;
        }
      } catch (error) {
        console.log('Share error:', error);
        shareMenuOpen = true;
        isProcessingClick = false;
      }
    }, 10);
  }

  // All sharing functions with improved debounce protection
  function performShare(callback) {
    return (event) => {
      // Prevent multiple rapid clicks
      const now = Date.now();
      if (now - lastClickTime < 500 || isProcessingClick) {
        event.preventDefault();
        event.stopPropagation();
        return;
      }

      isProcessingClick = true;
      lastClickTime = now;

      try {
        callback();
      } catch (error) {
        console.error('Share error:', error);
      } finally {
        // Always reset flags after a delay to prevent UI freeze
        setTimeout(() => {
          isProcessingClick = false;
        }, 200);
      }
    };
  }

  // Clipboard function with improved handler
  const copyToClipboard = performShare(() => {
    const url = window.location.origin + buttonLink;
    navigator.clipboard.writeText(url)
      .then(() => {
        copySuccess = true;
        setTimeout(() => {
          copySuccess = false;
          shareMenuOpen = false;
        }, 2000);
      })
      .catch(err => {
        console.error('Could not copy text: ', err);
        isProcessingClick = false;
      });
  });

  // Wrapped share functions with debounce protection
  const shareViaEmail = performShare(() => {
    const subject = encodeURIComponent('Surviving the Singularity - Book Recommendation');
    const body = encodeURIComponent(
      `Check out this book about navigating the technological singularity!\n\n` +
      `Surviving the Singularity will help you prepare for the rapid technological changes ahead.\n\n` +
      `Learn more at: ${window.location.origin + buttonLink}`
    );
    window.open(`mailto:?subject=${subject}&body=${body}`, '_blank');
    shareMenuOpen = false;
  });

  const shareViaWhatsApp = performShare(() => {
    const text = encodeURIComponent(`Check out this book about navigating the technological singularity! ${window.location.origin + buttonLink}`);
    window.open(`https://wa.me/?text=${text}`, '_blank');
    shareMenuOpen = false;
  });

  const shareViaSMS = performShare(() => {
    const text = encodeURIComponent(`Check out Surviving the Singularity: ${window.location.origin + buttonLink}`);
    window.open(`sms:?&body=${text}`, '_blank');
    shareMenuOpen = false;
  });

  const shareViaFacebook = performShare(() => {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.origin + buttonLink)}`, '_blank');
    shareMenuOpen = false;
  });

  const shareViaSocialMedia = (platform) => performShare(() => {
    let url = '';

    if (platform === 'twitter') {
      url = `https://twitter.com/intent/tweet?text=Check out this book about navigating the technological singularity!&url=${encodeURIComponent(window.location.origin + buttonLink)}`;
    } else if (platform === 'linkedin') {
      url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.origin + buttonLink)}`;
    }

    if (url) {
      window.open(url, '_blank');
      shareMenuOpen = false;
    }
  })();

  onMount(() => {
    // Don't run on the server - stronger protection
    if (typeof window === 'undefined' || typeof document === 'undefined' || !browser) return;

    // Check if element is in viewport using the bound reference
    if (bookCalloutElement) {
      const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
          visible = true;
          observer.disconnect();
        }
      }, { threshold: 0.2 });

      observer.observe(bookCalloutElement);
    }

    // Improved click outside handler with direct element references
    const handleClickOutside = (event) => {
      if (!shareMenuOpen) return;

      if (shareMenuElement && shareButtonElement &&
          !shareMenuElement.contains(event.target) &&
          !shareButtonElement.contains(event.target)) {
        shareMenuOpen = false;
      }
    };

    // Make sure we're in the browser before adding event listeners
    if (typeof document !== 'undefined') {
      document.addEventListener('click', handleClickOutside);

      return () => {
        document.removeEventListener('click', handleClickOutside);
      };
    }
  });
</script>

<div bind:this={bookCalloutElement} class="book-callout p-5 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 shadow-2xl rounded-lg max-w-3xl mx-auto my-2 border border-gray-700/50 backdrop-blur-sm">
  {#if visible}
    <div class="flex flex-col md:flex-row gap-6" in:fade={{ duration: 800 }}>
      <!-- Book cover image with enhanced glow effect -->
      <div class="flex-shrink-0 relative" in:fly={{ y: 20, duration: 800, delay: 200 }}>
        <div class="absolute inset-0 bg-blue-500/30 opacity-30 blur-2xl rounded-full"></div>
        <img src={imageSrc} alt="Book cover" class="w-40 md:w-48 h-auto rounded-md shadow-[0_10px_25px_rgba(59,130,246,0.3)] mx-auto md:mx-0 relative z-10 transform transition-all duration-500 hover:scale-105 hover:shadow-[0_15px_30px_rgba(59,130,246,0.4)]" />
      </div>

      <!-- Content with improved typography and spacing -->
      <div class="flex flex-col justify-center">
        <h2 class="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-blue-100 mb-3 tracking-wide" in:fly={{ y: 20, duration: 800, delay: 300 }}>
          {title}
        </h2>
        <p class="text-gray-300 mb-5 text-base md:text-lg leading-relaxed" in:fly={{ y: 20, duration: 800, delay: 400 }}>
          {description}
        </p>

        <!-- Enhanced features list with animated entry -->
        <div class="grid grid-cols-1 gap-3 mb-6" in:fly={{ y: 20, duration: 800, delay: 500 }}>
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            <span class="text-gray-300">Learn to navigate rapid technological changes</span>
          </div>
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            <span class="text-gray-300">Understand AI's impact on your career & future</span>
          </div>
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            <span class="text-gray-300">Actionable strategies to thrive in the new era</span>
          </div>
        </div>

        <!-- Action buttons with enhanced styling -->
        <div class="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4" in:fly={{ y: 20, duration: 800, delay: 600 }}>
          <!-- Main CTA Button -->
          <a href={buttonLink} class="inline-flex items-center px-6 py-3 text-base font-medium text-center text-white bg-gradient-to-r from-blue-600 via-blue-500 to-blue-600 rounded-lg hover:from-blue-500 hover:via-blue-400 hover:to-blue-500 focus:ring-4 focus:outline-none focus:ring-blue-300 shadow-lg shadow-blue-500/30 transition-all duration-300 hover:shadow-blue-500/50 hover:translate-y-[-2px] relative overflow-hidden group">
            <span class="relative z-10">{buttonText}</span>
            <svg class="w-5 h-5 ml-2 relative z-10 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
            <span class="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-blue-400 to-blue-300 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></span>
          </a>

          <!-- Share button with direct element binding -->
          <div class="relative">
            <button
              bind:this={shareButtonElement}
              class="share-button inline-flex items-center px-5 py-3 text-base font-medium text-center text-white bg-gradient-to-r from-purple-600 via-purple-500 to-purple-600 rounded-lg hover:from-purple-500 hover:via-purple-400 hover:to-purple-500 focus:ring-4 focus:outline-none focus:ring-purple-300 shadow-lg shadow-purple-500/30 transition-all duration-300 hover:shadow-purple-500/50 hover:translate-y-[-2px] relative overflow-hidden group"
              on:click={shareBook}
              aria-label="Share this book"
            >
              <span class="relative z-10 flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
                </svg>
                Share
              </span>
              <span class="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-purple-400 to-purple-300 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></span>
            </button>

            <!-- Enhanced Share menu dropdown with direct element binding -->
            {#if shareMenuOpen}
              <div
                bind:this={shareMenuElement}
                class="share-menu absolute right-0 mt-2 w-64 bg-gray-800 rounded-md shadow-lg z-20 border border-gray-700 overflow-hidden"
                in:scale={{ duration: 200, start: 0.95, opacity: 0 }}
              >
                <div class="py-1">
                  <!-- Social Media Sharing -->
                  <div class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-gray-700">
                    Social Media
                  </div>

                  <button
                    class="w-full text-left px-4 py-2 text-sm text-gray-200 hover:bg-gray-700 flex items-center"
                    on:click={shareViaSocialMedia('twitter')}
                  >
                    <svg class="w-4 h-4 mr-3 text-blue-400" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                    </svg>
                    Twitter
                  </button>

                  <button
                    class="w-full text-left px-4 py-2 text-sm text-gray-200 hover:bg-gray-700 flex items-center"
                    on:click={shareViaSocialMedia('linkedin')}
                  >
                    <svg class="w-4 h-4 mr-3 text-blue-600" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                    LinkedIn
                  </button>

                  <button
                    class="w-full text-left px-4 py-2 text-sm text-gray-200 hover:bg-gray-700 flex items-center"
                    on:click={shareViaFacebook}
                  >
                    <svg class="w-4 h-4 mr-3 text-blue-500" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1v2h3v3h-3v6.95c5.05-.5 9-4.76 9-9.95z"/>
                    </svg>
                    Facebook
                  </button>

                  <!-- Messaging -->
                  <div class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-gray-700 mt-1">
                    Messaging
                  </div>

                  <button
                    class="w-full text-left px-4 py-2 text-sm text-gray-200 hover:bg-gray-700 flex items-center"
                    on:click={shareViaWhatsApp}
                  >
                    <svg class="w-4 h-4 mr-3 text-green-500" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                    </svg>
                    WhatsApp
                  </button>

                  <button
                    class="w-full text-left px-4 py-2 text-sm text-gray-200 hover:bg-gray-700 flex items-center"
                    on:click={shareViaSMS}
                  >
                    <svg class="w-4 h-4 mr-3 text-yellow-500" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/>
                    </svg>
                    SMS
                  </button>

                  <button
                    class="w-full text-left px-4 py-2 text-sm text-gray-200 hover:bg-gray-700 flex items-center"
                    on:click={shareViaEmail}
                  >
                    <svg class="w-4 h-4 mr-3 text-red-400" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-.4 4.25l-7.07 4.42c-.32.2-.74.2-1.06 0L4.4 8.25c-.25-.16-.4-.43-.4-.72 0-.67.73-1.07 1.3-.72L12 11l6.7-4.19c.57-.35 1.3.05 1.3.72 0 .29-.15.56-.4.72z"/>
                    </svg>
                    Email
                  </button>

                  <!-- Copy Link -->
                  <div class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-gray-700 mt-1">
                    Other
                  </div>

                  <button
                    class="w-full text-left px-4 py-2 text-sm text-gray-200 hover:bg-gray-700 flex items-center relative overflow-hidden"
                    on:click={copyToClipboard}
                  >
                    {#if copySuccess}
                      <svg class="w-4 h-4 mr-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                      <span>Copied!</span>
                    {:else}
                      <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
                      </svg>
                      <span>Copy link</span>
                    {/if}
                  </button>
                </div>
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .book-callout {
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 30px rgba(59, 130, 246, 0.15) inset;
  }

  .book-callout::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, rgba(17, 24, 39, 0) 70%);
    z-index: 0;
    animation: pulse 8s ease-in-out infinite alternate;
  }

  .book-callout::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, transparent 50%, rgba(20, 184, 166, 0.1) 100%);
    z-index: 0;
    opacity: 0.5;
  }

  @keyframes pulse {
    0% {
      opacity: 0.3;
      transform: translate(-50%, -50%) scale(1);
    }
    100% {
      opacity: 0.5;
      transform: translate(-50%, -50%) scale(1.2);
    }
  }

  /* Share menu styling */
  .share-menu {
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  }

  /* Mobile optimization */
  @media (max-width: 768px) {
    .book-callout {
      padding: 1.5rem;
      margin: 1rem 0;
    }
  }
</style>