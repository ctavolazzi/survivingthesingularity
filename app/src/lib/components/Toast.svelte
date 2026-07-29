<script>
  import { toast } from '$lib/toast.svelte.js';
</script>

<div class="toast" class:is-on={toast.visible} role="status" aria-live="polite">
  {toast.message}
</div>

<style>
  .toast {
    position: fixed;
    left: 50%;
    bottom: 28px;
    transform: translate(-50%, 16px);
    background: var(--surface-3);
    border: 1px solid var(--border-2);
    border-radius: var(--r);
    padding: 13px 20px;
    font: 500 14.5px/1.45 var(--sans);
    color: var(--text);
    max-width: min(520px, calc(100vw - 40px));
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55);
    opacity: 0;
    visibility: hidden;
    transition: opacity 200ms ease, transform 200ms ease, visibility 200ms;
    z-index: 100;
    text-align: center;
  }
  .toast.is-on {
    opacity: 1;
    visibility: visible;
    transform: translate(-50%, 0);
  }

  @media (prefers-reduced-motion: reduce) {
    .toast { transition: none; transform: translate(-50%, 0); }
  }
</style>
