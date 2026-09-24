# Chapter 9: Deglobalization and the Neighborhood Factory

![Desktop 3D printer mid-print](/book-images/ch09-3d-printer.jpg)

*A desktop 3D printer. The neighborhood factory fits on a workbench. (John Abella, CC BY 2.0, via Wikimedia Commons)*



> *"The scattering of industries over the country … so as to bring the factory amidst the fields … is surely the next step to be made."*
> Peter Kropotkin, *Fields, Factories and Workshops* (revised edition, 1913), Chapter VII

**In this chapter:**

- You don't beat the global supply chain by lobbying it. You beat it by needing it less, one neighborhood at a time, without pretending you can do without it.
- A factory used to be a billion dollars and a river. Now it's a plasma table, a 3D printer, and somebody's cousin who can weld.
- Elegant is what a design is before it meets weather, budgets, and the parts that are actually in the drawer.
- The controller isn't dinner. Follow the food all the way to the person eating it.

---

The co-op's first real manufacturing run, the thing Elijah would later describe to strangers as *the neighborhood factory booting up*, though at the time it was just a January argument in a cold shed, was forty greenhouse controllers for the CSA network two valleys over.

The order came through a friend of a friend of Priya's: forty small boxes that could read soil moisture and air temperature and open a vent or a valve without asking a server in Virginia for permission. Real money, real deadline, real customers with real seedlings on the line. Elijah volunteered for the design with the eagerness of a man who had spent the autumn sweeping floors and learning the shop and could feel, at last, the shape of something he was actually trained to do.

He designed a beautiful thing. He wants that on the record, with the caveat that so does everyone in this story every time he says it. Custom four-layer PCB, an elegant little system-on-module, sensors from a Swiss outfit whose datasheets read like poetry, the whole thing potted in resin, sleek as a river stone, no user-serviceable parts inside. He presented it to the shop on a Tuesday with renders. *Renders.*

Marta looked at the renders for a while.

"Walk me through the bill of materials," she said, so he did, and she wrote three numbers on the whiteboard while he talked: **11**, **1**, **0**.

"Eleven weeks," she said, tapping the first number, "is the lead time on that Swiss sensor, I just looked it up, and that's the *quoted* lead time, which means it's a prayer. One," the second number, "is how many suppliers make that module, which means the day they discontinue it, all forty of these are bricks, and we're the ones who sold bricks to farmers. And zero," she tapped the last, "is how many people in this valley can fix a potted resin board when it fails during frost week. Including you, college. *Especially* you, because you'll be the one who's busy." She capped the marker. "It's a gorgeous design. It's a Claypot design. Everything single-sourced, nothing repairable, the whole thing optimized for the demo instead of the Tuesday three years from now when it breaks during calving. Design it again, and this time the spec is: parts from the drawer, parts from the junction box aisle, and nothing your neighbor can't fix with the tools he already owns."

"That'll be uglier," Elijah said.

"It'll be *ours*," Marta said. "Ugly is a maintenance feature. Ugly means the next guy can see how it works."

So he designed it again, and the second version was simpler to explain and repair: a Raspberry Pi the regional supplier had in stock, screw terminals instead of poetry, four-dollar capacitive probes you could swap by hand, a case Denny's kid printed forty of in PETG the color of school buses, and documented parts the growers could order from more than one source. The firmware did less and survived more. Every unit had a laminated one-page repair card zip-tied inside the lid, because Marta's rule was that documentation you have to go find is documentation that doesn't exist.

![A yellow PETG 3D-printed greenhouse controller box, lid open, a Raspberry Pi and screw terminals visible inside](/book-images/ch09-controller.png)

*The controller. Field-repairable. Screw terminals instead of poetry.*

The build itself took the shed three weekends, and it was during the second one, everyone deburring enclosures and crimping ferrules in an assembly line that Sal himself would have recognized from 1985, that the door opened and let in a rectangle of cold light and a lean man in a good coat who was too pleased with himself for a Saturday.

"Reuben Vance," Marta said, not looking up from the crimper. "Elijah. Elijah, Reuben. Reuben handles the part of the machine that runs on paper."

