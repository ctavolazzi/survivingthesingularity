# Chapter 17: Tools of the Trade

![Workbench with hand tools](/book-images/ch17-workbench.jpg)

*The workbench. Own the tools, own the output. (Shixart1985, CC BY 2.0, via Wikimedia Commons)*



> *"We are as gods and might as well get used to it."*
> Stewart Brand, *Whole Earth Catalog* (1968)

**In this chapter:**

- The tools that survive the transition are the ones you can understand, fix, and run with no cloud, no subscription, and no permission.
- Networks fail at the node somebody flashed in a hurry. Discipline you skip in fair weather collects its debt in the storm.
- Debugging in the dark is a solved problem: halve it. Power or brain, this side or that side, measure, cut again.
- Give the machines a worthwhile assignment: food first, then cleanup, shelter, and care. The proof is already on people's workbenches.

---

The first hard storm of the winter came up the valley on a Friday afternoon with the barometer falling like a dropped tool, and by dark the county was gone. Grid power went first, a whole hillside of windows going out between one gust and the next. The cell towers lasted forty minutes longer on their batteries and then they went too, and the valley was back in 1890, except for nineteen households, where it was still Tuesday. Somebody brought the printed contact list to the shop table. Somebody else started the soup.

The mesh held. That's the sentence Elijah had been building toward for a year, the LoRa lattice laid node by node across the ridgelines, and on the night it finally mattered it did what it was designed to do: shrugged. The co-op's map stayed lit, house to house, short messages hopping the valley on watts you could count on your fingers. Marta's shop stayed lit. The greenhouse alarms stayed armed. The whole nervous system he'd been laying into walls and fence posts for a year kept right on reporting, calm as a pulse.

Except node 7.

Node 7 was the ridge repeater, the high hop that stitched the north houses into everyone else, and node 7 was his, personally, in every sense that stung: his design, his install, and, the previous Sunday, his firmware flash, done alone, in a hurry, ahead of the weather, without a second set of eyes, because it was "just a repeater" and the checklist law was for things that touched the open internet, and he had let himself believe that discipline was a perimeter instead of a practice. The storm found the ridge at eight o'clock. At 8:04 the map showed a hole where the north houses used to be.

The north houses checked in on the voice radios, one by one. Everyone was fine. The hole was only in the map. But the hole was his.

He suited up. Nobody climbs the ridge alone, and Curtis was already lacing his boots, which at the co-op amounted to a verdict. Marta handed Elijah the handheld radio and the small pack, pointed at his headlamp, and said the thing she always said instead of luck: "Talk before you touch."

The ridge trail in a storm is a different country. Rain going sideways with gravel in it, madrone trunks slick as wet brick, the wind doing shift work: lean, release, lean. He climbed with the multimeter zipped inside his coat to keep the display warm, Curtis's light steady behind him, and the radio crackled at his collarbone every quarter mile, Marta running the net from the shop the way she'd once run a floor: short transmissions, no chatter, callsigns and traffic.

And he could hear, in the gaps, the system working around the hole he'd made. Priya's greenhouse, riding the alert chain: low-temp alarm at 8:40, relayed around the dead ridge the long way, south through Frank's node, and Denny's voice acknowledging, hauling the backup battery to keep the winter starts alive, all of it happening without him, around him, because the network's whole design assumed any one node, any one person, could be the one that failed. It is a strange, strong medicine, hearing a thing you built survive you.

Node 7's enclosure was where he'd bolted it, on the old fire-lookout stub, and the node was dark. Curtis held a garbage bag over them for a rain fly while Elijah got the lid off, fingers going stupid with cold, and keyed the radio, and he and Marta debugged it across two miles of storm, Marta asking the only question she ever asked:

"Power or brain? Halve it."

Battery voltage: 12.9, healthy. Power. Halved. "Downstream. Check the buck converter under load." Five point one volts, solid. Halved again. So: brain. The radio module's status light was flashing a pattern he'd never bothered to memorize, and Marta made him count it out loud, four short one long, and there it was, in the dark, at the exact intersection of wind and shame: bootloader error. Wrong image. He had flashed the 868-megahertz build onto a 915-megahertz board, Sunday, alone, confident, and the node had run on the old code in memory all week and died the first time the storm's brownout forced a reboot. The vise, the shovel, and now the ridge: the same exam, a third time, in worse weather.

