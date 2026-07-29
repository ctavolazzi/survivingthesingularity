<script>
  import '../app.css';
  import Header from '$lib/components/Header.svelte';
  import SiteFooter from '$lib/components/SiteFooter.svelte';
  import Toast from '$lib/components/Toast.svelte';

  let { children } = $props();
</script>

<div class="demo-flag" role="note">
  Demo MVP v0.0.1. Nothing on this site takes payment or stores an email address.
</div>

<Header />

<main>
  {@render children()}
</main>

<SiteFooter />
<Toast />

<style>
  .demo-flag {
    background: var(--accent-dim);
    border-bottom: 1px solid rgba(245, 158, 11, 0.25);
    color: var(--accent-hi);
    font: 500 12.5px/1.4 var(--mono);
    letter-spacing: 0.02em;
    text-align: center;
    padding: 9px 16px;
  }
</style>
