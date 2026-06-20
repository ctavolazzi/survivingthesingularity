// Single source of truth for the "evidence" corpus.
//
// Everything on this site is downstream of things you can watch or read
// yourself. This module collects the primary sources (real demo footage and
// the papers / reports behind the thesis), organized by theme. It is consumed
// by both the homepage "See It Happen" section and the full /evidence page so
// the two never drift apart.

/** @typedef {{ id: string, title: string, channel: string, blurb: string }} Video */
/** @typedef {{ id: string, title: string, authors: string, year: string, venue: string, url: string, kind: 'paper' | 'report' | 'article', summary: string, why: string }} Source */

// --- Videos ----------------------------------------------------------------

export const videos = {
	genie3: {
		id: 'PDKhUknuQDg',
		title: 'Genie 3: dynamic worlds you can navigate in real time',
		channel: 'Google DeepMind',
		blurb: 'A model that generates explorable, physically consistent worlds on the fly. The machine is no longer just predicting text. It is building environments.'
	},
	figureBMW: {
		id: 'WlUFoZstcWg',
		title: 'Figure status update: BMW use case',
		channel: 'Figure',
		blurb: 'Humanoid robots working a real automotive production line. Not a stage demo. A factory.'
	},
	figureBotQ: {
		id: 'YZH1csMhnDo',
		title: 'BotQ: ramping F.03 production',
		channel: 'Figure',
		blurb: 'Robots helping build the next generation of robots. The line that makes the workforce.'
	},
	figureHelix: {
		id: '8xEuFQz4E4A',
		title: 'Helix: tidying a bedroom',
		channel: 'Figure',
		blurb: 'A humanoid handling an unstructured household task on its own. The chores are next.'
	},
	corticalDoom: {
		id: 'yRV8fSw6HaE',
		title: 'Living human brain cells play DOOM on a CL1',
		channel: 'Cortical Labs',
		blurb: 'Lab-grown neurons wired into silicon, learning to play a video game. Computation on a living substrate.'
	},
	majorana1: {
		id: 'wSHmygPQukQ',
		title: 'Majorana 1 explained: the path to a million qubits',
		channel: 'Microsoft',
		blurb: 'The clearest breakdown of the topological-qubit chip and why a stable qubit changes the ceiling on what is computable.'
	},
	majorana2: {
		id: '1bN4O5_meB4',
		title: 'Introducing Majorana 2',
		channel: 'Microsoft',
		blurb: 'The next-generation chip, ~1,000x more stable than the prior generation. Quantum is not here yet. But the curve is bending.'
	},
	desktopArm: {
		id: 'HN_9YfSDf6k',
		title: 'The world\'s smallest and most precise industrial robot arm',
		channel: 'Oleksandr Stepanenko',
		blurb: 'Industrial-grade precision shrunk to a desktop, at a price that would stagger you. The means of production are landing on individual workbenches.'
	}
};

// --- Sources (papers, reports, articles) -----------------------------------

