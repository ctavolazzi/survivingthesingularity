# The consistency pass, 2026-11-19: every single-spot change outside chapters 13 to 15.
#
# Each entry: (chapter, kind, find, replace, why)
#   kind "L": find is literal text.  kind "R": find is a regular expression inside one paragraph.
#   In replace: a newline starts a new paragraph, [[i]]text[[/i]] is italic, and DEL removes the paragraph.
# Every find must match exactly one paragraph in the whole Doc. apply.py checks that.
#
# The finds are short quotes from the manuscript. The replacements are new text.

I, E = '[[i]]', '[[/i]]'
DEL = '[[DEL]]'
NB = ' '

OPS = [
    # ---- planting the forgetting, the ice cream, the filming, no family ----
    (3, 'L', "Your uncle says it's the pump.", "The well man says it's the pump.",
     'You ruled he has no family. The uncle is gone.'),
    (7, 'L', '"I watched it again," she said.', '"I watched your video," she said.',
     'She does not remember watching it the first time.'),
    (7, 'L', 'I said well, it looks like him."',
     'I said well, it looks like him."\nShe had watched it in October, the morning after he posted it. She had written to him about it twice.',
     'Plants the forgetting, a year before the stroke.'),
    (7, 'L', 'Somewhere in there he stopped sleeping.',
     'He kept filming, too. He would prop the phone on the dash after a call and tell it what had just happened, and it was posted before he could think better of it. People watched those.\nSomewhere in there he stopped sleeping.',
     'You said he makes many videos about what is happening to him.'),
    (8, 'L', 'doing the math on two days, and then he went in.',
     'doing the math on two days. He told the phone about the forty-eight dollars. Then he went in.',
     'He keeps filming.'),
    (10, 'L', 'He turned the dome light off. He smelled like cigarettes.',
     'He turned the dome light off. He smelled like cigarettes. He did not tell the phone about any of it.',
     'The one night he does not film.'),
    (11, 'L', "He went into his old bedroom, under a poster of a band he'd opened for once.",
     "He went into his old bedroom, under a poster of a band he'd opened for once.\n"
     'He told his mother it was only for a while.\n'
     '"Well." The pot went into the rack. "Then you\'re somewhere."\n'
     "She fed him. After supper she stood at the counter with the radio on and ate her ice cream out of the little tub, the way she had every night of his life. Twice in one evening she asked him if he'd eaten. He said yes both times.\n"
     'He was there a month before she looked at him over her glasses.\n'
     '"Go be useful, baby. You\'re underfoot."',
     'Two of her lines the stroke would have cost you, moved to before it: "Then you\'re somewhere" and "Go be useful, baby." The second now sends him to Stockton. Also the ice cream, and the forgetting.'),

    # ---- audit line fixes, chapters 9 to 12 ----
    (9, 'L', 'Twenty years of his stuff went into one of these', 'Seventeen years of his stuff went into one of these',
     "Audit 16. Wes's flyers start in 2006."),
    (10, 'L', "for three months he'd been a face", "for four months he'd been a face",
     'Audit 15. The video was in October and this is February.'),

    # ---- the old man ----
    (15, 'L', 'a long coat, in August,', 'a long coat, in that heat,',
     'The five weeks in the truck move this scene to October.'),

    # ---- chapter 17 ----
    (17, 'L', 'The co-op ate together on the first Friday of every month.',
     'For three weeks nobody asked him anything.\n'
     'He had a cot in the room over the pump house. The Fisher sat under a tarp in the corner of the shed, because there was nowhere to put it. The first night he slept fourteen hours. Grace put a plate in front of him at the kitchen trailer twice a day and stood there until it was empty. She did not ask about his mother. He had told her in six lines, and she let the six lines be all of it.\n'
     'Marta gave him the floor. Then the benches. Then a pump off the wash station that nobody had gotten to, which he took apart on a tarp and put back together right. She looked at it and gave him another one.\n'
     'Somebody left a pair of work gloves on his step. Somebody left a jacket that was too big. He never found out who. He was thin enough that October that he could see it scared people. By the second week it had stopped scaring them.\n'
     'On Sundays at 9:40 he sat on the pump house steps and called the place with the rose garden. The night aide held the phone by his mother\'s ear. He told the radio about his week.\n'
     "Nobody had told him he could come on Fridays, and he hadn't asked.\n"
     + NB + '\nThe co-op ate together every Friday.',
     'Your ruling of 18 November: the farm people nurse him back. The three weeks were a blank. Also audit 1: the dinner is weekly, and this is why his first one is three weeks in.'),
    (17, 'L', 'Elijah offered what sounded like the reasonable middle.',
     '"Face down, Curtis," Grace said. He put the phone face down by his plate. After that night it was a rule.\nElijah offered what sounded like the reasonable middle.',
     'Audit 18. The phone rule starts the night Curtis reads from his.'),

    # ---- chapter 18 ----
    (18, 'L', 'The spiral found Elijah again in November.', 'The spiral found Elijah again in December.',
     'He now reaches the farm in late October, and this is seven weeks later.'),
    (18, 'L', "all of them except his mother's number", 'all of them except the number of the place with the rose garden',
     'She cannot call him now.'),
    (18, 'L', 'Monday, seven a.m., he was at the bench.',
     'At 9:40 that night he called the place with the rose garden, the way he had every Sunday since he came north. The night aide held the phone by his mother\'s ear. He could hear the radio. He told her about the soup. After a while she said, "Barry?" and the aide said that was all for tonight, honey, and he sat there holding the phone.\nMonday, seven a.m., he was at the bench.',
     'The first time the reader sees the 9:40 call turned around: he calls her.'),

    # ---- chapter 19 ----
    (19, 'L', 'here at last was something he was actually trained to do.',
     "here at last was something he was actually trained to do.\nThe ninety days on the yellow ticket ran out on a Tuesday in January. He was under a sink at the time. He didn't find out until Thursday.",
     'You ruled the guitar is gone for good.'),

    # ---- chapter 21 ----
    (21, 'L', 'the links to the free plans riding', 'the links to the build notes riding',
     'Audit 5. The plans do not go free until chapter 27.'),

    # ---- chapter 22 ----
    (22, 'L', 'His mother called on a Thursday, at two in the afternoon, which she never did.',
     'The text came on a Thursday, at two in the afternoon. It was from David.',
     'She cannot call. David tells him himself.'),
    (22, 'R', r'"Ray McGrath passed," she said\..*"You\'ll come down\."',
     I + 'Dad died Tuesday night. In his sleep, they think. Service is Sunday at eleven, St. Rose.' + E
     + '\nThere was nothing after it. It did not ask him to come.',
     'Same facts, in a text from David.'),
    (22, 'L', '"Yeah. Yeah, Ma, of course."', I + "I'll be there," + E + ' he typed, and sent it.',
     'He promises David and not his mother.'),
    (22, 'L', "when you've been gone a year and a half", "when you haven't sat at his bar in a year and a half",
     'Audit 13. Ten lines earlier it is seven months.'),
    (22, 'R', r'At 9:40 the next Sunday his mother said, .*"I said working\."',
     'At 9:40 the next Sunday he called the rose garden.\n'
     '"She\'s been looking at that door all day," the aide said. "Her Sunday company didn\'t come." He took it to mean the church. She held the phone by his mother\'s ear.\n'
     'He told her Ray McGrath had died, and that he had not gone down. He didn\'t know if the name still meant anything to her.\n'
     '"Barry?" she said.',
     'Nobody covers for him now. The aide plants Ray without naming him: Ray was the Sunday company.'),

    # ---- chapter 23 ----
    (23, 'L', "The shed had been Walt Calder's equipment barn.", "The shed had been Walt Calder's packing shed.",
     'Audit 17. Chapter 16 calls it an apple-packing shed.'),
    (23, 'L', 'Fifty-some parcels in three years', 'Fifty-some parcels in two years',
     'Audit 23. Bidwell only has the idea in early 2023.'),
    (23, 'R', r'That Sunday, on the regular call, he asked.*for Reuben to check\.',
     "He knew one of the eleven names already. It took him until the fourth evening to go out to the truck. His own closing papers were in the glove box, under Curtis's hose, where he had put them the day he signed. Three letters and an LLC. Same agent. Three hours apart, the same signature. He sat in the cab with the dome light on. They had not been two fences from her. He had sold them her kitchen. He circled the link for Reuben to check, and did not tell Reuben how he came to have it.",
     'He cannot ask her. He finds the buyers in his own papers.'),
    (23, 'L', 'I have the dairy. I have the water on both sides.', 'I have the dairy down south. I have the water on both sides.',
     'Audit 24. The only dairy in the book is the Hollis place, three hours south.'),

    # ---- chapter 24 ----
    (24, 'L', 'He sent it to his mother at 9:41, on a Sunday. For nearly three years he had not found the words to tell her what was happening to the world. The phone rang before the checkmark showed.',
     'It was a Sunday. At 9:40 he stepped out under the eave and called the rose garden.',
     'She cannot answer a photograph.'),
    (24, 'R', r'"That\'s the Fisher," she said\. No hello\..*for ten years\."',
     'The aide held the phone by her ear. He could hear the radio.', 'Her line is gone.'),
    (24, 'L', '"Double-wall inside. Insulated through the roof. The inspector signed it Tuesday."',
     '"I lit the Fisher, Ma," he said. "It\'s got a room now. The pipe\'s double-wall. Insulated through the roof. The inspector signed it Tuesday." The Hendersons had a chimney fire in \'88, and his grandmother had talked about it for ten years, and his mother for thirty after that.',
     'He answers the question she would have asked. The Hendersons stay in the book.'),
    (24, 'R', r'"It looks right in there," his mother said,.*"It looks like somewhere\."', '"Barry?" she said.',
     '"It looks like somewhere" cannot be said anymore.'),
    (24, 'L', 'He wrote it in the notebook after she hung up.', 'He wrote it in the notebook before he went back in.',
     'Nobody hangs up.'),
    (24, 'L', 'By eleven everyone had gone but Grace.',
     'The next Sunday he drove down and held the picture where she could see it. "It looks like somewhere, Ma," he said. She looked at it a long time. Then her good hand came up off the blanket, and she put one finger on the stove.\n'
     + NB + '\nBy eleven everyone had gone but Grace.',
     'What she does with the photograph, since she cannot say it.'),
    (24, 'L', "He'd never told anyone up here.", "He'd never told the whole of it to anyone up here.",
     'Audit 27. He told Tyler a piece of it in chapter 19.'),
    (24, 'L', '"God. We\'re fun."',
     '"God. We\'re fun."\n'
     'He told her the other one too. He had not meant to. The two pages, the room with the window, the man with the folder.\n'
     '"Did you ask her?" Grace said.\n'
     '"She asked for somebody named Barry."\n'
     'Grace looked at the stove for a while.\n'
     '"I\'d have signed," she said. "I\'d have signed in the parking lot."',
     'He tells Grace about the sale at the stove. The fire in chapter 36 needs it.'),

    # ---- chapter 29 ----
    (29, 'L', 'Nineteen households is eighteen marriages and change', 'Nineteen households is a dozen marriages and change',
     'Audit 27. A widower, a divorcee and a single father are on the page.'),
    (29, 'L', 'It was a manual, with the open boxes left open.',
     'It was a manual, with the open boxes left open.\nBefore he went to bed he put the rebuilt sheet in the library folder, names column and all. In the morning Priya checked what an outsider could see, and it went out with the rest of what they gave away.',
     'Audit 11. The machine quotes the names column in chapter 38, so it has to have shipped.'),

    # ---- chapter 31 ----
    (31, 'L', 'We have fifty-one thousand people who took our plans.', 'We have fifty-eight thousand people who took our plans.',
     'Audit 14. The download count now climbs.'),
    (31, 'L', 'At 9:40 that night the phone rang.', 'At 9:40 that night he called the rose garden.', 'He calls her.'),
    (31, 'L', '"You sound tired," his mother said.',
     "The aide said she'd had a good day, and held the phone by her ear. He could hear the radio, and under it his mother breathing.",
     'Her line is gone.'),
    (31, 'L', "For four years he'd said the same two words to that. He had them ready. He looked at the tape on the door.",
     'For two and a half years he had told that phone the same thing. Working. All good. He had the words ready. He looked at the tape on the door.',
     'What he has been telling her since the stroke.'),
    (31, 'L', "The radio played behind her. She didn't turn it down.", 'The radio played. Nobody turned it down.', ''),
    (31, 'L', '"I know, baby," she said. "Are you eating?"', DEL, 'Her line is gone.'),
    (31, 'L', '"Who\'s Curtis?"', DEL, 'Her line is gone.'),
    (31, 'L', '"He\'s a guy who thinks the world\'s ending. He fixed my truck."', '"Barry?" she said.', ''),
    (31, 'L', '"Curtis made eggs."', '"Curtis made eggs," he said. "He\'s a guy who thinks the world\'s ending. He fixed my truck." He waited a second. "So I\'m somewhere, Ma."',
     'He tells her without being asked, and says her line for her.'),
    (31, 'L', '"Well." The pot went into the rack. "Then you\'re somewhere."', 'He had told somebody he was not okay. It was the first time.',
     'Her line is in chapter 11 now, and he has just said it back to her.'),

    # ---- chapter 32 ----
    (32, 'L', "He didn't bring anybody a plan.",
     "He didn't bring anybody a plan. He had said so out loud, at a Friday table, that he was done bringing plans. Wren had put her hand on her chest.",
     'Audit 26. Wren quotes this back in chapter 34, so he has to have said it.'),
    (32, 'L', 'The fifth came at 9:40 on Sunday.', "The fifth came on a Sunday, from a number he didn't know.", 'She cannot report it.'),
    (32, 'R', r'"The well\'s down four feet," his mother said\..*park the fair in\."',
     "It was Linda's granddaughter, the Hollis girl, the one with the nose ring. She had gotten his number from Manny. "
     + I + "thought you'd want to see what they did," + E + ' she wrote.',
     'The same girl who sent his mother the video in chapter 7.'),
    (32, 'L', '"What kind of building?"',
     "There was a picture, taken from the county road at night. He knew the line of the hill. There was one fence now around the Hollis place and his mother's. Where the barn had been there was a building you could park the fair in, with lights on poles.",
     'The machine is on the ground he sold.'),
    (32, 'L', '"I don\'t know, baby. It hums. You can hear it from the mailbox."',
     I + "manny says his well's down four feet. never been down in march," + E + ' she wrote. ' + I + 'it hums. you can hear it from the road' + E,
     ''),
    (32, 'L', 'After she hung up he sat at the table in the shouse', 'He sat at the table in the shouse', ''),
    (32, 'L', 'Ma. The well, the lights. It hums.', 'Home. The well, the lights. It hums.', ''),
    (32, 'L', 'There was a hum by a mailbox.', 'There was a hum by a county road.', ''),
    (32, 'L', 'he had written once, at a kitchen table.', 'he had written once, at one in the morning.',
     'Audit 21. Chapter 3 has him on the folding chair in front of the tower.'),
    (32, 'L', "It was ten miles from his mother's kitchen, drinking her well.",
     "It was standing on his mother's ground, drinking her well. He had signed the page himself.",
     'Audit 2, settled by the sale: it is not next door, it is on her place.'),
    (32, 'L', 'He turned to the old page.', 'He got the first notebook down and turned to the old page.',
     'Audit 6. He has eleven notebooks by now.'),

    # ---- chapter 33 ----
    (33, 'L', "I think it's ten miles from my mom's house.", "I think it's on my mom's old place.", 'Audit 2.'),
    (33, 'L', 'Fifty-one thousand people took our plans.', 'Sixty-six thousand people took our plans.', 'Audit 14.'),

    # ---- chapter 34 ----
    (34, 'L', "He's got a whole warehouse of them.", 'He buys them used, out of plants that shut down.',
     "Audit 10. Gus's own facts from chapter 11, and it is why they cost a few thousand."),

    # ---- chapter 36 ----
    (36, 'L', 'Nobody had said the word ', 'Nobody at the table had said the word ',
     'Audit 22. He says "the arms" to Grace three days earlier.'),
    (36, 'L', 'written to him and bought his gas', 'written to him and offered him gas money home',
     'Audit 20. Her offer was gas money home if he hated it.'),
    (36, 'L', '"Yes, it is."',
     '"Yes, it is."\n'
     'He looked at her. Her fist was still against her chest. He thought he saw it then, the whole shape of it.\n'
     '"Grace," he said. He said it quietly. "This is the gate."\n'
     'She went still.\n'
     '"The man at the end of the road. He told you. ' + I + 'My house, my choice.' + E + ' You couldn\'t have made him. That wasn\'t yours either."\n'
     'It was the kindest thing he had.\n'
     'She took a step back from it.\n'
     '"Don\'t." Her hand came up between them, flat. "Don\'t you bring him out here. I told you that in the dark."\n'
     '"I\'m not..."\n'
     '"You are. You kept it, and now you get it out." She was looking at his hands. "You do that. You called me the lamp. Did you know that? On your floor, with your head in my hands. ' + I + "You're just the lamp." + E + ' You don\'t even remember saying it."\n'
     "He didn't.\n"
     '"You signed your mother\'s house away and she couldn\'t tell you yes or no, and you\'ve been sick over it for three years. So now nobody gets to choose for anybody. And now you\'re taking out your mother trauma on me!"\n'
     'She growled, low in her throat, and shook both hands up by her chin.\n'
     'Elijah was speechless. His heart sank and fell out the bottom of his gut.\n'
     'Here was the woman he trusted most. In one instant all of that trust was utterly shattered.',
     'Your ruling B: he strikes first without knowing it. Her last line and the three beats after it are your words. "You\'re the lamp" was planted in chapter 31 and never fired. It fires here: the first thing he ever struck her with, and he did not know that either.'),
    (36, 'L', 'He loved her so much. He could not find one word.', 'He loved her so much.',
     'Your new beat already says he is speechless.'),

    # ---- chapter 37 ----
    (37, 'L', 'The broken coupons, in a coffee can.', "The broken coupons, in a coffee can. His mother's pot.",
     'He took the pot north in chapter 13.'),
    (37, 'L', 'Her grip was the same as the first day.', 'It was the first time she had.',
     'Audit 19. She hands him a broom on the first day. There is no handshake.'),
    (37, 'R', r'His mother was at the sink\. She looked at his face.*She got a second plate down\.',
     'Below the road the place had a new fence around it and lights on poles. He kept his eyes on the road for that part.\n'
     'The rose garden was on the east side of town. Nobody was sitting in it.\n'
     'There was a book on the front desk for visitors, with a pen on a chain. He wrote his name and the time. Then he turned back a page, and another. He had not meant to.\n'
     'There was a name on every Sunday. ' + I + 'D. McGrath, 10:15.' + E + ' It went back like that two and a half years, in the same blue pen. Before that the hand changed. ' + I + 'R. McGrath.' + E + " It was an old man's writing, and it leaned. That one went back to the first October.\n"
     'He looked for his own. It was in there a few times a year.\n'
     'He let the pen go on its chain.\n'
     'She was in the chair by the window. The radio was going on the sill. Next to it there was a lamp. A little one, with a linen shade.',
     'The house is sold. He goes to her room. The visitors\' book is how he learns who has been sitting with her.'),
    (37, 'L', 'There was a lamp on the counter by the radio. A little one, with a linen shade.', DEL, 'Moved into the paragraph above.'),
    (37, 'L', '"You must be Elijah. She\'s told me about you."',
     '"You must be Barry. She asks for you."\nHis mother turned her head. She looked at him, and then at the door behind him.',
     'She cannot tell the lamp about anyone. It has one name.'),
    (37, 'R', r'"The church ladies," his mother said\..*"It\'s just tools, baby\."',
     '"The church ladies brought that." It was the night aide, the big quiet one with the glasses on a chain. She was doing the bed. "For her birthday. It talks to her at night. She likes it."',
     'The aide says it for her.'),
    (37, 'R', r'He looked at his mother\. She was seventy-one\..*gone three years\.',
     "He looked at his mother. She had worried for seventy years. The well, the bank, the Hendersons' chimney. Nobody else could wash the pot. Now two girls lifted her in the morning and somebody else did the dishes for a hundred people, and she sat in the sun with the radio going. It was the first time in his life he had seen her sit down without getting up again for something.",
     'The perfectionist and the catastrophizer, at the end.'),
    (37, 'L', 'It was her house.', 'It was her room.', ''),
    (37, 'R', r'"Where\'s the Fisher\?" she said, setting the plate in front of him\.',
     'He pulled the other chair over.\n"Barry?" she said.\nFor three years he had told her there wasn\'t one.\n"Not yet, Ma."\nShe patted his hand.',
     'He stops correcting her.'),
    (37, 'L', '"Somewhere."', '"It\'s chicken tonight," the aide said. "I can have them send two."', ''),
    (37, 'L', 'She nodded, and went to get the chicken.',
     "He said two would be fine.\nHe slept that night at Manny's, in the back room, with his boots by the door. Manny had offered it once, three years back, through a truck window, in four words. It turned out the offer was still good. His was the one fence left on that road without a light on it.",
     'The house is sold, so he needs somewhere to be. Manny has carried the stove three times and never spoken. He is the last neighbor beside the machine.'),

    # ---- chapter 38 ----
    (38, 'L', "That's what he called it.", "That's what he calls it.", 'Audit 8. The ridge is first said at the co-op.'),
    (38, 'L', '"He told me. At a coffee machine.', '"He told me it was coming. At a coffee machine.', 'Audit 8.'),
    (38, 'L', 'Fifty-one thousand downloads.', 'Eighty thousand downloads.', 'Audit 14.'),

    # ---- chapter 39 ----
    (39, 'L', 'The first copy went to his mother, across her own kitchen table, with a note in pencil inside the front.',
     'The first copy went to his mother. He had written a note in pencil inside the front, and he read her that first.',
     'There is no kitchen table now, and she cannot read it.'),
    (39, 'R', r'His mother read hers in two days\..*He was in the next room\.',
     "He had mailed one other thing north that month. The week he got back he dug a pit behind Manny's barn, square-sided, a spade-width at a time, and sent Priya a paper bag of what was at thirty. It was dust. It was dust at fifty.\n"
     'He read his mother the book. It took Tuesday afternoon and all of Wednesday and an hour on Thursday morning. He read it over the radio. He did not ask anybody to turn it down. She looked at the window for most of it. She slept through the spreadsheet. The lamp did not say anything. He had thought it might.',
     'Priya hands him a sample bag in chapter 37: "Dig one at home. Tell me what you find at thirty." This is what he finds, next to the machine that is drinking the well. And audit 3 goes away: no Sunday between the Tuesday and the Thursday.'),
    (39, 'R', r'"I kept hearing you try to tell me this," she said,.*pressure switch\."',
     'At the part with the trees she turned her head toward him. It might have been the trees. A cart had gone by in the hall.\n'
     'When he shut it she said, "Barry?"\n"Not yet, Ma."\nShe patted the cover.',
     '"It reads better than it sounded" cannot be said anymore. Audit 9 goes away too.'),
    (39, 'L', 'They ate at two on Thursday, the three of them and his uncle.',
     'They ate at two on Thursday, in the dining room, off two trays. The turkey came cut up. There was a paper cup of vanilla on hers, with a wooden spoon, and she started with that.',
     'No house, no uncle.'),
    (39, 'L', "The phone had been going off on the seat since four o'clock.",
     'The phone started going off on the seat before he was out of the lot.',
     'Audit 4. The message goes out during dinner at the farm, and he watches that dinner live at the bar.'),
    (39, 'L', 'He let it buzz.',
     'He let it buzz.\n'
     'Behind the Bear Flag he turned the engine off and picked the phone up after all. He scrolled back five years to a text he had never answered. ' + I + 'is my stuff in that thing.' + E + '\n'
     + I + 'Yes,' + E + ' he typed. ' + I + "All of it. I should have said so that night. The guitar's gone, by the way. I hocked it in Santa Rosa and never went back." + E + '\n'
     'He sent it and went in.',
     'He finally answers Wes.'),
    (39, 'L', '"I asked your mom where you were. She said working."',
     '"No. You don\'t." David put the towel down. "He drove out to that place every Sunday. Sat with your mother. Seven months, till he died. He said somebody ought to." He picked the towel up again. "And you couldn\'t come down for one hour to bury him."',
     'Your ruling D: Ray sat with her. Seven months is the book\'s own count from October to his death.'),
    (39, 'L', 'It was just over.',
     'It was just over.\n'
     '"I saw the book," Elijah said. "At the desk out there. You\'re on every Sunday."\n'
     '"Somebody ought to."\n'
     "Elijah didn't say anything.\n"
     '"She ask you for Barry?" David said.\n'
     '"Every time. There isn\'t any Barry."\n'
     '"There\'s a Barry." David held the glass up to the light. "She asked Dad the first week and he about fell off the chair. Barry Whitlow. Pitched for Analy. She went with him two summers, before your dad was anybody. Dad said he had a Mustang and no sense."\n'
     '"I thought it was the stroke."\n'
     '"It is the stroke." David set the glass down with the others. "It\'s also Barry."',
     'Your ruling C: Barry was her first love. David is who tells him.'),
    (39, 'L', "He had cried on his mother's couch for four days. He had told it to Grace like a confession and to Marta like a murder.",
     'He had yelled about them at the roof of a truck. He had told it to Grace like a confession, and Marta had heard it as a murder.',
     'No couch now. And audit 7: he never told Marta. Grace did.'),
    (39, 'L', 'on a curb in Stockton', 'on a curb in Santa Rosa', 'The five weeks in the truck are in Santa Rosa.'),
    (39, 'L', "He couldn't change what was humming on the Hollis place. He couldn't change the room",
     "He couldn't change what was humming on his mother's ground. He couldn't take his name back off a page on a kitchen table. He couldn't change the room",
     'The sale goes on the list of what he cannot change.'),
    (39, 'L', 'He could let his mother keep her lamp.', 'He could let his mother keep her lamp, and her Barry.', ''),
    (39, 'L', '"You never looked up."',
     '"You never looked up."\nHis phone buzzed once against his leg. He looked. It was a thumb.',
     "Wes answers the way David always has."),

    # ---- the story pass: structure and character ----
    (5, 'L', 'He and Manny got it up one flight of stairs',
     "Manny had the next place over and had been fixing things on theirs since Elijah's father got sick. The two of them got it up one flight of stairs",
     'Manny carries the stove three times and the book never says who he is. He matters at the end now.'),
    (6, 'L', 'The meeting was short. They called it a restructuring.',
     'The meeting was short. They called it a restructuring. The pipeline he had built ran without him now. It had for a year.',
     'The layoff had no cause. His own work lets him go, the way it let three strangers go.'),
    (7, 'L', 'By Friday it was four hundred people and he quit counting.',
     "It had gotten out through the Hollis girl. Linda's granddaughter had put it on her own page with one line, " + I + 'is my neighbor ok,' + E + ' and eleven thousand people watched her do her eyebrows. By Friday it was four hundred people and he quit counting.',
     'A video on a page with two hundred followers had no way to spread. She is already the one who sends it to his mother, and she is the one who sends him the picture in chapter 32.'),
    (11, 'L', 'and he got there at six in the morning because the email said six.',
     'and he got there at six in the morning because the email said six. He had left the Ranger in the cannery lot the night before and ridden over with the crew at four.',
     'Audit B3. Otherwise the truck he sleeps in at the cannery is still in Oakland.'),
    (23, 'L', 'There was a long quiet on the line, the box fan working,',
     "Lou had come along and stood by the door with his hat in his hands. He had lost his pears outside Ukiah to one buyer and one price. He hadn't said a word all afternoon.\nThere was a long quiet on the line, the box fan working,",
     'Lou lost his ground to a single buyer and was missing from the one chapter where a single buyer loses.'),
    (23, 'L', 'Grace went over the next afternoon and sat on the porch with her for four hours.',
     'By the door, Lou put his hat back on.\nGrace went over the next afternoon and sat on the porch with her for four hours.', ''),
    (24, 'L', 'and looked, for Curtis, content.',
     "and looked, for Curtis, content.\nElijah watched them from beside the stove. It was his room, and they were all in it, and he caught himself making a list of what he would do differently if the place were his to run. He put that away. It didn't stay put.",
     'The midpoint was a high with no turn in it. This is where he stops learning the co-op and starts wanting to steer it, so the five failures from chapter 27 on read as one want and not five relapses.'),
    (25, 'L', "He didn't throw any of it away.",
     "He didn't throw any of it away.\n" + NB + '\n'
     'That was the night she knocked.\n'
     'It was late, after the Friday table had been broken down. One knock. Then the latch, and Grace was standing inside his door with her coat still on and a jar in her hand, looking like she had surprised herself.\n'
     '"I didn\'t wait," she said.\n'
     '"No."\n'
     '"I brought soup. I don\'t know why I brought soup. You\'re fine."\n'
     '"I\'m fine."\n'
     '"I know you are." She set the jar on the table. "You went and told him. Frank. You walked in there with the chart."\n'
     '"You told me to."\n'
     '"I tell everybody to." She sat down in Reuben\'s chair, on the far side of the room from the stove, and finally unbuttoned the coat. "Nobody does."\n'
     'He put a split of oak in and shut the door on it. He did not go and sit by her. He sat down on the floor where he was, the way he had the first night, and after a while she picked up the chair and brought it over.\n'
     'Her truck was still in the gravel in the morning. Curtis walked past it on his way to the shop and found something to look at in the other direction.',
     'How they become a couple was not on the page: a chair moved a foot, and a year later she is in his shirt. In chapter 18 she says "I should have knocked like Marta." The same day she tells him to knock on Frank, she knocks on him. He still never reaches for her, which chapter 36 needs.'),
    (27, 'L', 'and a budget that stops in June."',
     'and a budget that stops in June. Every winter there\'s somebody on that route we don\'t get to in time. I can tell you their names."',
     'Her speech at the fire, "Millions of people die every single day," had no root earlier in the book. She counts the dead, and she knows their names. He never learned the names of his three.'),
    (31, 'L', 'He ate what was in the pan.',
     "He ate what was in the pan. When he carried it out there was one of Wren's candles on the step, unlit, with no note.",
     "Wren leads the circle that puts him on the floor and the book never makes her look at it."),
    (32, 'L', 'to the dollar, plus ten percent."',
     'to the dollar, plus ten percent. And the last line asks. It says if she would rather not, she will not hear from them again. I have never seen a buyer put that in writing."',
     'Audit B1. In the same month the machine tells Bidwell it would rather ask. A letter that does not ask contradicted that. Now the letter is the first sign of it.'),
    (34, 'L', 'knew where he had spent 2024,', 'knew where he had been the winter before he came,',
     'Audit B2. On the page his time in the city is one day and one night. Patricia\'s "your year in the city" stays, as her unfair version.'),
    (35, 'L', 'Their whole identity is built around the illusion of control."',
     'Their whole identity is built around the illusion of control. And it is one, man. You don\'t control when you get hungry. You don\'t control when you have to pee. Nobody was ever driving."',
     'Your words of 19 November on what the book is about, in the mouth of the man who already says it.'),
    (10, 'L', "He didn't know where that had come from. Ruby didn't seem to mind.",
     "He didn't know where that had come from. " + I + 'Grub,' + E + " somebody said, a long way back in his head. Ruby didn't seem to mind.",
     'The first hint of his sister. The reader does not know who it is yet.'),
    (31, 'L', "He didn't have an answer he liked, and he didn't give one.",
     "He didn't have an answer he liked, and he didn't give one. He had blocked that number two and a half years ago, and he could still hear it.",
     'Patricia asks who paid for him, and it sounds like Dana.'),
    (39, 'L', 'pouring beer twenty minutes from this stool.',
     'pouring beer twenty minutes from this stool. He would have to tell Marta.',
     'She sent him to find out if they ate, and never learns the answer.'),
]

