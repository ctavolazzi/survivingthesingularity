"""One-time, baseline-checked editorial transformation. Run from repo root."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[2]
BOOK=ROOT/'src/lib/data/book'
BASE=json.loads((ROOT/'docs/v0.8.0/baseline.json').read_text())
FOUNDATIONS={}
def body(n,text): FOUNDATIONS[n]=text.strip()
body(1,'''## Four questions hiding inside one word

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

The Transformer paper describes an architecture for machine learning. It does not establish a date for AGI. A comparison between biological and artificial systems on a particular learning task does not establish the energy cost of an entire intelligence. A benchmark is evidence about the tested task and conditions; extending it to dependable physical work requires another argument.

This doesn't make the research unimportant. It makes the research usable. A result can be remarkable without proving the largest story somebody tells about it.

My optimism is that useful machine capabilities can keep expanding. My priority is to direct that expansion toward food people can obtain regardless of income. One is an expectation about technology. The other is a choice about what we want it to do.

## The first question to take outside

Ask a grower or food provider which repeated task consumes time without improving the food. Write down their answer before proposing a robot. Ask what would count as a better result and what would make a trial a failure. The answer might concern scheduling, irrigation, lifting, transport, or something you haven't thought of.

That's where the future becomes a piece of work somebody can examine.''')
body(2,'''## Stages are scenarios

The five stages below are a way to examine pressures that might accompany increasingly capable AI. They can overlap, stall, reverse, or fail to occur. Their order is a narrative device, not a discovered law of history.

## Stage 1: The Cash Grab

A useful capability attracts investment and attempts to profit from it. Some firms will sell good tools. Others will sell the appearance of a solution. Some workers will gain useful assistance; others may lose bargaining power or employment. Calling every participant greedy explains less than asking what they get paid to do.

For food, the practical question is specific: does the investment help produce and deliver something people can eat, and do people without money share in the benefit? A profitable machine and a dependable food baseline are different accomplishments.

## Stage 2: The Panic and the Plug

A powerful technology invites disputes over safety, ownership, access, and control. Restrictions can protect people, protect incumbents, do both, or do neither. Evaluate the particular rule and its effects. A critic's concern doesn't become false because a company might profit from it.

Nor does the existence of downloadable software settle the effects of regulation. Hardware, electricity, distribution, and permissions remain physical and institutional facts. We can argue for broad access without claiming that every attempt to restrict a technology must fail.

## Stage 3: Who Gets to Decide?

Someone has to operate the equipment. That doesn't give the operator a mandate to govern everyone who depends on it. An engineer can tell a community what a machine needs; the community still has to decide which needs to prioritize and whose burdens are acceptable.

I want informed experts and the people affected to learn from each other. Evidence can clarify options. It doesn't erase conflicts of interest or decide every value question. If our food program needs public trust, that trust has to survive a difficult question from someone who didn't build the machine.

## Stage 4: Food Without a Job Requirement

This is the hinge of the book. Suppose machines can do more of the necessary work. We could use that capacity to make adequate food available without making employment the admission ticket.

A restaurant could still charge for dinner. A cook could still take pride in a paid profession. A farmer could still sell a harvest. The proposed baseline changes what happens when someone's paycheck disappears. It doesn't require abolishing everything people might choose to buy above that baseline.

A business might have to offer better terms when workers have a stronger alternative to hunger. Prices, staffing, and business models could change. Those effects deserve serious attention, particularly from workers. They are not a logical proof that people must remain hungry to keep restaurants possible.

## Stage 5: Disagreement, Loss, and Adaptation

Someone can welcome food security and oppose a particular deployment. They may be right about a damaged crop, intrusive data collection, a dangerous machine, or a bad contract. Treat those objections as information.

Anger can also come from loss: a skill devalued, a business threatened, a familiar future disappearing. We don't have to endorse harmful conduct to understand the person experiencing it. People aren't sorted into morally fixed generations by the year they were born.

The way through is a proposal concrete enough to criticize. Who gets fed? Who does the remaining work? What happens when the machine fails? Let the answers change the plan.''')
body(3,'''## Beyond human capability

Artificial superintelligence, or ASI, names a possibility: machine capabilities exceeding ours across a very broad range of important tasks. It doesn't specify the system's motives. It doesn't tell us whether it is conscious, what it values, or whether its relationship with people will be cooperative.

That distinction matters because this chapter looks far beyond the food project. The scene is fiction. The stages are speculation. Neither is evidence that a safe outcome has already been secured.

## Stage 6: The Possible Exodus

An advanced system might help humans expand into space. It might operate equipment beyond Earth. Whether it would independently choose to leave, and whether that would make people safer, depends on assumptions about its goals and constraints that this book cannot establish.

A rocket photograph demonstrates a rocket. It doesn't demonstrate an autonomous civilization preparing to depart.

I favor mutually assured survival as an organizing goal. I want cooperation to become more useful than domination. That conviction is worth making explicit because it gives us something to work toward. It would be irresponsible to recast it as a theorem that greater intelligence must share my values.

Capability and care are separate questions. The work of making powerful systems accountable continues even if we believe a cooperative outcome is possible.

## Stage 7: Biology and the Longer Life

Better tools could help people investigate disease, design treatments, or assist with daily living. Those are different tasks with different standards of evidence. A household assistant helping someone prepare a meal has not thereby become a doctor. A model that explains a paper has not demonstrated a treatment.

The prospect of profound biological change belongs in this larger horizon. It doesn't belong in a promise that buying enough computer memory will make a machine fit to diagnose your family. Clinical claims require clinical evidence and appropriate institutions.

There will also be choices about how much change people want. Someone who declines an intervention is not automatically frightened or backward. A future worth pursuing has room for informed consent, including the answer no.

## The work that doesn't wait

None of these possibilities is a prerequisite for food access. We can study a narrow agricultural task without settling the future of consciousness. We can improve an existing service without knowing whether a machine will ever leave Earth.

Keep the horizon wide enough for imagination and the next task narrow enough to inspect. If the larger forecast turns out to be wrong, the person who received a useful meal still received it.''')
body(4,'''## Permission to imagine

A book about a technological singularity should have room for the strange possibilities. It should also tell you when it leaves observation behind. This chapter is that room. What follows is speculative philosophy, not a sequence of engineering commitments.

## Stage 8: Intelligence at a Larger Scale

Universal superintelligence is a name for an imagined expansion of capability beyond our present scale. The word *universal* doesn't demonstrate unlimited knowledge. More computation still raises questions about energy, matter, communication, error, and time.

It's possible to imagine systems operating across a solar system or beyond. It isn't possible to infer from a useful language model that this expansion must occur, that it will be beneficial, or that the resources required will be freely available. Those are additional claims.

The imaginative exercise can still be useful. It asks what we would value if many present constraints changed. Would we want only more output? Or more lives with room for curiosity, affection, art, rest, and adventure? A future with extraordinary machines and frightened hungry people would be an extraordinary failure of priorities.

## Stage 9: The Edge of the Map

Simulation arguments ask whether observers like us could inhabit an artificial world. Their conclusions depend on assumptions about possible civilizations, simulations, and observers. They aren't measurements showing that our world is simulated. Building a convincing virtual environment would not, on its own, establish that someone built ours.

Similarly, invoking a multiverse doesn't establish a place where a machine could obtain more resources. An unknown possibility is not an available engineering solution.

These ideas can change the questions we ask about meaning. They cannot supply the missing evidence for a agricultural claim or a date on a calendar. When the argument returns to food, leave the cosmic assumptions here.

## A useful return to Earth

Elijah's willingness to discover that his picture is incomplete is the important move in the scene. Keep that willingness when an idea feels inspiring, too. Certainty can be comforting in either direction: everything will be saved, or everything will be ruined. Neither comfort does the work.

You don't need an answer about the ultimate nature of the universe to care whether your neighbor can eat. That question is already close enough to touch.''')
body(5,'''## A machine still needs a world

A machine can perform work without a person doing every motion. It doesn't perform that work without inputs. A food service needs a food source, suitable equipment, water and energy where the task requires them, maintenance, and people or systems to handle the parts that aren't automated.

That is why thermodynamics belongs in this book. Energy accounting checks a claim against the physical world. It doesn't decide what a person deserves or tell a community how to distribute its food.

The first law concerns conservation of energy. The second constrains the conversion of energy into useful work. Neither supplies a moral ranking of people by output. Calling someone a meat engine may make a comparison vivid; it mustn't make their worth depend on how cheaply they compete with a motor.

## Keep the ledgers separate

Suppose a shared garden has solar generation, a water pump, and a harvest. Record electricity in kilowatt-hours, water in liters, edible harvest in appropriate mass units, labor in hours, and expenditure in money. Don't add them into one impressive-looking surplus number.

Food mass is not a complete nutritional account. A surplus of one vegetable is not a year's diet. Electricity available at noon is not automatically electricity available during a cloudy week. Installed capacity is not delivered service.

A useful calculation says what it includes and what it leaves out. If you want to compare a manual process with a machine, include setup, supervision, failed runs, repairs, and the inputs each option actually consumes. Otherwise you may merely move the work off the page.

## Free to eat, with the costs visible

When I say food should be free at the point of access, I don't mean that metal, land, labor, or energy stops costing anything. I mean the person who needs to eat shouldn't have to produce a payment before receiving adequate food.

We already know how to distinguish the recipient from the payer. A proposed service can have an operating budget while charging its recipients nothing. The unresolved work is making that provision dependable, fair, and sufficient. Automation could change the cost of some tasks. It doesn't choose who pays or who gets served.

This distinction strengthens the promise. If a project cannot explain how next month's maintenance is covered, it should not advertise permanent access. Find the gap while there is time to arrange support.

## This week's energy question

Choose one task with the people who already do it. Ask which resource actually limits it. An irrigation controller won't fix a missing water supply. A more efficient motor won't fix a distribution route that never reaches the recipient.

Write a short inventory: the task, required inputs, person responsible, remaining outside dependencies, and what happens during an interruption. Start with an existing tool or service where possible. You don't need a private microgrid to take part in a food project.

The goal is a useful increment of capacity. Independence from every distant supplier is a much larger claim, and it isn't an entry requirement.''')
body(6,'''## Possibility is enough to start

The scene shows Elijah entering a community that already knows things he doesn't. That is a better beginning than announcing that the future is settled. A useful capability can be real while its economic and political consequences remain undecided.

The title of this chapter is a question now. What would have to be a done deal? Reliable broad intelligence? Cheap physical equipment? A way for people without income to receive its output? Those thresholds aren't interchangeable, and no demonstration settles all three.

I expect powerful changes. I don't need to promise their exact sequence to argue that we should prepare useful alternatives to hunger.

## More than a change of attitude

Fear, pride, and habit can make learning harder. So can a broken pump, unaffordable equipment, a lack of time, an inaccessible site, or a project whose organizer won't listen. A willing person can encounter a real material limit.

If the only explanation for failure is that the participants weren't ready, the plan has made itself immune to evidence. That's no way to build anything people can depend on.

Instead, ask which part is missing. Capability can improve without deployment keeping up. Lower operating costs can coexist with high prices. A donated machine can become useless when a replacement part arrives six months late.

Those details don't cancel the possibility. They tell us what work stands between a possibility and a service.

## The baseline changes the stakes

The promise I care about is that a person can lose a job without losing the ability to eat. That would not settle rent, healthcare, debt, or every consequence of unemployment. It would remove one immediate threat from a difficult day.

A worker with dependable food access could have more room to refuse bad terms, retrain, care for someone, or look for a better fit. How much room depends on the rest of their life. Don't turn one improvement into a claim that every other constraint has disappeared.

Likewise, a free meal is not an argument that all labor must end. Producing food is useful work. Repairing equipment is useful work. Caring for someone is useful work. The question is how much necessary toil machines can take on, and how the benefits reach people rather than becoming another fee they cannot pay.

## Start where help already exists

Find an existing garden, grower, kitchen, pantry, or mutual-aid group willing to discuss its work. Ask what it needs, what it already does well, and what an outsider is likely to misunderstand. Offer one contribution small enough that a failed experiment won't interrupt anyone's food.

Build from what people know. The future doesn't need you to arrive pretending the room was empty.''')
body(7,'''## People have reasons

Denny's loss is real before it becomes a lesson. A job can carry income, friendships, competence, routine, and a sense of being needed. Telling someone that the machine is efficient doesn't replace those things.

A food baseline addresses part of that loss. It means a worker's access to adequate food need not vanish with their employment. It doesn't entitle us to tell them that everything else will work out automatically.

## Replace the battle lines

A generation isn't a personality type. An occupation isn't a measure of empathy. People can want useful machines and dislike the terms on which they arrive. They can be excited one day and frightened the next. They can be right about a failure even if they are wrong about the long-term trend.

Judge conduct and claims. If someone sabotages a project, describe the sabotage. If someone points out that the promised delivery didn't happen, investigate the missed delivery. Don't use the same label for both.

The food-first argument ought to make disagreement easier to locate. We might share the goal that nobody goes hungry and disagree about ownership, funding, deployment, or evidence. Naming the disagreement is more useful than announcing that one side is ready for the future and the other isn't.

## Work, bargaining, and the meal

Imagine a line cook whose shift is cut. In the future I'm arguing for, he can still eat without paying. He might want another restaurant job. He might want to learn something else. He might need time to care for a parent. The meal doesn't make those decisions for him.

An employer might have to improve pay or conditions when hunger is a weaker bargaining weapon. Some firms might reorganize or fail. It would be false to guarantee that every restaurant's costs and margins remain unchanged. It would also be false to infer that feeding people requires banning restaurants.

A meal sold for pleasure, convenience, craft, or company can coexist with an adequate baseline. Whether a particular business succeeds remains a business question. Whether a fired worker deserves to eat shouldn't depend on the answer.

## The people doing the transition

Ask workers what a proposed automation changes in their day. Include maintenance, training, pace, discretion, injury exposure, and pay. Ask who receives the time saved. A demonstration can look impressive while making the remaining work worse.

Institutions and communities have to deal with those effects. This book proposes a priority for that work, not a complete labor policy. My priority is to make basic food dependable while the rest of the transition is argued over and built.

For one conversation this week, explain the proposal without assigning your listener a motive. Ask for the strongest objection. Repeat it back until they recognize it. Then ask what evidence would help both of you evaluate it. Leave room for an answer that changes your plan.''')
body(8,'''## Attention you can use

Elijah's experience with the co-op isn't proof that every screen is an enemy or every quiet hour a cure. Attention is a limited resource in a life that also contains jobs, children, care obligations, emergencies, and useful digital work.

Try a small change you can undo. Silence one distracting category of notification during a task, while preserving the contacts and alarms you need. Compare the result with an ordinary day. If grayscale makes your phone harder to use, don't treat enduring it as evidence of discipline. If a notebook helps, use it. If accessibility software helps more, use that.

This is a practical experiment, not a dopamine treatment. The book makes no promise that a fixed number of hours resets receptors or repairs a brain. A diagram about distraction can illustrate a habit without pretending to measure a universal neurological mechanism.

## Cooperation without the threat of hunger

The point of pooling resources is to make lives less precarious. It contradicts that purpose to recommend starvation, social death, or the removal of essentials as the tool that makes people cooperate.

Our food baseline has to include someone who isn't productive today, someone who can't contribute physically, and someone who disagrees with an organizer. Otherwise employment has merely been replaced with a different loyalty test at the kitchen door.

A group can still address harmful conduct. It can limit someone's access to dangerous equipment, investigate misuse, or change responsibilities. Those decisions should not be casually turned into a justification for making the person hungry. Actual procedures and protections require collective work with the people affected.

## What a model can tell you

Sharing an expense among more people can reduce each person's share under stated assumptions. Coordination and maintenance can add costs. A simple reciprocal relationship is not an exponential reduction, and neither calculation proves that a community is fair.

Game-theory examples are useful when their assumptions are visible. A strategy that performs well in one modeled setting isn't a universal rule for human relationships. Trust, repeated interaction, mistakes, unequal power, and opportunities for repair change the situation.

Small groups can know each other well. They can also exclude, intimidate, or protect their most influential members. No magic group size makes those problems disappear. Communication topology and legitimate authority are different subjects.

## A meeting with an actual result

Choose one food-related task and invite the people who will do it and receive its output. Record the task, available resources, missing resources, and the next review date. Give someone responsibility for asking whether the intended recipient actually benefited.

Keep private details private. A shared food directory doesn't need to become a public map of who is vulnerable or when their house is empty.

After the first attempt, ask three questions: what helped, what burden did we overlook, and what will we change? Someone who names a flaw is helping maintain the project. The group should be capable of hearing that before it needs a crisis to force the conversation.''')
body(9,'''## Food first means following the food

If machines are going to take more jobs, put them to work on the thing a lost job threatens first: the ability to eat. That's the priority. A factory that makes a better controller can contribute to it, but the controller isn't dinner.

The chain continues through growing, harvesting, handling, storage, preparation where needed, and distribution. Someone has to receive food they can actually use. A person without a kitchen needs a different service from a household that can cook. A crop that never leaves the plot hasn't solved access.

This is a task for cooperation between farms, towns, kitchens, transport providers, and the people eating. A dense city doesn't have to grow its entire diet inside its boundary. Local capacity can complement regional supply instead of pretending the rest of the world has disappeared.

## What a garden robot demonstrates

FarmBot's manufacturer documentation describes tools for seeding, watering, and weeding. That is a concrete set of tasks worth examining. It is not evidence of a machine harvesting every crop, preparing a balanced diet, and delivering it to everybody for free. Keep the capability claim at the scale of the documented work. [FarmBot tool documentation](https://farm.bot/pages/tools)

The FAO's 2022 report on agricultural automation examines opportunities alongside barriers to adoption, particularly for smaller producers. That supports investigating useful automation and who can obtain it. It does not establish that a particular installation provides universal food access. [FAO, The State of Food and Agriculture 2022](https://www.fao.org/agrifood-economics/publications/detail/en/c/1613500/)

We can take both points seriously and still be ambitious. The question is which piece of the food chain a tool improves, at what total cost, and for whose benefit.

## A worked example: one delivery, all the way through

Here's an illustrative project, not a reported trial. An established garden has permission to grow food on a suitable site. A local food group already has handling and distribution arrangements. They agree to try a small additional weekly delivery to five households that want it. Nobody has to own a robot or pay for the produce to receive a share.

The garden tests whether an existing irrigation controller can reduce routine checking without compromising the crop. A grower selects the task and settings. A volunteer records time spent, water used where measured, failures, and manual interventions. The controller opens a valve; it doesn't decide that a plant is safe to eat.

At harvest, people pick, sort, and weigh what is usable. The food group handles packing and distribution through its established process. Recipients confirm whether the food arrived and was useful to them. The record distinguishes food grown, food usable, food delivered, and food people could actually eat.

Suppose, for the arithmetic only, there are 10 kilograms of usable vegetables and the agreed division is two kilograms per household. Five deliveries fit that harvest. If two kilograms become unusable before distribution, the same promise no longer fits. Record the shortfall and arrange a replacement through the partner before calling the week a success. Don't silently make the boxes lighter and leave the dashboard green.

Those vegetables supplement meals. They do not establish five complete diets. A dependable baseline would also need enough suitable food across seasons, access for different dietary needs, and provision for interruptions. The small trial tests one contribution to that larger goal.

The example's funding assumption is equally explicit: a partner budget covers the trial's supplies and transport; the equipment already exists; some labor is volunteered. Record the donated time and equipment instead of calling them costless. A permanent service needs dependable provision beyond a lucky month of volunteer availability.

## Compare before expanding

Run the comparison against the garden's ordinary method. Include maintenance, supervision, training, travel, and failed attempts. Keep the existing food service operating during the trial. If a simple timer or an extra paid shift performs better, use it. The recipient needs food, not a demonstration of our loyalty to robotics.

A first result might justify a larger trial. It cannot justify declaring hunger solved. Keep growing the claim only as far as the evidence grows with it.''')
body(10,'''## Your life is not a productivity ratio

Denny found a way to make something that mattered to him. The lesson is an invitation, not a condition attached to his right to eat. A person who is exhausted, disabled, caring for somebody, or simply between projects is still a person who needs food.

I want tools to leave more room for work people choose, and for the parts of life that aren't work. A song, a repaired gate, a quiet afternoon, a child's company, a meal shared without checking the bank balance: output doesn't exhaust the reasons to be alive.

## Choose one contribution

Start with a food need you can understand. You might help an existing group organize a pickup schedule, compare its request list with confirmed supplies, or document a repair someone else knows how to do. You might be the person receiving help and explaining why the proposed arrangement doesn't work for you. That information is a contribution too.

Use equipment you already have or can appropriately share. A solar panel, a private server, and a piece of land are not admission requirements.

For this week, give the task a beginning and an end. For example: ask a food group whether it wants help correcting its public pickup information, confirm the details with its organizer, publish the approved correction, and check whether someone could use it. Don't create a project on their behalf that they now have to maintain.

## Share a result people can judge

Documentation can help another group avoid your mistake. Say what you tried, what it cost, what happened, and what you still don't know. Obtain consent before making someone's hardship part of your story. They don't owe the internet their most difficult day in exchange for assistance.

Attention is not the same thing as usefulness. A dramatic video can travel while conveying a false lesson. A plain repair note can help three people and never go viral. Neither an algorithm nor a sincere voice guarantees income.

Research on model collapse concerns particular training conditions. It doesn't prove that all synthetic data inevitably destroys a model, and it doesn't guarantee a market for whatever a human creates. Keep the value of human testimony on its own footing: you were there, you can explain what you observed, and another person can question you about it.

## Make the handoff small

If the experiment helps, leave behind something another person can actually use: a corrected schedule, a short guide, a labeled record, a contact who agreed to be contacted. If it fails, leave a useful explanation and stop spending resources on it until there is a reason to try again.

The next chapter introduces your robotic court. Its purpose is assistance with a need, including food. You don't have to become a hardware business or a content business to deserve that assistance.''')
body(11,'''## What your court is for

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

If it helped, document the boundary around that success. If it didn't, stop or change the method. Then follow the work into the next chapter: the person asking for help, the people providing it, and the result at the door.''')
body(12,'''## Access before ownership

Land matters to food production. It doesn't follow that every hungry person should buy it, or that a speculative purchase is the first step toward security. A garden you can use, a grower you can partner with, or an existing food service may be more useful than a parcel you cannot afford to maintain.

The trust in the scene is a fictional arrangement between particular people. Its success isn't a promise that a template can make property immune to every future dispute, tax, or claim. Real arrangements need people with relevant expertise and the participation of those affected.

For the food-first program, begin with access to a suitable place and a workable relationship. Ownership is one possible route. It isn't a test of commitment.

## Grandma's request

Imagine an eighty-two-year-old neighbor on a fixed income. Arthritis makes yard work difficult. The yard is overgrown, a landscaping quote is beyond her budget, and a code-enforcement notice adds pressure she doesn't need. Those are the stakes. We don't need to invent a second grandmother to make them legible.

In this illustrative service arrangement, a local group already has a small funded help program and agreements with qualified operators. She can request help by phone, through a neighbor, or using a simple device if she prefers. She doesn't need to learn our favorite interface before somebody listens.

A coordinator confirms what she wants and what the group can offer. The request is for ordinary yard work assessed by an appropriate operator, plus a food delivery she has asked for. It is not an invitation for volunteers to improvise hazardous tree work or operate unfamiliar machinery.

The coordinator checks available people and tools, agrees a time, and records who is responsible. A schedule helps them keep the promise. It doesn't decide what she deserves.

On Saturday, the crew does the agreed yard work. A person checks the result with her. Separately, a food partner supplies a confirmed share, and a driver delivers it. If the share contains five kilograms of vegetables, that is what the record says. It doesn't silently become fifteen thousand calories or a complete pantry.

The group charges her nothing. Its budget, equipment, and donated time still exist. Free to grandma means somebody arranged provision; it doesn't mean the costs vanished.

## What the machines did

In that version, software assisted coordination and garden equipment may have helped tend the crop. People assessed the yard, operated the tools, harvested or obtained the food, and delivered it. Calling the whole sequence autonomous would give machines credit for work people performed.

A future robot service might do more of the physical work. That's a forecast to test against actual tasks, conditions, reliability, and availability. My personal 2027 AGI expectation is not evidence that such a service will be available to her that year.

The current example still matters. It shows where labor is needed and where a useful machine could reduce it. It also shows that we can help before the future version arrives.

## Count the result at the door

Keep separate records for food, equipment time, travel, money, and remaining labor. Ask whether the recipient got what was agreed, whether it met their needs, and whether the group can repeat the service. A machine's activity log alone can't answer those questions.

The larger goal is universal food access. A small cooperative isn't humanity, and a good Saturday isn't a permanent guarantee. Expansion needs reliable partners, provision for shortages, and ways to serve people outside the founders' circle. Keep those gaps visible without demanding that one neighbor solve all of them before helping another.

This week, ask one existing local organization how someone requests food or practical help. Check whether that route is usable without a smartphone, transport, or spare money. With the organization's agreement, help close one barrier. The first useful infrastructure might be an accurate phone number and somebody who answers it.''')
body(13,'''## Shelter belongs in the wider horizon

A home with room to repair things and share tools is an appealing possibility. Marta's shop makes the appeal physical. The failed weld also makes the limit physical: a convincing explanation and an attractive drawing don't establish that a structure will hold.

The shouse is an optional design idea in this book. You don't need to buy land, cut a container, or build a dwelling before participating in food work. Shelter comes later in the program's application order. That is not a rule asking someone without housing to postpone an urgent need.

## What the sketch leaves out

A structural calculation can answer one bounded question under stated assumptions. It cannot, by itself, establish foundation suitability, connections, stability, weather resistance, fire performance, ventilation, or a habitable building. A materials subtotal doesn't include every cost of making a legal, usable home.

This edition therefore offers no container-cutting dimensions, footing recipe, combustion-heating shortcut, or universal water-reuse arrangement. Those were larger promises than the examples could support. A real project needs appropriate design for its site and intended use, with the people responsible for the relevant work.

The useful principle survives: choose space and equipment around the work you need to do. A shared workshop might be valuable. So might an existing garage, a rented bench, or a partnership with someone who already has a suitable facility. Compare them before treating a new building as the only route.

## Respect the skill

Marta doesn't become less important because a machine can help draw a design. Someone still has to know what an acceptable joint looks like, when conditions invalidate the plan, and when to stop. Her teaching takes time. That time belongs in the budget.

Likewise, reducing the number of motions a person performs is not the same as eliminating their responsibility. If a tool accelerates fabrication but increases inspection or setup, count that work. If it changes the hazards, evaluate the new arrangement rather than assuming automation has removed them.

## A useful assignment before a purchase

Write the three jobs you actually need space for. Identify an existing place where each can be done, who can authorize its use, and what it would cost in time and money. Ask a person already doing the work what your list misses.

That exercise may lead to a building project. It may lead to a shared bench and no construction at all. Either is a useful answer if it lets people do the work well.

For now, keep the first food project small enough that it doesn't wait for a house to be finished. You can admire the larger possibility while getting dinner to somebody today.''')
body(14,'''## Shorter loops, visible dependencies

A local supplier can make a repair easier. A regional grower can make a food partnership more direct. Neither relationship makes the community independent of everything outside it. Replacement parts, seed, transport, fuel, expertise, and finance may still come from elsewhere.

Resilience means identifying what continues to work during a particular disruption, for how long, and with what support. It doesn't mean declaring every outside connection a weakness. Several different connections can be exactly what prevents one failure from becoming a crisis.

## Follow the missing meal

A retailer's stock turnover is not a countdown to a person's starvation. Household supplies, deliveries, access, nutrition, and the duration of an interruption are different measures. A useful plan asks what food people can actually obtain and which links are vulnerable.

Choose a real dependency with the people who operate the service. What happens if a vehicle is unavailable, a grower loses a crop, or a collection site closes? Name an alternative and confirm that it can help. Writing a second provider's name in a spreadsheet doesn't reserve its capacity.

A food baseline needs this kind of continuity. If the machine is down on Tuesday, the person still needs Tuesday's dinner. Maintain a way to provide it while repairs happen, and be honest about the coverage you have actually arranged.

## Tools for coordination

Use communication suited to the message. A compact request or status update is a different requirement from a video, a reference library, or ordinary voice service. Don't make one low-bandwidth link carry all of them in the story merely because a single diagram looks cleaner.

Existing phones, printed lists, and face-to-face arrangements can be part of the system. People outside a custom network still count. If joining the food service requires buying a radio, the access design needs another look.

The same discipline applies to logistics software. A route that is short on a map may not work for a driver or a recipient. Verify constraints with the people involved. Let the computer suggest; let reality correct.

## Adaptation without a victory myth

A company can adopt new technology and still fail financially. It can enter bankruptcy and continue operating. A worker doesn't have the same reserves or options as a diversified corporation. The historical examples at the end of this chapter are useful when those distinctions remain visible.

The immediate practice is smaller than reinventing your life. Map one existing food route from supplier to recipient. Find the point where an interruption would leave someone without a usable alternative. Ask the partners what a realistic backup would require, and record what remains unresolved.''')
body(15,'''## The sensor lesson is not a food-safety certificate

Priya's scene is about asking whether an instrument observes the thing you think it observes. A surface reading cannot stand in for the whole root zone. A healthy-looking plant cannot establish that an unknown site is suitable for producing food.

Those are separate questions. The story's measurements are fictional, and its revised trial doesn't establish a universal treatment effect. Real soil decisions need evidence appropriate to the site, crop, and intended use. The EPA's urban-agriculture guidance discusses potentially contaminated sites; it doesn't certify the fictional plot in this book. [EPA, Urban Agriculture](https://www.epa.gov/brownfields/urban-agriculture)

## Biology without a miracle recipe

Soil contains organisms with different roles. Rhizobial nitrogen fixation and mycorrhizal relationships are not interchangeable names for a single process. Nutrient cycling also doesn't make harvested nutrients cease to leave a site. A food system needs to account for what is removed and how it is replaced. [University of Minnesota Extension, Soil Biology](https://extension.umn.edu/natural-resources/conservation/agricultural-soil-and-water/soil-biology)

This edition does not prescribe an aerated compost-tea recipe or offer aeration as a pathogen guarantee. It also doesn't infer that every synthetic input destroys soil or every genetically engineered crop is sterile. Choose a claim narrow enough that relevant evidence can answer it.

A grower may have good reasons for a method. Ask what those reasons are and what would change the choice. Neither the word natural nor the presence of a sensor settles performance or safety.

## From a growing plot to useful food

Return to the Chapter 9 trial. The garden records the crop and usable harvest. A food partner handles the next steps. The record includes what was lost, what reached people, and what remained necessary from other sources.

The automation question belongs inside that record. Did the equipment reduce repetitive work? Did it need more intervention than expected? Did the time saved become something people actually valued? A graph of valve activations can't answer those questions by itself.

A complete food baseline is larger than a vegetable plot. It has to meet people's actual dietary needs and keep working across seasons and interruptions. A useful garden can contribute without being described as total self-sufficiency.

## Learn with someone who knows the ground

This week's task is to visit or speak with an established growing project, with permission. Ask which observation changed its operator's mind recently. What did they think was happening? What did they check? What did they change?

If they welcome assistance, help record that lesson accurately. Don't arrive with a recipe and assume the local experience is merely waiting for your instructions. A tool can extend someone's ability to observe; listening is how you discover where that extension would help.''')
body(16,'''## Documentation that gives something back

Denny's channel is a fictional success, not an income forecast for every reader. Useful work can fail to find an audience. Popular work can be misleading. A person doesn't owe the platform a business just because they have something to share.

For the food-first project, publish something another person can evaluate: the task, the conditions, the result, the cost you counted, and the limitation you found. If you didn't measure a result, say so. A photograph of plants is not a yield trial.

## People before the story

Ask permission before publishing someone's image, circumstances, address, or request for help. Consent to receive food isn't consent to become content. Give people a route to participate without appearing in the documentation.

Removing file metadata can reduce one kind of exposure. It doesn't remove a street sign in the photograph or stop a caption from identifying someone. Review the actual exported material, including what is visible and what your words reveal.

A local copy, a content address, and encryption do different jobs. Availability depends on someone keeping and serving the data. A content identifier doesn't promise perpetual hosting. Physical transfer avoids some network exposure but doesn't make a file immune to loss, damage, or unauthorized copying.

## Share the useful part

Make one short record with an existing partner. Keep private operational information separate from the public account. Let the partner check that you represented the result fairly before sharing it.

For permissions, choose terms that match the actual material and the rights you hold. Don't invent a dramatic license name and assume it has settled what others may do. Software, photographs, designs, and prose can have different needs.

The most useful sentence in a project report may be the one saying why you stopped. A failed attempt with clear conditions can save someone else time and money. You don't need to disguise it as a victory for the record to travel.

## This week's handoff

Offer a food group a simple choice: would a corrected public schedule, a translation checked by a competent speaker, a clear explanation of how to request help, or a short account of one repair be useful? Let them choose, including the answer none of those.

Finish the chosen item and confirm who will keep it current. A page nobody maintains becomes another obstacle. The point is to leave the next person with less confusion than you found.''')
body(17,'''## Choose the tool after the task

The mission order is food, other land management, trash cleanup, shelter, and further applications. The order is about emphasis. It isn't a demand that an urgent need wait its turn behind a global program.

For each task, compare the tools people can actually obtain and support. A machine that is impressive in a video may be hard to repair locally. A familiar tool may do the job well. Shared access can matter more than ownership.

## Food: count the whole job

Begin with the chain in Chapter 9. Identify the repetitive task, the present method, and the result at the recipient's end. Include setup, supervision, maintenance, transport, and the work still performed by people. Don't turn a reduction in one motion into a claim that a whole occupation has disappeared.

Power equipment needs a suitable, documented supply. This book no longer gives an undefined salvaged-cell battery assembly or describes a DC system as lossless. A custom power system is its own engineering project. It isn't a prerequisite to help with food.

Likewise, network equipment is optional infrastructure. A message service doesn't have to carry a video library. Range and reliability belong to the conditions of an actual deployment, not a promise about a whole valley.

## Cleanup: from litter to its destination

Consider a small ordinary-litter project, undertaken with permission at a suitable site. Locate the litter, collect what the established service can accept, transfer it into that service's disposal stream, and check the place afterward. If the material is unknown or hazardous, the task belongs with an appropriate specialist service rather than an improvised robot trial.

A future cleanup robot could perform part of that chain. To test whether it helps, compare the whole arrangement with an existing crew, better bins, or a simpler capture method. Count maintenance and recovery of the machine. Check whether less waste remains overall, not only how much the device reports picking up.

“Won't people just litter more?” They might change their behavior. They might also take better care of a cleaner place. Neither possibility is a measured result. Include prevention, accessible disposal, and repeat observation in the arrangement rather than treating abandoned trash as a lesson people need to endure.

EPA describes intentional and unintentional pathways by which trash reaches water. Wind, runoff, and losses during handling mean that a piece of litter alone doesn't identify a deliberate offender. Accountability should concern what actually happened. [EPA, Learn About Aquatic Trash](https://www.epa.gov/trash-free-waters/learn-about-aquatic-trash)

The dependency and jobs questions are addressed in Chapter 11. They belong in evaluation here too, without turning each cleanup into a referendum on every possible future.

## Recovery is a different task

Collecting a bottle is not the same as converting its material into a dependable replacement part. Recycling and waste-to-resource experiments have their own inputs, losses, and limits. An attractive loop drawn on a page doesn't establish a closed material balance.

Keep ordinary cleanup useful on its own. The place can be cleaner even if you haven't built a recycling plant. A repair shop can help people even if it still orders parts from distant manufacturers.

This week, inventory tools with the people doing one existing food or cleanup task. Record what is available, who can use it, what requires training, and who maintains it. The tool library starts with accurate information, not a shopping spree.''')
body(18,'''## Let the room improve the plan

The meeting worked because people supplied things Elijah's model missed. Preserve that quality in the practical version. A plan is more useful when someone can name a flaw without becoming its enemy.

The goal is dependable food access, not a certificate proving that nineteen households can replace every institution. A small project can do something valuable and still need regional suppliers, public services, technical specialists, and neighbors outside its membership.

## A premortem for one food service

Imagine the next promised delivery has failed. Work backward. Perhaps the crop was unavailable, transport broke down, the recipient couldn't use the food, the organizer was ill, or the operating money ran out. These are selected possibilities, not an exhaustive list of risks.

Use a short record:

| Question | What to record |
| --- | --- |
| Who is affected? | The people whose food or work would be disrupted. |
| What would we notice? | An observable warning, including a missing confirmation. |
| Who responds? | A named role and a backup who has agreed to help. |
| What happens to the meal? | A confirmed alternative, or an explicitly unresolved gap. |
| When do we check again? | A date and the evidence needed for the next decision. |

Don't circulate sensitive personal details just to make the table feel complete. The people receiving help should be able to correct the assumptions about them.

## The gap between a pilot and a baseline

A pilot can depend on a grant or a few volunteers for a defined period. A baseline people organize their lives around needs continuing provision. That difference belongs in the promise from the beginning.

Ask what happens when the machine is unavailable or the founder leaves. Ask how people outside the initial circle get access. Ask whether the service works for someone with no kitchen, limited mobility, or a dietary requirement. Ask which commitments are funded and which are hopes.

The answer may be that the project isn't ready to expand. That is useful information. It is not a verdict that the participants have failed at being human.

## Learn, revise, repeat

Hold a review after the first bounded trial. Compare the result with the ordinary method and the intended benefit. Include the people who did the extra work and the people who received the food. Keep a record of what will change and who has agreed to do it.

If the machine makes the task worse, change the machine or stop using it for that task. If the access arrangement excludes the people it was meant to help, change the arrangement. Neither decision requires abandoning the goal.

Wide lens, narrow focus. The lens holds the possibility of enough food for everyone. The focus holds the next useful thing that can be checked.''')
INTRO='''It's time to ask a better question about the robots.

If these things are going to take all our jobs, why not make them grow our fucking food first?

That's where I want to start. With food. Enough of it, suitable for the person who needs it, available whether that person has a paycheck or not. Then we can go from there.

“Nobody wants to work anymore,” as the saying goes. People do want to make things, solve problems, care for each other, run kitchens, grow plants, and become good at difficult work. What I object to is spending forty years renting the opportunity to survive, with the next meal caught up in the fear of getting fired. If a machine can take on necessary labor, I want its useful output to help loosen that grip.

The prospect of less compulsory toil ought to contain some good news.

## The cook and the meal

Imagine a line cook gets fired. In the future I want us to build, he still eats. He can obtain adequate food without having to find money first. Losing his job can still hurt. It can still leave rent due, plans broken, and a difficult conversation waiting at home. But dinner doesn't have to become another emergency.

That's the proposal.

It doesn't require restaurants to disappear. People can still sell a meal worth buying: for its taste, its convenience, the skill that went into it, or the pleasure of sitting across a table from somebody they love. A baseline of adequate food and a market for restaurant meals can exist together.

Would the economics change if a worker could say no without immediately risking hunger? They could. Would every business be guaranteed the same margins, wages, and staffing? No. That's a real discussion about the terms of work. It isn't a logical argument that people must remain afraid of starving so someone else can continue selling dinner.

I want the cook to have a choice worth the name.

> **Losing your job should not mean losing your food.**

## A commitment and a prediction

My commitment is that everyone should have enough to eat. My prediction is that AI and robotics can help us build the capacity to make that dependable. The commitment doesn't need a laboratory result. The prediction does need evidence, task by task, and it needs arrangements that let people receive the benefit.

A robot that can water a bed hasn't thereby harvested a crop. A harvest isn't automatically a balanced diet. Cheap production isn't automatically free access. Somebody has to connect the work to the person who needs the food, including when something breaks.

I don't say that to make the ambition smaller. I say it because I want the promise to reach the dinner table. Every missing step is work we can name, investigate, and organize around. Hiding it under the word abundance would leave it missing.

When I say free food, I mean free to the person receiving the baseline. The equipment and operating costs still exist. The people doing remaining work still matter. The question is how we provision that work so an empty wallet doesn't close the kitchen door.

This book argues for that priority. It doesn't pretend one author can settle every institution, budget, safety protocol, or public decision involved. Those are shared tasks for people with relevant expertise and the people whose lives the choices affect. The book does owe you clear claims, visible assumptions, and something specific enough to question.

## Begin with useful work

My application order is food, other land management, ordinary trash cleanup, shelter, and further possibilities. It's a way to focus the program, not a rule telling someone in urgent need of shelter or care to wait.

We can begin inside existing food systems. Talk to a grower, kitchen, pantry, or mutual-aid group. Find a task that is hard to provide reliably. Ask whether a tool could help and what a fair comparison would look like. Keep the existing service running while you learn.

Sometimes the best answer will be a robot. Sometimes it will be a timer, a staffed delivery route, or a clearer way to request help. The goal isn't a world forced to use my favorite machines. It's a world where people can eat. Use the method that helps.

A useful result can be modest without making the larger goal modest. One garden trial is not universal food access. It can tell us something about how to build capacity, what it costs, and where the next obstacle lies. The questions of scale, continuity, and access remain part of the work.

## How to read this book

Elijah Madrone and the co-op are fiction. Their scenes explore consequences, mistakes, relationships, and possibilities. The people and outcomes in those scenes are not field-trial evidence. The explanatory sections following them make the argument; where an example is invented to show the mechanics, it is identified as illustrative.

Part I explores what increasingly capable machines might mean. The nine stages are scenarios, with the later cosmic stages increasingly speculative. They aren't a timetable that history has agreed to follow. My personal AGI forecast remains Thanksgiving 2027, November 25. Why that day? Because. It is my expectation, not a guarantee of recursive improvement or a robot service at your door.

Part II asks how people cooperate through change without treating disagreement as a character defect. Part III starts the practical work: useful tasks, shared tools, actual recipients, and results somebody can check. You can begin with Chapters 9, 11, and 12 if you want the food example first, then return to the larger horizon.

The book keeps the imagination because possibility matters. It keeps the failures because consequences matter. Elijah doesn't become an engineer, an agronomist, and a lawyer by asking a machine to sound confident. Other people know things. Listening to them is part of his education.

## History as a question, not a verdict

The Precedent Ledger contains twenty-three cases, P-01 through P-23. Their purpose is to illuminate recurring incentives, adaptation, conflict, and uneven benefits. They cannot prove that today's critics are wrong or that my forecast will arrive on schedule.

Read each case for its mechanism and its limits. Who benefited? Who paid? What did people change? Which conditions don't carry over? A warning that helped avert harm belongs in the record alongside a prediction that failed. So does optimism that didn't deliver.

The practices ask you to make one observation, conversation, or small experiment useful. They don't ask you to prove your worth by becoming a tireless producer. Rest, care, art, and receiving help fit inside the future I'm arguing for.

Wide lens, narrow focus.

If these machines can take on more of the work of keeping us alive, let's direct them toward the people who need that help. Start with food. Make the result real enough that the fired cook can eat it.

Then let's see what else becomes possible.
'''
PREFACE='''So the robots are coming for the jobs. Congratulations, apparently. Now we get to decide what we mean by progress.

Popular stories give us plenty of machines to fear and plenty of ruined worlds to walk through. I want room for a different question: what useful work could these tools do for people who are tired of being afraid?

This is an optimist's field manual. Optimism here means wanting a better outcome enough to investigate how it might work. It doesn't mean calling every concern cowardice or every announcement a breakthrough. You can be hopeful and still ask who gets the food when the machine finishes its shift.

The first priority is a food baseline independent of employment and ability to pay. The larger horizon includes land care, cleanup, shelter, and other forms of assistance. Those possibilities are invitations to investigate, not promises that buying the right parts makes an entire life autonomous.

You will meet people who are wrong about important things. Some of them notice. Some need help noticing. That's the point of the scenes. The co-op has skills Elijah doesn't have, and the people who receive help can tell it something a dashboard can't.

A change of attitude can give you room to act. It doesn't erase coercion, exhaustion, poverty, disability, or a broken piece of equipment. If a recommendation doesn't fit your life, that is information about the recommendation too.

You don't need to become a different kind of person to enter this book. You don't need land, a server rack, or the spare cash to buy a robot. Start with curiosity. Ask somebody what they need. Try a bounded task with their agreement. Keep enough attention free to notice whether it helped.

The book is meant to give you something you can evaluate and criticize. If a claim is wrong, improve it. If a tool is unnecessary, put it down. If somebody is hungry, the argument has a destination beyond winning the argument.

Let's get to that destination.
'''
CONCLUSION='''## Food is a place to begin

The book ends where the proposal began: if machines can take on necessary work, direct that capability toward enough food for everyone, regardless of employment or money.

The line cook still eats after he loses the job. The restaurant can still sell a meal. People can still work, make things, earn money, argue over institutions, and choose different lives. A food baseline doesn't settle all of those questions. It changes the conditions under which people face them.

I think that would change a lot for the better. I want us to build it.

## My forecast remains a forecast

My personal expected date for AGI is Thanksgiving 2027. Why that day? Because. The date is my prediction, not a timetable the universe owes me.

Recursive improvement, reliable physical machines, and widespread access are separate questions. If the date passes without the capability I expected, the forecast needs revising. We don't need to pretend otherwise to keep working on useful food and mutual aid.

The result I'm asking you to look for is simpler than an argument about whether the singularity has technically happened. Did someone receive useful help? What work did the machine actually do? What did it cost, including other people's time? Could the person receive it without having money? What would keep it available next time?

## Talk, try, adapt

Have one conversation with someone whose work or needs give them a view you don't have. Explain the food-first proposal in plain language. Ask for the strongest concern and listen long enough to understand it.

With a willing partner, choose one small task. Keep it within the skills and resources available, preserve the existing service, and agree what a useful result would look like. You may be planning, documenting, coordinating, testing a tool, or explaining why a proposed delivery won't work for you. Participation has more than one shape.

Then review it. Count the mistakes and the extra labor. Let the recipient's experience matter. Keep what helped; revise or stop what didn't. Invite another person to inspect the result instead of requiring them to share your optimism first.

That's a beginning, not a replacement for the public and institutional work ahead. Food safety, dependable provision, access, worker transitions, and the terms of ownership need people working together over time. Naming that work doesn't mean each reader has to solve it alone.

## Keep the larger promise in view

I don't want a future where we invent extraordinary machines and use them to make ordinary people more frightened about dinner. I want the reduction in necessary toil to mean something in a person's actual day.

Enough food to eat. More room to choose. More time for the people and work we care about.

Wide lens, narrow focus. Make the first useful thing real, and give the next person something they can build on.

Food first. Then we can go from there.'''
APPENDIX_A='''# APPENDIX A: QUESTIONS FOR A FOOD BASELINE

*This is a discussion brief, not an ordinance or a claim of legal authority. Use it with affected residents, workers, food providers, relevant specialists, and public institutions.*

## The proposal

Make adequate food available regardless of employment or ability to pay. Use automation where it demonstrably helps supply that food, while preserving effective existing methods and services. Keep the person receiving food at the center of the account.

The proposal does not require abolishing restaurants, paid employment, or food sold above the baseline. It does require discussing how a dependable baseline will be provided, including for people who cannot prepare or store ingredients.

## Questions worth bringing to the table

1. **Need:** Who lacks dependable access now? What do they say is missing? Include people outside existing membership lists and people unable to attend meetings.
2. **Food:** What constitutes suitable and sufficient provision across dietary needs, seasons, and living circumstances? Who has the relevant expertise to evaluate it?
3. **Work:** Which tasks are already well served? Which are difficult to provide? What can a proposed machine actually do, and what remains human work?
4. **Access:** How does someone request or receive food without money, a smartphone, transport, or proof of employment? What happens when a person disagrees with an organizer?
5. **Provision:** Who covers equipment, operating costs, maintenance, remaining labor, storage, and distribution? Which commitments are real, and how long do they last?
6. **Continuity:** What happens to the meal when a machine, crop, vehicle, funding source, or organization fails? Is the alternative confirmed?
7. **Workers:** Who gains or loses income, time, discretion, or bargaining power? How do the people doing the work participate in the decisions?
8. **Authority:** Which existing permissions, responsibilities, and public processes apply? Who is accountable for resolving disputes and correcting harm?
9. **Evidence:** What comparison would show that a proposed change helps? Who checks the result? What would make us revise or stop it?

## A bounded first proposal

Describe a small trial in one page: the need, partners, task, recipient route, available resources, duration, comparison, and review date. Keep the existing service operating while the trial runs. State what has not yet been arranged.

Don't present this page as a universal legal template. It grants no tax exemption, power to terminate a contract, suspension of other rules, or immunity from a claim. Those earlier promises were beyond what the book could establish.

A community can endorse the goal and still disagree about the means. Evidence should inform that disagreement. It doesn't eliminate the need for judgment, public participation, and decisions people can challenge.

The purpose of the brief is to make the next conversation concrete enough to improve the proposal.'''
APPENDIX_C='''# APPENDIX C: EXECUTIVE REFERENCE GUIDE

## The proposal in one minute

Use AI and robots to help make adequate food available to everyone, regardless of employment or money. A person who loses a job should still be able to eat. Restaurants, paid work, and meals sold above the baseline can coexist with that goal.

Free to the recipient does not mean costless to provide. Equipment, maintenance, remaining labor, and distribution need dependable provision. Lower production costs don't automatically settle access.

## Four separate questions

| Question | What would answer it? |
| --- | --- |
| Capability | Evidence that the system performs the specified tasks reliably. |
| Improvement | Tested improvements, including failures and limits of the process. |
| Deployment | Useful operation under the actual physical and organizational conditions. |
| Access | People receiving the result on terms they can use, including without money. |

AGI is used here for broad, adaptable intellectual capability. RSI means recursive self-improvement. Neither term means that universal robotic food service has been delivered.

## The forecast

The author's personal AGI expectation is U.S. Thanksgiving, November 25, 2027. Timing is uncertain. That date is not a promised RSI milestone, a mathematical conclusion, or a delivery date for a household robot. Food work remains useful if the forecast is wrong.

## The nine-stage horizon

Stages 1–5 consider commercialization, restriction, authority, access, and human responses. They are possible pressures and choices, not an inevitable sequence. Stages 6–7 imagine much more advanced systems, space activity, and biological change. Stages 8–9 explore cosmic and simulation possibilities. The later stages are increasingly speculative and do not supply evidence for the practical proposal.

Mutually assured survival is the author's conviction and organizing goal, not a necessary consequence of intelligence.

## The practical sequence

Food; other land management; ordinary trash cleanup; shelter; further useful applications. This prioritizes the program rather than making urgent shelter or care wait.

Follow one need through a task, tools, human and machine roles, execution, and checked result. Count what actually reaches a person. Preserve access during experiments. Compare against simpler and existing methods.

## A first move

Talk with an existing food provider or someone who needs help. Agree one bounded trial. Review what happened, including costs, failures, and the recipient's experience. Keep the useful part and change the rest.

Wide lens, narrow focus.'''
APPENDIX_E='''# APPENDIX E: COMPUTING YOU CAN USE

A cyberdeck is a custom personal computer, often built around a particular set of interfaces and tasks. It can be an enjoyable way to learn, repair, and adapt equipment. It is optional here.

## Start with the device you have

A phone or existing computer may already support a task log, a pickup schedule, photographs taken with consent, or saved reference material. Some applications and content work offline when prepared for that use. Check the particular device and task rather than assuming that a disconnected phone becomes useless.

A shared computer may offer capabilities your own device lacks. A custom build becomes worthwhile when you can name the missing function and support the resulting machine. It shouldn't become the price of participating in mutual aid.

## Keep the capabilities separate

An offline library stores reference material. A language model generates responses that still need checking. A radio communicates within the capabilities of its hardware, configuration, and operating conditions. Combining them in a case doesn't make every answer correct or every communication dependable.

A machine operating locally still needs access controls, maintenance, and appropriate handling of private information. It is not automatically unhackable. A live network connection is not an air gap. Choose the terms by the actual connectivity, as discussed in Chapter 11.

For power, use a compatible, documented arrangement. This appendix does not depend on the salvaged-cell assembly removed from Chapter 17. A custom battery system is a separate engineering task.

## One useful offline check

With the device you already have, save a non-sensitive reference you are permitted to copy. Disconnect from the relevant network and confirm that you can open it, read it comfortably, and locate what you need. Record its source and date so someone can check whether it has become outdated.

That exercise establishes one limited capability: this copy can be read without that connection. It doesn't prove the source correct or turn the device into a complete emergency system.

If your next task requires additional equipment, ask someone experienced with that task to help compare options. Use communications equipment within the permissions and rules applicable to the actual use. A book about food access need not become a radio or intrusion manual to make computing useful.

The best machine for this project is the one that helps the people doing the work and can be kept working. Sometimes it fits in a custom case. Sometimes it is already in your pocket.'''
# Historical stories retained where possible; remove unsupported universal inferences.
RULES={
1:('A change in access can unsettle familiar authority. That possibility does not explain every concern, and it does not establish that every new medium is harmless.','Ask what changed and what the concern actually predicts.','Ask a younger or older user to show you a useful workflow.','Write down one benefit and one plausible cost.','Test the specific concern instead of assigning the speaker a motive.'),
2:('A demonstration can reveal an unfamiliar use. Adoption still depends on reliability, infrastructure, cost, and demand.','Separate a compelling demonstration from a delivered service.','Record what one demonstration actually shows.','List the work between that demonstration and ordinary use.','Revisit your prediction in six months, including what failed to arrive.'),
3:('The aviation forecast illustrates a large error. One failed pessimistic prediction cannot tell us the direction or size of the next error.','Hold optimistic and pessimistic forecasts to the same evidence.','Save one optimistic and one pessimistic prediction with their dates.','Write the observation that would count against each.','Choose a review date and include your own prediction in the record.'),
4:('A rule can change the cost and location of development. Its purpose and effects need a particular causal record, not a general story that every restriction is capture.','Read the rule before turning it into a morality play.','Identify one actual proposal relevant to your task.','Separate its stated purpose, operative terms, and predicted effects.','Ask who benefits, who bears costs, and what evidence would change your view.'),
5:('A state can stop supporting a capability for several reasons. One decision is not a complete explanation of a civilization or its later history.','Examine what sustains a capability before assuming it will persist.','Name one capability your project depends on.','Find who maintains its skills and equipment.','Identify what you could do if that support ended.'),
6:('New accounts of the world can challenge institutions and identities without eliminating meaning from ordinary life. The changes are neither painless nor uniform.','Leave room for meaning without making humanity the center of every explanation.','Name something you value that is not a contest with a machine.','Ask how assistance could give you more room for it.','Notice a person whose experience differs from your expectation.'),
7:('Machines changed the demand for animal labor and the occupations around it. Human dignity and rights do not follow from an animal-power cost comparison.','Measure the task without pricing the person as obsolete.','List the tasks a tool could change in one job.','Ask the worker what important work the list missed.','Separate time saved from the consequences for income and choice.'),
8:('Agricultural transitions involved different conditions and outcomes across places. Greater production or wider adoption does not establish better lives for every participant.','Count welfare and distribution separately from adoption.','Describe one claimed gain from a tool.','Ask who might bear a cost even if that gain is real.','Choose an outcome measure that includes those people.'),
9:('Worker resistance concerns wages, skill, power, and working conditions as well as machinery. Its outcomes cannot be reduced to whether a technology disappeared.','Take the livelihood claim seriously before judging the tactic.','Ask a worker which terms a proposed tool would change.','Identify who controls the introduction and the time saved.','Record a concern the project must address before expansion.'),
10:('Collective bargaining can alter how benefits are shared even when adoption continues. A funding mechanism is a different outcome from preserving every old job.','Study changes in the terms, not only whether the machine was stopped.','Name one benefit created by a proposed automation.','Ask how displaced workers participate in decisions about it.','Distinguish a proposed support mechanism from a funded commitment.'),
11:('Publicity can connect a commercial interest with a sincerely held value. That does not establish total control over an audience or every participant\'s private motive.','Ask who benefits from a message and check what it asks you to believe.','Record one persuasive technology claim.','Find its sponsor and the evidence it supplies.','Compare the promised result with something independently observable.'),
12:('Interdependence can transmit disruption. Different communities also have different resources and capacity to adapt; neither localism nor centralization guarantees survival.','Name the dependency and the disruption you are preparing for.','Map one input to your food project.','Confirm a realistic alternative with its provider.','Record what would remain unavailable during an interruption.'),
13:('A person can value one medium and use another for a different purpose. Mixed practice need not be hypocrisy; the important question is what each method provides.','Choose a medium by the job it does.','Name one task where a familiar method works well.','Compare a new tool on the same task.','Keep the option that helps, including the old one.'),
14:('An industry can combine technical change, restructuring, and differentiated products. That does not establish one universally successful strategy or erase workers\' losses.','Examine specific adaptations and their costs.','Identify the part of a craft people still choose to pay for.','Ask which tools support it and which pressures threaten it.','Do not infer an individual worker\'s options from a large firm\'s resources.'),
15:('Land policy creates opportunity for some people while affecting those already there. Access cannot be understood without eligibility, dispossession, and the terms of ownership.','Ask whose land and whose opportunity the story describes.','Investigate an existing local route to garden or farm access.','Include the rights and interests of current occupants.','Compare purchase with sharing or leasing without assuming future price gains.'),
16:('Standardized components can make some work easier. A delivered kit still depends on a site, assembly, services, and appropriate design.','Count the work outside the box.','Choose an advertised kit relevant to a project.','List what its price excludes.','Ask an experienced operator which additional skills and approvals it needs.'),
17:('Technical awareness, investment, business structure, and financial survival are separate facts. Adoption does not guarantee success, and bankruptcy does not necessarily mean disappearance.','Verify what a company actually did before using it as a warning.','Check an original corporate or archival source for one familiar story.','Separate the technology decision from the financial outcome.','Rewrite your lesson to fit the narrower record.'),
18:('Existing capabilities may find new applications, but firms facing similar shocks can have different assets and constraints. Comparison is not a controlled experiment.','Look for transferable skills without promising effortless reinvention.','List a skill you can demonstrate.','Ask someone in another field where it would be useful.','Test one small application before committing to a costly pivot.'),
19:('Food production can expand through coordinated participation. Inputs, skills, institutions, and the kind of food counted matter to the result.','A vegetable harvest is a contribution, not a complete diet.','Ask an existing garden how it measures usable output.','Follow one harvest through handling and distribution.','Record the food needs that harvest does not meet.'),
20:('Accessible language and distribution can help an argument travel. Political change also depends on organizing, circumstances, and other people.','Give people something clear enough to discuss and verify.','Write a short account of one useful result.','Ask a reader to explain it back and identify a weakness.','Revise before sharing more widely, with appropriate consent.'),
21:('Curation can make tools and knowledge easier to find. Access also involves cost, skills, maintenance, and whether a tool fits the task.','Build a useful toolset, not a collection of promises.','Inventory what your group already has.','Identify one missing function rather than a fashionable product.','Find who can teach and maintain the proposed tool.'),
22:('Preparation can change the outcome that a warning anticipates. A quiet result alone cannot tell us how much harm would otherwise have occurred.','Evaluate precautions by the risk and evidence, not by whether disaster supplied a spectacle.','Choose one failure in the food-service premortem.','Confirm a response and who will carry it out.','Review the warning and response after a bounded exercise.'),
23:('Some prominent internet forecasts failed. That establishes human fallibility, not a law that every technology improves or every criticism becomes obsolete.','Let actual results change the plan, including your optimistic plan.','Keep a dated record of claims from enthusiasts, critics, and yourself.','Record reliability, cost, access, and effects on people alongside capability.','At the review date, retain the useful part and revise what the evidence did not support.')}
STORIES={
2:'''At the 1876 Centennial Exhibition, the large Corliss steam engine and Alexander Graham Bell's telephone offered very different pictures of useful machinery. The telephone carried a human voice over a wire, a capability whose eventual uses extended far beyond a single demonstration.

The contrast is worth considering without pretending the entire audience agreed about either machine. A fairground reaction is a small piece of a much longer adoption story.''',
3:'''On October 9, 1903, the New York Times published “Flying Machines Which Do Not Fly.” The editorial imagined a working flying machine taking an extraordinarily long period of further effort. Later that year, the Wright brothers flew at Kitty Hawk.

The juxtaposition is memorable because the forecast failed so dramatically. It does not turn a newspaper editorial into a representative sample of all contemporary expertise, or a warrant to disregard expertise now.''',
4:'''Britain's Locomotives Act of 1865 imposed restrictions on road locomotives, including a person proceeding ahead with a red flag. The flag was carried ahead of the vehicle; it was not sixty yards of cloth.

The episode raises useful questions about how law, public concern, transport interests, and new equipment interact. It should not be compressed into a claim that all road vehicles faced identical conditions or that a single statute explains the later geography of the automobile industry. An analogy to a present restriction needs the text and context of both rules.''',
5:'''Zheng He's early-fifteenth-century expeditions connected Ming China with ports across the Indian Ocean. The court later stopped sponsoring those voyages.

The decision belongs to a complicated political and economic history. It did not mean that China ceased changing, that all maritime activity ended, or that five subsequent centuries can be explained by one abandoned program. The size of the fleets and the reasons for the decision need their own evidence; neither establishes that future machine civilizations must expand into space.''',
6:'''Copernicus's account displaced Earth from the center of the planetary system. Later developments in astronomy and biology challenged other familiar pictures of humanity's place.

People continued to make breakfast, fall in love, and plant gardens while arguments about those pictures continued. Institutions adapted, resisted, and changed in different ways. There was no single universal reaction, and no simple disappearance of every hierarchy attached to an older account.''',
8:'''The transition to agriculture changed food production, settlement, and social organization across different places and long periods. Some early farming populations show evidence of health burdens associated with those changes.

That makes agriculture a useful complication for a book about technology. A practice can spread while imposing costs on some of the people adopting it. The history is not a single vote by humanity, and it is not a uniform story in which every forager became a farmer or every farmer became better off.''',
9:'''The Luddites were workers responding to changes in their trades, including wages, quality, and the use of machinery. Their actions cannot be adequately described as people who simply failed to understand a new invention.

Machine-breaking met severe repression. The history carries losses that a story about eventual technological adoption can too easily erase. Whether a particular tactic worked is a question about its aims and consequences, not a reason to dismiss every grievance held by the people who used it.''',
10:'''Recorded sound changed work for musicians, including the employment associated with silent-film accompaniment. The American Federation of Musicians campaigned against the displacement and later used recording bans and bargaining to seek different terms.

The Music Performance Trust Fund grew out of that history. Its institutional account describes funding free public performances through arrangements involving the recording industry. This is an example of organized benefit sharing, not evidence that every displaced musician recovered their income or that a fraction of every play automatically reaches the fund. [Music Performance Trust Fund, About](https://musicpf.org/about/)

The useful question is what the bargaining changed. Calling it a failure simply because recorded music survived would miss the institutional achievement. Calling it a complete cure would miss the people whose work disappeared.''',
14:'''Quartz technology and industrial change put Swiss watchmaking under substantial pressure. The Swiss industry was also involved in developing quartz; it was not a single bloc that refused the technology out of purity.

The later Swatch story offers an example of adaptation through products, manufacturing, and restructuring. It should not be made into a claim that only one strategy has ever worked or that success at the industry level erased the losses experienced by workers.''',
15:'''The Homestead Act of 1862 made land available to eligible claimants under specified conditions. Its promise of opportunity helped shape settlement and agriculture.

That land was already inhabited by Indigenous peoples. The National Park Service's account recognizes that history alongside the experiences of homesteaders. Access for one group cannot be told honestly as though it took place on a blank map. [National Park Service, Homestead History and Culture](https://www.nps.gov/home/learn/historyculture/index.htm)

The case belongs in a discussion of land access, eligibility, power, and dispossession. It supplies no evidence that buying rural property today guarantees appreciation or security.''',
16:'''Sears sold house plans and materials through its catalog, later including precut lumber. The kits could make parts of construction easier to organize and assemble.

They still needed a site, a foundation, labor, local infrastructure, and the other work required to turn supplied materials into a home. A surviving house is evidence that a particular house endured, not proof that every kit was safer or better than every alternative. The useful lesson concerns how expertise can be embodied in components and instructions without making the surrounding work disappear.''',
17:'''Kodak, Sears, Blockbuster, and Borders are often compressed into one warning about businesses that failed to adapt. Their histories are not identical, and the details matter.

Kodak developed digital-camera technology and sold digital products. Its own milestones also record emergence from Chapter 11 in 2013. “Never adopted digital” and “ceased to exist” therefore fail as summaries. [Kodak, Milestones](https://www.kodak.com/en/company/page/milestones/)

The cases of Sears, Blockbuster, and Borders raise their own questions about distribution, business models, debt, competition, and decisions made under uncertainty. Each needs a separate causal account. A collection of famous names isn't a controlled test proving that one attitude determines survival.''',
18:'''Fujifilm applied capabilities associated with its photographic business to other fields as demand for film changed. The comparison with Kodak can prompt a useful inventory of skills and assets.

It cannot establish that the firms were identical, faced identical choices, or had outcomes caused by one difference in attitude. Nor can a corporation's ability to diversify be handed to a displaced worker as though it were a resource already in their pocket.''',
19:'''During the Second World War, Victory Gardens made household and community growing part of a broader food effort in the United States. The example belongs here because it joins participation with organized practical support.

Claims about their share of production must keep the denominator visible: fresh vegetables are not all food or all dietary energy. The story also includes access to land, knowledge, supplies, and coordination. A garden's contribution can be substantial without making a household independent of the rest of the food system.''',
20:'''Thomas Paine's Common Sense helped make an argument for independence accessible to readers in 1776. Printing and circulation mattered to the pamphlet's reach.

The argument moved through an existing political conflict, networks of readers and printers, and other people's organizing. It did not create a revolution by itself. The case makes a strong argument for clear language and distribution without requiring one author to become the sole cause of a historical transformation.''',
22:'''The year-2000 computing problem prompted extensive checking, repair, testing, and coordination. The GAO's retrospective describes lessons from that work. [GAO, Year 2000 Computing Challenge](https://www.gao.gov/products/aimd-00-290)

The relatively quiet transition doesn't by itself show that the work was unnecessary. It also doesn't establish exactly what would have happened without it. The counterfactual remains a different question from the documented preparation. A useful lesson can preserve both points without an unsupported superlative or a dramatic global cost estimate.''',
23:'''Clifford Stoll, Paul Krugman, and a Daily Mail headline supplied memorable skeptical predictions about the internet's future. The internet subsequently became important in ways those particular predictions failed to anticipate.

A missed forecast deserves correction. It doesn't follow that every contemporary complaint was accurate, that every technological weakness is temporary, or that the next optimistic forecast is safe. The point of keeping receipts is to become easier to correct, including when you want the prediction to be true.'''}
TITLES={6:'Chapter 6: Is the Singularity a Done Deal?',7:'Chapter 7: Work, Loss, and the Cooperative Response',11:'Chapter 11: King and Queen of Your Own Robotic Court',13:'Chapter 13: Shelter as a Later Application'}
BRIEFS={
1:['AGI, recursive improvement, physical deployment, and access are separate questions.','Thanksgiving 2027 is a personal forecast, not a mathematical deadline.','Useful food work need not wait for a system that can do everything.'],
2:['The stages are scenarios that may overlap or fail to occur.','Technical competence does not confer authority over a community.','A food baseline and paid work can coexist.'],
3:['Greater capability does not establish a system\'s motives.','Space activity and biological transformation remain speculative horizons.','Food work can proceed without settling those possibilities.'],
4:['Cosmic scenarios are an imaginative horizon, not operational evidence.','Simulation arguments depend on assumptions.','The practical proposal stands without a claim about the ultimate universe.'],
5:['Machines require inputs, maintenance, and provision.','Keep food, energy, labor, and money in separate ledgers.','Free to a recipient is different from costless to provide.'],
6:['Capability, deployment, and access can move at different speeds.','Material constraints matter alongside attitudes.','Begin with people already doing useful work.'],
7:['Job loss is a real loss even when automation improves a task.','A person can disagree about a machine and still support food access.','The cook can lose the job and still eat.'],
8:['Try attention practices as adaptable experiments, not medical treatments.','Cooperation must not depend on threatening someone with hunger.','Models and small groups do not automatically produce fair decisions.'],
9:['Follow the work through growing, harvesting, handling, and delivery.','A modest trial can test a contribution without proving complete nutrition.','Count remaining labor and compare the machine with an existing method.'],
10:['Productivity is not a condition of deserving food.','Start with an existing need and a bounded contribution.','Share useful results without promising virality or income.'],
11:['Your robotic court begins with useful assistance, food first.','A food baseline can coexist with restaurants and chosen work.','Local computing still needs careful operation; the postmortem matters.'],
12:['Land access need not mean buying property.','Grandma\'s request needs a confirmed service, not a technological label.','Count what people and machines actually do, and what reaches her door.'],
13:['The failed weld teaches respect for skill.','A sketch and a materials subtotal do not establish a habitable dwelling.','Shelter is an optional later application, not the entry fee for food work.'],
14:['Local capacity still has outside dependencies.','An interruption plan needs a confirmed alternative.','Communication tools should match the messages they carry.'],
15:['An instrument observes a particular part of the world.','The soil scene is fiction, not a treatment trial or safety certificate.','Follow the harvest into food people can actually use.'],
16:['A useful record can help without becoming a media business.','Consent and privacy belong in the publishing process.','Availability and income are not guaranteed by a platform or a file format.'],
17:['Choose tools by the task and the support available.','Food comes first; ordinary cleanup can follow an existing disposal route.','Compare whole outcomes, including maintenance and remaining human work.'],
18:['The room can identify what the model missed.','Every promised service needs a response when a dependency fails.','A pilot and a dependable baseline are different commitments.']}

def main():
 for f,h in BASE['files'].items():
  assert hashlib.sha256((BOOK/f).read_bytes()).hexdigest()==h, f'Changed baseline: {f}'
 files={f:(BOOK/f).read_text() for f in BASE['files']}
 for f,t in list(files.items()):
  m=re.match(r'\d+-chapter(\d+)\.md',f)
  if m and int(m[1]) in FOUNDATIONS:
   n=int(m[1]);pre,rest=t.split('## The Foundations',1);prec=re.search(r'^## Precedent ',rest,re.M)
   assert prec,f
   t=pre+'## The Foundations\n\n'+FOUNDATIONS[n]+'\n\n---\n\n'+rest[prec.start():]
   t=re.sub(r'\*\*In this chapter:\*\*.*?\n---', '**In this chapter:**\n\n'+'\n'.join('- '+s for s in BRIEFS[n])+'\n\n---',t,count=1,flags=re.S)
   if n in TITLES:t=re.sub(r'^# .*', '# '+TITLES[n],t,count=1)
  files[f]=t
 t=files['02-introduction.md'];cut=t.index("It's time.");files['02-introduction.md']=t[:cut]+INTRO+'\n'
 t=files['01-preface.md'];a=t.index('So the robots');b=t.index('## Precedent');files['01-preface.md']=t[:a]+PREFACE+'\n---\n\n'+t[b:]
 t=files['21-conclusion.md'];pre,rest=t.split('## The Foundations',1);b=rest.index('## Precedent');t=pre+'## The Foundations\n\n'+CONCLUSION+'\n\n---\n\n'+rest[b:]
 t=re.sub(r'\*\*In this chapter:\*\*.*?\n---','**In this chapter:**\n\n- Food remains the first priority, whatever the forecast date.\n- Talk with curiosity, try a bounded task, and review what happened.\n- Keep the story\'s human ending and carry the work into your own circumstances.\n\n---',t,count=1,flags=re.S)
 files['21-conclusion.md']=t
 for f,txt in [('22-appendix-a.md',APPENDIX_A),('24-appendix-c.md',APPENDIX_C),('26-appendix-e.md',APPENDIX_E)]:files[f]=txt+'\n'
 for f,text in [('part1-divider.md','This part separates observed capability, personal forecasts, and speculative horizons. The nine stages are a framework for asking questions, not an inevitable sequence. Keep food and useful help in view as the horizon widens.'),('part2-divider.md','Change involves equipment, resources, institutions, and people. This part asks how we cooperate without making disagreement a moral defect or hunger a tool of compliance.'),('part3-divider.md','Begin with food reaching a person. Use existing relationships and tools where they work; compare new methods on a bounded task. You can take part without owning land, a rack of servers, or a robot. Wider possibilities remain available as the work develops.')]:
  t=files[f];head=t.split('\n\n',2);files[f]='\n\n'.join(head[:2])+'\n\n'+text+'\n'
 # Rebuild the interpretive tail of each precedent, preserving the indexed ID.
 for f,t in list(files.items()):
  def case(m):
   block=m.group();n=int(re.search(r'P-(\d+)',block)[1]);heading=block.splitlines()[0]
   story=block.split('**The mechanism.**')[0].split('\n',1)[1].strip()
   if n in STORIES:story=STORIES[n]
   mechanism,rule,*actions=RULES[n]
   return heading+'\n\n'+story+'\n\n**The mechanism.** '+mechanism+'\n\n**The rule.** '+rule+'\n\n**The practice.**\n\n'+'\n'.join(f'{i}. {a}' for i,a in enumerate(actions,1))+'\n\n---\n\n'
  files[f]=re.sub(r'^## Precedent P-\d+.*?(?=^## Precedent|\Z)',case,t,flags=re.M|re.S)
 # Appendix D remains an index, with the same rules as the chapter entries.
 t=files['25-appendix-d.md'];table=t[t.index('| ID |'):t.index('## The rules')].strip()
 files['25-appendix-d.md']='# APPENDIX D: THE PRECEDENT LEDGER\n\nTwenty-three historical cases, P-01 through P-23, accompany the argument. Each case asks about a mechanism and its limits. None proves a date for AGI or a universal law about progress.\n\n## How to use the ledger\n\nRead the case, then identify one similarity and one difference from your situation. Ask who benefited, who bore costs, and what would count against the proposed lesson. Choose a practice that fits your resources and circumstances. Discomfort alone is not evidence that an exercise is useful.\n\n## The Ledger\n\n'+table+'\n\n## The rules, in one breath each\n\n'+'\n'.join(f'- **P-{n:02}.** {v[1]}' for n,v in RULES.items())+'\n\n## Sources and limits\n\nAppendix B preserves the research bibliography. Historical interpretation remains distinct from the events it describes. Compare original records where possible, treat quotations in context, and record corrections. A precedent is a prompt for investigation, not permission to ignore a present objection.\n'
 # Mechanical cross-version repairs and narrative clarifications.
 for f,t in list(files.items()):
  t=t.replace('Using the Tech to Your Advantage','King and Queen of Your Own Robotic Court')
  t=t.replace('Chapter 6: The Singularity Is a Done Deal',TITLES[6]).replace('Chapter 7: The Battle Lines: The Entitled vs. The Ready',TITLES[7]).replace('Chapter 13: The Shouse Protocol',TITLES[13])
  t=t.replace('twenty-two','twenty-three').replace('twenty-one practices','twenty-two practices')
  t=t.replace('eight years of Claypot','two years of Claypot').replace('three days before, right on schedule','four days before, right on schedule')
  t=t.replace('an entire generation of authority figures','some contemporary authority figures')
  t=t.replace('The women in the parade experienced it as liberation.','The campaign presented the act as liberation.')
  t=t.replace('the back-to-the-land commune and the personal computer both came out of its pages, carried by the same readers.','its readership connected strands of back-to-the-land culture and personal computing without being the sole source of either.')
  t=t.replace('The weirdness arrived on schedule.','An earlier chapter in the history of robotics.')
  t=t.replace('The same machines ending careers will happily work for you.','A robot demonstrates a particular set of physical capabilities.')
  t=t.replace('The data does not care how you feel about it.','A demonstration is the beginning of a capability question.')
  t=t.replace('Senior and calm. Wrong about the thing that mattered.','Senior and calm. Elijah needs more than reassurance.')
  t=t.replace('The Foundations below are the hearth. Build the stones before you strike the spark.','The checklist was a beginning. It was not the last thing they would have to learn.')
  files[f]=t
 # Preserve the plot while removing a false general inference from one training run.
 f='03-chapter1.md';t=files[f];a=t.index("The thing hadn't hit a ceiling");b=t.index('He left the tower off',a)
 files[f]=t[:a]+'''The run had stopped at a limit he could feel: heat. He wanted that to explain everything. Give it more power, give it better cooling, and perhaps the curve would keep falling. He almost wrote that down as proof.

Then he looked at the notebook again. The run had not tested every task. A falling training loss was not the same as understanding an unfamiliar problem. The machine had forced one question into the room and left the larger ones where they were. He wrote COOLING in one column and WHAT DID IT LEARN? in another.

He still didn't know what to tell Devendra. He knew only that reassurance was not a measurement, and neither was fear.

'''+t[b:]
 # Rewrite the contaminated-site trial as a sensor lesson, not a treatment recipe.
 f='17-chapter15.md';t=files[f];a=t.index('The reclamation beds went in');b=t.index('In July he brought',a)
 t=t[:a]+'''The trial beds went in beside the co-op's established garden, on ground Priya had already assessed for the project. The old equipment parking area behind the shed stayed outside the food plot. At one end a hydraulic-fluid stain marked a question they weren't going to answer by planting vegetables and hoping.

"The parking lot can wait," she said. "The people eating this can't be the experiment."

That spring she set up a small soil-monitoring trial, comparing mulched beds with reference beds. Elijah instrumented them with probes from the greenhouse-controller stock and a dashboard that made the rows look orderly from anywhere he stood. He liked that part. Priya asked for the readings weekly. She never once asked him to mistake the diagram for the ground.

'''+t[b:]
 t=t.replace('tea beds','mulched beds').replace('tea bed','mulched bed').replace('Whatever the tea is doing','Whatever the treatment is doing')
 a=t.index('And the re-run data was not subtle.');b=t.index('What she got from him',a)
 t=t[:a]+'''The new readings showed that the surface and the deeper soil had been telling different stories. They didn't settle why the beds differed. The irrigation had not been equal, the baseline was incomplete, and a better instrument could not repair the experiment backward in time.

Priya crossed out his first conclusion and wrote a smaller one: THE SENSOR MISSED THE ROOT ZONE. Underneath it she added: RUN THE COMPARISON AGAIN.

'''+t[b:]
 t=t.replace('exactly where the roots had followed the biology','where the roots were growing').replace('watered the healthiest beds hardest','watered those beds more often')
 files[f]=t
 f='20-chapter18.md';t=files[f];needle='"Apprenticeship\'s four years if you\'re serious. So we start Monday."'
 assert needle in t
 t=t.replace(needle,needle+'\n\n"That leaves two years we haven\'t covered," Priya said.\n\nMarta nodded. "Then put that on the board too. We need someone qualified to cover the gap. Starting an apprentice doesn\'t make one finished."\n\nElijah wrote INTERIM WELDING CAPACITY: UNRESOLVED, and left the box open.')
 files[f]=t
 # Bibliography retained as a research record; no claim that every old entry supports this edition.
 t=files['23-appendix-b.md'];pos=t.index('\n')+1
 t=t[:pos]+'''\n*This bibliography retains the book's research history. Inclusion is not a claim that every earlier inference survives in v0.8.0. The focused sources below support only the scope stated; fictional scenes and illustrative calculations are not research findings.*\n\n## Food-first edition: focused source map\n\n- **Agricultural automation and adoption:** FAO, The State of Food and Agriculture 2022. Opportunities and barriers, including inclusion of smaller producers; no universal-service guarantee. https://www.fao.org/agrifood-economics/publications/detail/en/c/1613500/\n- **Bounded garden tasks:** FarmBot tool documentation. Manufacturer description of seeding, watering, and weeding tools; not independent evidence of complete diets or delivery. https://farm.bot/pages/tools\n- **Site suitability:** EPA, Urban Agriculture. Guidance for potentially contaminated sites, not a finding about the fictional garden. https://www.epa.gov/brownfields/urban-agriculture\n- **Soil biology:** University of Minnesota Extension, Soil Biology. Distinct organism functions; no validation of the removed compost-tea recipe. https://extension.umn.edu/natural-resources/conservation/agricultural-soil-and-water/soil-biology\n- **Trash pathways:** EPA, Learn About Aquatic Trash. Intentional and unintentional pathways; no measured claim about a proposed robot's effect on behavior. https://www.epa.gov/trash-free-waters/learn-about-aquatic-trash\n- **Organized benefit sharing:** Music Performance Trust Fund, About. Institutional account; no assertion about the funding effect of every individual recording play. https://musicpf.org/about/\n- **Historical continuity:** Kodak, Milestones. Digital activity and emergence from Chapter 11; a corporate source, not a complete independent causal history. https://www.kodak.com/en/company/page/milestones/\n- **Land history:** National Park Service, Homestead History and Culture. Homesteading and prior Indigenous habitation. https://www.nps.gov/home/learn/historyculture/index.htm\n- **Preparation:** GAO, Year 2000 Computing Challenge, AIMD-00-290. Documented management work, not a measured global counterfactual. https://www.gao.gov/products/aimd-00-290\n\n## Earlier research bibliography\n'''+t[pos:]
 files['23-appendix-b.md']=t
 for f,t in files.items():
  (BOOK/f).write_text(t.replace('\u2014',',').replace('a agricultural','an agricultural'))
 m=json.loads((BOOK/'book.json').read_text());m.update(version='0.8.0',lastUpdated='2026-09-21',subtitle='Food First, Then the Future')
 for s in m['sections']:
  match=re.fullmatch('chapter(\d+)',s['id'])
  if match and int(match[1]) in TITLES:s['title']=TITLES[int(match[1])]
  if s['id']=='appendix-a':s['title']='Appendix A: Questions for a Food Baseline'
  if s['id']=='appendix-e':s['title']='Appendix E: Computing You Can Use'
 (BOOK/'book.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
 print('Edited',len(files),'sections. Version',m['version'])
if __name__=='__main__':main()
