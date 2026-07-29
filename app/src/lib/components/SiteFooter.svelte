<footer class="site-foot">
  <div class="wrap foot-inner">
    <p class="foot-c">Surviving the Singularity. Operated by Johnny Autoseed LLC.</p>
    <nav class="foot-nav" aria-label="Legal">
      <a href="/policies">Policies</a>
      <a href="/policies#refunds">Refunds</a>
      <a href="/policies#terms">Terms</a>
    </nav>
  </div>
</footer>

<style>
  .site-foot {
    border-top: 1px solid var(--border);
    padding: 32px 0;
    background: var(--surface);
  }
  .foot-inner {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    align-items: center;
    justify-content: space-between;
  }
  .foot-c { margin: 0; font-size: 14px; color: var(--text-3); }
  .foot-nav { display: flex; gap: 20px; flex-wrap: wrap; }
  .foot-nav a { color: var(--text-3); font-size: 14px; text-decoration: none; }
  .foot-nav a:hover { color: var(--text-2); }

  @media (max-width: 700px) {
    .foot-inner { flex-direction: column; align-items: flex-start; }
  }
</style>