![A lean man in a well-tailored dark coat, carrying a leather folio of papers](/book-images/ch09-reuben.png)

*Reuben Vance. Handles the part of the machine that runs on paper.*

"I heard," Reuben said, pulling folding chairs toward the woodstove like a man dealing cards, "that this operation is about to *sell manufactured electrical goods across county lines*." He said it the way other men say *rob a train*. He produced a folder. "So I made a list. Registration, taxes, the use of this building, the promises on the invoice. Then I found people whose job it is to answer the parts I can't."

He laid three sheets beside the crimper. The seller registration had been filed. A tax adviser had marked the purchases that needed separate treatment. The county had asked for more information about the shed's mixed use. That one had a yellow tab.

"I thought agricultural equipment meant we were covered," Elijah said.

"You thought a noun was a permit. Happens all the time." Reuben tapped the tab. "This stays open until somebody with authority answers the actual question. And the invoice goes past counsel before it goes to a customer. Describing a thing as a farm tool doesn't make our promises disappear."

Elijah looked at the folder, then at Marta. "Did we ask him to do this?"

"Nobody asks Reuben," Priya said, from the crimping line. "Reuben *notices*."

The CSA hired an electrical technician to review the installation plan, and two growers tried the first units with their ordinary controls still available. Their notes came back covered in pencil: a label nobody could read in dim light, an alarm nobody heard over the fan, a sensor connection that needed better protection. Elijah revised the boxes before the rest went out.

By the time the forty units shipped in February, the yellow tab had an answer attached and the folder had grown thick enough to prop open a door. Denny delivered them in apple boxes, each one tested on the bench against a space heater and a cup of wet dirt, with the instructions and the agreed support number. Two growers needed replacement probes in the first month. With the power isolated and help from the support call, they could change the documented part without discarding the controller. Marta put the repair emails up on the corkboard like other shops hang their first dollar.

And somewhere in the middle of all that, without ceremony, somebody finally fixed Elijah's check-engine light. Curtis, it turned out, diagnosed it in nine minutes off a fourteen-dollar OBD dongle, a cracked vacuum line, two dollars of hose. The light had been on since the drive north. The dealership had quoted him twelve hundred dollars and a week; The man who wanted to fence out the world did the repair while the coffee brewed. He left the remaining length on the dashboard, coiled like a small black snake.

Elijah put the repair card for controller number forty in the folder. Curtis's hose went in the glove box.

---

## The Foundations

The strategy isn't to stop the big companies or to appeal to the conscience of people rich enough to fund rocket hobbies while veterans sleep outside. It's to build a working alternative so obviously better that switching to it becomes a no-brainer.

- **Deglobalization, not decentralization.** "Decentralized" is a slippery word, and it isn't the goal. Quality, safety, and protection against bad actors sometimes need a central standard. The real target is *deglobalization*: shortening the supply lines we depend on for survival, so a shock on the other side of the planet doesn't reach all the way to your dinner.
- **Neighborhood factories.** We already have factories. The shift is putting small, automated production capacity in every neighborhood and town, close enough that the people who use the goods can fix them.
- **Survival by charter.** That capacity should serve basic needs first: food, then shelter and care. Not by waiting for a government decree, but by writing it into the charter of your own infrastructure: the co-op bylaw that says the kitchen feeds whoever's hungry before it sells a single meal, the land-trust covenant that says nobody gets evicted into the market. Chapter 12 goes into how that ground gets held.
- **The prototype is already in backyards.** Drip lines that open on soil moisture. Sensor rigs that turn a raised bed into something closer to a Tamagotchi than a chore. Open, non-proprietary garden robots. None of it waits on anybody's permission.

![Two supply lines compared side by side: a long fragile global chain of raw material, overseas factory, ocean freight and last-mile truck, versus a short hyper-local loop of local material, neighborhood factory, and you](/book-images/ch09-hyperlocal-vs-global.svg)

*Not decentralization for its own sake. A shorter line: one you can hold in your head, that depends on your neighbors' hands instead of strangers far away.*

## A dense city can't feed itself, and it doesn't have to

