<script>
  // The Discord invite link
  const discordInvite = 'https://discord.gg/xU6DQyGTnS';
</script>

<div class="discord-button-container">
  <a href="/discord" class="discord-button">
    <div class="discord-icon-wrapper">
      <svg class="discord-icon" viewBox="0 -28.5 256 256" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid">
        <path d="M216.856339,16.5966031 C200.285002,8.84328665 182.566144,3.2084988 164.041564,0 C161.766523,4.11318106 159.108624,9.64549908 157.276099,14.0464379 C137.583995,11.0849896 118.072967,11.0849896 98.7430163,14.0464379 C96.9108417,9.64549908 94.1925838,4.11318106 91.8971895,0 C73.3526068,3.2084988 55.6133949,8.86399117 39.0420583,16.6376612 C5.61752293,67.146514 -3.4433191,116.400813 1.08711069,164.955721 C23.2560196,181.510915 44.7403634,191.567697 65.8621325,198.148576 C71.0772151,190.971126 75.7283628,183.341335 79.7352139,175.300261 C72.104019,172.400575 64.7949724,168.822202 57.8887866,164.667963 C59.7209612,163.310589 61.5131304,161.891452 63.2445898,160.431257 C105.36741,180.133187 151.134928,180.133187 192.754523,160.431257 C194.506336,161.891452 196.298154,163.310589 198.110326,164.667963 C191.183787,168.842556 183.854737,172.420929 176.223542,175.320965 C180.230393,183.341335 184.861538,190.991831 190.096624,198.16893 C211.238746,191.588051 232.743023,181.531619 254.911949,164.955721 C260.227747,108.668201 245.831087,59.8662432 216.856339,16.5966031 Z" fill="currentColor"></path>
      </svg>
    </div>
    <span>Join the Discord</span>
    <div class="first-100-badge">First 100 only</div>
  </a>
  <p class="discord-tagline">Connect with others preparing for the singularity.</p>
</div>

<style>
  .discord-button-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin: 1.5rem auto;
    width: 100%;
    max-width: 400px;
  }

  .discord-button {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #5865F2;
    color: white;
    font-weight: bold;
    padding: 0.75rem 2rem;
    border-radius: 8px;
    text-decoration: none;
    font-size: 1.1rem;
    transition: all 0.2s ease;
    width: 100%;
    box-shadow: 0 4px 12px rgba(88, 101, 242, 0.3);
    overflow: visible;
  }

  .discord-button:hover {
    background-color: #4752c4;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(88, 101, 242, 0.4);
  }

  .discord-icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
  }

  .discord-icon {
    width: 24px;
    height: 24px;
  }

  .first-100-badge {
    position: absolute;
    top: -10px;
    right: -10px;
    background: #FF1F8E;
    color: white;
    font-size: 0.7rem;
    font-weight: bold;
    padding: 3px 8px;
    border-radius: 12px;
    transform: rotate(5deg);
    box-shadow: 0 2px 6px rgba(255, 31, 142, 0.5);
    z-index: 2;
  }

  .discord-tagline {
    margin-top: 0.75rem;
    color: var(--color-text-secondary, #adb5bd);
    font-size: 0.9rem;
  }

  /* Make sure it adapts to the page styling */
  :global(.dark) .discord-tagline {
    color: var(--color-text-secondary-dark, #adb5bd);
  }
</style>