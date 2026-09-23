# Chapter 11: King and Queen of Your Own Robotic Court

![Boston Dynamics Spot quadruped robot](/book-images/ch11-spot.jpg)

*Spot. The same machines ending careers will happily work for you. (Jonte, CC BY-SA 4.0, via Wikimedia Commons)*



> *"Give me a place to stand, and I shall move the Earth."*
> attributed to Archimedes

**In this chapter:**

- The same class of machine that's ending careers can work for you, on hardware the corporate upgrade cycle throws away. Its first job at your court: food.
- Every cloud query is a page of your diary mailed to the company store. Local compute is one of the last private places left to think.
- A food baseline and a restaurant can coexist. The meal is free at the door and paid for somewhere.
- One careless config line published nineteen households of ordinary life to the open internet for 41 hours. The discipline is part of the tool. So is the honest postmortem.

---

The servers arrived in mud season, in the back of Denny's truck: three retired enterprise machines from a county surplus auction, five years old, built like filing cabinets, sold for less than the co-op had spent that month on welding gas. Elijah had argued for the purchase all winter, and the argument that finally landed was not technical. "Every question we ask the cloud," he said at a Friday dinner, "goes out with an envelope of context around it. What we're building, what we're worried about, what we don't know yet. We're mailing our diary to the company store, one page at a time, and paying the postage."

Marta cared about one number, watts, and he had that answer ready, because a $211 power bill had taught it to him before anyone here knew his name. Priya wanted help searching the plant-pathology references she already trusted. Reuben wanted a first pass through forty pages of easement language before he brought his questions to counsel. Curtis wanted nothing to do with any of it, and said so, and that mattered later.

The rack went together the way everything in the shed went together: Marta on steel and power, Elijah on software, everyone else on opinions. Two scavenged compute cards with a combined forty-eight gigabytes of memory. A salvaged Civic radiator bolted to the shady north wall, two brass bulkheads through the corrugated steel, a marine pump the size of a fist. And on the first cold boot, fans screaming like weather, they loaded the model: a granddaughter of Silvana, open weights, three generations downstream of the thing that had started all of this, small enough now to live on scavenged silicon and capable enough to suggest wording, locate a likely bug, or turn a confusing manual into questions somebody could check. Elijah sat with that for a minute in the dark of the shed. The fire that had burned down his old life, purring in a stove he had built.

![A stack of three scavenged rack-mount servers beside a salvaged car radiator with brass pipe fittings](/book-images/ch11-crucible.png)

*The Crucible. Three filing cabinets and a salvaged radiator.*

For five weeks it was purely good. Reuben fed it easements and it found a cross-reference he'd missed; he checked it against the document and brought a sharper question to counsel. Priya's intern learned blight triage from it in an afternoon, then caught it inventing a source and wrote that failure on the board beside the successes. It never got tired and it never billed and it never, not once, phoned home, because there was no home to phone. The electricity meter kept turning. Elijah kept a log of what the machine had saved them and what checking it had cost.

He started calling the rack the Crucible. Priya said that was fine as long as the things that didn't survive testing stayed in the log.

The breach began with an ordinary convenience. Their system had no reliable stop between that convenience and everyone else's private life.

Elijah wanted his dashboards from town. Uptime, coolant temperature, the channel numbers, all of it on his phone while he sat at the library uploading Denny's videos on borrowed bandwidth. Fifteen minutes of work on a Friday night: a tunnel out, a reverse proxy in front of the co-op's services. While chasing a bug he commented out the authentication line, two slashes, to rule it out as the problem. He meant to put it back. He deployed with the comment marks still in.

What the proxy served, to anyone on earth who looked, was the mesh journal: the plain-text nervous system of nineteen households. Maintenance logs. Meeting minutes. The duty roster. The CSA customer list with addresses. Priya's greenhouse alarms. Marta's physical-therapy schedule, Tuesdays, for the shoulder she never mentioned. Which houses stood empty on which afternoons, computable by anyone who could read a grid log. All of it indexed, unauthenticated, public, for forty-one hours.

It was one of Denny's subscribers who caught it, a network engineer four states away, with a screenshot and one line: "you probably want to lock your journal, brother." Elijah killed the proxy before he finished reading the sentence. Then he pulled the access logs and did the arithmetic he would have paid anything not to do. Three crawlers had been through. You can delete a mistake from your own server. The internet does not run your deletion for you.