The first objection to all this is always the same, and it's fair: New York City can't grow its own food. Neither can Los Angeles or Denver or anywhere people are stacked a hundred feet deep. Density is a feature, not a flaw, and hyper-local never meant every city block smelts its own steel.

The trick is to stop drawing the circle around the city and start drawing it around the region. A dense core doesn't have to make everything inside its own limits. It has to sit inside a ring of towns and counties that can fold food production, neighborhood factories, and materials recovery into the way they're already growing. That's not a fantasy. It's a jobs program: honest, well-paid, local work for the trades, the fabricators, the growers, and everyone who keeps a place running.

Think of it at the scale it deserves, which is Manhattan Project scale. Not a bunker in the woods. A deliberate, regional, out-loud build-out of the capacity to feed and house ourselves, handing the back-breaking work to machines. The goal is never to cut the city off from the world. It's to make sure that if the world's supply lines seize up for a week or a season, the region keeps its people fed instead of waiting on a truck that isn't coming. Resilience, not secession. So ask the only question that matters: if the trucks stopped tomorrow, how long could your region feed its people? Most places don't know. That gap is the work.

![A dense city core ringed by four surrounding municipalities that supply it: food production, materials recovery, energy and water, and neighborhood factories, with supply flowing inward to the core](/book-images/ch09-region-ring.svg)

*You don't deglobalize a city by walling it off. You ring it with towns that produce what it can't, which is also where the good jobs are.*

## The controller isn't dinner

The neighborhood factory earns its name when somebody can keep doing useful work because it exists. A repairable controller helps a grower. A local crew knows which part fails during the week nobody has a spare afternoon.

But food first means following the benefit past the machine. Growing, harvesting, handling, storage, cooking, and delivery all stand between a valve opening and a person eating. Rosa couldn't turn a bag of potatoes into dinner with one working hand. The crop was fine. The offer was wrong. How much food exists and what a person can actually eat are different questions, and any honest account of abundance keeps them apart.

## The nitrogen problem

Here's why the food system burns so much fuel, and what biology offers instead.

Plants need nitrogen, and the air is almost eighty percent nitrogen, but plants can't use it in that form. Industrial agriculture solves this with the Haber-Bosch process:

> **N₂ + 3H₂ → 2NH₃** (catalyst, high pressure, high temperature)

To force that reaction, plants run at 150 to 250 times atmospheric pressure and 400 to 500°C, with hydrogen made mostly from natural gas. Ammonia production eats roughly one to two percent of the world's energy supply and accounts for something over one percent of global energy-related carbon emissions. It also feeds billions of people. Synthetic fertilizer is one of the great achievements of the last century, and it's fossil energy stabilized in a bag.

Biology does the same chemistry at outdoor temperature. Legumes, clover, peas, beans, vetch, host *Rhizobium* bacteria in their roots, and those bacteria use an enzyme called nitrogenase to break the nitrogen triple bond:

> **N₂ + 8H<sup>+</sup> + 8e<sup>−</sup> + 16 ATP → 2NH₃ + H₂ + 16 ADP + 16 P<sub>i</sub>** (via nitrogenase)

The plant pays in sugar from sunlight. That's not the same job as the fungi that help roots take up phosphorus and water, and none of it means a garden feeds itself forever: every harvest carries nutrients away, and something has to put them back. But a living soil, managed well, can carry a lot of the load that currently comes from a gas well. (Chapter 15 goes down into the dirt.)

## What a garden robot actually does

FarmBot's own documentation describes a gantry on rails over a raised bed, driven by stepper motors to millimeter-class accuracy, with tool heads for seeding, watering, and weeding. [FarmBot tool documentation](https://farm.bot/pages/tools) Every plant becomes a coordinate. That's a concrete, useful set of tasks. It isn't a machine that harvests every crop, cooks a balanced diet, and delivers it for free, so keep the claim the size of the documented work.

![The CNC Autonomous Bed: a gantry travels the X-axis over a dense raised bed while a Z-axis tool head seeds, waters, and weeds plants addressed by X-Y coordinate, with no walking paths wasted](/book-images/ch09-cnc-bed.svg)

