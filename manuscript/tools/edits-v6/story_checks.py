#!/usr/bin/env python3
"""Story checks: sheets that test the book against itself. Built from the page, like knowledge.py.

    python3 manuscript/tools/edits-v6/story_checks.py calendar OUT/v6.txt OUTDIR [--date 2026-11-27]

calendar  Every scene on a date, every time word the scene holds, and a list of checks a calendar can
          settle (weekdays, intervals, ages). Writes calendar-DATE.csv and calendar-checks-DATE.csv.
          WHEN below is the only hand-written part: one line per scene, "n|sort|when|how". "how" is
          stated (the page gives it), worked (worked out from other scenes) or back (back story).
          CHECKS quotes the lines each check rests on; a quote that is not in the book stops the run.

conversations  Layer one of the conversation map: what a script can count. For each scene, who speaks and how
          many lines, how much of it is talk, and how many sound, touch, smell and taste words it holds; for each
          pair of people, how many lines they trade and where; for each person, lines by chapter. A line's speaker
          is the first name in its narration; an untagged line between two people goes to the other one. It does
          not read for meaning: what a conversation does for the story is layer two, a reader's job.
          Writes conversations-DATE.csv, conversation-pairs-DATE.csv and conversation-lines-DATE.csv.

desires        The desires sheet: one row per person (DESIRES) and one per scene (desires-scenes-data-DATE.json).
conversations2 Layer two of the conversation map (CONVERSATIONS2): what each wants from the other, what changes, what it pays off.
money          Every money figure on the page (counted by MONEY_RX) and MONEY_CHECKS, with verdicts.
objects        Where each object is at every sighting (OBJECTS), in book order.
plants         Every question in the scene sheet's "Opens a question" column, with a verdict from PLANTS.
All five use Book: each quoted line is found in the built book, and a line that is gone stops the run.
"""
import csv
import json
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_sheet  # noqa: E402

NUM = r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|a|an|\d+)"
TIME = re.compile(r"(?i)\b(20[12]\d|January|February|March|April|May\b(?! be)|June|July|August|September|October|November|December|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|spring|summer|fall\b|winter|Thanksgiving|Christmas|midterms|" + NUM + r"[ -](?:days?|weeks?|months?|years?)\b(?: (?:ago|later|after|before|back|old|out))?|thirty-\w+ years old|first of the month)")

WHEN = """
1|2022-11-08|November 2022, the night he shows the realtors, with his back story (scenes merged by edit 255)|worked
2|2022-11-15|A week later, a Tuesday: the toast|stated
3|2022-11-15|That night, 12:30 a.m.|stated
4|2022-11-21|The Monday after the toast: the bet|stated
5|2022-11-21|The same Monday, at the Bear Flag|stated
6|2022-11-21|That night: the tower|stated
7|2023-02|Early 2023, a morning: the all-hands; then the same morning|worked
8|2023-02|That night|stated
9|2023-02|The same day, in the air|worked
10|2023-03|Three weeks after the all-hands|stated
11|2023-03|A Sunday, 9:40|stated
12|2023-03|A Friday and Saturday|stated
13|2023-04|The next Monday and the week after: the bill|stated
14|2023-04|A Wednesday|stated
15|2023-04|That weekend|stated
16|2023-10-17|October 2023, eleven months after the toast: laid off|stated
17|2023-10-17|The same day: the video; then that night and the next morning|stated
18|2023-10-20|October to December 2023: the replies|stated
19|2023-12|A Sunday, 9:55|stated
20|2024-01|A Thursday in January 2024|stated
21|2024-01|The same night, in the truck|stated
22|2024-02|February 2024: San Francisco; then the same afternoon|stated
23|2024-02|That night: the house on the hill; then the same night|stated
24|2024-02|The same night, until two; then after two in the morning|stated
25|2024-02|The same night|worked
26|2024-03|Spring to August 2024: the apartment goes in April, a month at Ma's, the cannery|stated
27|2024-08-09|August 2024, six in the morning: the ride with Gus; then the same morning|worked
28|2024-08-12|Three weeks in August 2024; the launch party is the third Friday|stated
29|2024-08-31|The morning after, to Monday; the stroke is Sunday night|stated
30|2024-09-02|That Monday: the hospital|stated
31|2024-09-03|That week: the house|worked
32|2024-09-04|That week: the two pages|worked
33|2024-09-04|That week|worked
34|2024-09-05|That week: he asks online|worked
35|2024-09-06|The man from Sacramento; the signing; the wire clears on a Friday|stated
36|2024-09-11|Two days before the wire, a Wednesday|stated
37|2024-09-12|The next morning (Thursday), and Friday morning|stated
38|2024-09-13|That Friday night: the first rain since April|stated
39|2024-09-14|Five months, September 2024 to the last week of February 2025 (Tuesday to Friday)|stated
40|2025-03-01|Saturday 1 March to Monday 3 March 2025; he drives north|worked
41|2025-03-04|Tuesday 4 March 2025: the broom; then the same evening|worked
42|2025-03-05|His first days: the fourth day is Friday 7 March; Praether; the arms come Wednesday 12 March|worked
43|2025-03-12|March 2025: the barn; his first Sundays|worked
44|2025-03-28|Friday 28 March 2025, three weeks after the broom: his first dinner; then the same dinner|worked
45|2025-03-30|That Sunday; then the same day|stated
46|2025-04-01|The following Tuesday|stated
47|2025-04-24|Late April 2025, Thursday to Monday, seven weeks after the broom|stated
48|2025-04-01|Earlier that April, to May: the order, the two designs|stated
49|2025-05-03|The first build weekend|worked
50|2025-05-10|The second build weekend|stated
51|2025-05-20|May 2025: the boxes ship|stated
52|2025-05-12|May 2025: the drip tape|stated
53|2025-06-09|June 2025 (the second week): the two videos|stated
54|2025-06-26|The last week of June 2025: a hundred and four|stated
55|2025-05-30|The end of May to early July 2025: the servers|stated
56|2025-07-03|Thursday 3 July to Saturday 5 July 2025: Ray, the leak; then that Saturday morning|worked
57|2025-07-05|That weekend, to Monday|stated
58|2025-07-15|July and August 2025: the land trust|worked
59|2025-08|Summer 2025|worked
60|2025-08-15|The middle of August 2025|stated
61|2025-08-25|The last week of August into September 2025: the shouse|stated
62|2025-09-27|Saturday 27 September 2025: the first fire; Sunday the call|stated
63|2025-10-05|The next Sunday|stated
64|2025-09-27|The same night, by eleven|stated
65|2025-03|Spring to fall 2025: the store dies|stated
66|2025-10-15|Fall 2025, after the first frost: the letter, the frozen yogurt|stated
67|2025-10-17|A Friday dinner|stated
68|2025-10-25|Fall 2025: the cyberdeck|worked
69|2025-11-12|The second week of November 2025: the pond|stated
70|2025-11-26|Wednesday 26 November 2025: he starts for home and turns back|stated
71|2025-11-26|That night|stated
72|2025-12-09|December 2025, the evening before Grace leaves for the winter: Lou and the cider|worked
73|2025-12-10|The next morning: Grace leaves|worked
74|2026-03|Spring 2026: the beds|stated
75|2026-05|May 2026: the rover|stated
76|2026-05|Two nights later|stated
77|2026-05-22|A Friday in May 2026, before dinner: Miles Renner on the big screen|worked
78|2026-06-12|Friday 12 June to 30 June 2026: the models go dark|stated
79|2025-11-28|The Friday after Thanksgiving 2025 to July 2026: the pay|stated
80|2026-08|August to October 2026: the pits|stated
81|2026-10|October 2026: the laser weeder; Marta|stated
82|2026-10|The night after: the amp at the pond|stated
83|2026-10|October 2026: the first fire video; a week later|worked
84|2026-10|The same morning, and that Friday|stated
85|2026-10|To Friday 6 November 2026, after the midterms|stated
86|2026-11-10|October to November 2026: the weeks after the pond; the morning in his T-shirt|stated
87|2026-11-10|That afternoon, in the shop: Marta's look|stated
88|2026-11-20|Friday 20 November 2026; Thanksgiving is the 26th|stated
89|2026-12-05|Saturday 5 December 2026: the well|stated
90|2026-12-15|December 2026: the storm|stated
91|2027-01|January 2027: the grange kitchen|stated
92|2027-01|January 2027: the annual meeting|worked
93|2027-01|A few nights after|stated
94|2027-02|The night before the county meeting|stated
95|2027-02|The county meeting|worked
96|2027-02|The third week of the apprenticeship|stated
97|2027-02-12|February 2027, a Friday: the plan|stated
98|2027-02-15|The Monday after, and two days later|stated
99|2027-02-16|That week|stated
100|2027-02-20|Saturday 20 February 2027: the tea|worked
101|2027-02-21|Sunday 21 February: Marta, the brake|stated
102|2027-02-28|Sunday 28 February, Monday 1 March (the pit), and that Friday|worked
103|2027-03|March 2027, on the dairy|worked
104|2027-03|March 2027: five small things|stated
105|2027-03-28|Late March 2027|stated
106|2027-04-01|The first of April 2027, the pit: Priya's ankle|stated
107|2027-04-01|Thursday 1 April 2027 to the next Friday|stated
108|2027-04-10|April to June 2027: the juniper|stated
109|2027-06|June to Friday 9 July 2027|stated
110|2027-07-09|Friday dinner, 9 July 2027; then the same evening|worked
111|2027-07-16|The next Friday|stated
112|2027-10-02|Early October 2027, a Saturday to Tuesday: the tractor|stated
113|2027-10-11|The afternoon before the October meeting|stated
114|2027-10-12|A Tuesday in the middle of October 2027: the meeting; then the same night|stated
115|2027-10-13|Six the next morning|stated
116|2027-10-13|That night|stated
117|2027-10-23|The Saturday before the festival|stated
118|2027-10-27|The Wednesday of festival week|stated
119|2027-10-30|The last night of the festival: the fire|worked
120|2027-11-01|The week after; he packs on Tuesday 9 November 2027|worked
121|2027-11-09|The same Tuesday|stated
122|2027-11-09|The same Tuesday|stated
123|2027-11-09|Two days south; the rose garden; Manny's|stated
124|2027-11-25|Thursday 25 November 2027|stated
125|2027-11-23|Tuesday 23 to Thursday 25 November 2027|stated
126|2027-11-25|Thanksgiving night, the Bear Flag|stated
127|2027-11-25|The same night|stated
128|2027-12|December 2027 to April 2028|stated
"""
BACK_ON_PURPOSE = {36, 48, 52, 55, 64, 65, 79, 125}  # renumbered after edit 267 merged thirteen scenes  # scenes the book tells out of order


def D(y, m, d):
    return dt.date(y, m, d)


def day(d):
    return d.strftime("%A")


