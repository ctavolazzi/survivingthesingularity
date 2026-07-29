<script>
  let email = $state('');
  let note = $state(
    'Demo build. This field validates and reports back. It stores nothing and sends nothing.'
  );
  /** @type {'' | 'ok' | 'bad'} */
  let noteKind = $state('');
  let invalid = $state(false);
  /** @type {HTMLInputElement | undefined} */
  let input = $state();

  const steps = [
    {
      n: '01',
      title: 'Something happens.',
      detail: 'A model ships, a price collapses, a policy lands, a factory turns on.'
    },
    {
      n: '02',
      title: 'It gets checked against the argument.',
      detail: 'Most things do not change it. That is the point of having one.'
    },
    {
      n: '03',
      title: 'If the argument changes, the book changes.',
      detail: 'The section is revised, and you get told what changed and why.'
    }
  ];

  /** @param {SubmitEvent} e */
  function onsubmit(e) {
    e.preventDefault();
    const value = email.trim();

    if (!value) {
      note = 'Enter an email address first.';
      noteKind = 'bad';
      invalid = true;
      input?.focus();
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
      note = 'That does not look like a valid address.';
      noteKind = 'bad';
      invalid = true;
      input?.focus();
      return;
    }

    // It stops here on purpose. A demo with no privacy policy behind it has no
    // business holding a real address.
    invalid = false;
    noteKind = 'ok';
    note = 'Valid. In production this would be stored and confirmed. This demo stored nothing.';
  }
</script>

<section class="band" id="updates">
  <div class="wrap">
    <p class="kicker">The update engine</p>
    <h2 class="sec-h2">The book is the artifact. The updates are the product.</h2>

    <ol class="steps">
      {#each steps as s (s.n)}
        <li>
          <span class="step-n">{s.n}</span>
          <b>{s.title}</b>
          {s.detail}
        </li>
      {/each}
    </ol>

    <div class="cadence">
      <p>
        <b>No schedule.</b> You hear from me when the argument changes, and not
        otherwise. No weekly send, no filler, no "just checking in."
      </p>
    </div>

    <form class="signup" {onsubmit} novalidate>
      <label class="signup-l" for="email">Get the updates</label>
      <div class="signup-row">
        <input
          bind:this={input}
          bind:value={email}
          type="email"
          id="email"
          name="email"
          placeholder="you@example.com"
          autocomplete="email"
          spellcheck="false"
          aria-invalid={invalid}
          oninput={() => (invalid = false)}
        />
        <button class="btn btn-primary" type="submit">Notify me</button>
      </div>

      <p class="signup-note" class:is-ok={noteKind === 'ok'} class:is-bad={noteKind === 'bad'} role="status" aria-live="polite">
        {note}
      </p>

      <p class="signup-fine">
        One click to unsubscribe, in every message, and the link is right here
        too. Not buried in a footer.
      </p>
    </form>
  </div>
</section>

<style>
  .steps {
    list-style: none;
    margin: 0 0 28px;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
  .steps li {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 22px 20px;
    font-size: 15.5px;
    color: var(--text-2);
  }
  .steps b {
    display: block;
    color: var(--text);
    margin: 12px 0 6px;
    font-size: 16px;
  }
  .step-n {
    font: 600 12px/1 var(--mono);
    letter-spacing: 0.1em;
    color: var(--accent);
  }

  .cadence {
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 18px 22px;
    margin-bottom: 36px;
    background: var(--surface);
  }
  .cadence p { margin: 0; font-size: 15.5px; color: var(--text-2); }
  .cadence b { color: var(--text); }

  .signup {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: clamp(22px, 3vw, 32px);
    max-width: 660px;
  }
  .signup-l {
    display: block;
    font: 600 13px/1 var(--mono);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 14px;
  }
  .signup-row { display: flex; gap: 10px; flex-wrap: wrap; }
  .signup-row input {
    flex: 1 1 260px;
    min-width: 0;
    background: var(--bg);
    border: 1px solid var(--border-2);
    border-radius: var(--r);
    padding: 14px 16px;
    color: var(--text);
    font: 400 16px/1.2 var(--sans);
  }
  .signup-row input::placeholder { color: var(--text-3); }
  .signup-row input:focus { border-color: var(--accent); outline: none; }
  .signup-row input[aria-invalid='true'] { border-color: var(--bad); }

  .signup-note {
    font: 400 13.5px/1.55 var(--mono);
    color: var(--text-3);
    margin: 14px 0 0;
  }
  .signup-note.is-ok { color: var(--ok); }
  .signup-note.is-bad { color: var(--bad); }

  .signup-fine {
    font-size: 13.5px;
    color: var(--text-3);
    margin: 12px 0 0;
  }

  @media (max-width: 940px) {
    .steps { grid-template-columns: 1fr; }
  }
</style>
