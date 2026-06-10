// FarmBot crop data — 12-plant subset adapted from the Johnny Autoseed
// plant database (johnnyautoseed.com, src/data/plants.js). Real growing data,
// compressed to game time: gameDays = max(3, round(daysToMaturity / 10)).

function gameDays(realDays) {
	return Math.max(3, Math.round(realDays / 10));
}

// Sale price per harvest approximates yieldPerPlant (kg) x a category price.
export const CROP_PRESETS = [
	{
		id: 'greens',
		name: 'Greens Bed',
		desc: 'Fast, light harvests. Cash trickles in early.',
		plants: [
			{ id: 'lettuce-buttercrunch', name: 'Buttercrunch Lettuce', gameDays: gameDays(55), salePrice: 14, height: 15, category: 'leafy-green' },
			{ id: 'spinach', name: 'Spinach', gameDays: gameDays(40), salePrice: 11, height: 15, category: 'leafy-green' },
			{ id: 'arugula', name: 'Arugula', gameDays: gameDays(30), salePrice: 9, height: 20, category: 'leafy-green' },
			{ id: 'kale', name: 'Curly Kale', gameDays: gameDays(55), salePrice: 18, height: 40, category: 'leafy-green' }
		]
	},
	{
		id: 'roots',
		name: 'Roots Bed',
		desc: 'Steady mid-speed harvests.',
		plants: [
			{ id: 'carrots-nantes', name: 'Nantes Carrots', gameDays: gameDays(65), salePrice: 22, height: 30, category: 'root-vegetable' },
			{ id: 'radish', name: 'Cherry Belle Radish', gameDays: gameDays(22), salePrice: 8, height: 15, category: 'root-vegetable' },
			{ id: 'beets', name: 'Detroit Red Beets', gameDays: gameDays(55), salePrice: 20, height: 25, category: 'root-vegetable' },
			{ id: 'turnips', name: 'Purple Top Turnips', gameDays: gameDays(50), salePrice: 19, height: 30, category: 'root-vegetable' }
		]
	},
	{
		id: 'fruiting',
		name: 'Fruiting Bed',
		desc: 'Slow to mature, big paydays.',
		plants: [
			{ id: 'tomato-cherry', name: 'Cherry Tomatoes', gameDays: gameDays(65), salePrice: 42, height: 120, category: 'fruiting' },
			{ id: 'pepper-bell', name: 'Bell Peppers', gameDays: gameDays(75), salePrice: 38, height: 60, category: 'fruiting' },
			{ id: 'cucumber', name: 'Slicing Cucumber', gameDays: gameDays(60), salePrice: 35, height: 30, category: 'fruiting' },
			{ id: 'zucchini', name: 'Zucchini', gameDays: gameDays(50), salePrice: 48, height: 40, category: 'fruiting' }
		]
	}
];

export function getCropPreset(id) {
	return CROP_PRESETS.find((c) => c.id === id) || CROP_PRESETS[0];
}
