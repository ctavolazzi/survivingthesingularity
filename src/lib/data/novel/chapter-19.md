# Chapter 19: Ugly Is a Maintenance Feature

The co-op's first real manufacturing run was forty greenhouse controllers.

The order came in January, through a friend of a friend of Priya's, from the CSA network two valleys over. Forty small boxes that could read soil moisture and air temperature and open a vent or a valve without asking a server in Virginia for permission. Real money, a real deadline, real customers with seedlings on the line. Elijah volunteered for the design. He had spent the fall sweeping and learning the shop, and here at last was something he was actually trained to do.

The four months on the yellow ticket ran out on a Tuesday in February. He was under a sink at the time. He didn't find out until Thursday.

He designed a beautiful thing. A custom four-layer board, an elegant little brain on a module, sensors from a Swiss outfit whose datasheets read like poetry, the whole thing sealed in resin, sleek as a river stone, no user-serviceable parts inside. He presented it to the shop on a Tuesday with renders. Renders.

Marta looked at the renders for a while.

"Walk me through the bill of materials," she said. So he did, and she wrote three numbers on the whiteboard while he talked. 11, 1, 0.

"Eleven weeks," she said, tapping the first one, "is the lead time on that Swiss sensor. I just looked it up. That's the quoted lead time, which means it's a prayer. One," the second number, "is how many suppliers make that module, which means the day they quit making it, all forty of these are bricks, and we're the ones who sold bricks to farmers. And zero," she tapped the last, "is how many people in this valley can fix a board sealed in resin when it fails during frost week. Including you, college." She capped the marker. "It's a gorgeous design. It's a Claypot design. Design it again. Parts from the drawer, parts from the hardware store, and nothing your neighbor can't fix with the tools he already owns."

"That'll be uglier," Elijah said.

"It'll be ours," Marta said. "Ugly is a maintenance feature. Ugly means the next guy can see how it works."

So he designed it again. The second version was a Raspberry Pi the regional supplier had in stock, screw terminals instead of poetry, and four-dollar probes you could swap by hand. Every unit had a laminated one-page repair card zip-tied inside the lid, because Marta's rule was that documentation you have to go find is documentation that doesn't exist.

![The controller. Screw terminals instead of poetry.](/images/novel/figure-09.webp)

<em>The controller. Screw terminals instead of poetry.</em>

The cases came from a kid named Tyler.

Tyler worked the register at Kowalski's Hardware in town, where Elijah had bought the screw terminals, forty at a time, until Tyler asked what they were for. He was nineteen. He had a mustache he was still negotiating with and a 3D printer in his bedroom, and the next Saturday he drove out with a milk crate of forty cases, printed in plastic the color of a school bus. Nobody had asked him to. Marta turned one over in her hands and said "Huh," which from her was a parade.

* * *

The build took the shed three weekends. On the first one, everybody was in a line, deburring cases and crimping wire ends, when the door opened and let in the cold. A lean man in a good coat came in with it. He looked too pleased with himself for a Saturday.

"Reuben Vance," Marta said, not looking up from the crimper. "The part of the machine that runs on paper."

![Reuben Vance. Handles the part of the machine that runs on paper.](/images/novel/figure-10.webp)

<em>Reuben Vance. Handles the part of the machine that runs on paper.</em>

"I heard," Reuben said, pulling a folding chair toward the heater, "that this operation is about to sell manufactured electrical goods across county lines." He said it the way other men say <em>rob a train.</em> He produced a folder. "So I made a list."

He laid three sheets beside the crimper. A seller registration, filed. A tax question, answered. A letter from the county about the shed, with a yellow tab on it.

"I thought agricultural equipment meant we were covered," Elijah said.

"You thought a noun was a permit. Happens all the time." Reuben tapped the yellow tab. "This stays open until somebody with authority answers the actual question."

Elijah looked at the folder, then at Marta. "Did we ask him to do this?"

"Nobody asks Reuben," Priya said, from the crimping line. "Reuben notices."

* * *

The second weekend, Grace brought a visitor.

