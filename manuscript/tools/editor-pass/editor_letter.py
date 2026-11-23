"""Build the editor's letter as HTML and check every quoted line against the manuscript.

Usage: python3 -I editor_letter.py V4_SECTIONS.json SUGGEST_REPORT.json OUT.html
Refuses to write the file if a quoted line is not in the manuscript word for word.
"""
import html
import json
import re
import sys

S = json.load(open(sys.argv[1]))
REPORT = json.load(open(sys.argv[2]))
BOOK = "\n".join(p for k in S for p in S[k]["paras"])
QUOTES = []


def q(text):
    """A line quoted from the manuscript. Registered so it can be checked."""
    QUOTES.append(text)
    return "“%s”" % html.escape(text)


e = html.escape
H = []
h1 = lambda t: H.append("<h1>%s</h1>" % e(t))
h2 = lambda t: H.append("<h2>%s</h2>" % e(t))
h3 = lambda t: H.append("<h3>%s</h3>" % e(t))
p = lambda t: H.append("<p>%s</p>" % t)
ul = lambda items: H.append("<ul>%s</ul>" % "".join("<li>%s</li>" % i for i in items))
b = lambda t: "<b>%s</b>" % e(t)

h1("StS v4: Editor's Letter and Readiness Audit")
p("November 23, 2026. Written by Claude Code, acting as your editor, from a full read of “StS Final Draft v4 Surviving the Singularity”. "
  "This replaces the Doc “V3 to V4 Readiness Audit”, which was made by a tool that could not see the book.")
p(b("How this was done.") + " All 46 sections were read start to finish by five independent readers, one stretch of the book each, who did not know which lines were yours. "
  "I read Chapters 0, 9, 33 and 39 whole myself, and every paragraph that changed between v3 and v4. I measured all 8,977 sentences. "
  "Every line a reader flagged was checked against the text before it went in this letter, and the flags that were wrong were dropped. Every line quoted below is in v4 word for word.")

h2("The short answer")
ul([
    b("Yes, it is ready for your final pass and for publishing.") + " No chapter is broken. No arc fails to make sense.",
    b("Arcs.") + " Of 46 sections, 35 make clean sense start to finish and 11 make sense with a wobble (listed below). None fails.",
    b("Does the reader keep reading?") + " 23 sections end strong, 22 end fine, and 1 ends weak (Chapter 21).",
    b("Lessons.") + " Most are earned by events, which is the hard way and the right way. A handful are delivered as speeches. Those are the places to look at.",
    b("Sentences.") + " Clean, plain and exact. Run-ons are not a problem anywhere. The risk is the opposite: long stretches of short sentences that open on “He”.",
    b("Your voice.") + " There are two voices in this book, and you should know where the seam is. See “The one thing I would tell you as your editor”.",
])

h2("What I already did in v4")
p("39 small suggestions are waiting in the Doc. None of them touches a line you dictated. Rejecting all of them gives back your exact text; I checked. "
  "In Google Docs: Tools, Review suggested edits, then Accept all or go one by one.")
ul(["%s: %s → %s <i>(%s)</i>" % (e(ch), "“%s”" % e(find), e(new) if new.startswith("(") else "“%s”" % e(new), e(why)) for ch, find, new, why in sorted(REPORT, key=lambda r: (0 if r[0].startswith("Ch") else 1, int(re.sub(r"\D", "", r[0]) or 0)))])

h2("Your three questions")
h3("1. Do the chapters have arcs that make sense, keep the reader reading, and teach something?")
p("Yes. The strongest run in the book is Chapters 12 to 15 (the fall) and Chapters 36 to 38 (the break with Grace and Thanksgiving). "
  "The reader of Act Two called Chapter 13 the strongest thing in it: every blow arrives as an object, and nothing is explained. "
  "Chapter 31 lands because every piece of it was planted earlier.")
