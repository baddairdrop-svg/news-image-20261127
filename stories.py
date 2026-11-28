# Story data for news-image-20261127 — FOCUSED REBUILD (36 stories).
#
# Selection: the strongest stories from the FINAL verified pool
# for Friday 27 November 2026 (102 unique verified stories in
# the research database after the Saturday closing sweep; every
# story happened or was first reported that day in some time
# zone, verified against its named source before any design).
# No story outside that pool is used. Items that only LOOK like
# 27 November news are listed in DATECHECK with their real
# dates. All times UTC. Local dates are named where they differ.
# Intraday market snapshots use closing numbers where the
# closing sweep superseded them (oil, gold, crypto, indices).
#
# This focused rebuild (Bedill's order 2026-11-28 17:18 WIB)
# follows the STRUCTURE and visual quality of a competitor
# reference Bedill supplied (big masthead, region chips, UTC
# timeline strip, 3 large pictorial heroes, pictorial grid,
# "day in numbers" panel, numbered ALSO list, numbered-pin
# map, honest DATE CHECK) — with 100% own code, art and text,
# and stories ONLY from our verified database. It cuts the
# submitted 58-story entry to 36 stronger stories: 3 heroes +
# 12 grid cards + 21 ALSO lines. A new submission would
# permanently replace the counted 58-story entry, so this
# rebuild stops at SIAP SUBMIT until Bedill orders otherwise.
#
# Regions are split finely (13 slots; all 13 carry stories):
# 0 North America, 1 South America, 2 North Europe,
# 3 West Europe, 4 East Europe, 5 Middle East, 6 Africa,
# 7 South Asia, 8 Southeast Asia, 9 East Asia, 10 Oceania,
# 11 Global, 12 Space.
#
# Story tuple: (kind, art, place, category, headline, summary,
#               source, region, field, confidence, chip, pin)
# kind: "hero" | "grid" | "also"; pin: (lon, lat) or None.

