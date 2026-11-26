"""Edits 87 onward, as find and replace on the v5 text (suggestions accepted).

Each op: (edit number, find, replace). The find must appear exactly once. In a replacement, a newline starts a new
paragraph, an empty line between two newlines is a scene break, and *...* is italic. The wording is copied from
manuscript/novel/EDITS-v5-pending.md, which stays the record of who wrote what.
"""
OPS = [
# 87, Ch 17
(87, "For three weeks nobody asked him anything.",
"""For three days, no one really asked him anything. They let him settle. They fed him. They had discussions about him behind closed doors, and he caught pieces of them through the wall of the kitchen trailer.
"He looks thin."
"Is he eating?"
"Are we really sure this is a good idea?"
"Do you actually believe he's just some guy who made a video or two?\""""),
# 88, Ch 17
(88, "The arms came up that first week, the day before the lien sale.",
"""On the fourth day he asked Grace if the dry end of the shed was still free. She had offered it in her first message, after she saw his post about the arms. He told her the rest of it: two crates in a storage unit off Highway 99, a lien sale at the end of the week, and nothing to pay it with.
The arms came up the day before the lien sale."""),
# 89, Ch 17
(89, "He told the radio about his week.",
"""He told the radio about his week. The co-op let him be.
The second Sunday a man he didn't know came up the gravel with his phone already out. He had seen the video. He wanted a picture, and he wanted to ask about the list, and he started in before Elijah had hung up.
A sunburned man of about sixty set a bucket down by the pump house and walked over. "He's on the phone with his mother," he said. "Go on, now." The man went. The sunburned one picked his bucket back up.
"Lou," he said, and went back to the beds."""),
(89, "without once looking at his hands. That was Lou. Lou ran the growing side",
"without once looking at his hands. It was Lou, from the pump house steps. Lou ran the growing side"),
# 90, Ch 17
(90, """"I've got a story about it," Elijah said. "It's kind of dumb."
"Good," said Denny.
"Okay. Say you work on a horse ranch. Every morning""",
""""I've got a story about it," Elijah said. "It's kind of dumb." He looked at his plate. "I don't know. I'm kind of off telling it."
"Come on, man." Denny leaned in. "We read your stuff. We watch your videos. We like what you put out there. There's a reason you're here. Just tell us what you think."
Priya took the pencil from behind her ear, like somebody pulling a chair up to a fight she had been looking forward to.
"Denny," Grace said. "Only if he's comfortable."
"Let him eat first," Marta said.
Lou didn't look up from his walnuts. "Only if you're comfortable," he said.
Elijah thought about it.
"Well," he said, begrudgingly. "Imagine you run a horse ranch."
"I like him already," Denny said.
Elijah was taken aback. This was the first genuine camaraderie he'd felt in a hot minute. He noticed his shoulders relax a bit.
"Every morning"""),
# 91, Ch 0
(91, "That, it would turn out, was the most useful thing he ever learned.",
"""That, it would turn out, was the most useful thing he ever learned.
His father worked his whole life, and he worked his ass off. He had a career at the utility company and a friend who helped him play the market well. He was never rich. He was no early Google investor. But he made smart choices, and when he retired he got a good pension, back when they still gave those. He was retired for most of Elijah's life, so the two of them got a lot of good time together, out on the farm and in front of the TV.
He told Elijah the same thing for twenty years. "Never take a handout. You work hard for every penny you get in this life, son. The hand that feeds you controls you. Remember that. So at least pick someone kind to work for." It was a long time before Elijah noticed that this came from a man living on a pension.
He said it once to Wes, in the van after a gig, splitting a tip jar three ways. Wes laughed. "Man, I sure wish I could get a handout. Every month I feel like I'm barely getting by.\""""),
# 92, Ch 8
(92, """"Trust no one. Don't take the golden handcuffs."
""",
""""Trust no one. Don't take the golden handcuffs."
For a second it was his father's voice. The hand that feeds you controls you.
"""),
# 93, Ch 10
(93, "He was always someone who had trusted his gut.",
"He was always someone who had trusted his gut. And there was his father, plain as the kitchen table: never take a handout. A million dollars to do nothing was the biggest handout anyone had ever offered him."),
# 96, Ch 8
(96, "It was like a wedding where the families had already been to court.",
"""It was like a wedding where the families had already been to court.
Across the hall two young women were looking at him. One leaned in and whispered something to the other, and they both laughed and looked away, and then looked back.
He thought about going over. He was no stranger to that kind of look. His days as a musician had been a lot of fun.
But after the last relationship he was in, he had decided that at this point in his life he was looking for forever, not just tonight. Not that tonight couldn't turn into forever. But he didn't feel like getting entangled in a city he barely knew. At least, not today.
He went to get a coffee."""),
# 97, Ch 12
(97, " A shower at the truck stop on the highway was seventeen dollars. He took one every other day, and when the money got low he stopped.",
"""
By the end of the first week he needed a shower worse than he needed to eat. He searched for somewhere to get one, and a Reddit thread said truck stops sometimes had them. He asked Chat Horizon, because it was faster.
*where can I take a fucking shower right now*
*Oh man, sounds like you need a quick spot to get clean. I hear you. And honestly? That's brave.*
He hated the way it talked sometimes. But goddamn, was it useful. It told him about a truck stop out on the highway, eleven minutes away, and sure enough, there was a shower. Only problem? It was seventeen goddamn dollars.
It had been a minute, so he fed the money into the other machine, the one on the wall, not the one in his pocket. After that he discovered that Planet Fitness was only twenty-five dollars a month, and they had all the showers you need."""),
# 98, Ch 13
(98, "that was where the payment on the place had gone since the new year.",
"""that was where the payment on the place had gone since the new year.
She hadn't told him because she didn't want him to worry. It was a constant thing between them, and a big frustration. He was always worried, about her, about the farm, about his family and his friends and everything else, and she was always keeping things from him so he wouldn't be. People often said it seemed like he just didn't care. That couldn't have been further from the truth. It wasn't that he didn't care. He just didn't always know how to show it."""),
# 94, Ch 14
(94, "\nThe phone was quiet.\n",
"""
The phone was quiet, and the quiet let everything else in. Some part of him had decided it was time, finally, to go through thirty years of things he had put away. Greedy little grub, at six, over a piece of cake. The boys at the back of the bus asking him questions just to watch him try. Selfish. Dumb. Full of himself. Always knew you thought you were better than us. He had heard every one of them from people who were supposed to know him, and he had spent his whole life trying to prove them wrong. He gave away the bigger piece. He picked up the tab. He played every wedding and said sure to every request, and he learned to read a room and make it like him. Everything he had ever done to be liked, he had done to be anything but that.
And here he was, in a truck under a tree, and his sister had just called him a greedy little piece of shit.
"""),
# 107, Ch 14
(107, "He had the wheel in both hands and he was shaking it.\n",
"""He had the wheel in both hands and he was shaking it with the whole force of his body. Somehow it stayed attached.
"I lost everything!" He shook it again. "Everything!!"
"""),
# 95, Ch 14
(95, """Tell me what I did!"
He waited.
He actually waited. He sat there with his chest going and his hands open on his knees, like a man who has asked a fair question and is owed an answer.
Nothing answered.""",
"""Tell me what I did!"
"Why? Why me? Why now? Why!?!"
He waited for God's answer.
He actually waited. He sat there with his chest going and his hands open on his knees, like a man who has asked a fair question and is owed an answer.
It was met only with the crushing weight of his own feelings in the silence."""),
# 99, Ch 15
(99, "He looked at himself in the little window for a while and closed it.",
"He looked at himself in the phone screen and realized just how haggard he'd become. He closed it and put it away with disgust."),
# 100, Ch 15 (Grace's April email is CT's to write; its placeholder is left out of v6)
(100, """Nobody asked him for anything. There was no form. Two women at a folding table were handing out bags, and when he got to the front one of them looked at him the way his mother would have, and handed him two.
"You come back in two weeks, honey," she said. "We're here every other Saturday."
He looked for the old man in the line. He didn't see him.
He ate a peanut butter sandwich sitting in the truck with the door open, and then he ate another one.
Then he sat there with the twenty in his hand.
Focus on the people that say yes, an old man had told him.
There was one. He turned the phone over.
He wrote back badly. He typed with his thumbs for twenty minutes and what he sent was six lines. He told her he was living in his truck. He told her about his mother. He hadn't typed that to anybody. The important line was the last.
I don't want a boss. I don't want to be one either.""",
"""Nobody asked him for anything. There was no form. Two women at a folding table were handing out bags, and when he got to the front one of them looked at him the way his mother would have, and handed him two.
"You come back in two weeks, honey," she said. "We're here every other Saturday."
Honey. It landed somewhere under his ribs. He said thank you and got out of the way fast, before his face could do anything in front of all those people.
He looked for the old man in the line. Not seeing him sat in his chest longer than it should have.
The first peanut butter sandwich went down in the truck with the door open, so fast he barely tasted it. The second one he ate slowly, because it might have to last, and because his body had finally figured out it was allowed to be hungry.
Then he sat there with the twenty in his hand. It had gone soft from being folded, warm from the old man's coat and then from his own fist. *Somebody did it for me.*
*Focus on the people that say yes,* an old man had told him.
He turned the phone over. It occurred to him that he hadn't checked his email in a while. Months, maybe. What the hell. Maybe somebody owed him a free coffee. Maybe he had enough points for free guac at Chipotle.
He scrolled. Eleven hundred unread, give or take, and most of them were people who wanted something. Then, down in April, a name he knew now.
Grace.
He didn't know why he stopped on it. Most people never do, at moments like that. But something told him to open it, so he did.
She had been saying yes to him since spring. He just hadn't been looking.
He didn't answer right away. He sat with his thumb over the screen and ran it the way he ran everything now. A stranger, eight hundred miles away, offering a broke man a room. He had seen that one before. It could be a scam. It could be a cult with a nice website. It could be one more person who wanted him to be something, and he didn't have anything left to be.
Then that same little voice spoke up again, the one that had told him to open it. The quiet one that steers you toward where you're supposed to be, if you let it.
So he typed out his reply.
Writing back was the hardest thing he'd done in that town. Twenty minutes of thumbs, and what came out was six lines. That he was living in his truck. That his mother was in a chair by a window. He had never typed that to anybody, and seeing it on the screen made it true in a way it hadn't been in his head. He had to stop and look out the windshield a while before he could finish. The important line was the last one, and it was the only one he didn't have to think about.
*I don't want a boss. I don't want to be one either.*
He sent it."""),
# 101, Ch 15
(101, "Can't be worse, he thought.", "Can't be much worse, he thought."),
# 102, Ch 17
(102, """He picked up his water glass and held it out over the table like a man at a wedding.
"So the robots have taken over. Congratulations! You've lost.\"""",
"""Denny picked up his water glass and held it out over the table like a man at a wedding.
"So the robots have taken over," he said. "Congratulations! You've lost.\""""),
# 103, Ch 17
(103, """Six months. Nights."
He looked around the table, then back.""",
"""Six months. Nights."
Nobody moved. Priya was looking straight at Denny, almost daring him to say something to her directly, waiting for her moment to pounce. Curtis found something interesting about his napkin. Across the table somebody started to say something and stopped, and the quiet got heavier for it. Elijah could feel the whole table wishing he hadn't said the word.
But Denny kept going anyway, oblivious to the mood of the people around him, as he usually was.
He looked around the table, then back."""),
# 104 and 105, Ch 17
(104, "He looked at the page a long time.",
"""He looked at the page a long time, while listening to the frogs at the pond nearby. You know, he thought, this is a pretty good bleed-out spot.
A chuckle came over him and he went to bed that night feeling a little bit lighter."""),
(105, "feeling a little bit lighter.\nThat Sunday Grace helped him clean out the truck.",
"feeling a little bit lighter.\n\nThat Sunday Grace helped him clean out the truck."),
# 106, Ch 17
(106, """"Oh my God."
She had the amp out on the tailgate before he could say anything, turning it to the light""",
""""Oh my God." She looked at him. "Can I?"
He nodded.
She asked me first, Elijah thought. He liked the way it made him feel. He was more or less accustomed to being treated like a thing. Inside his psyche something started to turn. Although Elijah was quite unaware of it, his nervous system was beginning to let down its guard.
She had the amp out on the tailgate, turning it to the light"""),
# 108, Ch 17
(108, """than most of us."
She didn't say anything for a while. Through the little window over the sink she could see the truck, and Elijah putting the blanket back over the amp and tucking in the corners, like something asleep.""",
"""than most of us."
"I was just asking him if he wanted to play."
"I know you were." Lou set down another bunch. "He will play when he's ready. We cannot force the music out of him."
She didn't say anything for a while. Through the little window over the sink she could see the truck, and Elijah putting the blanket back over the amp and tucking in the corners, like something asleep.
She got a glass down and filled it at the sink and drank some of it. "I'm gonna go see if Marta needs any help."
Lou smiled with one side of his mouth and nodded, and patted her on the shoulder.
"You do that," he said."""),
# 110, Ch 17
(110, "Rosa opened the door with her left hand and a smile that took in both of them, and asked if they were hungry before they could ask her anything. Her right wrist was in a brace.",
"""Rosa opened the door with her left hand and a smile that took in both of them. She looked at Elijah.
"Mijo, you look muy flaco. Come in, eat."
She reminded him of some of his extended family.
Her right wrist was in a brace."""),
# 109, Ch 17
(109, """Curtis lowered the phone. "You don't owe us a work day.\"""",
"""Curtis lowered the phone. "You don't owe us a work day," he told her."""),
(109, "They got to the kitchen before it closed and drove back. Rosa checked",
"""They got to the kitchen before it closed. Grace was at the pass with a clipboard. While Curtis loaded the right container into the cooler, Elijah stayed where he was.
"Can I ask you something? At Rosa's, Curtis told her she didn't owe us a work day." He heard how it sounded. "I'm sorry. I thought I was here to contribute."
"You are," Grace said. "And you do." She touched his arm.
It went through him like current. It was a plain, warm, affectionate touch, and it was one of the first he'd felt in a long while. He didn't move, in case it stopped.
"Your knowledge earns your keep here, Elijah. That's all."
"Your knack for marketing is going to come in real handy," Curtis said from the cooler.
Grace didn't turn around. "Curtis. Not now."
"What? The dude's got the gift for gab. I thought we agreed."
"Curtis, I said not now."
Curtis shut the cooler lid. Nobody said anything else. The warm place on Elijah's arm stayed warm, but something behind it had gone quiet.
They drove back.
Rosa checked"""),
# 111, Ch 17
(111, """You don't knock out a wall till you know what it's holding up. So go on.""",
"""You don't knock out a wall till you know what it's holding up." Curtis adjusted himself in the seat. "So go on."""),
# 112, Ch 18
(112, """The spiral found Elijah again in late April.
It was seven weeks after he'd walked into the shop, and it did not announce itself as a spiral. It announced itself as diligence.""",
"""Elijah's next crisis found him in late April, seven weeks after he'd walked into the shop. It didn't announce itself, as most don't. He more or less stumbled into it."""),
# 113, Ch 18
(113, "He read the launch post standing in the gravel lot",
"Elijah read the announcement post standing in the gravel lot"),
# 114 and 115, Ch 18
(114, "a man with a flag avatar explaining whose fault it was.",
"""a man with an anime avatar explaining whose fault it was.
He saw many such posts. He consumed until he couldn't consume anymore. He was voracious in his appetite. And the compelling crackpots of the world rose to meet his demand."""),
(115, "the compelling crackpots of the world rose to meet his demand.",
"""the compelling crackpots of the world rose to meet his demand.
It had grown harder to tell whose voice was worth listening to in all the clutter, but it was clear that somewhere between all the different voices was something that resembled consensus. The truth was never clean. It often came as an amalgamation, like Frankenstein's monster, made of everyone's hopes and dreams and pain."""),
# 116, Ch 18
(116, "He had been here before. At a kitchen table with a chatbot",
"Elijah had been here before. At a kitchen table with a chatbot"),
# 117, Ch 18
(117, "It doesn't leave much day.",
"It doesn't leave much room in the day for the good things to surprise you."),
# 118, Ch 18
(118, """she will never once ask if you can walk. Don't let her.\"""",
"""she will never once ask if you can walk. Don't let her effort go to waste.\""""),
# 119, Ch 18
(119, """Soup's on at noon. That's not a reward, spreadsheet. It's lunch.\"""",
"""Soup's on at noon. That's not a reward, spreadsheet, for all your doom scrolling." Her eyes twinkled. "It's just lunch.\""""),
# 120, Ch 18
(120, "Then he went and turned the notifications off, all of them except the number of the place with the rose garden, and put the phone in a drawer that closed.",
"Then he put the phone on Do Not Disturb, with one exception: the number for the place with the rose garden. He put it in a drawer that closed."),
# 121, Ch 18
(121, """He just declined to rehearse it all day." She shrugged.""",
"""He just declined to rehearse it all day. That was Sal's rule, if he'd have called it one: one thing with an end to it, before noon." She shrugged."""),
# 122, Ch 18
(122, "At 9:40 he called the place with the rose garden, the way he had every Sunday since he came north.",
"At 9:40 that morning he called the place with the rose garden, the way he had every Sunday since he came north."),
# 123, Ch 18
(123, """"Marta knocks like a cop," she said. "Some doors, that's right." She was still looking at the jars. "I should have knocked like Marta.\"""",
""""Marta knocks like a cop," she said, and chuckled. Elijah found his eyes lingering on the curves of her mouth. "With some doors, that's the right approach." She was still looking at the jars. "Maybe I'm a little too cautious. Maybe I should have knocked like Marta."
"I think what you're doing is just right," he said."""),
# 124, Ch 19
(124, """She capped the marker. "It's a gorgeous design. It's a Claypot design. Design it again. Parts from the drawer, parts from the hardware store, and nothing your neighbor can't fix with the tools he already owns.\"""",
"""She capped the marker. "It's a gorgeous design, but it has your prior work experience written all over it. It reminds me way too much of the mainstream devices we're starting to see come out, Elijah."
Elijah's shoulders dropped a little.
"You're a good engineer," she said. "I mean it. I just want you to spend a little more time making this feel more like us than like Claypot."
Marta hooked the bottom drawer of the parts cabinet with her boot and slid it open. It rattled. Resistors in envelopes, a coil of wire, a coffee can of old relays.
"Parts from the drawer," she said. "Parts from the hardware store, and nothing your neighbor can't fix with the tools he already owns.\""""),
# 125, Ch 19
(125, "Real money, a real deadline, real customers with seedlings on the line. Elijah volunteered for the design.",
"""Real money, a real deadline, real customers with seedlings on the line.
Denny wanted to film the order coming in. Grace hugged Priya, and then Lou, and then Priya again. Curtis asked what happened if they couldn't deliver, and nobody answered him right away. Lou asked who was paying for the parts. Marta didn't say anything. She read the order twice and pinned it to the whiteboard.
Elijah volunteered for the design."""),
(125, "\nThe four months on the yellow ticket ran out on a Tuesday in May. He was under a sink at the time. He didn't find out until Thursday.\n", "\n"),
(125, "Marta pinned the repair emails to the corkboard the way other shops hang their first dollar.",
"""Marta pinned the repair emails to the corkboard the way other shops hang their first dollar.
The four months on the pawn ticket had run out in May while he was under a sink. By the time he remembered, his Telecaster was in the window on Fourth Street."""),
# 131, Ch 19
(131, "So he designed it again. The second version",
"""So he designed it again, and this time he started the old way. He spent a weekend at the bench with calipers and graph paper, measuring relays out of Marta's coffee can one at a time, because no two of them had the same footprint. By the end of the weekend he had a third of a board and a stack of crossed-out pages. The first design had already eaten the better part of a month, and forty growers had seedlings waiting on him.
So he went looking for help. A startup out of Iowa had an AI that laid out circuit boards. One evening with it turned into two, and every answer opened three more questions. By midnight on the second night, Elijah was lost.
Finally he came up for air. Did he actually need to know all this?
Not really. Then he remembered his training: the minimum viable product, the least you can build that still does the job. Forty boxes. Read the dirt, read the air, open a vent. With that, he got to work, and by morning the board was done.
He printed it out and laid it on the bench under the whiteboard. Marta's three numbers were still up there, with the order pinned beside them. Forty small boxes that could open a vent or a valve without asking a server in Virginia for permission. One company made the thing that had drawn his board. Zero people in the valley could say why it had put a trace where it did, and he was one of the zero.
Marta came in with her coffee and looked the drawing over for a long time. She ran a finger along one of the traces.
"Now that's ours," she said.
He didn't mention Iowa. It was a tool, he told himself, and he would have gotten there by hand in a couple of weeks anyway. Then he blocked out two weeks to write the firmware himself, line by line, as if that squared it.
The second version"""),
# 126, Ch 19
(126, "which from her was a parade.", "which from her was practically a parade."),
# 127, Ch 19
(127, "The build took the shed three weekends. On the first one, everybody was in a line, deburring cases and crimping wire ends, when the door opened and let in the cold.",
"""The build took all of them three weekends, and it took something out of every one of them. Thumbs got cut on case edges. Curtis swore at a crimper until Tyler showed him the trick of it. Priya asked what every part did and wrote the answers down. Lou, who had never held a multimeter, was arguing with one by the second Saturday.
Elijah felt, for the first time in a while, like maybe he was starting to fit in somewhere. He didn't lean on the feeling. Every so often he caught himself watching Curtis down the line and wondering what, exactly, Curtis and Grace had agreed on. But recent events and the flow of the day put that doubt out of his mind quickly. The work felt good, to him and to everybody else in the line.
On the first weekend they were all in that line, deburring cases and crimping wire ends, when the door opened and let in the cold."""),
# 128, Ch 19
(128, "came in with it. He looked too pleased with himself for a Saturday.",
"came in with it. Reuben had spent thirty years as a title officer at the county, and he looked too pleased with himself for a Saturday."),
# 129 and 130, Ch 19
(129, """"Nobody asks Reuben," Priya said, from the crimping line. "Reuben notices.\"""",
""""Nobody asks Reuben," Priya said, from the crimping line. "Reuben notices things. It's what makes him such a pain in the ass. But he's quite useful.\""""),
(130, "But he's quite useful.\"",
"""But he's quite useful."
"Saved our ass quite a few times," Lou said, from down the line."""),
# 132 and 133, Ch 19
(133, """somewhere. He knew what the thing drank. He also knew a nineteen-year-old had just done in a night what would have taken him two weeks, and that the boxes worked, and that forty growers would get them for a price they could pay.
He had helped build one of these machines. He had shown one off in a bar, and three people lost their jobs. Kelsey. Carol. Mateo. Their names had come off the realtors' website the week after the toast. He had never looked them up. He could have said any of it. He stood there with""",
"""somewhere, so he knew what the thing drank. But the real reason was the board, where he had used one himself, at midnight, and told no one. One company. Zero people who could read it. He had done that arithmetic at the whiteboard, and then he had kept going. Now a nineteen-year-old had done the same thing out loud. In one night he had written the firmware Elijah had set aside two weeks to write by hand, to make up for the board. The boxes worked. Forty growers would get them for a price they could pay.
He had helped build one of these machines. Once, in a bar, he had shown one off, and three people lost their jobs. Kelsey. Carol. Mateo. Their names had come off the realtors' website the week after the toast, and he had never looked them up. He could have said any of it. Instead he stood there with"""),
(132, "didn't say a word, and both of them noticed.",
"""didn't say a word, and both of them noticed.
Tyler noticed something else. He had the board's files on his laptop, the way he had everything, and the Iowa company's name was at the top of every one of them. To Tyler it had never been a secret. It was a file. He looked down the line at Elijah once, saw his face, and understood. He didn't say it. Nobody had asked him to."""),
# 134, Ch 19
(134, "Marta hadn't said anything either. She was looking",
"Marta hadn't said a word either, not since Grace walked Patricia down the line. She was looking"),
# 135, Ch 19
(135, """"Look," Marta said.
"We'll see," she said, to nobody, and went back to work.
Patricia left before lunch. She shook everyone's hand. Grace walked her to the car, talking low, and came back alone and went straight to the kitchen trailer without looking at anybody.
Elijah found Tyler outside afterward, sitting on the trunk of a Corolla, flashing units one after another.
"I showed some realtors once," Elijah said.
"Okay," Tyler said.
He didn't ask what happened. He was nineteen and he had twenty-six boxes left.""",
""""Look," Marta said.
He scrolled. The whole line waited on him, and he was still scrolling when Marta went back to crimping. "We'll see," she said, to nobody.
Patricia left before lunch. On her way out she went down the line and shook everyone's hand. Grace walked her to the car, and the two of them talked low beside it for a while. Then Grace came back alone and went straight to the kitchen trailer without looking at anybody.
Nobody picked a crimper back up.
"So we pull it," Curtis said. He was looking at the laptop, not at Tyler. "Throw the code out and write it by hand. That's what she was telling us."
"Lay off the kid, Curtis," Lou said. "Those boxes go out in June either way."
"Nobody's throwing anything out," Priya said. "We test it. Whatever fails goes up on the board, with the date."
Curtis turned around. "You're the engineer, bud. Is the kid's code any good or isn't it?"
Elijah hadn't read it. He couldn't vouch for it, and with his own board sitting in the same box, he couldn't say one word against how it was made, either.
"It passed the bench," he said.
It was Tyler's line, and everybody in the shed had just heard Tyler say it. Curtis looked at Elijah a second longer than he needed to. Then he went back to his crimper.
"Wire ends," Marta said, and that was the end of it.
Tyler shut the laptop, picked up a crate of units and carried them outside. Afterward Elijah found him there, sitting on the trunk of a Corolla and flashing units one after another.
"I showed an AI to some realtors once," Elijah said. "In a bar." It was as close as he could get to the rest of it.
"Okay," Tyler said. He didn't look up from the screen. "Your board's from Iowa, man. It says so in the file."
Elijah didn't have anything to say to that.
"You could've just told them."
Tyler didn't ask what happened with the realtors. He was nineteen, and he still had twenty-six boxes to go."""),
# 136, Ch 19
(136, """"You picked." She turned off the tap. "You picked nothing.\"""",
""""You picked." She turned off the tap. "You picked nothing."
He had picked. He had picked keeping his board quiet over a nineteen-year-old on a bucket, and he didn't tell her that either.
Tyler was still out on the trunk of the Corolla when the yard light came on, with nineteen boxes to go. Elijah carried a finished unit out from the shed and sat down on the bumper.
"Marta's question," he said. "Let's find out."
Neither of them could have said where the answer was in the code, so they tested it. Tyler pulled the probe wire on it, and the two of them sat and watched the little valve. A dead probe looked exactly like dry dirt. The valve clicked open and stayed open. On the coldest night of the year, it would have stayed open all night.
"Shit," Tyler said.
He asked Rod Code for a fix, and four lines came back. They pulled the wire again. This time the valve stayed shut, and a light on the lid started blinking. Neither of them could have told you why the four lines worked, and Elijah was in no position to complain about that. He wrote a new line for the repair card: *Light blinking? Valve stays shut. Swap the probe.* In the morning Marta read it, and ran the card through the laminator herself.
The last number on her whiteboard was still a zero. Nobody in the valley could read what was inside those boxes, including the two people who had put it there."""),
(136, "Two growers needed new probes in the first month. They changed them by hand",
"Two probes died in the first month. Both valves failed shut. The growers changed the probes by hand"),
# 137, Ch 22
(137, "and read them the timestamps.",
"and read them the timestamps. Then, because he was already standing there, he told them about the board too. The startup out of Iowa, the two nights it took, and the two weeks of firmware he had blocked out to make it square. At the back of the crowd, Tyler looked at the floor."),
# 138, Ch 15: two lines edit 100 left behind
(138, "\nHe went and looked. It was there, from April, under eleven hundred other things he hadn't opened. It had been sitting there the whole time.\n", "\n"),
(138, "holding a rich man's empty glass. It could be a cult. It could be nothing,", "holding a rich man's empty glass. It could be nothing,"),
# 139, Author's Note
(139, "was a tool that does a thing. The shovel never dug its own hole.", "was a tool that does a thing. But this is different. The shovel never dug its own hole."),
# 140, Author's Note
(140, "I'm not asking you to trust me. I'm asking you to take a look for yourself.", "If I can ask anything of anyone, it's that you take a look at this for yourself."),
# 141, Author's Note: the empty paragraph (scene break) before the last three lines
(141, "you might not be paying enough attention.\n\nThis could be the most pivotal moment", "you might not be paying enough attention.\nThis could be the most pivotal moment"),
# 142, Ch 1
(142, "So it had a ceiling. The ceiling was a power bill. Whoever", "So it had a ceiling. Whoever"),
# 143, Ch 2: Wes's text in italics
(143, "to drink.\nis this true\nElijah didn't answer.", "to drink.\n*is this true*\nElijah didn't answer."),
# 144, Ch 2
(144, "so that later he couldn't pretend he hadn't seen it coming.", "so that later he could look back and see if he was right."),
# 145, Ch 5
(145, "He never got around to the jam. He set it in the corner of the living room and didn't plug anything into it, as a monument, which was the point.\nThe call never came.",
"He plugged in and started to play, but a few bars in he noticed the time and stopped. He set the amp in the corner of the living room and didn't plug anything into it again, as a monument, which was the point.\nThe call he was expecting never came."),
# 146, Ch 6
(146, """"Head down," she said. "For me."\nHe didn't put his head down. He didn't know how anymore.""",
""""Keep your head down and stay focused for me," she said.\nHe meant to. He wanted to. But life gets in the way sometimes."""),
# 147, Ch 6
(147, "For a year he had explained it to every one of them, one at a time.", "For a year he had tried explaining it to each of them one at a time."),
# 148, Ch 9
(148, "Ruby shouldered through the swinging door. It swung shut behind him.", "Ruby walked through the swinging door, and it swung shut behind him, closing Elijah off from seeing what was going on. But from the hall, he could still hear."),
# 149, Ch 10
(149, "He couldn't figure out how to write to a billionaire without wanting something, and he couldn't figure out what he wanted.", "He couldn't write a billionaire without wanting something, and for the life of him, he still couldn't figure out what he wanted."),
# 150, Ch 11
(150, "Trent thought about that. They had six robot arms coming down from Oakland, a launch party in three weeks and nobody to put them in. They also had two spares in crates that they were never going to need. \"Tell you what,\" he said. \"Ride down with the arms. Help the crew bolt them in for the launch. Do that, and the two spares are yours.\"",
"Trent pondered for a moment. They had six robot arms coming down from Oakland, a launch party in three weeks and nobody to put them in. \"Tell you what,\" he said. \"You say you're good at carrying stuff. I got a lot of things that need to be carried, and some of them are quite expensive. Ride down with the arms. Help the crew bolt them in for the launch. If you do the work, we got two spare robot arms with your name on 'em.\""),
]

# Lines that must be italic from end to end (verify.py cannot see italics).
ITALIC = [(143, "is this true")]