The fix took eleven minutes because he had, at least, packed like Marta taught: the SD card with the known-good image, hashes checked, lived in a film canister in the pack's top pocket, next to the spare fuses. Reflash, reboot, and the status light went to its slow steady breathing, and in his collar the radio said, in Priya's voice, "North houses just came back. Hello, ridge." Below them the whole county was black to the horizon, and across that blackness the co-op's houses held their small stubborn constellation, and node 7 was a star in it again instead of a hole.

He stood up into the wind to pack the tools, and Marta's voice came up the hill one more time, dry as the inside of the enclosure was supposed to be. "Brand's line. On the shop wall. 'We are as gods and might as well get used to it.' He changed it, later. Get *good* at it." A crackle, wind on her end too, the shop door open to the weather. "Gods, hell. Gods is the easy part, college. Gods with cold fingers and a multimeter, that's the job. Getting good at it means next time you flash a node, somebody's watching. Come down. There's soup."

They came down. There was soup. And the checklist got its amendment that Sunday, in Reuben's careful language: the two-eyes rule now covered everything people depended on, with a recorded recovery check, because the network doesn't care whether the packet that kills it came from the internet or from your own confident thumb. The storm blew out by noon Saturday. The county's power was back Tuesday. The co-op barely noticed, except as traffic on a mesh that had already moved on to arguing about seed orders. Curtis asked who still needed soup taken over.

---

## The Foundations

We live in a golden age of high-tech dependency.

Your refrigerator may have more computing power than the Apollo guidance computer. It can track your milk, reorder groceries, and show recipes on a touchscreen. It can also stop working properly when the manufacturer's cloud has a bad day, nag you about a subscription, and report more about your household than you'd ever tell a stranger. Call it the smart-home trap: every door, thermostat, bulb, and tool quietly depending on a server somebody else owns.

The alternative is simple to say: **tools you own.** Repairable, documented, able to run without an internet connection, and understandable by the person using them. If you can't understand how it works, can't fix it with ordinary tools, and can't run it offline, it's less a tool than a leash.

![A pixel-art specimen board of the field kit: a photobioreactor, a vertical grow tower, a LoRa mesh node, a solar-and-battery rig, a 3D printer, a CNC plasma table, a walk-behind tractor, and a cyberdeck](/book-images/ch17-field-kit.png)

*The field kit. Every one of these already exists, and a person with modest money and stubbornness can get their hands on most of it.*

## Give the machines a worthwhile assignment

Imagine the priorities written above the workbench: feed people, restore damaged places, make safe homes, relieve suffering. Those are assignments worthy of a powerful technology. They are also a way to judge the uses of it that actually receive our money and attention.

Food comes first in this book because nobody needs an elaborate explanation of why dinner matters. The wider ambition includes land care, waste cleanup, housing, and health. These projects can proceed together. Somebody who needs treatment or shelter should not have to wait for the last food problem on Earth to be solved.

The question for any proposed machine is what useful work it can do under the conditions where people need it. Compare the tools they can obtain and support. A machine impressive in a video may be hard to repair locally. A familiar tool may do the job well. Shared access can matter more than ownership.

## The proof isn't hypothetical

Everything in this chapter already exists, and you can watch people build it this weekend. This is the part the doom crowd never accounts for: while the comment sections argue about whether the machine ends the world, a growing number of people are pointing the same technology at their own food and posting the plans.

One of them, working under the handle SECTOR 07, wanted his home aquaponics loop to stop depending on a store. The system grows fish and vegetables together, but it still needed bought fish food, so the loop was never closed. His fix was to grow the food too: microalgae, cultivated the way labs do it, in a machine called a photobioreactor. Commercial units are priced for research budgets. He printed his on a Bambu A1, a 3D printer that costs less than a used laptop, and ran it on a Raspberry Pi and two Arduinos, with sensors he made himself out of magnets. It grows about eight grams of algae a week. He says plainly in his own build log that it isn't finished: features he isn't using, automation he never completed, a design he'd rework for a second version. That honesty is the point. This isn't a product launch. It's a person learning in public. [SECTOR 07, I 3D Printed a Photobioreactor](https://www.youtube.com/watch?v=SLckTj_tJg4)

