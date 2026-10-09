<script>
  // Hand-authored, not postforge. The other devlog post carries a postforge
  // provenance block because a generator built it; this one does not, and
  // claiming otherwise would put a false provenance record on the page that
  // the rest of the devlog exists to argue against.
  //
  // Self-contained: markup and styles live here rather than in a raw-imported
  // content.html, so there is no generated stylesheet to keep in sync.
</script>

<svelte:head>
  <title>The Void Between the Panes</title>
  <meta
    name="description"
    content="A responsive signup layout passed every automated check at twelve viewports and still looked broken. The thing that was wrong with it was not a thing the checker could measure."
  />
  <!-- Same policy as the rest of the devlog: linked from the footer, kept out
       of search. Working notes, not a landing page. -->
  <meta name="robots" content="noindex, follow" />
</svelte:head>

<a class="back" href="/devlog">back to devlog</a>

<article class="post">
  <header class="head">
    <p class="kicker">Devlog</p>
    <h1>The Void Between the Panes</h1>
    <p class="dek">
      A signup layout passed every automated check at twelve viewports and still
      looked wrong. What was broken was not something the checker could measure,
      and that gap is the interesting part.
    </p>
    <p class="meta">
      <time datetime="2026-08-01">2026-08-01</time>
      <span class="dot">·</span>
      <span>7 min read</span>
      <span class="dot">·</span>
      <span>hand-authored</span>
    </p>
  </header>

  <div class="body">

    <p>
      The site needed a way to create an account. Before writing a line of auth
      code, the layout had to be settled, because a signup form is the one screen
      where a layout bug costs you the user outright. There is no second
      impression on a page whose entire job is a single decision.
    </p>

    <p>
      So it got drawn mobile first, resolved at desktop, checked back through
      tablet, and then measured. The measuring is where it got interesting.
    </p>

    <h2>Breakpoints are claims that something breaks</h2>

    <p>
      The reflex is to reach for 768px and 1024px because those are the numbers
      everyone uses. They are the wrong numbers, or at least they are numbers
      chosen by someone else for someone else's content.
    </p>

    <p>
      A breakpoint is an assertion: <em>at this width, the layout stops
      working.</em> If you cannot say what breaks, you do not have a breakpoint,
      you have a habit. So each one here was placed by widening the window until
      the layout actually failed, then setting the threshold just before the
      failure.
    </p>

    <p>
      The one worth defending is the tablet. The obvious move is to split an
      834px tablet into two panes, form on one side, sales copy on the other.
      Try it and both halves lose. Each pane lands around 380px: the copy sets at
      roughly thirty characters per line, which reads as a ragged column, and the
      form is narrow enough that the federated sign-in buttons drop back to
      stacked anyway. You paid for a split and got nothing for it.
    </p>

    <p>
      So the split waits until 1140px, which is the first width where the form
      can hold 480px and the copy still clears 500px. Between 900 and 1139 the
      page composes as one centered column instead. A tablet is not a small
      desktop. It is a phone with more room, and it should be laid out like one.
    </p>

    <h2>Height is a dimension too</h2>

    <p>
      Responsive design is taught as a width problem, and that is half of it. The
      layout also has to survive an 800 by 600 window, a landscape phone, a square
      viewport, and a laptop whose browser toolbar has eaten 200px.
    </p>

    <p>
      These all fail the same way and it is not horizontal overflow. The submit
      button falls below the fold, and the user lands on an argument they did not
      ask to re-read instead of the field they came for. Two height thresholds
      handle it: below 760px tall the vertical rhythm compresses, and below 560px
      tall the value column collapses to its headline, because at that size the
      sales copy has stopped being persuasion and become an obstacle.
    </p>

    <h2>What the probe caught</h2>

    <p>
      The checker is a stdlib Python script that renders the page at twelve
      viewports and measures horizontal overflow, elements escaping the viewport,
      tap targets under 44px, and whether the primary action clears the fold.
      Three findings came out of it, and all three would have shipped:
    </p>

    <ul>
      <li>
        <strong>The value column pushed the form off the fold on short wide
        screens.</strong> On a 900 by 900 square the submit button landed 269px
        below the fold. On a 1112 by 834 tablet in landscape, 412px below. The
        rule that promotes the copy above the form is now gated on height, not
        just width, so square and short viewports keep the form first.
      </li>
      <li>
        <strong>Four controls were under the 44px accessible target.</strong> The
        wordmark link at 22px, both mode tabs at 40px, the password reveal toggle
        at 38px. None of that is visible by eye. All of it is one measurement away.
      </li>
      <li>
        <strong>The consent checkbox measured 20px,</strong> which turned out to
        be the checker's fault rather than the layout's. The box is wrapped in a
        label, and clicking a label activates its input, so the label is the real
        target. The probe was measuring the wrong rectangle.
      </li>
    </ul>

    <p>
      That last one is worth sitting with. A checker that reports a real number
      about the wrong object is more dangerous than one that reports nothing,
      because it looks like evidence.
    </p>

    <h2>Watching it go red</h2>

    <p>
      Every viewport reported zero horizontal overflow on the first run, which
      should make you suspicious rather than pleased. A check that has only ever
      returned green has not been shown to work. It has been shown to return
      green.
    </p>

    <p>
      So it got broken on purpose: a 1400px-wide element injected into the page,
      the probe re-run. It reported <code>overflow-x 1136px</code> at 280px wide
      and failed every viewport, and the element came back out. Now a green run
      means the check ran. Before that, a green run meant nothing at all, and
      there was no way to tell the two apart from the output.
    </p>

    <h2>Then the part the probe could not see</h2>

    <p>
      Twelve viewports passing, screenshots reviewed, the thing looked done. Then
      it went up on a real 1440px monitor and the desktop layout was visibly
      wrong. The two panes did not read as one composition. They read as two
      unrelated things that happened to share a page.
    </p>

    <figure class="fig">
      <svg viewBox="0 0 640 190" role="img" aria-label="Diagram: a 1.05fr column measures 790px while its content is capped at 560px, leaving 230px of dead space before the gap">
        <rect width="640" height="190" fill="#0b1120" rx="8"/>

        <text x="20" y="26" class="lbl">BEFORE</text>
        <rect x="20" y="36" width="380" height="54" fill="none" stroke="#475569" stroke-width="1.5" stroke-dasharray="4 3"/>
        <rect x="20" y="36" width="270" height="54" fill="#1e293b"/>
        <text x="32" y="68" class="tx">rail content, capped 560px</text>
        <text x="300" y="60" class="bad">230px</text>
        <text x="300" y="76" class="bad">of nothing</text>
        <rect x="424" y="36" width="196" height="54" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="470" y="68" class="tx">form card</text>
        <path d="M400 100 L400 112 L424 112" fill="none" stroke="#f87171" stroke-width="1.2"/>
        <text x="300" y="126" class="bad">gap starts here, 86px later</text>

        <text x="20" y="152" class="lbl">AFTER</text>
        <rect x="20" y="158" width="270" height="26" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
        <text x="32" y="175" class="tx">rail column = 560px</text>
        <rect x="330" y="158" width="196" height="26" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="376" y="175" class="tx">form card</text>
        <text x="292" y="152" class="ok">gap</text>
        <text x="540" y="175" class="ok">centered as a pair</text>
      </svg>
      <figcaption>
        The column was sized by the viewport. The content inside it was sized for
        readability. Nobody owned the difference.
      </figcaption>
    </figure>

    <p>
      The cause: the copy column was declared as <code>1.05fr</code>, which
      computes to roughly 790px at a 1440px viewport. But the copy inside it is
      capped at 560px, because past that a line of text gets too long to track
      comfortably. Both of those decisions are correct on their own. Together
      they left about 230px of dead space padding the inside of the column,
      before the deliberate 86px gap even started.
    </p>

    <p>
      The fix is small: size both columns to their content and center the pair as
      a unit, rather than handing one of them a fraction of the viewport and
      capping what goes in it. The general form of the mistake is worth naming,
      because it will happen again:
    </p>

    <blockquote>
      <code>fr</code> sizes a column. <code>max-width</code> sizes the content
      inside it. When they disagree, the difference becomes invisible dead space.
    </blockquote>

    <p>
      Invisible is the operative word. Empty space is not overflow. Nothing
      escapes the viewport, nothing is clipped, no element is undersized, no
      target is too small. Every assertion in the probe was true, and the probe
      was right to pass it. The layout was still wrong.
    </p>

    <h2>The part that generalises</h2>

    <p>
      There is a comfortable story where the automated check is the rigorous part
      and looking at it is the soft part. That is not what happened. The probe
      caught three real defects that no amount of staring would have surfaced,
      including two that are literally invisible: a 38px tap target and a 40px one
      look identical to a 44px one. And then a human glance caught a fourth that
      the probe was structurally incapable of seeing, because nobody had thought
      to assert on the absence of content.
    </p>

    <p>
      Both instruments were necessary and neither was sufficient. The failure
      mode to avoid is not skipping one of them. It is believing that the one you
      ran covers the ground the other one covers, and reading a green result as
      a broader claim than the assertions actually made.
    </p>

    <p>
      A checker tells you that the things you thought to measure are fine. It
      cannot tell you whether you measured the right things. That second question
      does not have an automated answer, and pretending otherwise is how a suite
      full of green checks ships a page that looks broken to everyone who opens it.
    </p>

    <p class="sig">
      The signup design itself is not live yet: the site has no account system
      behind it. The layout is settled and measured, and the auth work is the
      next job.
    </p>

  </div>
