// The six build stages of the ultimate shouse, mapped from the $25k BOM
// in Blueprint Chapter 02 (The Shouse) and the autoseed-systems exit-strategy
// chapter. Costs total $25,400 against a $25,000 start: the player closes the
// gap with rent savings, the content engine, or a lucky scavenger find.

export const STAGES = [
	{
		id: 'foundation',
		buildDays: 3,
		name: 'Site Prep & Foundation',
		shortName: 'Foundation',
		cost: 3000,
		waterDrain: 0,
		powerDrain: 0,
		incomePerDay: 0,
		needsResources: false,
		blueprintSlug: 'physical-exit',
		blueprintTitle: 'The Physical Exit',
		desc: 'Grade the pad, set gravel, pour the piers. Everything else lands on this.',
		lesson: 'Site prep runs $2-4k. Cheap land with bad drainage is expensive land.'
	},
	{
		id: 'container',
		buildDays: 2,
		name: 'Container Shell',
		shortName: 'Container',
		cost: 5500,
		waterDrain: 0,
		powerDrain: 0,
		incomePerDay: 0,
		needsResources: false,
		blueprintSlug: 'the-shouse',
		blueprintTitle: 'The Shouse',
		desc: 'A 40ft high-cube shipping container, craned onto the piers. 2/3 shop, 1/3 living.',
		lesson: 'One-trip containers run $2.5-9k delivered. The hull of industrial civilization becomes your walls.'
	},
	{
		id: 'utilities',
		buildDays: 5,
		name: 'Utilities Rough-In',
		shortName: 'Utilities',
		cost: 7000,
		waterDrain: 4,
		powerDrain: 3,
		incomePerDay: 0,
		needsResources: false,
		blueprintSlug: 'the-shouse',
		blueprintTitle: 'The Shouse',
		desc: '200A panel, plumbing runs, closed-cell foam insulation. Water and power systems go live.',
		lesson: 'Licensed electrical inspection is non-negotiable. Closed-cell foam doubles as your vapor barrier.'
	},
	{
		id: 'living',
		buildDays: 2,
		name: 'Living Quarters',
		shortName: 'Living',
		cost: 3500,
		waterDrain: 3,
		powerDrain: 3,
		incomePerDay: 60,
		incomeLabel: 'rent savings',
		needsResources: true,
		blueprintSlug: 'the-shouse',
		blueprintTitle: 'The Shouse',
		desc: 'RV ramps into the shop bay as the caretaker unit. You move in — rent payments stop.',
		lesson: 'The RV sidesteps residential code: a "tractor repair shop with accessory caretaker unit." +$60/day stays in your pocket.'
	},
	{
		id: 'crucible',
		buildDays: 2,
		name: 'The Crucible + Mesh',
		shortName: 'Crucible',
		cost: 1800,
		waterDrain: 0,
		powerDrain: 8,
		incomePerDay: 140,
		incomeLabel: 'content engine',
		needsResources: true,
		blueprintSlug: 'digital-sovereignty',
		blueprintTitle: 'Digital Sovereignty',
		desc: '48U rack: surplus GPU server, UPS, switch, NAS, mesh antenna. Local AI comes online.',
		lesson: 'Surplus Xeons + a used RTX card run 70B-class models for under $2k. The rack powers the content engine: +$140/day.'
	},
	{
		id: 'solar_farmbot',
		buildDays: 3,
		name: 'Solar + FarmBot',
		shortName: 'Solar+Bot',
		cost: 4600,
		waterDrain: 2,
		powerDrain: 0,
		powerRegen: 14,
		incomePerDay: 0,
		needsResources: true,
		blueprintSlug: 'robotics',
		blueprintTitle: 'Open-Source Robotics',
		desc: 'Ground-mount solar with LiFePO4 storage, plus a FarmBot gantry over an 8×4 bed.',
		lesson: 'Solar regen makes the grid optional. The FarmBot turns sunlight into groceries while you sleep.'
	}
];

export const TOTAL_BUILD_COST = STAGES.reduce((s, st) => s + st.cost, 0);

export function getStage(index) {
	return STAGES[index] || null;
}
