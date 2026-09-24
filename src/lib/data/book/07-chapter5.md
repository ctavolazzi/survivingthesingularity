# Chapter 5: The Thermodynamics of Survival

![The Sun imaged by NASA's Solar Dynamics Observatory](/book-images/ch05-sdo-sun.jpg)

*The Sun, via NASA's Solar Dynamics Observatory. The dominant energy income of everything alive on Earth. (NASA/SDO (AIA), Public domain, via Wikimedia Commons)*


> *"But if your theory is found to be against the second law of thermodynamics I can give you no hope; there is nothing for it but to collapse in deepest humiliation."*
> Arthur Eddington, *The Nature of the Physical World* (1928)

**In this chapter:**

- Every intelligence, silicon or biological, pays its bills in the same currency: watts.
- You're a hundred-watt machine with expensive fuel requirements. The machine's hard ceilings are heat and power. Whoever owns energy has a big say in the transition.
- Keep food, energy, labor, and money in separate ledgers. Free to eat isn't free to provide.
- The counterattack starts small and already has a name: the cyberdeck. The kids are building it.

---

The envelope was thin, which fooled him.

Elijah's power bills had always been the boring kind of mail: forty-something dollars, autopay, straight into the recycling. This one he opened over the kitchen sink out of pure Monday inertia, and then he stood there long enough for the tap he'd been about to run to matter, because the number at the bottom said $211.46.

His first instinct was that he'd been hacked. His second, arriving with the slow heat of a blush, was the truth: the meter hadn't lied, *he'd* simply never been the kind of animal it was built to catch before. One month. One month of fine-tuning runs on the tower, of tests left running overnight, of two GPUs breathing like sled dogs under his desk while he chased the far end of the curve. A hundred and seventy dollars of difference between a man who *thinks about* machine intelligence and a man who *runs* it, printed on paper and mailed to his door by the utility company like a grade.

He sat down at the kitchen table with the bill and the notebook, and for once he didn't need to build the insight. It walked in and pulled up a chair.

The night the tower had cooked itself into a shutdown, he'd written down that the machine's only wall was heat. He'd understood it then the way you understand a headline. Now, holding the invoice, he understood it the way you understand a hangover. Intelligence wasn't magic. Intelligence was *energy, arranged*. Every token the machine produced was a little cone of waste heat over a server rack somewhere; every clever thing it said had a wattage. And every clever thing *he* said did too: roughly a hundred watts, day and night, the output of one warm incandescent bulb, fueled by groceries. He wrote the two numbers side by side. The datacenter measured in gigawatts, him measured in sandwiches. The whole coming war, right there in one line of notebook arithmetic.

That week he became insufferable in a brand-new way. He bought a plug-in power meter (a little gray box, fourteen dollars, the single highest-leverage instrument purchase of his life) and went through the apartment like an auditor with a grudge. The television, off, sipping eleven watts around the clock for the privilege of turning on two seconds faster. The cable box, twenty-three watts, doing *nothing*, a tenant who paid no rent. The microwave clock. The laser printer he used four times a year. He filled two notebook pages with the ledger of it, and the ledger gave him a much smaller assignment than predicting the end of the world: he had been leaking energy (money, agency, *survival margin*) in a fine mist, everywhere, always, invisibly, to machines that did not love him.

Then he did the other math, the one that mattered. The tower drew 600 watts flat-out to run a model that could think alongside him. His phone drew five to make him dumber. Somewhere between those two numbers, he realized, there was a machine worth owning: something small, something *his*, something that ran on watts he could count on his fingers and served nobody's meter but his own. He didn't have the name for it yet. The kids, as we're about to see, already did.

On Sunday he drove out to the storage unit where his grandmother's things had been sitting since the estate sale nobody could face finishing, and he came back with the woodstove. It was a squat black Fisher, older than he was, four hundred pounds of plate steel with a crack in one firebrick, and he had no fireplace and no flue and no permission from his landlord, so it sat in the corner of the living room as a monument, which was the point. His grandmother had heated a whole farmhouse with it, cooked on it, dried socks over it, kept lambs alive behind it in bad Februaries, all on wood she'd bucked herself from her own downed oaks. Total utility bill, as far as he knew it then: a chainsaw's gas and her own hundred watts. For a moment he wanted to count the cost as nothing but fuel and muscle. Then he remembered the borrowed trailer, the neighbor who helped when her shoulder went, the work of keeping a chimney clear. There had been a whole small arrangement around that stove. His grandmother knew what it needed and who she could call. That was part of the warmth.

![A squat black cast-iron wood stove with the door open, one cracked firebrick visible inside](/book-images/ch05-woodstove.png)

*The Fisher. Four hundred pounds of steel, one cracked firebrick. Older than him.*

He put his hand flat on the cold steel the way she used to put his hand on the madrones. She hadn't been outside the world. She had known how to make a place in it.


The stove sat in the corner of a rented apartment with no flue to feed. He left his hand on it a little longer.

He unplugged the cable box on his way to bed. It was, he'd say later, only half joking, the first act of the rest of his life: the first watt he ever took back.

---

## The Foundations

Let's talk about energy.

And no, I don't mean the "I'm really vibing with your aura" kind. Nobody ever stayed warm in January by aligning their chakras.

I mean real energy. The brutal, unforgiving energy of physics, measured in joules, calories, and kilowatt-hours. Whether you're a frontier model running in a warehouse full of chillers or a wet, anxious ape eating a dented can of beans, you're bound by the same laws of thermodynamics. No algorithm can patch them out. No lobbyist can buy them off.

## The rules of the board

**The first law: you can't cheat the universe.** Energy can't be created or destroyed, only changed from one form to another. Everything you do needs an input. To think a thought, your brain burns glucose. To run a water filter, you need electricity. To run a model, somebody pays a utility.

**The second law: there's no breaking even.** In every transfer, some energy leaks away as heat, and the universe slides steadily toward disorder. Your body is a highly organized structure that, left alone, would decay into a cold puddle of carbon and water. To stay alive you have to keep importing organized energy, food, and exporting waste and heat.

For most of us, a global supply system does that heavy lifting out of sight. It burns an astonishing amount of fuel to move a strawberry across a continent so you can eat its sugar in February. Most days it works. The days it doesn't are when you find out how far you live from your own dinner.

## The meat engine and the silicon machine

Here's a hard truth the tech-utopians skip: as an engine, you're not very efficient.

| System | Share of the energy in that comes out as useful work |
| :-- | :-: |
| Human muscle (food chemistry to motion) | about 14% to 27% |
| Combustion engine (small engines to large diesels) | about 10% to 50% |
| Combined-cycle gas plant (fuel to electricity) | up to about 63% |
| Electric motor, over 200 watts | about 70% to 99% |

*Typical conversion efficiencies, as compiled in [Wikipedia, Energy conversion efficiency](https://en.wikipedia.org/wiki/Energy_conversion_efficiency). Ranges, not specifications: a particular machine can sit anywhere in its band.*

You burn roughly 2,000 to 2,500 kilocalories a day to keep your heart pumping, your lungs moving, and your brain generating existential dread. That's about 100 watts of continuous power, the draw of an old incandescent bulb, and about twenty of those watts run your brain. To get them, you need proteins, carbohydrates, and fats that somebody had to grow, harvest, move, and cook.

The machines are less picky. They eat raw electricity, from sunlight, wind, uranium, or coal. They don't spend energy repairing cell walls or fighting off a cold.

That comparison is vivid, and it's exactly where people get dangerous with it. Calling someone a meat engine can make the physics easy to feel. It must never make their worth depend on how cheaply they compete with a motor. Thermodynamics checks a claim against the physical world. It doesn't tell you what a person deserves or who gets to eat.

## A machine still needs a world

A machine can do work without a person making every motion. It can't do it without inputs. A robot that helps with food needs a food source, the right equipment, water and power where the task calls for them, maintenance, and people or systems to handle the parts it can't. Every one of those is metered, and somebody owns the meter.

So keep the ledgers separate. Suppose a shared garden has solar panels, a water pump, and a harvest. Record electricity in kilowatt-hours, water in liters, food in kilograms, labor in hours, and spending in dollars. Don't add them together into one heroic surplus number. A pile of zucchini isn't a year's diet. Power at noon isn't power during a cloudy week. Installed capacity isn't delivered service. If you compare a manual job with a machine, count the setup, the babysitting, the failed runs, and the repairs, or you've just moved the work off the page.

## Free to eat, with the costs visible

When I say food should be free at the point of access, I don't mean steel, land, labor, or electricity stop costing money. I mean the person who needs to eat shouldn't have to produce a payment first.

We already know how to separate the person eating from the person paying. A library has a budget and charges you nothing at the door. Automation can bring down the cost of some of the work. It doesn't decide who pays or who gets served. If a project can't say how next month's maintenance gets covered, it has no business advertising a permanent promise. Find the gap while there's still time to fix it.

## The cyberdeck: your first machine

Before we go any further into land and grids and agreements, I want to show you what energy agency looks like when it's small enough to fit in a Pelican case. I want to show you what the kids are building. And first, I need to show you a couple of centuries of adults being wrong about what the kids are building.

### A brief history of "kids these days"

You already met the novel panic at the end of the Preface. It had company.

In 1816, *The Times* of London condemned an "indecent foreign dance" sweeping the ballrooms and warned parents to keep their daughters away from it. The dance was the **waltz**. [The Times (July 1816), as quoted in John Hood, Hayek, Strauss, and the Political Waltz, FEE](https://fee.org/articles/hayek-strauss-and-the-political-waltz/)

In the 1890s, when the safety bicycle let young women go where they pleased without a chaperone, some physicians warned of a condition called **"bicycle face,"** a strained, haggard expression supposedly caused by the effort of balancing. The thing actually on the move wasn't anybody's face. It was women's freedom of movement. [McGill Office for Science and Society, The Moral and Medical Panic Over Bicycles](https://www.mcgill.ca/oss/article/history-did-you-know/moral-and-medical-panic-over-bicycles)

In 1906, John Philip Sousa, the most famous musician in America, published "The Menace of Mechanical Music," warning that the phonograph would wither the human voice: "the vocal cords will be eliminated by a process of evolution." His own band was already one of the best-selling recording acts in the country. [Sousa, The Menace of Mechanical Music (1906)](https://ocw.mit.edu/courses/21m-380-music-and-technology-contemporary-history-and-aesthetics-fall-2009/18ab3aba9fe7aa1502a55cd049333659_MIT21M_380F09_read02_sousa.pdf)

Then radio was rotting children's brains. Then comic books were, and the United States Senate held hearings about it. Then television. Then Dungeons & Dragons was Satanic, then video games were murder simulators, then the internet, then the phone, and now, right on schedule, the machine this book is about.

Some of those worries had a grain of something real in them. None of the panics was how anybody found out which grain. So here's the translation key, and I want you to laminate it: a lot of the time, "kids these days" means *a tool I don't understand is making someone I can't supervise powerful in a way I didn't sign off on.*

Which brings me to the kids, and what they're actually doing.

### What a cyberdeck is

Right now, while the professionally worried write op-eds about screen time, a lot of mostly young builders are constructing an alternative computing culture out of parts, spite, and joy. They call the machines **cyberdecks**, a name lifted from the "cyberspace deck" Case jacks into in William Gibson's *Neuromancer* (1984). A cyberdeck is, simply, a personal computer you *build instead of buy*. Not picked off a menu. Designed. Fabricated. Owned the way you can only own something you could rebuild from a pile of its own parts.

There's no factory spec, but a common anatomy has emerged:

- **The brain:** a single-board computer, often a Raspberry Pi. Total draw: single-digit watts.
- **The face:** a small screen, or e-ink for sunlight and almost no power.
- **The hands:** a mechanical keyboard, often a tiny one, sometimes hand-wired key by key.
- **The body:** a Pelican case, an ammo can, a 3D-printed shell, a thrift-store briefcase.
- **The ears:** a cheap software-defined radio stick, and a LoRa radio running Meshtastic, the off-grid mesh messaging network.
- **The library:** offline. A full copy of Wikipedia, manuals, maps, sometimes a small local model, everything the owner might need when the network is gone.

Read that list again, slowly, because you've seen it before. Owned hardware. Understood systems. Offline knowledge. Mesh communication. A power budget in watts. Repair as a value. **A cyberdeck is this whole book at model-railroad scale**, and the people building them didn't wait for permission, funding, or a curriculum. Appendix E has more, including the easier route: the phone already in your pocket.

### The Tiffany Doctrine

Here's the part I need the older readers to sit with, because I'm on your side and this is going to sting.

The kids building these machines don't know how things used to be. They don't much care how things used to be. Why would they? "How things used to be" isn't a place they can live. The ladder a lot of their grandparents climbed, the cheap house, the one-income family, the job that couldn't reach you after five, got pulled up behind them. The kids mostly know that world as a rent bill and a lecture. So they're doing what young people have done in every turning before this one: building an alternative with the materials at hand, while the previous tenants explain that the materials are morally inferior.

So: Grandpa. I'm sorry Tiffany wasn't around when they put a man on the moon. But right now she's learning the skills to put *herself* on the moon. She doesn't need a lecture about how kids these days can't adjust a TV antenna. She needs your help and your patience while she builds a goddamn cyberdeck. She's teaching herself the pieces of the kind of machine that might someday fold your laundry and grab you a beer, so she can spend her own hours on something more important: her life. Your job is to help her handle frustration, not to hand her more of it.

And Grandpa, you've got more to offer her than anybody in her Discord server, if you can drop the sermon. You know how to solder. You know why the fuse blows. You know what it feels like to stay with a broken thing until it isn't, which is one of the rarest skills in her world of infinite scroll and one-click everything. She's building the exact machine this chapter has been describing: low-watt, owned, repairable, still working when the network isn't. That's not brain rot. It's the novel, the waltz, the bicycle, and the phonograph all over again, and this time you get to choose which side of the letter to the editor you're on.

The pattern holds, generation after generation: the tool the elders mock becomes part of the world the kids build. The novel readers became the reading public. The bicycle girls rode into the suffrage era. The kids wasting their lives on computers built the thing you're mad at now. Tiffany and her cyberdeck aren't the collapse of civilization. They're the *continuity plan*.

Your first machine doesn't need to be pretty. It needs to be yours. Build one with her.

## Step one: audit your energy budget

Before you pool anything with anybody, run a cold-eyed audit of your own balance sheet.

1. **What are your inputs?** Where does your food come from, where does your power come from, and what happens to each during a week-long interruption?
2. **Where are your leaks?** Standby loads, subscriptions, fuel, and attention. Attention is energy too: hours spent doomscrolling are hours somebody else is billing for.
3. **Who's in your pod?** Which people within walking distance could share tools, meals, rides, and labor with you?

Then pick one task you actually care about, food first if you can, and write a short inventory with the people who already do it: the task, what it needs, who's responsible, what it still depends on from outside, and what happens during an interruption. An irrigation controller won't fix a missing water supply. A better motor won't fix a delivery route that never reaches the person.

You don't need a private microgrid to take part in a food project. You need to know what your part runs on. It's time to stop leaking energy to machines that don't love you.

---

## Precedent P-07: The Horse and the Ledger (Britain and United States, eighteenth to twentieth centuries)

James Watt had a marketing problem. He needed to sell steam engines to men who owned horses, so he took the engine-sellers' old boast, this machine does the work of so many horses, and standardized it into a unit of account that priced the animal in its own currency: *horsepower*, thirty-three thousand foot-pounds per minute. From the moment that number existed, every horse in the world was walking around with it on its back, whether its owner knew it or not.

The paperwork survives. The Science Museum holds a contract dated March 1, 1786, between Boulton and Watt and a distillery near Whitechapel Road, for a ten-horsepower engine to grind grain and pump liquids. The distillers would put it up and maintain it; the inventors would collect an annual premium for the rest of the patent term, a payment the firm tied to what the customer saved compared with doing the work another way. [Science Museum Group, engine agreement of 1786](https://collection.sciencemuseumgroup.org.uk/objects/co50966/original-indenture-of-agreement-for-erection-of-a-agreements) The machine was physical. The deal was a ledger: somebody had to define the alternative, measure the work, and keep the engine running.

The horse looked untouchable for another century. The horse and mule population on American farms kept climbing right through the railroad age, peaking above twenty-six million in 1918, with a whole economy of hay fields, stables, farriers, harness makers, and teamsters built on its metabolism. Then tractors, trucks, feed prices, farm wages, and a dozen other lines in the farm ledger moved, and within a working lifetime the herd collapsed. [USDA, Statistical Bulletin 83, table 14](https://downloads.usda.library.cornell.edu/usda-esmis/files/7m01bk68h/d217qs47w/4f16c641b/frmprodcostreturn_Farm_Production_Practices_Costs_and_Returns__1910-48.pdf) The horse never got less noble, less strong, or less willing. Sentiment just never appeared as a row in anybody's books.

![Two stacked line charts sharing a year axis, 1910 to 1949. Horses and mules on US farms peak at 26.7 million in 1918 and fall to 8.3 million by 1949. Tractors on farms rise from about 1,000 in 1910 to 3.5 million in 1949.](/book-images/ch05-horses-tractors.svg)

*The herd and the machine. The horse didn't get worse; the ledger changed. Source: USDA Statistical Bulletin 83, table 14.*

**The mechanism.** The horse's owners argued about tradition, beauty, and loyalty. The machine's buyers ran operating cost per unit of work, alongside wages, feed, and credit. The arithmetic doesn't negotiate, and it doesn't send a warning before it closes the account.

**The rule.** You're a twenty-watt thinking engine inside a hundred-watt body, in a market that's started selling intelligence by the kilowatt-hour. Measure the task without pricing the person as obsolete, and audit your own ledger before somebody else runs the numbers on you. The horse found out its price after the fact. You still get to set some of the terms.

**The practice.**

1. Run the energy audit from this chapter on paper: what comes in (calories, kilowatt-hours, dollars), what goes out (labor, attention, rent), and who captures the spread. Most people have never once seen their own ledger the way a buyer would. The horse never saw its ledger at all.
2. List the tasks in your job the way a buyer would, then ask a coworker what the list missed. Mark the parts where you're competing on raw output against silicon, and the parts where you aren't: trust, presence, hands, judgment on the ground, relationships. Shift your effort toward the second list this quarter.
3. Move one meaningful expense from rented energy to owned energy this year: insulation, a bicycle that replaces short car trips, a panel and battery sized by someone who knows the job. Watt priced the horse in the horse's own currency. Every watt you own is a watt nobody can price you in.

---
