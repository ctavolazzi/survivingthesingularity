// Achievement definitions. check(state) runs against the live sim state.

export const ACHIEVEMENT_DEFS = [
	{
		id: 'first_pour',
		name: 'First Pour',
		desc: 'Complete the foundation',
		check: (s) => s.stage >= 1
	},
	{
		id: 'steel_on_dirt',
		name: 'Steel on Dirt',
		desc: 'Set the container shell',
		check: (s) => s.stage >= 2
	},
	{
		id: 'lights_on',
		name: 'Lights On',
		desc: 'Bring utilities online',
		check: (s) => s.stage >= 3
	},
	{
		id: 'move_in_day',
		name: 'Move-In Day',
		desc: 'Ramp the RV into the bay',
		check: (s) => s.stage >= 4
	},
	{
		id: 'crucible_hums',
		name: 'The Crucible Hums',
		desc: 'Rack the local AI core',
		check: (s) => s.stage >= 5
	},
	{
		id: 'closed_loop',
		name: 'Closed Loop',
		desc: 'Finish the shouse',
		check: (s) => s.won
	},
	{
		id: 'under_budget',
		name: 'Under Budget',
		desc: 'Win with $2,000+ still in hand',
		check: (s) => s.won && s.cash >= 2000
	},
	{
		id: 'storm_proof',
		name: 'Storm-Proof',
		desc: 'Win after surviving 5+ events',
		check: (s) => s.won && s.eventsTriggered >= 5
	}
];
