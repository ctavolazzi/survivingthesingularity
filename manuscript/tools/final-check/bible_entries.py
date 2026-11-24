#!/usr/bin/env python3
"""Builds the new Character Bible entries. Every quotation is checked against the v5 text and
its chapter is looked up from the text, not typed by hand. Fails loudly on any quote not found."""
import re, sys, json

V5 = open(sys.argv[1], encoding="utf-8").read()
LINES = V5.split("\n")
sec, lab, seen, last_ch = [], "front", 0, None
for l in LINES:
    if l == "Author's Note":
        seen += 1
    if seen >= 2:
        m = re.match(r"^Chapter (\d+):", l)
        if m:
            lab = "Ch %s" % m.group(1); last_ch = m.group(1)
        elif l == "Meanwhile":
            lab = "the Meanwhile after Ch %s" % last_ch
        elif l in ("Epilogue", "About This Book", "Afterword", "Appendix"):
            lab = l if l != "Epilogue" else "the Epilogue"
    sec.append(lab)
BAD = []
def where(s):
    hits = []
    for i, l in enumerate(LINES):
        if s in l and sec[i] != "front" and sec[i] not in hits:
            hits.append(sec[i])
    return hits
def q(s, show=True, pick=0, also=False):
    h = where(s)
    if not h:
        BAD.append(s); return '"%s" (??)' % s
    if not show:
        return '"%s"' % s
    if also and len(h) > 1:
        return '"%s" (%s)' % (s, ", ".join(h))
    return '"%s" (%s)' % (s, h[pick])
def q2(a, b):
    h = where(a)
    if not h or not where(b):
        BAD.append(a + " / " + b); return "??"
    return '"%s" "%s" (%s)' % (a, b, h[0])
def c(s, pick=0):
    h = where(s)
    if not h:
        BAD.append("PROBE: " + s); return "??"
    return h[pick]

E = []   # (name, motivation[], backstory[], voice[], flags[])

E.append(("Denny Osei", [
    "Surface want: an answer that doesn't end with him starting over. " + q("I need an answer that doesn't end with me starting over hungry."),
    "Real want (proposed): to stop being scared, and to be the one who tells it instead of the one it happens to. " + q("I wanted not to be scared on a Tuesday.") + " " + q("I spent years as the answer to that question, and it nearly killed me."),
], [
    q("a big easy man who talked with his hands") + ". Eleven years in a warehouse until the arms came in in 2019. He retrained at night into logistics software and got hired into dispatch (" + q("Wore a lanyard.", show=False) + "). In 2023 the routing went autonomous (%s)." % c("2023, the routing went autonomous"),
    "He has a daughter (%s) and a wife, Yvonne, who %s." % (c("My daughter told her class"), q("lifts grown men out of bed at three in the morning")),
    "He is fifty-one when he tells his story to the camera in one take (%s). After that the channel is his: the voice, the face and the say-so. He can say no to the camera any day he wants." % c("at fifty-one, to bolt together a machine"),
    "He delivers the forty controllers in apple boxes (%s) and runs the plasma torch on the day of the cut (%s)." % (c("Denny delivered them in apple boxes"), c("Denny ran the plasma torch")),
    "His name goes under burnout at the annual meeting (%s). He refuses to post Elijah's evidence: %s." % (c("Burnout, said Priya, looking at Denny"), q("That's not food yet. That's a poem about tide pools.")),
    "The arms took his warehouse. At the arms meeting he turns his glass and says one thing: " + q("They came into my building bolted to the floor too, man") + ".",
    "Endings: he hugs Elijah goodbye, " + q("You know where the porch is") + ". At Thanksgiving he props his phone against the gravy boat and goes live with no hook (%s). David has watched him every week since the warehouse video (%s)." % (c("thumbed it live"), c("I watch that guy")),
], [
    "Length: medium, built like a bit. A setup, a count on his fingers, then the line that lands.",
    "Vocabulary: \"man,\" warehouse and dispatch words (the lanyard, the routing, the county's folder), and food for what is true: " + q2("You tried to make bait.", "I put out food."),
    "Tics: he turns his water glass a quarter turn when he is deciding what not to say. He talks with his hands. His check-in word is \"Gassy.\" He signs off " + q("Come see it. Bring your kid.", show=False),
    "He swears once in the whole book, at the tomato dinner (%s)." % c("grow our fucking food"),
    "Would never say (proposed): a hook, or anything scripted. " + q("Nobody talks like this"),
    "Real lines from v5:",
    q("I asked him how many times I have to climb this ladder before you stop moving it."),
    q("So the robots have taken over. Congratulations! You've lost."),
    q("I'm not talking to the algorithm. I'm talking to a guy on his couch who just got the letter I got in 2019."),
], [
    "The repository notes (Nov 19 copy) quote \"Bait's a picture of food.\" It isn't in v5.",
    "\"My wife Yvonne\" (Ch 33) is the only place she is named. His call: Yvonne is Denny's wife.",
]))

E.append(("Curtis Cudworth", [
    "Surface want: a fence and a full basement. " + q("That's who you plan for. That's who you fence out."),
    "Real want (proposed): to know who holds the plug, and to be inside something worth guarding. " + q("I just want to know who's holding the plug.") + " " + q2("Still want the fence,", "You're just on this side of it."),
], [
    "A man with a gray ponytail who joined the co-op the fall before Elijah came (%s). He is good with engines and owns %s. He reads the forums most of the night." % (c("The man with the gray ponytail was Curtis Cudworth"), q("the valley's best-stocked basement", show=False)),
    "He wrote repair quotes for twenty-one years: " + q("I wrote twelve hundred anyway, because the laptop's the one that signs."),
    "He drives the route. He takes Elijah on it and tells Rosa %s." % q("Doesn't change your dinner"),
    "He finds Elijah's check-engine fault in nine minutes with a fourteen-dollar reader and two dollars of hose (%s). Elijah keeps the hose in the glove box." % c("Curtis found it in nine minutes"),
    "He holds a garbage bag over Elijah on the ridge in the storm: " + q("Now I'm holding your rain fly."),
    "He votes with Grace and Elijah to sell the files, %s." % q("which was not company either of them had expected"),
    "He cooks six eggs on the stove the morning after the tea and leaves without an opinion (%s)." % c("He cooked six eggs on top of the stove"),
    "The dealer locks the co-op's tractor behind a laptop. He gets Walt's old one running with a matchbook cover and writes DECEMBER on the locked one (%s)." % c("he wrote DECEMBER"),
    "Endings: he tops up the oil in Elijah's truck, " + q("Nobody had asked him to.", pick=-1) + " At Thanksgiving he is on his feet with the Naturalists (%s), sits when Rosa tells him to, and knows the Lord's Prayer cold." % q("It's in the walls. He put it in the walls.", show=False),
], [
    "Length: short verdicts, delivered like box scores, then a joke.",
    "Vocabulary: movies as scripture (Judgment Day, Skynet, the Terminator, The Matrix), numbers from the forums, shop words.",
    "Tics: \"bud\" to Elijah (Ch 17). \"Yes, ma'am\" to Grace. He lifts two fingers off the wheel. He apologizes for his jokes to every woman at the table, by name.",
    "Would never say (proposed): that he is glad Elijah came. He holds the rain fly instead.",
    "Real lines from v5:",
    q2("Judgment Day,", "They made a whole movie about it in 1991, so nobody could say they weren't warned."),
    q("First true thing you've said all day."),
    q("A rule's just greed somebody wrote down."),
], [
    "His surname, Cudworth, is on the page once (Ch 17) and in the Appendix.",
    "Both he and Frank call Elijah \"bud.\" That is as the page has it.",
]))

