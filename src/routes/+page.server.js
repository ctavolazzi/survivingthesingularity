// The homepage is fully static content — prerender it so the launch spike is
// absorbed by the CDN edge instead of invoking a serverless function per view.
// (The previous server load fetched a waitlist count the page never rendered.)
export const prerender = true;
