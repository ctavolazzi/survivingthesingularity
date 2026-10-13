// Never print the report: it contains customer addresses and purchase references.
const origin = process.env.RECONCILE_ORIGIN || 'https://survivingthesingularity.com';
const token = process.env.ADMIN_RECONCILE_TOKEN;
if (!token || token.length < 32) throw new Error('Configure ADMIN_RECONCILE_TOKEN in the monitor secret store');
const endpoint = new URL('/api/admin/reconcile', origin);
if (endpoint.protocol !== 'https:') throw new Error('Reconciliation requires HTTPS');
const response = await fetch(endpoint, {
  headers: { authorization: `Bearer ${token}` },
  redirect: 'error',
  signal: AbortSignal.timeout(60_000)
});
if (!response.ok) throw new Error(`Reconciliation unavailable (HTTP ${response.status})`);
const report = await response.json();
if (!report.ok || !report.configured || !Number.isInteger(report.count)) {
  throw new Error('Reconciliation incomplete; inspect the protected report');
}
if (report.count > 0) throw new Error(`${report.count} payment record(s) need operator review`);
console.log(`Reconciliation passed; checked through ${report.checkedThrough}, ${report.scanned} Stripe sessions scanned.`);
