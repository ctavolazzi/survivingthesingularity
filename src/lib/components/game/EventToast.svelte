<script>
  // In-game toast stack (events, achievements, stage completions).
  // Separate from the site-wide toast store so game noise never leaks out.
  export let toasts = [];
</script>

<div class="toast-stack" aria-live="polite">
  {#each toasts as t (t.id)}
    <div class="toast toast-{t.kind}">
      <div class="toast-title">{t.title}</div>
      {#if t.msg}<div class="toast-msg">{t.msg}</div>{/if}
      {#if t.link}
        <a class="toast-link" href={t.link.href} target="_blank" rel="noopener">{t.link.label} →</a>
      {/if}
    </div>
  {/each}
</div>

<style>
  .toast-stack {
    position: absolute;
    top: 3.8rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    z-index: 15;
    pointer-events: none;
    width: min(420px, calc(100% - 2rem));
  }
  .toast {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.3);
    border-left: 3px solid #3b82f6;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    backdrop-filter: blur(6px);
    pointer-events: auto;
    animation: slide-in 0.25s ease-out;
  }
  .toast-event {
    border-left-color: #ef4444;
  }
  .toast-achievement {
    border-left-color: #f59e0b;
  }
  .toast-stage {
    border-left-color: #10b981;
  }
  .toast-title {
    font-weight: 700;
    font-size: 0.88rem;
    color: #f1f5f9;
  }
  .toast-msg {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 0.15rem;
    line-height: 1.4;
  }
  .toast-link {
    display: inline-block;
    margin-top: 0.3rem;
    font-size: 0.74rem;
    color: #60a5fa;
    text-decoration: none;
  }
  .toast-link:hover {
    text-decoration: underline;
  }
  @keyframes slide-in {
    from {
      opacity: 0;
      transform: translateY(-8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
