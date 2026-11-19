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
     "He went into his old bedroom, under a poster of a band he'd opened for once.\nHis mother fed him. After supper she stood at the counter with the radio on and ate her ice cream out of the little tub, the way she had every night of his life. Twice in one evening she asked him if he'd eaten. He said yes both times.",
     'The ice cream once, early, and the forgetting.'),

    # ---- audit line fixes, chapters 9 to 12 ----
    (9, 'L', 'Twenty years of his stuff went into one of these', 'Seventeen years of his stuff went into one of these',
     "Audit 16. Wes's flyers start in 2006."),
    (10, 'L', "for three months he'd been a face", "for four months he'd been a face",
     'Audit 15. The video was in October and this is February.'),

    # ---- the old man ----
    (15, 'L', 'a long coat, in August,', 'a long coat, in that heat,',
     'The five weeks in the truck move this scene to October.'),

    # ---- chapter 17 ----
    (17, 'L', 'The co-op ate together on the first Friday of every month.', 'The co-op ate together every Friday.',
     'Audit 1. It is weekly everywhere else.'),
    (17, 'L', 'that he found out where the lines actually ran.',
     "that he found out where the lines actually ran. Nobody had told him he could come to the first two, and he hadn't asked.",
     'Audit 1. Why his first dinner is three weeks in.'),
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
     'The next Sunday he drove down and held the picture where she could see it. She looked at it a long time. Then her good hand came up off the blanket, and she put one finger on the stove.\n'
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
    (31, 'L', '"Curtis made eggs."', '"Curtis made eggs," he said. "He\'s a guy who thinks the world\'s ending. He fixed my truck."',
     'He tells her without being asked.'),
    (31, 'L', '"Well." The pot went into the rack. "Then you\'re somewhere."', 'It was the first time he had said it to anybody.',
     '"Then you\'re somewhere" cannot be said anymore.'),

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
     '"You are. You kept it, and now you get it out." She was looking at his hands. "You signed your mother\'s house away and she couldn\'t tell you yes or no, and you\'ve been sick over it for three years. So now nobody gets to choose for anybody. And now you\'re taking out your mother trauma on me!"\n'
     'She growled, low in her throat, and shook both hands up by her chin.\n'
     'Elijah was speechless. His heart sank and fell out the bottom of his gut.\n'
     'Here was the woman he trusted most. In one instant all of that trust was utterly shattered.',
     'Your ruling B: he strikes first without knowing it. Her last line and the three beats after it are your words.'),
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
    (37, 'L', 'She nodded, and went to get the chicken.', 'He said two would be fine.', ''),

    # ---- chapter 38 ----
    (38, 'L', "That's what he called it.", "That's what he calls it.", 'Audit 8. The ridge is first said at the co-op.'),
    (38, 'L', '"He told me. At a coffee machine.', '"He told me it was coming. At a coffee machine.', 'Audit 8.'),
    (38, 'L', 'Fifty-one thousand downloads.', 'Eighty thousand downloads.', 'Audit 14.'),

    # ---- chapter 39 ----
    (39, 'L', 'The first copy went to his mother, across her own kitchen table, with a note in pencil inside the front.',
     'The first copy went to his mother. He had written a note in pencil inside the front, and he read her that first.',
     'There is no kitchen table now, and she cannot read it.'),
    (39, 'R', r'His mother read hers in two days\..*He was in the next room\.',
     'He read his mother the book. It took Tuesday afternoon and all of Wednesday and an hour on Thursday morning. He read it over the radio. He did not ask anybody to turn it down. She looked at the window for most of it. She slept through the spreadsheet. The lamp did not say anything. He had thought it might.',
     'Audit 3 goes away with this: no Sunday between the Tuesday and the Thursday.'),
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
]

# Audit items left alone on purpose, with the reason.
LEFT = [
    ('Audit 25', 'Chat Horizon is "for free" and "twenty dollars a month" in chapter 0. Both are true of the real thing, and chapter 0 is your hand-edited text. Not touched.'),
    ('Audit 12', 'The two first laughs. The second one was on the couch, and the couch is gone.'),
    ('Audit B1 to B6', 'These are decisions, not fixes: whether the machine always asks, "his year in the city," how the Ranger gets to the cannery, the last line, why the video spreads, and what is left open at the end. Not touched.'),
    ('The top of the Doc', 'Your TO DO, Story plan and Character pages still describe the earlier version. Not touched.'),
]