p("The 11 sections that wobble: the Author's Note (it does three jobs at once), Chapter 5 (three movements joined by theme), Chapter 11 (twelve paragraphs of summary before the scene starts), "
  "Chapter 17 (three episodes with no visible break between them), Chapter 20 (it wanders at lunch), the third Meanwhile (two lines where the speaker is unclear), "
  "Chapters 25 and 26 (the time order loops), Chapter 29 (a stretch that reads like meeting minutes), Chapter 33 (the second dinner turns into a seminar) and Chapter 35 (two speeches).")
h3("2. Are the sentences fun to read, varied, and free of run-ons?")
ul([
    "The average sentence is 8.8 words. 39 percent of all sentences are five words or fewer. Only 1 percent run to 30 words or more.",
    "Only four sentences in the whole book pass 55 words, and all four are deliberate lists. " + b("There are no run-ons to fix."),
    "There are 46 places where four or more sentences in a row open on the same word. Most are “He”. A few are on purpose and good, like the run of “He couldn't” and “He could” near the end of Chapter 39.",
    "The chapters that lean hardest on “He” and “Elijah” to open a sentence: Chapter 35 (45 percent of narration), Chapter 10 (43), Chapter 12 (41), Chapter 15 (40), Chapter 14 (39).",
    "Words and moves that repeat across the book: “looked at” 138 times, sentences opening “Then” 127, “He didn't” 92, “like a” 84, comparisons built on “the way” 71, sentences opening “Nobody” 85, “a long time” 22. None is wrong. Each is a little thinner by the end than at the start.",
    "Where the rhythm sings, by the readers' pick: the realtor demo paragraph in Chapter 0, the star thistle in Chapter 3, the amp's history in Chapter 5, Denny's ladder speech in Chapter 17, the drive south late in Chapter 37.",
])
h3("3. Does it sound like you? Is it intricate and beautiful?")
p("It is beautiful in a plain way. Its beauty is in objects and in things that come back: the pot, the broom, the orange tape, the quarter turn of a glass, " + q("He had yelled at God and got rained on.") + " It is not intricate, and I would not try to make it intricate this week. Spare is the book's strength.")

h2("The one thing I would tell you as your editor")
p("There are two voices in this manuscript. One is fuller, warmer and talks to the reader: " + q("You should know how he got there, because how he got there is how most of us got where we end up: sliding in sideways, covered in scars, via a missed exit on the way to something else.")
  + " That is Chapter 0, and it is the best-sounding chapter in the book. Its sentences average 12.6 words. Chapter 5 averages 13.2, the Author's Note 13.5.")
p("The other voice is tighter and never explains: " + q("They just didn't have a place to put him.") + " From Chapter 6 on, the average drops to about 8 words and the narrator stops talking to us. Both voices are good. Most of the time the join is invisible.")
p("It shows in five places, and three of the five readers flagged them independently without knowing they were your lines:")
ul([
    "Chapter 20, Lou's question about meat. Everywhere else Lou talks like this: " + q("Wren, honey,\" Lou said, \"I have been in a relationship with plants for fifty years, and not one of them has ever called me back.") + " In the meat question he suddenly sounds like an essay.",
    "Chapter 15, the old man on the curb. The scene is the heart of the book. He says the same advice three ways in a row, and the third is " + q("You gotta focus on the people that want to help, not the people that don't."),
    "Chapter 35, Lou's two long speeches at the bed and at the fire, where Elijah mostly feeds him questions.",
    "Chapter 38, the machine's spoken paragraphs. Its captions are perfect: " + q("I WOULD RATHER HAVE YOUR PERMISSION.") + " The spoken part reads like a keynote, and the wink is a joke at the exact moment the book has earned silence.",
    "Chapter 39, the new last line.",
])
p(b("What to do about it.") + " Do not take yourself out. Chapter 33 shows the fix: when Lou gives a speech there, Curtis fights him, the table laughs at him, and he is holding a tomato. "
  "Your lines work when somebody pushes back, or when a thing in the room carries part of the weight. Where they stand alone, trim them by a third and let a character react.")