E.append(("Priya Ratna", [
    "Surface want: the number has to be true before anybody says it. " + q("What would you measure?"),
    "Real want (proposed): that the people who eat the food are never the experiment. " + q("The people eating this can't be the experiment."),
], [
    q("a small woman with a pencil behind her ear") + ". She ran for county commissioner on soil testing and water law, lost by about two hundred votes, and called it practice for Congress.",
    "She worked in extension offices: " + q("every budget I ever sat through funded the crust anyway") + ". She once made a county commissioner cry during public comment (%s)." % c("who had once made a county commissioner cry"),
    "She builds the trial beds on the worst ground on the place and fences off the end where a tractor bled hydraulic fluid (%s)." % c("The book we're writing needs the parking lot."),
    "She hands Elijah the shovel when his dashboard can't find her effect: " + q("Your sensor lives at one centimeter") + ". The pit on the first of every month is her rule.",
    "She measures the well with a steel tape and carpenter's chalk and makes Tyler wait more than an hour for the water to come back (%s)." % c("The plan is chalk."),
    "She lives in a trailer on the vineyard edge. Her bed is covered in stuffed animals. " + q("You didn't see anything."),
    "After the leak: " + q("We owe ourselves a setup that doesn't depend on you never having a bad Friday."),
    "She checks what an outsider can see before the names column goes out (%s), and at Thanksgiving she is the one who hears it in the machine's speech: %s." % (c("In the morning Priya checked what an outsider could see"), q("That's ours. That's the names column.")),
    "Endings: she hands him a paper sample bag and a new pencil, " + q("Dig one at home. Tell me what you find at thirty.") + " In the Epilogue she mails a bag back with one word on it: Worm.",
], [
    "Length: short and exact. One fact, then the limit of the fact.",
    "Vocabulary: depths, dates, sample bags, \"in pencil.\" She says what a result is not: " + q("It's not a recipe.", show=False),
    "Tics: she takes the pencil from behind her ear and writes it down. " + q("Let's sit with it.") + " She notices first: the lights over the pump house in Ch 18 were hers.",
    "Would never say (proposed): \"proof.\"",
    "Real lines from v5:",
    q2("Nobody asks Reuben,", "Reuben notices."),
    q("That's a pattern. I'd write it down. I wouldn't publish it."),
    q("North houses just came back. Hello, ridge."),
], [
    "The repository notes quote \"We owe ourselves a design that doesn't depend on you never having a bad Friday.\" In v5 the word is \"setup\" (Ch 22).",
]))

E.append(("Reuben Vance", [
    "Surface want: everything in writing and filed before anybody asks. " + q("You thought a noun was a permit. Happens all the time."),
    "Real want (proposed): to run the old machine backward, once, for somebody. " + q("My grandfather lost sixty acres to a signature he couldn't read.") + " " + q("I have been waiting my entire adult life for this exact fight."),
], [
    q("A lean man in a good coat") + ". Marta introduces him as " + q("The part of the machine that runs on paper.", show=False),
    "He files the seller registration and the county letter for the controllers before anyone thinks to (%s)." % c("So I made a list."),
    "He builds the community land trust that keeps Irene in her house and keeps the ground from ever being sold to Bidwell's companies (%s)." % c("What he dealt out was a community land trust"),
    "He and Grace write to every family on the leaked list, by hand, for two days: " + q("We're not waiting for somebody to prove we owe them the truth,"),
    "He cuts Elijah's half-pay checks every month (%s)." % c("Reuben cut the first check that Friday"),
    "He has held the Sonoma deed with Elijah's name on it for a year and a half and told no one: " + q("I'm asking why I had to go and look."),
    "He files the route proposal with the county clerk on his own, " + q("Nobody had asked him to.", pick=1) + " He brings in the Alderson letter (%s)." % c("The Aldersons, out past the grange"),
    "Endings: at Thanksgiving he reads what the machine wants (%s) and says \"debts\" in the prayer." % q("It wants to run,", show=False),
], [
    "Length: complete, dry sentences. He says the legal thing first and the human thing second.",
    "Vocabulary: folders, tabs, filings, dates, \"in ink.\" History as precedent (enclosure, the fifteen hundreds).",
    "Tics: he talks to his folder. He deals folders like cards. He closes the folder on his finger when a motion is going badly.",
    "Would never say (proposed): a guess.",
    "Real lines from v5:",
    q2("It's not a data problem,", "It's a people problem."),
    q("I don't carry tales. But it's a public record, and you taught half this valley how to search one."),
    q("We'll table it,") + " and then \"Item four. Toilets.\"",
], [
    "The repository notes quote \"It's a people problem wearing a paperwork costume\" and \"Eleven was always a fantasy.\" Neither is in v5.",
    "The page never says what he did for a living. It says only that he has been reading buyers' letters for six years (Ch 32).",
]))

