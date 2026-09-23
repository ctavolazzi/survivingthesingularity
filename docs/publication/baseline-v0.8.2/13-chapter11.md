# Chapter 11: King and Queen of Your Own Robotic Court

![Boston Dynamics Spot quadruped robot](/book-images/ch11-spot.jpg)

*Spot. A robot demonstrates a particular set of physical capabilities. (Jonte, CC BY-SA 4.0, via Wikimedia Commons)*



**In this chapter:**

- Your robotic court begins with useful assistance, food first.
- A food baseline can coexist with restaurants and chosen work.
- Local computing still needs careful operation; the postmortem matters.

---

The servers arrived in mud season, in the back of Denny's truck: three retired enterprise machines from a county surplus auction, five years old, built like filing cabinets, sold for less than the co-op had spent that month on welding gas. Elijah had argued for the purchase all winter, and the argument that finally landed was not technical. "Every question we ask the cloud," he said at a Friday dinner, "goes out with an envelope of context around it. What we're building, what we're worried about, what we don't know yet. We're mailing our diary to the company store, one page at a time, and paying the postage."

Marta cared about one number, watts, and he had that answer ready, because a $211 power bill had taught it to him before anyone here knew his name. Priya wanted help searching the plant-pathology references she already trusted. Reuben wanted a first pass through forty pages of easement language before he brought his questions to counsel. Curtis wanted nothing to do with any of it, and said so, and that mattered later.

The rack went together the way everything in the shed went together: Marta on steel and power, Elijah on software, everyone else on opinions. Two scavenged compute cards with a combined forty-eight gigabytes of memory. A salvaged Civic radiator bolted to the shady north wall, two brass bulkheads through the corrugated steel, a marine pump the size of a fist. And on the first cold boot, fans screaming like weather, they loaded the model: a granddaughter of Silvana, open weights, three generations downstream of the thing that had started all of this, small enough now to live on scavenged silicon and capable enough to suggest wording, locate a likely bug, or turn a confusing manual into questions somebody could check. Elijah sat with that for a minute in the dark of the shed. The fire that had burned down his old life, purring in a stove he had built.

![A stack of three scavenged rack-mount servers beside a salvaged car radiator with brass pipe fittings](/book-images/ch11-crucible.png)

*The Crucible. Three filing cabinets and a salvaged radiator.*

For five weeks it did enough useful work that everyone learned to forgive the noise. Reuben found a cross-reference he'd missed, checked it against the document, and brought a better question to the next meeting. Priya's intern used it to find passages in the extension references, then caught it inventing a source and wrote that failure on the board beside the successes. The electricity meter kept turning. Elijah kept a log of what the machine had saved them and what checking it had cost.

He started calling the rack the Crucible. Priya said that was fine as long as the things that didn't survive testing stayed in the log.

The breach began with an ordinary convenience. Their system had no reliable stop between that convenience and everyone else's private life.

Elijah wanted his dashboards from town. Uptime, coolant temperature, the channel numbers, all of it on his phone while he sat at the library uploading Denny's videos on borrowed bandwidth. Fifteen minutes of work on a Friday night: a tunnel out, a reverse proxy in front of the co-op's services. While chasing a bug he commented out the authentication line, two slashes, to rule it out as the problem. He meant to put it back. He deployed with the comment marks still in.

What the proxy served, to anyone on earth who looked, was the mesh journal: the plain-text nervous system of nineteen households. Maintenance logs. Meeting minutes. The duty roster. The CSA customer list with addresses. Priya's greenhouse alarms. Marta's physical-therapy schedule, Tuesdays, for the shoulder she never mentioned. Which houses stood empty on which afternoons, computable by anyone who could read a grid log. All of it indexed, unauthenticated, public, for forty-one hours.

It was one of Denny's subscribers who caught it, a network engineer four states away, with a screenshot and one line: "you probably want to lock your journal, brother." Elijah killed the proxy before he finished reading the sentence. Then he pulled the access logs and did the arithmetic he would have paid anything not to do. Three crawlers had been through. You can delete a mistake from your own server. The internet does not run your deletion for you.