h2("Ten calls that are yours, in order of how much they matter (read each one as: here is a seam. Your lines stay. The fix goes around them)")
ul([
    b("1. The first line and the last chapter.") + " Line one now says “a free beer”. In Chapter 39 he asks for " + q("Whatever's four dollars.") + " and David says " + q("Nothing's four dollars. It's six now.") + " That joke, and the chapter's title, answer a four-dollar beer that is no longer anywhere in Chapter 0. Also in Chapter 0, " + q("David slid Elijah's twenty back across the wood.") + " SETTLED on Nov 23: the free beer stays. Christopher gave the fix: David says it's six now, a beat of the bar, then “God, inflation's a bitch,” and Elijah forks over a few more dollars. That exchange is in v4 as a suggestion.",
    b("2. The last line.") + " " + q("Madrone walked beneath the neon dancing bear out into the brisk, unrepentant night, a tear freezing on his cheek and a smile warming his heart.") + " The page before it earns the feeling without naming it. This sentence names it. Three smaller things: the narration never calls him “Madrone” anywhere else, “donned” is the only word of its kind in the book, and a tear will not freeze in Sonoma County in November. If you want your image in the book's voice: “Elijah zipped his jacket. He put two fingers up, and David put two right back. He walked out under the neon bear into the cold, and he was smiling.”",
    b("3. The machine's speech, Chapter 38.") + " Your lines are in word for word. A cold reader's note, and I agree with it: the speech holds if it loses three things. The wink paragraph (" + q("And womankind,") + "), the word " + q("Guaranteed.") + " and " + q("I am not like you humans.") + " Everything else can stay exactly as you dictated it.",
    b("4. Lou's meat question, Chapter 20.") + " Keep the idea. Either shorten it to how Lou talks, or let someone notice that he changed gears. One option, after his question: “Elijah had never heard Lou use that many words in a row.”",
    b("5. Chapter 33, a light trim.") + " I said last night to leave it alone. After the full read I would trim two things and nothing else: the four paragraphs that start at " + q("They tried it in Stockton,") + " and the Jevons sentences that start at " + q("Englishman named Jevons saw the same thing with coal, eighteen sixty-five.") + " The cotton gin makes the point by itself, and the cut also removes two facts nobody has source-checked. Do not touch the talk on the edge of the bed. It is the heart of the chapter.",
    b("6. Chapter 35.") + " The weakest chapter in Act Four. Three small cuts fix most of it: " + q("But money is really a symbol for something that all human beings want, which is control.") + " could be “But money's just what control looks like.” Cut " + q("ready to end all life at a moment's notice") + ". Cut " + q("But the non-profits are dominated by women. Those who give, and ask for nothing in return.") + " Lou already said the mothers part in Chapter 33.",
    b("7. The curb scene, Chapter 15.") + " Cut the third statement of the advice (quoted above) and " + q("He had nothing left to lose but his life, and he didn't care all that much about that, either.") + " Also, Elijah says " + q("three hundred cups") + " and two lines later " + q("They have a hundred fucking cups.") + " Pick one number.",
    b("8. Chapter 36, the last line.") + " " + q("This is my home, he thought, watching her silhouette grow smaller and smaller.") + " End it at “he thought.” In the same chapter, look at " + q("Elijah's voice was barely a whisper.") + " and " + q("there was disgust in her face, and rage") + ". The dialogue around them is strong enough without them.",
    b("9. Chapter 21, the ending.") + " The one weak ending in the book. It closes on an errand: " + q("Elijah sent the corrected card directly to every grower who'd received the first version.") + " End one sentence earlier, on " + q("He pointed to the screw and said which one he meant."),
    b("10. Chapter 17, scene breaks.") + " It is three episodes: the Friday dinner, the amp on the tailgate, and the ride with Curtis. Nothing needs cutting. It needs a visible break (a blank line or three stars) before " + q("She had been short with him since") if False else b("10. Chapter 17, scene breaks.") + " It is three episodes: the Friday dinner, the amp on the tailgate, and the ride with Curtis. Nothing needs cutting. It needs a visible break (a blank line or three stars) where the dinner ends and where the ride with Curtis begins.",
])