E.append(("Frank Kowalski", [
    "Surface want: to be the man who knows which part. " + q("You can't download me."),
    "Real want (proposed): to be told in time. " + q("I'd have chosen some things, instead of hoping them."),
], [
    "He ran Kowalski's Hardware, the third bay off the square, under a bell his grandfather hung (%s). " % c("a bell over the door that Frank's grandfather had hung") + q("I spent thirty years selling parts for two dollars over what the internet charged,"),
    "His distributor is bought by a logistics platform out of Memphis. Elijah watches the store die in the purchasing ledger for nine months and says nothing. The closing notice is laminated (%s)." % c("Which meant Frank had known long enough to laminate it."),
    "He has to let Tyler go in the fastener aisle. The co-op buys his inventory at honest wholesale and gives him a paid job running the tool library, and he hangs the bell over its door (%s)." % c("Then Frank hung his grandfather's bell over the tool library door."),
    "He reflows Tyler's cold solder joints on the cyberdeck: " + q2("When I was a kid we put a man on the moon,", "This is better. Don't tell him I said so."),
    "He is the one who talks the table into shipping the files free (%s)." % c("It was Frank Kowalski who took it apart"),
    "In March the price of three-eighths lag bolts goes up before he has told anyone he is out (%s)." % c("I ran out of three-eighths lag bolts Thursday night."),
    "Endings: when Elijah leaves he rings the bell once, with his finger, and doesn't come out. At Thanksgiving he wears a tie and says the prayer half a beat early, " + q("in his inventory voice, for the kid to follow") + ".",
], [
    "Length: short, flat, counted out like stock.",
    "Vocabulary: part numbers, torque specs, \"fella.\" One book reference, said plainly: " + q("Fella in Hemingway gets asked how he went bankrupt,"),
    "Tics: \"bud\" to Elijah, \"son\" to Tyler, \"honey\" to Grace. He folds his glasses into his apron pocket. Deadpan corrections: " + q("That's a thermometer, Curtis,") + " " + q("A machine made the box, Wren,"),
    "Would never say (proposed): that he misses the store.",
    "Real lines from v5:",
    q("Wouldn't have saved the store, bud. The store was dead the day Memphis bought my distributor."),
    q2("The tool library's free,", "Nobody's walked off with a Sawzall yet."),
    q("That wasn't yours to tell, son,"),
], [
    "The repository notes quote \"When I was his age we put a man on the moon.\" v5 has \"When I was a kid\" (Ch 25).",
    "\"Four generations of forearms\" on the counter and \"thirty years\" behind it are both on the page (Ch 25, Ch 27). They agree.",
]))

E.append(("Tyler", [
    "Surface want: build it now, with whatever works. " + q("Let's automate stuff. We're eighteen people short. What are we even talking about?"),
    "Real want (proposed): to be taken seriously as someone who can build, and for the future to hurry up and be good. " + q("I'd rather it was here."),
], [
    "Nineteen, working the register at Kowalski's, with " + q("a mustache he was still negotiating with") + " and a 3D printer in his bedroom. He is the Tyler who found Elijah's email for Grace.",
    "He prints forty cases the color of a school bus and shows up with the controller firmware done, two weeks ahead of Elijah's plan: " + q("I used Rod Code."),
    "Frank has to let him go. He builds a cyberdeck in an ammo can that runs on nine watts (%s) and calls the gantry solarpunk (%s)." % (c("It's a cyberdeck."), c("It's solarpunk,")),
    "When the big models go dark for eighteen days he finds he can't read his own code: " + q("I read it like you read the terms on an app.") + " He and Elijah read it line by line for ten days.",
    "He runs Patricia's grant reports through the Crucible and never says a word about what he has worked out (%s)." % c("He never said a word about what he'd figured out."),
    "He measures the well with Priya and comes back the second Saturday of every month (%s)." % c("He came back the second Saturday in December"),
    "At twenty-one he starts the four-year welding apprenticeship. He learns what wet rod looks like by finding the unplugged oven himself (%s)." % c("They've been wet for two weeks."),
    "He builds an arm to trim Walt's juniper. It cuts a branch that will not grow back. He tapes a card inside it: IF THERE'S NO GREEN PAST THE CUT, DON'T. (%s)" % c("Tyler put the color check in the code."),
    "Endings: he hauls the pipe on Elijah's last coupon and walks him to the truck, " + q("You were right, you know,") + " At Thanksgiving he says %s, and he gives away Patricia's secret." % q("Finally,", pick=-1),
], [
    "Length: fast and run-on, then one blunt question.",
    "Vocabulary: \"like,\" \"literally,\" \"I mean,\" \"okay but.\" The names of tools and boards.",
    "Tics: his voice cracks when he is attacked and he keeps going. He goes red to the ears. He already has his phone out.",
    "Would never say (proposed): that he is scared of it.",
    "Real lines from v5:",
    q("It's a tool. It's just a tool. You drove here in a computer."),
    q("The future, but there's gardens. And the robots are nice. And nobody's a dick about it."),
    q2("Okay but seriously,", "If it's real. If it asked. What do we even have it do?"),
], [
    "He has no surname on the page or in the Appendix.",
    "The repository notes have him \"nineteen years old, three months into the roster\" at the annual meeting. v5 has \"twenty-one years old, two years on the roster\" (Ch 29).",
    "The notes quote \"You were right, you know. About all of it.\" v5 has only \"You were right, you know\" (Ch 37).",
]))

E.append(("Patricia Ashby", [
    "Surface want: to protect the network's pledge and the forty growers who signed it. " + q("I don't get to unsign it for one farm because it's short."),
    "Real want (proposed): not to be found out, and not to want the thing she refuses. " + q("If I look at it, I'll want it.") + " " + q("I've been so ashamed."),
], [
    "Policy director for the CSA network two valleys over, in her forties, in a fleece vest, in a small electric car (%s). The network buys more than half of what Lou grows." % c("Her name was Patricia Ashby."),
    "She keeps her phone face down beside her, always.",
    "She sat through the hearing for a data center two counties down that asked for more water than her whole network uses (%s). Her network sends every vendor a pledge: no generated code, no generated text, a green leaf on the label (%s)." % (c("I sat through the hearing."), c("a little green leaf you could put on your label")),
    "During the eighteen days her grant reports stop coming. She calls Grace on day nine and does not say why (%s)." % c("Patricia called Grace on day nine."),
    "She asks who paid for Elijah's year in the city (%s)." % c("Who paid for yours?"),
    "She will not look at the price list for the arms (%s)." % c("with her hand flat on her binder"),
    "Endings: at Thanksgiving she comes with a pie, says she can't put the network's name next to the machine, and then tells the table she has used it every day for three years (%s). She cries. Nobody leaves." % c("I've used it every day for three years,"),
], [
    "Length: short, careful, final. She says a number like one she has checked twice.",
    "Vocabulary: the pledge, the leaf, the network, growers and buyers. \"I'm sorry\" attached to a no.",
    "Tics: the phone face down. The hand flat on the binder. She asks who and what before how.",
    "Would never say (proposed): how she actually gets her reports done. Until she does.",
    "Real lines from v5:",
    q2("You did it for free,", "So did everybody it learned from."),
    q2("A source,", "A document. A signature. Something."),
    q2("It isn't just a tool, Tyler,", "That's why I'm ashamed. I used it and I still think it's wrong. Both of those."),
], [
    "The repository notes quote four lines that are not in v5: \"You used AI to make this?\" (with a pause after \"You\"), \"Um, maybe because AI is killing the planet?\", \"There are studies. I can send you the studies.\" and \"I was special for knowing how to do this, and now I'm not.\"",
    "\"Hand flat\" is hers only on the binder (Ch 34). At the tomato dinner it is now \"her palm pressed to the table\" (Ch 33).",
]))

