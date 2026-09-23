# Chapter 9: Deglobalization and the Neighborhood Factory

![Desktop 3D printer mid-print](/book-images/ch09-3d-printer.jpg)

*A desktop 3D printer. The neighborhood factory fits on a workbench. (John Abella, CC BY 2.0, via Wikimedia Commons)*



**In this chapter:**

- Follow the work through growing, harvesting, handling, and delivery.
- A machine earns its place by improving the complete service.
- A local workshop can serve a regional system without pretending to replace it.

---

The co-op's first real manufacturing run, the thing Elijah would later describe to strangers as *the neighborhood factory booting up*, though at the time it was just a January argument in a cold shed, was forty greenhouse controllers for the CSA network two valleys over.

The order came through a friend of a friend of Priya's: forty small boxes that could read soil moisture and air temperature and open a vent or a valve without asking a server in Virginia for permission. Real money, real deadline, real customers with real seedlings on the line. Elijah volunteered for the design with the eagerness of a man who had spent the autumn sweeping floors and learning the shop and could feel, at last, the shape of something he was actually trained to do.

He designed a beautiful thing. He wants that on the record, with the caveat that so does everyone in this story every time he says it. Custom four-layer PCB, an elegant little system-on-module, sensors from a Swiss outfit whose datasheets read like poetry, the whole thing potted in resin, sleek as a river stone, no user-serviceable parts inside. He presented it to the shop on a Tuesday with renders. *Renders.*

Marta looked at the renders for a while.

"Walk me through the bill of materials," she said, so he did, and she wrote three numbers on the whiteboard while he talked: **11**, **1**, **0**.

"Eleven weeks," she said, tapping the first number, "is the lead time on that Swiss sensor, I just looked it up, and that's the *quoted* lead time, which means it's a prayer. One," the second number, "is how many suppliers make that module, which means when we need a replacement, we're waiting on one company to decide whether to sell it. We need another way to keep these running. And zero," she tapped the last, "is how many people in this valley can fix a potted resin board when it fails during frost week. Including you, college. *Especially* you, because you'll be the one who's busy." She capped the marker. "It's a gorgeous design. It's a Claypot design. Everything single-sourced, nothing repairable, the whole thing optimized for the demo instead of the Tuesday three years from now when it breaks during calving. Design it again, and this time the spec is: parts from the drawer, parts from the junction box aisle, and nothing your neighbor can't fix with the tools he already owns."

"That'll be uglier," Elijah said.

"It'll be *ours*," Marta said. "Ugly is a maintenance feature. Ugly means the next guy can see how it works."

So he designed it again, and the second version was simpler to explain and repair: a Raspberry Pi the regional supplier had in stock, screw terminals instead of poetry, replaceable probes, a case Denny's kid printed forty of in PETG the color of school buses, and documented parts the growers could order from more than one source. The firmware did less and survived more. Every unit had a laminated one-page repair card zip-tied inside the lid, because Marta's rule was that documentation you have to go find is documentation that doesn't exist.

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

By the time the forty units shipped in February, the yellow tab had an answer attached and the folder had grown thick enough to prop open a door. Denny delivered them in apple boxes with the instructions and the agreed support number. Two growers needed replacement probes in the first month. With the power isolated and help from the support call, they could change the documented part without discarding the controller. Marta put the repair emails up on the corkboard like other shops hang their first dollar.

And somewhere in the middle of all that, without ceremony, somebody finally fixed Elijah's check-engine light. Curtis, it turned out, diagnosed it in nine minutes off a fourteen-dollar OBD dongle, a cracked vacuum line, two dollars of hose. The light had been on since the drive north. The dealership had quoted him twelve hundred dollars and a week; Curtis did the repair while the coffee brewed. He left the remaining length on the dashboard, coiled like a small black snake.

Elijah put the repair card for controller number forty in the folder. Curtis's hose went in the glove box.

---

## The Foundations

## The controller isn't dinner

The neighborhood factory earns its name when somebody can keep doing useful work because it exists. A repairable controller can help a grower. A workshop can shorten a repair. A local crew can know which part fails during the season when nobody has a spare afternoon.

But food first means following the benefit past the machine. Growing, harvesting, handling, storage, cooking where needed, and delivery all stand between a controlled valve and a person's meal. Somebody has to organize that chain, and somebody has to be able to use what arrives.

Rosa could not turn a bag of potatoes into dinner with one working hand. The crop was fine. The offer was wrong. That distinction belongs in any serious account of abundance: how much exists and what a person can obtain are different questions.

We can bring local skill into a wider system. A dense city doesn't need to grow every calorie inside its boundary. A rural workshop doesn't need to manufacture every part it uses. Farms, towns, kitchens, transport providers, and public institutions can share responsibility across a region. The useful question is which connections make provision stronger and which leave a person dependent on one failing link.

