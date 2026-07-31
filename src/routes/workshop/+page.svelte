<script>
  import { onMount, onDestroy, tick } from 'svelte';
  import { fade } from 'svelte/transition';
  import { isValidWorkshopPassword } from '$lib/workshopAccessCode.js';
  import data from '$lib/data/workshop.json';

  let unlocked = false;
  let password = '';
  let formError = '';
  let passwordInput;
  let canvas;
  let readout = 'drag to orbit · hover a section';
  let metric = 'claims';
  let streamFilter = 'all';
  let disposeScene = null;

  const streams = ['all', ...new Set(data.commits.map((c) => c.stream))];

  $: visibleCommits =
    streamFilter === 'all' ? data.commits : data.commits.filter((c) => c.stream === streamFilter);

  // Sections come from the claim-type breakdown the factcheck pass produced.
  // Height metric switches between total claims and broken receipts.
  const SECTIONS = [
    ['introduction', 23, 0], ['preface', 9, 0], ['chapter0', 31, 0], ['part-1', 1, 0],
    ['chapter1', 64, 0], ['chapter2', 42, 0], ['chapter3', 16, 0], ['chapter4', 19, 0],
    ['chapter5', 29, 0], ['part-2', 2, 0], ['chapter6', 34, 0], ['chapter7', 60, 0],
    ['chapter8', 64, 0], ['chapter9', 43, 43], ['part-3', 1, 0], ['chapter10', 32, 32],
    ['chapter11', 39, 39], ['chapter12', 40, 0], ['chapter13', 37, 37], ['chapter14', 62, 0],
    ['chapter15', 29, 0], ['chapter16', 25, 0], ['chapter17', 24, 0], ['chapter18', 29, 0],
    ['conclusion', 18, 0], ['appendix-a', 8, 0], ['appendix-b', 330, 0], ['appendix-c', 8, 0],
    ['appendix-d', 101, 0], ['appendix-e', 22, 0]
  ];

  async function submitPassword() {
    formError = '';
    if (isValidWorkshopPassword(password)) {
      unlocked = true;
      password = '';
      await tick();
      startScene();
    } else {
      formError = 'Not that one. Ask CT for the code.';
    }
  }

  function setMetric(m) {
    metric = m;
    if (retargetScene) retargetScene();
  }

  let retargetScene = null;

  // The scene is built only after unlock, so a locked visitor never pays the
  // cost of loading three.js at all.
  async function startScene() {
    if (!canvas || disposeScene) return;
    const THREE = await import('three');
    const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js');

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(44, 16 / 9, 0.1, 300);
    // Framed so the tallest column still fits when the metric switches to
    // "broken only" and four chapters jump to full height. The first pass
    // clipped them off the top of the canvas.
    camera.position.set(0, 17, 34);
    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;
    controls.enablePan = false;
    controls.target.set(0, 3.2, 0);
    controls.minDistance = 14;
    controls.maxDistance = 60;
    controls.maxPolarAngle = Math.PI / 2.1;

    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const key = new THREE.DirectionalLight(0xffffff, 1.4);
    key.position.set(6, 18, 10);
    scene.add(key);

    // A ring rather than a grid, so the book reads as one continuous object and
    // the broken run is visibly contiguous rather than scattered.
    const group = new THREE.Group();
    scene.add(group);
    const RADIUS = 11;
    const bars = SECTIONS.map(([label, total, broken], i) => {
      const angle = (i / SECTIONS.length) * Math.PI * 2;
      const mat = new THREE.MeshStandardMaterial({
        color: broken > 0 ? 0xf87171 : 0x38bdf8,
        roughness: 0.45,
        metalness: 0.1,
        emissive: broken > 0 ? 0x3a0d0d : 0x000000
      });
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1, 1.15), mat);
      mesh.position.set(Math.cos(angle) * RADIUS, 0, Math.sin(angle) * RADIUS);
      mesh.rotation.y = -angle;
      mesh.userData = { label, total, broken };
      group.add(mesh);
      return mesh;
    });

    const ring = new THREE.Mesh(
      new THREE.RingGeometry(RADIUS - 1.4, RADIUS + 1.4, 64),
      new THREE.MeshBasicMaterial({ color: 0x1c2431, side: THREE.DoubleSide, transparent: true, opacity: 0.5 })
    );
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = -0.02;
    scene.add(ring);

    retargetScene = () => {
      const vals = SECTIONS.map(([, total, broken]) => (metric === 'claims' ? total : broken));
      const max = Math.max(...vals, 1);
      bars.forEach((b, i) => {
        b.userData.targetH = Math.max(0.12, (vals[i] / max) * 7);
      });
    };
    retargetScene();

    const ray = new THREE.Raycaster();
    const ptr = new THREE.Vector2();
    const onMove = (e) => {
      const r = canvas.getBoundingClientRect();
      ptr.x = ((e.clientX - r.left) / r.width) * 2 - 1;
      ptr.y = -((e.clientY - r.top) / r.height) * 2 + 1;
      ray.setFromCamera(ptr, camera);
      const hit = ray.intersectObjects(bars)[0];
      if (hit) {
        const d = hit.object.userData;
        readout = d.label + ' · ' + d.total + ' claims' + (d.broken ? ' · ' + d.broken + ' broken' : '');
      } else {
        readout = 'drag to orbit · hover a section';
      }
    };
    canvas.addEventListener('pointermove', onMove);

    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    renderer.setAnimationLoop(() => {
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;
      if (w && h && canvas.width !== Math.round(w * renderer.getPixelRatio())) {
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      }
      for (const b of bars) {
        const t = b.userData.targetH ?? 1;
        b.scale.y += (t - b.scale.y) * 0.12;
        b.position.y = b.scale.y / 2;
      }
      if (!still) group.rotation.y += 0.0018;
      controls.update();
      renderer.render(scene, camera);
    });

    disposeScene = () => {
      canvas.removeEventListener('pointermove', onMove);
      renderer.setAnimationLoop(null);
      renderer.dispose();
    };
  }

  onMount(() => {
    passwordInput?.focus();
  });

  onDestroy(() => {
    if (disposeScene) disposeScene();
  });

  const pct = Math.round((data.book.receiptsResolvable / data.book.claims) * 100);