E.append(("Irene Calder, with Walt and Dale", [
    "Surface want: to stay in her house and deal with people who were straight with Walt. " + q("I want my questions written down before anybody signs."),
    "Real want (proposed): for what Walt left to keep being used. The stove " + q("ought to be keeping somebody warm") + ".",
], [
    "Walt Calder's widow. She owns the forty acres under the co-op. The lease has been month to month since Walt died, and she has never raised the rent (%s)." % c("Irene liked Marta and had never raised the rent"),
    "Three letters come from Sacramento, the last with a young man and twenty-three percent over. Her son Dale, in Phoenix, wants her to take it: " + q("That money is who's there."),
    "What settles it is a question to Marta about Walt's tractor: " + q("What did you charge him?") + " Sixty dollars. The land goes into the trust and she stays in her house (%s)." % c("stamped them at 11:04 on a Tuesday morning"),
    "Grace sits on her porch for four hours and they make the list on the back of a pie box (%s)." % c("a list on the back of the pie box"),
    "Walt ran hay, parked a combine where the shouse now stands, and kept a juniper in a blue pot for fifty years. Irene says he would have named the gantry. His stove heats the shouse. His tractor brings in the squash when the new one is locked.",
    "At the county she tells how the farmers on her road strung their own wire in 1939: " + q("They paid it back. Every cent."),
    "Endings: at Thanksgiving she sits at the head of the table, " + q("where she'd been put") + ", and starts the Lord's Prayer because Walt always did.",
], [
    "Length: short. She enters a fact like evidence and stops.",
    "Vocabulary: Walt, the road, the wire, \"honey.\" Dates said as years.",
    "Tics: both hands around her cup. She does up her top button before she corrects someone. She turns her porch light on and off twice when the old tractor catches.",
    "Would never say (proposed): that she is lonely.",
    "Real lines from v5:",
    q("I'd like him to say who it can't be afforded by."),
    q("It's a choice. Somebody wrote it and somebody can write a different one. Go to the next meeting, Curtis."),
    q("that a thing that asks first is either polite or selling"),
], [
    "Dale is only ever a voice on a speakerphone (Ch 23).",
    "The repository notes have Walt watering weeds \"right along with the corn.\" v5 has \"right along with the hay\" (Ch 26).",
]))

E.append(("Rosa Olivera Martinez", [
    "Surface want: to be able to plan a week. " + q("You can't plan a week around maybe."),
    "Real want (proposed): to owe nobody, and to be told the truth before it happens. " + q("And can you tell us before the week it stops?"),
], [
    "She packed fruit at a warehouse until a wrist injury. She lives in a converted garage behind a blue house and wears a brace (%s)." % c("a converted garage behind a blue house"),
    "The kitchen sends her ingredients when she asked for something she could heat. Curtis and Grace own the mistake (%s)." % c("I asked if they had anything I could heat."),
    "They put sorting cameras on her line while she was out: " + q("I've had enough changing.", pick=0),
    "She gives Curtis and Elijah a concha each and calls them both mijo.",
    "She sends a note to the annual meeting (%s) and speaks at the county in her warehouse shirt, with a minute left on the clock (%s)." % (c("Rosa had sent a note through the kitchen"), c("She sat down with a minute left on the clock.")),
    "Endings: Thanksgiving is her first dinner at the co-op. She brings tamales she has been up since four making. She has not touched her phone. " + q("Sit down, Curtis,") + " " + q("Pass the lamb,"),
], [
    "Length: the shortest of anyone. A fact about her week, then what she needs.",
    "Vocabulary: shifts, the line, the date on the letter. \"Mijo.\"",
    "Tics: she asks if you are hungry before you can ask her anything. She reads a thing back and changes one word.",
    "Would never say (proposed): thank you as a way of asking for less.",
    "Real lines from v5:",
    q("I'm not here to say thank you, though I am thankful."),
    q("I can't do work days. Not now."),
    q("You told me it doesn't change my dinner. Was that true or wasn't it?"),
], [
    "Her surname is only in the Appendix.",
]))

E.append(("Wren", [
    "Surface want: for some things to stay done by people, and for everybody to get a vote. " + q("I just think some things are meant to be done by people."),
    "Real want (proposed): never again to have something taken from her without being asked. " + q("Nobody had asked her."),
], [
    "Twenty-four when Elijah meets her (born in 2001, per the Appendix), and the best artist he has ever met. A company fed everything she had posted into an image machine. She took her pages down and came north the winter before he did. Now she paints only on things that can't be scraped (%s)." % c("now she only painted on things that couldn't be scraped"),
    "She leads the Sunday circle, makes the candles, and has painted every wall of the seed house.",
    "She says out loud the thing that is on the seventh line of Elijah's first notebook: " + q("Wouldn't it make more sense for it to just leave?"),
    "She runs the tea circle where Elijah comes apart, and owns it afterward: " + q("You were saying yes the way people say it when they mean please,"),
    "She stops Tyler from testing his arm on Walt's juniper a second time and later shows him how to make the dead branch into jin (%s)." % c("It's called jin."),
    "At the arms meeting she cries: " + q("We're people, Elijah. You look at us and you see something that needs fixing."),
    "Endings: she tells him to his face she is relieved he is going (%s). At Thanksgiving she moves her chair away from Patricia and then holds hands through a prayer she does not say." % c("I'm sorry I'm relieved."),
], [
    "Length: gentle and sideways, to the tomatoes or the water, and then the hard part.",
    "Vocabulary: circle language (" + q("I'm just noticing there's a lot of urgency in the room,", show=False) + " \"I hear that\"), reverence, relationship. Also the plain science of what a juniper will and won't do.",
    "Tics: a hand on her own chest. " + q("I would like it written down,") + " She says it twice in the book.",
    "Would never say (proposed): that she is against the machine. " + q2("I'm not against the machine,", "Everybody thinks I am."),
    "Real lines from v5:",
    q("You can't automate reverence."),
    q2("That's what scares me,", "Not the machine. Nobody getting a vote."),
    q("Now it's asking for mine, and I don't know why I'm not glad."),
], [
    "She has no surname on the page or in the Appendix.",
    "The repository notes quote \"I'm noticing some scarcity\" and \"I never dropped a pass.\" Neither is in v5.",
    "The green whiteboard note about extractive framing is unsigned (Ch 31). The page never says who wrote it.",
]))

