import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { once } from 'node:events';
import { requestJson, RequestTimeoutError } from '../../src/lib/requestJson.js';

async function withServer(handler, verify) {
  const server = createServer(handler);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  try { await verify(`http://127.0.0.1:${server.address().port}`); }
  finally { server.closeAllConnections(); await new Promise(resolve => server.close(resolve)); }
}

test('request deadline aborts a server that never sends headers', async () => {
  await withServer(() => {}, async url => {
    await assert.rejects(requestJson(url, {}, 40), RequestTimeoutError);
  });
});

test('request deadline also covers a stalled response body', async () => {
  await withServer((_req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.write('{"url":');
  }, async url => {
    await assert.rejects(requestJson(url, {}, 40), RequestTimeoutError);
  });
});

test('successful and malformed HTTP responses retain status without inventing data', async () => {
  await withServer((req, res) => {
    if (req.url === '/good') {
      res.writeHead(201, { 'Content-Type': 'application/json' });
      res.end('{"ok":true}');
    } else {
      res.writeHead(503, { 'Content-Type': 'text/html' });
      res.end('<h1>Unavailable</h1>');
    }
  }, async url => {
    const good = await requestJson(url + '/good');
    assert.equal(good.response.status, 201);
    assert.deepEqual(good.data, { ok: true });
    const bad = await requestJson(url + '/bad');
    assert.equal(bad.response.status, 503);
    assert.deepEqual(bad.data, {});
  });
});
