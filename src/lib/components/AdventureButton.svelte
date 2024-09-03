<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  function handleClick() {
    dispatch('click');
  }
</script>

<button class="adventure-button" on:click={handleClick}>
  <slot>Begin the Adventure</slot>
</button>

<style>
  .adventure-button {
    background: linear-gradient(135deg, #ff9933, #ff8000);
    color: #ffffff;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 0.25rem;
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .adventure-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
  }

  :global(.dark) .adventure-button {
    background: linear-gradient(135deg, #ff9933, #ff7708);
    color: #1a202c;
  }

  :global(.dark) .adventure-button:hover {
    box-shadow: 0 6px 8px rgba(255, 153, 51, 0.3);
  }
</style>