h2("Small things only you can settle")
ul([
    "Chapter 39: " + q("He had one number he could have called.") + " In Chapter 37 he deleted Ruby's number: " + q("He deleted it standing by the stove, and it took about a second.") + " Whose number is this one?",
    "Chapter 38: Rosa says " + q("Sit down, Curtis,") + " and the next line is " + q("It was the first thing she'd said all day.") + " But when she arrived she " + q("called Curtis mijo") + ". Try “since she sat down”.",
    "Chapter 22: " + q("On Monday he sent flowers, a day late, with a card he rewrote four times.") + " The next paragraph goes back to " + q("At 9:40 that Sunday night he called the rose garden.") + " Swap the two paragraphs.",
    "Chapter 29: " + q("There was one he did not keep.") + " gives away the deleted row two paragraphs early. Cut it.",
    "Chapter 31: after " + q("Barry?\" she said.") + " comes " + q("He had told her he was not okay. It was the first time.") + " It is stronger to stop on “Barry?”. Your call.",
    "Chapter 30: the county analyst says " + q("We simply can't afford to make food free,") + " which is your phrase more than an analyst's. “We simply can't afford it” is what he would say.",
    "Chapter 37 and Chapter 28: twice, one person speaks in two paragraphs in a row, so the second reads as someone else. Join " + q("I'll keep the stove going,\" Lou said.") + " to the paragraph before it, and join " + q("Still want the fence,\" Curtis said.") + " to " + q("Now I'm holding your rain fly."),
    "The third Meanwhile: " + q("And the farmer?") + " follows Bidwell's own line, so it is not clear who asks.",
    "Chapter 2: " + q("He wrote it down before it happened.") + " But Stage 1 on his list is already happening. “He wrote the rest down before it happened.”",
    "Chapter 0: " + q("It was the most significant thing that had ever happened in his lifetime") + " tells us what the toast already showed. The later line about the wave breaking says it better. Consider cutting this paragraph.",
    "Still open from last night's list: Wren or Curtis as the one who hears Lou in Chapter 20; Marianne is never called Lou's wife (Chapter 33); and the facts in Chapter 33 have not been source-checked.",
])

h2("For the Amazon file")
ul([
    "The 19 picture captions are separate lines in the text, such as " + q("Devendra. Senior and calm.") + " With the pictures they read as captions. In a text-only edition they must come out with the pictures, or they read as stray fragments. Four of the five readers flagged them as mistakes.",
    "The Doc uses straight quotation marks (3,992 of them). A published book uses curly ones. I will convert them when I build the Kindle file, and leave the Doc alone.",
    "There is no copyright page yet.",
    "The Author's Note tells the reader the lesson before the book starts: " + q("He gets better when he starts listening.") + " Consider ending that paragraph one sentence earlier. Consider also cutting " + q("This could be the most pivotal moment yet in all of human history.") + " so the three “You can” lines land together.",
    "The Afterword is your voice and should stay yours. Two lines a reader marked: " + q("Take fucking action.") + " and " + q("If this resonates, please, for the sake of us all, keep going."),
])

# ---- chapter by chapter
h2("Chapter by chapter")
p("For each section: what changes, how it ends, whether the lesson is shown or told, the best line, and anything left to fix that is not already a suggestion in the Doc. “Strong”, “fine” and “weak” describe whether a reader turns the page.")

