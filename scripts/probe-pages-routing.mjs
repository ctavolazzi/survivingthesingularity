#!/usr/bin/env node
/**
 * probe-pages-routing.mjs - will Cloudflare Pages actually serve this path?
 *
 * Why this exists
 * ---------------
 * On 2026-08-01 the /factcheck page shipped with a button pointing at
 * /factcheck-trace.html. In production that returned 308 -> /factcheck-trace
 * -> 404, while every local check said the file was fine. It was fine: the
 * 1.1 MB asset was committed, deployed, and reachable by Pages. What failed
 * was ROUTING.
 *
 * adapter-cloudflare emits a _routes.json telling Pages which paths skip the
 * Worker. Cloudflare caps that file at 100 rules. This site blew the cap and
 * the adapter dropped 624 exclude rules, so most paths now reach the Worker
 * first. The Worker then decides, in files/worker.js:
 *
 *     is_static_asset = manifest.assets.has(filename)
 *                    || manifest.assets.has(filename + "/index.html");
 *     if (is_static_asset || prerendered.has(pathname) || ...) ASSETS.fetch()
 *     else if (prerendered.has(pathname + "/"))                308
 *     else                                                     server.respond()
 *
 * "factcheck-trace" is not an asset. "factcheck-trace/index.html" was not an
 * asset. It is not a prerendered route. So it fell through to SvelteKit, which
 * has no such route, and answered 404. A root-level static .html is reachable
 * only at its .html name, and Pages redirects that name away.
 *
 * This probe replays that exact predicate against a real build, so the failure
 * is visible before a deploy instead of after one.
 *
 * `npm run build` locally uses adapter-auto, which picks Cloudflare only when
 * CF_PAGES is set. Build the way production builds:
 *
 *     npm install --no-save @sveltejs/adapter-cloudflare@3
 *     CF_PAGES=1 npm run build
 *     node scripts/probe-pages-routing.mjs
 *
 * Exits non-zero if any checked path would not be served.
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

// Paths that must resolve to real content in production. Add to this list
// whenever a page links to something that is not a SvelteKit route.
const MUST_SERVE = [
	'/',
	'/factcheck',
	'/factcheck-trace/',
	'/workshop',
	'/devlog'
];

const MANIFEST = resolve('.svelte-kit/cloudflare-tmp/manifest.js');
const ROUTES = resolve('.svelte-kit/cloudflare/_routes.json');

if (!existsSync(MANIFEST)) {
	console.error(
		`no build output at ${MANIFEST}\n` +
			'run: npm install --no-save @sveltejs/adapter-cloudflare@3 && CF_PAGES=1 npm run build'
	);
	process.exit(2);
}

const { manifest, prerendered } = await import(MANIFEST);
const assets = manifest.assets;

/**
 * The adapter-cloudflare worker's routing decision, transcribed. Keep this in
 * step with node_modules/@sveltejs/adapter-cloudflare/files/worker.js.
 */
function classify(pathname) {
	const stripped = pathname.replace(/\/$/, '');
	const filename = stripped.substring(1);

	let is_static_asset = false;
	if (filename) {
		is_static_asset = assets.has(filename) || assets.has(filename + '/index.html');
	}

	if (is_static_asset) return { served: true, via: 'static asset' };
	if (prerendered.has(pathname)) return { served: true, via: 'prerendered' };

	const location = pathname.at(-1) === '/' ? stripped : pathname + '/';
	if (location && prerendered.has(location)) {
		return { served: true, via: `308 -> ${location}` };
	}

	// Reaches SvelteKit. That is correct for a real route and a 404 otherwise,
	// which this probe cannot tell apart without booting the Worker. Anything
	// the site links to as a static file must not land here.
	return { served: false, via: 'SvelteKit worker (404 unless a real route)' };
}

const results = MUST_SERVE.map((p) => ({ path: p, ...classify(p) }));

let excludeCount = null;
if (existsSync(ROUTES)) {
	excludeCount = JSON.parse(readFileSync(ROUTES, 'utf8')).exclude.length;
}

const failures = results.filter((r) => !r.served);

const report = {
	generated: new Date().toISOString().slice(0, 10),
	assets: assets.size,
	prerendered: prerendered.size,
	routes_json_exclude_rules: excludeCount,
	routes_json_at_cap: excludeCount !== null && excludeCount >= 99,
	checked: results,
	failures: failures.length
};

if (process.argv.includes('--json')) {
	console.log(JSON.stringify(report, null, 2));
} else {
	console.log(`Pages routing probe - ${assets.size} assets, ${prerendered.size} prerendered`);
	if (report.routes_json_at_cap) {
		console.log(
			`  _routes.json is at the ${excludeCount}-rule cap, so most paths reach the Worker.\n` +
				'  Static files are only served if the Worker recognises them by name.'
		);
	}
	console.log('');
	for (const r of results) {
		console.log(`  ${r.served ? 'OK  ' : 'FAIL'}  ${r.path.padEnd(20)} ${r.via}`);
	}
	console.log('');
	console.log(failures.length ? `  ${failures.length} path(s) would not be served.` : '  All checked paths resolve.');
}

process.exit(failures.length ? 1 : 0);