The chapter's title names a pressure toward bringing some work closer. It isn't a command to sever trade. Food-first cooperation has room for a neighbor's repair bench and a shipment from a different climate.

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

## What would make the machine worth it?

Compare the complete arrangement with the garden's ordinary method. The controller might reduce water checks while adding maintenance. It might make an awkward task accessible to someone who couldn't previously do it. It might save a paid worker time that the organization then fills with more work. Those are different outcomes. Ask the worker which one happened.

A simple timer or another paid shift may be the better purchase. If a robot is useful, you should be able to explain what became easier, safer, more reliable, or less resource-intensive. Enthusiasm is a reason to investigate. A result is a reason to keep going.

The question about the gain comes next. Does it lower a selling price? Improve working conditions? Fund additional free deliveries? Increase a private return? A machine doesn't select among those uses. They are decisions about the organization around it.

For the illustrative project, the partner could agree in advance that any verified saving first supports completing the five promised deliveries and compensating the remaining work. That would be a small, explicit connection between technical improvement and access. Without such an arrangement, the saving might never reach a recipient at all.

## From a garden to a food service

Five households receiving vegetables is a contribution. A dependable baseline needs a broader food supply, suitable preparation, routes people can use, and the means to continue through a failed crop or a broken vehicle. It also needs a place for someone who wasn't among the first five households.

The next meeting therefore belongs as much to food providers and recipients as to the people holding the tools. A grower knows the seasonal limits. A kitchen knows what can be prepared. A driver knows where the mapped route becomes an impossible delivery. A resident knows that a collection window can be inaccessible even when the food is free.

Put those facts beside the equipment record. The expanded proposal should name the additional food, paid and voluntary work, transport, operating money, and service commitments it requires. Ask existing institutions which part they can support and on what terms. A public purchase from growers, a cooperative food service, and a partnership with an existing kitchen are possible arrangements; none is funded simply by being named.

Start small enough to learn, while keeping the destination large enough to matter. Nobody should have to wait for a perfect robot before being fed. Nor should a successful demonstration let us forget the person still waiting outside the service area.

---

## Precedent P-12: The Networks Behind the Bronze (Eastern Mediterranean, fourteenth to twelfth centuries BC)

Late Bronze Age societies around the eastern Mediterranean depended on trade, including the movement of materials used to make bronze. Several societies experienced severe disruption around the end of that period.

To make the network tangible, go back earlier, to a ship that sank off what is now Turkey in the fourteenth century BC. Archaeologists excavating the Uluburun wreck recovered copper and tin ingots, glass, ivory, jewelry, pottery, and stone anchors. Some of the copper had been cast into the broad, four-cornered shapes archaeologists call oxhide ingots. Here is a supply chain you can point to: material intended for transformation elsewhere, carried together in a vessel whose journey ended. [Institute of Nautical Archaeology, Uluburun excavation](https://nauticalarch.org/projects/uluburun-late-bronze-age-shipwreck-excavation/)

The cargo carried copper and tin in approximately the proportions used to make bronze. The institute describes an elite shipment, with luxury goods for wealthy recipients alongside raw materials. Its contents show that long connections could assemble extraordinary resources. They don't show that everyone living near a destination could obtain those resources. The difference between a rich network and a secure household was already a question worth asking. [Institute of Nautical Archaeology, cargo and interpretation](https://nauticalarch.org/projects/uluburun-late-bronze-age-shipwreck-excavation/)

Uluburun sank well before the disruptions conventionally gathered around 1200 BC. Its cargo gives us something concrete to ask about when considering that later period: which materials had to arrive, who could arrange their passage, and what could continue if they didn't? The later crisis involved different places and times; there was no single date on which the Mediterranean switched off. [Knapp and Manning, Crisis in Context](https://doi.org/10.3764/aja.120.1.0099)

Researchers examine interacting pressures rather than one universal switch: climate, conflict, migration, political organization, and interrupted exchange. Places did not all experience the same collapse or recovery. The example invites an investigation of dependencies; it cannot prove that local production always survives or that every large network fails.

The controller in Marta's shed carries its own map of connections: probes, boards, terminals, the supplier's stock, the person who knows the fault. Moving assembly into the neighborhood doesn't erase that map. It gives the neighborhood a chance to understand more of it and change the connections it can. Keep the exchange that brings something useful. Build the capacity to repair, substitute, and keep feeding people when one route fails. A workshop's strength is measured partly by the relationships it can keep working.

**The mechanism.** Interdependence can transmit disruption. Different communities also have different resources and capacity to adapt; neither localism nor centralization guarantees survival.

**The rule.** Name the dependency and the disruption you are preparing for.

**The practice.**

1. Map one input to your food project.
2. Confirm a realistic alternative with its provider.
3. Record what would remain unavailable during an interruption.

---

