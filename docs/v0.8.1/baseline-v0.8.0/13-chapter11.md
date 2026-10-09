# Chapter 11: King and Queen of Your Own Robotic Court

![Boston Dynamics Spot quadruped robot](/book-images/ch11-spot.jpg)

*Spot. A robot demonstrates a particular set of physical capabilities. (Jonte, CC BY-SA 4.0, via Wikimedia Commons)*


> *"Give me a place to stand, and I shall move the Earth."*
> attributed to Archimedes, *via Pappus of Alexandria* (c. 340 AD)

**In this chapter:**

- Your robotic court begins with useful assistance, food first.
- A food baseline can coexist with restaurants and chosen work.
- Local computing still needs careful operation; the postmortem matters.

---

The servers arrived in mud season, in the back of Denny's truck: three retired enterprise machines from a county surplus auction, five years old, built like filing cabinets, sold for less than the co-op had spent that month on welding gas. Elijah had argued for the purchase all winter, and the argument that finally landed was not technical. "Every question we ask the cloud," he said at a Friday dinner, "goes out with an envelope of context around it. What we're building, what we're worried about, what we don't know yet. We're mailing our diary to the company store, one page at a time, and paying the postage."

Marta cared about one number, watts, and he had that answer ready, because a $211 power bill had taught it to him years before anyone here knew his name. Priya wanted the plant-pathology models. Reuben wanted a machine that could read a forty-page easement without billing in six-minute increments. Curtis wanted nothing to do with any of it, and said so, and that mattered later.

The rack went together the way everything in the shed went together: Marta on steel and power, Elijah on software, everyone else on opinions. Two scavenged compute cards with a combined forty-eight gigabytes of memory. A salvaged Civic radiator bolted to the shady north wall, two brass bulkheads through the corrugated steel, a marine pump the size of a fist. And on the first cold boot, fans screaming like weather, they loaded the model: a granddaughter of Silvana, open weights, three generations downstream of the thing that had started all of this, small enough now to live on scavenged silicon and capable enough to draft a contract, debug a controller, or walk a stranger through a fuel line at two in the morning. Elijah sat with that for a minute in the dark of the shed. The fire that had burned down his old life, purring in a stove he had built.

![A stack of three scavenged rack-mount servers beside a salvaged car radiator with brass pipe fittings](/book-images/ch11-crucible.png)

*The Crucible. Three filing cabinets and a salvaged radiator.*

For five weeks it was purely good. Reuben fed it easements and it found the clause a lawyer had missed. Priya's intern learned blight triage from it in an afternoon. It never got tired and it never billed and it never, not once, phoned home, because there was no home to phone. Elijah started calling the rack the Crucible, and the name stuck the way names do when a thing has earned one.

The mistake, when it came, was not the machine's.

Elijah wanted his dashboards from town. Uptime, coolant temperature, the channel numbers, all of it on his phone while he sat at the library uploading Denny's videos on borrowed bandwidth. Fifteen minutes of work on a Friday night: a tunnel out, a reverse proxy in front of the co-op's services. While chasing a bug he commented out the authentication line, two slashes, to rule it out as the problem. He meant to put it back. He deployed with the comment marks still in.

What the proxy served, to anyone on earth who looked, was the mesh journal: the plain-text nervous system of nineteen households. Maintenance logs. Meeting minutes. The duty roster. The CSA customer list with addresses. Priya's greenhouse alarms. Marta's physical-therapy schedule, Tuesdays, for the shoulder she never mentioned. Which houses stood empty on which afternoons, computable by anyone who could read a grid log. All of it indexed, unauthenticated, public, for forty-one hours.

It was one of Denny's subscribers who caught it, a network engineer four states away, with a screenshot and one line: "you probably want to lock your journal, brother." Elijah killed the proxy before he finished reading the sentence. Then he pulled the access logs and did the arithmetic he would have paid anything not to do. Three crawlers had been through. You can delete a mistake from your own server. The internet does not run your deletion for you.

He thought about carrying it alone for exactly as long as it took to imagine Marta finding out some other way. Then he rang the dinner bell on a Saturday, which the co-op did not do, and stood in front of everyone it summoned and read them the timestamps.

Marta did not raise her voice, which everyone in the shed understood to be the worst available outcome. "You published which houses stand empty between two and four on a Tuesday," she said. "At the plant we had lockout-tagout. You don't work a press that can take your hand off unless the breaker is locked and your name is on the lock. You put our hands in the press, college."

Curtis said his piece, and for once it had teeth: this is what happens, you brought their machine inside the wire, pull the plug and melt it down. Heads were nodding when Priya, who had been quiet, set down her cup.

"The first family that ever kept fire burned something down," she said. "I promise you they did. A roof, a winter store, somebody's child. And nobody handed the fire back. They built the hearth. Stones in a circle, rules about who tends it, a bucket that never goes empty." She looked at Elijah, and it was not a rescue. "We did not get burned by the model, Curtis. We got burned by a boy who left it lit on the porch rail."

Reuben spent the weekend doing what Reuben does. The customer list crossed county lines; he mapped the exposure, drafted the letter to every family on it, and answered the question nobody had asked out loud: "I can build you an argument that we don't owe anyone notice. I'd rather we not be the people who went looking for that argument."

It was Denny who found the judo in it. "People already know things break," he said. "What they never once get to see is somebody stand up and say so." So they published it, the whole incident, on the channel: what leaked, for how long, who was told, what changed. Elijah read it to the camera himself, because it was his name on the lock. It traveled further than anything they had posted except Denny's first video. Strangers wrote to say it was the first incident report they had ever read that was not written by lawyers. Two of them drove out that summer to help harden the mesh for free.

