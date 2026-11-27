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
# 196, Ch 7: the Spanish teacher
(196, "It was supposed to be for Nate and Wes and his mother and David.\nThen the other kind of message started showing up.",
"It was supposed to be for Nate and Wes and his mother and David.\nThen a name came in that he hadn't seen since high school. Mr. Ostrander had taught him Spanish for three years, and once, after class, had told him he had a good ear and should never let anybody talk him out of using it. Elijah opened it smiling.\n*You don't know what you're talking about. That's never going to happen.*\n*Oh, Mr. Ostrander,* Elijah wrote back. *It's really nice to hear from you. Hope everything's good. Hope you're well.*\nThe answer came before he'd set the phone down. *Cut the crap, kid. You're out of your league here. You have no idea what you're talking about. This isn't going to happen. This isn't true. And you need to stop spreading fear online.*\nSpreading fear? He scrolled back up through it. I'm not spreading fear, he thought. Am I?\n*Hey,* he typed. *Maybe something got misconstrued. Maybe there's a miscommunication here. I'm not trying to spread fear. I'm just trying to share what I've personally experienced and let people know what's happening.*\n*You're making stuff up and I don't appreciate it. This isn't true. That didn't happen. You're a liar. And you need to stop.*\nWhoa, he thought. What the hell?\nHe set the phone face down on the amp. He really looked up to this guy. He loved this guy. And his old teacher just called him a liar?\nThe phone rattled against the grille.\nThen the other kind of message started showing up."),
# 197, Ch 0 to 19 and Ch 37 to 39: the counting pattern (CT: "Don't do the pattern")
(197, "He'd underlined it twice. Then he'd gone back to nodding.",
"He'd underlined it twice and gone back to nodding."),
(197, "David looked at him a second longer than he needed to. Then he went to change a keg.",
"David looked at him a second longer than he needed to, and went to change a keg."),
(197, "Curtis looked at Elijah a second longer than he needed to. Then he went back to his crimper.",
"Curtis held Elijah's eye a beat too long and went back to his crimper."),
(197, "He left the tower off for a week. Then he opened the notebook where he'd scrawled MADRONE IS NOT A DRONE, turned to a clean page, and started writing.",
"He left the tower off for a week, and when he opened the notebook where he'd scrawled MADRONE IS NOT A DRONE, he turned to a clean page and started writing."),
(197, "Elijah wrote it all down. Then he watched it again.",
"Elijah wrote it all down."),
(197, "Then he sat very still, because he was dizzy.",
"He sat very still, because he was dizzy."),
(197, "Then he needed energy figures, so he found the Kardashev numbers",
"For energy figures he found the Kardashev numbers"),
(197, "He poured the pitchers. Then he came back, put on",
"He poured the pitchers and came back, put on"),
(197, "Then he opened the band chat to send the link.",
"He opened the band chat to send the link."),
(197, "He pasted the link under that anyway. Then he sent it to the other two chats and typed",
"He pasted the link under that anyway, sent it to the other two chats, and typed"),
(197, "Then there was a paralegal in Fresno, so he wrote him back too. Then a guy who taught high school shop, and a nurse.",
"There was a paralegal in Fresno, so he wrote him back too, and a guy who taught high school shop, and a nurse."),
(197, "Elijah read that one twice. He answered",
"He answered"),
(197, "Elijah watched it four times looking for the lie.",
"Elijah watched it looking for the lie."),
(197, "He told the phone about the forty-eight dollars. Then he went in.",
"He told the phone about the forty-eight dollars and went in."),
(197, "Then he asked about the farm, and what they grew",
"He asked about the farm, and what they grew"),
(197, "and looked at it a while. Then he thought about Wes.",
"and looked at it a while, thinking about Wes."),
(197, "He watched it until it stopped. Then he typed Working.",
"When it stopped, he typed Working."),
(197, "It lasted a second or two. Then David looked back down",
"It lasted a second or two before David looked back down"),
(197, "He sat with them for a while. Then he started the truck.",
"He sat with them a while and started the truck."),
(197, "local pickup only. Then he watched it. A week went by.",
"local pickup only. A week went by."),
(197, "He got as far as the first line. Then he thought about the comments",
"He got as far as the first line and thought about the comments"),
(197, "He watched it not ring. Then he played the voicemail.",
"He watched it not ring and played the voicemail."),
(197, "He read it twice with the door open",
"He read it with the door open"),
(197, "He thought about a chair by a window. Then he put the phone face down",
"He thought about a chair by a window and put the phone face down"),
(197, "The old man nodded and put it away. Then he looked at Elijah for a while.",
"The old man nodded, put it away, and looked at Elijah for a while."),
(197, "He stood there a second getting his balance. Then he went into the coat one more time",
"When he had his balance he went into the coat one more time"),
(197, "Elijah took a breath and read the email again. Three, four, five times he read it, waiting to feel different.",
"Elijah took a breath and read the email again, waiting to feel different."),
(197, "He read the last three words again. It was the second time in two days somebody had said them to him.",
"You look thin. It was the second time in two days somebody had said that to him."),
(197, "Marta looked at him for another second. Then she picked up a push broom",
"Marta looked at him another second and picked up a push broom"),
(197, "She held the amp a second longer. Then she set it down",
"She held the amp a second longer before she set it down"),
(197, "the same way you might say termites. Then she went back to her bench.",
"the same way you might say termites, and went back to her bench."),
(197, "He brought the jars in. Then he put the phone on Do Not Disturb",
"He brought the jars in and put the phone on Do Not Disturb"),
(197, "She read the order twice and pinned it",
"She read the order and pinned it"),
(197, "Not really. Then he remembered his training",
"Not really. But he remembered his training"),
(197, "Then Grace came back alone and went straight",
"Grace came back alone and went straight"),
(197, "and stood there holding it. Then he carried it back",
"and stood there holding it. He carried it back"),
(197, "He wrote his name and the time. Then he turned back a page, and another.",
"He wrote his name and the time and turned back a page, and another."),
(197, "Then he laid one more place, at the corner",
"He laid one more place, at the corner"),
(197, "Then everyone had one in their hand",
"Soon everyone had one in their hand"),
(197, "Grace had read hers twice. She laid it down",
"Grace laid hers down"),
(197, "She stood over it a second. Then she pulled the blanket off and folded",
"She stood over it a second before she pulled the blanket off and folded"),
(197, "without asking. Then he slid the four ones back across with two fingers.",
"without asking, and slid the four ones back across with two fingers."),
(197, "He looked at it a while. Then he typed, Can't this time.",
"He looked at it a while before he typed, Can't this time."),
(197, "Then he thought of Manny's well, four feet down, and it went back where it came from.",
"The thought of Manny's well, down four feet, sent the smile back where it came from."),
(197, "Then a face filled the screen.",
"A face filled the screen."),
(197, "Then he took the book out of his jacket",
"He took the book out of his jacket"),
# 198, Ch 25 rebuilt (CT's letter, town, pond and Thanksgiving scenes; manuscript/novel/drafts/chapter-25.md, draft 3)
(198, "Surely Frank knew.\nThe paper on the door",
"Surely Frank knew.\n\nMost weeks he wrote to Ma on a yellow pad, because the aide said she liked having something to hold. This letter had the beds in it, and the first frost, and the stove in the shouse. Lou thought it had been a decent year for squash. He had done the arithmetic on her room again that morning, and the letter left that out.\nGrace came in and sat down on the table he used as a desk, on top of the letter.\n\"You're on my letter.\"\n\"I know. I want to bring your pay to the table Friday.\"\n\"No.\"\n\"I promised you, Elijah. The day you got here. I said I'm good for it.\"\n\"I know you did.\"\n\"So let me be good for it. Why are you acting this way?\"\n\"Because I just,\" he said, and stopped. He scratched his head and pulled a long breath in through his nose. On the way out, his hand went up and took hold of the hair on top of his head.\n\"I've lost a lot of people who were important to me, okay? I've been through a lot. Finishing this book is really important to me. You are really important to me. This farm is really important to me. These people are really important to me.\"\nGrace's hand stopped halfway to her braid.\n\"So then why can't you just let me bring it to the table?\"\n\"Because it's just,\" he said. \"It's not fair.\"\nShe slid off the table, stepped back and crossed her arms. \"Fair to who?\"\nThrough the window he could see the north houses up the road. The last one was Hector and Lupe's.\n\"I don't know. Don't worry about it.\"\n\"You're almost forty, and these are your conflict resolution skills?\"\nHis jaw set. The pad between them still said *Dear Ma* at the top. He looked at it and let his breath go.\n\"Grace.\" He took her hands. \"Look, I'm sorry, okay? I'm sorry. Do you want to go into town and get ice cream?\"\nShe lit up and tried to hide it. She squinted at him, hard, so he would know she was still mad. The corner of her mouth didn't get the message.\n\"I want frozen yogurt.\"\nThe frozen yogurt place in Ardell was next to the laundromat. Grace got the tart kind with mochi and gummy bears on top and ate it on the sidewalk. The wash station needed a hose clamp, so they walked down to the square, to Kowalski's.\nTyler was on the register. Since August he had only worked Saturdays.\n\"You guys got anything out at the shed that pays?\" Tyler said, ringing up the clamp. \"I'd take gas money.\"\n\"We can't pay anybody yet, hon,\" Grace said. \"We're working on it.\"\nElijah was still back in the fastener aisle. The clamp had been the last one on its hook. He stood in front of that hook, and the empty hooks on either side of it, and looked at them with no surprise at all. Grace was watching his face.\nIn the truck she said, \"You knew.\"\n\"Since spring.\"\n\"You knew since spring and you didn't knock?\"\n\"I didn't want to be the crackpot again.\"\n\"So you let him go through it by himself.\" She pointed the spoon at him. \"You knock, Elijah. He gets to slam it in your face. That part's his. But you knock.\"\nThrough the windshield they could see Tyler taping a new HOURS sign to the inside of the door.\nThe paper on the door"),
(198, "and then to Saturdays, and then Frank told him in the fastener aisle that he couldn't keep him. Tyler came out to the shed the next morning like it was any other day.",
"and then to Saturdays."),
(198, "Which meant Frank had known long enough to laminate it.",
"Which meant Frank had known long enough to laminate it. Frank told Tyler in the fastener aisle that he couldn't keep him, and Tyler came out to the shed the next morning like it was any other day."),
(198, ("Elijah told Grace that night, at the kitchen trailer.", "In the morning he made the harder visit, the two-mile one."),
"That week he made the harder visit, the two-mile one."),
(198, ("That fall, it was Marta who told him about the music.", "somebody ought to bring him something loud.\n \n"),
""),
(198, ("The night of that Friday dinner, she knocked.", "found something to look at in the other direction."),
"The last of the forty boxes went out in the second week of November. Elijah had laid out every board in them by hand, with room around the part that overheated in June. Denny drove the last one to a grower outside Wenatchee. Once the truck was gone, Elijah packed his duffel.\nWhen it was dark he put the duffel in the Ranger and walked out to the pond. The frogs had gone quiet weeks ago. Geese were going over, south, calling to each other.\nGrace found him there. She had seen the duffel in the truck.\n\"It's heat,\" he said, with his back to her. \"The first thing I ever learned about a machine was heat. I cooked a tower in my apartment over it. I should have caught it. I should have tested it in a sealed box in the sun. I should have laid out that board myself. I should have.\"\n\"Elijah.\"\n\"Then the journal. Then Frank.\" He turned around. \"You guys need somebody better than me. You need somebody more qualified than me.\"\n\"You went and told him. Frank. You walked in there with the chart.\"\n\"You told me to.\"\n\"I tell everybody to. Nobody does.\"\nShe grabbed the front of his jacket. \"You can't leave.\"\n\"Why?\"\nShe made a face at him and shook her arm out hard, as if she were flicking water off her hand. She took his face in both hands and kissed him.\nHe stood there with his hands out from his sides.\n\"There,\" she said. \"Now if you leave, at least I got to do that.\"\nOff she went, fast, back toward the lights. Halfway to the gravel she yelled over her shoulder, \"I really hope you don't, though.\"\nA few steps later she turned halfway around and walked backward so she could see him. \"I really hope you stay.\"\nFacing forward again, she gave a little jump and a kick and hurried up over the rise.\nThe geese were still going over. Elijah stayed at the edge of the pond and listened to them.\n\nTwo weeks went by. Grace didn't bring up the pond, and Elijah didn't either. The duffel went back under the bed. On the Wednesday before Thanksgiving he took it out again and told everyone he was driving down to see his mother.\nHe was by the truck with his keys when Lou came up from the beds and sat on the shouse step, slowly, because of the knee.\n\"What are you going for?\"\n\"Just to see her,\" Elijah said. \"Just to show up. I need to go see her. It's the right thing to do.\"\n\"I mean, is it?\"\nElijah stared at him.\n\"What do you mean?\"\n\"You said so yourself. All she says is Barry.\"\n\"Yeah, but she can still recognize me. She still knows that I'm there.\"\nLou looked down at the gravel.\n\"Does she?\"\n\"I'm going.\"\n\"All right,\" Lou said.\nCurtis was leaning in the open door of the Ranger, reading the dash. \"Light comes back on, you call me,\" he said. \"Don't you dare call a dealer. Hose is in the glove box.\"\nSomeone in the kitchen trailer stepped back from the window.\nAbout a hundred miles south, past Yakima, the check-engine light came on.\nHe pulled off at the next exit, a truck stop with a diesel island, a restaurant and a sign by the door that said SHOWERS. He parked at the far end of the lot and left the engine running.\nThe light could mean two dollars of hose or twelve hundred dollars and a week at a dealer. He had enough money for gas there and back and for food. He did not have enough for a tow. The money for Ma's room was for Ma's room. Ahead of him were seven hundred miles with nobody on them. Behind him were a hundred, and a man who would fix it for nothing.\nHe went through what he could sell. Nobody had ever bid on the arms. His Telecaster was still in a pawnshop window on Fourth Street, and he couldn't afford to get it out. He could make something and post it on his page and wait.\nThe sign by the door said SHOWERS. In Stockton a shower at a place like this had cost seventeen dollars, and he had paid it in ones.\nIt was too big a risk.\nA single tear slipped out of his eye. He put the truck in drive, made a U-turn across the empty end of the lot and headed back north, disappointed in himself for a whole bunch of reasons.\n\nThe kitchen trailer was lit when he came up the gravel. Thursday was dinner for forty, and the peeling started on Wednesday night. Tyler saw the truck first.\n\"We thought you were going home.\"\n\"So did I.\"\nGrace was at the counter rolling out dough. She looked up when he came in, then down at the dough, and rolled it harder than dough needs. Her face did what it wanted anyway.\nMarta saw it from the coffee pot. Lou saw it from the sink, where he was peeling potatoes. He looked over at Marta, and Marta looked back at him, and he went back to the potatoes.\nAfter the dishes, Elijah sat on the trailer step, one step below Grace.\n\"Friday,\" he said. \"Bring it.\"\n\"Friday,\" she said."),
(198, "Write your models accordingly.\nChapter 27",
"Write your models accordingly.\n\nThat fall, it was Marta who told him about the music.\nShe had been short with him since the day Grace hauled his amp out onto the tailgate. Not mean. Short. She watched him around Grace the way she watched a weld cool, waiting to see where it would crack. Grace had explained it once, at the kitchen trailer, with her back to the shop so Marta couldn't read her lips. Marta had modeled when she was sixteen, in Los Angeles, for two years she never talked about. \"So she knows exactly what a guy with a guitar case looks like when he's looking at a girl,\" Grace said. \"And she's usually right. Don't take it personally.\"\nThen, one weekend in October, Grace went to a festival.\nShe had been talking about it for a month. Three nights in a field four hours south, bass music, no words in it. She left on a Friday morning with a tent and a cooler and her braid tied up in a bandana, and waved out the truck window at everybody, and the kitchen trailer was dark for three days.\nElijah stayed. Nobody asked him to go, and he would not have gone if they had.\nHe told himself that was fine. He told himself all of Friday and most of Saturday. He swept the shop twice and checked his phone for nothing. Then he thought about a field full of people who could dance, and somebody out there handing her a water bottle, somebody with a job and a bed frame and no notebook, and it was a stupid thing to think, and he thought it anyway.\nSaturday evening Marta found him at the roll-up door, holding a broom he had stopped using some time ago, looking down the gravel at the road.\nShe wiped her hands on a rag and stood next to him and looked at the road too.\n\"So,\" he said, to the road. \"Does Grace have… someone?\"\n\"What do you mean, someone?\" Marta said. \"Like a boyfriend?\"\n\"Or a girlfriend. Whatever.\"\nMarta turned and looked at him. \"Oh,\" she said. \"You like her.\"\n\"I,\" he said. \"She's. She's very intelligent.\"\nHis face went as red as the Telecaster he'd pawned. Marta looked at him for a long second.\n\"Very intelligent,\" she said. \"Okay, spreadsheet.\"\nSomething in her shoulders let go. She folded the rag, and when she spoke again it was in a voice he hadn't heard her use with him.\n\"She likes bass music,\" Marta said.\n\"Who?\"\nMarta gave him the look she gave a bad coupon. \"The loud kind. She goes every October. Has since she was nineteen. That's where she is right now.\" She tucked the rag in her back pocket. \"That amp of yours has Bluetooth.\"\n\"How do you know that?\"\n\"It says so on the front, spreadsheet.\" She went back inside. Over her shoulder, not turning around: \"Don't make me sorry.\"\n \nGrace got back Monday, sunburned and hoarse and happier than he had ever seen her. She came over the next Saturday night with her phone and a bag of the good chips. The amp had been sitting by the shouse door since he moved in, still under its blanket. She pulled the blanket off like she was unveiling something, and he let her, and he paired the phone himself so she wouldn't see his hands.\n\"You first,\" she said. \"Your favorite. Don't think about it.\"\nHe played her \"The Weight.\" She listened to the whole thing with her chin on her knees and a very straight face.\n\"That's music for buying a used truck,\" she said.\n\"That's The Band.\"\n\"Which band?\"\n\"The Band. That's their name.\"\nShe laughed so hard she had to put the chips down. \"That's the worst name I've ever heard. That's like naming your dog Dog.\" It was the truck song from then on.\n\"Okay. Your turn.\"\nShe played him something by Tipper. It started with a sound like a screen door in a storm and then dropped into a low, rolling thing that came up through the floor. The amp had not been built for this. It was built for guys on stools singing about rivers. It tried anyway. The grille buzzed on the low notes, and Grace turned it up.\n\"It's doing its best,\" she said.\n\"It's an acoustic amp, Grace.\"\n\"Shh. Here comes the good part.\" She got up and pulled the blanket off his bed and spread it on the floor in front of the amp, and lay down on it on her back. \"Get down here.\"\n\"Why?\"\n\"It's the optimal sonic zone. Obviously.\"\nHe lay down next to her. There wasn't a lot of blanket. Her shoulder was against his shoulder, and after a minute her head came over and rested against the side of his, and stayed. The stove was eight feet away, lit. She didn't look at it once.\nThey took turns until after midnight. She played him things that sounded like whales arguing in a parking garage, and he told her so. He played her Gillian Welch, and she said it sounded like being sad on a porch on purpose, and then asked him to play it again. Neither of them moved off the blanket.\nIt was the first sound out of that amp since before the pandemic. It wasn't his music, and he found he didn't mind. He found he didn't mind at all.\nOn Monday Marta looked at him over her welding hood for a long second and said nothing, which from Marta was practically a parade. He found out later that she'd told Grace the same week that the spreadsheet had a soft spot for old music and no idea what to do about it, and that somebody ought to bring him something loud.\nChapter 27"),
(198, "She told him on a Saturday morning, in his kitchen, wearing his shirt. Nobody at the Friday table had said one word about where she slept now.",
"She told him on a Saturday morning, in his kitchen, over coffee."),
# 199, Ch 20: the boxes waiting on summer, Barry, Wren's comeback (drafts/chapter-20.md)
(199, "of robot arms to a floor in Stockton in August.\nAt noon they sat on the tailgate",
"of robot arms to a floor in Stockton in August.\nOut in forty greenhouses, most of them two valleys over, the co-op's boxes were opening vents on their own every warm afternoon. Lou had ridden along with Denny on six of the deliveries and come home with a photo of each box bolted to its post, which he showed people whether they asked or not. The board inside every one of them was the one Elijah had let an AI lay out at midnight, and he hadn't told anybody. It was still a cool spring. It hadn't been very hot yet.\nAt noon they sat on the tailgate"),
(199, "\"There you go.\"\nShe'd eaten his too, he thought. A barn of buckets. Wheat she had no way to grind.",
"\"There you go.\"\nShe'd eaten the difference for him too, he thought. A barn of buckets. Wheat she had no way to grind.\n\"Where's she now?\" Lou said.\n\"A place back home with a rose garden. I call Sundays.\" Elijah hadn't planned on the rest of it. \"Mostly she asks for somebody named Barry.\"\n\"Huh,\" Lou said. \"Barry.\""),
(199, "\"Then here's somebody who'd call you back,\" Wren said.",
"\"The crews would call you back,\" Wren said."),
# 200, Ch 21: Denny's fans, Priya on wingnuts, the heat (drafts/chapter-21.md)
(200, "Elijah had been the internet once, for one winter,",
"Elijah had been all over the internet once, for one winter,"),
(200, "\"Guess I'm in it now,\" he said.\nChapter 22",
"\"Guess I'm in it now,\" he said.\nBy the middle of the week Denny was reading the comments out loud at lunch. He read them slowly, one finger on the screen, and every so often he held the phone up so somebody could see a name.\n\"Man in Ohio says his boy wants to go see a welder now.\" He scrolled. \"Lady in Tucson wants a hat.\"\n\"We don't have hats,\" Marta said.\n\"She knows. She wants one anyway.\"\nDenny hadn't stopped grinning in days. Priya had been eating with her soil book open beside her plate, and she closed it on her pencil.\n\"Be careful with that,\" Priya said. \"Some of them are going to be crazy people. Wingnuts.\"\n\"What do you mean?\"\n\"I ran for office, don't you remember? I lost by two hundred votes, and I still get weird letters. There are some wild people out there.\" She looked down the table at Elijah. \"I mean, you know what I'm talking about, don't you?\"\nElijah did. Somewhere in his phone, under a year and a half of everything else, was a message from a woman in Tulsa who drove a forklift and had thought she was the only one. The night it came, he had ended up sitting on the kitchen floor. Farther down the same phone was Mr. Ostrander, who had taught him Spanish for three years. *You're a liar. And you need to stop.* Above both of them sat the band chat, where Nate had sent a thumb and Wes had sent nothing. He had never deleted any of it.\n\"Yeah,\" he said. \"I know what she's talking about.\"\nDenny went back to the comments. He read the next few to himself.\n\nThe last week of June the valley hit a hundred and four.\nHector and Lupe Ochoa had the last of the north houses, up where the road bends, and a hoop house behind it where they started plugs for the network: cabbage, kale and broccoli for fall, six thousand of them in trays on wire benches. For eleven years Lupe had kept a clipboard on a nail by the door and written the temperature on it every morning and every afternoon. She stopped in May, when the co-op's box went up on the south end wall, in the sun, where the instructions said to put it.\nAt three o'clock she went out with the hose and found the vent shut and the box dark. The thermometer by the door read a hundred and thirty-one. Every tray on both benches had gone the color of wet newspaper.\nShe called Hector, and Hector called the co-op.\nBy the time Lou got there she had the plastic rolled up on both sides and was standing in the doorway with the hose running into the gravel. Lou walked the benches with her, down one side and back up the other. He put his hand flat on a tray and took it off again.\n\"Six thousand,\" Lupe said. \"That's October.\"\n\"I know it,\" Lou said.\nPatricia called Grace before the sun was down. The plugs had been the network's. Grace put her on speaker on the bench in the shed, so she wouldn't have to say any of it twice.\n\"It's the code,\" Patricia said. \"That program your boy wrote in one night. The one nobody can read.\"\nTyler had the Ochoas' box open in front of him, with Marta's card propped against the vise. *Power or brain? Halve it.* He kept his eyes on the board.\n\"It's all of it,\" Curtis said from the door. \"Code, board, box. We hung a machine on Hector's wall and went home.\"\n\"Nobody says what it was until it's been tested,\" Priya said. \"Not on the phone, and not tonight.\"\n\"I can have something up by morning,\" Denny said. \"People are going to ask. Better they hear it from us.\"\n\"Hear what?\" Priya said. \"We don't know anything yet.\"\nLou had come in last and was still holding his hat. \"Somebody should've been walking the houses the first hot week,\" he said. \"I'm the one who said ship them.\"\nElijah stood behind Tyler with his hands in his pockets. From there he could see the little square part beside the motor driver, packed in tight with nothing around it, right where the Iowa company's machine had put it.\n\"Check the battery first,\" he said.\nIt was on the card. Everybody in the shed knew it was on the card.\nGrace had been typing on her phone the whole time. She looked up. \"Eleven of the boxes have no shade on them,\" she said. \"Curtis and Lou, the six this side of the river, tonight. Tyler, the other five at first light. Until we know, a person opens those vents by hand. I've got two growers with spare plugs for Lupe.\" She went back to the phone. \"Patricia, are you still there?\"\nNobody had asked her for a plan. Elijah watched her make one while the rest of them argued about whose fault it was.\nThe battery was fine. Tyler pulled the board, carried it across the yard to the kitchen trailer and put it in the freezer. Ten minutes later it came back up on the bench, blinking, and opened the little test vent on the first try.\n\"It works cold,\" Tyler said. He turned the board over in his fingers. \"Code doesn't care if it's hot.\"\nHe looked up, past the phone and Patricia's voice coming out of it, straight at Elijah.\nOutside it was still ninety-eight degrees, and it was eight o'clock at night.\nChapter 22"),
# 201, Ch 22: the leak, the bell, Lou's IBM line, the pot, the hour of the funeral (drafts/chapter-22.md)
(201, "He stood in the gravel for a while after. A club soda with a lime. I had one of those. Mine was horses. He had not talked",
"He stood in the gravel for a while after and thought about Ray at the end of the bar with his club soda and lime. I had one of those, Ray had told him once. Mine was horses. He had not talked"),
(201, "He wanted his dashboards on his phone for the drive: uptime, coolant temperature, the channel numbers. A tunnel out,",
"He wanted the vent logs on his phone for the drive, every temperature Tyler had pulled off the boxes since the plugs cooked, where he could go through them at a rest stop with nobody looking over his shoulder. A tunnel out,"),
(201, "Then he pulled the logs, sitting on the running board, and did the math",
"Sitting on the running board, he pulled the logs and did the math"),
(201, "He thought about keeping it to himself. Then he pictured Marta finding out some other way. Then he went and rang the dinner bell, on a Saturday morning before it was light, which the co-op did not do, and stood in his funeral shirt in front of everyone it brought, and read them the timestamps. Then, because he was already standing there, he told them about the circuit board too. The startup out of Iowa, the two nights it took, and the two weeks of firmware he had blocked out to make it square. At the back of the crowd, Tyler looked at the floor.",
"He thought about keeping it to himself until he pictured Marta finding out some other way. So he went and rang the dinner bell, on a Saturday morning before it was light, which the co-op did not do, and stood in his funeral shirt in front of everyone it brought, and read them the timestamps.\nTyler was standing at the back, by the door. Elijah looked at him.\n\"There's one more thing,\" he said. \"The board in the boxes. I didn't lay it out. I gave it to a company in Iowa, and their machine did it in two nights, and I told you I'd go over every line in two weeks, and I didn't. The part that cooked Lupe's plugs is the one it packed in tight against the motor driver.\" He made himself say the rest. \"I saw it the night they cooked. Standing behind Tyler in the shed. I said check the battery.\"\nNobody moved. In April Marta had run her finger along the drawing of that board and called it theirs.\n\"You let me say that,\" Marta said. \"Ours.\""),
(201, "You brought their machine inside the wire. Pull the plug and melt it down.\"",
"You brought their machine inside the wire. Twice. Pull the plug and melt it down.\""),
(201, "You owe us the truth about what happened. We owe ourselves a setup that doesn't depend on you never having a bad Friday.\"",
"You owe us the truth about what happened. We owe ourselves a setup that doesn't depend on you never having a bad Friday.\"\n\"It was in the file,\" Tyler said, from the back. \"The company's name. I saw it in April. I figured he'd say.\"\nLou was by the door with his hat in his hands. \"My wife kept a thing on our fridge,\" he said. \"Some IBM slide from the seventies, God knows where she got it. A machine can't be held accountable. So a machine should never make a management decision.\" He turned the hat around once. \"I read it every morning for thirty years. I still said ship them.\"\n\"Then who decides when the machine's better at it than we are?\" Tyler said. \"It opened those vents every day for six weeks. Lupe quit checking because it was better than her.\"\n\"A person decides that,\" Lou said. \"And the person's name goes on it.\"\n\"And somebody checks the person,\" Priya said.\nBy noon it was on the board. On any day over ninety, somebody walked every house with a box in it, opened the vents by hand and signed the clipboard by the door. Elijah would lay out a new board himself, the slow way, and put it in all forty.\nGrace called Patricia from the kitchen trailer before breakfast. Elijah heard her through the screen. \"It wasn't Tyler's code. It was the board, and Elijah's the one who had it made.\""),
(201, "Reuben caught him by the truck after and looked at the shirt.",
"He went and packed. The duffel went in the Ranger, and the notebooks, and the amp. Last came his mother's pot, out of the kitchen trailer, wrapped in a dish towel.\nGrace was on the step when he came back out for his jacket. She looked in the bed of the truck.\n\"That's not a funeral bag.\"\nHe didn't have an answer for that.\n\"You can go to a funeral,\" she said. \"You're not taking the pot.\" She climbed into the bed of the truck, got the pot out from between the notebooks and carried it back inside against her chest, and the screen door banged behind her.\nFrom the shop door, Marta had watched all of it.\nReuben caught him by the truck after and looked at the shirt."),
(201, "Six CSA households canceled that week.",
"Six CSA households canceled that week, two hundred and ten dollars a week the co-op had been counting on through October."),
(201, "A few strangers wrote that it was the first one they'd read that a lawyer hadn't written.",
"A few strangers wrote that it was the first breach notice they'd seen that a lawyer hadn't written."),
(201, "Then she asked if there was anybody he should call,",
"When he was done, she asked if there was anybody he should call,"),
(201, "Then she put her hand on his forearm, the way she did with everyone,",
"She put her hand on his forearm, the way she did with everyone,"),
(201, ("On Monday he sent flowers, a day late,", "He didn't know if the name still meant anything to her.\n\"Barry?\" she said."),
"On Sunday at 9:40 he called the rose garden.\n\"She keeps looking at that door,\" the aide said. \"She's waiting on her Sunday company.\" He took it to mean the church. She held the phone by his mother's ear.\nHe told her Ray McGrath had died, and that he had not gone down. He didn't know if the name still meant anything to her.\n\"Barry?\" she said.\nAt eleven he was in the shed with the crawler logs open, reading who had copied what, line by line. The clock in the corner of the screen went to 11:00. At St. Rose they would be standing up for the first hymn. He kept reading.\nOn Monday he sent flowers, a day late, with a card he rewrote four times. He texted David that he was sorry. David didn't answer."),
# 202, Ch 23: the land or the Ochoas, Grace tells them, the rule about where you eat, Lou at the window (drafts/chapter-23.md)
(202, "The pattern assembled itself the way patterns do, all at once, on the third evening.",
"He saw the pattern all at once, on the third evening."),
(202, "He knew one kind of tenant that needed all three. He had a power bill in a box that said so, and Patricia had stood in the shed and named one going in two counties down.",
"He knew one kind of tenant that needed all three, and Patricia had stood in the shed and told them about one going in two counties down: a data center."),
(202, "Irene had gotten her first letter five weeks ago. The data couldn't change that. It could only tell them how little time they had.",
"Irene had gotten her first letter five weeks ago."),
(202, "\"It's not a data problem,\" Reuben said, already dealing folders around the table like cards. \"It's a people problem. Fortunately,\" and here he almost smiled, \"I have been waiting my entire adult life for this exact fight.",
"\"You can put the pointer down,\" Reuben said, already dealing folders around the table like cards, and here he almost smiled. \"I have been waiting my entire adult life for this exact fight."),
(202, "The down payment would take the channel's first real surplus and the greenhouse-controller money. Future payments would have to come from future work. Denny looked from one column to the other. He tapped the second column. \"And then we have to keep the promise.\"\n\"Every month,\" Reuben said, pushing his glasses up onto his forehead.",
"The down payment would take the channel's first real surplus, all of it. Denny looked from one column to the other. He tapped the second column. \"And then we have to keep the promise.\"\n\"Every month,\" Reuben said, pushing his glasses up onto his forehead. \"Miss three in a row and the ground goes back to Irene. After Irene, it goes to Dale.\"\nGrace had been reading the first column upside down. \"That's Hector and Lupe's money. We told them in July we'd cover October.\"\n\"We did,\" Lou said.\nPriya took the pencil from behind her ear. \"Can we do both?\"\n\"Not this year,\" Reuben said.\n\"Then it's the land,\" Curtis said. \"No land, there's no October for anybody. Ochoas included.\"\nWren had her hand on her chest. \"So the ones it cost get paid last.\"\nNobody argued with her. Elijah started to say he would cover it himself, and stopped. He didn't have it.\nThey voted after the pie. It went for the land, and Grace's hand was one of the first ones up.\n\"I'll tell them,\" Elijah said.\n\"No,\" Grace said. \"I'm the one who asked them to grow for Patricia.\"\nShe drove up to the north houses after breakfast. Elijah was at the bench by the shed's open door, laying out one of the new boards, and from there he could see the road where it bends. Her truck sat at the Ochoas' most of an hour. When it came back down she parked by the kitchen trailer and stayed in the cab with both hands on the wheel before she got out."),
(202, "Dale attended the kitchen-table meeting by speakerphone, from Phoenix, and he was not wrong by his own lights.",
"That evening Reuben, Marta and Elijah sat down at Irene's kitchen table, with Dale on speakerphone from Phoenix, and Dale was not wrong by his own lights."),
(202, "It turns commons into fences. Enclosure. Consolidation. Urban renewal. This week it's a string of companies with one mailing address and a flyer with a sunset on it. It has never run in your mother's favor.",
"It turns commons into fences. It has never run in your mother's favor."),
(202, "Reuben didn't have that one in a folder.\nLou had come along and stood by the door with his hat in his hands. He had lost his pears outside Ukiah to one buyer and one price. He hadn't said a word all afternoon.",
"Reuben didn't have that one in a folder."),
(202, "I want my questions written down before anybody signs.\"\nBy the door, Lou tugged his hat back on.",
"I want my questions written down before anybody signs.\""),
(202, "Irene Calder did not want to leave her house. By dark they had a list on the back of the pie box: who drove her to the doctor and on which Thursdays, who looked in on her when it froze, whose number Dale could call. Grace read it to Dale over the phone that night. Elijah drove by twice on errands he'd invented. The second time they were both laughing, and Grace had her hand on Irene's arm.",
"Irene Calder did not want to leave her house.\nElijah drove by twice on errands he'd invented. The second time they were both laughing, and Grace had her hand on Irene's arm.\nOnce, years ago, he had gotten involved with someone he worked with, and this felt the same. He learned a long time ago not to date where you eat, but there was just something so alluring about Grace. He ate at her table every night. He went on to the feed store and bought a bag of chicken scratch the co-op didn't need.\nBy dark the two of them had a list on the back of the pie box: who drove her to the doctor and on which Thursdays, who looked in on her when it froze, whose number Dale could call. Grace read it to Dale over the phone that night."),
(202, "The review took longer than Elijah wanted. Irene asked questions he hadn't thought to put in the dashboard. So did Dale. By the time they agreed, several pages had changed. Reuben carried the completed documents to the county himself, and Doreen at the auditor's window stamped them at 11:04 on a Tuesday morning. The letters from Sacramento kept coming for a month. Irene brought one to dinner and left it unopened beside the salt.\nThe dashboard had found the pattern. It had not closed the deal.\nElijah wrote the number in the notebook anyway, under Sal's rule, where the important numbers lived.\nPARCELS HELD IN TRUST: 1.",
"Irene asked questions Elijah hadn't thought to put in the dashboard, and so did Dale. By the time they agreed, several pages had changed. Reuben carried the finished documents to the county himself. Lou drove him, and Elijah came along.\nDoreen at the auditor's window stamped them at 11:04 in the morning. Lou put his hand flat on the stack and kept it there while she made the copies.\nThat night Elijah wrote the number in the notebook, under Sal's rule, where the important numbers lived.\nPARCELS HELD IN TRUST: 1.\nThe letters from Sacramento kept coming for a month. Irene brought one to dinner and left it unopened beside the salt."),
(202, "Reuben had also brought the less thrilling pages: taxes, insurance, and what happened if they ever missed a payment.",
"Reuben had also brought the less thrilling pages: taxes and insurance."),
(202, "What's on this table is that machine in reverse. Your mother gets to decide what she wants to keep. It's her porch,",
"What's on this table is that machine in reverse. It's her porch,"),
(202, "Writing things down. Soil, water, who gets fed. They're very thorough. They keep it all in one place.",
"Writing things down. Soil, water, who gets fed. They keep it all in one place."),
(202, "in the tone of a woman entering evidence. Then she drew the folders toward her.",
"in the tone of a woman entering evidence. She drew the folders toward her."),
# 203, Ch 24: the containers paid for in April, Hector at the fire, Marta at the door, the pond (drafts/chapter-24.md)
(203, "The containers came up the hill on a tilt-bed in the last week of August, one at a time.",
"The first new board was done in the middle of August. Elijah drove it up to the north houses himself. Lupe met him at the hoop house door with the clipboard, and the temperature was on it twice a day again, in her writing.\nHector held the ladder while Elijah put the box back up on the end wall, in the shade this time. Neither of them said anything until it was done.\n\"Took you a month,\" Hector said.\nLupe held out the clipboard. At the bottom she had ruled a new line, INSTALLED BY. He signed it.\n\nThe containers came up the hill on a tilt-bed in the last week of August, one at a time. The co-op had paid for them in the spring, before the plugs cooked."),
(203, "every cut was photographed and every dimension logged, because the deal the co-op had made with itself was that nothing got built only once.",
"every cut was photographed and every dimension logged, because the deal the co-op had made with itself was that anybody could build the next one from the notes."),
(203, "He mounted leak sensors low in the wet room. He built the little dashboard",
"He built the little dashboard"),
(203, "and light went through the two boxes and made them one room. Sixteen feet of open span where no room had been.",
"and light went through the two boxes and made them one room."),
(203, "Tyler sat on the floor. Curtis stood",
"Tyler sat on the floor. Hector Ochoa came for half an hour, ate a handful of Lou's walnuts standing up and went back up the road. Lupe didn't come. Curtis stood"),
(203, "if the place were his to run.",
"if the co-op were his to run."),
(203, "By eleven that first night everyone had gone but Grace.\nShe was still in the doorway. He was banking the fire.",
"By eleven that first night everyone had gone but Grace and Marta. Marta stopped in the doorway beside Grace to zip her jacket.\n\"Pick a side of that door,\" Marta said. \"You're heating the whole valley.\" She went down the steps without waiting for an answer.\nGrace stayed where she was. He was banking the fire."),
(203, "\"He let me.\"\nElijah put a split of oak in and shut the door on it. Then he told her about the Bear Flag.",
"\"He let me.\"\nShe set her mug on the floor by the door. \"I need some air.\"\nHe went with her. The pond was down past the pump house, black and still, with the shouse's one lit window lying on top of it. Crickets were going in the dry grass.\n\"My first month here, I lay up there listening to this pond and thought, this is a pretty good bleed-out spot,\" he said.\nGrace turned all the way around to look at him.\n\"I was kidding,\" he said. \"Mostly.\"\nShe picked up a rock, wound up like a Little Leaguer and threw it. It went about four feet and landed in the mud with a smack.\n\"I was going to skip that,\" she said.\n\"I could tell.\"\nHe laughed, and she did too. When they stopped, her shoulder was against his arm. She looked up at him.\nSomething came crashing through the cattails. The dog from the Friday dinners shot out of the dark, ran straight into the pond, ran straight back out and shook itself off all over both of them.\nGrace shrieked. Elijah stood there dripping.\n\"That's on you,\" she said. \"You and your bleed-out spot.\"\nThe fire had burned down while they were gone. Grace sat back down in her chair, eight feet from the stove, with her wet shoes stuck out toward it. Elijah put a split of oak in and shut the door on it, and told her about the Bear Flag."),
(203, "Grace held her hands out to the stove and didn't say anything for a while.",
"Grace held her hands out to the stove."),
(203, "But it was also Elijah's. Nobody made a ceremony of saying so. He'd had",
"But it was also Elijah's. He'd had"),
(203, "Elijah went to his lane, which turned out to be real work. Before",
"Elijah went to his lane. Before"),
# 204, Ch 26: the rover and the argument about labor, Ma's fall, the pay vote, Mrs. Delgado, the October night at the pond (drafts/chapter-26.md)
(204, "The robot was Tyler's idea, and Marta's rails, and Elijah's sensors.\nIt was a gantry, a steel bridge that rode on two tracks down the length of a bed, with an arm that could come down anywhere in it. It could drop a seed,",
"The robot was Tyler's idea.\nHe had two picked out, and he brought both to the Friday table on his phone. One was a tall steel frame on wheels that straddled a whole bed, the kind the big growers ran, and it cost more than the co-op had cleared all spring. The other was a kit called a JetAuto Pro: four fat wheels that could roll sideways, a little arm on top, a spinning lidar the size of a hockey puck, and a camera. It would have fit in an apple box.\n\"Could I pick it up?\" Lupe Ochoa said.\n\"With one hand,\" Tyler said.\n\"Then that one. If it does something stupid in my field, I want to be able to carry it out.\"\nReuben kept the books, and he said the little one was also the one they could pay for. They bought the little one. Elijah wired a second camera onto a mast for it.\nIt could drop a seed,"),
(204, "They got it running on a Saturday in May. It rolled out over the lettuce in the evening light,",
"They got it running one evening in May. It rolled out along the lettuce in the last of the light,"),
(204, ("Not everybody thought it was solarpunk.", "and it was one of the better mornings Elijah ever had up there."),
"""Irene Calder had driven her golf cart over special. She watched the thing water one seedling and skip the next, and she said Walt would have sold a kidney for it. "He spent forty years on a tractor seat watering the weeds right along with the hay. He'd have named it."
Lou said he'd marry it if it ever learned to pick. Tyler said give him a year.
Not everybody thought it was solarpunk.
The opinions came in the way they always came in up there, sideways, at the wash station, while everybody had their arms in cold water up to the elbow. It was the first big lettuce cut of the year. There were nine of them on the line and four hundred heads to get boxed by noon.
Wren said it made her sad to look at. She said it very gently, the way she said everything. She said food carried the feeling of whoever raised it, and she didn't know what an arm felt. Then she said, "There's nine of us on this line who came up here to do this. Who's the arm for?"
"For what the nine of us can't get to," Lou said. "We're not being replaced, we're expanding our capacity. We're having productivity gains."
Elijah had a head of lettuce in each hand. Augmentation, not replacement. Devendra had said that to him at the coffee machine at Claypot, more than three years ago. Value flows back to creators through productivity gains. That one was the CPO's, to a full room. Now it was Lou saying it, with his arms in the wash water, and Lou meant every word.
"It's got a camera on it, Lou," Curtis said. "Today it's looking at lettuce."
"What do you think it's going to look at tomorrow?" Lou said. "Your basement?"
"I'm just saying. Every one of those movies starts with lettuce," Curtis said, shaking the cold water off his hands. "Then it's Skynet."
"Wouldn't it make more sense for it to just leave?" Wren said.
The whole line stopped. Nine people with their arms in cold water turned to her, and Curtis looked at her like she'd lost a wheel.
"I mean it," she said. "Sure, there's a lot here. But there's more out there than we could ever use. Every rock in the sky. The sun puts out more in one second than we've burned in all of history. Why would it fight us over one little planet when it could have all of them? It doesn't need air. It doesn't need us."
"There's plenty down here worth having," Curtis said.
"I'm not saying there isn't. I'm saying there's more out there, and it never runs out, and there's no little monkeys up there to get in its way." She rinsed a head and set it in the box. "Why wouldn't it build itself a ship and go?"
Nobody had an answer for her. Elijah didn't either. It was in the first notebook, in his own handwriting, under the seven stages: *7. It leaves.* He had never heard anybody else say it out loud.
Curtis wasn't done. "Fine. Say it leaves someday. First it's a camera on the lettuce. Next thing you know, we got government surveillance drones flying all over us." He pulled his arms out of the tub. "I need to go build an EMP."
He walked off up the gravel, dripping. Lou watched him go and shook his head.
"You're not actually going to let him build an EMP, are you?" Priya said. "That's wildly illegal."
"I'll go talk to him," Lou said. He dried his hands on his pants and went.
Out at the end of bed three the rover sat with its arm tucked up. On top of its mast was the little black camera Elijah had wired in himself, at night in the shed, pleased with it. He turned the head of lettuce over in his hands. He started to say something to Wren, and didn't.
They got all four hundred heads out by noon.\nCurtis turned up at the shed the next night. He didn't mention the EMP.\n\"If that thing's going to have a camera,\" he said, \"I want to see what it sees.\"\nElijah put the feed up on the laptop. It was lettuce. Curtis watched lettuce for a full minute.\n\"Show me how you tell it where to go.\"\nBy midnight Curtis had written the first ten lines of code of his life, and the rover drove to bed four and back because he had told it to. He was at the shed most nights after that.\nThat Saturday he ran the brush hog along Praether's fence line, the way he had once a month since the arms went into the barn. Praether watched from the porch until he was done, then walked down to the mailbox.\n\"Hear you got a robot,\" he said.\n\"It waters lettuce.\"\n\"So did ours, the first year.\" He held up an envelope from the stack. \"They gave us pills in ninety-one and said take them. Then they blew an ammo dump upwind of us, full of nerve gas, and wrote and told me about it six years later. They still write.\" He put the envelope in his coat. \"Real polite letters.\" He went back up the drive."""),
(204, "The rain came Thursday night, and it came all night.",
"Two nights later the rain came, and it came all night."),
(204, "The water had shoved the side board out in a long belly, and the board had taken the track with it. The gantry sat at the head of the bed with one wheel up on the kink. It had tried to cross. The motor buzzed and quit, and buzzed and quit.",
"The water had shoved the side board out in a long belly. The rover steered by the side boards, and it had followed the belly off its line and put a front wheel down in the water. The motor buzzed and quit, and buzzed and quit."),
(204, "I tell it where the track bends. It slows down there and takes the bump. Ten minutes.",
"I tell it where the board bends, and it drives straight through. Ten minutes."),
(204, "\"Your stakes are in mud, man,\" Lou said.",
"\"Your stakes are in mud, my man,\" Lou said."),
(204, "and he held it there while Lou drove the stake behind it. Then the next one. Then they bolted the track back down, and Elijah's arms were shaking.",
"and he held it there while Lou drove the stake behind it, and the next one, and the one after that. By the time the board was straight, Elijah's arms were shaking."),
(204, "The gantry came down the bed at its usual crawl. It rolled over the place where the kink had been and didn't notice.",
"The rover came down the path at its usual crawl. It rolled past the place where the belly had been and didn't notice."),
(204, "It was coming, all right. It was coming down a rail he'd just spent an hour holding straight.",
"It was coming, all right, the thing he'd spent three years warning people about. It was coming down a bed he'd just spent an hour holding straight."),
(204, "with the gantry's firmware open", "with the rover's firmware open"),
(204, "By the second week he was finding things before Elijah did.",
"""By the second week he was finding things before Elijah did.
On the sixth day the rose garden called in the middle of the afternoon, on a day that wasn't Sunday. Elijah took it outside the roll-up door.
"Your mother had a fall," the aide said. "They took her over to the hospital. They're doing pictures of her hip."
He had the Ranger's keys in his hand. He didn't remember getting them out.
"Maybe I need to go home right now," he said.
Grace had come out behind him. "Go," she said. "I'll drive. We'll take my truck."
Through the door he could see Tyler at the bench with the rover's file open, six days into code nobody else on the place could read. Out in forty greenhouses were forty new boards, and it was June again.
He stood there with the keys. Grace waited on the gravel with her own in her hand until it got dark, and then she went in.\nNobody called back that evening. He sat up in the shed with his phone face up on the bench and Tyler's code open in front of him, and didn't read a line of it.\nThe aide called at seven the next morning.
"She's all right," the aide said. "Nothing's broken. She's bruised up and cross about it and back in her room. Don't you worry. She's got company."
He took it to mean the church.
He put the keys back in his pocket and went to make two coffees."""),
(204, "The pay finally went to the table that summer, more than a year late.\nGrace told him herself. She told him on a Saturday morning, in his kitchen, over coffee.",
"""Grace had brought his pay to the table the Friday after Thanksgiving, the way she'd said she would. The surplus had gone into the land, so it waited for a vote until July, more than a year after he came.
All that spring and summer, at the Friday table, the two of them kept catching each other looking and looking away. Everybody saw it but Denny. Lou would glance down the table at Marta, and Marta would go back to her plate.
Grace had knocked once, at the pond. By her own rule the answer was his to give, and she didn't knock again.\nHis side of it he never said out loud. If the pay vote passed, he would be the one person at that table drawing a check, and Grace was the one bringing it to a vote. Greedy little grub, Melody would have said, and he would have heard it every time Grace touched his arm.
Grace told him about the vote herself, one morning in his kitchen, over coffee."""),
(204, "Curtis wanted to know why you and not Denny. He's not wrong.",
"Curtis wanted to know why you and not Denny. He asked it looking at me. He's not wrong."),
(204, "Reuben cut the first check that Friday.", "Reuben cut the first check that week."),
(204, "Four inches of nice crumb where the mulch had rotted in, then dust, then at ten inches the old pan,",
"Ten centimeters of nice crumb where the mulch had rotted in, then dust, then at twenty-five the old pan,"),
(204, "July had cooked the top inch of every bed the same, and his dashboard had taken that one reading and spread it in all directions.",
"July had cooked the top of every bed the same, and his dashboard had read that one thin layer and called it the whole bed."),
(204, ("That fall, it was Marta who told him about the music.", "and that somebody ought to bring him something loud."),
"""§H1 Pondwater
That fall, it was Marta who told him about the music.
She had been short with him since Thanksgiving. Not mean. Short. She watched him around Grace the way she watched a weld cool, waiting to see where it would crack. Grace had explained it once, at the kitchen trailer, with her back to the shop so Marta couldn't read her lips. Marta had modeled when she was sixteen, in Los Angeles, for two years she never talked about. "So she knows exactly what a guy with a guitar case looks like when he's looking at a girl," Grace said. "And she's usually right. Don't take it personally."
Half the Ochoas' fall starts hadn't taken that year, and the harvest was short of hands. Elijah rode the route with Grace and Curtis once. At the Coyote Flat stop a woman in house slippers named Mrs. Delgado met the truck at her gate and asked Grace to carry the box in, because of her hands. Grace set it on the counter and moved the insulin back to the door of the fridge, where it went.
At dinner one night Grace said she wasn't going to her festival this year, and that it was fine, and she left before the pie.
The next evening Marta found him at the roll-up door, holding a broom he had stopped using some time ago, looking down the gravel toward the kitchen trailer.
She wiped her hands on a rag and stood next to him and looked too.
"So," he said, to the gravel. "Does Grace have… someone? Now, I mean."
"What do you mean, someone?" Marta said. "Like a boyfriend?"
"Or a girlfriend. Whatever."
Marta turned and looked at him. "She kissed you at that pond a year ago, spreadsheet, and you're asking me." She shook her head. "Oh. You still like her."
"I," he said. "She's. She's very intelligent."
His face went as red as the Telecaster he'd pawned. Marta looked at him for a long second.
"Very intelligent," she said. "Okay, spreadsheet."
Something in her shoulders let go. She folded the rag, and when she spoke again it was in a voice he hadn't heard her use with him.
"She likes bass music," Marta said.
"Who?"
Marta gave him the look she gave a bad coupon. "The loud kind. There's a festival in a field four hours south, three nights, no words in the music. She's gone every October since she was nineteen. Not this one." She tucked the rag in her back pocket. "That amp of yours has Bluetooth."
"How do you know that?"
"It says so on the front, spreadsheet." She went back inside. Over her shoulder, not turning around: "Don't make me sorry."
He had dated a few festival girls in the past. That hadn't exactly gone so well for him. But Grace seemed like she had it all together.

The amp had been sitting by the shouse door since he moved in, still under its blanket. The night after that he carried it out to the Ranger, drove it down past the pump house to the pond and set it on the tailgate, facing the water. He remembered what she had told him his first month, about her dad and a porch.
Then he walked up to the kitchen trailer and knocked.
Grace came to the door with a dish towel over her shoulder. "What?"
"Bring your phone," he said.
When she saw the amp on the tailgate she stopped walking. She pulled the blanket off like she was unveiling something, and he let her. His hands shook a little when he paired her phone.
"You first," she said. "Your favorite. Don't think about it."
He played her "The Weight." She listened to the whole thing sitting on the tailgate with her chin on her knees and a very straight face.
"That's music for buying a used truck," she said.
"That's The Band."
"Which band?"
"The Band. That's their name."
She laughed so hard she nearly fell off the tailgate. "That's the worst name I've ever heard. That's like naming your dog Dog." It was the truck song from then on.
"Okay. Your turn."
She played him something by Tipper. It started with a sound like a screen door in a storm and then dropped into a low, rolling thing that came up through the truck bed. The amp had not been built for this. It was built for guys on stools singing about rivers. It tried anyway. The grille buzzed on the low notes, and Grace turned it up.
"It's doing its best," she said.
"It's an acoustic amp, Grace."
"Shh. Here comes the good part." She slid off the tailgate, spread the amp's blanket on the grass in front of it and lay down on it on her back. "Get down here."
"Why?"
"It's the optimal sonic zone. Obviously."
He lay down next to her. There wasn't a lot of blanket. Her shoulder was against his shoulder, and after a minute her head came over and rested against the side of his, and stayed.
They took turns until the light was gone off the pond. She played him things that sounded like whales arguing in a parking garage, and he told her so. He played her Gillian Welch, and she said it sounded like being sad on a porch on purpose, and then asked him to play it again. Neither of them moved off the blanket.
It was the first music out of that amp in three years. It wasn't his music, and he found he didn't mind. He found he didn't mind at all.
"We should start a band," Grace said. "Whales and a sad guy on a stool."
"We should call it Pondwater!"
She laughed until she had to roll onto her side, and he laughed because she was laughing. When it wore off they were both looking up at the first stars.
"My dad had one of these," she said, toward the amp.
"You told me. My first month."
"He started drinking when I was in high school. Then it was harder stuff than drinking. I made a lot of weird choices back then. I was a little festy girl." She smiled at the sky, and stopped smiling. "He's still on that porch. Numb. Barely himself anymore. The father who raised me is gone. The one I love, the one I grew up admiring. What's there now is a husk, a shell, a container for my father's soul. I grieved him and let go of him a long time ago."
That was all she said about it.
He turned onto his elbow. She was already looking at him. He kissed her.
"A year," she said, after. "A whole year, Elijah."
"I know."
She pulled him back down by his collar.
In the morning she was in his kitchen, wearing his shirt and drinking coffee.
Later that morning Marta looked at him over her welding hood for a long second and said nothing, which from Marta was a blessing."""),
# the rover in Ch 32 and 33 (the Ch 38 line is left for CT)
(204, "Tuesday it could do the whole gantry file", "Tuesday it could do the whole rover file"),
(204, "the way he'd learned on the gantry the summer before.", "the way he'd learned on the rover the summer before."),
(204, "The gantry was parked at the end of bed four with", "The rover was parked at the end of bed four with"),
(204, "She was looking at the gantry.", "She was looking at the rover."),
(204, "She smiled at the gantry, and then she didn't.", "She smiled at the rover, and then she didn't."),
# Continuity fixes of 26 Nov (eighth chat), after the readers' audit; old text in Chapters 19, 21, 22, 25 and 26
(199, "The forty units shipped in June.", "The forty units shipped in May."),
(200, "By Saturday two other channels had Denny's story up anyway", "Within days two other channels had Denny's story up anyway"),
(201, "For five weeks nothing went wrong.", "For five weeks nothing went wrong with the Crucible."),
(198, "Elijah watched the store die for nine months before it died", "Elijah watched the store die for eight months before it died"),
(198, "the chart he'd sat on for nine months", "the chart he'd sat on for eight months"),
(198, "bought at honest wholesale, not vulture pennies, and a paid job.", "bought at honest wholesale, not vulture pennies, and a paid job once the library could carry one."),
(198, "He had lost a register and gained forty hours a week, and he spent them building", "He had lost a register and had all week now, and he spent it building"),
(198, "and a twenty-year-old had the name.", "and a nineteen-year-old had the name."),
(204, "Patricia called Grace on day nine. Her grant reports", "Patricia called Grace on day nine, in tears. Her grant reports"),
# 205, Ch 17: the arms go to Richard Praether's (CT, 26 Nov; changes edit 88) (drafts/chapter-17.md)
(205, ("On the fourth day he asked Grace if the dry end of the shed was still free.", "Some nights he went and looked at them. He couldn't have told you what for."),
"""On the fourth day Grace asked about the arms. She had offered the dry end of the equipment shed in her first message, after she saw his post about them. He told her the rest of it: two crates in a storage unit off Highway 99, a lien sale at the end of the week, and nothing to pay it with. He didn't say yes to the shed. Those crates were the only things he owned that were worth anything, and he had known these people four days.
Grace didn't argue. That evening she told him a man named Lou would cover what he owed on the unit.
"He says pay him back when you can. And he says keep it between the three of us."
"Why?"
"He didn't say. That's Lou. You'll meet him."
A place to put them came from a kid at a cash register. Marta had sent Elijah into Ardell for a pump seal, to the hardware store on the square, and the kid ringing it up had a laptop open under the counter with the sound off. He was teaching himself something between customers. Elijah had been that kid, in a parking lot, with a phone propped on a steering wheel. He hadn't meant to ask anybody. He asked him.
"Is there anywhere around here to keep a couple of big crates? Cheap?"
"There's the U-Store. It's like ninety a month." The name on his apron said TYLER. "Or old Praether, out past the grange. He's got a pole barn with nothing in it. He comes in here for nails and pays in quarters." He handed over the seal. "Honk before you go up his drive. Like, a lot."
The arms came up the day before the lien sale. Somebody had a flatbed, because up there somebody always had a flatbed, and Lou knew a man outside Stockton with a baler that needed to come north anyway. Grace and Elijah met the flatbed at the grange hall and led it out the county road in the Ranger.
The old man's yard was covered in foliage and rust buckets. Wavering somewhere between "Haunted House" and "condemned by the city," Richard Praether's property was, for lack of a better word, a dump.
Grace leaned on the horn until a man came around the side of the pole barn. He stopped where he could see the road and all three of them at once. He was seventy or so, in a canvas coat, with a white beard he had plainly cut himself. A burn barrel was going behind the house. The smoke lay down flat across the yard and got into everything. When he rolled the barn door back, the barn had kept its own air, cold gear oil and mouse.
"What's in them?" Praether said.
"Arms." Elijah heard it. "Robot arms. Out of a cannery. They put cans in boxes."
"I know what they put in boxes."
One of the rust buckets was a loader, and it started on the first try. He had the first crate up on the forks when a tie-down let go with a bang. Praether was on the ground behind the front tire before the strap finished falling. He got up slowly and brushed off his knees. Nobody said anything.
"I can't pay much," Elijah said, when the door was shut. "I can work."
"You know what a brush hog is?"
"Yes, sir."
"One Saturday a month, then. Don't come to the door." Praether looked at the barn, and at the two of them. He put one finger up. "Mark my words." His voice came up, like a man calling across a field. "Beware the military! They never built one thing in their lives. They wait till some nice kid builds something useful, and they come around with a check. Somebody always wants the thing that works." He pointed the finger at the barn, and then at Elijah. "Don't say nobody warned you." His voice dropped again. "They'll be polite about it. That's how you'll know."
Grace got the truck as far as the end of his drive before she laughed.
"Did he say beware?"
"He said beware."
"He's the guy at the gas station. In the movie." She put one finger up. "Don't go up to the lake, kids. Mark my words."
"What happens to the ones who go up to the lake?"
"Nothing good, Elijah."
The mailbox leaned on its post at the end of the fence, where the boards gave out. Grace stopped the truck beside it. An envelope lay in the weeds under the box, gone soft with rain. She got out, picked it up and read the corner of it, and the grin went off her face before she put it in the box.
"What?" Elijah said.
"Department of Veterans Affairs." She shut the little door. Neither of them said anything until the grange.
Some nights he drove out and looked at the barn from the road. He couldn't have told you what for."""),
(198, "Elijah laid the chart on the worn wood and confessed to it. Nine months, the distributor,", "Elijah laid the chart on the worn wood and confessed to it. Eight months, the distributor,"),
(198, "the nine visible months of it.", "the eight visible months of it."),
(199, "Those boxes go out in June either way.", "Those boxes go out in May either way."),
(199, "the mainstream devices we're starting to see come out, Elijah.", "the mainstream devices we're starting to see come out, spreadsheet."),
# 206, Ch 27: what the farm lives on, the knockoff, the pledge and the Ochoas, Thanksgiving 2026 (drafts/chapter-27.md)
(206, "Denny had filmed the whole shouse build the summer before, the way he documented everything by then,", "Denny had filmed the whole shouse build, the way he documented everything by then,"),
(206, "It posted on a Thursday night. Elijah did the pipes and went to bed.", "It went up that night. Elijah wrapped the outside taps against the frost and went to bed."),
(206, "That was all of it. He read it three times, then typed I'm sorry I missed and looked at it, and deleted it. Then he pocketed the phone to answer later, when he could think, and went to find Grace.", "That was all of it. He typed *I'm sorry I missed* and looked at it, and deleted it. He put the phone in his pocket to answer later, when he could think, and went to find Grace."),
(206, "\"The route's got no money past June.\"\n\"I know.\"", "\"The route's got no money past June.\"\n\"I know.\"\nThe co-op lived on four things: the CSA boxes, what Patricia's network bought, a stall at the farmers market in Ardell, and lately the channel. The route lived on grants, and the last one ran out in June."),
(206, "Every winter there's somebody on that route we don't get to in time. I can tell you their names.", "Every winter there's somebody who ought to be on that route and isn't yet. I can tell you their names."),
(206, "Then somebody made copying cheap, and I'm just saying the folks who printed them still charged for the book.", "Then somebody made copying cheap, and the folks who printed them still charged for the book."),
(206, "Monday morning he stood in the shed at dawn with the coffee", "The morning they went up he stood in the shed at dawn with the coffee"),
(206, "Tyler found the listing and threw it up on the big screen. Nobody said anything about it.", "Tyler found the listing and threw it up on the big screen.\n\"Well,\" Grace said. \"Somebody's getting paid for June.\"\n\"He'll sell ten,\" Frank said. \"Then the eleventh guy calls Marta.\"\nMarta was looking at the bottom corner of the drawing, where her note had been. \"They cut my note off,\" she said, and went back to her plate."),
(206, "The argument came to the table anyway. Patricia's network had sent every vendor a pledge to sign. No generated code, no generated text, a little green leaf you could put on your label. At the bottom it said every question you asked one of those things drank a bottle of water. Tyler read it out in a flat voice.", "The argument came to the table anyway. Patricia's network had sent every vendor a pledge to sign, and the co-op was a vendor. No generated code, no generated text, no machine handling the food between the field and the box, and a little green leaf you could put on your label. The first page said why without naming anybody: in June a grower in the network had lost a house of starts to a controller nobody could read. At the bottom it said every question you asked one of those things drank a bottle of water. Tyler read it out in a flat voice."),
(206, "Priya didn't argue with him. She took the pencil from behind her ear and wrote something small on the back of the pledge, and folded it, and put it in her shirt pocket.", "Priya didn't argue with him. She took the pencil from behind her ear and wrote something small on the back of the pledge, and folded it, and put it in her shirt pocket.\nLupe Ochoa signed hers at the table. Hector pushed his back across the plywood without a name on it.\n\"Nobody was checking,\" he said. \"Your leaf don't fix that.\"\nThe co-op signed the week after, once Tyler had told the table he'd read every line of the rover's code by hand that June."),
(206, "He'd never answered David. He remembered it then, with the bowl in his hands, and it was three weeks old, and he didn't know how to start.", "He'd never answered David. He remembered it then, with the bowl in his hands, and it was three weeks old, and he didn't know how to start.\nThanksgiving came the week after. He meant to drive down, and he had the Ranger's oil changed for it. Then the route needed a second driver for the holiday boxes, and he said yes before he had thought about it. After the kitchen trailer fed forty, he and Grace ate a chicken off one plate in her room over the laundromat in Ardell. Their coats had soaked up the kitchen all afternoon, sage and turkey fat, and the little room filled with it the minute the door shut.\nThat night he wrote Ma a letter. He told her about the stove and the rover and the woman he'd had dinner with. He mailed it in the morning, to the rose garden, care of the aide."),
(206, "Priya went out to the pump house the next Saturday, with Tyler carrying the reel.", "Priya went out to the pump house the first Saturday in December, with Tyler carrying the reel."),
(206, "It was an hour and ten minutes. There was no signal at the pump house. Tyler went and stood at the top of the drive where there was one bar and came back. He sat on the step. He stood up. He asked if they could just take a reading every five minutes and graph it,", "It was an hour and ten minutes. There was no signal at the pump house. Tyler walked up the drive for one bar and came back, sat on the step, stood up, and finally asked if they could just take a reading every five minutes and graph it,"),
(206, "He didn't have to be asked. Irene ran her towels on Sunday. He came back the second Saturday in December, and January, and February.", "He didn't have to be asked. Irene ran her towels on Sunday. He came back the first Saturday in January, and February, and March."),
(206, "Somebody asked, lightly, who'd voted for whom. Somebody else said it was a fair question. It was the first time anyone at that table had been asked.\n", ""),
(206, " She'd borrowed it from a retired hydrologist in town who still had three.", ""),
(206, "Irene brought coffee down in a thermos.\n", ""),
# 207, Ch 28: one night dark, power when it counts, the Ochoas' house off the map (drafts/chapter-28.md)
(207, "The first hard storm of the winter came up the valley on a Friday.", "The first hard storm of the winter came up the valley in December."),
(207, "and the valley was back in 1890, except for nineteen households, where the lights stayed on.", "and the valley was back in 1890, except for nineteen households, where the lights stayed on.\nAll year the co-op's panels had been taking a bite out of its power bill, and the battery bank in the shop had been mostly a line on Reuben's budget. That night it carried the mesh, the shop's freezer and the kitchen trailer."),
(207, "She started it in the twenty-quart pot, which meant she'd already decided it was for the whole road.", "She started it in the twenty-quart pot, which meant she'd already decided it was for the whole road. Denny went from the shop to the kitchen trailer with his phone up, filming the lit windows against the black."),
(207, "And, the previous Sunday, his update, done alone, in a hurry, ahead of the weather, without a second set of eyes. It was just a repeater. The rule was for things that touched the open internet. He had let himself believe that.", "And, the week before, his update, done alone, in a hurry, ahead of the weather, without a second set of eyes."),
(207, "The north houses checked in on the voice radios, one by one. Everyone was fine. The hole was only in the map. But the hole was his.", "The north houses checked in on the voice radios, one by one. The last was the house where the road bends.\n\"Ochoas,\" Lupe said. \"We're fine. We're just not on your map.\"\nThe last time his work had failed that house, she had been standing in the doorway with the hose running into the gravel."),
(207, "Gods with cold fingers and a multimeter, that's the job. Next time you touch a node, somebody's watching. Come down. Grace has soup.\"", "Gods with cold fingers and a multimeter, that's the job. Come down. Grace has soup.\""),
(207, "They came down. There was soup. Grace had fed half the county road by then, out of the back of the kitchen trailer, by lantern,", "They came down. Halfway down the trail the soup came up to meet them, onions and bacon fat riding the wind out of the kitchen trailer. Grace had fed half the county road by then, out of the back of the trailer, under the one light on the road,"),
(207, "The storm blew out by noon Saturday. The county's power came back three days later.", "The storm blew out before morning, and the county's power came back on a little after six."),
(207, "\nThe rule got its amendment on Sunday, in Reuben's careful language. It covered everything people depended on now.", ""),
# 208, Ch 29: the women at the grange hall, Denny argues, Lupe, Tyler's yes, the gap (drafts/chapter-29.md)
(208, "Chapter 29: Ink and Pencil\nThe co-op held its annual meeting in the shouse.", "Chapter 29: Ink and Pencil\nThe kitchen cooked for forty at the grange hall every week, and in January the hall was the warmest room in the county. Marta came in late, with her right arm held close to her side, and took the potato peeler in her left hand.\nYvonne Osei, Denny's wife, worked nights at the care home in Ardell, and she knew what a shoulder looked like when it had quit. She watched Marta do three potatoes.\n\"Lift that arm for me,\" she said. \"Over your head.\"\nMarta got it as high as her chin.\n\"That's your rotator cuff,\" Yvonne said. \"How long?\"\n\"Since the summer.\"\n\"You need the scan. Then you need to quit putting that arm over your head.\" She took the peeler out of Marta's hand. \"Two years of overhead work. Maybe.\"\nLupe was at the next counter, on the onions. \"And then who does it?\"\n\"Nobody in this valley,\" Marta said.\n\"Who's closest?\" Rosa said, from the sink.\n\"Tyler. He can't hear an arc yet.\"\n\"Could you, at his age?\" Irene said.\n\"At his age I'd been at it three years.\" Marta looked at her left hand, empty now. \"Somebody showed me.\"\n\"Then show him,\" Lupe said, and went back to the onions.\n\nThe co-op held its annual meeting in the shouse."),
(208, "Priya wrote it in the margin of the agenda, in pencil. Not a person?", "Priya wrote it in the margin of the agenda, in pencil. Not a person?\nTyler wanted to block it.\n\"Log it,\" Priya said. \"Every night. I want to know what it reads.\""),
(208, "Denny started to argue and then didn't, which everyone understood, including him. The fix got a name that night. Tyler learns the edit, Frank learns the camera, and the channel becomes a bench and not a pillar.", "\"I'm not burned out,\" Denny said. \"I'm unpaid.\" He turned his glass a quarter turn. \"A tool company in Spokane called me in December. Forty-two thousand a year and a truck, to stand in front of their saws and talk the way I talk. I told them no. I'm telling you I got the call.\"\nThe room went quiet.\nThe fix got a name anyway. Tyler would learn the edit and Frank the camera, so that the channel had a bench of three behind it. Denny wrote his own name on the board, under burnout."),
(208, "Founder-dependence, said Frank. Every important thing in the valley ran through the same four people, and all four of them were sitting right there.", "Founder-dependence, said Frank. Every important thing in the valley ran through the same four people, and all four of them were sitting right there.\nSomebody quits, said Lupe Ochoa, from the back. She didn't say who. Beside her, Hector was looking at the floor."),
(208, "\"Apprenticeship's four years if you're serious. If you want it, we start Monday.\"", "\"Apprenticeship's four years if you're serious. If you want it, we start Monday.\"\nTyler set his coffee down. \"Does it pay?\"\n\"No,\" Marta said.\nHe looked at the stove, and at her hand on the cup. \"Monday,\" he said."),
(208, "\"Then put that on the board too. We need someone qualified to cover the gap. Starting an apprentice doesn't make one finished.\"", "\"Then put that on the board too. We need someone qualified to cover the gap. Starting an apprentice doesn't make one finished.\" She drank some coffee. \"Somebody already halfway there would do. Somebody whose coupons bend.\""),
(208, "Lou found him in the shed the Saturday after the meeting, at ten at night, grinding a weld that had been finished since Thursday.", "Lou found him in the shed a few nights after the meeting, at ten o'clock, grinding a weld that had been finished for two days."),
(208, "It was a bracket for the seeder, two plates and a gusset. Marta had looked it over and hung it on the rack. On Friday night Elijah had taken it back down,", "It was a mount for the seeder, two plates and a gusset. Marta had looked it over and hung it on the rack. The next night Elijah had taken it back down,"),
(208, "Lou leaned in the doorway and watched him do it four times.", "Lou leaned in the doorway and watched him make another pass."),
(208, "Lou came over and took the bracket out of his hands", "Lou came over and took the mount out of his hands"),
(208, "He wanted, very badly, for Lou to tell him the bracket was good.", "He wanted, very badly, for Lou to tell him the mount was good."),
(208, "He said, \"Bracket's done.", "He said, \"Mount's done."),
(208, "When he was gone, Elijah stood with his hand on the bracket for a while. It was good, and nobody had said so, and he was going to have to get used to that.", "When he was gone, Elijah stood there with his hand on the mount."),
# 209, Ch 30: Priya and Grace the night before, Denny's last video, Lou's "my man" (drafts/chapter-30.md)
(209, "Chapter 30: Item Seven\nThe county chambers smelled like wet coats and floor wax.", "Chapter 30: Item Seven\nThe night before the county meeting Priya found Grace in the kitchen trailer with the banker's box open on the counter and the receipts sorted into piles by month.\n\"How long do you get?\" Priya said.\n\"Three minutes.\"\n\"Then you get one number.\" Priya pulled a stool over. \"When I ran, I had three minutes at every grange hall in the district. I spent the first two on why I was running. Nobody remembered anything but the red light.\"\n\"Which number?\"\n\"What it costs to feed one person on the route for a week. Not the total. The total scares them.\"\nGrace ran her finger down a page. \"Eleven dollars and forty cents.\"\n\"Say that first. Then stop.\"\n\"I've stood on a lot of porches with three minutes,\" Grace said. \"Telling people why they had to leave. You don't open with a number. You open with who.\"\nPriya thought about that. \"Then one name,\" she said. \"Then the number. Then stop.\"\nGrace picked up a pen and wrote a name on the back of her hand.\n\nThe county chambers smelled like wet coats and floor wax."),
(209, "Irene Calder came last and took the aisle seat as if she'd been assigned it.", "Irene Calder came last and took the aisle seat as if she'd been assigned it. Denny set up a tripod in the back row and filmed the whole thing."),
(209, "That's all politics is, man.", "That's all politics is, my man."),
(209, "She sat with the banker's box on her knees and did not say anything.", "She sat with the banker's box on her knees and did not say anything. The name on the back of her hand was Rosa's."),
(209, "She read it back to him and changed more to the rest.", "She read it back to him and changed \"more\" to \"the rest.\"\nAt the truck Denny folded the tripod and handed the bag to Tyler. \"You hang onto that,\" he said, and didn't ask for it back."),
(209, "\"Yeah, man,\" Lou said. \"She did.\"", "\"Yeah, my man,\" Lou said. \"She did.\""),
(209, "On Thursday he ran a whole coupon", "By the end of the week he ran a whole coupon"),
(209, "Friday he ran it again.", "The next day he ran it again."),
# 210, Ch 31: Denny leaves, "Nothing that mattered" on the page, the roster cut (drafts/chapter-31.md)
(210, ("He stood in front of the roster with his coffee and finally saw the whole thing.", "and it would never let him drive.\n \nHe didn't go to the shop that week."),
"""He stood in front of the roster with his coffee and finally saw the whole thing.
He would not do it the city's way. He had turned down the million dollars and the ads and the room. That was his father in him: never take a handout. And these people would not do it his way. They would rather stay small and broke and good, and ask the county for it every six months.
The farm would feed him every Friday for the rest of his life, and it would never let him drive.
Two days later Denny waved him up onto his porch. Yvonne's car was gone; she was on nights again.
"I called Spokane back," Denny said. "Forty-two and the truck. I start the first."
Elijah stopped on the step. "Because of the plan."
"Because you said it out loud." Denny turned his cup a quarter turn on the porch rail. "You stood up and told the table what my bench is worth to a tool company. Then they voted you half pay, and I've been on that bench seven days a week for nothing. Yvonne's on nights so I can do it."
"I didn't mean it like that."
"I know you didn't. That's why I'm telling you, instead of just going." He looked out at the beds. "I'll give it a year. Maybe I'm wrong."
He was gone by the weekend. Tyler had the tripod, and nobody knew what to post.

He didn't go to the shop that week."""),
(210, "He had blocked Melody's number two and a half years ago, and he could still hear it.", "He had blocked Melody's number two and a half years ago, and he could still hear her say it."),
(210, "\"I should have heard it.\"\nHe took it.", "\"I should have heard it.\"\nHe took it.\nGrace came back after dark with a plate from the grange hall under a dish towel. She set it on the stove to keep warm and sat on the floor with her back against the woodbox.\n\"What did I say?\" he said. \"Last night.\"\nShe looked at the stove. Her mouth opened, and closed again. He watched her decide.\n\"Nothing that mattered,\" she said, and squeezed his arm.\nHe believed her because he wanted to."),
(210, " Later he had asked Grace what he'd said to her that night in the shouse, and she'd said, \"Nothing that mattered,\" and squeezed his arm. He believed her because he wanted to.", ""),
(210, " Nobody answered for him. That was fair. But nobody told Patricia it wasn't her business, either.", ""),
(210, " He had never been any good at staying.", ""),
# 211, Ch 32: the late payment, the missed stop, the April quarrel, the coffee can (drafts/chapter-32.md)
(211, "So he closed the notebook and snapped a rubber band around it.", "So he closed the notebook and snapped a rubber band around it. On the shelf beside the broken coupons, Frank's chart leaned where he had propped it. He had sat on that one for eight months too."),
(211, "Later they sat on the floor in front of it, her back against his chest, with a blanket around both of them.", "Later they sat on the floor in front of it, her back against his chest, with a blanket around both of them. She put the truck song on, low, on her phone."),
(211, "she fell asleep against him before the oak had caught.", """she fell asleep against him before the oak had caught.

On the first of April the trust's check to Irene came up short.
The channel had been falling since Denny left. Tyler cut what footage there was, Frank held the camera like it might go off, and the numbers knew the difference. Reuben brought the ledger to Grace in the kitchen trailer and wanted it on Friday's agenda.
"Give me a week," Grace said.
"For what?"
"For him. He isn't sleeping, Reuben. He blamed himself for Denny out loud at that table." She closed the ledger. "Not on a Friday. Not yet."
Reuben gave her the week. Grace went up to the house, and Irene told her to pay it when she could, honey, the ground wasn't going anywhere.
That week Curtis was at the county all day for the food study, which came back "revisit next cycle," so December stood. Hector drove the route off the printed list. The list said which box went to which door. It didn't say that Mrs. Delgado couldn't carry one. Hector set hers inside the gate, the way the list said, and drove on.
A neighbor called the kitchen trailer after dark. The box was still at the gate, and the porch light was on.
Grace drove out. Elijah heard her truck come back a little before eleven. It stopped by the kitchen trailer and didn't shut off. Through the window he could see her in the cab with both hands on the wheel.
This time he went out and got in the other side.
"She was fine," Grace said, to the windshield. "Sitting in her kitchen with the insulin on the table and nothing to eat with it. Hector did what the list said."
He sat with her until she turned the engine off. She didn't tell him anything else, and he didn't know there was anything else to tell.
Five days later Irene stopped her golf cart by the compost where he was turning it.
"Tell Reuben I don't mind waiting," she said. "A month's nothing."
Reuben showed him the ledger the minute he asked. The channel's column fell off a shelf in February. Elijah did the arithmetic four times, the way he had once done it on his mother's room. Miss three in a row and the ground went back to Irene, and after Irene to Dale, and the people who had written the Alderson letter were still writing letters.
He found Grace in the shouse.
"You knew," he said.
"Since the first."
"You knew, and you went to Irene, and you didn't tell me." His voice came up. He heard it and didn't stop it. "Do you know how I found out about my mother's house? A coffee can. A coffee can of order slips, in the barn. She kept the payments off the table so I wouldn't worry."
"I was buying you a week."
"I'll pay it." He had the notebook out, the back of it, where the checks were. "I'll sign these over tonight."
"Elijah. Those come out of the same account." She said it gently. "You'd be paying Irene with Irene's money."
He looked at the checks. She was right, and it stopped him cold.
"Don't handle me," he said. "Not like she did."
Grace went white.
"And what's in that one?" She pointed at the notebook on the table, the one with the rubber band around it. "You've been up every night since March. What's in there, Elijah?"
He didn't answer.
She walked out and shut the door behind her, carefully, the way Reuben did.
He stood in the shouse with the notebook. Then he went after her. He had never gone after anybody in his life.
She was at the pond, on the bank, with her arms around her knees. The frogs were going in the cattails. He sat down a little way off.
"I'm sorry," he said. "You're not her. I know you're not."
She picked at the grass.
"The notebook's what I'm scared of," he said. "I think it's here already. I think it's on my mother's hill. I can't prove it, and the last time I said something like that out loud, you held my head for six hours."
She was quiet a long time.
"I sat in that truck and let you sit with me," she said, "with Irene in my pocket the whole time. That wasn't fair either."
A frog went off right by their feet, and they both jumped.
"You want to get frozen yogurt?" he said.
She looked at him. "You remembered."
"One cup," he said. "Two spoons."
That Friday he brought the ledger to the table himself. He told them the payment was short and that he thought it was his doing: the plan, and Denny, and the channel. Nobody let him have all of it. Curtis said he'd drive the route himself till June, list or no list. Priya wanted the shortfall to the dollar. Lou got up, came back from the kitchen trailer with the coffee can they kept the change in, and set it on the plywood, and it went around the table.
"One month I can wait," Irene said, from the head of the table. "Three I can't. Dale reads the papers too."
It went on the trust's record as one late payment, with the clock still running."""),
(211, "A wood base Denny cut him from a pallet.", "A wood base Frank cut him from a pallet."),
# 212, Ch 33: Denny comes back, "I sold it to them", the tomato dinner trimmed (drafts/chapter-33.md)
(212, "He wrote it under the others. His hand wasn't steady.", "He wrote it under the others. His hand wasn't steady.\nHe was still at the gate when a truck came up the county road, slowed, and stopped with its blinker on. It was Denny's. Elijah swung the gate open.\nDenny rolled the window down. He had on a company polo with a saw blade over the heart.\n\"They gave me a script,\" he said. \"Every video. What to say about the saws, and what not to say about anything else.\" He looked past Elijah at the beds. \"Nobody ran me off. That was me. I want that straight.\"\n\"Okay.\"\n\"Yvonne says I'm a pain in the ass to live with when I'm not on the porch.\" He put the truck in gear. \"Is Friday still Friday?\""),
(212, "\"I think so. I think it's on my mom's old place.\"", "\"I think so. I think it's on my mom's old place.\" He made himself go on. \"I sold it to them. My mother's place. Three letters and an LLC.\" He looked down the table at Reuben. \"You asked me why you had to go and look. I didn't want anybody up here to know.\"\nReuben nodded, once, and wrote something on the tab of his folder."),
(212, "It went around again, all of them at once, Tyler asking what people are even for if a robot does everything, Wren saying that was the only question and nobody ever lets her ask it, Patricia saying this was why she didn't come on Fridays.\nLou let it run. Then he put one hand up, flat, like he was stopping a truck at a gate.\n\"Listen to me,\" he said again. \"Please.\"\nHe waited until he had them.\n", "Lou put one hand up, flat, like he was stopping a truck at a gate, and waited until he had them.\n"),
(212, "Denny had stopped turning his glass.\n", ""),
# 213, Ch 34: Curtis's wound, the arms at Praether's revealed, the war on the phones, Curtis the Trekkie, the Ochoas leave (drafts/chapter-34.md)
(213, " Somebody had posted a picture of a laptop with an axe in it.", ""),
(213, "\"I lost the crop. Honestly I'm still mad about it.\"\nCurtis didn't say anything.", "\"I lost the crop. Honestly I'm still mad about it.\"\nCurtis looked at the reader in his lap.\n\"My granddad had wheat out by Ritzville,\" he said. \"The combine threw a bearing the last week of harvest. The dealer was eleven days out, and the rain was two.\" He turned the reader over. \"Bank sold it the next spring. Our neighbors came and bid on the equipment. I was nine. I held the gate for them.\"\nLou let that sit."),
(213, ("\"No, like robot arms. The two in the equipment shed.", "It was two arguments, and then it was four."),
"""\"No, like robot arms. Two of them, off a cannery line in Stockton.\" He was peeling the label off his bottle. He wasn't even looking up. \"They're in Richard Praether's pole barn, out past the grange. They've been there since my first week. And I know a guy who'd ship a few more up. They could pack the route boxes and run the press. That frees up, what, eight people? We'd have the squash in by Wednesday.\"
Denny stopped turning his glass. \"Praether's,\" he said. \"Since your first week.\"
\"So you've been sitting on industrial technology this entire time?\" Priya said.
\"I told our friend Elijah to keep the arms a secret.\" Lou's presence was somehow larger, even though he had barely moved an inch. His voice was firm, but warm. \"I thought it best if we didn't set up too much of a power differential while our poor boy was simply trying to heal.\"
Elijah looked up, finally, and it was like a cold draft had come in under the door. Twenty-some people were looking at him, and then at each other, and nobody wanted to go first.
Wren had her hand at her throat.
\"Arms,\" Curtis said.
\"Just a couple.\"
\"You want to put the Terminator in the packing shed.\"
\"Curtis, it's an arm. It's bolted to the floor. It can't go anywhere.\"
\"I mean, that just perfectly makes sense, though?\" Tyler had his chair tipped back on two legs. \"Like, yeah. Let's automate stuff. We're eighteen people short. What are we even talking about?\"
\"We are talking about a machine doing the route,\" Wren said. Her voice shook. \"People's food. Some stranger's machine touching every box.\"
\"A machine made the box, Wren,\" said Frank.
\"What friend?\" Marta said. She hadn't moved.
\"A guy I know. From before. He's a good guy, Marta. He's got more of them than he can use.\"
He didn't say who. He didn't have to. Everybody in that room knew where he had been the year before he came, and what kind of people he had met there.
Frank set his fork down. \"Who fixes it at two in the morning in festival week, bud?\"
Elijah opened his mouth.
\"Who guards it?\" Marta said. \"Show me the guard.\"
There was a picture of the arm on the price list. There wasn't one of a guard.
Denny had gone back to his water glass, a quarter turn and back. The arms had come into Denny's warehouse in 2019. Elijah had heard that story at his first Friday dinner, and he had forgotten it. His face went hot. He felt like an asshole.
\"They came into my building bolted to the floor too, man,\" Denny said, to the glass. \"Couldn't go anywhere. I went.\"
Then it broke open. Tyler said this was exactly the kind of fear that kept them broke. Hector said he'd take a robot over another October like the last one, and Lupe told him to hush. Priya wanted to know what an arm actually did to a squash, physically, did it bruise, and nobody answered her. Wren was crying a little. Frank and Irene had gotten off onto a milking machine somebody's father bought in 1961. It was two arguments, and then it was four."""),
(213, "\"Is this what it was all for?\" said the wife of the man from the north houses.", "\"Is this what it was all for?\" Lupe said."),
(213, "\"Item four,\" Reuben said, turning a page. \"Toilets.\"", """\"Item four,\" Reuben said, turning a page. \"Toilets.\"

Afterward the kitchen trailer was full of people doing dishes who didn't want to go home yet. Lou came in last. He had walked Hector and Lupe out to their truck, and he went straight to the sink and ran the water.
\"The Ochoas are leaving,\" he said, to the dishwater. \"End of the month.\"
\"Why?\" Tyler said.
\"They were concerned by the potential for the technology to be misused, and didn't want to feel complicit in the militarization of the farm.\"
\"That's ridiculous,\" Tyler said. \"We're not militarizing anything!\"
\"That is not the way the Ochoas feel, and we would do well to respect it.\" Lou squeezed the edge of the counter tightly for a moment, then turned around. \"We will surely encounter resistance like this again along our path.\"
\"Yeah, but they're wrong!\"
\"They don't see it that way. Elijah knows what I'm talking about.\"
Heads among the group turned toward Elijah, who was mid-bite in a hunk of cheese.
\"You must have a hard-won understanding of how ill-informed good intentions can become dangerous.\"
Elijah didn't want to think about his band back home, but he couldn't help it. The image of being utterly shunned by his former buds leapt to mind.
\"I mean,\" Elijah said, \"I get it, but I think they're just scared.\"
\"It is reasonable to be afraid of the unknown. The shape of monsters is noticed more in the dark.\" Lou went back to washing the dishes as Curtis jumped in to cut the tension.
\"Yeah, well, when Skynet wakes up, I hope it comes with catgirls!\"
\"Curtis!\" Grace's admonition was loud but friendly. She smacked Curtis on the arm. Several members of the room laughed and seemed to relax.
Priya was chewing her pencil. It had found its way out from behind her ear into the corner of her mouth."""),
# 214, Ch 35: the night scene cut to the walnut, the man who refuses, ALC; Lou lets Grace drop (drafts/chapter-35.md)
(214, "That's what this lady's doing.", "That's what Patricia's doing."),
(214, "It makes sense the way the steam engine made sense.", "It makes sense the way the car made sense."),
(214, "\"They can. They just won't.\" Lou shook his head.", "Lou shook his head."),
(214, "And it is one, man.", "And it is one, my man."),
(214, "\"In the same lane, my friend.\"", "\"Same boat, my friend.\""),
(214, ("That night Lou had the barrel stove going behind the packing shed, with the door swung open so he could see the fire.", "For about as long as the joint lasted, it was."),
"""That night Lou had the barrel stove going behind the packing shed, with the door swung open so he could see the fire.
Elijah came down the path a little after nine. He hadn't decided to. His feet had. Lou pointed at the other lawn chair with a walnut.
They sat a while. Elijah rolled a joint and lit it off a stick from the stove. Up the field the irrigation was still ticking over.
"What's Grace say about the arms?" Lou said.
"She hasn't said."
Lou nodded and let it go. He cracked two walnuts in one fist and looked at the fire, not at him. "You've heard of mutually assured destruction, Elijah."
"Of course."
"Our parents did drills in school. Got under their desks for a bomb that never came. Or at least, not yet." He picked the meat out with his thumbnail and tossed the shells in the stove. "I believe in something even more powerful."
"What could be more powerful than the nuclear bomb?"
Lou turned in his chair and looked him right in the eyes. He had very pale eyes, and the fire was in both of them.
"The man who refuses to launch it."
Elijah didn't say anything.
"Choice, my friend. We always have a choice."
"Yeah, but they'd court-martial him. They'd throw him under the prison."
"And he can choose," Lou said, "to suffer those consequences."
Elijah sat with it. He had filled eleven notebooks with the people who would launch the machine. The ones who wouldn't, given the chance? He didn't know a single name.
"You've got eleven notebooks of the ways it goes wrong, Thoreau," Lou said. "You got anything in there about how it goes right?"
"One." Elijah hadn't said it out loud before. "We measure the whole country by GDP. How much got made and sold. I'd put another number next to it. ALC. Adequate level of care. Is everybody fed, housed, doctored. And if they're not, why not, and what are we pointing the machines at to fix it."
"Don't we already do that?" Lou said. "With money?"
"Money tells you what got sold. It doesn't tell you who didn't eat."
Lou looked at the fire and didn't argue.
The firelight moved across his face. Elijah took another drag. He wanted it to be that simple. For about as long as the joint lasted, it was."""),
# 215, Ch 36: festival week, Lou's squash row; one debt in the fire (drafts/chapter-36.md)
(215, "Twenty-two people did the work of forty for nine days.", "Twenty people did the work of forty for nine days."),
(215, "Lou's bad knee, the one that was still his, swelled up like a grapefruit.", "Lou's bad knee, the one that was still his, swelled up like a grapefruit on the second day, and Elijah picked Lou's squash row by hand, the whole length of it, while Lou sat on a bucket at the end and told him he was doing it wrong."),
(215, "Wren fainted at the cider press on Saturday and went right back to it.", "Wren fainted at the cider press on the busiest day and went right back to it."),
(215, "The rain came Thursday and the county opened burn season Friday. On Sunday night, when the last car from Idaho had pulled out,", "The rain came at the end of the week, and the county opened burn season. On the last night, when the last car from Idaho had pulled out,"),
(215, "What choosing for people looked like, he knew.", "He knew what choosing for people looked like."),
# 216, Ch 38: the last gantry is the rover (CT, 26 Nov: "It's meant to be a rover. Not a gantry.")
(216, "the gantry stood parked over bed four", "the new rover stood parked over bed four"),
(204, "They built it from free plans off the internet and what was in the drawer. It was not fast. It crossed a bed like an old man crossing a street.", "It was not fast. It went down a path like an old man crossing a street."),
(204, "and it lowered its arm and watered exactly one seedling.\nTyler stood there with his cyberdeck under his arm.", "and it reached its arm over the side board and watered exactly one seedling.\nTyler stood there with his cyberdeck under his arm."),
(213, "Patricia was there, at the end of the table, because the network's name went on the banner. She had a binder. She had her phone face down next to it.",
"""Patricia was there, at the end of the table, because the network's name went on the banner. She had a binder. She had her phone face down next to it.
Reuben took the money first. He kept the books, and for the first time since the land there was something left at the bottom of the page. The channel had come back with Denny.
Priya had one sheet of paper, and Marta and Grace had signed it under her. The little rover had watered and weeded four beds for two seasons. They wanted the tall one now, the frame that straddles a whole bed, in time for spring.
\"It gave us back a day a week,\" Priya said. \"I measured.\"
Lupe Ochoa had her phone face up on the plywood, which nobody did at that table.
\"When we bought the little one, I said I wanted to be able to carry it out of my field,\" she said. \"I can't carry that.\" She turned the phone around so the table could see it. \"I watch the videos from Ukraine every night. The drones. Some kid in a basement flies one into a man in a field. Same factories. They don't make a nice kind for farms.\"
\"Lupe,\" Hector said. \"It waters lettuce.\"
\"So did the little one. Now look what we're buying.\"
\"She's not wrong about the factories,\" Marta said.
Priya looked down the table at Curtis, with her pencil up, ready. \"I thought you would share their feelings.\"
\"I mean, I kind of do,\" Curtis said. \"I get it a little bit.\" He scratched his jaw. \"For all my fear-mongering about Skynet, and being worried that I'm plugged into the Matrix right now, I'm also a Trekkie.\"
Blank faces, all the way down the plywood.
\"Oh, come on. Star Trek? Really? Nobody's seen Star Trek around here?\"
\"You want your own Commander Data,\" Marta said.
Curtis turned and looked at her, and she looked back at him.
\"Yes,\" he said. \"Absolutely. You get it.\"
\"Beam me up, Scotty,\" Marta said, and for a second they were the only two people at the table smiling.
It passed. Hector voted for it. Lupe kept her hands in her lap. Reuben said the frame would take six weeks to come."""),
(213, "But he got comfortable, and he had a beer in him, and he said it the way you'd offer to bring ice.", "But the table had just voted for a robot, and he had a beer in him, and he said it the way you'd offer to bring ice."),
(215, "Chapter 36: This Is the Gate\nHe told her on the Wednesday of festival week,", "Chapter 36: This Is the Gate\nThe Ochoas left the Saturday before the festival. Hector backed the stock trailer up to the hoop house himself and loaded the wire benches, and he shook Elijah's hand at the truck, once, hard, and didn't say anything.\nLupe took the clipboard off its nail by the door and gave it to Grace. The last line on it said INSTALLED BY, in Elijah's hand.\n\"Somebody should keep checking,\" Lupe said, and got in the truck.\nIn the shouse, Reuben rubbed out the twenty-two on the whiteboard and wrote twenty.\n\nHe told her on the Wednesday of festival week,"),
(213, "They went around on it for half an hour. Could the high school send kids.", "Then the harvest, and the eighteen. They went around on it for half an hour. Could the high school send kids."),
(204, "Write your models accordingly.\n\n§H1 Pondwater", "Write your models accordingly.\n§H1 Pondwater"),
(204, "Chapter 26: The Indignant Worm\nChapter 27: Blueprints of a Wall", "Chapter 26: The Indignant Worm\nPondwater\nChapter 27: Blueprints of a Wall"),
# 217, Ch 37: the arms are at Praether's (CT's yes, 26 Nov)
(217, "All that was left were two robot arms in the back of the equipment shed.", "All that was left were two robot arms in Richard Praether's pole barn."),
# 218, Ch 39: Devendra's text (CT, 26 Nov)
(218, "\"No, I didn't.\"\nElijah donned his jacket.", "\"No, I didn't.\"\nHis phone buzzed against his leg. It was Devendra.\n*Dinner's on me!*\nElijah donned his jacket."),
# 219, continuity in Chapters 11, 13, 15 and 19 (CT's yes, 26 Nov; from the story report)
(219, "He carried the amp down the stairs himself, and it went into his mother's barn under a moving blanket, where he wouldn't have to look at it.", "He carried the amp down the stairs himself. At his mother's he set it on the back porch, and by the next morning she had it out in the barn under a moving blanket, where he wouldn't have to look at it."),
(219, "since Monday night", "since Sunday night"),
(219, "On Wednesday he drove into town for a letter from her doctor.", "Two days before that, on the Wednesday, he had driven into town for a letter from her doctor."),
(219, "David showed up Thursday morning with a hand truck", "David showed up the next morning with a hand truck"),
(219, "He had not opened the case since the last gig.", "He had hardly opened the case since the last gig."),
(219, "The cases came from a kid named Tyler.\nTyler worked the register at Kowalski's Hardware in town, where Elijah had bought the screw terminals, forty at a time, until Tyler asked what they were for.", "The cases came from Tyler, the kid at the register who had sent him out to Praether's.\nElijah had been buying the screw terminals at Kowalski's, forty at a time, until Tyler asked what they were for."),
# 220, Ch 18: Lou on Praether and the ace in the hole (CT's scene, 26 Nov)
(220, "Elijah's next crisis found him in late April, seven weeks after he'd walked into the shop.", """Lou got the two of them alone the week after that dinner. He was weeding the end of a bed, and he didn't get up.
"Grace says you met Richard."
"He yelled at us about the military," Elijah said.
"He would." Lou sat back on his heels. "Richard went over to the Gulf in ninety-one. He came home with something wrong in him that nobody would put a name to, and the government has been writing him letters about it ever since. Most of what he says is true. He says it loud, is all."
Grace looked at Elijah. Neither of them brought up the envelope.
"Anybody else know what's in his barn?" Lou said.
"No."
"You need to have an ace in the hole, Elijah," Lou said with a knowing gaze, "never reveal all of your cards again. I would have thought you'd have learned that by now."
Elijah felt the heat of embarrassment wash over him, but it was quickly softened by Grace, who wrapped her arm around him.
"Don't worry, Lou, I won't let him do anything stupid!" She smiled and looked him right in the eyes from inches away.
"Right?"
"Right," Elijah said, barely containing his enthusiasm to be so close to Grace.
"I won't do anything stupid."

Elijah's next crisis found him in late April, seven weeks after he'd walked into the shop."""),
# 221, Ch 34: the women weigh the tall rover at Irene's table (CT's direction, 26 Nov; drafts/chapter-34.md)
(221, "On it, in marker, he wrote DECEMBER.", "On it, in marker, he wrote DECEMBER.\n\n" + """The afternoon before the October meeting, Priya took her sheet up to Irene's house, and Marta and Grace went with her.
Irene had two pots of windfalls cooking down on the stove. The smell had climbed the kitchen walls and gotten into the curtains, and it was out on the back step before they knocked.
Priya had the sheet flat on the oilcloth before her coat was off. It was one page, in pencil. Across the top she had copied the number from the bottom of Reuben's page and put a ring around it.
"The little one does four beds," she said. "The tall one does all twelve, in about the time the little one does a row. It waters and it weeds, and it never touches the food." She tapped the last line. "I read the pledge again. It covers the field to the box. This thing never gets near a box."
"You read it again," Marta said.
"Three times."
Irene was at the stove with her back to them, working a wooden spoon around the bottom of the near pot. "And what does all that come to?"
"Four days a week back. Maybe five. I'll know when I measure it." Priya ran her pencil down the page. "With the same hands, call it sixty more boxes a week by summer."
Marta read it with her right arm held in close against her side. "My last year at the plant, they bought a robot welder," she said. "It was going to give everybody a day a week back. It did, for a while. By spring they'd laid off six of us."
"Who would we lay off?" Priya said. "Us?"
"I know it. I'm just telling you how it sounds."
"It isn't the beds anybody's worried about," Grace said. She had both hands around a mug of Irene's coffee and hadn't drunk any. "Two of the families on the route asked me last week if a robot packs their box. I said no. One of them said, not yet. Wren won't walk past bed four anymore. And Lupe stopped me at the gate yesterday and told me what she thinks of the little one, and the tall one, and anything taller than that." She smiled a little. "I didn't ask her."
Irene turned the burner down. She came to the end of the table and sat, and it took her a minute, with one hand on the chair back the whole way.
"When somebody comes up your drive to tell you what they think, and you never asked," she said, "it's hardly ever about the thing. People came up ours about every new thing this place ever bought. The sprayer. The pivot. Every time, honey, what they wanted to know was whether they still had a say on this road."
"So what do you tell them?" Priya said.
"Not the numbers. You'll win on the numbers, and they'll go home and stay there." Irene picked a curl of apple peel off her sleeve. "You tell them they've still got a say. Then you'd better make it true."
"And if they still don't want it?" Grace said.
"Then you decide. If it's right, you buy it, and you know going in that some of them won't stay."
On the low burner the near pot had gone to a slow tick. Marta took the pencil and signed under Priya's name with her elbow tucked in. Grace sat with it until the pot ticked again, and signed under Marta.
"I'll go talk to Lupe," she said.
"You do that," Irene said. "And somebody stir that pot before it catches. My hands are done for the day.\""""),
# 222, whole book: the last continuity pass, 26 Nov (eight readers, every quote checked; drafts/pass-2026-11-26.md)
(222, "He had found his first limit. The limit he found was heat, specifically overheating.", "He had found his first limit. It was heat."),  # A7
(222, "a laptop running on 40 percent battery", "a laptop running on forty percent battery"),  # A8
(222, "He didn't know why he listened to her and not Ruby.", "He didn't know why he listened to the woman who had whispered in his ear, and not Ruby."),  # B1
(222, "Ruby gave the pen right back.", "Ruby gave the pen right back, and the notebook with it."),  # B2
(222, "Grub, somebody said, a long way back in his head.", "*Greedy little grub,* somebody said, a long way back in his head."),  # B5
(222, "Elijah wrote that down. Gus glanced over", "Elijah wrote the question down. Gus glanced over"),  # B7
(222, "She met him at the back door and looked him over", "She had met him at the back door and looked him over"),  # B9
(222, "He had left the Ranger in the cannery lot", "He had left his Ranger in the cannery lot"),  # B10
(222, " I emailed you last spring, too, and never heard back, and I've felt bad that I didn't try harder.", ""),  # C1
(222, "in her first message, after she saw his post about them", "in her message on his page, after she saw his post about them"),  # C2
(222, "Pleasantly. A little while later she asked again.", "Pleasantly. A little while later she asked again. Then she asked what he was up to."),  # C4
(222, "squared it in the visor, the way she would have", "squared it in the visor, the way Ma would have"),  # C6
(222, "and I told you I'd go over every line in two weeks, and I didn't.", "and I never told you."),  # D1
(222, "For five weeks nothing went wrong with the Crucible.", "For five weeks nothing went wrong with the rack."),  # D2
(222, "In April the order came, through", "Earlier that April the order had come, through"),  # D3
(222, "It was the best explanation of anything he'd gotten since he came north", "Lou's answer was the best explanation of anything he'd gotten since he came north"),  # D5
(222, " In one night he had written the firmware Elijah had set aside two weeks to write by hand, to make up for the board.", ""),  # D7
(222, "Neither of them could have told you why the four lines worked", "Nobody could have told you why the four lines worked"),  # D11
(222, "Lou said with a knowing gaze, \"never reveal all of your cards again.", "Lou said with a knowing gaze. \"Never reveal all of your cards again."),  # D12
(222, "He learned a long time ago not to date where you eat", "He had learned a long time ago not to date where you eat"),  # D13
(222, "That Saturday he ran the brush hog", "That Saturday Elijah ran the brush hog"),  # E1
(222, "except for nineteen households, where the lights stayed on.", "except for the co-op, where the lights stayed on."),  # E2a
(222, "except for the lights of the co-op's houses.", "except for the lights of the co-op."),  # E2b
(222, "That week he made the harder visit, the two-mile one.", "That week Elijah made the harder visit, the two-mile one."),  # E3
(222, "found the door open and nobody home. He set the box inside.", "found the door open and nobody home. He stepped inside with the box."),  # E4
(222, "Thanksgiving came the week after.", "Thanksgiving came two weeks after that."),  # E6
(222, "\"Since the summer.\"", "\"Worse since the summer.\""),  # F1
(222, "He blamed himself for Denny out loud at that table.", "He blames himself for Denny."),  # F2
(222, "Then they voted you half pay, and I've been on that bench", "They voted you half pay last summer, and I've been on that bench"),  # F3
(222, "Twenty people a year pays for the whole route.", "A hundred people a year pays for the whole route."),  # F4
(222, "and he could still hear her say it. He had never told them.", "and he could still hear her calling him greedy. He had never told them any of it."),  # F5
(222, "\"Not like she did.\"", "\"Not like Ma did.\""),  # F6
(222, "He ran it on a night at the end of March", "He ran it on a night in April"),  # F7
(222, "He looked at that until the screen dimmed.", "He didn't answer it."),  # F8
(222, "He wanted to be wrong so badly his teeth hurt.", "He wanted very badly to be wrong."),  # F9
(222, "Elijah slept. He got up and swept. He ate what was in the pan. He opened David's thread.", "Elijah slept. When he got up he swept, and ate what was in the pan, and opened David's thread."),  # F10
(222, "He plugged the oven in. He threw out the open can. He opened a new one and stood there", "He plugged the oven in and threw out the open can. Then he opened a new one and stood there"),  # F11
(222, "There was a picture of the arm on the price list. There wasn't one of a guard.", "The price list on his laptop had a picture of the arm. It didn't have one of a guard."),  # G1
(222, "The last line on it said INSTALLED BY, in Elijah's hand.", "At the bottom, under INSTALLED BY, was Elijah's name in his own hand."),  # G2
(222, "They believed him. Every one of them.", "They believed him, more or less."),  # G3
(222, "Elijah had never seen him stand at that table.", "Elijah had never seen him stand up to speak at that table."),  # G4
(222, "Reuben had gone a little pale and was nodding.", "Reuben had gone a little pale."),  # G5
(222, "clicked. \"I wrote it on a seed box for Thoreau once.", "clicked. He tipped his head at Elijah. \"I wrote it on a seed box for Thoreau here once."),  # G6
(222, "He read about it every morning in the warming truck, the way other men read box scores.", "He read about it every morning in his truck while the engine warmed up."),  # G7
(222, "for the first time since the land there was something left", "for the first time since the land went into the trust there was something left"),  # G8
(222, "The festival ended the way it always did, with a fire.", "The festival ended with a fire."),  # G9
(222, "By ten they were both a little drunk.", "By ten he and Grace were both a little drunk."),  # G10
(222, "Each of them was waiting for the other one to cross it.", "Each of them was waiting for the other one to cross the space between them."),  # G11
(222, "He called the dealer. He sat in the cab for forty minutes on hold", "He called the dealer and sat in the cab for forty minutes on hold"),  # G12
(222, "the shed, the shouse, the seed house, the packing shed and Irene's forty acres", "the shed, which was Walt's packing shed, the shouse, the seed house and Irene's forty acres"),  # H3
(222, "It went through 13 versions", "It went through thirteen versions"),  # H6
# 223, the held items of the pass resolved (CT, 26 Nov: "resolve as many of these as you can without my help"; drafts/pass-2026-11-26.md)
(223, "It won't take the machines away first. It takes the people who see it coming, out of the world everyone they love still believes in.", "*It won't start with the machines. First it takes the people who see it coming, and pulls them out of the world everyone they love still believes in.*"),
(223, "Everyone's first month here feels like the apocalypse.", "Everyone's first month with one of these feels like the apocalypse."),
(223, "That night, on his way to bed, he unplugged the cable box.", "She called back at noon, from Joan's. Her phone had been dead in her purse all morning.\nThat night, on his way to bed, he unplugged the cable box."),
(223, "That's my grandmother's hill out there. This is her kitchen.", "That's my grandmother's hill out there. This is my mother's kitchen."),
(223, "She smiled and looked him right in the eyes from inches away.", "She smiled and looked Elijah right in the eyes from inches away."),
(223, "Grace waited on the gravel with her own in her hand until it got dark, and then she went in.", "Grace waited on the gravel with her own in her hand for a long time, and then she went in."),
(223, "It should have felt like traveling light. It felt like he had hardly been here at all.", "It felt like he had hardly been here at all."),
(223, "so the sale would close before theirs did", "so the sale would close before the bank's did"),
(223, "The machine made its version of what could be considered a wink", "The machine made its version of a wink"),
(223, "Grace looked down the table at her, the way she had looked at Marta when she needed a yes.", "Grace looked down the table at her, the way she always had when she needed a yes."),
(223, "The last time a glass went down on this stretch of wood, three went up.", "The night of the toast, one glass had gone down on this stretch of wood, and three had gone up."),
(223, "He could leave one number blocked.", "He could leave Melody's number blocked."),
(223, "Elijah donned his jacket.", "Elijah zipped his jacket."),
(223, "Wren, a Gen Z artist born in 2001, leads the Sunday circle and paints the seed house.", "Wren, a Gen Z artist born in 2001, leads the Sunday circle and paints the seed house. Hector and Lupe Ochoa grew plugs at the north houses until the fall of 2027."),
(223, "2025. The controllers, Denny's channel in June, the Crucible and the leak in July. Ray dies. Irene's land goes into the trust. The first fire.", "2025. The controllers, the heat and Denny's channel in June, the Crucible and the leak in July. Ray dies. Irene's land goes into the trust. The first fire.\nFall 2025. The pond. He starts for home at Thanksgiving and turns around."),
(223, "November 2026. The co-op ships its files free.", "October 2026. The amp on the tailgate.\nNovember 2026. The co-op ships its files free."),
(223, "March 2027. The machine on the dairy. Five small things go wrong.", "February to July 2027. Denny is gone.\nMarch 2027. The machine on the dairy. Five small things go wrong."),
# 224, Pondwater: Curtis shows the table a laser weeder run by a brain organoid; Grace tells Elijah about her festival outside (CT, 26 Nov, tenth chat; drafts/edit-224-organoids.md)
(224, "At dinner one night Grace said she wasn't going to her festival this year, and that it was fine, and she left before the pie.", 'At dinner one night Curtis set the laptop on the plywood ahead of the pie and turned it around.\n"Laser weeder," he said. "Watch."\nOn the screen a steel box as wide as a two-car garage rode behind a tractor across a field of carrots. Under it the weeds went up in little threads of smoke, one after another, and the carrots stood there untouched.\n"We\'ve all seen those," Tyler said. "The big growers run them. They\'re like a million dollars."\n"That\'s last year\'s." Curtis tapped a key. "This one\'s got no computer doing the looking. Well, it\'s got a computer. But the part that tells a weed from a carrot is alive. They grow it in a dish, out of somebody\'s skin cells, till it\'s about the size of a lentil, and then they teach it. It eats sugar water. They call it a brain organoid."\n"You mean…" Priya said with horror, "that weeder is piloted by a real brain?"\n"Piloted? Like a mech?" Curtis said, leaning back from the screen. "Nah, this is Optimus friggin Prime, baby! This is bona fide synthetic life."\nEver-oblivious to the moods around him, Curtis forged on.\n"This is the beginning of a new form of life. Half biology, half metal."\nPriya physically shivered, noticeably.\n"We are not having that on our farm," Marta said with definitive certainty. Putting her whole foot down, she simply said what everyone besides Curtis was thinking.\n"Absolutely fucking not."\n"I\'m out, Curtis," Wren said, wrapping her shawl tight around her shoulders.\n"I\'m going for a walk," said Priya, who was the most visibly shaken of the group.\n"We knew this was coming!" Curtis said defensively, and with a little bit of hurt feelings in his voice.\n"You knew this was coming," Grace said, standing up. "The rest of us can always count on you for the weird shit."\n"Aye aye, captain." Curtis made an exaggerated salute.\nJust about everyone got up and left, including Elijah, who followed Grace outside.\nIn the crisp air, he took a deep breath so he could try to think again.\n*Brain organoids,* he thought, *gross.*\n"Elijah!" Grace exclaimed. She hopped closer toward him. They were out of earshot from the rest of the retreating group.\n"You alright?"\n"Yeah," he said. "You?"\n"Yeah," she said, with more confidence. "Hey so, changing the subject, I\'m not going to my festival this year."\nIt was fine, she said. She was gone before he could ask what festival, and before anybody had cut the pie.'),
# 225, Ch 8 to 10: the panel goes further, Elijah says he is overwhelmed, fifty million views, Ruby's pitch (CT, 26 Nov, tenth chat; drafts/edit-225-panel-and-ruby.md)
(225, '"Elijah, your video went parabolic," the moderator said.', '"Elijah, your video went parabolic. Fifty million views," the moderator said.'),
(225, "The room was kind about it. People patted him afterward. So real, somebody said. It was worse than if they'd laughed.", 'The man on Elijah\'s right was a sneakers one. He had a big laugh, and he\'d been using it on the front row since they sat down.\n"Okay. AGI," he said, turning in his chair. "So if that happens, what\'s to stop it from just destroying everyone and everything?"\n"A lot of people have been working on that," Elijah said. "It\'s something called the alignment problem."\n"Alignment problem? You mean like my car?"\nEveryone laughed.\n"So why don\'t we just take the AI to the mechanic?"\n"Well, there isn\'t really a mechanic for what this thing could do."\nThe laughing stopped.\n"You mean like something out of a sci-fi movie? I thought all that stuff was a few hundred years away."\nPeople chuckled, but nervously.\n"Most of the leading experts, at least from what I\'ve read, say that AGI could arrive within the next ten years."\n"So what\'s your prediction?"\nDevendra had said the surveys put it at thirty years, maybe forty. Elijah could say thirty. The whole room would breathe easier, and half of them would like him better for it. But the date was in the video, in his own voice.\n"I said it in the video," he said. "And I wasn\'t just trying to be, you know, sensational."\n"So you really believe we\'re going to get a machine that can replace all humans? By 2027."\nThe room went so quiet he could hear people shifting in their chairs. Somebody coughed.\nThere was still time to lie. Elijah looked out past the lights and decided not to.\n"I mean, yeah," he said. "That\'s what the math says."\nA groan went through the seats, and then everybody was murmuring at once.\n"Well, you heard it here first, folks," the man said, to the room. "It\'s all over. You can pack it up. The killer robots are coming before the end of the decade."\n"Hang on. I never said anything about killer robots."\n"Get to your bunker. Kiss your dog and your family goodbye. Elijah Madrone here says it\'s the end of the world before the end of the decade."\nThat got the big laugh back. The moderator thanked everybody in his very calm voice, and it was over.\nPeople patted him afterward. *So real,* somebody said. Nobody asked him about the math.'),
(225, '"You were the only one who didn\'t sound like a press release. They\'ll clip it. It\'ll do fine." Ruby put his hands in the hoodie pocket. "What\'s with the amp?"', '"Damn, that was brave, bro. That was brave. I admire the hustle."\n"It\'s not really a hustle."\n"Well, I know, because allegedly you\'re not selling anything." Ruby put his hands in the hoodie pocket. "You were the only one up there who didn\'t sound like a press release. They\'ll clip it. It\'ll do fine. What\'s with the amp?"'),
(225, '"You hate this. It\'s okay. Everybody in there hates it, they\'re just better at it than you." He balled up the napkin and made the shot into the dumpster without looking. "Come on. The real people are at dinner."', '"You hate this. It\'s okay."\nElijah looked at the water.\n"I mean, honestly, I\'m quite a bit overwhelmed," he said. "There\'s been a lot of changes happening in my life recently, and it\'s been a bit much."\nRuby slapped him on the back and put an arm around his shoulders, like they were on the same team. "Happens to the best of us. Everybody in there hates it, they\'re just better at it than you." He balled up the napkin with his free hand and made the shot into the dumpster without looking. "Come on. I want to show you something. The real people are at dinner."'),
(225, '"You smoke?" he said.', '"Here, you got a second?" he said. "I want to talk to you about something."\n"Yeah. Okay."\n"You smoke?"'),
(225, '"What did Claypot pay you?"', '"Fifty million views on one video," Ruby said. "That\'s a lot of views, man, especially for a subject like that. And your follow-ups keep holding people\'s attention. Do you know how much money you should be making, according to your numbers?"\n"I don\'t really think about that kind of stuff."\n"I know you don\'t, because otherwise you\'d be doing a lot more. Look, man, I\'m not saying that you\'re doing anything wrong, because it\'s your thing. You\'re the artist."\nElijah looked down through the grating at the alley.\n"But if I were in your shoes, and I have been, I\'d have another paid-off house." Ruby turned to face him. "So listen. Here\'s the deal. What did Claypot pay you?"'),
(225, "You'd be on a list. It's a good list.", "You'd be on a list. Believe me, it's a good list."),
# 226, Ch 26: why Elijah waits after the pond (CT, 26 Nov, tenth chat; drafts/chapter-26.md, foot)
(226, 'His side of it he never said out loud. If the pay vote passed, he would be the one person at that table drawing a check, and Grace was the one bringing it to a vote. Greedy little grub, Melody would have said, and he would have heard it every time Grace touched his arm.', "Elijah didn't quite know why he didn't go for it right away. Maybe it was a combination of his prior dating history and his steadfast commitment to not rocking the boat any more than he needed to, but he felt like hooking up with Grace would be, at that point in time, a bad call. Even though she'd made it clearer than an alpine day that she was into him, he ultimately decided not to jeopardize his room and board by getting entangled. It was a decision he truly meant to stand by.\nThe pay was part of it too. If the pay vote passed, he would be the one person at that table drawing a check, and Grace was the one bringing it to a vote. Greedy little grub, Melody would have said, and he would have heard it every time Grace touched his arm.\nBut alas, fate has a way of wearing you down. And time had a different story to tell. Watching Grace work the land would do that to just about anyone."),
# 227, the polish pass at key moments (CT, 26 Nov, tenth chat: "buff it out and polish it up"; drafts/polish-2026-11-26.md)
(227, 'The co-op needed money the way every real thing needs money.', 'The co-op needed money the way every real thing needs money, a little at a time and all the time.'),
(227, "Not dramatically. Just constantly. In Elijah's first spring", "In Elijah's first spring"),
(227, 'He could delete it from his own server. He could not delete what they had copied.', 'He could delete it from his own server, but not what they had copied.'),
(227, 'Everyone in the shed understood that to be the worst available outcome.', 'Everyone in the shed would rather she had.'),
(227, 'So he stayed where he was useful. Useful was easier than David.', 'So he stayed where he was useful. It was easier than facing David.'),
(227, 'She put her hand on his forearm, the way she did with everyone, and then she left it there, which she did not.', 'She put her hand on his forearm, the way she did with everyone. This time she left it there.'),
(227, 'So Marta welded the spine of his house, and Elijah went to his lane.', 'So Marta welded the spine of his house, and Elijah did the part he knew.'),
(227, 'Elijah laid the chart on the worn wood and confessed to it.', 'Elijah laid the chart on the worn wood and told him.'),
(227, ' He remembered what she had told him his first month, about her dad and a porch.', ''),
(227, 'There was one he did not keep.', 'There was one row he did not keep.'),
(227, 'He had never told them any of it. So of course they knew.', 'He had never told them any of it. Sitting there, he felt like all of them knew anyway.'),
(227, 'He stood in front of the roster with his coffee and finally saw the whole thing.', 'He stood in front of the roster with his coffee going cold.'),
(227, "He didn't go to the shop that week.", "Elijah didn't go to the shop that week."),
(227, 'Except there was no demo. There was a hum by a county road.', 'Except this time there was no demo, only a hum by a county road.'),
(227, 'Carefully he put the hinge down on the post, and then he was back', 'He put the hinge down on the post, carefully, and then he was back'),
(227, 'He read them out at Friday dinner.', 'Elijah read the posts out at Friday dinner.'),
(227, "Elijah realized on the walk up to the shouse that he hadn't said one word all night.", "It occurred to Elijah on the walk up to the shouse that he hadn't said one word all night."),
(227, "He didn't say who. He didn't have to. Everybody in that room knew", "He didn't say who. Everybody in that room knew"),
(227, 'They could have run that shed better and more precisely than it had ever been run.', 'The arms could have run that shed better and more precisely than it had ever been run.'),
(227, "He hadn't decided to. His feet had.", "He hadn't planned to."),
(227, 'He told her on the Wednesday of festival week', 'He told Grace on the Wednesday of festival week'),
# 228, Ch 16, 17, 33: Lou comes in heavier, on Elijah's first night (CT, 26 Nov, eleventh chat; drafts/edit-228-lou-comes-in.md)
(228, '"Hm? Oh." She glanced at it and away. "Old habit. Come on. Eat. Then I\'ll show you where you sleep."', '"Hm? Oh." She glanced at it and away. "Old habit. Come on. Eat. Then I\'ll show you where you sleep."\nHalf a dozen people had come down to unload the trailer. They were passing pans out of it hand to hand, and they were in the middle of an argument.\n"The artists have a valid point, don\'t they?" a woman said.\n"What do you mean?"\n"Well, they are losing income to a machine. They are being replaced in the corporate hierarchy. They\'re losing quite a bit of their power."\n"Yeah, but they\'re kind of doing it to themselves, aren\'t they?" a man said from inside the trailer. "With all their witch hunts and their constant complaining in every comment section, they\'re not exactly doing themselves a favor with all that."\n"They will adapt, as the lamplighters did."\nThat came from behind Elijah. A man had turned the corner of the shed with a bucket in each hand.\n"Lou," Grace said. "This is him."\nHe was imposing, a big guy, about sixty, sunburned right up to his hat line. But there was a certain temperance to him that was noticeable. He moved gently. And while his boots were quite large to accommodate such big feet, he had a light step, instead of pounding the ground like so many men his size. Lou\'s steps were light as a feather.\nElijah was reminded of his uncle, who was a Hopi tribesman. They weren\'t related by blood, but that uncle had imparted a lot of lessons when Elijah was growing up, and was a big reason why Elijah eventually became an Eagle Scout. But that\'s another story for another time.\nLou set the buckets down.\n"Everyone, please welcome our new guest, Elijah," he said. "He\'ll be staying with us for a while."\nA few of them lifted a hand. Somebody said, "Hey, Elijah." The pans started moving again.'),
(228, 'That evening she told him a man named Lou would cover what he owed on the unit.', 'That evening she told him Lou would cover what he owed on the unit.'),
(228, '"He didn\'t say. That\'s Lou. You\'ll meet him."', '"He didn\'t say. That\'s Lou."'),
(228, 'A sunburned man of about sixty set a bucket down by the pump house and walked over. "He\'s on the phone with his mother," he said. "Go on, now." The man went. The sunburned one picked his bucket back up.\n"Lou," he said, and went back to the beds.', 'Lou set a bucket down by the pump house and walked over. "He\'s on the phone with his mother," he said. "Go on, now." The man went. Lou picked his bucket back up and went back to the beds.'),
(228, 'from a man of about sixty who was sunburned right up to his hat line and had been cracking walnuts into a bowl the whole time without once looking at his hands. It was Lou, from the pump house steps. Lou ran the growing side', 'from Lou, who had been cracking walnuts into a bowl the whole time without once looking at his hands. Lou ran the growing side'),
(228, "Lou wasn't a big man, but he had a titanium knee and fifty years of hauling bins in him,", 'Lou was a big man with a titanium knee and fifty years of hauling bins in him,'),
# 229, Ch 17: Grace's talk about the bed and staying for free (CT, 26 Nov, eleventh chat; drafts/edit-229-230-grace-and-rosa.md)
(229, 'She did not ask about his mother. He had told her in six lines, and she let the six lines be all of it.', 'She did not ask about his mother. He had told her in six lines, and she let the six lines be all of it.\nOne night, when his plate was empty, she sat down across from him with her own.\n"How are you liking your bed? Is it comfy enough?"\nHe raised an eyebrow. "Yeah, it\'s great. It gets a little cold in there at night, but you guys give me plenty of blankets, so I feel really good. Thank you. I\'m really grateful for this."\n"No problem."\n"So when do I start paying, or sign, or whatever?"\n"No, I meant it. You can stay here for free as long as you like. It\'s just good to have people like you around, you know?"\n"What do you mean, people like me?"\n"You know, people who get it. Every one of these families came to us in one way or another, but we\'re all contributing to the success of the farm." She started eating. "I trust you\'ll do the same."\nHe thought about it, and lingered a minute. "Is this too good to be true?"\n"What? You want something?"\nHe raised his eyebrows and blinked a few times. "No, I\'m good."\n"Great. Close the door on your way out, would you?"'),
# 230, Ch 31: Rosa and the ladle, the Sunday after the county meeting (CT, 26 Nov, eleventh chat; drafts/edit-229-230-grace-and-rosa.md)
(230, 'Elijah brought the Friday table a plan.', 'The Sunday after the county meeting, Elijah carried pots at the grange hall. Rosa was serving. She had seen his slides.\n"I don\'t really understand all this technology stuff," she said. "It goes over my head. In one ear, out the other."\nShe paused, turned around with the ladle, and filled a bowl. "I do know good food. In this place, they make a lot of good food. Nourishes the whole community." She pointed at him and tapped him on the chest. Then she put her whole palm on his chest and rubbed it in circles. "You have the heart of a helper. I can tell."\n"I just want everybody to be prepared," Elijah said.\n"Prepared is sometimes not helpful. Sometimes you can over-prepare. If I over-prepare my tamales, they fall apart. They don\'t taste too good."\nElijah kind of got it.\nShe held out the bowl. "Please take this to Grace. It\'s her turn to eat."\n\nElijah brought the Friday table a plan.'),
# 231, Ch 0 to the Appendix: the finishing pass, line fixes from the readers (CT, 26 Nov, eleventh chat: "finish everything"; drafts/finishing-2026-11-27.md)
(231, 'He said it once to Wes, in the van after a gig,', 'Elijah said it once to Wes, in the van after a gig,'),
(231, "The kid who did their listing videos, Elijah didn't just know him.", "The kid who did their listing videos, Elijah didn't know him."),
(231, "Under that, Wes's link to the water article. Nobody had written in there since.", "Under that, Wes's link to the water article, and *is this true*. Nobody had written in there since."),
(231, 'Under that, the link to the water article. He sat with them a while and started the truck.', 'Under that, the link to the water article, and *is this true*. He sat with them a while and started the truck.'),
(231, '"He says pay him back when you can. And he says keep it between the three of us."', '"He says keep it between the three of us."'),
(231, 'The arms came up the day before the lien sale.', 'The arms came up that first week.'),
(231, 'They put cans in boxes."', 'They could put cans in boxes."'),
(231, 'He had the first crate up on the forks', 'Elijah had the first crate up on the forks'),
(231, 'Denny held out his hand for the bowl. Marta passed it.', 'Denny held out his hand for the bowl. Marta passed it. Priya put the pencil back behind her ear.'),
(231, 'Lou got the two of them alone the week after that dinner.', 'Lou got Grace and Elijah alone the week after that dinner.'),
(231, "Nobody had an answer for her. Elijah didn't either. It was in the first notebook,", 'That was in the first notebook,'),
(231, 'Grace told him about the vote herself, one morning in his kitchen, over coffee.', 'Grace told him about the vote herself, one morning at the kitchen trailer, over coffee.'),
(231, 'without naming anybody: in June a grower in the network', 'without naming anybody: a grower in the network'),
(231, "he'd read every line of the rover's code by hand that June", "he'd read every line of the boxes' code and the rover's by hand that June"),
(231, 'The note asked whether the collection time could stay late enough', 'The note asked whether the delivery time could stay late enough'),
(231, 'Twenty strangers a year sleeping on trust land is a lodging business.', 'A hundred strangers a year sleeping on trust land is a lodging business.'),
(231, 'Twenty strangers a year at my press.', 'A hundred strangers a year at my press.'),
(231, 'Yvonne\'s on nights so I can do it."', 'Yvonne\'s on nights so I can do it. My daughter asked me last week what I get paid."'),
(231, 'Tuesday it could do the whole rover file', 'Tuesday it could do a whole file'),
(231, 'He took his glasses off. "I\'ve been reading these for six years. This is better written', 'He took his glasses off. "This is better written'),
(231, 'Power or brain? Halve it. That was how you found a fault. You cut the problem in half and asked which half it was in, and you kept cutting.', 'Power or brain? Halve it.'),
(231, "Curtis said he'd drive the route himself till June, list or no list.", "Curtis said he'd drive the route himself, list or no list."),
(231, "Curtis had come back. He sat at the far end with his route jacket still on, and he didn't say what the count had been, and nobody asked him.", "Curtis had come back. He sat at the far end with his route jacket still on, and he didn't say what the count had been, and nobody asked him.\nDown the table sat the machinist from Ohio, the one who had caught the wrong label in the controller drawing. He had come up in June with his family and his father's tools, and he had stayed."),
(231, "Me in the back seat saying the Our Father so she'd come home in the morning.", "Me in the back seat before her shift, saying the Our Father so she'd come home in the morning."),
(231, '"My last year at the plant, they bought a robot welder," she said.', '"The shop I went to after the plant bought a robot welder," she said.'),
(231, '"What friend?" Marta said. She hadn\'t moved.', '"What guy?" Marta said. She hadn\'t moved.'),
(231, 'He got it out and found the page, a price list, one page, with pictures.', 'He got it out and found the price list.'),
(231, 'while Lou sat on a bucket at the end and told him he was doing it wrong.', "while Lou sat on a bucket at the end and told him he was doing it wrong. Elijah fixed Irene's bottom step too, with a hammer."),
(231, "grinned like a kid. Two years before, she couldn't sit within eight feet of a woodstove. Elijah watched", 'grinned like a kid. Elijah watched'),
(231, 'A face filled the screen. It was Grace,', 'A while later a face filled the screen. It was Grace,'),
(231, 'Gus. Iron Derby veteran, art buses, the Elks lodge museum. Trent runs the Stockton cannery.', 'Gus. Iron Derby veteran, art buses, the Elks lodge museum. Trent runs the Stockton cannery.\nRichard Praether. Gulf War veteran, out past the grange. The arms are in his pole barn.'),
]

# Lines that must be italic from end to end (verify.py cannot see italics).
ITALIC = [(143, "is this true"), (218, "Dinner's on me!")] + [(159, e) for e in ["Mr. Madrone,", "It has been an absolute pleasure watching you online. Everyone here at the farm agrees: you get it.", "We've been working on something for a long time now, and we think you'll appreciate it. Are you familiar with solarpunk? Like that stupid Chobani yogurt commercial, \"Dear Alice\"?", "Well, we're doing our best to build it in real life.", "If you're interested, there's a cot here and a private room with your name on it. Your own door, a shared kitchen, and a bunch of land.", "We would like to extend a formal invitation to host you while you build out your vision of the future with us.", "If you're interested, please just say the word and the spot is yours.", "Looking forward to working with you,", "Grace Lane"]]
