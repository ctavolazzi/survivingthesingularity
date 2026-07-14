import signalsData from '$lib/data/signals.json';

export function load() {
  return {
    items: signalsData.items,
    generatedAt: signalsData.generated_at,
    itemCount: signalsData.item_count,
  };
}