The checklist became law that Sunday: nothing touches the open internet without a second set of eyes and a signature in the log. Lockout-tagout, ported to packets. And the Crucible came off the wire for good, its model updates arriving by hand after that, hashes checked at the library, the weights carried home on a disk in Elijah's jacket like a transplant organ.

The machine noticed none of it. It went on drafting and debugging and never billing, the pump ticking, the radiator clicking against the north wall while it thought. Fire in its stones. The leak had not taught Elijah machine learning; he had arrived knowing that. It taught him the difference between knowing a system and operating one, and the tuition was forty-one hours of other people's privacy. The checklist was a beginning. It was not the last thing they would have to learn.

---

## The Foundations

## What your court is for

King and Queen of Your Own Robotic Court is a playful title for a serious possibility: useful assistance available to ordinary people. The first assignment is food. After that, other land care, ordinary trash cleanup, shelter, and whatever else we can responsibly make work.

You don't need a humanoid servant that does everything. A planning tool, a suitable farm machine, a kitchen, a distribution service, and people who know their jobs might each do part. Owning every component yourself isn't the point. Being able to receive the useful result is.

## The line cook still eats

Imagine a line cook getting fired on a Tuesday. He's lost his income. He may be angry, frightened, or relieved. In the future I'm arguing for, he can still get adequate food without paying for it. If he can't cook or store it, access has to include a usable meal rather than a box he has no way to turn into dinner.

That's the baseline I want the machines to help make dependable.

“Then nobody will work. Restaurants will all go out of business.”

That doesn't follow from the proposal. People can eat at home and still want a restaurant meal. Taste, convenience, celebration, hospitality, and another person's skill are things people can choose to pay for. Providing a baseline doesn't require forbidding any of them.

It also doesn't mean nothing changes. Workers with dependable food have one less immediate threat hanging over a negotiation. Some jobs may need better pay, hours, or conditions to attract people. Some businesses may change or close. We should take those transitions seriously without making a worker's hunger the device that protects a business model.

The cook can lose his job and still eat. The restaurant can still offer something people want to buy. Hold both thoughts at once.

## Free to the person who needs it

“Who's paying?” is a reasonable question. “Therefore the cook should go hungry” is not its answer.

The equipment, energy, land, people, repairs, and distribution still need provision. The proposal is to cover that provision so receiving adequate food doesn't depend on the recipient having money. The exact arrangement may differ by place. Public services, cooperatives, existing producers, and other organizations have real work to do here. This book doesn't pretend a sentence settles their budgets.

Nor does a cheaper machine automatically make its output accessible. The access arrangement is part of the project. If someone can own all the productive capacity and deny the result to everyone else, we haven't reached the baseline I'm describing.

## More choices, including the choice to work

The WALL-E objection asks whether assistance could leave us dependent, passive, or less skilled. Those are reasonable things to watch. A system might remove useful choices or give people more time and means to exercise them. Observe the difference instead of declaring either outcome inevitable.

People who need substantial assistance aren't morally deficient. The objective is room to live: to learn, move, create, care, work, or rest as circumstances allow. Receiving dinner shouldn't require performing gratitude or proving ambition.

And if an existing crew, a simpler machine, or a better distribution arrangement solves the task better, use it. Robotics is promising because it may expand capacity. It isn't a religious requirement. The food is the point.

## From a request to a checked result

Give a tool a bounded task. A model might help organize an anonymized pickup schedule. A person checks it against the actual vehicles, time, and recipients' needs. The drivers do the trip. Recipients confirm that the food arrived. Those are different contributions; credit them accurately.

An answer that sounds confident hasn't earned permission to operate machinery or decide that food is safe. A sensor reading is not a guess to fill with invented values when the sensor fails. Missing data should stay visibly missing.

The Crucible story shows what happens when useful computing and careless operation share a room. Local means running on nearby equipment. Offline means working without the relevant network connection. An air gap is a deliberate separation, not a synonym for privacy. A machine receiving live network messages is not physically isolated from that network. Updates, transfers, permissions, and maintenance still need care.

Choose computing around the task. You may be able to use an existing phone, computer, or shared service. Don't buy a rack because a book made ownership sound like adulthood. Don't put neighbors' private records into an experiment without their agreement and appropriate handling.

## One useful trial

With a willing food partner, take a non-sensitive planning task that somebody can check before it affects service. Compare the tool-assisted result with the ordinary method. Count correction time as work. Ask whether the result improved anything.

If it helped, document the boundary around that success. If it didn't, stop or change the method. Then follow the work into the next chapter: the person asking for help, the people providing it, and the result at the door.

---

## Precedent P-14: The Quartz Heresy (Switzerland, 1969 to 1983)

Quartz technology and industrial change put Swiss watchmaking under substantial pressure. The Swiss industry was also involved in developing quartz; it was not a single bloc that refused the technology out of purity.

The later Swatch story offers an example of adaptation through products, manufacturing, and restructuring. It should not be made into a claim that only one strategy has ever worked or that success at the industry level erased the losses experienced by workers.

**The mechanism.** An industry can combine technical change, restructuring, and differentiated products. That does not establish one universally successful strategy or erase workers' losses.

**The rule.** Examine specific adaptations and their costs.

**The practice.**

1. Identify the part of a craft people still choose to pay for.
2. Ask which tools support it and which pressures threaten it.
3. Do not infer an individual worker's options from a large firm's resources.

---

