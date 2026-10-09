# Chapter 1: The Event Horizon

![Event Horizon Telescope image of the M87 supermassive black hole](/book-images/ch01-m87-black-hole.jpg)

*The shadow of the black hole M87\*. An image at the edge of what we can observe. (Event Horizon Telescope Collaboration, CC BY 4.0, via Wikimedia Commons)*


> *"Within thirty years, we will have the technological means to create superhuman intelligence. Shortly after, the human era will be ended."*
> Vernor Vinge, *The Coming Technological Singularity* (1993)

**In this chapter:**

- AGI, recursive improvement, physical deployment, and access are separate questions.
- Thanksgiving 2027 is a personal forecast, not a mathematical deadline.
- Useful food work need not wait for a system that can do everything.

---

The Monday after the toast, Elijah brought the printout to work.

He'd read "Attention Is All You Need" so many times over the weekend that the pages had gone soft at the corners, furred with highlighter in four colors that had stopped meaning anything distinct. He'd slept maybe five hours across two nights. He carried the thing into Claypot the way you carry a lab result you don't want confirmed, and he found Devendra at the good coffee machine on the fourth floor, because Devendra was senior, and calm, and had been doing this since before Elijah could spell *gradient descent*, and Elijah needed someone to tell him he was overreacting.


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

The run had stopped at a limit he could feel: heat. He wanted that to explain everything. Give it more power, give it better cooling, and perhaps the curve would keep falling. He almost wrote that down as proof.

Then he looked at the notebook again. The run had not tested every task. A falling training loss was not the same as understanding an unfamiliar problem. The machine had forced one question into the room and left the larger ones where they were. He wrote COOLING in one column and WHAT DID IT LEARN? in another.

He still didn't know what to tell Devendra. He knew only that reassurance was not a measurement, and neither was fear.

He left the tower off for a week. Then he opened the notebook where he'd written MADRONE ≠ DRONE, and under it, he started keeping the arithmetic.

---

## The Foundations

## Four questions hiding inside one word

People use *singularity* to mean accelerating change, an intelligence explosion, or a threshold beyond which prediction becomes unreliable. Those are related ideas, but they aren't interchangeable. The historical definition sources in Appendix B are a starting point for that disagreement, not a vote that settles it.

For the practical argument in this book, keep four questions separate.

**Capability:** Can a system perform a broad range of unfamiliar intellectual tasks with the reliability and adaptability we'd expect from a capable person? That's the working sense of AGI here. A polished answer to one prompt doesn't settle it. Evaluation needs tasks the system hasn't merely rehearsed, independent checking, and an account of failures.

**Improvement:** Can the system contribute to making a better successor? Can the claimed improvement survive testing? Recursive self-improvement means feeding improvements back into the process that makes improvements. It doesn't mean every proposed change works, that the process accelerates without limit, or that physical experiments become instantaneous.

**Deployment:** Can that capability operate useful equipment under ordinary conditions? Growing food means encountering weather, mud, wear, living organisms, and people. A better model does not manufacture a missing actuator.

**Access:** Who actually receives the result? A machine can be capable and unavailable. A service can be cheap to operate and expensive to buy. Someone can live beside a productive farm and still go hungry.

Those four questions are the spine of the forecast. Don't let an answer to one stand in for all the others.

## My date, and what it does not promise

My personal expected date for AGI is U.S. Thanksgiving 2027, November 25. Why that day? Because.

That's the joke, and it's also the boundary around the claim. This is my forecast, not a mathematical deadline. I expect substantial change and I want to prepare for it. I could be wrong about the date, the capability, or both. Evidence that systems remain brittle on unfamiliar tasks would count against my expectation. Evidence of reliable breadth would count in its favor. Neither observation would, by itself, establish autonomous farming or universal access to meals.

Keep a dated record of what I predict. Hold me to the distinction. Thanksgiving can come and go without anyone getting permission to pretend a missed forecast was secretly a different forecast all along.

The food-first proposal survives a late arrival. People can improve food access using tools and organizations that already exist while evaluating new capabilities. We don't need to wait for a machine to become good at everything before asking it to help with something useful.

## What the research can carry

The Transformer paper describes an architecture for machine learning. It does not establish a date for AGI. What matters is what a system can do reliably outside a rehearsed demonstration. A benchmark is evidence about the tested task and conditions; extending it to dependable physical work requires another argument.

This doesn't make the research unimportant. It makes the research usable. A result can be remarkable without proving the largest story somebody tells about it.

My optimism is that useful machine capabilities can keep expanding. My priority is to direct that expansion toward food people can obtain regardless of income. One is an expectation about technology. The other is a choice about what we want it to do.

## The first question to take outside

Ask a grower or food provider which repeated task consumes time without improving the food. Write down their answer before proposing a robot. Ask what would count as a better result and what would make a trial a failure. The answer might concern scheduling, irrigation, lifting, transport, or something you haven't thought of.

That's where the future becomes a piece of work somebody can examine.

---

## Precedent P-03: One Million Years, Give or Take (New York, 1903)

On October 9, 1903, the New York Times published “Flying Machines Which Do Not Fly.” The editorial imagined a working flying machine taking an extraordinarily long period of further effort. Later that year, the Wright brothers flew at Kitty Hawk.

The juxtaposition is memorable because the forecast failed so dramatically. It does not turn a newspaper editorial into a representative sample of all contemporary expertise, or a warrant to disregard expertise now.

Four years before the flight, Wilbur Wright had written to the Smithsonian Institution on his bicycle company's stationery. The letter, dated May 30, 1899, asked for publications about flight and a list of other works he could study. He offered to pay. He believed flight was possible, but described his next step as learning what other investigators already knew. The future aviator was requesting a reading list. [Wilbur Wright to the Smithsonian, May 30, 1899](https://siarchives.si.edu/history/featured-topics/stories/letter-dated-may-30-1899)

Learning from predecessors didn't require treating their measurements as untouchable. After disappointing glider trials in 1901, the brothers built a wooden wind tunnel in their Dayton shop. Their shop engine drove its fan. They made small metal wing models and balances to compare lift and drag. Even the measuring apparatus needed work: the fan disturbed the airflow, and they spent time straightening it before trusting the results. The better aircraft followed a better way of asking what the air was doing. [NASA Glenn, Wright 1901 Wind Tunnel](https://www.grc.nasa.gov/WWW/K-12/airplane/wrights/tunnel.html)

The newspaper supplies the punch line. The shop supplies the useful history. Existing research gave the brothers a place to begin; a disagreement between prediction and observation gave them a reason to investigate further. Neither reverence for authority nor pleasure in defying it would have done the measuring for them.

That is the standard I want applied to the dates in this book. My confidence is a reason to make a claim inspectable. A forecast earns its place by surviving contact with evidence, and by becoming more useful when it doesn't survive intact.

**The mechanism.** The aviation forecast illustrates a large error. One failed pessimistic prediction cannot tell us the direction or size of the next error.

**The rule.** Hold optimistic and pessimistic forecasts to the same evidence.

**The practice.**

1. Save one optimistic and one pessimistic prediction with their dates.
2. Write the observation that would count against each.
3. Choose a review date and include your own prediction in the record.

---
