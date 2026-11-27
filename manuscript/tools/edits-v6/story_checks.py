#!/usr/bin/env python3
"""Story checks: sheets that test the book against itself. Built from the page, like knowledge.py.

    python3 manuscript/tools/edits-v6/story_checks.py calendar OUT/v6.txt OUTDIR [--date 2026-11-27]

calendar  Every scene on a date, every time word the scene holds, and a list of checks a calendar can
          settle (weekdays, intervals, ages). Writes calendar-DATE.csv and calendar-checks-DATE.csv.
          WHEN below is the only hand-written part: one line per scene, "n|sort|when|how". "how" is
          stated (the page gives it), worked (worked out from other scenes) or back (back story).
          CHECKS quotes the lines each check rests on; a quote that is not in the book stops the run.

(money, objects, plants and senses are to come; CT asked for all five on 27 Nov 2026.)
"""
import csv
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_sheet  # noqa: E402

NUM = r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|a|an|\d+)"
TIME = re.compile(r"(?i)\b(20[12]\d|January|February|March|April|May\b(?! be)|June|July|August|September|October|November|December|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|spring|summer|fall\b|winter|Thanksgiving|Christmas|midterms|" + NUM + r"[ -](?:days?|weeks?|months?|years?)\b(?: (?:ago|later|after|before|back|old|out))?|thirty-\w+ years old|first of the month)")

