# v5 edits: the running list

Running list, started 2026-11-25. These are CT's edits to the v5 manuscript (Google Doc "StS v5 draft (Nov 23)").

**Edits 1 to 86 are done: all of them are in the Doc as suggestions, waiting for CT to accept them.** Checked
2026-11-25 against a fresh read of the Doc; the edit-by-edit record is `EDITS-v5-applied.md`. New edits start at
87 and go in "New edits" below. The publication files (`publication/novel/build/build.sh`) have not been rebuilt.

## New edits (from 87)

Not in the Doc yet. Same rules as below: [CT] is his wording, [Claude] is Claude's.

### Chapter 17: Twice Certified

87. The opening line, "For three weeks nobody asked him anything.", becomes:

    > For three days, no one really asked him anything. They let him settle. They fed him. They had discussions
    > about him behind closed doors, and he caught pieces of them through the wall of the kitchen trailer.
    >
    > "He looks thin."
    >
    > "Is he eating?"
    >
    > "Are we really sure this is a good idea?"
    >
    > "Do you actually believe he's just some guy who made a video or two?"

    Then "He had a cot in the room over the pump house..." as before. [CT: three days, they let him settle, they fed
    him, discussions behind closed doors, and the four lines. Claude: "and he caught pieces of them through the wall
    of the kitchen trailer", so the reader hears them from where Elijah is.] Left as is: "three weeks after he
    picked up the broom" at his first Friday dinner, a few paragraphs on; the co-op talked about him for three days,
    and he still waited three weeks for Friday.
88. How the arms get north (CT: how do they know anything about his life; he would have asked permission; they
    wouldn't just show up). What the book already has: Grace saw his public post ("Anybody have a dry corner for two
    robot arms? Can't pay much. Can work.") and offered the shed in her first email ("Your arms can live there for
    free while you figure it out."). Nobody up north knows about the lien sale. So Elijah asks, and tells them.
    "The arms came up that first week, the day before the lien sale. Somebody had a flatbed..." becomes:

    > On the fourth day he asked Grace if the dry end of the shed was still free. She had offered it in her first
    > email, after she saw his post about the arms. He told her the rest of it: two crates in a storage unit off
    > Highway 99, a lien sale at the end of the week, and nothing to pay it with.
    >
    > The arms came up the day before the lien sale. Somebody had a flatbed...

    and the paragraph goes on as before (the table voting to cover the unit as a loan, the crates in the dry end of
    the equipment shed). [Claude's wording, from CT's question. "On the fourth day" follows edit 87's three days.]
89. The Sunday calls on the pump house steps, and how he meets Lou (CT: the calls are 9:40 on Sunday mornings, as
    changed in edit 30; the farm lets him be; a fan comes up and tries to talk to him, and one of them shoos the
    fan off, and that's how he meets Lou). Edit 30 already changes "The night aide held the phone" to "The aide
    held the phone" here; that is in the Doc as a pending suggestion. The paragraph "On Sundays at 9:40 he sat on
    the pump house steps and called the place with the rose garden. The aide held the phone by his mother's ear.
    He told the radio about his week." gets a new last sentence and is followed by:

    > ...He told the radio about his week. The co-op let him be.
    >
    > The second Sunday a man he didn't know came up the gravel with his phone already out. He had seen the video.
    > He wanted a picture, and he wanted to ask about the list, and he started in before Elijah had hung up.
    >
    > A sunburned man of about sixty set a bucket down by the pump house and walked over. "He's on the phone with
    > his mother," he said. "Go on, now." The man went. The sunburned one picked his bucket back up.
    >
    > "Lou," he said, and went back to the beds.

    Knock-on, at the first Friday dinner: Lou's description moves earlier in the dinner and names him as the man from
    the pump house steps (see edit 90).
    [CT's beats. Claude's wording. Lou's look (about sixty, sunburned) is taken from his description at the dinner.]
90. The first Friday dinner: they have to coax him before he talks (CT: after everything, he wouldn't just go off
    on these people; they goad him: we read your stuff, we like you, we watch your videos, there's a reason you're
    here, just tell us your thoughts; Grace steps in, and Lou and Marta; Priya is looking forward to arguing; Denny
    is really trying to get him to talk; Lou puts a foot down, "only if you're comfortable", echoing Grace). After
    Denny's "...I don't want the conference version." and before "Elijah lowered his fork. He'd choked on this once,
    under lights.", insert:

    > Elijah looked at his plate. "I don't know. I'm kind of off that."
    >
    > "Come on, man." Denny leaned in. "We read your stuff. We watch your videos. We like what you put out there.
    > There's a reason you're here. Just tell us what you think."
    >
    > At the far end a small woman with a pencil behind her ear set her fork down, like somebody pulling a chair up
    > to a fight she had been looking forward to.
    >
    > "Denny," Grace said. "Only if he's comfortable."
    >
    > "Let him eat first," Marta said.
    >
    > In the corner a man of about sixty, sunburned right up to his hat line, had been cracking walnuts into a bowl
    > the whole time without once looking at his hands. It was Lou, from the pump house steps. Lou ran the growing
    > side, which meant the actual food. He didn't look up. "Only if you're comfortable," he said.

    Then "Elijah lowered his fork. He'd choked on this once, under lights." and his answer as before.
    Knock-on: further down, "'What's it eat?' / That came from the corner of the table, from a man of about sixty who
    was sunburned right up to his hat line and had been cracking walnuts into a bowl the whole time without once
    looking at his hands. That was Lou. Lou ran the growing side, which meant the actual food." becomes "'What's it
    eat?' / That was Lou again." [CT's beats; Denny's lines close to CT's words; "Only if you're comfortable" is CT's.
    Claude's wording otherwise. Priya is not named here, because the book introduces her by name a page later and
    says she "hadn't said a thing since the check-in"; she only sets her fork down.]

How to read it:

- **[CT]** means the words are CT's, as he said them. **[Claude]** means Claude wrote the wording, from a beat CT
  described or to keep the book consistent. CT can overrule anything marked [Claude].
- CT, 2026-11-25: "We should definitely keep whatever's relevant to the story and useful for dialogue purposes ...
  I'm trusting you to keep track of where stuff goes and the details of how to keep the composition rolling."
  That is the basis for every [Claude] knock-on below.
- Edit numbers are the order CT gave them and never change. Numbers 56 to 62 are knock-ons found in the full
  continuity pass of 2026-11-25 (see "Continuity pass" at the end).
- When an edit is made, move it to "Applied" with the date. To change the Doc, use the bridge:
  `node scripts/sts-bridge.mjs edit READ.json --find "old words" --replace "new words"`.

## Needs CT (answered)

Settled by CT on 2026-11-25: keep edit 5 ("chasm"), keep edits 14 and 56 (David's line), keep edit 9 ("first month
here"). The satellite office is in the North Bay. The original questions follow, for the record.

1. **Edit 5, "bridge".** Claude's reading of his dictation: the second sentence becomes "Until he saw what was on
   the other side of that chasm." Confirm.
2. **Edits 14 and 56, whose words Elijah eats.** In v5 Elijah tells David "people land where they put themselves",
   and in Chapter 15 he stands in a food bank line remembering he said it. CT's new bar exchange gives the "they'll
   land somewhere" line to David, so the food bank line now remembers David's words (edit 56). It works, and it
   sets up Chapter 39, where David is the one who knows where the three landed. But it changes Elijah from the man
   who said the callous thing to the man who doubted it. Confirm that is wanted.
3. **Edit 13, where the satellite office is.** Elijah walks into the Bear Flag (Sonoma County) after work on a
   Monday, so the office reads as North Bay. But Devendra "stayed in his house in San Jose" (Ch 25), "kept the job
   in San Jose" (Ch 32) and "stays in San Jose" (Appendix), about two hours away. Also, in Ch 2 the CPO speaks "to
   the room" at this office's all-hands. Say where the office is and Claude will line those up.
4. **Edit 9, "first month here".** Devendra says "Everyone's first month here feels like the apocalypse", but
   Elijah has been at Claypot more than a year by then (his pipeline project was fourteen months earlier). Keep
   "here", or drop it?

## Edits 1 to 86, in book order (all in the Doc as suggestions)

### Author's Note

1. Delete the line "You can doubt my forecast." [CT]
2. Keep "You can rise to meet it." as the close, then add a new line after it: "Let's begin to imagine how." [CT]

The end of the note then reads: "...you might not be paying enough attention. / This could be the most pivotal
moment yet in all of human history. / You can rise to meet it. / Let's begin to imagine how."

### Chapter 0: Three Glasses Up

3. After "The band was called Crop Dust." add "Har har." and end the paragraph there. The next paragraph starts at
   "Nate played bass and Wes played drums..." [CT]
4. "David had called him Mad since they were eight. His grandmother used to walk him..." becomes "...Elijah's
   grandmother used to walk him..." so it is clear whose grandmother. [Claude, at CT's request to clarify]
5. "He thought of himself as a bridge." stays. "Until he saw what was on the other side of that bridge." becomes
   "Until he saw what was on the other side of that chasm." [Claude's reading of CT: "He thought of himself as a
   bridge until he saw what was on the other side of that chasm. We need to change the word there." NEEDS CT.]
   (Chapter 3's "tried, for the third Sunday in a row, to build the bridge" stays; it is the same image.)
6. After "Google drew the engine." and before "PorusAI built the bomb." add: "If Google was Einstein, PorusAI was
   Oppenheimer." [CT, Option A]
7. "David gave him the look too, and then gave him a beer." becomes "David gave him the look too, but at least
   David's looks came with a side of beer." [CT. His first pass was "David gave him the look too, but at least he
   gave him beer", then he reworked the second half to "But at least David's looks came with a side of beer."]
13. Elijah's Claypot office is a satellite office. New sentence before "But Claypot moved like a big company
    moves...": "Elijah worked out of a satellite office, a long way from where anything got decided." [Claude's
    wording, CT's fact. NEEDS CT on where it is.]

### Chapter 1: A Bet for Lamb

8. Where Devendra is introduced (the paragraph ending "He found him at the good coffee machine on the fourth
   floor."), add: "Devendra liked his coffee the same way every day and got very annoyed if it wasn't right." [CT;
   placement Claude's]
9. His quote at the coffee machine becomes: "You'll calibrate. Everyone's first month here feels like the
   apocalypse." He picked up his cup. "I got a mortgage and three kids. I gave up identity crises a long time ago."
   [CT. "You'll calibrate." and "He picked up his cup." are kept from the book. NEEDS CT on "here".]
10. "Three jobs in one bar is an anecdote," Devendra said. "You build models for a living. What's your n?" /
    Elijah didn't have one. / "Fine." Devendra was enjoying himself now. "Give me a date." becomes:

    > "Three jobs in one bar is an anecdote," Devendra said. "You build models for a living. Relax."
    >
    > Elijah didn't relax. He still looked stressed.
    >
    > "Fine." Devendra was enjoying himself now. "You want to play forecaster? Be my guest. Give me a date."

    [CT's lines. "Elijah didn't relax. He still looked stressed." is Claude's wording of CT's beat. "forecaster" is
    lower case; it sets up the moderator's "the people's forecaster" in Chapter 8 and "Hey, forecaster!" in
    Chapter 11.]
11. After Elijah's "Five years. Thanksgiving, 2027. A machine that can do any job in this building.", Devendra's
    "And if it's just a Thursday?" becomes: "Five years," Devendra said. "That's one of the more aggressive ones
    I've heard yet. Okay, fine. And if it's just another Thursday?" [CT, who said "just another Tuesday". Claude
    kept Thursday, because Thanksgiving 2027 is a Thursday and the Appendix says so. "Devendra said" and "Okay" are
    Claude's.]
12. "Loser cooks" becomes "Loser cooks dinner" [CT] in: Ch 1, Elijah's reply; Ch 1, the sticky note ("E.M.
    Thanksgiving 2027. Loser cooks dinner."); Ch 2, the note in the corner; the Appendix ("He took the bet:
    Thanksgiving 2027, loser cooks dinner."). [Placement Claude's.] Left alone on purpose: Ch 6, where he says on
    video "I bet a guy dinner on it. Loser cooks." (the word is right before it), and Ch 7, the T-shirt that says
    LOSER COOKS, which quotes that video.
14. The bar. David's "You sleeping?" stays. Elijah's reply, "Sure. They'll land somewhere," Elijah said. "The
    realtors. People land where they put themselves. Retrain, learn the new thing. Nobody owes you a job.", becomes:

    > "Sure. A little. I can't stop thinking about the people the realtors fired."
    >
    > "They'll land somewhere," David said. "There's always a job."
    >
    > "I'm not so sure about that."

    [CT] David's next line, "What's a job for?", follows as it is, and the rest of the exchange is unchanged.
    Elijah's old speech is cut. See edit 56 for the Chapter 15 line that used to quote it. NEEDS CT (item 2).
15. "Devendra wanted an n. He'd get one. He'd try to break a model himself." becomes: "Devendra wanted a
    prediction. He'd give him a better one. And he'd do it by cracking one of these things open himself." [CT, who
    said "He'd give it one". Claude: "him a better one", because Elijah has already given Devendra a date.]
20. When the tower shuts off, Elijah says "Shit." [CT] The paragraph ends: Black screen. The fans coasted to
    silence. "Shit." The room ticked as it cooled. [Placement Claude's]
16. "The limit he found was heat." becomes: "He had found his first limit. The limit he found was heat,
    specifically overheating." [CT]
17. "The machine that had dissolved three careers at the Bear Flag needed watts. It needed cooling." becomes: "The
    machine that had ended three careers at the Bear Flag needed watts, of course, but it also needed cooling."
    [CT] The paragraph goes on as before ("It ran on the same dumb physics...").
18. "He didn't tell Devendra any of this. One tower in one apartment was an n of one." becomes "He didn't tell
    Devendra any of this. One tower in one apartment wasn't much of a prediction engine." [CT]
19. Last line of the chapter becomes: "He left the tower off for a week. Then he opened the notebook where he'd
    scrawled MADRONE IS NOT A DRONE, turned to a clean page, and started writing." [CT. Changes: "written" to
    "scrawled", "wrote the date at the top" cut, "started keeping track" to "started writing".]

### Chapter 2: The Coin Slot

21. At the all-hands, "He was done being surprised. He would write things down before they happened." becomes: "He
    was done being blindsided. He would try to pay closer attention." [CT]
    Knock-on at the end of the chapter: "That night Elijah sat at the kitchen table with the notebook and did what
    he'd promised. He wrote it down before it happened." becomes "...did what he'd promised. He paid closer
    attention, and he wrote down what he saw coming." [Claude] The list of stages still follows it. (Marta's line in
    Ch 18, "You're trying to watch every bad thing closely enough that it can't surprise you", fits the new promise.)
22 and 25. The texts with Wes. After "Let me look into it, he sent.", the line "He never did." is replaced by:

    > A minute later Wes sent a link. It was a hit piece on how much water Companion was going to drink.
    >
    > is this true
    >
    > Elijah didn't answer. He meant to do it, but he never got the chance.

    [CT: the link to a hit piece about water use, "is this true", Elijah never answers, and "He meant to do it,
    but he never got the chance." The first two sentences are Claude's wording. Companion is the book's name for
    the new Claypot product.]
    Callbacks [CT asked for a throwaway mention of the article]:
    - Ch 6: "Above the box, still, was Wes. is my stuff in that thing. Under it, his own. Let me look into it.
      Nobody had written in there since." becomes "...Under it, his own. Let me look into it. Under that, Wes's
      link to the water article. Nobody had written in there since."
    - Ch 13: "...to Wes. is my stuff in that thing. Under it, Let me look into it. He sat with the two of them for a
      while." becomes "...Under it, Let me look into it. Under that, the link to the water article. He sat with them
      for a while." [Claude]
    - Worth knowing: in Ch 27 Elijah finally answers the water claim, to the co-op: "A question doesn't drink a
      bottle. It's the big sites. The cooling." Nothing to change there.
23. Lena. He does not follow her to her car. Replace everything from "Afterward he went looking for the woman from
    illustration tools." through "She got in and slammed the door. He stood there while she backed out." with:

    > In the shuffle afterward, with everybody talking and comparing notes, some people excited and some maybe
    > apprehensive, Elijah saw the woman from illustration tools gathering her things. He wanted to ask her about what
    > she'd said. He went over. Her badge was clipped to her bag. LENA, it said, and under that, ILLUSTRATION.
    >
    > "Hey," he said, gently. "I liked what you said there."
    >
    > She looked up. She looked at his badge. "You're data team."
    >
    > "Yeah. I mean, I worked on some of it."
    >
    > "Then don't." She started putting things back in her bag.
    >
    > "Look, I'm not trying to…"
    >
    > "I said don't." She zipped the bag. "God, you people don't have any concern for what other people want. You just
    > think about you."
    >
    > She left.

    [CT's beats and dialogue; "You're data team." is kept from the book. The narration is Claude's.] Chapter 9 still
    fits: "A woman named Lena from illustration stood up at our all-hands and asked what the artists get, and nobody
    answered her."
    The next paragraph, "He went back up and found Devendra at the good coffee machine, watching the drip like it
    owed him money.", becomes: "Feeling weird, he went looking for a familiar face, a friendlier one, and found
    Devendra at the good coffee machine, watching the drip like it owed him money." [CT's beat]
24. Devendra after the all-hands. After "The sticky note was still on the side of it.", replace the exchange from
    "Good quarter," Devendra said... through "He rinsed his cup and went back to his desk." with:

    > Devendra looked at him. "You doing okay? You look a little rattled."
    >
    > "Well, I just had a weird exchange with that woman who spoke."
    >
    > "Don't mind people like that," Devendra said. "People like that have always existed. Luddites. They'll come
    > around. They always do. And if they don't, then, well, maybe she should start looking for another job."
    >
    > "Yeah, but you know what they called it when the commons got fenced? Enclosure. The land didn't stop
    > producing. It just stopped being theirs. All you have to build is the fence." Elijah nodded at the screen still
    > glowing through the commons doorway. "Don't we have a responsibility to caretake the rollout? Mitigate some of
    > these effects?"
    >
    > "Why?"
    >
    > They looked at each other for a second. Behind them the commons was thinning out, people drifting back toward
    > their desks.
    >
    > "What do you mean, why?"
    >
    > "I'm not their dad. You're not their mom." Devendra slapped him on the shoulder. "Man. You did a good thing
    > contributing to this. I'm really proud of you. We're going to change the world."
    >
    > Then he turned around and walked away.
    >
    > Elijah was left with a pit in his stomach.

    [CT's lines and beats. Claude: the tags, the commons thinning out, and keeping a short form of the book's
    enclosure lines inside Elijah's question.] Why the fence stays: two later lines point back at it. Ch 6, in the
    layoff meeting, he imagines saying "the realtors, the pipeline with his name in the commits, the fence, the
    notebook." Ch 33, to Grace: "And the fence at Claypot. It's all one thing." Both would lose their meaning if
    the enclosure beat were cut from Chapter 2.
    Cut from the book's version: "Good quarter" and the moat line, the hedges and Parliament, "That's the hedge. I
    helped plant it.", and "You did. And you took the bonus." Nothing later depends on them (the bonus comes up
    again on its own in Ch 10; Reuben gives the full enclosure history in Ch 23).

### Meanwhile (the first one, after Chapter 2: Bidwell and his reader)

26. "Corpus. The body of work. Everything anyone ever made with the software." becomes "...Everything anyone ever
    made with their software and stored on their servers." [CT]
27. "Find out what the dirt costs," he said. becomes "Find out what their dirt costs," he said. [CT]

### Chapter 3: A Satellite Over the Star Thistle

28. The Architect's lecture video:

    > "I am often asked if I am afraid of it," she said. "I am not. I am afraid of us. I am afraid of what mankind
    > might do with such a thing."
    >
    > The pit in Elijah's stomach grew deeper.
    >
    > "We do not exactly have a glowing track record with new technology."

    [CT. Claude: "We do not" instead of "We don't", because she never uses a contraction anywhere in the book.]
    Then "Elijah wrote it all down. Then he watched it again." as before. Her Chapter 9 callback ("I said once, in a
    lecture, that I was afraid of us. I was being polite.") still fits.
70. Who Manny is (CT: "It's Manny. Who the fuck is Manny?"). He is introduced only by name in Ch 3 and Ch 7, and the
    book explains him for the first time after his phone call in Ch 13. He matters later: Elijah ends the book
    sleeping in Manny's back room and digging his soil pits behind Manny's barn. [Claude's wording]
    - Ch 3, on the phone with his mother, after "Pump's doing that thing again. Manny says it's the pressure switch.
      The well man says it's the pump." add: "Manny had the next place over. He had been fixing things on theirs
      since Elijah's father got sick." (Then "A pause, the sound of the pot being set in the rack..." as before.)
    - Ch 13, the call: "It's Manny." The radio was on behind him. "I'm at the house, Elijah..." becomes "It's Manny.
      From next door." The radio was on behind him. "I'm at the house, Elijah..."
    - Ch 13, later: "Manny had smelled it from the yard. Manny had the next place over and had been fixing things on
      theirs since Elijah's father got sick. All his life..." becomes "Manny had smelled it from the yard. All his
      life..." (the introduction has moved to Ch 3).

29. "The phone rang at 9:40 on Sunday, because it always rang at 9:40 on Sunday." becomes "The phone rang at 9:40 on
    Sunday because it always rang around 9:40 every Sunday. That was church time." [CT]
30. The Sunday call is in the MORNING everywhere. [CT: "morning, change the other chapters to match". Every line
    below is Claude's, to make that true.]
    - Ch 3: "She called when her day ended, whether she had seen him that week or not." becomes "She called on her
      way out the door, whether she had seen him that week or not." (The radio, the running water and the pot still
      fit: breakfast dishes before church.)
    - Ch 3, after the call, see edit 61: the satellite he watches has to be at night.
    - Ch 5: see edits 38, 39 and 62.
    - Ch 7: see edit 41.
    - Ch 13: see edit 31. This is the one call that comes at night, on purpose.
    - Ch 15, living in the truck: "At 9:40 that night, back under the sycamore, the phone did not ring." becomes "The
      next Sunday at 9:40 in the morning, under the sycamore, the phone did not ring." The rest stays ("He watched it
      not ring. Then he played the voicemail. After that he did it every week.").
    - Ch 15, before he goes north: "Sundays," he said. "Nine-forty at night. I'm going to call. Could you just hold it
      by her ear?" becomes "Sundays," he said. "Nine-forty in the morning. I'm going to call. Could somebody just
      hold it by her ear?" (He still asks the night aide, who returns in Ch 37.)
    - Ch 17: "The night aide held the phone by his mother's ear." becomes "The aide held the phone by his mother's
      ear."
    - Ch 18: "At 9:40 that night he called the place with the rose garden" becomes "At 9:40 he called the place with
      the rose garden" (Marta came by at eight that morning and soup is at noon). "The night aide" becomes "The
      aide", and "that was all for tonight, honey" becomes "that was all for today, honey".
    - Ch 22, the Sunday of Ray's funeral: "The night before, at 9:40, he called the rose garden." becomes "The
      morning before, at 9:40, he called the rose garden." The aide's "She's been looking at that door all day. Her
      Sunday company didn't come." becomes "She keeps looking at that door. She's waiting on her Sunday company." "He
      took it to mean the church." stays. (Her Sunday company was Ray, who signed in on Sunday mornings and is being
      buried that day; at 9:40 he is not late yet, so she is still waiting.)
    - Ch 24, the first fire in the stove room: "It was a Sunday. At 9:40 he stepped out under the eave and called the
      rose garden." becomes "It was a Saturday. The next morning at 9:40 he stepped out under the eave and called the
      rose garden." (That gathering runs past eleven at night.)
    - Ch 31: "At 9:40 that night he called the rose garden." becomes "On Sunday at 9:40 he called the rose garden.";
      "The aide said she'd had a good day" becomes "The aide said she'd had a good night"; and "In the morning it was
      the first of the month, the day for the pit." becomes "The next morning was the first of the month, the day for
      the pit."
    - No change needed: Ch 24 "The next Sunday at 9:40", Ch 25 ("Elijah called him on Sundays, after his mother"),
      Ch 32, Ch 37 (the night aide; the lamp that "talks to her at night"; the visitor book, "D. McGrath, 10:15").
31. One call comes at night, as a sign something is off with his mother: she thinks it is morning. [CT's idea.
    Claude chose the call and the wording.] It is the Chapter 13 call, the Sunday before her stroke, the one he lets
    ring. Her voicemail from it holds the last whole sentences she ever says to him.
    - Ch 13: "On Sunday at 9:40 the phone rang on the dash. He watched it until it stopped. Then he typed Working
      late. All good. Love you, and sent it, and turned the phone off." becomes "On Sunday at 9:40 the phone rang on
      the dash. It was dark out, and he was too sick to wonder why. He watched it until it stopped. Then he typed
      Working. All good. Love you, and sent it, and put the phone down on the seat, and passed out." (The scene that
      follows is edit 69.) [CT, 2026-11-25: reading "at 9:40" he
      pictures morning, so "Working late" is wrong; his option, "it rang at 9:40 p.m. and Elijah was still too sick to
      notice". Claude's wording. "It was dark out" tells the reader it is night; Elijah doesn't register it. "Working.
      All good." also matches how Chapter 31 quotes his texts.]
    - Ch 13: "There was one voicemail, from Sunday, 9:41." becomes "There was one voicemail, from Sunday, 9:41 p.m."
      (This is where the hour first registers, on Tuesday, when he turns the phone back on.)
    - Ch 14, the voicemail: "Hi, baby. I watched your video." becomes "Morning, baby. I watched your video." The rest
      of it is unchanged.
32. In the notebook: "It takes the people who see it coming, out of the world everyone they love still lives in."
    becomes "...out of the world everyone they love still believes in." [CT]
61. Knock-on of the morning call [Claude]. After the call the book has him at the window watching "a satellite
    dragging itself across the dark", which is the chapter's title image and cannot happen at 9:40 in the morning.
    "After she hung up he stood there a long time. Outside, over the parking lot, the sky had that washed orange
    glow..." becomes "After she hung up he stood there a long time. He was back at the same window that night.
    Outside, over the parking lot, the sky had that washed orange glow..." The rest is unchanged.

### Chapter 4: Cell G14

33. "He typed it in scientific notation, 3.8 times ten to the twenty-sixth watts, and sat back, and felt nothing."
    becomes "He typed it in scientific notation, 3.8 times ten to the twenty-sixth watts, and sat back. He felt
    nearly nothing." [CT: "...and sat back. He felt nearly nothing." Claude kept the number in the sentence, because
    the next paragraph refers back to it.]
34. Last line of the chapter: "The electric bill was in the mailbox that Monday." becomes "The new electric bill
    would show up next Monday, and Elijah was dreading it." [CT]

### Chapter 5: The Tenant Who Paid No Rent

35. The bill: "$211.46" becomes "$2,011". [CT] Knock-on [Claude]: "A hundred and seventy dollars of difference
    between a man who thinks about machine intelligence and a man who runs it" becomes "Nearly two thousand dollars
    of difference between...".
    Note for CT (Claude's estimate, not checked against a real bill): the book says the tower draws 600 watts flat
    out. Running all month that is about 430 kWh, roughly $150 to $250 at California residential rates, so $2,011 is
    about ten times what one tower could run up.
62. Knock-ons of edits 34 and 30 [Claude]:
    - He now dreads the bill, so "This one he opened over the kitchen sink out of pure Monday inertia" becomes "This
      one he opened over the kitchen sink, braced for it". ("The envelope was thin, which fooled him." stays.)
    - The amp scene is now a Sunday morning, so "He unplugged the cable box on his way to bed." becomes "That night,
      on his way to bed, he unplugged the cable box."
36. After the paragraph ending "My dad told me, 'You and your mother shouldn't have to pay the interest on my
    sins.'", a new paragraph:

    > David loved him for it. Whatever else his father had gotten wrong, when it counted he had put the two of them
    > first. That was why Ray still had his stool at the end of the bar, club soda and lime, every night. He
    > sometimes still fell asleep on the bar top, even though he didn't drink. Alcohol is not the only vice.

    [The last two sentences are CT's words. The first three are Claude's wording of CT's beat. CT approved the
    paragraph: "Yeah, that's better."]
37. "Horses don't take anybody's job, Ray," he said. becomes:

    > "Horses don't take anybody's job, Ray," he said, deadpan. He didn't realize how heavy that was. Everybody
    > else did.

    [CT's beat and "deadpan"; the two short sentences are Claude's.]
38. "On Sunday he got the amp out of the hall closet, where it had been sitting in its bag since the last gig before
    the pandemic." becomes:

    > Back home in his apartment that weekend, Elijah was waiting for a call from his mother, and decided to kill
    > some time with a jam. He got the amp out of the hall closet, where it had been sitting in its bag since the
    > last gig before the pandemic.

    [CT] Knock-on [Claude]: "He set it in the corner of the living room and didn't plug anything into it, as a
    monument, which was the point." becomes "He never got around to the jam. He set it in the corner of the living
    room and didn't plug anything into it, as a monument, which was the point."
39. The call that doesn't come. New paragraphs after "...as a monument, which was the point." and before "He put his
    hand flat on the grille...":

    > The call never came. He looked at the clock. It was 10:30. That didn't make sense.
    >
    > He called her. It rang until the machine picked up, and there they were, the two of them, from years ago. His
    > own voice first: "Hello, you've reached the Madrones." Then hers: "Please leave a message after the beep."
    >
    > "Hey, Ma. Haven't heard from you. Hope everything's going okay. Don't make me call the local hospitals, all
    > right? You're probably just busy with Joan. Give me a call when you get a chance, all right?"

    [CT's beats, the greeting and the message. Claude: the first paragraph, "the two of them, from years ago", and
    Joan (Joan Hollis, Ma's neighbor, already in the book) instead of a new "Margaret".]

### Chapter 6: Four Minutes and Eleven Seconds

40. After "He posted the video there, with no caption, because he couldn't think of one." add: "He didn't think
    about it much. He'd been posting on that page for years as a musician. He just wanted to put it out there in the
    world." [CT's beat, close to his words]
    (The band chat line in this chapter changes under edits 22 and 25.)

### Chapter 7: You're Early

42. "By Friday it was four hundred replies and he quit counting." becomes "By Friday it was four thousand replies
    and he quit counting." [CT]
60. Knock-ons of edit 42 [Claude], both in the January scene with David: "He had a senator's office and a lab and
    hundreds of strangers." becomes "...thousands of strangers.", and "there's this woman in Tulsa, there's hundreds
    of them" becomes "...there's thousands of them".
41. "His mother called at 9:40 on a Sunday, the way she did." becomes "His mother called at 9:55 that Sunday. A
    little late, but not terribly unusual." [CT] (In this call the book already has her tell him about the video as
    if for the first time, though she watched it in October and wrote to him about it twice.)
43. "I pour beer, Mad. What's it going to do, pour it?" becomes "I pour beer, Mad. What's it gonna do? Yank the tap
    handle?" [CT; "tap" for his dictated "tab"]

### Chapter 8: Elijah Madrona

44. "They wore a lot of gray and they said off-ramp and guardrails." becomes "...they said guardrails and slow
    down."; "...and they said ship." becomes "...and they said ship and accelerate." [CT]
45. The woman at the coffee urn (the cooling founder). The paragraph introducing her ends "She looked at the room,
    and then at him." in place of "She looked at the room and spoke low, not really to him." Then:

    > "You know, you look pretty green."
    >
    > "I've never done anything like this before."
    >
    > "I thought not." She leaned in close. He could smell her perfume, and it was nice, and he felt a rush. She was
    > pretty attractive. Her hair brushed his cheek, and she said it right into his ear.
    >
    > "Trust no one. Don't take the golden handcuffs."
    >
    > She backed up, looked him right in the eyes, and nodded. "Nobody in here has any friends."
    >
    > Elijah looked around the room. They all looked like friends to him.
    >
    > Then somebody called her name, and her whole face came back on, and she went.

    [CT's beats and dialogue. Narration is Claude's; "her whole face came back on" is kept from the book.] Payoffs
    already in the book: in Ch 12 he texts four people from that room for help and she is the only one who answers,
    with a heart; Ch 14 remembers it. Ruby's million (edit 53) is the golden handcuffs.
46. The panel moderator:

    > "Elijah, your video went parabolic," the moderator said. "And your music is fantastic. We all love what you
    > bring to the table. Now, your biggest video, of course we've all seen it. But some of your recent ones seem to
    > be going into a little more of the nuance of what we're all going through. Tell me, do you fancy yourself sort
    > of the people's forecaster?"
    >
    > The room laughed nicely. Elijah didn't really know how to answer. "I, uh. I mean..."
    >
    > "Don't answer that. Don't worry about it. Listen. Everybody keeps saying AGI. I keep hearing it from all my
    > friends. It hasn't quite hit the mainstream yet. For anybody watching, can you define AGI for us?"

    [CT. Claude: the stammer words, and the room's laugh placed after the forecaster question.] "He knew this. He'd
    watched the Architect's old lecture..." follows as before.
47. After the panel, the woman who sat on his left:

    > On his way out, the woman who had sat on his left found him at the coffee urn. She didn't pat him. "Both sides
    > like you," she said. "Don't ruin that. You have no idea how valuable it is to be able to speak your mind and not
    > worry what anyone thinks about it."
    >
    > "What do you think I should do?"
    >
    > "You want my opinion on what you should do?"
    >
    > "Yeah. To be honest with you, I feel a little out of my depth here."
    >
    > She looked at him. "You are." She picked up her cup. "That's your advantage. You have beginner's luck. What you
    > choose to do with it is up to you."
    >
    > She took her coffee back into the hall.

    [CT's dialogue. "She looked at him." and "She picked up her cup." are Claude's.] Gone: "because you never say
    what anyone should do" and "That's not a forecast. It's a mirror."
48. Ruby by the dumpster:

    > "The replies. Under your video. You answered all of them the first day. I read them."
    >
    > "Yeah. Why wouldn't I?"
    >
    > "Nobody does that, man." He had a quick, light voice, like someone who'd never had to wait for a turn. "The
    > forklift lady. The drummer. Some guy named Earl who thinks you're a demon, and you wrote Earl three paragraphs.
    > There's way too many now. You must have given up."
    >
    > "No."
    >
    > "Then you have to stop that."
    >
    > "Why?"
    >
    > "Because there's four thousand of them and one of you. And tomorrow it'll be eight thousand. Who knows what
    > it'll be next week? Do you know how this game goes?"

    [CT: "the first day", "Yeah. Why wouldn't I?", "Nobody does that, man.", "There's way too many now. You must have
    given up.", and the last line. Claude: Elijah's "No." and Ruby's "Then you have to stop that.", to join them.
    Kept from the book: "I read them.", his voice, the Earl lines.] "He stood up and wiped his hand on his jeans and
    held it out. 'Ruby.'" follows. Gone: "All four hundred, and then you kept going", "next month it's forty
    thousand" and "It's arithmetic."

### Chapter 9: The Wrong Verb

49. In the kitchen, after "The singularity," Ruby said, with his mouth full. and before "It is borrowed from
    physics...":

    > "Do you know what it means?"
    >
    > "Of course I know what it means."
    >
    > "I do not believe you."
    >
    > "It's just a single point."
    >
    > "It is so much more than that."
    >
    > "Okay. Well then, enlighten me."

    [CT. Claude: no contractions for her.]
50. "I would like it to remember you. I spend some of my time on that." becomes "I would like it to remember you. I
    spend much of my time working out how to make it care." [CT, his corrected wording]
51. "The trucker cried," Ruby said. "She didn't like that." CT: very confusing. It becomes: "That trucker she talked
    about? He cried on her," Ruby said. "She didn't like that." [Claude. It points back to her line earlier in the
    scene, "One year it was a man who drove trucks", and explains why she left without meeting Elijah.]

### Chapter 10: Frozen Peas

52. "It tasted like the best night of his twenties." becomes "It tasted like the best nights of his twenties." [CT]
53. Ruby raises the offer. From "It's downstairs. They moved it." through "The truck was at the curb with a full
    tank. He hadn't asked for that either.":

    > "It's downstairs. They moved it."
    >
    > Of course they had. Ruby walked him to the elevator in his socks. He stood there with his hands in the hoodie
    > pocket while they waited for it.
    >
    > "How about half a mill?"
    >
    > "Nah. I'm sorry."
    >
    > "The full million?"
    >
    > Elijah froze. He was really standing there. He was being offered a million dollars, on the spot, just to
    > exist.
    >
    > "Ruby, I really appreciate it, but I really should be going."
    >
    > "Suit yourself, man. Hey, if you're ever in the city, give me a call. I'd love to do this again."
    >
    > He took Elijah's phone out of his hand and thumbed the number in himself, fast, and handed it back. He meant it.
    > A man like Ruby had people to do that for him.
    >
    > "Yeah," Elijah said. "No, yeah. For sure."
    >
    > The doors closed on him standing in all that white.
    >
    > Elijah walked out to his truck, having just turned down retirement. It was at the curb with a full tank. He
    > hadn't asked for that either.

    [CT: the offers ("half a mill" as words, never a number), Elijah's answers, "Suit yourself, man", "having just
    turned down retirement". Kept from the book: the elevator, the city line CT likes, the phone, the doors. The
    rest is Claude's.] It fits what Ruby says earlier on the fire escape, "Everybody says no the first time." The
    first offer was triple his $140,000, about $420,000, so half a mill is a casual $80,000 bump.

63. Why he said no. A new paragraph right after "Elijah walked out to his truck, having just turned down retirement.
    It was at the curb with a full tank. He hadn't asked for that either." and before "He sat behind the wheel with
    the dome light on and looked at the phone.":

    > He didn't know why he listened to her and not Ruby. I mean, Ruby had invited him and made the whole thing
    > happen, but this woman was just some face in the crowd. He didn't even remember her name. But there was truth
    > in her eyes. There was sincerity. He was always someone who had trusted his gut.

    [CT's words, as he said them. Placement is Claude's: it answers the reader's "why did he just do that?" at the
    moment he does it, and points back to the whisper in edit 45.]

### Meanwhile (the second one, after Chapter 10)

54. "Half of it believes him. The other half made a song about him." becomes "...The other half is laughing at a song
    about him." [CT]

### The million, remembered (Chapters 11 to 31)

CT: "When things get hard, he can remember that conversation. When stuff goes on with his mom, he can remember that
talk. But then he can also remember the woman's words." Placement and wording are Claude's.

58. Lines in the book that already mention the offer, brought up to date:
    - Ch 11, in the truck with Gus: "He offered me a job," Elijah said. "Ruby. For doing nothing. Triple what I
      made." becomes "...For doing nothing. A million dollars." Gus's answer changes under edit 64.
    - Ch 31: "He had turned down the triple salary and the ads and the room." becomes "He had turned down the
      million dollars and the ads and the room."
55. New lines:
    - Ch 12, sick in the truck outside the launch party, thumb over Ruby's number. After "One more person who wanted
      something." add: "Six months ago that kid had offered him a million dollars at an elevator, and he had said
      no."
    - Ch 14, under the madrones, at the end of the paragraph that ends "...a face was worth exactly a heart from a
      woman with a cooling company. He had bolted two million dollars of robot arms to a floor and he was not on the
      list." add: "He had turned down a million dollars at an elevator. Trust no one, she had said into his ear.
      Don't take the golden handcuffs. He had taken her advice, and here he was."
    - Ch 15, paying for his mother's room, after "Every twenty he took out came off the far end of her room." add:
      "A million dollars would have pushed the far end of that room out past where he could see it. He did that
      division too, once, and then he stopped doing it."

### Chapter 11: It's Always a Strap

64. In the truck with Gus, after "You take it?" / "No.": "Good. The ones for nothing are the expensive ones." becomes
    "Good. The ones they offer you for nothing usually cost the most in the end." [CT]
    With edit 58 the exchange reads: "He offered me a job," Elijah said. "Ruby. For doing nothing. A million
    dollars." / "You take it?" / "No." / "Good. The ones they offer you for nothing usually cost the most in the
    end."

65. Gus's pitch for the show. He plays his cards too soon (CT: "Nobody would do that if they're trying to sell
    somebody on an idea"), so the admission moves to after Elijah says no.
    - Cut from the pitch: He kept his eyes on the road. "Truth is, I've got a shop full of arms nobody wanted and a
      bus with nobody in the other seat. I'm tired of driving it alone." The pitch ends on "I'll fly you out to the
      shop next week. Let's do it." and goes straight to "It was a good idea. Elijah could see it."
    - After Elijah's no and "Elijah braced. He figured the air would change...", Gus's reply "Your choice," Gus
      said. "I can't force you to do it." becomes:

      > "Yeah, I figured," Gus said. "Thought I'd ask, though." He kept his eyes on the road. "Truth is, I got a
      > bunch of arms nobody wants, and I'm just tired of driving alone. If you ever do want to, though, I'll give
      > you my number."

    - Then "Gus reached over and turned the radio up a little..." as before.
    - At the cannery dock. "When the last arm was off the truck, he took a pen out of his jacket and wrote on the
      back of a gas receipt and handed it to Elijah." stays. The next line, "Here's my phone number. Give me a call if
      you ever want to talk about anything.", becomes:

      > Elijah started to tell him he didn't have to.
      >
      > "No, take my number. I meant it. Here." He pushed the receipt at him. "Give me a call if you ever want to talk
      > about anything."

      Then the rest as before: "Okay. Thanks. I mean it, thank you." / "Sure." / the bus to go look at / "Oh, by the
      way. I saw that you're working on a book. Let me know when it comes out." [CT: "No, take my number, I meant
      it. Here." Claude: Elijah starting to wave it off, so Gus's "No" answers something, and "He pushed the receipt
      at him." "Give me a call if you ever want to talk about anything." is kept from the book. Elijah's "I mean it"
      now echoes Gus's "I meant it".]

    [CT's lines; "tired of driving alone" for his dictated "driving along". Claude: "Gus said", "He kept his eyes on
    the road" (moved from the cut paragraph), and "I'll give you my number" as the way he offers it, since he hands
    it over at the dock. Writing context from CT, not for the page: Gus had a feeling Elijah would say no, which is
    why he lets it slip. The chapter already counts him as billionaire number two: "Two billionaires, two phone
    numbers."]

66. Why he is at the cannery: the promise is two of the arms (CT: "the promise is that he's going to get two of the
    arms, that they'll be his. That's where the connection is. And that's where his insurance policy is ... It's
    enough to survive off of. It's his big emergency fund that comes into play later in the book. But right now, it
    just needs to be more clear how this bridges with the rest of the stuff.") In v5 the arms only turn up in
    Chapter 15, as a surprise, "in place of his wages". Now they are the deal from the start. [CT's facts; all
    wording Claude's; no dollar figures added.]
    - Ch 11: after "I can carry stuff," Elijah said. "I drove delivery for six years. I'm good at carrying stuff.",
      the line "So they let him carry stuff." becomes:

      > Trent thought about that. They had six robot arms coming down from Oakland, a launch party in three weeks
      > and nobody to put them in. They also had two spares in crates that they were never going to need. "Tell you
      > what," he said. "Ride down with the arms. Help the crew bolt them in for the launch. Do that, and the two
      > spares are yours."
      >
      > Elijah didn't know what one of those was worth. He knew it was more than he had. It wasn't a salary. It was
      > an insurance policy, something to stand on if the floor went out.
      >
      > So they let him carry stuff.

    - Ch 11, when Gus prices them. After Gus's paragraph that starts "About three-thirty apiece, installed." and
      before Elijah's "They're yours?", add a line: "Elijah did the arithmetic on two of them and kept it to
      himself."
    - Ch 12, first line: "He worked at the cannery for three weeks on a promise." becomes "He worked at the cannery
      for three weeks on Trent's promise."
    - Ch 12, the paid guy at lunch: "'You on the books?' Elijah said they were sorting him out Friday." becomes
      "'You on the books?' Elijah said he was getting paid in arms. Two of them, Friday." The guy's answer stays:
      "He's done this to two guys already. You're working for a picture, man." So does "Elijah said Trent was good
      for it." and Trent's "We'll sort you out Friday."
    - Ch 15: "In the second week Trent's office finally wrote back. There was no money for him, a woman said, and
      she was sorry about that. But two spare arms were still sitting on the cannery dock in their crates, never
      unpacked, and the company would sign them over in place of his wages if he could get them off the property by
      Friday." becomes "In the second week Trent's office finally wrote back. The two spare arms were still sitting
      on the cannery dock in their crates, never unpacked, a woman said, and the company would sign them over, the
      way Trent had promised, if he could get them off the property by Friday." The rest of Chapter 15 stays: the
      storage unit, no bids on eBay, the scrap offer, "there were always the arms. He could sell them." That is the
      insurance policy failing to pay out, which is the point.
    - Nothing changes later: the arms go north in Ch 17, and in Ch 34 to 37 they are the emergency fund that comes
      into play.

### Chapter 12: The Seventeen-Dollar Shower

67. Sick in the truck after the launch party. The jump to "if he died" is too fast (CT: he's not depressed, he's
    overwhelmed and sick from doing too much; he doesn't want to bother anybody, he already feels like enough of a
    bother, so he decides to sleep it off in the truck; the "if he died" line is his humor, and it gets worse from
    there). After "The phone went face down on the dash.", the paragraph "He wasn't angry. He was too sick to be
    angry. He'd spent ten months saying yes to people. If he died in this truck tonight, the party would go until
    one. Somebody would notice the Ranger on Monday. They just didn't have a place to put him." becomes:

    > He wasn't angry. He was too sick to be angry, and too tired. He'd spent ten months saying yes to people on four
    > hours of sleep, and somewhere in there his body had stopped asking his permission. He didn't want to be a
    > bother. He had been underfoot at his mother's, and a lot at the Bear Flag, and one more person who wanted
    > something everywhere else. He'd sleep it off. People slept things off in trucks all the time.
    >
    > He pulled the jacket up to his chin. If he died in this truck tonight, he thought, the party would go until
    > one, and somebody would notice the Ranger on Monday. It was almost funny. They just didn't have a place to put
    > him.

    [CT's beats. Claude's wording; "underfoot" calls back his mother's "You're underfoot" in Chapter 11, and "one
    more person who wanted something" calls back the Ruby text a few paragraphs earlier. "It was almost funny." is
    there so the line reads as his humor. "They just didn't have a place to put him." is kept from the book.]
    Chapter 13 still opens "In the morning the fever was down enough to drive.", which is him having slept it off,
    and things get worse from there.

### Chapter 13: The Buckets in the Barn

68. First lines of the chapter. "In the morning the fever was down enough to drive. He did not go in to get sorted
    out." becomes "In the morning the fever was down enough to drive. He decided not to go to the hospital. He was
    tough. He could tough it out." [CT]
    Note: "go in to get sorted out" probably meant going into the cannery office to get paid, echoing Trent's "We'll
    sort you out Friday". With CT's line that echo is gone; the arms deal (edit 66) is still settled in Chapter 15.
69. The morning after the night call (CT: he passes out, wakes Monday in the truck, the phone is dead, he starts the
    truck to charge it and waits; no direction, just reflecting; choked up but can't cry, still in go mode; a young
    couple sharing a cup of frozen yogurt; he wants that; he thinks about his last relationship a few years ago, how
    it went, and remembers why he isn't dating and doesn't plan to soon). Replaces "He turned it back on Tuesday, to
    look for work." Everything between the night call (edit 31) and "At two in the afternoon the phone rang in his
    hand" becomes:

    > When he woke up it was Monday. He had slept in the truck all night, sitting up, with his jacket over him. The
    > first thing he did was reach for the phone. It was dead.
    >
    > He needed a charge. He started the truck, plugged the phone into the lighter, and sat there with the engine
    > running and the needle on a quarter tank.
    >
    > Downtown Stockton went about its Monday. A man hosed off the sidewalk in front of a check-cashing place. A bus
    > went by with nobody on it. He didn't have anywhere to be. That was new. For ten months there had always been
    > somewhere to be, and now there was a side street, and a truck, and a phone that wouldn't turn on.
    >
    > His throat got tight. He waited for it to turn into something, and it didn't. He was still in go mode. Some
    > part of him was still standing on the cannery dock, waiting for Friday.
    >
    > Across the street was a frozen yogurt place. A couple came out of it, young, sharing one cup with two spoons,
    > bumping shoulders, arguing about something that made them both laugh. He watched them all the way to the
    > corner.
    >
    > He wanted that. He hadn't let himself want it in a while.
    >
    > The last time had been a few years ago. It had gone the way his things went. He'd said yes to everything and
    > been easy to be around, and one day there wasn't enough of him left to be with. She had said that, more or
    > less, on her way out. He'd told her she was right, and he had meant it.
    >
    > That was why. He had nothing to offer anybody right now but a truck and a list, and he knew exactly how he would
    > do it again.
    >
    > The phone came on. There was one voicemail, from Sunday, 9:41 p.m. He would listen to it later. He would listen
    > to it a great many times.

    Then "At two in the afternoon the phone rang in his hand, and it was her number. She never called at two in the
    afternoon." as before; the call from Manny is now on Monday. [CT's beats. Claude's wording. The ex is not named
    and gets no details beyond why it ended; nothing else in the book mentions a past relationship. Why it ended is
    Claude's: his saying yes until there is nothing left, the pattern the book already gives him ("Yeah. No, yeah, of
    course" in Ch 7, Wren's "You were saying yes the way people say it when they mean please" in Ch 31). It sets up
    Grace, where Ch 25 has him asking Marta "Does Grace have... someone?"]

71. After Manny's call: "He didn't remember the drive. He remembered the gauge." becomes "He didn't remember the
    drive." [CT] ("The gauge" was the gas gauge: a quarter tank, no money, two hours to Santa Rosa. Nobody could
    tell.)

72. At his mother's kitchen table, finding there is nobody to call. "...He had not heard her voice since the funeral,
    and he did not want to hear it now. He went down the list twice, to be sure." / "He was the call." becomes:

    > ...He had not heard her voice since the funeral, and he did not want to hear it now.
    >
    > He got up and went down the hall and ran cold water over his face. He went through the list every which way,
    > but the only person to call was staring at him in the bathroom mirror.

    [CT's last sentence. Claude's bridge: "He got up and went down the hall and ran cold water over his face.", so
    the mirror is really there; he was sitting at the kitchen table.]

73. The hospital woman with the lanyard. "Is there anybody else in the family who should be part of this?" / "No." /
    "Then it's you," she said, and she was sorry about it. becomes:

    > "Is there somebody else?"
    >
    > "No. It's just me."
    >
    > She nodded, with a knowing smile, and that was it.

    [CT]

74. The messages after the clip. "He read every one. His mother had raised him to answer a letter. He couldn't answer
    these, and he couldn't stop reading them." becomes "He read every one. His mother had always raised him to be
    someone who wrote back. He couldn't bring himself to answer these, but he also couldn't stop himself from
    reading." [CT]
    Knock-on [Claude]: the same phrase first appears in Ch 7, when the first messages come in: "They had taken the
    trouble to write, and his mother had raised him to answer a letter." becomes "...and his mother had raised him to
    be someone who wrote back." so the Ch 13 line still reads as a callback.

75. The illustrator in Petaluma. "One was from an illustrator in Petaluma he had never met. You built the thing that
    took my clients. Now you want my twenty? He read that one more than the rest." The last sentence becomes "He only
    needed to read that one once. It bounced around inside his head, rent-free, for days after." [CT]
    The message itself stays "Now you want my twenty?" (CT quoted it as "now you want my money"; "twenty" ties to the
    next paragraph, where he sends Tulsa her twenty back.)

76. In the hospital hallway. "...Forty feet away his mother was asking a nurse for Barry. He could not make it fit in
    one head, and the head was his." / "He didn't answer any of it." becomes:

    > ...Forty feet away his mother was asking a nurse for Barry.
    >
    > It was too much.
    >
    > He didn't answer any of it. He put his phone away and went for a walk to go buy cigarettes.

    [CT. Claude kept "He didn't answer any of it." because it closes out the offers in the paragraph before. He
    already smokes by then: Ch 12, "He had started smoking again in February, on a fire escape."]

77. The trust paper. "After his father died, and after Melody stood up at the funeral lunch and asked what the place
    was worth, a lawyer in town had put it in a trust. Elijah had signed a page at twenty-six and never thought about
    it again. He found it in the drawer under the bank's envelopes. It said that if she couldn't, he could." becomes:

    > After his father died, and after Melody stood up at the funeral lunch and asked what the place was worth, a
    > lawyer in town had put the farm in a trust. Elijah had signed a page at twenty-six and forgotten about it,
    > until now, going through his mother's important papers. He found it in the drawer under the bank's envelopes.
    > It named him the successor trustee. In plain words, it said that if she couldn't, he could. The farm was his to
    > sign for, and his to sell.

    [CT's beats: he signed at 26 and forgot, finds it rummaging through her papers, and the paper has to say what it
    is. Claude's wording and the legal term. CT suggested "executor of the will and power of attorney, or something
    like that"; an executor only acts after a death, and she is alive. For a farm held in a trust, the person who
    steps in is the successor trustee, and that is what lets him sell it to the man from Sacramento in the next
    scene. Claude's general knowledge, not checked with a lawyer.]
78. After the trust paper, before the man from Sacramento. Elijah sits with what the paper means and thinks about
    calling Ruby or a few other people, and then a car pulls in (CT: "A very nice yellow Oldsmobile. You don't see
    those anymore."). "The man from Sacramento came Monday, in a clean pickup, with a folder." becomes:

    > He sat at her table with it a long time. If she couldn't, he could. The farm, the barn, the well with the
    > pressure switch, his grandmother's hill. All of it was his to sign for now, and he had never signed for anything
    > bigger than a truck.
    >
    > He got the phone out and scrolled to ruby, lower case. A million dollars, at an elevator. He could call and say
    > he had changed his mind. He scrolled past it to Gus, and to David, and back up to ruby, and sat there with his
    > thumb over the screen.
    >
    > A car pulled into the driveway. It was a very nice yellow Oldsmobile. You don't see those anymore.
    >
    > The man from Sacramento got out with a folder.

    Then the next paragraph opens with a new sentence [CT]: "He was polite and kind, but firm. He was very sorry
    about Elijah's mother..." and goes on as before. ("He" for CT's "The man from Sacramento", since the line before
    already names him.)
    Knock-on: the notary's Camry is gone (edit 79 moves the signing to the bank), so the Oldsmobile is the only car.
    [CT: "we need to keep it consistent".] [CT's beats and the Oldsmobile lines. Claude's
    wording otherwise. The man no longer comes "Monday, in a clean pickup"; he arrives in the middle of this. Ruby's
    number here is the golden handcuffs coming back (edits 45, 53, 55).]

79. He doesn't just sign (CT: he'd tell the man to get bent, snap, yell, all the stress finally comes out; "I'll
    fucking figure it out"; he thinks of the robot arms and how they could be leveraged, everything he could have
    done, the money he turned down; then the dam breaks and he sobs over the kitchen counter where they made
    Christmas dinner, over the sink where his mom washed his hand after he took a digger and the gravel chewed his
    palm up, covered it in Crisco, an old wives' tale that kind of worked, and bandaged it; he looks around the house
    where he spent so much of his life wishing to be anywhere else; he calls David, who doesn't pick up; he cries
    harder, goes to bed crying, wakes up crying; when he gets himself together he thinks of everyone he could call
    for advice and comes up empty). After the man names the outfit ("...They liked the valley, he said."), and
    before "A notary came out and they did it on the kitchen table" (edit 78), insert:

    > Elijah stood up. "Get bent."
    >
    > The man didn't move. "Mr. Madrone..."
    >
    > "No. You don't get to come in here with a folder while she's lying in that bed." He was yelling. He could hear
    > himself, and he couldn't stop, and ten months of it came up at once. "That's my grandmother's hill out there.
    > This is her kitchen. I'll fucking figure it out."
    >
    > The man set the folder on the table, squared it to the edge, and put his card on top. "The offer's good through
    > Friday," he said. "I am sorry about your mother." The Oldsmobile backed down the drive.
    >
    > Elijah sat back down. He would figure it out. He went through it. The two arms Trent owed him, still crated on
    > the cannery dock; he had heard Gus say what one of those cost. The million he had turned down at an elevator.
    > The stages, the podcasts, the rate he didn't have. All the things he could have done, and hadn't.
    >
    > Then the dam broke.
    >
    > He sobbed. He stood over the kitchen counter where they had made every Christmas dinner of his life, and he
    > sobbed over the sink where his mother had washed out his hand the summer he took a digger in the driveway and
    > the gravel chewed his palm up. She had covered it in Crisco, an old wives' tale that kind of worked, and
    > bandaged it. He looked around the house where he had spent so much of his life wishing he was anywhere else.
    >
    > He called David. David didn't pick up.
    >
    > He cried harder. He went to bed that night crying, and he woke up the next morning crying.
    >
    > When he finally got himself together, he sat at the table and thought of everyone he could call for advice. He
    > came up empty.
    >
    > After staring at the card the man had left behind for what felt like an hour, Elijah picked up the phone.
    >
    > Before he signed anything, he took it all to the bank, to make sure what he was doing was legit. He may have
    > been naive, but he wasn't an idiot. The banker went through every page and said the paperwork was in order,
    > and asked if he wanted to use the bank's notary. He did. Elijah signed where the yellow tabs were, and the bank
    > faxed everything over to the man from Sacramento. Going through somebody in the middle made it all feel a
    > little safer.
    >
    > A few days later, on Friday, the wire cleared. The money went into an account that said Linda Madrone across
    > the top, with his name under hers, and the place with the rose garden took the first of it that afternoon.
    > Elijah knew his mother was safe.
    >
    > He did not keep any. He thought about it for the length of time it took the notary to find her stamp.

    This replaces the book's "A notary came out in a Camry and they did it on the kitchen table. Elijah signed where
    the yellow tabs were. On Friday, when it closed, the money would go into an account that said Linda Madrone
    across the top, with his name under hers, and the place with the rose garden would take the first of it that
    afternoon. / He did not keep any. He thought about it for the length of time it took the notary to find her
    stamp." [CT: the card and the phone, the bank first, "He may have been naive, but he wasn't an idiot", the bank's
    notary, the bank faxing it over, the intermediary feeling safer, the wire clearing a few days later, "Elijah knew
    his mother was safe". The DocuSign line from CT's earlier message is dropped, since his newer version runs it
    through the bank. Kept from the book: the yellow tabs, the account in her name, the rose garden, and the notary
    finding her stamp, which now happens at the bank. "On Friday" keeps David's later "Heard they close Friday"
    true.] "The buckets went with the place. He did not bring them up, and neither did the man." stays. [CT's beats and lines ("Get bent", "I'll fucking figure it out", "Then the dam broke" in
    substance, the digger, the Crisco, "came up empty", the card and the phone). Claude's wording otherwise.]
    Claude's calls:
    - The arms. In the book they only become his, and go into storage, in Chapter 15 (edit 66). Here they are still
      "the two arms Trent owed him, still crated on the cannery dock". CT said "the robot arms that he put in
      storage"; moving them into storage this early would need Chapter 15 reworked. CT can say so.
    - David. Later in this chapter: "David showed up Thursday morning with a hand truck in the back of his pickup. /
      Elijah hadn't called him. Nobody had." Now Elijah did call. That line becomes "Elijah had called him once and
      he hadn't picked up. Manny had called him." (CT chose Manny; see edit 81.)

80. Pruitt, outside the Bear Flag. He appears only in this chapter. "There were two men smoking out front. He knew one
    of them. Pruitt, who had the tire shop." becomes "There were two men smoking out front. He recognized one of
    them: Pruitt, from the tire shop, who had put every set of tires on the Ranger since Elijah bought it." [CT: "He
    recognized Pruitt from the tire shop. Or something like that." Claude's wording; the Ranger detail is added so
    the reader knows why Elijah knows him.]

81. David shows up Thursday with the hand truck. After "David showed up Thursday morning with a hand truck in the back
    of his pickup.", the book's "Elijah hadn't called him. Nobody had." becomes "Elijah had called him once and he
    hadn't picked up. Manny had called him." Then add: "He didn't mention the call. Neither did Elijah." Then
    "'Heard they close Friday,' David said." as before. [Claude's lines; CT approved both and chose Manny as the one
    who told David. Manny is at the farm that morning, lives next door, and David already knows him ("Manny's always
    right" in Ch 7).]

82. The last line of the chapter jumps from the rose garden to the farmhouse. "He left the key to the house on its
    kitchen table, on top of the mail." becomes a new paragraph:

    > Friday morning, he said goodbye to his childhood home, and to what he had always assumed would be his
    > inheritance. Everything he'd taken for granted. For some reason, all the tears he'd cried there were unavailable
    > to him now. Elijah simply laid the house key down on the kitchen table and allowed the door to lock behind him.

    [CT. Claude: "Friday morning," as the opening (CT dictated "Friday. Morning."), "now" for "in that moment", and
    "previously" dropped after "cried there". The tears are the ones from edit 79.] Chapter 14 follows as before.

### Chapter 15: The Twenty, Folded Small

83. Grace's invitation asks first (CT: he's been through a lot and won't just trust strangers from the internet; she
    is polite, asks permission and consent, asks what he wants; "We have a farm. We'd like to have you on it";
    "obviously we know who you are, but also that's not the point"; people up here think he'd bring a lot to the
    group; an offer to come stay a little while if he'd like; they don't expect him to take their word for it or to
    just come; a video call or two if he wants; "Up to you"). Her reply after "I don't want a boss. I don't want to be
    one either." / "She answered in an hour." keeps its first paragraph ("Good. We already have a welder who thinks
    she's the boss..."). The next line, "Come see. I'm sending gas money. If you hate it I'll buy your gas home too.",
    becomes:

    > We have a farm, and we'd like to have you on it. Obviously we know who you are, but that's not the point. The
    > point is, people up here think you'd bring a lot to the group, and we'd like to offer you the chance to come
    > stay with us for a little while, if you want to.
    >
    > We don't expect you to take our word for it, and we don't expect you to just come. You can get to know us
    > first. If you want, we could do a video call or two. Up to you.
    >
    > If you do come, I'll send gas money. If you hate it I'll buy your gas home too.

    Then "Blessings, / Grace / P.S. Eat something first..." as before.
    Later, the video call: "Early Sunday she put him on a video call with the kitchen." becomes "He asked for the
    video call. Early Sunday she put him on with the kitchen." The rest of that paragraph stays.
    [CT's beats and most of the words. Claude: the order, "If you do come" for the gas money, and "He asked for the
    video call", so it is his choice. It echoes the Architect in Ch 9: "I work on whether it asks first."]

84. His answer to the way she asks. After Grace's reply ("...Blessings, / Grace / P.S. Eat something first. It's two
    days of driving and you look thin.") and before "He read the last three words again.", add:

    > There was something about the way she asked that reminded Elijah of the truth he had seen in the eyes of the
    > woman from the conference. As burned and cautious as he was, something in him felt a tug.

    [CT] It points back to edit 63 ("there was truth in her eyes") and the whisper at the coffee urn in Ch 8 (edit 45).
    "The woman from the conference" replaces CT's first "the woman at Ruby's party", which could be read as the night
    at Ruby's place in Ch 10; CT approved the change.

56. The food bank line. "He got in it. Once, at the Bear Flag, he'd told David that people land where they put
    themselves. He stood in that line forty minutes, and he couldn't find one person in it who had." becomes "He got
    in it. Once, at the Bear Flag, David had told him people land somewhere. There's always a job. He stood in that
    line forty minutes. This was somewhere." [Claude, forced by edit 14. NEEDS CT (item 2).]

### Chapter 16: The Red Bin

85. Marta at the plasma table. "She jerked her chin toward the sparks. 'That could be worth something. Not an app.'"
    becomes "She gestured with her chin toward the sparks. 'That thing right there is worth something, not some
    app.'" [CT] It now points plainly at the work on the table; "In the quiet the plasma table ticked as it cooled."
    follows as before.
86. Marta hands him the broom. "'Swarf goes in the red bin,' she said. 'We'll see.'" becomes "'We'll see,' she said.
    'Swarf goes in the red bin.'" [CT] Her answer comes first, and the chore lands last; the chapter is named for the
    bin.

### Chapter 25: Long Enough to Laminate

59. Devendra: "I have a mortgage and two kids in a good school" becomes "I have a mortgage and three kids in a good
    school", to match edit 9. [Claude]

## Continuity pass, 2026-11-25

CT asked Claude to sit with all the edits and make sure the repo is fully up to date. Claude read every edit against
the whole v5 text (3,600 paragraphs), searching for every later line that points back at something an edit changes.

Found and fixed in this file:

- **Edit 7** had dropped "David gave him the look too". Restored as CT first said it.
- **Edit 14** cut a line that Chapter 15 quotes back at the food bank. See edit 56 and "Needs CT".
- **Edit 24** would have cut the enclosure exchange that Chapters 6 and 33 point back to ("the fence"). A short form
  is kept inside Elijah's question.
- **Edit 9** (three kids) contradicted Chapter 25 (two kids). Edit 59.
- **Edit 53** (the million) made two existing lines out of date, in Chapters 11 and 31. Edit 58. The Chapter 13
  memory line moved to Chapter 12, where he already has his thumb over Ruby's number.
- **Edit 30** (morning calls) put the Chapter 3 satellite in daylight (edit 61), sent Elijah "to bed" at 10:30 in
  the morning in Chapter 5 (edit 62), and left "she'd had a good day" at 9:40 a.m. in Chapter 31. The Chapter 22
  call is reworked around Ray's funeral, and the Chapter 15 line is simplified.
- **Edit 34** (he dreads the bill) contradicted "out of pure Monday inertia". Edit 62.
- **Edit 42** (four thousand replies) left "hundreds" twice in Chapter 7. Edit 60.
- **Edit 51** no longer invents a "last guy with a notebook"; it points at her own line.
- **Edit 10**: "forecaster" in lower case.
- **Edit 5**: read from CT's own sentence as "chasm". See "Needs CT".

Checked and fine as they are: the LOSER COOKS T-shirt (Ch 7), "Hey, forecaster!" (Ch 11), Marta's "can't surprise
you" (Ch 18), Lena in Chapter 9, the Architect's "I was being polite" (Ch 9), the heart from the cooling founder
(Ch 12 and 14), the visitor book (Ch 37), "Everybody says no the first time" (Ch 10), the Appendix timeline.

Not changed by any edit but worth CT's eye: the back cover says "A few weeks later, they fired their social media
team"; the book says one week, and names a transaction coordinator, a marketing person and the kid who made their
listing videos.

## Applied

- Author's Note, 2026-11-25: "They may tell you they moved on because I was an asshole, and they might be right."
  and "But I'm not wrong about our trajectory." Entered in the Doc as suggestions. Still pending in the read of
  2026-11-25 (revision AHj4eMResiURoAJEhT0nN-6E), with the rest. The publication files were built as if accepted.
- All edits 1 to 86, 2026-11-25: entered in the Doc as suggestions, through the Appendix, and read back after each
  batch. Nothing accepted yet. CT's rulings above went in as written. Checked again the same day by a separate
  session against a fresh read: every edit present. Record: `EDITS-v5-applied.md`.
- Follow-ups CT asked for on 2026-11-25, also suggestions:
  - The power bill is $2,011.46 in Chapters 5, 19 and 21 (CT: "$2011.46 in all places"; the comma matches the
    book's other amounts).
  - CT chose to keep the bill and explain it: "A rate hike cuz he went over a limit of some kind." Chapter 5, "One
    month. One month of training runs..." becomes "He had gone over some limit the utility set, and once he crossed
    it, the rate jumped. One month. One month of training runs..." [Claude's wording of CT's beat]
  - North Bay office: "in San Jose" cut from Devendra's lines in Chapters 25 and 32; the Appendix's "He stays in San
    Jose." becomes "He stays put." [Claude]
  - Chapter 13: "it took the notary to find her stamp" becomes "it had taken the notary to find her stamp", since the
    stamp now comes at the bank, before the wire. [Claude]
- Checked and left alone: Chapter 7, where Ma talks about the video as new. The book already says, right after,
  that she watched it in October and wrote to him twice; it is her memory going, before the stroke.
- Back cover (`publication/novel/build/book.json`): "A few weeks later, they fired their social media team" becomes
  "A week later, ...", to match Chapter 0 ("One week later, almost to the hour").