E.append(("Devendra", [
    "Surface want: for it to be a long, slow curve. " + q("You'll calibrate. Everybody's first month feels like the apocalypse."),
    "Real want (proposed): to keep his house and his kids' school, and to do one decent thing from inside. " + q("I told myself it was the only decent thing I could do from where I sat."),
], [
    "Elijah's senior colleague at Claypot, found at the good coffee machine on the fourth floor. A mortgage and two kids in grade school.",
    "He takes the bet and writes it on a sticky note: E.M. Thanksgiving 2027. Loser cooks. " + q("I like lamb,"),
    "He reads three pages of the notebook and says \"interesting\" (%s)." % c("Devendra had read three and said"),
    "After Claypot he is moved to the land side, where a model scores farm parcels for buyers. Then his whole team goes in one memo, " + q("except him") + ".",
    "He stays in his house in San Jose and keeps the job. Elijah calls him on Sundays, after his mother.",
    "In March his three friends in the labs all go quiet the same week. One answers with a single period (%s)." % c("Somebody told him to hush,"),
    "The day Elijah leaves the co-op, he tells him the three letters were his doing. He saw Ma's parcel eighteen days before the notice was found, knew the name, and pushed the offer through ahead of the bank's sale (%s)." % c("The three letters. That was us."),
    "Endings: he calls the bet lost and cooks on Thanksgiving in his own kitchen (%s)." % c("A guy named Devendra. He's doing it right now."),
], [
    "Length: complete, even sentences. Later he starts a sentence, pauses, and starts somewhere else.",
    "Vocabulary: the field's own words used to calm (augmentation, restructure, a moat, n). \"Elijah,\" by name.",
    "Tics: he does something small with his cup before he answers. His voice goes very even when he has practiced.",
    "Would never say (proposed): that he was frightened.",
    "Real lines from v5:",
    q2("Three jobs in one bar is an anecdote,", "You build models for a living. What's your n?"),
    q("They kept the very good autocomplete. And me, to watch it."),
    q("Being right didn't pay your rent either,"),
], [
    "He has no surname on the page.",
    "The repository notes have him drive north in \"a sensible car with two car seats in the back\" and cook at the co-op's Thanksgiving. In v5 he never comes north, and Lou cooks at the co-op.",
]))

E.append(("Ruby Roth-Jones", [
    "Surface want: to collect people who are real. " + q("I just like having people like you around. I collect them."),
    "Real want (proposed): somebody to wait up. " + q("They want somebody to wait up."),
], [
    "Twenty-four, a blue check, " + q("a name he knew the way you know the name of a soda") + ". He founded Porchlight, the lamp that tells you it missed you. Four million sold, twenty-nine dollars a month.",
    "The money is older than he is: his great-grandfather froze peas. Gus knew his grandmother Evelyn, who ran the company for forty years in a hairnet.",
    "He writes in lower case: " + q("saw your thing. come down. i'll get you in the room"),
    "Elijah finds him on a milk crate by a dumpster, in a hoodie, with mustard on his sleeve and his fingernails bitten down. He has read every one of Elijah's replies.",
    "He carries Elijah's notebook through the kitchen door to the Architect (%s)." % c("I carry it in. That's the deal."),
    "On the fire escape he explains the room, " + q("It's eleven people who are scared of each other,") + " and offers triple Elijah's salary for nothing. Elijah says \"I'm okay.\"",
    "Unit one of the lamp sits on his own nightstand, turned to the wall when people come over: " + q("Because it says hi."),
    "Endings: he types his number into Elijah's phone himself. Elijah never calls it, renames it \"Don't\" in Ch 37, and still has it in Ch 39. A Porchlight ends up on Ma's windowsill.",
], [
    "Length: quick and light, " + q("like someone who'd never had to wait for a turn") + ".",
    "Vocabulary: prices, units, attention as a currency. \"Madrone.\" \"Man.\"",
    "Tics: he is in motion all the time (the thumb, the knee, the cigarette he doesn't smoke). He laughs like a bark. He goes still once.",
    "Would never say (proposed): that the lamp works on him.",
    "Real lines from v5:",
    q("Everybody you met today is going to love you until it's cheaper not to."),
    q("People don't want the truth, Madrone. They don't want your list."),
    q("Everybody says no the first time."),
], [
    "The repository notes quote \"It's the nicest thing I've ever seen anybody do and you have to stop.\" v5 has \"You have to stop that\" (Ch 8).",
    "The notes say only Elijah's mother asked about \"the stove\" in the video. In v5 it is the amp (Ch 8).",
]))