He thought about carrying it alone for exactly as long as it took to imagine Marta finding out some other way. Then he rang the dinner bell on a Sunday afternoon, which the co-op did not do, and stood in front of everyone it summoned and read them the timestamps.

Marta did not raise her voice, which everyone in the shed understood to be the worst available outcome. "You published which houses stand empty between two and four on a Tuesday," she said. "At the plant we had lockout-tagout. You don't work a press that can take your hand off unless the breaker is locked and your name is on the lock. You put our hands in the press, college."

Curtis said his piece, and for once it had teeth: this is what happens, you brought their machine inside the wire, pull the plug and melt it down. Heads were nodding. Marta let them nod for a moment.

"The first family that ever kept fire burned something down," Marta said. "A roof, a winter store, somebody's child. And nobody handed the fire back. They built the hearth. Stones in a circle, rules about who tends it, a bucket that never goes empty." She looked at Elijah, and it was not a rescue. "We didn't get burned by the model, Curtis. We got burned by a boy who left it lit on the porch rail."

Priya, who had been quiet, set down her cup. "Pulling the model out won't change which service he exposed."

"He built it," Curtis said.

"Yes. And we let one person change the thing that held all our addresses. We put information together without asking whether it needed to be together. Then we treated his confidence as our check." She looked at Elijah. "You owe us the truth about what happened. We owe ourselves a design that doesn't depend on you never having a bad Friday."

Reuben spent the next two days doing what Reuben does. The customer list crossed county lines; he mapped the exposure, drafted the letter to every family on it, and answered the question nobody had asked out loud: "I can build you an argument that we don't owe anyone notice. I'd rather we not be the people who went looking for that argument."

It was Denny who found the judo in it. "People already know things break," he said. "What they never once get to see is somebody stand up and say so." After the affected households reviewed what could be shared, they published an account on the channel: the categories of information exposed, the duration, the notification process, and the changes. The private records stayed out of the report. Elijah read it to the camera himself, because it was his name on the lock. It traveled further than anything they had posted except Denny's first video. Strangers wrote to say it was the first incident report they had ever read that was not written by lawyers. Two of them drove out that summer to help harden the mesh for free.

At that first Sunday meeting, the co-op had adopted a new rule: a change exposing a service to the internet needed a second reviewer and a recorded check of what an outsider could reach. They separated the private records from the public material and assigned someone besides Elijah responsibility for reviewing access. Marta called it borrowing a habit from lockout-tagout. The analogy gave them a place to start; the network needed its own procedures. The model server came off the external network. Updates arrived by hand after that, with the source and file checks recorded before installation, the disk carried home in Elijah's jacket. The team still had to inspect what it brought into the room.

The pump kept ticking. The radiator clicked against the north wall. When Reuben next asked the machine to summarize a document, he still had to read the document. The leak had not taught Elijah machine learning; he had arrived knowing that. It taught him the difference between knowing a system and operating one, and the tuition was forty-one hours of other people's privacy. The machine went on drafting and checking and never billing, the radiator clicking against the north wall while it thought. Fire in its stones.

---

## The Foundations

## Useful help within reach

King and Queen of Your Own Robotic Court is a playful name for a serious change in who gets help. I want the person who needs assistance to be able to get it without first becoming rich, technical, or employable in this year's fashionable field.

The first assignment is food. A farm machine, a kitchen, a delivery service, some planning software, and the people who keep each of them running might together provide it. The person eating doesn't need to own every piece, any more than someone reading a library book needs to own the printing press. What matters is a usable claim on the result. Can you get adequate food when your income stops? Can you ask for a form you can actually eat? Can you get an answer when a delivery fails? Can you complain without losing your next meal?

You don't need to be an engineer to put these tools to work. You need to be persistent. Treat a good model as a tireless research assistant. If the answer is generic, argue with it. Push it to be specific. Ask it for the procedure, the part number, the code section. Then check what it tells you against the source, because it will sometimes make things up with a perfectly straight face, the way it did for Priya's intern.

- **Teach yourself.** Use it to learn the technical task in front of you: how to read a wiring diagram, how to troubleshoot a pump, how to set up a simple spreadsheet that tracks deliveries. Make the machine explain, not just do.
- **Read the ground.** Use it alongside public maps and records: county parcel records, zoning codes, soil surveys, water maps, the Bureau of Land Management's land records where they apply. Once you understand the rules of the place you live, you stop being surprised by them.