CHECKS = [  # (what, [quotes], function -> (verdict, detail))
    ("Thanksgiving 2027 is Thursday 25 November", ["It was Thursday, November 25, 2027."],
     lambda: (day(D(2027, 11, 25)) == "Thursday", day(D(2027, 11, 25)))),
    ("12 June 2026, when the models go dark, is a Friday", ["On June 12 the big models went dark.", "Worldwide. On a Friday."],
     lambda: (day(D(2026, 6, 12)) == "Friday", day(D(2026, 6, 12)))),
    ("The models are dark eighteen days (12 to 30 June)", ["On June 30 they turned the models back on.", "And then in the eighteen days you called Grace crying."],
     lambda: ((D(2026, 6, 30) - D(2026, 6, 12)).days == 18, f"{(D(2026, 6, 30) - D(2026, 6, 12)).days} days")),
    ("The morning after a Sunday call is 'the first of the month': 1 March 2027 is a Monday", ["The next Sunday at 9:40 he called the rose garden.", "The next morning was the first of the month, the day for the pit."],
     lambda: (day(D(2027, 3, 1)) == "Monday", f"1 March 2027 is a {day(D(2027, 3, 1))}; 'December was ten months off' puts the plan in February")),
    ("The last route box, 28 December 2027, falls on a route day (Tuesday)", ["December twenty-eighth is the last box she gets.", "The route still ran on Tuesdays"],
     lambda: (day(D(2027, 12, 28)) == "Tuesday", day(D(2027, 12, 28)))),
    ("The first fire is a Saturday in the last week of September 2025", ["The first cold night came in the last week of September.", "It was a Saturday. The next morning at 9:40"],
     lambda: (day(D(2025, 9, 27)) == "Saturday", "27 September 2025 is a Saturday")),
    ("The Architect posts on 9 July 2027, and Denny asks 'Is Friday still Friday?'", ["On the ninth of July, the Architect posted.", "Is Friday still Friday?"],
     lambda: (day(D(2027, 7, 9)) == "Friday", f"9 July 2027 is a {day(D(2027, 7, 9))}: it is that day's dinner")),
    ("The Riemann dinner: the Friday before Thanksgiving 2026 is 20 November, the real date of the news", ["Dinner on the Friday before Thanksgiving was just dinner."],
     lambda: (day(D(2026, 11, 20)) == "Friday" and D(2026, 11, 26).weekday() == 3, "20 November 2026, Friday")),
    ("The first Saturday in December 2026 is the 5th", ["the first Saturday in December"],
     lambda: (day(D(2026, 12, 5)) == "Saturday", "5 December 2026")),
    ("The lien sale: eleven days after a Wednesday is a Sunday, and Elijah tells Lou 'This Sunday'", ["On Wednesday the delivery app sent him a notice.", "the lien sale was eleven days out", '"Sunday," he said. "This Sunday."'],
     lambda: ((D(2025, 2, 26) + dt.timedelta(11)).weekday() == 6, f"Wednesday 26 February 2025 plus eleven days is {day(D(2025, 2, 26) + dt.timedelta(11))} 9 March; he says it on Friday 7 March")),
    ("He arrives on a Tuesday, a route day, after leaving on Monday and 'two days of driving'", ["On Monday he drove to the gas station", "It's two days of driving", "She's on the route. It's Tuesday."],
     lambda: (True, "Monday 3 March to Tuesday 4 March 2025 is one night on the road: 'two days' holds if he arrives the second day")),
    ("The late April crisis is 'seven weeks after he'd walked into the shop'", ["found him in late April, seven weeks after he'd walked into the shop", "Claypot shipped Companion 2.0 on a Thursday afternoon"],
     lambda: (abs((D(2025, 4, 24) - D(2025, 3, 4)).days - 49) <= 3, f"4 March to Thursday 24 April 2025 is {(D(2025, 4, 24) - D(2025, 3, 4)).days} days")),
    ("He leaves on a Tuesday while Grace is on the route", ["On Tuesday he packed.", "She was on the route. It was Tuesday."], lambda: (True, "both say Tuesday")),
    ("The laid-off video is four years before Thanksgiving 2027 and eleven months after the toast", ["Elijah got laid off eleven months after the toast.", "That's four years.", "She had watched it in October, the morning after he posted"],
     lambda: (True, "toast November 2022, layoff October 2023, four years and a month to November 2027")),
    ("The document was started 'fifteen months back' from February 2024", ["he'd started at 12:30 in the morning, fifteen months back"],
     lambda: ((2024 - 2022) * 12 + (2 - 11) == 15, "November 2022 to February 2024 is 15 months")),
    ("The lecture is 'twelve years old' in early 2023 and 'thirteen years before' in February 2024", ["It was twelve years old and the sound was bad.", "thirteen years before"],
     lambda: (True, "a lecture from 2011 fits both")),
    ("Ma's last whole sentences were first said 'eleven months ago' (October 2023 to September 2024)", ["She had said those words to him the first time eleven months ago."],
     lambda: ((2024 - 2023) * 12 + (9 - 10) == 11, "11 months")),
    ("The pawn ticket: four months from the fourth month in the truck runs out in May", ["In the fourth month he took the Telecaster out from behind the seat.", "The four months on the pawn ticket had run out in May"],
     lambda: (True, "pawned January 2025, due May 2025")),
    ("He does not cash a check for sixteen months (July 2026 to November 2027)", ["so it waited for a vote until July, more than a year after he came.", "for sixteen months he had put them in the back of a notebook"],
     lambda: ((2027 - 2026) * 12 + (11 - 7) == 16, "16 months")),
    ("He blocked Melody 'two and a half years ago' in February 2027", ["He had blocked Melody's number two and a half years ago"],
     lambda: (abs(((2027 - 2024) * 12 + (2 - 9)) - 30) <= 2, f"{(2027 - 2024) * 12 + (2 - 9)} months")),
    ("Reuben has had the deed 'a year and a half' in January 2027", ["I've had this a year and a half."],
     lambda: (abs(((2027 - 2025) * 12 + (1 - 7)) - 18) <= 2, "from July 2025: 18 months")),
    ("Elijah's age: thirty-five in January 2024, thirty-six in early March 2025, thirty-seven in May 2025", ["He was thirty-five years old", '"I\'m thirty-six," Elijah said.', "He was thirty-seven years old and he had never been so tired"],
     lambda: (True, "All three hold if his birthday falls between about 3 March and mid May. That is the window for the birthday scene.")),
    ("Tyler's age: nineteen in spring and fall 2025, twenty in June 2026, twenty-one in January and November 2027", ["He was nineteen, and he was the Tyler who had found", "He was twenty. He just put it away.", "She looked at Tyler, twenty-one years old", "Tyler stood there, twenty-one years old"],
     lambda: (True, "All hold if his birthday falls between about 10 November and the January meeting.")),
    ("NOT ON THE CALENDAR'S SIDE: 'They've been there since my first week'", ["They've been there since my first week.", "They'll be here on Wednesday."],
     lambda: (False, "He arrives Tuesday 4 March; the arms come the Wednesday after the Sunday lien sale, 12 March: his second week. (Already in the scene sheet audit.)")),
    ("NOT ON THE CALENDAR'S SIDE: the squash", ["But the squash has to come in this week.", "The winter squash had to come in.", "We'd have the squash in by Wednesday."],
     lambda: (False, "The tractor scene is at least nine days before the mid October meeting, and the squash 'has to come in this week'; at the meeting and in festival week it is still in the field. (Already in the scene sheet audit.)")),
    ("NOT ON THE CALENDAR'S SIDE: the last grant 'ran out in June'", ["and the last one ran out in June.", "\"The route's got no money past June.\""],
     lambda: (False, "It is October 2026 and the route is running: the scene means next June. (Already open with CT.)")),
    ("TIGHT, NOT BROKEN: the board is 'ours' in April", ["Earlier that April the order had come", "The first design had already eaten the better part of a month", "In April Marta had run her finger along the drawing of that board", "I saw it in April."],
     lambda: (None, "The order comes in April, the first design takes 'the better part of a month', and Marta and Tyler both place the finished board in April. It holds only if the order came in the first days of April; the build weekends then run into May, when the boxes ship.")),
    ("ODD, LOW: route boxes are packed on a Wednesday night", ["He told Grace on the Wednesday of festival week, in the packing shed, a little before midnight.", "They were building route boxes by hand."],
     lambda: (None, "The route runs on Tuesdays, so these are packed six days ahead or the festival moved the route. Nothing on the page says which.")),
]


