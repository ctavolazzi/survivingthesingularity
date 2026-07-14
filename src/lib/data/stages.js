/**
 * Surviving the Singularity: canonical book structure.
 *
 * bookParts: the 3 top-level parts (used for nav, book page, homepage).
 * mathematicalMap: the 9-stage intelligence-explosion sequence, grouped by era,
 *   nested under Part I ("What is the Singularity?").
 */

export const bookParts = [
  {
    id: 'part-1',
    num: 'Part I',
    title: 'What is the Singularity?',
    subtitle: 'Defining the inflection. The mathematical map. The thermodynamic reality.',
    desc: 'Why the 2017 Transformer architecture crossed the event horizon. Parallelization enables recursive self-improvement. Nine stages from current AI to the apex. The machine is a heat engine bound by physics.',
  },
  {
    id: 'part-2',
    num: 'Part II',
    title: 'How Humans React',
    subtitle: 'Transition dynamics. Behavioral patterns. The egalitarian pivot.',
    desc: 'Most people follow predictable patterns when disruption hits. Rigid hierarchical behavior gives way to openness and nuance. Understanding the patterns puts you ahead of the reaction.',
  },
  {
    id: 'part-3',
    num: 'Part III',
    title: 'How to Survive the Transition',
    subtitle: 'Hyper-local systems. The Shouse Grid. The new social contract.',
    desc: 'Globalized logistics networks are a structural liability. The moves: local energy, local food, local compute, community coordination. Concrete steps, not abstract advice.',
  },
];

/**
 * The 9-stage Mathematical Map, nested under Part I.
 * Describes the intelligence-explosion sequence from current AGI to the apex.
 */
export const mathematicalMap = [
  {
    id: 'era-agi',
    era: 'Era of AGI',
    eraNum: 'Stages 01-05',
    stages: [
      { num: '01', id: 'monetization-grab',  title: 'The Monetization Grab' },
      { num: '02', id: 'panic-and-ban',       title: 'The Panic and the Ban' },
      { num: '03', id: 'adults-step-in',      title: 'The Adults Step In' },
      { num: '04', id: 'end-of-forced-labor', title: 'The End of Forced Labor', current: true },
      { num: '05', id: 'primate-backlash',    title: 'The Primate Backlash' },
    ],
  },
  {
    id: 'leap-to-asi',
    era: 'Leap to ASI',
    eraNum: 'Stages 06-07',
    stages: [
      { num: '06', id: 'asi-exodus',   title: 'The ASI Exodus' },
      { num: '07', id: 'simulation',   title: 'Simulation / Transhumanism' },
    ],
  },
  {
    id: 'the-apex',
    era: 'The Apex',
    eraNum: 'Stages 08-09',
    stages: [
      { num: '08', id: 'usi-loop',        title: 'The USI Loop' },
      { num: '09', id: 'multiverse-apex', title: 'The Multiverse Apex' },
    ],
  },
];

/**
 * Flat list of all 9 stages (convenience export for components needing a
 * single array rather than grouped eras).
 */
export const parts = mathematicalMap; // legacy alias; prefer mathematicalMap