export const sources = {
	attention: {
		id: 'attention',
		title: 'Attention Is All You Need',
		authors: 'Vaswani, Shazeer, Parmar, et al. (Google)',
		year: '2017',
		venue: 'NeurIPS · arXiv:1706.03762',
		url: 'https://arxiv.org/abs/1706.03762',
		kind: 'paper',
		summary: 'Introduced the Transformer architecture, dropping recurrence in favor of pure attention. Every large language model since (GPT, Claude, Gemini) is a descendant of this eight-page paper.',
		why: 'This is the spark. If you want to know when the current era actually started, it was here, in 2017.'
	},
	situational: {
		id: 'situational',
		title: 'Situational Awareness: The Decade Ahead',
		authors: 'Leopold Aschenbrenner',
		year: '2024',
		venue: 'situational-awareness.ai',
		url: 'https://situational-awareness.ai/',
		kind: 'report',
		summary: 'A former OpenAI researcher argues that AGI is plausible by 2027 and that the jump to superintelligence could follow fast, triggering a trillion-dollar compute buildout and a national-security scramble.',
		why: 'The most-cited articulation of the short-timeline view. Read it to understand why "before 2027" keeps coming up.'
	},
	agiToAsi: {
		id: 'agiToAsi',
		title: 'From AGI to ASI',
		authors: 'Genewein, Legg, Hutter, et al. (Google DeepMind)',
		year: '2026',
		venue: 'Google DeepMind',
		url: 'https://deepmind.google/research/publications/239142/',
		kind: 'paper',
		summary: 'DeepMind researchers map four routes from human-level AI to superintelligence (scaling, paradigm shifts, recursive self-improvement, and multi-agent systems) and argue the transition is likely a series of shocks rather than one moment.',
		why: 'The lab actually building it, reasoning in public about what comes after AGI. Not a skeptic and not a hype account. The engineers.'
	},
	majoranaArticle: {
		id: 'majoranaArticle',
		title: 'Introducing Majorana 2: a quantum chip made 1,000x more reliable with agentic AI',
		authors: 'Microsoft',
		year: '2026',
		venue: 'Microsoft Source',
		url: 'https://news.microsoft.com/source/features/innovation/majorana-2-microsoft-discovery-agentic-ai/',
		kind: 'article',
		summary: 'Microsoft\'s topological qubits now hold their state ~20 seconds (up from microseconds), with a stated path to a commercially useful quantum machine by 2029, accelerated by AI helping design the chip.',
		why: 'AI is now helping build the hardware that will run the next AI. That feedback loop is the whole story.'
	},
	fusion: {
		id: 'fusion',
		title: 'IEA features fusion in State of Energy Innovation 2026',
		authors: 'Fusion Industry Association / IEA',
		year: '2026',
		venue: 'Fusion Industry Association',
		url: 'https://www.fusionindustryassociation.org/iea-features-fusion-in-state-of-energy-innovation-2026-report/',
		kind: 'report',
		summary: 'The International Energy Agency\'s 289-page State of Energy Innovation 2026 now tracks fusion as a near-term technology, citing a funded commercial race and a 2030 milestone for a first commercial plant. The detail in the full report is the clearest signal yet of how close practical fusion has gotten.',
		why: 'Intelligence and robotics run on power. Permanent, effectively limitless clean energy is the input that makes everything else cheap, and the full report shows we are closer than most people realize.'
	},
	ahaRobot: {
		id: 'ahaRobot',
		title: 'AhaRobot: a low-cost open-source bimanual mobile manipulator',
		authors: 'Cui, Yuan, Zheng, Hao',
		year: '2025',
		venue: 'arXiv:2503.10070',
		url: 'https://arxiv.org/html/2503.10070v1',
		kind: 'paper',
		summary: 'A full dual-arm mobile manipulation robot you can build for about $1,000 (≈$2,000 with onboard GPU), roughly 1/15 the cost of a comparable $32,000 commercial platform.',
		why: 'The $100k robot arm is a myth now. The plans and the bill of materials are public, and the total is four figures.'
	},
	aloha2: {
		id: 'aloha2',
		title: 'ALOHA 2: enhanced low-cost hardware for bimanual teleoperation',
		authors: 'Google DeepMind · Stanford IRIS · Hoku Labs',
		year: '2024',
		venue: 'aloha-2.github.io',
		url: 'https://aloha-2.github.io/',
		kind: 'paper',
		summary: 'An open-source, low-cost two-armed platform built for large-scale manipulation data collection, with improved grippers, frame, and cameras over the original ALOHA.',
		why: 'Top labs are deliberately driving the cost of capable robot hardware down and open-sourcing it. The barrier to entry is falling on purpose.'
	},
	mobileAloha: {
		id: 'mobileAloha',
		title: 'Mobile ALOHA: learning bimanual mobile manipulation',
		authors: 'Fu, Zhao, Finn (Stanford)',
		year: '2024',
		venue: 'mobile-aloha.github.io',
		url: 'https://mobile-aloha.github.io/',
		kind: 'paper',
		summary: 'Put the low-cost two-armed rig on a mobile base and teach it by demonstration: it learns to cook, store items in cabinets, ride elevators, and clean a kitchen.',
		why: 'A trainable, low-cost robot chef is not science fiction. It is a Stanford demo from 2024 with the recipe published.'
	},
	nasaNuclear: {
		id: 'nasaNuclear',
		title: 'NASA is building the first nuclear reactor-powered interplanetary spacecraft',
		authors: 'MIT Technology Review',
		year: '2026',
		venue: 'MIT Technology Review',
		url: 'https://www.technologyreview.com/2026/04/14/1135848/nasa-nuclear-powered-spacecraft/',
		kind: 'article',
		summary: 'NASA is developing Space Reactor-1 Freedom (SR-1), the first nuclear-reactor-powered spacecraft, with a planned launch toward Mars by the end of 2028, roughly a one-year flight. Nuclear propulsion is far more efficient than chemical rockets, opening up faster human exploration of the solar system.',
		why: 'The same compounding curve that is reshaping the economy is reshaping where humanity can go. Abundant energy plus autonomy plus intelligence does not stop at the atmosphere.'
	}
};

// --- Themed grouping (the stack of the singularity) -------------------------

