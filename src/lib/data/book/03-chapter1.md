# Chapter 1: The Event Horizon

![Event Horizon Telescope image of the M87 supermassive black hole](/book-images/ch01-m87-black-hole.jpg)

*The shadow of the black hole M87\*. Past a certain line, there's no going back. (EHT Collaboration, CC BY 4.0, via Wikimedia Commons)*


> *"Within thirty years, we will have the technological means to create superhuman intelligence. Shortly after, the human era will be ended."*
> Vernor Vinge, *The Coming Technological Singularity* (1993)

**In this chapter:**

- Nobody agrees what the word means. A hundred and eighty years of definitions sort into three schools that quietly contradict each other, and picking the wrong one is how you talk yourself into waiting.
- The book's working definition: the point where intelligence stops being scarce, and every institution built on its scarcity starts failing before anyone has written the replacement.
- My call is AGI by Thanksgiving 2027. Here's what would prove me wrong, and why the food work doesn't wait to find out.

---

The Monday after the toast, Elijah brought the printout to work.

He'd read "Attention Is All You Need" so many times over the weekend that the pages had gone soft at the corners, furred with highlighter in four colors that had stopped meaning anything distinct. He'd slept maybe five hours across two nights. He carried the thing into Claypot the way you carry a lab result you don't want confirmed, and he found Devendra at the good coffee machine on the fourth floor, because Devendra was senior, and calm, and had been doing this since before Elijah could spell *gradient descent*, and Elijah needed someone to tell him he was overreacting.

![A tech worker in business casual clothing with a laptop bag over one shoulder](/book-images/ch01-devendra.png)

*Devendra. Senior and calm. Wrong about the thing that mattered.*

"I think it's already over," Elijah said. No preamble. "I watched three people get replaced last week. Real people. Not a projection… a bar, a Tuesday, three jobs, gone. And nobody who did it even thought of it as a big deal."

Devendra tapped his cup against the drip tray, unhurried. "Augmentation, not replacement," he said. It had the worn smoothness of a thing said many times. "It's a very good autocomplete, Elijah. It makes the people who use it faster. The realtors didn't fire humans because a chatbot is a person. They restructured. Companies restructure." He smiled, not unkindly, the way you smile at someone who's just discovered a thing you made your peace with years ago. "You'll calibrate. Everybody's first month feels like the apocalypse."

Elijah wanted to be talked down. That was the humiliating part. He stood there holding the soft pages and *wanted* the calm to work on him. But it slid off, because he'd seen the training curves inside this building, and he'd done the one thing Devendra's reassurance depended on him not doing, which was the arithmetic.

So that night he decided to settle it with his own hands, the only way a farm kid ever really trusts a thing: he'd try to break it.

He had an old tower at home, a space heater of a machine he'd built for cheap during the pivot, two consumer GPUs zip-tied into a case that didn't quite fit them. He pulled a modest open model and started fine-tuning it on his own data, telling himself that if he could feel where it topped out, if he could find the ceiling by touch, he'd know it was just software, bounded like all software, and he could sleep.

![A beige mini-tower PC case with two mismatched GPUs zip-tied inside, visible through an open side panel](/book-images/ch01-pc-rig.png)

*The rig. Two GPUs zip-tied into a case that never fit them. It throttles by design.*

The room got warm around eleven. Warm the way the cab of his delivery car used to get in August, that thick engine-heat with a smell to it. The fans spun up to a howl he could hear from the kitchen. He kept feeding it. The loss curve kept sliding down, not magically, not infinitely, but *steadily*, the way a thing slides when there's real signal underneath and you've simply never had the compute to chase it before. Every increment cost him more. More power off the wall, more heat into the room, the meter he couldn't see spinning somewhere out in the garage.

At 1:20 a.m. the machine threw the temperature warning, throttled itself to protect the silicon, and then, when he stubbornly queued another run, shut down hard. Black screen. The fans coasted to silence. The room ticked as it cooled, exactly like the engine of a car after a long haul.

Elijah sat in the sudden quiet with sweat cooling on the back of his neck and understood something he would spend a whole later chapter of this book trying to say properly.

The thing hadn't hit a ceiling of *intelligence*. It had hit a ceiling of *heat*. The curve was still falling when the hardware quit. The machine that had dissolved three careers at the Bear Flag wasn't magic and it wasn't bounded by cleverness. It was bounded by *watts*, by *cooling*, by the same brutal physics that decided whether his grandmother's crop lived or died.