WHEN = """
1|2022-11-08|November 2022, the night he shows the realtors|worked
2|1990|Back story: the farm, his father, the band, 2020, Claypot|back
3|2022-10|Fall 2022: Chat Horizon goes public; the month nobody listens|worked
4|2022-11-08|The same night: the realtors, the napkin|worked
5|2022-11-15|A week later, a Tuesday: the toast|stated
6|2022-11-15|That night, 1:40 a.m.|stated
7|2022-11-21|The Monday after the toast: the bet|stated
8|2022-11-21|The same Monday, at the Bear Flag|stated
9|2022-11-21|That night: the tower|stated
10|2023-02|Early 2023, a Thursday: the all-hands|worked
11|2023-02|The same morning|stated
12|2023-02|That night|stated
13|2023-02|The same day, in the air|worked
14|2023-03|Three weeks after the all-hands|stated
15|2023-03|A Sunday, 9:40|stated
16|2023-03|A Friday and Saturday|stated
17|2023-04|The next Monday and the week after: the bill|stated
18|2023-04|A Wednesday|stated
19|2023-04|That weekend|stated
20|2023-10-17|October 2023, a Tuesday, eleven months after the toast: laid off|stated
21|2023-10-17|The same day: the video|stated
22|2023-10-18|That night and the next morning|stated
23|2023-10-20|October to December 2023: the replies|stated
24|2023-12|A Sunday, 9:55|stated
25|2024-01|A Thursday in January 2024|stated
26|2024-01|The same night, in the truck|stated
27|2024-02|February 2024: San Francisco|stated
28|2024-02|The same afternoon|stated
29|2024-02|That night: the house on the hill|stated
30|2024-02|The same night|stated
31|2024-02|The same night, until two|stated
32|2024-02|After two in the morning|stated
33|2024-02|The same night|worked
34|2024-03|Spring to August 2024: the apartment goes in April, a month at Ma's, the cannery|stated
35|2024-08-09|August 2024, six in the morning: the ride with Gus|worked
36|2024-08-09|The same morning|stated
37|2024-08-12|Three weeks in August 2024; the launch party is the third Friday|stated
38|2024-08-31|The morning after, to Monday; the stroke is Sunday night|stated
39|2024-09-02|That Monday: the hospital|stated
40|2024-09-03|That week: the house|worked
41|2024-09-04|That week: the two pages|worked
42|2024-09-04|That week|worked
43|2024-09-05|That week: he asks online|worked
44|2024-09-06|The man from Sacramento; the signing; the wire clears on a Friday|stated
45|2024-09-11|Two days before the wire, a Wednesday|stated
46|2024-09-12|The next morning (Thursday), and Friday morning|stated
47|2024-09-13|That Friday night: the first rain since April|stated
48|2024-09-14|Five months, September 2024 to the last week of February 2025 (Tuesday to Friday)|stated
49|2025-03-01|Saturday 1 March to Monday 3 March 2025; he drives north|worked
50|2025-03-04|Tuesday 4 March 2025: the broom|worked
51|2025-03-04|The same evening|stated
52|2025-03-05|His first days: the fourth day is Friday 7 March; Praether; the arms come Wednesday 12 March|worked
53|2025-03-12|March 2025: the barn; his first Sundays|worked
54|2025-03-28|Friday 28 March 2025, three weeks after the broom: his first dinner|worked
55|2025-03-28|The same dinner|stated
56|2025-03-30|That Sunday|stated
57|2025-03-30|The same day|stated
58|2025-04-01|The following Tuesday|stated
59|2025-04-24|Late April 2025, Thursday to Monday, seven weeks after the broom|stated
60|2025-04-01|Earlier that April, to May: the order, the two designs|stated
61|2025-05-03|The first build weekend|worked
62|2025-05-10|The second build weekend|stated
63|2025-05-20|May 2025: the boxes ship|stated
64|2025-05-12|May 2025: the drip tape|stated
65|2025-06-09|June 2025 (the second week): the two videos|stated
66|2025-06-26|The last week of June 2025: a hundred and four|stated
67|2025-05-30|The end of May to early July 2025: the servers|stated
68|2025-07-03|Thursday 3 July to Saturday 5 July 2025: Ray, the leak|worked
69|2025-07-05|That Saturday morning|stated
70|2025-07-05|That weekend, to Monday|stated
71|2025-07-15|July and August 2025: the land trust|worked
72|2025-08|Summer 2025|worked
73|2025-08-15|The middle of August 2025|stated
74|2025-08-25|The last week of August into September 2025: the shouse|stated
75|2025-09-27|Saturday 27 September 2025: the first fire; Sunday the call|stated
76|2025-10-05|The next Sunday|stated
77|2025-09-27|The same night, by eleven|stated
78|2025-03|Spring to fall 2025: the store dies|stated
79|2025-10-15|Fall 2025, after the first frost: the letter, the frozen yogurt|stated
80|2025-10-17|A Friday dinner|stated
81|2025-10-25|Fall 2025: the cyberdeck|worked
82|2025-11-12|The second week of November 2025: the pond|stated
83|2025-11-26|Wednesday 26 November 2025: he starts for home and turns back|stated
84|2025-11-26|That night|stated
85|2026-03|Spring 2026: the beds|stated
86|2026-05|May 2026: the rover|stated
87|2026-05|Two nights later|stated
88|2026-06-12|Friday 12 June to 30 June 2026: the models go dark|stated
89|2025-11-28|The Friday after Thanksgiving 2025 to July 2026: the pay|stated
90|2026-08|August to October 2026: the pits|stated
91|2026-10|October 2026: the laser weeder; Marta|stated
92|2026-10|The night after: the amp at the pond|stated
93|2026-10|October 2026: the first fire video; a week later|worked
94|2026-10|The same morning, and that Friday|stated
95|2026-10|To Friday 6 November 2026, after the midterms|stated
96|2026-11-20|Friday 20 November 2026; Thanksgiving is the 26th|stated
97|2026-12-05|Saturday 5 December 2026: the well|stated
98|2026-12-15|December 2026: the storm|stated
99|2027-01|January 2027: the grange kitchen|stated
100|2027-01|January 2027: the annual meeting|worked
101|2027-01|A few nights after|stated
102|2027-02|The night before the county meeting|stated
103|2027-02|The county meeting|worked
104|2027-02|The third week of the apprenticeship|stated
105|2027-02-12|February 2027, a Friday: the plan|stated
106|2027-02-15|The Monday after, and two days later|stated
107|2027-02-16|That week|stated
108|2027-02-20|Saturday 20 February 2027: the tea|worked
109|2027-02-21|Sunday 21 February: Marta, the brake|stated
110|2027-02-28|Sunday 28 February, Monday 1 March (the pit), and that Friday|worked
111|2027-03|March 2027, on the dairy|worked
112|2027-03|March 2027: five small things|stated
113|2027-03-28|Late March 2027|stated
114|2027-04-01|Thursday 1 April 2027 to the next Friday|stated
115|2027-04-10|April to June 2027: the juniper|stated
116|2027-06|June to Friday 9 July 2027|stated
117|2027-07-09|Friday dinner, 9 July 2027|worked
118|2027-07-09|The same evening|stated
119|2027-07-16|The next Friday|stated
120|2027-10-02|Early October 2027, a Saturday to Tuesday: the tractor|stated
121|2027-10-11|The afternoon before the October meeting|stated
122|2027-10-12|A Tuesday in the middle of October 2027: the meeting|stated
123|2027-10-12|The same night|stated
124|2027-10-13|Six the next morning|stated
125|2027-10-13|That night|stated
126|2027-10-23|The Saturday before the festival|stated
127|2027-10-27|The Wednesday of festival week|stated
128|2027-10-30|The last night of the festival: the fire|worked
129|2027-11-01|The week after; he packs on Tuesday 9 November 2027|worked
130|2027-11-09|The same Tuesday|stated
131|2027-11-09|The same Tuesday|stated
132|2027-11-09|Two days south; the rose garden; Manny's|stated
133|2027-11-25|Thursday 25 November 2027|stated
134|2027-11-23|Tuesday 23 to Thursday 25 November 2027|stated
135|2027-11-25|Thanksgiving night, the Bear Flag|stated
136|2027-11-25|The same night|stated
137|2027-12|December 2027 to April 2028|stated
"""
BACK_ON_PURPOSE = {2, 3, 45, 60, 64, 67, 77, 78, 89, 134}  # scenes the book tells out of order


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
    ("The laid-off video is four years before Thanksgiving 2027 and eleven months after the toast", ["Elijah got laid off on a Tuesday, eleven months after the toast.", "That's four years.", "She had watched it in October, the morning after he posted"],
     lambda: (True, "toast November 2022, layoff October 2023, four years and a month to November 2027")),
    ("The document was started 'fifteen months back' from February 2024", ["he'd started at 1:40 in the morning, fifteen months back"],
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


if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] != "calendar":
        sys.exit(__doc__)
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else "2026-11-27"
    calendar(sys.argv[2], sys.argv[3], date)