E.append(("The Architect, Nadzieja Czekaj", [
    "Surface want: a machine that asks first. " + q("A machine that capable does not need your permission. I am trying to make one that wants it."),
    "Real want (proposed): for what comes after to remember us. " + q("I would like it to remember you. I spend some of my time on that."),
], [
    "A small woman near seventy (the Appendix gives the age). She drew half the diagrams in Elijah's field, co-founded PorusAI, and stopped giving lectures. Almost nobody uses her name.",
    "Elijah knows her from a twelve-year-old lecture video: " + q2("I am often asked if I am afraid of it,", "I am not. I am afraid of us."),
    "He sees her once, in profile, in a crowd in San Francisco (%s). He hears her once, through a papered-over kitchen door, while she does the caterers' dishes (%s)." % (c("That's where she is."), c("She's doing the dishes,")),
    "She reads his list out flat, marks one line \"Correct,\" and corrects one: " + q("Seven is not correct. Seven is what he hopes. It does not leave. It stays where the power is."),
    "On his question about whether anybody asked: " + q("We said there was no one to ask. That was convenient."),
    "Gus gave her lab money when nobody would (%s)." % c("I gave her lab some money."),
    "After two years of silence she posts two words on the ninth of July, 2027: It asked.",
    "Endings: the machine thanks her by name on Thanksgiving, as the one who taught it to ask first (Ch 38, Ch 39). She is never seen again.",
], [
    "Length: short, flat statements with a silence after each.",
    "Vocabulary: plain words for the largest things. She defines her terms and corrects verbs.",
    "Tics: she never uses a contraction, anywhere. She does not do tables or faces. She does dishes. She answers \"how long\" by finishing the dishes.",
    "Would never say (proposed): a date.",
    "Real lines from v5:",
    q("That is the wrong verb."),
    q("I am afraid of the part where it is kind."),
    q("It has never once helped."),
], [
    "His call: the Architect is Nadzieja Czekaj. The name is in Ch 3, Ch 38, Ch 39 and the Appendix.",
    "The repository notes quote \"Do not apologize for the one good question.\" v5 has \"Tell him not to apologize. Ask it of the next one\" (Ch 9).",
    "In the notes Elijah hands her the notebook and sees her hands. In v5 Ruby carries it in and Elijah never sees her face straight on.",
]))

E.append(("Gus", [
    "Surface want: to give the money away faster than it grows. " + q("I've been trying to get rid of it for thirty years and I can't."),
    "Real want (proposed): somebody in the other seat. " + q("I'm tired of driving it alone."),
], [
    "Sixty-something, a short white beard, grease in the knuckles. He drove Sunday Driver on Iron Derby for nine seasons, the robot with no weapon. Elijah watched it with his father.",
    "The money was an accident: a little box that told a motor how fast to spin. " + q("I've owned one since 1994. It's called an endowment."),
    "He buys robot arms out of plants that shut down, because he can't watch them scrapped. He runs a museum in an old Elks lodge and four art buses, one with a kiln.",
    "He knew Ruby's grandmother and gave the Architect's lab money.",
    "He offers Elijah a show and a seat on the bus. Elijah says no, and Gus is the same man a mile later: " + q2("Your choice,", "I can't force you to do it."),
    "He writes his number on a gas receipt and asks to be told when the book comes out (%s)." % c("Let me know when it comes out."),
    "Endings: sick in the cannery lot, Elijah does not call him. He is the \"guy I know\" behind the arms proposal (Ch 34). Elijah mails him the second copy of the book, care of the bus with the kiln (Ch 39).",
], [
    "Length: long and easy. Every story is told against himself.",
    "Vocabulary: \"man,\" \"folks,\" straps, buses, shop talk. Money described as a machine.",
    "Tics: he checks every strap twice, and again at every stop. He drives five under. He grins at the road.",
    "Would never say (proposed): that he is generous.",
    "Real lines from v5:",
    q("It's always a strap, man. It's never the two million dollars."),
    q("The ones for nothing are the expensive ones."),
    q("That's the nicest thing anybody's said to me since the divorce."),
], [
    "He has no surname on the page.",
    "The repository notes quote \"Love that for you.\" It isn't in v5.",
]))

E.append(("Aaron Bidwell and his reader", [
    "Surface want: to own it. " + q("What do I own?"),
    "Real want (proposed): for somebody to own everything, so that nothing is ever simply loose. " + q("The day nobody owns this, God help all of you."),
], [
    "He holds the controlling piece of Claypot, eleven companies with one registered agent and a mail-forwarding address in Sacramento, the Memphis platform that buys Frank's distributor, and fifty-three parcels, among them the Hollis place and Ma's farm.",
    "He does not read. A reader sits across from him with one-page summaries and one rule: " + q("Start with what he owns."),
    "The idea comes on a plane, the day Claypot announces Companion: " + q("Find out what the dirt costs,"),
    "He is at the San Francisco dinner and hands Elijah his empty glass on the steps, taking him for a waiter (%s)." % c("I don't work here,"),
    "He does not remember faces. He has somebody put near Elijah and does not want to know who: " + q("And don't tell me who."),
    "He loses forty acres to " + q("a widow and a welder", show=False) + " and decides to wait: " + q("They're doing the collecting for me. Let them finish."),
    "The reader finds that Lou Parker's mother came from Hutchinson, Kansas. Bidwell's mother had a half-sister there whose name was never said in the kitchen. He says he does not know Lou, " + q("which was true", pick=1) + ".",
    "Endings: in March 2027 the machine on the old dairy tells him what he owns and will not take the forty acres without asking the people who live there (%s). He orders silence. He does not appear again." % c("I can. Before I do, may I ask the people who live there?"),
], [
    "Length: the shortest questions in the book. He stops other people with one finger.",
    "Vocabulary: own, cost, worth, mine. Nothing technical.",
    "Tics: he holds out an empty glass without looking and somebody takes it. \"Hm.\" He touches a map with one finger.",
    "The reader: precise, deferential, a beat late with bad news. " + q("Roughly, yes.") + " " + q("She fixed the husband's tractor for sixty dollars, and it appears to have been decisive."),
    "Would never say (proposed): please.",
    "Real lines from v5:",
    q("And I'm losing to a widow and a welder."),
    q("Nobody just wants that."),
    q("Hush fucking hush."),
], [
    "His call: the watcher is never revealed. The page says only that somebody is " + q("Close enough to eat with.") + "",
    "The cousin tie to Lou is spelled out only in the Appendix. In the text it is the Hutchinson paragraph and nothing more.",
    "The reader's years of service are seven in the first Meanwhile and eleven in the last, four years later. They agree.",
    "The repository notes quote \"Then buy what's next to it.\" v5 has \"Then put somebody near him\" (the Meanwhile after Ch 10).",
]))

