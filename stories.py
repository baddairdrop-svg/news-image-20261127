# Story data for news-image-20261127.
#
# Selection: the strongest stories from the verified pool for
# Friday 27 November 2026 (every story happened or was first
# reported that day in some time zone, verified against its named
# source in the research database before any design began).
# No story outside that pool is used. Items that only LOOK like
# 27 November news are listed in DATECHECK with their real dates.
# All times UTC. Local dates are named where they differ.
#
# Flexible slots: this file is the single edit point for the
# Saturday closing sweep — evening stories (F1 Qatar, Wall Street
# close, Friday-night sport, CPI prints) swap into grid/also
# slots here and the page re-renders with no code change.
#
# Regions are split finely (11 slots; 10 carry stories today):
# 0 North America, 1 South America, 2 West Europe, 3 East Europe,
# 4 Middle East, 5 Africa, 6 South Asia, 7 Southeast Asia,
# 8 East Asia, 9 Oceania, 10 Global.
#
# Story tuple: (kind, art, place, category, headline, summary,
#               source, region, field, confidence, chip, pin)
# kind: "hero" | "grid" | "also"; pin: (lon, lat) or None.

STORIES = [
    ("hero", "ballot", "WELLINGTON", "POLITICS",
     "New Zealand election ends in deadlock",
     "Final count declared Friday: right bloc 65 seats, left 58; "
     "Opportunity's 7 seats hold the balance.",
     "ELECTIONS NZ · AP", 9, "Politics", "OFFICIAL", "65 · 58 · 7",
     (174.8, -41.3)),
    ("hero", "rocket", "MAHIA, NEW ZEALAND", "SPACE",
     "Electron lifts off on night launch",
     "Rocket Lab's 101st Electron put the StriX-14 radar "
     "satellite into a 569 km orbit.",
     "ROCKET LAB · SPACEFLIGHT NOW", 10, "Space", "CONFIRMED",
     "00:15 UTC", (177.9, -39.3)),
    ("hero", "jets", "TAIPEI", "DEFENCE",
     "Taiwan votes as Chinese jets circle",
     "Final campaign day in Taiwan; 26 Chinese military "
     "aircraft were tracked around the island Friday.",
     "REUTERS · MND", 8, "Defence", "REPORTED", "26 AIRCRAFT",
     (121.6, 25.0)),

    ("grid", "prices", "TOKYO", "ECONOMY",
     "Tokyo inflation hits 16-month high",
     "Core prices +2.9% in November; a Bank of Japan "
     "rate rise is now expected.",
     "REUTERS", 8, "Economy", "REPORTED", "+2.9%", (139.7, 35.7)),
    ("grid", "tanker", "CANBERRA", "ENERGY",
     "Australia reserves 20% of LNG for home",
     "Domestic gas reservation passed, from 2028.",
     "REUTERS", 9, "Energy", "OFFICIAL", "FROM 2028",
     (149.1, -35.3)),
    ("grid", "fire", "BANGKOK", "DISASTER",
     "Fire sweeps Bangkok market at dawn",
     "Pattavikorn Market ablaze before dawn; out 06:27.",
     "NATION THAILAND", 7, "Disaster", "REPORTED", "OUT 06:27",
     (100.5, 13.8)),
    ("grid", "court", "MANILA", "LAW",
     "Duterte trial opens Monday at ICC",
     "Victims' families travelled to The Hague; the "
     "former president's trial starts 30 Nov.",
     "REUTERS", 7, "Law", "REPORTED", "MON 30 NOV",
     (121.0, 14.6)),
    ("grid", "fence", "SEOUL", "DEFENCE",
     "North Korean troops crossed line ~40 times",
     "Joint Chiefs data on crossings since October.",
     "JOONGANG DAILY", 8, "Defence", "CLAIM", "~40 TIMES",
     (127.0, 37.5)),
    ("grid", "tube", "LONDON", "LABOUR",
     "Tube strike shuts two lines till midday",
     "RMT walkout; two lines shut until noon.",
     "THE TIMES", 2, "Labour", "REPORTED", "TILL 12:00",
     (-0.12, 51.5)),
    ("grid", "car", "LONDON", "INDUSTRY",
     "UK car output jumps 4.8%",
     "Factories built 64,141 vehicles in October, "
     "SMMT said Friday; exports +14.2%.",
     "REUTERS · SMMT", 2, "Industry", "OFFICIAL", "+4.8%",
     (-0.12, 51.5)),
    ("grid", "vote", "TOKYO", "POLITICS",
     "Censure of minister fails by 4 votes",
     "Upper house rejected the motion against "
     "Minister Seki by 124 votes to 120.",
     "TBS", 8, "Politics", "REPORTED", "124–120",
     (139.7, 35.7)),
    ("grid", "ferry", "HONG KONG", "TRANSPORT",
     "Ferry hits dock, 24 injured",
     "A ferry struck a pier off Tsing Yi at "
     "01:21 UTC; 24 passengers hurt.",
     "XINHUA", 8, "Transport", "REPORTED", "24 INJURED",
     (114.1, 22.3)),
    ("grid", "flags", "NEW DELHI", "DIPLOMACY",
     "India hosts Indian Ocean summit",
     "The 25th IORA Council of Ministers met in New Delhi "
     "on Friday.",
     "IANS", 6, "Diplomacy", "REPORTED", "25TH IORA",
     (77.2, 28.6)),
    ("grid", "shoppers", "NEW YORK", "ECONOMY",
     "Black Friday opens $1tn season",
     "Shoppers queued at dawn; holiday sales are "
     "forecast above $1 trillion.",
     "REUTERS · AP", 0, "Economy", "REPORTED", "FORECAST",
     (-74.0, 40.7)),
    ("grid", "stars", "BRUSSELS", "DIPLOMACY",
     "EU leaders scrap Friday session",
     "Friday's session was cancelled; the €45bn "
     "Ukraine loan slips to 17 Dec.",
     "EURONEWS · CONSILIUM", 2, "Diplomacy", "CONFIRMED",
     "TO 17 DEC", (4.4, 50.8)),

    ("also", "", "CHRISTCHURCH", "SPORT",
     "NZ 246/5 at stumps, Day 1 of 2nd Test v India",
     "", "REUTERS", 9, "Sport", "REPORTED", "", (172.6, -43.5)),
    ("also", "", "TOKYO", "TECH",
     "JERA in talks with Anthropic and Meta on data centres",
     "", "NIKKEI VIA REUTERS", 8, "Tech", "CLAIM", "",
     (139.7, 35.7)),
    ("also", "", "ISLAMABAD", "DEFENCE",
     "Pakistan hosts Makkah Defence Alliance talks, 27–28 Nov",
     "", "GNP", 6, "Defence", "REPORTED", "", (73.1, 33.7)),
    ("also", "", "ANKARA", "DIPLOMACY",
     "Erdoğan completes Turkey's ratification of Mecca pact",
     "", "REUTERS", 4, "Diplomacy", "OFFICIAL", "", (32.9, 39.9)),
    ("also", "", "NEW DELHI", "POLITICS",
     "India Parliament to reconvene 30 Nov; Cabinet met Friday",
     "", "DAILY JAGRAN", 6, "Politics", "REPORTED", "",
     (77.2, 28.6)),
    ("also", "", "MANILA", "POLITICS",
     "Sara Duterte: resignation “out of the question”",
     "", "REUTERS", 7, "Politics", "REPORTED", "", (121.0, 14.6)),
    ("also", "", "SEOUL", "DIPLOMACY",
     "South Korea repatriates 6 North Koreans; one stays",
     "", "REUTERS", 8, "Diplomacy", "REPORTED", "", (127.0, 37.5)),
    ("also", "", "YOGYAKARTA", "LAW",
     "Daycare head jailed 9 years (verdict 26 Nov, reported Fri)",
     "", "REUTERS", 7, "Law", "REPORTED", "", (110.4, -7.8)),
    ("also", "", "FUJIAN", "DEFENCE",
     "China landing drill with floating bridge still under way",
     "", "REUTERS", 8, "Defence", "REPORTED", "", (119.3, 26.1)),
    ("also", "", "MELBOURNE", "POLITICS",
     "Victoria poll: conservatives lead 57.5–42.5 before vote",
     "", "NEWSPOLL VIA REUTERS", 9, "Politics", "REPORTED", "",
     (145.0, -37.8)),
    ("also", "", "KUALA LUMPUR", "CRIME",
     "6 charged over 96.2 kg meth haul at Subang",
     "", "SCOOP", 7, "Crime", "REPORTED", "", (101.7, 3.1)),
    ("also", "", "LONDON", "BUSINESS",
     "European CEO sentiment at two-year high (47 vs 40)",
     "", "REUTERS SURVEY", 2, "Business", "REPORTED", "",
     (-0.12, 51.5)),
    ("also", "", "MADRID", "POLITICS",
     "Spain's final campaign day; vote on Sunday 29 Nov",
     "", "EFE VIA REUTERS", 2, "Politics", "REPORTED", "",
     (-3.7, 40.4)),
    ("also", "", "WARSAW", "POLITICS",
     "Poland's conservatives face KKP dilemma (analysis)",
     "", "REUTERS", 3, "Politics", "REPORTED", "", (21.0, 52.2)),
    ("also", "", "NAIROBI", "POLITICS",
     "Senator Sifuna calls President Ruto an “existential threat”",
     "", "PEOPLE DAILY", 5, "Politics", "REPORTED", "",
     (36.8, -1.3)),
    ("also", "", "SPACE", "SPACE",
     "Asteroid 2026 WU1 passed safely, 12.5 lunar distances away",
     "", "ESA NEO", 10, "Space", "OFFICIAL", "", None),
    ("also", "", "GENEVA", "RIGHTS",
     "UN Minority Forum held its second day of panels",
     "", "OHCHR", 10, "Rights", "OFFICIAL", "", (6.1, 46.2)),
    ("also", "", "WORLD", "RIGHTS",
     "First International Day to Eliminate Child Marriage observed",
     "", "UN · PLAN", 10, "Rights", "OFFICIAL", "", None),
    ("also", "", "WORLD", "MARKETS",
     "Stocks rose: Nikkei +2.1%, China +3.8%, Nasdaq fut. +2.4%",
     "", "REUTERS", 10, "Markets", "REPORTED", "", None),
    ("also", "", "SINGAPORE", "ENERGY",
     "Oil near November highs; first weekly gain in four",
     "", "REUTERS", 10, "Energy", "REPORTED", "", (103.8, 1.35)),
    ("also", "", "WORLD", "MARKETS",
     "Bitcoin ~$61.5k as $7bn of options expired Friday",
     "", "COINDESK", 10, "Markets", "REPORTED", "", None),
    ("also", "", "WORLD", "MARKETS",
     "Gold $3,650 (+2.3%) and silver $44.07 (+6.2%) rebounded",
     "", "REUTERS", 10, "Markets", "REPORTED", "", None),
    ("also", "", "BEIJING", "ECONOMY",
     "China industrial profits +20.1% in October (NBS, Friday)",
     "", "NBS", 8, "Economy", "OFFICIAL", "", (116.4, 39.9)),
    ("also", "", "BANGKOK", "WEATHER",
     "Thailand issued heavy-rain advisory for 27–30 Nov",
     "", "TMD", 7, "Weather", "REPORTED", "", (100.5, 13.8)),
    ("also", "", "WORLD", "TECH",
     "AI briefing: DeepSeek and Mistral updates reported Friday",
     "", "REUTERS", 10, "Tech", "REPORTED", "", None),
    ("also", "", "LONDON", "MARKETS",
     "Europe futures +0.7%; SAP and tobacco results in focus",
     "", "REUTERS", 2, "Markets", "REPORTED", "", (-0.12, 51.5)),
    ("also", "", "WORLD", "SCIENCE",
     "Friday journals: cancer-cell, landslide and livestock papers",
     "", "SCIENTIFIC REPORTS", 10, "Science", "REPORTED", "",
     None),
]

# The day in UTC — anchor moments shown on the timeline strip.
TIMELINE = [
    ("00:06", "UK car data"),
    ("00:15", "Electron launch"),
    ("01:21", "HK ferry crash"),
    ("02:59", "India Cabinet call"),
    ("04:32", "Asteroid passes"),
    ("06:19", "IORA opens"),
    ("07:00", "NZ count final"),
    ("12:00", "Tube strike ends"),
]

# Stories that look like 27 November news but are not, with
# their real dates. Shown honestly, never counted as today.
DATECHECK = [
    "EU budget summit collapse — Thu 26 Nov",
    "Kyiv missiles wound 7 — night of 25–26 Nov",
    "Gaza strikes kill 9 — Thu 26 Nov",
    "Two Italians killed in Kuwait — Thu 26 Nov",
    "Hormuz tanker mine claims — Thu 26 Nov",
    "Cairo tanker fire kills 31 — Wed 25 Nov",
    "Thanksgiving storm, ~961k without power — 25–26 Nov",
    "Zaporizhzhia loses offsite power (28th) — 25 Nov",
    "Guinea-Bissau vote moved to 2028 — Thu 26 Nov",
    "DRC Ebola passes 12,000 cases — Thu 26 Nov data",
]
