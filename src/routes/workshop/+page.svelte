<script>
  import { onDestroy, onMount, tick } from 'svelte';
  import { fade } from 'svelte/transition';
  import { isValidWorkshopPassword } from '$lib/workshopAccessCode.js';
  import data from '$lib/data/workshop.json';

  let unlocked = false;
  let password = '';
  let formError = '';
  let passwordInput;

  // ---------- three.js scene, created lazily and paused when not visible -----
  let canvas;
  let sceneStarted = false;
  let readout = 'drag to orbit · hover a section';
  let metric = 'claims';
  let retarget = null;
  let disposeScene = null;
  let sceneStatus = 'idle';

  // ---------- section table -------------------------------------------------
  let sectionQuery = '';
  let sortKey = 'order';
  let expanded = null;

  const SECTIONS = data.sectionsDetail;
  const maxClaims = Math.max(...SECTIONS.map((s) => s.claims));
  const maxWords = Math.max(...SECTIONS.map((s) => s.words));

  $: filteredSections = SECTIONS.map((s, i) => ({ ...s, order: i }))
    .filter((s) => {
      const q = sectionQuery.trim().toLowerCase();
      if (!q) return true;
      if (q === 'broken') return s.broken > 0;
      return s.id.includes(q) || s.title.toLowerCase().includes(q) || (s.topType || '').includes(q);
    })
    .sort((a, b) => {
      if (sortKey === 'order') return a.order - b.order;
      if (sortKey === 'claims') return b.claims - a.claims;
      if (sortKey === 'broken') return b.broken - a.broken;
      if (sortKey === 'words') return b.words - a.words;
      return 0;
    });

  // ---------- commits -------------------------------------------------------
  let streamFilter = 'all';
  const streams = ['all', ...Array.from(new Set(data.commits.map((c) => c.stream)))];
  $: visibleCommits =
    streamFilter === 'all' ? data.commits : data.commits.filter((c) => c.stream === streamFilter);
  $: churn = visibleCommits.reduce(
    (a, c) => ({ files: a.files + c.files, adds: a.adds + c.adds, dels: a.dels + c.dels }),
    { files: 0, adds: 0, dels: 0 }
  );

  // ---------- derived numbers ----------------------------------------------
  const coveragePct = Math.round((data.book.receiptsResolvable / data.book.claims) * 100);
  const verdictRows = Object.entries(data.verdicts).sort((a, b) => b[1] - a[1]);
  const typeRows = Object.entries(data.claimTypes).sort((a, b) => b[1] - a[1]);
  const maxVerdict = Math.max(...verdictRows.map((r) => r[1]));
  const maxType = Math.max(...typeRows.map((r) => r[1]));
  const highBlockers = data.blockers.filter((b) => b.severity === 'high').length;

  const NAV = [
    ['state', 'State of play'],
    ['blocked', 'Needs a human'],
    ['coverage', 'Provenance'],
    ['ring', 'The ring'],
    ['sections', 'Sections'],
    ['work', 'Recent work'],
    ['devlog', 'Devlog']
  ];
  let activeNav = 'state';

  /** Count-up that respects reduced motion and only fires once, on view. */
  function countup(node, value) {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const render = (n) => (node.textContent = Math.round(n).toLocaleString());
    if (reduce) { render(value); return {}; }
    const io = new IntersectionObserver((es, o) => {
      for (const e of es) {
        if (!e.isIntersecting) continue;
        o.disconnect();
        const t0 = performance.now();
        const tick2 = (now) => {
          const p = Math.min(1, (now - t0) / 900);
          render(value * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(tick2);
        };
        requestAnimationFrame(tick2);
      }
    }, { threshold: 0.6 });
    io.observe(node);
    return { destroy: () => io.disconnect() };
  }

  async function submitPassword() {
    formError = '';
    if (isValidWorkshopPassword(password)) {
      unlocked = true;
      password = '';
      await tick();
      watchNav();
      watchScene();
    } else {
      formError = 'Not that one. Ask CT for the code.';
    }
  }

  function watchNav() {
    const spy = new IntersectionObserver(
      (es) => {
        for (const e of es) if (e.isIntersecting) activeNav = e.target.id;
      },
      { rootMargin: '-12% 0px -75% 0px' }
    );
    for (const [id] of NAV) {
      const el = document.getElementById(id);
      if (el) spy.observe(el);
    }
  }

  /**
   * The scene is not built until its panel is actually scrolled into view, and
   * the render loop stops whenever the canvas leaves the viewport or the tab is
   * hidden. A dashboard is a page people leave open; spinning a WebGL loop at
   * 60fps behind a background tab is pure battery burn for nothing on screen.
   */
  function watchScene() {
    const panel = document.getElementById('ring');
    if (!panel) return;
    let running = false;
    let onScreen = false;

    const io = new IntersectionObserver(async (es) => {
      onScreen = es.some((e) => e.isIntersecting);
      if (onScreen && !sceneStarted) {
        sceneStarted = true;
        await startScene();
      }
      sync();
    }, { threshold: 0.05 });
    io.observe(panel);

    const sync = () => {
      const want = onScreen && !document.hidden;
      if (want === running || !window.__wsRenderer) return;
      running = want;
      sceneStatus = want ? 'running' : 'paused';
      window.__wsRenderer.setAnimationLoop(want ? window.__wsFrame : null);
    };
    document.addEventListener('visibilitychange', sync);
    window.__wsSync = sync;
  }

  async function startScene() {
    const THREE = await import('three');
    const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js');

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'low-power' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(44, 16 / 9, 0.1, 300);
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

    // One shared geometry and two shared materials across all 30 columns, so the
    // scene costs 2 materials rather than 30.
    const geo = new THREE.BoxGeometry(1.15, 1, 1.15);
    const matOk = new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.45, metalness: 0.1 });
    const matBad = new THREE.MeshStandardMaterial({ color: 0xf87171, roughness: 0.45, metalness: 0.1, emissive: 0x3a0d0d });

    const group = new THREE.Group();
    scene.add(group);
    const RADIUS = 11;
    const bars = SECTIONS.map((s, i) => {
      const a = (i / SECTIONS.length) * Math.PI * 2;
      const m = new THREE.Mesh(geo, s.broken > 0 ? matBad : matOk);
      m.position.set(Math.cos(a) * RADIUS, 0, Math.sin(a) * RADIUS);
      m.rotation.y = -a;
      m.userData = s;
      group.add(m);
      return m;
    });

    const ring = new THREE.Mesh(
      new THREE.RingGeometry(RADIUS - 1.4, RADIUS + 1.4, 64),
      new THREE.MeshBasicMaterial({ color: 0x1c2431, side: THREE.DoubleSide, transparent: true, opacity: 0.5 })
    );
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = -0.02;
    scene.add(ring);

    retarget = () => {
      const vals = SECTIONS.map((s) => (metric === 'claims' ? s.claims : metric === 'broken' ? s.broken : s.words));
      const max = Math.max(...vals, 1);
      bars.forEach((b, i) => { b.userData._t = Math.max(0.12, (vals[i] / max) * 7); });
    };
    retarget();

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
        readout = `${d.id} · ${d.claims} claims · ${d.words.toLocaleString()} words` + (d.broken ? ` · ${d.broken} broken` : '');
      } else readout = 'drag to orbit · hover a section';
    };
    canvas.addEventListener('pointermove', onMove);

    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const frame = () => {
      const w = canvas.clientWidth, h = canvas.clientHeight;
      if (w && h && canvas.width !== Math.round(w * renderer.getPixelRatio())) {
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      }
      for (const b of bars) {
        const t = b.userData._t ?? 1;
        b.scale.y += (t - b.scale.y) * 0.12;
        b.position.y = b.scale.y / 2;
      }
      if (!still) group.rotation.y += 0.0018;
      controls.update();
      renderer.render(scene, camera);
    };

    window.__wsRenderer = renderer;
    window.__wsFrame = frame;
    if (window.__wsSync) window.__wsSync();

    disposeScene = () => {
      canvas.removeEventListener('pointermove', onMove);
      renderer.setAnimationLoop(null);
      geo.dispose(); matOk.dispose(); matBad.dispose();
      renderer.dispose();
      delete window.__wsRenderer; delete window.__wsFrame; delete window.__wsSync;
    };
  }

  function setMetric(m) {
    metric = m;
    if (retarget) retarget();
  }

  onMount(() => passwordInput?.focus());
  onDestroy(() => { if (disposeScene) disposeScene(); });