![A DIY 3D-printed photobioreactor: a clear vessel of bright green algae culture on a printed frame with a Raspberry Pi board and status light](/book-images/ch17-photobioreactor.png)

*Tens of thousands of dollars in a lab. A few hundred on a workbench.*

![The closed algae fish-food loop drawn as a cycle: fish tank to grow beds to dry-and-grind to photobioreactor and back to the fish as home-made food](/book-images/ch17-algae-loop.svg)

*Grow the fish food too, and one more store-bought input drops out.*

Or take the one-man operation behind EasyGrow, run out of a garage. He designs recirculating vertical grow towers that, by his account, pack about eight times the plants into the same footprint and use about ninety percent less water. When off-grid customers told him his pumps needed power they didn't have, he taught himself to build wind systems, hand-winding axial-flux alternators, and rural antennas so greenhouses could report their own status. By his account his towers feed a stadium in Florida and lettuce gardens in Nigeria, and his wind systems turn in Buenos Aires. Ask him why he won't build pots cheap enough to need replacing, and he'll tell you: "I'm not in business to get rich. I'm in business to grow food and help people grow food." [Kirsten Dirksen, Mad scientist's homestead](https://www.youtube.com/watch?v=QSnHShly5R0)

Now hold that next to the other version of the very same technology. Some industrial vertical-farm vendors sell nearly identical hardware with the opposite pitch: their promotional material brags that the system reduces labor costs and decreases human touch. Same sensors, same pumps, same automation. One spirit builds the tool to take people out of the loop. The other builds it to put a scared, capable person back in charge of feeding their family, and gives away the plans. The tools don't choose which future they serve. People do.

## The nervous system: mesh nodes

Chapter 14 made the case for a neighborhood mesh. Here's the hardware. A typical node is a small, cheap board that pairs a microcontroller with a LoRa radio (the Heltec V3 and LilyGO T-Beam are popular), running the open-source Meshtastic firmware.

![Anatomy of a hyper-local mesh node: a waterproof Pelican case containing a 5-watt solar panel feeding two salvaged 18650 batteries feeding an ESP32 LoRa chip, with a tuned antenna broadcasting to the next node on 915 or 868 MHz](/book-images/ch17-lora-node.svg)

*A mesh node. Sunlight in, short encrypted messages out.*

- **Tiny power draw.** A node sips a fraction of a watt most of the time. A small panel and a battery can keep it going through a lot of weather.
- **License-free bands.** In North America these radios use the 915 MHz band; in Europe, 868 MHz. Use the build for your region, which is, as Elijah learned, not a small detail.
- **Self-organizing.** Nodes running Meshtastic find each other and relay messages automatically, with encryption.

To put one up: use a weatherproof box, a proper solar charge board and battery rated for outdoor use (buy it assembled if you're not sure), and the best antenna you can mount high. Height and line of sight matter more than anything else; a well-placed node can reach many miles. Then check what it can actually carry before anybody depends on it.

## The muscle: power you understand

Most of what a small workshop or a mesh network runs is natively low-voltage DC: LED lights, phone and laptop chargers, radios, small pumps. A conventional off-grid system turns the panels' DC into household AC with an inverter, and then every device's power brick turns it back into DC. Each conversion wastes some energy as heat, often ten percent or more.

![The inverter trap versus the DC-native protocol: the conventional chain loses 10 to 15 percent converting DC to AC and again converting back to DC at the wall brick, while the DC-native chain runs solar to battery to fuse block to devices with zero conversion loss](/book-images/ch17-dc-native.svg)

*The round-trip toll. When a load already wants DC, the inverter chain charges you twice to deliver it.*

So for small loads, a DC-native setup, panel to charge controller to battery to a fused distribution block to 12-volt devices, can be simpler and more efficient. Batteries store a lot of energy and can fail dangerously if they're built or charged wrong, so use a packaged battery with a proper management system, fuse everything, and have someone who knows electrical work check it. And be realistic about lifespans: a good lead-acid battery in daily use lasts years, not decades; lithium lasts longer but costs more up front.

## The skeleton: machines that make machines

Eventually something breaks: a gear, a bracket, a bolt. If every replacement part has to come from a distant distributor, you're still waiting on permission.

![The Neighborhood Fab Lab: recycled raw materials feed three open-source machine cores, a RepRap 3D printer, a CNC plasma router, and an open-source tractor, producing custom parts, structural steel, and field power](/book-images/ch17-fab-lab.svg)

*The neighborhood fab lab. Broken means fabricate, not wait.*

The Open Source Ecology project's Global Village Construction Set documents open designs for dozens of the industrial machines a small community might need, tractors, presses, printers, and more. Three good starting points for any neighborhood shop:

1. **A 3D printer.** Open, repairable designs like the RepRap family, some of whose parts can be printed by another RepRap, are ideal. Plenty of people start, like SECTOR 07, on an inexpensive consumer machine; just know which parts you can fix and which you'll have to buy. People have turned discarded PET bottles into recycled filament, usually called rPET, with small homemade extruders, which turns trash into brackets, gears, and replacement knobs.
2. **A walk-behind tractor.** A heavy two-wheel tractor with swappable implements, like the BCS style, can mow, till, chip, pump, and generate, for a fraction of the fuel and complexity of a four-wheeled one. Share one among several households.
3. **A cutting and welding station.** A CNC plasma table and a good welder turn steel stock into brackets, racks, and repairs, in the hands of someone trained like Marta.

## Food: count the whole job

Begin with Chapter 9's chain. Name the repetitive task, the current method, and the result at the recipient's end. Count setup, supervision, maintenance, transport, and the work people still do. Don't turn a machine that saves one motion into a claim that a whole job disappeared. Equipment needs power, spare parts, and an operator's time; count those too.

## Cleanup: from litter to its destination

Here's a small cleanup job, done with permission at a suitable site. Find the litter. Collect what the local service will take. Get it into that service's stream, not just out of the photo. Come back later and check whether it stayed clean. Moving trash from one place to someone else's backyard isn't success.

A future cleanup robot might do part of that chain. To tell whether it helps, compare the whole arrangement with an existing crew, better bins, or a trash trap in a creek, and count the machine's maintenance and recovery. "Won't people just litter more?" Maybe. Maybe they'll take better care of a cleaner place. Neither is a measured result, so build in prevention and easier disposal, and look again. Trash reaches water by the wind, runoff, and spills as well as dumping, so the litter itself rarely tells you who's to blame. [EPA, Learn About Aquatic Trash](https://www.epa.gov/trash-free-waters/learn-about-aquatic-trash)

Toxic waste is a much bigger assignment, and it belongs to properly equipped specialists. The ambition is worth keeping: machines can take dangerous work off people's bodies. Remotely operated robots are already doing inspection and cleanup work in hazardous areas at the Sellafield nuclear site in Britain. [Sellafield Ltd, Spot robot deployment](https://www.gov.uk/government/news/sellafield-robotics-using-spot-more-for-spotless-nuclear-clean-up) But identifying, containing, and disposing of dangerous material is a job for trained people with the right equipment. Unknown material is never a neighborhood experiment.

## Help that reaches a body

Health belongs in the same larger ambition. We want less pain, earlier help, better treatment, and more room to live. A machine that advances a laboratory task, a tool that assists a clinician, and an aid that helps someone move through a day are different possibilities. Each needs evidence about the benefit it claims. An encouraging research result isn't yet a treatment someone can depend on.

The access question remains after the technical achievement. If useful care exists but a person can't obtain it, the work of making that advance serve humanity is unfinished. A person should not have to wish the invention had never happened because they fear what its business model will do to them.

This is what I want optimism to demand of us. Use capability to relieve the burdens people already carry. Evaluate the machine honestly. Arrange access deliberately. Keep people able to question what is being done to them and for them. A society can choose those purposes, then do the practical work required to make them real.

This week, inventory tools with the people doing one existing food or cleanup task. Record what is available, who can use it, what requires training, and who maintains it. The tool library starts with accurate information, not a shopping spree.

---

## Build your first node

Autonomy isn't an idea. It's calluses.

1. **Get a Meshtastic board.** Buy a Heltec V3 or LilyGO T-Beam for your region's band. Flash Meshtastic from your web browser, pair it with your phone, and find the other nodes near you.
2. **Build a small DC corner.** A packaged 12-volt battery or power station, a fused distribution block, a few 12-volt LED lights, and a USB charger. Keep a phone and a radio alive through the next outage.
3. **Learn to solder.** A basic soldering iron and an afternoon of practice on scrap wire. Learn a clean, strong splice. The wise ones are learning how to solder.
4. **Inventory the tools.** With the people doing one food or cleanup job near you, write down what tools exist, who can use them, what needs training, and who maintains them. The tool library starts with an accurate list, not a shopping spree.

Build for the long haul.

---

## Precedent P-21: Access to Tools (Menlo Park, 1968)

In 1968 Stewart Brand put NASA's photograph of the whole Earth on a big black paperback cover and printed three words under the title: **Access to Tools.** [Whole Earth Catalog, Fall 1968](https://wholeearth.info/p/whole-earth-catalog-fall-1968)

The *Whole Earth Catalog* listed books on dome building, organic gardening, beekeeping, and cybernetics, along with tool suppliers and a desktop calculator: anything that helped an individual, in Brand's words, conduct his own education, find his own inspiration, and shape his own environment. Each entry was a review with a price and where to get it, what the catalog's own statement of purpose called an evaluation and access device. It refused to separate the homestead from the computer; its readers carried strands of both the back-to-the-land movement and personal computing. Steve Jobs, closing his 2005 Stanford commencement address, called it "sort of like Google in paperback form, 35 years before Google came along," and gave the graduates its sign-off as his own final advice: stay hungry, stay foolish. [Stanford Report](https://news.stanford.edu/stories/2005/06/youve-got-find-love-jobs-says)

Its rules for what got in were stricter than a list of things the editor liked. An item had to be useful, help with independent education, be high quality or low cost, not already be common knowledge, and be available by mail. And the catalog promised to keep revising itself from what its readers and staff learned. [Whole Earth Catalog, 1968 purpose and function pages](https://eastofborneo.org/wp-content/uploads/2016/08/Whole_Earth_1968_sample.pdf) It wasn't above commerce, either: the Menlo Park office shared a storefront with the affiliated Truck Store, which sold some of what the catalog listed, and supplements printed readers' corrections and suggestions for the next edition. [Museum of Modern Art, Access to Tools](https://www.moma.org/interactives/exhibitions/2011/AccesstoTools/) Decades later, an anniversary reprint had to warn that the old addresses and prices were long out of date. Time had worn down the *access* half of Access to Tools, even where the idea still held.

**The mechanism.** A catalog of tools is secretly a map of possible selves. People don't become capable by being credentialed. They become capable by getting access, and then getting started. Curation was the product; the tools already existed, scattered and invisible. And access, unlike the idea, has to be maintained.

**The rule.** Build a useful toolset, not a collection of promises: something you understand, can repair, and can't be locked out of.

**The practice.**

1. Write your own one-page catalog tonight: every tool you own that you actually understand, can repair, and can't be remotely disabled or locked out of. Be strict. The page will be shorter than you expect. The gaps aren't a judgment. They're your curriculum, in priority order.
2. Close one gap a month. Either learn an owned tool down to the repair level (take it apart, find its manual, buy its spare parts) or replace one rented capability with an owned one. Twelve months of this and your catalog is a different document, and so are you.
3. Be somebody's access. Brand's genius wasn't owning tools; it was cataloging them for people who didn't know where to start. Publish your list, lend your tools with a signature and a return date, or run one workshop for your street. And keep the list current: a recommendation with a dead address is just a memory.

---
