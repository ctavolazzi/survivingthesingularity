// Upgrade tree: one free choice of two offered alongside stages 3-6.
// The trade-off is the path not taken, not a price tag.

export const UPGRADE_TREE = [
	{
		stageIndex: 2, // offered when buying utilities (stage 3)
		label: 'Utilities Rough-In',
		options: [
			{
				id: 'pex_manifold',
				name: 'PEX Manifold',
				desc: 'Home-run plumbing. Water drain -30%.',
				color: '#3b82f6'
			},
			{
				id: 'pro_conduit',
				name: 'Pro Conduit Run',
				desc: 'Oversized conduit, clean runs. Power drain -25%.',
				color: '#f59e0b'
			}
		]
	},
	{
		stageIndex: 3, // offered with living quarters
		label: 'Living Quarters',
		options: [
			{
				id: 'rain_catchment',
				name: 'Rainwater Catchment',
				desc: 'Gutters + IBC totes off the container roof. +6 water/day.',
				color: '#3b82f6'
			},
			{
				id: 'wood_stove',
				name: 'Wood Stove',
				desc: 'Heat the living third for free. Living power drain -50%.',
				color: '#ef4444'
			}
		]
	},
	{
		stageIndex: 4, // offered with the Crucible
		label: 'The Crucible',
		options: [
			{
				id: 'quantized_models',
				name: 'Quantized Models',
				desc: 'Q4 quants on the GPU. Crucible power drain -40%.',
				color: '#a78bfa'
			},
			{
				id: 'sponsor_pipeline',
				name: 'Sponsor Pipeline',
				desc: 'Outreach templates in the rack. Content income +40%.',
				color: '#f59e0b'
			}
		]
	},
	{
		stageIndex: 5, // offered with solar + farmbot
		label: 'Solar + FarmBot',
		options: [
			{
				id: 'tracking_mounts',
				name: 'Tracking Mounts',
				desc: 'Panels follow the sun. Solar regen +50%.',
				color: '#f59e0b'
			},
			{
				id: 'lifepo4_expansion',
				name: 'LiFePO4 Expansion',
				desc: 'Double the bank. Power cap raised to 150.',
				color: '#10b981'
			}
		]
	}
];

export function getUpgradeTier(stageIndex) {
	return UPGRADE_TREE.find((t) => t.stageIndex === stageIndex) || null;
}
