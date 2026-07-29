/**
 * THE PRECEDENT FILE
 *
 * Three cases are open on the page in full, and the other twenty are listed by
 * title and date.
 *
 * The three are not a random sample. Each maps to a different pillar of the
 * book's argument:
 *
 *   P-07  labor displacement that completed
 *   P-09  organized resistance that failed
 *   P-19  a distributed response that worked, at national scale, in two years
 *
 * The body text is the real passage from src/lib/data/book/*.md, not a summary
 * written for a sales page. That distinction is the entire persuasive weight of
 * this section. A visitor who reads it is reading the book.
 *
 * PRODUCTION: parse these from the book source at build time by reading the
 * `## Precedent P-NN:` headings and the prose that follows, so the site can
 * never disagree with the manuscript. In the MVP they are transcribed.
 */

export const open = Object.freeze([
  Object.freeze({
    id: 'P-07',
    title: "The Horse's Last Ledger",
    date: '1783 to 1960',
    shortTitle: "The Horse's Last Ledger",
    body: Object.freeze([
      'James Watt had a marketing problem. He needed to sell steam engines to men who owned horses, so he invented a unit of account that priced the animal in its own currency: <em>horsepower</em>. From the moment that word existed, every horse in the world was walking around with a number on its back, whether its owner knew it or not.',
      'For a century the horse looked untouchable. The horse population of the United States kept climbing right through the railroad age, peaking above twenty-five million in the 1910s, with an entire economy of hay fields, stables, farriers, harness makers, and teamsters built on its metabolism. Then internal combustion crossed the cost line, joules per dollar, and in a single working lifetime the population collapsed to a few million animals kept mostly for pleasure. The horse never became less noble, less strong, or less willing. It was out-priced per watt, and sentiment appeared in exactly zero rows of the ledger.'
    ]),
    rule: 'You are a twenty-watt thinking engine inside a hundred-watt body, in a market that has just started selling intelligence by the kilowatt-hour. Audit your own energy ledger, what you consume, what you produce, and who captures the difference, before someone else runs the numbers on you.'
  }),
  Object.freeze({
    id: 'P-09',
    title: 'The Frame-Breakers',
    date: 'England, 1811 to 1816',
    shortTitle: 'The Frame-Breakers',
    body: Object.freeze([
      'The croppers and framework knitters of the English Midlands were the elite of their trade, and their analysis was flawless. They saw precisely how the wide stocking frames would flood the market with degraded goods made by degraded labor. They were even surgical about it: crews often smashed only the frames of owners who cut wages and quality, and spared the machines of masters who kept fair terms. This was not ignorance of technology. It was a labor negotiation conducted with hammers, because no other negotiating table existed.',
      "Parliament's reply was the Frame Breaking Act, which made machine-wrecking a capital crime, and twelve thousand soldiers sent into the disturbed counties to enforce it. Seventeen men were hanged at York in January 1813. And the frames won anyway. The wages fell anyway. The craft died anyway. The Luddites got the future exactly right and the strategy exactly wrong, and they paid for the difference at the gallows."
    ]),
    rule: "Every joule spent fighting the machine's existence is a joule taken from securing your position, and the frame-breaker's hammer is now batting zero for two hundred years. Fight for terms, not against physics."
  }),
  Object.freeze({
    id: 'P-19',
    title: 'Twenty Million Gardens',
    date: 'United States, 1943 to 1944',
    shortTitle: 'Twenty Million Gardens',
    body: Object.freeze([
      'When the war strained the industrial food system, the United States government asked amateurs, office workers, schoolchildren, grandmothers, to grow food. Not as a symbol. As logistics.',
      'Roughly twenty million Victory Gardens appeared in backyards, vacant lots, schoolyards, and rooftops, and by 1944 they were producing on the order of <strong>forty percent of the fresh vegetables consumed in the country</strong>. Read that number again. Not agribusiness. Not a centrally planned mega-farm program. Yards. The entire parallel food system materialized in about two growing seasons, run by people the food industry would have described, the year before, as hopeless amateurs. Then the emergency passed, the marketing stopped, and the whole capacity was allowed to evaporate, which is why your neighbor thinks food comes from a truck.'
    ]),
    rule: 'The soil within reach of your door is standby infrastructure with a documented national-scale activation record of about twenty-four months. Every raised bed you build now is a node the next emergency does not have to improvise. You are not gardening. You are pre-positioning.'
  })
]);

