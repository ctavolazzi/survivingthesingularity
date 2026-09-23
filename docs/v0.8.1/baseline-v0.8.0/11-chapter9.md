# Chapter 9: Deglobalization and the Neighborhood Factory

![Desktop 3D printer mid-print](/book-images/ch09-3d-printer.jpg)

*A desktop 3D printer. The neighborhood factory fits on a workbench. (John Abella, CC BY 2.0, via Wikimedia Commons)*


> *"Man is small, and, therefore, small is beautiful."*
> E. F. Schumacher, *Small Is Beautiful* (1973)

**In this chapter:**

- Follow the work through growing, harvesting, handling, and delivery.
- A modest trial can test a contribution without proving complete nutrition.
- Count remaining labor and compare the machine with an existing method.

---

The co-op's first real manufacturing run, the thing Elijah would later describe to strangers as *the neighborhood factory booting up*, though at the time it was just a January argument in a cold shed, was forty greenhouse controllers for the CSA network two valleys over.

The order came through a friend of a friend of Priya's: forty small boxes that could read soil moisture and air temperature and open a vent or a valve without asking a server in Virginia for permission. Real money, real deadline, real customers with real seedlings on the line. Elijah volunteered for the design with the eagerness of a man who had spent the autumn sweeping floors and learning the shop and could feel, at last, the shape of something he was actually trained to do.

He designed a beautiful thing. He wants that on the record, with the caveat that so does everyone in this story every time he says it. Custom four-layer PCB, an elegant little system-on-module, sensors from a Swiss outfit whose datasheets read like poetry, the whole thing potted in resin, sleek as a river stone, no user-serviceable parts inside. He presented it to the shop on a Tuesday with renders. *Renders.*

Marta looked at the renders for a while.

"Walk me through the bill of materials," she said, so he did, and she wrote three numbers on the whiteboard while he talked: **11**, **1**, **0**.

"Eleven weeks," she said, tapping the first number, "is the lead time on that Swiss sensor, I just looked it up, and that's the *quoted* lead time, which means it's a prayer. One," the second number, "is how many suppliers make that module, which means the day they discontinue it, all forty of these are bricks, and we're the ones who sold bricks to farmers. And zero," she tapped the last, "is how many people in this valley can fix a potted resin board when it fails during frost week. Including you, college. *Especially* you, because you'll be the one who's busy." She capped the marker. "It's a gorgeous design. It's a Claypot design. Everything single-sourced, nothing repairable, the whole thing optimized for the demo instead of the Tuesday three years from now when it breaks during calving. Design it again, and this time the spec is: parts from the drawer, parts from the junction box aisle, and nothing your neighbor can't fix with the tools he already owns."

"That'll be uglier," Elijah said.

"It'll be *ours*," Marta said. "Ugly is a maintenance feature. Ugly means the next guy can see how it works."

So he designed it again, and the second version was simpler to explain and repair: a Raspberry Pi anybody could buy anywhere, screw terminals instead of poetry, capacitive sensor probes at four dollars, a case Denny's kid printed forty of in PETG the color of school buses, relays you could buy at any electrical counter in America. The firmware did less and survived more. Every unit had a laminated one-page repair card zip-tied inside the lid, because Marta's rule was that documentation you have to go find is documentation that doesn't exist.

![A yellow PETG 3D-printed greenhouse controller box, lid open, a Raspberry Pi and screw terminals visible inside](/book-images/ch09-controller.png)

*The controller. Field-repairable. Screw terminals instead of poetry.*

The build itself took the shed three weekends, and it was during the second one, everyone deburring enclosures and crimping ferrules in an assembly line that Sal himself would have recognized from 1985, that the door opened and let in a rectangle of cold light and a lean man in a good coat who was too pleased with himself for a Saturday.

"Reuben Vance," Marta said, not looking up from the crimper. "Elijah. Elijah, Reuben. Reuben handles the part of the machine that runs on paper."

![A lean man in a well-tailored dark coat, carrying a leather folio of papers](/book-images/ch09-reuben.png)

*Reuben Vance. Handles the part of the machine that runs on paper.*

