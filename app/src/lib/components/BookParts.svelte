<script>
  import { parts } from '$lib/precedents.js';
  import { stat } from '$lib/stats.js';
</script>

<!-- The book comes after the offer and after the proof, not before. The
     artifact is not the product. The updates are. -->
<section class="band band-alt" id="book">
  <div class="wrap">
    <p class="kicker">The book</p>
    <h2 class="sec-h2">Three parts. {stat('words').value} words so far.</h2>
    <div class="parts">
      {#each parts as p (p.n)}
        <article class="part">
          <p class="part-n">{p.n}</p>
          <h3 class="part-h">{p.title}</h3>
          <p class="part-d">{p.detail}</p>
        </article>
      {/each}
    </div>
  </div>
</section>

<style>
  .parts {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
  .part {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 26px 24px;
  }
  .part-n {
    font: 600 12px/1 var(--mono);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 14px;
  }
  .part-h {
    font: 600 21px/1.25 var(--serif);
    letter-spacing: -0.01em;
    margin: 0 0 12px;
  }
  .part-d {
    font-size: 15.5px;
    line-height: 1.65;
    color: var(--text-2);
    margin: 0;
  }

  @media (max-width: 940px) {
    .parts { grid-template-columns: 1fr; }
  }
</style>