*The CNC bed. Every plant is a coordinate; the machine tends the grid from one rail.*

The UN Food and Agriculture Organization's 2022 report on agricultural automation looks at the opportunities alongside the barriers, especially for smaller farms. [FAO, The State of Food and Agriculture 2022](https://www.fao.org/agrifood-economics/publications/detail/en/c/1613500/) That's a reason to investigate useful automation and who can afford it, not proof that any one installation feeds a town.

### The greenhouse brain

For the controller in the scene, or one like it, the open-source project Mycodo turns a Raspberry Pi into an environmental controller: sensors in, relays out, and feedback loops in between.

![The Greenhouse Automation Bus: a Raspberry Pi running Mycodo reads an I2C sensor bus (SHT31-D air, STEMMA soil) and drives a GPIO relay board controlling a water solenoid, exhaust fan, and grow lights, in a closed sense-decide-actuate loop](/book-images/ch09-greenhouse-bus.svg)

*The greenhouse bus. Sensors in on I2C, low-voltage actuators out on relays, control loops in the middle.*

- **Sensors:** an air temperature and humidity sensor (the SHT31-D is common) and a capacitive soil-moisture probe, which resists corrosion better than the cheap resistive kind.
- **Actuators:** a relay board switching low-voltage devices: an exhaust fan, a solenoid valve on the irrigation line, supplemental lights. Have someone who knows electrical work check anything that touches mains power.

On a clean Raspberry Pi OS install, the project's documented installer is:

```bash
sudo apt update && sudo apt upgrade -y
curl -L https://kizniche.github.io/Mycodo/install | bash
```

Then browse to `https://<your-pi-ip>/` for the web interface. From there you can set up PID (proportional-integral-derivative) loops, the standard control law for holding a value steady:

> $$u(t) = K_p e(t) + K_i \int e(\tau) d\tau + K_d \, de(t)/dt$$

where $e(t)$ is the gap between the moisture you want and the moisture the probe reads, and the three $K$ values tune how hard and how smoothly the valve responds. Start with a grower's judgment about what the plants need, keep the manual valve working, and check the soil with your hands until you trust the numbers. (Chapter 15 is about what happens when you don't.)

## A worked example: one delivery, all the way through

Here's an illustrative project, not a reported trial. An established garden has permission to grow food on a suitable site. A local food group already has handling and distribution arrangements. They agree to try a small extra weekly delivery to five households that want it. Nobody has to own a robot or pay for the produce to get a share.

The garden tests whether an irrigation controller can cut down on routine checking without hurting the crop. A grower picks the settings. A volunteer records time spent, water used, failures, and manual interventions. The controller opens a valve; it doesn't decide a plant is safe to eat.

At harvest, people pick, sort, and weigh what's usable. The food group packs and delivers through its usual process. Recipients say whether it arrived and whether they could use it.

Suppose there are 10 kilograms of usable vegetables and the plan is two kilograms per household. Five deliveries fit. If two kilograms spoil first, the promise no longer fits. Write down the shortfall and get the replacement from the partner before calling the week a success. Don't quietly make the boxes lighter and leave the dashboard green.

| Item | Example entry |
| --- | --- |
| Promise | Five households each get two kilograms of vegetables they can use on Friday, free. |
| Machine's task | Open an irrigation valve on grower-approved settings. |
| Human work | Inspect crop and equipment; harvest, sort, pack, transport, confirm receipt. |
| Available after loss | Eight kilograms from the garden. |
| Remaining commitment | Two kilograms, sourced through the food partner before delivery. |
| Funding | Partner covers supplies and transport; donated time and existing equipment recorded separately. |
| Outcome to check | All five deliveries arrive, people can use them, and the partner's extra work shows up in the record. |

Those vegetables supplement meals. They don't make five complete diets. A dependable baseline needs enough suitable food across seasons, prepared food for people who can't cook, and a plan for interruptions. The small trial tests one contribution to that. The donated time and equipment get written down too, not called free: a permanent service can't run on a lucky month of volunteers.

## What would make the machine worth it?

