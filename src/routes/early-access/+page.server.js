import { sections } from '$lib/data/blueprint.js';
import signalsData from '$lib/data/signals.json';
import { getWaitlistCount } from '$lib/server/supabaseAdmin.js';

// Keep SSR: shows the live waitlist count and most-recent signals. Opting out
// so the homepage-driven prerender crawl doesn't try to bake this page.
export const prerender = false;

// Only surface a signup count once it's genuinely impressive. Below this it
// reads as "nobody signed up" and hurts conversion, so we hide it entirely.
const SOCIAL_PROOF_THRESHOLD = 100;

// Early Access hub. Surfaces the blueprint chapters, the most recent research
// signals, and (downstream) the full readiness checklist behind a single
// email gate. Chapter and signal data are pulled from the same sources the
// rest of the site uses so this page never drifts out of sync.
export async function load() {
  const chapters = sections.map((s) => ({
    number: s.number,
    title: s.title,
    subtitle: s.subtitle,
    slug: s.slug,
  }));

  const recentSignals = [...signalsData.items]
    .sort((a, b) => String(b.published_at).localeCompare(String(a.published_at)))
    .slice(0, 4)
    .map((s) => ({
      id: s.id,
      title: s.title,
      url: s.url,
      tag: s.tag,
      published_at: s.published_at,
    }));

  let count = 0;
  try {
    count = await getWaitlistCount();
  } catch {
    count = 0;
  }
  const signupCount =
    typeof count === 'number' && count >= SOCIAL_PROOF_THRESHOLD ? count : null;

  return {
    chapters,
    recentSignals,
    signalsUpdated: signalsData.generated_at,
    signupCount,
  };
}
