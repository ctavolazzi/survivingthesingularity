import { json } from '@sveltejs/kit';
import { rateLimit } from '$lib/server/rateLimit.js';

const ALLOWED_HOSTS = new Set([
  'arxiv.org',
  'www.arxiv.org',
  'situational-awareness.ai',
  'github.com',
  'www.github.com',
  'youtube.com',
  'www.youtube.com',
  'substack.com'
]);

const PRIVATE_IP = /^(10\.|127\.|0\.|169\.254\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|::1$|fc|fd|fe80:)/i;
const FETCH_TIMEOUT_MS = 4000;
const MAX_BYTES = 256 * 1024;

function isHostAllowed(hostname) {
  if (!hostname) return false;
  if (PRIVATE_IP.test(hostname)) return false;
  if (hostname === 'localhost') return false;
  if (ALLOWED_HOSTS.has(hostname)) return true;
  for (const allowed of ALLOWED_HOSTS) {
    if (hostname.endsWith('.' + allowed)) return true;
  }
  return false;
}

export async function GET({ url, getClientAddress }) {
  const ip = getClientAddress();
  const { allowed } = rateLimit(`fetch-title:${ip}`, 10, 60_000);
  if (!allowed) {
    return json({ error: 'Too many requests.' }, { status: 429 });
  }

  const targetUrl = url.searchParams.get('url');
  if (!targetUrl) {
    return json({ error: 'URL parameter is required' }, { status: 400 });
  }

  let parsed;
  try {
    parsed = new URL(targetUrl);
  } catch {
    return json({ error: 'Invalid URL' }, { status: 400 });
  }

  if (parsed.protocol !== 'https:') {
    return json({ error: 'Only https URLs allowed' }, { status: 400 });
  }
  if (!isHostAllowed(parsed.hostname)) {
    return json({ error: 'Host not allowed' }, { status: 403 });
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  try {
    const response = await fetch(parsed.toString(), {
      redirect: 'manual',
      signal: controller.signal,
      headers: { 'User-Agent': 'STS-TitleBot/1.0' }
    });
    if (response.status >= 300 && response.status < 400) {
      return json({ error: 'Redirects not allowed' }, { status: 400 });
    }
    if (!response.ok) {
      return json({ error: 'Upstream error' }, { status: 502 });
    }

    const reader = response.body?.getReader();
    if (!reader) return json({ title: parsed.hostname });

    const decoder = new TextDecoder();
    let html = '';
    let received = 0;
    while (received < MAX_BYTES) {
      const { done, value } = await reader.read();
      if (done) break;
      received += value.byteLength;
      html += decoder.decode(value, { stream: true });
      const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
      if (m) {
        try { await reader.cancel(); } catch {}
        return json({ title: m[1].trim().slice(0, 300) });
      }
    }
    return json({ title: parsed.hostname });
  } catch (error) {
    if (error?.name === 'AbortError') {
      return json({ error: 'Upstream timeout' }, { status: 504 });
    }
    return json({ error: 'Failed to fetch title' }, { status: 500 });
  } finally {
    clearTimeout(timer);
  }
}