/**
 * The other twenty. Titles and dates only, greyed on the page, never blurred.
 *
 * A blur says "there is more text". Twenty real titles with real dates say
 * "there is more work, it is specific, and none of it is filler". The second is
 * a stronger argument and it is also simply true.
 */
export const rest = Object.freeze([
  Object.freeze({ id: 'P-01', title: 'The Reading Rage', date: '1790s' }),
  Object.freeze({ id: 'P-02', title: 'The Toy at the Fair', date: 'Philadelphia, 1876' }),
  Object.freeze({ id: 'P-03', title: 'One Million Years, Give or Take', date: 'New York, 1903' }),
  Object.freeze({ id: 'P-04', title: 'The Red Flag', date: 'Britain, 1865' }),
  Object.freeze({ id: 'P-05', title: 'The Fleet That Sailed Home Forever', date: 'Ming China, 1433' }),
  Object.freeze({ id: 'P-06', title: 'The Great Demotion', date: 'Frombork, 1543' }),
  Object.freeze({ id: 'P-08', title: 'The Grain Trap', date: 'Fertile Crescent, c. 9500 BC' }),
  Object.freeze({ id: 'P-10', title: 'The Robot in the Orchestra Pit', date: 'United States, 1929 to 1948' }),
  Object.freeze({ id: 'P-11', title: 'Torches of Freedom', date: 'New York, 1929' }),
  Object.freeze({ id: 'P-12', title: 'The Year the Bronze Stopped', date: 'Eastern Mediterranean, c. 1177 BC' }),
  Object.freeze({ id: 'P-13', title: "The Abbot's Confession", date: 'Sponheim, 1492' }),
  Object.freeze({ id: 'P-14', title: 'The Quartz Heresy', date: 'Switzerland, 1969 to 1983' }),
  Object.freeze({ id: 'P-15', title: 'One Hundred Sixty Acres', date: 'United States, 1862' }),
  Object.freeze({ id: 'P-16', title: 'The House That Came by Mail', date: 'Chicago, 1908 to 1942' }),
  Object.freeze({ id: 'P-17', title: 'The Graveyard of the Unconvinced', date: '1975 to 2011' }),
  Object.freeze({ id: 'P-18', title: 'The Mirror Twin', date: 'Tokyo, 2000s' }),
  Object.freeze({ id: 'P-20', title: 'Seventy-Nine Pages', date: 'Philadelphia, 1776' }),
  Object.freeze({ id: 'P-21', title: 'Access to Tools', date: 'Menlo Park, 1968' }),
  Object.freeze({ id: 'P-22', title: 'The Apocalypse That Ran On Time', date: '1999' }),
  Object.freeze({ id: 'P-23', title: 'The Passing Fad', date: '1995 to 2000' })
]);

/** Total count, derived. Never typed. This is what makes the 29 impossible. */
export const total = open.length + rest.length;

export const parts = Object.freeze([
  Object.freeze({
    n: 'Part I',
    title: 'What is the Singularity?',
    detail:
      'Defining the inflection. The mathematical map. The thermodynamic reality. Why the 2017 Transformer paper was the event horizon, and which physical limits even a superintelligence cannot skip.'
  }),
  Object.freeze({
    n: 'Part II',
    title: 'How Humans React',
    detail:
      'Transition dynamics. Behavioral patterns. The egalitarian pivot. What people actually do when the ground moves, and which of those responses have ever worked.'
  }),
  Object.freeze({
    n: 'Part III',
    title: 'How to Survive the Transition',
    detail:
      'Hyper-local systems. The Shouse Grid. The new social contract. Neighborhood-scale infrastructure, DC-native microgrids, and food you did not have to trust a truck for.'
  })
]);