Her name was Patricia. She was the policy director for the CSA network, which made her the customer, and she had driven over in a small electric car to see what forty of her growers were buying. She was in her forties, in a fleece vest, and she kept her phone face down on the bench beside her the whole time. Grace walked her down the line with a hand on her arm, introducing everybody. Grace was proud of them. You could see it.

Tyler was on an upturned bucket at the end, with a laptop covered in stickers on his knee. He was the firmware. Elijah had blocked out two weeks to write it. Tyler had shown up on Thursday with it done.

They ran a unit on the bench for her. The test was a space heater and a cup of wet dirt. Tyler pointed the heater at the box, and at eighty-five degrees the little vent motor woke up and turned. He pulled the probe out of the cup and the valve clicked open. He put it back and the valve clicked shut. He did it without looking up from the screen.

Patricia was delighted. She actually clapped, once.

"How on earth did you do this?"

"I used Rod Code."

Immediately the vibe shifted. You could cut the tension with a spork.

"You…used AI to make this?" Patricia said, disgust oozing out of her words like molasses.

"I mean, yeah. Why wouldn't I?"

"Um, maybe because AI is killing the planet?"

The crimpers stopped. Tyler finally looked up. He honestly didn't seem to know he was in a fight yet.

"It's forty boxes that water tomatoes."

"It's a data center in the desert drinking a river so you could skip learning to code. There are studies. I can send you the studies. And how many companies make Rod Code?"

Nobody answered. It was one. It was PorusAI.

"And how many people in this shed can read what it wrote?"

"I can," Tyler said. "I read all of it. Most of it. It passed the bench, you just watched it. There's a card in every lid that says how to fix it. And I mean, your growers can't pay a programmer. They can't pay <em>me,</em> I did it for free." His voice cracked on <em>free,</em> and he went red, and kept going. "It's a tool. It's just a tool. You drove here in a computer."

"Can we pause?" Grace said. She had both hands up, palms out, the warm voice turned all the way on. "Can we just pause, and check in? I'm hearing a lot of…"

Nobody paused.

They were both right. That was Elijah's problem. He had a power bill for $211.46 in a box somewhere. He knew what the thing drank. He also knew a nineteen-year-old had just done in a night what would have taken him two weeks, and that the boxes worked, and that forty growers would get them for a price they could pay. He had helped build one of these machines. He had shown one off in a bar, and three people lost their jobs. He could have said any of it. He stood there with a case in one hand and a deburring tool in the other and didn't say a word, and both of them noticed.

Marta hadn't said anything either. She was looking at Tyler and at the laptop on his knee. Something had gone out of her face. She had the crimper in her hand and she wasn't using it.

"We'll see," she said, to nobody, and went back to work.

Patricia left before lunch. She shook everyone's hand. Grace walked her to the car, talking low, and came back alone and went straight to the kitchen trailer without looking at anybody.

Elijah found Tyler outside afterward, sitting on the trunk of a Corolla, flashing units one after another.

"I showed some realtors once," Elijah said.

"Okay," Tyler said.

He didn't ask what happened. He was nineteen and he had twenty-six boxes left.

* * *

The forty units shipped in February. An electrician the CSA hired looked over the install plan, and two growers ran the first boxes for a week and sent back notes in pencil, and Elijah fixed what they found before the rest went out. By then Reuben's yellow tab had an answer stapled to it and the folder was thick enough to prop a door.

Denny delivered them in apple boxes. Two growers needed new probes in the first month. They changed them by hand, off the card, without throwing anything away. Marta pinned the repair emails to the corkboard the way other shops hang their first dollar.

And somewhere in the middle of all that, somebody finally fixed Elijah's check-engine light.

It had been on since the drive north. A dealership had quoted him twelve hundred dollars and a week. Curtis found it in nine minutes with a fourteen-dollar gadget plugged in under the dash. A cracked vacuum line. Two dollars of hose. He did the repair while the coffee brewed, and left the rest of the hose on the dashboard.

Elijah put the hose in the glove box.