Compare the whole arrangement with the ordinary way of doing it. The controller might cut water checks and add maintenance. It might let someone with a bad back do a job they couldn't before. It might save a paid worker time that the organization then fills with more work. Ask the worker which one happened. Sometimes a simple timer or one more paid shift is the better buy.

Then decide in advance where the saving goes: more free deliveries, better conditions for the people doing the work, a lower price, somebody's profit. A machine doesn't pick. The organization around it does. For the five-household trial, the partners could agree up front that any real saving goes first to keeping the promise and paying for the remaining work. That's a small, explicit wire between a technical gain and a fed person.

Five households getting vegetables is a contribution. A dependable baseline needs more food, more kinds of it, preparation, routes people can actually use, and a way to keep going through a failed crop or a broken van. It also needs a place for the household that wasn't one of the first five. So the next meeting belongs as much to growers, cooks, drivers, and the people receiving food as to the people holding the tools. Start small enough to learn. Keep the destination big enough to matter.

## Where to start this season

1. **Build the soil before the robot.** Spend your first fall layering organic mulch, wood chips, and compost into the beds, and let the biology build structure through the winter. A gantry over dead dirt is an expensive way to water sand.
2. **Save seed from what thrived.** Keep a little from your hardiest plants each year, alongside good seed you buy, and your garden slowly adapts to your place.
3. **Close one small loop.** Kitchen scraps into a worm bin, castings back into the beds. It won't make you independent of the world. It'll teach you, cheaply, how loops actually behave.

---

## Precedent P-12: The Networks Behind the Bronze (Eastern Mediterranean, fourteenth to twelfth centuries BC)

The Late Bronze Age was a globalized world. Bronze itself was a supply-chain product: copper from Cyprus, tin from sources far to the east, moving through trade networks that tied together Egypt, the Hittites, Mycenaean Greece, Ugarit, and Babylon. Palace economies specialized, traded, and grew rich on the interdependence.

You can put your hand on that network. Off the coast of what's now Turkey, a ship went down in the fourteenth century BC, and archaeologists excavating the Uluburun wreck brought up copper and tin ingots in roughly the proportions used to make bronze, along with glass, ivory, jewelry, and pottery. Some of the copper had been cast into the four-cornered shapes called oxhide ingots. [Institute of Nautical Archaeology, Uluburun excavation](https://nauticalarch.org/projects/uluburun-late-bronze-age-shipwreck-excavation/) It was an elite shipment: raw materials for wealthy workshops and luxuries for wealthy households. A rich network isn't the same thing as a secure household, and even then, people could tell the difference.

Around 1200 BC, that world came apart the way complex systems fail: not from one blow but from interacting pressures, drought, conflict, migration, political breakdown, and interrupted trade, unevenly, in different places at different times. Many of the great palace centers of the eastern Mediterranean were destroyed or abandoned, and in Greece writing fell out of use for centuries. [Knapp and Manning, Crisis in Context](https://doi.org/10.3764/aja.120.1.0099) There was no single year the Mediterranean switched off, and not every place fell the same way. But the most specialized, most interconnected palace economies had a great deal to lose when the tin stopped moving.

**The mechanism.** Interdependence is efficiency in fair weather and contagion in foul. When a critical input stops arriving, everything downstream of it stops being possible. Neither localism nor size guarantees survival; knowing your dependencies and having some ability to substitute for them is what helps.

**The rule.** Name the dependency and the disruption you're preparing for. Then decide, in advance, which side of the cascade your street is on.

**The practice.**

1. Map your tin. List the five things your household can't function without for a month: a medication, a fuel, a staple food, a spare part, a service. For each, trace where it actually comes from, as far up the chain as twenty minutes of looking will get you. Pick the most fragile line and build one local or stored alternative for it this quarter.
2. Take the neighbor census before you need it. Write down, or better, learn in person, which people within walking distance can fix an engine, stitch a wound, grow food, wire a panel, keep bees, weld. If you can't name five, that's your project for the season. The mesh network is mostly people.
3. Adopt the fair-weather buying rule: when two options are close, take the one that's repairable, local, or standardized over the one that's optimal and single-sourced. You're not paying extra for a product. You're paying for which side of the cascade your household sits on.

---