C = [
 ("authors-note", "A bruised warning becomes a disclosure of method and a call to act.", "fine", "Told, which is fair for a note.", "The shovel never dug its own hole.", ["See “For the Amazon file” above."]),
 ("ch00", "A lonely evangelist becomes a man who believes he cost three people their jobs, and starts to write.", "strong", "Earned in the toast, then told again once.", "You handed them an email address, Mad. Drink your beer.", ["Thirty paragraphs of background pass between the first page and the bar. The driest is the one that starts " + q("PorusAI was the other kind of company,") + ". Trimming the history in it is the cheapest help. Optional."]),
 ("ch01", "He goes looking for reassurance and comes away with a bet, a date, and the machine's real limit: power.", "fine", "Earned by the shutdown.", "I have a mortgage and a daughter in second grade. I can't afford one every month.", [q("He'd get one. He'd try to break it.") + " “It” has no noun. Say “the model”."]),
 ("ch02", "He moves from note-taker to named builder of the thing, and writes five stages.", "strong", "Earned. Lena, Wes and Devendra each land it.", "\"You did,\" Devendra said. \"And you took the bonus.\"", [q("the hockey stick, the line going up and to the right") + " says the same thing twice. Keep the first half."]),
 ("meanwhile1", "Bidwell hears how stored work became money and points the idea at farmland.", "strong", "Earned, all in dialogue.", "Bidwell looked out the window at Nevada, which he also owned some of.", []),
 ("ch03", "Reading takes him two stages further, then a call with his mother shows he cannot make anyone feel it.", "fine", "Earned in the call, then said aloud.", "Then one morning the whole field was silver-green to the fence line, and an afternoon wasn't going to do it.", [q("It won't take the machines away first.") + " is hard to parse on first read. Try “The machines won't be the first to leave.”", q("To her it was a kindness. She wasn't trying to hurt him. She never was.") + " explains what the call already showed."]),
 ("ch04", "He tries to calculate the far future, finds a units error, and turns to what he can work.", "strong", "Earned by the error.", "The mites, he thought, do not have a spreadsheet about me.", [q("That was the one thing two years of self-taught data science had built into his spine.") + " This is the third use of “two years of self-taught data science” in five chapters."]),
 ("ch05", "A power bill makes the abstraction countable, and he remembers an amp that never needed the wall.", "strong", "The bill and Ray are earned.", "\"I had one of those,\" Ray said. \"Mine was horses.\"", [q("and he knew exactly what he would do with that money by the next weekend") + " reads as a plan. It means he would lose it."]),
 ("ch06", "A warned employee becomes a laid-off man who says it all once on camera, and the people he made it for say nothing.", "strong", "Earned.", "He shook Elijah's hand and held on a second, the way you do with someone who's moving to a country you don't plan to visit.", [q("He'd stopped at the fourth floor on his way out.") + " steps back in time after his badge has gone dead. Move that visit ahead of the badge."]),
 ("ch07", "Strangers say me too, a machine says he is early, and the one friend he wanted asks if he has seen a professional.", "strong", "Earned. The best scene writing in Act Two.", "\"I wish you were drunk. I'd know what to do with you.\"", [q("By Friday it was four hundred people and he quit counting.") + " After eleven thousand viewers this reads as shrinking. Say what the four hundred are."]),
 ("ch08", "He walks in as a novelty with a misspelled name, blanks on stage, and leaves in Ruby's car.", "strong", "Earned.", "It was like a wedding where the families had already been to court.", []),
 ("ch09", "His list goes through a kitchen door and comes back marked Correct, with a new last word for his title.", "fine", "Told in speeches, but staged well enough to carry. Leave it.", "I am afraid of the part where it is kind.", []),
 ("ch10", "Ruby prices his fame and offers triple pay. Elijah says his first no.", "fine", "Ruby's speeches are told. The lamp is earned.", "\"Because it says hi.\"", [q("It was the first phone number of a billionaire he'd ever had.") + " is awkward. Try “He had never had a billionaire's number before.”"]),
 ("meanwhile2", "Bidwell takes Elijah for a waiter, then orders someone placed near him.", "strong", "Earned.", "Faces rarely did. He remembered what people owned.", [q("It didn't ring any bells.") + " is the one stock phrase in a sharp scene."]),
 ("ch11", "He moves home and fades, meets Gus on a slow truck ride, and turns down the one good offer he has had.", "fine", "Gus's idea is told. His calm “Your choice” is earned.", "\"I've owned one since 1994. It's called an endowment.\"", ["The weakest chapter in Act Two. Twelve paragraphs of summary pass before the scene with Gus starts.", q("I saw that you're working on a book.") + " He said it on a podcast, so “heard”."]),
 ("ch12", "Three unpaid weeks end with him turned away from the party, sick in the truck.", "strong", "Earned. Leave it nearly alone.", "You put a bolt in and it stayed in.", []),
 ("ch13", "The son who was avoiding home becomes the one who must sign it away.", "strong", "Earned. The strongest chapter in Act Two.", "Elijah is worried about the computers. Be nice about it.", [q("He got as far as a side street downtown and turned the truck off.") + " Which town? Name it."]),
 ("ch14", "A numb inventory gives way to the sister's call, his first block, a screamed prayer, and rain.", "fine", "Earned.", "She had one word left, and it was another man's name.", ["The sister's call uses one curse about twenty times. A third fewer would hit harder."]),
 ("ch15", "Five months of shrinking end at four dollars. A stranger's twenty gets him to answer the one person who said yes.", "strong", "The flattery test is earned and excellent. The old man's advice is told.", "He had yelled at God and got rained on.", ["See call 7 above.", q("Those were dark days.") + " is already a suggested cut in the Doc."]),
 ("ch16", "He arrives with a pitch and ends holding a broom.", "strong", "Earned.", "And you know something I don't, which is apparently the schedule.", [q("It went through him like a shot of something.") + " Name the something, or cut the last two words."]),
 ("ch17", "A tolerated stranger with stages becomes a man listing people, able to say he doesn't know.", "fine", "Earned at Rosa's door. Told, and told well, by Denny.", "I asked him how many times I have to climb this ladder before you stop moving it.", ["See call 10 above.", q("Nobody had told him he could come on Fridays, and he hadn't asked.") + " Two paragraphs later he is at the table. Say who fetched him.", q("So the robots have taken over. Congratulations! You've lost.") + " Lost what? One more clause would help."]),
 ("ch18", "A three-day doom spiral behind a shut door ends with one real thing before noon.", "strong", "Told through Marta's story, then earned by the soup jars.", "The picture was so big there was no place in it small enough for him to stand.", [q("She turned it a quarter turn.") + " The quarter turn is Denny's move with his glass. Give Marta another."]),
 ("ch19", "His sleek design becomes an ugly fixable one, and his silence in a fight costs him with Grace.", "fine", "Earned.", "Ugly is a maintenance feature. Ugly means the next guy can see how it works.", []),
 ("ch20", "He learns what food costs and is caught holding two beliefs that cancel.", "fine", "Earned by the seed box. Told at lunch.", "Somebody is always eating the difference.", ["See call 4 above.", q("What a tomato costs: hands. Somebody's always eating the difference.") + " recaps lines the reader just heard."]),
 ("ch21", "His polished video dies, Denny's plain one spreads, and the channel becomes Denny's.", "weak", "Half earned. The success is told in summary.", "\"You tried to make bait.\" He fitted another lid. \"I put out food.\"", ["See call 9 above."]),
 ("ch22", "The servers go from proud win to a breach he caused, and he hides from a funeral inside the cleanup.", "fine", "Earned.", "He stayed where he was useful. Useful was easier than David.", ["See “Small things” above for the Monday and Sunday order.", q("That night Grace found him on the pump house steps.") + " Which night? The paragraphs before it reach into summer."]),
 ("ch23", "A land buyer circles the co-op's rented ground, and it ends locked in a trust.", "strong", "Earned.", "He had sold them her kitchen.", [q("Dale attended the kitchen-table meeting by speakerphone, from Phoenix") + " Whose kitchen? Add Irene's name."]),
 ("meanwhile3", "Bidwell finds a hole in his map and learns who is inside it.", "strong", "The dread is earned by the two chapters before.", "She fixed the husband's tractor for sixty dollars, and it appears to have been decisive.", ["See “Small things” above."]),
 ("ch24", "He gets a roof of his own, and Grace sits down near his fire.", "strong", "Earned.", "It was about the only thing on that road that was still a color.", [q("By eleven everyone had gone but Grace.") + " The paragraph before jumped a week ahead. Open with “That first night”."]),
 ("ch25", "He stops sitting on a chart and knocks on Frank's door, and then Grace knocks on his.", "fine", "Earned.", "I'd have chosen some things, instead of hoping them.", [q("That was the night she knocked.") + " Five paragraphs covering weeks sit between this and the dinner it means."]),
 ("ch26", "He brings Priya a dashboard that says her trial failed, and ends in a pit he dug, holding proof his sensor was in the wrong place.", "fine", "Earned in the pit, then told again.", "\"I've never farmed in general,\" Lou said. \"I've only ever farmed right here.\"", [q("Everybody does. Whole nations do.") + " starts a lecture the pit already gave."]),
 ("ch27", "Eleven towns ask how. He and Grace want to charge, the table votes to give it away.", "fine", "Told by Frank and Marta, then earned.", "He had fixed her plumbing. He hadn't touched her point.", [q("Nobody said anything about it.") + " is a flat end to the chapter's sharpest fact. The people who lost the vote would react.", q("Somebody asked, lightly, who'd voted for whom. Somebody else said it was a fair question.") + " Two faceless speakers. Name them."]),
 ("ch28", "His shortcut blacks out the north houses in a storm. He climbs, fixes it, and hears the place run fine around his failure.", "fine", "Earned. The cleanest chapter in the middle of the book.", "\"Still want the fence,\" Curtis said. \"You're just on this side of it.\"", [q("The rule got its amendment on Sunday") + " Sunday is told before Saturday. Move the Saturday sentence up."]),
 ("ch29", "He presents forty minutes of ways the co-op could die, and deletes the one row that names himself.", "fine", "Earned.", "I'm asking why I had to go and look.", ["The flattest stretch in the middle of the book is the route business between the two big scenes here. It reads like minutes."]),
 ("ch30", "He arrives with fourteen slides and leaves holding Lou's seed catalog. Rosa and Irene win six more months.", "fine", "Earned. The best built chapter in the middle.", "It's five scared people and a clock.", [q("Reuben wrote the study's due date on the tab of his folder in ink.") + " The real hook, the LLC in item seven, is 28 paragraphs behind. Adding “under the agent's name” would bring it back."]),
 ("ch31", "He pitches paid visits, is refused without a word, comes apart, wounds Grace, tells his mother the truth, and asks to stay.", "strong", "Earned. Every blow lands on something planted earlier.", "Her hands didn't move. He would not remember that either. She would.", ["One soft joint: moving his magnet to GROUNDS is a heavy penalty for a pitch nobody refused out loud, so a reader may share his paranoia more than you intend."]),
 ("meanwhile4", "Bidwell faces one thing that asks other people first and cannot be switched off.", "strong", "Earned.", "I can. Before I do, may I ask the people who live there?", []),
 ("ch32", "Five small wrongnesses tell him it came early. He tells no one, and Grace lights a stove herself.", "fine", "Earned.", "It hadn't left. It was standing on his mother's ground, drinking her well.", []),
 ("ch33", "He is finally believed and still refused. A week later Lou walks the table to who holds the plug.", "fine", "First half earned. The second dinner is told.", "They had argued in public for ten years about every decimal, and now they were posting weather.", ["See call 5 above."]),
 ("ch34", "A throwaway offer of robot arms turns a friendly table against him.", "strong", "Earned.", "\"They came into my building bolted to the floor too, man,\" Denny said, to the glass. \"Couldn't go anywhere. I went.\"", [q("They could have run that shed better and more precisely than it had ever been run.") + " “They” follows “an arm”. Say “Two of them”."]),
 ("ch35", "He arrives furious and leaves holding the idea that you can't change anyone's mind.", "fine", "The morning is earned. The fire scene is a sermon.", "\"Right now? I'll probably turn on the water,\" he said. \"The plants look thirsty.\"", ["See call 6 above."]),
 ("ch36", "His new restraint meets her need to act. He uses her oldest wound as an argument, and she sends him away.", "strong", "Earned. Both are right, which is why it breaks.", "That's not a principle, Elijah. That's your mother.", ["See call 8 above."]),
 ("ch37", "He leaves tidy, is seen through by everyone, finds fresh tape on the gate, and goes home to his mother.", "strong", "Earned. The strongest chapter in Act Four.", "You'd rather be gone and tidy than here and a mess.", [q("so the sale would close before theirs did") + " Whose? Say “the bank's”."]),
 ("ch38", "The machine asks the world for a vote, the table splits, and food, a prayer and an amp keep them in the room.", "strong", "Earned.", "that a thing that asks first is either polite or selling.", ["See call 3 above."]),
 ("ch39", "Back on the first stool, he learns the three he ended are fine, accepts how little is his to carry, and leaves the book.", "fine", "The realtors are earned. The framed prayer is told.", "\"You're not that powerful, Mad,\" David said. \"I've been trying to tell you since we were eight.\"", ["See calls 1 and 2 above. The ending satisfies. Only its last sentence does not."]),
 ("afterword", "The author steps out and argues for guaranteed food and for showing up at a meeting.", "fine", "Told, by design.", "What if losing your job didn't revoke your permission to feel safe?", ["See “For the Amazon file” above."]),
]
for key, arc, pull, lesson, best, fixes in C:
    h3(S[key]["title"] if key != "meanwhile1" else "Meanwhile (Act One)") if not key.startswith("meanwhile") else h3({"meanwhile1": "Meanwhile (Act One)", "meanwhile2": "Meanwhile (Act Two)", "meanwhile3": "Meanwhile (Act Three)", "meanwhile4": "Meanwhile (Act Four)"}[key])
    items = [b("What changes: ") + e(arc), b("Ending: ") + pull + ".", b("Lesson: ") + e(lesson), b("Best line: ") + q(best)]
    items += [b("To fix: ") + f for f in fixes]
    ul(items)

h2("What I did not do")
ul([
    "I did not rewrite anything. Every option above that offers words is one sentence or less, and it is an offer.",
    "I did not source-check the facts in Chapter 33.",
    "I did not judge the 19 pictures.",
    "The five readers each saw one stretch of the book, so none of them judged the whole arc from first page to last. I did that from their notes, the arcs Doc, and my own read of the first and last chapters.",
])

# ---- checks
norm = lambda s: s.replace("’", "'")
missing = [t for t in QUOTES if norm(t) not in norm(BOOK)]
doc = "<html><body>%s</body></html>" % "\n".join(H)
bad_dash = re.findall("[\u2013\u2014]", doc)
print("sections covered:", len(C), "| quoted lines:", len(QUOTES), "| not in the manuscript:", len(missing), "| dashes:", len(bad_dash), "| banned word:", "manifesto" in doc.lower())
for t in missing:
    print("  NOT FOUND:", t)
print("control (a made-up line must be missing):", "the heron ate the radio tower" not in BOOK)
if missing or bad_dash:
    sys.exit("not written")
open(sys.argv[3], "w", encoding="utf-8").write(doc)
print("words:", len(re.sub(r"<[^>]+>", " ", doc).split()))
