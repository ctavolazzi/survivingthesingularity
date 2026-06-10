// Shouse-themed event table. Event discipline (no events before day 5,
// 3-day spacing, stage gating, deterministic 2-day forecast) adapted from
// Johnny Autoseed's homestead-engine.

export const EVENTS = [
	{
		id: 'heatwave',
		name: 'Heat wave',
		msg: 'Scorching temps. Water drains 2x for 3 days.',
		icon: 'sun',
		duration: 3,
		effect: 'water_drain_2x',
		minStage: 3
	},
	{
		id: 'grid_outage',
		name: 'Grid outage',
		msg: 'The county grid drops. -15 power, no grid regen for 2 days.',
		icon: 'zap-off',
		duration: 2,
		effect: 'power_regen_zero',
		instant: { power: -15 },
		minStage: 3
	},
	{
		id: 'county_inspection',
		name: 'County inspection',
		msg: 'Inspector on site. $400 in fees, builds locked for 2 days.',
		icon: 'clipboard',
		duration: 2,
		effect: 'build_lock',
		instant: { cash: -400 },
		minStage: 1
	},
	{
		id: 'gpu_spike',
		name: 'GPU price spike',
		msg: 'Used GPU market jumps. Crucible costs +$400 while it lasts — or pays +$60/day if yours is already racked.',
		icon: 'cpu',
		duration: 3,
		effect: 'gpu_market',
		minStage: 0
	},
	{
		id: 'rain_storm',
		name: 'Rain storm',
		msg: 'Heavy rain. Free +25 water.',
		icon: 'cloud-rain',
		duration: 0,
		effect: 'instant',
		instant: { water: 25 },
		minStage: 3
	},
	{
		id: 'storm_winds',
		name: 'High winds',
		msg: 'Gusts batter the site. -15 power, loose materials damaged.',
		icon: 'wind',
		duration: 0,
		effect: 'wind_damage',
		instant: { power: -15 },
		minStage: 0
	},
	{
		id: 'scavenger_find',
		name: 'Scavenger find',
		msg: 'Surplus auction score. Next build stage costs 15% less.',
		icon: 'package',
		duration: 0,
		effect: 'discount_next',
		minStage: 0
	},
	{
		id: 'neighbor_barter',
		name: 'Neighbor barter',
		msg: 'A neighbor trades water and generator time for shop hours. +10 water, +10 power.',
		icon: 'handshake',
		duration: 0,
		effect: 'instant',
		instant: { water: 10, power: 10 },
		minStage: 3
	},
	{
		id: 'freight_delay',
		name: 'Freight delay',
		msg: 'Carrier lost the booking. Builds locked for 2 days.',
		icon: 'truck',
		duration: 2,
		effect: 'build_lock',
		minStage: 1,
		maxStage: 5
	},
	{
		id: 'sponsor_deal',
		name: 'Sponsor deal',
		msg: 'A tool brand sponsors the build series. +$500.',
		icon: 'coins',
		duration: 0,
		effect: 'instant',
		instant: { cash: 500 },
		minStage: 5
	}
];

export function getEvent(id) {
	return EVENTS.find((e) => e.id === id) || null;
}

// Deterministic 2-day weather forecast. Same seeding trick as the original
// engine so forecasts never contradict themselves between renders.
export function generateForecast(day, maxDay) {
	const forecast = [];
	for (let d = 1; d <= 2; d++) {
		const futureDay = day + d;
		if (futureDay > maxDay) continue;
		if (futureDay < 5) {
			forecast.push({ day: futureDay, icon: 'sun', label: 'Clear' });
			continue;
		}
		const seed = (futureDay * 7919 + 31) % 100;
		if (seed < 15) forecast.push({ day: futureDay, icon: 'cloud-rain', label: 'Rain likely' });
		else if (seed < 25) forecast.push({ day: futureDay, icon: 'sun', label: 'Heat risk' });
		else if (seed < 35) forecast.push({ day: futureDay, icon: 'wind', label: 'Winds' });
		else if (seed < 42) forecast.push({ day: futureDay, icon: 'cloud', label: 'Overcast' });
		else forecast.push({ day: futureDay, icon: 'sun', label: 'Clear' });
	}
	return forecast;
}