</script>

<svelte:head>
  <title>Workshop</title>
  <meta name="robots" content="noindex, nofollow" />
</svelte:head>

{#if !unlocked}
  <div class="gate" in:fade={{ duration: 200 }}>
    <div class="gate-box">
      <p class="kicker">Surviving the Singularity</p>
      <h1 class="gate-h">Workshop</h1>
      <p class="gate-lede">
        A working dashboard of the book build and the engineering around it. Not public,
        not finished, and deliberately showing its own gaps.
      </p>
      <form on:submit|preventDefault={submitPassword}>
        <input bind:this={passwordInput} bind:value={password} type="password"
          placeholder="access code" aria-label="Access code" autocomplete="off" />
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

    <nav class="railnav" aria-label="Sections">
      {#each NAV as [id, label]}
        <a href="#{id}" class:on={activeNav === id}>{label}</a>
      {/each}
    </nav>

    <div class="main">
      <header class="head">
        <p class="kicker">Surviving the Singularity · workshop</p>
        <h1>The book, measured</h1>
        <p class="lede">
          A snapshot generated by <code>scripts/build_workshop_data.py</code> from
          <code>sts.py factcheck</code>, the manuscript index and <code>git</code>.
          It changes only when that script runs and the site is rebuilt. Nothing here is live.
        </p>
        <div class="repobar">
          <span class="pill">{data.repo.branch}</span>
          <span class="pill mono">{data.repo.head}</span>
          <span class="pill" class:warn={!data.repo.pushed}>
            {data.repo.pushed ? 'pushed' : `${data.repo.aheadOfMain} commits unpushed`}
          </span>
          <span class="pill">{data.repo.dirtyPaths} dirty paths</span>
          <span class="stamp">generated {data.generatedAt.replace('T', ' ').replace('Z', ' UTC')}</span>
        </div>
      </header>

      <section id="state" class="stats" aria-label="Headline numbers">
        <a class="stat" href="#sections">
          <span class="n" use:countup={data.book.words}>0</span><span class="l">words</span>
          <span class="s">{data.book.sections} sections</span>
        </a>
        <a class="stat" href="#coverage">
          <span class="n" use:countup={data.book.claims}>0</span><span class="l">claims traced</span>
          <span class="s">{data.book.blocks.toLocaleString()} blocks</span>
        </a>
        <a class="stat" href="#coverage">
          <span class="n good" use:countup={data.book.receiptsResolvable}>0</span><span class="l">receipts resolve</span>
          <span class="s">{coveragePct}% coverage</span>
        </a>
        <a class="stat" href="#blocked">
          <span class="n bad" use:countup={data.book.receiptsBroken}>0</span><span class="l">receipts broken</span>
          <span class="s">all in 4 chapters</span>
        </a>
        <a class="stat" href="#blocked">
          <span class="n">{data.network.checked}<small>/{data.network.of}</small></span>
          <span class="l">citations fetched</span><span class="s">{data.network.dead} dead so far</span>
        </a>
        <a class="stat" href="#blocked">
          <span class="n warn" use:countup={highBlockers}>0</span><span class="l">high blockers</span>
          <span class="s">need a decision</span>
        </a>
      </section>

      <aside class="tldr">
        <h2 class="tldr-h">State of play</h2>
        <ol>
          <li>The manuscript is <strong>{data.book.words.toLocaleString()} words</strong> across
            {data.book.sections} sections, with {data.book.claims.toLocaleString()} mechanically
            detectable claims traced back to the commit that wrote them.</li>
          <li><strong>{coveragePct}% of those claims resolve</strong> to an immutable receipt. The
            other {data.book.receiptsBroken} sit in four chapters that are committed locally but
            never pushed, so no permalink exists for them.</li>
          <li>The external half is <strong>barely started</strong>: {data.network.checked} of
            {data.network.of} citations fetched, 0 dead so far.</li>
          <li>{highBlockers} of the {data.blockers.length} open items need a human decision rather
            than more engineering.</li>
        </ol>
      </aside>

      <section id="blocked" class="panel">
        <h2>Needs a human</h2>
        <p class="sub">The measured numbers above are generated. This list is judgement, and it is
        separated on purpose. Each item is stuck on a decision, not on more code.</p>
        <div class="blockers">
          {#each data.blockers as b}
            <article class="blocker" data-sev={b.severity}>
              <header>
                <span class="sev">{b.severity}</span>
                <h3>{b.title}</h3>
              </header>
              <p class="why">{b.why}</p>
              <dl>
                <div><dt>needs</dt><dd>{b.needs}</dd></div>
                <div><dt>effort</dt><dd>{b.effort}</dd></div>
              </dl>
            </article>
          {/each}
        </div>
      </section>

      <section id="coverage" class="panel">
        <h2>Provenance coverage</h2>
        <p class="sub">
          {data.book.receiptsResolvable.toLocaleString()} of {data.book.claims.toLocaleString()}
          claims resolve to an immutable commit.
        </p>
        <svg class="cov" viewBox="0 0 720 62" role="img"
          aria-label="{data.book.receiptsResolvable} of {data.book.claims} claims have a resolvable receipt">
          <rect x="0" y="8" width="720" height="26" rx="6" fill="#131a26" stroke="#232b39" />
          <rect x="0" y="8" height="26" rx="6" fill="#38bdf8" width="0">
            <animate attributeName="width" to={(720 * data.book.receiptsResolvable) / data.book.claims}
              dur="1.1s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1" />
          </rect>
          <text x="6" y="52" fill="#93a1b8" font-size="11" font-family="ui-monospace, Menlo, monospace">
            {data.book.receiptsResolvable} resolvable
          </text>
          <text x="714" y="52" text-anchor="end" fill="#f87171" font-size="11" font-family="ui-monospace, Menlo, monospace">
            {data.book.receiptsBroken} broken
          </text>
        </svg>

        <div class="twoup">
          <div>
            <h3>By verdict</h3>
            <svg viewBox="0 0 340 {verdictRows.length * 30 + 8}" role="img" aria-label="Claims by verdict">
              {#each verdictRows as [name, n], i}
                <text x="0" y={i * 30 + 18} fill="#93a1b8" font-size="11" font-family="ui-monospace, Menlo, monospace">{name.toLowerCase()}</text>
                <rect x="112" y={i * 30 + 6} height="15" rx="3"
                  fill={name === 'SUPPORTED' ? '#34d399' : name === 'UNCHECKED' ? '#f59e0b' : name === 'UNCHECKABLE' ? '#a78bfa' : '#64748b'} width="0">
                  <animate attributeName="width" to={(n / maxVerdict) * 170} dur="0.9s"
                    begin="{0.1 + i * 0.1}s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1" />
                </rect>
                <text x="292" y={i * 30 + 18} fill="#e6edf7" font-size="11" font-family="ui-monospace, Menlo, monospace">{n}</text>
              {/each}
            </svg>
            <p class="note">UNCHECKED is not a failure. It is a claim nobody has checked yet, which
            is almost entirely the 227 external URLs.</p>
          </div>
          <div>
            <h3>By claim type</h3>
            <svg viewBox="0 0 340 {typeRows.length * 26 + 8}" role="img" aria-label="Claims by type">
              {#each typeRows as [name, n], i}
                <text x="0" y={i * 26 + 16} fill="#93a1b8" font-size="11" font-family="ui-monospace, Menlo, monospace">{name.replace('_', ' ')}</text>
                <rect x="112" y={i * 26 + 5} height="13" rx="3" fill="#38bdf8" width="0">
                  <animate attributeName="width" to={(n / maxType) * 170} dur="0.9s"
                    begin="{0.1 + i * 0.07}s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1" />
                </rect>
                <text x="292" y={i * 26 + 16} fill="#e6edf7" font-size="11" font-family="ui-monospace, Menlo, monospace">{n}</text>
              {/each}
            </svg>
          </div>
        </div>

        <details class="ev">
          <summary>What the harness cannot see</summary>
          <div class="ev-body">
            <ul>
              <li>Whether any cited source is live, dead, paywalled or archived. That is the network
              pass, and it has run against {data.network.checked} of {data.network.of} citations.</li>
              <li>Whether a quotation matches its source wording. Quotations are detected as
              attributions, never compared.</li>
              <li>Whether a causal claim is true. {data.claimTypes.causal_claim} are detected and
              none is adjudicated.</li>
              <li>The 36 comparison claims that the project's own post mortem calls this book's real
              failure mode. Flagged, never checked against a primary source.</li>
            </ul>
          </div>
        </details>
      </section>

      <section id="ring" class="panel">
        <div class="phead">
          <h2>The manuscript as a ring</h2>
          <div class="chips">
            <button class="chip" class:on={metric === 'claims'} on:click={() => setMetric('claims')}>claims</button>
            <button class="chip" class:on={metric === 'broken'} on:click={() => setMetric('broken')}>broken</button>
            <button class="chip" class:on={metric === 'words'} on:click={() => setMetric('words')}>words</button>
          </div>
        </div>
        <p class="sub">30 sections in book order, clockwise from the introduction. Switch to
        <em>broken</em> and the four unpushed chapters stand up as one contiguous run, which is the
        shape of the problem: not scatter, a block.</p>
        <div class="stage">
          <canvas bind:this={canvas} class="canvas"></canvas>
          <div class="readout">{readout}</div>
          <div class="scenestate" aria-live="polite">{sceneStatus}</div>
        </div>
        <div class="legend">
          <span><i style="background:#38bdf8"></i>receipt resolves</span>
          <span><i style="background:#f87171"></i>receipt broken</span>
          <span>renders only while on screen</span>
        </div>
      </section>

      <section id="sections" class="panel">
        <div class="phead">
          <h2>Every section</h2>
          <div class="chips">
            <input class="search" type="search" bind:value={sectionQuery}
              placeholder="filter (try: broken, chapter1, url)" aria-label="Filter sections" />
            <button class="chip" class:on={sortKey === 'order'} on:click={() => (sortKey = 'order')}>book order</button>
            <button class="chip" class:on={sortKey === 'claims'} on:click={() => (sortKey = 'claims')}>claims</button>
            <button class="chip" class:on={sortKey === 'broken'} on:click={() => (sortKey = 'broken')}>broken</button>
            <button class="chip" class:on={sortKey === 'words'} on:click={() => (sortKey = 'words')}>words</button>
          </div>
        </div>
        <p class="count">{filteredSections.length} of {SECTIONS.length} sections</p>
        <div class="rows">
          {#each filteredSections as s (s.id)}
            <div class="row" class:broken={s.broken > 0}>
              <button class="rowhead" on:click={() => (expanded = expanded === s.id ? null : s.id)}
                aria-expanded={expanded === s.id}>
                <span class="chev" class:open={expanded === s.id}></span>
                <span class="rid">{s.id}</span>
                <span class="rtitle">{s.title}</span>
                <span class="rbar" aria-hidden="true">
                  <span class="rbar-fill" style="width:{(s.claims / maxClaims) * 100}%"></span>
                </span>
                <span class="rnum">{s.claims}</span>
                <span class="rnum broken-n">{s.broken || ''}</span>
              </button>
              {#if expanded === s.id}
                <div class="rowbody" transition:fade={{ duration: 120 }}>
                  <dl class="facts">
                    <div><dt>words</dt><dd>{s.words.toLocaleString()}</dd></div>
                    <div><dt>claims</dt><dd>{s.claims}</dd></div>
                    <div><dt>broken receipts</dt><dd class:bad={s.broken > 0}>{s.broken}</dd></div>
                    <div><dt>dominant type</dt><dd>{(s.topType || 'none').replace('_', ' ')}</dd></div>
                    <div><dt>words per claim</dt><dd>{s.claims ? Math.round(s.words / s.claims) : 'n/a'}</dd></div>
                  </dl>
                  <div class="mini">
                    <span class="minih">types</span>
                    {#each Object.entries(s.types).sort((a, b) => b[1] - a[1]) as [t, n]}
                      <span class="tag">{t.replace('_', ' ')} {n}</span>
                    {/each}
                  </div>
                  <div class="mini">
                    <span class="minih">verdicts</span>
                    {#each Object.entries(s.verdicts).sort((a, b) => b[1] - a[1]) as [v, n]}
                      <span class="tag v-{v.toLowerCase()}">{v.toLowerCase()} {n}</span>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>
          {/each}
        </div>
      </section>

      <section id="work" class="panel">
        <div class="phead">
          <h2>Recent work</h2>
          <div class="chips">
            {#each streams as s}
              <button class="chip" class:on={streamFilter === s} on:click={() => (streamFilter = s)}>{s}</button>
            {/each}
          </div>
        </div>
        <p class="count">
          {visibleCommits.length} commits · {churn.files} files ·
          <span class="add">+{churn.adds.toLocaleString()}</span>
          <span class="del">-{churn.dels.toLocaleString()}</span>
        </p>
        <ol class="commits">
          {#each visibleCommits as c (c.sha)}
            <li>
              <code class="sha">{c.sha}</code>
              <span class="date">{c.date}</span>
              <span class="subject">{c.subject}</span>
              <span class="churn">
                <span class="add">+{c.adds}</span><span class="del">-{c.dels}</span>
              </span>
            </li>
          {/each}
        </ol>
      </section>

      <section id="devlog" class="panel">
        <h2>Devlog</h2>
        <p class="sub">Long-form writeups of how the machinery works. Each is a self-contained page
        carrying its own provenance record.</p>
        <div class="posts">
          {#each data.posts as p}
            <a class="post" href={p.href}>
              <span class="pdate">{p.date} · {p.readingMinutes} min</span>
              <span class="ptitle">{p.title}</span>
              <span class="pdek">{p.dek}</span>
              <span class="ptags">{#each p.tags as t}<span class="tag">{t}</span>{/each}</span>
              <span class="pbuilt">built by {p.builtBy}</span>
            </a>
          {/each}
          {#each data.links as l}
            <a class="post alt" href={l.href}>
              <span class="pdate">tool</span>
              <span class="ptitle">{l.label}</span>
              <span class="pdek">{l.note}</span>
            </a>
          {/each}
        </div>
      </section>

      <footer class="foot">
        <p>Snapshot of a working branch, generated by {data.generator}. The numbers move when the
        work moves, and this page only catches up when that script runs and the site rebuilds.</p>
        <p>Measured values come from the factcheck pass, the manuscript index and git. The
        <a href="#blocked">Needs a human</a> list is judgement, marked as such.</p>
      </footer>
    </div>
  </div>
{/if}

<style>
  :global(body) { background: #020617; }

  .kicker { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: .72rem;
    letter-spacing: .18em; text-transform: uppercase; color: #94a3b8; margin: 0 0 .6rem; }

  /* gate */
  .gate { min-height: 80vh; display: grid; place-items: center; padding: 2rem 1.25rem; }
  .gate-box { max-width: 30rem; text-align: center; }
  .gate-h { font-size: 2.6rem; margin: 0 0 .8rem; color: #f1f5f9; letter-spacing: -.03em; }
  .gate-lede { color: #94a3b8; line-height: 1.6; margin: 0 0 1.6rem; }
  .gate form { display: flex; gap: .5rem; justify-content: center; }
  .gate input { flex: 1 1 auto; max-width: 16rem; background: rgba(30,41,59,.5); border: 1px solid #334155;
    border-radius: 8px; padding: .6rem .8rem; color: #f1f5f9; font-family: 'JetBrains Mono', monospace; }
  .gate button { background: #f59e0b; border: 0; border-radius: 8px; padding: .6rem 1.2rem;
    font-weight: 700; color: #0b0e14; cursor: pointer; }
  .err { color: #f87171; font-size: .9rem; margin-top: .8rem; }
  .gate-foot { color: #64748b; font-size: .74rem; margin-top: 1.6rem; line-height: 1.5; }

  /* layout */
  .dash { max-width: 78rem; margin: 0 auto; padding: 2.5rem 1.25rem 5rem; color: #f1f5f9;
    display: grid; grid-template-columns: 1fr; gap: 0; }
  .dash > * { min-width: 0; }
  .railnav { display: none; }
  @media (min-width: 1100px) {
    .dash { grid-template-columns: 11rem minmax(0, 1fr); gap: 2.5rem; }
    .railnav { display: block; position: sticky; top: 1.5rem; align-self: start;
      font-family: 'JetBrains Mono', monospace; font-size: .74rem; border-left: 1px solid #1e293b; }
    .railnav a { display: block; padding: .32rem .7rem; color: #64748b; text-decoration: none;
      border-left: 2px solid transparent; margin-left: -1px; }
    .railnav a:hover { color: #cbd5e1; }
    .railnav a.on { color: #f59e0b; border-left-color: #f59e0b; }
  }
  .main { min-width: 0; }

  h1 { font-size: clamp(1.9rem, 5vw, 2.9rem); margin: 0 0 .6rem; letter-spacing: -.03em; }
  h2 { font-size: 1.15rem; margin: 0 0 .4rem; letter-spacing: -.01em; }
  /* The site navbar is fixed and about 90px tall, so an anchor jump lands the
     panel heading underneath it. Every jump target clears it explicitly. */
  section[id], .stats { scroll-margin-top: 6.5rem; }
  h3 { font-size: .82rem; font-family: 'JetBrains Mono', monospace; color: #94a3b8;
    text-transform: uppercase; letter-spacing: .1em; margin: 0 0 .6rem; font-weight: 600; }
  .lede { color: #94a3b8; max-width: 46rem; line-height: 1.6; }
  .lede code, .sub code { font-family: 'JetBrains Mono', monospace; font-size: .86em;
    background: rgba(30,41,59,.6); padding: .1em .35em; border-radius: 4px; }
  .sub { color: #94a3b8; font-size: .9rem; margin: 0 0 1rem; line-height: 1.6; max-width: 50rem; }
  .note { color: #64748b; font-size: .78rem; line-height: 1.5; margin: .5rem 0 0; }
  .count { font-family: 'JetBrains Mono', monospace; font-size: .74rem; color: #64748b; margin: 0 0 .7rem; }

  .repobar { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; margin-top: 1rem; }
  .pill { font-family: 'JetBrains Mono', monospace; font-size: .68rem; padding: .2rem .55rem;
    border-radius: 999px; border: 1px solid #1e293b; color: #94a3b8; background: #0b1220; }
  .pill.warn { border-color: #78350f; color: #fbbf24; }
  .stamp { font-family: 'JetBrains Mono', monospace; font-size: .66rem; color: #475569; }

  /* stats */
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1px;
    background: #1e293b; border: 1px solid #1e293b; border-radius: 12px; overflow: hidden; margin: 1.8rem 0; }
  .stat { background: #0b1220; padding: 1rem .9rem; text-decoration: none; display: block; transition: background .18s; }
  .stat:hover { background: #111a2b; }
  .stat .n { display: block; font-family: 'JetBrains Mono', monospace; font-size: 1.55rem;
    font-weight: 700; color: #f1f5f9; letter-spacing: -.02em; }
  .stat .n small { font-size: .85rem; color: #64748b; }
  .stat .n.good { color: #34d399; } .stat .n.bad { color: #f87171; } .stat .n.warn { color: #fbbf24; }
  .stat .l { display: block; font-size: .76rem; color: #94a3b8; margin-top: .2rem; }
  .stat .s { display: block; font-family: 'JetBrains Mono', monospace; font-size: .64rem; color: #475569; margin-top: .25rem; }

  .tldr { background: rgba(15,23,42,.55); border: 1px solid #1e293b; border-left: 3px solid #f59e0b;
    border-radius: 0 12px 12px 0; padding: 1.1rem 1.3rem; margin: 1.4rem 0; }
  .tldr-h { font-family: 'JetBrains Mono', monospace; font-size: .7rem; text-transform: uppercase;
    letter-spacing: .15em; color: #f59e0b; margin: 0 0 .7rem; }
  .tldr ol { margin: 0; padding-left: 1.1rem; font-size: .92rem; color: #cbd5e1; line-height: 1.6; }
  .tldr li { margin-bottom: .4rem; }

  .panel { background: rgba(15,23,42,.55); border: 1px solid #1e293b; border-radius: 14px;
    padding: 1.3rem; margin: 1.3rem 0; }
  .phead { display: flex; flex-wrap: wrap; gap: .7rem; align-items: center; justify-content: space-between; margin-bottom: .5rem; }
  .twoup { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.6rem; margin-top: 1.4rem; }
  .twoup > * { min-width: 0; }
  .cov { width: 100%; height: auto; }

  .chips { display: flex; flex-wrap: wrap; gap: .35rem; align-items: center; }
  .chip { font-family: 'JetBrains Mono', monospace; font-size: .7rem; padding: .25rem .6rem;
    border-radius: 999px; border: 1px solid #334155; background: transparent; color: #94a3b8; cursor: pointer; }
  .chip:hover { color: #f1f5f9; border-color: #64748b; }
  .chip.on { background: #f59e0b; border-color: #f59e0b; color: #0b0e14; font-weight: 700; }
  .search { font-family: 'JetBrains Mono', monospace; font-size: .72rem; padding: .28rem .6rem;
    border-radius: 999px; border: 1px solid #334155; background: #0b1220; color: #f1f5f9; min-width: 14rem; }

  /* blockers */
  .blockers { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: .9rem; }
  .blocker { background: #0b1220; border: 1px solid #1e293b; border-radius: 12px; padding: 1rem; }
  .blocker[data-sev='high'] { border-top: 3px solid #f87171; }
  .blocker[data-sev='medium'] { border-top: 3px solid #fbbf24; }
  .blocker header { display: flex; flex-direction: column; gap: .3rem; margin-bottom: .5rem; }
  .sev { font-family: 'JetBrains Mono', monospace; font-size: .62rem; text-transform: uppercase;
    letter-spacing: .12em; color: #64748b; }
  .blocker h3 { font-family: inherit; font-size: 1rem; text-transform: none; letter-spacing: -.01em;
    color: #f1f5f9; margin: 0; font-weight: 650; }
  .why { font-size: .85rem; color: #94a3b8; line-height: 1.55; margin: 0 0 .7rem; }
  .blocker dl { margin: 0; display: grid; gap: .3rem; font-size: .78rem; }
  .blocker dl div { display: grid; grid-template-columns: 3.6rem 1fr; gap: .5rem; }
  .blocker dt { font-family: 'JetBrains Mono', monospace; font-size: .64rem; text-transform: uppercase;
    letter-spacing: .08em; color: #64748b; }
  .blocker dd { margin: 0; color: #cbd5e1; }

  /* evidence */
  .ev { border: 1px solid #1e293b; border-radius: 10px; background: #0b1220; margin-top: 1.3rem; overflow: hidden; }
  .ev summary { cursor: pointer; padding: .7rem .9rem; font-family: 'JetBrains Mono', monospace;
    font-size: .76rem; color: #cbd5e1; }
  .ev summary:hover { background: #111a2b; }
  .ev-body { padding: .2rem .9rem 1rem; border-top: 1px solid #1e293b; }
  .ev-body ul { margin: .8rem 0 0; padding-left: 1.1rem; font-size: .85rem; color: #94a3b8; line-height: 1.6; }
  .ev-body li { margin-bottom: .4rem; }

  /* scene */
  .stage { position: relative; }
  .canvas { width: 100%; aspect-ratio: 16 / 9; display: block; }
  .readout { position: absolute; top: .6rem; left: .6rem; font-family: 'JetBrains Mono', monospace;
    font-size: .72rem; background: rgba(2,6,23,.82); border: 1px solid #1e293b; border-radius: 6px;
    padding: .35rem .55rem; color: #94a3b8; pointer-events: none; max-width: calc(100% - 1.2rem); }
  .scenestate { position: absolute; top: .6rem; right: .6rem; font-family: 'JetBrains Mono', monospace;
    font-size: .62rem; color: #475569; pointer-events: none; }
  .legend { display: flex; flex-wrap: wrap; gap: 1rem; font-family: 'JetBrains Mono', monospace;
    font-size: .7rem; color: #64748b; margin-top: .6rem; }
  .legend i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: .35rem; }

  /* section rows */
  .rows { display: flex; flex-direction: column; }
  .row { border-bottom: 1px solid #131c2b; }
  .row:last-child { border-bottom: 0; }
  .rowhead { display: grid; grid-template-columns: 12px 6.4rem 1fr 5rem 2.6rem 2rem; gap: .6rem;
    align-items: center; width: 100%; text-align: left; background: none; border: 0; cursor: pointer;
    padding: .5rem .2rem; color: inherit; font: inherit; }
  .rowhead:hover { background: #0d1626; }
  .chev { width: 0; height: 0; border-left: 5px solid #475569; border-top: 4px solid transparent;
    border-bottom: 4px solid transparent; transition: transform .15s; }
  .chev.open { transform: rotate(90deg); }
  .rid { font-family: 'JetBrains Mono', monospace; font-size: .74rem; color: #38bdf8; }
  .row.broken .rid { color: #f87171; }
  .rtitle { font-size: .84rem; color: #cbd5e1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .rbar { display: block; height: 6px; background: #131c2b; border-radius: 3px; overflow: hidden; }
  .rbar-fill { display: block; height: 100%; background: #38bdf8; }
  .row.broken .rbar-fill { background: #f87171; }
  .rnum { font-family: 'JetBrains Mono', monospace; font-size: .74rem; color: #94a3b8; text-align: right; }
  .broken-n { color: #f87171; }
  .rowbody { padding: .6rem .2rem 1rem 1.6rem; }
  .facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: .5rem; margin: 0 0 .7rem; }
  .facts div { background: #0b1220; border: 1px solid #1e293b; border-radius: 8px; padding: .45rem .6rem; }
  .facts dt { font-family: 'JetBrains Mono', monospace; font-size: .6rem; text-transform: uppercase;
    letter-spacing: .09em; color: #64748b; }
  .facts dd { margin: .15rem 0 0; font-family: 'JetBrains Mono', monospace; font-size: .82rem; color: #f1f5f9; }
  .facts dd.bad { color: #f87171; }
  .mini { display: flex; flex-wrap: wrap; gap: .3rem; align-items: center; margin-bottom: .4rem; }
  .minih { font-family: 'JetBrains Mono', monospace; font-size: .6rem; text-transform: uppercase;
    letter-spacing: .1em; color: #475569; margin-right: .2rem; }
  .tag { font-family: 'JetBrains Mono', monospace; font-size: .64rem; color: #94a3b8;
    border: 1px solid #1e293b; border-radius: 999px; padding: .1rem .45rem; }
  .tag.v-supported { color: #34d399; border-color: #14532d; }
  .tag.v-unchecked { color: #fbbf24; border-color: #78350f; }

  /* commits */
  .commits { list-style: none; margin: 0; padding: 0; font-size: .84rem; }
  .commits li { display: grid; grid-template-columns: 4.4rem 5.2rem 1fr auto; gap: .7rem;
    padding: .4rem 0; border-bottom: 1px solid #131c2b; align-items: baseline; }
  .commits li:last-child { border-bottom: 0; }
  .sha { font-family: 'JetBrains Mono', monospace; color: #f59e0b; font-size: .76rem; }
  .date { font-family: 'JetBrains Mono', monospace; color: #475569; font-size: .72rem; }
  .subject { color: #cbd5e1; }
  .churn { font-family: 'JetBrains Mono', monospace; font-size: .7rem; white-space: nowrap; }
  .add { color: #34d399; margin-right: .4rem; } .del { color: #f87171; }
  @media (max-width: 700px) {
    .commits li { grid-template-columns: 4.4rem 1fr; }
    .date, .churn { display: none; }
    /* On a phone the fixed grid squeezed every title to "Chapt...", which makes
       the table unreadable. Wrap to two lines instead: id and count on the
       first, the full title on the second. */
    .rowhead { display: flex; flex-wrap: wrap; align-items: center; gap: .1rem .5rem; }
    .rid { flex: 0 0 auto; }
    .rnum { margin-left: auto; }
    .rtitle { flex: 1 0 100%; white-space: normal; font-size: .78rem; color: #94a3b8;
      order: 3; padding-left: 1.1rem; }
    .rbar, .broken-n { display: none; }
  }

  /* posts */
  .posts { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: .9rem; }
  .post { display: flex; flex-direction: column; gap: .3rem; background: #0b1220; border: 1px solid #1e293b;
    border-radius: 12px; padding: 1rem; text-decoration: none; transition: border-color .18s, transform .18s; }
  .post:hover { border-color: #f59e0b; transform: translateY(-2px); }
  .post.alt:hover { border-color: #38bdf8; }
  .pdate { font-family: 'JetBrains Mono', monospace; font-size: .68rem; color: #475569; }
  .ptitle { font-size: 1.02rem; font-weight: 650; color: #f1f5f9; letter-spacing: -.01em; }
  .pdek { font-size: .85rem; color: #94a3b8; line-height: 1.5; }
  .ptags { display: flex; flex-wrap: wrap; gap: .3rem; margin-top: .25rem; }
  .pbuilt { font-family: 'JetBrains Mono', monospace; font-size: .62rem; color: #475569; margin-top: .25rem; }

  .foot { color: #64748b; font-size: .8rem; border-top: 1px solid #1e293b; margin-top: 2rem; padding-top: 1.3rem; }
  .foot a { color: #94a3b8; }

  @media (prefers-reduced-motion: reduce) {
    .post:hover { transform: none; }
    .chev { transition: none; }
  }
</style>
