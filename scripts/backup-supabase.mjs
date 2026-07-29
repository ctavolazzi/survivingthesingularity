#!/usr/bin/env node
/**
 * Nightly export of every Supabase table to a second physical location.
 *
 * WHY
 *
 * Until now the only copy of the customer data lived in one Supabase project on
 * a free plan. "Backed up" meant "Supabase presumably has backups", which is a
 * belief about someone else's infrastructure rather than a copy you control. A
 * dropped table, a mistaken migration, or an account problem would have taken
 * the waitlist, the preorders and the entire payment ledger with it.
 *
 * This writes a full, timestamped, checksummed copy onto local disk. It is
 * deliberately boring: plain JSON, no dependencies, no service to keep running.
 *
 * WHAT IT IS NOT
 *
 * This is not point-in-time recovery and does not pretend to be. It is the
 * second copy, so that losing the first is survivable rather than fatal.
 *
 * USAGE
 *
 *   node scripts/backup-supabase.mjs
 *   BACKUP_DIR=/Volumes/External/sts node scripts/backup-supabase.mjs
 *
 * Reads SUPABASE_URL and SUPABASE_SERVICE_KEY from the .env alongside the
 * canonical working copy. Exits non-zero on any failure, so cron or launchd
 * surfaces a broken backup instead of silently producing nothing - a backup
 * that fails quietly is worse than no backup, because you stop checking.
 */
import { readFileSync, mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, resolve } from 'node:path';
import { homedir } from 'node:os';

// The .env with real credentials lives with the deploy copy, not this one.
const ENV_PATH = process.env.STS_ENV_PATH
  || join(homedir(), 'Code/active/survivingthesingularity/.env');

// Default output is OUTSIDE the repository on purpose. These files contain
// customer email addresses and payment references; a backup that lands inside a
// git worktree is one `git add -A` away from being published to GitHub.
const OUT_ROOT = process.env.BACKUP_DIR
  || join(homedir(), 'Backups/sts-supabase');

const TABLES = [
  'waitlist',
  'preorders',
  'fulfilled_sessions',
  'discord_applications',
  'email_deliveries',
  'checkout_transactions',
];

const PAGE = 1000; // PostgREST's default ceiling; paginate rather than assume.

function readEnv(path) {
  if (!existsSync(path)) fail(`no .env at ${path} (set STS_ENV_PATH to override)`);
  const out = {};
  for (const line of readFileSync(path, 'utf8').split('\n')) {
    const m = line.match(/^([A-Z_][A-Z0-9_]*)=(.*)$/);
    if (m) out[m[1]] = m[2].trim().replace(/^["']|["']$/g, '');
  }
  return out;
}

function fail(msg) {
  console.error(`\n  FAILED: ${msg}\n`);
  process.exit(1);
}

/** Fetch every row of a table, following pagination to the end. */
async function fetchAll(base, key, table) {
  const headers = { apikey: key, Authorization: `Bearer ${key}` };
  const rows = [];
  for (let offset = 0; ; offset += PAGE) {
    const url = `${base}/rest/v1/${table}?select=*&limit=${PAGE}&offset=${offset}`;
    const res = await fetch(url, { headers });
    if (!res.ok) {
      throw new Error(`${table}: HTTP ${res.status} ${(await res.text()).slice(0, 200)}`);
    }
    const page = await res.json();
    rows.push(...page);
    // A short page means we reached the end. Checking length rather than
    // trusting a count header keeps this correct if rows are written mid-run.
    if (page.length < PAGE) break;
  }
  return rows;
}

/** Authoritative row count straight from PostgREST, for cross-checking. */
async function exactCount(base, key, table) {
  const res = await fetch(`${base}/rest/v1/${table}?select=*`, {
    method: 'HEAD',
    headers: {
      apikey: key,
      Authorization: `Bearer ${key}`,
      Prefer: 'count=exact',
      Range: '0-0',
    },
  });
  const range = res.headers.get('content-range');
  return range ? Number(range.split('/')[1]) : null;
}

const env = readEnv(ENV_PATH);
const base = env.SUPABASE_URL;
const key = env.SUPABASE_SERVICE_KEY;
if (!base || !key) fail('SUPABASE_URL or SUPABASE_SERVICE_KEY missing from .env');

// Timestamp to the minute so two runs on one day cannot silently overwrite each
// other. An overwritten backup is an undetectable loss of the very history the
// backup exists to preserve.
const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 16);
const outDir = resolve(OUT_ROOT, stamp);

if (outDir.includes('/Code/active/sts-v0.7.3')) {
  fail('refusing to write customer data inside the git worktree');
}

mkdirSync(outDir, { recursive: true });
console.log(`\n  source : ${base}`);
console.log(`  target : ${outDir}\n`);

const manifest = { generated_at: new Date().toISOString(), source: base, tables: {} };
let failures = 0;

for (const table of TABLES) {
  try {
    const [rows, expected] = await Promise.all([
      fetchAll(base, key, table),
      exactCount(base, key, table),
    ]);

    const body = JSON.stringify(rows, null, 2);
    const sha256 = createHash('sha256').update(body).digest('hex');
    writeFileSync(join(outDir, `${table}.json`), body);

    // Verify rather than assume. If the paginated read disagrees with the
    // server's own count, the file is incomplete and saying "backed up" would
    // be a lie that only surfaces during a restore.
    const complete = expected === null || rows.length === expected;
    manifest.tables[table] = { rows: rows.length, expected, complete, sha256 };

    if (!complete) {
      failures++;
      console.log(`  ${table.padEnd(24)} ${String(rows.length).padStart(5)} rows  MISMATCH (server says ${expected})`);
    } else {
      console.log(`  ${table.padEnd(24)} ${String(rows.length).padStart(5)} rows  ${sha256.slice(0, 12)}`);
    }
  } catch (e) {
    failures++;
    manifest.tables[table] = { error: String(e.message ?? e) };
    console.log(`  ${table.padEnd(24)} ERROR  ${e.message ?? e}`);
  }
}

manifest.ok = failures === 0;
writeFileSync(join(outDir, 'manifest.json'), JSON.stringify(manifest, null, 2));

const total = Object.values(manifest.tables).reduce((n, t) => n + (t.rows ?? 0), 0);
console.log(`\n  ${total} rows across ${TABLES.length} tables`);

if (failures) fail(`${failures} table(s) did not back up cleanly - see manifest.json`);
console.log(`  manifest: ${join(outDir, 'manifest.json')}\n`);