"I heard," Reuben said, pulling folding chairs toward the woodstove like a man dealing cards, "that this operation is about to *sell manufactured electrical goods across county lines*." He said it the way other men say *rob a train*. He produced a folder. "So before anyone gets excited, here is what I did yesterday instead of having a life. Seller's permit: done, we're registered. Resale certificate for the component purchases, which, you're welcome, is about nine percent of your margin back. The shed's ag-exempt status survives because the controllers are agricultural equipment, and I have the assessor's email agreeing they are, in writing, because the assessor and I have an understanding built on me never making her think twice." He looked up. "Also your liability language on the invoice was going to get you sued by the first frost, so I rewrote it. You're a farm tool now, legally speaking. Farm tools have four hundred years of friendly precedent. Software has forty years of hostile precedent. Never be software if you can be a tool."

Elijah looked at the folder, then at Marta. "Did we ask him to do this?"

"Nobody asks Reuben," Priya said, from the crimping line. "Reuben *notices*."

The forty units shipped in February in apple boxes, hand-delivered in Denny's truck, each one tested on the bench against a space heater and a cup of wet dirt. Two came back in the first month, one lightning, one gopher, and both were fixed in an afternoon by the farmers themselves, off the laminated card, with parts from town. Marta put the repair emails up on the corkboard like other shops hang their first dollar.

And somewhere in the middle of all that, without ceremony, somebody finally fixed Elijah's check-engine light. Curtis, it turned out, diagnosed it in nine minutes off a fourteen-dollar OBD dongle, a cracked vacuum line, two dollars of hose. Eleven months that light had been on. The dealership had quoted him twelve hundred dollars and a week; the man who wanted to fence out the world did it while the coffee brewed, because Elijah was co-op now, and that's what the machine of nineteen households does: it notices what's blinking on your dash, and it has the part in a drawer.

That's the whole chapter, really. The rest is engineering.

---

## The Foundations

## Food first means following the food

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

## The record that keeps the promise honest

For that five-household example, the task record could look like this. Every quantity below belongs to the illustration, not to a measured trial.

| Item | Example entry |
| --- | --- |
| Promise | Five households each receive two kilograms of suitable vegetables on Friday, with no charge to recipients. |
| Machine's task | Open an irrigation valve on grower-approved settings. |
| Human work | Inspect the crop and equipment; harvest, sort, pack, transport, and confirm receipt. |
| Available after loss | Eight kilograms from the garden. |
| Remaining commitment | Two kilograms, obtained through the food partner before delivery. |
| Funding | Partner covers supplies and transport; donated time and existing equipment recorded separately. |
| Outcome to check | All five deliveries arrive; recipients can use them; the partner's replacement and extra work appear in the record. |

If the replacement cannot be confirmed, the record must say the promise remains unfulfilled. Calling a shortfall a learning experience does not supply the missing food. The trial's organizers carry that problem; the recipient should not have to discover it by opening an undersized box.

## Compare before expanding

Run the comparison against the garden's ordinary method. Include maintenance, supervision, training, travel, and failed attempts. Keep the existing food service operating during the trial. If a simple timer or an extra paid shift performs better, use it. The recipient needs food, not a demonstration of our loyalty to robotics.

A first result might justify a larger trial. It cannot justify declaring hunger solved. Keep growing the claim only as far as the evidence grows with it.

---

## Precedent P-12: The Year the Bronze Stopped (Eastern Mediterranean, c. 1177 BC)

Late Bronze Age societies around the eastern Mediterranean depended on trade, including the movement of materials used to make bronze. Several societies experienced severe disruption around the end of that period.

Researchers examine interacting pressures rather than one universal switch: climate, conflict, migration, political organization, and interrupted exchange. Places did not all experience the same collapse or recovery. The example invites an investigation of dependencies; it cannot prove that local production always survives or that every large network fails.

**The mechanism.** Interdependence can transmit disruption. Different communities also have different resources and capacity to adapt; neither localism nor centralization guarantees survival.

**The rule.** Name the dependency and the disruption you are preparing for.

**The practice.**

1. Map one input to your food project.
2. Confirm a realistic alternative with its provider.
3. Record what would remain unavailable during an interruption.

---