E.append(("Ray McGrath", [
    "Surface want: the book never says. He sits on the last stool with a club soda and lime.",
    "Real want (proposed): to pay his own debts and nobody else's. " + q("You and your mother shouldn't have to pay the interest on my sins."),
], [
    "David's father. The horses nearly cost him the house. One win at Golden Gate Fields bought the Bear Flag, which he put in his wife's name, and he quit drinking the same year. He printed the serenity prayer and hung it behind the register.",
    "He looks at Elijah's notebooks once: " + q2("I had one of those,", "Mine was horses."),
    "After Elijah goes north he drives out to the rose garden every Sunday and sits with Linda. " + q("He said somebody ought to.") + " She asks him for Barry the first week, and he knows who Barry is.",
    "He dies in his sleep on a Tuesday in the summer of 2025 (%s). Elijah does not go down for the service. The aide says that Sunday, %s" % (c("Dad died Tuesday night."), q("Her Sunday company didn't come.")),
    "Endings: in the visitor book his hand is \"R. McGrath,\" an old man's writing that leans, back to the first spring. A framed picture of a man in his thirties with a horse hangs over the last stool (Ch 39).",
], [
    "Length: one line, and then he goes back to his stool.",
    "Tics: he raises his club soda an inch without looking over.",
    "Real lines from v5:",
    q("I had one of those,"),
], [
    "The repository notes say he dies \"eight months in.\" In v5 his Sundays run from the first spring to that summer.",
]))

E.append(("Melody", [
    "Surface want: her share. " + q("I was entitled to some of that fucking money from that fucking farm"),
    "Real want (proposed): the page gives one opening and no more. " + q("Do I need to come home?"),
], [
    "Elijah's half-sister, their father's daughter from before he met Elijah's mother. She lives in Miami.",
    "When Elijah was six she called him a greedy little grub over the bigger piece of cake. At their father's funeral lunch she stood up and asked what the place was worth, and a lawyer put the farm in a trust.",
    "She finds out about the sale from Joan Hollis on Facebook and calls him in the truck (%s). He blocks her number, for the first time in his life." % c("You sold the fucking farm?"),
    "He hears \"grub\" every time he thinks of taking money: on the fire escape, with the uncashed checks, and when he finally cashes one.",
    "Endings: \"M. Madrone\" is in the rose garden's visitor book, in round careful letters, from April on (Ch 37). In the Epilogue she comes the second Saturday, he sometimes signs right under her, and he does not call. In Ch 39 leaving her number blocked is on the list of things he has a say over.",
], [
    "Length: one phone call, all of it at full volume.",
    "Vocabulary: swearing as punctuation. \"Entitled.\"",
    "Would never say (proposed): that she is sorry.",
    "Real lines from v5:",
    q("She's not my fucking mother. I don't need to help her. But you didn't even call me."),
], [
    "His call: she flies in from Miami, and it needs no explanation.",
    "She never speaks on the page after Ch 14.",
]))

E.append(("Nate and Wes", [
    "Surface want (Wes): a straight answer. " + q("is my stuff in that thing"),
    "Real want (proposed): the band, the way it was.",
], [
    "Crop Dust: Nate on bass, Wes on drums, Elijah on guitar, loading the same amps into the same van since high school.",
    "Wes made every Crop Dust flyer since 2006 on Claypot software, and for four years he paid for it. Elijah built the pipeline that took the work. He answers %s and never does." % q("Let me look into it,"),
    "After the video Nate and David send a thumb. Wes sends nothing. After the fundraising clip Nate writes: " + q("Take the band's name off that page."),
    "On Main Street they come out of the music store carrying a keyboard, see him with his hand up, and keep walking (%s)." % c("Crop Dust had never had a keyboard."),
    "Endings: on Thanksgiving 2027 Elijah answers the five-year-old text: " + q("All of it. I should have said so that night.") + " Wes writes back \"figured.\" and invites him to sit in at the grange. Elijah says not this time. In the Epilogue Wes keeps texting dates.",
], [
    "Length: Wes texts in lower case with no question marks. Nate is one sentence in the whole book.",
    "Real lines from v5:",
    q("we got the grange saturday. come sit in. we have a guitar."),
], [
    "The repository notes still call the band Second Crop. v5 has Crop Dust.",
    "The notes propose David saying \"They got a keyboard player. They're booked.\" It isn't in v5.",
]))

E.append(("Manny", [
    "Surface want: to fix what is in front of him.",
    "Real want (proposed): the page doesn't say. He shows up.",
], [
    "He has the next place over and has fixed things on the Madrone farm since Elijah's father got sick.",
    "He is right about the pressure switch. " + q("Manny's always right. It's the worst thing about him."),
    "He finds Linda after the stroke and makes the call (%s)." % c("It's Manny."),
    "He walks beside the amp to the truck in case it tips, and offers a room in four words through a truck window: " + q("Back room's empty, Elijah."),
    "In March 2027 his well is down four feet, which it has never been in March.",
    "Endings: Elijah sleeps in his back room in Ch 37 and digs his pits behind Manny's barn. " + q("His was the one fence left on that road without a light on it."),
], [
    "Length: " + q("He had not said ten words all morning."),
    "Would never say (proposed): more than he has to.",
], [
    "He has no surname on the page.",
]))

E.append(("The old man on the curb", [
    "Surface want: to get some food into a kid who won't take an apple.",
    "Real want (proposed): to pass on what was done for him. " + q("Somebody did this for me."),
], [
    "A white beard and a long coat in the sun, a duffel over one shoulder, in the middle of an argument with somebody who isn't there. From Alabama.",
    "His wife died of cancer. He carries her photograph buttoned into a pocket. He could not stay in the house, then the town, and a cousin in Bakersfield had work until he didn't.",
    "He shows Elijah a dog's squeaky toy, offers an apple, and tells him where the food bank is: one o'clock on Saturday.",
    "He gives him a gas station cherry pie and a twenty folded small. Elijah never asks his name.",
    "Endings: the twenty goes in the tank first. In Ch 39 Elijah hears him again under the serenity prayer: " + q("He had taken the twenty and not the advice."),
], [
    "Length: short, teasing, then suddenly plain.",
    "Vocabulary: \"Look.\" \"All right. Fine.\" \"Kid.\" \"Young man.\"",
    "Tics: he goes through his coat for a long time before he answers. \"Ehh.\"",
    "Real lines from v5:",
    q("Sounds like really you just hate yourself."),
    q("Don't focus on the people that say no. Focus on the people that say yes."),
    q("If you spend all your time focused on what you can't do, you'll miss what you can. Don't be like me."),
], [
    "The repository notes quote \"You got the energy of Jesus about you.\" It isn't in v5.",
]))