</article>

<style>
  .back {
    display: inline-block;
    width: fit-content;
    align-self: start;
    margin: 1.4rem 0 0 1.4rem;
    font-family: ui-monospace, 'JetBrains Mono', Menlo, monospace;
    font-size: 0.74rem;
    text-decoration: none;
    color: #94a3b8;
    border: 1px solid #1e293b;
    border-radius: 999px;
    padding: 0.35rem 0.8rem;
  }
  .back:hover { color: #f1f5f9; border-color: #64748b; }

  .post {
    max-width: 44rem;
    margin: 0 auto;
    padding: 2.5rem 1.25rem 5rem;
    color: #e6edf7;
    font-size: 1.06rem;
    line-height: 1.7;
  }

  .kicker {
    font-family: ui-monospace, 'JetBrains Mono', Menlo, monospace;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #f59e0b;
    margin: 0 0 0.9rem;
  }
  h1 {
    font-size: clamp(2rem, 6.5vw, 3.2rem);
    line-height: 1.04;
    letter-spacing: -0.035em;
    margin: 0 0 0.9rem;
    font-weight: 800;
  }
  .dek {
    font-size: clamp(1.02rem, 2.4vw, 1.2rem);
    color: #93a1b8;
    margin: 0 0 1.4rem;
    line-height: 1.6;
  }
  .meta {
    font-family: ui-monospace, 'JetBrains Mono', Menlo, monospace;
    font-size: 0.74rem;
    color: #64748b;
    margin: 0;
    padding-bottom: 1.6rem;
    border-bottom: 1px solid #232b39;
  }
  .dot { margin: 0 0.5rem; color: #334155; }

  .body { padding-top: 2.2rem; }
  h2 {
    font-size: clamp(1.35rem, 3.2vw, 1.85rem);
    line-height: 1.2;
    letter-spacing: -0.018em;
    margin: 3.4rem 0 0.9rem;
    font-weight: 700;
  }
  p { margin: 0 0 1.15rem; }
  em { color: #cbd5e1; }
  strong { color: #f8fafc; font-weight: 600; }

  ul { margin: 0 0 1.15rem; padding-left: 1.1rem; }
  li { margin-bottom: 0.85rem; }

  code {
    font-family: ui-monospace, 'JetBrains Mono', Menlo, monospace;
    font-size: 0.86em;
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.09);
    padding: 0.1em 0.36em;
    border-radius: 4px;
  }

  blockquote {
    margin: 1.6rem 0;
    padding: 1rem 1.2rem;
    border-left: 2px solid #f59e0b;
    background: rgba(245, 158, 11, 0.05);
    color: #cbd5e1;
  }

  .fig { margin: 2rem 0; }
  .fig svg { width: 100%; height: auto; display: block; border-radius: 10px; }
  figcaption {
    margin-top: 0.7rem;
    font-size: 0.86rem;
    color: #64748b;
    line-height: 1.55;
  }
  .lbl { fill: #f59e0b; font-family: ui-monospace, monospace; font-size: 10px; letter-spacing: 0.14em; }
  .tx  { fill: #cbd5e1; font-family: ui-monospace, monospace; font-size: 10px; }
  .bad { fill: #f87171; font-family: ui-monospace, monospace; font-size: 10px; }
  .ok  { fill: #34d399; font-family: ui-monospace, monospace; font-size: 10px; }

  .sig {
    margin-top: 2.6rem;
    padding-top: 1.4rem;
    border-top: 1px solid #232b39;
    color: #64748b;
    font-size: 0.94rem;
  }
</style>
