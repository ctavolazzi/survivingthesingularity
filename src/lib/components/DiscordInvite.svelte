<script>
  import { fade, scale, fly, blur } from 'svelte/transition';
  import { onMount } from 'svelte';

  // Using actual Discord invite link
  const discordInvite = 'https://discord.gg/xU6DQyGTnS';

  let cardElement;

  function openDiscord() {
    window.open(discordInvite, '_blank');
  }

  onMount(() => {
    // Initial subtle fade-in animation
    if (cardElement) {
      setTimeout(() => {
        cardElement.classList.add('loaded');
      }, 500);
    }
  });
</script>

<style>
  .invite-container {
    width: 100%;
    max-width: 450px;
    margin: 0 auto;
  }

  .invite-card {
    position: relative;
    background-color: #1a1f2d;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    transition: all 0.3s ease-in-out;
  }

  .invite-card.loaded {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  }

  .invite-card:hover {
    box-shadow: 0 12px 40px rgba(88, 101, 242, 0.2);
    transform: translateY(-5px);
  }

  .title {
    font-size: 1.75rem;
    font-weight: bold;
    color: white;
    margin: 0 0 1rem 0;
  }

  .subtitle {
    color: #adb5bd;
    font-size: 1rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
  }

  .discord-logo {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.25rem;
    filter: drop-shadow(0 0 8px rgba(88, 101, 242, 0.3));
    animation: float 5s ease-in-out infinite;
  }

  @keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-7px); }
    100% { transform: translateY(0px); }
  }

  .btn {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #5865F2;
    color: white;
    font-weight: bold;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    text-decoration: none;
    font-size: 1.1rem;
    transition: all 0.2s ease;
    width: 100%;
    max-width: 300px;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .btn:hover {
    background-color: #4752c4;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(88, 101, 242, 0.3);
  }

  .btn-icon {
    width: 20px;
    height: 20px;
  }

  .btns-container {
    display: flex;
    gap: 1rem;
    width: 100%;
    max-width: 400px;
    justify-content: center;
    flex-wrap: wrap;
  }

  .discord-direct-link {
    flex: 1;
    min-width: 180px;
  }

  .copy-btn {
    flex: 1;
    min-width: 180px;
    background-color: transparent;
    border: 1px solid #5865F2;
    color: #5865F2;
  }

  .copy-btn:hover {
    background-color: rgba(88, 101, 242, 0.1);
  }

  .copied-text {
    color: #5cdb95;
    font-size: 0.9rem;
    margin-top: 0.75rem;
    font-weight: 500;
  }

  .member-count {
    color: #6c757d;
    font-size: 0.85rem;
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    width: 100%;
  }

  .member-highlight {
    color: #5865F2;
    font-weight: 600;
  }

  .limited-badge {
    position: absolute;
    top: -12px;
    right: -12px;
    background: #FF1F8E;
    color: white;
    font-size: 0.8rem;
    font-weight: bold;
    padding: 5px 10px;
    border-radius: 15px;
    transform: rotate(5deg);
    box-shadow: 0 2px 6px rgba(255, 31, 142, 0.5);
    z-index: 2;
  }

  .privacy-text {
    color: #6c757d;
    font-size: 0.8rem;
    margin-top: 1rem;
  }

  @media (max-width: 480px) {
    .invite-card {
      padding: 1.5rem;
    }

    .title {
      font-size: 1.5rem;
    }

    .discord-logo {
      width: 60px;
      height: 60px;
    }
  }
</style>

<div class="invite-container">
  <div
    class="invite-card"
    in:fade={{ duration: 600 }}
    bind:this={cardElement}
  >
    <div class="limited-badge" in:scale={{ delay: 200 }}>First 100 only!</div>

    <div in:scale={{ delay: 300, duration: 500 }}>
      <svg class="discord-logo" viewBox="0 -28.5 256 256" version="1.1" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid">
        <g>
          <path d="M216.856339,16.5966031 C200.285002,8.84328665 182.566144,3.2084988 164.041564,0 C161.766523,4.11318106 159.108624,9.64549908 157.276099,14.0464379 C137.583995,11.0849896 118.072967,11.0849896 98.7430163,14.0464379 C96.9108417,9.64549908 94.1925838,4.11318106 91.8971895,0 C73.3526068,3.2084988 55.6133949,8.86399117 39.0420583,16.6376612 C5.61752293,67.146514 -3.4433191,116.400813 1.08711069,164.955721 C23.2560196,181.510915 44.7403634,191.567697 65.8621325,198.148576 C71.0772151,190.971126 75.7283628,183.341335 79.7352139,175.300261 C72.104019,172.400575 64.7949724,168.822202 57.8887866,164.667963 C59.7209612,163.310589 61.5131304,161.891452 63.2445898,160.431257 C105.36741,180.133187 151.134928,180.133187 192.754523,160.431257 C194.506336,161.891452 196.298154,163.310589 198.110326,164.667963 C191.183787,168.842556 183.854737,172.420929 176.223542,175.320965 C180.230393,183.341335 184.861538,190.991831 190.096624,198.16893 C211.238746,191.588051 232.743023,181.531619 254.911949,164.955721 C260.227747,108.668201 245.831087,59.8662432 216.856339,16.5966031 Z M85.4738752,135.09489 C72.8290281,135.09489 62.4592217,123.290155 62.4592217,108.914901 C62.4592217,94.5396472 72.607595,82.7145587 85.4738752,82.7145587 C98.3405064,82.7145587 108.709962,94.5189427 108.488529,108.914901 C108.508531,123.290155 98.3405064,135.09489 85.4738752,135.09489 Z M170.525237,135.09489 C157.88039,135.09489 147.510584,123.290155 147.510584,108.914901 C147.510584,94.5396472 157.658606,82.7145587 170.525237,82.7145587 C183.391518,82.7145587 193.761324,94.5189427 193.539891,108.914901 C193.539891,123.290155 183.391518,135.09489 170.525237,135.09489 Z" fill="#5865F2" fill-rule="nonzero">
          </path>
        </g>
      </svg>
    </div>

    <h2 class="title" in:fade={{ y: -5, duration: 500, delay: 200 }}>Join our Discord community</h2>
    <p class="subtitle" in:fade={{ duration: 500, delay: 300 }}>
      Connect with others preparing for the technological singularity. Share insights and strategies.
    </p>

    <a href={discordInvite} target="_blank" rel="noopener noreferrer" class="btn" in:fade={{ duration: 400, delay: 500 }}>
      <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
        <polyline points="10 17 15 12 10 7"></polyline>
        <line x1="15" y1="12" x2="3" y2="12"></line>
      </svg>
      Join the Discord
    </a>

    <div class="member-count" in:fade={{ delay: 600 }}>
      <span class="member-highlight">Join the movement</span> - Prepare for what's coming
    </div>

    <p class="privacy-text" in:fade={{ delay: 700 }}>We maintain a respectful and focused community environment.</p>
  </div>
</div>