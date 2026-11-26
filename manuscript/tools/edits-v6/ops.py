"""Edits 87 onward, as find and replace on the v5 text (suggestions accepted).

Each op: (edit number, find, replace). The find must appear exactly once. In a replacement, a newline starts a new
paragraph, an empty line between two newlines is a scene break, and *...* is italic. The wording is copied from
manuscript/novel/EDITS.md, which stays the record of who wrote what.
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
# 141: no op. The blank paragraph came from a bug in make_v6.py (fixed 26 Nov); see edit 141 in the list.
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
# 151: no op, for the same reason as 141.
# 152, Ch 12
(152, "with the windows cracked and a towel over the wheel.", "with the windows cracked and a towel over the wheel.\nThe farm was two hours north, and his mother would have left the porch light on for him. But gas there and back every day was more than he had, and she had sent him off to be useful. He wasn't going to walk back through the door with nothing to show for it. Not again. Not after what happened last time."),
# 153, Ch 13
(153, "They took her to Santa Rosa.\"\nHe didn't remember the drive.", "They took her to Santa Rosa.\"\nHe left immediately. He didn't remember the drive."),
# 154, Ch 13
(154, "\nThe pot was on the stove.\nIt was not in the rack.", "\nWhen he got to the house, he saw what had happened. There was a pot on the stove.\nIt was not in the rack."),
# 155, Ch 7
(155, "\"Wes doing okay?\"\n\"I don't know. He's not really answering me.\"",
"\"Hey, you heard from the guys?\"\n\"No. I haven't heard from a lot of people, actually. Wes isn't really answering me.\""),
(155, "\"I'm serious, man. Why don't you just stick to music? You were good. People loved you up there. Stay in your lane.\"\n\"Bro. What do you mean?\"\nDavid didn't say what he meant. He let his eyes drop to his beer and kept them there.",
"\"I'm serious, dude. You gotta stop. Why don't you just stick to music? You were good. People loved you up there. Stay in your lane.\"\n\"I mean, as much as I'd like to, we're living through historic times, Dave. This is an unprecedented moment, and I kind of helped create it.\"\nDavid didn't say anything to that. He let his eyes drop to his beer and kept them there."),
(155, "\"It's not like that.\"\n\"Okay.\"\n\"Dave. It's not.\"\n\"Okay, Mad.\"\nThen they sat there",
"\"I'm fine,\" Elijah said. \"I just know things, and I'm trying to figure out how to tell people what I know.\"\n\"People don't care what you know, man. They care how you make them feel. You should know that from all your years playing music with all of us.\"\nElijah thought about it for a second. \"I appreciate that, man. But this is just too important.\"\nDavid made a face. \"All right,\" he said. \"Well, can I get you anything else?\"\nThen they sat there"),
# 156, Ch 13
(156, "He put his hand down.\nHe got the letter. He walked back to the truck the other way, which took him past the Bear Flag.",
"Eventually his hand came down. The doctor's letter was still waiting at the office, so he went and picked it up. On the way back to the truck he went around the other way, which took him past the Bear Flag."),
# 157, Ch 13
(157, "He heaved the hand truck back into his pickup. He looked at the porch a second. There was nobody on it. He lifted two fingers off the wheel going down the drive, and Elijah lifted his hand.",
"David heaved the hand truck back into his pickup and looked at the porch a second. There was nobody on it. Going down the drive, he lifted two fingers off the wheel, and Elijah lifted his hand."),
# 158, Ch 14
(158, "He lay back down.\nHe pulled the jacket up. He cried the way he had yelled, all the way, with his mouth open. Nobody was going to hear it over that. He cried until his ribs hurt, and then for a while after that he just lay there and leaked.",
"Slowly he lay back down and pulled the jacket up. Then the crying came, the way the yelling had, all the way, with his mouth open. Nobody was going to hear it over that. It went on until his ribs hurt, and for a while after that he just lay there and leaked."),
# 159, Ch 15 and 26: Grace's April email
(159, "But something told him to open it, so he did.\nShe had been saying yes to him since spring.",
"But something told him to open it, so he did.\n*Mr. Madrone,*\n*It has been an absolute pleasure watching you online. Everyone here at the farm agrees: you get it.*\n*We've been working on something for a long time now, and we think you'll appreciate it. Are you familiar with solarpunk? Like that stupid Chobani yogurt commercial, \"Dear Alice\"?*\n*Well, we're doing our best to build it in real life.*\n*If you're interested, there's a cot here and a private room with your name on it. Your own door, a shared kitchen, and a bunch of land.*\n*We would like to extend a formal invitation to host you while you build out your vision of the future with us.*\n*If you're interested, please just say the word and the spot is yours.*\n*Looking forward to working with you,*\n*Grace Lane*\nElijah took a breath and read the email again. Three, four, five times he read it, waiting to feel different.\nShe had been saying yes to him since spring."),
(159, "Then that same little voice spoke up again, the one that had told him to open it. The quiet one that steers you toward where you're supposed to be, if you let it.\nSo he typed out his reply.",
"Inside his chest was that same little voice that told him to join Crop Dust, to take the job at Claypot, and to do every other harebrained thing he had never regretted.\nHe started typing his reply."),
(159, "Elijah had never heard the word.",
"Elijah had seen the word once, in Grace's first email, and never thought about it again."),
# 160, Ch 16
(160, "He hadn't meant to. He'd meant to say hello. But he had spent",
"Going off wasn't the plan. All he'd meant to say was hello. But he had spent"),
(160, "fixed things for her neighbors. He told her what was coming, fast: the models, the list, the end of the deal. And then he started pitching.\nHe heard himself say the shop could scale. He said platform. He said there ought to be an app, a network of co-ops, a marketplace layer. He could build it in a month. This thing could be in fifty towns by Christmas. They could get ahead of the wave. He said first-mover, and heard it come out of his mouth in Ruby's voice, quick and light.",
"fixed things for her neighbors. So he told her what was coming, fast: the models, the list, the end of the deal. And then he started pitching.\nThe shop could scale, he heard himself say. Platform. There ought to be an app, a network of co-ops, a marketplace layer. He could build it in a month. This thing could be in fifty towns by Christmas. They could get ahead of the wave. *First-mover,* he said, and heard it come out of his mouth in Ruby's voice, quick and light."),
# 161, Ch 17
(161, "\"That's a picture,\" Priya said. \"What would you measure?\"",
"\"That's a picture,\" Priya said, fidgeting with the pencil behind her ear. \"What would you measure?\""),
# 162, physical beats
(162, "\"Fire escape,\" Ruby said. \"It's the only good room.\"",
"\"Fire escape,\" Ruby said, already sliding a window up. \"It's the only good room.\""),
(162, "\"Heard they close Friday,\" David said.",
"\"Heard they close Friday,\" David said, looking past him at the house."),
(162, "\"They broke things,\" Curtis said.",
"\"They broke things,\" Curtis said, pointing his fork down the table at her."),
(162, "\"Every month,\" Reuben said.",
"\"Every month,\" Reuben said, pushing his glasses up onto his forehead."),
(162, "starts with lettuce,\" Curtis said. \"Then it's Skynet.\"",
"starts with lettuce,\" Curtis said, shaking the cold water off his hands. \"Then it's Skynet.\""),
(162, "\"Wait, so the plan is chalk,\" Tyler said.",
"\"Wait, so the plan is chalk,\" Tyler said, shifting the reel to his other arm."),
(162, "\"I know it,\" Lou said.",
"\"I know it,\" Lou said, and set down his fork."),
(162, "\"It's a sensor,\" Curtis said. \"It's two wires.\"",
"\"It's a sensor,\" Curtis said, pinching the bridge of his nose. \"It's two wires.\""),
(162, "\"Thirty years that's been on that wall,\" David said.",
"\"Thirty years that's been on that wall,\" David said, following his eyes up to the frame."),
# 163, Ch 17
(163, "\"I don't know. I'm kind of off telling it.\"",
"\"I don't know, I'm kind of turned off on telling it.\""),
# 164, Ch 17
(164, "He noticed his shoulders relax a bit.",
"Without being conscious of it, his shoulders relaxed a few inches."),
# 165, Ch 17
(165, "said one word, \"Musician,\" the way you'd say termites.",
"said one word, \"Musicians,\" the same way you might say termites."),
# 166, Ch 18
(166, "\"I think what you're doing is just right,\" he said.",
"\"I think the way you're doing it is just right,\" Elijah said.\nOut by the pond, the birds were chirping magnificently."),
# 167, Ch 19
(167, "Chapter 19: Eleven, One, Zero\nThe co-op's first real manufacturing run was forty greenhouse controllers.\nIn April the order came",
"Chapter 19: Eleven, One, Zero\nIn April the order came"),
# 168, Ch 19
(168, "I just want you to spend a little more time making this feel more like us than like Claypot.\"",
"I just want you to spend a little more time making this feel like it was made by us and not Claypot.\""),
# 169, Ch 19
(169, "and Elijah fixed what they found",
"and the fledgling production team fixed what they found"),
# 170, Ch 20
(170, "Lou put him on drip tape in May, and it just about killed him.",
"What Lou did to Elijah in May just about killed him."),
# 171, Ch 20
(171, "\"Ivy League,\" he said, wiping his eyes.",
"\"Hey, Ivy League,\" he said, wiping his eyes."),
# 172, Ch 20 to 39
(172, "He had come north to do something about it. He also believed nobody could do anything about it. He had never put those two facts next to each other.",
"He had come north to do something about it, and he also believed nobody could do anything about it. Until now, those two facts had never sat next to each other in his head."),
(172, "He stood there with the keys and thought about the logs",
"Instead he stood there with the keys and thought about the logs"),
(172, "He stayed where he was useful. Useful was easier than David.",
"So he stayed where he was useful. Useful was easier than David."),
(172, "He swept the shop twice. He checked his phone for nothing. He thought about a field full of people who could dance",
"He swept the shop twice and checked his phone for nothing. Then he thought about a field full of people who could dance"),
(172, "He wanted to draw a line through it and extend it. He opened the inbox.",
"He wanted to draw a line through it and extend it. Instead he opened the inbox."),
(172, "he had stopped sleeping for a month. He read it standing up, with the coffee going cold.",
"he had stopped sleeping for a month. This time he read it standing up, with the coffee going cold."),
(172, "He read it three times. He typed I'm sorry I missed and looked at it",
"He read it three times, then typed *I'm sorry I missed* and looked at it"),
(172, "He pocketed the phone to answer later, when he could think, and went to find Grace.",
"Then he pocketed the phone to answer later, when he could think, and went to find Grace."),
(172, "He'd come with a better plan. He had it on his phone.",
"He'd come with a better plan, and he had it on his phone."),
(172, "every fifteen minutes. He'd already priced it. He showed her.",
"every fifteen minutes. It was already priced. He showed her."),
(172, "He didn't sleep. He lay in the shouse with the phone on his chest",
"He didn't sleep. All night he lay in the shouse with the phone on his chest"),
(172, "The stove ticked as it cooled. He lay there and listened to it until the window went gray.",
"The stove ticked as it cooled, and he listened to it until the window went gray."),
(172, "He'd have a fix drafted by March. He had, everyone knew, already started.",
"A fix would be drafted by March. He had, everyone knew, already started."),
(172, "Then the red light came on. He watched himself skip to the last slide",
"Then the red light came on. From somewhere outside himself he watched himself skip to the last slide"),
(172, "into the microphone. He sat down with eight minutes of the talk unsaid.",
"into the microphone. When he sat down, eight minutes of the talk were still unsaid."),
(172, "He wanted numbers. He had a notebook of them already.",
"What he wanted was numbers, and he had a notebook of them already."),
(172, "He knew what he was doing. He had a name for it in the notebook and a rule against it. He did it for three nights anyway.",
"He knew what he was doing. There was a name for it in the notebook, and a rule against it. For three nights he did it anyway."),
(172, "He didn't bring anybody a plan. He had said out loud, at a Friday table, that he was done bringing plans. Wren had put her hand on her chest. He had asked Grace",
"Nobody got a plan from him. At a Friday table he had said out loud that he was done bringing plans, and Wren had put her hand on her chest. Later he had asked Grace"),
(172, "He looked at the date in the corner, the one with his initials",
"There was the date in the corner, the one with his initials"),
(172, "He didn't tell anyone. He had nothing he could show them.",
"He didn't tell anyone. There was nothing he could show them."),
(172, "He closed the notebook and snapped a rubber band around it.",
"So he closed the notebook and snapped a rubber band around it."),
(172, "He wanted to argue. He wanted to run it again, with the fix in, right now, and show everybody it worked. He looked at Irene.",
"He wanted to argue, to run it again with the fix in, right now, and show everybody it worked. Then he looked at Irene."),
(172, "He put the hinge down on the post. He was back in a hallway",
"Carefully he put the hinge down on the post, and then he was back in a hallway"),
(172, "He had gotten it from Nate and Wes, and from his mother, and from David across a bar.",
"Nate and Wes had given it to him, and his mother, and David across a bar."),
(172, "Curtis stood up. He didn't say a word. He wiped his mouth",
"Curtis stood up. Without a word, he wiped his mouth"),
(172, "He had heard no in that room before.",
"That room had told him no before."),
(172, "He sat there with the laptop pointed at her shoulder.",
"So he sat there with the laptop pointed at her shoulder."),
(172, "He had eleven notebooks about a machine and not one line about that. He never thought about it. He didn't think about it because",
"Eleven notebooks about a machine, and not one line about that. He never thought about it, because"),
(172, "He heard how it sounded the second it was out. He meant that he wished",
"The second it was out, he heard how it sounded. What he meant was that he wished"),
(172, "He knew what choosing for people looked like. He'd been paid for it.",
"What choosing for people looked like, he knew. He'd been paid for it."),
(172, "He drove past the turn twice on the way to the feed store and didn't take it.",
"Twice, on the way to the feed store, he drove past the turn and didn't take it."),
(172, "He tuned it, and it slipped, and he tuned it again.",
"It took him a minute to tune it, and it slipped, and he tuned it again."),
(172, "He leaned the guitar back in its corner and put the blanket back on.",
"Afterward he leaned the guitar back in its corner and put the blanket back on."),
(172, "He lifted the hose over his head with one hand",
"From down there he lifted the hose over his head with one hand"),
(172, "He cashed the newest one for this.",
"For this he cashed the newest one."),
(172, "He didn't put a note in that one.",
"That one went without a note."),
(172, "He knew what it was. He had known since a hinge and a gatepost in July.",
"He knew what it was, and had known since a hinge and a gatepost in July."),
(172, "He would have to be careful in here now, more careful than he used to be.",
"From now on he would have to be careful in here, more careful than he used to be."),
(172, "He'd built eleven notebooks on it.",
"Eleven notebooks rested on it."),
(172, "He meant the part about another time. He put the phone back in his pocket.",
"He meant the part about another time. The phone went back in his pocket."),
(172, "He drank half. He tipped like a man who used to get tipped. He took the book out",
"He drank half and tipped like a man who used to get tipped. Then he took the book out"),
# 173, Ch 33, 34, 38
(173, "\"Owned by who?\" Curtis said.",
"\"Owned by who?\" Curtis said, not looking up from his plate."),
(173, "\"Name one,\" Marta said.",
"\"Name one,\" Marta said, and set her cup down."),
(173, "\"Easy for you,\" Curtis said.",
"\"Easy for you,\" Curtis said, sitting back in his chair."),
(173, "\"Most of them,\" Denny said.",
"\"Most of them,\" Denny said, raising his glass."),
(173, "\"Nine days,\" Curtis said.",
"\"Nine days,\" Curtis said, looking out the windshield."),
(173, "\"Item four,\" Reuben said.",
"\"Item four,\" Reuben said, turning a page."),
(173, "\"Hell, I'll look at it,\" said Lou.",
"\"Hell, I'll look at it,\" said Lou, and held out his hand for the laptop."),
(173, "\"That's a thermometer, Curtis,\" Frank said.",
"\"That's a thermometer, Curtis,\" Frank said, rubbing his eyes."),
(173, "\"I know,\" Tyler said.",
"\"I know,\" Tyler said, looking at his plate."),
(173, "\"Sit down, Curtis,\" Rosa said.",
"\"Sit down, Curtis,\" Rosa said, and patted the bench beside her."),
# 174, Ch 32, 34, 35, 38
(174, "\"It's not the Terminator, Curtis. It's an arm. It's bolted",
"\"Curtis, it's an arm. It's bolted"),
(174, "\"It's not that they can't. It's that they won't.\"",
"\"They can. They just won't.\""),
(174, "This time it wasn't a yes. It was three tables now, at one table.",
"This time nobody said yes. There were three tables now, at one table."),
(174, "But it didn't break. It's on purpose.",
"But it didn't break. Somebody did it on purpose."),
# 175, Ch 31
(175, "He had turned down the million dollars and the ads and the room. And these people",
"He had turned down the million dollars and the ads and the room. That was his father in him: never take a handout. And these people"),
# 176, Ch 26
(176, "the low spot at the end of bed three was a pond,",
"the low spot at the end of bed three was under water,"),
(176, "looked at the pond, and wrote it down.",
"looked at the water, and wrote it down."),
(176, "He got down in the pond with his shoulder",
"He got down in the water with his shoulder"),
# 177, Ch 37
(177, "Somebody checked.\nHe sat there with the engine running and cried.",
"Somebody checked.\nOut by the pond, the birds had started up.\nHe sat there with the engine running and cried."),
# 178, Ch 37
(178, "It took a morning. A bag of clothes. The laptop. A milk crate of notebooks, eleven of them now, and the manuscript, which was three hundred pages and had a title. The broken coupons, in a coffee can. His mother's pot. Everything he owned fit in the bed of the Ranger with room left over, except two robot arms in the back of the equipment shed.",
"It took a morning. A bag of clothes went in, and the laptop. Then a milk crate of notebooks, eleven of them now, and the manuscript, which was three hundred pages and had a title. He stood holding that one a while before he set it down. The broken coupons went in a coffee can. His mother's pot went in beside them. Going on three years, and everything he owned fit in the bed of the Ranger with room left over. It should have felt like traveling light. It felt like he had hardly been here at all. All that was left were two robot arms in the back of the equipment shed."),
# 179, Ch 24, 28, 30
(179, "The sweep signed off on it Tuesday.",
"The sweep signed off on it."),
(179, "The county's power was back Tuesday.",
"The county's power came back three days later."),
(179, "He'd filed it with the clerk on Tuesday.",
"He'd already filed it with the clerk."),
# 180, Ch 17
(180, "He looked around the table, then back.\n\"You know what I asked him?",
"He looked around the table, then back at Elijah.\n\"You know what I asked him?"),
# 181, Ch 17
(181, "The warm place on Elijah's arm stayed warm, but something behind it had gone quiet.",
"The warm place on Elijah's arm stayed warm, but under it was a question he hadn't had a minute ago. Agreed on what?"),
# 182, Ch 21 to 39, clarity pass
(182, "He watched her do forty in a night.",
"Elijah watched her do forty in a night."),
(182, "He set the next lid down. \"You put my face",
"Denny set the next lid down. \"You put my face"),
(182, "The servers arrived at the end of May, in the back of Denny's truck.",
"The servers had come at the end of May, in the back of Denny's truck."),
(182, "He started calling the rack the Crucible.",
"Elijah started calling the rack the Crucible."),
(182, "He had a text that said Saw the video with the warehouse guy. He's good, and he'd put a thumb on it",
"He had a text from David that said *Saw the video with the warehouse guy. He's good.* Elijah had put a thumb on it"),
(182, "he told them about the board too.",
"he told them about the circuit board too."),
(182, "The co-op adopted a rule that Saturday.",
"The co-op adopted a rule that same Saturday."),
(182, "That night Grace found him on the pump house steps.",
"That Saturday night Grace found him on the pump house steps."),
(182, "The morning before, at 9:40, he called the rose garden.",
"The morning before, on Sunday at 9:40, he called the rose garden."),
(182, "The aide held the phone by her ear.",
"The aide held the phone by his mother's ear."),
(182, "the aide said she had shown it to her.",
"the aide said she had shown it to his mother."),
(182, "Elijah called him on Sundays, after his mother.",
"Elijah called him on Sundays, after he called Ma."),
(182, "It came to the table anyway.",
"The argument came to the table anyway."),
(182, "All of it happened around him, because",
"All of it happened around Elijah, because"),
(182, "\"Now I'm holding your rain fly.\"\n\"Still want the fence,\" Curtis said.",
"\"Now I'm holding your rain fly. Still want the fence,\" Curtis said."),
(182, "\"I've been reading deeds a long time. I know what a man signs",
"\"I've been reading deeds a long time,\" Reuben said. \"I know what a man signs"),
(182, "He brought the Friday table a plan.",
"Elijah brought the Friday table a plan."),
(182, "But nobody told her it wasn't her business, either.",
"But nobody told Patricia it wasn't her business, either."),
(182, "He slept. He got up and swept.",
"Elijah slept. He got up and swept."),
(182, "The aide said she'd had a good night",
"The aide said Ma had had a good night"),
(182, "He means me. He's said so.",
"My dad means me. He's said so."),
(182, "\"Us. Like Irene's wire.\"",
"\"Us,\" Lou said. \"Like Irene's wire.\""),
(182, "like he was stopping a truck at a gate.\n\"Listen to me,\" he said. \"Please.\"",
"like he was stopping a truck at a gate.\n\"Listen to me,\" he said again. \"Please.\""),
(182, "He looked down the table. \"So tell me this.",
"He looked from face to face. \"So tell me this."),
(182, "Lou was on the step when he came out.",
"Lou was on the step when Elijah came out."),
(182, "\"I'll keep the stove going.\" He slid the key",
"\"I'll keep the stove going,\" Lou said. He slid the key"),
(182, "She held it out to him. He took it.",
"She held it out to Elijah. He took it."),
(182, "Elijah had wanted to ask him one more question.",
"He had wanted to ask Lou one more question."),
(182, "She was in the chair by the window.",
"His mother was in the chair by the window."),
(182, "His was the one fence left on that road",
"Manny's was the one fence left on that road"),
(182, "scooted her chair six inches away from her.",
"scooted her chair six inches back from Patricia's."),
(182, "just as he had left it.",
"just as Elijah had left it."),
(182, "a text he had never really answered.",
"a text from Wes he had never really answered."),
(182, "\"Mad.\" David put the glass down. He leaned on the bar",
"\"Mad.\" David leaned on the bar"),
(182, "He heard her. Under all the others.",
"He heard Grace. Under all the others."),
(182, "Wes kept texting dates. He hadn't made one yet.",
"Wes kept texting dates. Elijah hadn't made one yet."),
# 183, Ch 18
(183, "Claypot shipped Companion 2.0 on a Thursday. Elijah read the announcement post standing in the gravel lot",
"Claypot shipped Companion 2.0 on a Thursday afternoon, just fifteen minutes before the financial markets closed. Elijah read the announcement post standing in the co-op's gravel lot"),
# 184 to 186, the v7 changes brought into v6 (CT, 26 Nov: "I want the v6 that I'm reading in large print to be the
# most current version"). The wording is in manuscript/tools/edits-v7/ops_v7.py and V7-CHANGES.md.
# 185, Contents and the Author's Note: the note becomes a Dedication, and Thank You joins the contents
(185, "Contents\nAuthor's Note\n", "Contents\nDedication\n"),
(185, ("Appendix\nAuthor's Note\nFor years, I've been talking about this.\n", "Let's begin to imagine how."),
"Appendix\nThank You\n§H1 Dedication\n§C For the people I love who looked me in the eye like I'd finally lost it."),
# 184, "Recognize Your Power" closes the Dedication (corrected 26 Nov: it was a first page of its own)
(184, "For the people I love who looked me in the eye like I'd finally lost it.",
"For the people I love who looked me in the eye like I'd finally lost it.\n§C Recognize Your Power"),
# 186, the very end: Thank You, and the last line
(186, "Thursday, November 25, 2027. Thanksgiving.",
"""Thursday, November 25, 2027. Thanksgiving.
§H1 Thank You
Thank you for reading. Thank you for your time.
Please consider how much of a difference each and every one of us can make in this world if we really try. But you don't really need to make that big of a difference to everyone. You are someone. And if you touch any heart, please be sure to start with your own.
§C Recognize Your Power"""),
# 187, Ch 31: the call moves a week, because Marta's knock at eight, the shop, the eggs and Wren all come first
(187, "On Sunday at 9:40 he called the rose garden.",
"The next Sunday at 9:40 he called the rose garden."),
# 188, Ch 15: the check-engine light
(188, "Somewhere past Cloverdale the check-engine light came on.",
"""Somewhere past Cloverdale the check-engine light came on.
Elijah looked at it and rolled his eyes. Then he snorted, and the snort turned into a laugh, and the laugh got away from him. All his pent-up pain started rolling out of his lungs at once. He wiped his eyes and turned up the radio. Willie Nelson was singing "On the Road Again."
Figures, he thought. I hope they have a good mechanic."""),
# 189, Ch 18: Marta's line about Grace reads as a warning
(189, "go to waste.\" She straightened up. \"Soup's on",
"go to waste.\" She straightened up and looked him dead in the eye. \"You waste it, and you and me are going to have a problem.\" She let that sit. \"Soup's on"),
# 190, Ch 20: cut the cable box line
(190, "He was a little ashamed of that. He had a notebook with the wattage of his cable box in it.",
"He was a little ashamed of that."),
# 191, Ch 20: Lou, "my man", and "Such as?"
(191, "\"It doesn't work, man. It's never worked. It works because nine people here don't get paid,",
"\"It doesn't work, my man. It works because we're lucky. Our specific constellation has some unique advantages.\"\n\"Such as?\"\n\"Well,\" Lou said. \"Nine people here don't get paid,"),
# 192, Ch 20: the pot points back to Ch 13
(192, "Elijah thought about his mother, and the pot she never let anyone else wash.",
"Elijah thought about his mother, and the sacred pot she never let anyone else wash that had been burned to a crisp on the back burner."),
# 193, Ch 20: Lou, "I already lost one orchard."
(193, "Not a subscription. I already lost one orchard to one buyer.\"",
"Not a subscription. I already lost one orchard.\""),
# 194, Ch 20: Wren, "a stranger had helped themselves to the inside of my house"
(194, "Then I found out a machine wrote it, and I felt like somebody had been in my house.\"",
"Then I found out a machine wrote it, and I felt like a fraud and like a stranger had helped themselves to the inside of my house.\""),
# 195, Ch 20: Wren introduced, the run-on split
(195, "That was Wren, who led the Sunday circle and made the candles and had painted every wall of the seed house, inside and out, with things that were half heron and half radio tower. She was twenty-four, and the best artist Elijah had ever met.",
"That was Wren. She led the Sunday circle and made the candles, and she had painted every wall of the seed house, inside and out, with things that were half heron and half radio tower. She was twenty-four, and one of the best artists most people had ever met."),
]

# Lines that must be italic from end to end (verify.py cannot see italics).
ITALIC = [(143, "is this true")] + [(159, e) for e in ["Mr. Madrone,", "It has been an absolute pleasure watching you online. Everyone here at the farm agrees: you get it.", "We've been working on something for a long time now, and we think you'll appreciate it. Are you familiar with solarpunk? Like that stupid Chobani yogurt commercial, \"Dear Alice\"?", "Well, we're doing our best to build it in real life.", "If you're interested, there's a cot here and a private room with your name on it. Your own door, a shared kitchen, and a bunch of land.", "We would like to extend a formal invitation to host you while you build out your vision of the future with us.", "If you're interested, please just say the word and the spot is yours.", "Looking forward to working with you,", "Grace Lane"]]