He thought about carrying it alone for exactly as long as it took to imagine Marta finding out some other way. Then he rang the dinner bell on a Sunday afternoon, which the co-op did not do, and stood in front of everyone it summoned and read them the timestamps.

Marta did not raise her voice, which everyone in the shed understood to be the worst available outcome. "You published which houses stand empty between two and four on a Tuesday," she said. "At the plant we had lockout-tagout. You don't work a press that can take your hand off unless the breaker is locked and your name is on the lock. You put our hands in the press, college."

Curtis said his piece, and for once it had teeth: this is what happens, you brought their machine inside the wire, pull the plug and melt it down. Heads were nodding when Priya, who had been quiet, set down her cup.

"Elijah left a service open," she said. "That is what the logs show. Pulling the model out won't change which service he exposed."

"He built it," Curtis said.

"Yes. And we let one person change the thing that held all our addresses. We put information together without asking whether it needed to be together. Then we treated his confidence as our check." She looked at Elijah. "You owe us the truth about what happened. We owe ourselves a design that doesn't depend on you never having a bad Friday."

Reuben spent the next two days doing what Reuben does. The customer list crossed county lines; he mapped the exposure, drafted the letter to every family on it, and answered the question nobody had asked out loud: "I can build you an argument that we don't owe anyone notice. I'd rather we not be the people who went looking for that argument."

It was Denny who found the judo in it. "People already know things break," he said. "What they never once get to see is somebody stand up and say so." After the affected households reviewed what could be shared, they published an account on the channel: the categories of information exposed, the duration, the notification process, and the changes. The private records stayed out of the report. Elijah read it to the camera himself, because it was his name on the lock. It traveled further than anything they had posted except Denny's first video. Strangers wrote to say it was the first incident report they had ever read that was not written by lawyers. Two of them drove out that summer to help harden the mesh for free.

At that first Sunday meeting, the co-op had adopted a new rule: a change exposing a service to the internet needed a second reviewer and a recorded check of what an outsider could reach. They separated the private records from the public material and assigned someone besides Elijah responsibility for reviewing access. Marta called it borrowing a habit from lockout-tagout. The analogy gave them a place to start; the network needed its own procedures. The model server came off the external network. Updates arrived by hand after that, with the source and file checks recorded before installation, the disk carried home in Elijah's jacket. The team still had to inspect what it brought into the room.

The pump kept ticking. The radiator clicked against the north wall. When Reuben next asked the machine to summarize a document, he still had to read the document. The leak had not taught Elijah machine learning; he had arrived knowing that. It taught him the difference between knowing a system and operating one, and the tuition was forty-one hours of other people's privacy. The checklist was a beginning. It was not the last thing they would have to learn.

---

## The Foundations

## Useful help within reach

King and Queen of Your Own Robotic Court is a playful name for a serious change in who gets assistance. I want the person who needs help to be able to obtain it without first becoming wealthy, technically expert, or employable in the latest fashionable field.

The first assignment is food. A suitable farm machine, a kitchen, a distribution service, planning software, and the people maintaining each part might together provide it. The person eating doesn't need to own every component any more than a person reading a library book needs to own the printing press.

What matters is a usable claim on the result. Can you obtain adequate food when your income stops? Can you request a form you can eat and prepare? Can you get an answer when a delivery fails? Can you criticize the service without losing your next meal?

Those questions describe the difference between admiring somebody else's productive power and having some security of your own.

## Free to eat, paid for somewhere

The line cook from Chapter 7 still matters here. He has lost a job. A restaurant can continue selling meals, and a funded food service can provide him with dinner. There is no logical contradiction between those arrangements.

There is an operating budget to arrange.

Consider one possible service, offered here as a design to evaluate rather than an existing program. A local public body funds a food partnership for a defined period. The partnership pays growers for agreed supplies and a kitchen for preparing meals. It pays for delivery, maintenance, and the human work still required. Recipients can collect or request the appropriate service without paying at the door. Some participating kitchens could be restaurants earning income for that work.

