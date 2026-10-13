import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { isSameOrigin } from '../../src/lib/server/sameOrigin.js';

// Execute the actual route functions with database and email adapters replaced.
// These fault-injection tests send no requests and need no service credentials.
function loadRoute(path, dependencies) {
  const source = readFileSync(new URL(`../../${path}`, import.meta.url), 'utf8')
    .replace(/^import .*;\r?\n/gm, '')
    .replace(/^export /gm, '');
  return Function(...Object.keys(dependencies), `${source}\nreturn { POST };`)(...Object.values(dependencies));
}

const common = {
  isSameOrigin,
  json: (body, init) => Response.json(body, init),
  console: { error() {}, warn() {} },
};

function requestEvent(path, body) {
  const url = new URL(path, 'https://example.invalid');
  return {
    url,
    request: new Request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Origin: url.origin },
      body: JSON.stringify(body),
    }),
    getClientAddress: () => '192.0.2.1',
  };
}

function waitlistFixture(insertError = null) {
  const inserts = [];
  const welcomes = [];
  const supabaseAdmin = {
    from(table) {
      assert.equal(table, 'waitlist');
      return {
        async insert(row) { inserts.push(row); return { error: insertError }; },
        select() { return { eq() { return { async single() { return { data: { unsubscribe_token: 'test-token' } }; } }; } }; },
      };
    },
  };
  const { POST } = loadRoute('src/routes/api/waitlist/+server.js', {
    ...common,
    supabaseAdmin,
    rateLimit: () => ({ allowed: true }),
    sendWelcomeEmail: async (args) => { welcomes.push(args); return { ok: true }; },
  });
  return { POST, inserts, welcomes };
}

for (const code of ['42703', 'PGRST204']) {
  test(`missing consent schema (${code}) fails closed without a second insert or welcome`, async () => {
    const { POST, inserts, welcomes } = waitlistFixture({ code });
    const response = await POST(requestEvent('/api/waitlist', {
      email: 'reader@example.invalid', newsletter_consent: true, book_release_consent: false,
    }));
    assert.equal(response.status, 503);
    assert.match((await response.json()).error, /temporarily unavailable/);
    assert.equal(inserts.length, 1);
    assert.equal(inserts[0].newsletter_consent, true);
    assert.equal(inserts[0].book_release_consent, false);
    assert.equal(welcomes.length, 0);
  });
}

test('a duplicate address preserves existing preferences and does not send another welcome', async () => {
  const { POST, inserts, welcomes } = waitlistFixture({ code: '23505' });
  const response = await POST(requestEvent('/api/waitlist', {
    email: 'reader@example.invalid', newsletter_consent: true, book_release_consent: true,
  }));
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'already_subscribed');
  assert.match(body.message, /preferences have not changed/);
  assert.equal(inserts.length, 1);
  // The fake exposes no update or upsert: either would fail this test.
  assert.equal(welcomes.length, 0);
});

test('a successful signup records explicit opt-outs and sends the unsubscribe token', async () => {
  const { POST, inserts, welcomes } = waitlistFixture();
  const response = await POST(requestEvent('/api/waitlist', {
    email: ' Reader@Example.invalid ', newsletter_consent: false, book_release_consent: false,
  }));
  assert.equal(response.status, 201);
  assert.deepEqual(inserts, [{
    email: 'reader@example.invalid', source: 'homepage', newsletter_consent: false, book_release_consent: false,
  }]);
  assert.deepEqual(welcomes, [{ to: 'reader@example.invalid', source: 'homepage', unsubscribeToken: 'test-token' }]);
});

function checklistFixture(sendChecklistEmail) {
  return loadRoute('src/routes/api/checklist-email/+server.js', {
    ...common,
    sendChecklistEmail,
    supabaseAdmin: {
      from() { return { select() { return { eq() { return { async maybeSingle() { return { data: { email: 'reader@example.invalid' } }; } }; } }; } }; },
    },
  });
}

const checklistRequest = () => requestEvent('/api/checklist-email', {
  email: 'reader@example.invalid',
  answers: [{ n: 1, title: 'Read <notes>', cat: 'foundation', checked: true, notes: '<script>unsafe</script>' }],
});

for (const [name, sendResult] of [
  ['missing email credentials', { skipped: true }],
  ['provider rejection', { error: { message: 'Unavailable' } }],
  ['missing provider result', undefined],
  ['ambiguous provider result', {}],
]) {
  test(`checklist ${name} reports unavailable instead of sent`, async () => {
    const { POST } = checklistFixture(async () => sendResult);
    const response = await POST(checklistRequest());
    assert.equal(response.status, 503);
    assert.equal((await response.json()).ok, undefined);
  });
}

test('a thrown email transport error produces a retryable response', async () => {
  const { POST } = checklistFixture(async () => { throw new Error('Simulated transport outage'); });
  const response = await POST(checklistRequest());
  assert.equal(response.status, 503);
  assert.match((await response.json()).error, /please try again later/);
});

test('checklist reports success only after acceptance and still escapes user notes', async () => {
  let sent;
  const { POST } = checklistFixture(async (args) => { sent = args; return { ok: true }; });
  const response = await POST(checklistRequest());
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { ok: true });
  assert.equal(sent.answers[0].notes, '&lt;script&gt;unsafe&lt;/script&gt;');
  assert.equal(sent.answers[0].title, 'Read &lt;notes&gt;');
});
