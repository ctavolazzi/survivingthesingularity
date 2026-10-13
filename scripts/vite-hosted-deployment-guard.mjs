async function inspectHosting() {
  // Load the CLI as native ESM. Vite 5's config bundler prepends import-meta
  // definitions before a bundled dependency's shebang, making that invalid JS.
  const checker = await import(new URL('./check-hosted-deployment.mjs', import.meta.url).href);
  return checker.runHostedDeploymentGate();
}

/** Build tooling only: no credentials or provider responses enter site output. */
export function hostedDeploymentGuard({ inspect = inspectHosting } = {}) {
  let ssr = false;
  let verification;
  return {
    name: 'sts-hosted-deployment-guard',
    apply: 'build',
    configResolved(config) {
      // SvelteKit also loads this config for its nested client build. The
      // server pass owns verification and must finish it before compiling.
      ssr = Boolean(config.build.ssr);
    },
    async buildStart() {
      if (!ssr) return;
      verification ??= (async () => {
        let report;
        try {
          report = await inspect();
        } catch {
          // Do not let a provider exception or credential-bearing URL become
          // a Vite error. The checker returns controlled diagnostics below.
          throw new Error('Hosted deployment verification could not complete; publication stopped.');
        }
        if (report.skipped && report.ok) return;
        for (const check of report.checks ?? []) {
          console.info(`[hosted deployment] ${check.id}: ${check.status} — ${check.detail}`);
        }
        if (!report.ok) {
          throw new Error('Hosted deployment prerequisites are unverified; publication stopped. See the hosted deployment checks above.');
        }
        console.info('[hosted deployment] Required configuration, exposed database interfaces and private bundle verified. This does not prove checkout or inbox delivery.');
      })();
      await verification;
    }
  };
}