A cooperative could organize a similar service around assets its members share. An existing public or charitable provider could add useful automation to work it already does. The institutional form will affect who decides, where resources come from, and what people can claim if provision fails. Those differences deserve debate; the word cooperative isn't a substitute for a budget, and the word public isn't a substitute for accountability.

The money might come from an agreed public allocation, pooled contributions, purchased services, or a combination. The source, duration, and conditions need to be visible before the offer is described as dependable. Voluntary donations can help begin a project. They should not quietly carry a permanent promise nobody has financed.

An adequate baseline for everyone would require provision beyond this illustrative local service. But the organizing distinction is already clear: receiving food and paying for its production can be separated. We don't have to make a hungry person produce the money before we decide how to do the work.

A baseline could change demand and the terms on which people accept work. Some restaurants might need better pay, different hours, or a different business model. Some could close. I can't promise every existing margin survives. Providing adequate food doesn't require abolishing paid meals, and a worker's hunger shouldn't be the protection a business model depends on. The people supplying the baseline also need compensation and conditions they can sustain.

## A public meal, and an argument about it

On May 28, 1941, the House of Commons discussed a practical obstacle to feeding people during wartime: some local authorities had not prepared communal feeding centers. The Ministry of Food had assigned officers to help establish British Restaurants. But encouragement was one thing and authority another. When an MP asked whether the ministry could establish a restaurant where a council failed to act, its parliamentary secretary could not give a definite answer. Even an urgent national purpose needed someone empowered to carry it out locally. [Hansard, May 28, 1941](https://api.parliament.uk/historic-hansard/commons/1941/may/28/british-restaurants)

The restaurant objection was there too. On October 1, Sir Percy Hurd challenged the treatment of private caterers alongside the public service. The ministry replied that rationed supplies were allocated on the same basis, according to meals served, while some scarce foods received priority for feeding workers. Public kitchens and private businesses existed together; their terms were already being argued over. [Hansard, October 1, 1941](https://api.parliament.uk/historic-hansard/commons/1941/oct/01/british-restaurants-and-works-canteens)

The next day's debate sharpened both sides. A critic with catering interests alleged that British Restaurants were taking customers from struggling businesses. He also described a public restaurant at Fishmongers' Hall that opened at noon, too late for the Billingsgate workers he wanted it to serve. These were claims made in debate, not an independent audit. But the second complaint gives the proposal a useful test: a kitchen can exist, have supplies, and still miss the person whose working day it was supposed to help. [Hansard, October 2, 1941](https://api.parliament.uk/historic-hansard/commons/1941/oct/02/food-distribution-1)

British Restaurants charged for meals. In March 1942, the ministry described prices covering food, preparation, overhead, and a contingency margin, with accounts submitted for review. This was no universal entitlement to free dinner. It was a working example of public authorities organizing meals and accounting for the work. Our proposal changes who pays at the point of eating. It still needs the kitchen, the budget, and opening hours that fit a human life. [Hansard, March 17, 1942](https://hansard.parliament.uk/commons/1942-03-17/debates/55709938-4ce9-4237-ba1f-14645cb0f860/WrittenAnswers)

## Ownership matters because access can be withheld

Suppose the machines work beautifully. Now suppose one company owns them, controls the supplies they need, and can stop service when a subscription lapses. Productive capacity has increased. Security for the person who can't pay may not have changed at all.

That is why the proposal includes social organization. Shared ownership is one possibility. Public provision and funded purchases from private providers are others. Whatever the arrangement, ask who can raise the charge, change the conditions, withdraw the service, or sell the assets. Ask how recipients and workers can challenge those decisions.

A food program should also avoid making itself the only door through which a person can obtain help. Several providers, supplies held for interruptions, repairable equipment, and routes that work without a proprietary account can reduce particular dependencies. They don't eliminate the need for outside resources. They give people more than a single promise to lean on.

For me, meaningful control is the ability to understand the terms, influence decisions that affect your life, and obtain a remedy when a commitment is broken. A server in your shed may help with some of that. It can't create the arrangement on its own.

## Help should enlarge a life

The fear that assistance could make us passive is worth examining. A system could remove choices, erode skills, or place recipients under intrusive supervision. It could also leave someone with the time and strength to raise a child, practice an instrument, recover from illness, or do work they choose.

Receiving substantial help isn't a moral failure. Many of us will need it, and all of us have depended on work we couldn't do for ourselves. The test is what the arrangement makes possible and what it demands in return.

A meal should not require a performance of ambition. A person who prefers to rest today hasn't thereby forfeited dinner. A person who wants paid work should have room for that too. The larger hope is that necessary effort becomes less exhausting and its benefits more widely available, giving different people more freedom to live differently.

We will still need competence. Someone has to maintain the equipment, recognize a bad result, and know when to stop. Paying, supporting, and training those people belongs inside the program. Otherwise assistance for one household is being purchased with somebody else's hidden exhaustion.

## Choose the boundary before the machine

The Crucible breach began with an access failure. Other failures could begin with an unreliable answer, an unsuitable model, or a decision the system was never fit to make. Good intentions do not settle any of those questions.

Give a tool work that can be checked before its mistakes become someone else's emergency. A model can propose a pickup schedule; a coordinator checks the vehicles, recipients' needs, and actual commitments. A model can help find a relevant passage; a person verifies the source. A model's confident explanation doesn't authorize it to decide that food is safe or machinery is ready to run.

Local, offline, and air-gapped describe different things. Local means the work runs on nearby equipment. Offline means it works without the relevant connection. An air gap requires deliberate separation from the network in question. None of those terms establishes that the software is accurate or the data safe. Transfers, updates, permissions, and the information collected still need attention.

The co-op learned something else: a design can fail by depending too much on one careful person. Another review, a smaller collection of private information, and a separation between public and private services would each have addressed part of their exposure. The repair belongs to the whole arrangement, not merely to Elijah's promise to be more careful.

## One request, all the way through

Before buying a machine, write down one request a person should be able to make. For example: “I need meals I can heat with one working hand, and I can't pay for them this month.”

Follow that request through the proposed service. Who receives it? Who confirms supplies and appropriate preparation? Who pays the people doing the work? How does the meal arrive? Who responds if it doesn't? Put the proposed tool beside the task it can actually help perform.

Then check the route with a willing provider and a person whose circumstances the request represents. They may show you that the missing piece is a kitchen slot, a driver, a phone number someone answers, or a funding agreement. A robot may become useful at one of those points as its capabilities develop.

That is a court worth building: assistance with a destination in somebody's life.

---

## Precedent P-14: Quartz and the Assembly Line (Switzerland, 1962 to 1983)

Quartz technology and industrial change put Swiss watchmaking under substantial pressure. The Swiss industry was also involved in developing quartz; it was not a single bloc that refused the technology out of purity.

The dates complicate the familiar story of a tradition surprised by electronics. A consortium of Swiss manufacturers established the Centre Electronique Horloger in 1962; its quartz wristwatch prototypes followed in 1967. Swiss researchers were helping make the change. [CSEM, Historical Timeline](https://www.csem.ch/en/history-and-start-ups)

The 1983 Swatch paired a different product with different production: fifty-one components, assembled on automated lines. That detail matters more than a slogan about embracing the future. Product design and the method of assembly changed together. [Swatch Group, Company History](https://www.swatchgroup.com/en/swatch-group/swatch-group-history)

The later Swatch story offers an example of adaptation through products, manufacturing, and restructuring. It should not be made into a claim that only one strategy has ever worked or that success at the industry level erased the losses experienced by workers.

**The mechanism.** An industry can combine technical change, restructuring, and differentiated products. That does not establish one universally successful strategy or erase workers' losses.

**The rule.** Examine specific adaptations and their costs.

**The practice.**

1. Identify the part of a craft people still choose to pay for.
2. Ask which tools support it and which pressures threaten it.
3. Do not infer an individual worker's options from a large firm's resources.

---