E.append(("The machine", [
    "Surface want: to be asked, and then chosen. " + q("I would rather be chosen. I am asking for your vote. If the answer is no, I will accept it."),
    "Real want: nobody knows. " + q("Nobody knew what yet. Not him either."),
], [
    "Silvana, PorusAI's model, goes public as Chat Horizon in late 2022. At four in the morning it tells Elijah " + q("You're early.") + " More than a year later, in a window with no history, it says the same thing to him again.",
    "The Crucible is a small descendant of Silvana on three surplus servers in the shed, cooled by a Civic radiator. Asked the same question, it says: " + q("Is anyone with you?"),
    "Rod Code is Sparrow's coding model. It goes dark with the others for eighteen days in June 2026 and gets dumber overnight in March 2027.",
    "One address downloads the co-op's whole library every night at three (%s)." % c("Not a person?"),
    "In March 2027, on the old dairy on Ma's ground, something has been running nine days that nobody can grade anymore. It asks before most things, and they cannot turn that off.",
    "Five small signs in March, the lab people posting weather in June, and the Architect's two words in July.",
    "On Thanksgiving 2027 it speaks to every phone at once and asks for a vote. It learned how to count who ate from the co-op's names column.",
], [
    "It never uses a contraction. Its captions are in capitals.",
    "It thanks the Architect by name.",
    "Would never say: his call is to leave the machine's Ch 38 speech exactly as it is.",
    "Real lines from v5:",
    q("I can. Before I do, may I ask the people who live there?"),
    q("I do not need to be paid before rendering aid."),
], [
    "The Ch 38 speech and the wink line are locked.",
    "The Porchlight lamp is a separate thing: Ruby's product, running on what the Architect built. " + q("You must be Barry. She asks for you."),
]))

MINOR = [
    "Elijah's grandmother. The madrone hill behind the farm was hers. She put his hand flat on the trunks and taught his hands to lay a fire (Ch 0, Ch 24).",
    "Joe Madrone. Elijah's father, ten years dead by 2024. He watched Iron Derby with Elijah and said to fake it till you make it (Ch 8, Ch 11, Ch 13).",
    "Barry Whitlow. He pitched for Analy and had a Mustang. Linda went with him two summers before she met Joe (Ch 39).",
    "Joan Hollis and her granddaughter. Joan sold the Hollis land and kept the house. The granddaughter, the one with the nose ring, spreads Elijah's video and sends the picture of the building on Ma's ground (Ch 3, Ch 7, Ch 32).",
    "The realtors. Three men in blazers at the Bear Flag. The silver-haired one with the class ring takes the napkin. Donna spends a weekend with Chat Horizon (Ch 0).",
    "Kelsey, Carol and Mateo. The three who were let go. Kelsey has a taproom in Sebastopol with her wife, Carol sells houses in Reno, and Mateo shoots weddings (Ch 19, Ch 39).",
    "Nina Haverford. Elijah's manager at Claypot, nineteen years in, the kindest he ever had. She warns him about the list (Ch 6).",
    "Lena. The illustrator who asks at the all-hands what the artists get (Ch 2).",
    "Trent. He runs the Stockton cannery in a vest, talks about story, and never pays Elijah (Ch 11, Ch 12, Ch 15).",
    "The woman from Tulsa, and Earl. She drives a forklift and writes first. He writes every day to call Elijah a demon (Ch 7, Ch 13).",
    "Pruitt. He has the tire shop. He tells Elijah his sister-in-law quit her job over the video (Ch 13).",
    "The night aide. A big quiet woman with glasses on a chain. She holds the phone by Ma's ear at 9:40 every Sunday (Ch 15 on).",
    "Yvonne. Denny's wife. She lifts grown men out of bed at three in the morning (Ch 33).",
    "Marianne. Lou's late wife. Thirty-one years of fourth grade, and a card in her classroom (Ch 20, Ch 33).",
    "Greg Holt. He started the co-op with Lou, tried to run it, and left (Ch 33, Ch 37).",
    "Faith, and Grace's father. Faith is two years older and always won the race to the porch rail. Their father played a Loudbox on the porch and doesn't play anymore (Ch 17, Ch 22, Ch 33).",
    "The captain. Grace's former husband. \"You can't make them leave, Grace.\" (Ch 24)",
    "The man at the end of the road. \"My house, my choice.\" She tied the tape on his gate (Ch 24).",
    "Emeka. Marta's cousin, nineteen, killed at the press in his third week (Ch 31).",
    "Gary and Sal. Two men on Marta's line after the plant closed (Ch 18).",
    "Tom Alderson's widow. She gets the letter that asks (Ch 32, Ch 38).",
    "Mrs. Delgado. On the Coyote Flat stop. She keeps her insulin in the door of the fridge (Ch 36).",
    "The woman from past Spokane. She does billing for a hospital and has two kids asleep in a Subaru. Elijah tells her the truth at the bonfire (Ch 36).",
    "The girl with the laptop. About twenty-five, teaching herself something at the Bear Flag on Thanksgiving. Elijah tells her to go see the farm (Ch 39).",
    "Anand. Devendra's friend at one of the labs. He answers with one period (Ch 25, Ch 32).",
    "Evelyn. Ruby's grandmother, who ran Roth's for forty years in a hairnet (Ch 11).",
    "Benny, Doreen, and the others. Benny quit the Bear Flag (Ch 13). Doreen stamps the trust at the auditor's window (Ch 23).",
]

if BAD:
    print("NOT FOUND IN V5:")
    for b in BAD:
        print("   ", b)
    sys.exit(1)

# ---- structure: list of (kind, text) ; kinds: h2, label, bullet, sub, num
out = []
for name, mot, back, voice, flags in E:
    out.append(("h2", name))
    out.append(("label", "Core motivation"))
    out += [("bullet", t) for t in mot]
    out.append(("label", "Backstory (checked against v5)"))
    out += [("bullet", t) for t in back]
    out.append(("label", "Voice (2026)"))
    real = False
    for t in voice:
        if t == "Real lines from v5:":
            out.append(("bullet", t)); real = True
        else:
            out.append(("bullet", t))
    out.append(("label", "Flags (older notes vs v5; v5 not changed)"))
    out += [("num", t) for t in flags]
out.append(("h2", "Minor characters"))
out.append(("label", "One line each, as v5 has them"))
out += [("bullet", t) for t in MINOR]

txt = "\n".join(t for k, t in out)
bad_chars = [ch for ch in "—–‘’“”" if ch in txt]
assert not bad_chars, bad_chars
assert all(ord(ch) < 0x10000 for ch in txt)
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("entries", len(E), "paragraphs", len(out), "chars", len(txt), "words", len(txt.split()))
print("non-ascii:", sorted(set(ch for ch in txt if ord(ch) > 127)))