## Free to eat, paid for somewhere

The line cook from Chapter 7 still matters here. He's lost his job. A restaurant can keep selling meals, and a funded food service can give him dinner. There's no contradiction between those two arrangements. There's an operating budget to arrange.

Here's one design to argue about, not an existing program. A local public body funds a food partnership for a set period. The partnership pays growers for agreed supplies and a kitchen to prepare meals. It pays for delivery, maintenance, and the human work that's still needed. People collect or request the meal without paying at the door. Some of the participating kitchens could be restaurants, earning money for the work.

A co-op could run something similar on shared equipment. An existing food bank could add useful automation to work it already does. The form matters: it decides who's in charge, where the money comes from, and what people can claim when it breaks. "Cooperative" isn't a budget, and "public" isn't accountability. The money might come from a public allocation, pooled contributions, purchased services, or a mix. Donations can start a project. They shouldn't quietly carry a permanent promise nobody's actually funded.

A food baseline would change some things. Some restaurants might need better pay, different hours, or a different business model. Some could close. I can't promise every existing margin survives. But providing dinner doesn't require abolishing paid meals, and a worker's hunger shouldn't be the protection a business model depends on.

## A public meal, and an argument about it

On May 28, 1941, the House of Commons discussed a practical obstacle to feeding people during wartime: some local authorities had not prepared communal feeding centers. The Ministry of Food had assigned officers to help establish British Restaurants. But encouragement was one thing and authority another. When an MP asked whether the ministry could establish a restaurant where a council failed to act, its parliamentary secretary could not give a definite answer. Even an urgent national purpose needed someone empowered to carry it out locally. [Hansard, May 28, 1941](https://api.parliament.uk/historic-hansard/commons/1941/may/28/british-restaurants)

The restaurant objection was there too. On October 1, Sir Percy Hurd challenged the treatment of private caterers alongside the public service. The ministry replied that rationed supplies were allocated on the same basis, according to meals served, while some scarce foods received priority for feeding workers. Public kitchens and private businesses existed together; their terms were already being argued over. [Hansard, October 1, 1941](https://api.parliament.uk/historic-hansard/commons/1941/oct/01/british-restaurants-and-works-canteens)

The next day's debate sharpened both sides. A critic with catering interests alleged that British Restaurants were taking customers from struggling businesses. He also described a public restaurant at Fishmongers' Hall that opened at noon, too late for the Billingsgate workers he wanted it to serve. These were claims made in debate, not an independent audit. But the second complaint gives the proposal a useful test: a kitchen can exist, have supplies, and still miss the person whose working day it was supposed to help. [Hansard, October 2, 1941](https://api.parliament.uk/historic-hansard/commons/1941/oct/02/food-distribution-1)

British Restaurants charged for meals. In March 1942, the ministry described prices covering food, preparation, overhead, and a contingency margin, with accounts submitted for review. This was no universal entitlement to free dinner. It was a working example of public authorities organizing meals and accounting for the work. Our proposal changes who pays at the point of eating. It still needs the kitchen, the budget, and opening hours that fit a human life. [Hansard, March 17, 1942](https://hansard.parliament.uk/commons/1942-03-17/debates/55709938-4ce9-4237-ba1f-14645cb0f860/WrittenAnswers)

## The objections, answered once

You'll hear these. Here's how I'd answer each of them.

**"Won't having robots clean up after us make people stop caring?"** It could, if we build a service that encourages carelessness. That's a real concern, and we should watch what actually happens. We can make disposal easier, keep trash from escaping in the first place, and clean up what still gets through, then check whether the place stays cleaner overall. The trash doesn't tell you how it got there, either: wind, runoff, and overflowing bins carry plenty of it, and deliberate dumping happens too. Different problems, different responses. Leaving trash in a river is a poor way to teach responsibility.

**"Isn't this how we end up like WALL-E?"** The worry underneath is worth taking seriously: dependence, lost skills, a life with fewer choices. I want help that gives us *more* room to move, learn, make things, care for each other, and take part. Some people will need more help than others, and receiving it doesn't make them less worthy. Whether a tool widens a life or quietly shrinks it is something we can watch and change.

**"We already know how to do this without robots."** Yes. A robot doesn't have to be the answer. Sometimes a better bin, an existing crew, or a simpler machine does more good. But knowing how to do something isn't the same as making it available, affordable, and dependable everywhere it's needed. Compare the options and use whatever does the work well. There are many ways to make an omelette.

**"But what about the jobs?"** Dishwashers and washing machines make the idea of handing repetitive work to a machine familiar. That comparison doesn't pay the bills of someone whose income just disappeared, and their concern is real. Workers belong in the decisions about how these tools come in and how people are supported through the change. That's what this whole book is arguing for.

**"Why not send machines into the dangerous work?"** Where a suitable machine can keep people out of harm's way, that's a good reason to look hard at it, with the people who know the job. The deployment still has to show that it helps, including the work of maintaining and recovering the machine.

## Ownership matters because access can be withheld

Suppose the machines work beautifully. Now suppose one company owns them, controls their supplies, and can cut off service when a subscription lapses. Productive capacity went up. Security for the person who can't pay may not have moved at all.

So whatever the arrangement, shared ownership, public provision, or paying private providers, ask who can raise the price, change the rules, withdraw the service, or sell the equipment, and how the people receiving it and the people working it can challenge those decisions. And don't let any one program become the only door to help. Several providers, supplies held back for bad weeks, repairable equipment, and routes that don't need a proprietary account all make the promise sturdier.

## The Crucible: local compute you own

The scene's argument for owning the machine was privacy, and it's a good one. Every question you send a cloud service carries context with it: what you're building, what you're worried about, what you don't know. For a lot of work that's fine. For some of it, a food program's recipient list, a family's medical questions, a co-op's legal strategy, you'd rather it never left the building. Local compute is one of the last private places left to think.

You don't need enterprise money. Every few years, data centers retire perfectly good hardware onto the used market, and the co-op's rack came from exactly that: a county surplus auction.

### The memory math

For running language models, the bottleneck usually isn't raw processing speed. It's memory: the model's weights have to fit in the graphics card's memory (VRAM) to run fast. A good rule of thumb:

> $$V_{RAM} \approx \frac{P \cdot Q}{8} \cdot B \text{ [GB]}$$

where $P$ is the number of parameters in billions, $Q$ is the bits stored per weight (16 for full precision, 4 or 8 for compressed "quantized" versions), dividing by 8 turns bits into bytes, and $B \approx 1.2$ is a buffer for the working memory a conversation needs.

**A small model at full precision.** An 8-billion-parameter model at 16 bits:

> $$V_{RAM} = \frac{8 \cdot 16}{8} \cdot 1.2 = 19.2 \text{ GB}$$

That fits on one used 24 GB card.

**A large model, compressed.** A 70-billion-parameter model at 4 bits:

> $$V_{RAM} = \frac{70 \cdot 4}{8} \cdot 1.2 = 42 \text{ GB}$$

That needs two 24 GB cards, 48 GB together, which is what the co-op scavenged. Open tools like llama.cpp can split a model's layers across both cards. Ollama runs the models; a local chat interface like Open WebUI puts a friendly front on them. None of it needs to touch the internet to work.

### The heat math

A rack like that throws off somewhere between 600 and 1,000 watts of heat, all day. Inside an insulated building, that's a sauna you're paying an air conditioner to fight. The co-op's answer was to carry the heat outside in liquid. The physics is one line:

> $$\dot{Q} = \dot{m} \cdot C_p \cdot \Delta T$$

To move 1,000 watts with a water-glycol coolant ($C_p \approx 3{,}800$ J/kg·°C) while letting it warm only 5°C through the loop:

> $$\dot{m} = \frac{1000}{3800 \cdot 5} \approx 0.053 \text{ kg/s} \approx 3.2 \text{ liters per minute}$$

That's a gentle flow; a small pump the size of a fist handles it. A salvaged car radiator on a shady outside wall dumps the heat.

![The Split-Loop Thermal Exchange: GPU and CPU water blocks inside the insulated shell feed a 12V pump that sends hot coolant through the wall to a salvaged car radiator in free air, with cool coolant returning to the chips](/book-images/ch11-cooling-loop.svg)

*The split loop. Pull the heat off the silicon and dump it outside, instead of paying an air conditioner to fight your own server.*

### Choose the boundary before the machine

The Crucible breach started with an access failure. Other failures start with an unreliable answer, the wrong model for the job, or a decision the system was never fit to make. Good intentions settle none of those.

Give a tool work that can be checked before its mistakes become someone else's emergency. A model can propose a delivery schedule; a coordinator checks the vehicles and what people actually need. A model can find a relevant passage; a person reads the source. A confident explanation doesn't authorize a machine to decide that food is safe or equipment is ready to run.

And keep the words straight. *Local* means it runs on nearby equipment. *Offline* means it works without a connection. An *air gap* means deliberate, physical separation from a network. None of those means the software is right or the data is safe. Keep the system patched, from sources you've verified. Collect as little private information as the job needs. Keep public and private services separate. Have a second person check anything that exposes a service to the internet, and test what an outsider can actually reach. The co-op learned that the hard way: a design shouldn't depend on one careful person never having a bad Friday.

## Help should enlarge a life

Receiving a lot of help isn't a moral failure. Many of us will need it, and all of us have depended on work we couldn't do ourselves. The test is what the arrangement makes possible and what it demands in return.

A meal shouldn't require a performance of ambition. A person who wants to rest today hasn't forfeited dinner. A person who wants paid work should have room for that too. And somebody still has to maintain the equipment, recognize a bad result, and know when to stop. Paying, training, and supporting those people belongs inside the program. Otherwise one household's help is being bought with somebody else's hidden exhaustion.

## One request, all the way through

Before buying a machine, write down one request a person should be able to make. For example: "I need meals I can heat with one working hand, and I can't pay for them this month."

Follow that request through the service. Who receives it? Who confirms the food and how it's prepared? Who pays the people doing the work? How does the meal arrive? Who answers if it doesn't? Then put your proposed tool next to the one task it can actually help with. Check the route with a willing provider and with someone whose life the request describes. They may show you the missing piece is a kitchen slot, a driver, a phone number somebody answers, or a funding agreement. A robot may fit at one of those points as it gets more capable.

That's a court worth building: help with a destination in somebody's life.

---

## Precedent P-14: Quartz and the Assembly Line (Switzerland, 1962 to 1983)

The story everyone tells is that the Swiss, masters of mechanical watchmaking, sneered at the quartz watch and got wiped out by it. The real story is stranger and more useful.

The Swiss helped invent quartz timekeeping. A consortium of Swiss watchmakers founded the Centre Electronique Horloger in 1962, and its quartz wristwatch prototypes followed in 1967. [CSEM, Historical Timeline](https://www.csem.ch/en/history-and-start-ups) Seiko put the first quartz wristwatch on sale in 1969. Then came the crunch, from several directions at once: cheap quartz movements, a strong franc, and an industry built around costly mechanical production. [Seiko Museum, The Quartz Crisis and Recovery of Swiss Watches](https://museum.seiko.co.jp/en/knowledge/relation_11/) Between 1970 and the mid-1980s, Swiss watch employment fell from roughly ninety thousand to about a third of that, and the number of firms collapsed with it. Knowing about the technology wasn't enough. The business around it had to change, and for a lot of people it changed too late.

What saved the remnant was a kind of heresy. In 1983 the merged Swiss group launched the Swatch: a cheap, plastic, fifty-one-component quartz watch, assembled on automated lines. [Swatch Group, Company History](https://www.swatchgroup.com/en/swatch-group/swatch-group-history) It took the new technology to the bottom of the market, and the company that grew around it went on to own some of the most famous names in mechanical watchmaking at the top. The quartz Trojan horse helped pay for the craft it seemed to threaten.

**The mechanism.** Survival came from adopting the new technology on your own terms and using its output to support what you meant to keep. None of that erased the losses of the tens of thousands of workers who didn't make it through, and a big firm's options are never an individual's.

**The rule.** Don't beat the new machine by refusing it. Use it to pay for what you actually want to keep.

**The practice.**

1. Name your mechanical movement and your Swatch. On one line, write the thing you refuse to lose: the craft, the practice, the standard of work that's actually you. On the next line, sketch the cheap, fast, machine-assisted offering that could fund it. If the second line feels like a betrayal of the first, you've drawn it correctly.
2. Set the subsidy ratio and stick to it. Decide what fraction of your machine-assisted income funds the protected craft, time, tools, or savings, and write it down like a tax you owe yourself. Leverage without allocation is just drift.
3. Refuse purity tests, including your own. The next time someone says "real professionals don't use AI," translate it into 1975: "real watchmakers don't do quartz." Then remember that the Swiss were building quartz watches the whole time, and still nearly lost the industry. Adopting the tool is necessary. It isn't sufficient.

---