He had wanted proof it was just software. He'd gotten it. And the proof was worse than the fear, because *just software* running on *enough energy* was precisely the problem. There was no clever limit coming to save anyone. There was only the power bill, and the people who could afford it.

He didn't tell Devendra any of this. Devendra wasn't wrong about the small mechanics: it *was* autocomplete, it *did* make people faster. He was wrong about the only thing that mattered, which was where the curve went when you stopped pretending it would politely stop. Elijah had watched it not stop. He'd had to unplug it to make it stop.

He left the tower off for a week. Then he opened the notebook where he'd written MADRONE ≠ DRONE, and under it, he started keeping the arithmetic.

---

## The Foundations

## Seventeen definitions and no agreement

The word in the title of this book has no agreed meaning. That isn't a technicality, and it isn't pedantry. It's the reason the argument never resolves, and it's the reason two intelligent people can look at the same week of news and walk away with opposite plans.

Nikola Danaylov, who runs Singularity Weblog and has interviewed most of the people who think about this professionally, went looking for a definition and came back with sixteen. Not sixteen phrasings of one idea. Sixteen ideas, several of which contradict each other, all wearing the same word. He arranged them in the order they were written, which turns out to run back more than a century and a half, and then he left a seventeenth slot empty for the reader. That's either intellectual humility or a confession, and it's probably both. [Danaylov, 17 Definitions of the Technological Singularity](https://www.singularityweblog.com/17-definitions-of-the-technological-singularity/)

Here's the lineage, compressed.

**1847.** A Michigan preacher named R. Thornton reviews a new mechanical calculator for *The Expounder of Primitive Christianity*, and he doesn't like it. Students will turn a crank instead of thinking. Then, in the middle of the complaint, he trips over the whole thing: "But who knows that such machines when brought to greater perfection, may not think of a plan to remedy all their own defects and then grind out ideas beyond the ken of mortal mind!" That's recursive self-improvement, described in 1847, by a man annoyed about arithmetic homework.

**1863.** Samuel Butler, farming sheep in New Zealand, reads Darwin and writes to the Christchurch *Press* under a pen name. The letter is called "Darwin among the Machines." He expands it nine years later in *Erewhon*, where the line lands: "There is no security against the ultimate development of mechanical consciousness, in the fact of machines possessing little consciousness now. A mollusc has not much consciousness." His argument is about rate. Machines are doing in centuries what biology needs epochs for.

**1951.** Alan Turing, lecturing in Manchester: "once the machine thinking method had started, it would not take long to outstrip our feeble powers." And then, without hedging: "At some stage therefore we should have to expect the machines to take control." He credits Butler's *Erewhon* for the idea, by name.

**1958.** Stanislaw Ulam, writing his friend John von Neumann's obituary, recalls a conversation "centered on the ever accelerating progress of technology and changes in the mode of human life, which gives the appearance of approaching some essential singularity in the history of the race beyond which human affairs, as we know them, could not continue." That's the word arriving, borrowed from mathematics, where a singularity is the point at which your equation stops returning answers.

**1965.** I. J. Good, who spent the war breaking German ciphers alongside Turing, writes down the mechanism. "Let an ultraintelligent machine be defined as a machine that can far surpass all the intellectual activities of any man however clever." Such a machine can design better machines. "There would then unquestionably be an 'intelligence explosion.'" The first one, he wrote, would be the last invention we'd ever need to make, *provided* it was docile enough to tell us how to keep it under control. People quote the first half of that sentence and drop the condition. Don't.

**1993.** Vernor Vinge, mathematician and novelist, opens "The Coming Technological Singularity" on the two sentences at the head of this chapter. He also does something almost nobody who quotes him repeats: he lists four separate roads to the same destination. Computers that wake up. Networks that wake up. Human-computer interfaces so intimate that the pair counts as superhuman. Or straight biological enhancement of human intellect. Four doors, not one.

**2005.** Ray Kurzweil, in *The Singularity Is Near*: "a future period during which the pace of technological change will be so rapid, its impact so deep, that human life will be irreversibly transformed." Read that again and notice what's missing. There's no machine in that sentence. Kurzweil's singularity is a property of a curve, not of a mind.

The rest of the list fills in around those. Hans Moravec, in 1988, hands robots the succession somewhere around 2030 to 2040. Nick Bostrom, in 1997, defines superintelligence as "an intellect that is much smarter than the best human brains in practically every field, including scientific creativity, general wisdom and social skills." Kevin Kelly says all the change in the last million years will be superseded by the change in the next five minutes. John Smart calls it a permanent and irreversible developmental phase change.

Eighteen decades. No consensus. One word, doing all of that work.

### The three schools, and which one this book runs on

In 2007 Eliezer Yudkowsky did the sorting that makes the pile usable. Nearly every definition on that list, he argued, belongs to one of three schools, and the schools quietly contradict each other once you push on them. [Yudkowsky, Three Major Singularity Schools](https://intelligence.org/2007/09/30/three-major-singularity-schools/)

| School | The core claim | Whose | What it tells you to do |
| --- | --- | --- | --- |
| **Accelerating Change** | "Technological change feeds on itself, and therefore accelerates." | Kurzweil, Toffler, Smart | Read the curve, extrapolate, set a date. |
| **Event Horizon** | Build something smarter than us and the far side stops being predictable, by anyone, the builders included. | Vinge | Stop forecasting. Prepare for the unforecastable. |
| **Intelligence Explosion** | Intelligence is what produces technology. Aim it at itself and the loop closes. | Good, Yudkowsky | Watch one variable: can it improve itself yet? |

*Table 1: The three singularity schools (Yudkowsky, 2007), with the planning posture each one implies.*

Those are three genuinely different animals. Accelerating Change is a claim about a graph, and it doesn't require anything to be smarter than you. Event Horizon is a claim about the limits of prediction. Intelligence Explosion is a claim about a feedback loop, and a loop can close fast enough that no curve shows it to you in time.

This book runs on Event Horizon for the map and Intelligence Explosion for the engine, and it declines Accelerating Change as a planning tool on purpose.

Not because the curve is wrong. Because of what a curve does to the person reading it. A smooth exponential invites you to find your dot on it, notice that the interesting part is somewhere off to the right, and go back to work. It sells you a date, and a date is permission to wait. Yes, I have a date too, and you'll get it in a minute. But I don't plan by it, and neither should you. Plan by doors. Doors don't give notice.

> **A curve gives you a date. A door gives you a Monday.**

The book's one amendment to Good is Chapter 5, and it's the reason Elijah's tower shut itself down at 1:20 in the morning. Whatever the loop turns out to be, it's a physical process. It runs on watts. It sheds heat. Both are metered, and somebody owns the meter.

### The seventeenth slot

Danaylov left one open. Here's the one this book uses, and every claim in the rest of these pages runs downstream of it:

> **The Singularity is the point where intelligence stops being scarce, and every institution quietly built on its scarcity starts failing before anyone has written the replacement.**

Here's how I first pictured it, years before I had the words. Imagine every person on this spinning rock gets their own Einstein as entry-level tech support. Your mom stops calling you to fix her email, because she's got Einstein on speed dial, and by next week she's debating relativity over breakfast. It's a funny picture. Now ask what happens to everyone who was paid to be the smart one in the room.

Three things follow.

**It doesn't wait for a god.** It doesn't require a machine smarter than the smartest human at anything. It only requires that thinking gets cheap enough, in enough places, that the price of a trained person stops clearing. Nobody at the Bear Flag lost their livelihood to a superintelligence. They lost it to a competent autocomplete with a subscription fee.

**It's testable this quarter.** You don't need anyone's date, including mine. Has the market price of the cognitive work you sell fallen in the last eighteen months? Has the institution that pays for it started behaving strangely about it, restructuring, retitling, quietly not backfilling? That's the measurement, and you can run it on yourself before the end of the week.

**It names the actual emergency, which isn't the machine.** It's the gap. The old contract, sell your hours and eat, is failing on a schedule set by hardware, and the new one is being drafted by nobody in particular. Everything in Part II is about that gap. Everything in Part III is about what you build inside it while it's open. And the first clause of the new contract is the simplest one to write: losing your job doesn't cost you dinner.

Sixteen definitions spent a hundred and eighty years describing the same shadow from different angles, and nearly all of them looked up, toward the thing arriving. This one looks down, at the floor going soft under people you know by name.

## Four questions hiding inside one word

When somebody tells you the Singularity is here, or impossible, ask which of these four they mean. They're connected. They aren't the same.

**Capability.** Can a system do a broad range of unfamiliar intellectual work with the reliability you'd expect from a capable person? That's what I mean by AGI. A dazzling answer to one prompt doesn't settle it. Unrehearsed tasks, independent checking, and an honest count of failures do.

**Improvement.** Can the system help build a better successor, and does the improvement survive testing? That's recursive self-improvement. It doesn't mean every proposed change works or that lab experiments become instantaneous.

**Deployment.** Can the capability run useful equipment in ordinary conditions? Growing food means weather, mud, wear, living things, and people. A better model doesn't manufacture a missing motor.

**Access.** Who actually gets the result? A machine can be capable and unavailable. A service can be cheap to run and expensive to buy. Someone can live next door to a productive farm and still go hungry.

Don't let an answer to one stand in for the other three. Most of this book lives in the fourth.

## What the 2017 paper actually did

The modern run started in 2017, with a Google paper titled "Attention Is All You Need." Before it, the best language systems read the way you do, one word after another, which meant they couldn't use modern hardware to its full width. The Transformer threw out that sequence and let every word attend to every other word at once, so the whole job could run in parallel across a room full of chips.

The foundational model was small by today's standards: sixty-five million parameters in its base configuration, two hundred thirteen million in the big one. The big one beat every system that came before it, including ensembles stacked specifically to win these benchmarks, and it did it on a fraction of the training compute.

| Evaluation Metric / Task | Best Prior Result, Ensembles Included | Transformer, "Big" Configuration |
| :-: | :-: | :-: |
| WMT 2014 English-to-German (BLEU) | 26.4 (ConvS2S ensemble) | 28.4, a gain of more than 2 BLEU |
| WMT 2014 English-to-French (BLEU) | 41.3 (ConvS2S ensemble) | 41.8, a new single-model record |
| Training compute, English-to-German | 1.8 x 10^20 FLOPs (GNMT ensemble) | 2.3 x 10^19 FLOPs: 3.5 days on eight P100 GPUs |

*Table 2: Benchmarks from the 2017 Transformer paper. Figures are for the 213-million-parameter "big" configuration; the 65-million-parameter base model reached 27.3 and 38.1 on the same two tasks after twelve hours on the same hardware. [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762)*

That paper is an architecture, not a prophecy. It doesn't contain a date for AGI. What it did was make intelligence something you could buy by the rack, which is why the rest of this story is about racks, power, and who pays for them.

Silicon isn't the only road, either. Remember Vinge's fourth door, biology. In 2022, Cortical Labs reported a dish of roughly 800,000 living human and mouse neurons wired to electrodes that learned to play a simplified *Pong* within minutes of play, organizing its own activity to keep the ball in the game. On the handful of rallies a living culture can get, the cells learned faster per sample than several standard reinforcement-learning programs given the same limited data, and on a sliver of the power. It's a lab result, not a product. It's also a reminder that the doors aren't all in one building.

## My date, and what would prove it wrong

My personal expected date for AGI is U.S. Thanksgiving 2027, November 25. Why that day? Because.

That's the joke, and it's also the boundary around the claim. This is my forecast, not a mathematical deadline. I could be wrong about the date, the capability, or both. Evidence that systems stay brittle on unfamiliar tasks counts against me. Evidence of reliable breadth counts for me. Neither one, by itself, gets anybody fed.

I'm not alone out on this limb, and I'm not in the middle of the pack either. In 2024 the former OpenAI researcher Leopold Aschenbrenner published "Situational Awareness," arguing that stacked gains in compute and algorithms, roughly half an order of magnitude a year each, could carry these systems to automated AI research around 2027. That's one insider's argument, not a measurement. The researchers themselves have been moving too. The largest survey of AI researchers, run by Katja Grace and colleagues, asked the same questions a year apart:

| AI Milestone | 2022 Aggregate Forecast | 2023 Aggregate Forecast | Net Shift |
| :-: | :-: | :-: | :-: |
| High-Level Machine Intelligence (HLMI), 50% probability | 2060 | 2047 | 13 years sooner |
| Full Automation of Labor (FAOL), 50% probability | 2164 | 2116 | 48 years sooner |

*Table 3: Shifts in expert forecasts on AI timelines (Grace et al., 2024).*

The same survey put a 10 percent probability on high-level machine intelligence arriving as early as 2027. And on the darkest question it asked, between 37.8 and 51.4 percent of respondents, depending on how it was framed, gave at least a 10 percent chance to outcomes as bad as human extinction. These aren't doomers on a forum. These are the people building the systems, surveyed by the thousands, and the median moved thirteen years in twelve months.

So write my date down and hold me to it. Thanksgiving can come and go without anyone getting permission to pretend a missed forecast was secretly a different forecast all along. And here's the part that matters: the food-first proposal survives a late arrival. People can improve food access with tools and organizations that already exist while the capability develops. We don't need a machine that's good at everything before we ask it to help with something useful.

## Who gets the savings?

If thinking gets cheap, somebody saves a lot of money. The question is who.

A business under pressure treats payroll as its biggest cost and its biggest risk, and it's rewarded for cutting both. That's not villainy; it's the incentive. But in a society where your food, your housing, and your healthcare hang off a paycheck, automating the payroll without changing anything else turns a productivity gain into a hunger problem for somebody specific.

People have noticed. Sam Altman has floated Universal Basic Income and something he calls "universal basic compute." Aaron Bastani's *Fully Automated Luxury Communism* argues that automation, cheap renewable energy, and synthetic biology could make scarcity optional, and that the real fight is over who owns the result. You don't have to buy either package to see the shape of the argument. The capacity is arriving. The terms haven't been written. This book's proposal for the first term is small, concrete, and testable: food, regardless of whether you still have the job.

## The first question to take outside

Ask a grower or a food provider which repeated task eats time without making the food any better. Write their answer down before you propose a robot. Ask what would count as a better result, and what would make a trial a failure. The answer might be scheduling, irrigation, lifting, transport, or something you'd never have guessed.

That's where the future stops being a forecast and becomes a piece of work somebody can check.

---

## Precedent P-03: One Million Years, Give or Take (New York, 1903)

On October 9, 1903, the New York Times published an editorial titled "Flying Machines Which Do Not Fly." It suggested that a machine which would really fly might be evolved "by the combined and continuous efforts of mathematicians and mechanicians in from one million to ten million years." [NYT editorial, transcription](https://en.wikisource.org/wiki/The_New_York_Times/1903/10/9/Flying_Machines_Which_Do_Not_Fly)

Sixty-nine days later, the Wright Flyer lifted off the sand at Kitty Hawk.

The editors weren't fools. They were doing what respectable analysis is supposed to do: reasoning from the evidence in front of them, which was Samuel Langley's spectacularly public crash into the Potomac two days earlier. Langley had the Smithsonian and War Department money behind him. The two bicycle mechanics in Ohio had neither.

What they had was method. Four years earlier, Wilbur Wright had written to the Smithsonian on his bicycle company's stationery, asking for publications on flight and a list of other works worth studying, and offering to pay for them. The future aviator started by requesting a reading list. [Wilbur Wright to the Smithsonian, May 30, 1899](https://siarchives.si.edu/history/featured-topics/stories/letter-dated-may-30-1899) Then, after disappointing glider trials in 1901, the brothers stopped trusting the published numbers and built their own wooden wind tunnel in the Dayton shop, driven by the shop engine, with small metal wings on hand-made balances to measure lift and drag. Even the tunnel needed fixing first: the fan churned the air, and they spent time straightening the flow before they believed a single reading. [NASA Glenn, Wright 1901 Wind Tunnel](https://www.grc.nasa.gov/WWW/K-12/airplane/wrights/tunnel.html)

The newspaper supplies the punch line. The shop supplies the lesson. The Times was measuring the most recent failure. The Wrights were measuring the air.

**The mechanism.** Expert timelines are often autopsies of the most recent failure, not forecasts of the next success. The distance between "one to ten million years" and "done" was ten weeks, because progress at a frontier isn't a trend line. It's a door. It cuts both ways: one blown pessimistic forecast doesn't make the next optimistic one right, including mine.

**The rule.** When anyone hands you a timeline, mine included, remember that the unit of error isn't years. It's orders of magnitude. Plan by doors, not dates.

**The practice.**

1. Start a timeline file. Every time an expert publishes an AI timeline, paste it in with the date and the author. Add mine. Review it quarterly. Within a year you'll have taught yourself, with receipts, what a confident forecast is worth, and you'll stop outsourcing your planning horizon to whoever sounded calmest.
2. Plan by doors, not dates. Write down three things AI "can't do" that would change your work or your household if they opened. Check them monthly. When one opens, you act that week, because you decided what the door means before it moved.
3. Make one asymmetric bet this month: an action that looks slightly early if the transition takes ten years, and essential if it takes two. Learning the tools, planting the garden, and cutting a fixed cost all qualify. The Times editors risked nothing on their million-year estimate. You don't have that luxury; you live here.

---