</script>

<svelte:head>
  <title>Workshop</title>
  <meta name="robots" content="noindex, nofollow" />
</svelte:head>

{#if !unlocked}
  <div class="gate" in:fade={{ duration: 200 }}>
    <div class="gate-box">
      <p class="kicker">Surviving the Singularity</p>
      <h1>Workshop</h1>
      <p class="gate-lede">
        A working dashboard of the book build and the engineering around it. Not public,
        not finished, and deliberately showing its own gaps.
      </p>
      <form on:submit|preventDefault={submitPassword}>
        <input
          bind:this={passwordInput}
          bind:value={password}
          type="password"
          placeholder="access code"
          aria-label="Access code"
          autocomplete="off"
        />
        <button type="submit">Enter</button>
      </form>
      {#if formError}<p class="err">{formError}</p>{/if}
      <p class="gate-foot">
        This gate is a speed-bump, not access control. The code lives in the page bundle.
      </p>
    </div>
  </div>
{:else}
  <div class="dash" in:fade={{ duration: 250 }}>
    <header class="dash-head">
      <div>
        <p class="kicker">Surviving the Singularity · workshop</p>
        <h1>The book, measured</h1>
        <p class="lede">
          Everything below is a snapshot generated at build time from
          <code>sts.py factcheck</code> and <code>git log</code>. Nothing here is live.
          Generated {data.generatedAt.slice(0, 10)}.
        </p>
      </div>
    </header>

    <section class="stats" aria-label="Book statistics">
      <div class="stat"><span class="n">{data.book.words.toLocaleString()}</span><span class="l">words</span></div>
      <div class="stat"><span class="n">{data.book.sections}</span><span class="l">sections</span></div>
      <div class="stat"><span class="n">{data.book.claims.toLocaleString()}</span><span class="l">claims traced</span></div>
      <div class="stat"><span class="n good">{data.book.receiptsResolvable.toLocaleString()}</span><span class="l">receipts resolve</span></div>
      <div class="stat"><span class="n bad">{data.book.receiptsBroken}</span><span class="l">receipts broken</span></div>
      <div class="stat"><span class="n">{data.network.checked}<small>/{data.network.of}</small></span><span class="l">citations fetched</span></div>
    </section>

    <section class="panel">
      <h2>Provenance coverage</h2>
      <p class="panel-sub">
        {pct}% of traced claims can be resolved to an immutable commit. The remainder are the
        four chapters committed locally but never pushed, so no permalink exists for them yet.
      </p>
      <svg class="cov" viewBox="0 0 720 74" role="img"
        aria-label="{data.book.receiptsResolvable} of {data.book.claims} claims have a resolvable receipt">
        <rect x="0" y="18" width="720" height="26" rx="6" fill="#1b2230" stroke="#232b39" />
        <rect x="0" y="18" height="26" rx="6" fill="#38bdf8" width="0">
          <animate attributeName="width" to={(720 * data.book.receiptsResolvable) / data.book.claims}
            dur="1.1s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1" />
        </rect>
        <text x="8" y="62" fill="#93a1b8" font-size="11" font-family="ui-monospace, Menlo, monospace">
          {data.book.receiptsResolvable} resolvable
        </text>
        <text x="712" y="62" text-anchor="end" fill="#f87171" font-size="11" font-family="ui-monospace, Menlo, monospace">
          {data.book.receiptsBroken} broken
        </text>
      </svg>
    </section>

    <section class="panel">
      <div class="panel-head">
        <h2>The manuscript as a ring</h2>
        <div class="chips">
          <button class="chip" class:on={metric === 'claims'} on:click={() => setMetric('claims')}>all claims</button>
          <button class="chip" class:on={metric === 'broken'} on:click={() => setMetric('broken')}>broken only</button>
        </div>
      </div>
      <div class="stage">
        <canvas bind:this={canvas} class="canvas"></canvas>
        <div class="readout">{readout}</div>
      </div>
      <div class="legend">
        <span><i style="background:#38bdf8"></i>receipt resolves</span>
        <span><i style="background:#f87171"></i>receipt broken</span>
        <span>30 sections in book order, clockwise from the introduction</span>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <h2>Recent work</h2>
        <div class="chips">
          {#each streams as s}
            <button class="chip" class:on={streamFilter === s} on:click={() => (streamFilter = s)}>{s}</button>
          {/each}
        </div>
      </div>
      <ol class="commits">
        {#each visibleCommits as c (c.sha)}
          <li>
            <code class="sha">{c.sha}</code>
            <span class="date">{c.date}</span>
            <span class="subject">{c.subject}</span>
          </li>
        {/each}
      </ol>
      <p class="panel-foot">{visibleCommits.length} of {data.commits.length} commits shown. Local branch, not pushed.</p>
    </section>

    <section class="panel">
      <h2>Devlog</h2>
      <p class="panel-sub">Long-form writeups of how the machinery actually works. Each one is a
      self-contained page with its own provenance record.</p>
      <div class="posts">
        {#each data.posts as p}
          <a class="post" href={p.href}>
            <span class="post-date">{p.date} · {p.readingMinutes} min</span>
            <span class="post-title">{p.title}</span>
            <span class="post-dek">{p.dek}</span>
            <span class="post-tags">
              {#each p.tags as t}<span class="tag">{t}</span>{/each}
            </span>
            <span class="post-built">built by {p.builtBy}</span>
          </a>
        {/each}
      </div>
    </section>

    <footer class="dash-foot">
      <p>
        Snapshot of a working branch. The numbers move when the work moves, and this page only
        updates when the site is rebuilt.
      </p>
    </footer>
  </div>
{/if}

<style>
  :global(body) { background: #020617; }
  .gate { min-height: 80vh; display: grid; place-items: center; padding: 2rem 1.25rem; }
  .gate-box { max-width: 30rem; text-align: center; }
  .kicker { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 0.72rem;
    letter-spacing: 0.18em; text-transform: uppercase; color: #94a3b8; margin: 0 0 0.6rem; }
  .gate h1 { font-size: 2.6rem; margin: 0 0 0.8rem; color: #f1f5f9; letter-spacing: -0.03em; }
  .gate-lede { color: #94a3b8; line-height: 1.6; margin: 0 0 1.6rem; }
  .gate form { display: flex; gap: 0.5rem; justify-content: center; }
  .gate input { flex: 1 1 auto; max-width: 16rem; background: rgba(30,41,59,0.5); border: 1px solid #334155;
    border-radius: 8px; padding: 0.6rem 0.8rem; color: #f1f5f9; font-family: 'JetBrains Mono', monospace; }
  .gate button { background: #f59e0b; border: 0; border-radius: 8px; padding: 0.6rem 1.2rem;
    font-weight: 700; color: #0b0e14; cursor: pointer; }
  .err { color: #f87171; font-size: 0.9rem; margin-top: 0.8rem; }
  .gate-foot { color: #64748b; font-size: 0.74rem; margin-top: 1.6rem; line-height: 1.5; }

  .dash { max-width: 68rem; margin: 0 auto; padding: 3rem 1.25rem 5rem; color: #f1f5f9; }
  .dash-head h1 { font-size: clamp(1.9rem, 5vw, 2.8rem); margin: 0 0 0.6rem; letter-spacing: -0.03em; }
  .lede { color: #94a3b8; max-width: 44rem; line-height: 1.6; }
  .lede code { font-family: 'JetBrains Mono', monospace; font-size: 0.86em; background: rgba(30,41,59,0.6);
    padding: 0.1em 0.35em; border-radius: 4px; }

  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 1px;
    background: #1e293b; border: 1px solid #1e293b; border-radius: 12px; overflow: hidden; margin: 2rem 0; }
  .stat { background: #0b1220; padding: 1rem 0.9rem; }
  .stat .n { display: block; font-family: 'JetBrains Mono', monospace; font-size: 1.6rem; font-weight: 700; }
  .stat .n small { font-size: 0.9rem; color: #64748b; }
  .stat .n.good { color: #34d399; }
  .stat .n.bad { color: #f87171; }
  .stat .l { display: block; font-size: 0.76rem; color: #94a3b8; margin-top: 0.2rem; }

  .panel { background: rgba(15,23,42,0.55); border: 1px solid #1e293b; border-radius: 14px;
    padding: 1.4rem; margin: 1.4rem 0; }
  .panel h2 { font-size: 1.1rem; margin: 0 0 0.4rem; letter-spacing: -0.01em; }
  .panel-sub { color: #94a3b8; font-size: 0.9rem; margin: 0 0 1rem; line-height: 1.6; max-width: 48rem; }
  .panel-head { display: flex; flex-wrap: wrap; gap: 0.8rem; align-items: center;
    justify-content: space-between; margin-bottom: 1rem; }
  .panel-foot { color: #64748b; font-size: 0.76rem; margin: 0.9rem 0 0; }
  .cov { width: 100%; height: auto; }

  .chips { display: flex; flex-wrap: wrap; gap: 0.35rem; }
  .chip { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; padding: 0.25rem 0.6rem;
    border-radius: 999px; border: 1px solid #334155; background: transparent; color: #94a3b8; cursor: pointer; }
  .chip:hover { color: #f1f5f9; border-color: #64748b; }
  .chip.on { background: #f59e0b; border-color: #f59e0b; color: #0b0e14; font-weight: 700; }

  .stage { position: relative; }
  .canvas { width: 100%; aspect-ratio: 16 / 9; display: block; }
  .readout { position: absolute; top: 0.6rem; left: 0.6rem; font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; background: rgba(2,6,23,0.82); border: 1px solid #1e293b; border-radius: 6px;
    padding: 0.35rem 0.55rem; color: #94a3b8; pointer-events: none; }
  .legend { display: flex; flex-wrap: wrap; gap: 1rem; font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; color: #64748b; margin-top: 0.6rem; }
  .legend i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 0.35rem; }

  .commits { list-style: none; margin: 0; padding: 0; font-size: 0.86rem; }
  .commits li { display: grid; grid-template-columns: 4.6rem 5.4rem 1fr; gap: 0.7rem;
    padding: 0.45rem 0; border-bottom: 1px solid #1e293b; align-items: baseline; }
  .commits li:last-child { border-bottom: 0; }
  .sha { font-family: 'JetBrains Mono', monospace; color: #f59e0b; font-size: 0.78rem; }
  .date { font-family: 'JetBrains Mono', monospace; color: #64748b; font-size: 0.74rem; }
  .subject { color: #cbd5e1; }
  @media (max-width: 640px) {
    .commits li { grid-template-columns: 4.6rem 1fr; }
    .date { display: none; }
  }

  .posts { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.9rem; }
  .post { display: flex; flex-direction: column; gap: 0.35rem; background: #0b1220; border: 1px solid #1e293b;
    border-radius: 12px; padding: 1rem; text-decoration: none; transition: border-color 0.18s, transform 0.18s; }
  .post:hover { border-color: #f59e0b; transform: translateY(-2px); }
  .post-date { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748b; }
  .post-title { font-size: 1.05rem; font-weight: 650; color: #f1f5f9; letter-spacing: -0.01em; }
  .post-dek { font-size: 0.86rem; color: #94a3b8; line-height: 1.5; }
  .post-tags { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.3rem; }
  .tag { font-family: 'JetBrains Mono', monospace; font-size: 0.64rem; color: #38bdf8;
    border: 1px solid #1e3a5f; border-radius: 999px; padding: 0.1rem 0.45rem; }
  .post-built { font-family: 'JetBrains Mono', monospace; font-size: 0.64rem; color: #475569; margin-top: 0.3rem; }

  .dash-foot { color: #64748b; font-size: 0.8rem; border-top: 1px solid #1e293b;
    margin-top: 2rem; padding-top: 1.4rem; }
</style>