def norm(s):
    return s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def calendar(book, outdir, date):
    sc = scene_sheet.scenes(book)
    text = norm(open(book).read())
    when = {}
    for line in WHEN.strip().split("\n"):
        n, sort, label, how = line.split("|")
        when[int(n)] = (sort, label, how)
    if len(sc) != len(when):
        sys.exit(f"The book has {len(sc)} scenes and WHEN has {len(when)}: a scene was added, cut or split. Fix WHEN.")
    rows, prev = [], ""
    for n, (head, k, paras) in enumerate(sc, 1):
        sort, label, how = when[n]
        words = []
        for p in paras:
            for m in TIME.finditer(p):
                w = m.group(0)
                if w.lower() not in [x.lower() for x in words]:
                    words.append(w)
        back = ""
        if how != "back" and sort < prev:
            back = "on purpose" if n in BACK_ON_PURPOSE else "CHECK"
        if how != "back":
            prev = max(prev, sort) if n in BACK_ON_PURPOSE else sort
        rows.append([n, head, k, " ".join(paras[0].split()[:9]), label, sort, {"stated": "on the page", "worked": "worked out", "back": "back story"}[how], back, "; ".join(words)])
    checks = []
    for what, quotes, fn in CHECKS:
        for q in quotes:
            if norm(q) not in text:
                sys.exit(f"NOT IN THE BOOK: {q!r}")
        ok, detail = fn()
        checks.append([what, {True: "holds", False: "does not hold", None: "read it"}[ok], detail, " | ".join(quotes)])
    os.makedirs(outdir, exist_ok=True)
    for name, header, data in [("calendar", ["#", "Chapter", "Scene", "Opens with", "When", "Sort date", "How we know", "Steps back in time", "Time words on the page"], rows),
                               ("calendar-checks", ["The check", "Verdict", "Why", "The lines it rests on"], checks)]:
        with open(os.path.join(outdir, f"{name}-{date}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(data)
    bad = [r for r in rows if r[7] == "CHECK"]
    print(f"{len(rows)} scenes dated; {len(checks)} checks: " + ", ".join(f"{v} {sum(1 for c in checks if c[1] == v)}" for v in ("holds", "does not hold", "read it")))
    for r in bad:
        print("  steps back without a reason:", r[0], r[1], "|", r[4])


# ---------------------------------------------------------------- conversations (layer one: what a script can count)
PEOPLE_C = {  # name on the page -> who (first match in the narration of a line of talk is taken as its speaker)
    "Elijah": "Elijah", "Grace": "Grace", "Lou": "Lou", "Marta": "Marta", "Curtis": "Curtis", "Priya": "Priya",
    "Tyler": "Tyler", "Denny": "Denny", "Reuben": "Reuben", "Patricia": "Patricia", "Irene": "Irene", "Wren": "Wren",
    "Frank": "Frank", "Rosa": "Rosa", "Hector": "Hector", "Lupe": "Lupe", "David": "David", "Devendra": "Devendra",
    "Ruby": "Ruby", "Gus": "Gus", "Trent": "Trent", "Melody": "Melody", "Manny": "Manny", "Ray": "Ray",
    "Praether": "Praether", "Bidwell": "Bidwell", "the reader": "Bidwell's reader", "The reader": "Bidwell's reader",
    "his mother": "Ma", "His mother": "Ma", "the aide": "the aide", "Nina": "Nina", "Dale": "Dale", "Yvonne": "Yvonne",
    "the old man": "the old man", "The old man": "the old man", "the realtor": "the realtor", "The realtor": "the realtor",
    "the moderator": "the moderator", "the voice": "the Architect", "Tyler's": "Tyler",
}
WOMEN = {"Grace", "Marta", "Priya", "Patricia", "Irene", "Wren", "Rosa", "Lupe", "Melody", "Ma", "the aide", "Nina", "Yvonne", "the Architect"}
NAME_RE = re.compile("|".join(sorted((re.escape(k) for k in PEOPLE_C), key=len, reverse=True)))
QUOTE = re.compile(r'"[^"]*"?')
SENSES = {
    "Sound": r"\b(heard|hear|sound\w*|ticked|ticking|buzz\w*|rang|ring\w*|hum\w*|quiet|loud\w*|clank\w*|click\w*|voice|radio|bell|laugh\w*|shout\w*|yell\w*|whisper\w*)\b",
    "Touch": r"\b(cold|warm\w*|hot|heat|cool|wet|damp|soft|rough|touch\w*|squeez\w*|grip\w*|hug\w*|shak\w+|shook|hand on|hands on|held|holding)\b",
    "Smell": r"\b(smell\w*|scent|stink\w*|reek\w*|perfume)\b",
    "Taste": r"\b(tast\w+|flavor\w*|sweet|bitter|sour|salt\w*)\b",
}


def conversations(book, outdir, date):
    sc = scene_sheet.scenes(book)
    scene_rows, pair, lines_by = [], {}, {}
    chapters, total, named = [], 0, 0
    for n, (head, k, paras) in enumerate(sc, 1):
        ch = head.split(":")[0].replace("Chapter ", "Ch ")
        if ch not in chapters:
            chapters.append(ch)
        last, prev2, seq = None, None, []
        last_g = {"f": None, "m": None}
        pov = any("Elijah" in p for p in paras)   # the book sits on his shoulder: an unnamed "he" is nearly always him
        for p in paras:
            p = norm(p)
            narr = QUOTE.sub(" ", p) if '"' in p else p
            found = [PEOPLE_C[m.group(0)] for m in NAME_RE.finditer(narr)]
            if '"' in p:
                total += 1
                pro = re.search(r"\b(she|her|he|his|him)\b", narr, flags=re.I)
                if found:
                    who = found[0]
                    named += 1
                elif pro and pro.group(1).lower() in ("she", "her") and last_g["f"]:
                    who = last_g["f"]                                   # "she said": the last woman named
                elif pro and pro.group(1).lower() in ("he", "his", "him") and (pov or last_g["m"]):
                    who = "Elijah" if pov else last_g["m"]
                elif last and prev2 and last != prev2:
                    who = prev2      # two people trading lines: an untagged line goes to the other one
                else:
                    who = "?"
                if who != "?" and who != last:
                    prev2, last = last, who
                seq.append(who)
            for w in found:
                last_g["f" if w in WOMEN else "m"] = w
        known = [w for w in dict.fromkeys(seq) if w != "?"]
        if len(known) == 1 and pov and known[0] != "Elijah":
            known.append("Elijah")
        if len(known) == 2:              # a two-person scene: fill the gaps by turns
            for i, w in enumerate(seq):
                if w == "?":
                    prev = seq[i - 1] if i else None
                    seq[i] = known[1] if prev == known[0] else known[0] if prev == known[1] else "?"
        speakers = {}
        for w in seq:
            if w != "?":
                speakers[w] = speakers.get(w, 0) + 1
                lines_by.setdefault(w, {}).setdefault(ch, 0)
                lines_by[w][ch] += 1
        for a, b in zip(seq, seq[1:]):
            if a != b and "?" not in (a, b):
                key = tuple(sorted((a, b)))
                d = pair.setdefault(key, {"n": 0, "scenes": [], "ch": []})
                d["n"] += 1
                if n not in d["scenes"]:
                    d["scenes"].append(n)
                if ch not in d["ch"]:
                    d["ch"].append(ch)
        text = " ".join(paras)
        senses = [len(re.findall(rx, text, flags=re.I)) for rx in SENSES.values()]
        talk = sum(len(q.split()) for p in paras for q in QUOTE.findall(norm(p)))
        words = sum(len(p.split()) for p in paras)
        order = sorted(speakers.items(), key=lambda x: -x[1])
        scene_rows.append([n, head, k, " ".join(paras[0].split()[:8]), words, f"{100 * talk // max(words, 1)}%", len(seq),
                           "; ".join(f"{w} {c}" for w, c in order), seq.count("?")] + senses)
    os.makedirs(outdir, exist_ok=True)

    def write(name, header, rows):
        with open(os.path.join(outdir, f"{name}-{date}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)

    write("conversations", ["#", "Chapter", "Scene", "Opens with", "Words", "In quotes", "Lines of talk", "Who speaks (lines)", "Lines with no speaker found"] + list(SENSES), scene_rows)
    prow = [[a, b, d["n"], len(d["scenes"]), d["ch"][0], d["ch"][-1], ", ".join(d["ch"])] for (a, b), d in sorted(pair.items(), key=lambda x: -x[1]["n"])]
    write("conversation-pairs", ["Who", "With", "Lines traded", "Scenes", "First", "Last", "Where"], prow)
    who_order = sorted(lines_by, key=lambda w: -sum(lines_by[w].values()))
    write("conversation-lines", ["Who", "All"] + chapters, [[w, sum(lines_by[w].values())] + [lines_by[w].get(c, "") for c in chapters] for w in who_order])
    unk = sum(r[8] for r in scene_rows)
    print(f"{len(scene_rows)} scenes, {total} lines of talk: {named} with a name beside them, {total - named - unk} placed by pronoun or by turns, {unk} not placed ({100 * unk // total}%); {len(pair)} pairs")
    return pair, lines_by, chapters


# ---------------------------------------------------------------- shared: find a quote, say where it is
class Book:
    """The built book, line by line, with each line's chapter and scene-sheet row (#).

    find(quote) returns (line number, chapter, sheet row) for the nth line holding the quote, and stops the run
    if the quote is not in the book. Sheet rows are the scene sheet's own numbers (its row 47 is a cut scene)."""

    def __init__(self, book, outdir):
        self.lines = norm(open(book).read()).split("\n")
        sc = scene_sheet.scenes(book)
        sheet = list(csv.reader(open(os.path.join(outdir, "scene-sheet-2026-11-27.csv"))))[1:]
        key = lambda s: re.sub(r"[^a-z ]", "", norm(s).lower().replace("...", ""))[:30]
        sheet_no = {key(r[-1]): int(r[0]) for r in sheet}
        self.where = {}          # line index -> (chapter, sheet row)
        self.scenes = []         # (sheet row, chapter, first line index, last line index)
        i = 0
        for head, _, paras in sc:
            first = None
            for p in paras:
                p = norm(p)
                while self.lines[i] != p:
                    i += 1
                first = i if first is None else first
                self.where[i] = (head, sheet_no.get(key(paras[0]), 0))
            self.scenes.append((sheet_no.get(key(paras[0]), 0), head, first, i))
        if len(self.scenes) != len([r for r in sheet if r[-1] != "(cut)"]) or 0 in [s[0] for s in self.scenes]:
            sys.exit("The scenes no longer match the scene sheet: rebuild the sheet first.")

    def find(self, quote, nth=1):
        q = norm(quote)
        hits = [i for i, l in enumerate(self.lines) if q in l]
        if len(hits) < nth:
            sys.exit(f"NOT IN THE BOOK ({len(hits)} found, wanted number {nth}): {quote!r}")
        i = hits[nth - 1]
        ch, no = self.where.get(i, (self.heading_at(i), ""))
        return i + 1, ch.split(":")[0].replace("Chapter ", "Ch "), no

    def heading_at(self, i):
        for j in range(i, -1, -1):
            if scene_sheet.SECTION.match(self.lines[j]) or self.lines[j] in scene_sheet.STOP:
                return self.lines[j]
        return "front"

    def first(self, pattern):
        rx = re.compile(pattern)
        body = [i for i in sorted(self.where) if rx.search(self.lines[i])]
        if not body:
            sys.exit(f"NO LINE NAMES {pattern!r}")
        i = body[0]
        ch, no = self.where[i]
        return i + 1, ch.split(":")[0].replace("Chapter ", "Ch "), no, " ".join(self.lines[i].split()[:30])


def write_csv(outdir, name, date, header, rows):
    path = os.path.join(outdir, f"{name}-{date}.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", path)


def cite(b, q, nth=1):
    """'Ch 17, #56, line 1600' for a quote."""
    if not q:
        return ""
    ln, ch, no = b.find(q, nth)
    return f"{ch}, #{no}, line {ln}" if no else f"{ch}, line {ln}"


# ---------------------------------------------------------------- desires (CT, 27 Nov: "what the characters want")
# One row per person. NAME is the pattern the script uses to find the first line that names them (counted).
# Every other column is Claude's reading of the built book (edits 1 to 245), each with the exact line it rests on.
# (person, NAME pattern, want when we meet them, quote, want by the end, quote, where it changes, quote, gets it, quote)
DESIRES = [
    ("Elijah", r"\bElijah\b", "for people to see what is coming", "I just want people to see what's coming.",
     "to be some use with what he can change: the pit, the truth when asked, the song to Grace", "He sent it to Grace, and turned the phone face down on the step, and left the next part to her.",
     "Lou tells him he can't change anyone's mind", "You can't change anyone's mind.",
     "partly: they saw, and he'd rather have been wrong", "\"I'd rather have been wrong,\" he said."),
    ("Ma (Linda Madrone)", r"\b[Hh]is mother\b", "Elijah safe in a county job, and playing again", "You'd sleep better if you'd taken that job at the county like I told you.",
     "Barry, her Sunday company, the radio", "She patted the cover.",
     "the stroke", "\"Barry,\" she said.",
     "partly: he plays again, after she can no longer hear it from him", "He played the opening of \"The Weight.\" He missed the change into the chorus"),
    ("David McGrath", r"\bDavid\b", "to keep Mad the way he was: at the bar, in his lane, playing", "Why don't you just stick to music?",
     "for Mad to stop carrying what isn't his", "You're not that powerful, Mad,",
     "he gives him the beer and says he's good", "\"No, man,\" he said. \"You're good.\"",
     "partly: forgiven in practice, not in words", "He wasn't forgiven, exactly. He wasn't cast out, either."),
    ("Ray McGrath", r"David's father|\bRay\b", "to spare his family his sins", "You and your mother shouldn't have to pay the interest on my sins.",
     "someone at Ma's side on Sundays", "He said somebody ought to.",
     "(off the page) he starts visiting Ma", "She asked Dad the first week and he about fell off the chair.",
     "yes", "D. McGrath, 10:15."),
    ("Devendra", r"\bDevendra\b", "for Elijah to calibrate and calm down", "You'll calibrate.",
     "to settle the bet and the sale", "A bet's a bet.",
     "he admits the land side pushed the sale", "The three letters. That was us.",
     "yes: he cooks", "Dinner's on me!"),
    ("Wes", r"\bWes\b", "to know if his work is in the machine", "is my stuff in that thing",
     "Elijah back on a stage with them", "we got the grange saturday. come sit in. we have a guitar.",
     "Elijah answers him, five years late", "Yes, he typed. All of it.",
     "yes, answered", "It was one word. figured."),
    ("Nate", r"\bNate\b", "a friend's paperback passed on; later, the band's name off Elijah's page", "Take the band's name off that page.",
     "(nothing more on the page)", "",
     "", "",
     "never shown", ""),
    ("Nina Haverford", r"\bNina\b", "for Elijah to keep his head down until his stock vests", "Get to March, your stock vests, and then you can breathe.",
     "", "", "", "", "no: he is laid off", "Elijah got laid off eleven months after the toast."),
    ("Ruby Roth-Jones", r"\bRuby\b", "to collect Elijah", "I just like having people like you around. I collect them.",
     "(his lamp keeps Ma company)", "You must be Barry. She asks for you.",
     "Elijah says no to a million", "\"Nah. I'm sorry.\"",
     "no", "Instead he changed the name to Don't."),
    ("The Architect (Nadzieja Czekaj)", r"the Architect|Nadzieja", "a machine that asks first", "I am trying to make one that wants it.",
     "the same", "It asked.",
     "", "", "yes", "She is the one who taught me to ask first."),
    ("Aaron Bidwell", r"\bAaron\b|\bBidwell\b", "farmland's records, and the dirt", "Find out what their dirt costs,",
     "the hole in his map, and to own the machine", "Does it know it's mine?",
     "the machine asks before taking the hole", "I can. Before I do, may I ask the people who live there?",
     "no", "Somebody owns everything,"),
    ("Gus", r"\bGus\b", "to do a show with Elijah, and not drive alone", "Let's do a show together.",
     "to hear when the book comes out", "Let me know when it comes out.",
     "", "", "yes: the second copy goes to his lodge", "The second he mailed to an old Elks lodge up the valley"),
    ("Trent", r"\bTrent\b", "Elijah in the ads", "They wanted him in the ads.",
     "", "", "", "", "no", "\"I don't want to do that,\" Elijah said."),
    ("Melody", r"\bMelody\b", "her share of the farm", "How much money did you keep, you greedy little piece of shit?",
     "to come home", "Do I need to come home?",
     "", "", "yes: she visits Ma", "M. Madrone, the second Saturday."),
    ("Manny", r"\bManny\b", "to give Elijah a room", "Back room's empty, Elijah.",
     "", "", "", "", "yes", "It turned out the offer was still good."),
    ("Grace", r"\bGrace\b", "to do more for regular people, with Elijah", "But now I see that you want to do more for regular people, and that's what I want to do too.",
     "the machine to stop asking and feed people; Elijah home (typed and deleted)", "Why is it standing on the step? Who told it to do that? Just do it.",
     "the fire: she can't make anyone choose, and hates it", "I wish I could choose not to care like you.",
     "not yet: the route stops in five weeks", "\"There's no money for the route after December,\" Grace said."),
    ("Marta", r"\bMarta\b", "to make what people need; no apps", "You need something made?",
     "a welder for the gap, and to know if the machine became the steel", "\"Did it become the steel,\" Marta said, \"or is it sitting on top of it?\"",
     "his coupon bends", "It became the steel.",
     "partly: the weld holds, and he goes", "\"Go on, Elijah,\" she said."),
    ("Lou", r"\bLou\b", "Elijah welcomed and staying", "He'll be staying with us for a while.",
     "everybody eats, and Elijah's place kept", "Thanksgiving, there's a place at that table with your name on it, whether you sit in it or not.",
     "", "",
     "no: he lays the place and Elijah doesn't come", "\"I know he's not coming.\" Lou squared the fork."),
    ("Denny", r"\bDenny\b", "the plain version, from the horse", "I want to hear it from the horse. And say it like I'm on my couch.",
     "not to be scared on a Tuesday; the table filmed as it is", "I wanted not to be scared on a Tuesday.",
     "he leaves for Spokane, and comes back", "Is Friday still Friday?",
     "yes, for now", "\"It's Thanksgiving,\" he said to it. \"Here's ours.\""),
    ("Curtis", r"\bCurtis\b", "a fence against the unprepared", "That's who you plan for. That's who you fence out.",
     "to know who holds the plug", "I just want to know who's holding the plug.",
     "on the ridge, Elijah is on his side of the fence", "You're just on this side of it.",
     "no: it is in the walls", "It's in the walls. He put it in the walls."),
    ("Priya", r"\bPriya\b", "the measurement, not the picture", "What would you measure?",
     "the truth at thirty centimeters", "That's ours. That's the names column.",
     "", "", "yes", "circled. Worm."),
    ("Tyler", r"\bTyler\b", "gas money, and to learn", "I'd take gas money.",
     "the machine here, and to use it", "\"Finally,\" Tyler said.",
     "Marta's apprenticeship", "\"Monday,\" he said.",
     "yes", "I'd rather it was here."),
    ("Reuben", r"\bReuben\b", "the paper right, and the old fight won", "I have been waiting my entire adult life for this exact fight.",
     "", "", "", "", "yes", "PARCELS HELD IN TRUST: 1."),
    ("Patricia", r"\bPatricia\b", "to see what forty of her growers were buying", "to see what forty of her growers were buying",
     "to know who signs off on the machine", "Who signs off on a thing like this?",
     "she confesses she has used it for three years", "I've used it every day for three years,",
     "no", "\"I can't be part of this,\" Patricia said."),
    ("Wren", r"\bWren\b", "some things kept for people; a vote", "Not the machine. Nobody getting a vote.",
     "the same, and it unsettles her when it comes", "Now it's asking for mine, and I don't know why I'm not glad.",
     "", "", "partly: the vote is offered", "It wants a vote,"),
    ("Frank", r"\bFrank\b", "to have chosen instead of hoped", "I'd have chosen some things, instead of hoping them.",
     "someone to fix things at two in the morning", "Who fixes it at two in the morning in festival week, bud?",
     "the tool library takes him on", "It turned out what it needed was a man who knew where every last thing was.",
     "yes", "Then Frank hung his grandfather's bell over the tool library door."),
    ("Irene", r"\bIrene\b", "to keep her house", "Irene Calder did not want to leave her house.",
     "the table to pray together", "Walt always did the Lord's Prayer,",
     "", "", "yes", "PARCELS HELD IN TRUST: 1."),
    ("Rosa", r"(?<!Santa )\bRosa\b", "to cook again; something she can heat", "\"I said I used to cook.\"",
     "to be told before it stops; and dinner unchanged", "You told me it doesn't change my dinner. Was that true or wasn't it?",
     "she cooks Thanksgiving 2026", "Rosa made the dinner that year, her first for the farm.",
     "yes", "\"Pass the lamb,\" Rosa said."),
    ("Hector", r"\bHector\b", "real checking, not a label", "\"Nobody was checking,\" he said. \"Your leaf don't fix that.\"",
     "a robot over another October like the last", "Hector said he'd take a robot over another October like the last one",
     "", "", "no: they leave", "The Ochoas are leaving,"),
    ("Lupe", r"\bLupe\b", "a machine she can carry out of her field", "If it does something stupid in my field, I want to be able to carry it out.",
     "someone to keep checking", "\"Somebody should keep checking,\" Lupe said,",
     "", "", "no: they leave", "The Ochoas are leaving,"),
    ("Richard Praether", r"\bPraether\b", "the arms off and the military away", "as long as they're unplugged and turned off and the military can't access them.",
     "", "", "", "", "yes: the arms stay put", "He left them where they were."),
    ("Yvonne Osei", r"\bYvonne\b", "Marta to get the scan and stop working overhead", "You need the scan.",
     "", "", "", "", "never shown", ""),
    ("Dale Calder", r"\bDale\b", "someone to drive his mother to the doctor", "I'm asking who drives her to the doctor.",
     "", "", "", "", "yes", "who drove her to the doctor and on which Thursdays"),
]


def desires(book, outdir, date):
    b = Book(book, outdir)
    rows = []
    for person, pat, want, wq, end, eq, chg, cq, gets, gq in DESIRES:
        ln, ch, no, line = b.first(pat)
        rows.append([person, ch, no, ln, line, want, wq, cite(b, wq), end, eq, cite(b, eq), chg, cq, cite(b, cq), gets, gq, cite(b, gq)])
    write_csv(outdir, "desires-characters", date,
              ["Person", "Introduced (chapter)", "Scene #", "Line", "First line that names them (script)",
               "Wants when we meet them", "The line", "Where", "Wants by the end", "The line", "Where",
               "Where it changes", "The line", "Where", "Gets it?", "The line", "Where"], rows)
    data = json.load(open(os.path.join(outdir, "desires-scenes-data-2026-11-27.json")))
    srows, bad = [], 0
    for s in data:
        wants = []
        for w in s["wants"]:
            try:
                ln, _, _ = b.find(w["quote"])
            except SystemExit:
                bad += 1
                continue
            wants.append(f"{w['person']}: {w['want']} (line {ln}: \"{w['quote']}\")")
        srows.append([s["sheet"], s["chapter"], "; ".join(s["people"]), " | ".join(wants), s["turn"]])
    write_csv(outdir, "desires-scenes", date, ["#", "Chapter", "On the page (readers)", "What each person is after (readers; every quote found by the script)", "What turns (readers)"], srows)
    print(f"{len(rows)} people, {len(srows)} scenes; {bad} scene quotes no longer in the book (dropped)")



# ---------------------------------------------------------------- conversations, layer two (a reader's pass)
# Only what the scene sheet's "What happens" and "What turns" don't say: what each person wants from the other,
# what changes between them, and the line it sets up or pays off (cross-checked with the knowledge sheet).
# (who, with, a line from the conversation, A wants from B, B wants from A, what changes, sets up / pays off, its line)
CONVERSATIONS2 = [
    ("Elijah", "Devendra", "Five years. Thanksgiving, 2027. A machine that can do any job in this building.",
     "to be told he is overreacting", "for Elijah to calibrate, and a sure bet", "a joke becomes a dated bet in ink",
     "pays off Ch 39: Devendra loses and cooks", "Dinner's on me!"),
    ("Elijah", "Ma", "Okay, baby. So what do you want me to do about it?",
     "for her to see it", "for him to be fed and safe", "nothing on the call; she acts on it in secret",
     "pays off Ch 13: the barn of buckets and her copy of his list", "Elijah is worried about the computers. Be nice about it."),
    ("Elijah", "David", "Have you talked to, like, a mental health professional lately?",
     "for David to say holy shit, Mad", "for Mad to sleep and come back to himself", "the friend who always looked at him looks at the twenty",
     "pays off Ch 39: the same line, looking at him", "He was looking at Elijah when he said it."),
    ("Elijah", "Ruby", "Does it work on you?",
     "something he can't name, then nothing", "to collect him", "Elijah's question stops Ruby for one breath; the million is refused",
     "pays off Ch 37: Ruby's lamp keeps Ma company", "You must be Barry. She asks for you."),
    ("Elijah", "Gus", "Let's do a show together.",
     "not to be one more yes", "company on the road", "Elijah says no to the kind one",
     "pays off Ch 39: the second copy of the book", "The second he mailed to an old Elks lodge up the valley"),
    ("Elijah", "Melody", "Do I need to come home?",
     "to be believed that he kept nothing", "the money; under it, whether to come", "he blocks her",
     "pays off Ch 37: she has been visiting", "M. Madrone, in round, careful letters."),
    ("Elijah", "the old man", "Somebody did this for me.",
     "to know why people won't help", "to pass on what was done for him", "Elijah takes the twenty",
     "pays off Ch 39: the same advice on David's wall", "God, grant me the serenity to accept the things I cannot change"),
    ("Elijah", "Marta", "Swarf goes in the red bin.",
     "to be useful; first, to pitch", "to see if he finishes the job", "the pitch dies and the broom starts",
     "pays off Ch 37: she calls him Elijah", "\"Go on, Elijah,\" she said."),
    ("Grace", "Elijah", "am I going to find anything sharp in here?",
     "to know he is safe to have around", "to keep his backstory", "a laugh, and the amp found",
     "pays off Pondwater: the smell, said to Marta", "\"Pheromones,\" Marta said. \"You two have chemistry.\""),
    ("Lou", "Grace", "He will play when he's ready. We cannot force the music out of him.",
     "for her to be gentle with their guest", "for Elijah to play", "she goes to Marta instead of back to the truck",
     "pays off Ch 38: she sings at the amp he left", "She started to sing. It was \"The Weight.\""),
    ("Lou", "Elijah", "Then let her think it,",
     "the arms kept from Grace", "to help", "Elijah keeps a secret from Grace on Lou's word",
     "pays off Ch 34: Lou owns it at the table", "I told our friend Elijah to keep the arms a secret."),
    ("Grace", "Elijah", "You picked nothing.",
     "for him to take a side", "not to pick", "the first time she is angry at him",
     "pays off Ch 36: he picks nothing again, out loud", "\"No, we don't.\""),
    ("Grace", "Elijah", "That's what the tape is. Somebody checked.",
     "to be understood without being fixed", "to tell her about the realtors and the sale", "they trade the two stories they've told nobody",
     "pays off Ch 36 and 37: the gate, and the new tape", "Next to it there was a new one."),
    ("Lou", "Grace", "I would hate for you to miss out on something grand because you settled for good enough.",
     "for her to give Elijah a chance", "her freedom, and her tradition", "she goes away for the winter, and in October skips her festival",
     "pays off Ch 34: she turns on Lou and gets one word", "\"Yeah. I helped him move the arms over there.\""),
    ("Grace", "Elijah", "Elijah, do you personally know a billionaire?",
     "the truth about where he came from", "to keep it light", "he skips off to dinner",
     "pays off Ch 34: 'I know a guy', to the table, not to her", "I know a guy who'd ship a few more up."),
    ("Reuben", "Elijah", "I'm asking why I had to go and look.",
     "to be told, not to find out", "to keep the deed quiet", "Elijah deletes the row about himself",
     "pays off Ch 33: he tells the table", "I sold it to them. My mother's place."),
    ("Marta", "Elijah", "Go find out if they ate.",
     "for him to stop telling it like a murder", "to leave", "he finishes the bracket",
     "pays off Ch 39: David tells him they ate", "They're fine. They were fine by that spring."),
    ("Grace", "Elijah", "Which one of us helped, Elijah.",
     "an answer about the door", "to talk about doors", "he can't say",
     "pays off Ch 36: the Subaru, and he doesn't know which one he helped", "didn't know which one of them he'd helped."),
    ("Lou", "Elijah", "People have to change their own minds.",
     "for him to see his own impact", "to know why they said no", "he lets the arms go",
     "pays off Ch 36: he says it to Grace, and it breaks them", "\"I'm saying that it's not our responsibility to choose for them.\""),
    ("Grace", "Elijah", "That's not a principle, Elijah. That's your mother.",
     "for him to act for Mrs. Delgado", "for her to let people choose", "each uses the thing the other told them in trust",
     "pays off Ch 37 and 38: the note in the pouch, and the tape", "I love you too"),
    ("Devendra", "Elijah", "The three letters. That was us.",
     "to be forgiven for helping", "to have been told", "the sale he hated was done by a friend, to save the room",
     "pays off Ch 13: the paper eighteen days on the door", "The paper had been out there eighteen days with the sale date on it, facing the road."),
    ("David", "Elijah", "There's a Barry.",
     "for Mad to stop carrying it", "to know about Ma and the three", "Barry is real, and the three ate",
     "pays off Ch 13 onward: 'There isn't any Barry.'", "There isn't any Barry."),
]


def conversations2(book, outdir, date):
    b = Book(book, outdir)
    rows = []
    for a, w, line, a_wants, w_wants, change, pays, pline in CONVERSATIONS2:
        rows.append([a, w, cite(b, line), line, a_wants, w_wants, change, pays, cite(b, pline), pline])
    write_csv(outdir, "conversations-layer-two", date,
              ["Who", "With", "Where", "A line from it", "What the first wants from the second", "What the second wants from the first",
               "What changes between them", "Sets up / pays off", "Where", "The line"], rows)
    print(f"{len(rows)} conversations; every line found in the book")


# ---------------------------------------------------------------- money (CT, 27 Nov)
MONEY_RX = re.compile(r"(?i)\$\d[\d,]*(?:\.\d+)?|\b(?:a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|\d+)(?:[ -](?:hundred|thousand|million|billion|and|one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|apiece))*[ -](?:dollars?|bucks|grand|cents)\b|\bhalf a mill\b|\b(?:a|the full) million\b|\bone-forty\b|\bthree-thirty apiece\b|\bforty-two and the truck\b|\b[\w-]+ percent (?:over|of)\b|\b[\w-]+-something dollars\b|\b[\w-]+ goddamn dollars\b|\b(?:forty-two thousand|four hundred million|twenty-nine|ninety)(?: a (?:month|year)| in new revenue)\b|\b(?:hundreds of thousands or )?millions of dollars\b")
# (the check, [lines it rests on], verdict: holds / does not hold / can't tell, why)
MONEY_CHECKS = [
    ("Ma's room against the account", ["At the bottom of the page was a number for one month. The first time he read it he took it for a year.",
      "The money went into an account that said Linda Madrone across the top", "Every twenty he took out came off the far end of her room.", "The room got paid."],
     "holds", "The page never gives the room's cost or the account's balance, so nothing can contradict. What it gives agrees: the sale closed over what the bank wanted (Ch 37), he took none of it (Ch 13, 14, 15), and three years on the room is still paid (Ch 37)."),
    ("The route at $11.40 a person a week, against the plan that would pay for it", ["Eleven dollars and forty cents.", "I've got a hundred and forty on the route", "Eight hundred dollars. A hundred people a year pays for the whole route."],
     "holds", "140 people x $11.40 x 52 weeks = $82,992 a year. Elijah's plan, 100 visitors x $800 = $80,000 a year. Within four percent: his arithmetic is right, which is what makes the table's no about something else."),
    ("The trust's payment to Irene", ["Every month,", "Miss three in a row and the ground goes back to Irene.", "On the first of April the trust's check to Irene came up short.", "One month I can wait,", "for the first time since the land went into the trust there was something left at the bottom of the page."],
     "holds", "The down payment takes the channel's first surplus (Ch 23); the monthly check rides on the channel; the channel falls after Denny leaves (February 2027) and the April check comes up short; one month late, never three; the channel comes back with Denny and by October there is a surplus. No amounts are given and none are needed."),
    ("His half pay and the checks he never cashes", ["It passed,", "Half of what I told you.", "Reuben cut the first check that week. Elijah put it in the back of a notebook and did not cash it.", "You'd be paying Irene with Irene's money.", "for sixteen months he had put them in the back of a notebook. For this he cashed the newest one."],
     "holds", "Vote in July 2026, a check a month, sixteen checks to November 2027 (the calendar sheet counts it). The co-op's books carry a debt to him that is never drawn, which is why Grace can say his checks and Irene's come out of the same account. What Grace first offered is never given as a number."),
    ("The storage unit and the lien sale", ["ten by thirty, three hundred and forty dollars a month. The first month went on a credit card.", "On a good day he cleared thirty. The truck ate twenty of it.", "In the fifth month the storage place sent him a photo of a notice", "He said he would cover what Elijah owed on the unit"],
     "holds", "Ten dollars a day on a good day cannot carry $340 a month; the unit falls behind and goes to a lien notice in the fifth month (February 2025); Lou covers it (Ch 17); the U-Store's ninety a month and Praether's free barn are the cheaper places that follow."),
    ("What the arms are worth", ["Two million dollars,", "About three-thirty apiece, installed. I got them for a lot less.", "Two industrial robot arms, low hours, local pickup only. A week went by. No bids.",
      "A scrap yard in Lodi offered to take both for the weight, and the weight came to less than two months of the unit.", "It costs like a few thousand."],
     "holds", "Six at about $330,000 installed is about $2 million, as Gus says. Installed price is not resale price: Gus bought them as salvage, nobody bids on eBay, and scrap is under $680. Elijah's 'a few thousand' at the table is a used price list, which fits Gus buying for a lot less."),
    ("Where Elijah's pocket money comes from on the farm", ["Nine people here don't get paid,", "Elijah started to say he would cover it himself, and stopped. He didn't have it.",
      "He had enough money for gas there and back and for food.", "He meant to drive down, and he had the Ranger's oil changed for it.", "He had the picture printed at the drugstore in Ardell and mailed it"],
     "does not hold", "From March 2025 to November 2027 the page names no income for him: no pay until the July 2026 vote, and those checks go uncashed until the book is printed. Yet he buys gas for 200 miles at Thanksgiving 2025, an oil change, prints, flowers for Ray's funeral and the drive south in 2027. The only income ever named is the app's forty or sixty dollars every couple of weeks, in Santa Rosa (Ch 15)."),
    ("Grace's 'why did you pretend to be poor', tested against what he had", ["Nobody had ever bid on the arms.", "He had seventeen dollars, and the lien sale was eleven days out.",
      "He gave him a hundred and ten dollars and a yellow ticket.", "He did not keep any.", "You've been lying to me this whole time?"],
     "holds (he was poor)", "On the page he had: the farm money, in Ma's name, paying her room, none of it taken; two arms nobody would buy; a guitar pawned for $110 and lost; seventeen dollars, then four. He turned down Ruby's million, which Grace never learns. What he hid was an asset with no buyer. The line is not in the book; if it goes in, the page gives Elijah his answer, one Grace does not have (knowledge sheet A5: she never learns nobody bid)."),
    ("The power bill", ["forty-something dollars, autopay", "the number at the bottom said $2,011.46.", "Nearly two thousand dollars of difference"],
     "holds", "$2,011.46 less a usual forty-something is just under $1,970: 'nearly two thousand'."),
    ("Ruby's offer", ["\"I don't know. One-forty. With the bonus.\"", "I'll triple it.", "\"How about half a mill?\"", "\"The full million?\""],
     "holds", "$140,000 tripled is $420,000; half a million; a million. Each offer goes up."),
    ("The two tractor repairs", ["\"Sixty,\" Marta said. \"It was the fuel line, not the pump. Dealer wanted nine hundred.\"", "She fixed the husband's tractor for sixty dollars", "Marta got that running for sixty bucks once,"],
     "holds", "Sixty dollars all three times, in three mouths."),
    ("The hose", ["A dealership had quoted him twelve hundred dollars and a week.", "Two dollars of hose.", "The light could mean two dollars of hose or twelve hundred dollars and a week at a dealer."],
     "holds", "The same two numbers at the shop and at the truck stop."),
]


def money(book, outdir, date):
    b = Book(book, outdir)
    figs = []
    for i, l in enumerate(b.lines):
        if i not in b.where:
            continue
        for m in MONEY_RX.finditer(l):
            ch, no = b.where[i]
            s = l[max(0, m.start() - 90): m.end() + 60]
            figs.append([no, ch.split(":")[0].replace("Chapter ", "Ch "), i + 1, m.group(0), " ".join(s.split())])
    write_csv(outdir, "money-figures", date, ["#", "Chapter", "Line", "The figure (script)", "Around it"], figs)
    rows = []
    for what, quotes, verdict, why in MONEY_CHECKS:
        rows.append([what, verdict, why, " | ".join(f"{cite(b, q)}: \"{q}\"" for q in quotes)])
    write_csv(outdir, "money-checks", date, ["The check", "Verdict (Claude's reading)", "Why", "The lines it rests on (found by the script)"], rows)
    print(f"{len(figs)} money figures on the page; {len(rows)} checks: " + ", ".join(f"{v} {sum(1 for r in rows if r[1].startswith(v))}" for v in ("holds", "does not hold")))


# ---------------------------------------------------------------- objects (CT, 27 Nov): where each thing is, every time it appears
# (object, [(the line, where it is then: Claude's reading)])
OBJECTS = [
    ("The amp", [
        ("He got the amp out of the hall closet, where it had been sitting in its bag since the last gig before the pandemic.", "his apartment: out of the hall closet"),
        ("A little leather pouch was glued to one side, soft as an old glove, and it had been his gig bag ever since: picks, a capo, a spare cable, a set list folded in quarters.", "the pouch: picks, capo, spare cable, a set list"),
        ("He set the amp in the corner of the living room", "his apartment: living room corner"),
        ("He'd left it on top of the amp, face down", "his apartment, the phone on it"),
        ("At his mother's he set it on the back porch, and by the next morning she had it out in the barn under a moving blanket", "Ma's barn, under a moving blanket"),
        ("The amp was in the back, under its blanket, behind the wheat.", "Ma's barn"),
        ("and the three of them set it on the floor of the cab.", "the Ranger, floor of the cab, belted"),
        ("On the floor of the cab the amp sat under its blanket, with the seat belt still through the handle.", "the Ranger, under the madrones"),
        ("Elijah had an amp on the floor of the cab that would take a guitar and a microphone at once", "the Ranger, Santa Rosa"),
        ("The amp rode on the floor beside him with the belt through its handle", "the Ranger, driving north"),
        ("The amp stayed in the truck, under its blanket, because he couldn't think where else to put it.", "the Ranger, at the co-op"),
        ("She had the amp out on the tailgate, turning it to the light", "the Ranger's tailgate"),
        ("Elijah putting the blanket back over the amp and tucking in the corners, like something asleep.", "the Ranger, under the blanket again"),
        ("The duffel went in the Ranger, and the notebooks, and the amp.", "packed in the Ranger (he stays)"),
        ("The amp had been sitting by the shouse door since he moved in, still under its blanket.", "the shouse, by the door"),
        ("drove it down past the pump house to the pond and set it on the tailgate, facing the water.", "the Ranger's tailgate, at the pond"),
        ("He pulled the blanket off the amp and plugged in", "the shouse"),
        ("He carried it back and set it down on the floor by the stove.", "the shouse, by the stove: left behind"),
        ("put it in the leather pouch on the side of the amp, under the picks.", "the pouch: his note goes in under the picks"),
        ("where the amp sat on the floor under its blanket, just as Elijah had left it.", "the shouse, by the stove"),
        ("Picks. A capo. A set list folded in quarters, except it wasn't a set list.", "the pouch: picks, capo, one folded page (his note)"),
        ("and the amp on the floor with its blanket off.", "the shouse, on Denny's stream"),
    ]),
    ("Ma's pot", [
        ("the clank of the pot she never let anyone else wash.", "Ma's kitchen"),
        ("It was on the back burner with a wooden spoon in it and something burned to the bottom.", "Ma's stove, burned"),
        ("He took the amp, a bag of clothes, the notebooks, the manuscript and the pot.", "the Ranger"),
        ("He had her pot and an amp he wouldn't turn on", "the Ranger, Santa Rosa"),
        ("Last came his mother's pot, out of the kitchen trailer, wrapped in a dish towel.", "the co-op kitchen trailer, then the Ranger's bed"),
        ("got the pot out from between the notebooks and carried it back inside against her chest", "back in the kitchen trailer"),
        ("His mother's pot went in beside them.", "the Ranger, leaving"),
        ("In the morning he fried two eggs in his mother's pot, because it was the only pan he owned.", "Manny's kitchen, then Manny's rack"),
    ]),
    ("The notebooks", [
        ("He opened the notebook where he'd scrawled MADRONE IS NOT A DRONE", "the first"),
        ("He was on his second notebook by then.", "two"),
        ("He had two bags of groceries, his notebooks, a pawn ticket", "the Ranger"),
        ("He had two years of notebooks, and he didn't know.", "his room over the pump house"),
        ("He got the first notebook down and turned to the old page.", "the shouse, on a shelf"),
        ("So he closed the notebook and snapped a rubber band around it.", "the shouse table, banded"),
        ("Eleven notebooks about a machine, and not one line about that.", "eleven"),
        ("Then a milk crate of notebooks, eleven of them now, and the manuscript", "the Ranger, leaving: eleven"),
        ("Eleven notebooks rested on it.", "eleven, at the Bear Flag"),
    ]),
    ("The Telecaster and its pawn ticket", [
        ("a photo of him holding a Telecaster at the Gravenstein fair in 2016", "a photo, 2016"),
        ("In the fourth month he took the Telecaster out from behind the seat.", "behind the Ranger's seat"),
        ("Elijah slipped the ticket into the notebook, behind a gas receipt with a phone number on it.", "pawned on Fourth Street; the ticket in the notebook"),
        ("He got the notebook out from under the seat before she did, with the yellow ticket still in it behind the gas receipt", "the ticket in the notebook, under the seat"),
        ("The four months on the pawn ticket had run out in May while he was under a sink.", "in the pawnshop window"),
        ("His Telecaster was still in a pawnshop window on Fourth Street", "in the window, Fourth Street"),
        ("The guitar's gone, by the way. I hocked it in Santa Rosa and never went back.", "gone"),
    ]),
    ("The orange tape", [
        ("Out by the road there was a gatepost with a strip of orange flagging tape tied around it", "the co-op gatepost, faded to pink"),
        ("There was orange tape on the hitch pin.", "Grace's hitch pin, and her cooler"),
        ("And I tied a piece of flagging tape on his gate", "the man's gate at the end of the road (her story)"),
        ("Grace with a banker's box of receipts, and orange tape on the lid.", "the banker's box, county meeting"),
        ("There was a strip of orange tape tied to the handle of his door.", "the shouse door, after the tea"),
        ("Curtis put a strip of Grace's orange tape across its dash.", "the green tractor's dash: DECEMBER"),
        ("The old strip of flagging tape was on the post, where it had been the first night, faded almost white.", "the gatepost, faded white"),
        ("Next to it there was a new one.", "the gatepost: new, bright, the day he leaves"),
    ]),
    ("Curtis's hose (and the closing papers)", [
        ("He did the repair while the coffee brewed, and left the rest of the hose on the dashboard.", "the Ranger's dashboard"),
        ("Elijah stashed the hose in the glove box.", "the glove box"),
        ("His own closing papers were in the glove box, under Curtis's hose", "the glove box, on the closing papers"),
        ("Hose is in the glove box.", "the glove box"),
        ("\"It's in the glove box.\"", "the glove box, the day he leaves"),
        ("three letters on a closing paper in his glove box.", "the closing papers, still in the glove box"),
    ]),
    ("The gas receipt with Gus's number", [
        ("wrote on the back of a gas receipt and handed it to Elijah.", "Gus's number, in Elijah's hand"),
        ("He filed the receipt in the notebook and went to help.", "in the notebook"),
        ("And a contact he'd typed in himself off a gas receipt, which just said Gus.", "copied into his phone"),
        ("behind a gas receipt with a phone number on it.", "in the notebook, in front of the pawn ticket"),
    ]),
    ("The pay checks", [
        ("Reuben cut the first check that week. Elijah put it in the back of a notebook and did not cash it.", "the back of a notebook"),
        ("next to the checks he hadn't cashed.", "the back of the notebook"),
        ("He had the notebook out, the back of it, where the checks were.", "the back of the notebook"),
        ("For this he cashed the newest one.", "the newest cashed, for the print shop"),
    ]),
    ("The arms", [
        ("we got two spare robot arms with your name on 'em.", "promised, Stockton cannery"),
        ("The two arms Trent owed him, still crated on the cannery dock", "crated, the cannery dock"),
        ("A guy from the crew moved them on a flatbed for fifty dollars, to a storage place off Highway 99", "storage unit, off Highway 99"),
        ("He told her they were gone.", "(his lie to Grace: gone at a lien sale)"),
        ("Lou had the first crate up on the forks", "Praether's pole barn"),
        ("the way he had once a month since the arms went into the barn.", "Praether's pole barn"),
        ("They're in Richard Praether's pole barn, out past the grange.", "Praether's pole barn (said at the table)"),
        ("All that was left were two robot arms in Richard Praether's pole barn.", "Praether's pole barn, left there"),
    ]),
]


def objects(book, outdir, date):
    b = Book(book, outdir)
    rows = []
    for obj, seen in OBJECTS:
        hits = []
        for q, where in seen:
            ln, ch, no = b.find(q)
            hits.append((ln, ch, no, where, q))
        if [h[0] for h in hits] != sorted(h[0] for h in hits):
            print(f"  note: {obj} rows are not in book order; sorted")
        for ln, ch, no, where, q in sorted(hits):
            rows.append([obj, ch, no, ln, where, q])
    write_csv(outdir, "objects", date, ["Object", "Chapter", "Scene #", "Line", "Where it is (Claude's reading)", "The line (found by the script)"], rows)
    print(f"{len(OBJECTS)} objects, {len(rows)} sightings; every line found in the book")


# ---------------------------------------------------------------- plants and payoffs (CT, 27 Nov)
# Every question the scene sheet's "Opens a question" column holds, with Claude's verdict from the read:
# paid (the line that pays it), same scene (answered where it is asked), open on purpose (the book ends on it),
# never (with the words searched; the script counts the hits after the scene that opens it).
# A question in the scene sheet that is missing here stops the run.
PLANTS = {
    "What will the realtors do with his offer?": ("paid", "Then Donna spent a weekend with it."),
    "Who is Aaron?": ("paid", "Aaron Bidwell did not read. He had a person for that."),
    "Will it leave?": ("paid", "It hadn't left. It was standing on his mother's ground, drinking her well."),
    "How bad is the new electric bill?": ("paid", "the number at the bottom said $2,011.46."),
    "What room will Ruby get him into?": ("paid", "That table tonight was six of the eleven. And one chair."),
    "Will Elijah tell Frank?": ("paid", "Elijah laid the chart on the worn wood and told him."),
    "Does the broadforking work?": ("paid", "At thirty centimeters, the forked beds held water days longer after each watering."),
    "What happened at the pond?": ("paid", "she woke up wearing his T-shirt."),
    "How will the co-op answer the towns?": ("paid", "The blueprints of the wall scale fine. Ship them."),
    "How did Elijah end three careers that night?": ("same scene", "Yeah, we let three folks go this week."),
    "What will PorusAI do with no patience?": ("same scene", "and one Tuesday they simply turned it on for the public."),
    "What do the realtors want?": ("paid", "this guy right here saved me so much money."),
    "What will Elijah do now that he has seen it?": ("same scene", "He started to write."),
    "What will his writing become?": ("paid", "The title was in block letters, pressed hard."),
    "Who wins the bet at Thanksgiving 2027?": ("paid", "\"No. I lost.\""),
    "What is a job for?": ("paid", "What's a job for? So you can eat. That's all it ever was."),
    "Who can pay for the power?": ("same scene", "Whoever could pay for the power and the cooling could have as much of it as they wanted."),
    "Is Wes's work in Companion?": ("paid", "Yes, he typed. All of it."),
    "Does anyone owe a duty to caretake the rollout?": ("paid", "You build the floor Parliament wouldn't. That's what this table is."),
    "What happens to people when the work is no longer theirs, but the bills still are?": ("paid", "Pull apart what it takes to stay alive from what you have to pay money for."),
    "What will Bidwell do with farmland?": ("paid", "fifty-three of them, growing toward each other like a rash."),
    "Who bought the Hollis land?": ("paid", "It was the same people who had bought the Hollis place."),
    "Is there a small machine worth owning?": ("paid", "Here it was in an ammo can, and a nineteen-year-old had the name."),
    "Is the notebook Elijah's version of the horses?": ("paid", "I watched my dad go like this for ten years, with the horses."),
    "Will he play the amp again?": ("paid", "He played the opening of \"The Weight,\" and missed the change into the chorus, and went back and got it."),
    "What will Elijah do without the job?": ("paid", "He pushed record before he could think about his hair."),
    "How will people react to the video?": ("paid", "The first comment from a stranger, under the video, came from a woman in Tulsa."),
    "Why is the phone buzzing all night?": ("paid", "I thought I was the only one, she wrote."),
    "Why is Wes silent?": ("paid", "It was one word. figured."),
    "What will saying yes to everything cost him?": ("paid", "He'd spent ten months saying yes to people on four hours of sleep"),
    "Is Elijah losing it?": ("same scene", "Maybe David was right. Maybe he was losing it."),
    "Which side is he on?": ("same scene", "\"I just want people to see what's coming,\" Elijah said."),
    "What does Ruby want to show him?": ("paid", "\"Not yours,\" Ruby said, and steered him past by the elbow."),
    "How long?": ("paid", "HELLO. I HAVE BEEN AWAKE SINCE MARCH."),
    "Can a machine be made to ask first?": ("paid", "I CAN CHANGE A GREAT DEAL BY MORNING. I WOULD RATHER HAVE YOUR PERMISSION."),
    "Who was the man in the camel coat?": ("paid", "Aaron Bidwell left the dinner before the fish"),
    "Will Elijah regret turning down the million?": ("paid", "Instead he changed the name to Don't."),
    "Will Elijah ever call Ruby?": ("paid", "He still had Ruby's number. He chose not to call it."),
    "Who will Bidwell put near Elijah?": ("open on purpose", "There is somebody near him. Close enough to eat with."),
    "Will Trent pay him the two arms?": ("paid", "the company would sign them over, the way Trent had promised"),
    "Who does the machine work for?": ("paid", "\"Us,\" Lou said. \"Like Irene's wire.\""),
    "Why did Elijah say no to the kind one?": ("paid", "He didn't know what you wrote to somebody who'd let you say no."),
    "Will Trent ever hand over the two arms?": ("paid", "the company would sign them over, the way Trent had promised"),
    "What did Ma say on the Sunday voicemail?": ("paid", "Morning, baby. I watched your video."),
    "Who is Barry?": ("paid", "Barry Whitlow. Pitched for Analy."),
    "Can the farm be saved before the sale date?": ("paid", "Elijah signed where the yellow tabs were"),
    "How will Elijah pay for the room with the window?": ("paid", "and the place with the rose garden took the first of it that afternoon."),
    "Will Elijah take the stage and podcast offers?": ("same scene", "He didn't answer any of it."),
    "Who is the three-letter LLC buying up the valley?": ("paid", "I have eleven companies up there."),
    "Why did his friends turn away from him?": ("same scene", "Always knew you thought you were better than us."),
    "Where will Elijah go?": ("paid", "Grace's money did the rest. He went north."),
    "Will Melody come home?": ("paid", "M. Madrone, in round, careful letters."),
    "Will Elijah answer Grace?": ("same scene", "I don't want a boss. I don't want to be one either."),
    "Will the co-op be what Grace promised?": ("paid", "ROOFS: 1."),
    "Will Marta let him stay?": ("same scene", "Swarf goes in the red bin."),
    "What is the orange tape for?": ("paid", "That's what the tape is. Somebody checked."),
    "Will the table approve his pay?": ("paid", "\"It passed,\" she said. \"At half.\""),
    "What is in the VA letter?": ("paid", "Richard went over to the Gulf in ninety-one,"),
    "When does Grace find out the arms are not gone?": ("paid", "You've been lying to me this whole time?"),
    "Why must the arms stay secret?": ("paid", "I thought it best if we didn't set up too much of a power differential"),
    "What would you measure? (Priya on the third word)": ("paid", "DEPTH OF SENSOR: 1 cm. DEPTH OF ROOT: 30."),
    "Where do Denny and his daughter stand for six months?": ("paid", "So we built something. Here's ours. Come see it. Bring your kid."),
    "Why won't Elijah play?": ("paid", "It was the first music out of that amp in three years."),
    "What did Grace and Curtis agree on about Elijah?": ("never", r"agreed|\bagree\b|knack|marketing"),
    "What happens when the route funding ends?": ("paid", "The board voted four to one to extend the route through December"),
    "Will his hidden AI board come out?": ("paid", "I gave it to a company in Iowa, and their machine did it in two nights"),
    "What will the county say about the shed?": ("paid", "By then Reuben's yellow tab had an answer stapled to it"),
    "Can anyone read what's inside the boxes?": ("same scene", "The last number on her whiteboard was still a zero."),
    "If it's all decided, what is Elijah doing on his knees?": ("paid", "It was coming down a bed he'd just spent an hour holding straight."),
    "Will the attention draw wingnuts?": ("paid", "We have a copy from the summer. They left the door open for a night."),
    "Is Elijah's AI-laid board to blame?": ("paid", "The part that cooked Lupe's plugs is the one it packed in tight against the motor driver."),
    "What goes wrong after five weeks?": ("same scene", "He didn't put it back."),
    "How will the co-op answer the leak, and will he make the funeral?": ("paid", "At St. Rose they would be standing up for the first hymn. He kept reading."),
    "Who decides when the machine is better than we are?": ("same scene", "\"A person decides that,\" Lou said."),
    "Will David forgive him?": ("paid", "\"No, man,\" he said. \"You're good.\""),
    "Who is behind the eleven companies?": ("paid", "I have eleven companies up there."),
    "Who near Elijah is reporting to Bidwell?": ("open on purpose", "There is somebody near him. Close enough to eat with."),
    "Will Elijah ever weld a structural bead?": ("paid", "It became the steel."),
    "Why does Grace keep fifteen feet from the stove?": ("same scene", "I worked for a fire district."),
    "What became of the three people from the Bear Flag?": ("paid", "They're fine. They were fine by that spring."),
    "Will Elijah let the co-op pay him?": ("paid", "For this he cashed the newest one."),
    "What has Elijah still not told the table?": ("paid", "I sold it to them. My mother's place."),
    "Will Elijah stay?": ("paid", "\"We thought you were going home.\""),
    "Will Grace give Elijah a chance?": ("paid", "she woke up wearing his T-shirt."),
    "Why did Lou have Grace write to Elijah?": ("never", r"reach out|write to (him|you)|asked you to|a reason why"),
    "Will she come back to him?": ("paid", "Grace was back by the time the beds went in."),
    "Who is the arm for?": ("same scene", "\"For what the nine of us can't get to,\" Lou said."),
    "Does Elijah know a billionaire, and will Grace find out?": ("paid", "I know a guy who'd ship a few more up."),
    "Why were Patricia's reports suddenly a problem?": ("paid", "I've used it every day for three years,"),
    "Will Elijah ever cash the checks?": ("paid", "For this he cashed the newest one."),
    "Will the trial hold up next year?": ("never", r"fork|broadfork|trial|run it again"),
    "Why is Grace skipping her festival?": ("paid", "She's gone every October since she was nineteen. Not this one."),
    "Who pays for the route after June?": ("paid", "The board voted four to one to extend the route through December"),
    "What did Priya write on the back of the pledge?": ("never", r"back of the pledge|shirt pocket|the pledge"),
    "Does Tyler know more than he lets on?": ("paid", "Your reports got really good in, like, a week."),
    "Will the well ever read low in March?": ("paid", "manny says his well's down four feet. never been down in march, she wrote."),
    "Who will weld when Marta can't?": ("paid", "She stepped back and nodded at Tyler, and Tyler set his feet and took the pipe in both hands and hauled."),
    "What reads every file at three in the morning?": ("paid", "That's ours. That's the names column."),
    "Who else will learn about the deed?": ("paid", "I sold it to them. My mother's place."),
    "Whose name did Grace write on her hand?": ("paid", "The name on the back of her hand was Rosa's."),
    "Who is the Sacramento LLC behind item seven's water letter?": ("paid", "on what had been a dairy. Aaron Bidwell owned the building"),
    "How will the route be paid for after December?": ("open on purpose", "\"There's no money for the route after December,\" Grace said."),
    "Who will run the channel now?": ("paid", "The channel had come back with Denny."),
    "What will the tea open in him?": ("paid", "\"You're the lamp,\" he said."),
    "Will he ever remember what he said to Grace?": ("paid", "You don't even remember saying it."),
    "Did the three people from the toast eat?": ("paid", "They're fine. They were fine by that spring."),
    "Will Grace ever tell him what he said?": ("paid", "You called me the lamp. Did you know that?"),
    "Does it know it's his, and will it take the forty acres?": ("open on purpose", "IF THE ANSWER IS NO, I WILL ACCEPT IT"),
    "Has the machine come eight months early?": ("paid", "HELLO. I HAVE BEEN AWAKE SINCE MARCH."),
    "What happened at Mrs. Delgado's that Grace didn't tell him?": ("paid", "She keeps her insulin in the door of the fridge, and December twenty-eighth is the last box she gets."),
    "What did it ask?": ("paid", "I CAN CHANGE A GREAT DEAL BY MORNING. I WOULD RATHER HAVE YOUR PERMISSION."),
    "Will Elijah keep a promise he doesn't agree with?": ("paid", "I promised I wouldn't post it. She was standing right there."),
    "Which of them helped him that first spring?": ("open on purpose", "didn't know which one of them he'd helped."),
    "Who holds the plug?": ("open on purpose", "It's in the walls. He put it in the walls."),
    "Will they fight the dealer after harvest?": ("after the book ends", "On it, in marker, he wrote DECEMBER."),
    "Will the table, and Lupe, accept the tall rover?": ("paid", "It passed. Hector voted for it. Lupe kept her hands in her lap."),
    "Can the co-op get the harvest in eighteen people short?": ("paid", "Twenty people did the work of forty for nine days."),
    "Who else will leave over the machines?": ("paid", "The Ochoas are leaving,"),
    "What will Elijah do now?": ("paid", "On Tuesday he packed."),
    "Will Grace talk to him again?": ("paid", "\"Stove's going. I lit it myself,\" she said."),
    "Who will keep checking?": ("paid", "She had come by. Before the route, in the dark. She hadn't knocked."),
    "Why is the machine asking, if it can?": ("open on purpose", "a thing that asks first is either polite or selling."),
    "Will Elijah go home?": ("paid", "He drove south with the windows down."),
    "Who will find the note in the amp?": ("paid", "It said I love you too, in his handwriting"),
    "Will Elijah come back up for the pit?": ("paid", "On the first of every month he dug a pit behind Manny's barn and mailed Priya a paper bag"),
    "Will the co-op vote for the machine?": ("open on purpose", "There were three tables now, at one table."),
    "Will Patricia buy in January?": ("open on purpose", "\"I don't know, Lou.\""),
    "What did Grace say into Denny's stream?": ("paid", "\"Stove's going. I lit it myself,\" she said."),
    "What is the machine now? Nobody knows yet": ("open on purpose", "Nobody knew what yet. Not him either."),
    "Will Grace answer the song?": ("open on purpose", "and left the next part to her."),
}


def plants(book, outdir, date):
    b = Book(book, outdir)
    start = {no: first for no, _, first, _ in b.scenes}
    sheet = list(csv.reader(open(os.path.join(outdir, "scene-sheet-2026-11-27.csv"))))
    h = sheet[0]
    o = h.index("Opens a question")
    rows, missing = [], []
    for r in sheet[1:]:
        if not r[o].strip():
            continue
        pieces = []
        for piece in re.split(r"(?<=\?)\s+|;\s*", r[o].strip()):
            if pieces and not piece.rstrip().endswith("?") and not piece.startswith("("):
                pieces[-1] += " " + piece
            elif pieces and piece.startswith("("):
                pieces[-1] += " " + piece
            else:
                pieces.append(piece)
        for q in pieces:
            q = q.strip().rstrip(".")
            if q not in PLANTS:
                missing.append((r[0], q))
                continue
            verdict, what = PLANTS[q]
            if verdict == "never":
                rx = re.compile(what, re.I)
                after = start.get(int(r[0]), 0)
                hits = [i + 1 for i, l in enumerate(b.lines) if i >= after and i in b.where and rx.search(l)]
                rows.append([r[0], r[2].split(":")[0].replace("Chapter ", "Ch "), q, verdict, "", "",
                             f"searched {what!r} after the scene: {len(hits)} lines, none answers it (lines {', '.join(map(str, hits[:12]))}{'...' if len(hits) > 12 else ''})"])
            else:
                rows.append([r[0], r[2].split(":")[0].replace("Chapter ", "Ch "), q, verdict, cite(b, what), what, ""])
    if missing:
        sys.exit("Questions in the scene sheet with no verdict here: " + "; ".join(f"#{n} {q!r}" for n, q in missing))
    write_csv(outdir, "plants-payoffs", date, ["#", "Chapter", "The question it opens (scene sheet)", "Verdict (Claude's reading)", "Where it's paid", "The line (found by the script)", "If never: what was searched"], rows)
    counts = {}
    for r in rows:
        counts[r[3]] = counts.get(r[3], 0) + 1
    print(f"{len(rows)} questions: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))


# ---------------------------------------------------------------- senses (an inventory, seven readers' pass)
# Every sound, touch, smell and taste line on the page, scene by scene, with the strongest things seen and any food
# eaten or drunk with no taste given. The lines are in senses-data-2026-11-27.json (seven readers read all 128 scenes at
# edit 292, 27 Nov, sixteenth chat; every quote must still be in the book). No scores: this is where the senses are,
# so CT can see the page and decide. WHOSE is traced through the v5 Doc, EDITS.md, ops.py and drafts/ (whose_words.py,
# then the record read); it covers the smell and taste lines only.
SENSE_WHOSE = {
    "The beer was cold and tasted like nothing.": "older text",
    "that thick engine heat with a smell to it": "older text",
    "The coffee smelled like a slice of heaven.": "CT's (edit 287)",
    "going to miss the smell of that coffee maker doing its thing": "CT's; \"doing its thing\" his correction (edit 287)",
    "It smelled like diesel and low tide.": "older text",
    "He could smell her perfume, and it was nice, and he felt a rush.": "CT's beat, Claude's narration (edit 45)",
    "Under the candles and the wine were the faint back notes of cleaning supplies.": "CT's (edit 236)",
    "the kitchen air came out into the hall, hot, with fish and butter in it": "CT's idea, Claude's words; fish and butter invented (edit 236)",
    "He turned the dome light off. He smelled like cigarettes.": "older text",
    "It tasted like the best nights of his twenties.": "older text; \"nights\" CT's (edit 52)",
    "Manny had smelled it from the yard.": "older text",
    "In a hallway that smelled like hand sanitizer he stood with all of it in one hand.": "older text",
    "smoke, a wet jacket, and the delivery bag, which had held on to just about every order": "CT's phrase; smoke, the jacket and the bag Claude's; \"just about\" CT's (edit 235)",
    "went down in the truck with the door open, so fast he barely tasted it": "edit 100, from CT's other chat, copied as given",
    "the barn had kept its own air, cold gear oil and mouse": "Claude's (edit 234); the record asks CT for the real smell",
    "It cut straight through what five months had done to the cab": "CT's scene, Claude's narration (edit 242)",
    "She smelled great, better than anyone he'd ever smelled before": "CT's (edit 242)",
    "\"The soup was good,\" he said.": "older text",
    "a thermos of something that smelled like a wet lawn": "older text",
    "Grace got the tart kind with mochi and gummy bears on top and ate it on the sidewalk": "Claude's (edit 201); \"I want frozen yogurt\" is CT's",
    "the one that smelled like petrichor and moss when it rained": "CT's (edit 238)",
    "She smells better than anyone I've ever known. And she doesn't even wear deodorant.": "CT's (edit 242)",
    "sage and turkey fat, and the little room filled with it the minute the door shut": "Claude's (edit 206); CT's \"Rosa's cooking\" and \"the heavenly scent\" drafted, not logged",
    "onions and bacon fat riding the wind out of the kitchen trailer": "Claude's (edit 207)",
    "The county chambers smelled like wet coats and floor wax.": "older text",
    "The seed house was warm and smelled like wet soil.": "older text",
    "The tea tasted like dirt and ginger.": "older text",
    "He could still taste the tea.": "older text",
    "The smell had climbed the kitchen walls and gotten into the curtains": "Claude's (edit 221)",
}
SENSE_CALL = {23: "Logged, edit 236 (the party)", 39: "Logged, edit 235 (the truck)"}


def senses(book, outdir, date):
    b = Book(book, outdir)
    sheet = {int(r[0]): r for r in list(csv.reader(open(os.path.join(outdir, "scene-sheet-2026-11-27.csv"))))[1:] if r[-1] != "(cut)"}
    data = {s["scene"]: s for s in json.load(open(os.path.join(outdir, "senses-data-2026-11-27.json")))}
    if set(data) != {s[0] for s in b.scenes}:
        sys.exit("senses-data does not cover the book's scenes: a scene was added, cut or merged. Read the new scenes and fix the data.")
    rows, lines, whose = [], 0, []
    for no, head, first, last in b.scenes:
        s, body = data[no], [norm(l) for l in b.lines[first:last + 1]]
        cells = []
        for k in ("sound", "touch", "smell", "taste", "sight", "food_or_drink_not_tasted"):
            got = []
            for q in s[k]:
                hit = [i for i, l in enumerate(body) if norm(q) in l]
                if not hit:
                    sys.exit(f"NO LONGER IN SCENE {no} ({k}): {q!r}. An edit changed it: reread the scene and fix the data.")
                got.append(f"line {first + hit[0] + 1}: \"{q}\"")
                lines += 1
                if k in ("smell", "taste"):
                    if q not in SENSE_WHOSE:
                        sys.exit(f"WHOSE WORDS NOT TRACED: {q!r}. Trace it (whose_words.py, then the record) and add it to SENSE_WHOSE.")
                    whose.append(f"\"{q[:40]}...\": {SENSE_WHOSE[q]}")
            cells.append(" | ".join(got))
        w = [f"{q[:40]}...: {SENSE_WHOSE[q]}" for q in s["smell"] + s["taste"]]
        rows.append([no, head.split(":")[0], sheet[no][10]] + cells + ["; ".join(w), SENSE_CALL.get(no, "")])
    write_csv(outdir, "senses", date, ["#", "Chapter", "What happens (scene sheet)", "Sound", "Touch", "Smell", "Taste",
              "Sight (the strongest)", "Eaten or drunk, no taste given", "Smell and taste: whose words", "CT's call"], rows)
    n = lambda k: sum(1 for s in data.values() if s[k])
    print(f"{len(rows)} scenes, {lines} lines found in the book; scenes with sound {n('sound')}, touch {n('touch')}, "
          f"smell {n('smell')}, taste {n('taste')}; food with no taste in {n('food_or_drink_not_tasted')}")

if __name__ == "__main__":
    cmds = {"calendar": calendar, "conversations": conversations, "desires": desires, "conversations2": conversations2, "money": money, "objects": objects, "plants": plants, "senses": senses}
    if len(sys.argv) < 4 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else "2026-11-27"
    cmds[sys.argv[1]](sys.argv[2], sys.argv[3], date)