STORIES = [
    ("hero", "ballot", "WELLINGTON", "POLITICS",
     "New Zealand election ends in deadlock",
     "Final count declared Friday: right bloc 65 seats, left 58; "
     "Opportunity's 7 seats hold the balance.",
     "ELECTIONS NZ · AP", 10, "Politics", "OFFICIAL", "65 · 58 · 7",
     (174.8, -41.3)),
    ("hero", "rocket", "MAHIA, NEW ZEALAND", "SPACE",
     "Electron lifts off on night launch",
     "Rocket Lab's 101st Electron put the StriX-14 radar "
     "satellite into a 569 km orbit.",
     "ROCKET LAB · SPACEFLIGHT NOW", 12, "Space", "CONFIRMED",
     "00:15 UTC", (177.9, -39.3)),
    ("hero", "jets", "TAIPEI", "DEFENCE",
     "Taiwan votes as Chinese jets circle",
     "Final campaign day in Taiwan; 30 Chinese military "
     "aircraft tracked, 26 crossed the median line.",
     "REUTERS · MND", 9, "Defence", "REPORTED", "30 AIRCRAFT",
     (121.6, 25.0)),

    ("grid", "prices", "TOKYO", "ECONOMY",
     "Tokyo inflation hits 16-month high",
     "Core prices +2.9% in November.",
     "REUTERS", 9, "Economy", "REPORTED", "+2.9%", (139.7, 35.7)),
    ("grid", "tanker", "CANBERRA", "ENERGY",
     "Australia reserves 20% of LNG for home",
     "Domestic gas reservation passed, from 2028.",
     "REUTERS", 10, "Energy", "OFFICIAL", "FROM 2028",
     (149.1, -35.3)),
    ("grid", "fire", "BANGKOK", "DISASTER",
     "Fire sweeps Bangkok market at dawn",
     "Pattavikorn Market ablaze before dawn; out 06:27.",
     "NATION THAILAND", 8, "Disaster", "REPORTED", "OUT 06:27",
     (100.5, 13.8)),
    ("grid", "court", "MANILA", "LAW",
     "Duterte trial opens Monday at ICC",
     "Former president's trial starts 30 Nov.",
     "REUTERS", 8, "Law", "REPORTED", "MON 30 NOV",
     (121.0, 14.6)),
    ("grid", "tube", "LONDON", "LABOUR",
     "Tube strike shuts two lines till midday",
     "Ended 11:59; recovery expected by 18:00.",
     "THE TIMES · TFL", 2, "Labour", "REPORTED", "TILL 12:00",
     (-0.12, 51.5)),
    ("grid", "ferry", "HONG KONG", "TRANSPORT",
     "Ferry hits dock, 24 injured",
     "Ferry struck a pier off Tsing Yi at 01:21 UTC.",
     "XINHUA", 9, "Transport", "REPORTED", "24 INJURED",
     (114.1, 22.3)),
    ("grid", "flags", "NEW DELHI", "DIPLOMACY",
     "India hosts Indian Ocean summit",
     "25th IORA Council adopted the Delhi Communiqué.",
     "IANS", 7, "Diplomacy", "REPORTED", "25TH IORA",
     (77.2, 28.6)),
    ("grid", "shoppers", "NEW YORK", "ECONOMY",
     "Black Friday opens $1tn season",
     "Footfall −2% midday; $12.9bn online forecast.",
     "REUTERS · PASSBY", 0, "Economy", "REPORTED", "FORECAST",
     (-74.0, 40.7)),
    ("grid", "stars", "BRUSSELS", "DIPLOMACY",
     "EU leaders scrap Friday session",
     "Session cancelled; €45bn loan slips to 17 Dec.",
     "EURONEWS · CONSILIUM", 3, "Diplomacy", "CONFIRMED",
     "TO 17 DEC", (4.4, 50.8)),
    ("grid", "f1car", "LUSAIL", "SPORT",
     "Antonelli fastest in both Qatar sessions",
     "FP1 1:23.217, FP2 1:23.077; Russell P2 both.",
     "PIRELLI · CRASH.NET", 5, "Sport", "CONFIRMED", "FP1 + FP2",
     (51.5, 25.5)),
    ("grid", "chart", "NEW YORK", "MARKETS",
     "Wall Street rallies in half-day session",
     "Dow 50,780.64 (+1.19%); Nasdaq +2.31%.",
     "REUTERS", 0, "Markets", "REPORTED", "DOW 50,781",
     (-74.0, 40.7)),
    ("grid", "prices", "MADRID", "ECONOMY",
     "Spain inflation 4.1% in flash reading",
     "CPI 4.1% year on year; core 2.6%, INE said Friday.",
     "INE", 3, "Economy", "OFFICIAL", "4.1%", (-3.7, 40.4)),

    ("also", "", "MELBOURNE", "SPORT",
     "Australia 84–67 Iran: qualify for 2027 World Cup, 9–0",
     "", "FIBA · BASKETBALL AUS", 10, "Sport", "CONFIRMED", "",
     (145.0, -37.8)),
    ("also", "", "NEW DELHI", "POLITICS",
     "India Cabinet approves delimitation, women's-quota bill",
     "", "REUTERS", 7, "Politics", "REPORTED", "", (77.2, 28.6)),
    ("also", "", "ANKARA", "DIPLOMACY",
     "Erdoğan completes Turkey's ratification of Mecca pact",
     "", "REUTERS", 5, "Diplomacy", "OFFICIAL", "", (32.9, 39.9)),
    ("also", "", "SEOUL", "DIPLOMACY",
     "South Korea repatriates 6 North Koreans; one stays",
     "", "REUTERS", 9, "Diplomacy", "REPORTED", "", (127.0, 37.5)),
    ("also", "", "HANOI", "TRADE",
     "CPTPP opens accession talks with UAE, Indonesia, Philippines",
     "", "REUTERS", 8, "Trade", "REPORTED", "", (105.8, 21.0)),
    ("also", "", "PARIS", "ECONOMY",
     "France CPI 2.9% in November; Q3 GDP revised to −0.2%",
     "", "INSEE", 3, "Economy", "OFFICIAL", "", (2.35, 48.9)),
    ("also", "", "BERLIN", "ECONOMY",
     "Germany jobless +9k to 3.025m; rate steady at 6.4%",
     "", "BA", 3, "Economy", "OFFICIAL", "", (13.4, 52.5)),
    ("also", "", "WARSAW", "TECH",
     "Poland signs ~$300m Palantir defence deal, 5 years",
     "", "REUTERS", 4, "Tech", "REPORTED", "", (21.0, 52.2)),
    ("also", "", "JOHANNESBURG", "HEALTH",
     "Constitutional Court dismisses both NHI challenges",
     "", "BUSINESSDAY", 6, "Health", "REPORTED", "", (28.0, -26.2)),
    ("also", "", "GAZA", "CONFLICT",
     "Friday strikes kill 5, hospitals say; IDF targeted militants",
     "", "AP", 5, "Conflict", "REPORTED", "", (34.4, 31.5)),
    ("also", "", "TAIYUAN", "SPACE",
     "Long March 6A launches Yaogan-50 04 successfully",
     "", "XINHUA", 12, "Space", "OFFICIAL", "", (112.5, 37.9)),
    ("also", "", "BEIJING", "ECONOMY",
     "China industrial profits +20.1% in October (NBS, Friday)",
     "", "NBS", 9, "Economy", "OFFICIAL", "", (116.4, 39.9)),
    ("also", "", "PITTSBURGH", "SPORT",
     "Steelers beat Broncos 27–5 in Friday night game",
     "", "REUTERS", 0, "Sport", "REPORTED", "", (-80.0, 40.4)),
    ("also", "", "BRASÍLIA", "POLITICS",
     "Lula taps Trabuco; confirmed Friday as markets rally",
     "", "REUTERS", 1, "Politics", "REPORTED", "", (-47.9, -15.8)),
    ("also", "", "OTTAWA", "LAW",
     "Top court largely upholds Quebec Bill 21 (2026 SCC 41)",
     "", "SUPREME COURT OF CANADA", 0, "Law", "OFFICIAL", "",
     (-75.7, 45.4)),
    ("also", "", "ISLAMABAD", "DEFENCE",
     "Pakistan hosts Makkah Defence Alliance talks, 27–28 Nov",
     "", "GNP", 7, "Defence", "REPORTED", "", (73.1, 33.7)),
    ("also", "", "BEIJING", "LAW",
     "Ex-Guangxi chief Lan Tianli gets suspended death sentence",
     "", "REUTERS · XINHUA", 9, "Law", "REPORTED", "",
     (116.4, 39.9)),
    ("also", "", "SPACE", "SPACE",
     "Asteroid 2026 WU1 passed safely, 12.5 lunar distances away",
     "", "ESA NEO", 12, "Space", "OFFICIAL", "", None),
    ("also", "", "WORLD", "TECH",
     "DeepSeek tests per-turn cost display, first reported Friday",
     "", "REUTERS", 11, "Tech", "REPORTED", "", None),
    ("also", "", "FUJIAN", "DEFENCE",
     "China landing drill with floating bridge still under way",
     "", "REUTERS", 9, "Defence", "REPORTED", "", (119.3, 26.1)),
    ("also", "", "LONDON", "BUSINESS",
     "European CEO sentiment at two-year high (47 vs 40)",
     "", "REUTERS SURVEY", 2, "Business", "REPORTED", "",
     (-0.12, 51.5)),
]

# The day in numbers — verified closing figures for Friday
# 27 November 2026 (Reuters market reports; Bitcoin per
# CoinDesk at 18:00 UTC). Shown as figures, not counted as
# stories.
NUMBERS = [
    ("50,780.64", "DOW JONES CLOSE · +1.19%"),
    ("+2.31%", "NASDAQ CLOSE"),
    ("$95.44", "BRENT CRUDE SETTLE"),
    ("$3,653", "GOLD · +2.5%"),
    ("$59,861", "BITCOIN · 18:00 UTC"),
    ("+1.1%", "STOXX 600 CLOSE"),
]

# The day in UTC — anchor moments shown on the timeline strip.
TIMELINE = [
    ("00:15", "Electron launch"),
    ("01:21", "HK ferry crash"),
    ("06:19", "IORA opens"),
    ("07:00", "NZ count final"),
    ("12:00", "Tube strike ends"),
    ("13:05", "Long March 6A"),
    ("17:00", "F1 FP2 Qatar"),
    ("18:00", "Wall St close"),
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
]