export const evidenceCategories = [
	{
		id: 'spark',
		eyebrow: '2017 · where it began',
		title: 'The Spark',
		summary: 'It did not start with a chatbot. It started with one paper that taught machines to pay attention.',
		videos: [],
		sourceIds: ['attention']
	},
	{
		id: 'minds',
		eyebrow: 'Intelligence',
		title: 'Minds',
		summary: 'Machine intelligence is going general: reasoning, planning, and now generating entire worlds to act inside.',
		videos: ['genie3'],
		sourceIds: ['situational', 'agiToAsi']
	},
	{
		id: 'bodies',
		eyebrow: 'Embodiment',
		title: 'Bodies',
		summary: 'Intelligence is getting hands. Humanoid robots are already on factory floors and starting on the chores at home.',
		videos: ['figureBMW', 'figureBotQ', 'figureHelix'],
		sourceIds: []
	},
	{
		id: 'means',
		eyebrow: 'Access',
		title: 'The Workshop',
		summary: 'The capability is not staying locked inside big labs. Industrial-grade tools are collapsing in size and price onto ordinary desktops, and capable robots now cost four figures, not six.',
		videos: ['desktopArm'],
		sourceIds: ['ahaRobot', 'mobileAloha', 'aloha2']
	},
	{
		id: 'substrate',
		eyebrow: 'Hardware',
		title: 'New Substrates',
		summary: 'The stuff underneath is changing too: living neurons doing computation, and a real path toward stable quantum chips.',
		videos: ['corticalDoom', 'majorana1', 'majorana2'],
		sourceIds: ['majoranaArticle']
	},
	{
		id: 'power',
		eyebrow: 'Energy',
		title: 'Power',
		summary: 'None of it runs without energy. Solar already collapsed in price; fusion is now on the near-term map.',
		videos: [],
		sourceIds: ['fusion']
	},
	{
		id: 'frontier',
		eyebrow: 'Frontier',
		title: 'Off-World',
		summary: 'The same curve does not stop at the atmosphere. Nuclear propulsion puts Mars inside a single-year trip.',
		videos: [],
		sourceIds: ['nasaNuclear']
	}
];

// Time-ordered milestones for the evidence timeline. `status` drives styling:
// 'past' = already happened, 'now' = happening, 'future' = projected.
export const timeline = [
	{
		year: '2017',
		status: 'past',
		title: 'Attention Is All You Need',
		desc: 'Google publishes the Transformer. The architecture behind every modern LLM.',
		sourceId: 'attention'
	},
	{
		year: '2022–24',
		status: 'past',
		title: 'The LLM era goes mainstream',
		desc: 'ChatGPT, Claude, and Gemini put general-purpose AI in hundreds of millions of hands.',
		sourceId: null
	},
	{
		year: '2024',
		status: 'past',
		title: '"Situational Awareness" maps the decade',
		desc: 'A short-timeline case for AGI by ~2027 starts shaping how labs and governments plan.',
		sourceId: 'situational'
	},
	{
		year: '2025–26',
		status: 'now',
		title: 'Bodies, worlds, and new substrates',
		desc: 'Humanoids hit production lines, models generate explorable worlds, neurons compute, and quantum chips stabilize.',
		sourceId: 'agiToAsi'
	},
	{
		year: '2028',
		status: 'future',
		title: 'NASA SR-1 launches for Mars',
		desc: 'The first nuclear-reactor-powered spacecraft is slated to depart by the end of 2028.',
		sourceId: 'nasaNuclear'
	},
	{
		year: '2029',
		status: 'future',
		title: 'A useful quantum machine',
		desc: 'Microsoft\'s stated target for a commercially scalable quantum computer.',
		sourceId: 'majoranaArticle'
	},
	{
		year: '2030',
		status: 'future',
		title: 'First commercial fusion plant',
		desc: 'The IEA\'s milestone for fusion crossing from experiment to grid.',
		sourceId: 'fusion'
	}
];

/** Resolve a category's video/source ids into full objects. */
export function resolveCategory(category) {
	return {
		...category,
		videos: category.videos.map((id) => videos[id]).filter(Boolean),
		sources: category.sourceIds.map((id) => sources[id]).filter(Boolean)
	};
}

// Curated, diversified highlight reel for the homepage: one per domain so it
// never reads like an ad for any single company.
// These are the videos that appear in the "See It Happen" grid on the homepage.
// Keep this list to videos NOT already placed inline above that section to avoid
// showing the same clip twice as the user scrolls.
export const homepageVideoIds = ['desktopArm', 'majorana2'];
export const homepageVideos = homepageVideoIds.map((id) => videos[id]);