# Audit items left alone on purpose, with the reason.
LEFT = [
    ('Audit 25', 'Chat Horizon is "for free" and "twenty dollars a month" in chapter 0. Both are true of the real thing, and chapter 0 is your hand-edited text. Not touched.'),
    ('Audit 12', 'The two first laughs. The second one was on the couch, and the couch is gone.'),
    ('Audit B4 and B6', 'The last line, "You\'re holding it," and what is left open at the end (the route money, the welder for the gap, his pay, the letter he signed half read). Yours.'),
    ('The top of the Doc', 'Your TO DO, Story plan and Character pages still describe the earlier version. Not touched.'),
]

# Chapter 11 reuses her line from chapter 31, so chapter 31 has to be changed first.
OPS.sort(key=lambda op: op[2].startswith("He went into his old bedroom"))

# The story decisions, for the top of the report. (what, where, why)
DECIDED = [
    ('His sister, and why he will not take money', 'Chapters 10, 13, 14 and 31',
     'Yours, 19 November. Dana is his father\'s daughter from before, in Miami. She called him "greedy little grub" when he was small. The night after he sells the farm she calls, and the call is what sets off the crash out. Her side of it and most of his are your words as you said them. He blocks her, which he has never done, and takes it for weakness. One hint before (he hears "Grub" when Ruby offers him money) and one after (Patricia asks who paid for his year in the city). Her name is mine. Change it with one word.'),
    ('The three weeks after he arrives', 'Chapter 17',
     'You ruled the farm people nurse him back. The book jumped from "Eat. Then I\'ll show you where you sleep" to three weeks later. Now there is half a page: a cot, a plate twice a day, a pump to fix, gloves on the step, and nobody asks him anything.'),
    ('How he and Grace become a couple', 'Chapter 25',
     'It was a chair moved one foot, and then a year later she is wearing his shirt. Now, on the same day she tells him "You knock, Elijah," she knocks on his door once and does not wait. He still never reaches for her. Chapter 36 depends on that.'),
    ('"You\'re the lamp" comes back', 'Chapter 36',
     'He says it to her in chapter 31 and "would never remember it. She would." Then nothing. It now fires inside the fight, as the first thing he ever struck her with without knowing. That is your ruling B twice over.'),
    ('The midpoint turns', 'Chapter 24',
     'At the first fire he catches himself listing what he would change if the place were his to run. From chapter 27 he fails five times running (paid plans, node 7, the slides, the one-page plan, the arms). With this line those read as one want, to steer, and not five relapses.'),
    ('Grace\'s speech gets a root', 'Chapter 27',
     '"Millions of people die every single day" came from nowhere. Now, when she loses the vote: "Every winter there\'s somebody on that route we don\'t get to in time. I can tell you their names."'),
    ('Her lines survive the stroke', 'Chapters 11, 24 and 31',
     '"Then you\'re somewhere" and "Go be useful, baby. You\'re underfoot" move to the spring before the stroke, where the second one now sends him to Stockton. After the stroke he says her lines for her: "It looks like somewhere, Ma." "So I\'m somewhere, Ma."'),
    ('Where he lives at the end', 'Chapters 37 and 39',
     'The house is sold. He sleeps in Manny\'s back room, beside the one fence on that road without a light on it. He digs Priya\'s pit there. At thirty centimeters it is dust.'),
    ('The lamp calls him Barry', 'Chapter 37',
     'She cannot tell it about anyone. It has listened to her for months and it has one name. He does not correct it, and he has just stopped correcting her.'),
    ('The visitors\' book', 'Chapters 22, 37 and 39',
     'Ray sat with her, then David. If David is there every Sunday, Elijah would meet him in her room before the bar. So he reads it in the sign-in book the day he comes home, and walks into the Bear Flag already knowing. In chapter 22 the aide says "Her Sunday company didn\'t come," and he takes it to mean the church.'),
    ('The machine\'s letter asks', 'Chapter 32',
     'The letter to the new widow was perfect and did not ask, in the same month the machine tells Bidwell it would rather ask. Now its last line asks, and Reuben has never seen a buyer put that in writing.'),
    ('Lou at Irene\'s table', 'Chapter 23',
     'He lost his pears to one buyer and was absent from the one chapter where one buyer loses. He stands by the door with his hat, says nothing, and puts it back on when she takes the folders.'),
    ('Causes for three things that just happened', 'Chapters 6, 7 and 11',
     'The layoff: the pipeline he built runs without him. The video: the Hollis girl reposts it. The truck: he leaves it at the cannery the night before.'),
    ('Your two lines, in Lou\'s mouth', 'Chapter 35',
     '"You don\'t control when you get hungry. You don\'t control when you have to pee."'),
]

# What I considered and turned down, and why.
REJECTED = [
    ('Grace asks him out loud to bring the arms.',
     'My earlier notes proposed it. I now think it is wrong. She wants the truck to just arrive, the way she wants the machine to "just do it." Her not asking is the character.'),
    ('Grace makes the call herself and the truck comes.',
     'A new plot event, and it would change the scene you dictated.'),
    ('A clock on her room: the money from the farm runs out at Thanksgiving 2027.',
     'It would give the ending a second question, and it would make every plan he brings to the table look like it is about his own bills. I added one line in chapter 15 so the reader knows why he will not touch that account. The clock is still there for you if you want it.'),
    ('A second Meanwhile for Ruby, or David explaining what happened to the band.',
     'Chapter 39 already settles David, his mother, the three, Wes and Gus. One more and it is a checklist.'),
    ('"They ate," texted to Marta from the bar.',
     'Two texts in one chapter. It is a thought now: "He would have to tell Marta."'),
    ('Giving her last three lost lines to somebody else.',
     '"It reads better than it sounded," "She married? I\'m asking," and "Where\'s the Fisher?" are gone. They only work in her mouth.'),
]
